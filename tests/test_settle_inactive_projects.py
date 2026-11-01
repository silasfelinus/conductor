"""settle_inactive_projects.py: live claims/reviews in inactive projects are flagged and released."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import settle_inactive_projects as sip  # noqa: E402

ROADMAP = """project: demo
kind: software
tasks:
  - id: t-001
    title: stale claim
    status: claimed
    note: started
    claimed_by: sess-1
    claimed_at: '2026-10-01T00:00:00Z'
  - id: t-002
    title: gated with provenance
    status: needs-human
    note: waiting on Silas
    claimed_by: sess-2
  - id: t-003
    title: parked
    status: ready
"""


def _repo(tmp_path: Path, status: str) -> Path:
    (tmp_path / "projects" / "demo").mkdir(parents=True)
    (tmp_path / "projects" / "demo" / "roadmap.yaml").write_text(ROADMAP)
    (tmp_path / "project-overrides.yaml").write_text(
        f"overrides:\n  - slug: demo\n    status: {status}\n")
    return tmp_path


def test_active_project_is_ignored(tmp_path):
    result = sip.scan(_repo(tmp_path, "active"))
    assert result == {"live": [], "retired_open": [], "parked": {}}


def test_retired_project_open_work_is_cancelled(tmp_path):
    root = _repo(tmp_path, "retired")
    result = sip.scan(root)
    assert [i["task"] for i in result["retired_open"]] == ["t-001", "t-002", "t-003"]
    sip.cancel_retired(root, result["retired_open"], "2026-11-01")
    tasks = yaml.safe_load((root / "projects/demo/roadmap.yaml").read_text())["tasks"]
    assert {t["status"] for t in tasks} == {"cancelled"}
    assert all(t["cancelled_reason"] == "project-retired" and t["claimed_by"] is None for t in tasks)
    assert sip.scan(root)["retired_open"] == []


def test_inactive_project_flags_only_live_statuses(tmp_path):
    result = sip.scan(_repo(tmp_path, "paused"))
    assert [i["task"] for i in result["live"]] == ["t-001"]
    assert result["parked"]["demo"]["count"] == 2


def test_settle_releases_claim_and_keeps_gate(tmp_path):
    root = _repo(tmp_path, "finished")
    sip.settle(root, sip.scan(root)["live"], "2026-11-01")
    tasks = {t["id"]: t for t in yaml.safe_load((root / "projects/demo/roadmap.yaml").read_text())["tasks"]}
    assert tasks["t-001"]["status"] == "ready"
    assert tasks["t-001"]["claimed_by"] is None and tasks["t-001"]["claimed_at"] is None
    assert tasks["t-001"]["note"].startswith("started")
    assert "released by settle_inactive_projects.py" in tasks["t-001"]["note"]
    assert tasks["t-002"]["status"] == "needs-human" and tasks["t-002"]["claimed_by"] == "sess-2"
    assert sip.scan(root)["live"] == []


def test_cancelled_tasks_leave_progress_denominator():
    import build_status
    tasks = [{"status": "done"}, {"status": "cancelled"}, {"status": "cancelled"}, {"status": "ready"}]
    assert build_status.compute_progress([], tasks) == 50.0
    assert build_status.compute_progress([], [{"status": "cancelled"}]) == 0.0
