"""The daily broadcast must have authored briefs beyond today's render."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_dead_air_runway import check_runway


def test_dated_runway_detects_a_missing_future_brief(tmp_path):
    for day in ("2026-11-15", "2026-11-16", "2026-11-18"):
        (tmp_path / f"{day}-episode.yaml").write_text(
            f"date: '{day}'\nstatus: authored\n"
        )
    assert check_runway("2026-11-15", tmp_path, days=4) == ["2026-11-17"]
    assert check_runway("2026-11-15", tmp_path, days=2) == []


def test_unsubmitted_and_completed_are_distinct_from_dated_drafts(tmp_path):
    (tmp_path / "completed.yaml").write_text(
        "date: '2026-11-15'\nstatus: completed\n"
    )
    (tmp_path / "rendering.yaml").write_text(
        "date: '2026-11-16'\nstatus: rendering\n"
    )
    assert check_runway("2026-11-15", tmp_path, days=2) == [
        "2026-11-15", "2026-11-16",
    ]


def test_seven_original_briefs_are_currently_ready():
    assert check_runway(
        "2026-11-14", ROOT / "projects/dead-air/episodes", days=7
    ) == []
