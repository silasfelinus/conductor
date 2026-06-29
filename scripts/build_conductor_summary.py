#!/usr/bin/env python3
"""
build_conductor_summary.py — hourly conductor health assessment.

Checks both repos (conductor + kind_robots) via GitHub API, scans local
roadmaps for blockers, fetches open todos from kind_robots, then calls
Claude to produce a brief actionable summary.

Writes CONDUCTOR-REPORT.md (or prints to stdout with --dry-run).

Usage:  python scripts/build_conductor_summary.py [--dry-run]
Env:    ANTHROPIC_API_KEY  (required for LLM assessment; falls back to rules)
        GITHUB_TOKEN       (recommended; avoids rate limits)
        KR_API_TOKEN       (optional; fetches open todos from kind_robots)
"""

from __future__ import annotations

import argparse
import datetime
import glob
import json
import os
import sys
import urllib.error
import urllib.request

try:
    import yaml
except ImportError:
    sys.exit("PyYAML not installed — run: pip install pyyaml")

REPOS = [
    {"owner": "silasfelinus", "name": "conductor"},
    {"owner": "silasfelinus", "name": "kind_robots"},
]
KR_API_URL = "https://kind-robots.vercel.app/api/todos"
REPORT_PATH = "CONDUCTOR-REPORT.md"
STALE_CLAIMED_HOURS = 4   # flag tasks stuck in "claimed" longer than this
STALE_PR_HOURS = 8        # flag worker/* PRs open longer than this without review
UTC = datetime.timezone.utc


# ── Helpers ──────────────────────────────────────────────────────────────────

def _now() -> datetime.datetime:
    return datetime.datetime.now(UTC)


def _age_hours(iso: str) -> float:
    if not iso:
        return 0.0
    try:
        dt = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return (_now() - dt).total_seconds() / 3600
    except ValueError:
        return 0.0


def _gh(path: str, token: str | None, params: dict | None = None) -> object:
    url = f"https://api.github.com/{path}"
    if params:
        url += "?" + "&".join(f"{k}={v}" for k, v in params.items())
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "conductor-hourly/1.0",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"  [gh] {path}: {e}", file=sys.stderr)
        return {}


# ── Data gathering ───────────────────────────────────────────────────────────

def fetch_repo(owner: str, name: str, token: str | None) -> dict:
    since_24h = (_now() - datetime.timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Recent commits (skip bot noise)
    raw = _gh(f"repos/{owner}/{name}/commits", token, {"since": since_24h, "per_page": "30"})
    commits = []
    if isinstance(raw, list):
        for c in raw:
            msg = c.get("commit", {}).get("message", "").splitlines()[0]
            if "[skip ci]" in msg or msg.startswith("chore: refresh STATUS"):
                continue
            commits.append({
                "sha": c["sha"][:7],
                "message": msg,
                "author": c.get("commit", {}).get("author", {}).get("name", "?"),
            })

    # Open PRs — flag stale worker/* PRs waiting for Reviewer
    raw = _gh(f"repos/{owner}/{name}/pulls", token, {"state": "open", "per_page": "20"})
    open_prs, stale_worker_prs = [], []
    if isinstance(raw, list):
        for pr in raw:
            branch = pr.get("head", {}).get("ref", "")
            age = _age_hours(pr.get("created_at", ""))
            entry = {
                "number": pr["number"],
                "title": pr["title"],
                "branch": branch,
                "author": pr.get("user", {}).get("login", "?"),
                "age_hours": round(age, 1),
                "draft": pr.get("draft", False),
            }
            open_prs.append(entry)
            if branch.startswith("worker/") and age > STALE_PR_HOURS and not pr.get("draft"):
                stale_worker_prs.append(entry)

    # Open issues (exclude PRs)
    raw = _gh(f"repos/{owner}/{name}/issues", token, {"state": "open", "per_page": "20"})
    issues = []
    if isinstance(raw, list):
        for iss in raw:
            if "pull_request" not in iss:
                issues.append({
                    "number": iss["number"],
                    "title": iss["title"],
                    "labels": [la["name"] for la in iss.get("labels", [])],
                })

    # Recent CI runs on main
    raw = _gh(f"repos/{owner}/{name}/actions/runs", token, {"per_page": "10", "branch": "main"})
    ci_recent, failing_ci = [], []
    if isinstance(raw, dict):
        for run in raw.get("workflow_runs", [])[:10]:
            conclusion = run.get("conclusion")
            ci_recent.append({"name": run["name"], "status": run["status"], "conclusion": conclusion})
            if conclusion == "failure":
                failing_ci.append(run["name"])

    return {
        "repo": f"{owner}/{name}",
        "commits_24h": commits,
        "open_prs": open_prs,
        "stale_worker_prs": stale_worker_prs,
        "open_issues": issues,
        "ci_recent": ci_recent[:5],
        "failing_ci": failing_ci,
    }


def fetch_roadmaps() -> dict:
    """Scan all local project roadmaps for health signals."""
    blocked, needs_human, stale_claimed = [], [], []
    ready = waiting = in_review = 0

    for path in sorted(glob.glob("projects/*/roadmap.yaml")):
        if "_template" in path:
            continue
        rm = yaml.safe_load(open(path)) or {}
        project = rm.get("project", "?")
        kind = rm.get("kind", "software")

        for t in rm.get("tasks", []):
            status = t.get("status")
            tid = f"{project}/{t.get('id', '?')}"
            title = t.get("title", "")

            if status == "blocked":
                blocked.append({
                    "id": tid, "title": title, "kind": kind, "passes": t.get("passes", 0)
                })
            elif status == "needs-human":
                needs_human.append({"id": tid, "title": title, "kind": kind})
            elif status == "claimed":
                age = _age_hours(t.get("updated", ""))
                if age > STALE_CLAIMED_HOURS:
                    stale_claimed.append({"id": tid, "title": title, "age_hours": round(age, 1)})
            elif status == "ready":
                ready += 1
            elif status == "waiting":
                waiting += 1
            elif status == "review":
                in_review += 1

    return {
        "blocked": blocked,
        "needs_human": needs_human,
        "stale_claimed": stale_claimed,
        "ready": ready,
        "waiting": waiting,
        "in_review": in_review,
    }


def fetch_todos(token: str | None) -> list:
    if not token:
        return []
    req = urllib.request.Request(
        KR_API_URL,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read())
        prio = {"HIGH": 0, "NORMAL": 1, "LOW": 2}
        open_todos = sorted(
            [t for t in body.get("data", []) if t.get("status") == "OPEN"],
            key=lambda t: (prio.get(t.get("priority", "NORMAL"), 1), -(t.get("id") or 0)),
        )
        return [
            {"id": t.get("id"), "title": t.get("title"), "priority": t.get("priority")}
            for t in open_todos
        ]
    except Exception as e:
        print(f"  [todos] {e}", file=sys.stderr)
        return []


# ── Claude assessment ────────────────────────────────────────────────────────

SYSTEM = """\
You are the Conductor — the project manager for an autonomous AI coordination system called AI_Networker.
You run every hour to assess the health of two GitHub repos:
- conductor (the orchestration layer: CI, scripts, task roadmaps, agent protocols)
- kind_robots (the main app and public-facing service)

Review the state data and produce a brief, scannable report. Your job:
1. Identify real signals: CI failures, blocked tasks, needs-human gates, stale PRs, open todos.
2. Ignore noise: chore commits, skip-ci, bot status refreshes.
3. Decide: does anything need Silas's attention, or is the autonomous loop running smoothly?

Output format (tight markdown, no preamble):
- Open with `## ACTION NEEDED` or `## ALL CLEAR`
- If action needed: bullet the top 1–3 items. For each: what it is, why it matters, specific next step.
  Reference exact IDs (e.g. conductor/t-001, PR #42, workflow "CI").
- If all clear: one summary sentence.
- Always end with:
  `**Stats:** {ready} ready | {waiting} waiting | {blocked} blocked | {needs-human} needs-human | {todos} open todos`

Under 250 words. No filler.
"""


def assess(state: dict) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("  ANTHROPIC_API_KEY not set — rule-based fallback", file=sys.stderr)
        return _fallback(state)

    payload = json.dumps({
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 400,
        "system": SYSTEM,
        "messages": [{
            "role": "user",
            "content": (
                f"State as of {state['as_of']}:\n\n"
                f"```json\n{json.dumps(state, indent=2)}\n```"
            ),
        }],
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read())
        return body["content"][0]["text"].strip()
    except Exception as e:
        print(f"  Claude call failed: {e} — rule-based fallback", file=sys.stderr)
        return _fallback(state)


def _fallback(state: dict) -> str:
    """Rule-based summary when Claude is unavailable."""
    rm = state.get("roadmap", {})
    items = []

    for r in state.get("repos", []):
        for wf in r.get("failing_ci", []):
            items.append(f"**CI failure** in `{r['repo']}` — `{wf}`: investigate and fix.")
        for pr in r.get("stale_worker_prs", []):
            items.append(
                f"**Stale worker PR** #{pr['number']} in `{r['repo']}` "
                f"({pr['age_hours']}h old): Reviewer should assess."
            )

    for t in rm.get("blocked", []):
        items.append(
            f"**Blocked:** `{t['id']}` — {t['title']} "
            f"(passes: {t.get('passes', '?')}): Silas must unblock or retire."
        )
    for t in rm.get("needs_human", []):
        items.append(f"**Needs-human:** `{t['id']}` — {t['title']}: awaiting Silas approval.")
    for t in rm.get("stale_claimed", []):
        items.append(
            f"**Stale claimed:** `{t['id']}` ({t['age_hours']}h): Worker may be stuck."
        )
    for todo in state.get("open_todos", []):
        items.append(
            f"**Open todo** [{todo.get('priority')}] #{todo.get('id')}: {todo.get('title')}"
        )

    stats = (
        f"**Stats:** {rm.get('ready', 0)} ready | {rm.get('waiting', 0)} waiting | "
        f"{len(rm.get('blocked', []))} blocked | {len(rm.get('needs_human', []))} needs-human | "
        f"{len(state.get('open_todos', []))} open todos"
    )

    if not items:
        return f"## ALL CLEAR\nAutonomous loop running — no blockers, no CI failures, no stale work.\n\n{stats}"

    bullets = "\n".join(f"- {i}" for i in items[:3])
    return f"## ACTION NEEDED\n\n{bullets}\n\n{stats}"


# ── Output ───────────────────────────────────────────────────────────────────

def write_report(summary: str, as_of: str, dry_run: bool) -> None:
    content = (
        "<!-- auto-generated by scripts/build_conductor_summary.py — do not edit -->\n"
        "# Conductor Report\n"
        f"_Last run: {as_of}_\n\n"
        f"{summary}\n"
    )
    if dry_run:
        print(content)
    else:
        with open(REPORT_PATH, "w") as f:
            f.write(content)
        print(f"  wrote {REPORT_PATH}", file=sys.stderr)


# ── Entry point ──────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(description="Hourly conductor health assessment")
    ap.add_argument("--dry-run", action="store_true", help="Print report; do not write file")
    args = ap.parse_args()

    github_token = os.environ.get("GITHUB_TOKEN")
    kr_token = os.environ.get("KR_API_TOKEN")
    as_of = _now().strftime("%Y-%m-%d %H:%M UTC")

    print(f"[conductor] {as_of}", file=sys.stderr)

    repos = []
    for r in REPOS:
        print(f"  checking {r['owner']}/{r['name']}...", file=sys.stderr)
        repos.append(fetch_repo(r["owner"], r["name"], github_token))

    print("  scanning roadmaps...", file=sys.stderr)
    roadmap = fetch_roadmaps()

    print("  fetching todos...", file=sys.stderr)
    todos = fetch_todos(kr_token)

    state = {
        "as_of": as_of,
        "repos": repos,
        "roadmap": roadmap,
        "open_todos": todos,
    }

    print("  assessing...", file=sys.stderr)
    summary = assess(state)

    write_report(summary, as_of, args.dry_run)


if __name__ == "__main__":
    main()
