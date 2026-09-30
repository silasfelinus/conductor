#!/usr/bin/env python3
"""Flag recurring tasks that are burning agent sessions on repeated re-arms.

Why this exists (2026-09-30, token essentialization). Nothing reported how often a
task was being picked up, so two recurring loops ran for weeks unnoticed:
coloring-book/t-022 was claimed 40 times in 48h while every next step was gated on
Silas (found only in a usage investigation, then the project was paused), and
model-builder/t-029 ran 122 cycles -- about 43 in ten days -- each one a full hourly
agent session concluding "no model-builder commits, re-arming to ready".

Counts, from `origin/main` history, the `close: <project>/<task> -> status=ready`
re-arm commits (close_task.py) per task over a window, and flags any task at or over
the threshold. Unless you pass --all, a task that is currently resting (`rest_until`
in the future, i.e. the no-op backoff is already doing its job) is not flagged.

The fix for a flagged task is one of:
  * its cycles really are no-ops -> re-arm with `close_task.py ... ready --noop`
    (2h..48h backoff; see roadmap_claims.NOOP_REST_HOURS);
  * its next step is waiting on Silas -> `needs-human`, not `ready`;
  * it is a pure watcher a script could answer -> make it a script/workflow, or
    set `max_rest_hours` high.

Advisory only. Exit 0 clean, 1 when at least one task is flagged, 2 when history
could not be read far enough back to cover the window. No network/token needed
beyond `git fetch` of origin/main.

Usage:
  python scripts/check_recurring_churn.py                 # 7-day window, threshold 8
  python scripts/check_recurring_churn.py --days 3 --threshold 5
  python scripts/check_recurring_churn.py --include-inactive
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from roadmap_claims import task_is_resting  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
REARM_RE = re.compile(r"^close: (?P<project>[\w.-]+)/(?P<task>t-[\w-]+) -> status=ready\b")
CLAIM_RE = re.compile(r"^claim: (?P<project>[\w.-]+)/(?P<task>t-[\w-]+)\b")


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout


def ensure_history(since: datetime) -> bool:
    """Make sure origin/main history reaches back to `since`; deepen a shallow clone if not."""
    stamp = since.strftime("%Y-%m-%d")
    try:
        git("fetch", "-q", "origin", "main")
    except subprocess.CalledProcessError:
        pass
    try:
        shallow = git("rev-parse", "--is-shallow-repository").strip() == "true"
    except subprocess.CalledProcessError:
        return False
    if shallow:
        oldest = git("log", "--format=%cI", "--reverse", "origin/main").splitlines()[:1]
        if not oldest or datetime.fromisoformat(oldest[0]) > since:
            try:
                git("fetch", "-q", f"--shallow-since={stamp}", "origin", "main")
            except subprocess.CalledProcessError:
                return False
            oldest = git("log", "--format=%cI", "--reverse", "origin/main").splitlines()[:1]
            return bool(oldest) and datetime.fromisoformat(oldest[0]) <= since + timedelta(days=1)
    return True


def active_slugs(include_inactive: bool) -> set[str] | None:
    if include_inactive:
        return None
    data = yaml.safe_load((ROOT / "project-overrides.yaml").read_text()) or {}
    return {
        entry.get("slug")
        for entry in data.get("overrides", [])
        if isinstance(entry, dict) and entry.get("status", "active") == "active"
    }


def load_task(project: str, task_id: str) -> dict | None:
    path = ROOT / "projects" / project / "roadmap.yaml"
    if not path.is_file():
        return None
    doc = yaml.safe_load(path.read_text()) or {}
    for task in doc.get("tasks") or []:
        if isinstance(task, dict) and str(task.get("id")) == task_id:
            return task
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=float, default=7.0)
    ap.add_argument("--threshold", type=int, default=8, help="re-arms in the window that count as churn")
    ap.add_argument("--include-inactive", action="store_true")
    ap.add_argument("--all", action="store_true", help="also list tasks already resting under the backoff")
    args = ap.parse_args()

    now = datetime.now(timezone.utc)
    since = now - timedelta(days=args.days)
    if not ensure_history(since):
        print(f"Recurring churn: UNRESOLVED -- origin/main history does not reach back {args.days:g} days.")
        return 2

    log = git("log", f"--since={since.isoformat()}", "--format=%s", "origin/main")
    rearms: Counter[tuple[str, str]] = Counter()
    claims: Counter[tuple[str, str]] = Counter()
    for subject in log.splitlines():
        if m := REARM_RE.match(subject):
            rearms[(m["project"], m["task"])] += 1
        elif m := CLAIM_RE.match(subject):
            claims[(m["project"], m["task"])] += 1

    allowed = active_slugs(args.include_inactive)
    flagged = []
    for (project, task_id), count in rearms.most_common():
        if count < args.threshold:
            break
        if allowed is not None and project not in allowed:
            continue
        task = load_task(project, task_id) or {}
        resting = task_is_resting(task, now=now)
        if resting and not args.all:
            continue
        flagged.append((project, task_id, count, claims[(project, task_id)], task, resting))

    if not flagged:
        print(
            f"No recurring churn -- no active task re-armed to ready {args.threshold}+ times "
            f"in the last {args.days:g} days without the no-op backoff."
        )
        return 0

    print(
        f"Recurring churn: {len(flagged)} task(s) re-armed to ready {args.threshold}+ times in "
        f"{args.days:g} days (each re-arm is roughly one full agent session):"
    )
    for project, task_id, count, n_claims, task, resting in flagged:
        state = f"resting until {task.get('rest_until')}" if resting else f"status={task.get('status')}"
        streak = task.get("noop_streak")
        extra = f", noop_streak={streak}" if streak else ""
        print(f"  {project}/{task_id}: {count} re-arms, {n_claims} claims ({state}{extra}) -- {str(task.get('title', ''))[:80]}")
    print(
        "Fix: re-arm no-op cycles with `close_task.py <p> <t> ready --noop`; move a task waiting on "
        "Silas to needs-human; turn a pure watcher into a script. See docs/sweep-checks.md."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
