"""Pre-enqueue WAN budget checks for the C.A.T.S. opening."""
import importlib.util
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "export_rainbow_opening", ROOT / "scripts/export_rainbow_opening.py"
)
opening = importlib.util.module_from_spec(spec)
spec.loader.exec_module(opening)


def ledger(duration=3, fps=16):
    return {
        "round": opening.DOODLE_ROUND,
        "lanes": [{"key": "wan-mp4", "fps": fps}],
        "subjects": [
            {"key": "intro-cats-launch", "lane": "wan-mp4", "duration": duration}
        ],
    }


def test_actual_approved_ledger_stays_inside_budget():
    data = yaml.safe_load(opening.LEDGER.read_text())
    opening.validate_opening_queue_budget(data)


@pytest.mark.parametrize(
    ("duration", "fps"),
    [(9, 16), (8, 17), (3, 60), (0, 16), (-1, 16), (float("nan"), 16)],
)
def test_over_budget_or_invalid_requests_rejected_before_enqueue(duration, fps):
    with pytest.raises(ValueError, match="intro-cats-launch"):
        opening.validate_opening_queue_budget(ledger(duration, fps))


def test_missing_or_invalid_lane_fps_is_rejected():
    with pytest.raises(ValueError, match="invalid fps"):
        opening.validate_opening_queue_budget(ledger(fps=0))
    with pytest.raises(ValueError, match="missing"):
        opening.validate_opening_queue_budget(
            {"round": opening.DOODLE_ROUND, "lanes": [], "subjects": []}
        )


def test_legacy_opening_is_unaffected():
    opening.validate_opening_queue_budget({"round": "original-opening"})
