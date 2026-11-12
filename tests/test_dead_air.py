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
    assert sum(s["motion"] == "clip" for s in episode["shots"]) >= 2
    assert len(episode["references"]) >= 3
    assert all(r["transformation"] and r["assets"] for r in episode["references"])


def test_shot_timing_must_have_no_gap_or_overlap():
    original = load_episode(PILOT)
    changed = {**original, "shots": [dict(s) for s in original["shots"]]}
    changed["shots"][2]["start"] = 5.4
    assert any("boundary" in error for error in validate(changed))


def test_still_only_is_not_a_finished_film():
    original = load_episode(PILOT)
    changed = {**original, "shots": [dict(s) for s in original["shots"]]}
    for shot in changed["shots"]:
        shot["motion"] = "kenburns"
    assert any("real clip" in error for error in validate(changed))


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
    assert sum(s["motion"]["kind"] == "clip" for s in scenes) >= 2
    assert all(s["promptSource"] == "user" for s in scenes)
    assert all(original["visual_style"] in s["prompt"] for s in scenes)


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
