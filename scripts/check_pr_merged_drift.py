#!/usr/bin/env python3
"""
check_pr_merged_drift.py — Flag conductor tasks stuck at claimed/review whose
referenced cross-repo PR has already merged.

Kaizen from conductor/t-071 (Reviewer, burst-mode, 2026-07-19, from
newsfeed/t-020): the conductor claim commit for a task can land, and then the
real implementation (a PR in a target repo like kind_robots) can merge minutes
later with no `status: review` checkpoint ever recorded in between. Roadmap
state alone then gives no signal the work is already done — the last session
that hit this only caught it by manually re-checking kind_robots' commit
history on its next sweep. This script closes that gap: it scans every
projects/*/roadmap.yaml for tasks at `status: claimed` or `status: review`
whose `title`/`note` names a specific cross-repo PR (e.g. "kind_robots PR
#517", "conductor PR #503"), looks up that PR's merge state via the GitHub
API, and flags any that are already merged — the drift a Reviewer sweep
should catch and close out within the same cycle instead of relying on luck.

Read-only: never edits a roadmap. Bare "PR #N" references with no recognized
repo prefix are ambiguous across repos and are skipped, not guessed.

Usage:
  python scripts/check_pr_merged_drift.py            # human-readable report, exit 1 on drift
  python scripts/check_pr_merged_drift.py --json      # machine-readable findings

Requires: GITHUB_TOKEN env var (recommended; avoids rate limits, required for
private repos).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"
IN_PROGRESS = {"claimed", "review"}

# Repos this conductor instance tracks cross-repo work against. Keep in sync
# with the actual GitHub remotes agents push to (see CLAUDE.md repo scope).
REPO_ALIASES = {
    "conductor": "silasfelinus/conductor",
    "kind_robots": "silasfelinus/kind_robots",
    "kind-robots": "silasfelinus/kind_robots",
    "kindrobots-unraid": "silasfelinus/kindrobots-unraid",
    "serendipity-voice": "silasfelinus/serendipity-voice",
    "comfyui": "silasfelinus/comfyui",
    "ComfyUI": "silasfelinus/comfyui",
    "portos": "silasfelinus/PortOS",
    "PortOS": "silasfelinus/PortOS",
}

PR_REF_RE = re.compile(
    r"\b(" + "|".join(re.escape(a) for a in REPO_ALIASES) + r")\s+PR\s+#(\d+)\b"
)


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def find_pr_refs(text: str) -> list[tuple[str, int]]:
    """Return deduped (owner/repo, pr_number) pairs referenced in text."""
    seen: list[tuple[str, int]] = []
    for alias, number in PR_REF_RE.findall(text or ""):
        pair = (REPO_ALIASES[alias], int(number))
        if pair not in seen:
            seen.append(pair)
    return seen


def scan(projects_dir: Path = PROJECTS) -> list[dict[str, Any]]:
    """Find every claimed/review task with a resolvable cross-repo PR reference."""
    candidates = []
    for roadmap_path in sorted(projects_dir.glob("*/roadmap.yaml")):
        slug = roadmap_path.parent.name
        if slug == "_template":
            continue
        data = load_yaml(roadmap_path)
        for task in data.get("tasks", []) or []:
            status = task.get("status")
            if status not in IN_PROGRESS:
                continue
            text = f"{task.get('title', '')}\n{task.get('note', '')}"
            for repo, number in find_pr_refs(text):
                candidates.append({
                    "project": slug,
                    "task_id": task.get("id"),
                    "title": task.get("title"),
                    "status": status,
                    "repo": repo,
                    "pr_number": number,
                })
    return candidates


def gh_pr(repo: str, number: int, token: str | None) -> dict | None:
    url = f"https://api.github.com/repos/{repo}/pulls/{number}"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "conductor-check-pr-merged-drift/1.0",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"  [gh] {repo}#{number}: HTTP {e.code}", file=sys.stderr)
        return None
    except Exception as e:  # noqa: BLE001 — best-effort network call, never fatal
        print(f"  [gh] {repo}#{number}: {e}", file=sys.stderr)
        return None


def check(candidates: list[dict[str, Any]], token: str | None) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return (findings, unresolved). `unresolved` holds candidates whose PR
    lookup failed (network/auth error) — these were NOT verified either way
    and must not be reported as "clean"."""
    findings = []
    unresolved = []
    for c in candidates:
        pr = gh_pr(c["repo"], c["pr_number"], token)
        if not pr:
            unresolved.append(c)
            continue
        if pr.get("merged") or pr.get("merged_at"):
            findings.append({
                **c,
                "pr_merged_at": pr.get("merged_at"),
                "pr_title": pr.get("title"),
            })
    return findings, unresolved


def render(findings: list[dict[str, Any]], unresolved: list[dict[str, Any]], total: int) -> str:
    lines = []
    if unresolved:
        lines.append(
            f"⚠  {len(unresolved)}/{total} candidate(s) could NOT be verified (API lookup failed — "
            f"see stderr for HTTP codes). This is common in sandboxed sessions that only have "
            f"GitHub MCP tools, not direct API/token access — a raw urllib call to api.github.com "
            f"will 403 there even with GITHUB_TOKEN set. Do not treat this run as a clean audit; "
            f"re-check the unresolved task(s) via the GitHub MCP `pull_request_read` tool instead:"
        )
        for c in unresolved:
            lines.append(f"    {c['project']}/{c['task_id']} -> {c['repo']}#{c['pr_number']}")
        lines.append("")
    if findings:
        lines.append(f"Found {len(findings)} task(s) at claimed/review whose referenced PR already merged:\n")
        for f in findings:
            lines.append(
                f"  {f['project']}/{f['task_id']} (status: {f['status']}) references "
                f"{f['repo']}#{f['pr_number']} \"{f['pr_title']}\", merged {f['pr_merged_at']}"
            )
    elif not unresolved:
        lines.append(f"No drift found — all {total} claimed/review PR reference(s) verified still open.")
    elif len(unresolved) < total:
        lines.append(f"No drift found among the {total - len(unresolved)} candidate(s) successfully verified.")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("⚠  GITHUB_TOKEN not set — rate limits apply", file=sys.stderr)

    candidates = scan()
    findings, unresolved = check(candidates, token)

    if args.json:
        print(json.dumps({"findings": findings, "unresolved": unresolved}, indent=2))
    else:
        print(render(findings, unresolved, len(candidates)))

    # Exit codes: 0 = verified clean, 1 = drift found, 2 = could not fully
    # verify (some/all lookups failed) — distinct from "clean" so callers
    # (and agent sessions) don't mistake an unverified run for a passing one.
    if findings:
        sys.exit(1)
    if unresolved:
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
