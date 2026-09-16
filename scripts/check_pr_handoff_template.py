#!/usr/bin/env python3
"""Validate the required Worker PR handoff sections.

The check is intentionally small and transport-agnostic: CI passes the pull request
body on stdin. Non-worker branches are ignored so human/close/reviewer PRs are not
forced into the Worker handoff format.
"""

from __future__ import annotations

import argparse
import sys

REQUIRED_SECTIONS = (
    "### Task",
    "### What changed / what I produced",
    "### How I verified",
    "### Stakes",
    "### Kaizen suggestion",
    "### Notes for reviewer",
)


def missing_sections(body: str) -> list[str]:
    return [heading for heading in REQUIRED_SECTIONS if heading not in body]


def github_error_annotation(heading: str) -> str:
    """Return a GitHub Actions workflow-command annotation for a missing heading."""
    return f"::error title=Worker PR handoff incomplete::Missing required heading: {heading}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--head-ref", required=True)
    args = parser.parse_args()

    if not args.head_ref.startswith("worker/"):
        print(f"SKIP: {args.head_ref} is not a worker/* branch")
        return 0

    body = sys.stdin.read()
    missing = missing_sections(body)
    if missing:
        print(github_error_annotation(missing[0]), file=sys.stderr)
        print("ERROR: Worker PR body is missing required handoff section(s):", file=sys.stderr)
        for heading in missing:
            print(f"  - {heading}", file=sys.stderr)
        print(
            "Flags for Reviewer is optional when there is nothing to flag; all other "
            "AGENTS.md handoff headings must be present.",
            file=sys.stderr,
        )
        return 1

    print("OK: Worker PR body contains the required handoff sections")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
