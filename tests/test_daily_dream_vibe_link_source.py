from pathlib import Path


def test_daily_dream_entities_share_the_main_vibe_link():
    source = Path("scripts/build_dream_records.py").read_text(encoding="utf-8")

    assert source.count(
        "link_ids = [i for i in (world_id, genre_id) if i]"
    ) == 3
    assert (
        "scenario_links = [i for i in "
        "[world_id, genre_id, *location_ids] if i]"
    ) in source
