#!/usr/bin/env python3
"""Promote connector claim events that target an abandoned stale claim.

`next_ready_task.py` and `claim_task.py` intentionally treat a claimed task older than
CLAIM_TTL_MINUTES as claimable again. The connector task-event processor historically
did not: its collision guard consumed every replacement claim as ALREADY_CLAIMED before
it could apply. This tiny preflight keeps connector-only workers on the same shared TTL
contract without weakening fresh-claim collision protection.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from roadmap_claims import claim_is_stale  # noqa: E402


def _load_mapping(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return data


def promote_stale_claims(root: Path) -> list[Path]:
    """Set `force: true` only on claim events targeting an abandoned stale claim."""
    changed: list[Path] = []
    event_dir = root / "task-events"
    for event_path in sorted(event_dir.glob("*.yaml")):
        if event_path.name == "example.yaml":
            continue
        event = _load_mapping(event_path)
        if event.get("operation") != "claim" or event.get("force"):
            continue
        project = event.get("project")
        task_id = event.get("task")
        if not isinstance(project, str) or not isinstance(task_id, str):
            continue  # the normal processor owns shape validation/quarantine
        roadmap_path = root / "projects" / project / "roadmap.yaml"
        if not roadmap_path.is_file():
            continue
        roadmap = _load_mapping(roadmap_path)
        tasks = roadmap.get("tasks")
        if not isinstance(tasks, list):
            continue
        task = next(
            (item for item in tasks if isinstance(item, dict) and item.get("id") == task_id),
            None,
        )
        if not task or task.get("status") != "claimed":
            continue
        if not claim_is_stale(task.get("claimed_at")):
            continue

        event["force"] = True
        event_path.write_text(
            yaml.safe_dump(event, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        changed.append(event_path)
        print(
            f"Promoted stale claim recovery: {project}/{task_id} -> "
            f"session={event.get('session', '<missing>')}"
        )
    return changed


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    promote_stale_claims(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
