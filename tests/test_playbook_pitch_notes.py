"""Silas's Gestation notes reach the next day's playbook challenge brief."""
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import playbook_pitch_memory as memory

DOCKET = """date: "2026-10-26"
pitches:
  - slug: moon-laundry
    concept_id: moon-laundry
    title: Moon Laundry
    mode: new
    parents: []
    genre_pillar: Cozy science fiction
    next_questions: ["What is lost?", "Who decides?"]
"""


def _dockets(root: Path, notes: str | None) -> Path:
    (root / "2026-10-26.yaml").write_text(DOCKET)
    if notes is not None:
        (root / memory.NOTES_FILE).write_text(notes)
    return root


def test_open_notes_lead_the_memory_summary():
    with TemporaryDirectory() as d:
        root = _dockets(Path(d), """notes:
  moon-laundry:
    - at: '2026-10-26T23:50:00Z'
      by: silas
      note: Make the socks sentient and unionized.
      status: open
    - at: '2026-10-25T10:00:00Z'
      by: silas
      note: An older note already answered.
      status: addressed
      addressed_in: 2026-10-26/moon-laundry
""")
        index = memory.build_index(root, before="2026-10-27")
        assert len(index["concepts"]["moon-laundry"]["silas_notes"]) == 2
        summary = memory.memory_summary(index)
        assert "OPEN NOTES FROM SILAS" in summary
        assert "Make the socks sentient and unionized." in summary
        assert "An older note already answered." not in summary


def test_no_notes_file_is_fine():
    with TemporaryDirectory() as d:
        index = memory.build_index(_dockets(Path(d), None), before="2026-10-27")
        assert index["concepts"]["moon-laundry"]["silas_notes"] == []
        assert "OPEN NOTES FROM SILAS" not in memory.memory_summary(index)


def test_bad_status_is_refused():
    with TemporaryDirectory() as d:
        root = _dockets(Path(d), "notes:\n  moon-laundry:\n    - note: x\n      status: maybe\n")
        with pytest.raises(ValueError):
            memory.build_index(root, before="2026-10-27")
