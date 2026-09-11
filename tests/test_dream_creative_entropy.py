"""Regression coverage for Daily Dream catalog-scale creative entropy."""
from __future__ import annotations

import copy
import json

import scripts.build_dream_proposal as bdp
import scripts.check_dream_creative_contract as creative_contract
from scripts import dream_creative_entropy as entropy


def _facet(title: str, taxonomy: str, *, weight: float = 1.0) -> dict:
    return {
        "title": title,
        "slug": bdp.slugify(title),
        "taxonomy": taxonomy,
        "randomWeight": weight,
    }


def _catalog() -> dict[str, list[dict]]:
    return {
        key: [copy.deepcopy(bdp._fallback(key)[i]) for i in range(len(rows))]
        for key, rows in bdp.FALLBACK_FACETS.items()
    }


def _proposal(idea: str, *, title: str = "Fresh World", seeds: dict | None = None) -> dict:
    proposal = copy.deepcopy(bdp.SAMPLE_PROPOSAL)
    proposal["title"] = title
    proposal["idea"] = idea
    proposal["vibe"]["title"] = title
    proposal["vibe"]["line"] = idea
    proposal["locations"][0]["known_for"] = "A place with an ordinary physical habit."
    proposal["locations"][0]["local_rule"] = "Visitors leave their shoes by the door."
    proposal["locations"][0]["best_scene"] = "A door opens and afternoon light crosses the floor."
    proposal["characters"][0]["role_drive"] = "They want to understand what changed."
    proposal["characters"][0]["complication"] = "They may prefer the changed version."
    proposal["scenarios"][0]["setup"] = (
        f"In {title} at {proposal['locations'][0]['title']}, "
        f"{proposal['characters'][0]['name']} decides what to do next."
    )
    proposal["seed_facets"] = seeds or {"umbrella": {"genres": []}, "shared": {}, "extra_genres": {}}
    return proposal


def _write_proposal(path, proposal: dict) -> None:
    path.write_text(
        "---\nproposal: true\n---\n\n<!-- proposal-data\n"
        + json.dumps(proposal)
        + "\n-->\n",
        encoding="utf-8",
    )


def test_recent_facet_cooldown_prefers_fresh_rows_but_falls_back_for_thin_pool():
    old = _facet("Old Favorite", "THEME")
    fresh = _facet("Fresh Turn", "THEME")

    assert entropy.apply_recent_facet_cooldown([old, fresh], {old["slug"]}) == [fresh]
    assert entropy.apply_recent_facet_cooldown([old], {old["slug"]}) == [old]


def test_recent_facet_slugs_reads_the_curated_sequence(tmp_path):
    backlog = tmp_path / "backlog"
    backlog.mkdir()
    older = _proposal("Old idea")
    older["seed_facets"] = {
        "elements": {
            "vibe": [_facet("Accidental Diplomat", "OCCUPATION")],
            "location": [_facet("Pulse Metal", "MATERIAL")],
        }
    }
    _write_proposal(backlog / "2026-09-01-old.md", older)

    spent = bdp.recent_facet_slugs("2026-09-02", backlog_dir=backlog)

    assert "accidental-diplomat" in spent
    assert "pulse-metal" in spent


def test_seed_plan_avoids_recent_exact_facets_when_each_pool_has_room():
    catalog = _catalog()
    spent = set()
    for taxonomy, rows in catalog.items():
        threshold = 7 if taxonomy == "GENRE" else 1
        if len(rows) > threshold:
            rows[0]["randomWeight"] = 10_000.0
            spent.add(entropy.facet_key(rows[0]))

    plan = bdp.facet_seed_plan(
        "2026-10-01",
        catalog=catalog,
        cooldowns=set(),
        spent_facets=spent,
        saturated_story_families=set(),
    )
    drawn = [
        facet
        for values in plan["elements"].values()
        for facet in values
        if isinstance(facet, dict)
    ]

    for facet in drawn:
        taxonomy = str(facet.get("taxonomy") or "")
        threshold = 7 if taxonomy == "GENRE" else 1
        if taxonomy in catalog and len(catalog[taxonomy]) > threshold:
            assert entropy.facet_key(facet) not in spent
    assert plan["creative_entropy_version"] == entropy.ENTROPY_VERSION


def test_story_core_excludes_reward_costs_from_semantic_rut_scoring():
    proposal = _proposal("A child learns a new dance in an empty gym.")
    proposal["rewards"][0]["catch"] = "A debt is owed and the tally comes due."

    assert "debt-obligation" not in entropy.families_in_text(
        entropy.story_core_text(proposal)
    )


def test_debt_family_only_blocks_after_recent_saturation_and_without_a_drawn_request():
    recent = [
        "A debt diver keeps a running tally of what the wreck still owes.",
        "Every debtor repays an obligation before the old balance comes due.",
    ]
    candidate = _proposal(
        "A village measures every favor as debt, and every debt is tallied until it is owed back."
    )

    complaints = entropy.story_family_complaints(candidate, recent, candidate["seed_facets"])
    assert any("debt / obligation" in complaint for complaint in complaints)

    explicit = {
        "umbrella": {"genres": [_facet("Debt Economy", "GENRE")]},
        "shared": {},
        "extra_genres": {},
    }
    assert entropy.story_family_complaints(candidate, recent, explicit) == []


def test_correspondence_contract_family_cools_after_one_recent_world():
    recent = [
        "A notary witnesses a treaty, and every oath becomes a contract when the signer leaves."
    ]
    candidate = _proposal(
        "A missive contains the missing treaty, and a second contract changes who may sign it."
    )

    complaints = entropy.story_family_complaints(candidate, recent, candidate["seed_facets"])

    assert any("letters / missives / contracts" in complaint for complaint in complaints)


def test_semantic_seed_cooldown_avoids_facets_that_request_a_saturated_family():
    contract = _facet("Contract Notary", "OCCUPATION")
    fresh = _facet("Roof Acrobat", "OCCUPATION")

    assert entropy.apply_semantic_family_cooldown(
        [contract, fresh], {"correspondence-contract"}
    ) == [fresh]
    assert entropy.apply_semantic_family_cooldown(
        [contract], {"correspondence-contract"}
    ) == [contract]


def test_grief_family_detects_different_nouns_for_the_same_emotional_engine():
    recent = [
        "A grief clerk maps every sorrow and every mourner leaves a grief-shaped fold.",
        "Regrets feed the roots until mourning becomes the village's harvest fuel.",
    ]
    candidate = _proposal(
        "The town stores grief in walls, and every mourner must keep mourning to hold the roof up."
    )

    complaints = entropy.story_family_complaints(candidate, recent, candidate["seed_facets"])
    assert any("grief / regret / memory" in complaint for complaint in complaints)


def test_deadline_skeleton_is_rejected_after_three_of_five_recent_worlds_use_it():
    recent = [
        "She has one night to reach the gate.",
        "They have three days before the tower falls.",
        "A pilot has one solar-sail tide before the collectors arrive.",
        "A family learns a song together.",
        "A garden changes color each afternoon.",
    ]
    candidate = _proposal("A courier has one hour before the bridge closes.")

    complaints = entropy.structural_repetition_complaints(
        candidate, recent, candidate["seed_facets"]
    )
    assert any("countdown/deadline" in complaint for complaint in complaints)


def test_deadline_facets_can_request_time_pressure_on_purpose():
    recent = ["One night remains.", "Three days remain.", "A one hour countdown starts."]
    seeds = {
        "umbrella": {"genres": [_facet("Tournament Race", "GENRE")]},
        "shared": {},
        "extra_genres": {},
    }
    candidate = _proposal("A racer has one hour before the final gate closes.", seeds=seeds)

    assert entropy.structural_repetition_complaints(candidate, recent, seeds) == []


def test_the_x_y_title_shape_is_a_hard_creative_guard():
    assert entropy.title_shape_complaints(_proposal("Anything", title="The Drowned Compact"))
    assert entropy.title_shape_complaints(_proposal("Anything", title="The Kindest Bite"))
    assert entropy.title_shape_complaints(_proposal("Anything", title="Feed of the Devouring Choir")) == []
    assert entropy.title_shape_complaints(_proposal("Anything", title="Amberglass")) == []


def test_invented_facets_do_not_persist_a_recent_semantic_rut():
    recent = [
        "A debt diver keeps a running tally of what a wreck owes.",
        "A family repays an old debt before an obligation comes due.",
    ]
    invented = [
        {
            "title": "Debt to No One",
            "slug": "debt-to-no-one",
            "taxonomy": "ALIGNMENT",
            "description": "A vow never to owe another authority a debt again.",
        }
    ]

    complaints = entropy.invented_facet_complaints(invented, recent, [])
    assert any("reusable catalog" in complaint for complaint in complaints)


def test_invented_facets_reject_close_siblings_of_recent_inventions():
    recent_invented = [
        {
            "title": "Compartmented Mourner",
            "description": "Someone who schedules contained bursts of grief because uncontrolled mourning has physical consequences.",
        }
    ]
    candidate = [
        {
            "title": "Scheduled Mourner",
            "description": "Someone who contains mourning in scheduled bursts because uncontrolled grief changes the room around them.",
        }
    ]

    complaints = entropy.invented_facet_complaints(candidate, [], recent_invented)
    assert complaints


def test_new_contract_validation_is_opt_in_so_historical_bundles_do_not_retroactively_break(tmp_path, monkeypatch):
    monkeypatch.setattr(bdp, "BACKLOG", tmp_path)
    legacy = {"date": "2026-10-01", "invent": [], "invented": [{"title": "Debt", "description": "Debt owed."}]}

    assert bdp.validate_inventions(legacy) == []


def test_consumption_contract_rejects_unversioned_queued_proposals():
    stale = {"seed_facets": {}}
    current = {"seed_facets": {"creative_entropy_version": entropy.ENTROPY_VERSION}}

    error = creative_contract._entropy_version_error(stale)

    assert error is not None
    assert "re-author" in error
    assert creative_contract._entropy_version_error(current) is None


def test_build_brief_carries_structural_title_visual_and_invention_contrast():
    brief = bdp.build_brief("2026-10-01", catalog=_catalog())
    joined = "\n".join(brief["instructions"])

    assert brief["seed_facets"]["creative_entropy_version"] == entropy.ENTROPY_VERSION
    assert "THE SCHEMA IS STORAGE SHAPE, NOT PLOT SHAPE" in joined
    assert "STRUCTURAL CONTRAST FOR TODAY:" in joined
    assert "TITLE CONSTRUCTION FOR TODAY:" in joined
    assert "VISUAL CONTRAST FOR TODAY:" in joined
    assert "TITLE SHAPE IS ENFORCED" in joined
    assert "Letters, missives, contracts" in joined
    assert "seeds for FUTURE worlds" in joined


def test_contrast_axes_do_not_rotate_in_lockstep():
    days = [f"2026-10-{day:02d}" for day in range(1, 13)]
    titles = [entropy.title_direction(day) for day in days]
    structures = [entropy.structural_direction(day) for day in days]
    visuals = [entropy.visual_direction(day) for day in days]

    assert len(set(titles)) >= 4
    assert len(set(structures)) >= 4
    assert len(set(visuals)) >= 4
    assert list(zip(titles, structures, visuals)) != [
        (titles[0], structures[0], visuals[0])
    ] * len(days)
