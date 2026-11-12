#!/usr/bin/env python3
"""Flag Memory Dungeon tasks closed while their latest acceptance gap remains unmet."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
REMAINING = re.compile(r"^\s*(?:\d{4}-\d{2}-\d{2}(?:\s+PT)?\s+)?remaining\s*:", re.IGNORECASE)
MET = re.compile(r"^\s*(?:\d{4}-\d{2}-\d{2}(?:\s+PT)?\s+)?remaining\s+met\s*:", re.IGNORECASE)


def unresolved_done_tasks(roadmap: dict) -> list[str]:
    failures: list[str] = []
    for task in roadmap.get("tasks", []):
        if task.get("status") != "done":
            continue
        note = str(task.get("note") or "")
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
    failures = unresolved_done_tasks(roadmap)
    if failures:
        print("Memory Dungeon done tasks with unverified latest remaining acceptance: " + ", ".join(failures))
        return 1
    print("Memory Dungeon done-task acceptance notes: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
