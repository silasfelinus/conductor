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


# --- Recurring no-op backoff (close_task.py --noop, roadmap_claims.task_is_resting) ---

from datetime import datetime, timedelta, timezone  # noqa: E402

import close_task  # noqa: E402
import roadmap_claims  # noqa: E402
import run_worker  # noqa: E402

NOW = datetime(2026, 9, 30, 6, 0, tzinfo=timezone.utc)


def test_noop_backoff_schedule_and_cap():
    assert [roadmap_claims.noop_rest_hours(n) for n in (1, 2, 3, 4, 5, 9)] == [2, 6, 12, 24, 48, 48]
    assert roadmap_claims.noop_rest_hours(5, max_hours=6) == 6


def test_resting_task_is_not_claimable_until_rest_ends():
    task = {"status": "ready", "recurring": True, "rest_until": "2026-09-30T08:00:00Z"}
    assert not roadmap_claims.task_is_claimable(task, now=NOW)
    assert roadmap_claims.task_is_claimable(task, now=NOW + timedelta(hours=2, minutes=1))
    # A garbage timestamp never locks a task.
    assert roadmap_claims.task_is_claimable({"status": "ready", "rest_until": "soon"}, now=NOW)


def test_run_worker_skips_resting_task():
    roadmaps = [{
        "_project": "demo", "_path": "x", "_lifecycle": "active",
        "tasks": [
            {"id": "t-001", "status": "ready", "recurring": True, "rest_until": "2026-09-30T08:00:00Z"},
            {"id": "t-002", "status": "ready"},
        ],
    }]
    picked = run_worker.find_ready_task(["demo"], roadmaps, now=NOW)
    assert picked["task_id"] == "t-002"


def test_close_task_noop_fields_grow_then_reset():
    task = {"recurring": True, "noop_streak": 2}
    fields = close_task.rest_fields(task, "ready", True, now=NOW)
    assert fields == {"noop_streak": "3", "rest_until": "2026-09-30T18:00:00Z"}
    assert close_task.rest_fields({"recurring": True, "noop_streak": 3}, "ready", False) == {
        "noop_streak": "0", "rest_until": "null"}
    assert close_task.rest_fields({"recurring": True}, "ready", False) == {}


@pytest.mark.parametrize("task,status", [
    ({"recurring": False}, "ready"),
    ({"recurring": True}, "needs-human"),
    ({"recurring": True, "daily_commitment": True}, "ready"),
])
def test_close_task_noop_refuses_wrong_shapes(task, status):
    with pytest.raises(close_task.CloseError):
        close_task.rest_fields(task, status, True, now=NOW)


def test_close_task_noop_writes_valid_roadmap_fields():
    yaml = pytest.importorskip("yaml")
    text = (
        "project: demo\nkind: software\ntasks:\n"
        "  - id: t-001\n    title: demo\n    status: claimed\n    recurring: true\n"
        "    note: first cycle\n"
    )
    fields = close_task.rest_fields({"recurring": True}, "ready", True, now=NOW)
    out = close_task.apply_close(text, "t-001", "ready", fields, "no-op cycle", False)
    task = yaml.safe_load(out)["tasks"][0]
    assert task["status"] == "ready" and task["noop_streak"] == 1
    assert not roadmap_claims.task_is_claimable(task, now=NOW)


# --- archive_recurring_task_note.py: rounds, auto-pointer, signal guard ---

import archive_recurring_task_note as archiver  # noqa: E402


def _daily_note() -> str:
    spec = "Standing contract: ship one thing per Pacific calendar day. Keep it small."
    middle = "\n\n".join(f"Cycle {i}: did a thing on 2026-08-{i:02d} Pacific. RAN 2026-08-{i:02d} filler." for i in range(1, 29))
    latest_mid = "Out-of-order entry: shipped on 2026-09-27 Pacific per the contract."
    tail = "\n\n".join(f"Recent cycle {i}: NO-OP 2026-09-{i:02d} nothing to do." for i in range(10, 13))
    return "\n\n".join([spec, middle, latest_mid, tail])


def test_auto_pointer_keeps_spec_latest_signals_and_shrinks():
    note = _daily_note()
    pointer = archiver.auto_pointer(note, "projects/x/T001-HISTORY.md", 200, 150)
    assert len(pointer) < len(note) / 3
    assert pointer.startswith("Standing contract:")
    assert "projects/x/T001-HISTORY.md" in pointer
    assert archiver.parsed_signals(pointer) == archiver.parsed_signals(note)


def test_hard_wrapped_note_splits_on_blank_lines_only():
    note = "First sentence of the spec wraps\nonto a second line. Done.\n\nSecond para."
    assert archiver._paragraphs(note)[0].endswith("Done.")


def test_archiver_appends_round_and_guards_signals(tmp_path, monkeypatch):
    yaml = pytest.importorskip("yaml")
    proj = tmp_path / "projects" / "demo"
    proj.mkdir(parents=True)
    note = _daily_note()
    doc = {"project": "demo", "kind": "software",
           "tasks": [{"id": "t-001", "title": "demo", "status": "ready", "recurring": True, "note": note}]}
    (proj / "roadmap.yaml").write_text(yaml.safe_dump(doc, sort_keys=False, width=100))
    (proj / "T001-HISTORY.md").write_text("# hand archive without markers\n\nold text\n")
    monkeypatch.setattr(archiver, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["x", "demo", "t-001", "--keep-head", "200", "--keep-tail", "150"])
    archiver.main()
    hist = (proj / "T001-HISTORY.md").read_text()
    assert hist.startswith("# hand archive without markers\n\nold text\n")  # earlier round untouched
    assert archiver.extract_note(hist, "t-001", 2) == note + "\n"
    new_note = yaml.safe_load((proj / "roadmap.yaml").read_text())["tasks"][0]["note"]
    assert len(new_note) < len(note)
    assert archiver.parsed_signals(new_note) == archiver.parsed_signals(note)
