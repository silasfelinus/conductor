from pathlib import Path
import sys

from scripts.project_lifecycle import (
    PROJECT_LIFECYCLE_STATUSES,
    WORKABLE_PROJECT_STATUSES,
    ordered_workable_slugs,
)
from scripts.playtest_readiness import playtest_readiness_errors
from scripts.build_status import compute_progress
from scripts import sync_playtest_master_issues as handoff
from scripts.sync_playtest_master_issues import eligible_issues, PREFIX


def test_playtest_is_workable_fallback_with_continuous():
    assert "playtest" in PROJECT_LIFECYCLE_STATUSES
    assert "playtest" in WORKABLE_PROJECT_STATUSES
    overrides = {
        "ongoing": {"status": "continuous"},
        "game": {"status": "playtest"},
        "build": {"status": "active"},
        "paused": {"status": "paused"},
    }
    assert ordered_workable_slugs(
        ["ongoing", "game", "paused", "build"], overrides
    ) == ["build", "ongoing", "game"]


def test_readiness_requires_complete_build_not_a_human_playtest_task():
    done = {"id": "build", "status": "done"}
    verdict = {
        "id": "human-verdict",
        "status": "needs-human",
        "gate_human": True,
        "gate_reason": "subjective-acceptance",
    }
    assert playtest_readiness_errors([done]) == []
    assert playtest_readiness_errors([done, verdict]) == []
    assert playtest_readiness_errors([verdict]) == ["no completed finite production task"]
    assert playtest_readiness_errors([{"id": "build", "status": "ready"}])
    assert playtest_readiness_errors([done, {**verdict, "status": "ready"}]) == []
    assert playtest_readiness_errors([done, {**verdict, "status": "waiting"}]) == []
    assert playtest_readiness_errors([done, {"id": "art", "status": "review"}])
    assert playtest_readiness_errors([done, {"id": "publish", "status": "waiting",
                                            "gate_human": True, "gate_reason": "publish"}]) == []
    assert playtest_readiness_errors([done, {"id": "legal", "status": "needs-human",
                                            "gate_human": True, "gate_reason": "legal"}])
    assert playtest_readiness_errors([done, {"id": "post-launch", "status": "ready",
                                            "playtest_iteration": True}]) == []
    assert playtest_readiness_errors([done, {"id": "recurring", "status": "ready",
                                            "recurring": True}]) == []



def test_one_hundred_percent_means_no_agent_owned_production_left():
    milestones = [{"weight": 100, "status": "done"}]
    unfinished_art = [{"id": "art", "status": "ready"}]
    assert compute_progress(milestones, unfinished_art) == 99.0
    assert compute_progress(milestones, [{"id": "cancelled", "status": "cancelled"}]) == 99.0

    finished = [{"id": "build", "status": "done"}]
    assert compute_progress([{"weight": 100, "status": "in-progress"}], finished) == 100.0

    human_verdict = {
        "id": "verdict",
        "status": "needs-human",
        "gate_human": True,
        "gate_reason": "subjective-acceptance",
    }
    assert compute_progress(milestones, finished + [human_verdict]) == 100.0

    waiting_verdict = {**human_verdict, "status": "waiting"}
    assert compute_progress(milestones, finished + [waiting_verdict]) == 100.0

    release_gate = {
        "id": "publish",
        "status": "needs-human",
        "gate_human": True,
        "gate_reason": "publish",
    }
    assert compute_progress(milestones, finished + [release_gate]) == 100.0

    no_production = [{"id": "recurring", "status": "ready", "recurring": True}]
    assert compute_progress([{"weight": 100, "status": "in-progress"}], no_production) == 50.0


def test_issue_handoff_is_scoped_to_valid_playtest_games(tmp_path: Path):
    game = tmp_path / "game"
    game.mkdir()
    (game / "roadmap.yaml").write_text(
        "tasks:\n"
        "  - id: t-001\n    status: done\n",
        encoding="utf-8",
    )
    projects = {
        "game": {"status": "playtest"},
        "other": {"status": "continuous"},
    }
    issues, errors = eligible_issues(
        projects,
        {"game": "https://github.com/silasfelinus/kind_robots/issues/123"},
        tmp_path,
    )
    assert issues == [("game", 123)]
    assert errors == []
    assert PREFIX == "[FLAGGED FOR HUMAN TESTING] "
    (game / "roadmap.yaml").write_text("tasks:\n  - id: t-001\n    status: ready\n", encoding="utf-8")
    issues, errors = eligible_issues(projects, {"game": "https://github.com/silasfelinus/kind_robots/issues/123"}, tmp_path)
    assert not issues
    assert errors



def test_handoff_fails_closed_for_malformed_roadmap_structures(tmp_path: Path):
    game = tmp_path / "game"
    game.mkdir()
    project = {"game": {"status": "playtest"}}
    issue = {"game": "https://github.com/silasfelinus/kind_robots/issues/123"}
    for bad_yaml in (
        "- id: t-001\n  status: done\n",
        "ready\n",
        "tasks: null\n",
        "tasks: {t-001: done}\n",
        "tasks: 'done'\n",
        "tasks: []\n",
        "tasks: [invalid\n",
    ):
        (game / "roadmap.yaml").write_text(bad_yaml, encoding="utf-8")
        issues, errors = eligible_issues(project, issue, tmp_path)
        assert issues == [], f"must not close issue for {bad_yaml!r}"
        assert errors and errors[0].startswith("game:")


def _handoff_fixture(tmp_path, monkeypatch, *, status="playtest", task_status="done"):
    (tmp_path / "projects" / "game").mkdir(parents=True)
    (tmp_path / "docs" / "agents").mkdir(parents=True)
    (tmp_path / "project-overrides.yaml").write_text(
        f"overrides:\n  - slug: game\n    status: {status}\n", encoding="utf-8"
    )
    (tmp_path / "docs" / "agents" / "master-issues.yaml").write_text(
        "master_issues:\n  game: https://github.com/silasfelinus/kind_robots/issues/123\n",
        encoding="utf-8",
    )
    (tmp_path / "projects" / "game" / "roadmap.yaml").write_text(
        "tasks:\n"
        f"  - id: t-001\n    status: {task_status}\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(handoff, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["sync_playtest_master_issues.py"])
    monkeypatch.setenv("ISSUE_BRIDGE_TOKEN", "test-not-a-real-token")


def test_verified_playtest_handoff_flags_and_closes_once(tmp_path, monkeypatch):
    _handoff_fixture(tmp_path, monkeypatch)
    issue = {"title": "[ROADMAP] Game", "state": "open"}
    writes = []

    def fake_github(method, number, token, data=None):
        assert number == 123
        if method == "GET":
            return issue.copy()
        assert method == "PATCH"
        writes.append(data)
        issue.update(data)
        return issue.copy()

    monkeypatch.setattr(handoff, "github_issue", fake_github)
    assert handoff.main() == 0
    assert writes == [{
        "title": "[FLAGGED FOR HUMAN TESTING] [ROADMAP] Game",
        "state": "closed",
        "state_reason": "completed",
    }]
    assert handoff.main() == 0
    assert len(writes) == 1, "repeated sync must not write again"


def test_incomplete_playtest_does_not_close_issue(tmp_path, monkeypatch):
    _handoff_fixture(tmp_path, monkeypatch, task_status="ready")
    writes = []
    monkeypatch.setattr(handoff, "github_issue", lambda *args: writes.append(args))
    assert handoff.main() == 1
    assert writes == [], "incomplete games must not change GitHub issues"


def test_active_project_does_not_close_master_issue(tmp_path, monkeypatch):
    _handoff_fixture(tmp_path, monkeypatch, status="active")
    writes = []
    monkeypatch.setattr(handoff, "github_issue", lambda *args: writes.append(args))
    assert handoff.main() == 0
    assert writes == [], "active development must not alter the roadmap issue"

def test_shifting_desks_owner_waiver_preserves_known_incomplete_work(tmp_path: Path):
    game = tmp_path / "shifting-desks"
    game.mkdir()
    (game / "roadmap.yaml").write_text(
        "tasks:\n"
        "  - id: t-041\n    status: claimed\n"
        "  - id: t-046\n    status: review\n"
        "  - id: t-021\n    status: needs-human\n"
        "    gate_human: true\n    gate_reason: creative-approval\n",
        encoding="utf-8",
    )
    project = {
        "status": "playtest",
        "early_playtest_owner_waiver": {
            "approved_by": "Silas",
            "approved_on": "2026-11-17",
            "direction": "Open for early public playtesting",
            "handoff": "projects/shifting-desks/PLAYTEST-HANDOFF-2026-11-17.md",
            "known_open_tasks": ["t-041", "t-046"],
        },
    }
    master = {"shifting-desks": "https://github.com/silasfelinus/kind_robots/issues/4150"}
    eligible, errors = eligible_issues({"shifting-desks": project}, master, tmp_path)
    assert eligible == [("shifting-desks", 4150)]
    assert errors == []

    # Never extend this owner waiver to newly discovered incomplete work.
    with (game / "roadmap.yaml").open("a", encoding="utf-8") as file:
        file.write("  - id: t-999\n    status: ready\n")
    eligible, errors = eligible_issues({"shifting-desks": project}, master, tmp_path)
    assert eligible == []
    assert "t-999" in str(errors)

    # The exception may not be borrowed by a different game.
    eligible, errors = eligible_issues(
        {"another-game": project},
        {"another-game": "https://github.com/silasfelinus/kind_robots/issues/4150"},
        tmp_path,
    )
    assert eligible == []
    assert errors
