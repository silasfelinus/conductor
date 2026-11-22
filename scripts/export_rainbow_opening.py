#!/usr/bin/env python3
"""Cut Rainbow Space Princess's opening music video and ship it into kind_robots.

rainbow-bullet-hell-space-princess t-034. Silas (2026-10-23 PT): "We can use a real animation at the
beginning, maybe a 15 second high energy thrash metal music video."

The picture is eight C.A.T.S. doodle shots cut to the beat of the ACE-Step thrash track (kind_robots
``utils/arcade/games/rainbowOpening.ts`` RAINBOW_OPENING_TRACK, job designer ``rainbow-score:v1:opening``):

* each shot plays its WAN MP4 from ``art/OPENING-CLIPS-2-DOODLE.yaml`` once that clip is DONE (sped up, ping-ponged
  to fill the shot), or until then the approved still it is pinned to, with a punch-in and beat shake;
* every downbeat pulses the zoom, every cut opens on a white flash, and the last beats slam the title on.

It writes ``public/rainbow-princess-video/opening.{mp4,webm}`` and ``opening-poster.webp`` and rewrites the
RAINBOW_OPENING line of ``rainbowOpening.ts`` with what it shipped, so the Fly tab offers exactly that file.
Re-run it when more clips render: it always cuts from the ledger's current state.

Usage:
    python scripts/export_rainbow_opening.py --kind-robots ../kind_robots
    python scripts/export_rainbow_opening.py --kind-robots ../kind_robots --stills-only   # ignore clips
    python scripts/export_rainbow_opening.py --kind-robots ../kind_robots --track song.mp3

Environment: KR_API_TOKEN (never printed), KR_BASE_URL. Needs ffmpeg (libx264, libvpx-vp9, libopus) and Pillow.
Exit codes: 0 shipped, 3 the track has not rendered yet, 1 error.
"""

from __future__ import annotations

import argparse
import io
import json
import math
import re
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "projects/rainbow-bullet-hell-space-princess/art/OPENING-CLIPS-2-DOODLE.yaml"
VIDEO_DIR = Path("public") / "rainbow-princess-video"
MANIFEST = Path("utils") / "arcade" / "games" / "rainbowOpening.ts"
TRACK_KEY = "rainbow-score:v1:opening"

BPM = 176
FPS = 24
SIZE = (1280, 720)
CLIP_FPS = 16
CLIP_SPEED = 1.5
MAX_CLIP_FRAMES = 128
MAX_CLIP_SECONDS = 8
# (ledger key, beats). The title slams on over the last TITLE_BEATS beats of the final shot.
SHOTS = [
    ("opening-01-palace-storm", 8),
    ("opening-02-lilt-alarm", 4),
    ("opening-03-eclipse-orb", 6),
    ("opening-04-maribel", 2),
    ("opening-05-azure", 2),
    ("opening-06-solenne", 2),
    ("opening-07-vivi", 2),
    ("opening-08-dolphin-fleet", 6),
    ("opening-09-ships-launch", 12),
]
DOODLE_SHOTS = [
    ("intro-cats-launch", 8),
    ("intro-lilt-signal", 4),
    ("intro-dolphin-armada", 6),
    ("intro-maribel-bloom", 3),
    ("intro-azure-prism", 3),
    ("intro-solenne-halo", 3),
    ("intro-vivi-comet", 3),
    ("intro-cats-formation", 14),
]
DOODLE_ROUND = "rainbow-doodle-opening-recut-2"
TITLE_BEATS = 6
EXIT_DONE, EXIT_ERROR, EXIT_RENDERING = 0, 1, 3
FONTS = [
    "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf",
    "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
RAINBOW = [(255, 159, 216), (255, 211, 138), (255, 242, 168), (166, 255, 240), (158, 231, 255), (201, 169, 255)]


def _core():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import consume_art_queue_core as core

    return core


def download(art_image_id: int) -> bytes:
    core = _core()
    request = urllib.request.Request(f"{core.KR_BASE_URL}/api/art/images/{art_image_id}/file")
    request.add_header("Authorization", f"Bearer {core.KR_API_TOKEN}")
    with urllib.request.urlopen(request, timeout=300) as resp:
        return resp.read()


def track_image_id() -> tuple[str, int | None]:
    """The opening track job's status and its ArtImage once DONE."""
    core = _core()
    status, resp = core.http_json("GET", f"{core.KR_BASE_URL}/api/art/queue?projectSlug=kr-arcade&pageSize=200")
    if status != 200:
        raise RuntimeError(f"GET /api/art/queue: HTTP {status}")
    data = (resp or {}).get("data")
    jobs = data if isinstance(data, list) else (data or {}).get("jobs") or (data or {}).get("items") or []
    mine = [job for job in jobs if TRACK_KEY in json.dumps(job.get("payload", "")).replace('\\"', '"')]
    if not mine:
        return "MISSING", None
    done = [job for job in mine if job.get("status") == "DONE" and job.get("artImageId")]
    if done:
        latest = max(done, key=lambda job: job["id"])
        return "DONE", int(latest["artImageId"])
    return max(mine, key=lambda job: job["id"]).get("status", "?"), None



def wan_shot_budgets(ledger: dict) -> list[dict]:
    """Per WAN shot: requested seconds, fps, frames and headroom vs the clip budget.

    Raises ValueError for malformed lanes/durations; does not enforce the limit,
    so reviewers can see over-budget values. Returns [] for non-doodle ledgers.
    """
    if ledger.get("round") != DOODLE_ROUND:
        return []
    lanes = {lane.get("key"): lane for lane in ledger.get("lanes", [])}
    lane = lanes.get("wan-mp4")
    if not lane:
        raise ValueError("opening WAN queue is missing its wan-mp4 lane")
    fps = lane.get("fps")
    if type(fps) is not int or fps <= 0:
        raise ValueError(f"opening WAN lane has invalid fps: {fps!r}")
    budgets = []
    for shot in ledger.get("subjects", []):
        if shot.get("lane") != "wan-mp4":
            continue
        duration = shot.get("duration")
        if (type(duration) not in (int, float) or
                not math.isfinite(duration) or duration <= 0):
            raise ValueError(f"{shot.get('key')}: invalid WAN duration {duration!r}")
        frames = math.ceil(duration * fps)
        budgets.append({
            "key": shot.get("key"),
            "seconds": duration,
            "fps": fps,
            "frames": frames,
            "seconds_headroom": round(MAX_CLIP_SECONDS - duration, 3),
            "frame_headroom": MAX_CLIP_FRAMES - frames,
        })
    return budgets


def validate_opening_queue_budget(ledger: dict) -> None:
    """Reject WAN requests the opening exporter cannot decode before GPU enqueue.

    Queue callers may invoke this preflight without needing audio, ffmpeg, or
    downloaded art. A finished clip's actual metadata is still checked at export.
    """
    for budget in wan_shot_budgets(ledger):
        if budget["seconds"] > MAX_CLIP_SECONDS or budget["frames"] > MAX_CLIP_FRAMES:
            raise ValueError(
                f"{budget['key']}: WAN request {budget['seconds']:g}s at {budget['fps']} fps "
                f"({budget['frames']} frames) exceeds opening clip budget "
                f"({MAX_CLIP_SECONDS}s, {MAX_CLIP_FRAMES} frames); do not enqueue"
            )


def validate_shot_coverage(ledger: dict) -> None:
    """Reject incomplete or ambiguous cuts before downloading expensive media."""
    subjects = ledger.get("subjects")
    if not isinstance(subjects, list):
        raise ValueError("opening ledger must contain a subjects list")
    expected = DOODLE_SHOTS if ledger.get("round") == DOODLE_ROUND else SHOTS
    keys = [subject.get("key") for subject in subjects if isinstance(subject, dict)]
    for key, _ in expected:
        matches = [
            subject for subject in subjects
            if isinstance(subject, dict) and subject.get("key") == key
        ]
        if len(matches) != 1:
            raise ValueError(f"{key}: expected exactly one opening shot, found {len(matches)}")
        source_id = matches[0].get("source_image_id")
        if type(source_id) is not int or source_id <= 0:
            raise ValueError(f"{key}: missing valid approved source ArtImage ID")
    if len(keys) != len(set(keys)):
        raise ValueError("opening ledger contains duplicate shot keys")


def shot_sources(ledger: dict, stills_only: bool):
    """Per shot: (key, beats, source still id, delivered clip id or None)."""
    by_key = {subject["key"]: subject for subject in ledger["subjects"]}
    doodle = ledger.get("round") == DOODLE_ROUND
    lane = "wan-mp4" if doodle else "wan-clips"
    for key, beats in (DOODLE_SHOTS if doodle else SHOTS):
        subject = by_key[key]
        art = (subject.get("art") or {}).get(lane) or {}
        clip = art.get("art_image_id") if art.get("status") == "DONE" and not stills_only else None
        yield key, beats, int(subject["source_image_id"]), (int(clip) if clip else None)


def cover(image, size=SIZE):
    """Scale and centre-crop an image to fill ``size``."""
    from PIL import Image

    scale = max(size[0] / image.width, size[1] / image.height)
    resized = image.resize((math.ceil(image.width * scale), math.ceil(image.height * scale)), Image.LANCZOS)
    left = (resized.width - size[0]) // 2
    top = (resized.height - size[1]) // 2
    return resized.crop((left, top, left + size[0], top + size[1]))


def zoomed(frame, zoom: float, dx: float = 0.0, dy: float = 0.0):
    """``frame`` (already SIZE) zoomed about its centre, nudged by (dx, dy) pixels."""
    from PIL import Image

    if zoom <= 1.0 and not dx and not dy:
        return frame
    w, h = SIZE
    cw, ch = w / zoom, h / zoom
    left = (w - cw) / 2 - dx / zoom
    top = (h - ch) / 2 - dy / zoom
    left = min(max(left, 0), w - cw)
    top = min(max(top, 0), h - ch)
    return frame.resize(SIZE, Image.BICUBIC, box=(left, top, left + cw, top + ch))


def clip_frames(payload: bytes):
    """Decode ArtImage MP4/WebM and animated WebP to the same RGB frames."""
    from PIL import Image

    is_mp4 = payload[4:8] == b"ftyp"
    is_webm = payload.startswith(b"\x1a\x45\xdf\xa3")
    if is_mp4 or is_webm:
        with tempfile.TemporaryDirectory() as work:
            source = Path(work) / ("shot.mp4" if is_mp4 else "shot.webm")
            source.write_bytes(payload)
            command = [
                "ffmpeg", "-v", "error", "-nostdin", "-i", str(source),
                "-t", str(MAX_CLIP_SECONDS),
                "-vf",
                f"fps={CLIP_FPS},scale={SIZE[0]}:{SIZE[1]}:force_original_aspect_ratio=increase,"
                f"crop={SIZE[0]}:{SIZE[1]}",
                "-frames:v", str(MAX_CLIP_FRAMES),
                "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1",
            ]
            result = subprocess.run(command, capture_output=True, check=False, timeout=90)
            if result.returncode:
                raise RuntimeError(
                    f"WAN video decode failed: {result.stderr.decode(errors='replace')[-500:]}"
                )
            frame_size = SIZE[0] * SIZE[1] * 3
            if not result.stdout or len(result.stdout) % frame_size:
                raise RuntimeError("WAN video decode produced incomplete RGB frames")
            frames = [
                Image.frombytes("RGB", SIZE, result.stdout[i : i + frame_size])
                for i in range(0, len(result.stdout), frame_size)
            ]
    else:
        image = Image.open(io.BytesIO(payload))
        frames = []
        frame_count = getattr(image, "n_frames", 1)
        if frame_count > MAX_CLIP_FRAMES:
            raise ValueError(f"excessive animated image frames {frame_count}")
        for index in range(frame_count):
            image.seek(index)
            frames.append(cover(image.convert("RGB")))
    # WAN settles from the sharp plate over its first frames; skip them.
    return frames[3:] if len(frames) > 12 else frames


def validated_clip(payload: bytes, key: str, expected_size=(832, 480)) -> list | None:
    """Fail closed on corrupt or undersized WAN media, retaining the approved still."""
    from PIL import Image

    is_mp4 = len(payload) > 12 and payload[4:8] == b"ftyp"
    is_webm = payload.startswith(b"\x1a\x45\xdf\xa3")
    if not (is_mp4 or is_webm):
        print(f"{key}: unsupported WAN container; using approved still", file=sys.stderr)
        return None
    try:
        with tempfile.TemporaryDirectory() as work:
            source = Path(work) / ("clip.mp4" if is_mp4 else "clip.webm")
            source.write_bytes(payload)
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "v:0",
                 "-show_entries", "stream=width,height,nb_frames,duration:format=duration",
                 "-of", "json", str(source)],
                capture_output=True, text=True, check=True, timeout=30,
            )
            streams = json.loads(probe.stdout).get("streams") or []
            if not streams:
                raise ValueError("no video stream")
            width, height = int(streams[0]["width"]), int(streams[0]["height"])
            if width < expected_size[0] or height < expected_size[1]:
                raise ValueError(f"undersized video {width}x{height}")
            # Bound untrusted WAN media before decoding full RGB frames into memory.
            duration = streams[0].get("duration") or json.loads(probe.stdout).get("format", {}).get("duration")
            if duration is None or not (0.5 <= float(duration) <= MAX_CLIP_SECONDS):
                raise ValueError(f"invalid video duration {duration}")
            frame_count = streams[0].get("nb_frames")
            if frame_count not in (None, "N/A") and int(frame_count) > MAX_CLIP_FRAMES:
                raise ValueError(f"excessive video frames {frame_count}")
        frames = clip_frames(payload)
        if not 12 <= len(frames) <= MAX_CLIP_FRAMES or not all(isinstance(frame, Image.Image) for frame in frames):
            raise ValueError(f"insufficient decoded frames ({len(frames)})")
        return frames
    except (OSError, ValueError, KeyError, RuntimeError, OverflowError, subprocess.SubprocessError) as exc:
        print(f"{key}: invalid WAN clip ({exc}); using approved still", file=sys.stderr)
        return None


def safe_clip_download(clip_id: int, key: str):
    """An unavailable WAN artifact must not prevent the still-backed cut."""
    try:
        return validated_clip(download(clip_id), key)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"{key}: WAN download failed ({exc}); using approved still", file=sys.stderr)
        return None


def ping_pong(count: int, length: int) -> int:
    if length <= 1:
        return 0
    period = 2 * (length - 1)
    k = count % period
    return k if k < length else period - k


def title_layer():
    """The title card: two lines, rainbow-filled, thick dark outline, on a transparent layer."""
    from PIL import Image, ImageDraw, ImageFont

    font_path = next((path for path in FONTS if Path(path).exists()), None)
    layer = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    lines = [("RAINBOW BULLET HELL", 64), ("SPACE PRINCESS", 118)]
    y = SIZE[1] - 300
    for text, px in lines:
        font = ImageFont.truetype(font_path, px) if font_path else ImageFont.load_default()
        box = draw.textbbox((0, 0), text, font=font, stroke_width=10)
        x = (SIZE[0] - (box[2] - box[0])) // 2
        mask = Image.new("L", SIZE, 0)
        ImageDraw.Draw(mask).text((x, y), text, font=font, fill=255)
        draw.text((x, y), text, font=font, fill=(26, 10, 48, 255), stroke_width=10, stroke_fill=(26, 10, 48, 255))
        gradient = Image.new("RGBA", SIZE)
        gdraw = ImageDraw.Draw(gradient)
        for column in range(SIZE[0]):
            t = column / SIZE[0] * (len(RAINBOW) - 1)
            a, b = RAINBOW[int(t)], RAINBOW[min(int(t) + 1, len(RAINBOW) - 1)]
            f = t - int(t)
            gdraw.line([(column, 0), (column, SIZE[1])], fill=tuple(round(a[i] + (b[i] - a[i]) * f) for i in range(3)) + (255,))
        layer.paste(gradient, (0, 0), mask)
        y += box[3] - box[1] + 6
    return layer


def render(sources, last: list, accepted_clips: list | None = None, rejected_clips: list | None = None):
    """Yield every output frame (PIL RGB, SIZE) of the cut; ``last[0]`` keeps the last frame before the title
    slams on, for the poster (the page sets its own title over it)."""
    from PIL import Image, ImageEnhance

    beat = 60.0 / BPM
    title = title_layer()
    total_beats = sum(beats for _, beats, _, _ in sources)
    elapsed_beats = 0
    for index, (key, beats, still_id, clip_id) in enumerate(sources):
        start = round(elapsed_beats * beat * FPS)
        end = round((elapsed_beats + beats) * beat * FPS)
        frames = safe_clip_download(clip_id, key) if clip_id else None
        if frames and accepted_clips is not None:
            accepted_clips.append(key)
        elif clip_id and not frames and rejected_clips is not None:
            rejected_clips.append(key)
        still = None if frames else cover(Image.open(io.BytesIO(download(still_id))).convert("RGB"))
        last_shot = index == len(sources) - 1
        for n in range(end - start):
            t = (start + n) / FPS
            local = n / max(1, end - start - 1)
            since_beat = (t / beat) % 1.0
            pulse = 0.035 * max(0.0, 1 - since_beat * 3)
            if frames:
                base = frames[ping_pong(int(n * CLIP_FPS * CLIP_SPEED / FPS), len(frames))]
                zoom = 1.04 + pulse
            else:
                base = still
                zoom = 1.0 + 0.14 * local + pulse
            shake = 6 * max(0.0, 1 - since_beat * 4)
            frame = zoomed(base, zoom, shake * math.sin(t * 91), shake * math.cos(t * 77))
            if n < 3:
                frame = Image.blend(frame, Image.new("RGB", SIZE, (255, 255, 255)), 0.55 * (1 - n / 3))
            if last_shot:
                title_from = beats - TITLE_BEATS
                into = (n / FPS) / beat - title_from
                if into < 0:
                    last[:] = [frame]
                else:
                    slam = max(1.0, 1.6 - into * 1.2)
                    layer = title if slam == 1.0 else zoomed(title.convert("RGBA"), slam)
                    frame = frame.copy()
                    frame.paste(ImageEnhance.Brightness(frame).enhance(0.75), (0, 0))
                    frame.paste(layer, (0, 0), layer)
                    if into < 0.25:
                        frame = Image.blend(frame, Image.new("RGB", SIZE, (255, 255, 255)), 0.6 * (1 - into * 4))
            yield frame
        elapsed_beats += beats
    assert elapsed_beats == total_beats


def encode(frames, audio: Path | None, mp4: Path, seconds: float):
    mp4.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{SIZE[0]}x{SIZE[1]}", "-r", str(FPS), "-i", "-"]
    if audio:
        fade = max(0.0, seconds - 0.35)
        cmd += ["-i", str(audio), "-filter:a",
                f"silenceremove=start_periods=1:start_threshold=-45dB,atrim=0:{seconds:.3f},afade=t=out:st={fade:.3f}:d=0.35",
                "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "slow", "-movflags", "+faststart", str(mp4)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    count = 0
    for frame in frames:
        proc.stdin.write(frame.tobytes())
        count += 1
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"ffmpeg failed for {mp4}")
    webm = mp4.with_suffix(".webm")
    vp9 = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-c:v", "libvpx-vp9", "-b:v", "0", "-crf", "32",
           "-row-mt", "1"]
    vp9 += ["-c:a", "libopus", "-b:a", "160k"] if audio else ["-an"]
    if subprocess.run(vp9 + [str(webm)]).returncode != 0:
        raise RuntimeError(f"ffmpeg failed for {webm}")
    return count


def delivery_report(sources, accepted_clips, rejected_clips, budgets=None):
    """Give reviewers the exact failed WAN shots to re-queue after delivery.

    ``budgets`` (from wan_shot_budgets) adds each WAN shot's requested seconds,
    fps, frames and headroom so near-limit re-queues are visible at a glance.
    """
    accepted = set(accepted_clips)
    rejected = set(rejected_clips)
    return {
        "shots": len(sources),
        "animated_shots": len(accepted),
        "accepted_shots": [key for key, _, _, _ in sources if key in accepted],
        "rejected_shots": [key for key, _, _, _ in sources if key in rejected],
        "wan_requeue_shots": [key for key, _, _, _ in sources if key in rejected],
        "still_fallback_shots": [key for key, _, _, _ in sources if key not in accepted],
        "wan_shot_budgets": list(budgets or []),
    }



def write_delivery_report(target: Path, sources, accepted_clips, rejected_clips, budgets=None):
    """Write the single authoritative review sidecar; remove legacy duplicates."""
    report = delivery_report(sources, accepted_clips, rejected_clips, budgets)
    target.with_name("opening-delivery-report.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    target.with_name("opening-rejected-clips.json").unlink(missing_ok=True)
    return report


def write_manifest(kind_robots: Path, media: dict | None):
    path = kind_robots / MANIFEST
    text = path.read_text()
    if media:
        body = (
            "export const RAINBOW_OPENING: RainbowOpeningMedia | null = {\n"
            f"  webm: '{media['webm']}',\n  mp4: '{media['mp4']}',\n  poster: '{media['poster']}',\n"
            f"  seconds: {media['seconds']:g},\n  clips: {media['clips']},\n  shots: {media['shots']},\n}}\n"
        )
    else:
        body = "export const RAINBOW_OPENING: RainbowOpeningMedia | null = null\n"
    new, count = re.subn(r"export const RAINBOW_OPENING: RainbowOpeningMedia \| null = (?:null\n|\{.*?\n\}\n)", body, text, flags=re.S)
    if count != 1:
        raise RuntimeError(f"{path}: RAINBOW_OPENING line not found")
    path.write_text(new)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--kind-robots", default="../kind_robots")
    parser.add_argument("--ledger", default=str(LEDGER))
    parser.add_argument("--track", help="use this audio file instead of the ACE-Step job's render")
    parser.add_argument("--stills-only", action="store_true", help="cut from the stills even where clips are DONE")
    parser.add_argument("--allow-silent", action="store_true", help="preview cut with no track (never shipped)")
    parser.add_argument("--out", help="write the MP4 here instead of shipping into kind_robots (a preview)")
    parser.add_argument("--check-queue-budget", action="store_true", help="validate WAN duration/fps before submitting ArtJobs")
    args = parser.parse_args(argv)

    kind_robots = Path(args.kind_robots)
    ledger = yaml.safe_load(Path(args.ledger).read_text())
    try:
        validate_opening_queue_budget(ledger)
        validate_shot_coverage(ledger)
    except ValueError as exc:
        print(f"opening WAN queue budget: {exc}", file=sys.stderr)
        return EXIT_ERROR
    if args.check_queue_budget:
        print("opening WAN queue budget: OK")
        return EXIT_DONE
    sources = list(shot_sources(ledger, args.stills_only))
    if ledger.get("round") == DOODLE_ROUND:
        # The approved first-round review is the identity-lock authority.
        approved = yaml.safe_load(
            (LEDGER.parent / "DOODLE-SET-1-REVIEW.yaml").read_text()
        )["decisions"]
        first_round = yaml.safe_load(
            (LEDGER.parent / "DOODLE-SET-1.yaml").read_text()
        )
        keep_ids = {
            int(subject["art"][subject["lane"]]["art_image_id"])
            for subject in first_round["subjects"]
            if approved.get(subject.get("asset", "").removeprefix("rainbow-princess-art/doodle/")) == "keep"
            and (subject.get("art") or {}).get(subject["lane"], {}).get("status") == "DONE"
        }
        checked = []
        for key, beats, still_id, clip_id in sources:
            if still_id not in keep_ids:
                print(f"{key}: source ArtImage {still_id} is not an approved DOODLE-SET-1 keeper; refusing export", file=sys.stderr)
                return EXIT_ERROR
            checked.append((key, beats, still_id, clip_id))
        sources = checked
    seconds = round(sum(beats for _, beats, _, _ in sources) * 60.0 / BPM, 3)

    with tempfile.TemporaryDirectory() as work:
        audio = Path(args.track) if args.track else None
        if not audio:
            status, image_id = track_image_id()
            if image_id:
                audio = Path(work) / "track.mp3"
                audio.write_bytes(download(image_id))
                print(f"track: ArtImage {image_id}")
            elif not args.allow_silent:
                print(f"track {TRACK_KEY}: {status}; nothing shipped (re-run once it renders)")
                return EXIT_RENDERING
        if not audio and not args.out:
            print("a silent cut is a preview only: pass --out")
            return EXIT_ERROR
        target = Path(args.out) if args.out else kind_robots / VIDEO_DIR / "opening.mp4"
        kept: list = []
        accepted_clips: list[str] = []
        rejected_clips: list[str] = []
        frames = encode(render(sources, kept, accepted_clips, rejected_clips), audio, target, seconds)
        clips = len(accepted_clips)
        print(f"{target}: {frames} frames, {seconds}s, {clips}/{len(sources)} shots animated")
        poster = target.with_name("opening-poster.webp")
        kept[-1].save(poster, "WEBP", quality=88)
        if rejected_clips:
            print("WAN clips rejected (stills substituted): " + ", ".join(rejected_clips), file=sys.stderr)
        if args.out:
            return EXIT_DONE
        report = write_delivery_report(
            target, sources, accepted_clips, rejected_clips, wan_shot_budgets(ledger)
        )
        print(f"WAN re-queue shots: {', '.join(report['wan_requeue_shots']) or 'none'}")
        url = "/" + str(VIDEO_DIR.relative_to("public")).replace("\\", "/")
        write_manifest(kind_robots, {
            "webm": f"{url}/opening.webm", "mp4": f"{url}/opening.mp4", "poster": f"{url}/opening-poster.webp",
            "seconds": seconds, "clips": clips, "shots": len(sources),
        })
    return EXIT_DONE


if __name__ == "__main__":
    sys.exit(main())
