#!/usr/bin/env python3
"""
check_priority_queue_starvation.py — flag a priority queue that only produced
work by walking past several gate-bound or busy projects.

Filed conductor/t-149 (2026-09-11, portfolio-assessment sweep). `priority.yaml` is
the deterministic worker pickup order, and `next_ready_task.py` already falls
through it correctly when the top projects have no claimable work -- but nothing
reports HOW FAR a session had to walk before landing on real work. From the
session end, "I picked up the top-ranked available task" and "I walked past six
gate-blocked projects to get here" are indistinguishable, so a portfolio that has
quietly become gate-bound rather than work-bound looks identical to one running
normally. That distinction is exactly what Silas needs to decide whether to spend
a session clearing gates or building features, and until now it was only
discoverable by hand-auditing every roadmap.

This is not a bug in the resolver -- fall-through is the intended behavior, and the
work it lands on is real. This script only makes the fall-through depth visible.

For each project skipped before the landing project, it reports why that project
produced no claimable work, using the same shared claim/dependency rules
`next_ready_task.py` uses (`roadmap_claims.task_is_claimable`,
`roadmap_deps.dependency_satisfied`, `daily_gate.already_recorded_today`) so the
two scripts can never disagree about what counts as "ready":

  GATED AT NEEDS-HUMAN: at least one task is `status: needs-human`. Named
  explicitly (task id + title) so this doubles as "here is what only Silas can
  unblock, ranked by how much agent work it frees" -- audit_human_gates.py reports
  gates flat, with no priority context; this adds that context.

  ALL WAITING-BLOCKED: every non-done task is `status: waiting` on an unmet
  dependency (see roadmap_deps.dependency_satisfied).

  ALL CLAIMED: every non-done task is `status: claimed` with a fresh (non-stale)
  claim -- someone is already actively on it.

  ALL DONE: no task in any of the above buckets remains -- the project's queue is
  genuinely empty (finished work, or only `blocked`/`review`/`challenged` tasks
  left, which are not this script's concern).

A skipped project can show more than one reason; the message picks the single
most actionable one, in this order: needs-human, then waiting-blocked, then
claimed, then done. A human gate is worth surfacing over a structural dependency
block, which is in turn more informative than "someone's already claimed
something else here" (transient, usually self-resolving).

Advisory only, same discipline as check_milestone_status_drift.py and
check_container_log_drift.py: it must never block task selection or gate
anything. Exit non-zero only past a threshold depth (default 3, i.e. the landing
project ranks 4th or worse) so normal fall-through of one or two gate-bound
projects stays quiet and this does not become wallpaper. A priority order with NO
claimable work anywhere is always reported, regardless of threshold.

Purely local YAML analysis -- no network access, no KR_API_TOKEN needed.

Usage:
  python scripts/check_priority_queue_starvation.py
  python scripts/check_priority_queue_starvation.py --json
  python scripts/check_priority_queue_starvation.py --threshold 3

Exit codes: 0 = landing project rank is within the threshold (or nothing to
check), 1 = landing project rank exceeds the threshold, or no project in the
entire order has claimable work at all.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT / "projects"
PRIORITY_FILE = ROOT / "projects" / "priority.yaml"
OVERRIDES_FILE = ROOT / "project-overrides.yaml"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from daily_gate import already_recorded_today  # noqa: E402
from roadmap_claims import claim_is_stale, task_is_claimable  # noqa: E402
from roadmap_deps import dependency_satisfied  # noqa: E402
from project_lifecycle import load_project_overrides, ordered_workable_slugs  # noqa: E402

DEFAULT_THRESHOLD = 3

Task = dict[str, Any]


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


def load_priority_order(path: Path | None = None) -> list[str]:
    raw = load_yaml(path or PRIORITY_FILE) or {}
    order = raw.get("order", [])
    return [slug for slug in order if isinstance(slug, str)]


def load_roadmap(slug: str, projects_dir: Path) -> dict[str, Any] | None:
    if slug == "_template":
        return None
    raw = load_yaml(projects_dir / slug / "roadmap.yaml")
    return raw if isinstance(raw, dict) else None


def task_is_unblocked(task: Task, tasks_by_id: dict[str, Task]) -> bool:
    deps = as_list(task.get("depends_on"))
    return all(dependency_satisfied(tasks_by_id.get(str(dep))) for dep in deps)


def has_claimable_ready_task(
    tasks: list[Task], tasks_by_id: dict[str, Task], *, now: Any = None
) -> bool:
    for task in tasks:
        if not task_is_claimable(task, tasks_by_id=tasks_by_id, now=now):
            continue
        if not task_is_unblocked(task, tasks_by_id):
            continue
        if already_recorded_today(task, now=now):
            continue
        return True
    return False


def classify_starvation(
    tasks: list[Task], tasks_by_id: dict[str, Task], *, now: Any = None
) -> tuple[str, list[Task]]:
    """Return (reason, evidence tasks) for a project with no claimable ready task.

    Precedence: a human gate is the most actionable signal, then a real
    dependency block, then "busy" (already claimed), then "nothing left".
    """
    needs_human = [t for t in tasks if t.get("status") == "needs-human"]
    if needs_human:
        return "gated-at-needs-human", needs_human

    waiting = [
        t
        for t in tasks
        if t.get("status") == "waiting" and not task_is_unblocked(t, tasks_by_id)
    ]
    if waiting:
        return "all-waiting-blocked", waiting

    claimed = [
        t
        for t in tasks
        if t.get("status") == "claimed" and not claim_is_stale(t.get("claimed_at"), now=now)
    ]
    if claimed:
        return "all-claimed", claimed

    return "all-done", []


REASON_LABELS = {
    "gated-at-needs-human": "gated at needs-human",
    "all-waiting-blocked": "all waiting-blocked",
    "all-claimed": "all claimed",
    "all-done": "all done",
}


def scan(
    *,
    projects_dir: Path | None = None,
    priority_path: Path | None = None,
    overrides_path: Path | None = None,
    now: Any = None,
) -> dict[str, Any]:
    projects_dir = projects_dir or PROJECTS_DIR
    order = load_priority_order(priority_path)
    overrides = load_project_overrides(overrides_path or OVERRIDES_FILE)

    skipped: list[dict[str, Any]] = []
    landing: dict[str, Any] | None = None
    rank = 0

    for slug in ordered_workable_slugs(order, overrides):
        roadmap = load_roadmap(slug, projects_dir)
        if roadmap is None:
            continue
        rank += 1

        tasks = [t for t in roadmap.get("tasks", []) if isinstance(t, dict)]
        tasks_by_id = {str(t.get("id")): t for t in tasks if t.get("id")}

        if has_claimable_ready_task(tasks, tasks_by_id, now=now):
            landing = {"project": slug, "rank": rank}
            break

        reason, evidence = classify_starvation(tasks, tasks_by_id, now=now)
        skipped.append(
            {
                "project": slug,
                "rank": rank,
                "reason": reason,
                "evidence": [
                    {"task_id": t.get("id"), "title": t.get("title")} for t in evidence
                ],
            }
        )

    return {
        "order_depth": rank,
        "skipped": skipped,
        "landing": landing,
    }


def render(result: dict[str, Any], *, threshold: int) -> str:
    landing = result["landing"]
    skipped = result["skipped"]

    if landing is None:
        lines = [
            "Priority queue starvation: NO project in projects/priority.yaml has any "
            "claimable ready work right now.",
            "",
        ]
        relevant = skipped
    elif landing["rank"] <= threshold:
        return (
            f"Priority queue holds: {landing['project']} (rank {landing['rank']}) has "
            f"claimable ready work within the first {threshold}."
        )
    else:
        lines = [
            f"Priority queue starvation: walked past {len(skipped)} project(s) before "
            f"landing on {landing['project']} at rank {landing['rank']} "
            f"(threshold {threshold}).",
            "",
        ]
        relevant = skipped

    for entry in relevant:
        label = REASON_LABELS.get(entry["reason"], entry["reason"])
        detail = ""
        if entry["evidence"]:
            named = ", ".join(
                f"{e['task_id']} ({e['title']})" if e["title"] else str(e["task_id"])
                for e in entry["evidence"]
            )
            detail = f": {named}"
        lines.append(f"  {entry['rank']}. {entry['project']} — {label}{detail}")

    if landing is not None:
        lines.append("")
        lines.append(f"Landed on {landing['project']} (rank {landing['rank']}).")

    lines.append("")
    lines.append(
        "Advisory only -- this never blocks task selection or gates anything. A "
        "'gated at needs-human' project is worth clearing via audit_human_gates.py; "
        "'all claimed' and 'all waiting-blocked' usually resolve on their own as "
        "in-flight work lands."
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument(
        "--threshold",
        type=int,
        default=DEFAULT_THRESHOLD,
        help=f"exit non-zero only when the landing rank exceeds this (default {DEFAULT_THRESHOLD})",
    )
    args = parser.parse_args()

    result = scan()
    result["threshold"] = args.threshold

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render(result, threshold=args.threshold))

    landing = result["landing"]
    if landing is None:
        sys.exit(1)
    sys.exit(1 if landing["rank"] > args.threshold else 0)


if __name__ == "__main__":
    main()
