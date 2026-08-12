#!/usr/bin/env python3
"""
build_conductor_summary.py — hourly conductor health assessment.

Checks both repos (conductor + kind_robots) via GitHub API, scans local
roadmaps for blockers, fetches open todos from kind_robots, then calls
Claude to produce a brief actionable summary.

Writes CONDUCTOR-REPORT.md (or prints to stdout with --dry-run).

Daily-dream duties: the PROPOSAL is authored by the sweeping LLM agent itself
(no scripted model call — see build_dream_proposal.py --brief); this script
only FLAGS when today's proposal is missing so the next agent sweep writes it.
It does still run the record builder + art-attach pass (pure REST, no LLM):
build_dream_records.ensure_records().

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
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML not installed — run: pip install pyyaml")

sys.path.insert(0, str(Path(__file__).parent))
import build_dream_proposal  # noqa: E402 — proposal existence check only (agents author proposals)
import build_dream_records  # noqa: E402 — proposal → kind_robots records builder (Phase 2)

REPOS = [
    {"owner": "silasfelinus", "name": "conductor"},
    {"owner": "silasfelinus", "name": "kind_robots"},
]
KR_API_URL = "https://kindrobots.org/api/todos"
REPORT_PATH = "CONDUCTOR-REPORT.md"
DAILY_DREAM_STATUS_PATH = os.environ.get("DAILY_DREAM_BUILD_STATUS", "")
STALE_CLAIMED_HOURS = 4   # flag tasks stuck in "claimed" longer than this
STALE_PR_HOURS = 8        # flag worker/* PRs open longer than this without review
UTC = datetime.timezone.utc


# ── Helpers ─────────────────────────────

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


# ── Data gathering ────────────────────────────

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


def inactive_project_slugs() -> set[str]:
    """Slugs whose project-overrides.yaml status is anything but `active`.

    roadmap.yaml has no lifecycle field, so a scan that reads it directly
    resurfaces tasks from paused/retired/finished projects forever — their
    roadmaps are deliberately kept as historical records, blocked and
    needs-human entries included. This is the same bug CLAUDE.md documents for
    the session-startup sweep; the summary builder had it too, which is why
    retired `approval-portal` tasks (t-004, t-005) kept appearing under
    ACTION NEEDED months after the project was closed.
    """
    try:
        with open("project-overrides.yaml", encoding="utf-8") as handle:
            doc = yaml.safe_load(handle) or {}
    except FileNotFoundError:
        return set()
    return {
        override["slug"]
        for override in doc.get("overrides", [])
        if override.get("slug")
        and str(override.get("status", "active")).lower() != "active"
    }


def fetch_roadmaps() -> dict:
    """Scan active project roadmaps for health signals."""
    blocked, needs_human, stale_claimed = [], [], []
    ready = waiting = in_review = 0
    inactive = inactive_project_slugs()

    for path in sorted(glob.glob("projects/*/roadmap.yaml")):
        if "_template" in path:
            continue
        # The directory name is the canonical slug — it is what
        # project-overrides.yaml and sync_projects.py both key on.
        if os.path.basename(os.path.dirname(path)) in inactive:
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


# ── Art queue + image pipeline ──────────────────────────────────

def fetch_art_queue() -> dict:
    """Count pending art generation requests and images waiting to be distributed."""
    # Images sitting in projects/process/ not yet moved to their target repos
    process_dir = Path("projects/process")
    pending_images = []
    if process_dir.exists():
        for p in process_dir.rglob("*"):
            if p.is_file() and p.suffix.lower() in {".webp", ".png", ".jpg", ".jpeg"} and p.name != ".gitkeep":
                pending_images.append(p.name)

    # Active generation queue (items ready to send to the image generator right now)
    active_queue = 0
    try:
        gen_data = yaml.safe_load(Path("projects/art-generate.yaml").read_text()) or {}
        active_queue = len(gen_data.get("images", []))
    except Exception:
        pass

    # Full prompt catalog — count entries that haven't been generated yet
    pending_prompts = 0
    try:
        prompts_data = yaml.safe_load(Path("projects/art-prompts.yaml").read_text()) or {}
        for section in ("images", "inspirations", "requests"):
            entries = prompts_data.get(section) or []
            for entry in entries:
                if isinstance(entry, dict):
                    for variant in ("icon", "card", "hero"):
                        v = entry.get(variant)
                        if isinstance(v, dict) and not v.get("done"):
                            pending_prompts += 1
                    if entry.get("image_path") and not entry.get("done"):
                        pending_prompts += 1
    except Exception:
        pass

    return {
        "images_to_distribute": len(pending_images),
        "images_waiting": pending_images[:5],
        "active_gen_queue": active_queue,
        "pending_prompts": pending_prompts,
    }


def fetch_vercel_status(token: str | None) -> dict:
    """Get latest Vercel deployment state for kind_robots via GitHub Deployments API."""
    raw = _gh("repos/silasfelinus/kind_robots/deployments", token, {"per_page": "5"})
    if not isinstance(raw, list) or not raw:
        return {"state": "unknown"}
    latest = raw[0]
    dep_id = latest.get("id")
    statuses = _gh(
        f"repos/silasfelinus/kind_robots/deployments/{dep_id}/statuses", token, {"per_page": "1"}
    )
    state = "unknown"
    if isinstance(statuses, list) and statuses:
        state = statuses[0].get("state", "unknown")
    return {
        "state": state,
        "environment": latest.get("environment", "?"),
        "age_hours": round(_age_hours(latest.get("created_at", "")), 1),
    }


# ── Claude assessment ──────────────────────────────

SYSTEM = """\
You are the Conductor — the project manager for an autonomous AI coordination system called AI_Networker.
You run every hour to assess the health of two GitHub repos:
- conductor (the orchestration layer: CI, scripts, task roadmaps, agent protocols)
- kind_robots (the main app and public-facing service)

Review the state data and produce a brief, scannable report. Your job:
1. Identify real signals: CI failures, Vercel deploy failures, failed daily-dream object builds,
   blocked tasks, needs-human gates, stale PRs, open todos, images waiting to distribute,
   pending art generation queue.
2. Ignore noise: chore commits, skip-ci, bot status refreshes.
3. Decide: does anything need Silas's attention, or is the autonomous loop running smoothly?

Output format (tight markdown, no preamble):
- Open with `## ACTION NEEDED` or `## ALL CLEAR`
- If action needed: bullet the top 1–3 items. For each: what it is, why it matters, specific next step.
  Reference exact IDs (e.g. conductor/t-001, PR #42, workflow "CI").
- If all clear: one summary sentence.
- Always end with:
  `**Stats:** {ready} ready | {waiting} waiting | {blocked} blocked | {needs-human} needs-human | {todos} open todos | {images} images to distribute | {queue} in gen queue`

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
    art = state.get("art_queue", {})
    vercel = state.get("vercel", {})
    items = []

    daily_dream = state.get("daily_dream_build", {})
    if daily_dream.get("status") == "failed":
        items.append(
            "**Daily-dream creation failed** — "
            f"{daily_dream.get('message', 'the object bundle was not recorded')}. "
            "The proposal is pinned for retry; inspect the Hourly Conductor run."
        )

    for r in state.get("repos", []):
        for wf in r.get("failing_ci", []):
            items.append(f"**CI failure** in `{r['repo']}` — `{wf}`: investigate and fix.")
        for pr in r.get("stale_worker_prs", []):
            items.append(
                f"**Stale worker PR** #{pr['number']} in `{r['repo']}` "
                f"({pr['age_hours']}h old): Reviewer should assess."
            )

    if vercel.get("state") not in ("success", "unknown"):
        items.append(
            f"**Vercel deploy** `{vercel.get('environment', '?')}` is `{vercel.get('state')}` "
            f"({vercel.get('age_hours', '?')}h ago): check Vercel dashboard."
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
    if art.get("images_to_distribute", 0) > 0:
        items.append(
            f"**Images to distribute:** {art['images_to_distribute']} file(s) in projects/process/ — "
            "run `python scripts/distribute_images.py`."
        )
    if art.get("active_gen_queue", 0) > 0:
        items.append(
            f"**Art generation queue:** {art['active_gen_queue']} item(s) in projects/art-generate.yaml "
            "ready to send to the image generator."
        )
    if state.get("daily_dream_proposal_missing"):
        items.append(
            "**Daily-dream proposal missing** for today — the next agent sweep should "
            "author it (`python scripts/build_dream_proposal.py --brief`, then `--from-json`)."
        )

    stats = (
        f"**Stats:** {rm.get('ready', 0)} ready | {rm.get('waiting', 0)} waiting | "
        f"{len(rm.get('blocked', []))} blocked | {len(rm.get('needs_human', []))} needs-human | "
        f"{len(state.get('open_todos', []))} open todos | "
        f"{art.get('images_to_distribute', 0)} images to distribute | "
        f"{art.get('active_gen_queue', 0)} in gen queue"
    )
    if state.get("daily_dream_proposal_missing"):
        stats += " | ⚠ daily-dream proposal MISSING (agent sweep should author it)"

    if not items:
        return f"## ALL CLEAR\nAutonomous loop running — no blockers, no CI failures, no stale work.\n\n{stats}"

    bullets = "\n".join(f"- {i}" for i in items[:3])
    return f"## ACTION NEEDED\n\n{bullets}\n\n{stats}"


# ── Output ────────────────────────────

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


def write_daily_dream_status(outcome: dict) -> None:
    """Leave a same-job status file for the workflow's final truth check."""
    if not DAILY_DREAM_STATUS_PATH:
        return
    Path(DAILY_DREAM_STATUS_PATH).write_text(
        json.dumps(outcome, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def ensure_daily_dream_failure_is_visible(summary: str, outcome: dict) -> str:
    """Do not let the prose model omit the one signal this workflow just observed."""
    if outcome.get("status") != "failed":
        return summary
    message = str(outcome.get("message") or "the object bundle was not recorded")
    bullet = (
        "- **Daily-dream creation failed** — "
        f"{message} The proposal is pinned for retry; no completed bundle was recorded."
    )
    if "Daily-dream creation failed" in summary:
        return summary
    if summary.startswith("## ALL CLEAR"):
        rest = summary.split("\n", 1)[1] if "\n" in summary else ""
        return f"## ACTION NEEDED\n\n{bullet}\n\n{rest}".rstrip()
    if summary.startswith("## ACTION NEEDED"):
        return summary.replace("## ACTION NEEDED", f"## ACTION NEEDED\n\n{bullet}", 1)
    return f"## ACTION NEEDED\n\n{bullet}\n\n{summary}"


# ── Entry point ────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(description="Hourly conductor health assessment")
    ap.add_argument("--dry-run", action="store_true", help="Print report; do not write file")
    args = ap.parse_args()

    github_token = os.environ.get("GITHUB_TOKEN")
    kr_token = os.environ.get("KR_API_TOKEN")
    as_of = _now().strftime("%Y-%m-%d %H:%M UTC")

    print(f"[conductor] {as_of}", file=sys.stderr)

    # Build first, then report exactly what happened.  This is the daily creation
    # transaction: successful API writes, art requests, and the durable built-data
    # record land together.  A failure leaves a retry marker instead of disappearing
    # into stderr while the workflow reports green.
    print("  daily-dream records + art attach...", file=sys.stderr)
    daily_dream_build = build_dream_records.ensure_records(dry_run=args.dry_run)
    write_daily_dream_status(daily_dream_build)

    repos = []
    for r in REPOS:
        print(f"  checking {r['owner']}/{r['name']}...", file=sys.stderr)
        repos.append(fetch_repo(r["owner"], r["name"], github_token))

    print("  scanning roadmaps...", file=sys.stderr)
    roadmap = fetch_roadmaps()

    print("  fetching todos...", file=sys.stderr)
    todos = fetch_todos(kr_token)

    print("  checking art queue...", file=sys.stderr)
    art_queue = fetch_art_queue()

    print("  checking vercel status...", file=sys.stderr)
    vercel = fetch_vercel_status(kr_token)

    # Daily-dream proposal: authored by the sweeping LLM agent, not this script.
    # Surface a missing proposal as a signal so the next agent sweep writes one.
    today_pacific = build_dream_proposal._target_date()
    proposal_missing_today = not build_dream_proposal.proposal_exists_for(today_pacific)

    state = {
        "as_of": as_of,
        "repos": repos,
        "roadmap": roadmap,
        "open_todos": todos,
        "art_queue": art_queue,
        "vercel": vercel,
        "daily_dream_proposal_missing": proposal_missing_today,
        "daily_dream_build": daily_dream_build,
    }

    print("  assessing...", file=sys.stderr)
    summary = assess(state)
    summary = ensure_daily_dream_failure_is_visible(summary, daily_dream_build)

    write_report(summary, as_of, args.dry_run)



if __name__ == "__main__":
    main()
