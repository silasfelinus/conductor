#!/usr/bin/env python3
"""Print the lowest unused t-NNN id from a project's live origin/main roadmap.

Usage:
    python scripts/next_free_task_id.py interface-vision

The helper fetches origin/main before reading the roadmap so agents do not choose an
identifier from a stale checkout. It only considers canonical ``t-NNN`` task ids;
other identifiers remain valid roadmap history but do not occupy a numeric slot.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from git_plumbing import read_file_at_ref, run_git  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TASK_ID_RE = re.compile(r"^t-(\d{3})$")


class NextTaskIdError(Exception):
    pass


def used_numeric_ids(doc: dict) -> set[int]:
    used: set[int] = set()
    for task in doc.get("tasks", []) or []:
        if not isinstance(task, dict):
            continue
        match = TASK_ID_RE.fullmatch(str(task.get("id", "")))
        if match:
            used.add(int(match.group(1)))
    return used


def next_free_task_id(doc: dict) -> str:
    used = used_numeric_ids(doc)
    for number in range(1, 1000):
        if number not in used:
            return f"t-{number:03d}"
    raise NextTaskIdError("no free canonical task id remains in t-001..t-999")


def load_live_roadmap(project: str) -> dict:
    run_git(ROOT, "fetch", "origin", "main", "-q")
    path = f"projects/{project}/roadmap.yaml"
    text = read_file_at_ref(ROOT, "origin/main", path)
    if text is None:
        raise NextTaskIdError(f"{path} not found on origin/main")
    doc = yaml.safe_load(text) or {}
    if not isinstance(doc, dict):
        raise NextTaskIdError(f"{path} is not a YAML mapping")
    return doc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="Project slug under projects/")
    args = parser.parse_args()

    try:
        print(next_free_task_id(load_live_roadmap(args.project)))
    except (NextTaskIdError, OSError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
