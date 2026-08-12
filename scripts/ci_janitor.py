#!/usr/bin/env python3
"""Create high-priority Kind Robots Todos for newly failed critical CI runs."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

GITHUB_API = "https://api.github.com"
TODOS_API = "https://kindrobots.org/api/todos"
RED_CONCLUSIONS = {
    "action_required",
    "cancelled",
    "failure",
    "startup_failure",
    "stale",
    "timed_out",
}


@dataclass(frozen=True)
class WorkflowCheck:
    repository: str
    workflow: str
    branch: str
    label: str


DEFAULT_CHECKS = (
    WorkflowCheck(
        repository="silasfelinus/kind_robots",
        workflow="cypress.yml",
        branch="main",
        label="Kind Robots Cypress Tests",
    ),
)


def request_json(
    url: str,
    *,
    token: str = "",
    method: str = "GET",
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    headers = {
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "kind-conductor-ci-janitor",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(url, data=body, headers=headers, method=method)

    with urllib.request.urlopen(request, timeout=20) as response:
        raw = response.read().decode("utf-8")
        return json.loads(raw) if raw else {}


def load_checks() -> tuple[WorkflowCheck, ...]:
    raw = os.environ.get("CI_JANITOR_CHECKS_JSON", "").strip()
    if not raw:
        return DEFAULT_CHECKS

    parsed = json.loads(raw)
    if not isinstance(parsed, list):
        raise ValueError("CI_JANITOR_CHECKS_JSON must contain a JSON array")

    return tuple(
        WorkflowCheck(
            repository=str(item["repository"]),
            workflow=str(item["workflow"]),
            branch=str(item.get("branch", "main")),
            label=str(item.get("label") or f"{item['repository']} {item['workflow']}"),
        )
        for item in parsed
    )


def latest_completed_run(check: WorkflowCheck, github_token: str) -> dict[str, Any] | None:
    repository = urllib.parse.quote(check.repository, safe="/")
    workflow = urllib.parse.quote(check.workflow, safe="")
    branch = urllib.parse.quote(check.branch, safe="")
    url = (
        f"{GITHUB_API}/repos/{repository}/actions/workflows/{workflow}/runs"
        f"?branch={branch}&status=completed&per_page=1"
    )
    response = request_json(url, token=github_token)
    runs = response.get("workflow_runs", [])
    return runs[0] if isinstance(runs, list) and runs else None


def latest_run_for_branch(check: WorkflowCheck, github_token: str) -> dict[str, Any] | None:
    """The single most recent run for this branch/workflow, regardless of status.

    Used to detect the cancel-in-progress concurrency-supersede pattern: a `cancelled`
    completed run whose commit isn't actually the newest one on the branch was killed
    by a newer push landing on the same concurrency group, not by a real failure.
    """
    repository = urllib.parse.quote(check.repository, safe="/")
    workflow = urllib.parse.quote(check.workflow, safe="")
    branch = urllib.parse.quote(check.branch, safe="")
    url = (
        f"{GITHUB_API}/repos/{repository}/actions/workflows/{workflow}/runs"
        f"?branch={branch}&per_page=1"
    )
    response = request_json(url, token=github_token)
    runs = response.get("workflow_runs", [])
    return runs[0] if isinstance(runs, list) and runs else None


def cancelled_run_is_superseded(
    check: WorkflowCheck, run: dict[str, Any], github_token: str
) -> bool:
    """True when `run` (a `cancelled` completed run) isn't the newest run on the branch.

    A newer run for a different commit means the concurrency group's cancel-in-progress
    killed this one on a supersede, not a real failure -- see conductor/t-062. Whether
    that newer run has itself finished yet doesn't matter: either way this cancelled run
    is stale noise, not the branch's actual current state.
    """
    latest = latest_run_for_branch(check, github_token)
    if not latest:
        return False
    return str(latest.get("head_sha") or "") != str(run.get("head_sha") or "")


def todo_marker(check: WorkflowCheck, run_id: int) -> str:
    return f"ci-janitor:{check.repository}:{check.workflow}:{run_id}"


def existing_markers(todos: list[dict[str, Any]]) -> set[str]:
    markers: set[str] = set()
    for todo in todos:
        description = str(todo.get("description") or "")
        for line in description.splitlines():
            stripped = line.strip()
            if stripped.startswith("ci-janitor:"):
                markers.add(stripped)
    return markers


def fetch_todos(kr_token: str) -> list[dict[str, Any]]:
    response = request_json(TODOS_API, token=kr_token)
    todos = response.get("data", [])
    return todos if isinstance(todos, list) else []


def create_incident_todo(
    check: WorkflowCheck,
    run: dict[str, Any],
    kr_token: str,
) -> dict[str, Any]:
    run_id = int(run["id"])
    conclusion = str(run.get("conclusion") or "unknown")
    run_url = str(run.get("html_url") or "")
    head_sha = str(run.get("head_sha") or "")
    marker = todo_marker(check, run_id)

    description = "\n".join(
        [
            marker,
            f"Critical main-branch CI is red: {check.label}.",
            f"Conclusion: {conclusion}",
            f"Commit: {head_sha}",
            f"Run: {run_url}",
            "Inspect the failing job logs and uploaded artifacts, identify the shared root cause, and restore main to green.",
            "Do not weaken, skip, or delete legitimate tests to manufacture a pass. Fix the product, test contract, environment, or workflow fault that caused the run.",
            "Open the repair PR in the affected repository, link this run in the PR, and complete this Todo only after the relevant verification has passed or the remaining gate is clearly documented.",
            "Operational policy: CI-JANITOR.md",
        ]
    )

    return request_json(
        TODOS_API,
        token=kr_token,
        method="POST",
        payload={
            "title": f"Fix red CI: {check.label}",
            "description": description,
            "priority": "HIGH",
            "category": "AGENT",
            "icon": "kind-icon:bug",
        },
    )


def main() -> int:
    github_token = os.environ.get("GITHUB_TOKEN", "").strip()
    kr_token = os.environ.get("KR_API_TOKEN", "").strip()

    if not kr_token:
        print("::error::KR_API_TOKEN is required to create CI repair Todos.")
        return 1

    try:
        checks = load_checks()
        todos = fetch_todos(kr_token)
    except (ValueError, urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as error:
        print(f"::error::Unable to initialize CI janitor: {error}")
        return 1

    markers = existing_markers(todos)
    created = 0
    red = 0

    for check in checks:
        try:
            run = latest_completed_run(check, github_token)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as error:
            print(f"::error::Unable to inspect {check.label}: {error}")
            return 1

        if not run:
            print(f"::warning::No completed run found for {check.label}.")
            continue

        conclusion = str(run.get("conclusion") or "unknown")
        run_id = int(run["id"])
        run_url = str(run.get("html_url") or "")
        print(f"{check.label}: {conclusion} ({run_url})")

        if conclusion not in RED_CONCLUSIONS:
            continue

        if conclusion == "cancelled":
            try:
                superseded = cancelled_run_is_superseded(check, run, github_token)
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as error:
                print(f"::error::Unable to check for a superseding run of {check.label}: {error}")
                return 1
            if superseded:
                print(
                    f"{check.label}: cancelled run {run_id} superseded by a newer commit on "
                    f"the branch (concurrency cancel-in-progress) -- treating as noise, not red."
                )
                continue

        red += 1
        marker = todo_marker(check, run_id)
        if marker in markers:
            print(f"Todo already exists for run {run_id}; skipping duplicate.")
            continue

        try:
            response = create_incident_todo(check, run, kr_token)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as error:
            print(f"::error::Unable to create Todo for {check.label}: {error}")
            return 1

        if response.get("success") is not True:
            print(
                f"::error::Kind Robots rejected the CI Todo: {json.dumps(response, sort_keys=True)}"
            )
            return 1

        created += 1
        markers.add(marker)
        todo = response.get("data") or {}
        print(f"Created HIGH priority Todo #{todo.get('id', '?')} for run {run_id}.")

    print(f"CI janitor complete: checks={len(checks)} red={red} created={created}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
