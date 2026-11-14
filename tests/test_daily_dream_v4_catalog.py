"""The user wants proposed setting and character catalog objects, not more game content."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_daily_dream_v3_contract import example_v3  # noqa: E402
import apply_daily_dream_facets as facets  # noqa: E402
import build_dream_proposal as proposal_writer  # noqa: E402
import build_dream_records as writer  # noqa: E402
import daily_dream_v4_contract as v4  # noqa: E402
import enrich_daily_dream_digest_impl as digest  # noqa: E402
import run_daily_dream_build as scheduler  # noqa: E402


def example_v4():
    proposal = copy.deepcopy(example_v3())
    proposal["bundle_version"] = 4
    proposal["zuzu_assets"].pop("rewards")
    proposal["zuzu_assets"].pop("scenarios")
    seed = proposal["seed_facets"]
    seed["version"] = 4
    seed["elements"] = {
        slot: value for slot, value in seed["elements"].items()
        if slot in v4.FACET_SLOTS
    }
    return proposal


def test_new_contract_is_six_plus_four_not_new_gameplay():
    proposal = example_v4()
    assert v4.validate_v4(proposal) == []
    assets = v4.asset_manifest(proposal)
    assert len(assets) == 10
    assert len({asset.slot for asset in assets}) == 10
    assert sum(asset.lane == "dream" for asset in assets) == 6
    assert sum(asset.lane == "zuzu" for asset in assets) == 4
    for kind in ("locations", "characters"):
        assert {r["project_target"] for r in proposal["zuzu_assets"][kind]} == set(v4.PROJECT_TARGETS)
    assert set(proposal["zuzu_assets"]) == {"locations", "characters"}
    assert all(a.kind in ("locations", "characters") for a in assets if a.lane == "zuzu")


def test_no_rewards_scenarios_or_game_links_can_enter_candidate_shape():
    proposal = example_v4()
    proposal["zuzu_assets"]["scenarios"] = []
    assert any("only locations and characters" in error for error in v4.validate_v4(proposal))
    proposal["zuzu_assets"].pop("scenarios")
    proposal["zuzu_assets"]["characters"][0]["dreamIds"] = [123]
    assert any("may not join" in error for error in v4.validate_v4(proposal))


def test_v4_brief_and_markdown_include_exactly_four_candidates():
    catalog = proposal_writer._fallback("THEME")
    # Reuse the established six-slot planner and an independent real-facet pool.
    facet_catalog = {
        category: proposal_writer._fallback(category)
        for category in proposal_writer.FALLBACK_FACETS
    }
    assert catalog
    brief = proposal_writer.build_brief("2026-11-14", catalog=facet_catalog)
    assert brief["bundle_version"] == 4
    assert set(brief["seed_facets"]["elements"]) == set(v4.FACET_SLOTS)
    assert brief["required_counts"]["zuzu_locations"] == 2
    assert brief["required_counts"]["zuzu_characters"] == 2
    assert "zuzu_scenarios" not in brief["required_counts"]
    md = proposal_writer.render_markdown(example_v4(), "2026-11-14")
    assert "Four private Zuzu/Emperor setting and character candidates" in md
    assert "### Zuzu Locations (2)" in md
    assert "### Zuzu Characters (2)" in md
    assert "### Zuzu Rewards" not in md
    assert "### Zuzu Scenarios" not in md


def test_v4_writer_creates_only_private_project_catalog_rows(monkeypatch):
    proposal = example_v4()
    calls = []
    next_id = 501

    def fake_http(method, url, body=None, timeout=60):
        nonlocal next_id
        assert method == "POST"
        next_id += 1
        calls.append((url, body, next_id))
        return 201, {"data": {"id": next_id}}

    monkeypatch.setattr(writer, "http_json", fake_http)
    built, results, art = writer.build_records(
        proposal, proposal["slug"], "2026-11-14", False
    )
    assert all(row["ok"] for row in results)
    assert built["bundle_version"] == 4
    assert len(art) == len(built["art"]) == 10
    assert len({row["request_id"] for row in built["art"]}) == 10
    zuzu = built["records"]["zuzu"]
    assert set(zuzu) == {"locations", "characters"}
    assert len(zuzu["locations"]) == len(zuzu["characters"]) == 2

    created_rewards = [body for url, body, _ in calls if url.endswith("/api/rewards")]
    created_scenarios = [body for url, body, _ in calls if url.endswith("/api/scenarios")]
    assert len(created_rewards) == 2  # Original Daily Dream only.
    assert len(created_scenarios) == 1  # Original Daily Dream only.

    locations = [body for url, body, _ in calls if url.endswith("/api/dreams")
                 and body.get("dreamType") == "LOCATION"]
    assert len(locations) == 3
    assert locations[0]["isPublic"] is True
    assert all(row["isPublic"] is False for row in locations[1:])
    assert all(row["allowReviews"] is False for row in locations[1:])
    assert {row["designer"] for row in locations[1:]} == {
        "dream-cycle:zuzu-gamebook", "dream-cycle:emperor-of-dust"
    }

    chars = [body for url, body, _ in calls if url.endswith("/api/characters")]
    assert len(chars) == 3
    assert chars[0]["dreamIds"]
    assert all(row["isPublic"] is False for row in chars[1:])
    assert all(row["dreamIds"] == [] for row in chars[1:])
    assert all(row["role"] == "Proposed character model" for row in chars[1:])
    assert {row["designer"] for row in chars[1:]} == {
        "dream-cycle:zuzu-gamebook", "dream-cycle:emperor-of-dust"
    }

    tagged_sheets = [
        json.loads(body["extraData"])
        for url, body, _ in calls if "/api/sheets/by-dream/" in url
        and "projectTarget" in json.loads(body["extraData"])
    ]
    assert {item["projectTarget"] for item in tagged_sheets} == set(v4.PROJECT_TARGETS)
    assert all(row["checkpoint_family"] in v4.CHECKPOINT_FAMILIES
               for row in built["art"] if row.get("project_target"))
    assert len([row for row in built["art"] if row.get("project_target")]) == 4
    assert len(facets._record_targets(proposal, built)) == 10

    cards = digest._asset_rows(
        {"data": proposal, "built": built}, probe_images=False
    )
    assert len(cards) == 10
    assert sum(card["lane"] == "zuzu" for card in cards) == 4


def test_scheduled_writer_does_not_reanimate_old_v3_scenarios(tmp_path, monkeypatch):
    old = example_v3()
    file_path = tmp_path / "old-v3.md"
    file_path.write_text(
        "---\\nproposal: true\\nproposal_date: '2026-11-08'\\nstatus: outline\\n---\\n"
        "<!-- proposal-data\\n" + json.dumps(old) + "\\n-->\\n",
        encoding="utf-8",
    )
    text = file_path.read_text()
    monkeypatch.setattr(writer, "find_proposals", lambda: [(
        file_path,
        {"proposal_date": "2026-11-08", "status": "outline"},
        text,
    )])
    selected, reason = scheduler.eligible_proposal(None)
    assert selected is None
    assert "legacy draft retained" in reason
