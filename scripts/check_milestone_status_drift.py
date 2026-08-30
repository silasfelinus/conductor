#!/usr/bin/env python3
"""
check_milestone_status_drift.py — Flag a milestone whose `status:` field has
drifted from what its own tasks actually say.

Kaizen from cthulhuquarium/t-063 (2026-08-28): a milestone-scope audit found
m3's own `status` field stuck at `not-started` despite 25 of 31 tasks under it
already `done` -- stale since before the bulk of m3's work landed and never
updated as tasks closed. Every roadmap TASK status has some form of
cross-referencing tooling (next_ready_task.py, claim_task.py, select_role.py,
audit_roadmaps.py's INVALID_STATUS check), but milestone status is only ever
READ (build_digest.py, build_digest_email.py for portfolio-percentage math)
and never audited for internal consistency against its own project's task
list. Wrong milestone status doesn't block task selection or gate anything --
it only skews the digest's portfolio-percentage math -- so this is advisory
only, like audit_roadmaps.py's own advisory findings: it never fails CI, it
just reports.

Three mismatch shapes, symmetric with check_pr_merged_drift.py's "roadmap state
must reflect live reality" principle:

  NOT-STARTED WITH DONE WORK: milestone status is a not-yet-started value
  (not-started/pending/waiting) but at least one task under it is `done`.
  This is the m3 shape that prompted this task -- work landed and nobody
  bumped the milestone forward.

  DONE WITH OPEN WORK: milestone status is a done value (done/complete) but
  at least one non-recurring task under it is not `done`. Recurring tasks
  (recurring: true) never reach `done` by design (see AGENTS.md's "Recurring
  tasks" section) and are excluded from this side of the check -- a milestone
  can legitimately be "done" while a recurring polish/upkeep task under it
  keeps cycling forever.

  NON-DONE STATUS WITH ALL WORK DONE: milestone status is anything other than
  a done value while every non-recurring task under it is already `done`.
  This catches stale in-progress/planned/custom status values after their
  finite work has actually finished. Recurring tasks are ignored here for the
  same reason as above: they are standing work and never become `done`.

Excludes paused, retired, and finished projects by default according to
project-overrides.yaml, matching check_pr_merged_drift.py,
check_project_scaffold_drift.py, and audit_human_gates.py. Use
--include-inactive for an intentional archive sweep. Purely local YAML
analysis -- no network access, no KR_API_TOKEN needed.

Usage:
  python scripts/check_milestone_status_drift.py
  python scripts/check_milestone_status_drift.py --json
  python scripts/check_milestone_status_drift.py --include-inactive

Exit codes: 0 = clean (or nothing to check), 1 = at least one mismatch found.
This is advisory -- a non-zero exit is a reconciliation prompt, not a genuine
gate; nothing here blocks a merge or a task claim.
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
OVERRIDES_PATH = ROOT / "project-overrides.yaml"
ACTIVE_STATUS = "active"

# Vocabulary is not fully standardized across roadmaps (seen in the wild:
# not-started/pending/waiting, in-progress/planned/ready, done/complete) --
# stay tolerant rather than hard-failing on an unrecognized value. The third
# finding shape below deliberately treats any non-done status as stale only
# when every finite task under the milestone is already done.
NOT_STARTED_STATUSES = {"not-started", "pending", "waiting"}
DONE_STATUSES = {"done", "complete"}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_project_statuses(path: Path | None = None) -> dict[str, str]:
    path = path or OVERRIDES_PATH
    if not path.exists():
        return {}
    data = load_yaml(path)
    statuses: dict[str, str] = {}
    for entry in data.get("overrides", []) or []:
        if not isinstance(entry, dict):
            continue
        slug = str(entry.get("slug") or "").strip()
        if not slug:
            continue
        statuses[slug] = str(entry.get("status") or ACTIVE_STATUS).strip().lower()
    return statuses


def project_roadmap_paths(
    projects_dir: Path | None = None,
    overrides_path: Path | None = None,
    include_inactive: bool = False,
) -> list[Path]:
    projects_dir = projects_dir or PROJECTS_DIR
    statuses = load_project_statuses(overrides_path)
    paths = []
    for path in sorted(projects_dir.glob("*/roadmap.yaml")):
        slug = path.parent.name
        if slug == "_template":
            continue
        if not include_inactive and statuses.get(slug, ACTIVE_STATUS) != ACTIVE_STATUS:
            continue
        paths.append(path)
    return paths


def milestone_findings(project: str, roadmap: dict[str, Any]) -> list[dict[str, Any]]:
    """Return mismatch findings for one project's milestones vs. its tasks."""
    milestones = {
        str(m.get("id")): m
        for m in (roadmap.get("milestones") or [])
        if isinstance(m, dict) and m.get("id")
    }
    if not milestones:
        return []

    tasks_by_milestone: dict[str, list[dict[str, Any]]] = {}
    for task in roadmap.get("tasks") or []:
        if not isinstance(task, dict):
            continue
        milestone_id = str(task.get("milestone") or "")
        if milestone_id:
            tasks_by_milestone.setdefault(milestone_id, []).append(task)

    findings = []
    for milestone_id, milestone in milestones.items():
        tasks = tasks_by_milestone.get(milestone_id) or []
        if not tasks:
            continue
        status = str(milestone.get("status") or "").strip().lower()
        done_tasks = [t for t in tasks if str(t.get("status") or "").strip().lower() == "done"]
        finite_tasks = [t for t in tasks if not t.get("recurring")]
        open_non_recurring = [
            t
            for t in finite_tasks
            if str(t.get("status") or "").strip().lower() != "done"
        ]

        if status in NOT_STARTED_STATUSES and done_tasks:
            findings.append(
                {
                    "project": project,
                    "milestone": milestone_id,
                    "title": milestone.get("title"),
                    "milestone_status": milestone.get("status"),
                    "shape": "not-started-with-done-work",
                    "done_task_count": len(done_tasks),
                    "total_task_count": len(tasks),
                    "detail": (
                        f"milestone status is {milestone.get('status')!r} but "
                        f"{len(done_tasks)}/{len(tasks)} of its tasks are already done"
                    ),
                }
            )
        elif status in DONE_STATUSES and open_non_recurring:
            findings.append(
                {
                    "project": project,
                    "milestone": milestone_id,
                    "title": milestone.get("title"),
                    "milestone_status": milestone.get("status"),
                    "shape": "done-with-open-work",
                    "open_task_count": len(open_non_recurring),
                    "total_task_count": len(tasks),
                    "detail": (
                        f"milestone status is {milestone.get('status')!r} but "
                        f"{len(open_non_recurring)}/{len(tasks)} of its non-recurring "
                        "tasks are not done"
                    ),
                }
            )
        elif (
            status not in DONE_STATUSES
            and finite_tasks
            and not open_non_recurring
        ):
            findings.append(
                {
                    "project": project,
                    "milestone": milestone_id,
                    "title": milestone.get("title"),
                    "milestone_status": milestone.get("status"),
                    "shape": "not-done-status-with-all-work-done",
                    "done_task_count": len(finite_tasks),
                    "total_task_count": len(tasks),
                    "detail": (
                        f"milestone status is {milestone.get('status')!r} but all "
                        f"{len(finite_tasks)} non-recurring task(s) are already done"
                    ),
                }
            )
    return findings


def scan(
    projects_dir: Path | None = None,
    overrides_path: Path | None = None,
    include_inactive: bool = False,
) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    for path in project_roadmap_paths(projects_dir, overrides_path, include_inactive):
        project = path.parent.name
        try:
            roadmap = load_yaml(path)
        except yaml.YAMLError as error:  # noqa: BLE001 - report, don't crash the sweep
            findings.append(
                {
                    "project": project,
                    "milestone": None,
                    "title": None,
                    "milestone_status": None,
                    "shape": "unparseable-roadmap",
                    "detail": f"{path.relative_to(ROOT)} failed to parse: {error}",
                }
            )
            continue
        findings.extend(milestone_findings(project, roadmap))
    return {"findings": findings}


def render(result: dict[str, Any]) -> str:
    findings = result["findings"]
    if not findings:
        return "No milestone status drift found — every milestone's status agrees with its own task list."
    lines = [f"Milestone status drift ({len(findings)}):"]
    for f in findings:
        if f["shape"] == "unparseable-roadmap":
            lines.append(f"  - {f['project']}: {f['detail']}")
            continue
        lines.append(
            f"  - {f['project']}/{f['milestone']} {f['title']!r}: {f['detail']}"
        )
    lines.append(
        "\nAdvisory only -- wrong milestone status doesn't block task selection or "
        "gate anything, it only skews the digest's portfolio-percentage math. Fix by "
        "editing the milestone's status: field to match its actual task-done fraction."
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument(
        "--include-inactive",
        action="store_true",
        help="also check paused, retired, and finished projects",
    )
    args = parser.parse_args()

    result = scan(include_inactive=args.include_inactive)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render(result))

    sys.exit(1 if result["findings"] else 0)


if __name__ == "__main__":
    main()
