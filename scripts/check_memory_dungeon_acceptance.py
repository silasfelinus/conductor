#!/usr/bin/env python3
"""Flag Memory Dungeon tasks closed while their latest acceptance gap remains unmet."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REMAINING = re.compile(r"^\s*(?:\d{4}-\d{2}-\d{2}(?:\s+PT)?\s+)?remaining\s*:", re.IGNORECASE)
MET = re.compile(r"^\s*(?:\d{4}-\d{2}-\d{2}(?:\s+PT)?\s+)?remaining\s+met\s*:", re.IGNORECASE)


ARCHIVED_NOTE = re.compile(
    r"<!-- note:begin (?P<id>[^\s>]+) -->\n(?P<body>.*?)<!-- note:end (?P=id) -->\n", re.DOTALL
)


def archived_notes(history_text: str) -> dict[str, str]:
    """Verbatim done-task notes moved to HISTORY.md by archive_done_task_notes.py."""
    return {m.group("id"): m.group("body") for m in ARCHIVED_NOTE.finditer(history_text)}


def full_note(task: dict, archive: dict[str, str]) -> str:
    """The live note, with its archived verbatim body restored when it was archived.

    The archiver keeps only a short head (often the first "remaining:" line) plus a
    pointer, so judging the live stub alone would resurrect an already-met gap.
    Lines appended after the archive pointer still count, last.
    """
    note = str(task.get("note") or "")
    archived = archive.get(str(task.get("id")))
    if archived is None:
        return note
    lines = note.splitlines()
    pointer = max((i for i, line in enumerate(lines) if "HISTORY.md#" in line), default=-1)
    extra = lines[pointer + 1 :] if pointer >= 0 else []
    return archived + "\n" + "\n".join(extra)


def unresolved_done_tasks(roadmap: dict, archive: dict[str, str] | None = None) -> list[str]:
    failures: list[str] = []
    for task in roadmap.get("tasks", []):
        if task.get("status") != "done":
            continue
        note = full_note(task, archive or {})
        lines = note.splitlines()
        latest_gap = max((i for i, line in enumerate(lines) if REMAINING.search(line)), default=-1)
        if latest_gap < 0:
            continue
        if not any(MET.search(line) for line in lines[latest_gap + 1 :]):
            failures.append(str(task.get("id", "<unknown>")))
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roadmap", type=Path, default=ROOT / "projects/memory-dungeon/roadmap.yaml")
    args = parser.parse_args()
    with args.roadmap.open(encoding="utf-8") as source:
        roadmap = yaml.safe_load(source)
    history = args.roadmap.with_name("HISTORY.md")
    archive = archived_notes(history.read_text(encoding="utf-8")) if history.is_file() else {}
    failures = unresolved_done_tasks(roadmap, archive)
    if failures:
        print("Memory Dungeon done tasks with unverified latest remaining acceptance: " + ", ".join(failures))
        return 1
    print("Memory Dungeon done-task acceptance notes: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
