"""creation_burst.py bundle shapes: the classic single-character burst and the
party shape (`characters:` + `locations:`, rewards and scenario optional)."""

import pytest

import scripts.creation_burst as burst


def classic_bundle():
    return {
        "slug": "ferrywake",
        "title": "Ferrywake",
        "vibe": "Every crossing takes exactly as long as the story told aboard.",
        "character": {"name": "Ambrose Quillfeather", "look": "a tall grey heron-folk man"},
        "rewards": [
            {"name": "The Short-Story Oar", "reward_type": "ITEM", "look": "a pale ash oar"},
            {"name": "Cliffhanger Mooring", "reward_type": "SKILL", "look": "a ferry held mid-river"},
        ],
        "scenario": {"title": "The Crossing With No Ending", "setup": "A passenger begins a story with no ending."},
    }


def party_bundle():
    return {
        "slug": "tom-tomtum",
        "title": "Tom Tomtum and the Long Quiet",
        "vibe": "A rock gnome monk finally goes out to see the world.",
        "designer": "silasfelinus",
        "creation_source": "hybrid",
        "locations": [
            {
                "title": "The Monastery of the Long Quiet",
                "known_for": "It keeps sixteen hours of silence a day.",
                "local_rule": "The evening bell is the last sound until morning.",
                "best_scene": "A small gnome ran screaming down the terrace steps.",
                "art_direction": "a mountain monastery of pale stone terraces",
            }
        ],
        "characters": [
            {
                "name": "Tom Tomtum",
                "class": "Monk",
                "level": 3,
                "luck": "epic",
                "art_prompt": "a small rock gnome meditating on the back of a giant turtle, watching a butterfly",
            },
            {"name": "DeeDum", "look": "an enormous very old turtle"},
        ],
    }


def test_classic_bundle_keeps_its_legacy_keys():
    shape = burst.normalize_bundle(classic_bundle())
    assert shape["legacy_character"] is True
    assert [c["name"] for c in shape["characters"]] == ["Ambrose Quillfeather"]
    assert shape["locations"] == []
    assert shape["designer"] == burst.DESIGNER
    assert shape["creation_source"] == "AI"
    keys = set(burst.bundle_prompts(classic_bundle()))
    assert keys == {"character", "scenario", "reward:the-short-story-oar", "reward:cliffhanger-mooring"}


def test_party_bundle_lists_every_record_without_rewards_or_scenario():
    shape = burst.normalize_bundle(party_bundle())
    assert shape["legacy_character"] is False
    assert [c["name"] for c in shape["characters"]] == ["Tom Tomtum", "DeeDum"]
    assert shape["rewards"] == [] and shape["scenario"] is None
    assert shape["designer"] == "silasfelinus"
    assert shape["creation_source"] == "HYBRID"
    keys = set(burst.bundle_prompts(party_bundle()))
    assert keys == {"character:tom-tomtum", "character:deedum", "location:the-monastery-of-the-long-quiet"}


def test_art_prompt_override_leads_and_still_gets_the_house_tail():
    prompt = burst.bundle_prompts(party_bundle())["character:tom-tomtum"]
    assert prompt.startswith("a small rock gnome meditating on the back of a giant turtle")
    assert "character portrait" not in prompt
    assert "set in the world of Tom Tomtum and the Long Quiet" in prompt
    assert prompt.endswith(burst.prompts.NO_TEXT)
    # The character without an override keeps the portrait builder.
    assert burst.bundle_prompts(party_bundle())["character:deedum"].startswith("character portrait of DeeDum")


def test_character_body_carries_stats_level_and_links():
    ch = party_bundle()["characters"][0]
    body = burst.character_body(ch, "prompt", "silasfelinus", [], [42])
    assert body["level"] == 3 and body["luck"] == "EPIC" and body["class"] == "Monk"
    assert body["dreamIds"] == [42] and body["designer"] == "silasfelinus"
    assert "might" not in body and "species" not in body


def test_location_body_is_a_location_dream_with_prose_description():
    loc = party_bundle()["locations"][0]
    body = burst.location_body(loc, "prompt", "silasfelinus", "HYBRID")
    assert body["dreamType"] == "LOCATION" and body["creationSource"] == "HYBRID"
    assert body["description"].startswith("It keeps sixteen hours") and body["description"].endswith("terrace steps.")
    assert body["flavorText"] == "The evening bell is the last sound until morning."
    assert body["icon"] == "kind-icon:map-pin"


@pytest.mark.parametrize(
    "mutate, message",
    [
        (lambda b: b.pop("characters") and b.pop("locations"), "at least one"),
        (lambda b: b["characters"][1].pop("look"), "needs a visual `look` or an `art_prompt`"),
        (lambda b: b["locations"][0].pop("art_direction"), "needs an `art_direction` or an `art_prompt`"),
        (lambda b: b["characters"][0].__setitem__("luck", "mythic"), "luck must be one of"),
        (lambda b: b.__setitem__("creation_source", "magic"), "creation_source must be one of"),
        (lambda b: b.__setitem__("rewards", [{"name": "Only One", "reward_type": "ITEM", "look": "x"}]), "exactly one ITEM and one SKILL"),
    ],
)
def test_party_bundle_validation(mutate, message):
    bundle = party_bundle()
    mutate(bundle)
    with pytest.raises(ValueError, match=message):
        burst.normalize_bundle(bundle)


def test_facet_collections_cover_location_dreams():
    assert burst.FACET_COLLECTIONS["dream"] == "dreams"
