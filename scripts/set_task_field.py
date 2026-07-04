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
"""

from __future__ import annotations

import argparse
import difflib
import pathlib
import re
import sys
from datetime import datetime, timezone


PROJECTS_DIR = pathlib.Path("projects")
TASK_ID_RE = re.compile(r"^(?P<indent>\s*)-\s+id:\s*(?P<id>[^#\n]+?)\s*(?:#.*)?$")
KEY_RE = re.compile(r"^(?P<indent>\s*)(?P<key>[A-Za-z_][A-Za-z0-9_-]*):(?P<rest>.*)$")
ALLOWED_FIELDS = {
    "status",
    "owner",
    "updated",
    "passes",
    "stakes",
    "gate_human",
    "approved_by_human",
    "depends_on",
    "note",
}


class TaskFieldError(Exception):
    pass


def normalize_scalar(value: str) -> str:
    raw = value.strip()
    lowered = raw.lower()

    if lowered == "now":
        return datetime.now(timezone.utc).strftime("'%Y-%m-%dT%H:%M:%SZ'")
    if lowered in {"null", "none", "~"}:
        return "null"
    if lowered in {"true", "false"}:
        return lowered
    if re.fullmatch(r"-?\d+", raw):
        return raw
    if re.fullmatch(r"[A-Za-z0-9_.:/@+-]+", raw):
        return raw

    escaped = raw.replace("'", "''")
    return f"'{escaped}'"


def roadmap_path(project: str) -> pathlib.Path:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", project):
        raise TaskFieldError(f"Invalid project slug: {project!r}")
    return PROJECTS_DIR / project / "roadmap.yaml"


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

    field_indent = task_indent + 2
    return start, end, field_indent


def set_task_field_text(text: str, task_id: str, field: str, value: str) -> str:
    if field not in ALLOWED_FIELDS:
        allowed = ", ".join(sorted(ALLOWED_FIELDS))
        raise TaskFieldError(f"Field {field!r} is not allowed. Allowed fields: {allowed}")

    lines = text.splitlines(keepends=True)
    if not lines:
        raise TaskFieldError("Roadmap is empty")

    start, end, field_indent = find_task_block(lines, task_id)
    rendered = normalize_scalar(value)
    replacement = f"{' ' * field_indent}{field}: {rendered}\n"

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

    if found_field_idx is not None:
        lines[found_field_idx] = replacement
    else:
        insert_at = start + 1
        while insert_at < end:
            stripped = lines[insert_at].strip()
            if stripped and not stripped.startswith("#"):
                insert_at += 1
                continue
            break
        lines.insert(insert_at, replacement)

    return "".join(lines)


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
        description="Set one field on one task in projects/<project>/roadmap.yaml without YAML reserialization."
    )
    parser.add_argument("project", help="Project slug, matching projects/<project>/")
    parser.add_argument("task_id", help="Task id, such as t-016")
    parser.add_argument("field", help="Task field to set, such as status, owner, updated")
    parser.add_argument("value", help="New scalar value. Use now, null, true, false, numbers, or a string.")
    parser.add_argument("--dry-run", action="store_true", help="Print the diff without writing")
    args = parser.parse_args()

    path = roadmap_path(args.project)
    if not path.exists():
        print(f"ERROR: Roadmap not found: {path}", file=sys.stderr)
        return 1

    before = path.read_text()
    try:
        after = set_task_field_text(before, args.task_id, args.field, args.value)
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
