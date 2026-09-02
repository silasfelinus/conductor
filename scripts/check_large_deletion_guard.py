#!/usr/bin/env python3
"""
check_large_deletion_guard.py — flag a PR whose diff deletes a large fraction
of an append-mostly conductor file (projects/art-prompts.yaml, or any
projects/*/roadmap.yaml), even though nothing else in this repo's CI reads
the actual size of the change.

Kaizen from t-143's TALKBACK entry (root TALKBACK.md, 2026-09-02, "art-job
requeue audit"): conductor commit 0e671cd deleted 11,014 lines of
projects/art-prompts.yaml (577 Mandarin request rows plus three in-flight
missing-image requests) in one automated write, and nothing flagged it — no
check, no alert, no digest line. It was found only by chance while reading
git log for something unrelated. t-143's own fix (kind_robots#2320) addresses
the write-side root cause (a >1MB GitHub Contents-API blind-decode bug) with
an append-only invariant on that one call site, but there was no standing
guard on the conductor side for the general shape: any large deletion in a
file that is supposed to only grow.

This is deliberately a SOFT warning, not a hard CI gate. A deliberate large
prune (an archival pass, a roadmap reorganization) is legitimate; the point
is surfacing an unusually large deletion for a reviewer's attention before
merge, the way this incident had to be found by hand.

A file is flagged when a single base...head diff either:
  - deletes at least ABS_LINE_THRESHOLD lines from it, or
  - deletes at least PCT_LINE_THRESHOLD of its base line count, when the
    base file itself has at least MIN_BASE_LINES_FOR_PCT lines (small files
    are excluded from the percentage rule so a brand-new 10-line roadmap
    shrinking to 3 lines doesn't false-positive on a 70% swing).

Usage:
  python scripts/check_large_deletion_guard.py --base <ref> --head <ref>
  python scripts/check_large_deletion_guard.py --base origin/main --head HEAD --json

Exit codes: 0 = clean (or nothing to check), 1 = at least one large deletion
found. Wired into ci.yml's "Validate roadmap YAML" job with
`continue-on-error: true` so a finding is visible on the PR without blocking
merge — see AGENTS.md's "Hard vs soft needs-human" framing for why this
repo's soft checks report rather than gate.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

ABS_LINE_THRESHOLD = 500
PCT_LINE_THRESHOLD = 0.20
MIN_BASE_LINES_FOR_PCT = 50


def target_paths(root: Path | None = None) -> list[str]:
    """Repo-relative paths this guard watches: art-prompts.yaml and every
    project's roadmap.yaml. Returns path strings (not Path objects) since
    they're fed straight into git diff/show pathspecs."""
    root = root or ROOT
    paths = []
    art_prompts = root / "projects" / "art-prompts.yaml"
    if art_prompts.exists():
        paths.append("projects/art-prompts.yaml")
    for path in sorted(root.glob("projects/*/roadmap.yaml")):
        paths.append(str(path.relative_to(root)))
    return paths


def evaluate_deletion(
    path: str, base_line_count: int, removed_lines: int, added_lines: int
) -> dict[str, Any] | None:
    """Pure threshold check, independent of git — the part unit tests exercise
    directly without a real repo fixture."""
    if removed_lines <= 0:
        return None
    pct = removed_lines / base_line_count if base_line_count else 0.0
    large_absolute = removed_lines >= ABS_LINE_THRESHOLD
    large_fraction = base_line_count >= MIN_BASE_LINES_FOR_PCT and pct >= PCT_LINE_THRESHOLD
    if not (large_absolute or large_fraction):
        return None
    return {
        "path": path,
        "base_lines": base_line_count,
        "added_lines": added_lines,
        "removed_lines": removed_lines,
        "removed_pct": round(pct * 100, 1),
    }


def run_git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=True
    )
    return result.stdout


def numstat(base: str, head: str, paths: list[str], cwd: Path) -> list[tuple[int, int, str]]:
    """Return (added, removed, path) for each of `paths` that changed between
    base and head, via git's own diffstat rather than re-deriving it from
    two full file reads — respects renames/binary markers for free."""
    if not paths:
        return []
    output = run_git(
        ["diff", "--numstat", f"{base}...{head}", "--", *paths], cwd=cwd
    )
    rows = []
    for line in output.splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        added, removed, path = parts
        if added == "-" or removed == "-":
            continue  # binary file, numstat can't count lines
        rows.append((int(added), int(removed), path))
    return rows


def base_line_count(base: str, path: str, cwd: Path) -> int:
    """Line count of `path` at `base`, or 0 if the file didn't exist there
    (a brand-new file can't have "deleted" a fraction of itself)."""
    result = subprocess.run(
        ["git", "show", f"{base}:{path}"], cwd=cwd, capture_output=True, text=True
    )
    if result.returncode != 0:
        return 0
    return len(result.stdout.splitlines())


def scan(base: str, head: str, cwd: Path | None = None) -> dict[str, Any]:
    cwd = cwd or ROOT
    paths = target_paths(cwd)
    findings = []
    for added, removed, path in numstat(base, head, paths, cwd):
        base_count = base_line_count(base, path, cwd)
        finding = evaluate_deletion(path, base_count, removed, added)
        if finding:
            findings.append(finding)
    return {"base": base, "head": head, "findings": findings}


def render(result: dict[str, Any]) -> str:
    findings = result["findings"]
    if not findings:
        return "No large deletions found in art-prompts.yaml or any roadmap.yaml."
    lines = [f"Large deletion(s) found ({len(findings)}):"]
    for f in findings:
        lines.append(
            f"  - {f['path']}: {f['removed_lines']} line(s) removed of "
            f"{f['base_lines']} base line(s) ({f['removed_pct']}%), "
            f"{f['added_lines']} added"
        )
    lines.append(
        "\nSoft warning only -- a deliberate large prune (archival pass, "
        "reorganization) is legitimate. Confirm this deletion was intended "
        "before merging; see scripts/check_large_deletion_guard.py for context."
    )
    return "\n".join(lines)


def render_github_annotations(result: dict[str, Any]) -> str:
    lines = []
    for f in result["findings"]:
        lines.append(
            f"::warning file={f['path']}::Large deletion: {f['removed_lines']} of "
            f"{f['base_lines']} line(s) removed ({f['removed_pct']}%). Confirm this "
            "was intended before merging (soft warning, see "
            "scripts/check_large_deletion_guard.py)."
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="base ref to diff from (e.g. origin/main)")
    parser.add_argument("--head", default="HEAD", help="head ref to diff to (default: HEAD)")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument(
        "--github-annotations",
        action="store_true",
        help="emit ::warning:: lines for GitHub Actions log annotations instead of the plain report",
    )
    args = parser.parse_args()

    result = scan(args.base, args.head)

    if args.json:
        print(json.dumps(result, indent=2))
    elif args.github_annotations:
        annotations = render_github_annotations(result)
        if annotations:
            print(annotations)
        print(render(result))
    else:
        print(render(result))

    sys.exit(1 if result["findings"] else 0)


if __name__ == "__main__":
    main()
