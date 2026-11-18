#!/usr/bin/env python3
"""Close a game's master roadmap issue only after the actual playtest handoff.

Conductor lifecycle and finite roadmap verification are authoritative. The issue is flagged and
closed as completed to clear the open roadmap backlog, but no human verdict or
publication permission is implied.
Run from the Conductor root, using ISSUE_BRIDGE_TOKEN for cross-repository writes.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
import urllib.request

import yaml

try:
    from project_lifecycle import load_project_overrides
    from playtest_readiness import playtest_readiness_errors, pending_agent_owned_task_ids
except ModuleNotFoundError:
    from scripts.project_lifecycle import load_project_overrides
    from scripts.playtest_readiness import playtest_readiness_errors, pending_agent_owned_task_ids

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "[FLAGGED FOR HUMAN TESTING] "
MASTER_URL = re.compile(r"^https://github\.com/silasfelinus/kind_robots/issues/(\d+)$")


def explicitly_waived_owner_playtest(slug: str, config: dict, tasks: list[dict], errors: list[str]) -> bool:
    """One documented owner decision can accept known open tasks, never unknown tasks.

    This is a narrow early-access exception for Downward Mobility, not a way
    to turn unfinished ordinary project roadmaps into approved playtests.
    """
    waiver = config.get("early_playtest_owner_waiver")
    if slug != "shifting-desks" or not isinstance(waiver, dict):
        return False
    if waiver.get("approved_by") != "Silas" or str(waiver.get("approved_on")) != "2026-11-17":
        return False
    if not waiver.get("handoff") or not waiver.get("direction"):
        return False
    known = waiver.get("known_open_tasks")
    if not isinstance(known, list) or len(known) != len(set(map(str, known))):
        return False
    if not all(isinstance(task_id, str) and task_id.startswith("t-") for task_id in known):
        return False
    pending = pending_agent_owned_task_ids(tasks)
    expected_error = "agent-owned tasks still open: " + ", ".join(pending[:12])
    return bool(pending) and errors == [expected_error] and set(pending).issubset(set(known))


def eligible_issues(overrides: dict, masters: dict, roadmaps_dir: Path) -> tuple[list[tuple[str, int]], list[str]]:
    changes = []
    problems = []
    for slug, config in overrides.items():
        if config.get("status") != "playtest":
            continue
        url = masters.get(slug, "")
        match = MASTER_URL.fullmatch(str(url))
        if not match:
            problems.append(f"{slug}: no mapped Kind Robots master issue")
            continue
        path = roadmaps_dir / slug / "roadmap.yaml"
        if not path.exists():
            problems.append(f"{slug}: roadmap missing")
            continue
        tasks = (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("tasks", [])
        errors = playtest_readiness_errors(tasks)
        if explicitly_waived_owner_playtest(slug, config, tasks, errors):
            print(f"OWNER-APPROVED EARLY PLAYTEST {slug}: known unfinished tasks retained", file=sys.stderr)
            errors = []
        for problem in errors:
            problems.append(f"{slug}: {problem}")
        if not any(problem.startswith(f"{slug}:") for problem in problems):
            changes.append((slug, int(match.group(1))))
    return changes, problems


def github_issue(method: str, number: int, token: str, data: dict | None = None) -> dict:
    url = f"https://api.github.com/repos/silasfelinus/kind_robots/issues/{number}"
    request = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8") if data is not None else None,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "conductor-playtest-gate/1.0",
            **({"Content-Type": "application/json"} if data is not None else {}),
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate handoffs without GitHub writes")
    args = parser.parse_args(argv)
    overrides = load_project_overrides(ROOT / "project-overrides.yaml")
    masters = (yaml.safe_load((ROOT / "docs/agents/master-issues.yaml").read_text(encoding="utf-8")) or {}).get("master_issues", {})
    eligible, errors = eligible_issues(overrides, masters, ROOT / "projects")
    for error in errors:
        print(f"PLAYTEST NOT READY: {error}", file=sys.stderr)
    if errors:
        return 1
    if args.check:
        for slug, number in eligible:
            print(f"READY {slug}: Kind Robots issue #{number}")
        return 0

    token = os.environ.get("ISSUE_BRIDGE_TOKEN", "").strip()
    if not token:
        print("ISSUE_BRIDGE_TOKEN missing: playtest issue handoff skipped", file=sys.stderr)
        return 1 if eligible else 0
    for slug, number in eligible:
        issue = github_issue("GET", number, token)
        title = str(issue["title"])
        flagged_title = title if title.startswith(PREFIX) else PREFIX + title
        if issue.get("state") == "closed" and flagged_title == title:
            print(f"ALREADY CLOSED {slug}: #{number}")
            continue
        updated = github_issue("PATCH", number, token, {
            "title": flagged_title,
            "state": "closed",
            "state_reason": "completed",
        })
        print(f"CLOSED FOR PLAYTEST {slug}: #{number} {updated['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
