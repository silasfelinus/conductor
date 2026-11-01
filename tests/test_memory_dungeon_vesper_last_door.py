"""Writer-contract tests for Vesper's e12 Hoshimori collision and Last Door.

This simulates narrative decisions and save contracts only. It does NOT establish
playable encounters, production ArtJobs, rendered art or 32 shipped endings.
"""

import itertools
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
STORY = ROOT / "projects/memory-dungeon/story"


def load(name):
    return json.loads((STORY / name).read_text(encoding="utf-8"))


PACKET = load("HOSHIMORI-COLLISION-VESPER-QUESTS.json")
PIP = load("BRIAR-COLLISION-PIP-QUESTS.json")
MORROW = load("EARTH-COLLISION-MORROW-QUESTS.json")
CHAR = load("SEA-COLLISION-CHAR-QUESTS.json")
ENTRY = PACKET["entryContract"]
VALUES = ENTRY["choiceValues"]
SCENES = PACKET["scenes"]
FRAGMENTS = ("village-wolf-door", "village-tidal-oven")
HISTORIES = tuple(
    itertools.product(
        VALUES["e04"], VALUES["e06"], VALUES["e08"], VALUES["e11Bell"]
    )
)


def history(e04="open-the-tide-gate", e06="publish-twin-testimony",
            e08="keep-shelter-charter", bell="two-consenting-witnesses"):
    return {
        "e02": "trust-witnesses",
        "e04": e04,
        "e05": "tell-char",
        "e06": e06,
        "e08": e08,
        "e10": "destroy-price-ledger",
        "e11Bell": bell,
    }


def blank():
    return {"choices": {}, "flags": set(), "fragments": set(), "routes": {}}


def eligible(h, earned_prior, continuity=True):
    return (
        continuity
        and set(earned_prior) == set(ENTRY["requiresEarnedFragments"])
        and all(h.get(k) in options for k, options in VALUES.items())
    )


def choose(h, prior, scene_id, choice_id, state, continuity=True):
    if not eligible(h, prior, continuity):
        raise ValueError("unearned or forged entry")
    scene = next((s for s in SCENES if s["id"] == scene_id), None)
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


def family(h, final):
    bits = PACKET["endingContract"]["bitValues"]
    return sum(
        bits[k][v] * (1 << n)
        for n, (k, v) in enumerate(
            (("e02", h["e02"]), ("e04", h["e04"]), ("e06", h["e06"]),
             ("e08", h["e08"]), ("e12", final))
        )
    )


def last_door(h, prior, state, final, hearing=True, continuity=True):
    if not eligible(h, prior, continuity):
        raise ValueError("unearned history")
    if not hearing or set(state["fragments"]) != set(FRAGMENTS):
        raise ValueError("unfinished Last Door")
    if set(prior) | set(state["fragments"]) != set(
        PACKET["exitContract"]["requiresAllEightFragments"]
    ):
        raise ValueError("missing fragment")
    if final not in PACKET["exitContract"]["finalChoiceIds"]:
        raise ValueError("invalid final choice")
    return family(h, final)


def test_canonical_sources_and_no_runtime_claims():
    assert PACKET["status"] == "WRITER_PACKET_ONLY_NOT_PLAYABLE"
    assert PACKET["world"] == "e12" and PACKET["viewpoint"] == "Vesper"
    assert PACKET["sourceCanon"].endswith("TWELVE-REALITY-COLLISION-FINALE.md")
    assert "not runtime events" in ENTRY["priorSaveSafety"]
    assert "older Char" in ENTRY["charContinuity"]
    assert "Legacy e09-e16" in ENTRY["priorSaveSafety"]
    assert "Neither e12 scene" in PACKET["exitContract"]["noRuntimeClaim"]
    assert set(VALUES["e11Bell"]) == {
        c["id"] for c in CHAR["scenes"][1]["choices"]
    }
    assert set(ENTRY["requiresEarnedFragments"]) == {
        *(s["fragment"] for s in PIP["scenes"]),
        *(s["fragment"] for s in MORROW["scenes"]),
        *(s["fragment"] for s in CHAR["scenes"]),
    }
    assert VALUES["e02"] == ["protect-village", "trust-witnesses"]
    assert VALUES["e06"] == [
        "protect-private-memory", "publish-twin-testimony"
    ]
    assert VALUES["e08"] == ["keep-shelter-charter", "unbar-all-doors"]
    assert PACKET["exitContract"]["finalChoiceIds"] == [
        "disable-transit", "free-transit"
    ]


def test_both_scenes_have_distinct_consequential_choices_and_fair_fallbacks():
    assert {s["id"] for s in SCENES} == set(FRAGMENTS)
    flags, routes = [], []
    for scene in SCENES:
        assert scene["id"] == scene["fragment"]
        assert len(scene["opening"]) > 350
        assert len(scene["dialogue"]) >= 5
        assert len({line["speaker"] for line in scene["dialogue"]}) >= 4
        assert len(scene["puzzle"]) > 300
        assert "fallback" in scene["puzzle"].lower()
        assert len(scene["choices"]) == 3
        assert len({c["id"] for c in scene["choices"]}) == 3
        assert "revisit" in scene["replay"].lower()
        for choice in scene["choices"]:
            for field in (
                "label", "visibleCost", "reply", "outcome", "savedFlag",
                "routeEffect", "laterCallback", "failureContinuation",
                "artSubject",
            ):
                assert len(choice[field]) >= 25, (scene["id"], field)
            assert "Last Door" in choice["laterCallback"]
            flags.append(choice["savedFlag"])
            routes.append(choice["routeEffect"])
    assert len(set(flags)) == len(flags) == 6
    assert len(set(routes)) == len(routes) == 6


@pytest.mark.parametrize("e04,e06,e08,bell", HISTORIES)
def test_all_36_history_overlays_keep_costs_and_char_causality(
    e04, e06, e08, bell
):
    overlays = PACKET["historyOverlays"]
    parts = (
        overlays["e04"][e04], overlays["e06"][e06],
        overlays["e08"][e08], overlays["e11Bell"][bell],
    )
    assert all(len(p["dialogue"]) > 90 and len(p["cost"]) > 55 for p in parts)
    assert len({p["dialogue"] for p in parts}) == 4
    if e04 == "open-the-tide-gate":
        assert "older Char died" in parts[0]["dialogue"]
        assert "original death" in parts[0]["cost"]
    else:
        assert "Char survived" in parts[0]["cost"]
    assert "two historical people" in overlays["e11Bell"][
        "two-consenting-witnesses"
    ]["cost"]


@pytest.mark.parametrize("e04,e06,e08,bell", HISTORIES)
@pytest.mark.parametrize("a,b", itertools.product(range(3), repeat=2))
@pytest.mark.parametrize("reverse", (False, True))
def test_648_two_scene_routes_save_restore_without_duplicate_awards(
    e04, e06, e08, bell, a, b, reverse
):
    h = history(e04, e06, e08, bell)
    prior = ENTRY["requiresEarnedFragments"]
    sequence = [(SCENES[0], SCENES[0]["choices"][a]),
                (SCENES[1], SCENES[1]["choices"][b])]
    if reverse:
        sequence.reverse()
    state = blank()
    for scene, choice in sequence:
        state = choose(h, prior, scene["id"], choice["id"], state)
    assert state["fragments"] == set(FRAGMENTS)
    assert state["flags"] == {c["savedFlag"] for _, c in sequence}
    assert state["routes"] == {
        s["id"]: c["routeEffect"] for s, c in sequence
    }
    restored = {
        "choices": dict(state["choices"]),
        "flags": set(state["flags"]),
        "fragments": set(state["fragments"]),
        "routes": dict(state["routes"]),
    }
    for scene, choice in sequence:
        assert choose(h, prior, scene["id"], choice["id"], restored) is restored
        alternate = next(c for c in scene["choices"] if c["id"] != choice["id"])
        with pytest.raises(ValueError, match="irreversible"):
            choose(h, prior, scene["id"], alternate["id"], restored)
    assert last_door(h, prior, restored, "free-transit", hearing=True) in range(32)


@pytest.mark.parametrize("bad", [
    {"e02": "unearned-default"},
    {"e04": "char-automatically-resurrected"},
    {"e05": "invented-departure"},
    {"e06": "both"},
    {"e08": "locked-forever"},
    {"e10": "not-a-real-crossroad"},
    {"e11Bell": "made-up-bell"},
])
def test_forged_history_cannot_award_fragments(bad):
    h = {**history(), **bad}
    state = blank()
    with pytest.raises(ValueError, match="unearned"):
        choose(h, ENTRY["requiresEarnedFragments"], FRAGMENTS[0],
               SCENES[0]["choices"][0]["id"], state)
    assert state == blank()


def test_missing_fragments_or_char_continuity_cannot_unlock():
    prior = ENTRY["requiresEarnedFragments"]
    h = history()
    state = blank()
    for missing in prior:
        with pytest.raises(ValueError, match="unearned"):
            choose(h, [f for f in prior if f != missing], FRAGMENTS[0],
                   SCENES[0]["choices"][0]["id"], state)
    with pytest.raises(ValueError, match="unearned"):
        choose(h, prior, FRAGMENTS[0], SCENES[0]["choices"][0]["id"],
               state, continuity=False)
    assert state == blank()


def test_no_fragment_on_visit_or_final_choice_before_local_hearing():
    h, prior = history(), ENTRY["requiresEarnedFragments"]
    state = blank()
    with pytest.raises(ValueError, match="unknown scene"):
        choose(h, prior, "unwritten-location", "free", state)
    with pytest.raises(ValueError, match="unknown choice"):
        choose(h, prior, FRAGMENTS[0], "free-fragment", state)
    assert state == blank()
    state = choose(h, prior, FRAGMENTS[0], SCENES[0]["choices"][0]["id"], state)
    with pytest.raises(ValueError, match="unfinished"):
        last_door(h, prior, state, "free-transit")
    state = choose(h, prior, FRAGMENTS[1], SCENES[1]["choices"][0]["id"], state)
    with pytest.raises(ValueError, match="unfinished"):
        last_door(h, prior, state, "free-transit", hearing=False)
    with pytest.raises(ValueError, match="invalid"):
        last_door(h, prior, state, "unearned-third-ending")
    assert PACKET["exitContract"]["noFragmentOnVisit"] is True
    assert PACKET["exitContract"]["noRepeatAwards"] is True
    assert PACKET["exitContract"]["noEndingOnFragmentsAlone"] is True


def test_exactly_32_families_and_e04_survival_subbranches_share_only_core_bit():
    e02, e04, e06, e08, e12 = (
        VALUES["e02"], VALUES["e04"], VALUES["e06"], VALUES["e08"],
        PACKET["exitContract"]["finalChoiceIds"],
    )
    keys = {
        family({**history(), "e02": a, "e04": b, "e06": c, "e08": d}, e)
        for a, b, c, d, e in itertools.product(e02, e04, e06, e08, e12)
    }
    assert keys == set(range(32))
    assert PACKET["endingContract"]["coreFamilyCount"] == 32
    for a, c, d, e in itertools.product(e02, e06, e08, e12):
        h = {**history(), "e02": a, "e06": c, "e08": d}
        assert family({**h, "e04": "seal-the-tide-gate"}, e) == family(
            {**h, "e04": "divert-the-current"}, e
        )
        assert family({**h, "e04": "open-the-tide-gate"}, e) != family(
            {**h, "e04": "seal-the-tide-gate"}, e
        )


def test_four_authored_exemplars_have_unique_keys_and_real_scene_differences():
    exemplars = PACKET["endingContract"]["exemplars"]
    assert len(exemplars) == 4
    assert len({e["key"] for e in exemplars}) == 4
    assert len({e["title"] for e in exemplars}) == 4
    assert len({e["location"] for e in exemplars}) == 4
    assert len({e["action"] for e in exemplars}) == 4
    for e in exemplars:
        assert f"{family(e['history'], e['history']['e12']):02d}" == e["key"]
        assert all(len(e[k]) > 100 for k in ("action", "voices", "cost"))
        assert len(e["closing"]) > 50
    assert {e["history"]["e04"] for e in exemplars} == set(VALUES["e04"])
    assert {e["history"]["e12"] for e in exemplars} == set(
        PACKET["exitContract"]["finalChoiceIds"]
    )
    assert "NOT_32_DELIVERED" in PACKET["endingContract"]["exemplarStatus"]


def test_art_is_twelve_unsubmitted_targets_and_no_claimed_delivery():
    art = PACKET["artProduction"]
    assert art["status"] == "NOT_SUBMITTED"
    assert art["artJobIds"] == art["deliveredImages"] == []
    expected = {
        f"{s['id']}:{target}"
        for s in SCENES
        for target in ["opening", *(c["id"] for c in s["choices"])]
    } | {
        f"ending-exemplar:{e['key']}"
        for e in PACKET["endingContract"]["exemplars"]
    }
    assert len(expected) == 12
    assert set(art["targets"]) == expected
    assert len(art["targets"]) == len(set(art["targets"]))
