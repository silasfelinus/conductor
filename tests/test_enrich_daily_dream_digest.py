import json
from datetime import date
from pathlib import Path

import scripts.enrich_daily_dream_digest as enrich


def proposal(
    path: Path,
    proposal_date: str,
    *,
    built: bool,
    title: str = "Dream",
    built_at: str | None = None,
) -> dict:
    data = {
        "title": title,
        "slug": title.lower().replace(" ", "-"),
        "idea": "A connected bundle.",
        "vibe": {"title": "Vibe", "line": "Umbrella", "art_direction": "wide art"},
        "locations": [{"title": "Place", "known_for": "wonder"}],
        "characters": [{"name": "Hero", "role_drive": "help"}],
        "rewards": [
            {"name": "Item", "reward_type": "ITEM", "grants": "opens"},
            {"name": "Skill", "reward_type": "SKILL", "grants": "knows"},
        ],
        "scenarios": [{"title": "Scene", "setup": "Vibe at Place with Hero."}],
        "seed_facets": {
            "elements": {
                key: [{"title": key, "slug": key, "taxonomy": "GENRE"}]
                for key in (
                    "vibe",
                    "location",
                    "character",
                    "reward_item",
                    "reward_skill",
                    "scenario",
                )
            }
        },
    }
    built_data = None
    if built:
        built_data = {
            "built_at": built_at or f"{proposal_date}T10:00:00-07:00",
            "page": "https://kind-robots.vercel.app",
            "records": {
                "world": {"id": 1},
                "locations": [{"id": 3}],
                "characters": [{"id": 4}],
                "rewards": [{"id": 5}, {"id": 6}],
                "scenarios": [{"id": 7}],
            },
            "art": [
                {
                    "element": data["slug"],
                    "public_path": "/vibe.webp",
                    "attached": True,
                    "request_id": "vibe",
                },
                {
                    "element": "place",
                    "public_path": "/place.webp",
                    "attached": True,
                    "request_id": "place",
                },
                {
                    "element": "hero",
                    "public_path": "/hero.webp",
                    "attached": False,
                    "request_id": "hero",
                },
                {
                    "element": "item",
                    "public_path": "/item.webp",
                    "attached": True,
                    "request_id": "item",
                },
                {
                    "element": "skill",
                    "public_path": "/skill.webp",
                    "attached": True,
                    "request_id": "skill",
                },
                {
                    "element": "scene-scenario",
                    "public_path": "/scene.webp",
                    "attached": True,
                    "request_id": "scene",
                },
            ],
        }
    return {
        "path": path,
        "meta": {"proposal": True},
        "data": data,
        "built": built_data,
        "proposal_date": proposal_date,
    }


def test_digest_roles_are_next_proposal_then_two_completed_generations(tmp_path):
    older = proposal(
        tmp_path / "older.md",
        "2026-07-28",
        built=True,
        title="Older",
        built_at="2026-07-29T08:00:00-07:00",
    )
    previous = proposal(
        tmp_path / "previous.md",
        "2026-07-29",
        built=True,
        title="Previous Art Rich",
        built_at="2026-07-30T08:00:00-07:00",
    )
    current = proposal(
        tmp_path / "current.md",
        "2026-07-30",
        built=True,
        title="Just Built",
        built_at="2026-07-31T08:10:00-07:00",
    )
    next_proposal = proposal(
        tmp_path / "next.md",
        "2026-07-31",
        built=False,
        title="Next Steering Proposal",
    )

    result = enrich.enrich_digest(
        {},
        [older, previous, current, next_proposal],
        today=date(2026, 7, 31),
        probe_images=False,
    )

    assert result["next_dream_proposal"]["title"] == "Next Steering Proposal"
    assert result["next_dream_proposal"]["built"] is False
    assert result["current_dream_output"]["title"] == "Just Built"
    assert result["current_dream_output"]["display_mode"] == "just-built"
    assert result["previous_dream_output"]["title"] == "Previous Art Rich"
    assert result["previous_dream_output"]["display_mode"] == "art-rich"
    assert "tomorrow_proposal" not in result
    assert "yesterday_output" not in result
    assert result["recent_dream_outputs"] == []


def test_completed_selection_uses_build_order_not_proposal_date(tmp_path):
    built_later = proposal(
        tmp_path / "older-proposal.md",
        "2026-07-20",
        built=True,
        title="Built Later",
        built_at="2026-07-31T09:00:00-07:00",
    )
    built_earlier = proposal(
        tmp_path / "newer-proposal.md",
        "2026-07-30",
        built=True,
        title="Built Earlier",
        built_at="2026-07-30T18:30:00-07:00",
    )
    next_proposal = proposal(
        tmp_path / "today.md",
        "2026-07-31",
        built=False,
        title="Steering",
    )

    result = enrich.enrich_digest(
        {},
        [built_later, built_earlier, next_proposal],
        today=date(2026, 7, 31),
        probe_images=False,
    )
    assert result["current_dream_output"]["title"] == "Built Later"
    assert result["previous_dream_output"]["title"] == "Built Earlier"


def test_current_output_does_not_probe_or_claim_unattached_art_ready(tmp_path):
    current = proposal(tmp_path / "current.md", "2026-07-30", built=True)
    result = enrich.enrich_digest(
        {}, [current], today=date(2026, 7, 31), probe_images=True
    )
    hero = next(
        row for row in result["current_dream_output"]["assets"]
        if row["key"] == "character"
    )
    assert hero["image_url"] == ""
    assert hero["art_status"] == "queued"
    assert result["previous_dream_output"] is None


def test_previous_output_has_six_readable_asset_rows(tmp_path):
    previous = proposal(tmp_path / "previous.md", "2026-07-29", built=True)
    current = proposal(
        tmp_path / "current.md",
        "2026-07-30",
        built=True,
        built_at="2026-07-31T08:00:00-07:00",
    )
    result = enrich.enrich_digest(
        {}, [previous, current], today=date(2026, 7, 31), probe_images=False
    )
    output = result["previous_dream_output"]
    assert [row["key"] for row in output["assets"]] == [
        "vibe",
        "location",
        "character",
        "reward_item",
        "reward_skill",
        "scenario",
    ]
    assert len(output["images"]) == 5
    hero = next(row for row in output["assets"] if row["key"] == "character")
    assert hero["art_status"] == "queued"
    assert hero["facets"] == ["GENRE: character"]


def test_unbuilt_assets_are_awaiting_build(tmp_path):
    current = proposal(tmp_path / "today.md", "2026-07-31", built=False)
    payload = enrich.proposal_payload(current, probe_images=False)
    assert {asset["art_status"] for asset in payload["assets"]} == {"awaiting build"}


def test_scenario_queue_entry_uses_builder_suffix(tmp_path):
    built = proposal(tmp_path / "built.md", "2026-07-30", built=True)
    payload = enrich.proposal_payload(built, probe_images=False)
    scenario = next(asset for asset in payload["assets"] if asset["key"] == "scenario")
    assert scenario["art_status"] == "ready"
    assert scenario["request_id"] == "scene"


def test_only_one_completed_bundle_is_current_not_art_rich(tmp_path):
    current = proposal(
        tmp_path / "current.md",
        "2026-07-30",
        built=True,
        title="First Completed",
    )
    result = enrich.enrich_digest(
        {}, [current], today=date(2026, 7, 31), probe_images=False
    )
    assert result["current_dream_output"]["title"] == "First Completed"
    assert result["previous_dream_output"] is None
    assert "no earlier completed bundle" in result["daily_dream_output_status"]
