"""Regression tests for the Krea 2 Daily Dream prompt builder."""
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
    assert prompt.startswith("a single Tidefortune Ladle, one object alone")
    assert prompt.index("dented tin ladle") < prompt.index("hidden fortune")


@pytest.mark.parametrize("reward", [LADLE, SEASONING], ids=["item", "skill"])
def test_reward_prompts_never_request_a_cast(reward):
    prompt = dap.reward_prompt(**reward)
    assert dap.CAST_DIRECTION not in prompt
    assert "cast the figures" not in prompt


def test_item_prompt_states_the_frame_is_empty_of_people():
    assert dap.UNPEOPLED in dap.reward_prompt(**LADLE)


def test_skill_prompt_makes_the_effect_the_subject_and_crops_out_the_figure():
    """The effect is the subject and the figure is CROPPED OUT, not forbidden.

    This test used to assert `"no full figure" in prompt` and `"no onlookers"
    in prompt` -- it certified the bug. Krea 2 runs at cfg 1, where the
    ComfyUI negative prompt is inert, so those three people nouns landed in
    positive conditioning and it drew them. A test that pins the exact wording
    of an exclusion is a test that keeps the exclusion alive.
    """
    prompt = dap.reward_prompt(**SEASONING)
    assert prompt.startswith("Nanite Seasoning, a single practiced technique caught mid-use")
    assert "cropped close" in prompt
    assert "one pair of hands enters at the very edge" in prompt
    for banned in ("no full figure", "no faces", "no onlookers"):
        assert banned not in prompt, f"{banned!r} commissions what it names on a cfg-1 engine"


def test_skill_prompt_survives_a_legacy_proposal_with_no_look_field():
    prompt = dap.reward_prompt(**{**SEASONING, "look": ""})
    assert "the visible signature of the technique in mid-use" in prompt
    assert dap.CAST_DIRECTION not in prompt


def test_character_prompt_is_single_figure_without_cast_injection():
    prompt = dap.character_prompt(
        "Perrin Voss", "a bog-punk chorister in a patched oilcloth cassock",
        "translate a hymnal that keeps rewriting itself", "a warped brass tuning fork",
        "Choir of the Drowned Kingdom", "Ancient sea-gods drift like slow leviathans.")
    assert prompt.startswith("character portrait of Perrin Voss")
    assert "single figure" in prompt
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
    """The landscape leads, stated as a fact about the frame.

    This used to assert "any figures present are incidental to the place".
    That is a conditional -- Krea can no more evaluate "present" than it can
    evaluate "no" -- and because the phrase carries no leading when/if,
    artPromptContract's CONDITIONAL_PATTERNS never matched it. 103 dream
    records shipped it past every check (2026-09-20), found by looking at
    pictures rather than by any gate.
    """
    prompt = dap.world_prompt(
        "Choir of the Drowned Kingdom", "A submerged kingdom sings.",
        "Sea-gods sing.", "a submerged amphitheater of coral columns")
    assert "an expansive landscape" in prompt
    assert "distant figures near the horizon giving it scale" in prompt
    # The intent survives; the condition must not come back.
    assert "any figures present" not in prompt
    assert "only for scale" not in prompt


def test_location_prompt_keeps_figures_incidental_to_the_architecture():
    prompt = dap.location_prompt(
        "The Sunken Cantata", "a submerged amphitheater of coral columns",
        "drowned acoustics", "a hymn unravels a listener",
        "Choir of the Drowned Kingdom", "Sea-gods sing.")
    assert "expansive architecture" in prompt
    assert "distant figures near the horizon giving it scale" in prompt
    assert "any figures present" not in prompt
    assert "only for scale" not in prompt
    assert dap.CAST_DIRECTION not in prompt


def _all_prompt_kinds(world_title="Choir of the Drowned Kingdom"):
    vibe = "Sea-gods sing."
    return [
        dap.reward_prompt(**{**LADLE, "world_title": world_title, "vibe_line": vibe}),
        dap.reward_prompt(**{**SEASONING, "world_title": world_title, "vibe_line": vibe}),
        dap.character_prompt("A", "b", "c", "d", world_title, vibe),
        dap.location_prompt("A", "b", "c", "d", world_title, vibe),
        dap.scenario_prompt("A", "b", "c", world_title, vibe),
        dap.world_prompt(world_title, "i", vibe, "a"),
    ]


def test_no_builder_emits_the_phrase_that_triggered_house_substitution():
    for prompt in _all_prompt_kinds():
        assert "Kind Robots" not in prompt
        assert dap.NO_TEXT in prompt
        assert len(prompt) <= dap.MAX_PROMPT_CHARS


def test_every_asset_in_one_world_uses_the_same_selected_style():
    world = "Choir of the Drowned Kingdom"
    selected = dap.style_for_world(world)
    assert selected in dap.STYLE_DIRECTIONS
    for prompt in _all_prompt_kinds(world):
        assert selected in prompt
        assert sum(style in prompt for style in dap.STYLE_DIRECTIONS) == 1


def test_world_style_selection_is_stable_across_rebuilds():
    assert dap.style_for_world("A City Made of Thunder") == dap.style_for_world("A City Made of Thunder")


def test_many_worlds_actually_span_the_style_bank():
    styles = {
        dap.style_for_world(f"Portal World {index}: {index * 7919}")
        for index in range(64)
    }
    assert len(styles) >= 8


def test_style_bank_contains_materially_different_media_not_one_house_style():
    joined = " ".join(dap.STYLE_DIRECTIONS).lower()
    for medium in ("superhero-comic", "charcoal", "gouache", "stop-motion", "risograph",
                   "photorealism", "stained-glass", "paper-cut"):
        assert medium in joined
    assert len(dap.STYLE_DIRECTIONS) >= 10


def test_prompts_are_capped_at_a_clause_boundary():
    prompt = dap.reward_prompt(**{**LADLE, "look": "brass. " + ("very ornate " * 400)})
    assert len(prompt) <= dap.MAX_PROMPT_CHARS
    assert not prompt.endswith(",")


def test_item_prompt_does_not_double_the_article_on_a_the_name():
    prompt = dap.reward_prompt(**{**LADLE, "name": "The Corsair's Encore"})
    assert prompt.startswith("The Corsair's Encore, one object alone")
    assert "a single The" not in prompt


@pytest.mark.parametrize("prompt_fn", [
    lambda: dap.reward_prompt(**LADLE),
    lambda: dap.reward_prompt(**SEASONING),
    lambda: dap.character_prompt("A", "b", "c", "d", "W", "v"),
    lambda: dap.location_prompt("A", "b", "c", "d", "W", "v"),
    lambda: dap.scenario_prompt("A", "b", "c", "W", "v"),
    lambda: dap.world_prompt("W", "i", "v", "a"),
], ids=["item", "skill", "character", "location", "scenario", "world"])
def test_no_builder_asks_for_a_card(prompt_fn):
    assert "card" not in prompt_fn().lower()


def test_the_text_direction_names_no_text_at_all():
    """Describe the surface; never name what must not be on it.

    This asserted `NO_TEXT.lower().count("text") == 1` -- "say it once" rather
    than "do not say it". One is still one more than zero on a Qwen-lineage
    model running at cfg 1, where the negative prompt is inert and every noun
    in the positive prompt is a candidate to draw.
    """
    for banned in ("text", "lettering", "logo", "logos", "watermark", "signature", "caption"):
        assert banned not in dap.NO_TEXT.lower(), (
            f"{banned!r} in the text direction is an order for {banned}"
        )
    assert dap.NO_TEXT, "the direction still has to say what the surface looks like"


def test_the_unpeopled_direction_names_no_people_at_all():
    """The 2026-08-08 anti-crowd clause was itself a cast list.

    "an unpeopled frame, the subject stands alone with no bystanders, no
    onlookers, and no crowd" is three people nouns in positive conditioning.
    It is why Rewards kept rendering as crowds for six weeks after the sweep
    that was supposed to stop it.
    """
    import re

    text = dap.UNPEOPLED.lower()
    # Word-boundary matching, because "unpeopled" is the one word that carries
    # the intent without naming anyone -- a substring check finds "people"
    # inside it and rejects the correct answer.
    for banned in ("bystanders?", "onlookers?", "crowds?", "figures?", "faces?", "persons?", "people"):
        assert not re.search(rf"\b{banned}\b", text), (
            f"{banned!r} in the unpeopled direction is an order for it"
        )
    assert "unpeopled" in text


def test_generated_directions_do_not_request_frames_or_pictures():
    import re

    prompts = _all_prompt_kinds() + list(dap.TREATMENTS)
    for prompt in prompts:
        assert not re.search(r"\b(?:frame|picture)\b", prompt, re.I), prompt
    assert "close-up" in dap.character_prompt("A", "b", "c", "d", "World", "Sea-gods sing.")
    assert "wrists cropped tightly" in dap.reward_prompt(**SEASONING)
