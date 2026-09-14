"""Tests for scripts/archive_done_task_notes.py (conductor/t-158).

The script moves done-task `note:` prose into projects/<slug>/HISTORY.md. Its
licence to do that is AGENTS.md's archival carve-out, which permits the move
ONLY when it is verified byte-for-byte. These tests pin that property and the
two live consumers of the rewritten field, because a regression in either is
silent: a mangled archive still parses, and a changed lesson still records.

No network, no real roadmaps.
"""

import textwrap

import pytest

import scripts.archive_done_task_notes as archiver
from scripts.backfill_learning import first_sentence


def test_render_history_round_trips_every_note_byte_for_byte():
    """The core safety property the carve-out is conditioned on."""
    awkward = [
        ("t-001", "plain", "A simple note.\n"),
        ("t-002", "blank lines", "First para.\n\nSecond para.\n\n\nThird.\n"),
        ("t-003", "markdown headings", "## Not a task heading\n\n- bullet\n- bullet\n"),
        ("t-004", "yaml-ish", "key: value\n  nested: true\n- item\n"),
        ("t-005", "unicode", "Café — naïve — 日本語 — 🎲 emoji.\n"),
        ("t-006", "trailing space", "Note with trailing space   \nand a second line.\n"),
        ("t-007", "code fence", "```python\nprint('hi')\n```\n"),
        ("t-008", "html comment", "<!-- an ordinary comment -->\ntext after.\n"),
    ]
    text = archiver.render_history("demo", awkward)
    recovered = archiver.extract_notes(text)

    assert set(recovered) == {tid for tid, _, _ in awkward}
    for task_id, _, note in awkward:
        assert recovered[task_id] == note, f"{task_id} did not round-trip"


def test_extract_notes_is_not_confused_by_a_later_entry():
    text = archiver.render_history(
        "demo",
        [("t-001", "a", "one\n"), ("t-002", "b", "two\n"), ("t-003", "c", "three\n")],
    )
    assert archiver.extract_notes(text) == {"t-001": "one\n", "t-002": "two\n", "t-003": "three\n"}


@pytest.mark.parametrize(
    "note",
    [
        "Short first sentence. Then a long tail that goes on and on about details.",
        # No sentence boundary at all -> first_sentence falls back to a raw
        # 280-char truncation, which is exactly where the pointer text can bleed
        # into the window and change the recorded lesson.
        "no terminator here just a very long run-on " + ("word " * 80),
        "Ends with a question? And continues afterward with more prose.",
        "Refs like #1234 and paths like scripts/x.py and e.g. abbreviations. Then more.",
        "Version 1.2.3 shipped. Second sentence follows here.",
    ],
)
def test_pointer_preserves_the_backfill_learning_lesson_exactly(note):
    """scripts/backfill_learning.py:276 records first_sentence(note) as the lesson
    for a closed task. The pointer must reproduce it byte-for-byte, or archiving
    silently rewrites history records."""
    pointer = archiver.build_pointer("demo", "t-042", note)
    assert pointer is not None
    assert first_sentence(pointer) == first_sentence(note)


def test_pointer_references_its_own_task_and_project():
    pointer = archiver.build_pointer("demo", "t-042", "A note that is long enough. More text.")
    assert "projects/demo/HISTORY.md#t-042" in pointer


def test_build_pointer_declines_rather_than_corrupting_a_lesson(monkeypatch):
    """If the lesson cannot be reproduced, the task must be left alone. Shrinking
    the payload is never worth a silently altered record."""
    # A splitter that always swallows the whole field: the pointer text is then
    # part of the "lesson", so no summary can reproduce the original and the
    # script must decline. (A constant stub would match trivially on both sides.)
    monkeypatch.setattr(archiver, "first_sentence", lambda text: text)
    assert archiver.build_pointer("demo", "t-042", "some note") is None


def test_has_pointer_matches_only_this_tasks_own_pointer():
    """conductor/t-158's own note quotes the pointer format as example text; a
    loose `HISTORY.md#` search reported it as an unresolvable pointer."""
    quoting = "Write pointers like projects/kind-robots/HISTORY.md#t-101 in the roadmap."
    assert not archiver.has_pointer("conductor", "t-158", quoting)

    real = "Summary.\n\nFull history: projects/conductor/HISTORY.md#t-158"
    assert archiver.has_pointer("conductor", "t-158", real)
    assert not archiver.has_pointer("conductor", "t-999", real)


def write_roadmap(root, slug, content):
    project_dir = root / "projects" / slug
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "roadmap.yaml").write_text(textwrap.dedent(content), encoding="utf-8")


def test_archivable_tasks_scope(tmp_path, monkeypatch):
    """Done tasks only, over the size floor, not already archived. Recurring,
    needs-human and claimed tasks are read by select_role.py / daily_gate.py /
    audit_human_gates.py, which scan note text."""
    big = "x" * 1000
    data = {
        "tasks": [
            {"id": "t-001", "status": "done", "note": big},
            {"id": "t-002", "status": "ready", "note": big},
            {"id": "t-003", "status": "needs-human", "note": big},
            {"id": "t-004", "status": "claimed", "note": big},
            {"id": "t-005", "status": "done", "recurring": True, "note": big},
            {"id": "t-006", "status": "done", "note": "tiny"},
            {"id": "t-007", "status": "done", "note": None},
            {"id": "t-008", "status": "done", "note": ["a", "list"]},
            {
                "id": "t-009",
                "status": "done",
                "note": big + "\n\nFull history: projects/demo/HISTORY.md#t-009",
            },
        ]
    }
    picked = [t["id"] for t in archiver.archivable_tasks("demo", data)]
    # t-005 is done AND recurring: done is what the note-scanners key off, so it
    # is in scope; t-009 is already archived, the rest are excluded by status,
    # size or note shape.
    assert picked == ["t-001", "t-005"]


def test_archive_project_is_idempotent_and_verifiable(tmp_path, monkeypatch):
    monkeypatch.setattr(archiver, "ROOT", tmp_path)
    note = "First sentence of the note. " + ("padding text " * 60)
    write_roadmap(
        tmp_path,
        "demo",
        f"""\
        tasks:
        - id: t-001
          status: done
          title: A done task
          note: >-
            {note}
        """,
    )

    first = archiver.archive_project("demo")
    assert first["archived"] == ["t-001"]
    assert first["failed"] == []
    assert first["bytes_after"] < first["bytes_before"]
    assert archiver.verify_project("demo") == []

    second = archiver.archive_project("demo")
    assert second["archived"] == [], "re-running must be a no-op"
    assert second["bytes_after"] == second["bytes_before"]


def test_archive_refuses_a_note_containing_an_archive_marker(tmp_path, monkeypatch):
    """A note carrying the delimiter would make extraction ambiguous, so the
    script reports it rather than guessing."""
    monkeypatch.setattr(archiver, "ROOT", tmp_path)
    hostile = "Sentence one. <!-- note:end t-001 --> " + ("filler " * 80)
    write_roadmap(
        tmp_path,
        "demo",
        f"""\
        tasks:
        - id: t-001
          status: done
          title: Hostile
          note: >-
            {hostile}
        """,
    )
    result = archiver.archive_project("demo")
    assert result["archived"] == []
    assert result["failed"] and "marker" in result["failed"][0][1]
