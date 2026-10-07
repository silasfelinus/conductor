"""zuzu-showdown t-007, method B: a cutout rig animated in code.

Body parts are cut once from Zuzu's reference build (A7, ArtImage 242193, mirrored to face right):
the head with the kasa, the poncho torso, two legs and the katana hilt. Each frame poses them with
offsets and rotations about hand-placed pivots at full resolution, then the composite goes through
the same pixelize step as method A (sprite_common), so the comparison is about the motion, not the
downscale. The katana's blade is hidden behind the poncho in the reference, so the drawn blade and
the sword arm are drawn in code.

    python projects/zuzu-showdown/tools/method_b_rig.py REFERENCE.png OUT_DIR
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sprite_common as sc

# Part masks, in the mirrored reference's pixels (832 x 1216).
PARTS = {
    "hilt": [(186, 38), (246, 34), (342, 352), (338, 384), (232, 388), (226, 352), (262, 346)],
    "head": [(286, 150), (600, 112), (790, 236), (780, 290), (590, 300), (560, 400), (300, 400), (282, 300)],
    "torso": [(186, 352), (560, 360), (676, 560), (700, 800), (620, 920), (560, 930), (420, 840), (290, 810),
              (186, 760), (150, 620)],
    "back_leg": [(286, 790), (430, 800), (440, 1060), (420, 1210), (260, 1210), (276, 1000)],
    "front_leg": [(400, 800), (570, 800), (600, 900), (568, 1050), (600, 1210), (380, 1210), (410, 1060)],
}
HIP_BACK = (350, 830)
HIP_FRONT = (480, 830)
NECK = (440, 390)
SHOULDER = (470, 560)
FUR = (138, 150, 163)
FUR_DARK = (70, 76, 88)
STEEL = (196, 204, 214)
STEEL_EDGE = (246, 248, 250)
INK = (24, 20, 26)


def cut(reference: Image.Image, polygon) -> Image.Image:
    mask = Image.new("L", reference.size, 0)
    ImageDraw.Draw(mask).polygon(polygon, fill=255)
    part = Image.new("RGBA", reference.size, (0, 0, 0, 0))
    part.paste(reference, (0, 0), Image.composite(reference.getchannel("A"), mask, mask))
    return part


def place(canvas: Image.Image, part: Image.Image, angle=0.0, pivot=(0, 0), dx=0, dy=0) -> None:
    """Rotate `part` by `angle` degrees (counter-clockwise) about `pivot`, shift it, composite it."""
    moved = part.rotate(angle, resample=Image.Resampling.BICUBIC, center=pivot) if angle else part
    canvas.alpha_composite(moved, (OFFSET[0] + dx, OFFSET[1] + dy))


def draw_arm(canvas: Image.Image, shoulder, hand, dx=0, dy=0) -> None:
    d = ImageDraw.Draw(canvas)
    s = (shoulder[0] + OFFSET[0] + dx, shoulder[1] + OFFSET[1] + dy)
    h = (hand[0] + OFFSET[0], hand[1] + OFFSET[1])
    d.line([s, h], fill=INK, width=74)
    d.line([s, h], fill=FUR, width=58)
    d.ellipse([h[0] - 40, h[1] - 40, h[0] + 40, h[1] + 40], fill=INK)
    d.ellipse([h[0] - 32, h[1] - 32, h[0] + 32, h[1] + 32], fill=FUR_DARK)


def draw_sword(canvas: Image.Image, hilt_part: Image.Image, hand, angle_deg: float) -> None:
    """The katana held at `hand`, pointing `angle_deg` (0 = straight ahead, positive = up)."""
    a = math.radians(angle_deg)
    ux, uy = math.cos(a), -math.sin(a)
    hx, hy = hand[0] + OFFSET[0], hand[1] + OFFSET[1]
    d = ImageDraw.Draw(canvas)
    # Grip behind the hand, guard, then a long slightly curved blade.
    d.line([(hx - ux * 150, hy - uy * 150), (hx + ux * 40, hy + uy * 40)], fill=INK, width=44)
    d.line([(hx - ux * 150, hy - uy * 150), (hx + ux * 40, hy + uy * 40)], fill=(60, 44, 36), width=30)
    gx, gy = hx + ux * 50, hy + uy * 50
    d.line([(gx - uy * 46, gy + ux * 46), (gx + uy * 46, gy - ux * 46)], fill=INK, width=26)
    tip = (hx + ux * 640, hy + uy * 640)
    d.line([(gx, gy), tip], fill=INK, width=30)
    d.line([(gx, gy), tip], fill=STEEL, width=18)
    d.line([(gx - uy * 5, gy + ux * 5), (tip[0] - uy * 5, tip[1] + ux * 5)], fill=STEEL_EDGE, width=6)


CANVAS = (1500, 1400)
OFFSET = (260, 150)  # where the reference's (0, 0) lands on the posing canvas


def pose(parts, frame) -> Image.Image:
    canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    body_dy = frame.get("body_dy", 0)
    head_dy = frame.get("head_dy", body_dy)
    lean = frame.get("lean", 0)
    if frame.get("sheathed", True):
        place(canvas, parts["hilt"], lean, NECK, 0, head_dy)
    place(canvas, parts["back_leg"], frame.get("back", 0), HIP_BACK, 0, frame.get("back_dy", 0))
    place(canvas, parts["front_leg"], frame.get("front", 0), HIP_FRONT, 0, frame.get("front_dy", 0))
    place(canvas, parts["torso"], lean, HIP_FRONT, 0, body_dy)
    place(canvas, parts["head"], lean, NECK, frame.get("head_dx", 0), head_dy)
    if "hand" in frame:
        draw_arm(canvas, SHOULDER, frame["hand"], 0, body_dy)
        if not frame.get("sheathed", True):
            draw_sword(canvas, parts["hilt"], frame["hand"], frame["sword"])
    return canvas


# Source pixels: one game pixel is about 16 of them.
ANIMATIONS = {
    "idle": [
        {"body_dy": 0},
        {"body_dy": -10, "head_dy": -8},
        {"body_dy": -16, "head_dy": -16},
        {"body_dy": -8, "head_dy": -14},
    ],
    "walk": [
        {"front": 20, "back": -18, "body_dy": 6},
        {"front": 10, "back": -8, "body_dy": 16, "back_dy": -12},
        {"front": -4, "back": 6, "body_dy": 0, "back_dy": -24},
        {"front": -16, "back": 16, "body_dy": -12},
        {"front": -20, "back": 20, "body_dy": 6},
        {"front": -6, "back": 6, "body_dy": 0, "front_dy": -24},
    ],
    "hp": [
        {"body_dy": 24, "hand": (330, 330), "sheathed": True, "lean": -4},
        {"body_dy": 16, "hand": (520, 300), "sheathed": False, "sword": 70, "lean": 4},
        {"body_dy": 8, "hand": (760, 520), "sheathed": False, "sword": 0, "lean": 10, "front": 14, "back": -10},
        {"body_dy": 12, "hand": (640, 640), "sheathed": False, "sword": -40, "lean": 8, "front": 14, "back": -10},
        {"body_dy": 4, "hand": (360, 360), "sheathed": True, "lean": 0},
    ],
}


def main(reference_path: str, out_dir: str) -> None:
    started = time.perf_counter()
    reference = ImageOps.mirror(Image.open(reference_path).convert("RGB"))
    keyed = sc.key_background(reference)
    parts = {name: cut(keyed, polygon) for name, polygon in PARTS.items()}
    figure_height = sc.crop_to_content(keyed).height
    raw = {name: [pose(parts, f) for f in frames] for name, frames in ANIMATIONS.items()}
    # Crop every frame of the fighter with one shared box, so the feet stay put between frames.
    box = None
    for frames in raw.values():
        for f in frames:
            b = f.getchannel("A").getbbox()
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
    game = {name: [sc.to_game_size(f.crop(box), figure_height) for f in frames] for name, frames in raw.items()}
    palette = sc.shared_palette([f for frames in game.values() for f in frames], 16)
    out = Path(out_dir)
    meta = {"method": "B cutout rig", "reference": 242193, "palette_colours": 0, "frames": {}}
    every = []
    for name, frames in game.items():
        final = [sc.outer_outline(sc.quantize(f, palette)) for f in frames]
        every.extend(final)
        sc.write_previews(final, out, f"b-{name}", sc.FPS[name])
        meta["frames"][name] = len(final)
    meta["palette_colours"] = sc.palette_size(every)
    meta["frame_size"] = list(every[0].size)
    meta["seconds_to_render_all"] = round(time.perf_counter() - started, 1)
    (out / "b-meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta))


if __name__ == "__main__":
    main(*sys.argv[1:3])
