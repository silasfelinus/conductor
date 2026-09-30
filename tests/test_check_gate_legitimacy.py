"""Contract for scripts/check_gate_legitimacy.py (Silas, 2026-09-30)."""
from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path

import yaml

from scripts import check_gate_legitimacy as cgl

TODAY = date(2026, 9, 30)


def _project(tmp_path: Path, tasks: list[dict], kind: str = "software", slug: str = "demo") -> Path:
    projects = tmp_path / "projects"
    (projects / slug).mkdir(parents=True)
    (projects / slug / "roadmap.yaml").write_text(
        yaml.safe_dump({"project": slug, "kind": kind, "tasks": tasks}), encoding="utf-8"
    )
    (projects / "priority.yaml").write_text(yaml.safe_dump({"order": [slug]}), encoding="utf-8")
    (tmp_path / "project-overrides.yaml").write_text(
        yaml.safe_dump({"overrides": [{"slug": slug, "status": "active"}]}), encoding="utf-8"
    )
    return projects


def _codes(projects: Path, **kwargs) -> dict[str, list[str]]:
    return {
        item["task_id"]: [f["code"] for f in item["findings"]]
        for item in cgl.check(projects, today=TODAY, **kwargs)
    }


def gate(**fields) -> dict:
    return {"id": "t-001", "title": "x", "status": "needs-human", "updated": "2026-09-29T00:00:00Z", **fields}


def test_hard_gate_with_no_basis_is_flagged(tmp_path):
    projects = _project(tmp_path, [gate(gate_human=False, stakes="reversible")])
    assert "NO_GATE_BASIS" in _codes(projects)["t-001"]


def test_real_hard_gates_are_not_no_basis(tmp_path):
    for fields in ({"gate_human": True}, {"stakes": "outward-facing"}, {"stakes": "irreversible"},
                   {"gate_reason": "money"}, {"soft_gate": True}):
        projects = _project(tmp_path / str(len(list(tmp_path.iterdir()))), [gate(**fields)])
        assert "NO_GATE_BASIS" not in _codes(projects).get("t-001", [])
    projects = _project(tmp_path / "content", [gate()], kind="content")
    assert "NO_GATE_BASIS" not in _codes(projects).get("t-001", [])


def test_approved_but_parked(tmp_path):
    projects = _project(tmp_path, [gate(gate_human=True, approved_by_human=True)])
    assert "APPROVED_PARKED" in _codes(projects)["t-001"]


def test_approved_waiting_on_hands_is_legitimate(tmp_path):
    for reason in ("physical-access", "secrets"):
        projects = _project(tmp_path / reason, [gate(gate_human=True, approved_by_human=True, gate_reason=reason)])
        assert "APPROVED_PARKED" not in _codes(projects).get("t-001", [])


def test_unmet_dependency_should_be_waiting(tmp_path):
    projects = _project(tmp_path, [
        gate(gate_human=True, depends_on=["t-002"]),
        {"id": "t-002", "title": "y", "status": "ready"},
    ])
    assert "SHOULD_BE_WAITING" in _codes(projects)["t-001"]


def test_met_dependency_is_fine(tmp_path):
    projects = _project(tmp_path, [
        gate(gate_human=True, depends_on="t-002"),
        {"id": "t-002", "title": "y", "status": "done"},
    ])
    assert "SHOULD_BE_WAITING" not in _codes(projects).get("t-001", [])


def test_unreviewed_windows(tmp_path):
    old = "2026-09-01T00:00:00Z"
    projects = _project(tmp_path / "soft", [gate(soft_gate=True, updated="2026-09-22T00:00:00Z")])
    assert "UNREVIEWED" in _codes(projects)["t-001"]  # 8 days, soft window 7
    projects = _project(tmp_path / "hard", [gate(gate_human=True, updated="2026-09-22T00:00:00Z")])
    assert "UNREVIEWED" not in _codes(projects).get("t-001", [])  # 8 days, hard window 14
    projects = _project(tmp_path / "reasoned", [gate(gate_human=True, gate_reason="money", updated=old)])
    assert "UNREVIEWED" not in _codes(projects).get("t-001", [])  # 29 days, reasoned window 30
    projects = _project(tmp_path / "rechecked", [gate(soft_gate=True, updated=old, gate_rechecked="2026-09-29")])
    assert "UNREVIEWED" not in _codes(projects).get("t-001", [])


def test_deploy_prereq_met_only_when_note_waits_on_deploy(tmp_path):
    deployed = datetime(2026, 9, 30, 4, 58, tzinfo=timezone.utc)
    projects = _project(tmp_path / "a", [gate(gate_human=True, note="Needs a Force Update on Alexandria first.")])
    assert "DEPLOY_PREREQ_MET" in _codes(projects, deployed_at=deployed)["t-001"]
    projects = _project(tmp_path / "b", [gate(gate_human=True, note="Silas picks a colour.")])
    assert "DEPLOY_PREREQ_MET" not in _codes(projects, deployed_at=deployed).get("t-001", [])
    projects = _project(tmp_path / "c", [gate(gate_human=True, note="Force Update pending.",
                                              updated="2026-09-30T06:00:00Z")])
    assert "DEPLOY_PREREQ_MET" not in _codes(projects, deployed_at=deployed).get("t-001", [])


def test_inactive_projects_are_skipped(tmp_path):
    projects = _project(tmp_path, [gate(gate_human=False)])
    (tmp_path / "project-overrides.yaml").write_text(
        yaml.safe_dump({"overrides": [{"slug": "demo", "status": "paused"}]}), encoding="utf-8"
    )
    assert _codes(projects) == {}
