import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from repair_duplicate_updated import repair_text

ROADMAP = """tasks:
  - id: t-001
    status: review
    claimed_at: '2026-11-21T00:33:30Z'
    updated: '2026-11-21T00:33:30Z'
    note: |-
      long note
      updated: '1999-01-01T00:00:00Z'
    updated: '2026-11-21T00:21:12Z'
  - id: t-002
    status: done
    updated: '2026-10-01T00:00:00Z'
version: 1
"""


def test_keeps_newest_updated_and_ignores_note_body():
    new, ids = repair_text(ROADMAP)
    assert ids == ["t-001"]
    assert "updated: '2026-11-21T00:33:30Z'" in new
    assert "updated: '2026-11-21T00:21:12Z'" not in new
    assert "      updated: '1999-01-01T00:00:00Z'" in new  # note text untouched
    assert "updated: '2026-10-01T00:00:00Z'" in new


def test_newest_may_be_the_trailing_one():
    text = ROADMAP.replace("00:21:12Z", "05:00:00Z")
    new, ids = repair_text(text)
    assert ids == ["t-001"]
    assert "updated: '2026-11-21T05:00:00Z'" in new
    assert "updated: '2026-11-21T00:33:30Z'" not in new


def test_clean_roadmap_unchanged():
    clean = ROADMAP.replace("    updated: '2026-11-21T00:21:12Z'\n", "")
    new, ids = repair_text(clean)
    assert ids == [] and new == clean


def test_unindented_task_list():
    text = "tasks:\n- id: t-9\n  updated: '2026-01-02T00:00:00Z'\n  x: 1\n  updated: '2026-01-01T00:00:00Z'\n"
    new, ids = repair_text(text)
    assert ids == ["t-9"]
    assert new.count("updated:") == 1 and "01-02" in new
