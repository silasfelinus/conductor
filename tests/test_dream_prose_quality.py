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
