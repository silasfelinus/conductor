#!/usr/bin/env python3
"""
select_role.py — decide the right role on arrival (conductor/t-026, extended).

Neither role is a property of which trigger fired a session; it's a property
of what the repo actually needs right now. This script is the single front
door a session runs FIRST, before following AGENTS.md's per-role steps — it
answers "what does this repo need from me today?" so a session that was
scheduled as one role but finds nothing for it does not idle or no-op: it
picks up whatever real work exists instead.

Root cause this replaces (conductor/t-026): platform triggers assign a role
BEFORE a session ever looks at live state, so a mismatched trigger schedule
produces no-ops (documented case: the Reviewer trigger fired 48+ times with
zero worker/* PRs to review). The trigger schedule itself is a platform-level
setting outside this repo — this script is the repo-side half of the fix.

Four roles, each backed by an existing piece of tooling this script composes
rather than duplicates:
  - reviewer      — run_reviewer.py's open-worker/*-branch check
  - pr-medic      — open PRs (this repo) whose CI is red AND stale (no push
                    in --pr-stale-hours despite failing) — an error nobody is
                    actively fixing, as opposed to a PR mid-iteration
  - branch-medic  — run_worker.py-adjacent: branch_janitor.py's STRANDED tier
                    (unique unmerged commits, older than --branch-stale-hours)
                    — the tier branch_janitor.py deliberately never auto-acts
                    on itself ("a human/session rescues it")
  - worker        — run_worker.py's ready-task check
  - idle          — none of the above; dream-cycle fallback applies

Decision order (first match wins) — reviewing fresh work stays highest
leverage (keeps the pipeline flowing); fixing a broken PR recovers value
already in flight before archaeology on stale branches; new work and idle
fall through last:
  1. candidate_worker_branch_count > 0        -> reviewer
  2. red_stale_pr_count > 0                   -> pr-medic
  3. stranded_branch_count > 0                -> branch-medic
  4. ready_task exists                        -> worker
  5. none of the above                        -> idle

Scope note: pr-medic/branch-medic's LOCAL checks below only cover this
repo (conductor) — the one this script's own git checkout and GITHUB_TOKEN
scope naturally reach. Other repos this session can access (e.g. kind_robots)
need the equivalent check done via the session's own GitHub MCP tools
(list_pull_requests / pull_request_read / list_branches), not this script —
see AGENTS.md's "If you're fixing PR errors" / "If you're triaging stale
branches" sections for the cross-repo instruction. Direct api.github.com
calls from an interactive sandbox session may 403 regardless of token (a
known, pre-existing egress limitation shared with ci_janitor.py and
check_pr_merged_drift.py) — this script is written to run cleanly from a
GitHub Actions job with open egress; degrade to skipping the PR-CI check
(never crash) when the API is unreachable, same as those two scripts.

This intentionally does not call OpenAI, Claude, or any other model API — same
contract as the scripts it composes. Real role-appropriate work still happens
in the actual session, following AGENTS.md's "Role assignment" section.

Usage:
  python scripts/select_role.py [--dry-run]
  python scripts/select_role.py --pr-stale-hours 6 --branch-stale-hours 24

Env:
  KR_API_TOKEN  optional; forwarded to run_worker.py's queue summary
  GITHUB_TOKEN  optional; enables the pr-medic CI-status check (skipped,
                not crashed, if absent or unreachable)
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# Allow `python scripts/select_role.py` (sys.path[0] == scripts/) as well as
# `import scripts.select_role` / `python -m scripts.select_role` (repo root on
# sys.path) — both are used, by the CLI usage above and by tests respectively.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import scripts.branch_janitor as branch_janitor
import scripts.run_reviewer as run_reviewer
import scripts.run_worker as run_worker

GITHUB_API = 'https://api.github.com'
DEFAULT_REPO = 'silasfelinus/conductor'
DEFAULT_PR_STALE_HOURS = 3.0
DEFAULT_BRANCH_STALE_HOURS = branch_janitor.DEFAULT_STALE_HOURS


def _gh_request(url: str, token: str) -> object | None:
    headers = {
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'conductor-select-role/1.0',
    }
    if token:
        headers['Authorization'] = f'Bearer {token}'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as error:
        print(f'[select-role] GitHub API unreachable ({error}); skipping pr-medic check', file=sys.stderr)
        return None


def list_open_prs(repo: str, token: str) -> list[dict]:
    data = _gh_request(f'{GITHUB_API}/repos/{repo}/pulls?state=open&per_page=100', token)
    return data if isinstance(data, list) else []


def commit_combined_state(repo: str, sha: str, token: str) -> str | None:
    data = _gh_request(f'{GITHUB_API}/repos/{repo}/commits/{sha}/status', token)
    if not isinstance(data, dict):
        return None
    return data.get('state')


def find_red_stale_prs(
    repo: str,
    token: str,
    *,
    stale_hours: float = DEFAULT_PR_STALE_HOURS,
    now: datetime | None = None,
) -> list[dict]:
    """Open PRs whose latest commit's combined CI status is failure/error AND
    hasn't been pushed to in `stale_hours` — i.e. broken and NOT currently
    being iterated on, as opposed to a PR mid-fix with fresh red CI."""
    if not token:
        return []

    now = now or datetime.now(timezone.utc)
    flagged: list[dict] = []
    for pr in list_open_prs(repo, token):
        head = pr.get('head') or {}
        sha = head.get('sha')
        updated_at = pr.get('updated_at')
        if not sha or not updated_at:
            continue

        state = commit_combined_state(repo, sha, token)
        if state not in ('failure', 'error'):
            continue

        pushed_at = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        age_hours = (now - pushed_at).total_seconds() / 3600.0
        if age_hours < stale_hours:
            continue  # still being actively iterated on, not an orphaned error

        flagged.append({
            'repo': repo,
            'number': pr.get('number'),
            'title': pr.get('title'),
            'html_url': pr.get('html_url'),
            'ci_state': state,
            'stale_hours': round(age_hours, 1),
        })

    return flagged


def find_stranded_branches(*, stale_hours: float = DEFAULT_BRANCH_STALE_HOURS) -> list[str]:
    """This repo's STRANDED tier from branch_janitor.py's own classifier —
    unique unmerged commits, old enough that nobody's actively pushing to
    them, but never auto-deleted (could be real un-PR'd work)."""
    branches = branch_janitor.list_remote_branches(branch_janitor.DEFAULT_PREFIXES)
    plan = branch_janitor.classify(
        branches,
        is_merged_fn=branch_janitor.is_merged,
        age_fn=branch_janitor.branch_age_hours,
        force_set=set(),
        stale_hours=stale_hours,
    )
    return plan[branch_janitor.STRANDED]


def select_role(
    *,
    repo: str = DEFAULT_REPO,
    github_token: str = '',
    pr_stale_hours: float = DEFAULT_PR_STALE_HOURS,
    branch_stale_hours: float = DEFAULT_BRANCH_STALE_HOURS,
) -> dict[str, object]:
    try:
        run_reviewer.refresh_remotes()
    except Exception as error:  # pragma: no cover - network-dependent
        print(f'[select-role] remote refresh warning: {error}', file=sys.stderr)

    review_branches = run_reviewer.remote_worker_branches()
    red_prs = find_red_stale_prs(repo, github_token, stale_hours=pr_stale_hours)
    stranded = find_stranded_branches(stale_hours=branch_stale_hours)
    queue = run_worker.build_queue_summary()
    ready_task = queue.get('ready_task')

    if review_branches:
        role = 'reviewer'
        reason = f'{len(review_branches)} open worker/* branch(es) awaiting review'
    elif red_prs:
        role = 'pr-medic'
        reason = f'{len(red_prs)} open PR(s) with red, stale CI nobody is actively fixing'
    elif stranded:
        role = 'branch-medic'
        reason = f'{len(stranded)} stranded branch(es) with unmerged work older than {branch_stale_hours}h'
    elif ready_task:
        role = 'worker'
        reason = f'ready task available: {ready_task.get("project")}/{ready_task.get("task_id")}'
    else:
        role = 'idle'
        reason = 'nothing to review, fix, triage, or work — dream-cycle fallback applies'

    return {
        'role': role,
        'reason': reason,
        'candidate_worker_branch_count': len(review_branches),
        'candidate_worker_branches': review_branches,
        'red_stale_pr_count': len(red_prs),
        'red_stale_prs': red_prs,
        'stranded_branch_count': len(stranded),
        'stranded_branches': stranded,
        'ready_task': ready_task,
        'projects_with_ready_tasks': queue.get('projects_with_ready_tasks', []),
        'projects_needing_human': queue.get('projects_needing_human', []),
    }


def main() -> None:
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='accepted for interface parity; this script never writes')
    parser.add_argument('--repo', default=DEFAULT_REPO, help='repo to check for red/stale PRs and stranded branches')
    parser.add_argument('--pr-stale-hours', type=float, default=DEFAULT_PR_STALE_HOURS)
    parser.add_argument('--branch-stale-hours', type=float, default=DEFAULT_BRANCH_STALE_HOURS)
    args = parser.parse_args()

    print('[select-role] model API calls are disabled by design', file=sys.stderr)
    print('[select-role] this only recommends a role; the session decides what to do with it', file=sys.stderr)

    result = select_role(
        repo=args.repo,
        github_token=os.environ.get('GITHUB_TOKEN', '').strip(),
        pr_stale_hours=args.pr_stale_hours,
        branch_stale_hours=args.branch_stale_hours,
    )
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
