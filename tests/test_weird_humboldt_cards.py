"""Weird Humboldt v1 deck: contract validation and seeded playtest determinism."""
import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "validate_weird_humboldt_cards.py"
spec = importlib.util.spec_from_file_location("wh_validate", SCRIPT)
wh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wh)

SKILLS = {"rizz": 1, "burly": 1, "wits": 2, "local_lore": 1, "psyche": 1}


def test_deck_is_valid():
    assert wh.validate(wh.load_cards()) == []


def test_deck_shape():
    cards = wh.load_cards()
    assert len(cards) == 121
    assert {c["chapter"] for c in cards} == {1, 2, 3, 4, 5, 6}
    assert len({c["id"] for c in cards}) == 121


def test_playtest_is_deterministic_and_states_keep_canon():
    cards = wh.load_cards()
    a = wh.playtest(cards, 5, "sober", SKILLS, "mara")
    assert a == wh.playtest(cards, 5, "sober", SKILLS, "mara")
    assert a != wh.playtest(cards, 6, "sober", SKILLS, "mara")


def test_validator_rejects_power_up_state():
    cards = wh.load_cards()
    pivotal = next(c for c in cards if c.get("by_state"))
    pivotal["by_state"]["stoned"]["check_mods"] = {"a": 1, "b": 1}
    assert any("power-up" in p for p in wh.validate(cards))


def test_validator_rejects_failure_on_no_roll_option():
    cards = wh.load_cards()
    opt = next(o for c in cards for o in c["options"] if o["skill"] == "none")
    opt["failure"] = {"text": "x " * 12, "effects": []}
    assert any("no-roll option cannot have a failure" in p for p in wh.validate(cards))


def test_no_dead_end_proof_holds_for_every_chapter():
    cards = wh.load_cards()
    assert wh.no_dead_end_problems(cards) == []
    for ch in range(1, 7):
        assert len(wh.guaranteed_pool(cards, ch)) >= wh.MIN_GUARANTEED_PER_CHAPTER


def test_no_dead_end_proof_catches_flag_locked_chapter():
    cards = wh.load_cards()
    for c in cards:
        if c["chapter"] == 3:
            c["eligibility"]["requires_flags"] = ["minor_companion"]
    assert any("chapter 3" in p and "dead end" in p for p in wh.validate(cards))


def _enums():
    import json
    schema = json.loads(wh.SCHEMA.read_text())
    return {"skill": schema["$defs"]["option"]["properties"]["skill"]["enum"],
            "tier": schema["properties"]["tier"]["enum"], "rarity": schema["properties"]["rarity"]["enum"]}


def test_six_chapter_anchors_are_valid():
    anchors = wh.load_anchors()
    assert [a["id"] for a in anchors] == [f"WH-A{i}" for i in range(1, 7)]
    assert wh.validate_anchors(anchors, _enums()) == []


def test_anchor_crossroads_must_set_stay_and_follow():
    anchors = wh.load_anchors()
    for o in anchors[1]["options"]:
        for br in ("success", "failure"):
            if br in o:
                o[br]["effects"] = [e for e in o[br]["effects"] if "followed" not in e]
    assert any("crossroads1_followed" in p for p in wh.validate_anchors(anchors, _enums()))


def test_anchor_cannot_be_flag_gated():
    anchors = wh.load_anchors()
    anchors[0]["eligibility"]["requires_flags"] = ["minor_companion"]
    assert any("flag-gated" in p for p in wh.validate_anchors(anchors, _enums()))


def test_endings_are_valid():
    endings = wh.load_endings()
    assert len(endings) >= 10
    assert wh.validate_endings(endings, wh.load_cards()) == []


def test_endings_reject_unearnable_flag_and_missing_core():
    endings = wh.load_endings()
    endings[0]["requires_flags"] = ["never_set_flag"]
    assert any("never_set_flag" in p for p in wh.validate_endings(endings, wh.load_cards()))
    assert any("missing core" in p for p in wh.validate_endings(endings[1:], wh.load_cards()))
