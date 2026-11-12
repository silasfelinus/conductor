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
