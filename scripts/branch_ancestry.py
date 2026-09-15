#!/usr/bin/env python3
"""branch_ancestry.py — pure commit-relationship classifier (conductor/t-163).

Factored out of close_task.py's ``assert_local_branch_safe`` (conductor/t-161), which
only needed a binary equal/not-equal check between a named local branch and the remote
tip it was about to build a close-out commit on top of. That binary check cannot tell
"local has unpushed commits beyond remote" (the actual t-161 danger — building on the
stale remote tip would silently omit them) apart from "remote has moved ahead of a
stale local checkout" (no unpushed work at risk) or "the two have genuinely diverged"
(real ambiguity). This module makes that three/four-way classification a small, pure,
independently testable primitive so other branch-plumbing scripts (``claim_task.py``'s
branch-naming paths were flagged as worth checking for the same assumption class) can
reuse one tested function instead of re-deriving an equality-only comparison each time.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

try:
    from scripts.git_plumbing import GitError, resolve_ref
except ImportError:
    from git_plumbing import GitError, resolve_ref

RelationshipT = str  # one of: "equal" | "ahead" | "behind" | "diverged"


def classify_relationship(root: Path, a: str, b: str) -> RelationshipT:
    """Classify commit-ish ``a`` relative to commit-ish ``b``.

    Returns one of:
      "equal"    — ``a`` and ``b`` resolve to the same commit.
      "ahead"    — ``a`` is a descendant of ``b`` (``b`` is an ancestor of ``a``): ``a``
                   has every commit ``b`` has, plus more. This is the ordinary state of
                   a local branch with commits not yet pushed to its remote counterpart.
      "behind"   — ``b`` is a descendant of ``a`` (``a`` is an ancestor of ``b``): ``b``
                   has every commit ``a`` has, plus more. This is the ordinary state of
                   a stale local checkout whose remote has moved on without it.
      "diverged" — neither is an ancestor of the other: they share a common ancestor,
                   but each has commits the other lacks. Real ambiguity — no
                   fast-forward in either direction resolves it.

    Raises ``GitError`` if either ref cannot be resolved.
    """
    a_sha = resolve_ref(root, a)
    b_sha = resolve_ref(root, b)
    if a_sha == b_sha:
        return "equal"
    b_is_ancestor_of_a = _is_ancestor(root, b_sha, a_sha)
    a_is_ancestor_of_b = _is_ancestor(root, a_sha, b_sha)
    if b_is_ancestor_of_a and not a_is_ancestor_of_b:
        return "ahead"
    if a_is_ancestor_of_b and not b_is_ancestor_of_a:
        return "behind"
    return "diverged"


def _is_ancestor(root: Path, maybe_ancestor: str, descendant: str) -> bool:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", maybe_ancestor, descendant],
        cwd=root,
        capture_output=True,
        text=True,
    )
    # `git merge-base --is-ancestor` uses its exit code as the answer: 0 = yes, 1 = no.
    # Anything else (128, missing objects, etc.) is a real error, not "no".
    if result.returncode in (0, 1):
        return result.returncode == 0
    raise GitError(
        f"git merge-base --is-ancestor {maybe_ancestor} {descendant} failed: "
        f"{result.stderr.strip()}"
    )
