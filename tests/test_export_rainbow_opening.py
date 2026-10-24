import yaml

import scripts.export_rainbow_opening as opening


def test_the_cut_is_about_fifteen_seconds_on_the_beat_grid():
    beats = sum(beats for _, beats in opening.SHOTS)
    seconds = beats * 60.0 / opening.BPM
    assert 14.0 <= seconds <= 16.0
    assert opening.TITLE_BEATS < opening.SHOTS[-1][1], "the title lands inside the last shot"


def test_every_shot_is_a_ledger_subject_pinned_to_one_still():
    ledger = yaml.safe_load(opening.LEDGER.read_text())
    subjects = {subject["key"]: subject for subject in ledger["subjects"]}
    for key, _ in opening.SHOTS:
        subject = subjects[key]
        assert subject["source_image_id"] == subject["last_image_id"], f"{key} stays on its approved still"


def test_shot_sources_use_done_clips_unless_stills_only():
    ledger = {
        "subjects": [
            {"key": key, "source_image_id": 100 + i, "art": {"wan-clips": {"status": "DONE", "art_image_id": 900 + i}}}
            if i == 0
            else {"key": key, "source_image_id": 100 + i, "art": {"wan-clips": {"status": "PENDING"}}}
            for i, (key, _) in enumerate(opening.SHOTS)
        ]
    }
    sources = list(opening.shot_sources(ledger, stills_only=False))
    assert sources[0][2:] == (100, 900)
    assert all(clip is None for *_, clip in sources[1:])
    assert all(clip is None for *_, clip in opening.shot_sources(ledger, stills_only=True))


def test_manifest_rewrite_round_trips(tmp_path):
    manifest = tmp_path / opening.MANIFEST
    manifest.parent.mkdir(parents=True)
    manifest.write_text(
        "export type RainbowOpeningMedia = {}\n\n"
        "// Written by conductor scripts/export_rainbow_opening.py from what it shipped. Do not edit by hand.\n"
        "export const RAINBOW_OPENING: RainbowOpeningMedia | null = null\n"
    )
    media = {"webm": "/v/o.webm", "mp4": "/v/o.mp4", "poster": "/v/p.webp", "seconds": 15.0, "clips": 2, "shots": 9}
    opening.write_manifest(tmp_path, media)
    text = manifest.read_text()
    assert "  seconds: 15,\n" in text, "a whole number prints the way Prettier keeps it"
    assert "  clips: 2,\n" in text
    opening.write_manifest(tmp_path, {**media, "clips": 9})
    text = manifest.read_text()
    assert text.count("export const RAINBOW_OPENING") == 1
    assert "  clips: 9,\n" in text
    opening.write_manifest(tmp_path, None)
    assert manifest.read_text().endswith("export const RAINBOW_OPENING: RainbowOpeningMedia | null = null\n")
