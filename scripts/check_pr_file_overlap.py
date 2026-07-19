#!/usr/bin/env python3
"""check_pr_file_overlap.py — advisory same-project open-PR file-overlap check.

Kaizen from newsfeed/t-008 + t-010 (Reviewer, kind_robots PR #484/#486,
2026-07-19, see newsfeed/t-016): two `claimed` newsfeed tasks both touched
newsfeed-feed.vue and contract-tests.yml and merged minutes apart, producing
an avoidable merge conflict discovered only when reviewing the second PR.

This is the lightweight Reviewer-side check that TALKBACK entry asked for:
before merging a PR, compare its changed-file set against every other
currently-open PR from the same project (project inferred from the
`<project>/t-NNN` task id referenced in the title/body, same convention as
check_pr_kaizen.py) and flag any overlap. Advisory only -- overlapping files
don't always conflict -- so it never blocks a merge, it just surfaces the
warning so the conflict is anticipated instead of discovered at merge time.

Pure function over data the caller already has (e.g. from the GitHub MCP
`list_pull_requests` / `pull_request_read(method="get_files")` results) --
no network calls of its own, same reasoning as check_pr_kaizen.py: keeps this
usable regardless of which credentials/connector the calling session has.

Usage:
    python scripts/check_pr_file_overlap.py --target target_pr.json --others other_prs.json
    python scripts/check_pr_file_overlap.py --target target_pr.json --others other_prs.json --json

Each PR JSON object has the shape:
    {"number": 846, "title": "...", "body": "...", "files": ["path/a.vue", "path/b.ts"]}

`--others` accepts a JSON array of such objects (other currently-open PRs to compare against).
Exit code is always 0 (advisory) unless usage/input is wrong.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

TASK_ID_RE = re.compile(r"\b([a-z][a-z0-9-]*)\/t-\d+\b")


def find_projects(text: str) -> list[str]:
    """Return the distinct project slugs referenced via <project>/t-NNN task ids, in order."""
    seen: list[str] = []
    for match in TASK_ID_RE.finditer(text):
        project = match.group(1)
        if project not in seen:
            seen.append(project)
    return seen


def find_overlaps(
    target: dict[str, Any], others: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Return, for each `others` PR sharing a project with `target`, the overlapping file set.

    Only PRs referencing at least one of the same project slugs as `target` are considered --
    a same-repo, different-project PR touching an unrelated file isn't the concern this guards
    against. PRs with no overlapping files are omitted from the result.
    """
    target_projects = set(find_projects(f"{target.get('title', '')}\n{target.get('body', '')}"))
    if not target_projects:
        return []
    target_files = set(target.get("files", []))
    if not target_files:
        return []

    results: list[dict[str, Any]] = []
    for other in others:
        if other.get("number") == target.get("number"):
            continue
        other_projects = set(find_projects(f"{other.get('title', '')}\n{other.get('body', '')}"))
        if not (target_projects & other_projects):
            continue
        overlap = target_files & set(other.get("files", []))
        if overlap:
            results.append(
                {
                    "number": other.get("number"),
                    "title": other.get("title", ""),
                    "shared_projects": sorted(target_projects & other_projects),
                    "overlapping_files": sorted(overlap),
                }
            )
    return results


def format_warning(target: dict[str, Any], overlaps: list[dict[str, Any]]) -> str:
    lines = [
        f"WARNING: PR #{target.get('number')} shares changed files with "
        f"{len(overlaps)} other open PR(s) from the same project. Not a blocker -- "
        "overlapping files don't always conflict -- but worth anticipating before merge "
        "(per newsfeed/t-016):"
    ]
    for o in overlaps:
        files = ", ".join(o["overlapping_files"])
        lines.append(f"  - PR #{o['number']} ({o['title']!r}): {files}")
    return "\n".join(lines)


def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--target", required=True, help="Path to JSON file describing the PR being reviewed")
    parser.add_argument("--others", required=True, help="Path to JSON file with an array of other open PRs")
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    args = parser.parse_args()

    target = _load_json(args.target)
    others = _load_json(args.others)
    if not isinstance(others, list):
        print("ERROR: --others must be a JSON array", file=sys.stderr)
        return 2

    overlaps = find_overlaps(target, others)

    if args.json:
        print(json.dumps({"target": target.get("number"), "overlaps": overlaps}, indent=2))
    elif overlaps:
        print(format_warning(target, overlaps))
    # Clean PR: print nothing, same convention as check_pr_kaizen.py.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
