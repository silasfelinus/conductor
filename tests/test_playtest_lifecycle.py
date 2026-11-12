from pathlib import Path

from scripts.project_lifecycle import (
    PROJECT_LIFECYCLE_STATUSES,
    WORKABLE_PROJECT_STATUSES,
    ordered_workable_slugs,
)
from scripts.playtest_readiness import playtest_readiness_errors
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


def test_readiness_needs_real_human_gate_and_all_finite_agent_tasks_complete():
    gate = {
        "id": "t-002",
        "status": "needs-human",
        "gate_human": True,
        "gate_reason": "subjective-acceptance",
    }
    assert playtest_readiness_errors([{"id": "t-001", "status": "done"}, gate]) == []
    assert playtest_readiness_errors([{"id": "t-001", "status": "ready"}, gate])
    assert playtest_readiness_errors([{"id": "t-001", "status": "done"}])
    assert playtest_readiness_errors([{"id": "t-001", "status": "done"}, {**gate, "status": "waiting"}])
    assert playtest_readiness_errors([{"id": "t-001", "status": "done"}, {**gate, "approved_by_human": True}])
    assert playtest_readiness_errors(
        [{"id": "t-001", "status": "done"}, {**gate, "gate_reason": "publish"}]
    )
    assert playtest_readiness_errors(
        [{"id": "t-001", "status": "ready", "recurring": True}, gate]
    ) == []
    assert playtest_readiness_errors(
        [{"id": "t-003", "status": "ready", "playtest_iteration": True}, gate]
    ) == []
    assert playtest_readiness_errors(
        [{"id": "art", "status": "waiting", "gate_human": True, "gate_reason": "creative-approval"}, gate]
    )
    assert playtest_readiness_errors(
        [{"id": "legal", "status": "needs-human", "gate_human": True, "gate_reason": "legal"}, gate]
    )


def test_issue_handoff_is_scoped_to_valid_playtest_games(tmp_path: Path):
    game = tmp_path / "game"
    game.mkdir()
    (game / "roadmap.yaml").write_text(
        "tasks:\n"
        "  - id: t-001\n    status: done\n"
        "  - id: t-002\n    status: needs-human\n    gate_human: true\n"
        "    gate_reason: subjective-acceptance\n",
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
