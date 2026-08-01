import json
from datetime import date
from pathlib import Path

import scripts.enrich_daily_dream_digest as enrich


def proposal(path: Path, proposal_date: str, *, built: bool, title: str = "Dream") -> dict:
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
            "built_at": f"{proposal_date}T10:00:00-07:00", "page": "https://kind-robots.vercel.app/daily-dream",
            "records": {"world": {"id": 1}, "vibe": {"id": 2}, "locations": [{"id": 3}], "characters": [{"id": 4}], "rewards": [{"id": 5}, {"id": 6}], "scenarios": [{"id": 7}]},
            "art": [
                {"element": data["slug"], "public_path": "/vibe.webp", "attached": True, "request_id": "vibe"},
                {"element": "place", "public_path": "/place.webp", "attached": True, "request_id": "place"},
                {"element": "hero", "public_path": "/hero.webp", "attached": False, "request_id": "hero"},
                {"element": "item", "public_path": "/item.webp", "attached": True, "request_id": "item"},
                {"element": "skill", "public_path": "/skill.webp", "attached": True, "request_id": "skill"},
                {"element": "scene", "public_path": "/scene.webp", "attached": True, "request_id": "scene"},
            ],
        }
    return {"path": path, "meta": {"proposal": True}, "data": data, "built": built_data, "proposal_date": proposal_date}


def test_stale_first_creation_is_never_called_yesterday(tmp_path):
    stale = proposal(tmp_path / "kite.md", "2026-07-18", built=True, title="Kite String Exchange")
    result = enrich.enrich_digest({"projects": []}, [stale], today=date(2026, 7, 31), probe_images=False)
    assert result["yesterday_output"] is None
    assert "2026-07-30" in result["daily_dream_output_status"]
    assert "Kite String Exchange" not in json.dumps(result.get("yesterday_output"))


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
