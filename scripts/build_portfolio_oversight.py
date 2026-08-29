#!/usr/bin/env python3
"""Build a compact portfolio-oversight report for scheduled Conductor agents.

This composes three signals that previously lived in separate places or were not
surfaced to agent rotation at all:

* Kind Robots <-> Conductor project scaffold parity.
* Deterministic roadmap/CONTROL/priority findings from audit_roadmaps.py.
* Freshness of both external scheduled-Agent activity and the periodic semantic
  roadmap-intent review described in projects/conductor/OVERSIGHT-AGENT.md.

The script is intentionally read-only except for the two report files it writes.
It never repairs roadmap state itself. GitHub Actions has KR_API_TOKEN and persists
these reports so connector-only agents can consume the live parity result without
requiring production API credentials in their own session.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import audit_roadmaps  # noqa: E402
import check_project_scaffold_drift as scaffold_drift  # noqa: E402

INTENT_DIR = ROOT / "projects" / "conductor"
INTENT_REPORT_RE = re.compile(r"^INTENT-AUDIT-(\d{4}-\d{2}-\d{2})\.md$")
DEFAULT_INTENT_STALE_DAYS = 3.0
DEFAULT_AGENT_HEARTBEAT_HOURS = 6.0


def _parse_iso_datetime(value: str) -> datetime | None:
    value = value.strip()
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def latest_intent_report(directory: Path = INTENT_DIR) -> tuple[str, date] | None:
    if not directory.is_dir():
        return None
    found: list[tuple[str, date]] = []
    for path in directory.iterdir():
        match = INTENT_REPORT_RE.match(path.name)
        if not match:
            continue
        try:
            found.append((path.name, date.fromisoformat(match.group(1))))
        except ValueError:
            continue
    return max(found, key=lambda item: item[1]) if found else None


def intent_review_status(
    *,
    directory: Path = INTENT_DIR,
    stale_days: float = DEFAULT_INTENT_STALE_DAYS,
    today: date | None = None,
) -> dict[str, Any]:
    today = today or datetime.now(timezone.utc).date()
    latest = latest_intent_report(directory)
    if latest is None:
        return {"due": True, "last_report": None, "days_since": None, "stale_days": stale_days}
    name, report_date = latest
    days_since = (today - report_date).days
    return {
        "due": days_since >= stale_days,
        "last_report": name,
        "days_since": days_since,
        "stale_days": stale_days,
    }


def _scheduled_git_log() -> str:
    """Return the newest commit date that visibly came from a scheduled Agent.

    We cannot query the external scheduler from inside the repo, so this is a
    heartbeat, not a proof-of-scheduler API. The patterns match the session ids and
    prose already used by Conductor's scheduled Claude runs.
    """
    result = subprocess.run(
        [
            "git",
            "log",
            "--all",
            "-1",
            "--regexp-ignore-case",
            "--grep=claude-scheduled",
            "--grep=scheduled Agent run",
            "--grep=scheduled sweep",
            "--format=%cI",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def scheduled_agent_status(
    *,
    stale_hours: float = DEFAULT_AGENT_HEARTBEAT_HOURS,
    now: datetime | None = None,
    log_output: str | None = None,
) -> dict[str, Any]:
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    raw = _scheduled_git_log() if log_output is None else log_output
    last = _parse_iso_datetime(raw)
    if last is None:
        return {
            "overdue": True,
            "last_activity": None,
            "hours_since": None,
            "stale_hours": stale_hours,
            "note": "No scheduled-Agent heartbeat commit was found in available git history.",
        }
    hours_since = max(0.0, (now - last).total_seconds() / 3600.0)
    return {
        "overdue": hours_since >= stale_hours,
        "last_activity": last.isoformat(),
        "hours_since": round(hours_since, 2),
        "stale_hours": stale_hours,
        "note": "Commit activity is a heartbeat only; a clean no-op scheduled cycle may leave no commit.",
    }


def classify_report(
    *,
    roadmap_report: dict[str, Any],
    project_scan: dict[str, list[dict[str, Any]]] | None,
    project_unresolved: str | None,
    heartbeat: dict[str, Any],
    intent: dict[str, Any],
) -> dict[str, Any]:
    roadmap_errors = int((roadmap_report.get("summary") or {}).get("errors", 0) or 0)
    roadmap_warnings = int((roadmap_report.get("summary") or {}).get("warnings", 0) or 0)
    forward = list((project_scan or {}).get("forward", []))
    reverse = list((project_scan or {}).get("reverse", []))

    deterministic_action = bool(
        roadmap_errors
        or forward
        or reverse
        or heartbeat.get("overdue")
    )
    if deterministic_action:
        status = "action-needed"
    elif project_unresolved:
        status = "unresolved"
    elif intent.get("due"):
        status = "semantic-review-due"
    else:
        status = "clean"

    return {
        "status": status,
        "roadmap_errors": roadmap_errors,
        "roadmap_warnings": roadmap_warnings,
        "project_forward_drift": len(forward),
        "project_reverse_orphans": len(reverse),
        "project_unresolved": project_unresolved,
        "scheduled_agent_overdue": bool(heartbeat.get("overdue")),
        "intent_review_due": bool(intent.get("due")),
    }


def build_report(
    *,
    token: str | None = None,
    intent_stale_days: float = DEFAULT_INTENT_STALE_DAYS,
    agent_heartbeat_hours: float = DEFAULT_AGENT_HEARTBEAT_HOURS,
) -> dict[str, Any]:
    generated_at = datetime.now(timezone.utc)
    roadmap_report = audit_roadmaps.audit()
    heartbeat = scheduled_agent_status(stale_hours=agent_heartbeat_hours, now=generated_at)
    intent = intent_review_status(stale_days=intent_stale_days, today=generated_at.date())

    project_scan: dict[str, list[dict[str, Any]]] | None = None
    project_unresolved: str | None = None
    token = (token if token is not None else os.environ.get("KR_API_TOKEN", "")).strip()
    if not token:
        project_unresolved = "KR_API_TOKEN not set; Kind Robots project parity was not verified."
    else:
        try:
            kr_projects = scaffold_drift.fetch_kind_robots_projects(token)
            project_scan = scaffold_drift.scan(kr_projects)
        except Exception as error:  # noqa: BLE001 - unresolved must remain visible
            project_unresolved = f"Kind Robots project parity check failed: {type(error).__name__}: {error}"

    summary = classify_report(
        roadmap_report=roadmap_report,
        project_scan=project_scan,
        project_unresolved=project_unresolved,
        heartbeat=heartbeat,
        intent=intent,
    )

    return {
        "generated_at": generated_at.isoformat(),
        "summary": summary,
        "scheduled_agent": heartbeat,
        "intent_review": intent,
        "project_parity": {
            "forward": list((project_scan or {}).get("forward", [])),
            "reverse": list((project_scan or {}).get("reverse", [])),
            "unresolved": project_unresolved,
        },
        "roadmap_audit": {
            "generated_at": roadmap_report.get("generated_at"),
            "summary": roadmap_report.get("summary", {}),
            "errors": [
                item for item in roadmap_report.get("findings", []) if item.get("severity") == "error"
            ],
            "warnings": [
                item for item in roadmap_report.get("findings", []) if item.get("severity") == "warning"
            ],
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    heartbeat = report["scheduled_agent"]
    intent = report["intent_review"]
    parity = report["project_parity"]
    roadmap = report["roadmap_audit"]

    lines = [
        "# Conductor Portfolio Oversight",
        "",
        f"Generated: `{report['generated_at']}`",
        "",
        f"Overall status: **{summary['status']}**",
        "",
        "This is a deterministic sensor. For semantic roadmap/progress intent review, follow `projects/conductor/OVERSIGHT-AGENT.md`.",
        "",
        "## Scheduled-agent heartbeat",
        "",
    ]
    if heartbeat["last_activity"]:
        lines.append(
            f"- Latest visible scheduled-Agent activity: `{heartbeat['last_activity']}` "
            f"({heartbeat['hours_since']}h ago; overdue at {heartbeat['stale_hours']}h)."
        )
    else:
        lines.append("- No scheduled-Agent heartbeat commit found in available history.")
    lines.append(f"- Overdue: **{str(bool(heartbeat['overdue'])).lower()}**")
    lines.append(f"- Note: {heartbeat['note']}")

    lines.extend(["", "## Kind Robots ↔ Conductor project parity", ""])
    if parity["unresolved"]:
        lines.append(f"- **UNRESOLVED:** {parity['unresolved']}")
    else:
        lines.append(f"- Forward drift (KR row claims missing roadmap): **{len(parity['forward'])}**")
        lines.append(f"- Reverse orphans (active Conductor roadmap missing KR row): **{len(parity['reverse'])}**")
    for item in parity["forward"]:
        lines.append(
            f"  - `{item.get('conductor_slug')}` claimed by KR Project #{item.get('kr_project_id')} "
            f"{item.get('kr_title')!r}, but the roadmap is missing."
        )
    for item in parity["reverse"]:
        lines.append(f"  - `{item.get('conductor_slug')}` has no matching Kind Robots `conductorSlug` row.")

    rsum = roadmap.get("summary") or {}
    lines.extend(
        [
            "",
            "## Roadmap/CONTROL structural audit",
            "",
            f"- Errors: **{rsum.get('errors', 0)}**",
            f"- Warnings: **{rsum.get('warnings', 0)}**",
        ]
    )
    for item in roadmap["errors"]:
        location = f"`{item.get('project')}`"
        if item.get("task"):
            location += f" / `{item.get('task')}`"
        lines.append(f"  - **{item.get('code')}** — {location}: {item.get('message')}")
    if roadmap["warnings"]:
        lines.append("- Warning details remain in `ROADMAP-AUDIT.md`; errors above take precedence for this sensor.")

    lines.extend(["", "## Semantic intent review", ""])
    if intent["last_report"]:
        lines.append(
            f"- Latest: `{intent['last_report']}` ({intent['days_since']} day(s) ago; due at {intent['stale_days']} days)."
        )
    else:
        lines.append("- No completed `INTENT-AUDIT-YYYY-MM-DD.md` report exists yet.")
    lines.append(f"- Due: **{str(bool(intent['due'])).lower()}**")

    lines.extend(
        [
            "",
            "## Agent routing",
            "",
            "When action is needed, use `projects/conductor/OVERSIGHT-AGENT.md` before falling through to ordinary Worker/Reviewer selection.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", default="PORTFOLIO-OVERSIGHT.json")
    parser.add_argument("--markdown", default="PORTFOLIO-OVERSIGHT.md")
    parser.add_argument("--intent-stale-days", type=float, default=DEFAULT_INTENT_STALE_DAYS)
    parser.add_argument("--agent-heartbeat-hours", type=float, default=DEFAULT_AGENT_HEARTBEAT_HOURS)
    parser.add_argument(
        "--fail-on-action",
        action="store_true",
        help="exit non-zero when deterministic action, unresolved parity, or semantic review is due",
    )
    args = parser.parse_args()

    report = build_report(
        intent_stale_days=args.intent_stale_days,
        agent_heartbeat_hours=args.agent_heartbeat_hours,
    )
    (ROOT / args.json).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (ROOT / args.markdown).write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))

    if not args.fail_on_action:
        return 0
    if report["summary"]["status"] == "unresolved":
        return 2
    if report["summary"]["status"] in {"action-needed", "semantic-review-due"}:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
