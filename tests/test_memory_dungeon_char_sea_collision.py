"""Writer-packet validation for Char's unbuilt e11 collision quests.

This tests authoring and save-effect contracts, NOT runtime playability or art delivery.
"""

import itertools
import json
from pathlib import Path

import pytest


PACKET = json.loads(
    (
        Path(__file__).resolve().parents[1]
        / "projects/memory-dungeon/story/SEA-COLLISION-CHAR-QUESTS.json"
    ).read_text(encoding="utf-8")
)
FATES = ("open-the-tide-gate", "seal-the-tide-gate", "divert-the-current")
DEPARTURES = ("run-again", "stay", "tell-char")
FRAGMENTS = ("sea-unwritten-map", "sea-sister-bell")


def simulate_choice(fate, departure, scene_id, choice_id, earned_continuity, state):
    """Contract-level reducer; the game still needs its own implementation."""
    histories = {(h["e04"], h["e05"]) for h in PACKET["histories"]}
    if (fate, departure) not in histories or not earned_continuity:
        raise ValueError("Unverified Char continuity or invented history")
    scene = next((s for s in PACKET["scenes"] if s["id"] == scene_id), None)
    if scene is None:
        raise ValueError("Unknown scene")
    choice = next((c for c in scene["choices"] if c["id"] == choice_id), None)
    if choice is None:
        raise ValueError("Unknown choice")
    previous = state["choices"].get(scene_id)
    if previous and previous != choice_id:
        raise ValueError("Cannot rewrite an irreversible decision")
    if previous:
        return state
    return {
        "choices": {**state["choices"], scene_id: choice_id},
        "flags": {*state["flags"], choice["savedFlag"]},
        "fragments": {*state["fragments"], choice["fragment"]},
    }


def empty_state():
    return {"choices": {}, "flags": set(), "fragments": set()}


def test_packet_preserves_nine_distinct_causal_histories():
    assert PACKET["status"] == "WRITER_PACKET_ONLY_NOT_PLAYABLE"
    assert PACKET["world"] == "e11"
    assert PACKET["viewpoint"] == "Char"
    histories = PACKET["histories"]
    assert len(histories) == 9
    assert {(h["e04"], h["e05"]) for h in histories} == set(
        itertools.product(FATES, DEPARTURES)
    )
    for history in histories:
        assert history["entryRequires"] == "earned-e06-char-continuity"
        assert len(history["openingDialogue"]) > 55
        assert len(history["causalContract"]) > 85
        if history["e04"] == "open-the-tide-gate":
            assert "older Char died" in history["causalContract"]
            assert "younger" in history["causalContract"]
        else:
            assert "older Char survived" in history["causalContract"]
    assert "e06" in PACKET["entryContract"]["missingContinuityFallback"]
    assert PACKET["exitContract"]["noFragmentOnVisit"]
    assert PACKET["exitContract"]["noRepeatAwards"]


def test_each_scene_has_distinct_costs_dialogue_outcomes_and_callbacks():
    scenes = PACKET["scenes"]
    assert {scene["id"] for scene in scenes} == set(FRAGMENTS)
    flags = []
    for scene in scenes:
        assert scene["fragment"] == scene["id"]
        assert len(scene["opening"]) > 250
        assert len(scene["dialogue"]) >= 3
        assert len(scene["choices"]) == 3
        assert len({choice["id"] for choice in scene["choices"]}) == 3
        assert len({choice["routeEffect"] for choice in scene["choices"]}) == 3
        for choice in scene["choices"]:
            assert choice["fragment"] == scene["id"]
            for key in (
                "visibleCost", "reply", "outcome", "savedFlag", "laterCallback",
                "failureContinuation", "artSubject",
            ):
                assert len(choice[key]) >= 20, (scene["id"], choice["id"], key)
            flags.append(choice["savedFlag"])
    assert len(flags) == len(set(flags))
    assert PACKET["artStatus"] == "CONCEPT_ONLY_NO_ARTJOBS"


@pytest.mark.parametrize("fate,departure", itertools.product(FATES, DEPARTURES))
def test_all_causal_histories_have_nine_nonblocking_quest_routes(fate, departure):
    scenes = PACKET["scenes"]
    for first, second in itertools.product(scenes[0]["choices"], scenes[1]["choices"]):
        state = empty_state()
        assert not state["fragments"]
        state = simulate_choice(fate, departure, scenes[0]["id"], first["id"], True, state)
        assert state["fragments"] == {scenes[0]["fragment"]}
        state = simulate_choice(fate, departure, scenes[1]["id"], second["id"], True, state)
        assert state["fragments"] == set(FRAGMENTS)
        assert len(state["choices"]) == 2
        assert len(state["flags"]) == 2
        assert (
            simulate_choice(fate, departure, scenes[1]["id"], second["id"], True, state)
            is state
        )
        with pytest.raises(ValueError, match="irreversible"):
            alternate = next(c for c in scenes[1]["choices"] if c["id"] != second["id"])
            simulate_choice(fate, departure, scenes[1]["id"], alternate["id"], True, state)


def test_forged_history_or_missing_continuity_cannot_award_fragments():
    for fate, departure, earned in [
        ("invented-fate", "stay", True),
        ("open-the-tide-gate", "invented-departure", True),
        ("open-the-tide-gate", "run-again", False),
        ("seal-the-tide-gate", "tell-char", False),
    ]:
        with pytest.raises(ValueError, match="continuity or invented history"):
            simulate_choice(
                fate, departure, FRAGMENTS[0], "return-to-owners", earned, empty_state()
            )
    with pytest.raises(ValueError, match="Unknown choice"):
        simulate_choice(
            "open-the-tide-gate", "stay", FRAGMENTS[1], "fabricated-verdict",
            True, empty_state()
        )
    with pytest.raises(ValueError, match="Unknown scene"):
        simulate_choice(
            "open-the-tide-gate", "stay", "unearned-third-fragment",
            "return-to-owners", True, empty_state()
        )
