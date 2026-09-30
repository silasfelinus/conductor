"""Guards for the 2026-09-30 token-essentialization pass.

AGENTS.md was split into a core file plus on-demand docs; these tests keep the
pointers honest so a session told to "load only your playbook" can find it,
and keep show_task.py's line-oriented parser in agreement with PyYAML.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import select_role  # noqa: E402


def test_every_role_playbook_exists():
    for role, path in select_role.ROLE_PLAYBOOKS.items():
        if path is not None:
            assert (ROOT / path).is_file(), f"{role} -> missing {path}"


def test_agents_md_links_resolve():
    text = (ROOT / "AGENTS.md").read_text() + (ROOT / "CLAUDE.md").read_text()
    for rel in (
        "docs/agents/roles/worker.md",
        "docs/agents/roles/reviewer.md",
        "docs/agents/frontend-verification.md",
        "docs/agents/git-troubleshooting.md",
        "docs/sweep-checks.md",
    ):
        assert rel in text
        assert (ROOT / rel).is_file(), rel


@pytest.mark.parametrize("project", ["conductor", "kind-robots"])
def test_show_task_list_matches_yaml(project):
    yaml = pytest.importorskip("yaml")
    path = ROOT / "projects" / project / "roadmap.yaml"
    if not path.is_file():
        pytest.skip(f"no roadmap for {project}")
    data = yaml.safe_load(path.read_text()) or {}
    expected = [(str(t["id"]), str(t.get("status"))) for t in data.get("tasks") or []]
    out = subprocess.run(
        [sys.executable, "scripts/show_task.py", project, "--list"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout
    got = [tuple(line.split()[:2]) for line in out.splitlines()]
    assert got == expected


def test_show_task_single_and_no_note():
    yaml = pytest.importorskip("yaml")
    data = yaml.safe_load((ROOT / "projects/conductor/roadmap.yaml").read_text())
    task = data["tasks"][0]
    tid = str(task["id"])
    full = subprocess.run(
        [sys.executable, "scripts/show_task.py", f"conductor/{tid}"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout
    parsed = yaml.safe_load(full)[0]
    assert parsed["id"] == task["id"] and parsed.get("note") == task.get("note")
    trimmed = subprocess.run(
        [sys.executable, "scripts/show_task.py", "conductor", tid, "--no-note"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout
    assert len(trimmed) <= len(full)
    assert yaml.safe_load(trimmed)[0]["title"] == task["title"]


def test_session_sweep_offline_runs():
    proc = subprocess.run(
        [sys.executable, "scripts/session_sweep.py", "--skip-network",
         "--only", "check_milestone_status_drift,check_recurring_claim_drift"],
        cwd=ROOT, capture_output=True, text=True, timeout=120,
    )
    assert proc.returncode in (0, 1)
    assert "check_milestone_status_drift" in proc.stdout
    assert "check_recurring_claim_drift" in proc.stdout
