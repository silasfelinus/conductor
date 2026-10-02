#!/usr/bin/env python3
"""Agent-run music video pipeline: pitch to finished MP4, no human in the loop.

music-video/t-021. The browser exporter (t-014) needs someone at a screen, so
the first-run trailer (t-015) is built here instead. This drives the Kind
Robots music-video API (all admin-only) and assembles the result with ffmpeg:

    create MusicVideo -> write lyrics -> enqueue song (ACE-Step)
    -> plan scenes on the beat grid -> write scene prompts -> enqueue stills
    -> poll the ArtJobs -> download song + stills -> ffmpeg -> MP4

Renders take hours on the single 12 GB card, so every run RESUMES from the
MusicVideo doc and its ArtJobs: each step is chosen from what the doc already
holds (see plan_actions), and the scene render endpoint dedupes on its own, so
re-running never re-enqueues finished or in-flight work.

Usage:
    # Plan only: print what would happen, enqueue nothing.
    python scripts/build_music_video.py --dry-run --pitch "..." --title "..."
    # Start a run (prints the new video id; pass it back to resume).
    python scripts/build_music_video.py --pitch "..." --title "..." --duration 60
    # Resume and wait for renders, then assemble.
    python scripts/build_music_video.py --video-id 12 --wait --out trailer.mp4

KR_API_TOKEN must belong to an admin. Only its presence is ever checked or
reported; it is never printed. Exit codes: 0 finished (MP4 written, or the
dry-run plan printed), 3 still rendering (re-run later, or pass --wait),
1 error, 2 missing configuration.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kindrobots.org").rstrip("/")
KR_API_TOKEN = os.environ.get("KR_API_TOKEN", "").strip()

EXIT_DONE = 0
EXIT_ERROR = 1
EXIT_CONFIG = 2
EXIT_IN_PROGRESS = 3

ACTIVE_JOB_STATUSES = {"PENDING", "RUNNING"}
FAILED_JOB_STATUSES = {"FAILED", "CANCELLED"}

FRAME_SIZES = {
    "16:9": (1280, 720),
    "9:16": (720, 1280),
    "1:1": (1080, 1080),
}
DEFAULT_FPS = 30

# Ken Burns presets. These names are a contract with kind_robots
# utils/musicVideoMotion.ts (MUSIC_VIDEO_KEN_BURNS_PRESETS, music-video/t-009):
# keep the tuple identical, in the same order, since both sides assign a scene
# without a preset the one at its position.
KEN_BURNS_PRESETS = ("zoom-in", "pan-right", "zoom-out", "pan-left")
KEN_BURNS_ZOOM = 0.15


class PipelineError(Exception):
    pass


# --------------------------------------------------------------------------
# Resume planning (pure)
# --------------------------------------------------------------------------


@dataclass
class JobState:
    status: str
    art_image_id: int | None = None
    error: str | None = None


@dataclass
class RunState:
    """What the API currently says about one MusicVideo."""

    doc: dict
    song_job: JobState | None = None
    scene_jobs: dict[str, JobState] = field(default_factory=dict)
    clip_jobs: dict[str, JobState] = field(default_factory=dict)


def _scene_image_id(scene: dict, scene_jobs: dict[str, JobState]) -> int | None:
    image = scene.get("image") or {}
    if image.get("artImageId"):
        return int(image["artImageId"])
    job = scene_jobs.get(scene.get("id", ""))
    if job and job.status == "DONE" and job.art_image_id:
        return job.art_image_id
    return None


def _wants_lyrics(doc: dict) -> bool:
    vocal = (doc.get("settings") or {}).get("vocal")
    if vocal == "instrumental":
        return False
    sections = (doc.get("lyrics") or {}).get("sections") or []
    return not any(section.get("lines") for section in sections)


def plan_actions(state: RunState) -> list[str]:
    """The next steps for a run, in order, from what already exists.

    Returns a subset of: lyrics, song, song_retry, plan_scenes, scene_prompts,
    render_scenes, wait, assemble. "wait" means renders are in flight; nothing
    after it can run yet.
    """
    doc = state.doc
    actions: list[str] = []
    if _wants_lyrics(doc):
        # Song and scenes both read the lyrics, so nothing else can start.
        return ["lyrics"]

    song = doc.get("song") or None
    song_ready = bool(song and song.get("artImageId"))
    if not song_ready:
        if state.song_job and state.song_job.status == "DONE" and state.song_job.art_image_id:
            song_ready = True
        elif not song or not song.get("jobId"):
            actions.append("song")
        elif state.song_job is None or state.song_job.status in FAILED_JOB_STATUSES:
            actions.append("song_retry")

    scenes = doc.get("scenes") or []
    if not scenes:
        # Prompts and stills follow on the next pass, once the plan exists.
        actions.append("plan_scenes")
        return actions

    missing = [s for s in scenes if _scene_image_id(s, state.scene_jobs) is None]
    generated_missing = [
        s for s in missing if (s.get("image") or {}).get("source", "generated") == "generated"
    ]
    if any(not str(s.get("prompt") or "").strip() for s in generated_missing):
        actions.append("scene_prompts")

    needs_enqueue = [
        s
        for s in missing
        if str(s.get("prompt") or "").strip()
        and (
            not (s.get("image") or {}).get("jobId")
            or (state.scene_jobs.get(s["id"]) is not None and state.scene_jobs[s["id"]].status in FAILED_JOB_STATUSES)
        )
    ]
    if needs_enqueue or "scene_prompts" in actions:
        actions.append("render_scenes")

    # An opted-in clip still rendering is worth waiting for; a failed one is
    # not -- the scene keeps its Ken Burns preset and assembles without it.
    clips_pending = any(
        state.clip_jobs[s["id"]].status in ACTIVE_JOB_STATUSES
        for s in scenes
        if (s.get("motion") or {}).get("kind") == "clip"
        and not (s.get("motion") or {}).get("clipArtImageId")
        and s["id"] in state.clip_jobs
    )

    if missing or not song_ready or clips_pending:
        actions.append("wait")
    else:
        actions.append("assemble")
    return actions


# --------------------------------------------------------------------------
# Timeline -> ffmpeg (pure)
# --------------------------------------------------------------------------


@dataclass
class TimelineScene:
    scene_id: str
    start: float
    end: float
    source: Path
    is_clip: bool = False
    preset: str = "zoom-in"
    transition: str = "cut"  # how this scene ENTERS from the previous one
    transition_sec: float = 0.0


def ken_burns_expressions(preset: str, frames: int) -> tuple[str, str, str]:
    """zoompan z/x/y expressions for one preset over `frames` output frames."""
    n = max(frames - 1, 1)
    z_max = 1 + KEN_BURNS_ZOOM
    centre_x = "iw/2-(iw/zoom/2)"
    centre_y = "ih/2-(ih/zoom/2)"
    if preset == "zoom-out":
        return f"{z_max:.3f}-{KEN_BURNS_ZOOM:.3f}*on/{n}", centre_x, centre_y
    if preset == "pan-right":
        return f"{z_max:.3f}", f"(iw-iw/zoom)*on/{n}", centre_y
    if preset == "pan-left":
        return f"{z_max:.3f}", f"(iw-iw/zoom)*(1-on/{n})", centre_y
    return f"1+{KEN_BURNS_ZOOM:.3f}*on/{n}", centre_x, centre_y


def scene_durations(scenes: list[TimelineScene]) -> list[float]:
    """Seconds each scene's stream must last.

    A scene runs from its start to the next scene's start (holding through any
    gap), and the last one to its own end. When the NEXT scene crossfades in,
    this one is extended by that crossfade so the overlap does not shorten the
    video: the next scene still becomes fully visible at its own start time
    plus the fade, and every cut lands exactly on its scene boundary.
    """
    durations = []
    for index, scene in enumerate(scenes):
        if index + 1 < len(scenes):
            following = scenes[index + 1]
            length = following.start - scene.start
            if following.transition == "crossfade":
                length += following.transition_sec
        else:
            length = scene.end - scene.start
        if length <= 0:
            raise PipelineError(f"scene {scene.scene_id} has no duration")
        durations.append(round(length, 3))
    return durations


def build_filter_graph(
    scenes: list[TimelineScene], width: int, height: int, fps: int
) -> tuple[str, str]:
    """Return (filter_complex, final video label) for scenes as inputs 0..n-1."""
    if not scenes:
        raise PipelineError("no scenes to assemble")
    durations = scene_durations(scenes)
    parts: list[str] = []
    # Oversample before zoompan: zooming a frame-sized image steps visibly.
    big_w, big_h = width * 2, height * 2
    for index, (scene, duration) in enumerate(zip(scenes, durations)):
        frames = max(int(round(duration * fps)), 1)
        fit = (
            f"scale={big_w}:{big_h}:force_original_aspect_ratio=increase,"
            f"crop={big_w}:{big_h}"
        )
        if scene.is_clip:
            chain = (
                f"[{index}:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
                f"crop={width}:{height},fps={fps},"
                f"tpad=stop_mode=clone:stop_duration={duration:.3f},"
                f"trim=duration={duration:.3f},setpts=PTS-STARTPTS"
            )
        else:
            z, x, y = ken_burns_expressions(scene.preset, frames)
            chain = (
                f"[{index}:v]{fit},"
                f"zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={width}x{height}:fps={fps},"
                f"trim=duration={duration:.3f},setpts=PTS-STARTPTS"
            )
        parts.append(f"{chain},setsar=1,format=yuv420p[v{index}]")

    current = "v0"
    elapsed = durations[0]
    for index in range(1, len(scenes)):
        scene = scenes[index]
        out = f"x{index}"
        if scene.transition == "crossfade" and scene.transition_sec > 0:
            offset = elapsed - scene.transition_sec
            parts.append(
                f"[{current}][v{index}]xfade=transition=fade:"
                f"duration={scene.transition_sec:.3f}:offset={offset:.3f}[{out}]"
            )
            elapsed += durations[index] - scene.transition_sec
        else:
            parts.append(f"[{current}][v{index}]concat=n=2:v=1:a=0[{out}]")
            elapsed += durations[index]
        current = out
    return ";".join(parts), current


def build_ffmpeg_command(
    scenes: list[TimelineScene],
    song: Path,
    out: Path,
    width: int,
    height: int,
    fps: int = DEFAULT_FPS,
    total_sec: float | None = None,
) -> list[str]:
    filter_complex, video_label = build_filter_graph(scenes, width, height, fps)
    total = total_sec if total_sec is not None else scenes[-1].end
    command = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    for scene in scenes:
        command += ["-i", str(scene.source)]
    command += ["-i", str(song)]
    audio_index = len(scenes)
    command += [
        "-filter_complex",
        filter_complex,
        "-map",
        f"[{video_label}]",
        "-map",
        f"{audio_index}:a",
        "-t",
        f"{total:.3f}",
        "-r",
        str(fps),
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "20",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
        str(out),
    ]
    return command


def timeline_from_doc(doc: dict, assets: dict[str, Path]) -> list[TimelineScene]:
    """Scenes in time order, each pointing at its downloaded still or clip."""
    timeline = []
    ordered = sorted(doc.get("scenes") or [], key=lambda s: float(s.get("startSec", 0)))
    for index, scene in enumerate(ordered):
        scene_id = scene["id"]
        if scene_id not in assets:
            raise PipelineError(f"scene {scene_id} has no downloaded image")
        motion = scene.get("motion") or {}
        preset = str(motion.get("preset") or "")
        if preset not in KEN_BURNS_PRESETS:
            preset = KEN_BURNS_PRESETS[index % len(KEN_BURNS_PRESETS)]
        timeline.append(
            TimelineScene(
                scene_id=scene_id,
                start=float(scene["startSec"]),
                end=float(scene["endSec"]),
                source=assets[scene_id],
                is_clip=motion.get("kind") == "clip" and f"{scene_id}:clip" in assets,
                preset=preset,
                transition="crossfade" if scene.get("transition") == "crossfade" else "cut",
                transition_sec=float(scene.get("transitionSec") or 0),
            )
        )
    for scene in timeline:
        if scene.is_clip:
            scene.source = assets[f"{scene.scene_id}:clip"]
    if timeline and timeline[0].start > 0:
        timeline[0].start = 0.0
    return timeline


# --------------------------------------------------------------------------
# Kind Robots API (IO)
# --------------------------------------------------------------------------


class KrClient:
    def __init__(self, base_url: str, token: str, timeout: int = 120):
        self.base_url = base_url.rstrip("/")
        self._token = token
        self.timeout = timeout

    def _request(self, method: str, path: str, body: Any = None) -> dict:
        data = json.dumps(body).encode() if body is not None else None
        request = urllib.request.Request(f"{self.base_url}{path}", data=data, method=method)
        request.add_header("Content-Type", "application/json")
        request.add_header("Authorization", f"Bearer {self._token}")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                payload = json.loads(response.read().decode() or "null")
        except urllib.error.HTTPError as error:
            try:
                payload = json.loads(error.read().decode() or "null")
            except (ValueError, OSError):
                payload = None
            message = (payload or {}).get("message") if isinstance(payload, dict) else None
            raise PipelineError(f"{method} {path} -> HTTP {error.code}: {message or 'no message'}") from error
        except urllib.error.URLError as error:
            raise PipelineError(f"could not reach {self.base_url}: {error.reason}") from error
        if not isinstance(payload, dict) or payload.get("success") is False:
            message = payload.get("message") if isinstance(payload, dict) else payload
            raise PipelineError(f"{method} {path} failed: {message}")
        return payload

    def create_video(self, title: str, pitch: str, settings: dict) -> dict:
        return self._request(
            "POST", "/api/music-video", {"title": title, "pitch": pitch, "settings": settings}
        )["data"]

    def get_video(self, video_id: int) -> dict:
        return self._request("GET", f"/api/music-video/{video_id}")["data"]

    def write_lyrics(self, video_id: int) -> None:
        self._request("POST", f"/api/music-video/{video_id}/lyrics", {})

    def enqueue_song(self, video_id: int, force: bool = False) -> dict:
        return self._request("POST", f"/api/music-video/{video_id}/song", {"force": force})["data"]

    def song_status(self, video_id: int) -> dict:
        return self._request("GET", f"/api/music-video/{video_id}/song")["data"]

    def plan_scenes(self, video_id: int) -> None:
        self._request("POST", f"/api/music-video/{video_id}/scenes/plan", {})

    def write_scene_prompts(self, video_id: int) -> dict:
        return self._request("POST", f"/api/music-video/{video_id}/scenes/prompts", {})["data"]

    def render_scenes(self, video_id: int) -> dict:
        return self._request("POST", f"/api/music-video/{video_id}/scenes/render", {})["data"]

    def scene_status(self, video_id: int) -> list[dict]:
        return self._request("GET", f"/api/music-video/{video_id}/scenes/status")["data"]["scenes"]

    def download_art(self, art_image_id: int, destination: Path) -> Path:
        request = urllib.request.Request(f"{self.base_url}/api/art/images/{art_image_id}/file")
        request.add_header("Authorization", f"Bearer {self._token}")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                destination.write_bytes(response.read())
        except urllib.error.URLError as error:
            raise PipelineError(f"download of ArtImage {art_image_id} failed: {error}") from error
        return destination


def read_state(client: KrClient, video_id: int) -> RunState:
    doc = client.get_video(video_id)["doc"]
    state = RunState(doc=doc)
    if (doc.get("song") or {}).get("jobId"):
        job = client.song_status(video_id).get("job")
        if job:
            state.song_job = JobState(job["status"], job.get("artImageId"), job.get("error"))
    if doc.get("scenes"):
        for row in client.scene_status(video_id):
            if row.get("jobId"):
                state.scene_jobs[row["sceneId"]] = JobState(
                    row["status"], row.get("artImageId"), row.get("error")
                )
            if row.get("clipJobId") and row.get("clipStatus"):
                state.clip_jobs[row["sceneId"]] = JobState(
                    row["clipStatus"], row.get("clipArtImageId"), row.get("clipError")
                )
        # status.get syncs DONE ids into the doc; re-read so assembly sees them.
        doc = client.get_video(video_id)["doc"]
        state.doc = doc
    return state


def describe_state(state: RunState) -> str:
    scenes = state.doc.get("scenes") or []
    done = sum(1 for s in scenes if _scene_image_id(s, state.scene_jobs))
    failed = [sid for sid, job in state.scene_jobs.items() if job.status in FAILED_JOB_STATUSES]
    song = state.song_job.status if state.song_job else ("ready" if (state.doc.get("song") or {}).get("artImageId") else "none")
    line = f"song: {song}; scenes: {done}/{len(scenes)} with images"
    if failed:
        line += f"; failed: {', '.join(sorted(failed))}"
    return line


def run_actions(client: KrClient, video_id: int, actions: list[str]) -> None:
    for action in actions:
        if action == "lyrics":
            client.write_lyrics(video_id)
        elif action == "song":
            client.enqueue_song(video_id)
        elif action == "song_retry":
            client.enqueue_song(video_id, force=True)
        elif action == "plan_scenes":
            client.plan_scenes(video_id)
        elif action == "scene_prompts":
            result = client.write_scene_prompts(video_id)
            rejected = result.get("rejected") or []
            if rejected:
                print(f"  {len(rejected)} scene prompts rejected by the checker; they are retried next pass")
        elif action == "render_scenes":
            result = client.render_scenes(video_id)
            print(f"  {result.get('outcomes') and len(result['outcomes'])} scenes sent to the render queue")
        elif action in ("wait", "assemble"):
            return
        print(f"  done: {action}")


def assemble(client: KrClient, state: RunState, out: Path, workdir: Path, fps: int) -> Path:
    if not shutil.which("ffmpeg"):
        raise PipelineError("ffmpeg is not installed")
    doc = state.doc
    song_id = (doc.get("song") or {}).get("artImageId") or (state.song_job and state.song_job.art_image_id)
    if not song_id:
        raise PipelineError("the song has no audio ArtImage yet")
    song_path = client.download_art(int(song_id), workdir / f"song-{song_id}.mp3")
    assets: dict[str, Path] = {}
    for scene in doc.get("scenes") or []:
        image_id = _scene_image_id(scene, state.scene_jobs)
        if not image_id:
            raise PipelineError(f"scene {scene['id']} has no image yet")
        assets[scene["id"]] = client.download_art(image_id, workdir / f"{scene['id']}-{image_id}.img")
        clip_job = state.clip_jobs.get(scene["id"])
        clip_id = (scene.get("motion") or {}).get("clipArtImageId") or (
            clip_job.art_image_id if clip_job and clip_job.status == "DONE" else None
        )
        if clip_id:
            assets[f"{scene['id']}:clip"] = client.download_art(int(clip_id), workdir / f"{scene['id']}-{clip_id}.clip")
    timeline = timeline_from_doc(doc, assets)
    width, height = FRAME_SIZES.get((doc.get("settings") or {}).get("aspect", "16:9"), FRAME_SIZES["16:9"])
    total = float((doc.get("settings") or {}).get("durationSec") or timeline[-1].end)
    command = build_ffmpeg_command(timeline, song_path, out, width, height, fps, total)
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise PipelineError(f"ffmpeg failed: {result.stderr.strip()[-2000:]}")
    return out


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def settings_from_args(args: argparse.Namespace) -> dict:
    settings: dict[str, Any] = {"durationSec": args.duration, "aspect": args.aspect}
    for key, value in (
        ("bpm", args.bpm),
        ("genre", args.genre),
        ("mood", args.mood),
        ("vocal", args.vocal),
        ("styleBible", args.style_bible),
    ):
        if value not in (None, ""):
            settings[key] = value
    return settings


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--video-id", type=int, help="resume an existing MusicVideo")
    parser.add_argument("--title", default="Untitled music video")
    parser.add_argument("--pitch", help="the video idea (required to create a new run)")
    parser.add_argument("--duration", type=float, default=60.0, help="song length in seconds")
    parser.add_argument("--bpm", type=float)
    parser.add_argument("--genre")
    parser.add_argument("--mood")
    parser.add_argument("--vocal", choices=["female", "male", "duet", "instrumental"])
    parser.add_argument("--style-bible", help="look shared by every frame")
    parser.add_argument("--aspect", choices=sorted(FRAME_SIZES), default="16:9")
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS)
    parser.add_argument("--out", type=Path, help="MP4 path (default music-video-<id>.mp4)")
    parser.add_argument("--wait", action="store_true", help="poll until renders finish, then assemble")
    parser.add_argument("--poll-seconds", type=int, default=60)
    parser.add_argument("--max-wait-minutes", type=int, default=360)
    parser.add_argument("--dry-run", action="store_true", help="print the plan; enqueue nothing")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.video_id is None and not args.pitch:
        print("Pass --pitch to start a run, or --video-id to resume one.", file=sys.stderr)
        return EXIT_CONFIG

    if args.dry_run and args.video_id is None:
        print("DRY RUN: would create a MusicVideo with:")
        print(json.dumps({"title": args.title, "pitch": args.pitch, "settings": settings_from_args(args)}, indent=2))
        print("then: lyrics -> song -> plan_scenes -> scene_prompts -> render_scenes -> wait -> assemble")
        return EXIT_DONE

    if not KR_API_TOKEN:
        print("KR_API_TOKEN is not set (an admin token is required).", file=sys.stderr)
        return EXIT_CONFIG
    client = KrClient(KR_BASE_URL, KR_API_TOKEN)

    try:
        video_id = args.video_id
        if video_id is None:
            video = client.create_video(args.title, args.pitch, settings_from_args(args))
            video_id = int(video["id"])
            print(f"created MusicVideo {video_id}; resume with --video-id {video_id}")

        deadline = time.time() + args.max_wait_minutes * 60
        previous: list[str] = []
        repeats = 0
        while True:
            state = read_state(client, video_id)
            actions = plan_actions(state)
            print(f"MusicVideo {video_id}: {describe_state(state)}; next: {', '.join(actions)}")
            if args.dry_run:
                return EXIT_DONE
            if actions == ["assemble"]:
                break
            run_actions(client, video_id, actions)
            if "wait" not in actions:
                # Progress without renders in flight: re-read and continue,
                # unless the same steps keep coming back (an endpoint that
                # succeeds without changing the doc would otherwise spin).
                repeats = repeats + 1 if actions == previous else 0
                previous = actions
                if repeats >= 2:
                    raise PipelineError(f"no progress after repeating: {', '.join(actions)}")
                continue
            previous, repeats = [], 0
            if not args.wait:
                print("renders still in flight; re-run with the same --video-id (or --wait)")
                return EXIT_IN_PROGRESS
            if time.time() > deadline:
                print(f"gave up waiting after {args.max_wait_minutes} minutes", file=sys.stderr)
                return EXIT_IN_PROGRESS
            time.sleep(args.poll_seconds)

        out = args.out or Path(f"music-video-{video_id}.mp4")
        with tempfile.TemporaryDirectory(prefix=f"music-video-{video_id}-") as workdir:
            assemble(client, state, out, Path(workdir), args.fps)
        print(f"wrote {out}")
        return EXIT_DONE
    except PipelineError as error:
        print(f"error: {error}", file=sys.stderr)
        return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
