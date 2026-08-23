#!/usr/bin/env python3
"""
next_ready_task.py — print the first unblocked ready task across conductor roadmaps.

Usage:
    python scripts/next_ready_task.py
    python scripts/next_ready_task.py --json

This is intentionally read-only. It mirrors the Worker selection rules closely enough
for connector-only runs to confirm which task should be claimed without mutating any
roadmap files.

Picking a task here is advisory only -- it does not reserve it. Run
`scripts/claim_task.py <project> <task-id> --owner <worker|reviewer> --session <id>`
against the live `origin/main` before starting real implementation work, and rotate to
the next task/project if it reports ALREADY_CLAIMED (see conductor/t-040). A
`status: claimed` task whose `claimed_at` is older than CLAIM_TTL_MINUTES
(roadmap_claims.py) is treated as an abandoned claim and surfaced here as pickable
again, so a crashed session can't lock a task forever.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from daily_gate import already_recorded_today  # noqa: E402
from roadmap_claims import task_is_claimable  # noqa: E402
from roadmap_deps import dependency_satisfied  # noqa: E402
from project_lifecycle import load_project_overrides, ordered_workable_slugs  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT / "projects"
PRIORITY_FILE = ROOT / "projects" / "priority.yaml"
OVERRIDES_FILE = ROOT / "project-overrides.yaml"


Task = dict[str, Any]
Roadmap = dict[str, Any]


def load_yaml(path: Path) -> Any:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def load_priority_order() -> list[str]:
    raw = load_yaml(PRIORITY_FILE) or {}
    order = raw.get("order", [])
    return [slug for slug in order if isinstance(slug, str)]


def load_workable_overrides() -> dict[str, dict[str, Any]]:
    return load_project_overrides(OVERRIDES_FILE)


def load_roadmap(slug: str) -> Roadmap | None:
    if slug == "_template":
        return None
    path = PROJECTS_DIR / slug / "roadmap.yaml"
    raw = load_yaml(path)
    if not isinstance(raw, dict):
        return None
    return raw


def task_is_unblocked(task: Task, tasks_by_id: dict[str, Task]) -> bool:
    deps = as_list(task.get("depends_on"))
    return all(dependency_satisfied(tasks_by_id.get(str(dep))) for dep in deps)


def first_ready_task(
    order: list[str], active: dict[str, dict[str, Any]], *, now: Any = None
) -> dict[str, Any] | None:
    for slug in ordered_workable_slugs(order, active):
        roadmap = load_roadmap(slug)
        if not roadmap:
            continue
        tasks = [task for task in roadmap.get("tasks", []) if isinstance(task, dict)]
        tasks_by_id = {str(task.get("id")): task for task in tasks if task.get("id")}

        for task in tasks:
            if not task_is_claimable(task, tasks_by_id=tasks_by_id):
                continue
            if not task_is_unblocked(task, tasks_by_id):
                continue
            if already_recorded_today(task, now=now):
                # Same-day-gated recurring task (e.g. mermaids-of-venice/t-013) whose
                # note already records today's Pacific-date outcome -- claiming it now
                # would just repeat work an earlier session already did this cycle
                # (conductor/t-123). Skip to the next candidate instead.
                continue
            return {
                "project": roadmap.get("project") or slug,
                "kind": roadmap.get("kind"),
                "task_id": task.get("id"),
                "title": task.get("title"),
                "stakes": task.get("stakes"),
                "path": str(PROJECTS_DIR / slug / "roadmap.yaml"),
                "reclaimed_stale_claim": task.get("status") == "claimed",
            }
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    result = first_ready_task(load_priority_order(), load_workable_overrides())
    if args.json:
        print(json.dumps(result or {"task": None}, indent=2, sort_keys=True))
        return 0 if result else 1

    if not result:
        print("No unblocked ready tasks found.")
        return 1

    print(f"{result['project']}/{result['task_id']}: {result['title']}")
    print(f"kind: {result.get('kind') or 'unknown'}")
    print(f"stakes: {result.get('stakes') or 'unknown'}")
    print(f"roadmap: {result['path']}")
    if result.get("reclaimed_stale_claim"):
        print("note: reclaiming a stale claim (claimed_at older than CLAIM_TTL_MINUTES)")
    print("Run scripts/claim_task.py before starting real work -- see this script's docstring.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
