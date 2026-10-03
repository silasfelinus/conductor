"""Regression coverage for recurring Daily Dream wording, scenery and surnames.

Silas, 2026-10-03: "we're getting some repeated phrasing again in our daily dreams.
terrace is turning into the next waterworld." The live catalog had named The Puffin
Terraces, Spore Shelf and Landing Terrace, ended six of fourteen Scenarios on "has to
decide whether", and shipped six characters surnamed Voss, five of them in September.
"""
from __future__ import annotations

import copy

import scripts.author_dream_proposal as authoring
import scripts.build_dream_proposal as bdp
from scripts import dream_creative_entropy as entropy
from scripts import dream_creative_ruts as ruts


def _proposal(setup: str, *, known_for: str = "A place with an ordinary physical habit.") -> dict:
    proposal = copy.deepcopy(bdp.SAMPLE_PROPOSAL)
    proposal["locations"][0]["known_for"] = known_for
    proposal["scenarios"][0]["setup"] = setup
    return proposal


NO_FACETS = {"umbrella": {"genres": []}, "shared": {}, "extra_genres": {}}
DILEMMA = "and the town has to decide whether to pin the slope or learn to ride it."
TERRACED = "Stone-walled wheat terraces cut into the sea cliffs."


def test_dilemma_ending_is_rejected_when_a_recent_world_used_it():
    complaints = entropy.recent_phrase_rut_complaints(
        _proposal("Anjali Weng has to decide whether the creature is a guest."),
        ["A quiet world. " + DILEMMA],
        NO_FACETS,
    )
    assert len(complaints) == 1
    assert "dilemma ending" in complaints[0]


def test_dilemma_ending_variants_are_all_the_same_rut():
    for text in (
        "she must decide whether duty means matching that pace",
        "A dragon must choose: finish becoming herself the slow way",
        "has one shift to decide whether that means someone kept a promise",
        "has to decide which of the hundred versions counts",
    ):
        assert "decision-dilemma" in entropy.phrase_ruts_in_text(text), text


def test_dilemma_ending_is_allowed_once_it_has_left_the_window():
    stale = ["A world. " + DILEMMA] + ["An unrelated world of kites."] * 5
    assert entropy.recent_phrase_rut_complaints(
        _proposal("Ren decides whether to keep standing."), stale, NO_FACETS
    ) == []


def test_an_event_already_under_way_does_not_trip_the_dilemma_guard():
    assert entropy.recent_phrase_rut_complaints(
        _proposal("By dusk the first lamp is already replaying last night to the street."),
        ["A world. " + DILEMMA],
        NO_FACETS,
    ) == []


def test_terraced_scenery_cools_for_the_longer_lookback():
    recent = [TERRACED] + ["An unrelated world of kites."] * 6
    complaints = entropy.recent_phrase_rut_complaints(
        _proposal("Nobody hurries.", known_for="A country of terraced highland valleys."),
        recent,
        NO_FACETS,
    )
    assert any("terraced hillside" in complaint for complaint in complaints)


def test_a_terrace_facet_is_permission_for_terraced_scenery():
    seeds = {
        "umbrella": {"genres": [{"title": "Rice Paddy Pastoral", "slug": "rice-paddy-pastoral"}]},
        "shared": {},
        "extra_genres": {},
    }
    assert entropy.recent_phrase_rut_complaints(
        _proposal("Nobody hurries.", known_for="Terraced paddies under rain."),
        [TERRACED],
        seeds,
    ) == []


def test_terrace_shelf_and_ledge_place_names_are_a_name_rut():
    for name in ("Landing Terrace", "The Puffin Terraces", "Spore Shelf"):
        complaints = ruts.name_rut_complaints([name], "{}")
        assert any("stepped landform" in complaint for complaint in complaints), name


def test_shelf_furniture_inside_a_compound_name_is_not_the_landform_rut():
    assert ruts.name_rut_complaints(["Lanternrow Shelfyard", "Resin Pantry"], "{}") == []


def test_story_diversity_complaints_reports_the_terrace_name():
    proposal = copy.deepcopy(bdp.SAMPLE_PROPOSAL)
    proposal["locations"][0]["title"] = "Landing Terrace"
    complaints = authoring.story_diversity_complaints(proposal, [], NO_FACETS)
    assert any("stepped landform" in complaint for complaint in complaints)


def test_short_surname_cannot_repeat_verbatim():
    complaints = authoring.name_diversity_complaints(
        "Bereg Voss", ["Linh Voss", "Amara Okafor"]
    )
    assert any("exactly repeats" in complaint for complaint in complaints)


def test_distinct_short_surnames_still_pass():
    assert authoring.name_diversity_complaints("Bereg Tamm", ["Linh Voss"]) == []


def test_brief_names_currently_spent_phrasing(monkeypatch):
    # build_dream_proposal bootstraps the impl under its own module name; patch that one.
    monkeypatch.setitem(
        bdp.build_brief.__globals__, "recent_story_texts", lambda day, **_: ["A world. " + DILEMMA]
    )
    brief = bdp.build_brief("2026-10-08", catalog=None)
    spent = [line for line in brief["instructions"] if line.startswith("SPENT PHRASING")]
    assert len(spent) == 1 and "dilemma ending" in spent[0]
