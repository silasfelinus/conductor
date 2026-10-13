"""zuzu-pinball t-019: bake the River Croc's sprite atlas for the table.

The Croc toy is drawn from generated art: the key image Silas picked (ArtImage 245776), its Kontext phase
poses (art/T019-CROC-POSES.yaml) and WAN clips between them (art/T019-CROC-CLIPS.yaml). This fetches the
picked clips and stills, cuts every frame out of its white surround, resamples each clip to the frames the
table plays, packs them into one atlas and writes what the game loads:

    python projects/zuzu-pinball/tools/croc_atlas.py KIND_ROBOTS_DIR [--cache DIR]

  KIND_ROBOTS_DIR/public/zuzu-pinball/river-croc.webp            the atlas (lossy WebP, full alpha)
  KIND_ROBOTS_DIR/utils/arcade/pinball/tables/zuzuLastBell/crocSprite.ts   its layout and the clips

The art is inked: a black outline rings the croc and his pool, so a flood fill of near-white from the
picture's border stops at the ink and leaves the teeth, eyes and spray alone. The edges where the water
runs off the picture fade out, so the card melts into the painted pond under it. Needs KR_API_TOKEN (the
art is private) and Pillow, numpy and scipy.
"""

from __future__ import annotations

import argparse
import io
import json
import math
import os
import sys
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageSequence

FRAME = 320
COLS = 12
BASE_URL = os.environ.get("KR_BASE_URL", "https://kindrobots.org").rstrip("/")

# What the table plays. Each clip comes from a WAN clip (`clip`, its ArtImage), taking `frames` frames evenly
# from `start` to `end` (fractions of the source), or from a run of approved stills (`stills`), and plays at
# `fps`. `pingpong` plays a loop forward then back; `then` appends stills (the pose a clip lands on). HOLDS is
# the still each phase shows with reduced motion. Edit this, re-run, and commit both outputs.
CLIPS: dict[str, dict] = {
    # WAN TI2V clips (T019-CROC-CLIPS round 2): he breathes with his jaws wide, lurks, stirs to rise.
    "open": {"clip": 245794, "frames": 12, "start": 0.0, "end": 0.7, "fps": 8, "loop": True, "pingpong": True},
    "lurk": {"clip": 245799, "frames": 10, "fps": 6, "loop": True, "pingpong": True},
    "rise": {"clip": 245800, "frames": 8, "start": 0.3, "end": 1.0, "fps": 16, "then": [245782]},
    # Until the first-last-frame clips (round 3) are in: limited animation, cut between the approved poses.
    "snap": {"stills": [245782, 245776], "fps": 12},
    "roll": {"stills": [245776, 245788, 245789, 245788], "fps": 10, "loop": True},
    "spit": {"stills": [245776, 245782], "fps": 10},
    "sink": {"stills": [245776, 245792], "fps": 6},
}
HOLDS: dict[str, int] = {
    "submerged": 245792,
    "rising": 245782,
    "open": 245782,
    "captured": 245776,
    "death-roll": 245776,
    "spit": 245782,
}


def fetch(image_id: int, cache: Path) -> bytes:
    path = cache / f"{image_id}.webp"
    if path.exists():
        return path.read_bytes()
    token = os.environ.get("KR_API_TOKEN", "")
    if not token:
        sys.exit("KR_API_TOKEN is required: the croc art is private.")
    headers = {"Authorization": f"Bearer {token}"}
    with urllib.request.urlopen(
        urllib.request.Request(f"{BASE_URL}/api/art/image/{image_id}", headers=headers), timeout=60
    ) as response:
        info = json.load(response)
    image_path = (info.get("data") or info)["imagePath"]
    url = image_path if image_path.startswith("http") else BASE_URL + image_path
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=120) as response:
        raw = response.read()
    cache.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return raw


def frames_of(raw: bytes) -> list[Image.Image]:
    image = Image.open(io.BytesIO(raw))
    return [frame.convert("RGB") for frame in ImageSequence.Iterator(image)]


def edge_fade(size: int) -> np.ndarray:
    """1 inside, falling to 0 at the picture's edges: most at the top, where his body and the water run off."""
    ramp = np.linspace(0, 1, size)
    fade = lambda width: np.clip(ramp / width, 0, 1)  # noqa: E731
    top = fade(0.16)
    bottom = fade(0.02)[::-1]
    sides = np.minimum(fade(0.07), fade(0.07)[::-1])
    rows = np.minimum(top, bottom)
    return np.minimum(rows[:, None], sides[None, :])


def cutout(frame: Image.Image, light: int = 226) -> Image.Image:
    """The croc and his pool without the white surround, at FRAME x FRAME."""
    from scipy import ndimage

    frame = frame.resize((FRAME * 2, FRAME * 2), Image.LANCZOS)
    rgb = np.asarray(frame).astype(np.int16)
    white = (rgb.min(axis=2) >= light) & ((rgb.max(axis=2) - rgb.min(axis=2)) < 30)
    labels, _ = ndimage.label(white)
    edge = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
    background = np.isin(labels, edge[edge > 0])
    background = ndimage.binary_dilation(background, iterations=2)
    alpha = Image.fromarray(((~background) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    alpha = np.asarray(alpha).astype(np.float32) * edge_fade(FRAME * 2)
    out = frame.convert("RGBA")
    out.putalpha(Image.fromarray(alpha.clip(0, 255).astype(np.uint8)))
    return out.resize((FRAME, FRAME), Image.LANCZOS)


def pick(frames: list[Image.Image], count: int, start: float, end: float) -> list[Image.Image]:
    last = len(frames) - 1
    if count == 1:
        return [frames[round(start * last)]]
    return [frames[round((start + (end - start) * k / (count - 1)) * last)] for k in range(count)]


def write_ts(path: Path, layout: dict) -> None:
    clips = "\n".join(
        f"    {json.dumps(name)}: {{ first: {c['first']}, count: {c['count']}, fps: {c['fps']}, loop: {str(c['loop']).lower()} }},"
        for name, c in layout["clips"].items()
    )
    holds = "\n".join(f"    {json.dumps(phase)}: {index}," for phase, index in layout["holds"].items())
    path.write_text(
        f"""// /utils/arcade/pinball/tables/zuzuLastBell/crocSprite.ts
//
// GENERATED by conductor projects/zuzu-pinball/tools/croc_atlas.py (zuzu-pinball
// t-019): the River Croc's sprite atlas, cut from the Arthemy key image Silas
// picked (ArtImage 245776), its Kontext phase poses and the WAN clips between
// them. Re-run the tool to change it; do not edit by hand.

import type {{ CrocSprite }} from '../../types'

export const RIVER_CROC_SPRITE: CrocSprite = {{
  src: '/zuzu-pinball/river-croc.webp',
  frame: {layout['frame']},
  cols: {layout['cols']},
  rows: {layout['rows']},
  clips: {{
{clips}
  }},
  holds: {{
{holds}
  }},
}}
"""
    )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("kind_robots", type=Path)
    parser.add_argument("--cache", type=Path, default=Path(".croc-atlas-cache"))
    args = parser.parse_args(argv)

    cells: list[Image.Image] = []
    layout: dict = {"frame": FRAME, "cols": COLS, "clips": {}, "holds": {}}
    stills: dict[int, int] = {}
    for name, spec in CLIPS.items():
        if "stills" in spec:
            chosen = [frames_of(fetch(image_id, args.cache))[0] for image_id in spec["stills"]]
        else:
            source = frames_of(fetch(spec["clip"], args.cache))
            chosen = pick(source, spec["frames"], spec.get("start", 0.0), spec.get("end", 1.0))
        if spec.get("pingpong"):
            # A clip that cannot pin its last frame loops forward and back, so it never jumps.
            chosen = chosen + chosen[-2:0:-1]
        chosen += [frames_of(fetch(image_id, args.cache))[0] for image_id in spec.get("then", [])]
        layout["clips"][name] = {
            "first": len(cells),
            "count": len(chosen),
            "fps": spec["fps"],
            "loop": bool(spec.get("loop", False)),
        }
        cells.extend(cutout(frame) for frame in chosen)
    for phase, image_id in HOLDS.items():
        if image_id not in stills:
            stills[image_id] = len(cells)
            cells.append(cutout(frames_of(fetch(image_id, args.cache))[0]))
        layout["holds"][phase] = stills[image_id]

    rows = math.ceil(len(cells) / COLS)
    layout["rows"] = rows
    atlas = Image.new("RGBA", (COLS * FRAME, rows * FRAME), (0, 0, 0, 0))
    for index, cell in enumerate(cells):
        atlas.paste(cell, ((index % COLS) * FRAME, (index // COLS) * FRAME))
    public = args.kind_robots / "public" / "zuzu-pinball"
    public.mkdir(parents=True, exist_ok=True)
    atlas.save(public / "river-croc.webp", "WEBP", quality=82, alpha_quality=100, method=6)
    write_ts(args.kind_robots / "utils/arcade/pinball/tables/zuzuLastBell/crocSprite.ts", layout)
    size = (public / "river-croc.webp").stat().st_size
    print(f"{len(cells)} frames, atlas {atlas.width}x{atlas.height}, {size / 1e6:.2f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
