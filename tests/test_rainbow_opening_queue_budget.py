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


def test_wan_shot_budgets_report_exact_headroom():
    data = {
        "round": opening.DOODLE_ROUND,
        "lanes": [{"key": "wan-mp4", "fps": 16}],
        "subjects": [
            {"key": "a", "lane": "wan-mp4", "duration": 3},
            {"key": "still", "lane": "flux-still"},
            {"key": "b", "lane": "wan-mp4", "duration": 7.5},
        ],
    }
    assert opening.wan_shot_budgets(data) == [
        {"key": "a", "seconds": 3, "fps": 16, "frames": 48,
         "seconds_headroom": 5, "frame_headroom": 80},
        {"key": "b", "seconds": 7.5, "fps": 16, "frames": 120,
         "seconds_headroom": 0.5, "frame_headroom": 8},
    ]


def test_tiny_overage_is_still_rejected():
    with pytest.raises(ValueError, match="exceeds opening clip budget"):
        opening.validate_opening_queue_budget(ledger(8.0001, 16))


def test_actual_ledger_budgets_have_nonnegative_headroom():
    budgets = opening.wan_shot_budgets(yaml.safe_load(opening.LEDGER.read_text()))
    assert budgets and all(b["frame_headroom"] >= 0 and b["seconds_headroom"] >= 0 for b in budgets)
    assert budgets[0] == {"key": budgets[0]["key"], "seconds": 3, "fps": 16, "frames": 48,
                          "seconds_headroom": 5, "frame_headroom": 80}


def test_delivery_report_carries_budgets():
    sources = [("a", 4, 1, 2)]
    budgets = [{"key": "a", "seconds": 3, "fps": 16, "frames": 48,
                "seconds_headroom": 5, "frame_headroom": 80}]
    report = opening.delivery_report(sources, [], ["a"], budgets)
    assert report["wan_shot_budgets"] == budgets
    assert opening.delivery_report(sources, [], [])["wan_shot_budgets"] == []
