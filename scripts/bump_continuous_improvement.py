#!/usr/bin/env python3
"""
bump_continuous_improvement.py — advance a t-010-style recurring task's nested
`continuous_improvement` mapping (last_lane/next_lane/last_run/last_pr)
without YAML reserialization.

Fixes ai-art-academy/t-058: set_task_field.py's ALLOWED_FIELDS and
set_task_field_text() only ever touch a task's top-level scalar keys, never a
nested mapping like `continuous_improvement`, and process_task_events.py's
rearm/ready/done ops never write it either. Every close-out that needed to
advance the counter had to hand-edit the YAML, and the counter went stale at
least three times in two days as a result (see root TALKBACK.md and this
project's docs/continuous-improvement-run-log.md, both 2026-08-06).

Usage:
    python scripts/bump_continuous_improvement.py <project> <task-id> --lane N \\
        --pr <owner/repo#number> [--run <ISO8601 | now>] [--dry-run]

`--lane N` sets `last_lane: N` and derives `next_lane` as the next lane in the
1->2->3->4->1 rotation (`N % 4 + 1`). `--run` defaults to `now`. If the task's
`continuous_improvement` mapping is missing a key this call would otherwise
set, the key is appended to the mapping rather than treated as an error, so a
future task adopting the same convention doesn't need every key pre-seeded.

WARNING -- local working tree only, same caveat as set_task_field.py: this
script never fetches or reads from origin/main. Fetch/fast-forward first if a
direct-to-origin/main push (e.g. claim_task.py) happened earlier this session.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from datetime import datetime, timezone

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from set_task_field import (  # noqa: E402
    KEY_RE,
    TaskFieldError,
    build_diff,
    find_task_block,
    line_indent,
    normalize_scalar,
    roadmap_path,
)

MAPPING_KEY = "continuous_improvement"
LANE_COUNT = 4
PR_RE = re.compile(r"^[\w.-]+/[\w.-]+#\d+$")


def find_mapping_block(
    lines: list[str], task_start: int, task_end: int, task_field_indent: int
) -> tuple[int, int, int]:
    """Locate the `continuous_improvement:` mapping inside one task block.

    Returns (key_idx, block_end, entry_indent) where block_end is one past the
    mapping's last entry and entry_indent is the indent of each `key: value`
    line inside it (task_field_indent + 2, matching every nested mapping in
    these roadmaps).
    """
    key_idx: int | None = None
    for idx in range(task_start + 1, task_end):
        match = KEY_RE.match(lines[idx])
        if not match:
            continue
        if len(match.group("indent")) != task_field_indent:
            continue
        if match.group("key") == MAPPING_KEY:
            key_idx = idx
            break

    if key_idx is None:
        raise TaskFieldError(
            f"Task has no {MAPPING_KEY!r} mapping to bump -- add it first "
            "(see ai-art-academy/t-010 for the expected shape: last_lane, "
            "next_lane, last_run, last_pr)."
        )

    entry_indent = task_field_indent + 2
    block_end = task_end
    for idx in range(key_idx + 1, task_end):
        stripped = lines[idx].strip()
        if not stripped:
            continue
        if line_indent(lines[idx]) < entry_indent:
            block_end = idx
            break
    else:
        block_end = task_end

    return key_idx, block_end, entry_indent


def extract_trailing_comment(rest: str) -> str:
    """Return a line's trailing `  # comment`, aware that a quoted scalar's own
    value can legitimately contain `#` (e.g. an `owner/repo#123` PR reference).

    Only treats `#` as a comment start when it is outside any quoted scalar
    and preceded by whitespace, matching YAML's own comment rule for plain
    scalars.
    """
    rest = rest.strip()
    if rest[:1] in ("'", '"'):
        quote = rest[0]
        i = 1
        while i < len(rest):
            if rest[i] == quote:
                # A doubled quote (YAML's single-quote escape) is literal, not a close.
                if quote == "'" and rest[i : i + 2] == "''":
                    i += 2
                    continue
                i += 1
                break
            i += 1
        remainder = rest[i:]
    else:
        remainder = rest

    comment_match = re.search(r"(?:^|\s)(#.*)$", remainder)
    return f"  {comment_match.group(1)}" if comment_match else ""


def set_mapping_entry(
    lines: list[str],
    mapping_start: int,
    mapping_end: int,
    entry_indent: int,
    key: str,
    value: str,
) -> int:
    """Set one `key: value` line inside an already-located mapping block.

    Preserves a trailing `  # comment` on an existing line for that key.
    Returns the (possibly shifted) mapping_end after insertion/replacement.
    """
    for idx in range(mapping_start, mapping_end):
        match = KEY_RE.match(lines[idx])
        if not match or len(match.group("indent")) != entry_indent:
            continue
        if match.group("key") != key:
            continue
        comment = extract_trailing_comment(match.group("rest"))
        lines[idx] = f"{' ' * entry_indent}{key}: {normalize_scalar(value)}{comment}\n"
        return mapping_end

    # Key not present -- append at the end of the mapping block.
    new_line = f"{' ' * entry_indent}{key}: {normalize_scalar(value)}\n"
    lines.insert(mapping_end, new_line)
    return mapping_end + 1


def bump_continuous_improvement_text(
    text: str, task_id: str, lane: int, pr_ref: str, run_value: str
) -> str:
    if not 1 <= lane <= LANE_COUNT:
        raise TaskFieldError(f"--lane must be between 1 and {LANE_COUNT}, got {lane}")
    if not PR_RE.match(pr_ref):
        raise TaskFieldError(
            f"--pr must look like owner/repo#number, got {pr_ref!r}"
        )

    lines = text.splitlines(keepends=True)
    task_start, task_end, task_field_indent = find_task_block(lines, task_id)
    mapping_start, mapping_end, entry_indent = find_mapping_block(
        lines, task_start, task_end, task_field_indent
    )

    next_lane = lane % LANE_COUNT + 1
    run_iso = (
        datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        if run_value.strip().lower() == "now"
        else run_value
    )

    mapping_end = set_mapping_entry(
        lines, mapping_start, mapping_end, entry_indent, "last_lane", str(lane)
    )
    mapping_end = set_mapping_entry(
        lines, mapping_start, mapping_end, entry_indent, "next_lane", str(next_lane)
    )
    mapping_end = set_mapping_entry(
        lines, mapping_start, mapping_end, entry_indent, "last_run", run_iso
    )
    mapping_end = set_mapping_entry(
        lines, mapping_start, mapping_end, entry_indent, "last_pr", pr_ref
    )

    return "".join(lines)


def verify_result(text: str, task_id: str, lane: int, next_lane: int, pr_ref: str) -> bool | None:
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
        mapping = task.get(MAPPING_KEY)
        if not isinstance(mapping, dict):
            continue
        if (
            mapping.get("last_lane") == lane
            and mapping.get("next_lane") == next_lane
            and mapping.get("last_pr") == pr_ref
        ):
            return True
    raise TaskFieldError(
        f"Edit did not take: {task_id}.{MAPPING_KEY} does not show the expected "
        "values after parsing, refusing to write"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Advance a recurring task's nested continuous_improvement mapping "
            "(last_lane/next_lane/last_run/last_pr) without YAML reserialization."
        ),
    )
    parser.add_argument("project", help="Project slug, matching projects/<project>/")
    parser.add_argument("task_id", help="Task id, such as t-010")
    parser.add_argument(
        "--lane", type=int, required=True, help="Lane number just completed (1-4)"
    )
    parser.add_argument(
        "--pr", required=True, metavar="OWNER/REPO#N", help="PR that closed this cycle"
    )
    parser.add_argument(
        "--run", default="now", help="Timestamp for last_run (ISO8601, or 'now')"
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the diff without writing")
    args = parser.parse_args()

    path = roadmap_path(args.project)
    if not path.exists():
        print(f"ERROR: Roadmap not found: {path}", file=sys.stderr)
        return 1

    before = path.read_text()
    try:
        after = bump_continuous_improvement_text(before, args.task_id, args.lane, args.pr, args.run)
        next_lane = args.lane % LANE_COUNT + 1
        if before != after:
            verified = verify_result(after, args.task_id, args.lane, next_lane, args.pr)
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
    print(
        f"Updated {path}: {args.task_id}.{MAPPING_KEY} = "
        f"last_lane={args.lane}, next_lane={next_lane}, last_pr={args.pr}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
