"""The Daily Dream remains a complete original mini-world, PLUS eight Zuzu assets."""
from copy import deepcopy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import daily_dream_v3_contract as v3  # noqa: E402


def _facet(slug):
    return {"title": slug.title(), "taxonomy": "THEME", "slug": slug}


def example_v3():
    loc = dict(
        title="Ashwater Cut", known_for="An exposed crossing divides the camps.",
        local_rule="The watch accepts safe passage only after a pledge.",
        best_scene="A refuge caravan waits under two rival banners.",
        art_direction="A dusty rift lined by splintered saltstone.",
    )
    ch = dict(
        name="Vesper Trail", role_drive="She protects strays others abandoned.",
        carries="She wears a carved horn at her hip.",
        complication="Her patron commands the rival faction.",
        look="Older female fennec, scarred armor, dull indigo cloak.",
    )
    reward = dict(
        name="The Red Thread", reward_type="ITEM", rarity="RARE",
        grants="It helps locate a hidden path.",
        best_used_when="A caravan crosses contested ground.",
        catch="Its owner leaves a trace in the dust.",
        look="Red braided cord on an old brass hook.",
    )
    sc = dict(
        title="The Borrowed Crossing", setup="The caravan offers food to cross land held by an enemy.",
        choices=[
            {"label": "Give sanctuary", "tradeoff": "Cede precious grain.",
             "immediate_consequence": "Refugees survive.",
             "later_consequence": "The outpost's winter stores run thin."},
            {"label": "Hold the border", "tradeoff": "Refuse vulnerable travelers.",
             "immediate_consequence": "The granary stays secure.",
             "later_consequence": "The faction remembers the refusal."},
        ],
    )
    result = dict(
        bundle_version=3, title="A Lantern for Nobody",
        slug="a-lantern-for-nobody",
        idea="An original daily Dream about a strange new home.",
        vibe={"title": "Tomorrow's Elsewhere", "line": "A home appears only when needed.",
              "art_direction": "Bright prismatic towers and sharp clear sunlight."},
        locations=[dict(loc, title="Mirror Orchard")],
        characters=[dict(ch, name="The Faceted Gardener")],
        rewards=[
            dict(reward, name="Daylight Lantern", reward_type="ITEM"),
            dict(reward, name="Prism Step", reward_type="SKILL"),
        ],
        scenarios=[
            dict(sc, title="The Orchard Gate",
                 setup="In Tomorrow's Elsewhere, the Faceted Gardener waits at Mirror Orchard.")
        ],
        zuzu_assets={"locations": [], "characters": [], "rewards": [], "scenarios": []},
        seed_facets={"version": 3, "elements": {
            slot: [_facet(slot)] for slot in v3.FACET_SLOTS
        }},
    )
    for target in v3.PROJECT_TARGETS:
        for kind, sample in (
            ("locations", loc), ("characters", ch), ("rewards", reward), ("scenarios", sc)
        ):
            row = deepcopy(sample)
            row["project_target"] = target
            row["checkpoint_family"] = (
                "arthemy" if target == "zuzu-gamebook" else "illustrious"
            )
            if kind == "rewards":
                row["reward_type"] = "ITEM" if target == "zuzu-gamebook" else "SKILL"
            if kind == "locations" and target == "emperor-of-dust":
                row["title"] = "Hollow Bell Outskirts"
            if kind == "characters" and target == "emperor-of-dust":
                row["name"] = "Young Komodo's Scout"
            if kind == "scenarios" and target == "emperor-of-dust":
                row["title"] = "The Winter Claim"
            result["zuzu_assets"][kind].append(row)
    return result


def test_fourteen_assets_include_original_six_linked_dream_and_eight_separate_zuzu():
    proposal = example_v3()
    assert v3.validate_v3(proposal) == []
    assets = v3.asset_manifest(proposal)
    assert len(assets) == 14
    assert len({a.slot for a in assets}) == 14
    assert sum(a.lane == "dream" for a in assets) == 6
    assert sum(a.lane == "zuzu" for a in assets) == 8
    assert assets[0].slot == "vibe" and not assets[0].linked_to_vibe
    assert all(a.linked_to_vibe for a in assets if a.lane == "dream" and a.slot != "vibe")
    assert all(not a.linked_to_vibe and a.project_target for a in assets if a.lane == "zuzu")
    assert all(a.checkpoint_family is None for a in assets if a.lane == "dream")
    assert {a.checkpoint_family for a in assets if a.lane == "zuzu"} == {"arthemy", "illustrious"}
    for kind in v3.ZUZU_COUNTS:
        assert {a.project_target for a in assets if a.kind == kind and a.lane == "zuzu"} == set(v3.PROJECT_TARGETS)


def test_missing_dream_location_does_not_get_replaced_by_zuzu_location():
    p = example_v3()
    p["locations"] = []
    errors = " ".join(v3.validate_v3(p))
    assert "dream.locations has 0" in errors


def test_zuzu_extras_may_not_reparent_to_the_original_vibe():
    p = example_v3()
    p["zuzu_assets"]["characters"][0]["linked_to_vibe"] = True
    p["zuzu_assets"]["scenarios"][0]["dreamIds"] = [25]
    p["seed_facets"]["link_zuzu_to_vibe"] = True
    errors = " ".join(v3.validate_v3(p))
    assert "must not link to the daily vibe" in errors
    assert "Zuzu extras must not be linked" in errors


def test_original_dream_mini_world_keeps_its_links_and_shared_art_style():
    p = example_v3()
    p["characters"][0]["linked_to_vibe"] = False
    p["locations"][0]["checkpoint_family"] = "arthemy"
    errors = " ".join(v3.validate_v3(p))
    assert "must link to the daily vibe" in errors
    assert "must inherit the daily vibe" in errors


def test_zuzu_scenarios_need_substantive_moral_choices():
    p = example_v3()
    p["zuzu_assets"]["scenarios"][0]["choices"][1]["label"] = "Give sanctuary"
    p["zuzu_assets"]["scenarios"][1]["choices"] = [{"label": "Only choice"}]
    errors = " ".join(v3.validate_v3(p))
    assert "choice labels must be distinct" in errors
    assert "at least two moral choices" in errors


def test_zuzu_project_and_checkpoint_constraints():
    p = example_v3()
    p["zuzu_assets"]["locations"][1]["project_target"] = "zuzu-gamebook"
    p["zuzu_assets"]["characters"][0]["checkpoint_family"] = "flux"
    errors = " ".join(v3.validate_v3(p))
    assert "exactly one asset to each project" in errors
    assert "Arthemy or Illustrious" in errors


def test_offline_outline_validation_accepts_revised_v3(tmp_path):
    import scripts.check_dream_outlines as preflight

    p = example_v3()
    path = tmp_path / "new-daily-dream.md"

    def write():
        path.write_text(
            "---\nslug: test\ntitle: Test\ntype: dream\nstatus: outline\n"
            "proposal: true\n---\n"
            + "<!-- proposal-data\n" + json.dumps(p) + "\n-->\n",
            encoding="utf-8",
        )

    write()
    assert preflight.check_outline(path) == []
    p["zuzu_assets"]["scenarios"][0]["choices"] = []
    write()
    assert any("moral choices" in f.detail for f in preflight.check_outline(path))


def test_old_live_writer_fails_closed_on_unimplemented_v3():
    import scripts.build_dream_records as builder

    errors = builder._canonical_proposal_errors(example_v3())
    assert any("upgraded single writer" in error for error in errors)


def test_fourteen_record_builder_keeps_world_links_separate(monkeypatch):
    from scripts import build_dream_records as builder

    proposal = example_v3()
    assert v3.validate_v3(proposal) == []
    created_bodies = []
    next_id = 500

    def fake_http(method, url, body=None, timeout=60):
        nonlocal next_id
        if method != "POST":
            raise AssertionError(f"unexpected {method}: {url}")
        next_id += 1
        created_bodies.append((url, body, next_id))
        return 201, {"data": {"id": next_id}}

    monkeypatch.setattr(builder, "http_json", fake_http)
    built, results, art_entries = builder.build_records(
        proposal, proposal["slug"], "2026-10-13", dry_run=False
    )
    assert all(row["ok"] for row in results)
    assert built["bundle_version"] == 3
    assert len(art_entries) == len(built["art"]) == 14
    assert len({row["request_id"] for row in built["art"]}) == 14
    assert len(built["records"]["locations"]) == 1
    assert len(built["records"]["characters"]) == 1
    assert len(built["records"]["rewards"]) == 2
    assert len(built["records"]["scenarios"]) == 1
    assert all(len(built["records"]["zuzu"][key]) == 2 for key in v3.ZUZU_COUNTS)

    world_id = built["records"]["world"]["id"]
    original_location_id = built["records"]["locations"][0]["id"]
    zuzu_location_ids = {
        row["project_target"]: row["id"]
        for row in built["records"]["zuzu"]["locations"]
    }
    relations = [
        body for url, body, _ in created_bodies
        if url.endswith("/api/dream-relations")
    ]
    assert relations == [{
        "fromDreamId": world_id,
        "toDreamId": original_location_id,
        "relationType": "CONTAINS",
    }]
    # Zuzu Characters and Rewards have no linkage to random daily Dream.
    chars = [body for url, body, _ in created_bodies if url.endswith("/api/characters")]
    rewards = [body for url, body, _ in created_bodies if url.endswith("/api/rewards")]
    assert len(chars) == 3 and len(rewards) == 4
    assert chars[0]["dreamIds"] == [world_id]
    assert all(row["dreamIds"] == [] for row in chars[1:])
    assert all(row["dreamIds"] == [world_id] for row in rewards[:2])
    assert all(row["dreamIds"] == [] for row in rewards[2:])
    scenarios = [body for url, body, _ in created_bodies if url.endswith("/api/scenarios")]
    assert len(scenarios) == 3
    assert scenarios[0]["dreamIds"] == [world_id, original_location_id]
    assert all(world_id not in row["dreamIds"] for row in scenarios[1:])
    assert {row["dreamIds"][0] for row in scenarios[1:]} == set(zuzu_location_ids.values())
    assert all("Choices:" in row["description"] for row in scenarios[1:])
    extras = [row for row in built["art"] if row.get("project_target")]
    assert len(extras) == 8
    assert all(row["checkpoint_family"] in ("arthemy", "illustrious") for row in extras)
    assert len([e for e in art_entries if "engine: sdxl-checkpoint" in e]) == 8
    assert len([e for e in art_entries if "engine: sdxl-checkpoint" not in e]) == 6
    # Project attribution survives in generated metadata and ArtJob requests.
    assert all("  project_target: " in e and "  checkpoint_family: " in e
               for e in art_entries if "engine: sdxl-checkpoint" in e)


def test_v3_partial_transaction_can_rollback_all_fourteen(monkeypatch):
    from scripts import build_dream_records as builder

    proposal = example_v3()
    next_id = 900
    deleted = []

    def fake_http(method, url, body=None, timeout=60):
        nonlocal next_id
        if method == "DELETE":
            deleted.append(url)
            return 200, {"success": True}
        if method != "POST":
            raise AssertionError(method)
        next_id += 1
        if url.endswith("/api/scenarios") and "The Winter Claim" in str(body):
            return 503, {"message": "transient database outage"}
        return 201, {"data": {"id": next_id}}

    monkeypatch.setattr(builder, "http_json", fake_http)
    _, results, art = builder.build_records(
        proposal, proposal["slug"], "2026-10-13", dry_run=False
    )
    assert len(art) == 14
    assert any(not row["ok"] for row in results)
    successful_rows = [
        row for row in results if row["ok"] and row["created"] and row["id"]
    ]
    assert builder.rollback_created(results) > 0
    assert len(deleted) == len(successful_rows)
