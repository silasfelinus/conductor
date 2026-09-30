#!/usr/bin/env python3
"""Print one roadmap task (or a compact task index) without loading the whole roadmap.

Token essentialization (2026-09-30). The large roadmaps run 100-240KB each
(projects/conductor/roadmap.yaml alone is ~60k tokens), so reading one to look
at a single task costs a session more than its entire operating manual. Print
just the task instead -- the raw YAML block by default, so notes keep their
exact wording.

Usage:
  python scripts/show_task.py conductor t-125            # raw YAML block for one task
  python scripts/show_task.py conductor/t-125            # same, slash form
  python scripts/show_task.py conductor t-125 --no-note  # drop the (often long) note: field
  python scripts/show_task.py conductor t-125 --note-tail 1500  # only the last 1500 chars of note
  python scripts/show_task.py conductor --list           # one line per task: id, status, title
  python scripts/show_task.py conductor --list --status ready,needs-human
  python scripts/show_task.py conductor --milestones     # milestone ids/status/titles only
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASK_START = re.compile(r"^(\s*)- id:\s*['\"]?([^'\"\s#]+)")
FIELD = re.compile(r"^(\s*)([A-Za-z_][\w-]*):(.*)$")


def roadmap_lines(project: str) -> list[str]:
    path = ROOT / "projects" / project / "roadmap.yaml"
    if not path.is_file():
        sys.exit(f"no roadmap: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8").splitlines()


def task_blocks(lines: list[str]):
    """Yield (task_id, [lines]) for each `- id:` block under the top-level tasks: key."""
    in_tasks = False
    current_id, current, indent = None, [], None
    for line in lines:
        if not line.startswith((" ", "-", "#")) and line.strip():
            if current_id:
                yield current_id, current
                current_id, current = None, []
            in_tasks = line.startswith("tasks:")
            continue
        if not in_tasks:
            continue
        m = TASK_START.match(line)
        if m and (indent is None or len(m.group(1)) == indent):
            if current_id:
                yield current_id, current
            indent = len(m.group(1))
            current_id, current = m.group(2), [line]
        elif current_id:
            current.append(line)
    if current_id:
        yield current_id, current


def field_value(block: list[str], name: str) -> str:
    for line in block:
        m = FIELD.match(line.replace("- ", "  ", 1))
        if m and m.group(2) == name:
            return m.group(3).strip().strip("'\"")
    return ""


def drop_or_trim_note(block: list[str], note_tail: int | None) -> list[str]:
    out, i = [], 0
    field_indent = None
    while i < len(block):
        line = block[i]
        m = FIELD.match(line.replace("- ", "  ", 1))
        if field_indent is None and m:
            field_indent = len(m.group(1))
        if m and m.group(2) == "note" and len(m.group(1)) == field_indent:
            j = i + 1
            while j < len(block):
                n = FIELD.match(block[j])
                if block[j].strip() and n and len(n.group(1)) <= field_indent:
                    break
                j += 1
            note_text = "\n".join(block[i:j])
            if note_tail is None:
                out.append(f"{' ' * field_indent}note: <omitted {len(note_text):,} chars; rerun without --no-note>")
            else:
                tail = note_text[-note_tail:]
                out.append(f"{' ' * field_indent}note: <... {max(0, len(note_text) - note_tail):,} earlier chars omitted>")
                out.append(tail)
            i = j
            continue
        out.append(line)
        i += 1
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", help="project slug, or project/task-id")
    ap.add_argument("task_id", nargs="?")
    ap.add_argument("--list", action="store_true", help="one line per task")
    ap.add_argument("--status", default="", help="with --list: comma-separated statuses to keep")
    ap.add_argument("--milestones", action="store_true", help="print the milestones: section only")
    ap.add_argument("--no-note", action="store_true", help="omit the note: field")
    ap.add_argument("--note-tail", type=int, default=None, help="keep only the last N chars of note:")
    args = ap.parse_args()

    project, task_id = args.project, args.task_id
    if "/" in project and not task_id:
        project, task_id = project.split("/", 1)
    lines = roadmap_lines(project)

    if args.milestones:
        in_ms = False
        for line in lines:
            if line.startswith("milestones:"):
                in_ms = True
                continue
            if in_ms and line.strip() and not line.startswith((" ", "-", "#")):
                break
            if in_ms and re.match(r"^\s*-?\s*(id|title|status):", line):
                print(line)
        return 0

    if args.list or not task_id:
        keep = {s.strip() for s in args.status.split(",") if s.strip()}
        for tid, block in task_blocks(lines):
            status = field_value(block, "status")
            if keep and status not in keep:
                continue
            print(f"{tid:<8} {status:<12} {field_value(block, 'title')[:110]}")
        return 0

    for tid, block in task_blocks(lines):
        if tid == task_id:
            if args.no_note or args.note_tail is not None:
                block = drop_or_trim_note(block, None if args.no_note else args.note_tail)
            print("\n".join(block))
            return 0
    print(f"{project}/{task_id} not found", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
