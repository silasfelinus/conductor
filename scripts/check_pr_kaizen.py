#!/usr/bin/env python3
"""check_pr_kaizen.py — soft-flag a PR body missing the "Kaizen suggestion" section.

conductor/t-053: the PR handoff template (AGENTS.md) asks every task-referencing
PR for a "### Kaizen suggestion" section. Three PRs in one week (ai-art-academy/
t-023, t-027, kind-robots/t-034) shipped without one, each time caught only
because the Reviewer happened to notice by hand. This is the lightweight
Reviewer-side check that TALKBACK note asked for: run it against a PR's title +
body right before closing review.

This is a pure text check with no network access -- pass in the PR body you
already have (from the GitHub MCP `pull_request_read` result), it does not
fetch anything itself. That keeps it usable in this sandbox, where a prior
session found `$GITHUB_TOKEN` has no working REST API auth (see root
TALKBACK.md, 2026-07-17).

Usage:
    python scripts/check_pr_kaizen.py --body-file pr_body.txt [--title "..."]
    echo "$PR_BODY" | python scripts/check_pr_kaizen.py --title "..."
    python scripts/check_pr_kaizen.py --body "full PR body text" --title "..."

Exit code is always 0 (soft warning, never blocks) unless usage is wrong.
Prints nothing on a clean PR (no task id referenced, or section present).
"""
from __future__ import annotations

import argparse
import re
import sys

TASK_ID_RE = re.compile(r"\b[a-z][a-z0-9-]*\/t-\d+\b")
KAIZEN_HEADING_RE = re.compile(r"^#{1,6}\s*kaizen suggestion\b", re.IGNORECASE | re.MULTILINE)


def find_task_ids(text: str) -> list[str]:
    seen: list[str] = []
    for match in TASK_ID_RE.finditer(text):
        task_id = match.group(0)
        if task_id not in seen:
            seen.append(task_id)
    return seen


def has_kaizen_section(text: str) -> bool:
    return bool(KAIZEN_HEADING_RE.search(text))


def check(title: str, body: str) -> str | None:
    """Return a warning message, or None if the PR is clean."""
    combined = f"{title}\n{body}"
    task_ids = find_task_ids(combined)
    if not task_ids:
        return None
    if has_kaizen_section(body):
        return None
    ids = ", ".join(task_ids)
    return (
        f"WARNING: PR references task id(s) {ids} but has no "
        '"### Kaizen suggestion" section. Not a blocker -- some PRs genuinely '
        "have nothing to suggest -- but note it in the TALKBACK \"what to "
        "improve\" entry per conductor/t-053, rather than letting it pass "
        "silently."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", default="", help="PR title")
    parser.add_argument("--body", default=None, help="PR body text")
    parser.add_argument("--body-file", default=None, help="Path to a file containing the PR body")
    args = parser.parse_args()

    if args.body is not None:
        body = args.body
    elif args.body_file:
        with open(args.body_file, "r", encoding="utf-8") as f:
            body = f.read()
    else:
        body = sys.stdin.read()

    warning = check(args.title, body)
    if warning:
        print(warning)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
