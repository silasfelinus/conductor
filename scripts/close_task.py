#!/usr/bin/env python3
"""close_task.py — prepare a task close-out on a PR branch, never directly on main.

The script reads live ``origin/main``, applies the requested roadmap transition with the
line-oriented roadmap editor, creates one commit with scratch-index plumbing, and pushes
that commit to a close-out branch for the caller to PR and merge.

IMPORTANT BRANCH SAFETY (conductor/t-161): ``--branch`` is not an instruction to rebuild
an existing local implementation branch from its remote tip. If a local branch with that
name exists and its tip differs from ``origin/<branch>`` (or ``origin/main`` when the
remote branch does not yet exist), close_task refuses before writing anything. This
prevents an unpushed local implementation commit from being silently omitted. Push the
implementation commits first, or use a distinct close-out branch name.

Usage:
    python scripts/close_task.py <project> <task-id> <status> --session <id> \\
        [--branch <name>] [--set field=value ...] [--append-note TEXT] \\
        [--implementation-pr OWNER/REPO#N] [--force] [--dry-run]

Recurring re-arm after a cycle that did nothing (``status=ready`` with ``--noop``) records
``noop_streak`` and ``rest_until`` so no picker claims the task again until the rest
(2h, 6h, 12h, 24h, then 48h; ``max_rest_hours`` on the task caps it) has elapsed. A re-arm
WITHOUT ``--noop`` resets both, so the first cycle that does real work ends the backoff.
A task with ``min_rest_hours`` always rests at least that long after any re-arm (a cap on
how often a standing task runs, not just a no-op backoff).
See roadmap_claims.NOOP_REST_HOURS for why.

``note:`` is append-only in normal use. Prefer ``--append-note``; destructive note
replacement requires ``--force``. ``--implementation-pr`` stores the canonical
``owner/repo#number`` reference used by merged-PR drift checks.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from set_task_field import append_note_text, set_task_field_text, TaskFieldError  # noqa: E402
from branch_ancestry import classify_relationship  # noqa: E402
from git_plumbing import (  # noqa: E402
    GitError,
    commit_file_on_ref,
    read_file_at_ref,
    resolve_ref,
    run_git,
)
from process_task_events import HANDOFF_DOC_RE, missing_handoff_docs  # noqa: E402
from roadmap_claims import noop_rest_hours  # noqa: E402

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
        raise CloseError(f"ERROR: {path} not found on {ref}")
    doc = yaml.safe_load(text) or {}
    task = find_task(doc, task_id)
    if task is None:
        raise CloseError(f"ERROR: {project}/{task_id}: task not found in {ref} roadmap")
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
            raise CloseError(f"ERROR: could not append note: {exc}") from exc
    fields = {"status": status, "updated": "now", **extra_fields}
    for field, value in fields.items():
        try:
            text = set_task_field_text(text, task_id, field, value, force=force)
        except TaskFieldError as exc:
            raise CloseError(f"ERROR: could not apply close field {field}: {exc}") from exc
    return text


def _try_resolve(ref: str) -> str | None:
    try:
        return resolve_ref(ROOT, ref)
    except GitError:
        return None


def assert_local_branch_safe(branch: str, remote_ref: str) -> None:
    """Refuse to rebuild a named local branch when its tip is not the chosen remote base.

    close_task writes commits with a scratch index and does not consume the caller's worktree.
    Before t-161 that meant ``--branch <current-branch>`` could silently omit local-only
    commits because the commit was based on ``origin/<branch>`` instead. A differing local
    ref is therefore a hard ambiguity: the caller must push it first or choose another branch.

    conductor/t-163: the equal/not-equal check is built on ``classify_relationship``
    (scripts/branch_ancestry.py) rather than a bare SHA comparison, so the error message
    can name *how* the two differ (local has unpushed commits, the local checkout is
    merely stale, or the two have genuinely diverged) instead of just "not equal". The
    refusal itself is unchanged: only "equal" is treated as safe to build on.
    """
    local_sha = _try_resolve(f"refs/heads/{branch}")
    if local_sha is None:
        return
    remote_sha = resolve_ref(ROOT, remote_ref)
    relationship = classify_relationship(ROOT, f"refs/heads/{branch}", remote_ref)
    if relationship != "equal":
        raise CloseError(
            f"ERROR: local branch {branch!r} is at {local_sha[:12]} but {remote_ref} is at "
            f"{remote_sha[:12]} ({relationship}). Refusing to build a close-out from the "
            "remote tip because that could omit local/unpushed commits. Push the branch "
            "first or use a distinct --branch name."
        )


def missing_handoff_docs_at_ref(note: object, ref: str) -> list[str]:
    """Apply t-187's handoff guard to the committed tree `close_task` will extend.

    `missing_handoff_docs()` is intentionally reused as the shared filesystem/path
    contract. The extra ref read is load-bearing here: a handoff that exists only as an
    uncommitted worktree file must not make a close-out safe, because scratch-index
    close_task commits only roadmap.yaml and would leave that file behind.
    """
    if not isinstance(note, str):
        return []
    referenced = [match.group(0) for match in HANDOFF_DOC_RE.finditer(note)]
    missing_on_disk = set(missing_handoff_docs(note, ROOT))
    return [
        path
        for path in referenced
        if path in missing_on_disk or read_file_at_ref(ROOT, ref, path) is None
    ]


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
    noop: bool = False,
    now: datetime | None = None,
) -> None:
    run_git(ROOT, "fetch", "origin", "main", "-q")
    path = roadmap_relpath(project)
    branch = branch or default_branch_name(project, task_id, session)
    ref = f"refs/heads/{branch}"
    _, task = load_task_at_ref("origin/main", project, task_id)
    extra_fields = dict(extra_fields)
    extra_fields.update(rest_fields(task, status, noop, now=now))

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
            "update it, or --set implementation_pr=<same value> to confirm it is still current "
            "and silence this warning.",
            file=sys.stderr,
        )

    if not force and task.get("recurring") and status == "done":
        raise CloseError(
            f"ERROR: {project}/{task_id} has recurring: true -- recurring tasks never reach "
            "status=done; use status=ready, or --force only when intentionally retiring it."
        )
    if not force and task.get("status") == status:
        raise CloseError(
            f"ERROR: {project}/{task_id} is already status={status!r} on origin/main -- "
            "refusing a no-op close (pass --force if intentional)."
        )

    try:
        run_git(ROOT, "fetch", "origin", branch, "-q")
        ref_exists = True
    except GitError:
        ref_exists = False

    initial_base = f"origin/{branch}" if ref_exists else "origin/main"
    assert_local_branch_safe(branch, initial_base)

    for attempt in range(1, MAX_ATTEMPTS + 1):
        base_ref = f"origin/{branch}" if ref_exists else "origin/main"
        parent_sha = resolve_ref(ROOT, base_ref)
        before = read_file_at_ref(ROOT, base_ref, path)
        if before is None:
            raise CloseError(f"ERROR: {path} not found on {base_ref}")
        after = apply_close(before, task_id, status, extra_fields, append_note, force)

        # conductor/t-188: close_task is the direct/local sibling of the connector
        # task-events path. Apply the same t-187 invariant here before the scratch
        # commit is created. Checking the resulting task note covers both --append-note
        # and --set note=. Checking base_ref, not merely the worktree, ensures a loose
        # uncommitted handoff file cannot falsely satisfy a close that commits only the
        # roadmap and strands the handoff outside the pushed tree.
        if status == "needs-human":
            after_doc = yaml.safe_load(after) or {}
            after_task = find_task(after_doc, task_id)
            missing = missing_handoff_docs_at_ref(
                after_task.get("note") if after_task else None,
                base_ref,
            )
            if missing:
                raise CloseError(
                    f"ERROR: {project}/{task_id}: needs-human note references missing "
                    f"handoff document(s): {', '.join(missing)}. Commit the handoff "
                    "document before closing the task."
                )

        if dry_run:
            print(
                f"[dry-run] would close {project}/{task_id} -> status={status} "
                f"on top of {base_ref}@{parent_sha[:12]}"
            )
            print(f"[dry-run] would push {path} to {ref} (branch={branch})")
            return

        message = f"close: {project}/{task_id} -> status={status} ({session})"
        try:
            pushed = commit_file_on_ref(ROOT, parent_sha, ref, path, after, message)
        except GitError as exc:
            raise CloseError(f"ERROR: {exc}") from exc

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
        assert_local_branch_safe(branch, f"origin/{branch}")

    raise CloseError(
        f"ERROR: could not push close-out for {project}/{task_id} to {branch} after "
        f"{MAX_ATTEMPTS} attempts (repeated push races)"
    )


def rest_fields(
    task: dict, status: str, noop: bool, *, now: datetime | None = None
) -> dict[str, str]:
    """Fields implementing the recurring no-op backoff (see module docstring)."""
    if noop:
        if status != "ready" or not task.get("recurring"):
            raise CloseError(
                "ERROR: --noop is only for re-arming a recurring: true task to status=ready "
                "after a cycle that found nothing to do."
            )
        if task.get("daily_commitment"):
            raise CloseError(
                "ERROR: --noop does not apply to daily_commitment tasks -- the daily gate "
                "(daily_last_checked) already limits them to one attempt per Pacific day, and "
                "a multi-day rest would skip promised days."
            )
        try:
            streak = int(task.get("noop_streak") or 0) + 1
        except (TypeError, ValueError):
            streak = 1
        now = now or datetime.now(timezone.utc)
        hours = max(noop_rest_hours(streak, task.get("max_rest_hours")), _min_rest(task))
        until = (now + timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
        print(f"[close_task] no-op #{streak}: resting until {until} ({hours:g}h)", file=sys.stderr)
        return {"noop_streak": str(streak), "rest_until": until}
    if status == "ready" and _min_rest(task) > 0:
        # Capped standing task: rests min_rest_hours even after real work.
        now = now or datetime.now(timezone.utc)
        until = (now + timedelta(hours=_min_rest(task))).strftime("%Y-%m-%dT%H:%M:%SZ")
        return {"noop_streak": "0", "rest_until": until}
    if status == "ready" and (task.get("noop_streak") or task.get("rest_until")):
        return {"noop_streak": "0", "rest_until": "null"}
    return {}


def _min_rest(task: dict) -> float:
    try:
        return float(task.get("min_rest_hours") or 0)
    except (TypeError, ValueError):
        return 0.0


def parse_set_args(pairs: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for pair in pairs:
        if "=" not in pair:
            raise CloseError(f"ERROR: --set expects field=value, got {pair!r}")
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
    parser.add_argument("--implementation-pr", metavar="OWNER/REPO#NUMBER", help="Record the implementation PR as owner/repo#number")
    parser.add_argument("--append-note", metavar="TEXT", help="Append TEXT to the existing task note; mutually exclusive with --set note=...")
    parser.add_argument("--force", action="store_true", help="Allow same-status close and destructive --set note replacement")
    parser.add_argument("--dry-run", action="store_true", help="Check state and print intent; push nothing")
    parser.add_argument(
        "--noop",
        action="store_true",
        help="Recurring re-arm after a cycle that did nothing: rest the task (2h..48h backoff) before any picker takes it again",
    )
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
                "(--append-note adds a paragraph, --set note=... replaces the field outright)"
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
            noop=args.noop,
        )
    except CloseError as exc:
        print(str(exc), file=sys.stderr)
        return exc.code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
