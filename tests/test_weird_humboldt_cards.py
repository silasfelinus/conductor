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
    seed_chapters, problems = wh.parse_seed_chapters(wh.SEEDS.read_text())
    assert problems == []
    assert len(cards) == len(seed_chapters)
    assert {c["id"] for c in cards} == set(seed_chapters)
    assert {c["chapter"] for c in cards} == set(seed_chapters.values())
    assert all(c["chapter"] == seed_chapters[c["id"]] for c in cards)


def test_seed_catalog_ignores_editorial_mentions_and_rejects_duplicates():
    text = wh.SEEDS.read_text()
    seed_chapters, problems = wh.parse_seed_chapters(text)
    assert problems == []
    assert seed_chapters["WH-121"] == 2
    assert "WH-122" not in seed_chapters  # mentioned in prose, not a seed bullet
    duplicated = text.replace("- **WH-001 ·", "- **WH-121 · Duplicate:** test.\n- **WH-001 ·", 1)
    _, problems = wh.parse_seed_chapters(duplicated)
    assert any("duplicate premise" in p for p in problems)


def test_validator_rejects_wrong_chapter_and_missing_seed():
    cards = wh.load_cards()
    cards[0]["chapter"] = 2
    assert any("disagrees with seed chapter" in p for p in wh.validate(cards))
    cards = wh.load_cards()
    cards.pop()
    assert any("deck has" in p and "expected" in p for p in wh.validate(cards))


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


def test_eight_archetypes_are_valid():
    archetypes = wh.load_archetypes()
    assert len(archetypes) == 8
    assert wh.validate_archetypes(archetypes, wh.load_anchors()) == []


def test_archetype_rejects_bad_points_missing_reaction_and_mystic_framing():
    anchors = wh.load_anchors()
    arch = wh.load_archetypes()
    arch[0]["skills"]["rizz"] = 3
    arch[1]["anchor_reactions"].pop("WH-A3")
    arch[4]["perk"] += " A sacred racial ability."
    problems = wh.validate_archetypes(arch, anchors)
    assert any("total 6" in p for p in problems)
    assert any("one reaction per anchor" in p for p in problems)
    assert any("mystical" in p for p in problems)
