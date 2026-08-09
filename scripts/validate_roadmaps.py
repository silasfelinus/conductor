#!/usr/bin/env python3
"""
validate_roadmaps.py — confirm every projects/*/roadmap.yaml still parses as a
mapping with a `tasks` list, and that no project's tasks reuse an `id`. Used by
the process-task-events workflow after a surgical text edit, and by the pytest
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

The same promote-from-advisory-to-hard treatment applies to an invalid `stakes:`
enum value (conductor/t-107): `kindrobots-unraid/t-006` carried `stakes: high` --
not one of `reversible|outward-facing|irreversible` (looks like `priority: high`
bled into the wrong field) -- and went undetected until the task closed and
`process_task_events.prepare_learning`'s fallback silently coerced it to `None` in
the committed `LEARNING.yaml`, redding `test_committed_ledger_schema_conformance`
for every subsequent PR. audit_roadmaps.py's INVALID_STAKES_VALUE finding catches
this too, but only advisorily; failing CI here catches it at PR time on the
roadmap edit itself, before it ever reaches the learning-ledger fallback.

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

# Kept in sync by hand with audit_roadmaps.py's VALID_STAKES and
# backfill_learning.py's VALID_STAKES / process_task_events.py's inline check --
# the three enum values AGENTS.md/CLAUDE.md define for a task's `stakes:` field.
VALID_STAKES = {"reversible", "outward-facing", "irreversible"}


def duplicate_task_ids(tasks: list) -> list[str]:
    ids = [str(task.get("id")) for task in tasks if isinstance(task, dict) and task.get("id")]
    counts = collections.Counter(ids)
    return sorted(task_id for task_id, count in counts.items() if count > 1)


def invalid_stakes_values(tasks: list) -> list[str]:
    bad = []
    for task in tasks:
        if not isinstance(task, dict):
            continue
        stakes = task.get("stakes")
        if stakes is not None and str(stakes) not in VALID_STAKES:
            bad.append(f"{task.get('id')}={stakes!r}")
    return sorted(bad)


def main() -> int:
    ok = True
    overrides_path = ROOT / 'project-overrides.yaml'
    overrides = load_project_overrides(overrides_path) if overrides_path.exists() else {}
    for slug, cfg in overrides.items():
        status = str(cfg.get('status', 'active'))
        if status not in PROJECT_LIFECYCLE_STATUSES:
            print(f'invalid project lifecycle status for {slug}: {status}', file=sys.stderr)
            ok = False
    for path in sorted((ROOT / "projects").glob("*/roadmap.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("tasks", []), list):
            print(f"invalid roadmap: {path}", file=sys.stderr)
            ok = False
            continue

        slug = str(data.get('project') or path.parent.name)
        lifecycle = str(overrides.get(slug, {}).get('status', 'active'))
        if overrides and lifecycle == 'active':
            open_tasks = [task for task in data['tasks'] if isinstance(task, dict) and task.get('status') != 'done']
            if not open_tasks:
                print(
                    f'active project has no open tasks: {slug} -- reconcile its goal, add real work, or explicitly finish/pause it',
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

        bad_stakes = invalid_stakes_values(data["tasks"])
        if bad_stakes:
            print(
                f"invalid stakes value(s) in {path}: {', '.join(bad_stakes)} "
                "-- stakes must be one of reversible|outward-facing|irreversible "
                "(check for a status/priority value in the wrong field)",
                file=sys.stderr,
            )
            ok = False

    if not ok:
        return 1
    print("Roadmaps valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
