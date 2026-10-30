"""Slime City art round 1 (slime-city t-017): crews, districts, the 36 prototype cards and boards."""

from pathlib import Path

import yaml

from scripts.enqueue_art_requests import build_request, iter_cells
from scripts.repair_negation_art_prompts import violations

LEDGER = Path(__file__).resolve().parents[1] / "projects/slime-city/art/CREWS-DISTRICTS-CARDS-ROUND-1.yaml"
COUNTS = {"crews": 6, "districts": 7, "cards": 36, "boards": 3}


def test_ledger_covers_every_prototype_slot_once():
    data = yaml.safe_load(LEDGER.read_text())
    assert data["auto_submit"] is True and data["is_public"] is False and data["is_mature"] is False
    assert data["project_slug"] == "slime-city"
    (lane,) = data["lanes"]
    assert (lane["engine"], lane["prompt"]) == ("krea2", "prose")
    assets = [s["asset"] for s in data["subjects"]]
    assert len(assets) == len(frozenset(assets)) == sum(COUNTS.values())
    assert len({s["seed"] for s in data["subjects"]}) == len(assets)
    for group, count in COUNTS.items():
        assert sum(1 for a in assets if a.startswith(f"slime-city/{group}/")) == count
    for subject, render_lane in iter_cells(data):
        assert violations(subject["prompt_prose"]) == [], subject["key"]
        request = build_request(data, render_lane, subject)
        assert request["priority"] == 650 and request["isPublic"] is False
