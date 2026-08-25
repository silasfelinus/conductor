#!/usr/bin/env python3
"""
set_task_field.py — update one field on one roadmap task without reserializing YAML.

Usage:
    python scripts/set_task_field.py <project> <task-id> <field> <value>
    python scripts/set_task_field.py <project> <task-id> status done
    python scripts/set_task_field.py <project> <task-id> owner null
    python scripts/set_task_field.py <project> <task-id> updated now
    python scripts/set_task_field.py <project> <task-id> approved_by_human true --dry-run

This is intentionally line-oriented instead of yaml.safe_dump so agents can flip a single
roadmap task field without rewriting quoted strings, multiline notes, comments, or ordering.

WARNING -- local working tree only: unlike claim_task.py, this script never fetches or
reads from origin/main. It edits whatever projects/<project>/roadmap.yaml is already on
disk in the caller's checkout. If claim_task.py (or any other script that pushes straight
to origin/main) ran earlier in this same session, and this checkout was not independently
fetched/fast-forwarded afterward, a call here can silently overwrite that push with a
stale value from the local tree's old copy. Run `git fetch origin main && git merge
origin/main --ff-only` (or equivalent) immediately before calling this script whenever a
direct-to-origin/main push happened earlier in the session -- especially the common
claim-then-later-set-status sequence. (conductor/t-077, kaizen from davinci/t-014: this
exact sequence briefly clobbered a just-written claimed_by/claimed_at with a week-old
value.)

Multiline field values (folded `note: >` blocks, quoted notes spanning lines, and
`depends_on` block lists) are replaced as a whole; new fields are inserted at the end of
the task block so they can never land inside another field's value. Newlines in a new
value are flattened to spaces — the writer emits exactly one line per field — UNLESS the
field being replaced already exists as a block-literal scalar (`note: |-`, `note: >-`,
etc.) AND the new value itself contains embedded newlines. In that case the new value is
re-emitted in the same block style instead of being collapsed to a single quoted line,
preserving the hand-maintained per-paragraph-per-line convention used by long-running
`note:` fields (e.g. recurring tasks with one `RAN <date>: ...` paragraph per cycle).

If PyYAML is importable, the result is re-parsed after the edit and the write is refused
unless the document is valid YAML and the target task actually carries the field.

Destructive `note` replacement guard (conductor/t-129): `note:` is an append-only log in
practice across this repo's roadmaps -- a chain of `CORRECTION` / `RESOLVED` / `RAN <date>`
paragraphs, each preserving what it superseded. `--set field=value` substituting the whole
value is the right default for `status`, `owner`, and every other scalar field, but it is
the wrong default for `note`: doing `--set note='...'` on a task with substantial existing
note content silently deletes that history (conductor/t-033 lost 199 lines of diagnostic
record this way -- repaired in #2816, but the sharp edge was still live). If the existing
`note` exceeds `NOTE_REPLACE_GUARD_CHARS` and the new value does not still contain it,
`set_task_field_text`/the CLI refuse unless `force=True` / `--force` is passed. Use
`append_note_text()` (CLI: `close_task.py --append-note`) to add to the note instead of
replacing it outright.
"""

from __future__ import annotations

import argparse
import difflib
import pathlib
import re
import sys
import textwrap
from datetime import datetime, timezone

# `note:` fields longer than this are treated as substantial history -- replacing one
# outright (rather than appending) requires --force. See "Destructive `note` replacement
# guard" above.
NOTE_REPLACE_GUARD_CHARS = 300


PROJECTS_DIR = pathlib.Path("projects")
TASK_ID_RE = re.compile(r"^(?P<indent>\s*)-\s+id:\s*(?P<id>[^#\n]+?)\s*(?:#.*)?$")
KEY_RE = re.compile(r"^(?P<indent>\s*)(?P<key>[A-Za-z_][A-Za-z0-9_-]*):(?P<rest>.*)$")
BLOCK_STYLE_RE = re.compile(
    r"^(?P<indent>\s*)(?P<key>[A-Za-z_][A-Za-z0-9_-]*):\s*(?P<style>[|>][-+]?)\s*$"
)
ALLOWED_FIELDS = {
    "status",
    "owner",
    "updated",
    "passes",
    "stakes",
    "gate_human",
    "soft_gate",
    "approved_by_human",
    "depends_on",
    "note",
    "claimed_by",
    "claimed_at",
    "implementation_pr",
}
# Bare words YAML 1.1 parsers read as booleans; quote them so the value stays a string.
YAML11_BOOL_WORDS = {"yes", "no", "on", "off", "y", "n"}
# Bare scalars matching this also get parsed as native datetime/date objects by PyYAML's
# YAML 1.1 timestamp resolver; quote them too so a literal timestamp value (e.g. passed
# to `updated` or `claimed_at` instead of the `now` keyword) stays a plain string like
# every other timestamp field in the roadmaps.
TIMESTAMP_RE = re.compile(
    r"^\d{4}-\d\d-\d\d"
    r"([Tt ]\d\d:\d\d:\d\d(\.\d*)?\s*(Z|[-+]\d\d?(:\d\d)?)?)?$"
)


class TaskFieldError(Exception):
    pass


def normalize_scalar(value: str) -> str:
    raw = re.sub(r"\s*\n\s*", " ", value).strip()
    lowered = raw.lower()

    if lowered == "now":
        return datetime.now(timezone.utc).strftime("'%Y-%m-%dT%H:%M:%SZ'")
    if lowered in {"null", "none", "~"}:
        return "null"
    if lowered in {"true", "false"}:
        return lowered
    if re.fullmatch(r"-?\d+", raw):
        return raw
    if (
        lowered not in YAML11_BOOL_WORDS
        and not TIMESTAMP_RE.match(raw)
        and re.fullmatch(r"[A-Za-z0-9_.:/@+-]+", raw)
    ):
        return raw

    escaped = raw.replace("'", "''")
    return f"'{escaped}'"


def roadmap_path(project: str) -> pathlib.Path:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", project):
        raise TaskFieldError(f"Invalid project slug: {project!r}")
    return PROJECTS_DIR / project / "roadmap.yaml"


def line_indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def find_task_block(lines: list[str], task_id: str) -> tuple[int, int, int]:
    start = -1
    task_indent = 0

    for idx, line in enumerate(lines):
        match = TASK_ID_RE.match(line)
        if not match:
            continue
        found_id = match.group("id").strip().strip('"\'')
        if found_id == task_id:
            start = idx
            task_indent = len(match.group("indent"))
            break

    if start < 0:
        raise TaskFieldError(f"Task {task_id!r} not found")

    end = len(lines)
    for idx in range(start + 1, len(lines)):
        match = TASK_ID_RE.match(lines[idx])
        if match and len(match.group("indent")) == task_indent:
            end = idx
            break
        key_match = KEY_RE.match(lines[idx])
        if key_match and len(key_match.group("indent")) <= task_indent:
            # A mapping key at or above the task's own indent means the task
            # list ended (for example a new top-level section).
            end = idx
            break

    field_indent = task_indent + 2
    return start, end, field_indent


def field_value_end(lines: list[str], key_idx: int, block_end: int, field_indent: int) -> int:
    """Index one past the last line of the field's value block.

    Continuation lines are anything indented deeper than the key (folded/quoted
    scalars), blank lines inside the value, and block-list items (`- item`) at
    or below the key's own indent level, as `depends_on:` lists use.
    """
    idx = key_idx + 1
    while idx < block_end:
        line = lines[idx]
        stripped = line.strip()
        if not stripped:
            idx += 1
            continue
        indent = line_indent(line)
        if indent > field_indent:
            idx += 1
            continue
        if indent >= field_indent and stripped.startswith("- "):
            idx += 1
            continue
        break
    # Blank lines at the tail are separators between fields/tasks, not value.
    while idx > key_idx + 1 and not lines[idx - 1].strip():
        idx -= 1
    return idx


def existing_block_style(lines: list[str], key_idx: int) -> str | None:
    """Return the block-scalar indicator (`|-`, `>`, etc.) on a key line, if any."""
    match = BLOCK_STYLE_RE.match(lines[key_idx])
    return match.group("style") if match else None


def render_block_scalar(field: str, style: str, value: str, field_indent: int) -> list[str]:
    """Render `value` as a block-literal/folded scalar in the given style.

    Preserves blank lines (paragraph breaks) and does not escape or requote
    the content — block scalars carry their text as-is.
    """
    content_lines = value.split("\n")
    while content_lines and content_lines[0] == "":
        content_lines.pop(0)
    while content_lines and content_lines[-1] == "":
        content_lines.pop()

    content_indent = field_indent + 2
    rendered = [f"{' ' * field_indent}{field}: {style}\n"]
    for line in content_lines:
        if line.strip() == "":
            rendered.append("\n")
        else:
            rendered.append(f"{' ' * content_indent}{line}\n")
    return rendered


def _decode_scalar(raw: str) -> str:
    """Best-effort decode of a single-line flow scalar back to plain text.

    Handles the single-quoted form `normalize_scalar` writes ('' -> ') and, for
    robustness against hand-edited roadmaps, basic double-quoted escapes. A bare
    (unquoted) scalar is returned as-is.
    """
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] == "'":
        return raw[1:-1].replace("''", "'")
    if len(raw) >= 2 and raw[0] == raw[-1] == '"':
        return raw[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return raw


def _field_raw_value(lines: list[str], key_idx: int, value_end: int, field_indent: int) -> str:
    """Decode the current value of the field at `key_idx` back to plain text.

    Dedents and joins a block scalar's content lines (preserving blank-line
    paragraph breaks). A flow scalar (quoted or bare) can itself span several
    physical lines -- e.g. a single-quoted note with a blank line inside it --
    so this decodes the whole `key_idx:value_end` chunk with PyYAML when it's
    importable (dedented and re-keyed so it parses standalone), falling back to
    `_decode_scalar` on just the key line when PyYAML isn't available or the
    chunk doesn't parse.
    """
    style = existing_block_style(lines, key_idx)
    if style is not None:
        content_indent = field_indent + 2
        body: list[str] = []
        for line in lines[key_idx + 1 : value_end]:
            if line.strip() == "":
                body.append("")
            else:
                body.append(line[content_indent:].rstrip("\n"))
        return "\n".join(body).strip("\n")

    match = KEY_RE.match(lines[key_idx])
    key = match.group("key") if match else None

    if value_end > key_idx + 1 and key is not None:
        # A flow scalar spilling onto continuation lines -- dedent by field_indent
        # so the chunk parses as a standalone one-key mapping, then let PyYAML do
        # the actual folding/escape decoding rather than reimplementing it.
        chunk = "".join(
            line[field_indent:] if line.startswith(" " * field_indent) else line
            for line in lines[key_idx:value_end]
        )
        try:
            import yaml

            parsed = yaml.safe_load(chunk)
        except Exception:
            parsed = None
        if isinstance(parsed, dict) and key in parsed and isinstance(parsed[key], str):
            return parsed[key]

    rest = match.group("rest") if match else ""
    return _decode_scalar(rest)


def get_task_field_value(text: str, task_id: str, field: str) -> str | None:
    """Return the current decoded value of `field` on `task_id`, or None if absent."""
    lines = text.splitlines(keepends=True)
    start, end, field_indent = find_task_block(lines, task_id)
    for idx in range(start + 1, end):
        match = KEY_RE.match(lines[idx])
        if not match:
            continue
        if len(match.group("indent")) != field_indent or match.group("key") != field:
            continue
        value_end = field_value_end(lines, idx, end, field_indent)
        return _field_raw_value(lines, idx, value_end, field_indent)
    return None


def append_note_text(text: str, task_id: str, addition: str, *, width: int = 88) -> str:
    """Append `addition` as a new paragraph on `task_id`'s `note`, instead of
    replacing it (conductor/t-129). Always renders the result as a `note: >-`
    folded block (chomping indicator `-` so re-parsing doesn't pick up a stray
    trailing newline), regardless of the note's prior style, since an
    append-only log is the point.
    """
    addition = addition.strip()
    if not addition:
        raise TaskFieldError("Cannot append an empty note")

    existing = get_task_field_value(text, task_id, "note")
    wrapped = addition if "\n" in addition else textwrap.fill(addition, width=width)
    if existing and existing.strip():
        combined = f"{existing.rstrip(chr(10))}\n\n{wrapped}"
    else:
        combined = wrapped

    # combined always contains the prior note as a prefix, so the destructive-
    # replace guard below would never fire here anyway -- force=True just skips
    # the (redundant) substring check.
    return set_task_field_text(text, task_id, "note", combined, force=True, force_block=">-")


def set_task_field_text(
    text: str,
    task_id: str,
    field: str,
    value: str,
    *,
    force: bool = False,
    force_block: str | None = None,
) -> str:
    if field not in ALLOWED_FIELDS:
        allowed = ", ".join(sorted(ALLOWED_FIELDS))
        raise TaskFieldError(f"Field {field!r} is not allowed. Allowed fields: {allowed}")

    lines = text.splitlines(keepends=True)
    if not lines:
        raise TaskFieldError("Roadmap is empty")

    start, end, field_indent = find_task_block(lines, task_id)

    found_field_idx: int | None = None
    for idx in range(start + 1, end):
        match = KEY_RE.match(lines[idx])
        if not match:
            continue
        if len(match.group("indent")) != field_indent:
            continue
        if match.group("key") == field:
            found_field_idx = idx
            break

    if field == "note" and found_field_idx is not None and not force:
        value_end = field_value_end(lines, found_field_idx, end, field_indent)
        existing_raw = _field_raw_value(lines, found_field_idx, value_end, field_indent).strip()
        if len(existing_raw) > NOTE_REPLACE_GUARD_CHARS and existing_raw not in value:
            raise TaskFieldError(
                f"Refusing to replace {task_id}'s existing note ({len(existing_raw)} chars) with "
                "a value that does not contain it -- this looks like a silent note deletion "
                "(conductor/t-129: --set note=... on a substantial note lost 199 lines of "
                "diagnostic history this way). Use append_note_text() / close_task.py's "
                "--append-note to add to the note instead, or pass force=True / --force if this "
                "replacement is intentional."
            )

    if found_field_idx is not None:
        block_style = existing_block_style(lines, found_field_idx) if "\n" in value else None
        if force_block and "\n" in value:
            block_style = force_block
        if block_style is not None:
            replacement_lines = render_block_scalar(field, block_style, value, field_indent)
        else:
            replacement_lines = [f"{' ' * field_indent}{field}: {normalize_scalar(value)}\n"]
        # Replace the key line AND its whole value block, so a multiline note
        # or a depends_on list cannot leave dangling continuation lines behind.
        value_end = field_value_end(lines, found_field_idx, end, field_indent)
        lines[found_field_idx:value_end] = replacement_lines
    else:
        if force_block and "\n" in value:
            replacement_lines = render_block_scalar(field, force_block, value, field_indent)
        else:
            replacement_lines = [f"{' ' * field_indent}{field}: {normalize_scalar(value)}\n"]
        # Insert at the end of the task block (before trailing blank separators)
        # so the new line can never split another field's multiline value.
        insert_at = end
        while insert_at > start + 1 and not lines[insert_at - 1].strip():
            insert_at -= 1
        if not lines[insert_at - 1].endswith("\n"):
            lines[insert_at - 1] += "\n"
        lines[insert_at:insert_at] = replacement_lines

    return "".join(lines)


def verify_result(text: str, task_id: str, field: str) -> bool | None:
    """Re-parse the edited document when PyYAML is available.

    Returns True when the document parses and the task carries the field,
    None when PyYAML is not importable (stdlib-only environments skip this).
    Raises TaskFieldError when the edit produced invalid or incomplete YAML.
    """
    try:
        import yaml
    except ImportError:
        return None

    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise TaskFieldError(f"Edit produced invalid YAML, refusing to write: {exc}")

    def walk(node):
        if isinstance(node, dict):
            if str(node.get("id")) == task_id:
                yield node
            for child in node.values():
                yield from walk(child)
        elif isinstance(node, list):
            for item in node:
                yield from walk(item)

    for task in walk(data):
        if field in task:
            return True
    raise TaskFieldError(
        f"Edit did not take: {task_id}.{field} is absent after parsing, refusing to write"
    )


def build_diff(path: pathlib.Path, before: str, after: str) -> str:
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=f"a/{path}",
            tofile=f"b/{path}",
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Set one field on one task in projects/<project>/roadmap.yaml without YAML reserialization.",
        epilog="WARNING: operates on the local working tree only -- it never fetches or reads "
        "origin/main (unlike claim_task.py). If claim_task.py or any other direct-to-origin/main "
        "push happened earlier in this session, run `git fetch origin main && git merge "
        "origin/main --ff-only` first, or this call can silently overwrite that push with a "
        "stale local value.",
    )
    parser.add_argument("project", help="Project slug, matching projects/<project>/")
    parser.add_argument("task_id", help="Task id, such as t-016")
    parser.add_argument("field", help="Task field to set, such as status, owner, updated")
    parser.add_argument("value", help="New scalar value. Use now, null, true, false, numbers, or a string.")
    parser.add_argument("--dry-run", action="store_true", help="Print the diff without writing")
    parser.add_argument(
        "--force",
        action="store_true",
        help=(
            "Allow replacing a substantial existing `note` outright instead of appending "
            "(bypasses the conductor/t-129 destructive-note-replace guard). Has no effect "
            "on any other field."
        ),
    )
    args = parser.parse_args()

    path = roadmap_path(args.project)
    if not path.exists():
        print(f"ERROR: Roadmap not found: {path}", file=sys.stderr)
        return 1

    before = path.read_text()
    try:
        after = set_task_field_text(before, args.task_id, args.field, args.value, force=args.force)
        if before != after:
            verified = verify_result(after, args.task_id, args.field)
            if verified is None:
                print("note: PyYAML not available; skipped post-edit validation", file=sys.stderr)
    except TaskFieldError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if before == after:
        print("No change.")
        return 0

    if args.dry_run:
        print(build_diff(path, before, after), end="")
        return 0

    path.write_text(after)
    print(f"Updated {path}: {args.task_id}.{args.field} = {args.value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
