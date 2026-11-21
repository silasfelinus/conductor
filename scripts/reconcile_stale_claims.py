#!/usr/bin/env python3
"""Release abandoned roadmap claims during the serialized task-event writer.

A claim older than roadmap_claims.CLAIM_TTL_MINUTES is already reclaimable by
claim_task.py, but its roadmap status remains "claimed" indefinitely. This
writer reconciles that visible state to "ready" (or "waiting" when dependencies
are not met) without altering unfinished work, notes, or human gates.

Run inside the process-task-events writer's fetch/retry/commit transaction so
concurrent newer claims win instead of being overwritten.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from project_lifecycle import lifecycle_status, load_project_overrides
from roadmap_claims import CLAIM_TTL_MINUTES, claim_is_stale
from roadmap_deps import dependency_satisfied
from roadmap_text_patch import apply_task_field_ops

ROOT = Path(__file__).resolve().parents[1]
WORKABLE_STATUSES = {"active", "playtest", "continuous"}


def dependency_blockers(task: dict[str, Any], tasks: dict[str, dict[str, Any]]) -> list[str]:
    """An expired claim must not become ready if its prerequisites aren't done."""
    raw = task.get("depends_on") or []
    dependencies = [raw] if isinstance(raw, str) else raw
    if not isinstance(dependencies, list):
        raise ValueError(f"{task.get('id')}: invalid depends_on")
    return [
        str(dep)
        for dep in dependencies
        if not dependency_satisfied(tasks.get(str(dep)))
    ]


def reconcile(
    root: Path = ROOT,
    *,
    apply: bool = False,
    now: datetime | None = None,
    project: str | None = None,
) -> list[dict[str, Any]]:
    """Return expired claims; optionally apply minimal, validated text patches."""
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("now must have a timezone")
    stamp = now.astimezone(timezone.utc).replace(microsecond=0).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    overrides = load_project_overrides(root / "project-overrides.yaml")
    findings: list[dict[str, Any]] = []

    for path in sorted((root / "projects").glob("*/roadmap.yaml")):
        slug = path.parent.name
        if project is not None and slug != project:
            continue
        if lifecycle_status(overrides, slug) not in WORKABLE_STATUSES:
            continue

        original = path.read_text(encoding="utf-8")
        roadmap = yaml.safe_load(original) or {}
        tasks = roadmap.get("tasks") or []
        by_id = {str(task["id"]): task for task in tasks if isinstance(task, dict)}
        revised = original

        for task in tasks:
            if not isinstance(task, dict) or task.get("status") != "claimed":
                continue
            if not claim_is_stale(task.get("claimed_at"), now=now):
                continue

            task_id = str(task["id"])
            blockers = dependency_blockers(task, by_id)
            new_status = "waiting" if blockers else "ready"
            findings.append(
                {
                    "project": slug,
                    "task": task_id,
                    "claimed_by": task.get("claimed_by"),
                    "claimed_at": str(task.get("claimed_at")),
                    "status": new_status,
                    "blockers": blockers,
                }
            )
            revised = apply_task_field_ops(
                revised,
                task_id,
                [
                    ("set", "status", new_status),
                    ("unset", "owner", None),
                    ("unset", "claimed_by", None),
                    ("unset", "claimed_at", None),
                    ("set", "updated", stamp),
                ],
            )

        if revised != original:
            # Never write malformed YAML or an accidental unrelated rewrite.
            yaml.safe_load(revised)
            if apply:
                path.write_text(revised, encoding="utf-8")

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Write the repairs")
    parser.add_argument("--project", help="Limit to one project")
    args = parser.parse_args()

    findings = reconcile(apply=args.apply, project=args.project)
    verb = "RELEASED" if args.apply else "WOULD RELEASE"
    for claim in findings:
        print(
            f"{verb} {claim['project']}/{claim['task']} "
            f"({claim['claimed_at']}, {claim['claimed_by']}) "
            f"-> {claim['status']}"
        )
    print(f"{len(findings)} expired claim(s), TTL={CLAIM_TTL_MINUTES} minutes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
