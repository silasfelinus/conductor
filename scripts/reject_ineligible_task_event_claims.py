#!/usr/bin/env python3
"""Consume connector claim events that are not dependency-eligible.

The normal task-event processor intentionally accepts small connector-written events and
applies them against the complete roadmap. A claim must nevertheless obey the same
pipeline eligibility contract as claim_task.py: every dependency is done, and a
human-gated dependency is explicitly approved. This preflight runs immediately before
process_task_events.py in the serialized workflow and consumes only claims that cannot
legally reserve their task yet.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
EVENT_DIR = ROOT / "task-events"


def load_mapping(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return data


def find_task(roadmap: dict[str, Any], task_id: str) -> dict[str, Any]:
    tasks = roadmap.get("tasks")
    if not isinstance(tasks, list):
        raise ValueError("roadmap tasks must be a list")
    matches = [task for task in tasks if isinstance(task, dict) and task.get("id") == task_id]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one task {task_id!r}; found {len(matches)}")
    return matches[0]


def dependency_ids(task: dict[str, Any]) -> list[str]:
    raw = task.get("depends_on")
    if raw is None:
        return []
    if isinstance(raw, str) and raw.strip():
        return [raw.strip()]
    if isinstance(raw, list) and all(isinstance(item, str) and item.strip() for item in raw):
        return [item.strip() for item in raw]
    raise ValueError("depends_on must be a task id or a list of task ids")


def dependency_blockers(roadmap: dict[str, Any], task: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    for dependency_id in dependency_ids(task):
        dependency = find_task(roadmap, dependency_id)
        if dependency.get("status") != "done":
            blockers.append(f"{dependency_id} status={dependency.get('status')!r}")
        elif dependency.get("gate_human") and dependency.get("approved_by_human") is not True:
            blockers.append(f"{dependency_id} human approval missing")
    return blockers


def process_event(path: Path, *, dry_run: bool = False) -> str | None:
    event = load_mapping(path)
    if event.get("operation") != "claim" or event.get("force"):
        return None

    project = event.get("project")
    task_id = event.get("task")
    if not isinstance(project, str) or not project.strip():
        return None
    if not isinstance(task_id, str) or not task_id.strip():
        return None

    roadmap_path = ROOT / "projects" / project.strip() / "roadmap.yaml"
    if not roadmap_path.is_file():
        return None
    roadmap = load_mapping(roadmap_path)
    task = find_task(roadmap, task_id.strip())
    blockers = dependency_blockers(roadmap, task)
    if not blockers:
        return None

    if not dry_run:
        path.unlink()
    prefix = "WOULD CONSUME" if dry_run else "CONSUMED"
    return (
        f"{project.strip()}/{task_id.strip()}: DEPENDENCY_BLOCKED ({prefix}) -- "
        + ", ".join(blockers)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    for path in sorted(EVENT_DIR.glob("*.yaml")) if EVENT_DIR.exists() else []:
        if path.name == "example.yaml":
            continue
        result = process_event(path, dry_run=args.dry_run)
        if result:
            print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
