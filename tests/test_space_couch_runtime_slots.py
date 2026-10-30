"""Space Couch runtime-slot and party-adventure ledgers (2026-10-30 art refill)."""

from pathlib import Path

import yaml

from scripts.enqueue_art_requests import build_request, iter_cells
from scripts.repair_negation_art_prompts import violations

ART = Path(__file__).resolve().parents[1] / "projects/game-of-captains/art"
GROUPS = {"missions": 27, "antagonists": 5, "endings": 36}


def _load(name):
    return yaml.safe_load((ART / name).read_text())


def _check(data, priority):
    assert data["auto_submit"] is True
    assert data["is_public"] is False and data["cast_loras"] is False
    assert data["priority"] == priority
    (lane,) = data["lanes"]
    assert (lane["key"], lane["engine"], lane["prompt"]) == ("krea2", "krea2", "prose")
    for subject, render_lane in iter_cells(data):
        # The asset is game-of-captains/<the exact key artSlots.ts looks up>.
        assert subject["asset"].startswith("game-of-captains/")
        assert violations(subject["prompt_prose"]) == [], subject["key"]
        request = build_request(data, render_lane, subject)
        assert (request["width"], request["height"]) == (1344, 768)
        assert request["priority"] == priority


def test_runtime_slots_cover_missions_nemeses_and_endings():
    data = _load("RUNTIME-SLOTS-ROUND-2.yaml")
    _check(data, 700)
    keys = [s["asset"].removeprefix("game-of-captains/") for s in data["subjects"]]
    assert len(set(keys)) == len(keys)
    counts = {group: sum(1 for k in keys if k.startswith(group + "/")) for group in GROUPS}
    assert counts == GROUPS
    assert len({s["seed"] for s in data["subjects"]}) == len(keys)


def test_party_adventure_packs_are_low_priority_and_disjoint():
    assets = []
    for path in sorted(ART.glob("PARTY-ADVENTURES-ROUND-1-PACK-*.yaml")):
        data = yaml.safe_load(path.read_text())
        _check(data, 60)
        assets += [subject["asset"] for subject in data["subjects"]]
    assert all(asset.startswith("game-of-captains/trios/") for asset in assets)
    assert len(assets) == len(frozenset(assets)) == 850
