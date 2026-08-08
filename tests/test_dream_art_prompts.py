"""Regression tests for the Krea 2 daily-dream prompt builder.

The bug these guard against (2026-08-08): a Reward named "Tidefortune Ladle"
rendered as a crowd of fifteen people. Every prompt carried an unconditional
"cast characters naturally across many species, ages, body sizes..." clause,
which Krea 2 reads as subject matter rather than guidance.
"""
import importlib.util
import pathlib
import sys

import pytest

SCRIPTS = pathlib.Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location(
    "dream_art_prompts", SCRIPTS / "dream_art_prompts.py")
dap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dap)


LADLE = dict(
    name="Tidefortune Ladle",
    reward_type="ITEM",
    look=("a dented tin ladle the length of a forearm, bowl worn to mirror-bright, "
          "handle wrapped in salt-stiffened cord"),
    grants="stirred through any dish, it surfaces the hidden fortune buried in a person or object",
    rarity="RARE",
    world_title="The Lucky Ladle",
    vibe_line="Every bowl tastes like a fate someone else was supposed to have.",
)

SEASONING = dict(
    name="Nanite Seasoning",
    reward_type="SKILL",
    look="a pinch of grey dust suspended mid-fall over a steaming bowl, each mote lit from within",
    grants="reprogram edible nanites on the fly to season a meal toward any outcome you choose",
    rarity="UNCOMMON",
    world_title="The Lucky Ladle",
    vibe_line="Every bowl tastes like a fate someone else was supposed to have.",
)


def test_item_prompt_leads_with_the_object_not_its_function():
    prompt = dap.reward_prompt(**LADLE)
    # The subject must be the first thing Krea 2 reads.
    assert prompt.startswith("a single Tidefortune Ladle, one object alone in frame")
    # Physical description arrives before the abstract effect.
    assert prompt.index("dented tin ladle") < prompt.index("hidden fortune")


@pytest.mark.parametrize("reward", [LADLE, SEASONING], ids=["item", "skill"])
def test_reward_prompts_never_request_a_cast(reward):
    prompt = dap.reward_prompt(**reward)
    assert dap.CAST_DIRECTION not in prompt
    assert "cast the figures" not in prompt


def test_item_prompt_states_the_frame_is_empty_of_people():
    assert dap.UNPEOPLED in dap.reward_prompt(**LADLE)


def test_skill_prompt_makes_the_effect_the_subject_and_bans_full_figures():
    prompt = dap.reward_prompt(**SEASONING)
    assert prompt.startswith("Nanite Seasoning, a single practiced technique caught mid-use")
    assert "no full figure" in prompt
    assert "no onlookers" in prompt


def test_skill_prompt_survives_a_legacy_proposal_with_no_look_field():
    prompt = dap.reward_prompt(**{**SEASONING, "look": ""})
    # Without `look` the builder must still anchor on the effect, never a person.
    assert "the visible signature of the technique in mid-use" in prompt
    assert dap.CAST_DIRECTION not in prompt


def test_character_prompt_is_the_one_reward_free_case_that_wants_a_single_figure():
    prompt = dap.character_prompt(
        "Perrin Voss", "a bog-punk chorister in a patched oilcloth cassock",
        "translate a hymnal that keeps rewriting itself", "a warped brass tuning fork",
        "Choir of the Drowned Kingdom", "Ancient sea-gods drift like slow leviathans.")
    assert prompt.startswith("character portrait of Perrin Voss")
    assert "single figure" in prompt
    # A portrait is one person; a diversity cast clause here would add a crowd.
    assert dap.CAST_DIRECTION not in prompt


def test_only_scenario_prompt_injects_cast_direction():
    scenario = dap.scenario_prompt(
        "The Second Verse", "a congregation hums back from below",
        "The Sunken Cantata", "Choir of the Drowned Kingdom", "Sea-gods sing.")
    world = dap.world_prompt(
        "Choir of the Drowned Kingdom", "A submerged kingdom sings.",
        "Sea-gods sing.", "a submerged amphitheater of coral columns")
    location = dap.location_prompt(
        "The Sunken Cantata", "a submerged amphitheater of coral columns",
        "drowned acoustics", "a hymn unravels a listener",
        "Choir of the Drowned Kingdom", "Sea-gods sing.")
    assert dap.CAST_DIRECTION in scenario
    assert dap.CAST_DIRECTION not in world
    assert dap.CAST_DIRECTION not in location


def test_world_prompt_keeps_the_setting_as_subject():
    prompt = dap.world_prompt(
        "Choir of the Drowned Kingdom", "A submerged kingdom sings.",
        "Sea-gods sing.", "a submerged amphitheater of coral columns")
    assert "the setting is the subject" in prompt
    assert "any figures present are incidental" in prompt


def test_location_prompt_keeps_figures_incidental_to_the_architecture():
    prompt = dap.location_prompt(
        "The Sunken Cantata", "a submerged amphitheater of coral columns",
        "drowned acoustics", "a hymn unravels a listener",
        "Choir of the Drowned Kingdom", "Sea-gods sing.")
    assert "the environment is the subject" in prompt
    assert "figures present are small and incidental" in prompt
    assert dap.CAST_DIRECTION not in prompt


def test_no_builder_emits_the_phrase_that_triggered_the_house_substitution():
    """`replaceVagueArtDirection` in kind_robots swaps this phrase for a block
    containing the casting instruction. No prompt may contain it."""
    prompts = [
        dap.reward_prompt(**LADLE),
        dap.reward_prompt(**SEASONING),
        dap.character_prompt("A", "b", "c", "d", "W", "v"),
        dap.location_prompt("A", "b", "c", "d", "W", "v"),
        dap.scenario_prompt("A", "b", "c", "W", "v"),
        dap.world_prompt("W", "i", "v", "a"),
    ]
    for prompt in prompts:
        assert "Kind Robots" not in prompt
        assert dap.STYLE in prompt
        assert dap.NO_TEXT in prompt
        assert len(prompt) <= dap.MAX_PROMPT_CHARS


def test_prompts_are_capped_at_a_clause_boundary():
    prompt = dap.reward_prompt(**{**LADLE, "look": "brass. " + ("very ornate " * 400)})
    assert len(prompt) <= dap.MAX_PROMPT_CHARS
    assert not prompt.endswith(",")


def test_item_prompt_does_not_double_the_article_on_a_the_name():
    """"a single The Corsair's Encore" reads as noise to a caption-trained encoder."""
    prompt = dap.reward_prompt(**{**LADLE, "name": "The Corsair's Encore"})
    assert prompt.startswith("The Corsair's Encore, one object alone in frame")
    assert "a single The" not in prompt
