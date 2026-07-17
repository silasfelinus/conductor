#!/usr/bin/env python3
"""
git_plumbing.py — build and push a single-file commit without touching the caller's
checked-out branch, working tree, or index.

claim_task.py uses this so claiming a task never disturbs whatever branch or
uncommitted changes a session already has checked out: the new commit is built
entirely against a scratch index and pushed straight to the target ref.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


class GitError(Exception):
    pass


def run_git(root: Path, *args: str, input: str | None = None, env: dict | None = None) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        input=input,
        text=True,
        capture_output=True,
        encoding="utf-8",
        env=env,
    )
    if result.returncode != 0:
        raise GitError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def resolve_ref(root: Path, ref: str) -> str:
    return run_git(root, "rev-parse", ref).strip()


def gpgsign_enabled(root: Path) -> bool:
    """True when this repo's git config has commit.gpgsign set to true.

    Uses a plain `git config --get` (exit 1 / empty when unset) rather than run_git,
    which would raise GitError on the common "not configured" case.
    """
    result = subprocess.run(
        ["git", "config", "--get", "commit.gpgsign"],
        cwd=root,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    return result.returncode == 0 and result.stdout.strip().lower() == "true"


def read_file_at_ref(root: Path, ref: str, path: str) -> str | None:
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=root,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        return None
    return result.stdout


def commit_file_on_ref(
    root: Path,
    parent_sha: str,
    ref: str,
    path: str,
    content: str,
    message: str,
) -> bool:
    """Commits `content` at `path` on top of `parent_sha` and pushes it to `ref`.

    Builds the tree/commit via a scratch index (GIT_INDEX_FILE), so the caller's real
    index, working tree, and HEAD are never touched. Returns True on a successful
    (fast-forward) push, False on a non-fast-forward rejection -- meaning the ref moved
    since `parent_sha` was read and the caller should re-fetch, re-check, and retry.
    Raises GitError for any other git failure.

    Signs the commit (`commit-tree -S`) when this repo's `commit.gpgsign` is true --
    `commit-tree` doesn't apply that config automatically the way porcelain `git commit`
    does, so without this the commit lands unsigned/"Unverified" even with signing
    configured. `-S` reads the same `user.signingkey`/`gpg.format` config `git commit -S`
    would, so no separate signing setup is needed here.
    """
    git_dir = run_git(root, "rev-parse", "--git-dir").strip()
    git_dir_path = (root / git_dir) if not Path(git_dir).is_absolute() else Path(git_dir)

    with tempfile.NamedTemporaryFile(dir=git_dir_path, prefix="claim-index-", delete=False) as handle:
        scratch_index = Path(handle.name)

    try:
        import os

        env = {**os.environ, "GIT_INDEX_FILE": str(scratch_index)}
        run_git(root, "read-tree", parent_sha, env=env)

        blob_sha = run_git(root, "hash-object", "-w", "--stdin", input=content, env=env).strip()
        run_git(root, "update-index", "--add", "--cacheinfo", f"100644,{blob_sha},{path}", env=env)
        tree_sha = run_git(root, "write-tree", env=env).strip()
        commit_tree_args = ["commit-tree", tree_sha, "-p", parent_sha, "-m", message]
        if gpgsign_enabled(root):
            commit_tree_args.append("-S")
        commit_sha = run_git(root, *commit_tree_args).strip()

        push = subprocess.run(
            ["git", "push", "origin", f"{commit_sha}:{ref}"],
            cwd=root,
            text=True,
            capture_output=True,
            encoding="utf-8",
        )
        if push.returncode == 0:
            return True
        stderr = push.stderr.lower()
        if "non-fast-forward" in stderr or "fetch first" in stderr or "stale info" in stderr:
            return False
        raise GitError(f"git push failed: {push.stderr.strip()}")
    finally:
        scratch_index.unlink(missing_ok=True)
