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
    assert len(cards) == 114
    assert {c["chapter"] for c in cards} == {1, 2, 3, 4, 5, 6}
    assert len({c["id"] for c in cards}) == 114


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
