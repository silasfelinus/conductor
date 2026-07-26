#!/usr/bin/env python3
"""
append_ledger_entry.py — append a TALKBACK.md or LEARNING.yaml entry directly to
origin/main, safe under concurrent writers.

Kaizen from conductor/t-033's design doc (`projects/conductor/docs/concurrent-claims.md`,
section 3, "Gaps to close before rollout"). TALKBACK.md and LEARNING.yaml are hand-appended
by agents (never CI-regenerated, so hard rule 9's "always take the latest generated
version" doesn't apply to them). Today's only conflict guidance for them is the Reviewer
batch-merge companion note ("keep both sides' entries"), which assumes a human or
Reviewer resolving an occasional conflict during a sweep — not an automated
fetch-append-push loop running unattended. This module extracts claim_task.py's own
`commit_file_on_ref` pattern (scratch-index commit built on a freshly-fetched parent,
retried on non-fast-forward) into a small helper any script can call for exactly that
case, so two sessions appending to the same file in the same window land both entries
instead of one clobbering the other.

Usage (library):
    from scripts.append_ledger_entry import append_talkback_entry, append_learning_record

    append_talkback_entry(ROOT, "TALKBACK.md", entry_markdown, "talkback: ...")
    append_talkback_entry(ROOT, "projects/ai-art-academy/TALKBACK.md", entry_markdown, "talkback: ...")
    append_learning_record(ROOT, {"date": "2026-07-26", "project": "...", ...}, "learning: ...")

Usage (CLI):
    python scripts/append_ledger_entry.py talkback TALKBACK.md --file entry.md --message "..."
    python scripts/append_ledger_entry.py learning --file record.yaml --message "..."

Like claim_task.py, this pushes straight to `refs/heads/main` via git plumbing and never
touches the caller's checked-out branch, working tree, or index -- safe to call from a
session that has other uncommitted work in progress on its own feature branch.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Callable

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from git_plumbing import GitError, commit_file_on_ref, read_file_at_ref, resolve_ref, run_git  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
MAX_ATTEMPTS = 4
LEARNING_PATH = "LEARNING.yaml"


def append_with_retry(
    root: Path,
    path: str,
    build_new_text: Callable[[str], str],
    message: str,
    *,
    ref: str = "refs/heads/main",
    remote_ref: str = "origin/main",
    max_attempts: int = MAX_ATTEMPTS,
) -> str:
    """Fetches `remote_ref`, applies `build_new_text` to the current text of `path` at
    that ref, and pushes a single-file commit straight to `ref`.

    On a non-fast-forward push (another session appended to the same file first),
    re-fetches and recomputes `build_new_text` against the new tip, so a retry's append
    is never computed against a base that's already stale -- the same race
    `claim_task.py` closes for roadmap claims. `build_new_text` must be safe to call more
    than once (it's a pure function of the current file text, not a generator with
    side effects). Returns the final file text on success.
    """
    run_git(root, "fetch", "origin", "main", "-q")

    for attempt in range(1, max_attempts + 1):
        parent_sha = resolve_ref(root, remote_ref)
        before = read_file_at_ref(root, remote_ref, path)
        if before is None:
            raise GitError(f"{path} not found on {remote_ref}")

        after = build_new_text(before)
        if after == before:
            return after

        pushed = commit_file_on_ref(root, parent_sha, ref, path, after, message)
        if pushed:
            return after

        print(
            f"[append_ledger_entry] push race on attempt {attempt}/{max_attempts} "
            f"({path}: {remote_ref} moved) -- re-fetching and re-appending",
            file=sys.stderr,
        )
        run_git(root, "fetch", "origin", "main", "-q")

    raise GitError(
        f"could not append to {path} after {max_attempts} attempts (repeated push races on {remote_ref})"
    )


def build_talkback_append(before: str, entry: str) -> str:
    """Appends one TALKBACK entry, matching the file's existing '## heading, one blank
    line between entries' convention. Never touches a byte of any prior entry."""
    entry = entry.strip("\n")
    if not entry.startswith("## "):
        raise ValueError("TALKBACK entries must start with a '## ' heading line")

    text = before
    if not text.endswith("\n"):
        text += "\n"
    if not text.endswith("\n\n"):
        text += "\n"
    return text + entry + "\n"


def append_talkback_entry(root: Path, path: str, entry: str, message: str, **kwargs) -> str:
    """Appends `entry` (a full '## ...' TALKBACK section, e.g. the block described in
    TALKBACK.md's own format docstring) to the TALKBACK.md at `path` on origin/main."""
    return append_with_retry(
        root, path, lambda before: build_talkback_append(before, entry), message, **kwargs
    )


def build_learning_append(before: str, record: dict) -> str:
    """Appends one record to LEARNING.yaml as new trailing text -- mirrors
    process_task_events.py's write_learning_record so both writers produce the same
    on-disk shape, but returns the new text instead of writing a local file (this
    module never touches the caller's working tree; see append_with_retry)."""
    ledger = yaml.safe_load(before) or {}
    fragment = yaml.safe_dump(
        [record], sort_keys=False, default_flow_style=False, width=100, allow_unicode=True
    )
    if ledger.get("records"):
        text = before
        if not text.endswith("\n"):
            text += "\n"
        return text + fragment
    return "records:\n" + fragment


def append_learning_record(
    root: Path, record: dict, message: str, *, path: str = LEARNING_PATH, **kwargs
) -> str:
    return append_with_retry(
        root, path, lambda before: build_learning_append(before, record), message, **kwargs
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="mode", required=True)

    talkback = sub.add_parser("talkback", help="Append a TALKBACK.md entry")
    talkback.add_argument(
        "path", help="Path to the TALKBACK.md file, e.g. TALKBACK.md or projects/<p>/TALKBACK.md"
    )
    talkback.add_argument(
        "--file", required=True, help="File holding the full '## ...' entry text to append"
    )
    talkback.add_argument("--message", required=True, help="Commit message")

    learning = sub.add_parser("learning", help="Append a LEARNING.yaml record")
    learning.add_argument("--file", required=True, help="YAML file holding one record mapping")
    learning.add_argument("--message", required=True, help="Commit message")
    learning.add_argument(
        "--path", default=LEARNING_PATH, help=f"Path to LEARNING.yaml (default: {LEARNING_PATH})"
    )

    args = parser.parse_args()

    if args.mode == "talkback":
        entry = Path(args.file).read_text(encoding="utf-8")
        try:
            append_talkback_entry(ROOT, args.path, entry, args.message)
        except (GitError, ValueError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        print(f"Appended TALKBACK entry to {args.path}")
        return 0

    if args.mode == "learning":
        record = yaml.safe_load(Path(args.file).read_text(encoding="utf-8"))
        if not isinstance(record, dict):
            print("ERROR: --file must contain a single YAML mapping (one record)", file=sys.stderr)
            return 1
        try:
            append_learning_record(ROOT, record, args.message, path=args.path)
        except GitError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        print(f"Appended LEARNING.yaml record to {args.path}")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
