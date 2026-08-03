import json
from datetime import date
from pathlib import Path

import scripts.enrich_daily_dream_digest as enrich


def proposal(path: Path, proposal_date: str, *, built: bool, title: str = "Dream", built_at: str | None = None) -> dict:
    data = {
        "title": title, "slug": title.lower().replace(" ", "-"), "idea": "A connected bundle.",
        "vibe": {"title": "Vibe", "line": "Umbrella", "art_direction": "wide art"},
        "locations": [{"title": "Place", "known_for": "wonder"}],
        "characters": [{"name": "Hero", "role_drive": "help"}],
        "rewards": [{"name": "Item", "reward_type": "ITEM", "grants": "opens"}, {"name": "Skill", "reward_type": "SKILL", "grants": "knows"}],
        "scenarios": [{"title": "Scene", "setup": "Vibe at Place with Hero."}],
        "seed_facets": {"elements": {key: [{"title": key, "slug": key, "taxonomy": "GENRE"}] for key in ("vibe", "location", "character", "reward_item", "reward_skill", "scenario")}},
    }
    built_data = None
    if built:
        built_data = {
            "built_at": built_at or f"{proposal_date}T10:00:00-07:00", "page": "https://kind-robots.vercel.app/daily-dream",
            "records": {"world": {"id": 1}, "vibe": {"id": 2}, "locations": [{"id": 3}], "characters": [{"id": 4}], "rewards": [{"id": 5}, {"id": 6}], "scenarios": [{"id": 7}]},
            "art": [
                {"element": data["slug"], "public_path": "/vibe.webp", "attached": True, "request_id": "vibe"},
                {"element": "place", "public_path": "/place.webp", "attached": True, "request_id": "place"},
                {"element": "hero", "public_path": "/hero.webp", "attached": False, "request_id": "hero"},
                {"element": "item", "public_path": "/item.webp", "attached": True, "request_id": "item"},
                {"element": "skill", "public_path": "/skill.webp", "attached": True, "request_id": "skill"},
                {"element": "scene-scenario", "public_path": "/scene.webp", "attached": True, "request_id": "scene"},
            ],
        }
    return {"path": path, "meta": {"proposal": True}, "data": data, "built": built_data, "proposal_date": proposal_date}


def test_latest_completed_creation_is_used_when_prior_calendar_day_is_empty(tmp_path):
    stale = proposal(tmp_path / "kite.md", "2026-07-18", built=True, title="Kite String Exchange")
    result = enrich.enrich_digest({"projects": []}, [stale], today=date(2026, 7, 31), probe_images=False)
    assert result["yesterday_output"]["title"] == "Kite String Exchange"
    assert result["daily_dream_output_status"] == "ready"
    assert "Most recent completed bundle" in result["yesterday_output"]["calendar_label"]


def test_exact_yesterday_has_six_readable_asset_rows(tmp_path):
    yesterday = proposal(tmp_path / "yesterday.md", "2026-07-30", built=True)
    result = enrich.enrich_digest({}, [yesterday], today=date(2026, 7, 31), probe_images=False)
    output = result["yesterday_output"]
    assert output["proposal_date"] == "2026-07-30"
    assert [row["key"] for row in output["assets"]] == ["vibe", "location", "character", "reward_item", "reward_skill", "scenario"]
    assert len(output["images"]) == 5
    hero = next(row for row in output["assets"] if row["key"] == "character")
    assert hero["art_status"] == "queued"
    assert hero["facets"] == ["GENRE: character"]


def test_today_proposal_replaces_legacy_tomorrow_selection(tmp_path):
    stale = proposal(tmp_path / "stale.md", "2026-07-18", built=True, title="Old")
    current = proposal(tmp_path / "today.md", "2026-07-31", built=False, title="New Bundle")
    result = enrich.enrich_digest({"tomorrow_proposal": {"title": "Wrong"}}, [stale, current], today=date(2026, 7, 31), probe_images=False)
    assert result["tomorrow_proposal"]["title"] == "New Bundle"
    assert len(result["tomorrow_proposal"]["assets"]) == 6


def test_yesterday_means_actual_build_date_not_proposal_date(tmp_path):
    built_yesterday = proposal(
        tmp_path / "older-proposal.md",
        "2026-07-20",
        built=True,
        title="Built Yesterday",
        built_at="2026-07-30T18:30:00-07:00",
    )
    dated_yesterday_but_unbuilt = proposal(
        tmp_path / "dated-yesterday.md",
        "2026-07-30",
        built=False,
        title="Still Steering",
    )
    result = enrich.enrich_digest(
        {},
        [dated_yesterday_but_unbuilt, built_yesterday],
        today=date(2026, 7, 31),
        probe_images=False,
    )
    assert result["yesterday_output"]["title"] == "Built Yesterday"
    assert result["yesterday_output"]["calendar_label"] == (
        "Most recent completed bundle before today's proposal; built 2026-07-30 "
        "from the 2026-07-20 proposal"
    )


def test_unbuilt_assets_are_awaiting_build_not_reported_as_unqueued(tmp_path):
    current = proposal(tmp_path / "today.md", "2026-07-31", built=False)
    payload = enrich.proposal_payload(current, probe_images=False)
    assert {asset["art_status"] for asset in payload["assets"]} == {"awaiting build"}


def test_scenario_queue_entry_uses_builder_suffix(tmp_path):
    built = proposal(tmp_path / "built.md", "2026-07-30", built=True)
    payload = enrich.proposal_payload(built, probe_images=False)
    scenario = next(asset for asset in payload["assets"] if asset["key"] == "scenario")
    assert scenario["art_status"] == "ready"
    assert scenario["request_id"] == "scene"


def test_today_built_bundle_is_not_repeated_as_previous_output(tmp_path):
    previous = proposal(
        tmp_path / "previous.md",
        "2026-07-29",
        built=True,
        title="Previous Bundle",
        built_at="2026-07-31T09:00:00-07:00",
    )
    current = proposal(
        tmp_path / "current.md",
        "2026-07-31",
        built=True,
        title="Current Bundle",
        built_at="2026-07-31T10:00:00-07:00",
    )
    result = enrich.enrich_digest({}, [previous, current], today=date(2026, 7, 31), probe_images=False)
    assert result["tomorrow_proposal"]["title"] == "Current Bundle"
    assert result["yesterday_output"]["title"] == "Previous Bundle"


def test_recent_outputs_follow_creation_order_not_calendar_window(tmp_path):
    older = proposal(
        tmp_path / "older.md",
        "2026-07-10",
        built=True,
        title="Older",
        built_at="2026-07-20T10:00:00-07:00",
    )
    latest = proposal(
        tmp_path / "latest.md",
        "2026-07-11",
        built=True,
        title="Latest",
        built_at="2026-07-25T10:00:00-07:00",
    )
    result = enrich.enrich_digest({}, [older, latest], today=date(2026, 7, 31), probe_images=False)
    assert [row["title"] for row in result["recent_dream_outputs"]] == ["Latest", "Older"]
