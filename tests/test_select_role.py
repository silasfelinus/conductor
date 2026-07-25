"""Tests for scripts/select_role.py (conductor/t-026).

select_role.py is the repo-side fix for "the Reviewer trigger fires with
nothing to review": it composes run_reviewer.py's open-worker/*-branch check
with run_worker.py's ready-task check into one role recommendation, so a
session decides Worker-vs-Reviewer from live state on arrival instead of from
which platform trigger happened to fire it.
"""

import py_compile
from pathlib import Path
from unittest import mock

import scripts.select_role as select_role


ROOT = Path(__file__).resolve().parents[1]
SELECT_ROLE = ROOT / "scripts" / "select_role.py"


def test_script_compiles():
    py_compile.compile(str(SELECT_ROLE), doraise=True)


def test_reviewer_wins_when_worker_branches_exist():
    """A candidate worker/* branch always means role: reviewer, even if a
    ready task also exists -- reviewing unblocks a Worker's stuck PR, which is
    higher-leverage than starting fresh work."""
    branch = {
        "branch": "worker/some-project-t-001",
        "last_commit": "abc123 do the thing",
        "author": "some-worker",
        "age": "2 hours ago",
    }
    with mock.patch.object(select_role.run_reviewer, "refresh_remotes"), mock.patch.object(
        select_role.run_reviewer, "remote_worker_branches", return_value=[branch]
    ), mock.patch.object(
        select_role.run_worker,
        "build_queue_summary",
        return_value={
            "ready_task": {"project": "some-project", "task_id": "t-002", "title": "x"},
            "projects_with_ready_tasks": ["some-project"],
            "projects_needing_human": [],
        },
    ):
        result = select_role.select_role()

    assert result["role"] == "reviewer"
    assert result["candidate_worker_branch_count"] == 1
    assert result["candidate_worker_branches"] == [branch]
    # The ready task is still surfaced in the output even though it didn't
    # win the role decision -- a session that finishes reviewing can pick it
    # up next without a second scan.
    assert result["ready_task"]["task_id"] == "t-002"


def test_worker_when_no_branches_but_ready_task_exists():
    with mock.patch.object(select_role.run_reviewer, "refresh_remotes"), mock.patch.object(
        select_role.run_reviewer, "remote_worker_branches", return_value=[]
    ), mock.patch.object(
        select_role.run_worker,
        "build_queue_summary",
        return_value={
            "ready_task": {"project": "some-project", "task_id": "t-002", "title": "x"},
            "projects_with_ready_tasks": ["some-project"],
            "projects_needing_human": [],
        },
    ):
        result = select_role.select_role()

    assert result["role"] == "worker"
    assert "some-project/t-002" in result["reason"]


def test_idle_when_neither_branches_nor_ready_task():
    with mock.patch.object(select_role.run_reviewer, "refresh_remotes"), mock.patch.object(
        select_role.run_reviewer, "remote_worker_branches", return_value=[]
    ), mock.patch.object(
        select_role.run_worker,
        "build_queue_summary",
        return_value={
            "ready_task": None,
            "projects_with_ready_tasks": [],
            "projects_needing_human": [],
        },
    ):
        result = select_role.select_role()

    assert result["role"] == "idle"
    assert result["ready_task"] is None


def test_remote_refresh_failure_does_not_crash_selection():
    """A network hiccup on `git fetch` (sandbox egress, transient outage)
    should degrade to whatever refs are already known locally, not blow up
    the whole role-selection call."""
    with mock.patch.object(
        select_role.run_reviewer, "refresh_remotes", side_effect=RuntimeError("network down")
    ), mock.patch.object(
        select_role.run_reviewer, "remote_worker_branches", return_value=[]
    ), mock.patch.object(
        select_role.run_worker,
        "build_queue_summary",
        return_value={"ready_task": None, "projects_with_ready_tasks": [], "projects_needing_human": []},
    ):
        result = select_role.select_role()

    assert result["role"] == "idle"


def test_script_is_read_only_like_its_two_sources():
    """Same contract pinned for run_worker.py / run_reviewer.py: this script
    only recommends a role, it never mutates task status or roadmap files."""
    text = SELECT_ROLE.read_text()
    for forbidden in ("def claim_task", "def set_task_status", "def write_roadmap", "open(", "w+", "'w'"):
        assert forbidden not in text, f"{forbidden!r} would make this script no longer read-only"
