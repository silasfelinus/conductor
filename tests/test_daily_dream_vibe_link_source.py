from pathlib import Path


def test_daily_dream_entities_share_the_world_and_vibe_facets():
    source = Path("scripts/build_dream_records.py").read_text(encoding="utf-8")
    facet_source = Path("scripts/apply_daily_dream_facets.py").read_text(
        encoding="utf-8"
    )

    assert source.count("link_ids = [world_id] if world_id else []") == 3
    assert '"dreamType": "GENRE"' not in source
    assert (
        "scenario_links = [i for i in "
        "[world_id, *location_ids] if i]"
    ) in source
    assert 'add("vibe", "Dream", records.get("world"))' in facet_source


def test_temporary_hourly_push_trigger_cannot_run_from_pr_branches():
    workflow = Path(".github/workflows/hourly-conductor.yml").read_text(
        encoding="utf-8"
    )

    if "\n  push:\n" in workflow:
        push_block = workflow.split("\n  push:\n", 1)[1].split("\n  schedule:\n", 1)[0]
        assert "    branches:\n      - main\n" in push_block
