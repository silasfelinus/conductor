"""Contract tests for Shifting Desks encounter packs.

projects/shifting-desks/encounters/validate_pack.py is the authority; these tests
pin that every committed pack passes it, and that its core design rule (NO CLEAN
WINS: every choice's cost + success contains a harmful effect) actually bites.
"""

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
ENC_DIR = ROOT / "projects" / "shifting-desks" / "encounters"
PACK = ENC_DIR / "ORIENTATION-12.json"

_spec = importlib.util.spec_from_file_location("shifting_desks_validate_pack", ENC_DIR / "validate_pack.py")
vp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vp)


def _validate(tmp_path, pack):
    path = tmp_path / "PACK.json"
    path.write_text(json.dumps(pack), encoding="utf-8")
    return vp.validate_pack(path)


@pytest.fixture
def pack():
    return json.loads(PACK.read_text(encoding="utf-8"))


@pytest.mark.parametrize("path", vp.pack_paths([]), ids=lambda p: p.name)
def test_every_committed_pack_is_valid(path):
    assert vp.validate_pack(path) == []


def test_orientation_pack_shape(pack):
    assert len(pack["locations"]) == 3
    assert all(len(loc["encounter_ids"]) == 4 for loc in pack["locations"])
    polarity = [e["polarity"] for e in pack["encounters"]]
    assert {p: polarity.count(p) for p in set(polarity)} == {"good": 4, "bad": 4, "mixed": 4}
    assert len(pack["boss"]["choices"]) >= 3


def test_clean_win_is_rejected(tmp_path, pack):
    bad = copy.deepcopy(pack)
    choice = bad["encounters"][0]["choices"][0]
    choice["cost"] = {}
    choice["success"]["effects"] = {"clearance": 1, "composure": 1}
    errors = _validate(tmp_path, bad)
    assert any("clean win" in e for e in errors)


def test_suspicion_rise_counts_as_harm(tmp_path, pack):
    ok = copy.deepcopy(pack)
    choice = ok["encounters"][0]["choices"][0]
    choice["cost"] = {}
    choice["success"]["effects"] = {"clearance": 2, "suspicion": 1}
    assert _validate(tmp_path, ok) == []


def test_rolled_choice_needs_failure_and_certain_choice_must_not(tmp_path, pack):
    bad = copy.deepcopy(pack)
    rolled = next(c for c in bad["encounters"][0]["choices"] if c["roll"])
    rolled["failure"] = None
    certain = next(c for c in bad["encounters"][0]["choices"] if c["roll"] is None)
    certain["failure"] = copy.deepcopy(rolled["success"])
    errors = _validate(tmp_path, bad)
    assert any("failure" in e and "outcome must be an object" in e for e in errors)
    assert any("without a roll must have failure: null" in e for e in errors)


def test_art_prompts_are_positive_only(tmp_path, pack):
    bad = copy.deepcopy(pack)
    bad["encounters"][0]["art"]["brief"] = (
        "A worker at a desk with no text and no logos, halftone grain, every surface bare and unmarked"
    )
    assert any("positive-only" in e for e in _validate(tmp_path, bad))


def test_boss_route_requirement_must_be_grantable(tmp_path, pack):
    bad = copy.deepcopy(pack)
    gated = next(c for c in bad["boss"]["choices"] if c["requires"])
    gated["requires"] = {"flag": "a-flag-nothing-grants"}
    assert any("nothing in this pack grants" in e for e in _validate(tmp_path, bad))


def test_unknown_meter_and_skill_rejected(tmp_path, pack):
    bad = copy.deepcopy(pack)
    rolled = next(c for c in bad["encounters"][1]["choices"] if c["roll"])
    rolled["roll"]["skill"] = "steel"
    rolled["cost"] = {"hp": -1}
    errors = _validate(tmp_path, bad)
    assert any("unknown meter" in e for e in errors)
    assert any("skill 'steel'" in e for e in errors)


def test_lead_flavor_quota_is_enforced(tmp_path, pack):
    bad = copy.deepcopy(pack)
    for enc in bad["encounters"]:
        enc["tags"] = ["deathtrap"]
    assert any("lead tag" in e for e in _validate(tmp_path, bad))


DECKS = ENC_DIR / "DECKS.json"


def test_decks_reference_only_granted_flags():
    assert vp.validate_decks(DECKS, vp.pack_paths([])) == []


def test_decks_reject_a_society_flag_nothing_grants(tmp_path):
    decks = json.loads(DECKS.read_text(encoding="utf-8"))
    decks["societies"][0]["objectives"]["orientation"].append("a-flag-nothing-grants")
    path = tmp_path / "DECKS.json"
    path.write_text(json.dumps(decks), encoding="utf-8")
    errors = vp.validate_decks(path, vp.pack_paths([]))
    assert any("no pack grants" in e for e in errors)


def test_decks_are_not_validated_as_packs():
    assert DECKS not in vp.pack_paths([])
