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

Seven roles, each backed by an existing piece of tooling this script composes
rather than duplicates:
  - reviewer      — run_reviewer.py's open-worker/*-branch check (conductor only),
                    plus find_reviewable_claude_prs()'s check for any other open
                    conductor PR (e.g. claude/*) whose CI is fully green and that
                    has sat untouched for --pr-grace-minutes — a real reviewable
                    PR isn't only ever opened from a worker/* branch (conductor/t-083)
  - workflow-medic — find_failing_scheduled_workflows()'s check, across
                    --watched-workflows (default: seven scheduled workflows
                    picked deliberately, not "watch everything" — see
                    DEFAULT_WATCHED_WORKFLOWS's comment for which ones and
                    why, and which were left out on purpose), for
                    --workflow-fail-threshold (or a --workflow-fail-thresholds
                    per-workflow override, e.g. daily-digest.yml's lower bar)
                    or more consecutive completed runs with a non-success
                    conclusion — a scheduled workflow failing loudly on every
                    run but with nothing surfacing that beyond the raw
                    Actions log (conductor/t-102, widened in t-104)
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
leverage (keeps the pipeline flowing); a silently-failing scheduled workflow
recovers shared automation everything else depends on (conductor/t-102: the
2026-08-05 ai-art-academy/t-010 stuck-rearm incident sat failing on every
`process-task-events.yml` run for hours before a manual sweep noticed) before
a single broken PR, which in turn recovers value already in flight before
archaeology on stale branches; the audit is time-boxed (must happen roughly
weekly regardless of other queue state) so it outranks fresh ready-task
pickup once overdue, but never preempts anything already broken or
reviewable; idle falls through last:
  1. candidate_worker_branch_count > 0        -> reviewer
  2. failing_scheduled_workflow_count > 0     -> workflow-medic
  3. red_stale_pr_count > 0                   -> pr-medic
  4. stranded_branch_count > 0                -> branch-medic
  5. site_audit_overdue                       -> site-auditor
  6. ready_task exists                        -> worker
  7. none of the above                        -> idle

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

conductor/t-084: because that degradation is silent to anything reading only
the returned JSON (the warning only ever went to stderr), the output also
carries `github_api_unreachable` (bool) and `github_api_unreachable_detail`
(str | None) — true whenever GITHUB_TOKEN was missing or any api.github.com
call failed this run, so a caller can tell "checked GitHub, found nothing"
apart from "couldn't check GitHub, treated it as nothing" before trusting a
`role: worker`/`idle` recommendation as complete.

Usage:
  python scripts/select_role.py [--dry-run]
  python scripts/select_role.py --repos silasfelinus/conductor,silasfelinus/kind_robots
  python scripts/select_role.py --pr-stale-hours 6 --branch-stale-hours 24

Env:
  KR_API_TOKEN  optional; forwarded to run_worker.py's queue summary
  GITHUB_TOKEN  optional; enables the workflow-medic/pr-medic/cross-repo
                branch-medic checks (skipped, not crashed, if absent or
                unreachable)
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

# Tracks GitHub API reachability across all _gh_request() calls made during a
# single select_role() invocation. Reset at the start of select_role() and
# read at the end (conductor/t-084): the JSON output previously had no way to
# distinguish "checked GitHub, found nothing" from "couldn't reach GitHub,
# treated it as nothing" -- a caller that only captures the returned JSON
# (not stderr) could trust a `role: worker`/`idle` recommendation that was
# actually built on silently-skipped signals.
_unreachable_urls: list[str] = []


def _reset_github_reachability_tracking() -> None:
    _unreachable_urls.clear()

# The repo this script's own checkout belongs to — the one branch_janitor.py's
# local-git commands (git branch -r, git log) actually reach. Any other repo
# in DEFAULT_REPOS is checked via the GitHub API instead (see module docstring).
LOCAL_REPO = 'silasfelinus/conductor'
DEFAULT_REPOS = ('silasfelinus/conductor', 'silasfelinus/kind_robots')

DEFAULT_PR_STALE_HOURS = 3.0
# Grace period before a green, open claude/* PR is considered reviewable --
# short enough to not sit unreviewed for long, but long enough that a session
# still actively pushing to its own branch isn't immediately flagged as
# something else needs to review it (conductor/t-083).
DEFAULT_PR_GRACE_MINUTES = 5.0
DEFAULT_BRANCH_STALE_HOURS = branch_janitor.DEFAULT_STALE_HOURS
DEFAULT_PREFIXES = branch_janitor.DEFAULT_PREFIXES

# process-task-events.yml is the task queue's own cron-driven processor
# (task-events/*.yaml -> roadmap.yaml); a session's own AGENTS.md-driven work
# depends on it having actually run, but a scheduled workflow's failure
# otherwise only shows up in the Actions tab (conductor/t-102). Extensible to
# other scheduled workflows via --watched-workflows; only this one was watched
# by default at first, since it was the one that had actually caused a
# silent-failure incident so far (the 2026-08-05 ai-art-academy/t-010
# stuck-rearm).
#
# conductor/t-104 (2026-08-08) widened this deliberately after workflow-medic
# caught its first live incident for real: hourly-conductor.yml had failed
# EVERY run for 2+ days (a single stuck dream-cycle proposal whose Facet
# catalog was missing an alias row, so `apply_daily_dream_facets.py` retried
# and re-failed it forever -- see that script's `partial_new` vs
# `partial_persisting` split, added the same day, which stops a single
# already-reported stuck proposal from re-failing every run once it's known).
# That confirmed the class of risk this role exists for, so t-104 added the
# other `schedule:`-triggered workflows whose failure mode is unambiguous
# (routine hygiene/pipeline jobs that are expected to succeed almost always):
# branch-janitor.yml, ci-janitor.yml, process-color-art-events.yml,
# daily-digest.yml (lower threshold -- see DEFAULT_WORKFLOW_FAIL_THRESHOLDS,
# it only runs once/day so 3 misses in a row is 3 real digest-less days), and
# monster-recast-art-jobs.yml (has a real multi-day failure-streak history,
# not just theoretical risk).
#
# Deliberately NOT added:
#   - auto-art-generate.yml: its non-success streak is dominated by
#     `cancelled` (rapid push/schedule triggers superseding in-flight runs),
#     not `failure` -- consecutive_failing_runs() treats any non-success as
#     part of the streak, so this would page constantly on benign concurrency
#     noise, not real breakage.
#   - security-audit.yml / roadmap-audit.yml: both are pull_request-event
#     driven, and a "failure" conclusion there can legitimately mean a real
#     finding was caught (working as intended) rather than the workflow
#     itself being broken. They need a smarter alert that reads *why* a run
#     failed, not a naive consecutive-non-success counter.
#   - daily-digest-retry.yml: too new (a handful of runs total as of
#     2026-08-08) to have an established noise baseline yet -- revisit once
#     it accumulates real history.
DEFAULT_WATCHED_WORKFLOWS = (
    'process-task-events.yml',
    'hourly-conductor.yml',
    'branch-janitor.yml',
    'ci-janitor.yml',
    'process-color-art-events.yml',
    'daily-digest.yml',
    'monster-recast-art-jobs.yml',
)
DEFAULT_WORKFLOW_FAIL_THRESHOLD = 3
# Per-workflow overrides for the rare case a flat threshold is wrong for that
# workflow's own cadence. daily-digest.yml only runs ~once/day, so waiting for
# 3 consecutive misses (the global default) means 3 real digest-less days
# before anyone notices; every other watched workflow runs hourly-or-more
# often, where the global default's noise/latency trade-off already holds.
DEFAULT_WORKFLOW_FAIL_THRESHOLDS: dict[str, int] = {
    'daily-digest.yml': 2,
}

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
        _unreachable_urls.append(url)
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


# --- workflow-medic: a scheduled workflow failing run after run, unnoticed --


def workflow_runs_api(repo: str, workflow_file: str, token: str, *, per_page: int = 10) -> list[dict]:
    """Most recent runs of `workflow_file` (e.g. 'process-task-events.yml'),
    newest first -- the same order the Actions API itself returns them in."""
    encoded = urllib.parse.quote(workflow_file, safe='')
    data = _gh_request(
        f'{GITHUB_API}/repos/{repo}/actions/workflows/{encoded}/runs?per_page={per_page}',
        token,
    )
    if not isinstance(data, dict):
        return []
    runs = data.get('workflow_runs')
    return runs if isinstance(runs, list) else []


def consecutive_failing_runs(runs: list[dict]) -> int:
    """Count a non-success streak from the most recent run backward. Only
    `status: completed` runs carry a real `conclusion` -- a run still queued
    or in_progress hasn't reported a result yet, so it's skipped rather than
    breaking or extending the streak. Stops at the first completed run whose
    conclusion is 'success' (a scheduled workflow that's recovered stops
    counting as failing, even if an older run in the same page failed)."""
    count = 0
    for run in runs:
        if run.get('status') != 'completed':
            continue
        if run.get('conclusion') == 'success':
            break
        count += 1
    return count


def find_failing_scheduled_workflows(
    repo: str,
    token: str,
    *,
    workflow_files: tuple[str, ...] = DEFAULT_WATCHED_WORKFLOWS,
    fail_threshold: int = DEFAULT_WORKFLOW_FAIL_THRESHOLD,
    fail_thresholds: dict[str, int] | None = None,
) -> list[dict]:
    """Watched workflows in `repo` with >= threshold consecutive completed
    runs that didn't succeed -- a scheduled job that's been quietly failing on
    every tick, as opposed to one isolated blip (conductor/t-102). Each
    workflow uses its own entry in `fail_thresholds` if present, else the
    flat `fail_threshold` (conductor/t-104 -- cadence varies enough between
    watched workflows, e.g. hourly vs. once-daily, that one flat number is
    not always right).
    """
    if not token:
        return []

    fail_thresholds = fail_thresholds or {}
    flagged: list[dict] = []
    for workflow_file in workflow_files:
        runs = workflow_runs_api(repo, workflow_file, token)
        if not runs:
            continue

        threshold = fail_thresholds.get(workflow_file, fail_threshold)
        streak = consecutive_failing_runs(runs)
        if streak < threshold:
            continue

        latest = runs[0]
        flagged.append({
            'repo': repo,
            'workflow': workflow_file,
            'consecutive_failures': streak,
            'fail_threshold': threshold,
            'last_run_conclusion': latest.get('conclusion'),
            'last_run_status': latest.get('status'),
            'last_run_url': latest.get('html_url'),
        })

    return flagged


# --- reviewer: green, open non-worker/* PRs (e.g. claude/*) awaiting a look -


def find_reviewable_claude_prs(
    repo: str,
    token: str,
    *,
    grace_minutes: float = DEFAULT_PR_GRACE_MINUTES,
    now: datetime | None = None,
) -> list[dict]:
    """Open PRs in `repo` whose head branch is NOT `worker/*` (those are
    already covered by run_reviewer.remote_worker_branches()'s fast local-git
    check), whose latest commit's combined CI status is green, and that have
    sat untouched for at least `grace_minutes` -- long enough that its own
    author is unlikely to still be actively pushing to it.

    Fixes conductor/t-083: a fully-green, reversible, bookkeeping-only PR
    opened from a `claude/*` branch sat open on conductor for roughly an hour
    because select_role.py's reviewer signal only ever looked at `worker/*`
    branches, so a real reviewable PR from any other branch naming went
    unnoticed. This does NOT decide anything about merging -- it only
    surfaces the PR as a candidate for a session to look at, same as
    run_reviewer.py's own worker/* check."""
    if not token:
        return []

    now = now or datetime.now(timezone.utc)
    flagged: list[dict] = []
    for pr in list_open_prs(repo, token):
        head = pr.get('head') or {}
        ref = head.get('ref') or ''
        sha = head.get('sha')
        updated_at = pr.get('updated_at')
        if not sha or not updated_at or ref.startswith('worker/'):
            continue

        state = commit_combined_state(repo, sha, token)
        if state != 'success':
            continue

        pushed_at = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        age_minutes = (now - pushed_at).total_seconds() / 60.0
        if age_minutes < grace_minutes:
            continue  # still fresh -- author may still be actively pushing

        flagged.append({
            'repo': repo,
            'number': pr.get('number'),
            'title': pr.get('title'),
            'html_url': pr.get('html_url'),
            'branch': ref,
            'ci_state': state,
            'age_minutes': round(age_minutes, 1),
        })

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
    pr_grace_minutes: float = DEFAULT_PR_GRACE_MINUTES,
    watched_workflows: tuple[str, ...] = DEFAULT_WATCHED_WORKFLOWS,
    workflow_fail_threshold: int = DEFAULT_WORKFLOW_FAIL_THRESHOLD,
    workflow_fail_thresholds: dict[str, int] | None = None,
) -> dict[str, object]:
    repos = list(repos) if repos else list(DEFAULT_REPOS)
    _reset_github_reachability_tracking()

    try:
        run_reviewer.refresh_remotes()
    except Exception as error:  # pragma: no cover - network-dependent
        print(f'[select-role] remote refresh warning: {error}', file=sys.stderr)

    review_branches = run_reviewer.remote_worker_branches()
    reviewable_prs = find_reviewable_claude_prs(LOCAL_REPO, github_token, grace_minutes=pr_grace_minutes)
    failing_workflows = find_failing_scheduled_workflows(
        LOCAL_REPO,
        github_token,
        workflow_files=watched_workflows,
        fail_threshold=workflow_fail_threshold,
        fail_thresholds=workflow_fail_thresholds if workflow_fail_thresholds is not None else DEFAULT_WORKFLOW_FAIL_THRESHOLDS,
    )
    red_prs = find_red_stale_prs(repos, github_token, stale_hours=pr_stale_hours)
    stranded = find_stranded_branches(repos, github_token, stale_hours=branch_stale_hours)
    audit = site_audit_status(stale_days=audit_stale_days)
    queue = run_worker.build_queue_summary()
    ready_task = queue.get('ready_task')

    if review_branches or reviewable_prs:
        role = 'reviewer'
        parts = []
        if review_branches:
            parts.append(f'{len(review_branches)} open worker/* branch(es)')
        if reviewable_prs:
            parts.append(f'{len(reviewable_prs)} green non-worker/* PR(s)')
        reason = ' and '.join(parts) + ' awaiting review'
    elif failing_workflows:
        role = 'workflow-medic'
        # Per-workflow thresholds (conductor/t-104) mean the flagging bar isn't
        # always the same number, so describe each flagged workflow with its
        # own threshold rather than implying one flat number for all of them.
        names = ', '.join(
            sorted(
                f'{f["workflow"]} ({f["consecutive_failures"]}/{f.get("fail_threshold", workflow_fail_threshold)}+)'
                for f in failing_workflows
            )
        )
        reason = f'{len(failing_workflows)} scheduled workflow(s) failing enough runs in a row: {names}'
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

    github_token_missing = not github_token
    if github_token_missing:
        github_api_unreachable_detail = 'no GITHUB_TOKEN provided; GitHub-backed signals were never checked'
    elif _unreachable_urls:
        github_api_unreachable_detail = f'{len(_unreachable_urls)} GitHub API call(s) failed (see stderr for URLs)'
    else:
        github_api_unreachable_detail = None
    github_api_unreachable = github_token_missing or bool(_unreachable_urls)

    return {
        'role': role,
        'reason': reason,
        'repos_checked': repos,
        'candidate_worker_branch_count': len(review_branches),
        'candidate_worker_branches': review_branches,
        'candidate_reviewable_pr_count': len(reviewable_prs),
        'candidate_reviewable_prs': reviewable_prs,
        'failing_scheduled_workflow_count': len(failing_workflows),
        'failing_scheduled_workflows': failing_workflows,
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
        'github_api_unreachable': github_api_unreachable,
        'github_api_unreachable_detail': github_api_unreachable_detail,
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
    parser.add_argument('--pr-grace-minutes', type=float, default=DEFAULT_PR_GRACE_MINUTES)
    parser.add_argument(
        '--watched-workflows',
        default=','.join(DEFAULT_WATCHED_WORKFLOWS),
        help='comma-separated workflow filenames (in LOCAL_REPO) to check for a failing streak',
    )
    parser.add_argument('--workflow-fail-threshold', type=int, default=DEFAULT_WORKFLOW_FAIL_THRESHOLD)
    parser.add_argument(
        '--workflow-fail-thresholds',
        default=','.join(f'{name}:{count}' for name, count in DEFAULT_WORKFLOW_FAIL_THRESHOLDS.items()),
        help=(
            "comma-separated per-workflow overrides as 'filename:count' -- a watched "
            "workflow not listed here uses --workflow-fail-threshold instead"
        ),
    )
    args = parser.parse_args()

    print('[select-role] model API calls are disabled by design', file=sys.stderr)
    print('[select-role] this only recommends a role; the session decides what to do with it', file=sys.stderr)

    workflow_fail_thresholds: dict[str, int] = {}
    for entry in args.workflow_fail_thresholds.split(','):
        entry = entry.strip()
        if not entry:
            continue
        name, _, count = entry.partition(':')
        name = name.strip()
        if name and count.strip().lstrip('-').isdigit():
            workflow_fail_thresholds[name] = int(count.strip())

    result = select_role(
        repos=[r.strip() for r in args.repos.split(',') if r.strip()],
        github_token=os.environ.get('GITHUB_TOKEN', '').strip(),
        pr_stale_hours=args.pr_stale_hours,
        branch_stale_hours=args.branch_stale_hours,
        audit_stale_days=args.audit_stale_days,
        pr_grace_minutes=args.pr_grace_minutes,
        watched_workflows=tuple(w.strip() for w in args.watched_workflows.split(',') if w.strip()),
        workflow_fail_threshold=args.workflow_fail_threshold,
        workflow_fail_thresholds=workflow_fail_thresholds,
    )
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
