from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import scripts.build_digest_email_v2 as email
import scripts.build_dream_proposal as dreams
import scripts.enrich_daily_dream_digest as enrich


def _queued_proposal(day: str, slug: str, entropy_version: int) -> str:
    payload = {
        "title": slug.replace("-", " ").title(),
        "slug": slug,
        "idea": "Test steering proposal.",
        "seed_facets": {"creative_entropy_version": entropy_version},
    }
    return (
        "---\n"
        f"slug: {slug}\n"
        f"title: {payload['title']}\n"
        "type: dream\n"
        "status: outline\n"
        "proposal: true\n"
        f"created: '{day}'\n"
        f"proposal_date: '{day}'\n"
        "built_pr: null\n"
        "---\n\n"
        "<!-- proposal-data\n"
        + json.dumps(payload)
        + "\n-->\n"
    )


def test_stale_entropy_proposals_do_not_fill_or_own_the_docket_date(tmp_path, monkeypatch):
    day = "2026-09-13"
    monkeypatch.setattr(dreams, "BACKLOG", tmp_path)
    # This test isolates docket/version semantics; full proposal validity has its own suite.
    monkeypatch.setattr(dreams, "validate_proposal", lambda proposal: [])

    stale = tmp_path / f"{day}-old-contract.md"
    stale.write_text(
        _queued_proposal(day, "old-contract", dreams.CREATIVE_ENTROPY_VERSION - 1),
        encoding="utf-8",
    )

    assert dreams.stale_unbuilt_backlog() == [day]
    assert dreams.unbuilt_backlog() == []
    assert dreams.proposal_exists_for(day) is False

    fresh = tmp_path / f"{day}-current-contract.md"
    fresh.write_text(
        _queued_proposal(day, "current-contract", dreams.CREATIVE_ENTROPY_VERSION),
        encoding="utf-8",
    )

    assert dreams.unbuilt_backlog() == [day]
    assert dreams.proposal_exists_for(day) is True


def _completed_proposal(path: Path, built_at: str) -> dict:
    data = {
        "title": "Recovered Dream",
        "slug": "recovered-dream",
        "idea": "A completed bundle whose art should not disappear merely because the next build stalled.",
        "vibe": {"title": "Vibe", "line": "Umbrella", "art_direction": "wide art"},
        "locations": [{"title": "Place", "known_for": "wonder"}],
        "characters": [{"name": "Hero", "role_drive": "help"}],
        "rewards": [
            {"name": "Item", "reward_type": "ITEM", "grants": "opens"},
            {"name": "Skill", "reward_type": "SKILL", "grants": "knows"},
        ],
        "scenarios": [{"title": "Scene", "setup": "Vibe at Place with Hero."}],
        "seed_facets": {"elements": {}},
    }
    art = [
        ("recovered-dream", "/vibe.webp"),
        ("place", "/place.webp"),
        ("hero", "/hero.webp"),
        ("item", "/item.webp"),
        ("skill", "/skill.webp"),
        ("scene-scenario", "/scene.webp"),
    ]
    return {
        "path": path,
        "meta": {"proposal": True},
        "data": data,
        "proposal_date": "2026-09-10",
        "built": {
            "built_at": built_at,
            "page": "https://kindrobots.org",
            "records": {},
            "art": [
                {
                    "element": element,
                    "public_path": public_path,
                    "attached": True,
                    "request_id": element,
                }
                for element, public_path in art
            ],
        },
    }


def test_two_day_old_latest_bundle_is_art_rich_and_truthfully_labeled(tmp_path):
    current = _completed_proposal(
        tmp_path / "completed.md",
        "2026-09-11T08:10:00-07:00",
    )

    result = enrich.enrich_digest(
        {},
        [current],
        today=date(2026, 9, 13),
        probe_images=False,
    )
    latest = result["current_dream_output"]

    assert latest["display_mode"] == "latest-completed"
    assert len(latest["images"]) == 6
    assert "No newer completed bundle exists" in latest["calendar_label"]
    assert "No new Daily Dream bundle completed" in result["daily_dream_output_status"]

    html = email.proposal_section("ignored", latest)
    assert "Latest completed output" in html
    assert "Just built this cycle" not in html
    assert "Previous completed output" not in html
