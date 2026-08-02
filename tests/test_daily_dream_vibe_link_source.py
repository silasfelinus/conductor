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
