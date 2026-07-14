import subprocess
import sys
from pathlib import Path

import yaml

import scripts.resolve_deps as resolve_deps


SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "resolve_deps.py"


# ---------------------------------------------------------------------------
# satisfied() -- the core dependency check. ai-art-academy/t-012 asks us to
# confirm this treats a "decision" gate (t-011: a licensing ruling recorded as
# gate_human + approved_by_human) identically to a plain "brief-confirmation"
# gate, since the function has no notion of task *kind* at all -- it only
# looks at status/gate_human/approved_by_human.
# ---------------------------------------------------------------------------


def test_satisfied_plain_done_task():
    assert resolve_deps.satisfied({"status": "done"}) is True


def test_satisfied_false_when_not_done():
    assert resolve_deps.satisfied({"status": "ready"}) is False
    assert resolve_deps.satisfied({"status": "claimed"}) is False


def test_satisfied_gate_human_without_approval_is_unsatisfied():
    assert resolve_deps.satisfied({"status": "done", "gate_human": True}) is False


def test_satisfied_gate_human_with_approval_is_satisfied():
    assert (
        resolve_deps.satisfied(
            {"status": "done", "gate_human": True, "approved_by_human": True}
        )
        is True
    )


def test_satisfied_decision_style_gate_matches_brief_confirmation_gate():
    """A licensing DECISION (t-011's shape) and a scope-confirmation checkpoint
    are structurally identical to satisfied() -- both are just
    status: done + gate_human: true + approved_by_human: true. There is no
    task 'kind'/'type' field involved, so no type-specific branching exists
    to diverge between them."""
    decision_task = {
        "id": "t-011",
        "title": "Decide the commercial-licensing posture for FLUX-dev/Kontext LoRAs",
        "status": "done",
        "approved_by_human": True,
    }
    brief_confirmation_task = {
        "id": "t-002",
        "title": "Confirm scope before building",
        "status": "done",
        "gate_human": True,
        "approved_by_human": True,
    }
    assert resolve_deps.satisfied(decision_task) is True
    assert resolve_deps.satisfied(brief_confirmation_task) is True


def test_satisfied_approved_without_gate_human_still_satisfied():
    # t-011 in the real roadmap carries approved_by_human: true without
    # gate_human -- satisfied() must not require gate_human to be present.
    assert (
        resolve_deps.satisfied({"status": "done", "approved_by_human": True}) is True
    )


# ---------------------------------------------------------------------------
# main() -- end-to-end promotion of a waiting task once its dependency
# (recorded either as a decision or a brief-confirmation gate) resolves.
# ---------------------------------------------------------------------------


def write_roadmap(tmp_path: Path, project: str, roadmap: dict) -> Path:
    path = tmp_path / "projects" / project / "roadmap.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(roadmap, sort_keys=False), encoding="utf-8")
    return path


def run_cli(tmp_path: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )


def test_main_promotes_waiting_task_on_decision_style_gate(tmp_path: Path):
    roadmap = {
        "project": "demo",
        "tasks": [
            {
                "id": "t-011",
                "title": "Licensing decision",
                "status": "done",
                "approved_by_human": True,
            },
            {
                "id": "t-012",
                "title": "Depends on the decision",
                "status": "waiting",
                "depends_on": "t-011",
            },
        ],
    }
    path = write_roadmap(tmp_path, "demo", roadmap)

    result = run_cli(tmp_path)
    assert result.returncode == 0
    assert "unblocked t-012" in result.stdout

    updated = yaml.safe_load(path.read_text())
    task = next(t for t in updated["tasks"] if t["id"] == "t-012")
    assert task["status"] == "ready"


def test_main_promotes_waiting_task_on_brief_confirmation_gate(tmp_path: Path):
    roadmap = {
        "project": "demo",
        "tasks": [
            {
                "id": "t-001",
                "title": "Scope confirmation",
                "status": "done",
                "gate_human": True,
                "approved_by_human": True,
            },
            {
                "id": "t-002",
                "title": "Depends on scope confirmation",
                "status": "waiting",
                "depends_on": ["t-001"],
            },
        ],
    }
    path = write_roadmap(tmp_path, "demo", roadmap)

    run_cli(tmp_path)

    updated = yaml.safe_load(path.read_text())
    task = next(t for t in updated["tasks"] if t["id"] == "t-002")
    assert task["status"] == "ready"


def test_main_leaves_waiting_when_gate_human_not_approved(tmp_path: Path):
    roadmap = {
        "project": "demo",
        "tasks": [
            {"id": "t-001", "title": "Gated", "status": "done", "gate_human": True},
            {
                "id": "t-002",
                "title": "Depends on unapproved gate",
                "status": "waiting",
                "depends_on": "t-001",
            },
        ],
    }
    path = write_roadmap(tmp_path, "demo", roadmap)

    result = run_cli(tmp_path)

    updated = yaml.safe_load(path.read_text())
    task = next(t for t in updated["tasks"] if t["id"] == "t-002")
    assert task["status"] == "waiting"
    assert "No tasks to unblock." in result.stdout


def test_main_requires_all_deps_satisfied(tmp_path: Path):
    roadmap = {
        "project": "demo",
        "tasks": [
            {"id": "t-001", "title": "Done", "status": "done"},
            {"id": "t-002", "title": "Still working", "status": "claimed"},
            {
                "id": "t-003",
                "title": "Depends on both",
                "status": "waiting",
                "depends_on": ["t-001", "t-002"],
            },
        ],
    }
    path = write_roadmap(tmp_path, "demo", roadmap)

    run_cli(tmp_path)

    updated = yaml.safe_load(path.read_text())
    task = next(t for t in updated["tasks"] if t["id"] == "t-003")
    assert task["status"] == "waiting"


def test_main_dry_run_does_not_write(tmp_path: Path):
    roadmap = {
        "project": "demo",
        "tasks": [
            {"id": "t-001", "title": "Done", "status": "done"},
            {
                "id": "t-002",
                "title": "Depends on t-001",
                "status": "waiting",
                "depends_on": "t-001",
            },
        ],
    }
    path = write_roadmap(tmp_path, "demo", roadmap)
    before = path.read_text()

    result = run_cli(tmp_path, "--dry-run")
    assert "unblocked t-002" in result.stdout
    assert path.read_text() == before


def test_main_skips_template_project(tmp_path: Path):
    roadmap = {
        "project": "_template",
        "tasks": [
            {"id": "t-001", "title": "Done", "status": "done"},
            {
                "id": "t-002",
                "title": "Depends on t-001",
                "status": "waiting",
                "depends_on": "t-001",
            },
        ],
    }
    path = write_roadmap(tmp_path, "_template", roadmap)

    run_cli(tmp_path)

    updated = yaml.safe_load(path.read_text())
    task = next(t for t in updated["tasks"] if t["id"] == "t-002")
    assert task["status"] == "waiting"
