#!/usr/bin/env python3
"""Dispatch a real GitHub semantic review if due and no recent attempt exists."""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
# Support both module imports in pytest and execution as scripts/foo.py in Actions.
from scripts import semantic_intent_actions as actions


def ensure(report, token, repo, now):
    if not report.get("intent_review", {}).get("due"):
        return "current"
    runs = actions.fetch_runs(token, repo)
    if actions.recent_attempt(runs, now, hours=18):
        return "already-attempted"
    url = ("https://api.github.com/repos/" + repo +
           "/actions/workflows/semantic-intent-review.yml/dispatches")
    request = urllib.request.Request(
        url, data=json.dumps({"ref": "main"}).encode("utf-8"), method="POST",
        headers={"Authorization": "Bearer " + token,
                 "Accept": "application/vnd.github+json",
                 "Content-Type": "application/json",
                 "X-GitHub-Api-Version": "2022-11-28"},
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        if response.status != 204:
            raise RuntimeError("GitHub workflow dispatch returned non-204 status")
    return "dispatched"


def main():
    token = os.environ.get("GITHUB_TOKEN", "")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    report = json.loads(Path("PORTFOLIO-OVERSIGHT.json").read_text())
    if not report.get("intent_review", {}).get("due"):
        print("Semantic review current; no dispatch required")
        return 0
    if not token or not repo:
        print("::error::Cannot dispatch semantic review: Actions token/repo absent", file=sys.stderr)
        return 1
    try:
        result = ensure(report, token, repo, datetime.now(timezone.utc))
        print("Semantic review dispatcher: " + result)
        return 0
    except Exception as error:
        # No secrets or remote response body may appear in logs.
        print("::error::Semantic review dispatch failed: " + type(error).__name__, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
