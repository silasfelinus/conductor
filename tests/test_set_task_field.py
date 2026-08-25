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


def test_implementation_pr_field_is_allowed_and_round_trips(tmp_path):
    # conductor/t-099: close_task.py's --implementation-pr writes this field
    # directly. It must be allowed, and a value containing `#` (owner/repo#N)
    # must survive quoted so no YAML parser reads it as a comment.
    out = stf.set_task_field_text(
        ROADMAP, "t-001", "implementation_pr", "silasfelinus/kind_robots#1464"
    )
    tasks = parse_tasks(out)
    assert tasks["t-001"]["implementation_pr"] == "silasfelinus/kind_robots#1464"


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


LONG_NOTE_ROADMAP = """\
project: demo
kind: software
tasks:
- id: t-010
  milestone: m1
  title: Task with a long quoted note
  status: ready
  passes: 0
  note: 'CORRECTION 2026-08-01: first theory was wrong, evidence was X.

    RESOLVED TO TWO SEPARATE CAUSES: root cause A affects the claim path, root
    cause B affects the close-out path, found via git log -p over roadmap.yaml.

    ROOT CAUSE FOUND: A is the actual bug, B is a red herring from a stale
    checkout in the reproduction session.'
- id: t-011
  milestone: m1
  title: Task with a short note
  status: ready
  passes: 0
  note: 'Short note, well under the guard threshold.'
- id: t-012
  milestone: m1
  title: Task with no note
  status: ready
  passes: 0
"""


def test_set_note_guard_blocks_destructive_replace():
    # conductor/t-129: a --set note=... that would delete substantial existing
    # note content is refused by default.
    with pytest.raises(stf.TaskFieldError, match="Refusing to replace"):
        stf.set_task_field_text(LONG_NOTE_ROADMAP, "t-010", "note", "RESOLVED, short summary.")


def test_set_note_guard_names_append_note_and_force_in_error():
    with pytest.raises(stf.TaskFieldError, match="append_note_text.*--append-note"):
        stf.set_task_field_text(LONG_NOTE_ROADMAP, "t-010", "note", "RESOLVED, short summary.")
    with pytest.raises(stf.TaskFieldError, match="force=True"):
        stf.set_task_field_text(LONG_NOTE_ROADMAP, "t-010", "note", "RESOLVED, short summary.")


def test_set_note_guard_force_allows_replace():
    out = stf.set_task_field_text(
        LONG_NOTE_ROADMAP, "t-010", "note", "RESOLVED, short summary.", force=True
    )
    tasks = parse_tasks(out)
    assert tasks["t-010"]["note"] == "RESOLVED, short summary."


def test_set_note_guard_does_not_fire_under_threshold():
    # t-011's note is short -- no guard, no force needed.
    out = stf.set_task_field_text(LONG_NOTE_ROADMAP, "t-011", "note", "Replaced short note.")
    tasks = parse_tasks(out)
    assert tasks["t-011"]["note"] == "Replaced short note."


def test_set_note_guard_does_not_fire_when_new_value_still_contains_existing():
    # The guard compares the *input* value against the existing raw text, before
    # any flattening set_task_field_text applies on write -- a superset edit like
    # this (existing note plus more) must not raise, even without force.
    existing = stf.get_task_field_value(LONG_NOTE_ROADMAP, "t-010", "note")
    new_value = existing + "\n\nADDENDUM: one more paragraph."
    out = stf.set_task_field_text(LONG_NOTE_ROADMAP, "t-010", "note", new_value)
    tasks = parse_tasks(out)
    assert "ADDENDUM: one more paragraph." in tasks["t-010"]["note"]
    assert "ROOT CAUSE FOUND" in tasks["t-010"]["note"]


def test_set_note_guard_does_not_apply_to_non_note_fields():
    # A long value on any other allowed field is unaffected by the note guard.
    out = stf.set_task_field_text(LONG_NOTE_ROADMAP, "t-010", "status", "done")
    tasks = parse_tasks(out)
    assert tasks["t-010"]["status"] == "done"


def test_get_task_field_value_decodes_quoted_and_missing():
    assert stf.get_task_field_value(LONG_NOTE_ROADMAP, "t-011", "note") == (
        "Short note, well under the guard threshold."
    )
    assert stf.get_task_field_value(LONG_NOTE_ROADMAP, "t-012", "note") is None


def test_get_task_field_value_decodes_block_style():
    # Reuses the folded-note fixture from ROADMAP (t-002).
    value = stf.get_task_field_value(ROADMAP, "t-002", "note")
    assert value == "Folded note line one.\nFolded note line two."


def test_append_note_text_appends_as_new_paragraph_in_block_style():
    out = stf.append_note_text(LONG_NOTE_ROADMAP, "t-011", "New finding: it was a race.")
    tasks = parse_tasks(out)
    # One blank line in the file's folded block == one newline once folded/decoded
    # (YAML folded-scalar semantics), not two -- the file itself still shows a
    # blank line between paragraphs, matching the repo's existing note convention.
    assert tasks["t-011"]["note"] == (
        "Short note, well under the guard threshold.\nNew finding: it was a race."
    )
    block = task_block(out, "t-011")
    assert "note: >" in block
    # Prior content is fully preserved, not truncated, and the file shows the two
    # paragraphs separated by a blank line.
    assert "Short note, well under the guard threshold.\n\n    New finding" in block


def test_append_note_text_on_task_with_no_prior_note():
    out = stf.append_note_text(LONG_NOTE_ROADMAP, "t-012", "First note ever on this task.")
    tasks = parse_tasks(out)
    assert tasks["t-012"]["note"] == "First note ever on this task."


def test_append_note_text_wraps_long_single_line_addition():
    long_addition = "word " * 40  # far past the default width, all one line
    out = stf.append_note_text(LONG_NOTE_ROADMAP, "t-012", long_addition, width=40)
    tasks = parse_tasks(out)
    # Wrapping collapses back to the same words when re-parsed.
    assert tasks["t-012"]["note"].split() == long_addition.split()
    block = task_block(out, "t-012")
    # Actually wrapped onto multiple physical lines in the file.
    content_lines = [
        line for line in block.splitlines() if line.strip() and "note:" not in line
    ]
    assert len(content_lines) > 1


def test_append_note_text_rejects_empty_addition():
    with pytest.raises(stf.TaskFieldError, match="empty"):
        stf.append_note_text(LONG_NOTE_ROADMAP, "t-011", "   ")


def test_append_note_text_never_needs_force_despite_long_existing_note():
    # t-010's note is well over the guard threshold, but append_note_text's
    # combined value always contains it verbatim, so no force is needed.
    out = stf.append_note_text(LONG_NOTE_ROADMAP, "t-010", "One more paragraph.")
    tasks = parse_tasks(out)
    assert tasks["t-010"]["note"].startswith("CORRECTION 2026-08-01")
    assert tasks["t-010"]["note"].endswith("One more paragraph.")


def test_cli_force_flag_bypasses_note_guard(tmp_path: Path):
    roadmap = tmp_path / "projects" / "demo" / "roadmap.yaml"
    roadmap.parent.mkdir(parents=True)
    roadmap.write_text(LONG_NOTE_ROADMAP, encoding="utf-8")

    blocked = run_cli(tmp_path, "demo", "t-010", "note", "Replaced.")
    assert blocked.returncode == 1
    assert "Refusing to replace" in blocked.stderr
    assert roadmap.read_text() == LONG_NOTE_ROADMAP

    forced = run_cli(tmp_path, "demo", "t-010", "note", "Replaced.", "--force")
    assert forced.returncode == 0, forced.stderr
    assert parse_tasks(roadmap.read_text())["t-010"]["note"] == "Replaced."


def test_real_conductor_roadmap_roundtrip():
    # Exercise against the actual repo roadmap this tool exists to edit. t-016's note
    # is well over NOTE_REPLACE_GUARD_CHARS, so this outright replacement needs
    # force=True -- see the destructive-note-replace guard tests below.
    real = (Path(__file__).resolve().parent.parent / "projects" / "conductor" / "roadmap.yaml").read_text()
    out = stf.set_task_field_text(real, "t-016", "note", "Replaced for test purposes", force=True)
    data = yaml.safe_load(out)
    t016 = [t for t in data["tasks"] if t["id"] == "t-016"][0]
    assert t016["note"] == "Replaced for test purposes"
    out2 = stf.set_task_field_text(real, "t-001", "approved_by_human", "true")
    data2 = yaml.safe_load(out2)
    t001 = [t for t in data2["tasks"] if t["id"] == "t-001"][0]
    assert t001["approved_by_human"] is True
    assert "approved_by_human" not in t001["note"]
