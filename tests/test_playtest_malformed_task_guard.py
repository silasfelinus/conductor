"""Regression: malformed task records must never silently grant playtest readiness."""

from pathlib import Path

import yaml

from scripts.playtest_readiness import playtest_readiness_errors
from scripts.sync_playtest_master_issues import eligible_issues


def test_malformed_tasks_cannot_pass_human_gate():
    tasks = [
        {"id": "t-001", "status": "done"},
        None,
        "accidentally pasted task",
        {"id": "t-002", "status": "needs-human", "gate_human": True,
         "gate_reason": "subjective-acceptance", "approved_by_human": False},
    ]
    errors = playtest_readiness_errors(tasks)
    assert any("malformed roadmap tasks at positions: 2, 3" in error for error in errors)


def test_valid_human_handoff_still_passes():
    tasks = [
        {"id": "t-001", "status": "done"},
        {"id": "t-002", "status": "needs-human", "gate_human": True,
         "gate_reason": "creative-approval", "approved_by_human": False},
    ]
    assert playtest_readiness_errors(tasks) == []


def test_malformed_project_cannot_close_master_issue(tmp_path: Path):
    root = tmp_path / "projects" / "example"
    root.mkdir(parents=True)
    (root / "roadmap.yaml").write_text(yaml.safe_dump({"tasks": [
        {"id": "t-001", "status": "done"},
        [],
        {"id": "t-002", "status": "needs-human", "gate_human": True,
         "gate_reason": "subjective-acceptance"},
    ]}), encoding="utf-8")
    eligible, problems = eligible_issues(
        {"example": {"status": "playtest"}},
        {"example": "https://github.com/silasfelinus/kind_robots/issues/4150"},
        tmp_path / "projects",
    )
    assert eligible == []
    assert any("malformed roadmap tasks at positions: 2" in problem for problem in problems)
