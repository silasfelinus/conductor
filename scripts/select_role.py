#!/usr/bin/env python3
"""
select_role.py — decide the right role on arrival (conductor/t-026, extended).

Neither role is a property of which trigger fired a session; it's a property
of what the repo(s) actually need right now. This script is the single front
door a session runs FIRST, before following AGENTS.md's per-role steps — it
answers "what needs me today?" so a session that was scheduled as one role
but finds nothing for it does not idle or no-op: it picks up whatever real
work exists instead.

Root cause this replaces (conductor/t-026): platform triggers assign a role
BEFORE a session ever looks at live state, so a mismatched trigger schedule
produces no-ops (documented case: the Reviewer trigger fired 48+ times with
zero worker/* PRs to review). The trigger schedule itself is a platform-level
setting outside this repo — this script is the repo-side half of the fix.

Cross-repo (Silas, 2026-07-25/26): pr-medic and branch-medic cover BOTH
silasfelinus/conductor and silasfelinus/kind_robots — "it's a conductor
agent doing it" but the repos it watches aren't limited to its own. The
conductor repo (this script's own checkout) uses fast local git commands
(via branch_janitor.py, no API calls); kind_robots has no local checkout
guaranteed to exist in every session/job that runs this script, so it's
checked via the GitHub REST API instead (list branches, per-branch commit
date, and the compare API to determine merge state) — same information,
different transport. `worker`/`reviewer` stay conductor-only: `worker/*`
branch naming and roadmap-tracked ready tasks are conductor-repo concepts by
this system's own architecture (kind_robots work is tracked as a conductor
roadmap task that names a kind_robots PR, not as its own independent
Worker/Reviewer cycle) — see AGENTS.md's "Cross-repo tasks" section.

Six roles, each backed by an existing piece of tooling this script composes
rather than duplicates:
  - reviewer      — run_reviewer.py's open-worker/*-branch check (conductor only)
  - pr-medic      — open PRs, across every repo in --repos, whose CI is red
                    AND stale (no push in --pr-stale-hours despite failing) —
                    an error nobody is actively fixing, as opposed to a PR
                    mid-iteration
  - branch-medic  — the STRANDED tier (unique unmerged commits, older than
                    --branch-stale-hours) across every repo in --repos — for
                    conductor this is literally branch_janitor.py's own
                    classifier, which deliberately never auto-acts on this
                    tier itself ("a human/session rescues it"); for other
                    repos it's the API-driven equivalent below
  - site-auditor  — the weekly site audit (projects/global-ui/SITE-AUDIT-
                    AGENT.md) is overdue: no AUDIT-REPORT-<date>.md exists, or
                    the newest one is older than --audit-stale-days (default
                    7). Folds global-ui/t-016's originally-planned dedicated
                    Claude Code Remote Trigger into this same self-assigning
                    system instead — the audit now rides on whichever trigger
                    fires next (Worker/Reviewer-family, already far more
                    frequent than weekly) rather than needing a brand-new,
                    separately-approved platform trigger of its own.
  - worker        — run_worker.py's ready-task check (conductor only)
  - idle          — none of the above; dream-cycle fallback applies

Decision order (first match wins) — reviewing fresh work stays highest
leverage (keeps the pipeline flowing); fixing a broken PR recovers value
already in flight before archaeology on stale branches; the audit is time-
boxed (must happen roughly weekly regardless of other queue state) so it
outranks fresh ready-task pickup once overdue, but never preempts anything
already broken or reviewable; idle falls through last:
  1. candidate_worker_branch_count > 0        -> reviewer
  2. red_stale_pr_count > 0                   -> pr-medic
  3. stranded_branch_count > 0                -> branch-medic
  4. site_audit_overdue                       -> site-auditor
  5. ready_task exists                        -> worker
  6. none of the above                        -> idle

This intentionally does not call OpenAI, Claude, or any other model API — same
contract as the scripts it composes. Real role-appropriate work still happens
in the actual session, following AGENTS.md's "Role assignment" section, and
uses the session's own GitHub MCP tools to act (this script only recommends).

Direct api.github.com calls from an interactive sandbox session may 403
regardless of token (a known, pre-existing egress limitation shared with
ci_janitor.py and check_pr_merged_drift.py) — this script is written to run
cleanly from a GitHub Actions job with open egress; every network call
degrades to skipping that one check (never crashes) when the API is
unreachable, same as those two scripts.

Usage:
  python scripts/select_role.py [--dry-run]
  python scripts/select_role.py --repos silasfelinus/conductor,silasfelinus/kind_robots
  python scripts/select_role.py --pr-stale-hours 6 --branch-stale-hours 24

Env:
  KR_API_TOKEN  optional; forwarded to run_worker.py's queue summary
  GITHUB_TOKEN  optional; enables the pr-medic/cross-repo branch-medic checks
                (skipped, not crashed, if absent or unreachable)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timezone
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

# The repo this script's own checkout belongs to — the one branch_janitor.py's
# local-git commands (git branch -r, git log) actually reach. Any other repo
# in DEFAULT_REPOS is checked via the GitHub API instead (see module docstring).
LOCAL_REPO = 'silasfelinus/conductor'
DEFAULT_REPOS = ('silasfelinus/conductor', 'silasfelinus/kind_robots')

DEFAULT_PR_STALE_HOURS = 3.0
DEFAULT_BRANCH_STALE_HOURS = branch_janitor.DEFAULT_STALE_HOURS
DEFAULT_PREFIXES = branch_janitor.DEFAULT_PREFIXES

# projects/global-ui/SITE-AUDIT-AGENT.md's weekly report drop -- this repo's
# own local checkout, no API needed, same as branch_janitor.py's local checks.
AUDIT_REPORTS_DIR = _REPO_ROOT / 'projects' / 'global-ui'
AUDIT_REPORT_RE = re.compile(r'^AUDIT-REPORT-(\d{4}-\d{2}-\d{2})\.md$')
DEFAULT_AUDIT_STALE_DAYS = 7.0


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
        print(f'[select-role] GitHub API unreachable for {url} ({error}); skipping', file=sys.stderr)
        return None


# --- pr-medic: open PRs with red, stale CI (any repo) ----------------------


def list_open_prs(repo: str, token: str) -> list[dict]:
    data = _gh_request(f'{GITHUB_API}/repos/{repo}/pulls?state=open&per_page=100', token)
    return data if isinstance(data, list) else []


def commit_combined_state(repo: str, sha: str, token: str) -> str | None:
    data = _gh_request(f'{GITHUB_API}/repos/{repo}/commits/{sha}/status', token)
    if not isinstance(data, dict):
        return None
    return data.get('state')


def find_red_stale_prs_in_repo(
    repo: str,
    token: str,
    *,
    stale_hours: float = DEFAULT_PR_STALE_HOURS,
    now: datetime | None = None,
) -> list[dict]:
    """Open PRs in `repo` whose latest commit's combined CI status is
    failure/error AND hasn't been pushed to in `stale_hours` — i.e. broken and
    NOT currently being iterated on, as opposed to a PR mid-fix with fresh
    red CI."""
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


def find_red_stale_prs(
    repos: list[str],
    token: str,
    *,
    stale_hours: float = DEFAULT_PR_STALE_HOURS,
    now: datetime | None = None,
) -> list[dict]:
    """Aggregate find_red_stale_prs_in_repo() across every repo in `repos`."""
    flagged: list[dict] = []
    for repo in repos:
        flagged.extend(find_red_stale_prs_in_repo(repo, token, stale_hours=stale_hours, now=now))
    return flagged


# --- branch-medic: stranded branches, local (conductor) or API (elsewhere) -


def find_stranded_branches_local(*, stale_hours: float = DEFAULT_BRANCH_STALE_HOURS) -> list[str]:
    """LOCAL_REPO's STRANDED tier from branch_janitor.py's own classifier —
    unique unmerged commits, old enough that nobody's actively pushing to
    them, but never auto-deleted (could be real un-PR'd work). Local git
    only — fast, no API calls, no rate limit."""
    branches = branch_janitor.list_remote_branches(branch_janitor.DEFAULT_PREFIXES)
    plan = branch_janitor.classify(
        branches,
        is_merged_fn=branch_janitor.is_merged,
        age_fn=branch_janitor.branch_age_hours,
        force_set=set(),
        stale_hours=stale_hours,
    )
    return plan[branch_janitor.STRANDED]


def list_branches_api(repo: str, token: str, prefixes: tuple[str, ...]) -> list[dict]:
    data = _gh_request(f'{GITHUB_API}/repos/{repo}/branches?per_page=100', token)
    if not isinstance(data, list):
        return []
    return [b for b in data if isinstance(b, dict) and str(b.get('name', '')).startswith(prefixes)]


def branch_commit_date_api(repo: str, sha: str, token: str) -> datetime | None:
    data = _gh_request(f'{GITHUB_API}/repos/{repo}/commits/{sha}', token)
    if not isinstance(data, dict):
        return None
    date_str = (((data.get('commit') or {}).get('committer') or {}).get('date'))
    if not date_str:
        return None
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)


def is_branch_merged_api(repo: str, branch: str, token: str, *, base: str = 'main') -> bool | None:
    """True if `branch` has no commits `base` doesn't already have (merged or
    a no-op), via the compare API's `status` field. None if the comparison
    itself couldn't be determined (network failure) — treated as "don't know,
    don't flag" by the caller, never as "assume merged"."""
    encoded_branch = urllib.parse.quote(branch, safe='')
    data = _gh_request(f'{GITHUB_API}/repos/{repo}/compare/{base}...{encoded_branch}', token)
    if not isinstance(data, dict):
        return None
    status = data.get('status')
    if status in ('identical', 'behind'):
        return True
    if status in ('ahead', 'diverged'):
        return False
    return None


def find_stranded_branches_remote(
    repo: str,
    token: str,
    *,
    prefixes: tuple[str, ...] = DEFAULT_PREFIXES,
    stale_hours: float = DEFAULT_BRANCH_STALE_HOURS,
    now: datetime | None = None,
) -> list[dict]:
    """API-driven equivalent of branch_janitor.py's STRANDED tier, for a repo
    with no guaranteed local checkout (e.g. kind_robots from a conductor
    session). Same precedence as branch_janitor.classify(): merged or
    undetermined branches are never flagged; only branches confirmed to have
    unique commits AND old enough are STRANDED."""
    if not token:
        return []

    now = now or datetime.now(timezone.utc)
    stranded: list[dict] = []
    for branch in list_branches_api(repo, token, prefixes):
        name = branch.get('name')
        sha = (branch.get('commit') or {}).get('sha')
        if not name or not sha:
            continue

        merged = is_branch_merged_api(repo, name, token)
        if merged in (True, None):
            continue  # merged, or undetermined -- never flag on an unknown

        committed_at = branch_commit_date_api(repo, sha, token)
        if committed_at is None:
            continue  # can't confirm age -- don't guess

        age_hours = (now - committed_at).total_seconds() / 3600.0
        if age_hours < stale_hours:
            continue

        stranded.append({'repo': repo, 'branch': name, 'stale_hours': round(age_hours, 1)})

    return stranded


def find_stranded_branches(
    repos: list[str],
    token: str,
    *,
    stale_hours: float = DEFAULT_BRANCH_STALE_HOURS,
    now: datetime | None = None,
) -> list[dict]:
    """Aggregate stranded branches across every repo in `repos` — LOCAL_REPO
    via fast local git, everything else via the GitHub API."""
    stranded: list[dict] = []
    for repo in repos:
        if repo == LOCAL_REPO:
            stranded.extend(
                {'repo': repo, 'branch': b, 'stale_hours': None}
                for b in find_stranded_branches_local(stale_hours=stale_hours)
            )
        else:
            stranded.extend(
                find_stranded_branches_remote(repo, token, stale_hours=stale_hours, now=now)
            )
    return stranded


# --- site-auditor: is the weekly SITE-AUDIT-AGENT.md run overdue? ----------


def find_last_audit_report(reports_dir: Path = AUDIT_REPORTS_DIR) -> tuple[str, date] | None:
    """Most recent AUDIT-REPORT-<YYYY-MM-DD>.md in `reports_dir`, or None if
    the audit has never run. Purely a filename-date parse -- no git history
    walk needed, since the report's own name IS the date it ran."""
    if not reports_dir.is_dir():
        return None

    found: list[tuple[str, date]] = []
    for path in reports_dir.iterdir():
        match = AUDIT_REPORT_RE.match(path.name)
        if match:
            found.append((path.name, date.fromisoformat(match.group(1))))

    if not found:
        return None
    return max(found, key=lambda item: item[1])


def site_audit_status(
    *,
    reports_dir: Path = AUDIT_REPORTS_DIR,
    stale_days: float = DEFAULT_AUDIT_STALE_DAYS,
    today: date | None = None,
) -> dict[str, object]:
    """Never-run counts as maximally overdue (stale_days is a lower bound,
    not a grace period for a first run that's never happened)."""
    today = today or datetime.now(timezone.utc).date()
    last = find_last_audit_report(reports_dir)

    if last is None:
        return {'overdue': True, 'last_report': None, 'days_since': None}

    name, report_date = last
    days_since = (today - report_date).days
    return {'overdue': days_since >= stale_days, 'last_report': name, 'days_since': days_since}


def select_role(
    *,
    repos: list[str] | None = None,
    github_token: str = '',
    pr_stale_hours: float = DEFAULT_PR_STALE_HOURS,
    branch_stale_hours: float = DEFAULT_BRANCH_STALE_HOURS,
    audit_stale_days: float = DEFAULT_AUDIT_STALE_DAYS,
) -> dict[str, object]:
    repos = list(repos) if repos else list(DEFAULT_REPOS)

    try:
        run_reviewer.refresh_remotes()
    except Exception as error:  # pragma: no cover - network-dependent
        print(f'[select-role] remote refresh warning: {error}', file=sys.stderr)

    review_branches = run_reviewer.remote_worker_branches()
    red_prs = find_red_stale_prs(repos, github_token, stale_hours=pr_stale_hours)
    stranded = find_stranded_branches(repos, github_token, stale_hours=branch_stale_hours)
    audit = site_audit_status(stale_days=audit_stale_days)
    queue = run_worker.build_queue_summary()
    ready_task = queue.get('ready_task')

    if review_branches:
        role = 'reviewer'
        reason = f'{len(review_branches)} open worker/* branch(es) awaiting review'
    elif red_prs:
        role = 'pr-medic'
        by_repo = ', '.join(sorted({pr['repo'] for pr in red_prs}))
        reason = f'{len(red_prs)} open PR(s) with red, stale CI nobody is actively fixing ({by_repo})'
    elif stranded:
        role = 'branch-medic'
        by_repo = ', '.join(sorted({b['repo'] for b in stranded}))
        reason = f'{len(stranded)} stranded branch(es) with unmerged work older than {branch_stale_hours}h ({by_repo})'
    elif audit['overdue']:
        role = 'site-auditor'
        if audit['last_report'] is None:
            reason = 'weekly site audit has never run'
        else:
            reason = f'weekly site audit overdue ({audit["days_since"]} days since {audit["last_report"]})'
    elif ready_task:
        role = 'worker'
        reason = f'ready task available: {ready_task.get("project")}/{ready_task.get("task_id")}'
    else:
        role = 'idle'
        reason = 'nothing to review, fix, triage, audit, or work — dream-cycle fallback applies'

    return {
        'role': role,
        'reason': reason,
        'repos_checked': repos,
        'candidate_worker_branch_count': len(review_branches),
        'candidate_worker_branches': review_branches,
        'red_stale_pr_count': len(red_prs),
        'red_stale_prs': red_prs,
        'stranded_branch_count': len(stranded),
        'stranded_branches': stranded,
        'site_audit_overdue': audit['overdue'],
        'site_audit_last_report': audit['last_report'],
        'site_audit_days_since': audit['days_since'],
        'ready_task': ready_task,
        'projects_with_ready_tasks': queue.get('projects_with_ready_tasks', []),
        'projects_needing_human': queue.get('projects_needing_human', []),
    }


def main() -> None:
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='accepted for interface parity; this script never writes')
    parser.add_argument(
        '--repos',
        default=','.join(DEFAULT_REPOS),
        help='comma-separated owner/repo list to check for red/stale PRs and stranded branches',
    )
    parser.add_argument('--pr-stale-hours', type=float, default=DEFAULT_PR_STALE_HOURS)
    parser.add_argument('--branch-stale-hours', type=float, default=DEFAULT_BRANCH_STALE_HOURS)
    parser.add_argument('--audit-stale-days', type=float, default=DEFAULT_AUDIT_STALE_DAYS)
    args = parser.parse_args()

    print('[select-role] model API calls are disabled by design', file=sys.stderr)
    print('[select-role] this only recommends a role; the session decides what to do with it', file=sys.stderr)

    result = select_role(
        repos=[r.strip() for r in args.repos.split(',') if r.strip()],
        github_token=os.environ.get('GITHUB_TOKEN', '').strip(),
        pr_stale_hours=args.pr_stale_hours,
        branch_stale_hours=args.branch_stale_hours,
        audit_stale_days=args.audit_stale_days,
    )
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
