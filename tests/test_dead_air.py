"""Dead Air's dates, motion requirements and resumable artist contract."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from dead_air_produce import load_episode, validate, scenes_for, choose_episode


PILOT = ROOT / "projects/dead-air/episodes/2026-11-12-closed-caption-department.yaml"


def test_pilot_is_original_multishot_film_brief():
    episode = load_episode(PILOT)
    assert not validate(episode)
    assert episode["duration_seconds"] == 15
    assert len(episode["shots"]) == 5
    assert sum(s["motion"] == "clip" for s in episode["shots"]) == 1
    assert len(episode["references"]) >= 3
    assert all(r["transformation"] and r["assets"] for r in episode["references"])


def test_shot_timing_must_have_no_gap_or_overlap():
    original = load_episode(PILOT)
    changed = {**original, "shots": [dict(s) for s in original["shots"]]}
    changed["shots"][2]["start"] = 5.4
    assert any("boundary" in error for error in validate(changed))


def test_clip_free_kinetic_animation_is_accepted():
    original = load_episode(PILOT)
    changed = {**original, "shots": [dict(s) for s in original["shots"]]}
    for shot in changed["shots"]:
        shot["motion"] = "kenburns"
    assert not validate(changed)
    changed["shots"][0]["motion"] = "still"
    assert any("motion type" in error for error in validate(changed))


def test_pop_culture_references_have_provenance():
    original = load_episode(PILOT)
    changed = {**original, "references": []}
    assert any("pop-culture references" in error for error in validate(changed))


def test_movie_doc_has_correct_continuity_and_motion_contract():
    original = load_episode(PILOT)
    scenes = scenes_for(original)
    assert len(scenes) == 5
    assert scenes[0]["startSec"] == 0
    assert scenes[-1]["endSec"] == 15
    assert sum(s["motion"]["kind"] == "clip" for s in scenes) == 1
    assert all(s["promptSource"] == "user" for s in scenes)
    assert all(s["prompt"] == shot["image_prompt"] for s, shot in zip(scenes, original["shots"]))


def test_daily_selection_resumes_oldest_not_newest(monkeypatch, tmp_path):
    import dead_air_produce
    from shutil import copyfile
    episode_dir = tmp_path / "episodes"
    episode_dir.mkdir()
    copyfile(PILOT, episode_dir / PILOT.name)
    monkeypatch.setattr(dead_air_produce, "EPISODES", episode_dir)
    assert choose_episode({"episodes": {}}, "2026-11-11") is None
    assert choose_episode({"episodes": {}}, "2026-11-12") == episode_dir / PILOT.name
    state = {"episodes": {"closed-caption-department": {"status": "rendering"}}}
    assert choose_episode(state, "2026-11-13") == episode_dir / PILOT.name
    state["episodes"]["closed-caption-department"]["status"] = "completed"
    assert choose_episode(state, "2026-11-13") is None


def test_krea_prompt_grammar_is_checked_before_live_writes():
    from dead_air_produce import paint_prompt_problems
    episode = load_episode(PILOT)
    assert not paint_prompt_problems(episode["visual_style"])
    assert all(not paint_prompt_problems(s["image_prompt"]) for s in episode["shots"])
    assert paint_prompt_problems("close-up with caption and logo")
    assert paint_prompt_problems("no captions")


def test_renderer_http_success_without_artjob_ids_is_failure():
    import pytest
    from dead_air_produce import verify_enqueue_outcomes, PipelineError

    rejected = [
        {"sceneId": "s1", "status": "rejected", "reason": "lettering: caption"},
        {"sceneId": "s2", "status": "failed", "reason": "checkpoint unavailable"},
    ]
    with pytest.raises(PipelineError, match="still ArtJobs not created"):
        verify_enqueue_outcomes(rejected, 2)
    with pytest.raises(PipelineError, match="outcomes"):
        verify_enqueue_outcomes([], 2)

    accepted = [
        {"sceneId": "s1", "status": "queued", "jobId": 111},
        {"sceneId": "s2", "status": "reused", "jobId": 112},
    ]
    assert verify_enqueue_outcomes(accepted, 2) == {"s1": 111, "s2": 112}


def test_prompt_rendering_does_not_repeat_style_bible():
    episode = load_episode(PILOT)
    scenes = scenes_for(episode)
    assert all(scene["prompt"] == shot["image_prompt"]
               for scene, shot in zip(scenes, episode["shots"]))


def test_gpu_clip_budget_is_one_per_film():
    original = load_episode(PILOT)
    altered = {**original, "shots": [dict(s) for s in original["shots"]]}
    altered["shots"][0]["motion"] = "clip"
    assert any("at most 1" in e for e in validate(altered))


def test_production_budget_cannot_be_reset_by_retry():
    from datetime import datetime, timedelta
    from zoneinfo import ZoneInfo
    from dead_air_produce import production_budget, MAX_PRODUCTION_SECONDS
    began = datetime(2026, 11, 12, 2, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
    row = {"started_pt": began.isoformat(), "updated_pt": (began + timedelta(hours=1, minutes=50)).isoformat()}
    elapsed, expired = production_budget(row, began + timedelta(minutes=119))
    assert elapsed == 7140 and expired is False
    elapsed, expired = production_budget(row, began + timedelta(hours=2))
    assert elapsed == MAX_PRODUCTION_SECONDS and expired is True


def test_assembly_accepts_motion_fallback_only_after_deadline():
    from types import SimpleNamespace
    from dead_air_produce import ready_for_export
    episode = load_episode(PILOT)
    scenes = scenes_for(episode)
    for i, scene in enumerate(scenes):
        scene["image"]["artImageId"] = 10 + i
    state = SimpleNamespace(doc={"song": {"artImageId": 77}, "scenes": scenes}, scene_jobs={}, clip_jobs={})
    assert not ready_for_export(state, episode, deadline_hit=False)
    assert ready_for_export(state, episode, deadline_hit=True)
    state.doc["song"] = {}
    assert not ready_for_export(state, episode, deadline_hit=True)


def test_future_episode_seeds_are_valid_and_context_free():
    for slug in (
        "2026-11-13-plot-assist.yaml",
        "2026-11-14-clap-credit.yaml",
        "2026-11-15-apology-orchard.yaml",
        "2026-11-16-tomorrow-hotline.yaml",
        "2026-11-17-empty-square-realty.yaml",
        "2026-11-18-yesterdays-weather.yaml",
        "2026-11-19-opinion-zoo.yaml",
        "2026-11-20-ghost-exit-interview.yaml",
    ):
        e = load_episode(PILOT.parent / slug)
        assert len(e["shots"]) == 5
        assert sum(s["motion"] == "clip" for s in e["shots"]) <= 1
        assert e["product"] and e["reveal"]
        assert all(s["camera_preset"] in ("zoom-in", "zoom-out", "pan-left", "pan-right")
                   for s in e["shots"])


def test_no_second_daily_film_after_a_completed_screening(monkeypatch, tmp_path):
    import dead_air_produce
    from shutil import copyfile
    episode_dir = tmp_path / "episodes"
    episode_dir.mkdir()
    for name in ("2026-11-12-closed-caption-department.yaml", "2026-11-13-plot-assist.yaml"):
        copyfile(PILOT.parent / name, episode_dir / name)
    monkeypatch.setattr(dead_air_produce, "EPISODES", episode_dir)
    state = {"episodes": {
        "closed-caption-department": {"status": "completed", "completed_pt": "2026-11-13"}
    }}
    assert choose_episode(state, "2026-11-13") is None
    assert choose_episode(state, "2026-11-14") == episode_dir / "2026-11-13-plot-assist.yaml"


def test_camera_motion_comes_from_storyboard_not_round_robin():
    original = load_episode(PILOT)
    scenes = scenes_for(original)
    assert all(sc["motion"]["preset"] == sh["camera_preset"]
               for sc, sh in zip(scenes, original["shots"]))


def test_new_pacific_date_allows_recovery_without_new_episode_id():
    from datetime import datetime, timedelta
    from zoneinfo import ZoneInfo
    from dead_air_produce import production_budget
    first = datetime(2026, 11, 12, 1, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
    row = {
        "music_video_id": 18, "art_jobs": {"stills": {"s1": 68688}},
        "started_pt": first.isoformat(),
        "budget_day": first.date().isoformat(),
        "budget_started_pt": first.isoformat(),
    }
    _, expired = production_budget(row, first + timedelta(hours=2))
    assert expired
    # A later date can continue this exact MusicVideo with a new daily window.
    next_day = first + timedelta(days=1)
    elapsed, expired = production_budget(row, next_day)
    assert (elapsed, expired) == (0, False)
    row.update(budget_day=next_day.date().isoformat(), budget_started_pt=next_day.isoformat())
    elapsed, expired = production_budget(row, next_day + timedelta(minutes=45))
    assert (elapsed, expired) == (2700, False)
    assert row["music_video_id"] == 18
    assert row["art_jobs"]["stills"]["s1"] == 68688


def test_still_wait_observations_are_per_shot_and_never_invent_gpu_runtime():
    from datetime import datetime, timedelta
    from types import SimpleNamespace
    from zoneinfo import ZoneInfo
    from dead_air_produce import observe_still_waits, should_skip_optional_clip
    first = datetime(2026, 11, 14, 1, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
    scenes = [
        {"id": "s1", "image": {"jobId": 100}},
        {"id": "s2", "image": {"jobId": 101}},
    ]
    state = SimpleNamespace(
        doc={"scenes": scenes},
        scene_jobs={
            "s1": SimpleNamespace(status="QUEUED", art_image_id=None),
            "s2": SimpleNamespace(status="DONE", art_image_id=55),
        },
    )
    row = {"updated_pt": first.isoformat()}
    observe_still_waits(row, state, first)
    samples = row["still_render_observations"]
    assert "observed_wait_seconds" not in samples["s1"]
    assert "observed_wait_seconds" not in samples["s2"]

    second = first + timedelta(minutes=37)
    state.scene_jobs["s1"] = SimpleNamespace(status="DONE", art_image_id=54)
    observe_still_waits(row, state, second)
    assert samples["s1"]["observed_wait_seconds"] == 37 * 60
    assert "observed_wait_seconds" not in samples["s2"]
    assert should_skip_optional_clip({"episodes": {"pilot": row}}, 10, second)


def test_congested_pending_still_skips_clip_but_fresh_queue_does_not():
    from datetime import datetime, timedelta
    from zoneinfo import ZoneInfo
    from dead_air_produce import should_skip_optional_clip
    start = datetime(2026, 11, 14, 1, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
    row = {
        "updated_pt": start.isoformat(),
        "still_render_observations": {
            "s1": {
                "job_id": 12, "first_seen_pt": start.isoformat(),
                "first_seen_status": "QUEUED",
            },
        },
    }
    state = {"episodes": {"pilot": row}}
    assert not should_skip_optional_clip(state, 60, start + timedelta(minutes=10))
    assert should_skip_optional_clip(state, 60, start + timedelta(minutes=31))
    assert should_skip_optional_clip({"episodes": {}}, 90 * 60)


def test_next_seven_seed_films_have_original_visuals_and_story_progression():
    from datetime import date, timedelta

    base = date(2026, 11, 14)
    seeded = [load_episode(path) for path in PILOT.parent.glob("*.yaml")]
    by_date = {item["date"]: item for item in seeded}
    assert len(by_date) == len(seeded)  # one source episode per proposed broadcast day
    runway = [(base + timedelta(days=n)).isoformat() for n in range(7)]
    assert set(runway).issubset(by_date)
    assert len({by_date[d]["visual_style"] for d in runway}) == 7
    all_prompts = [shot["image_prompt"] for d in runway
                   for shot in by_date[d]["shots"]]
    assert len(all_prompts) == len(set(all_prompts))
    assert all(len(by_date[d]["references"]) >= 3 for d in runway)
    assert all(by_date[d]["status"] == "authored" for d in runway)
    assert all(sum(s["motion"] == "clip" for s in by_date[d]["shots"]) <= 1
               for d in runway)


def _synthetic_voice(tmp_path, seconds=8.5):
    import subprocess
    voice = tmp_path / "voice.wav"
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                    f"sine=frequency=300:duration={seconds}", "-af", "volume=2", str(voice)],
                   check=True)
    return voice


def test_mix_keeps_station_bed_audible_after_voiceover(tmp_path):
    """2026-11-14 review: MusicVideos 18/19 fell to -55 dB for 4-6s after the VO ended."""
    import shutil
    import pytest
    if not shutil.which("ffmpeg"):
        pytest.skip("ffmpeg unavailable")
    from dead_air_produce import mix_audio, longest_quiet_run
    song = mix_audio(_synthetic_voice(tmp_path), {}, tmp_path)
    assert longest_quiet_run(song) <= 0.6


def test_authored_silent_tail_is_short_and_honored(tmp_path):
    import shutil
    import pytest
    if not shutil.which("ffmpeg"):
        pytest.skip("ffmpeg unavailable")
    from dead_air_produce import mix_audio, longest_quiet_run
    song = mix_audio(_synthetic_voice(tmp_path), {"silent_tail_seconds": 1.0}, tmp_path)
    assert 0.8 <= longest_quiet_run(song) <= 1.6
    episode = load_episode(PILOT)
    assert any("silent_tail" in p for p in validate({**episode, "silent_tail_seconds": 4}))
    assert not validate({**episode, "silent_tail_seconds": 1.0})


def test_quiet_run_detector_flags_the_old_near_silent_tail(tmp_path):
    import shutil
    import subprocess
    import pytest
    if not shutil.which("ffmpeg"):
        pytest.skip("ffmpeg unavailable")
    from dead_air_produce import longest_quiet_run
    track = tmp_path / "old.mp3"
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error",
                    "-f", "lavfi", "-i", "sine=frequency=300:duration=9",
                    "-af", "volume=2,apad,atrim=duration=15", "-c:a", "libmp3lame", str(track)],
                   check=True)
    assert longest_quiet_run(track) >= 5.5
