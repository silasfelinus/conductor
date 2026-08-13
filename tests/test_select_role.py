"""Tests for scripts/select_role.py (conductor/t-026, extended, cross-repo,
+ weekly site audit, + green non-worker/* PR reviewer check).

select_role.py composes six signals (open worker/* branches, green non-
worker/* PRs past a grace period, red+stale open PRs, stranded branches, an
overdue weekly site audit, ready tasks) into one role recommendation, in
priority order, so a session decides its own role on arrival instead of
following a trigger label that may not match what the repos actually need.

The reviewer signal isn't only ever a worker/* branch (conductor/t-083): a
fully-green, reversible PR opened from a claude/* branch is just as
reviewable, so find_reviewable_claude_prs() flags it once its CI is green
and it's sat untouched past --pr-grace-minutes.

pr-medic and branch-medic cover BOTH silasfelinus/conductor (via fast local
git, through branch_janitor.py) and silasfelinus/kind_robots (via the GitHub
API, since a session running this script has no guaranteed local kind_robots
checkout) — "it's a conductor agent doing it" doesn't mean it only watches
its own repo.

site-auditor folds projects/global-ui/SITE-AUDIT-AGENT.md's weekly audit into
this same self-assigning system instead of needing its own dedicated,
separately-approved Claude Code Remote Trigger (global-ui/t-016) — it rides
whichever trigger fires next, as long as this script runs first.
"""

import contextlib
import py_compile
import urllib.error
from datetime import date, datetime, timezone
from pathlib import Path
from unittest import mock

import scripts.select_role as select_role


ROOT = Path(__file__).resolve().parents[1]
SELECT_ROLE = ROOT / "scripts" / "select_role.py"

EMPTY_QUEUE = {"ready_task": None, "projects_with_ready_tasks": [], "projects_needing_human": []}
SOME_READY_TASK = {
    "ready_task": {"project": "some-project", "task_id": "t-002", "title": "x"},
    "projects_with_ready_tasks": ["some-project"],
    "projects_needing_human": [],
}
AUDIT_NOT_OVERDUE = {"overdue": False, "last_report": "AUDIT-REPORT-2026-07-24.md", "days_since": 1}
AUDIT_OVERDUE = {"overdue": True, "last_report": "AUDIT-REPORT-2026-07-01.md", "days_since": 25}
AUDIT_NEVER_RUN = {"overdue": True, "last_report": None, "days_since": None}


def _patched(
    remote_worker_branches=(),
    reviewable_claude_prs=(),
    failing_scheduled_workflows=(),
    red_stale_prs=(),
    stranded_branches=(),
    audit_status=None,
    queue_summary=None,
):
    """One combined patch context covering all seven signals, each defaulted
    to "nothing found"/"not overdue" and overridden per-test — keeps each
    test asserting only the signal(s) it's actually about."""
    return (
        mock.patch.object(select_role.run_reviewer, "refresh_remotes"),
        mock.patch.object(
            select_role.run_reviewer, "remote_worker_branches", return_value=list(remote_worker_branches)
        ),
        mock.patch.object(
            select_role, "find_reviewable_claude_prs", return_value=list(reviewable_claude_prs)
        ),
        mock.patch.object(
            select_role, "find_failing_scheduled_workflows", return_value=list(failing_scheduled_workflows)
        ),
        mock.patch.object(select_role, "find_red_stale_prs", return_value=list(red_stale_prs)),
        mock.patch.object(select_role, "find_stranded_branches", return_value=list(stranded_branches)),
        mock.patch.object(select_role, "site_audit_status", return_value=audit_status or AUDIT_NOT_OVERDUE),
        mock.patch.object(
            select_role.run_worker, "build_queue_summary", return_value=queue_summary or EMPTY_QUEUE
        ),
    )


@contextlib.contextmanager
def _apply(patches):
    with contextlib.ExitStack() as stack:
        for patch in patches:
            stack.enter_context(patch)
        yield


def test_script_compiles():
    py_compile.compile(str(SELECT_ROLE), doraise=True)


def test_default_repos_include_kind_robots():
    """The whole point of the 2026-07-26 extension: pr-medic/branch-medic
    aren't conductor-only by default."""
    assert "silasfelinus/conductor" in select_role.DEFAULT_REPOS
    assert "silasfelinus/kind_robots" in select_role.DEFAULT_REPOS


def test_reviewer_outranks_everything():
    with _apply(_patched(
        remote_worker_branches=[{"branch": "worker/x-t-001"}],
        failing_scheduled_workflows=[{"repo": "silasfelinus/conductor", "workflow": "process-task-events.yml"}],
        red_stale_prs=[{"repo": "silasfelinus/conductor", "number": 1}],
        stranded_branches=[{"repo": "silasfelinus/kind_robots", "branch": "claude/some-stale"}],
        audit_status=AUDIT_OVERDUE,
        queue_summary=SOME_READY_TASK,
    )):
        result = select_role.select_role()

    assert result["role"] == "reviewer"
    assert result["candidate_worker_branch_count"] == 1
    # Other signals still surfaced even though they didn't win the role, so a
    # session that clears the reviewer queue doesn't have to re-scan from
    # scratch for what's next.
    assert result["failing_scheduled_workflow_count"] == 1
    assert result["red_stale_pr_count"] == 1
    assert result["stranded_branch_count"] == 1
    assert result["site_audit_overdue"] is True
    assert result["ready_task"]["task_id"] == "t-002"


def test_reviewer_triggered_by_green_reviewable_pr_alone():
    """No worker/* branch at all -- a lone green, grace-period-cleared
    claude/* PR must still win the reviewer role (conductor/t-083)."""
    with _apply(_patched(
        reviewable_claude_prs=[{"repo": "silasfelinus/conductor", "number": 5, "branch": "claude/x"}],
        queue_summary=SOME_READY_TASK,
    )):
        result = select_role.select_role()

    assert result["role"] == "reviewer"
    assert result["candidate_reviewable_pr_count"] == 1
    assert "green non-worker/* PR" in result["reason"]


def test_reviewer_reason_mentions_both_signals_when_both_present():
    with _apply(_patched(
        remote_worker_branches=[{"branch": "worker/x-t-001"}],
        reviewable_claude_prs=[{"repo": "silasfelinus/conductor", "number": 5, "branch": "claude/x"}],
    )):
        result = select_role.select_role()

    assert result["role"] == "reviewer"
    assert "open worker/* branch" in result["reason"]
    assert "green non-worker/* PR" in result["reason"]


def test_workflow_medic_outranks_pr_medic_branch_medic_audit_and_worker():
    with _apply(_patched(
        failing_scheduled_workflows=[
            {"repo": "silasfelinus/conductor", "workflow": "process-task-events.yml", "consecutive_failures": 4}
        ],
        red_stale_prs=[{"repo": "silasfelinus/kind_robots", "number": 42, "ci_state": "failure"}],
        stranded_branches=[{"repo": "silasfelinus/conductor", "branch": "claude/some-stale"}],
        audit_status=AUDIT_OVERDUE,
        queue_summary=SOME_READY_TASK,
    )):
        result = select_role.select_role()

    assert result["role"] == "workflow-medic"
    assert "process-task-events.yml" in result["reason"]
    # Other signals still surfaced even though they didn't win the role.
    assert result["red_stale_pr_count"] == 1
    assert result["stranded_branch_count"] == 1


def test_pr_medic_outranks_branch_medic_audit_and_worker():
    with _apply(_patched(
        red_stale_prs=[{"repo": "silasfelinus/kind_robots", "number": 42, "ci_state": "failure"}],
        stranded_branches=[{"repo": "silasfelinus/conductor", "branch": "claude/some-stale"}],
        audit_status=AUDIT_OVERDUE,
        queue_summary=SOME_READY_TASK,
    )):
        result = select_role.select_role()

    assert result["role"] == "pr-medic"
    assert "1 open PR" in result["reason"]
    assert "silasfelinus/kind_robots" in result["reason"]


def test_branch_medic_outranks_audit_and_worker():
    with _apply(_patched(
        stranded_branches=[{"repo": "silasfelinus/kind_robots", "branch": "claude/orphaned-work"}],
        audit_status=AUDIT_OVERDUE,
        queue_summary=SOME_READY_TASK,
    )):
        result = select_role.select_role()

    assert result["role"] == "branch-medic"
    assert result["stranded_branches"][0]["branch"] == "claude/orphaned-work"
    assert "silasfelinus/kind_robots" in result["reason"]


def test_site_auditor_outranks_worker_when_overdue():
    with _apply(_patched(audit_status=AUDIT_OVERDUE, queue_summary=SOME_READY_TASK)):
        result = select_role.select_role()

    assert result["role"] == "site-auditor"
    assert "25 days" in result["reason"]
    assert "AUDIT-REPORT-2026-07-01.md" in result["reason"]
    # Ready task still surfaced even though it didn't win.
    assert result["ready_task"]["task_id"] == "t-002"


def test_site_auditor_reason_when_audit_has_never_run():
    with _apply(_patched(audit_status=AUDIT_NEVER_RUN)):
        result = select_role.select_role()

    assert result["role"] == "site-auditor"
    assert "never run" in result["reason"]
    assert result["site_audit_last_report"] is None


def test_worker_when_only_ready_task_exists_and_audit_not_due():
    # github_token set + no failures -> github_api_unreachable is False, so
    # the conductor/t-115 downgrade below never applies and this exercises
    # plain decision-order logic only.
    with _apply(_patched(queue_summary=SOME_READY_TASK)):
        result = select_role.select_role(github_token="fake-token")

    assert result["role"] == "worker"
    assert "some-project/t-002" in result["reason"]


def test_idle_when_nothing_needs_doing():
    with _apply(_patched()):
        result = select_role.select_role(github_token="fake-token")

    assert result["role"] == "idle"


def test_remote_refresh_failure_does_not_crash_selection():
    with mock.patch.object(
        select_role.run_reviewer, "refresh_remotes", side_effect=RuntimeError("network down")
    ), mock.patch.object(
        select_role.run_reviewer, "remote_worker_branches", return_value=[]
    ), mock.patch.object(
        select_role, "find_reviewable_claude_prs", return_value=[]
    ), mock.patch.object(
        select_role, "find_failing_scheduled_workflows", return_value=[]
    ), mock.patch.object(
        select_role, "find_red_stale_prs", return_value=[]
    ), mock.patch.object(
        select_role, "find_stranded_branches", return_value=[]
    ), mock.patch.object(
        select_role, "site_audit_status", return_value=AUDIT_NOT_OVERDUE
    ), mock.patch.object(
        select_role.run_worker, "build_queue_summary", return_value=EMPTY_QUEUE
    ):
        result = select_role.select_role(github_token="fake-token")

    assert result["role"] == "idle"


def test_select_role_checks_both_default_repos():
    """select_role() should pass DEFAULT_REPOS through to both aggregators
    when the caller doesn't override `repos=`."""
    with mock.patch.object(select_role.run_reviewer, "refresh_remotes"), mock.patch.object(
        select_role.run_reviewer, "remote_worker_branches", return_value=[]
    ), mock.patch.object(
        select_role, "find_reviewable_claude_prs", return_value=[]
    ), mock.patch.object(
        select_role, "find_failing_scheduled_workflows", return_value=[]
    ), mock.patch.object(
        select_role, "find_red_stale_prs", return_value=[]
    ) as find_red, mock.patch.object(
        select_role, "find_stranded_branches", return_value=[]
    ) as find_stranded, mock.patch.object(
        select_role, "site_audit_status", return_value=AUDIT_NOT_OVERDUE
    ), mock.patch.object(
        select_role.run_worker, "build_queue_summary", return_value=EMPTY_QUEUE
    ):
        select_role.select_role()

    assert find_red.call_args.args[0] == list(select_role.DEFAULT_REPOS)
    assert find_stranded.call_args.args[0] == list(select_role.DEFAULT_REPOS)


# --- github_api_unreachable: conductor/t-084 --------------------------------


def test_github_api_unreachable_when_token_missing():
    """No GITHUB_TOKEN -> every GitHub-backed signal short-circuits to empty
    without ever attempting a call. That's still "never actually checked",
    not "checked and found nothing", so the flag must be set."""
    with _apply(_patched()):
        result = select_role.select_role(github_token='')

    assert result["github_api_unreachable"] is True
    assert "no GITHUB_TOKEN" in result["github_api_unreachable_detail"]


def test_github_api_reachable_and_flag_false_when_token_present_and_no_failures():
    with _apply(_patched()):
        result = select_role.select_role(github_token='fake-token')

    assert result["github_api_unreachable"] is False
    assert result["github_api_unreachable_detail"] is None


def test_github_api_unreachable_surfaced_when_real_requests_fail():
    """A 403/network failure against api.github.com must flip the flag even
    though every affected signal still degrades cleanly to an empty list
    (conductor/t-084's whole point: that emptiness alone is indistinguishable
    from a genuine zero-signal result unless this flag is checked). Per
    conductor/t-115, the resulting role is also downgraded from the bare
    "idle" it would otherwise be to "reviewer-uncertain" — see the dedicated
    tests below."""
    with mock.patch.object(select_role.run_reviewer, "refresh_remotes"), mock.patch.object(
        select_role.run_reviewer, "remote_worker_branches", return_value=[]
    ), mock.patch.object(
        select_role.branch_janitor, "list_remote_branches", return_value=[]
    ), mock.patch.object(
        select_role, "site_audit_status", return_value=AUDIT_NOT_OVERDUE
    ), mock.patch.object(
        select_role.run_worker, "build_queue_summary", return_value=EMPTY_QUEUE
    ), mock.patch(
        "urllib.request.urlopen",
        side_effect=urllib.error.HTTPError("url", 403, "Forbidden", {}, None),
    ):
        result = select_role.select_role(github_token='fake-token')

    assert result["role"] == "reviewer-uncertain"
    assert result["underlying_role"] == "idle"
    assert result["candidate_reviewable_pr_count"] == 0
    assert result["github_api_unreachable"] is True


# --- reviewer-uncertain downgrade: conductor/t-115 --------------------------


def test_worker_downgrades_to_reviewer_uncertain_when_api_unreachable():
    """The exact miss this task documents (root TALKBACK.md, 2026-08-13 ~05:15
    UTC): a ready task exists, but github_api_unreachable is true, so the
    reviewer/pr-medic/etc. checks it beat never got real signal. `worker`
    alone would silently hide that from a caller reading only `role`."""
    with _apply(_patched(queue_summary=SOME_READY_TASK)):
        result = select_role.select_role(github_token='')  # no token -> unreachable

    assert result["role"] == "reviewer-uncertain"
    assert result["underlying_role"] == "worker"
    assert "some-project/t-002" in result["underlying_reason"]
    assert "GitHub API was unreachable" in result["reason"]
    assert "worker" in result["reason"]


def test_idle_downgrades_to_reviewer_uncertain_when_api_unreachable():
    with _apply(_patched()):
        result = select_role.select_role(github_token='')

    assert result["role"] == "reviewer-uncertain"
    assert result["underlying_role"] == "idle"


def test_worker_not_downgraded_when_api_reachable():
    """The downgrade is conditional on github_api_unreachable, not automatic
    for worker/idle — a fully-reachable API with genuinely nothing to review
    must still recommend a bare `worker`."""
    with _apply(_patched(queue_summary=SOME_READY_TASK)):
        result = select_role.select_role(github_token='fake-token')

    assert result["role"] == "worker"
    assert result["underlying_role"] == "worker"


def test_reviewer_role_not_downgraded_even_when_api_unreachable():
    """Roles that already required a real GitHub-backed finding to win
    (reviewer, workflow-medic, pr-medic, branch-medic, site-auditor) are
    trustworthy regardless of github_api_unreachable — only worker/idle ever
    get downgraded."""
    with _apply(_patched(remote_worker_branches=["worker/some-task"])):
        result = select_role.select_role(github_token='')

    assert result["role"] == "reviewer"
    assert result["underlying_role"] == "reviewer"
    assert result["github_api_unreachable"] is True


def test_gh_request_records_failure_for_reachability_tracking():
    select_role._reset_github_reachability_tracking()
    with mock.patch(
        "urllib.request.urlopen",
        side_effect=urllib.error.HTTPError("url", 403, "Forbidden", {}, None),
    ):
        result = select_role._gh_request("https://api.github.com/repos/x/y/pulls", "token")

    assert result is None
    assert select_role._unreachable_urls == ["https://api.github.com/repos/x/y/pulls"]
    select_role._reset_github_reachability_tracking()  # leave tracker clean for other tests


def test_select_role_resets_tracker_between_calls():
    """A stale failure from a prior call must never leak into a later,
    fully-successful call's result."""
    select_role._unreachable_urls.append("https://stale-from-a-previous-run")
    with _apply(_patched()):
        result = select_role.select_role(github_token='fake-token')

    assert result["github_api_unreachable"] is False


# --- find_red_stale_prs: aggregates across repos ---------------------------


def _fake_gh_request(routes):
    """routes: {url_substring: parsed_json}. Falls back to None (simulating
    an unreachable/errored call) for anything unmatched."""

    def _request(url, token):
        for substring, value in routes.items():
            if substring in url:
                return value
        return None

    return _request


def test_find_red_stale_prs_flags_failing_and_old_enough():
    now = datetime(2026, 7, 26, 12, 0, 0, tzinfo=timezone.utc)
    pr = {
        "number": 7,
        "title": "broken thing",
        "html_url": "https://github.com/x/y/pull/7",
        "head": {"sha": "deadbeef"},
        "updated_at": "2026-07-26T05:00:00Z",  # 7 hours old
    }
    routes = {
        "/pulls?state=open": [pr],
        "/commits/deadbeef/status": {"state": "failure"},
    }
    with mock.patch.object(select_role, "_gh_request", side_effect=_fake_gh_request(routes)):
        flagged = select_role.find_red_stale_prs_in_repo(
            "silasfelinus/conductor", "fake-token", stale_hours=3.0, now=now
        )

    assert len(flagged) == 1
    assert flagged[0]["number"] == 7
    assert flagged[0]["ci_state"] == "failure"


def test_find_red_stale_prs_ignores_fresh_failures_still_being_iterated():
    now = datetime(2026, 7, 26, 12, 0, 0, tzinfo=timezone.utc)
    pr = {"number": 8, "head": {"sha": "cafef00d"}, "updated_at": "2026-07-26T11:00:00Z"}  # 1 hour old
    routes = {
        "/pulls?state=open": [pr],
        "/commits/cafef00d/status": {"state": "failure"},
    }
    with mock.patch.object(select_role, "_gh_request", side_effect=_fake_gh_request(routes)):
        flagged = select_role.find_red_stale_prs_in_repo(
            "silasfelinus/conductor", "fake-token", stale_hours=3.0, now=now
        )

    assert flagged == []  # red, but still actively being iterated on


def test_find_red_stale_prs_ignores_passing_ci():
    now = datetime(2026, 7, 26, 12, 0, 0, tzinfo=timezone.utc)
    pr = {"number": 9, "head": {"sha": "abc123"}, "updated_at": "2026-07-26T05:00:00Z"}
    routes = {
        "/pulls?state=open": [pr],
        "/commits/abc123/status": {"state": "success"},
    }
    with mock.patch.object(select_role, "_gh_request", side_effect=_fake_gh_request(routes)):
        flagged = select_role.find_red_stale_prs_in_repo(
            "silasfelinus/conductor", "fake-token", stale_hours=3.0, now=now
        )

    assert flagged == []


def test_find_red_stale_prs_returns_empty_without_a_token():
    """No GITHUB_TOKEN -> skip cleanly, never attempt an unauthenticated call."""
    with mock.patch.object(select_role, "list_open_prs") as list_open_prs:
        flagged = select_role.find_red_stale_prs_in_repo("silasfelinus/conductor", "", stale_hours=3.0)

    list_open_prs.assert_not_called()
    assert flagged == []


def test_find_red_stale_prs_aggregates_across_repos():
    now = datetime(2026, 7, 26, 12, 0, 0, tzinfo=timezone.utc)
    conductor_pr = {"number": 1, "head": {"sha": "aaa"}, "updated_at": "2026-07-26T05:00:00Z"}
    kr_pr = {"number": 2, "head": {"sha": "bbb"}, "updated_at": "2026-07-26T05:00:00Z"}

    def fake_in_repo(repo, token, *, stale_hours, now=None):
        return [{"repo": repo, "number": (conductor_pr if repo.endswith("conductor") else kr_pr)["number"]}]

    with mock.patch.object(select_role, "find_red_stale_prs_in_repo", side_effect=fake_in_repo):
        flagged = select_role.find_red_stale_prs(
            ["silasfelinus/conductor", "silasfelinus/kind_robots"], "fake-token", stale_hours=3.0, now=now
        )

    assert {f["repo"] for f in flagged} == {"silasfelinus/conductor", "silasfelinus/kind_robots"}
    assert len(flagged) == 2


# --- find_failing_scheduled_workflows: a scheduled workflow failing run after run --


def test_consecutive_failing_runs_counts_from_newest_until_a_success():
    runs = [
        {"status": "completed", "conclusion": "failure"},
        {"status": "completed", "conclusion": "failure"},
        {"status": "completed", "conclusion": "failure"},
        {"status": "completed", "conclusion": "success"},  # streak stops here
        {"status": "completed", "conclusion": "failure"},
    ]
    assert select_role.consecutive_failing_runs(runs) == 3


def test_consecutive_failing_runs_skips_in_progress_runs_without_breaking_streak():
    runs = [
        {"status": "in_progress", "conclusion": None},
        {"status": "completed", "conclusion": "failure"},
        {"status": "queued", "conclusion": None},
        {"status": "completed", "conclusion": "failure"},
    ]
    assert select_role.consecutive_failing_runs(runs) == 2


def test_consecutive_failing_runs_zero_when_latest_completed_run_succeeded():
    runs = [{"status": "completed", "conclusion": "success"}]
    assert select_role.consecutive_failing_runs(runs) == 0


def test_consecutive_failing_runs_empty_list():
    assert select_role.consecutive_failing_runs([]) == 0


def test_find_failing_scheduled_workflows_flags_at_or_above_threshold():
    routes = {
        "/actions/workflows/process-task-events.yml/runs": {
            "workflow_runs": [
                {"status": "completed", "conclusion": "failure", "html_url": "https://x/run/3"},
                {"status": "completed", "conclusion": "failure"},
                {"status": "completed", "conclusion": "failure"},
                {"status": "completed", "conclusion": "success"},
            ]
        },
    }
    with mock.patch.object(select_role, "_gh_request", side_effect=_fake_gh_request(routes)):
        flagged = select_role.find_failing_scheduled_workflows(
            "silasfelinus/conductor", "fake-token", fail_threshold=3
        )

    assert len(flagged) == 1
    assert flagged[0]["workflow"] == "process-task-events.yml"
    assert flagged[0]["consecutive_failures"] == 3
    assert flagged[0]["last_run_url"] == "https://x/run/3"


def test_find_failing_scheduled_workflows_ignores_streak_below_threshold():
    routes = {
        "/actions/workflows/process-task-events.yml/runs": {
            "workflow_runs": [
                {"status": "completed", "conclusion": "failure"},
                {"status": "completed", "conclusion": "success"},
            ]
        },
    }
    with mock.patch.object(select_role, "_gh_request", side_effect=_fake_gh_request(routes)):
        flagged = select_role.find_failing_scheduled_workflows(
            "silasfelinus/conductor", "fake-token", fail_threshold=3
        )

    assert flagged == []


def test_find_failing_scheduled_workflows_checks_every_watched_workflow():
    routes = {
        "/actions/workflows/process-task-events.yml/runs": {
            "workflow_runs": [{"status": "completed", "conclusion": "failure"}] * 3
        },
        "/actions/workflows/other.yml/runs": {
            "workflow_runs": [{"status": "completed", "conclusion": "success"}]
        },
    }
    with mock.patch.object(select_role, "_gh_request", side_effect=_fake_gh_request(routes)):
        flagged = select_role.find_failing_scheduled_workflows(
            "silasfelinus/conductor",
            "fake-token",
            workflow_files=("process-task-events.yml", "other.yml"),
            fail_threshold=3,
        )

    assert {f["workflow"] for f in flagged} == {"process-task-events.yml"}


def test_find_failing_scheduled_workflows_returns_empty_without_a_token():
    with mock.patch.object(select_role, "workflow_runs_api") as workflow_runs_api:
        flagged = select_role.find_failing_scheduled_workflows("silasfelinus/conductor", "")

    workflow_runs_api.assert_not_called()
    assert flagged == []


def test_find_failing_scheduled_workflows_applies_per_workflow_threshold_override():
    # conductor/t-104: daily-digest.yml gets a lower bar than the flat
    # default since it only runs ~once/day -- 2 misses in a row should flag
    # it even though the flat default (3) would not yet.
    routes = {
        "/actions/workflows/daily-digest.yml/runs": {
            "workflow_runs": [
                {"status": "completed", "conclusion": "failure"},
                {"status": "completed", "conclusion": "failure"},
                {"status": "completed", "conclusion": "success"},
            ]
        },
        "/actions/workflows/hourly-conductor.yml/runs": {
            "workflow_runs": [
                {"status": "completed", "conclusion": "failure"},
                {"status": "completed", "conclusion": "failure"},
                {"status": "completed", "conclusion": "success"},
            ]
        },
    }
    with mock.patch.object(select_role, "_gh_request", side_effect=_fake_gh_request(routes)):
        flagged = select_role.find_failing_scheduled_workflows(
            "silasfelinus/conductor",
            "fake-token",
            workflow_files=("daily-digest.yml", "hourly-conductor.yml"),
            fail_threshold=3,
            fail_thresholds={"daily-digest.yml": 2},
        )

    assert {f["workflow"] for f in flagged} == {"daily-digest.yml"}
    assert flagged[0]["fail_threshold"] == 2
    assert flagged[0]["consecutive_failures"] == 2


def test_default_watched_workflows_excludes_noisy_or_ambiguous_workflows():
    # These are deliberately left out (see DEFAULT_WATCHED_WORKFLOWS's own
    # comment) -- guard against silently re-adding them without the same
    # care that excluded them.
    assert "auto-art-generate.yml" not in select_role.DEFAULT_WATCHED_WORKFLOWS
    assert "security-audit.yml" not in select_role.DEFAULT_WATCHED_WORKFLOWS
    assert "roadmap-audit.yml" not in select_role.DEFAULT_WATCHED_WORKFLOWS
    assert "daily-digest-retry.yml" not in select_role.DEFAULT_WATCHED_WORKFLOWS
    # And the ones added deliberately are actually present.
    for name in (
        "process-task-events.yml",
        "hourly-conductor.yml",
        "branch-janitor.yml",
        "ci-janitor.yml",
        "process-color-art-events.yml",
        "daily-digest.yml",
        "monster-recast-art-jobs.yml",
    ):
        assert name in select_role.DEFAULT_WATCHED_WORKFLOWS
    assert select_role.DEFAULT_WORKFLOW_FAIL_THRESHOLDS == {"daily-digest.yml": 2}


def test_workflow_runs_api_returns_empty_on_unexpected_shape():
    with mock.patch.object(select_role, "_gh_request", return_value=None):
        assert select_role.workflow_runs_api("silasfelinus/conductor", "process-task-events.yml", "tok") == []


# --- find_reviewable_claude_prs: green, open, non-worker/* PRs (conductor/t-083) --


def test_find_reviewable_claude_prs_flags_green_pr_past_grace_period():
    now = datetime(2026, 7, 26, 12, 0, 0, tzinfo=timezone.utc)
    pr = {
        "number": 5,
        "title": "bookkeeping-only fix",
        "html_url": "https://github.com/x/y/pull/5",
        "head": {"sha": "feedface", "ref": "claude/loving-wright-wnugs2"},
        "updated_at": "2026-07-26T11:30:00Z",  # 30 minutes old
    }
    routes = {
        "/pulls?state=open": [pr],
        "/commits/feedface/status": {"state": "success"},
    }
    with mock.patch.object(select_role, "_gh_request", side_effect=_fake_gh_request(routes)):
        flagged = select_role.find_reviewable_claude_prs(
            "silasfelinus/conductor", "fake-token", grace_minutes=5.0, now=now
        )

    assert len(flagged) == 1
    assert flagged[0]["number"] == 5
    assert flagged[0]["branch"] == "claude/loving-wright-wnugs2"
    assert flagged[0]["ci_state"] == "success"


def test_find_reviewable_claude_prs_ignores_worker_branches():
    """worker/* branches are already covered by run_reviewer.remote_worker_branches()'s
    fast local-git check -- this function must not double-count them."""
    now = datetime(2026, 7, 26, 12, 0, 0, tzinfo=timezone.utc)
    pr = {
        "number": 6,
        "head": {"sha": "abc111", "ref": "worker/some-project-t-001"},
        "updated_at": "2026-07-26T11:00:00Z",
    }
    routes = {
        "/pulls?state=open": [pr],
        "/commits/abc111/status": {"state": "success"},
    }
    with mock.patch.object(select_role, "_gh_request", side_effect=_fake_gh_request(routes)):
        flagged = select_role.find_reviewable_claude_prs(
            "silasfelinus/conductor", "fake-token", grace_minutes=5.0, now=now
        )

    assert flagged == []


def test_find_reviewable_claude_prs_ignores_non_green_ci():
    now = datetime(2026, 7, 26, 12, 0, 0, tzinfo=timezone.utc)
    pr = {
        "number": 7,
        "head": {"sha": "bbb222", "ref": "claude/some-branch"},
        "updated_at": "2026-07-26T11:00:00Z",
    }
    routes = {
        "/pulls?state=open": [pr],
        "/commits/bbb222/status": {"state": "pending"},
    }
    with mock.patch.object(select_role, "_gh_request", side_effect=_fake_gh_request(routes)):
        flagged = select_role.find_reviewable_claude_prs(
            "silasfelinus/conductor", "fake-token", grace_minutes=5.0, now=now
        )

    assert flagged == []


def test_find_reviewable_claude_prs_ignores_fresh_pr_still_pushing():
    """A PR updated moments ago may still be having its author actively push
    to it -- must not be flagged until it clears the grace period."""
    now = datetime(2026, 7, 26, 12, 0, 0, tzinfo=timezone.utc)
    pr = {
        "number": 8,
        "head": {"sha": "ccc333", "ref": "claude/some-branch"},
        "updated_at": "2026-07-26T11:58:00Z",  # 2 minutes old
    }
    routes = {
        "/pulls?state=open": [pr],
        "/commits/ccc333/status": {"state": "success"},
    }
    with mock.patch.object(select_role, "_gh_request", side_effect=_fake_gh_request(routes)):
        flagged = select_role.find_reviewable_claude_prs(
            "silasfelinus/conductor", "fake-token", grace_minutes=5.0, now=now
        )

    assert flagged == []


def test_find_reviewable_claude_prs_returns_empty_without_a_token():
    with mock.patch.object(select_role, "list_open_prs") as list_open_prs:
        flagged = select_role.find_reviewable_claude_prs("silasfelinus/conductor", "", grace_minutes=5.0)

    list_open_prs.assert_not_called()
    assert flagged == []


def test_gh_request_degrades_on_unreachable_api_instead_of_crashing():
    """Matches ci_janitor.py/check_pr_merged_drift.py's convention: a 403/
    network failure against api.github.com (this sandbox's own known
    limitation) must never raise out of a role-selection call."""
    with mock.patch(
        "urllib.request.urlopen", side_effect=urllib.error.HTTPError("url", 403, "Forbidden", {}, None)
    ):
        result = select_role._gh_request("https://api.github.com/repos/x/y/pulls", "token")

    assert result is None


# --- find_stranded_branches: local (conductor) vs API (kind_robots) --------


def test_find_stranded_branches_local_delegates_to_branch_janitor_classify():
    with mock.patch.object(
        select_role.branch_janitor, "list_remote_branches", return_value=["claude/old-one"]
    ), mock.patch.object(
        select_role.branch_janitor, "is_merged", return_value=False
    ), mock.patch.object(
        select_role.branch_janitor, "branch_age_hours", return_value=999.0
    ):
        stranded = select_role.find_stranded_branches_local(stale_hours=12.0)

    assert stranded == ["claude/old-one"]


def test_find_stranded_branches_local_excludes_merged_and_fresh():
    with mock.patch.object(
        select_role.branch_janitor,
        "list_remote_branches",
        return_value=["claude/merged-one", "claude/fresh-one"],
    ), mock.patch.object(
        select_role.branch_janitor, "is_merged", side_effect=lambda b: b == "claude/merged-one"
    ), mock.patch.object(
        select_role.branch_janitor, "branch_age_hours", return_value=1.0
    ):
        stranded = select_role.find_stranded_branches_local(stale_hours=12.0)

    assert stranded == []


def test_find_stranded_branches_remote_flags_unmerged_and_old():
    now = datetime(2026, 7, 26, 12, 0, 0, tzinfo=timezone.utc)
    routes = {
        "/branches?per_page=100": [{"name": "claude/keen-fermat-87rn74", "commit": {"sha": "abc"}}],
        "/compare/main...claude%2Fkeen-fermat-87rn74": {"status": "diverged"},
        "/commits/abc": {"commit": {"committer": {"date": "2026-07-21T22:00:00Z"}}},  # ~4 days old
    }
    with mock.patch.object(select_role, "_gh_request", side_effect=_fake_gh_request(routes)):
        stranded = select_role.find_stranded_branches_remote(
            "silasfelinus/kind_robots", "fake-token", stale_hours=12.0, now=now
        )

    assert len(stranded) == 1
    assert stranded[0]["branch"] == "claude/keen-fermat-87rn74"
    assert stranded[0]["repo"] == "silasfelinus/kind_robots"


def test_find_stranded_branches_remote_excludes_merged():
    now = datetime(2026, 7, 26, 12, 0, 0, tzinfo=timezone.utc)
    routes = {
        "/branches?per_page=100": [{"name": "claude/already-merged", "commit": {"sha": "def"}}],
        "/compare/main...claude%2Falready-merged": {"status": "identical"},
        "/commits/def": {"commit": {"committer": {"date": "2026-07-21T22:00:00Z"}}},
    }
    with mock.patch.object(select_role, "_gh_request", side_effect=_fake_gh_request(routes)):
        stranded = select_role.find_stranded_branches_remote(
            "silasfelinus/kind_robots", "fake-token", stale_hours=12.0, now=now
        )

    assert stranded == []


def test_find_stranded_branches_remote_never_flags_undetermined_merge_state():
    """A failed/ambiguous compare call must never be treated as "assume
    stranded" -- that would risk flagging real merged work as needing a
    branch-medic look."""
    now = datetime(2026, 7, 26, 12, 0, 0, tzinfo=timezone.utc)
    routes = {
        "/branches?per_page=100": [{"name": "claude/unknown-state", "commit": {"sha": "ghi"}}],
        # no /compare/ route -> _gh_request returns None -> status undetermined
        "/commits/ghi": {"commit": {"committer": {"date": "2026-07-21T22:00:00Z"}}},
    }
    with mock.patch.object(select_role, "_gh_request", side_effect=_fake_gh_request(routes)):
        stranded = select_role.find_stranded_branches_remote(
            "silasfelinus/kind_robots", "fake-token", stale_hours=12.0, now=now
        )

    assert stranded == []


def test_find_stranded_branches_remote_returns_empty_without_a_token():
    with mock.patch.object(select_role, "list_branches_api") as list_branches_api:
        stranded = select_role.find_stranded_branches_remote("silasfelinus/kind_robots", "", stale_hours=12.0)

    list_branches_api.assert_not_called()
    assert stranded == []


def test_find_stranded_branches_routes_local_repo_to_local_and_others_to_remote():
    with mock.patch.object(
        select_role, "find_stranded_branches_local", return_value=["claude/conductor-stale"]
    ) as local_fn, mock.patch.object(
        select_role,
        "find_stranded_branches_remote",
        return_value=[{"repo": "silasfelinus/kind_robots", "branch": "claude/kr-stale", "stale_hours": 20.0}],
    ) as remote_fn:
        stranded = select_role.find_stranded_branches(
            ["silasfelinus/conductor", "silasfelinus/kind_robots"], "fake-token", stale_hours=12.0
        )

    local_fn.assert_called_once()
    remote_fn.assert_called_once()
    assert remote_fn.call_args.args[0] == "silasfelinus/kind_robots"
    repos_seen = {b["repo"] for b in stranded}
    assert repos_seen == {"silasfelinus/conductor", "silasfelinus/kind_robots"}


# --- site-auditor: find_last_audit_report / site_audit_status --------------


def _make_report(tmp_path, name):
    (tmp_path / name).write_text("# audit\n")


def test_find_last_audit_report_returns_none_when_dir_has_no_reports(tmp_path):
    assert select_role.find_last_audit_report(tmp_path) is None


def test_find_last_audit_report_returns_none_when_dir_missing(tmp_path):
    assert select_role.find_last_audit_report(tmp_path / "does-not-exist") is None


def test_find_last_audit_report_picks_the_newest_by_date_not_filename_sort(tmp_path):
    # Deliberately out of lexicographic order to prove it's a real date parse,
    # not a string sort (which would get 2026-07-9 vs 2026-07-10 wrong).
    _make_report(tmp_path, "AUDIT-REPORT-2026-07-09.md")
    _make_report(tmp_path, "AUDIT-REPORT-2026-07-10.md")
    _make_report(tmp_path, "AUDIT-REPORT-2026-06-30.md")
    _make_report(tmp_path, "not-an-audit-report.md")  # must be ignored

    result = select_role.find_last_audit_report(tmp_path)

    assert result == ("AUDIT-REPORT-2026-07-10.md", date(2026, 7, 10))


def test_site_audit_status_never_run(tmp_path):
    status = select_role.site_audit_status(reports_dir=tmp_path, stale_days=7.0, today=date(2026, 7, 26))
    assert status == {"overdue": True, "last_report": None, "days_since": None}


def test_site_audit_status_not_overdue(tmp_path):
    _make_report(tmp_path, "AUDIT-REPORT-2026-07-24.md")
    status = select_role.site_audit_status(reports_dir=tmp_path, stale_days=7.0, today=date(2026, 7, 26))
    assert status == {"overdue": False, "last_report": "AUDIT-REPORT-2026-07-24.md", "days_since": 2}


def test_site_audit_status_overdue_at_exactly_the_threshold(tmp_path):
    """>= stale_days counts as overdue, not strictly >, so a run scheduled
    for exactly one week later isn't treated as "still fine" for an extra
    cycle."""
    _make_report(tmp_path, "AUDIT-REPORT-2026-07-19.md")
    status = select_role.site_audit_status(reports_dir=tmp_path, stale_days=7.0, today=date(2026, 7, 26))
    assert status == {"overdue": True, "last_report": "AUDIT-REPORT-2026-07-19.md", "days_since": 7}


# --- read-only contract, same pin as run_worker.py/run_reviewer.py ---------


def test_script_is_read_only_like_its_sources():
    text = SELECT_ROLE.read_text()
    for forbidden in ("def claim_task", "def set_task_status", "def write_roadmap", "delete_branch(", "'w')"):
        assert forbidden not in text, f"{forbidden!r} would make this script no longer read-only"
