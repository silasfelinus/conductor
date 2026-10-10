#!/usr/bin/env python3
"""Decide whether a portfolio-oversight result should escalate to email.

The oversight report is an agent-routing signal first. Deterministic failures and
unresolved parity retain their existing escalation rules. A due semantic intent
review is *work to dispatch*, not an incident: only an explicit failed attempt,
recorded after the most recent successful audit, justifies a semantic email.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPEAT_ALERT_HOURS = 24


def incident_signature(report: dict[str, Any]) -> str:
    """Stable actionable sensors, excluding timestamps, counts, and legacy heartbeat."""
    summary = report.get("summary") or {}
    payload = {
        "status": summary.get("status"),
        "project_unresolved": summary.get("project_unresolved"),
        "forward": sorted(str(item.get("conductor_slug")) for item in (report.get("project_parity") or {}).get("forward", [])),
        "reverse": sorted(str(item.get("conductor_slug")) for item in (report.get("project_parity") or {}).get("reverse", [])),
        "roadmap_errors": sorted(str(item.get("code")) + ":" + str(item.get("project")) for item in (report.get("roadmap_audit") or {}).get("errors", [])),
        "intent_review_failure": (report.get("intent_review") or {}).get("failed_attempt"),
    }
    return json.dumps(payload, sort_keys=True)


def should_notify(report: dict[str, Any], previous: dict[str, Any] | None, now: datetime) -> bool:
    if not should_email(report):
        return False
    if not previous or previous.get("signature") != incident_signature(report):
        return True
    try:
        sent_at = datetime.fromisoformat(previous["sent_at"].replace("Z", "+00:00"))
        return (now - sent_at).total_seconds() >= REPEAT_ALERT_HOURS * 3600
    except (KeyError, TypeError, ValueError):
        return True



def should_email(report: dict[str, Any]) -> bool:
    status = str((report.get("summary") or {}).get("status") or "")
    if status in {"action-needed", "unresolved"}:
        return True
    if status != "semantic-review-due":
        return False

    # The overdue signal routes scheduled agents. It does not page a human
    # until at least one actual review attempt failed and that failure is
    # newer than the last successful review (validated by the report builder).
    failure = (report.get("intent_review") or {}).get("failed_attempt")
    return isinstance(failure, dict) and failure.get("status") == "failed" and bool(
        failure.get("attempted_at") and failure.get("reason")
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", nargs="?", default="PORTFOLIO-OVERSIGHT.json")
    parser.add_argument("--state", type=Path, default=Path("PORTFOLIO-OVERSIGHT-EMAIL-STATE.json"))
    parser.add_argument("--record", action="store_true", help="record a successfully delivered alert")
    args = parser.parse_args()

    report = json.loads(Path(args.report).read_text(encoding="utf-8"))
    now = datetime.now(timezone.utc)
    if args.record:
        args.state.write_text(json.dumps({"signature": incident_signature(report), "sent_at": now.isoformat()}, indent=2) + "\n", encoding="utf-8")
        return 0
    previous = json.loads(args.state.read_text(encoding="utf-8")) if args.state.exists() else None
    eligible = should_email(report)
    print("true" if eligible and should_notify(report, previous, now) else "false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
