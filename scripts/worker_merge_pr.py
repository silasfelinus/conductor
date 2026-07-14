#!/usr/bin/env python3
"""Merge a Worker PR and immediately mark its roadmap task done.

This helper exists so the Worker has one command for the two operations that must
stay paired: squash-merge the implementation PR, then update the conductor
roadmap with scripts/worker_task_status.py done and push that status commit.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPO = "silasfelinus/conductor"
MAX_MERGE_ATTEMPTS = 3


class WorkerMergeError(Exception):
    def __init__(self, message: str, status: int | None = None):
        super().__init__(message)
        self.status = status


def _gh(
    repo: str,
    path: str,
    token: str | None,
    *,
    method: str = "GET",
    body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    url = f"https://api.github.com/repos/{repo}/{path.lstrip('/')}"
    data = json.dumps(body).encode() if body is not None else None
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "conductor-worker-merge/1.0",
        **({"Authorization": f"Bearer {token}"} if token else {}),
        **({"Content-Type": "application/json"} if data else {}),
    }
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:500]
        raise WorkerMergeError(
            f"GitHub {method} {path} failed: HTTP {exc.code}: {detail}", status=exc.code
        ) from exc
    except Exception as exc:
        raise WorkerMergeError(f"GitHub {method} {path} failed: {exc}") from exc


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        raise WorkerMergeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def already_merged_sha(repo: str, pr_number: int, token: str | None) -> str | None:
    """Return the merge commit sha if GitHub says the PR is already merged, else None."""
    pr = _gh(repo, f"pulls/{pr_number}", token)
    if pr.get("merged"):
        return str(pr.get("merge_commit_sha") or "")
    return None


def merge_pr(repo: str, pr_number: int, token: str | None) -> str:
    last_error = "merge was not accepted"
    for attempt in range(1, MAX_MERGE_ATTEMPTS + 1):
        try:
            result = _gh(
                repo,
                f"pulls/{pr_number}/merge",
                token,
                method="PUT",
                body={"merge_method": "squash"},
            )
        except WorkerMergeError as exc:
            # GitHub answers 405 both for "already merged" and "not mergeable".
            # A re-run after a partially completed cycle (merge succeeded, status
            # flip didn't) hits the former — verify via GET and treat it as
            # success so mark_task_done still runs. Anything else re-raises.
            if exc.status == 405:
                merged_sha = already_merged_sha(repo, pr_number, token)
                if merged_sha is not None:
                    print(f"PR #{pr_number} was already merged; continuing to status flip.")
                    return merged_sha
            raise

        if result.get("merged"):
            return str(result.get("sha") or "")

        last_error = str(result.get("message") or last_error)
        if attempt < MAX_MERGE_ATTEMPTS:
            time.sleep(3)

    raise WorkerMergeError(f"PR #{pr_number} did not merge after {MAX_MERGE_ATTEMPTS} attempts: {last_error}")


def mark_task_done(project: str, task_id: str, note: str | None) -> None:
    command = [sys.executable, str(ROOT / "scripts" / "worker_task_status.py"), "done", project, task_id]
    if note:
        command.extend(["--note", note])
    result = subprocess.run(command, cwd=ROOT, text=True)
    if result.returncode != 0:
        raise WorkerMergeError(f"worker_task_status.py done failed for {project}/{task_id}")


def commit_done_status(project: str, task_id: str, session_branch: str | None) -> str:
    """Commit the done-status roadmap flip and push it, returning the ref it landed on.

    Permission-restricted sessions (git proxy allows only the designated claude/*
    branch) get the merge through fine but a straight `push origin main` for the
    status flip 403s. Rather than leaving a merged-but-not-marked-done gap for the
    next cycle to rediscover, fall back to committing on the session's own branch
    so the flip lands on main via that branch's normal PR instead.
    """
    roadmap = ROOT / "projects" / project / "roadmap.yaml"
    run_git("add", str(roadmap.relative_to(ROOT)))
    try:
        run_git("commit", "-m", f"done: {project}/{task_id} [skip ci]")
    except WorkerMergeError as exc:
        if "nothing to commit" not in str(exc).lower():
            raise

    try:
        run_git("push", "origin", "main")
        return "main"
    except WorkerMergeError as exc:
        if not session_branch or session_branch == "main":
            raise
        print(
            f"WARNING: push to origin/main was rejected for {project}/{task_id}'s "
            f"done-status commit ({exc}); falling back to session branch "
            f"'{session_branch}'.",
            file=sys.stderr,
        )

    done_sha = run_git("rev-parse", "HEAD")
    run_git("checkout", session_branch)
    run_git("cherry-pick", done_sha)
    run_git("push", "origin", session_branch)
    print(
        f"Done-status commit for {project}/{task_id} landed on '{session_branch}' "
        "instead of main (main push was rejected) -- it will reach main once that "
        "branch's PR merges. Merge that PR promptly so the roadmap status doesn't "
        "stay stale on main."
    )
    return session_branch


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Squash-merge a Worker PR, then immediately mark the roadmap task done."
    )
    parser.add_argument("pr_number", type=int)
    parser.add_argument("project")
    parser.add_argument("task_id")
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--note", help="Optional note to write when marking the task done")
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN"))
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.dry_run:
        print(f"would squash-merge {args.repo} PR #{args.pr_number}")
        print(f"would mark {args.project}/{args.task_id} done")
        return 0

    try:
        merge_sha = merge_pr(args.repo, args.pr_number, args.token)
        session_branch = run_git("rev-parse", "--abbrev-ref", "HEAD")
        run_git("checkout", "main")
        run_git("pull", "origin", "main")
        note = args.note or f"Completed in PR #{args.pr_number}."
        mark_task_done(args.project, args.task_id, note)
        status_branch = commit_done_status(args.project, args.task_id, session_branch)
    except WorkerMergeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"merged PR #{args.pr_number}; marked {args.project}/{args.task_id} done ({merge_sha})")
    if status_branch != "main":
        print(f"NOTE: roadmap done-status commit is on '{status_branch}', not main yet.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
