import copy

import scripts.author_dream_proposal as author
import scripts.build_dream_proposal as proposals
from scripts import dream_prose_quality as prose


def _quality_sample():
    proposal = copy.deepcopy(proposals.SAMPLE_PROPOSAL)
    proposal["idea"] = (
        "A courthouse turns every spoken testimony into living color, forcing witnesses "
        "to confront what their answers physically change."
    )
    proposal["vibe"]["line"] = (
        "Every answer changes the room that asked it, so truth becomes architecture."
    )
    proposal["locations"][0].update(
        known_for=(
            "Its prismatic chambers turn spoken testimony into color that stains the walls "
            "until each case is settled."
        ),
        local_rule=(
            "No witness may repeat a hue after their testimony has changed it."
        ),
        best_scene=(
            "A disputed childhood memory turns the courtroom black while every exit "
            "quietly moves to a new wall."
        ),
    )
    proposal["scenarios"][0]["setup"] = (
        "In The Kindly Cross-Examination at The Refracted Court, Mara Venn defends an "
        "engineered witness while the chamber changes color around every disputed answer."
    )
    return proposal


def test_user_facing_prose_accepts_complete_explanatory_copy():
    assert prose.complaints(_quality_sample()) == []


def test_sharp_complete_vibe_line_can_stay_short():
    proposal = _quality_sample()
    proposal["vibe"]["line"] = "The storm only spares the block that out-sings it."

    assert not any("vibe.line" in problem for problem in prose.complaints(proposal))


def test_user_facing_prose_rejects_monsoon_static_style_fragments():
    proposal = _quality_sample()
    proposal["locations"][0].update(
        known_for="rooftop stages wired straight into the flood barriers",
        local_rule="the loudest verse gets the power",
        best_scene="the surge climbs the stairwell while the mast crew hauls glowing silk line back up hand over hand",
    )

    problems = prose.complaints(proposal)

    assert any("known_for is too terse" in problem for problem in problems)
    assert any("known_for must begin" in problem for problem in problems)
    assert any("known_for must end" in problem for problem in problems)
    assert any("local_rule is too terse" in problem for problem in problems)
    assert any("best_scene must end" in problem for problem in problems)


def test_story_diversity_contract_includes_prose_quality_gate(monkeypatch):
    proposal = _quality_sample()
    proposal["locations"][0]["known_for"] = "rooftop stages wired straight into the flood barriers"
    monkeypatch.setattr(author.ruts, "name_rut_complaints", lambda names, facets: [])

    problems = author.story_diversity_complaints(proposal, [], proposal["seed_facets"])

    assert any("known_for is too terse" in problem for problem in problems)


def test_canonical_sample_proposal_satisfies_the_contract_it_documents():
    # The --sample fixture is the worked example of the card-copy contract, so it
    # must not itself be the telegraphic style the gate exists to reject.
    assert prose.complaints(proposals.SAMPLE_PROPOSAL) == []


def test_character_fields_are_card_copy_and_reject_stem_completion_fragments():
    # The 2026-08-16 bundle shipped "keep her cactus herd calm through the quakes
    # so the circus can perform" as a character's whole digest summary: the field
    # was written to complete "**Name** — ", not to be read on its own.
    proposal = _quality_sample()
    proposal["characters"][0].update(
        role_drive="keep her cactus herd calm through the quakes",
        carries="a coil of dragon-scale rope",
        complication="her herd is bred from the last wild line",
    )

    problems = prose.complaints(proposal)

    assert any("characters[0].role_drive must begin" in problem for problem in problems)
    assert any("characters[0].role_drive must end" in problem for problem in problems)
    assert any("characters[0].carries is too terse" in problem for problem in problems)
    assert any("characters[0].complication must begin" in problem for problem in problems)


def test_reward_fields_are_card_copy_and_reject_stem_completion_fragments():
    proposal = _quality_sample()
    for reward in proposal["rewards"]:
        reward.update(
            grants="reveals omissions",
            best_used_when="a story is too neat",
            catch="it reveals yours",
        )

    problems = prose.complaints(proposal)

    for label in ("item", "skill"):
        assert any(f"rewards[{label}].grants is too terse" in p for p in problems)
        assert any(f"rewards[{label}].best_used_when must begin" in p for p in problems)
        assert any(f"rewards[{label}].catch must end" in p for p in problems)


def test_art_prompt_fields_stay_exempt_from_the_sentence_contract():
    # `look` and `art_direction` feed Krea and are supposed to be visual noun
    # phrases; forcing them into sentences would degrade the render prompts.
    proposal = _quality_sample()
    proposal["characters"][0]["look"] = "mantis-shrimp advocate in a midnight suit"
    proposal["locations"][0]["art_direction"] = "prismatic courtroom"

    problems = prose.complaints(proposal)

    assert not any("look" in problem for problem in problems)
    assert not any("art_direction" in problem for problem in problems)
