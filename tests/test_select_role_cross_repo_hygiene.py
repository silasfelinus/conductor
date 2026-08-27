"""Focused regression coverage for the 2026-08-27 cross-repo hygiene sweep."""

from datetime import datetime, timezone
from unittest import mock

import scripts.select_role as select_role


def test_default_repos_cover_current_active_code_repos():
    assert select_role.DEFAULT_REPOS == (
        "silasfelinus/conductor",
        "silasfelinus/kind_robots",
        "silasfelinus/Kapowarr",
        "silasfelinus/cthulhuquarium",
    )


def test_pr_medic_ignores_intentionally_parked_draft_prs():
    now = datetime(2026, 8, 27, 22, 30, tzinfo=timezone.utc)
    parked = {
        "number": 2110,
        "draft": True,
        "head": {"sha": "deadbeef"},
        "updated_at": "2026-08-25T16:34:57Z",
    }
    with mock.patch.object(select_role, "list_open_prs", return_value=[parked]), mock.patch.object(
        select_role, "commit_combined_state"
    ) as commit_state:
        flagged = select_role.find_red_stale_prs_in_repo(
            "silasfelinus/kind_robots",
            "fake-token",
            stale_hours=3.0,
            now=now,
        )

    assert flagged == []
    commit_state.assert_not_called()


def test_reviewer_ignores_intentionally_parked_draft_prs():
    now = datetime(2026, 8, 27, 22, 30, tzinfo=timezone.utc)
    parked = {
        "number": 3029,
        "draft": True,
        "head": {"sha": "feedface", "ref": "claude/parked"},
        "updated_at": "2026-08-27T20:00:00Z",
    }
    with mock.patch.object(select_role, "list_open_prs", return_value=[parked]), mock.patch.object(
        select_role, "commit_combined_state"
    ) as commit_state:
        flagged = select_role.find_reviewable_claude_prs(
            "silasfelinus/conductor",
            "fake-token",
            grace_minutes=5.0,
            now=now,
        )

    assert flagged == []
    commit_state.assert_not_called()


def test_cthulhuquarium_branch_medic_compares_against_master():
    now = datetime(2026, 8, 27, 22, 30, tzinfo=timezone.utc)
    branch = {"name": "worker/old-fish", "commit": {"sha": "abc123"}}
    old_commit = datetime(2026, 8, 26, 0, 0, tzinfo=timezone.utc)

    with mock.patch.object(select_role, "list_branches_api", return_value=[branch]), mock.patch.object(
        select_role, "is_branch_merged_api", return_value=False
    ) as is_merged, mock.patch.object(
        select_role, "branch_commit_date_api", return_value=old_commit
    ):
        stranded = select_role.find_stranded_branches_remote(
            "silasfelinus/cthulhuquarium",
            "fake-token",
            stale_hours=12.0,
            now=now,
        )

    assert len(stranded) == 1
    assert stranded[0]["branch"] == "worker/old-fish"
    assert is_merged.call_args.kwargs["base"] == "master"


def test_other_remote_repos_still_compare_against_main():
    now = datetime(2026, 8, 27, 22, 30, tzinfo=timezone.utc)
    branch = {"name": "worker/old-comic", "commit": {"sha": "abc123"}}
    old_commit = datetime(2026, 8, 26, 0, 0, tzinfo=timezone.utc)

    with mock.patch.object(select_role, "list_branches_api", return_value=[branch]), mock.patch.object(
        select_role, "is_branch_merged_api", return_value=False
    ) as is_merged, mock.patch.object(
        select_role, "branch_commit_date_api", return_value=old_commit
    ):
        select_role.find_stranded_branches_remote(
            "silasfelinus/Kapowarr",
            "fake-token",
            stale_hours=12.0,
            now=now,
        )

    assert is_merged.call_args.kwargs["base"] == "main"
