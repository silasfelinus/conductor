#!/usr/bin/env python3
"""
build_pr_triage.py — generate PR-TRIAGE.md from roadmaps + GitHub PR API.

Usage:
    python scripts/build_pr_triage.py [--dry-run] [--output PATH]

Requires GITHUB_TOKEN env var for PR API. Gracefully degrades (roadmap-only
view) if the token is absent or the API is unreachable.

Output: PR-TRIAGE.md at repo root (or --output path).
"""

import argparse
import json
import os
import pathlib
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

import yaml


# ---------------------------------------------------------------------------
# Roadmap helpers
# ---------------------------------------------------------------------------

PROJECTS_DIR = pathlib.Path("projects")
OVERRIDES_FILE = pathlib.Path("project-overrides.yaml")


def load_overrides() -> dict:
    if not OVERRIDES_FILE.exists():
        return {}
    raw = yaml.safe_load(OVERRIDES_FILE.read_text()) or {}
    return raw.get("projects", raw)


def active_slugs(overrides: dict) -> list:
    return [
        slug
        for slug, cfg in overrides.items()
        if isinstance(cfg, dict) and cfg.get("status") == "active"
    ]


def load_roadmap(slug: str) -> dict | None:
    f = PROJECTS_DIR / slug / "roadmap.yaml"
    if not f.exists():
        return None
    try:
        return yaml.safe_load(f.read_text()) or {}
    except yaml.YAMLError:
        return None


def tasks_in_flight(roadmap: dict) -> list[dict]:
    """Return tasks that are claimed, review, needs-human, blocked, or challenged."""
    in_flight_statuses = {"claimed", "review", "needs-human", "blocked", "challenged"}
    return [
        t for t in roadmap.get("tasks", [])
        if isinstance(t, dict) and t.get("status") in in_flight_statuses
    ]


def pending_human_gates(roadmap: dict) -> list[dict]:
    """Return tasks where gate_human is true and approved_by_human is false/absent."""
    return [
        t for t in roadmap.get("tasks", [])
        if isinstance(t, dict)
        and t.get("gate_human") is True
        and not t.get("approved_by_human", False)
        and t.get("status") not in ("waiting",)
    ]


# ---------------------------------------------------------------------------
# GitHub API helpers
# ---------------------------------------------------------------------------

REPO = "silasfelinus/conductor"
GITHUB_API = "https://api.github.com"


def gh_get(path: str, token: str) -> dict | list | None:
    url = f"{GITHUB_API}{path}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"WARNING: GitHub API {path} returned {e.code}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"WARNING: GitHub API request failed: {e}", file=sys.stderr)
        return None


def fetch_open_prs(token: str) -> list[dict]:
    """Fetch open PRs from worker/* branches into main."""
    data = gh_get(f"/repos/{REPO}/pulls?state=open&base=main&per_page=100", token)
    if not isinstance(data, list):
        return []
    return [
        pr for pr in data
        if isinstance(pr, dict)
        and pr.get("head", {}).get("ref", "").startswith("worker/")
    ]


def pr_slug_task(pr: dict) -> tuple[str, str]:
    """Extract project slug and task-id from a branch name like worker/project-t-001."""
    ref = pr.get("head", {}).get("ref", "")
    # Strip 'worker/' prefix
    body = ref[len("worker/"):] if ref.startswith("worker/") else ref
    # Try to detect task id pattern (e.g. '-t-001')
    import re
    m = re.search(r"-?(t-\d+)$", body)
    if m:
        task_id = m.group(1)
        slug = body[: -(len(task_id) + 1)]
    else:
        slug = body
        task_id = "?"
    return slug, task_id


def pr_mergeable_label(pr: dict) -> str:
    state = pr.get("mergeable_state", "unknown")
    # mergeable_state values: clean, unstable, dirty, blocked, behind, draft, unknown
    labels = {
        "clean": "✓ mergeable",
        "unstable": "⚠ checks failing",
        "dirty": "✗ merge conflict",
        "blocked": "⛔ branch protection",
        "behind": "↑ needs rebase",
        "draft": "⊘ draft",
        "unknown": "? (not yet computed)",
    }
    return labels.get(state, state)


# ---------------------------------------------------------------------------
# Report assembly
# ---------------------------------------------------------------------------

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_report(
    slugs: list[str],
    roadmaps: dict[str, dict],
    prs: list[dict],
    token_present: bool,
) -> str:
    lines: list[str] = []
    ts = now_iso()

    lines.append("# PR-TRIAGE.md — open worker PRs snapshot")
    lines.append("")
    lines.append(f"Generated: {ts}")
    lines.append(f"Repo: {REPO}")
    if not token_present:
        lines.append("> ⚠ GITHUB_TOKEN not set — GitHub PR data omitted; roadmap view only.")
    lines.append("")

    # -----------------------------------------------------------------------
    # Section 1: Open worker PRs
    # -----------------------------------------------------------------------
    lines.append("## Open worker/* PRs")
    lines.append("")

    if not token_present or not prs:
        if not token_present:
            lines.append("_GitHub data unavailable — set GITHUB_TOKEN to populate this section._")
        else:
            lines.append("_No open worker/* PRs targeting main._")
    else:
        lines.append("| PR | Branch | Slug | Task | Status | Mergeability | Opened | Next action |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for pr in sorted(prs, key=lambda p: p.get("number", 0)):
            num = pr.get("number", "?")
            title = pr.get("title", "untitled")[:60]
            ref = pr.get("head", {}).get("ref", "?")
            slug, task_id = pr_slug_task(pr)
            road = roadmaps.get(slug, {})
            task = next(
                (t for t in road.get("tasks", []) if t.get("id") == task_id),
                None,
            )
            status = task.get("status", "?") if task else "?"
            gate = ""
            if task and task.get("gate_human") and not task.get("approved_by_human"):
                gate = " 🔑 awaiting Silas"
            elif task and task.get("stakes") in ("irreversible", "outward-facing"):
                gate = f" ⚠ {task['stakes']}"
            merge_label = pr_mergeable_label(pr)
            created = pr.get("created_at", "")[:10]

            # Derive next action
            if status == "needs-human":
                next_action = "Silas reviews"
            elif status == "review":
                next_action = "Reviewer merges or rejects"
            elif status == "blocked":
                passes = task.get("passes", "?") if task else "?"
                next_action = f"Blocked (pass {passes}) — Silas or Reviewer unblocks"
            elif status == "challenged":
                next_action = "Reviewer reads TALKBACK, responds"
            elif "conflict" in merge_label:
                next_action = "Worker rebases"
            elif "failing" in merge_label:
                next_action = "Worker fixes CI"
            else:
                next_action = "Ready to merge"

            url = pr.get("html_url", "")
            pr_link = f"[#{num}]({url})" if url else f"#{num}"
            lines.append(
                f"| {pr_link} | `{ref}` | {slug} | {task_id} | `{status}`{gate} | {merge_label} | {created} | {next_action} |"
            )

    lines.append("")

    # -----------------------------------------------------------------------
    # Section 2: In-flight tasks (roadmap view, no PR data needed)
    # -----------------------------------------------------------------------
    lines.append("## In-flight tasks (roadmap snapshot)")
    lines.append("")
    lines.append(
        "Tasks that are `claimed`, `review`, `needs-human`, `blocked`, or `challenged` "
        "across all active projects."
    )
    lines.append("")

    in_flight_rows: list[tuple[str, str, str, str]] = []
    for slug in sorted(slugs):
        road = roadmaps.get(slug, {})
        for t in tasks_in_flight(road):
            status = t.get("status", "?")
            title = t.get("title", "?")[:60]
            in_flight_rows.append((slug, t.get("id", "?"), status, title))

    if not in_flight_rows:
        lines.append("_No in-flight tasks across active projects._")
    else:
        lines.append("| Project | Task | Status | Title |")
        lines.append("|---|---|---|---|")
        for slug, tid, status, title in in_flight_rows:
            lines.append(f"| {slug} | {tid} | `{status}` | {title} |")

    lines.append("")

    # -----------------------------------------------------------------------
    # Section 3: Pending human gates
    # -----------------------------------------------------------------------
    lines.append("## Pending human approval gates")
    lines.append("")
    lines.append(
        "Tasks with `gate_human: true` and `approved_by_human: false` that are NOT `waiting`. "
        "Silas must approve these before their dependents can unblock."
    )
    lines.append("")

    gate_rows: list[tuple[str, str, str, str]] = []
    for slug in sorted(slugs):
        road = roadmaps.get(slug, {})
        for t in pending_human_gates(road):
            status = t.get("status", "?")
            title = t.get("title", "?")[:60]
            gate_rows.append((slug, t.get("id", "?"), status, title))

    if not gate_rows:
        lines.append("_No pending human approval gates._")
    else:
        lines.append("| Project | Task | Status | Title |")
        lines.append("|---|---|---|---|")
        for slug, tid, status, title in gate_rows:
            lines.append(f"| {slug} | {tid} | `{status}` | {title} |")

    lines.append("")
    lines.append("---")
    lines.append(f"_Auto-generated by `scripts/build_pr_triage.py` at {ts}_")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Build PR-TRIAGE.md")
    parser.add_argument("--dry-run", action="store_true", help="Print report; do not write file")
    parser.add_argument("--output", default="PR-TRIAGE.md", help="Output file path (default: PR-TRIAGE.md)")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN", "")
    token_present = bool(token)

    overrides = load_overrides()
    slugs = active_slugs(overrides)

    roadmaps: dict[str, dict] = {}
    for slug in slugs:
        rd = load_roadmap(slug)
        if rd:
            roadmaps[slug] = rd

    prs: list[dict] = []
    if token_present:
        print("Fetching open PRs from GitHub…", file=sys.stderr)
        prs = fetch_open_prs(token)
        print(f"  Found {len(prs)} open worker/* PR(s).", file=sys.stderr)
    else:
        print("WARNING: GITHUB_TOKEN not set — skipping PR API.", file=sys.stderr)

    report = build_report(slugs, roadmaps, prs, token_present)

    if args.dry_run:
        print(report)
    else:
        out = pathlib.Path(args.output)
        out.write_text(report)
        print(f"Written: {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
