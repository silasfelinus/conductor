"""Regression coverage for Daily Dream world-scale theme diversity."""
from __future__ import annotations

import copy
import json

import scripts.author_dream_proposal as authoring
import scripts.build_dream_proposal as bdp
from scripts import dream_theme_diversity as themes


def _facet(title: str, taxonomy: str, slug: str | None = None) -> dict:
    return {
        "title": title,
        "slug": slug or bdp.slugify(title),
        "taxonomy": taxonomy,
        "randomWeight": 1.0,
    }


def _fallback_catalog() -> dict[str, list[dict]]:
    return {
        key: [bdp._fallback(key)[index] for index in range(len(rows))]
        for key, rows in bdp.FALLBACK_FACETS.items()
    }


def _aquatic_proposal() -> dict:
    proposal = copy.deepcopy(bdp.SAMPLE_PROPOSAL)
    proposal["title"] = "The Salt Horizon"
    proposal["idea"] = (
        "A reef settlement follows the tide across an open ocean while coral gates "
        "close behind its last courier."
    )
    proposal["vibe"]["line"] = "The tide moves the whole settlement before dawn."
    proposal["locations"][0]["known_for"] = (
        "Its coral streets sit below the ocean surface whenever the tide turns."
    )
    proposal["locations"][0]["art_direction"] = (
        "A reef settlement of pale coral terraces beneath dark ocean water."
    )
    proposal["scenarios"][0]["setup"] = (
        "In The Kindly Cross-Examination at The Refracted Court, Mara Venn crosses "
        "the reef before the tide seals the coral gate."
    )
    return proposal


def test_aquatic_world_requires_multiple_world_scale_signals():
    assert not themes.is_aquatic_world("An otter drinks from a water bowl beside the road.")
    assert not themes.is_aquatic_world("A storm crosses the sea before breakfast.")
    assert themes.is_aquatic_world(
        "A reef city waits for the tide while coral gates open toward the ocean."
    )


def test_aquatic_creature_is_not_permission_to_make_the_whole_world_aquatic():
    for creature in (
        _facet("Otter", "ANIMAL"),
        _facet("Ocean Sunfish", "ANIMAL"),
        _facet("Marine Dragon", "SPECIES"),
    ):
        seeds = {"elements": {"vibe": [creature]}}
        assert themes.facet_is_aquatic_seed(creature)
        assert not themes.facets_explicitly_request_aquatic_world(seeds)


def test_explicit_aquatic_setting_or_genre_allows_an_aquatic_world():
    for facet in (
        _facet("Oceanic Mythology", "GENRE"),
        _facet("The Big Blue", "SETTING"),
        _facet("Underwater City", "SETTING"),
    ):
        seeds = {"elements": {"vibe": [facet]}}
        assert themes.facets_explicitly_request_aquatic_world(seeds), facet["title"]


def test_seed_cooldown_prefers_non_aquatic_candidates_but_never_breaks_a_draw():
    otter = _facet("Otter", "ANIMAL")
    cassowary = _facet("Cassowary", "ANIMAL")
    cooldowns = {themes.AQUATIC_WORLD_FAMILY}

    assert themes.apply_seed_cooldowns([otter, cassowary], cooldowns) == [cassowary]
    assert themes.apply_seed_cooldowns([otter], cooldowns) == [otter]


def test_proposal_detector_ignores_seed_metadata():
    proposal = copy.deepcopy(bdp.SAMPLE_PROPOSAL)
    proposal["seed_facets"] = {
        "elements": {
            "vibe": [
                _facet("Otter", "ANIMAL"),
                _facet("The Big Blue", "SETTING"),
            ]
        }
    }

    assert not themes.proposal_is_aquatic_world(proposal)


def test_recent_aquatic_world_activates_five_proposal_seed_cooldown(tmp_path):
    backlog = tmp_path / "backlog"
    backlog.mkdir()
    proposal = _aquatic_proposal()
    (backlog / "2026-09-04-salt-horizon.md").write_text(
        "<!-- proposal-data\n" + json.dumps(proposal) + "\n-->\n",
        encoding="utf-8",
    )

    assert bdp.recent_theme_cooldowns(
        "2026-09-05", backlog_dir=backlog
    ) == {themes.AQUATIC_WORLD_FAMILY}


def test_seed_plan_filters_aquatic_facets_during_cooldown_when_alternatives_exist():
    plan = bdp.facet_seed_plan(
        "2026-10-01",
        catalog=_fallback_catalog(),
        cooldowns={themes.AQUATIC_WORLD_FAMILY},
    )
    drawn = [
        facet
        for values in plan["elements"].values()
        for facet in values
        if isinstance(facet, dict)
    ]

    assert not any(themes.facet_is_aquatic_seed(facet) for facet in drawn)


def test_author_rejects_repeated_gratuitous_aquatic_world_from_an_otter_seed():
    recent = [
        "A reef city follows the tide across the ocean while coral gates close behind it."
    ]
    complaints = authoring.story_diversity_complaints(
        _aquatic_proposal(),
        recent,
        {"elements": {"vibe": [_facet("Otter", "ANIMAL")]}}
    )

    assert any("aquatic-world motif" in complaint for complaint in complaints)


def test_author_allows_isolated_aquatic_world_when_recent_history_is_dry():
    complaints = authoring.story_diversity_complaints(
        _aquatic_proposal(),
        ["A desert observatory negotiates with migrating glass moths at noon."],
        {"elements": {"vibe": [_facet("Otter", "ANIMAL")]}}
    )

    assert not any("aquatic-world motif" in complaint for complaint in complaints)


def test_author_allows_aquatic_world_when_oceanic_genre_requests_it():
    recent = [
        "A reef city follows the tide across the ocean while coral gates close behind it."
    ]
    complaints = authoring.story_diversity_complaints(
        _aquatic_proposal(),
        recent,
        {"elements": {"vibe": [_facet("Oceanic Mythology", "GENRE")]}}
    )

    assert not any("aquatic-world motif" in complaint for complaint in complaints)


def test_system_prompt_says_aquatic_creature_does_not_define_world_biome():
    prompt = authoring.SYSTEM_PROMPT.casefold()
    assert "aquatic animal or species facet constrains the creature" in prompt
    assert "not the whole world's" in prompt
