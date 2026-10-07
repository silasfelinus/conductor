"""zuzu-showdown t-010: the fighter rig (the t-007 recommendation, method B grown up).

A fighter is a config module in tools/rigs/<slug>.py: where each body part is cut from its HD source art
(polygon, pivot, draw order), how each animation poses those parts frame by frame, and the P2 colour
rules. This script poses every frame at HD, then writes, per style:

    OUT/<slug>-hd.png + <slug>-hd.json         HD atlas (4x game resolution) and frame map
    OUT/<slug>-pixel.png + <slug>-pixel.json   pixel atlas (game resolution, indexed palette, outline)
    OUT/<slug>-p2-hd.png, <slug>-p2-pixel.png  the P2 alternate colours, same frame maps
    OUT/preview/<anim>-<style>.gif             previews

Pixel is derived from HD (Silas, 2026-10-06 PT: "pixel is a style choice"), so both styles always share
poses, timing and boxes. Frame maps are in game units (Zuzu is 72 tall) with the anchor at the feet, so
the renderer and the sim's boxes agree whatever the style.

    python projects/zuzu-showdown/tools/rig.py SLUG SOURCE_DIR OUT_DIR

SOURCE_DIR holds the source art as <art_image_id>.png (method_a_process.py's cache layout).
"""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageOps

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sprite_common as sc

CANVAS = (2000, 1500)
OFFSET = (300, 200)  # where a source image's (0, 0) lands on the posing canvas


def load_source(source_dir: Path, art_id: int, mirror: bool) -> Image.Image:
    image = Image.open(source_dir / f"{art_id}.png").convert("RGB")
    return sc.key_background(ImageOps.mirror(image) if mirror else image)


def cut(source: Image.Image, polygon) -> Image.Image:
    mask = Image.new("L", source.size, 0)
    ImageDraw.Draw(mask).polygon([tuple(p) for p in polygon], fill=255)
    part = Image.new("RGBA", source.size, (0, 0, 0, 0))
    part.paste(source, (0, 0), Image.composite(source.getchannel("A"), mask, mask))
    return part


def place(canvas: Image.Image, part: Image.Image, pose: dict, pivot) -> None:
    """Scale (`sx`, `sy`, compounding from 1), then rotate (`angle`), both about the part's pivot, then
    shift (`dx`, `dy`). Squashing the legs about the hip is what makes a crouch read as a crouch."""
    sx, sy = 1 + pose.get("sx", 0), 1 + pose.get("sy", 0)
    moved = part
    if sx != 1 or sy != 1:
        px, py = pivot
        moved = moved.transform(moved.size, Image.Transform.AFFINE,
                                (1 / sx, 0, px - px / sx, 0, 1 / sy, py - py / sy),
                                resample=Image.Resampling.BICUBIC)
    angle = pose.get("angle", 0)
    moved = moved.rotate(angle, resample=Image.Resampling.BICUBIC, center=tuple(pivot)) if angle else moved
    canvas.alpha_composite(moved, (OFFSET[0] + pose.get("dx", 0), OFFSET[1] + pose.get("dy", 0)))


def pose_frame(rig, parts: dict[str, Image.Image], frame: dict) -> Image.Image:
    """Compose one frame: every part in draw order, posed by the frame (a part's pose falls back to
    its group's, e.g. the head follows `body` unless the frame poses `head` itself)."""
    canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    hidden = set(frame.get("hide", []))
    # Code-drawn pieces on the far side of the body (the Coyote's gun arm) go down first.
    for draw in frame.get("draw_behind", []):
        getattr(rig, draw["fn"])(canvas, OFFSET, **draw.get("args", {}))
    for name in sorted(rig.PARTS, key=lambda n: rig.PARTS[n]["z"]):
        if name in hidden:
            continue
        spec = rig.PARTS[name]
        pose = {}
        for group in spec.get("follows", []):
            for key, value in frame.get(group, {}).items():
                pose[key] = pose.get(key, 0) + value
        for key, value in frame.get(name, {}).items():
            pose[key] = pose.get(key, 0) + value
        place(canvas, parts[name], pose, spec["pivot"])
    for draw in frame.get("draw", []):
        getattr(rig, draw["fn"])(canvas, OFFSET, **draw.get("args", {}))
    return canvas


def shared_box(frames: list[Image.Image]):
    box = None
    for f in frames:
        b = f.getchannel("A").getbbox()
        if b:
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
    return box


def p2_recolour(frame: Image.Image, rules: list[dict]) -> Image.Image:
    """P2's alternate colours: every pixel whose hue, saturation and value fall inside a rule is
    hue-rotated (and optionally re-saturated). Working in HSV keeps HD shading and pixel art alike,
    and needs no exact palette colours, so it survives a re-cut of the parts.

    A rule: {"hue": (lo, hi) degrees, "sat_min", "val_min", "val_max", "shift" degrees, "sat" multiplier}.
    """
    if not rules:
        return frame
    alpha = np.asarray(frame.convert("RGBA"))[..., 3]
    hsv = np.asarray(frame.convert("RGB").convert("HSV")).astype(np.float32)
    hue = hsv[..., 0] * 360.0 / 255.0
    sat = hsv[..., 1] / 255.0
    val = hsv[..., 2] / 255.0
    out_h, out_s = hue.copy(), sat.copy()
    for rule in rules:
        lo, hi = rule["hue"]
        mask = (alpha > 0) & (hue >= lo) & (hue <= hi) & (sat >= rule.get("sat_min", 0.0))
        mask &= (val >= rule.get("val_min", 0.0)) & (val <= rule.get("val_max", 1.0))
        out_h[mask] = (hue[mask] + rule.get("shift", 0.0)) % 360.0
        out_s[mask] = np.clip(sat[mask] * rule.get("sat", 1.0), 0.0, 1.0)
    hsv_out = np.stack([out_h * 255.0 / 360.0, out_s * 255.0, val * 255.0], axis=-1)
    recoloured = Image.fromarray(np.round(hsv_out).astype(np.uint8), "HSV").convert("RGB")
    out = recoloured.convert("RGBA")
    out.putalpha(frame.getchannel("A"))
    return out


def pack(frames: dict[str, list[Image.Image]], scale: int):
    """Shelf-pack every frame into one atlas; returns the atlas and {anim: [rect...]}."""
    cell_w = max(f.width for fs in frames.values() for f in fs)
    cell_h = max(f.height for fs in frames.values() for f in fs)
    columns = max(len(fs) for fs in frames.values())
    atlas = Image.new("RGBA", (cell_w * columns, cell_h * len(frames)), (0, 0, 0, 0))
    rects = {}
    for row, (name, fs) in enumerate(frames.items()):
        rects[name] = []
        for col, f in enumerate(fs):
            x, y = col * cell_w, row * cell_h
            atlas.alpha_composite(f, (x, y))
            rects[name].append({"x": x, "y": y, "w": f.width, "h": f.height})
    return atlas, rects


def hurtbox(frame: Image.Image, scale: float) -> dict:
    """The silhouette's bounding box in game units, y up from the feet: a starting hurtbox drawn from
    the art itself, for t-024's balance pass to tune per move."""
    b = frame.getchannel("A").getbbox() or (0, 0, 0, 0)
    w, h = frame.size
    return {
        "x": round((b[0] - w / 2) / scale),
        "y": round((h - b[3]) / scale),
        "w": round((b[2] - b[0]) / scale),
        "h": round((b[3] - b[1]) / scale),
    }


def main(slug: str, source_dir: str, out_dir: str) -> None:
    rig = importlib.import_module(f"rigs.{slug}")
    src, out = Path(source_dir), Path(out_dir)
    sources = {}
    parts = {}
    for name, spec in rig.PARTS.items():
        key = (spec["art"], spec.get("mirror", False))
        if key not in sources:
            sources[key] = load_source(src, *key)
        parts[name] = cut(sources[key], spec["polygon"])
    # The scale reference need not be a part source (Zuzu's parts come from the stance render, his
    # scale from the standing build), so load it on its own when it isn't.
    ref_key = (rig.REFERENCE["art"], rig.REFERENCE.get("mirror", False))
    ref = sources.get(ref_key) or load_source(src, *ref_key)
    figure_height = sc.crop_to_content(ref).height

    raw = {name: [pose_frame(rig, parts, f) for f in anim["frames"]] for name, anim in rig.ANIMATIONS.items()}
    box = shared_box([f for fs in raw.values() for f in fs])
    hd = {n: [sc.to_hd(f.crop(box), figure_height, rig.HEIGHT * sc.HD_SCALE) for f in fs] for n, fs in raw.items()}
    game = {n: [sc.to_game_size(f.crop(box), figure_height, rig.HEIGHT) for f in fs] for n, fs in raw.items()}
    palette = sc.shared_palette([f for fs in game.values() for f in fs], rig.PALETTE_COLOURS)
    pixel = {n: [sc.outer_outline(sc.quantize(f, palette)) for f in fs] for n, fs in game.items()}

    out.mkdir(parents=True, exist_ok=True)
    for style, frames, scale in (("hd", hd, sc.HD_SCALE), ("pixel", pixel, 1)):
        atlas, rects = pack(frames, scale)
        atlas.save(out / f"{slug}-{style}.png")
        p2 = {n: [p2_recolour(f, rig.P2_RULES) for f in fs] for n, fs in frames.items()}
        pack(p2, scale)[0].save(out / f"{slug}-p2-{style}.png")
        frame_map = {
            "fighter": slug,
            "style": style,
            "scale": scale,
            "height": rig.HEIGHT,
            "atlas": f"{slug}-{style}.png",
            "atlas_p2": f"{slug}-p2-{style}.png",
            "animations": {
                name: {
                    "fps": rig.ANIMATIONS[name]["fps"],
                    "loop": rig.ANIMATIONS[name].get("loop", False),
                    "frames": [
                        {**rect, "anchor": {"x": rect["w"] // 2, "y": rect["h"]},
                         "hurt": hurtbox(frames[name][i], scale)}
                        for i, rect in enumerate(rects[name])
                    ],
                }
                for name in frames
            },
        }
        (out / f"{slug}-{style}.json").write_text(json.dumps(frame_map, indent=1) + "\n")
        for name, fs in frames.items():
            if style == "pixel":
                sc.write_previews(sc.anchor_frames(fs), out / "preview", f"{name}-pixel", rig.ANIMATIONS[name]["fps"])
            else:
                sc.write_hd_gif(fs, out / "preview", name, rig.ANIMATIONS[name]["fps"])
    print(json.dumps({
        "fighter": slug,
        "animations": {n: len(fs) for n, fs in hd.items()},
        "pixel_colours": sc.palette_size([f for fs in pixel.values() for f in fs]),
        "p2_rules": len(rig.P2_RULES),
    }))


if __name__ == "__main__":
    main(*sys.argv[1:4])
