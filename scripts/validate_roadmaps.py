#!/usr/bin/env python3
"""
validate_roadmaps.py — confirm every projects/*/roadmap.yaml still parses as a
mapping with a `tasks` list, that no project's tasks reuse an `id`, and that
actionable task stakes / effective project kinds use supported enum values. Used
by the process-task-events workflow after a surgical text edit, and by the pytest
suite (tests/test_validate_roadmaps.py) that runs on every PR via
.github/workflows/ci.yml, so this fails CI immediately rather than silently
landing. Safe to run standalone.

A duplicate task id lets tooling that keys on id (claim_task.py, set_task_field.py,
close_task.py -- see scripts/set_task_field.py's find_task_block, which matches the
FIRST occurrence and silently ignores the rest) operate on the wrong task, or make
the second occurrence unreachable entirely. This happened for real twice in
interface-vision's roadmap on 2026-08-02: first t-053/t-054/t-055/t-056 each used
twice, then the manual renumbering fix (to t-058..t-061) collided with pre-existing
t-061/t-062 -- see interface-vision/t-062's note and this repo's TALKBACK.md that
date. audit_roadmaps.py already detects this (DUPLICATE_TASK_ID) but only reports
it advisorily; it never fails CI, so the second collision landed anyway.

Usage: python scripts/validate_roadmaps.py
"""
from __future__ import annotations

import collections
import sys
from pathlib import Path

import yaml

try:
    from project_lifecycle import PROJECT_LIFECYCLE_STATUSES, load_project_overrides
except ModuleNotFoundError:  # imported as scripts.validate_roadmaps in pytest
    from scripts.project_lifecycle import PROJECT_LIFECYCLE_STATUSES, load_project_overrides

ROOT = Path(__file__).resolve().parents[1]
VALID_TASK_STAKES = {"reversible", "outward-facing", "irreversible"}
VALID_PROJECT_KINDS = {"software", "content", "proposal", "brainstorm", "infrastructure"}


def duplicate_task_ids(tasks: list) -> list[str]:
    ids = [str(task.get("id")) for task in tasks if isinstance(task, dict) and task.get("id")]
    counts = collections.Counter(ids)
    return sorted(task_id for task_id, count in counts.items() if count > 1)


def main() -> int:
    ok = True
    overrides_path = ROOT / "project-overrides.yaml"
    overrides = load_project_overrides(overrides_path) if overrides_path.exists() else {}
    for slug, cfg in overrides.items():
        status = str(cfg.get("status", "active"))
        if status not in PROJECT_LIFECYCLE_STATUSES:
            print(f"invalid project lifecycle status for {slug}: {status}", file=sys.stderr)
            ok = False
    for path in sorted((ROOT / "projects").glob("*/roadmap.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("tasks", []), list):
            print(f"invalid roadmap: {path}", file=sys.stderr)
            ok = False
            continue

        slug = str(data.get("project") or path.parent.name)
        override = overrides.get(slug, {})
        lifecycle = str(override.get("status", "active"))
        if overrides and lifecycle == "active":
            open_tasks = [task for task in data["tasks"] if isinstance(task, dict) and task.get("status") != "done"]
            if not open_tasks:
                print(
                    f"active project has no open tasks: {slug} -- reconcile its goal, add real work, or explicitly finish/pause it",
                    file=sys.stderr,
                )
                ok = False

        raw_kind = override.get("kind") or data.get("kind")
        if raw_kind is not None and str(raw_kind) not in VALID_PROJECT_KINDS:
            print(
                f"invalid project kind for {slug}: {raw_kind!r} -- expected one of {', '.join(sorted(VALID_PROJECT_KINDS))}",
                file=sys.stderr,
            )
            ok = False

        dupes = duplicate_task_ids(data["tasks"])
        if dupes:
            print(
                f"duplicate task id(s) in {path}: {', '.join(dupes)} "
                "-- each task id must be unique within a project's roadmap",
                file=sys.stderr,
            )
            ok = False

        for task in data["tasks"]:
            if not isinstance(task, dict) or task.get("status") == "done" or "stakes" not in task:
                continue
            stakes = task.get("stakes")
            if stakes not in VALID_TASK_STAKES:
                task_id = str(task.get("id") or "<missing>")
                print(
                    f"invalid task stakes in {path} for {task_id}: {stakes!r} -- expected one of {', '.join(sorted(VALID_TASK_STAKES))}",
                    file=sys.stderr,
                )
                ok = False

    if not ok:
        return 1
    print("Roadmaps valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
