"""Writer-contract tests for Morrow's e10 Earth collision encounters.

These are authoring and simulated save invariants, NOT a playable map, renderer,
or proof that production art has been submitted.
"""

import itertools
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PACKET = json.loads(
    (ROOT / "projects/memory-dungeon/story/EARTH-COLLISION-MORROW-QUESTS.json").read_text(
        encoding="utf-8"
    )
)
PIP = json.loads(
    (ROOT / "projects/memory-dungeon/story/BRIAR-COLLISION-PIP-QUESTS.json").read_text(
        encoding="utf-8"
    )
)
GATES = ("open-the-tide-gate", "seal-the-tide-gate", "divert-the-current")
CHARTERS = ("consent", "open")
OFFICE = tuple(c["id"] for c in PIP["scenes"][0]["choices"])
FRAGMENTS = ("earth-lantern-refuge-charter", "earth-living-hours-ledger")
HISTORIES = tuple(itertools.product(GATES, CHARTERS, OFFICE))


def blank_state():
    return {"choices": {}, "flags": set(), "fragments": set(), "routes": {}}


def earned_entry(gate, charter, office, *, earned=True, fragments=True):
    """No writer-only semantic labels may substitute for earned runtime events."""
    contract = PACKET["entryContract"]
    return (
        earned
        and fragments
        and gate in contract["e04Values"]
        and charter in contract["e07SouthWatchRuntimeChoices"]
        and office in contract["e09OfficeRuntimeChoices"]
    )


def choose(history, scene_id, choice_id, state, *, earned=True, fragments=True):
    gate, charter, office = history
    if not earned_entry(gate, charter, office, earned=earned, fragments=fragments):
        raise ValueError("unearned or forged history")
    scene = next((s for s in PACKET["scenes"] if s["id"] == scene_id), None)
    if scene is None:
        raise ValueError("unknown scene")
    choice = next((c for c in scene["choices"] if c["id"] == choice_id), None)
    if choice is None:
        raise ValueError("unknown choice")
    old = state["choices"].get(scene_id)
    if old is not None:
        if old != choice_id:
            raise ValueError("irreversible decision")
        return state
    return {
        "choices": {**state["choices"], scene_id: choice_id},
        "flags": {*state["flags"], choice["savedFlag"]},
        "fragments": {*state["fragments"], scene["fragment"]},
        "routes": {**state["routes"], scene_id: choice["routeEffect"]},
    }


def test_entry_requires_earned_history_and_actual_e09_office_choice_ids():
    assert PACKET["status"] == "WRITER_PACKET_ONLY_NOT_PLAYABLE"
    assert PACKET["world"] == "e10"
    assert PACKET["viewpoint"] == "Morrow"
    assert PACKET["sourceCanon"].endswith("TWELVE-REALITY-COLLISION-FINALE.md")
    entry = PACKET["entryContract"]
    assert len(entry["requires"]) == 5
    assert set(entry["e04Values"]) == set(GATES)
    assert set(entry["e07SouthWatchRuntimeChoices"]) == set(CHARTERS)
    assert set(entry["e09OfficeRuntimeChoices"]) == set(OFFICE)
    assert entry["e09RuntimeSource"].endswith("BRIAR-COLLISION-PIP-QUESTS.json")
    assert entry["entryOverlayOrder"] == ["e04", "e07", "e09Office"]
    assert "Never synthesize" in entry["missingHistoryFallback"]
    assert "not runtime events" in entry["priorSaveSafety"]


@pytest.mark.parametrize("gate,charter,office", HISTORIES)
def test_all_eighteen_histories_have_distinct_dialogue_and_non_erased_costs(
    gate, charter, office
):
    overlays = PACKET["historyOverlays"]
    parts = (
        overlays["e04"][gate],
        overlays["e07"][charter],
        overlays["e09Office"][office],
    )
    assert all(len(p["dialogue"]) > 100 and len(p["cost"]) > 45 for p in parts)
    assert len({p["dialogue"] for p in parts}) == 3
    if gate == "open-the-tide-gate":
        assert "Char died" in parts[0]["dialogue"]
        assert "death" in parts[0]["cost"]
    else:
        assert "Char survived" in parts[0]["cost"]
    if office == "break-midnight-clock":
        assert "lost" in parts[2]["cost"]
        assert "timecards burned" in parts[2]["dialogue"]
    assert earned_entry(gate, charter, office)


def test_scenes_have_fair_puzzles_full_dialogue_and_non_cosmetic_choices():
    assert {s["id"] for s in PACKET["scenes"]} == set(FRAGMENTS)
    flags, routes = [], []
    for scene in PACKET["scenes"]:
        assert scene["fragment"] == scene["id"]
        assert len(scene["opening"]) > 350
        assert len(scene["dialogue"]) >= 4
        assert len({d["speaker"] for d in scene["dialogue"]}) >= 3
        assert len(scene["puzzle"]) > 240
        assert "fallback" in scene["puzzle"].lower()
        assert len(scene["choices"]) == 3
        assert len({c["id"] for c in scene["choices"]}) == 3
        for choice in scene["choices"]:
            for field in (
                "label", "visibleCost", "reply", "outcome", "savedFlag",
                "routeEffect", "laterCallback", "failureContinuation", "artSubject",
            ):
                assert len(choice[field]) >= 20, (scene["id"], choice["id"], field)
            assert "e11" in choice["laterCallback"] or "e12" in choice["laterCallback"]
            flags.append(choice["savedFlag"])
            routes.append(choice["routeEffect"])
    assert len(flags) == len(set(flags)) == 6
    assert len(routes) == len(set(routes)) == 6


@pytest.mark.parametrize("history", HISTORIES)
@pytest.mark.parametrize("first,second", itertools.product(range(3), repeat=2))
@pytest.mark.parametrize("reverse", (False, True))
def test_all_324_two_scene_routes_preserve_save_replay_and_order(
    history, first, second, reverse
):
    a, b = PACKET["scenes"]
    choices = [(a, a["choices"][first]), (b, b["choices"][second])]
    if reverse:
        choices.reverse()
    state = blank_state()
    assert state["fragments"] == set()
    for scene, choice in choices:
        state = choose(history, scene["id"], choice["id"], state)
        assert scene["fragment"] in state["fragments"]
    assert state["fragments"] == set(FRAGMENTS)
    assert state["flags"] == {choice["savedFlag"] for _, choice in choices}
    assert state["routes"] == {
        scene["id"]: choice["routeEffect"] for scene, choice in choices
    }
    restored = {
        "choices": dict(state["choices"]),
        "flags": set(state["flags"]),
        "fragments": set(state["fragments"]),
        "routes": dict(state["routes"]),
    }
    for scene, choice in choices:
        assert choose(history, scene["id"], choice["id"], restored) is restored
        alternate = next(c for c in scene["choices"] if c["id"] != choice["id"])
        with pytest.raises(ValueError, match="irreversible"):
            choose(history, scene["id"], alternate["id"], restored)


@pytest.mark.parametrize(
    "history,earned,fragments",
    [
        (("made-up-gate", "consent", OFFICE[0]), True, True),
        ((GATES[0], "fabricated-charter", OFFICE[0]), True, True),
        ((GATES[0], "open", "fabricated-e09-choice"), True, True),
        ((GATES[0], "open", OFFICE[0]), False, True),
        ((GATES[0], "consent", OFFICE[0]), True, False),
    ],
)
def test_missing_or_forged_history_never_awards_a_fragment(
    history, earned, fragments
):
    state = blank_state()
    with pytest.raises(ValueError, match="unearned or forged"):
        choose(
            history, FRAGMENTS[0], PACKET["scenes"][0]["choices"][0]["id"],
            state, earned=earned, fragments=fragments,
        )
    assert state == blank_state()


def test_invalid_scene_or_choice_and_just_visiting_do_not_award():
    state = blank_state()
    history = HISTORIES[0]
    with pytest.raises(ValueError, match="unknown scene"):
        choose(history, "unwritten-third-fragment", "anything", state)
    with pytest.raises(ValueError, match="unknown choice"):
        choose(history, FRAGMENTS[0], "free-fragment-on-visit", state)
    assert state == blank_state()
    contract = PACKET["exitContract"]
    assert contract["requiresFragments"] == list(FRAGMENTS)
    assert contract["noFragmentOnVisit"] is True
    assert contract["noRepeatAwards"] is True
    assert "separate playable e10 crossroad" in contract["requiresLocalCrisis"]
    assert "not mint extra core ending identities" in contract["noFreeEnding"]
    assert "Neither e10 scene is wired" in contract["noRuntimeClaim"]


def test_art_is_eight_unsubmitted_targets_not_delivered_media():
    art = PACKET["artProduction"]
    assert art["status"] == "NOT_SUBMITTED"
    assert art["artJobIds"] == []
    assert art["deliveredImages"] == []
    assert len(art["targets"]) == len(set(art["targets"])) == 8
    assert set(art["targets"]) == {
        f"{scene['id']}:{target}"
        for scene in PACKET["scenes"]
        for target in ["opening", *(c["id"] for c in scene["choices"])]
    }
