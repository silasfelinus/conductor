import scripts.export_plumber_map_clips as clips


def test_finished_reads_done_loops_and_skips_withdrawn_and_pending():
    subjects = [
        {"key": "gen2-mapclip-1-bluebell", "art": {"wan-clips": {"status": "DONE", "art_image_id": 11}}},
        {"key": "gen2-mapclip-2-tideglass", "art": {"wan-clips": {"status": "PENDING", "art_image_id": None}}},
        {
            "key": "gen2-mapclip-3-orchard",
            "art": {"wan-clips": {"status": "DONE", "art_image_id": 33}},
            "withdrawn": {"wan-clips": "the waterfall melted"},
        },
        {"key": "gen2-clip-intro", "art": {"wan-clips": {"status": "DONE", "art_image_id": 44}}},
    ]
    assert list(clips.finished(subjects)) == [(1, 11)]


def test_manifest_lists_shipped_worlds_in_order(tmp_path):
    maps = tmp_path / clips.MAPS_DIR
    maps.mkdir(parents=True)
    for name in ("world-3.mp4", "world-3.webm", "world-1.mp4", "world-1.webm", "world-2.mp4", "world-1.webp", "notes.txt"):
        (maps / name).write_bytes(b"x")
    assert clips.shipped(tmp_path) == [1, 3], "a world ships only with both its WebM and its MP4"
    text = clips.render_manifest([3, 1])
    assert "Do not edit by hand." in text
    assert text.rstrip().endswith("export const MAP_CLIP_WORLDS: readonly number[] = [1, 3]")
    assert clips.render_manifest([]).rstrip().endswith("= []")
