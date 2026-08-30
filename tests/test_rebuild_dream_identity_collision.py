import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import rebuild_dream_identity_collision as repair  # noqa: E402


def _built(ids=(10, 11, 12, 13, 14, 15)):
    world, location, character, item, skill, scenario = ids
    roles = [
        ("world", "/api/dreams", "dream", world, "world-art"),
        ("location", "/api/dreams", "dream", location, "location-art"),
        ("character", "/api/characters", "character", character, "character-art"),
        ("reward_item", "/api/rewards", "reward", item, "item-art"),
        ("reward_skill", "/api/rewards", "reward", skill, "skill-art"),
        ("scenario", "/api/scenarios", "scenario", scenario, "scenario-art"),
    ]
    return {
        "records": {
            "world": {"model": "Dream", "id": world, "title": "World"},
            "locations": [{"model": "Dream", "id": location, "title": "Location"}],
            "characters": [{"model": "Character", "id": character, "name": "Person"}],
            "rewards": [
                {"model": "Reward", "id": item, "name": "Item", "reward_type": "ITEM"},
                {"model": "Reward", "id": skill, "name": "Skill", "reward_type": "SKILL"},
            ],
            "scenarios": [{"model": "Scenario", "id": scenario, "title": "Scenario"}],
        },
        "art": [
            {
                "element": element,
                "entity_type": entity_type,
                "entity_id": record_id,
                "target_endpoint": endpoint,
                "target_id": record_id,
                "public_path": f"/images/dreams/test/{element}.webp",
                "image_path": f"public/images/dreams/test/{element}.webp",
                "request_id": f"old-{element}",
                "attached": True,
            }
            for element, endpoint, entity_type, record_id, _ in roles
        ],
    }


def test_migrated_art_preserves_render_paths_but_retargets_fresh_ids():
    historical = _built((1, 2, 3, 4, 5, 6))
    fresh = _built((101, 102, 103, 104, 105, 106))

    migrated = repair.migrated_art(historical, fresh)

    assert [row["public_path"] for row in migrated] == [
        row["public_path"] for row in historical["art"]
    ]
    assert [row["target_id"] for row in migrated] == [101, 102, 103, 104, 105, 106]
    assert all(row["attached"] is True for row in migrated)
    assert all(row["identity_reused"] is True for row in migrated)


def test_role_records_requires_exact_canonical_shape():
    built = _built()
    assert set(repair.role_records(built)) == {
        "world", "location", "character", "reward_item", "reward_skill", "scenario"
    }

    broken = copy.deepcopy(built)
    broken["records"]["locations"].append({"model": "Dream", "id": 99, "title": "Extra"})
    with pytest.raises(ValueError, match="canonical six-record bundle"):
        repair.role_records(broken)


def test_validate_request_is_explicitly_bounded_and_approved():
    request = {
        "version": 1,
        "source_ref": "a" * 40,
        "approved_by_user": "Silas approved repair",
        "bundles": ["projects/dream-cycle/backlog/a.md", "projects/dream-cycle/backlog/b.md"],
        "protected_owners": [
            {"endpoint": "/api/dreams", "id": 1, "title": "A"},
            {"endpoint": "/api/dreams", "id": 2, "title": "B"},
        ],
    }
    source_ref, bundles, owners = repair.validate_request(request)
    assert source_ref == "a" * 40
    assert len(bundles) == 2
    assert len(owners) == 2

    missing_approval = dict(request)
    missing_approval.pop("approved_by_user")
    with pytest.raises(ValueError, match="approval"):
        repair.validate_request(missing_approval)

    too_broad = dict(request)
    too_broad["bundles"] = request["bundles"] + ["projects/dream-cycle/backlog/c.md"]
    with pytest.raises(ValueError, match="exactly two"):
        repair.validate_request(too_broad)


def test_current_source_must_be_collision_reset_and_unbuilt(tmp_path):
    proposal = {
        "vibe": {"title": "Vibe", "line": "A complete enough line."},
        "locations": [{"title": "Place"}],
        "characters": [{"name": "Person"}],
        "rewards": [
            {"name": "Item", "reward_type": "ITEM"},
            {"name": "Skill", "reward_type": "SKILL"},
        ],
        "scenarios": [{"title": "Scene"}],
        "seed_facets": {
            "version": 2,
            "elements": {
                "vibe": [], "location": [], "character": [],
                "reward_item": [], "reward_skill": [], "scenario": [],
            },
        },
    }
    path = tmp_path / "dream.md"
    text = (
        "---\nstatus: outline\nproposal: true\n---\n"
        "## Build log\n- 2026-08-30 | identity-repair | reset stale ledger\n"
        f"<!-- proposal-data\n{json.dumps(proposal)}\n-->\n"
    )
    path.write_text(text, encoding="utf-8")
    fm, parsed = repair._validate_current_source(path, text)
    assert fm["status"] == "outline"
    assert parsed == proposal

    with_built = text + "<!-- built-data\n{}\n-->\n"
    with pytest.raises(ValueError, match="built-data"):
        repair._validate_current_source(path, with_built)


def test_script_uses_builder_without_enqueuing_replacement_art():
    source = (ROOT / "scripts" / "rebuild_dream_identity_collision.py").read_text(encoding="utf-8")
    assert "records.build_records(" in source
    assert "append_art_requests(" not in source
    assert '"new_art_jobs": 0' in source
