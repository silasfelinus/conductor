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


def _solid(value):
    from PIL import Image

    return Image.new("RGB", (32, 18), (value, value, value))


def test_loop_frames_drops_the_settling_frames_and_crossfades_the_seam():
    import itertools
    import math

    # Two jumpy warm-up frames (the sharp plate settling into WAN's render), then a near-periodic shimmer
    # that drifts 12 levels over the clip, so the raw last frame does not meet the first.
    steady = [round(90 + 6 * math.sin(2 * math.pi * i / 40) + 0.3 * i) for i in range(40)]
    frames = [_solid(220), _solid(150)] + [_solid(v) for v in steady]
    looped = clips.loop_frames(frames, fade=8)
    values = [f.getpixel((0, 0))[0] for f in looped]
    raw_seam = abs(steady[-1] - steady[0])
    wrap = values + values[:1]
    assert len(looped) == 40 - 8, "warm-up dropped, and the head's fade frames folded into the tail"
    assert values[0] == steady[8], "the loop opens on the frame after the faded head"
    assert raw_seam >= 8, "the uncorrected clip would pop at the wrap"
    assert max(abs(b - a) for a, b in itertools.pairwise(wrap)) <= 3, "with the crossfade, no step pops, the wrap included"


def test_loop_frames_leaves_a_short_clip_alone():
    frames = [_solid(10 + i) for i in range(10)]
    assert len(clips.loop_frames(frames, fade=8)) == 10
