#!/usr/bin/env python3
"""
close_task.py — push a task's close-out roadmap edit (status: done/review/needs-human/
etc.) to its own branch, checked against live origin/main, so the commit can land via a
real PR instead of a direct push to `main`.

Fixes the gap flagged in conductor/t-091 (self-critique from the coloring-book/t-036
close-out, 2026-07-28): after merging a task's implementation PR, a session used
`set_task_field.py` to flip the task's roadmap status to `done` and pushed that
single-file bookkeeping commit straight to `main` with a plain `git commit && git push`
-- no PR. `git log --grep="close out"` shows every prior close-out commit in this
repo's history carries a `(#PR)` suffix (e.g. `d430c6a` #1353, `85bc7b2` #1347,
`aa5973e` #1345) -- the established and correct convention is a small follow-up PR, not
a direct push. Hard safety rule 1 ("PRs only into `main`, except the Worker's atomic
claim commit") does not exempt close-out commits -- only the claim commit in
`claim_task.py` is a sanctioned direct-to-main exception. This script gives close-outs
the same collision-resistant, fetch-checked git plumbing `claim_task.py` gives claims,
but targets a fresh branch instead of `refs/heads/main`, so the normal PR flow (open,
verify, merge) is what actually lands the change.

Usage:
    python scripts/close_task.py <project> <task-id> <status> --session <id> \\
        [--branch <name>] [--set field=value ...] [--append-note TEXT] \\
        [--implementation-pr OWNER/REPO#N] [--force] [--dry-run]

    python scripts/close_task.py model-builder t-029 done --session claude-20260728T2200Z-mb-t029
    python scripts/close_task.py media-watchlist t-016 needs-human \\
        --session claude-20260728T2200Z-mw-t016 --set soft_gate=true \\
        --set note='blocked on X, see task note'
    python scripts/close_task.py newsfeed t-020 done --session claude-20260805T0900Z-nf-t020 \\
        --implementation-pr silasfelinus/kind_robots#1464
    python scripts/close_task.py cthulhuquarium t-033 needs-human \\
        --session claude-20260825T0900Z-cq-t033 --append-note 'RESOLVED: root cause was X.'

Destructive note replacement (conductor/t-129): `note:` is an append-only diagnostic log
in practice across this repo's roadmaps, not a scalar to overwrite. Closing
cthulhuquarium/t-033 and t-034 with `--set note='RESOLVED ...'` once deleted 199 lines
of diagnostic record between them (repaired in #2816). `set_task_field_text` now refuses
a `--set note=...` that would replace a substantial existing note with a value that
doesn't still contain it, unless `--force` is passed. Use `--append-note TEXT` instead
to add a new paragraph without touching what's already there -- it appends against the
current `origin/<branch or main>` note on every retry attempt, same as every other field
here, and is mutually exclusive with `--set note=...`.

`--implementation-pr` (conductor/t-099) records the PR that actually implemented the
task on a dedicated `implementation_pr` roadmap field (e.g.
`silasfelinus/kind_robots#1464`), separate from any note-quoted PR reference.
check_pr_merged_drift.py's authoritative pass keys on this field first when present --
strictly stronger evidence than its title-text search, and immune to a close-out PR
whose title doesn't follow the `<project>/<task-id>:` convention.

What it does:
    1. Fetches `origin/main` and reads the task straight out of that ref's
       roadmap.yaml -- never the local working tree, which may be stale relative to
       a claim/close commit another script or session already pushed this run.
    2. Refuses (exit 1) if the task does not exist, if it has `recurring: true` and
       the caller passed `done` (unless --force -- recurring tasks never reach done
       per AGENTS.md's "Recurring tasks" rule, they go back to `ready` so they
       re-arm), or (unless --force) if it is already at the requested `status` -- a
       no-op close is almost always a sign the caller is working from stale state,
       not a real transition to make.
    3. Applies `status: <status>`, `updated: now`, and any `--set field=value` pairs
       (repeatable) via `set_task_field.py`'s line-oriented editor -- never
       `yaml.safe_dump`, so comments, multiline notes, and field ordering survive.
    4. Builds a commit on top of `origin/main` HEAD using the same scratch-index git
       plumbing `claim_task.py` uses (`git_plumbing.commit_file_on_ref`) and pushes it
       to `refs/heads/<branch>` (default: `close/<project>-<task-id>-<session-slug>`)
       -- never to `main` directly.
    5. On a non-fast-forward push (the branch already has other commits -- e.g. a
       reused branch name), re-fetches that branch and retries on top of its new tip
       (bounded retries), same shape as `claim_task.py`'s main-branch retry loop.

This script only pushes the branch -- it does not open or merge a PR. GitHub API
calls aren't reliably available to a plain git/Python process in this sandbox (see
AGENTS.md's egress notes), so opening/merging the PR is the calling session's job via
its own GitHub MCP tools, exactly like every other software task's close-out.

If the branch name is brand new, the caller may hit the HTTP 413 documented in
CLAUDE.md ("First push of a session fails with HTTP 413") on the underlying `git push`.
The documented workaround applies unchanged: call the GitHub MCP `create_branch` tool
(`from_branch: main`) to instantiate the ref with zero data transfer BEFORE running
this script, so the push here lands as a small one-commit delta instead of a
brand-new-ref pack. This script does not call `create_branch` itself -- it has no
GitHub API access -- so precreating the branch is left to the caller when needed.

Exit codes: 0 = pushed, 1 = error (missing task, already at target status, or push
exhausted its retries).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from set_task_field import append_note_text, set_task_field_text, TaskFieldError  # noqa: E402
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
SLUG_RE = re.compile(r"[^A-Za-z0-9_.-]+")
IMPLEMENTATION_PR_RE = re.compile(r"^[\w.-]+/[\w.-]+#\d+$")


class CloseError(Exception):
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


def default_branch_name(project: str, task_id: str, session: str) -> str:
    slug = SLUG_RE.sub("-", session).strip("-") or "session"
    return f"close/{project}-{task_id}-{slug}"


def load_task_at_ref(ref: str, project: str, task_id: str) -> tuple[str, dict]:
    path = roadmap_relpath(project)
    text = read_file_at_ref(ROOT, ref, path)
    if text is None:
        raise CloseError(f"ERROR: {path} not found on {ref}", code=1)

    doc = yaml.safe_load(text) or {}
    task = find_task(doc, task_id)
    if task is None:
        raise CloseError(f"ERROR: {project}/{task_id}: task not found in {ref} roadmap", code=1)
    return text, task


def apply_close(
    text: str,
    task_id: str,
    status: str,
    extra_fields: dict[str, str],
    append_note: str | None = None,
    force: bool = False,
) -> str:
    if append_note:
        try:
            text = append_note_text(text, task_id, append_note)
        except TaskFieldError as exc:
            raise CloseError(f"ERROR: could not append note: {exc}", code=1)

    fields = {"status": status, "updated": "now", **extra_fields}
    for field, value in fields.items():
        try:
            text = set_task_field_text(text, task_id, field, value, force=force)
        except TaskFieldError as exc:
            raise CloseError(f"ERROR: could not apply close field {field}: {exc}", code=1)
    return text


def close(
    project: str,
    task_id: str,
    status: str,
    session: str,
    branch: str | None,
    extra_fields: dict[str, str],
    dry_run: bool,
    force: bool = False,
    append_note: str | None = None,
) -> None:
    run_git(ROOT, "fetch", "origin", "main", "-q")
    path = roadmap_relpath(project)
    branch = branch or default_branch_name(project, task_id, session)
    ref = f"refs/heads/{branch}"

    _, task = load_task_at_ref("origin/main", project, task_id)

    existing_pr = task.get("implementation_pr")
    if (
        status in ("review", "ready")
        and "implementation_pr" not in extra_fields
        and isinstance(existing_pr, str)
        and IMPLEMENTATION_PR_RE.match(existing_pr)
    ):
        print(
            f"WARNING: {project}/{task_id} already carries implementation_pr={existing_pr!r} "
            f"and this close (status={status!r}) does not pass --implementation-pr. If the "
            "task was reclaimed and progressed via a different PR since that field was set, "
            "it is now stale (see conductor/t-139, t-140) -- pass --implementation-pr to "
            "update it, or --set implementation_pr=<same value> to confirm it is still "
            "current and silence this warning.",
            file=sys.stderr,
        )

    if not force and task.get("recurring") and status == "done":
        raise CloseError(
            f"ERROR: {project}/{task_id} has recurring: true -- recurring tasks never reach "
            "status=done (AGENTS.md's \"Recurring tasks\" rule: they go back to ready after "
            "each cycle so they re-arm). Pass status=ready instead, or --force if you are "
            "intentionally retiring this recurring task for good.",
            code=1,
        )
    if not force and task.get("status") == status:
        raise CloseError(
            f"ERROR: {project}/{task_id} is already status={status!r} on origin/main -- "
            "refusing a no-op close (pass --force if this is intentional, e.g. re-writing "
            "other --set fields at the same status).",
            code=1,
        )

    try:
        run_git(ROOT, "fetch", "origin", branch, "-q")
        ref_exists = True
    except GitError:
        ref_exists = False

    for attempt in range(1, MAX_ATTEMPTS + 1):
        base_ref = f"origin/{branch}" if ref_exists else "origin/main"
        parent_sha = resolve_ref(ROOT, base_ref)
        before = read_file_at_ref(ROOT, base_ref, path)
        if before is None:
            raise CloseError(f"ERROR: {path} not found on {base_ref}", code=1)
        after = apply_close(before, task_id, status, extra_fields, append_note, force)

        if dry_run:
            print(f"[dry-run] would close {project}/{task_id} -> status={status} on top of {base_ref}@{parent_sha[:12]}")
            print(f"[dry-run] would push {path} to {ref} (branch={branch})")
            return

        message = f"close: {project}/{task_id} -> status={status} ({session})"
        try:
            pushed = commit_file_on_ref(ROOT, parent_sha, ref, path, after, message)
        except GitError as exc:
            raise CloseError(f"ERROR: {exc}", code=1)

        if pushed:
            print(f"PUSHED: {project}/{task_id} -> status={status} on branch {branch}")
            print(f"Open a PR from {branch} into main to land this close-out.")
            return

        print(
            f"[close_task] push race on attempt {attempt}/{MAX_ATTEMPTS} "
            f"({ref} moved) -- re-fetching and re-checking",
            file=sys.stderr,
        )
        run_git(ROOT, "fetch", "origin", branch, "-q")
        ref_exists = True

    raise CloseError(
        f"ERROR: could not push close-out for {project}/{task_id} to {branch} after "
        f"{MAX_ATTEMPTS} attempts (repeated push races)",
        code=1,
    )


def parse_set_args(pairs: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for pair in pairs:
        if "=" not in pair:
            raise CloseError(f"ERROR: --set expects field=value, got {pair!r}", code=1)
        field, value = pair.split("=", 1)
        result[field.strip()] = value
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project", help="Project slug, matching projects/<project>/")
    parser.add_argument("task_id", help="Task id, such as t-029")
    parser.add_argument("status", help="Target status, such as done, review, needs-human, blocked")
    parser.add_argument("--session", required=True, help="Opaque session/run identifier, for the audit trail")
    parser.add_argument("--branch", help="Branch to push the close-out commit to (default: close/<project>-<task>-<session>)")
    parser.add_argument("--set", action="append", default=[], metavar="field=value", help="Extra roadmap field to set alongside status (repeatable)")
    parser.add_argument(
        "--implementation-pr",
        metavar="OWNER/REPO#NUMBER",
        help=(
            "Record the PR that actually implemented this task (e.g. "
            "silasfelinus/kind_robots#1464) as a dedicated `implementation_pr` "
            "roadmap field, so check_pr_merged_drift.py's authoritative pass can key "
            "on it directly instead of a title-text search (conductor/t-099)."
        ),
    )
    parser.add_argument(
        "--append-note",
        metavar="TEXT",
        help=(
            "Append TEXT as a new paragraph on the task's existing note instead of "
            "replacing it (conductor/t-129) -- the append-only-log convention most "
            "roadmap notes already follow. Mutually exclusive with --set note=...; "
            "always wins over --force's note-guard bypass since it never deletes "
            "prior content."
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help=(
            "Allow closing a task already at the target status, AND allow --set "
            "note=... to replace a substantial existing note outright (bypasses the "
            "conductor/t-129 destructive-note-replace guard)."
        ),
    )
    parser.add_argument("--dry-run", action="store_true", help="Check state and print intent; push nothing")
    args = parser.parse_args()

    if not (PROJECTS_DIR / args.project / "roadmap.yaml").exists():
        print(f"ERROR: unknown project {args.project!r}", file=sys.stderr)
        return 1

    if args.implementation_pr and not IMPLEMENTATION_PR_RE.match(args.implementation_pr):
        print(
            f"ERROR: --implementation-pr must look like owner/repo#123, got {args.implementation_pr!r}",
            file=sys.stderr,
        )
        return 1

    try:
        extra_fields = parse_set_args(args.set)
        if args.append_note and "note" in extra_fields:
            raise CloseError(
                "ERROR: cannot combine --append-note with --set note=... -- pick one "
                "(--append-note adds a paragraph, --set note=... replaces the field outright)",
                code=1,
            )
        if args.implementation_pr:
            extra_fields["implementation_pr"] = args.implementation_pr
        close(
            args.project,
            args.task_id,
            args.status,
            args.session,
            args.branch,
            extra_fields,
            args.dry_run,
            force=args.force,
            append_note=args.append_note,
        )
    except CloseError as exc:
        print(str(exc), file=sys.stderr)
        return exc.code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
