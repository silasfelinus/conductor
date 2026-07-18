import subprocess
import sys
from pathlib import Path

import pytest
import yaml

import scripts.set_task_field as stf


SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "set_task_field.py"

# Mirrors the shapes that appear in real roadmaps: a quoted multiline note with a
# blank line inside the quotes (t-001 style), a folded `note: >` block (t-016 style),
# a depends_on block list, and blank-line separators between tasks.
ROADMAP = """\
project: demo
kind: software
milestones:
- id: m1
  title: First milestone
  status: not-started
tasks:
- id: t-001
  milestone: m1
  title: Task with quoted multiline note
  status: ready
  passes: 0
  note: 'Multi-line quoted note.
    More detail here.

    '
- id: t-002
  milestone: m1
  title: Task with folded note
  status: done
  depends_on:
  - t-001
  - t-003
  note: >
    Folded note line one.
    Folded note line two.

- id: t-003
  milestone: m1
  title: Plain task
  status: ready
  passes: 2
- id: t-004
  milestone: m1
  title: Recurring task with hand-maintained block-literal note
  status: ready
  passes: 0
  note: |-
    RAN 2026-07-01: first cycle paragraph.

    RAN 2026-07-08: second cycle paragraph.
"""


def parse_tasks(text: str) -> dict:
    data = yaml.safe_load(text)
    return {task["id"]: task for task in data["tasks"]}


def task_block(text: str, task_id: str) -> str:
    lines = text.splitlines(keepends=True)
    start, end, _ = stf.find_task_block(lines, task_id)
    return "".join(lines[start:end])


def test_set_status_updates_only_that_field():
    out = stf.set_task_field_text(ROADMAP, "t-003", "status", "claimed")
    tasks = parse_tasks(out)
    assert tasks["t-003"]["status"] == "claimed"
    assert tasks["t-003"]["passes"] == 2
    assert tasks["t-003"]["title"] == "Plain task"


def test_unrelated_tasks_are_byte_identical():
    out = stf.set_task_field_text(ROADMAP, "t-003", "status", "claimed")
    assert task_block(out, "t-001") == task_block(ROADMAP, "t-001")
    assert task_block(out, "t-002") == task_block(ROADMAP, "t-002")
    # Only one line differs in the whole document.
    before_lines = ROADMAP.splitlines()
    after_lines = out.splitlines()
    assert len(before_lines) == len(after_lines)
    diff = [i for i, (a, b) in enumerate(zip(before_lines, after_lines)) if a != b]
    assert len(diff) == 1
    assert after_lines[diff[0]] == "  status: claimed"


def test_add_missing_field_lands_outside_multiline_note():
    # t-001's note is a quoted scalar with a blank line inside it; the new field
    # must not be inserted into the middle of that value.
    out = stf.set_task_field_text(ROADMAP, "t-001", "approved_by_human", "true")
    tasks = parse_tasks(out)
    assert tasks["t-001"]["approved_by_human"] is True
    assert "approved_by_human" not in tasks["t-001"]["note"]
    assert tasks["t-001"]["note"].startswith("Multi-line quoted note.")
    assert task_block(out, "t-002") == task_block(ROADMAP, "t-002")


def test_claim_fields_are_allowed_and_land_outside_note():
    # claimed_by/claimed_at back conductor/t-040's claim mechanism (claim_task.py).
    out = stf.set_task_field_text(ROADMAP, "t-001", "claimed_by", "reviewer-session-1")
    out = stf.set_task_field_text(out, "t-001", "claimed_at", "2026-07-14T15:00:00Z")
    tasks = parse_tasks(out)
    assert tasks["t-001"]["claimed_by"] == "reviewer-session-1"
    assert tasks["t-001"]["claimed_at"] == "2026-07-14T15:00:00Z"
    assert "claimed_by" not in tasks["t-001"]["note"]
    assert tasks["t-001"]["note"].startswith("Multi-line quoted note.")


def test_replace_folded_note_removes_old_block():
    out = stf.set_task_field_text(ROADMAP, "t-002", "note", "Short replacement note")
    tasks = parse_tasks(out)  # would raise if the edit left invalid YAML behind
    assert tasks["t-002"]["note"] == "Short replacement note"
    assert "Folded note line one." not in out
    assert tasks["t-002"]["depends_on"] == ["t-001", "t-003"]


def test_multiline_note_preserves_existing_block_literal_style():
    # conductor/t-064: appending a new paragraph to an existing `note: |-` block
    # must stay a block-literal scalar, not collapse to one quoted flow line.
    existing = parse_tasks(ROADMAP)["t-004"]["note"]
    new_value = existing + "\n\nRAN 2026-07-15: third cycle paragraph."
    out = stf.set_task_field_text(ROADMAP, "t-004", "note", new_value)

    block = task_block(out, "t-004")
    assert "note: |-" in block
    assert "note: '" not in block  # did not collapse to a quoted flow scalar

    tasks = parse_tasks(out)
    assert tasks["t-004"]["note"] == new_value
    assert "RAN 2026-07-01" in tasks["t-004"]["note"]
    assert "RAN 2026-07-15" in tasks["t-004"]["note"]
    # Other tasks/fields untouched.
    assert task_block(out, "t-002") == task_block(ROADMAP, "t-002")
    assert tasks["t-004"]["status"] == "ready"


def test_multiline_note_without_existing_block_style_still_flattens():
    # No prior block-literal to preserve (t-001's note is a quoted scalar) —
    # behavior is unchanged: newlines flatten to spaces as documented.
    out = stf.set_task_field_text(ROADMAP, "t-001", "note", "line one\nline two")
    tasks = parse_tasks(out)
    assert tasks["t-001"]["note"] == "line one line two"


def test_replace_depends_on_list_removes_old_items():
    out = stf.set_task_field_text(ROADMAP, "t-002", "depends_on", "t-001")
    tasks = parse_tasks(out)
    assert tasks["t-002"]["depends_on"] == "t-001"
    assert tasks["t-002"]["note"].startswith("Folded note line one.")


def test_missing_task_fails_clearly():
    with pytest.raises(stf.TaskFieldError, match="t-999"):
        stf.set_task_field_text(ROADMAP, "t-999", "status", "done")


def test_disallowed_field_is_rejected():
    with pytest.raises(stf.TaskFieldError, match="not allowed"):
        stf.set_task_field_text(ROADMAP, "t-001", "title", "sneaky rename")


def test_scalar_normalization():
    assert stf.normalize_scalar("true") == "true"
    assert stf.normalize_scalar("null") == "null"
    assert stf.normalize_scalar("3") == "3"
    assert stf.normalize_scalar("worker") == "worker"
    # YAML 1.1 bool words stay strings.
    assert stf.normalize_scalar("yes") == "'yes'"
    # Free text gets quoted, quotes escaped, newlines flattened.
    assert stf.normalize_scalar("it's done\nfor real") == "'it''s done for real'"
    # `now` renders a quoted UTC timestamp.
    rendered = stf.normalize_scalar("now")
    assert rendered.startswith("'") and rendered.endswith("Z'")


def write_demo_repo(tmp_path: Path) -> Path:
    roadmap = tmp_path / "projects" / "demo" / "roadmap.yaml"
    roadmap.parent.mkdir(parents=True)
    roadmap.write_text(ROADMAP, encoding="utf-8")
    return roadmap


def run_cli(tmp_path: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )


def test_cli_sets_status_and_reports(tmp_path: Path):
    roadmap = write_demo_repo(tmp_path)
    result = run_cli(tmp_path, "demo", "t-003", "status", "done")
    assert result.returncode == 0, result.stderr
    assert "Updated" in result.stdout
    assert parse_tasks(roadmap.read_text())["t-003"]["status"] == "done"


def test_cli_dry_run_prints_diff_without_writing(tmp_path: Path):
    roadmap = write_demo_repo(tmp_path)
    result = run_cli(tmp_path, "demo", "t-003", "status", "done", "--dry-run")
    assert result.returncode == 0, result.stderr
    assert "-  status: ready" in result.stdout
    assert "+  status: done" in result.stdout
    assert roadmap.read_text() == ROADMAP


def test_cli_missing_roadmap_fails_clearly(tmp_path: Path):
    (tmp_path / "projects").mkdir()
    result = run_cli(tmp_path, "nope", "t-001", "status", "done")
    assert result.returncode == 1
    assert "Roadmap not found" in result.stderr


def test_cli_missing_task_fails_clearly(tmp_path: Path):
    write_demo_repo(tmp_path)
    result = run_cli(tmp_path, "demo", "t-999", "status", "done")
    assert result.returncode == 1
    assert "not found" in result.stderr


def test_cli_no_change_is_a_noop(tmp_path: Path):
    roadmap = write_demo_repo(tmp_path)
    result = run_cli(tmp_path, "demo", "t-003", "status", "ready")
    assert result.returncode == 0, result.stderr
    assert "No change." in result.stdout
    assert roadmap.read_text() == ROADMAP


def test_verify_result_rejects_swallowed_field():
    # Simulates the pre-fix failure mode: the field text ends up inside a quoted
    # note value instead of becoming a real mapping key.
    corrupted = ROADMAP.replace(
        "    More detail here.",
        "    More detail here.\n  approved_by_human: true",
    )
    # That text parses, but approved_by_human is part of the note string.
    with pytest.raises(stf.TaskFieldError, match="did not take"):
        stf.verify_result(corrupted, "t-001", "approved_by_human")


def test_real_conductor_roadmap_roundtrip():
    # Exercise against the actual repo roadmap this tool exists to edit.
    real = (Path(__file__).resolve().parent.parent / "projects" / "conductor" / "roadmap.yaml").read_text()
    out = stf.set_task_field_text(real, "t-016", "note", "Replaced for test purposes")
    data = yaml.safe_load(out)
    t016 = [t for t in data["tasks"] if t["id"] == "t-016"][0]
    assert t016["note"] == "Replaced for test purposes"
    out2 = stf.set_task_field_text(real, "t-001", "approved_by_human", "true")
    data2 = yaml.safe_load(out2)
    t001 = [t for t in data2["tasks"] if t["id"] == "t-001"][0]
    assert t001["approved_by_human"] is True
    assert "approved_by_human" not in t001["note"]
