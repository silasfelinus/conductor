#!/usr/bin/env python3
"""
check_daily_commitment_staleness.py — flag a `daily_commitment: true` task
whose own upkeep has gone stale, the same way check_priority_queue_starvation.py
flags a starved priority queue.

Kaizen from animation-manager/t-020 (silasfelinus/conductor#5108, 2026-09-23,
conductor/t-194). select_role.py's `daily-creative` role
(find_due_daily_commitments()) surfaces a `daily_commitment: true` task the
moment its `daily_last_checked` predates today's Pacific date -- but that is a
one-shot selection trigger, not a report. "Checked today, honest no-op" and "a
session claimed it and stalled" or "nobody ran the role in days" all look
identical from the roadmap alone once a session is mid-claim, and nothing
surfaces HOW stale a daily task has actually become.

Two independent findings, either or both may fire on the same task:

  STALE CHECK: `daily_last_checked` is missing, or more than `--stale-days`
  (default 2) before today's Pacific date. A daily commitment is meant to be
  touched every Pacific calendar day -- an honest no-op still advances
  `daily_last_checked`, so silence past the threshold means the role stopped
  firing for this task, not that there was nothing to check.

  STALLED CLAIM: `status: claimed` with a `claimed_at` old enough that
  roadmap_claims.claim_is_stale() already treats it as abandoned (the same
  90-minute CLAIM_TTL_MINUTES claim_task.py/next_ready_task.py use elsewhere)
  -- several times a normal session's lifetime, with no closing PR.

Advisory only, same discipline as check_priority_queue_starvation.py and
check_milestone_status_drift.py: never blocks task selection or gates
anything. Excludes paused/retired/finished projects by default per
project-overrides.yaml, matching the other roadmap-reading checks;
--include-inactive for an intentional archive sweep. Purely local YAML
analysis -- no network access, no KR_API_TOKEN needed.

Usage:
  python scripts/check_daily_commitment_staleness.py
  python scripts/check_daily_commitment_staleness.py --json
  python scripts/check_daily_commitment_staleness.py --stale-days 3
  python scripts/check_daily_commitment_staleness.py --include-inactive

Exit codes: 0 = clean (or nothing to check), 1 = at least one daily_commitment
task flagged.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT / "projects"
OVERRIDES_PATH = ROOT / "project-overrides.yaml"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from project_lifecycle import load_project_overrides, lifecycle_status  # noqa: E402
from roadmap_claims import CLAIM_TTL_MINUTES, claim_is_stale, parse_timestamp  # noqa: E402
from select_role import PACIFIC_TZ, _extract_date  # noqa: E402

DEFAULT_STALE_DAYS = 2


def load_yaml(path: Path) -> Any:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def project_roadmap_paths(
    projects_dir: Path | None = None,
    overrides_path: Path | None = None,
    include_inactive: bool = False,
) -> list[Path]:
    projects_dir = projects_dir or PROJECTS_DIR
    overrides = load_project_overrides(overrides_path or OVERRIDES_PATH)
    paths = []
    for path in sorted(projects_dir.glob("*/roadmap.yaml")):
        slug = path.parent.name
        if slug == "_template":
            continue
        if not include_inactive and lifecycle_status(overrides, slug) not in (
            "active",
            "continuous",
        ):
            continue
        paths.append(path)
    return paths


def today_pacific(*, now: datetime | None = None) -> date:
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    return now.astimezone(PACIFIC_TZ).date()


def scan(
    *,
    projects_dir: Path | None = None,
    overrides_path: Path | None = None,
    include_inactive: bool = False,
    stale_days: int = DEFAULT_STALE_DAYS,
    now: datetime | None = None,
) -> list[dict[str, Any]]:
    today = today_pacific(now=now)
    reference = now or datetime.now(timezone.utc)
    if reference.tzinfo is None:
        reference = reference.replace(tzinfo=timezone.utc)

    findings: list[dict[str, Any]] = []

    for path in project_roadmap_paths(projects_dir, overrides_path, include_inactive):
        roadmap = load_yaml(path)
        if not isinstance(roadmap, dict):
            continue
        project = roadmap.get("project") or path.parent.name

        for task in roadmap.get("tasks", []) or []:
            if not isinstance(task, dict) or not task.get("daily_commitment"):
                continue

            issues: list[dict[str, Any]] = []

            raw_checked = task.get("daily_last_checked")
            last_checked = (
                _extract_date(str(raw_checked)) if raw_checked is not None else None
            )
            if last_checked is None:
                issues.append(
                    {"type": "stale-check", "days_since": None, "last_checked": None}
                )
            else:
                days_since = (today - last_checked).days
                if days_since >= stale_days:
                    issues.append(
                        {
                            "type": "stale-check",
                            "days_since": days_since,
                            "last_checked": last_checked.isoformat(),
                        }
                    )

            if task.get("status") == "claimed":
                claimed_at = task.get("claimed_at")
                if claim_is_stale(claimed_at, now=reference):
                    parsed = parse_timestamp(claimed_at)
                    minutes_since = (
                        round((reference - parsed).total_seconds() / 60)
                        if parsed is not None
                        else None
                    )
                    issues.append(
                        {
                            "type": "stalled-claim",
                            "claimed_at": claimed_at,
                            "minutes_since": minutes_since,
                            "ttl_minutes": CLAIM_TTL_MINUTES,
                        }
                    )

            if issues:
                findings.append(
                    {
                        "project": project,
                        "task_id": task.get("id"),
                        "title": task.get("title"),
                        "status": task.get("status"),
                        "issues": issues,
                    }
                )

    return findings


def render(findings: list[dict[str, Any]]) -> str:
    if not findings:
        return (
            "No daily_commitment task staleness found -- every daily task's own "
            "upkeep is current."
        )

    lines = [f"Daily commitment staleness: {len(findings)} task(s) flagged.", ""]
    for entry in findings:
        lines.append(
            f"  {entry['project']}/{entry['task_id']} [{entry['status']}] {entry['title']}"
        )
        for issue in entry["issues"]:
            if issue["type"] == "stale-check":
                if issue["last_checked"] is None:
                    lines.append("      STALE CHECK: daily_last_checked is missing")
                else:
                    lines.append(
                        f"      STALE CHECK: daily_last_checked={issue['last_checked']} "
                        f"({issue['days_since']} day(s) stale)"
                    )
            elif issue["type"] == "stalled-claim":
                lines.append(
                    f"      STALLED CLAIM: claimed_at={issue['claimed_at']} "
                    f"({issue['minutes_since']} min since, TTL {issue['ttl_minutes']} min)"
                )
        lines.append("")

    lines.append(
        "Advisory only -- this never blocks task selection or gates anything. A "
        "STALE CHECK usually means the daily-creative role stopped firing for this "
        "task; a STALLED CLAIM usually means a session claimed it and never closed "
        "out."
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument(
        "--include-inactive",
        action="store_true",
        help="also scan paused/retired/finished projects",
    )
    parser.add_argument(
        "--stale-days",
        type=int,
        default=DEFAULT_STALE_DAYS,
        help=f"days before a stale daily_last_checked is flagged (default {DEFAULT_STALE_DAYS})",
    )
    args = parser.parse_args()

    findings = scan(include_inactive=args.include_inactive, stale_days=args.stale_days)

    if args.json:
        print(json.dumps(findings, indent=2))
    else:
        print(render(findings))

    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
