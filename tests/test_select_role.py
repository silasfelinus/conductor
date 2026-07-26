"""Tests for scripts/select_role.py (conductor/t-026, extended).

select_role.py is the repo-side fix for "a session's role is decided by which
platform trigger fired it, not by live state": it composes four existing
signals (open worker/* branches, red+stale open PRs, stranded branches, ready
tasks) into one recommendation, in priority order, so a session decides its
own role on arrival instead of following a trigger label that may not match
what the repo actually needs.
"""

import py_compile
import urllib.error
from datetime import datetime, timezone
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


def _patched(
    remote_worker_branches=(),
    red_stale_prs=(),
    stranded_branches=(),
    queue_summary=None,
):
    """One combined patch context covering all four signals, each defaulted
    to "nothing found" and overridden per-test — keeps each test asserting
    only the signal(s) it's actually about."""
    return (
        mock.patch.object(select_role.run_reviewer, "refresh_remotes"),
        mock.patch.object(
            select_role.run_reviewer, "remote_worker_branches", return_value=list(remote_worker_branches)
        ),
        mock.patch.object(select_role, "find_red_stale_prs", return_value=list(red_stale_prs)),
        mock.patch.object(select_role, "find_stranded_branches", return_value=list(stranded_branches)),
        mock.patch.object(
            select_role.run_worker, "build_queue_summary", return_value=queue_summary or EMPTY_QUEUE
        ),
    )


def test_script_compiles():
    py_compile.compile(str(SELECT_ROLE), doraise=True)


def test_reviewer_outranks_everything():
    patches = _patched(
        remote_worker_branches=[{"branch": "worker/x-t-001"}],
        red_stale_prs=[{"repo": "silasfelinus/conductor", "number": 1}],
        stranded_branches=["claude/some-stale-branch"],
        queue_summary=SOME_READY_TASK,
    )
    with patches[0], patches[1], patches[2], patches[3], patches[4]:
        result = select_role.select_role()

    assert result["role"] == "reviewer"
    assert result["candidate_worker_branch_count"] == 1
    # Other signals still surfaced even though they didn't win the role, so a
    # session that clears the reviewer queue doesn't have to re-scan from
    # scratch for what's next.
    assert result["red_stale_pr_count"] == 1
    assert result["stranded_branch_count"] == 1
    assert result["ready_task"]["task_id"] == "t-002"


def test_pr_medic_outranks_branch_medic_and_worker():
    patches = _patched(
        red_stale_prs=[{"repo": "silasfelinus/conductor", "number": 42, "ci_state": "failure"}],
        stranded_branches=["claude/some-stale-branch"],
        queue_summary=SOME_READY_TASK,
    )
    with patches[0], patches[1], patches[2], patches[3], patches[4]:
        result = select_role.select_role()

    assert result["role"] == "pr-medic"
    assert "1 open PR" in result["reason"]


def test_branch_medic_outranks_worker():
    patches = _patched(stranded_branches=["claude/orphaned-work"], queue_summary=SOME_READY_TASK)
    with patches[0], patches[1], patches[2], patches[3], patches[4]:
        result = select_role.select_role()

    assert result["role"] == "branch-medic"
    assert result["stranded_branches"] == ["claude/orphaned-work"]


def test_worker_when_only_ready_task_exists():
    patches = _patched(queue_summary=SOME_READY_TASK)
    with patches[0], patches[1], patches[2], patches[3], patches[4]:
        result = select_role.select_role()

    assert result["role"] == "worker"
    assert "some-project/t-002" in result["reason"]


def test_idle_when_nothing_needs_doing():
    patches = _patched()
    with patches[0], patches[1], patches[2], patches[3], patches[4]:
        result = select_role.select_role()

    assert result["role"] == "idle"


def test_remote_refresh_failure_does_not_crash_selection():
    with mock.patch.object(
        select_role.run_reviewer, "refresh_remotes", side_effect=RuntimeError("network down")
    ), mock.patch.object(
        select_role.run_reviewer, "remote_worker_branches", return_value=[]
    ), mock.patch.object(
        select_role, "find_red_stale_prs", return_value=[]
    ), mock.patch.object(
        select_role, "find_stranded_branches", return_value=[]
    ), mock.patch.object(
        select_role.run_worker, "build_queue_summary", return_value=EMPTY_QUEUE
    ):
        result = select_role.select_role()

    assert result["role"] == "idle"


# --- find_red_stale_prs: real decision logic (not the role-priority mocks above)


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
        flagged = select_role.find_red_stale_prs(
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
        flagged = select_role.find_red_stale_prs(
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
        flagged = select_role.find_red_stale_prs(
            "silasfelinus/conductor", "fake-token", stale_hours=3.0, now=now
        )

    assert flagged == []


def test_find_red_stale_prs_returns_empty_without_a_token():
    """No GITHUB_TOKEN -> skip cleanly, never attempt an unauthenticated call."""
    with mock.patch.object(select_role, "list_open_prs") as list_open_prs:
        flagged = select_role.find_red_stale_prs("silasfelinus/conductor", "", stale_hours=3.0)

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


# --- find_stranded_branches: delegates to branch_janitor.py's own classifier


def test_find_stranded_branches_delegates_to_branch_janitor_classify():
    with mock.patch.object(
        select_role.branch_janitor, "list_remote_branches", return_value=["claude/old-one"]
    ), mock.patch.object(
        select_role.branch_janitor, "is_merged", return_value=False
    ), mock.patch.object(
        select_role.branch_janitor, "branch_age_hours", return_value=999.0
    ):
        stranded = select_role.find_stranded_branches(stale_hours=12.0)

    assert stranded == ["claude/old-one"]


def test_find_stranded_branches_excludes_merged_and_fresh():
    with mock.patch.object(
        select_role.branch_janitor,
        "list_remote_branches",
        return_value=["claude/merged-one", "claude/fresh-one"],
    ), mock.patch.object(
        select_role.branch_janitor, "is_merged", side_effect=lambda b: b == "claude/merged-one"
    ), mock.patch.object(
        select_role.branch_janitor, "branch_age_hours", return_value=1.0
    ):
        stranded = select_role.find_stranded_branches(stale_hours=12.0)

    assert stranded == []


# --- read-only contract, same pin as run_worker.py/run_reviewer.py ---------


def test_script_is_read_only_like_its_sources():
    text = SELECT_ROLE.read_text()
    for forbidden in ("def claim_task", "def set_task_status", "def write_roadmap", "delete_branch(", "'w')"):
        assert forbidden not in text, f"{forbidden!r} would make this script no longer read-only"
