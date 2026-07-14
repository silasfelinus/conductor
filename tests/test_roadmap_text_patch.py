"""Regression coverage for scripts/roadmap_text_patch.py.

conductor/challenge-center t-020: scripts/process_task_events.py and
resolve_deps.py used to reserialize the *entire* roadmap with yaml.safe_dump
for a one-task status change -- hundreds of unrelated changed lines, escaped
readable Unicode, and reformatted quote/block styles. These tests assert the
surgical patcher instead produces a status/note-sized diff and leaves every
byte outside the touched task untouched, using a fixture copied from the real
Challenge Center roadmap (tests/fixtures/challenge_center_roadmap.yaml) so the
coverage matches production-shaped content: long notes, Unicode arrows and em
dashes, quoted values, block scalars, and depends_on lists.
"""

from pathlib import Path

import pytest
import yaml

from scripts.roadmap_text_patch import (
    apply_task_field_ops,
    set_multiline_task_field_text,
    stf,
    unset_task_field_text,
)


FIXTURE = (Path(__file__).parent / "fixtures" / "challenge_center_roadmap.yaml").read_text(
    encoding="utf-8"
)


def parse_tasks(text: str) -> dict:
    data = yaml.safe_load(text)
    return {task["id"]: task for task in data["tasks"]}


def task_block_lines(text: str, task_id: str) -> list[str]:
    lines = text.splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() == f"- id: {task_id}")
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("- id:"):
            end = i
            break
    return lines[start:end]


# ---------------------------------------------------------------------------
# A claim-shaped event (status + owner + updated) touches only its own task.
# ---------------------------------------------------------------------------


def test_claim_event_only_changes_status_owner_updated_lines():
    # t-020 already carries status/owner/updated fields, so a claim event replaces
    # each in place -- no new lines, exactly those three lines change.
    ops = [
        ("set", "status", "claimed"),
        ("set", "owner", "worker"),
        ("set", "updated", "2026-07-14T23:10:00+00:00"),
    ]
    out = apply_task_field_ops(FIXTURE, "t-020", ops)

    tasks = parse_tasks(out)
    assert tasks["t-020"]["status"] == "claimed"
    assert tasks["t-020"]["owner"] == "worker"

    before_lines = FIXTURE.splitlines()
    after_lines = out.splitlines()
    assert len(after_lines) == len(before_lines)
    diff_idx = [i for i, (a, b) in enumerate(zip(before_lines, after_lines)) if a != b]
    assert len(diff_idx) == 3
    changed = {after_lines[i].strip() for i in diff_idx}
    assert changed == {
        "status: claimed",
        "owner: worker",
        "updated: '2026-07-14T23:10:00+00:00'",
    }


def test_claim_event_leaves_every_other_task_byte_identical():
    ops = [("set", "status", "claimed"), ("set", "owner", "worker")]
    out = apply_task_field_ops(FIXTURE, "t-020", ops)

    for task_id in ("t-001", "t-002", "t-003", "t-014", "t-019"):
        assert task_block_lines(out, task_id) == task_block_lines(FIXTURE, task_id), task_id


def test_done_event_note_preserves_unicode_literally_not_escaped():
    note = "Closed — confirmed the arrows (→) render fine end to end."
    out = apply_task_field_ops(FIXTURE, "t-020", [("set", "status", "done"), ("set", "note", note)])

    tasks = parse_tasks(out)
    assert tasks["t-020"]["note"] == note

    # The fixture's *other* fields already contain legacy \u-escaped text from a
    # prior yaml.safe_dump -- scope the "not escaped" assertion to the new note
    # line itself, not the whole document.
    note_line = next(line for line in out.splitlines() if "Closed" in line)
    assert "—" in note_line and "→" in note_line
    assert "\\u2014" not in note_line and "\\u2192" not in note_line


def test_multiline_note_keeps_paragraph_breaks_as_literal_block():
    note = "Paragraph one.\n\nParagraph two, second sentence."
    out = set_multiline_task_field_text(FIXTURE, "t-020", "note", note)

    assert "note: |-" in out
    tasks = parse_tasks(out)
    assert tasks["t-020"]["note"] == note
    # Untouched neighbor tasks stay byte-identical even though t-020 gained lines.
    assert task_block_lines(out, "t-019") == task_block_lines(FIXTURE, "t-019")


def test_multiline_note_replaces_existing_multiline_note_cleanly():
    # t-001 already carries a long double-quoted, backslash-continued note.
    note = "Replacement note.\n\nWith a second paragraph."
    out = set_multiline_task_field_text(FIXTURE, "t-001", "note", note)

    tasks = parse_tasks(out)
    assert tasks["t-001"]["note"] == note
    assert "Unblocks t-002" not in out  # old note content is gone, not appended alongside
    # Sibling fields on the same task (status, gate_human, ...) survive untouched.
    assert tasks["t-001"]["status"] == "done"
    assert tasks["t-001"]["gate_human"] is True


# ---------------------------------------------------------------------------
# unset / owner-removal
# ---------------------------------------------------------------------------


def test_unset_removes_owner_field_cleanly():
    out = unset_task_field_text(FIXTURE, "t-019", "owner")
    tasks = parse_tasks(out)
    assert "owner" not in tasks["t-019"]
    assert tasks["t-019"]["status"] == "claimed"  # sibling field untouched


def test_unset_missing_field_is_a_pure_noop():
    out = unset_task_field_text(FIXTURE, "t-020", "claimed_by")  # t-020 has no claimed_by
    assert out == FIXTURE


def test_apply_ops_set_then_unset_in_one_pass():
    out = apply_task_field_ops(
        FIXTURE,
        "t-019",
        [("set", "status", "ready"), ("unset", "owner", None), ("unset", "soft_gate", None)],
    )
    tasks = parse_tasks(out)
    assert tasks["t-019"]["status"] == "ready"
    assert "owner" not in tasks["t-019"]


# ---------------------------------------------------------------------------
# Idempotency: re-applying the identical op set produces zero further diff.
# ---------------------------------------------------------------------------


def test_reapplying_same_ops_is_a_noop_second_time():
    once = apply_task_field_ops(FIXTURE, "t-020", [("set", "status", "claimed")])
    twice = apply_task_field_ops(once, "t-020", [("set", "status", "claimed")])
    assert once == twice


def test_unknown_task_raises():
    with pytest.raises(stf.TaskFieldError, match="t-999"):
        apply_task_field_ops(FIXTURE, "t-999", [("set", "status", "done")])
