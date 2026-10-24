#!/usr/bin/env python3
"""Cut Rainbow Space Princess's opening music video and ship it into kind_robots.

rainbow-bullet-hell-space-princess t-034. Silas (2026-10-23 PT): "We can use a real animation at the
beginning, maybe a 15 second high energy thrash metal music video."

The picture is nine shots cut to the beat of the ACE-Step thrash track (kind_robots
``utils/arcade/games/rainbowOpening.ts`` RAINBOW_OPENING_TRACK, job designer ``rainbow-score:v1:opening``):

* each shot plays its WAN clip from ``art/OPENING-CLIPS-1.yaml`` once that clip is DONE (sped up, ping-ponged
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
LEDGER = ROOT / "projects/rainbow-bullet-hell-space-princess/art/OPENING-CLIPS-1.yaml"
VIDEO_DIR = Path("public") / "rainbow-princess-video"
MANIFEST = Path("utils") / "arcade" / "games" / "rainbowOpening.ts"
TRACK_KEY = "rainbow-score:v1:opening"

BPM = 176
FPS = 24
SIZE = (1280, 720)
CLIP_FPS = 16
CLIP_SPEED = 1.5
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


def shot_sources(ledger: dict, stills_only: bool):
    """Per shot: (key, beats, source still id, delivered clip id or None)."""
    by_key = {subject["key"]: subject for subject in ledger["subjects"]}
    for key, beats in SHOTS:
        subject = by_key[key]
        art = (subject.get("art") or {}).get("wan-clips") or {}
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


def clip_frames(webp: bytes):
    from PIL import Image

    image = Image.open(io.BytesIO(webp))
    frames = []
    for index in range(getattr(image, "n_frames", 1)):
        image.seek(index)
        frames.append(cover(image.convert("RGB")))
    # WAN settles from the sharp plate over its first frames; skip them.
    return frames[3:] if len(frames) > 12 else frames


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


def render(sources, last: list):
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
        frames = clip_frames(download(clip_id)) if clip_id else None
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
    args = parser.parse_args(argv)

    kind_robots = Path(args.kind_robots)
    ledger = yaml.safe_load(Path(args.ledger).read_text())
    sources = list(shot_sources(ledger, args.stills_only))
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
        frames = encode(render(sources, kept), audio, target, seconds)
        clips = sum(1 for *_, clip in sources if clip)
        print(f"{target}: {frames} frames, {seconds}s, {clips}/{len(sources)} shots animated")
        poster = target.with_name("opening-poster.webp")
        kept[-1].save(poster, "WEBP", quality=88)
        if args.out:
            return EXIT_DONE
        url = "/" + str(VIDEO_DIR.relative_to("public")).replace("\\", "/")
        write_manifest(kind_robots, {
            "webm": f"{url}/opening.webm", "mp4": f"{url}/opening.mp4", "poster": f"{url}/opening-poster.webp",
            "seconds": seconds, "clips": clips, "shots": len(sources),
        })
    return EXIT_DONE


if __name__ == "__main__":
    sys.exit(main())
