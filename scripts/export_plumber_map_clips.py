#!/usr/bin/env python3
"""Ship Save the Plumber's map motion loops into kind_robots as MP4s.

save-the-plumber t-024/t-025. Silas (2026-10-22): the world map should be animated, not a still.
projects/save-the-plumber/art/GEN2-MAP-CLIPS-1.yaml renders each world's painted map plate as a WAN 2.2
first/last-frame loop. WAN delivers an animated WebP, and a canvas draws only the first frame of an animated
image, so each finished loop is re-encoded twice, as VP9 WebM (Chrome, Firefox, open-source Chromium) and
H.264 MP4 (Safari), at ``<kind_robots>/public/save-the-plumber/maps/world-<n>.{webm,mp4}``; the game draws
whichever the browser can play through a detached video element, and
``utils/arcade/games/savePlumberMapClips.ts`` is rewritten from what is on disk so the game plays exactly the
loops it ships.

Usage:
    python scripts/export_plumber_map_clips.py --kind-robots ../kind_robots            # export new loops
    python scripts/export_plumber_map_clips.py --kind-robots ../kind_robots --manifest-only

Environment: KR_API_TOKEN, KR_BASE_URL. Needs ffmpeg with libx264 and libvpx-vp9 on PATH.
"""

from __future__ import annotations

import argparse
import io
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

import yaml

LEDGER = Path(__file__).resolve().parent.parent / "projects/save-the-plumber/art/GEN2-MAP-CLIPS-1.yaml"
MAPS_DIR = Path("public") / "save-the-plumber" / "maps"
MANIFEST = Path("utils") / "arcade" / "games" / "savePlumberMapClips.ts"
MANIFEST_HEADER = """// Written by conductor scripts/export_plumber_map_clips.py from the map
// motion ledger (projects/save-the-plumber/art/GEN2-MAP-CLIPS-1.yaml): the
// worlds whose painted map plate has a shipped motion loop at
// /save-the-plumber/maps/world-<n>.webm and .mp4. Do not edit by hand.
"""
KEY = re.compile(r"^gen2-mapclip-(\d+)-")


def finished(subjects):
    """(world, art_image_id) for every DONE loop that is not withdrawn."""
    for subject in subjects:
        match = KEY.match(subject.get("key", ""))
        if not match or (subject.get("withdrawn") or {}).get("wan-clips"):
            continue
        art = (subject.get("art") or {}).get("wan-clips") or {}
        if art.get("status") == "DONE" and art.get("art_image_id"):
            yield int(match.group(1)), art["art_image_id"]


def render_manifest(worlds):
    listed = ", ".join(str(w) for w in sorted(worlds))
    return MANIFEST_HEADER + f"\nexport const MAP_CLIP_WORLDS: readonly number[] = [{listed}]\n"


def shipped(kind_robots):
    root = Path(kind_robots) / MAPS_DIR
    worlds = {int(m.group(1)) for p in root.glob("world-*.mp4") if (m := re.match(r"world-(\d+)\.mp4$", p.name))}
    return sorted(w for w in worlds if (root / f"world-{w}.webm").exists())


def fetch_animation(art_image_id):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import consume_art_queue_core as core

    status, resp = core.http_json("GET", f"{core.KR_BASE_URL}/api/art/image/{art_image_id}")
    image_path = ((resp or {}).get("data") or {}).get("imagePath") if status == 200 else None
    if not image_path:
        raise RuntimeError(f"ArtImage {art_image_id}: HTTP {status}, no imagePath")
    request = urllib.request.Request(f"{core.KR_BASE_URL}{image_path}")
    request.add_header("Authorization", f"Bearer {core.KR_API_TOKEN}")
    with urllib.request.urlopen(request, timeout=300) as resp:
        return resp.read()


def _delta(a, b):
    """Mean per-channel difference of two same-size RGB frames, on a small thumbnail."""
    from PIL import ImageChops, ImageStat

    small = (160, 90)
    diff = ImageChops.difference(a.resize(small), b.resize(small))
    return sum(ImageStat.Stat(diff).mean) / 3


def loop_frames(frames, fade=8, settle_max=6, settle_delta=6.0):
    """Frames that loop without a pop.

    WAN spends its first few frames settling from the sharp source plate into its own render (world 1's
    first loop jumped 16.6 then 9.7 between its opening frames, then ran at 2-5), so those leading frames are
    dropped until one frame-to-frame step falls under ``settle_delta``. The last ``fade`` frames are then
    crossfaded into the first ``fade`` ones, which are dropped from the head, so the final frame flows into
    the first exactly as two neighbouring frames do.
    """
    from PIL import Image

    start = 0
    while start < min(settle_max, len(frames) - 1) and _delta(frames[start], frames[start + 1]) > settle_delta:
        start += 1
    frames = list(frames[start:])
    if len(frames) <= 2 * fade:
        return frames
    head, body = frames[:fade], frames[fade:]
    for j in range(fade):
        alpha = (j + 1) / (fade + 1)
        body[len(body) - fade + j] = Image.blend(body[len(body) - fade + j], head[j], alpha)
    return body


def encode_mp4(webp_bytes, out_path, fps=16):
    """Every frame of an animated WebP into a seamlessly looping H.264 MP4 (and a VP9 WebM)."""
    from PIL import Image

    image = Image.open(io.BytesIO(webp_bytes))
    width, height = (d - d % 2 for d in image.size)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    decoded = []
    for index in range(getattr(image, "n_frames", 1)):
        image.seek(index)
        frame = image.convert("RGB")
        decoded.append(frame.crop((0, 0, width, height)) if frame.size != (width, height) else frame)
    looped = loop_frames(decoded)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{width}x{height}", "-r", str(fps), "-i", "-",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "22", "-preset", "slow",
        "-movflags", "+faststart", "-an", str(out_path),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for frame in looped:
        proc.stdin.write(frame.tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"ffmpeg failed for {out_path}")
    webm = out_path.with_suffix(".webm")
    vp9 = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(out_path), "-c:v", "libvpx-vp9", "-b:v", "0",
           "-crf", "30", "-row-mt", "1", "-an", str(webm)]
    if subprocess.run(vp9).returncode != 0:
        raise RuntimeError(f"ffmpeg failed for {webm}")
    return len(looped)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ledger", default=str(LEDGER))
    parser.add_argument("--kind-robots", default="../kind_robots")
    parser.add_argument("--manifest-only", action="store_true")
    parser.add_argument("--force", action="store_true", help="re-encode loops already on disk")
    args = parser.parse_args(argv)
    if not args.manifest_only:
        subjects = yaml.safe_load(Path(args.ledger).read_text())["subjects"]
        for world, image_id in finished(subjects):
            out = Path(args.kind_robots) / MAPS_DIR / f"world-{world}.mp4"
            if out.exists() and out.with_suffix(".webm").exists() and not args.force:
                continue
            frames = encode_mp4(fetch_animation(image_id), out)
            print(f"world {world}: {frames} frames -> {out} ({out.stat().st_size} bytes)")
    worlds = shipped(args.kind_robots)
    manifest = Path(args.kind_robots) / MANIFEST
    manifest.write_text(render_manifest(worlds))
    print(f"map loops shipped for worlds: {worlds or 'none yet'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
