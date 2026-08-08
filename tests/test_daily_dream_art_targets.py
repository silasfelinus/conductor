import textwrap

import yaml

from scripts import build_dream_records as builder


def same_title_bundle():
    return {
        "title": "The Lantern Post",
        "idea": "A patient beacon where travelers trade memories for directions.",
        "vibe": {
            "title": "Warm nocturne",
            "line": "amber lanterns, blue dusk, and hand-built wayfinding",
        },
        "locations": [
            {
                "title": "The Lantern Post",
                "known_for": "a thousand tiny route markers",
                "local_rule": "leave one direction for the next traveler",
                "best_scene": "the beacon waking at dusk",
                "art_direction": "a ramshackle lantern tower at blue hour",
            }
        ],
        "characters": [
            {
                "name": "Mara Wick",
                "role_drive": "keeps lost travelers moving",
                "complication": "forgets a road each time she teaches it",
                "carries": "a brass route wheel",
                "look": "weathered courier with a coat full of tiny lanterns",
            }
        ],
        "rewards": [
            {
                "name": "Borrowed Compass",
                "reward_type": "ITEM",
                "rarity": "UNCOMMON",
                "grants": "reveals the safest nearby path",
                "catch": "it points home only once",
            },
            {
                "name": "Lantern Reading",
                "reward_type": "SKILL",
                "rarity": "RARE",
                "grants": "reads old travel intent from a flame",
                "catch": "the flame remembers your own detours too",
            },
        ],
        "scenarios": [
            {
                "title": "The Road With No Marker",
                "setup": "A familiar road arrives without a destination sign.",
            }
        ],
    }


def parse_requests(entries):
    document = yaml.safe_load(
        "requests:\n" + textwrap.indent("".join(entries), "  ")
    )
    return document["requests"]


def test_same_title_world_and_location_get_distinct_art_identities():
    built, _results, entries = builder.build_records(
        same_title_bundle(), "lantern-post", "2026-08-08", True
    )
    requests = parse_requests(entries)

    assert len(requests) == 6
    assert len({row["id"] for row in requests}) == 6
    assert len({row["image_path"] for row in requests}) == 6

    ids = {row["id"] for row in requests}
    assert "dream-cycle-lantern-post-lantern-post" in ids
    assert "dream-cycle-lantern-post-lantern-post-location" in ids

    paths = {row["image_path"] for row in requests}
    assert "public/images/dreams/lantern-post/lantern-post-card.webp" in paths
    assert (
        "public/images/dreams/lantern-post/lantern-post-location-card.webp"
        in paths
    )

    assert len({row["request_id"] for row in built["art"]}) == 6


def test_every_daily_dream_request_carries_atomic_entity_target():
    _built, _results, entries = builder.build_records(
        same_title_bundle(), "lantern-post", "2026-08-08", True
    )
    requests = parse_requests(entries)

    assert {row["entity_type"] for row in requests} == {
        "dream",
        "character",
        "reward",
        "scenario",
    }
    assert all(row["entity_field"] == "imagePath" for row in requests)
    # Dry-run record creation uses synthetic id=0, but the field must be
    # present so the live build carries the real positive API row id.
    assert all("entity_id" in row for row in requests)
