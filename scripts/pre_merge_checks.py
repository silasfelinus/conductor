#!/usr/bin/env python3
"""pre_merge_checks.py — run every advisory pre-merge PR check in one pass.

conductor/t-070: check_pr_kaizen.py and check_pr_file_overlap.py are both
pure, no-network, always-exit-0 advisory checks over data a Reviewer already
has from the GitHub MCP (`pull_request_read`, `list_pull_requests`) before
merging a PR. Having two separate scripts with the same invocation shape
means a Reviewer has to remember to run both every time. This script is
purely a shared invocation surface -- it imports and calls each check's
existing function unchanged, then prints their combined output. It does not
merge the checks' logic; each keeps its own module, tests, and behavior.

Usage:
    python scripts/pre_merge_checks.py --target target_pr.json --others other_prs.json
    python scripts/pre_merge_checks.py --target target_pr.json --others other_prs.json --json

`--target` is a JSON file shaped like:
    {"number": 846, "title": "...", "body": "...", "files": ["path/a.vue"]}
(the same shape check_pr_file_overlap.py already expects). `--others` is a
JSON array of other currently-open PRs in the same shape (pass `[]` if there
are none, or you only want the kaizen check).

Exit code is always 0 (advisory only) unless usage/input is wrong.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_pr_file_overlap as file_overlap  # noqa: E402
import check_pr_kaizen as kaizen  # noqa: E402


def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_checks(target: dict[str, Any], others: list[dict[str, Any]]) -> dict[str, Any]:
    """Run every advisory check against `target` (and `others` for overlap) and
    return a dict of check-name -> result (kaizen: str | None, overlap: list)."""
    kaizen_warning = kaizen.check(target.get("title", ""), target.get("body", ""))
    overlaps = file_overlap.find_overlaps(target, others)
    return {"kaizen": kaizen_warning, "overlap": overlaps}


def format_results(target: dict[str, Any], results: dict[str, Any]) -> str:
    lines = []
    if results["kaizen"]:
        lines.append(results["kaizen"])
    if results["overlap"]:
        lines.append(file_overlap.format_warning(target, results["overlap"]))
    return "\n\n".join(lines)


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

    results = run_checks(target, others)

    if args.json:
        print(json.dumps({"target": target.get("number"), **results}, indent=2))
    else:
        text = format_results(target, results)
        if text:
            print(text)
    # Clean PR: print nothing, same convention as the individual checks.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
