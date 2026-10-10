"""Inspect *actual* GitHub Actions semantic-review attempts; staleness is not failure."""
from __future__ import annotations
import json
import urllib.request
from datetime import date, datetime, timedelta, timezone
from typing import Any


def _timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def latest_attempt(runs: list[dict[str, Any]], report_date: date | None) -> dict | None:
    # A failure predating the last successful report must never page again.
    earliest = (report_date + timedelta(days=3)) if report_date else date.min
    eligible = [
        r for r in runs if r.get("created_at") and
        _timestamp(r["created_at"]).date() >= earliest
    ]
    return max(eligible, key=lambda r: r["created_at"]) if eligible else None


def failed_attempt(runs: list[dict[str, Any]], report_date: date | None) -> dict | None:
    latest = latest_attempt(runs, report_date)
    if not latest or latest.get("status") != "completed":
        return None
    conclusion = latest.get("conclusion")
    if conclusion not in ("failure", "timed_out", "startup_failure", "action_required"):
        return None
    return {
        "status": "failed",
        "attempted_at": latest.get("run_started_at") or latest["created_at"],
        "reason": ("GitHub scheduled semantic review " + str(conclusion)
                   + ": " + str(latest.get("html_url") or "workflow run")),
    }


def fetch_runs(token: str, repository: str) -> list[dict[str, Any]]:
    # Uses only the ephemeral Actions token. No token is serialized or logged.
    if not token or not repository:
        raise ValueError("GitHub Actions token and repository are required")
    url = ("https://api.github.com/repos/" + repository +
           "/actions/workflows/semantic-intent-review.yml/runs?per_page=40")
    req = urllib.request.Request(url, headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.load(resp)
    if not isinstance(result.get("workflow_runs"), list):
        raise ValueError("Invalid GitHub workflow-runs response")
    return result["workflow_runs"]


def recent_attempt(runs: list[dict[str, Any]], now: datetime, hours: int = 18) -> bool:
    return any(
        r.get("created_at") and
        (now - _timestamp(r["created_at"])).total_seconds() < hours * 3600
        for r in runs
    )
