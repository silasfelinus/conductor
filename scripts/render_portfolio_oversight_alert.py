#!/usr/bin/env python3
"""Render a human-readable email explanation for a portfolio oversight alert.

The oversight workflow intentionally detects conditions that need agent attention. Those
conditions are not the same thing as the workflow itself crashing, so the email should
say exactly which sensor fired instead of relying on GitHub's generic "run failed" mail.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _plural(count: int, singular: str, plural: str | None = None) -> str:
    return singular if count == 1 else (plural or singular + "s")


def alert_subject(report: dict[str, Any]) -> str:
    summary = report.get("summary") or {}
    heartbeat = report.get("openai_scheduled_agent") or {}
    parity = report.get("project_parity") or {}
    roadmap = report.get("roadmap_audit") or {}
    intent = report.get("intent_review") or {}

    if heartbeat.get("overdue"):
        return "Conductor Oversight: scheduled agent heartbeat overdue"
    errors = int((roadmap.get("summary") or {}).get("errors", 0) or 0)
    if errors:
        return f"Conductor Oversight: {errors} roadmap {_plural(errors, 'error')}"
    if parity.get("unresolved"):
        return "Conductor Oversight: project parity check unresolved"
    drift = len(parity.get("forward") or []) + len(parity.get("reverse") or [])
    if drift:
        return f"Conductor Oversight: {drift} project parity {_plural(drift, 'mismatch', 'mismatches')}"
    if intent.get("due"):
        return "Conductor Oversight: semantic intent review due"
    return f"Conductor Oversight: {summary.get('status') or 'attention needed'}"


def alert_body(report: dict[str, Any], *, run_url: str = "") -> str:
    summary = report.get("summary") or {}
    heartbeat = report.get("openai_scheduled_agent") or {}
    parity = report.get("project_parity") or {}
    roadmap = report.get("roadmap_audit") or {}
    intent = report.get("intent_review") or {}

    reasons: list[str] = []
    if heartbeat.get("overdue"):
        last = heartbeat.get("last_activity")
        hours = heartbeat.get("hours_since")
        threshold = heartbeat.get("stale_hours")
        if last:
            reasons.append(
                "OpenAI scheduled-agent heartbeat is overdue: "
                f"last visible activity was {last} ({hours}h ago; threshold {threshold}h)."
            )
        else:
            reasons.append(
                "OpenAI scheduled-agent heartbeat is overdue: no commit carrying the expected "
                f"{heartbeat.get('marker') or 'openai-scheduled-'} session marker was found."
            )

    errors = list(roadmap.get("errors") or [])
    for item in errors:
        location = str(item.get("project") or "unknown project")
        if item.get("task"):
            location += f"/{item['task']}"
        code = item.get("code") or "ROADMAP_ERROR"
        reasons.append(f"Roadmap audit {code} at {location}: {item.get('message') or 'error'}")

    unresolved = parity.get("unresolved")
    if unresolved:
        reasons.append(f"Kind Robots ↔ Conductor project parity could not be verified: {unresolved}")
    for item in parity.get("forward") or []:
        reasons.append(
            "Kind Robots project parity drift: "
            f"{item.get('conductor_slug') or 'unknown slug'} is claimed in Kind Robots but has no roadmap."
        )
    for item in parity.get("reverse") or []:
        reasons.append(
            "Kind Robots project parity drift: "
            f"{item.get('conductor_slug') or 'unknown slug'} has a Conductor roadmap but no matching Kind Robots row."
        )

    if intent.get("due"):
        latest = intent.get("last_report") or "no completed intent audit"
        reasons.append(
            "Semantic roadmap intent review is due: "
            f"latest report is {latest}; review interval is {intent.get('stale_days')} day(s)."
        )

    if not reasons:
        reasons.append(
            f"The oversight report returned status {summary.get('status') or 'unknown'} but did not expose a more specific reason."
        )

    warnings = int((roadmap.get("summary") or {}).get("warnings", 0) or 0)
    lines = [
        "Conductor Oversight found something that needs attention.",
        "",
        "Why this email was sent:",
        *[f"- {reason}" for reason in reasons],
        "",
        f"Overall sensor status: {summary.get('status') or 'unknown'}",
    ]
    if warnings:
        lines.append(
            f"Context: {warnings} roadmap {_plural(warnings, 'warning')} also present; warnings alone do not trigger this alert."
        )
    lines.extend(
        [
            "",
            "The full details are persisted in PORTFOLIO-OVERSIGHT.md and the workflow artifact.",
        ]
    )
    if run_url:
        lines.append(f"Workflow run: {run_url}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", nargs="?", default="PORTFOLIO-OVERSIGHT.json")
    parser.add_argument("--subject", action="store_true", help="print only the email subject")
    parser.add_argument("--run-url", default="")
    args = parser.parse_args()

    report = json.loads(Path(args.report).read_text(encoding="utf-8"))
    if args.subject:
        print(alert_subject(report))
    else:
        print(alert_body(report, run_url=args.run_url), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
