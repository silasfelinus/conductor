#!/usr/bin/env python3
"""
claim_task.py — atomically claim a roadmap task, checked against live origin/main.

Fixes the rotation-collision gap in conductor/t-040: burst-mode picking
(next_ready_task.py + priority.yaml) reads only the local working tree, so two
concurrent sessions can independently pick, and fully implement, the same
project/task before either one pushes. This happened for real on 2026-07-14 --
two sessions both built animation-manager/t-008 end-to-end; see TALKBACK.md and
projects/conductor/roadmap.yaml t-040 for the full account.

Usage:
    python scripts/claim_task.py <project> <task-id> --owner worker --session <id>
    python scripts/claim_task.py <project> <task-id> --owner reviewer --session <id> --dry-run

What it does:
    1. Fetches `origin/main` and reads the task straight out of that ref's
       roadmap.yaml -- never the local working tree, which is exactly the stale
       state that let two sessions collide.
    2. Refuses the claim (exit 3, "ALREADY_CLAIMED") unless the task is currently
       claimable: `status: ready`, or `status: claimed` with a `claimed_at` older
       than CLAIM_TTL_MINUTES (an abandoned/crashed claim -- see roadmap_claims.py).
    3. Builds a commit -- `status: claimed`, `owner: <owner>`, `claimed_by: <session>`,
       `claimed_at: <now>`, `updated: <now>` -- directly on top of origin/main using
       git plumbing (a scratch index, not the caller's real index/working tree/HEAD),
       and pushes it straight to `refs/heads/main`. This never touches whatever branch
       or uncommitted changes the caller currently has checked out.
    4. On a non-fast-forward push (someone else moved origin/main meanwhile),
       re-fetches and re-checks: if the SAME task was claimed by someone else in the
       interim, exits 3 (rotate to the next ready task/project); if it was an
       unrelated upstream change, rebuilds the commit on the new tip and retries
       (bounded retries).

Exit codes: 0 = claimed, 3 = ALREADY_CLAIMED (rotate to the next task), 1 = error.

After a successful claim, do the real implementation work on your own feature branch
as usual. Finishing the task (status -> done/review/needs-human/blocked/challenged)
is what releases the claim -- there is no separate "release" step. If a claiming
session crashes, the claim self-expires after CLAIM_TTL_MINUTES (see roadmap_claims.py)
so the task isn't locked forever.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from roadmap_claims import task_is_claimable  # noqa: E402
from set_task_field import set_task_field_text, TaskFieldError  # noqa: E402
from git_plumbing import (  # noqa: E402
    GitError,
    commit_file_on_ref,
    read_file_at_ref,
    resolve_ref,
    run_git,
)

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT / "projects"
MAX_ATTEMPTS = 4


class ClaimError(Exception):
    def __init__(self, message: str, *, code: int = 1):
        super().__init__(message)
        self.code = code


def roadmap_relpath(project: str) -> str:
    return f"projects/{project}/roadmap.yaml"


def find_task(doc: dict, task_id: str) -> dict | None:
    for task in doc.get("tasks", []) or []:
        if isinstance(task, dict) and str(task.get("id")) == task_id:
            return task
    return None


def check_claimable(project: str, task_id: str) -> str:
    """Reads projects/<project>/roadmap.yaml from origin/main and returns its text
    if the task is currently claimable; raises ClaimError(code=3) otherwise."""
    path = roadmap_relpath(project)
    text = read_file_at_ref(ROOT, "origin/main", path)
    if text is None:
        raise ClaimError(f"ERROR: {path} not found on origin/main", code=1)

    doc = yaml.safe_load(text) or {}
    task = find_task(doc, task_id)
    if task is None:
        raise ClaimError(f"ERROR: {project}/{task_id}: task not found in origin/main roadmap", code=1)

    if not task_is_claimable(task):
        raise ClaimError(
            f"ALREADY_CLAIMED: {project}/{task_id} is status={task.get('status')!r} "
            f"(owner={task.get('owner')!r}, claimed_by={task.get('claimed_by')!r}, "
            f"claimed_at={task.get('claimed_at')!r}) on origin/main -- rotate to the "
            "next ready task/project instead of starting real work here.",
            code=3,
        )
    return text


def apply_claim(text: str, task_id: str, owner: str, session: str) -> str:
    for field, value in (
        ("status", "claimed"),
        ("owner", owner),
        ("claimed_by", session),
        ("claimed_at", "now"),
        ("updated", "now"),
    ):
        try:
            text = set_task_field_text(text, task_id, field, value)
        except TaskFieldError as exc:
            raise ClaimError(f"ERROR: could not apply claim field {field}: {exc}", code=1)
    return text


def claim(project: str, task_id: str, owner: str, session: str, dry_run: bool) -> None:
    run_git(ROOT, "fetch", "origin", "main", "-q")
    path = roadmap_relpath(project)

    for attempt in range(1, MAX_ATTEMPTS + 1):
        parent_sha = resolve_ref(ROOT, "origin/main")
        before = check_claimable(project, task_id)  # raises ClaimError(code=3) if not
        after = apply_claim(before, task_id, owner, session)

        if dry_run:
            print(f"[dry-run] would claim {project}/{task_id} on top of origin/main@{parent_sha[:12]}")
            print(f"[dry-run] would write {path} and push a claim commit to origin/main")
            return

        message = f"claim: {project}/{task_id} ({owner}/{session})"
        try:
            pushed = commit_file_on_ref(ROOT, parent_sha, "refs/heads/main", path, after, message)
        except GitError as exc:
            raise ClaimError(f"ERROR: {exc}", code=1)

        if pushed:
            print(f"CLAIMED: {project}/{task_id} (owner={owner}, session={session})")
            return

        print(
            f"[claim_task] push race on attempt {attempt}/{MAX_ATTEMPTS} "
            "(origin/main moved) -- re-fetching and re-checking",
            file=sys.stderr,
        )
        run_git(ROOT, "fetch", "origin", "main", "-q")

    raise ClaimError(
        f"ERROR: could not claim {project}/{task_id} after {MAX_ATTEMPTS} attempts "
        "(repeated push races on origin/main)",
        code=1,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project", help="Project slug, matching projects/<project>/")
    parser.add_argument("task_id", help="Task id, such as t-016")
    parser.add_argument("--owner", required=True, choices=["worker", "reviewer"])
    parser.add_argument("--session", required=True, help="Opaque session/run identifier, for the audit trail")
    parser.add_argument("--dry-run", action="store_true", help="Check claimability and print intent; write nothing")
    args = parser.parse_args()

    if not (PROJECTS_DIR / args.project / "roadmap.yaml").exists():
        print(f"ERROR: unknown project {args.project!r}", file=sys.stderr)
        return 1

    try:
        claim(args.project, args.task_id, args.owner, args.session, args.dry_run)
    except ClaimError as exc:
        print(str(exc), file=sys.stderr)
        return exc.code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
