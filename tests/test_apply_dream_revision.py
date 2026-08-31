from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import apply_dream_revision as revision  # noqa: E402


def facet(title: str, slug: str, taxonomy: str) -> dict:
    return {"title": title, "slug": slug, "taxonomy": taxonomy, "randomWeight": 1.0}


def seed_facets() -> dict:
    low = facet("Low Fantasy", "low-fantasy", "GENRE")
    magical = facet("Magical Girl", "magical-girl", "GENRE")
    creature = facet("Sea Cucumber", "sea-cucumber", "ANIMAL")
    occupation = facet("Amazonian Scout", "amazonian-scout", "OCCUPATION")
    material = facet("Demonic Bone", "demonic-bone", "MATERIAL")
    personality = facet("Serious", "serious", "PERSONALITY")
    cozy = facet("Cozy Mystery", "cozy-mystery", "GENRE")
    scifi = facet("Sci-Fi", "sci-fi", "GENRE")
    vampire = facet("Vampire Gothic", "vampire-gothic", "GENRE")
    folk = facet("Folk Fantasy", "folk-fantasy", "GENRE")
    pastoral = facet("Revolutionary Pastoral", "revolutionary-pastoral", "GENRE")
    return {
        "version": 2,
        "date": "2026-08-26",
        "deterministic_seed": 42,
        "catalog_source": "test",
        "umbrella": {
            "genres": [low, magical],
            "creature": creature,
            "wildcard": occupation,
            "wildcard_role": "occupation",
        },
        "shared": {"material": material, "personality": personality},
        "extra_genres": {
            "location": cozy,
            "character": scifi,
            "reward_item": vampire,
            "reward_skill": folk,
            "scenario": pastoral,
        },
        "elements": {
            "vibe": [low, magical, creature, occupation],
            "location": [low, magical, cozy, creature, material],
            "character": [low, magical, scifi, creature, occupation, personality],
            "reward_item": [low, magical, vampire, material],
            "reward_skill": [low, magical, folk, occupation],
            "scenario": [low, magical, pastoral, cozy, scifi, creature],
        },
    }


def proposal() -> dict:
    seeds = seed_facets()
    return {
        "title": "Six Minutes of Dry Ocean",
        "slug": "tide-ledger-miracles",
        "idea": "At impossible low tide, a transformed scout races a returning wall of sea to relight a stranded village beacon.",
        "vibe": {
            "title": "Starwake Scouts",
            "line": "Transformation is a flare fired directly into hostile weather.",
            "art_direction": "A tide-light scout standing on exposed seabed as a silver wall of ocean rises behind her.",
        },
        "locations": [
            {
                "title": "The Boneglass Reach",
                "known_for": "A seabed road appears for six minutes whenever impossible low tide exposes the reach.",
                "local_rule": "Follow the sea cucumbers whenever the horizon suddenly goes silent.",
                "best_scene": "The returning ocean rises into a vertical wall beyond the final beacon on the road.",
                "art_direction": "Black demonic-bone ribs arch over wet mirror-bright sand while luminous sea cucumbers form a winding trail.",
            }
        ],
        "characters": [
            {
                "name": "Tessa Nunes",
                "role_drive": "She has to relight the far reef beacon before the returning sea cuts off the village.",
                "carries": "A folding prism spear built from salvaged survey technology hangs at her back.",
                "complication": "Her tide-light transformation lasts only ninety seconds and attracts every deep-water hunter nearby.",
                "look": "A serious river scout in weathered field gear transformed into layered pearl-white tide armor with a translucent cape.",
            }
        ],
        "rewards": [
            {
                "name": "Nightheart Lantern",
                "reward_type": "ITEM",
                "rarity": "RARE",
                "grants": "It stores one burst of moonlight powerful enough to relight a dead beacon.",
                "best_used_when": "Use it when the coast has gone completely dark.",
                "catch": "Every nearby shadow keeps moving for a minute after the light is spent.",
                "look": "A palm-sized lantern carved from glossy black bone, with a cold violet flame suspended inside a hollow rib cage.",
            },
            {
                "name": "River-Under-Sea",
                "reward_type": "SKILL",
                "rarity": "UNCOMMON",
                "grants": "It reads hidden currents through the pressure changes underfoot.",
                "best_used_when": "Use it when crossing exposed or flooded terrain with no visible trail.",
                "catch": "Living movement and rushing water come to feel exactly alike.",
                "look": "Concentric pale-blue ripples spread from each footfall and bend around unseen channels beneath the sand.",
            },
        ],
        "scenarios": [
            {
                "title": "The Returning Wall",
                "setup": "In Starwake Scouts at The Boneglass Reach, Tessa Nunes sprints the last exposed kilometer as the cliffside commune hand-lights a chain of mirrors and the returning ocean wakes a buried sci-fi beacon predator beneath her feet.",
            }
        ],
        "seed_facets": seeds,
    }


def test_revision_rejects_changed_seed_facets() -> None:
    old = proposal()
    new = copy.deepcopy(old)
    new["seed_facets"]["deterministic_seed"] = 99
    with pytest.raises(ValueError, match="preserve seed_facets exactly"):
        revision.validate_revision(
            old,
            new,
            "2026-08-26",
            built=False,
            premise_history=[],
            name_history={"characters": []},
        )


def test_built_revision_preserves_technical_slug() -> None:
    old = proposal()
    new = copy.deepcopy(old)
    new["slug"] = "different-slug"
    with pytest.raises(ValueError, match="technical world slug"):
        revision.validate_revision(
            old,
            new,
            "2026-08-26",
            built=True,
            premise_history=[],
            name_history={"characters": []},
        )


def test_revision_rejects_unrequested_ledger_rut() -> None:
    old = proposal()
    new = copy.deepcopy(old)
    new["idea"] = "A magical ledger controls the coast while clerks file every miracle."
    new["locations"][0]["known_for"] = "its enormous supernatural ledger"
    with pytest.raises(ValueError, match="bureaucracy/record-keeping"):
        revision.validate_revision(
            old,
            new,
            "2026-08-26",
            built=False,
            premise_history=[],
            name_history={"characters": []},
        )


def test_valid_revision_passes_creative_guard() -> None:
    candidate = proposal()
    revision.validate_revision(
        candidate,
        copy.deepcopy(candidate),
        "2026-08-26",
        built=True,
        premise_history=[],
        name_history={"characters": []},
    )


def test_built_source_keeps_built_data_and_marks_revision() -> None:
    candidate = proposal()
    built = {
        "built_at": "2026-08-27T14:00:00+00:00",
        "records": {"world": {"id": 1, "title": "Old"}},
        "art": [],
    }
    rendered = revision._render_source(candidate, "2026-08-26", built_data=built)
    assert "status: built" in rendered
    assert "| revised | creative reset after human feedback" in rendered
    block = revision._data_block(rendered, "built-data")
    assert block is not None
    assert block["records"]["world"]["id"] == 1
