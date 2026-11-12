#!/usr/bin/env python3
"""Build one private Dead Air commercial through Kind Robots' existing MusicVideo/ArtJob API.

Dry-run is the default. --daily resumes the earliest unfinished episode from the
dated archive, without starting another film while earlier renders remain pending.
It never publishes or changes isPublic. No credentials are printed.
"""
from __future__ import annotations

import argparse
import hashlib
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from zoneinfo import ZoneInfo

import yaml

from build_music_video import (
    KrClient, PipelineError, assemble, plan_actions, read_state,
    run_actions, clips_to_request, EXIT_DONE, EXIT_ERROR, EXIT_IN_PROGRESS, EXIT_CONFIG,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATE = ROOT / "projects/dead-air/production-state.json"
EPISODES = ROOT / "projects/dead-air/episodes"
BASE = "https://kind-robots.vercel.app"
DURATION = 15.0


def validate(e: dict) -> list[str]:
    problems: list[str] = []
    if not isinstance(e, dict) or e.get("version") != 1:
        return ["expected an episode mapping with version: 1"]
    for field in ("title", "slug", "date", "product", "universe", "world_law",
                  "visual_style", "voiceover", "reveal", "format"):
        if not isinstance(e.get(field), str) or not e[field].strip():
            problems.append(f"missing {field}")
    if e.get("duration_seconds") != 15 or e.get("aspect") != "16:9":
        problems.append("only a 15-second 16:9 commercial is allowed")
    refs = e.get("references")
    if not isinstance(refs, list) or len(refs) < 3:
        problems.append("at least three documented pop-culture references are required")
    else:
        for ref in refs:
            if not isinstance(ref, dict) or not all(ref.get(k) for k in ("work", "study", "transformation", "assets")):
                problems.append("every reference needs work, study, transformation and assets")
    shots = e.get("shots")
    if not isinstance(shots, list) or not 4 <= len(shots) <= 6:
        return problems + ["expected 4–6 shots"]
    clips, cursor, ids = 0, 0.0, set()
    for index, shot in enumerate(shots, 1):
        if not isinstance(shot, dict):
            problems.append(f"shot {index} must be a mapping")
            continue
        sid = shot.get("id")
        if not isinstance(sid, str) or not sid.isidentifier() or sid in ids:
            problems.append(f"shot {index} has missing, unsafe or duplicate id")
        ids.add(sid)
        for field in ("image_prompt", "motion_prompt", "camera", "overlay"):
            if not isinstance(shot.get(field), str) or not shot[field].strip():
                problems.append(f"shot {index} missing {field}")
        try:
            start, end = float(shot["start"]), float(shot["end"])
            if abs(start - cursor) > .01 or end <= start or end > 15.001:
                problems.append(f"shot {index} has an invalid boundary")
            cursor = end
        except (ValueError, TypeError, KeyError):
            problems.append(f"shot {index} missing numeric timing")
        if shot.get("motion") == "clip":
            clips += 1
        elif shot.get("motion") != "kenburns":
            problems.append(f"shot {index} invalid motion type")
    if abs(cursor - 15) > .01:
        problems.append("film must end at 15.0s")
    if clips < 2:
        problems.append("at least two shots must have real clip animation")
    return problems


def load_episode(path: Path) -> dict:
    e = yaml.safe_load(path.read_text(encoding="utf-8"))
    errors = validate(e)
    if errors:
        raise ValueError("; ".join(errors))
    return e


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"version": 1, "episodes": {}}
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("version") != 1 or not isinstance(value.get("episodes"), dict):
        raise ValueError(f"invalid state ledger: {path}")
    return value


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temp.replace(path)


def choose_episode(state: dict, today: str) -> Path | None:
    """Strict backlog-first: do not start a new episode while an old one is unfinished."""
    for path in sorted(EPISODES.glob("*.yaml")):
        episode = load_episode(path)
        if episode["date"] > today:
            continue
        if state["episodes"].get(episode["slug"], {}).get("status") != "completed":
            return path
    return None


def scenes_for(e: dict) -> list[dict]:
    output = []
    for i, shot in enumerate(e["shots"]):
        output.append({
            "id": shot["id"],
            "startSec": shot["start"], "endSec": shot["end"],
            "prompt": f'{shot["image_prompt"]} Shared visual continuity: {e["visual_style"]}',
            "promptSource": "user", "motionPrompt": shot["motion_prompt"],
            "lyricRefs": [],
            "image": {"source": "generated"},
            "motion": {"kind": "clip" if shot["motion"] == "clip" else "kenburns",
                       "preset": ("zoom-in", "pan-left", "zoom-out", "pan-right")[i % 4]},
            "transition": "cut", "transitionSec": 0,
        })
    return output


def make_audio(episode: dict, workdir: Path) -> Path:
    """Provisional original spoken VO + very quiet station-tone bed, exactly 15 seconds.

    This intentionally never reuses copyrighted music or dialogue. A later creative
    audio pass can replace the provisional narration before approval for publication.
    """
    voice_engine = shutil.which("espeak-ng") or shutil.which("espeak")
    if not voice_engine or not shutil.which("ffmpeg"):
        raise PipelineError("audio requires ffmpeg and espeak-ng or espeak")
    voice = workdir / "voice.wav"
    with voice.open("wb") as output:
        proc = subprocess.run([voice_engine, "-s", "165", "--stdout", episode["voiceover"]],
                              stdout=output, stderr=subprocess.PIPE, check=False)
    if proc.returncode:
        raise PipelineError("provisional voice synthesis failed")
    song = workdir / "dead-air-15sec.mp3"
    command = [
        "ffmpeg", "-nostdin", "-y", "-loglevel", "error",
        "-i", str(voice), "-f", "lavfi", "-i", "sine=frequency=220:sample_rate=44100:duration=15",
        "-filter_complex",
        "[0:a]adelay=350|350,volume=1.2,apad,atrim=duration=15[vo];"
        "[1:a]volume=0.018[bed];[vo][bed]amix=inputs=2:duration=first:normalize=0,"
        "alimiter=limit=0.93,atrim=duration=15[mix]",
        "-map", "[mix]", "-t", "15", "-ar", "44100", "-c:a", "libmp3lame", "-q:a", "4", str(song),
    ]
    proc = subprocess.run(command, capture_output=True, text=True, check=False)
    if proc.returncode:
        raise PipelineError(f"sound mix failed: {proc.stderr[-350:]}")
    return song


def caption_export(raw: Path, output: Path, episode: dict, workspace: Path) -> dict:
    """Bake timecoded broadcast captions over rendered footage and probe the final."""
    font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    if not Path(font).exists():
        raise PipelineError("caption font unavailable on the exporter")
    filters = []
    for shot in episode["shots"]:
        idx = len(filters)
        caption = workspace / f"caption-{idx}.txt"
        caption.write_text(shot["overlay"], encoding="utf-8")
        start, end = float(shot["start"]), float(shot["end"])
        show = f"between(t\\,{start:.3f}\\,{end - .001:.3f})"
        filters.append(
            "drawbox=x=0:y=ih-116:w=iw:h=116:color=black@0.80:t=fill:enable='" + show + "',"
            f"drawtext=fontfile={font}:textfile={caption}:fontcolor=white:fontsize=37:"
            f"x=(w-text_w)/2:y=h-79:enable='{show}'"
        )
    command = [
        "ffmpeg", "-nostdin", "-y", "-loglevel", "error",
        "-i", str(raw), "-vf", ",".join(filters), "-t", "15",
        "-c:v", "libx264", "-preset", "fast", "-crf", "24", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(output),
    ]
    proc = subprocess.run(command, capture_output=True, text=True, check=False)
    if proc.returncode:
        raise PipelineError(f"captioned encode failed: {proc.stderr[-500:]}")
    probe = subprocess.run([
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_entries", "format=duration:stream=codec_name,width,height,codec_type",
        str(output),
    ], capture_output=True, text=True, check=False)
    if probe.returncode:
        raise PipelineError("ffprobe could not inspect final MP4")
    meta = json.loads(probe.stdout)
    duration = float(meta["format"]["duration"])
    video = next((s for s in meta["streams"] if s.get("codec_type") == "video"), {})
    audio = next((s for s in meta["streams"] if s.get("codec_type") == "audio"), {})
    if not (14.8 <= duration <= 15.2 and video.get("codec_name") == "h264"
            and video.get("width") == 1280 and video.get("height") == 720
            and audio.get("codec_name") == "aac"):
        raise PipelineError(f"final media failed probe: {duration}s {video} audio={audio}")
    return {"duration_seconds": duration, "width": 1280, "height": 720,
            "video_codec": "h264", "audio_codec": "aac"}


def record(state: dict, path: Path, e: dict, **fields: object) -> None:
    row = state["episodes"].setdefault(e["slug"], {"episode": str(path.relative_to(ROOT))})
    row.update(fields)
    row["updated_pt"] = datetime.now(ZoneInfo("America/Los_Angeles")).isoformat()


def run_episode(e: dict, episode_path: Path, state: dict, state_file: Path, video_id: int | None) -> int:
    token = os.environ.get("KR_API_TOKEN")
    if not token:
        print("KR_API_TOKEN absent: private render not attempted", file=sys.stderr)
        return EXIT_CONFIG
    client = KrClient(os.environ.get("KR_BASE_URL", BASE), token)
    row = state["episodes"].get(e["slug"], {})
    existing = row.get("music_video_id")
    if existing and video_id and int(existing) != video_id:
        raise PipelineError("video-id differs from the durable episode ledger")
    if existing:
        video_id = int(existing)
    if not video_id:
        created = client.create_video(f"Dead Air: {e['title']}", e["product"], {
            "durationSec": 15, "aspect": "16:9", "vocal": "instrumental",
            "styleBible": e["visual_style"], "heroShots": 2,
        })
        video_id = int(created["id"])
        record(state, episode_path, e, music_video_id=video_id, status="created")
        save_state(state_file, state)  # Must persist ID before any extra API call.
    doc = client.get_video(video_id)["doc"]
    if not doc.get("scenes"):
        doc["scenes"] = scenes_for(e)
        doc["settings"]["vocal"] = "instrumental"
        client._request("PATCH", f"/api/music-video/{video_id}", {"doc": doc})
    if not (client.get_video(video_id)["doc"].get("song") or {}).get("artImageId"):
        with tempfile.TemporaryDirectory(prefix="dead-air-audio-") as tmp:
            track = make_audio(e, Path(tmp))
            client.upload_song(video_id, track, 15.0, 110)
    state_now = read_state(client, video_id)
    actions = plan_actions(state_now)
    if "render_scenes" in actions:
        run_actions(client, video_id, ["render_scenes"])
        state_now = read_state(client, video_id)
    clip_ids = [s["id"] for s in e["shots"] if s["motion"] == "clip"]
    for start in range(0, len(clip_ids), 8):
        request = clips_to_request(state_now, clip_ids[start:start + 8])
        if request:
            client.request_clips(video_id, request)
    state_now = read_state(client, video_id)
    failures = [sid for sid, job in state_now.clip_jobs.items() if job.status in ("FAILED", "CANCELLED")]
    if failures:
        record(state, episode_path, e, music_video_id=video_id, status="blocked", reason="failed motion clip: " + ",".join(failures))
        save_state(state_file, state)
        raise PipelineError("animation ArtJobs failed: " + ", ".join(failures))
    ready_clips = [
        sid for sid in clip_ids
        if (state_now.clip_jobs.get(sid) and state_now.clip_jobs[sid].status == "DONE"
            and state_now.clip_jobs[sid].art_image_id)
        or any(s["id"] == sid and (s.get("motion") or {}).get("clipArtImageId")
               for s in state_now.doc.get("scenes", []))
    ]
    jobs = {
        "song": (state_now.doc.get("song") or {}).get("jobId"),
        "stills": {s["id"]: (s.get("image") or {}).get("jobId") for s in state_now.doc.get("scenes", [])},
        "clips": {s["id"]: (s.get("motion") or {}).get("jobId") for s in state_now.doc.get("scenes", [])},
    }
    record(state, episode_path, e, music_video_id=video_id, art_jobs=jobs,
           status="rendering", motion_clips_ready=len(ready_clips))
    save_state(state_file, state)
    if len(ready_clips) < 2 or plan_actions(state_now) != ["assemble"]:
        print(f"Rendering private MusicVideo {video_id}: {len(ready_clips)}/{len(clip_ids)} real motion clips ready")
        return EXIT_IN_PROGRESS
    # A shot list is not distinct artwork if all scene IDs resolve to the same still.
    scene_ids = []
    for shot in e["shots"]:
        match = next((s for s in state_now.doc.get("scenes", []) if s["id"] == shot["id"]), {})
        image_id = (match.get("image") or {}).get("artImageId")
        if not image_id and shot["id"] in state_now.scene_jobs:
            image_id = state_now.scene_jobs[shot["id"]].art_image_id
        if not image_id:
            raise PipelineError(f"shot {shot['id']} has no delivered still ArtImage")
        scene_ids.append(image_id)
    if len(set(scene_ids)) != len(scene_ids):
        raise PipelineError("multiple shots resolved to the same still ArtImage")
    with tempfile.TemporaryDirectory(prefix=f"dead-air-{video_id}-") as tmp:
        workspace = Path(tmp)
        raw, final = workspace / "raw.mp4", workspace / "captioned.mp4"
        assemble(client, state_now, raw, workspace, 30)
        probe = caption_export(raw, final, e, workspace)
        film_hash = hashlib.sha256(final.read_bytes()).hexdigest()
        film_bytes = final.stat().st_size
        result = client.upload_final(video_id, final)
    image_id = result.get("artImageId")
    if not image_id:
        raise PipelineError("final upload returned no ArtImage ID")
    record(state, episode_path, e, status="completed", final_art_image_id=image_id,
           quality_probe=probe, sha256=film_hash, bytes=film_bytes,
           completed_pt=datetime.now(ZoneInfo("America/Los_Angeles")).date().isoformat())
    save_state(state_file, state)
    print(f"Completed private film {video_id}: final ArtImage {image_id}; {probe['duration_seconds']} seconds")
    return EXIT_DONE


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--episode", type=Path)
    p.add_argument("--daily", action="store_true", help="resume oldest unfinished dated film")
    p.add_argument("--state-file", type=Path, default=DEFAULT_STATE)
    p.add_argument("--video-id", type=int, help="recover existing MusicVideo ID")
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--start", action="store_true", help="create/recover a private film")
    mode.add_argument("--resume", action="store_true", help="reuse an existing MusicVideo ID")
    mode.add_argument("--dry-run", action="store_true", help="inspect without any API writes")
    args = p.parse_args(argv)
    try:
        state = load_state(args.state_file)
        episode_path = args.episode
        if args.daily:
            if episode_path:
                raise ValueError("--daily chooses the episode; omit --episode")
            today = datetime.now(ZoneInfo("America/Los_Angeles")).date().isoformat()
            episode_path = choose_episode(state, today)
            if episode_path is None:
                print("No pending dated episode. Not generating a duplicate or claiming a new film.")
                return EXIT_IN_PROGRESS
        if episode_path is None:
            raise ValueError("--episode or --daily is required")
        episode = load_episode(episode_path)
        if args.resume and not (args.video_id or state["episodes"].get(episode["slug"], {}).get("music_video_id")):
            raise ValueError("resume requires a recorded MusicVideo ID")
        if args.dry_run or not (args.start or args.resume or args.daily):
            print(json.dumps({"episode": str(episode_path), "title": episode["title"],
                "shots": len(episode["shots"]), "animated_shots": [
                    s["id"] for s in episode["shots"] if s["motion"] == "clip"
                ], "references": len(episode["references"]), "seconds": 15.0,
                "writes": False, "private": True}, indent=2))
            return EXIT_DONE
        return run_episode(episode, episode_path, state, args.state_file, args.video_id)
    except (ValueError, KeyError, PipelineError, OSError) as error:
        print(f"Dead Air: {error}", file=sys.stderr)
        return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
