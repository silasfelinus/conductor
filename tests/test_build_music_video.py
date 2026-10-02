"""Tests for scripts/build_music_video.py (music-video/t-021).

The pipeline is only trustworthy if three things hold, so those are what this
file pins:

1. Resume never re-enqueues: plan_actions chooses each step from what the
   MusicVideo doc and its ArtJobs already hold, and a run whose renders are in
   flight only waits.
2. The timeline semantics match the doc: scene starts are honoured, a cut lands
   on its boundary, and a crossfade overlaps without shortening the video.
3. The ffmpeg graph actually renders: one real end-to-end assembly from
   generated stills and a silent song, checked with ffprobe.
"""

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_music_video.py"
spec = importlib.util.spec_from_file_location("build_music_video", SCRIPT)
bmv = importlib.util.module_from_spec(spec)
sys.modules["build_music_video"] = bmv
spec.loader.exec_module(bmv)


def scene(sid, start, end, *, prompt="a brass robot", art=None, job=None, transition="cut", tsec=0.0):
    image = {"source": "generated"}
    if art:
        image["artImageId"] = art
    if job:
        image["jobId"] = job
    return {
        "id": sid,
        "startSec": start,
        "endSec": end,
        "prompt": prompt,
        "image": image,
        "motion": {"kind": "kenburns"},
        "transition": transition,
        "transitionSec": tsec,
    }


def doc(*, lyrics=True, vocal="male", song=None, scenes=None):
    return {
        "settings": {"durationSec": 8, "vocal": vocal, "aspect": "16:9"},
        "lyrics": {"sections": [{"id": "v1", "lines": ["hello"]}] if lyrics else []},
        "song": song,
        "scenes": scenes or [],
    }


# ---------------------------------------------------------------- resume plan


def test_fresh_video_writes_lyrics_first_and_nothing_else():
    assert bmv.plan_actions(bmv.RunState(doc(lyrics=False))) == ["lyrics"]


def test_instrumental_skips_lyrics_and_starts_song_and_scene_plan():
    state = bmv.RunState(doc(lyrics=False, vocal="instrumental"))
    assert bmv.plan_actions(state) == ["song", "plan_scenes"]


def test_planned_scenes_get_prompts_then_renders_while_song_renders():
    scenes = [scene("s1", 0, 4, prompt=""), scene("s2", 4, 8, prompt="")]
    state = bmv.RunState(
        doc(song={"source": "comfy-acestep", "jobId": 7}, scenes=scenes),
        song_job=bmv.JobState("PENDING"),
    )
    assert bmv.plan_actions(state) == ["scene_prompts", "render_scenes", "wait"]


def test_everything_in_flight_only_waits():
    scenes = [scene("s1", 0, 4, job=11), scene("s2", 4, 8, job=12)]
    state = bmv.RunState(
        doc(song={"source": "comfy-acestep", "jobId": 7}, scenes=scenes),
        song_job=bmv.JobState("RUNNING"),
        scene_jobs={"s1": bmv.JobState("PENDING"), "s2": bmv.JobState("RUNNING")},
    )
    assert bmv.plan_actions(state) == ["wait"]


def test_failed_jobs_are_retried_and_nothing_else_is():
    scenes = [scene("s1", 0, 4, art=101, job=11), scene("s2", 4, 8, job=12)]
    state = bmv.RunState(
        doc(song={"source": "comfy-acestep", "jobId": 7}, scenes=scenes),
        song_job=bmv.JobState("FAILED", error="oom"),
        scene_jobs={"s1": bmv.JobState("DONE", 101), "s2": bmv.JobState("FAILED")},
    )
    assert bmv.plan_actions(state) == ["song_retry", "render_scenes", "wait"]


def test_done_jobs_count_even_before_the_doc_syncs():
    scenes = [scene("s1", 0, 4, job=11), scene("s2", 4, 8, art=102, job=12)]
    state = bmv.RunState(
        doc(song={"source": "comfy-acestep", "jobId": 7}, scenes=scenes),
        song_job=bmv.JobState("DONE", 900),
        scene_jobs={"s1": bmv.JobState("DONE", 101)},
    )
    assert bmv.plan_actions(state) == ["assemble"]


def test_finished_run_only_assembles():
    scenes = [scene("s1", 0, 4, art=101), scene("s2", 4, 8, art=102)]
    state = bmv.RunState(doc(song={"source": "comfy-acestep", "artImageId": 900}, scenes=scenes))
    assert bmv.plan_actions(state) == ["assemble"]


# ------------------------------------------------------------- timeline math


def ts(sid, start, end, transition="cut", tsec=0.0, preset="zoom-in"):
    return bmv.TimelineScene(sid, start, end, Path(f"{sid}.png"), False, preset, transition, tsec)


def test_cut_durations_land_on_boundaries_and_crossfades_extend_the_outgoing_scene():
    scenes = [ts("s1", 0, 4), ts("s2", 4, 8, "crossfade", 0.5), ts("s3", 8, 10)]
    assert bmv.scene_durations(scenes) == [4.5, 4.0, 2.0]


def test_gaps_are_held_by_the_previous_scene():
    assert bmv.scene_durations([ts("s1", 0, 3), ts("s2", 4, 6)]) == [4.0, 2.0]


def test_filter_graph_uses_concat_for_cuts_and_xfade_at_the_scene_start():
    scenes = [ts("s1", 0, 4), ts("s2", 4, 8, "crossfade", 0.5), ts("s3", 8, 10)]
    graph, label = bmv.build_filter_graph(scenes, 1280, 720, 30)
    assert label == "x2"
    assert "[v0][v1]xfade=transition=fade:duration=0.500:offset=4.000[x1]" in graph
    assert "[x1][v2]concat=n=2:v=1:a=0[x2]" in graph
    assert "zoompan=" in graph and "d=135:" in graph  # 4.5 s at 30 fps
    assert "s=1280x720:fps=30" in graph


def test_ken_burns_presets_differ_and_unknown_falls_back_to_zoom_in():
    seen = {bmv.ken_burns_expressions(p, 60) for p in bmv.KEN_BURNS_PRESETS}
    assert len(seen) == len(bmv.KEN_BURNS_PRESETS)
    assert bmv.ken_burns_expressions("nope", 60) == bmv.ken_burns_expressions("zoom-in", 60)


def test_ffmpeg_command_maps_scenes_then_song():
    scenes = [ts("s1", 0, 4), ts("s2", 4, 8)]
    command = bmv.build_ffmpeg_command(scenes, Path("song.mp3"), Path("out.mp4"), 1280, 720, 30, 8.0)
    inputs = [command[i + 1] for i, arg in enumerate(command) if arg == "-i"]
    assert inputs == ["s1.png", "s2.png", "song.mp3"]
    assert command[command.index("-map") + 1] == "[x1]"
    assert "2:a" in command
    assert command[command.index("-t") + 1] == "8.000"
    assert command[-1] == "out.mp4"


def test_timeline_from_doc_sorts_assigns_presets_and_requires_assets():
    raw = doc(scenes=[scene("s2", 4, 8, transition="crossfade", tsec=0.5), scene("s1", 0.2, 4)])
    assets = {"s1": Path("a.png"), "s2": Path("b.png")}
    timeline = bmv.timeline_from_doc(raw, assets)
    assert [s.scene_id for s in timeline] == ["s1", "s2"]
    assert timeline[0].start == 0.0
    assert [s.preset for s in timeline] == ["zoom-in", "pan-right"]
    assert timeline[1].transition == "crossfade" and timeline[1].transition_sec == 0.5
    with pytest.raises(bmv.PipelineError):
        bmv.timeline_from_doc(raw, {"s1": Path("a.png")})


# --------------------------------------------------------------- end to end


@pytest.mark.skipif(not shutil.which("ffmpeg") or not shutil.which("ffprobe"), reason="ffmpeg not installed")
def test_real_ffmpeg_assembly(tmp_path):
    def run(*args):
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args], check=True)

    colours = {"s1": "red", "s2": "green", "s3": "blue"}
    for sid, colour in colours.items():
        run("-f", "lavfi", "-i", f"color=c={colour}:s=320x180", "-frames:v", "1", str(tmp_path / f"{sid}.png"))
    song = tmp_path / "song.wav"
    run("-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "3", str(song))

    scenes = [
        bmv.TimelineScene("s1", 0, 1, tmp_path / "s1.png", preset="zoom-in"),
        bmv.TimelineScene("s2", 1, 2, tmp_path / "s2.png", preset="pan-left", transition="crossfade", transition_sec=0.25),
        bmv.TimelineScene("s3", 2, 3, tmp_path / "s3.png", preset="zoom-out"),
    ]
    out = tmp_path / "out.mp4"
    subprocess.run(bmv.build_ffmpeg_command(scenes, song, out, 160, 90, 12, 3.0), check=True)

    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height:format=duration", "-of", "json", str(out)],
        check=True,
        capture_output=True,
        text=True,
    )
    info = json.loads(probe.stdout)
    assert abs(float(info["format"]["duration"]) - 3.0) < 0.2
    kinds = {stream["codec_type"] for stream in info["streams"]}
    assert kinds == {"video", "audio"}
    video = next(s for s in info["streams"] if s["codec_type"] == "video")
    assert (video["width"], video["height"]) == (160, 90)


# ---------------------------------------------------------------------- CLI


def test_cli_needs_a_pitch_or_a_video_id(capsys):
    assert bmv.main([]) == bmv.EXIT_CONFIG


def test_dry_run_without_a_video_needs_no_token(monkeypatch, capsys):
    monkeypatch.setattr(bmv, "KR_API_TOKEN", "")
    assert bmv.main(["--dry-run", "--pitch", "robots in a garden", "--duration", "45"]) == bmv.EXIT_DONE
    out = capsys.readouterr().out
    assert "DRY RUN" in out and '"durationSec": 45.0' in out


def test_missing_token_is_reported_without_printing_any_value(monkeypatch, capsys):
    monkeypatch.setattr(bmv, "KR_API_TOKEN", "")
    assert bmv.main(["--video-id", "5"]) == bmv.EXIT_CONFIG
    assert "KR_API_TOKEN is not set" in capsys.readouterr().err


class FakeClient:
    """A MusicVideo whose song and scenes are all still rendering."""

    def __init__(self, *_args, **_kwargs):
        self.calls = []

    def get_video(self, video_id):
        scenes = [scene("s1", 0, 4, job=11), scene("s2", 4, 8, job=12)]
        return {"id": video_id, "doc": doc(song={"source": "comfy-acestep", "jobId": 7}, scenes=scenes)}

    def song_status(self, video_id):
        return {"job": {"id": 7, "status": "RUNNING", "artImageId": None, "error": None}}

    def scene_status(self, video_id):
        return [
            {"sceneId": "s1", "jobId": 11, "status": "PENDING", "artImageId": None, "error": None},
            {"sceneId": "s2", "jobId": 12, "status": "RUNNING", "artImageId": None, "error": None},
        ]

    def __getattr__(self, name):
        def record(*args, **kwargs):
            self.calls.append(name)
            return {}

        return record


def test_resume_with_renders_in_flight_enqueues_nothing(monkeypatch, capsys):
    clients = []

    def make(*args, **kwargs):
        client = FakeClient()
        clients.append(client)
        return client

    monkeypatch.setattr(bmv, "KR_API_TOKEN", "test-token-value")
    monkeypatch.setattr(bmv, "KrClient", make)
    assert bmv.main(["--video-id", "5"]) == bmv.EXIT_IN_PROGRESS
    assert clients[0].calls == []
    out = capsys.readouterr().out
    assert "next: wait" in out
    assert "test-token-value" not in out


# ------------------------------------------------------- scene clips (t-009)


def clip_scene(sid, start, end, art, clip_job=None, clip_art=None):
    data = scene(sid, start, end, art=art)
    data["motion"] = {"kind": "clip", "preset": "zoom-in"}
    if clip_job:
        data["motion"]["jobId"] = clip_job
    if clip_art:
        data["motion"]["clipArtImageId"] = clip_art
    return data


def finished_song():
    return {"source": "comfy-acestep", "artImageId": 900}


def test_a_rendering_clip_is_waited_for():
    state = bmv.RunState(
        doc(song=finished_song(), scenes=[clip_scene("s1", 0, 4, 101, clip_job=55)]),
        clip_jobs={"s1": bmv.JobState("RUNNING")},
    )
    assert bmv.plan_actions(state) == ["wait"]


def test_a_failed_clip_falls_back_to_ken_burns_instead_of_blocking():
    state = bmv.RunState(
        doc(song=finished_song(), scenes=[clip_scene("s1", 0, 4, 101, clip_job=55)]),
        clip_jobs={"s1": bmv.JobState("FAILED", error="oom")},
    )
    assert bmv.plan_actions(state) == ["assemble"]
    timeline = bmv.timeline_from_doc(state.doc, {"s1": Path("still.png")})
    assert timeline[0].is_clip is False
    assert timeline[0].preset == "zoom-in"


def test_a_finished_clip_is_used_for_its_scene():
    raw = doc(song=finished_song(), scenes=[clip_scene("s1", 0, 4, 101, clip_art=77)])
    assert bmv.plan_actions(bmv.RunState(raw)) == ["assemble"]
    timeline = bmv.timeline_from_doc(raw, {"s1": Path("still.png"), "s1:clip": Path("clip.mp4")})
    assert timeline[0].is_clip is True
    assert timeline[0].source == Path("clip.mp4")


def test_read_state_picks_up_clip_rows():
    class ClipClient(FakeClient):
        def get_video(self, video_id):
            return {"id": video_id, "doc": doc(song=finished_song(), scenes=[clip_scene("s1", 0, 4, 101, clip_job=55)])}

        def scene_status(self, video_id):
            return [
                {
                    "sceneId": "s1",
                    "jobId": None,
                    "status": "READY",
                    "artImageId": 101,
                    "error": None,
                    "clipJobId": 55,
                    "clipStatus": "PENDING",
                    "clipArtImageId": None,
                    "clipError": None,
                }
            ]

    state = bmv.read_state(ClipClient(), 9)
    assert state.clip_jobs["s1"].status == "PENDING"
    assert "s1" not in state.scene_jobs
    assert bmv.plan_actions(state) == ["wait"]


def test_preset_names_match_kind_robots_motion_contract():
    # kind_robots utils/musicVideoMotion.ts MUSIC_VIDEO_KEN_BURNS_PRESETS
    assert bmv.KEN_BURNS_PRESETS == ("zoom-in", "pan-right", "zoom-out", "pan-left")
