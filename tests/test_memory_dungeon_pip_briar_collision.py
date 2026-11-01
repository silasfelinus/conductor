"""Authoring contract for Pip's e09 finale collision scenes.

This is not a runtime playthrough or proof that artwork has been delivered.
"""
import itertools
import json
from pathlib import Path

import pytest


PACKET = json.loads(
    (
        Path(__file__).resolve().parents[1]
        / "projects/memory-dungeon/story/BRIAR-COLLISION-PIP-QUESTS.json"
    ).read_text(encoding="utf-8")
)
VERDICTS = ("sealed-village", "witness-open-village")
GATES = ("open-the-tide-gate", "seal-the-tide-gate", "divert-the-current")
FRAGMENTS = ("briar-office-key", "briar-tide-roots")


def blank_state():
    return {"choices": {}, "flags": set(), "fragments": set(), "routes": {}}


def choose(verdict, gate, scene_id, choice_id, state, *, earned=True):
    """Contract-level simulation, not an application reducer."""
    histories = {(h["e02"], h["e04"]) for h in PACKET["histories"]}
    if not earned or (verdict, gate) not in histories:
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
            raise ValueError("irreversible choice")
        return state
    return {
        "choices": {**state["choices"], scene_id: choice_id},
        "flags": {*state["flags"], choice["savedFlag"]},
        "fragments": {*state["fragments"], scene["fragment"]},
        "routes": {**state["routes"], scene_id: choice["routeEffect"]},
    }


def test_all_six_earned_history_openings_preserve_causal_costs():
    assert PACKET["status"] == "WRITER_PACKET_ONLY_NOT_PLAYABLE"
    assert PACKET["world"] == "e09"
    assert PACKET["viewpoint"] == "Pip"
    assert {(h["e02"], h["e04"]) for h in PACKET["histories"]} == set(
        itertools.product(VERDICTS, GATES)
    )
    assert "writer-only" in PACKET["entryContract"]["e02RuntimeMapping"]
    assert "Never invent" in PACKET["entryContract"]["e02RuntimeMapping"]
    for history in PACKET["histories"]:
        assert len(history["openingDialogue"]) > 130
        assert len(history["continuity"]) > 80
        if history["e04"] == "open-the-tide-gate":
            assert "Char" in history["continuity"] and "death" in history["continuity"] or "Char died" in history["continuity"]
        else:
            assert "Char survived" in history["continuity"]
    assert "Do not award" in PACKET["entryContract"]["missingHistoryFallback"]


def test_both_fragment_scenes_have_costs_voice_failure_and_distinct_callbacks():
    assert {s["id"] for s in PACKET["scenes"]} == set(FRAGMENTS)
    flags, routes = [], []
    for scene in PACKET["scenes"]:
        assert scene["id"] == scene["fragment"]
        assert len(scene["opening"]) > 350
        assert len(scene["dialogue"]) >= 3
        assert len(scene["puzzle"]) > 110
        assert len(scene["choices"]) == 3
        assert len({c["id"] for c in scene["choices"]}) == 3
        for choice in scene["choices"]:
            for field in (
                "label", "visibleCost", "reply", "outcome", "savedFlag",
                "routeEffect", "laterCallback", "failureContinuation", "artSubject",
            ):
                assert len(choice[field]) >= 18, (scene["id"], choice["id"], field)
            assert "e10" in choice["laterCallback"] or "e11" in choice["laterCallback"]
            flags.append(choice["savedFlag"])
            routes.append(choice["routeEffect"])
    assert len(flags) == len(set(flags)) == 6
    assert len(routes) == len(set(routes)) == 6


@pytest.mark.parametrize("verdict,gate", itertools.product(VERDICTS, GATES))
@pytest.mark.parametrize("first,second", itertools.product(range(3), repeat=2))
def test_all_fifty_four_two_scene_routes_save_replay_and_forbid_rewrites(
    verdict, gate, first, second
):
    office, roots = PACKET["scenes"]
    a, b = office["choices"][first], roots["choices"][second]
    state = choose(verdict, gate, office["id"], a["id"], blank_state())
    state = choose(verdict, gate, roots["id"], b["id"], state)
    assert state["fragments"] == set(FRAGMENTS)
    assert state["flags"] == {a["savedFlag"], b["savedFlag"]}
    assert state["routes"] == {
        office["id"]: a["routeEffect"],
        roots["id"]: b["routeEffect"],
    }
    restored = {
        "choices": dict(state["choices"]),
        "flags": set(state["flags"]),
        "fragments": set(state["fragments"]),
        "routes": dict(state["routes"]),
    }
    assert choose(verdict, gate, office["id"], a["id"], restored) is restored
    assert choose(verdict, gate, roots["id"], b["id"], restored) is restored
    with pytest.raises(ValueError, match="irreversible"):
        choose(
            verdict, gate, office["id"],
            office["choices"][(first + 1) % 3]["id"], restored,
        )
    with pytest.raises(ValueError, match="irreversible"):
        choose(
            verdict, gate, roots["id"],
            roots["choices"][(second + 1) % 3]["id"], restored,
        )


@pytest.mark.parametrize(
    "verdict,gate,earned",
    [
        ("invented-witness", "open-the-tide-gate", True),
        ("sealed-village", "fabricated-gate", True),
        ("sealed-village", "open-the-tide-gate", False),
        ("witness-open-village", "divert-the-current", False),
    ],
)
def test_forged_or_unearned_histories_never_award_a_fragment(verdict, gate, earned):
    state = blank_state()
    with pytest.raises(ValueError, match="unearned or forged history"):
        choose(verdict, gate, FRAGMENTS[0], "translate-shift-oath", state, earned=earned)
    assert not state["fragments"] and not state["choices"]


def test_unknown_scene_or_choice_cannot_award_and_visiting_does_not_count():
    state = blank_state()
    with pytest.raises(ValueError, match="unknown scene"):
        choose("sealed-village", GATES[0], "secret-third-fragment", "anything", state)
    with pytest.raises(ValueError, match="unknown choice"):
        choose("sealed-village", GATES[0], FRAGMENTS[0], "auto-award", state)
    assert state == blank_state()
    assert PACKET["exitContract"]["noFragmentOnVisit"] is True
    assert PACKET["exitContract"]["noRepeatAwards"] is True
    assert PACKET["exitContract"]["requiresFragments"] == list(FRAGMENTS)


def test_art_is_eight_unsubmitted_targets_not_fictional_deliveries():
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
    assert "Neither scene is wired" in PACKET["exitContract"]["noRuntimeClaim"]
