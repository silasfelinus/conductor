#!/usr/bin/env python3
"""Decide whether a portfolio-oversight result should escalate to email.

The oversight report is an agent-routing signal first. Deterministic failures and
unresolved parity still escalate immediately, but a routine semantic intent review
gets a grace window so the next scheduled agents can perform the audit before Silas
is emailed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DEFAULT_INTENT_EMAIL_GRACE_DAYS = 1.0


def should_email(
    report: dict[str, Any],
    *,
    intent_email_grace_days: float = DEFAULT_INTENT_EMAIL_GRACE_DAYS,
) -> bool:
    status = str((report.get("summary") or {}).get("status") or "")
    if status in {"action-needed", "unresolved"}:
        return True
    if status != "semantic-review-due":
        return False

    intent = report.get("intent_review") or {}
    days_since = intent.get("days_since")
    stale_days = float(intent.get("stale_days") or 0.0)

    # No baseline audit is exceptional rather than routine staleness, so do not
    # suppress the only external signal indefinitely.
    if days_since is None:
        return True

    return float(days_since) >= stale_days + intent_email_grace_days


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", nargs="?", default="PORTFOLIO-OVERSIGHT.json")
    parser.add_argument(
        "--intent-email-grace-days",
        type=float,
        default=DEFAULT_INTENT_EMAIL_GRACE_DAYS,
        help="days after semantic review first becomes due before email escalation",
    )
    args = parser.parse_args()

    report = json.loads(Path(args.report).read_text(encoding="utf-8"))
    print(
        "true"
        if should_email(report, intent_email_grace_days=args.intent_email_grace_days)
        else "false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
