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
the renderer and the sim's boxes agree whatever the style. Each frame carries `hurt` (the silhouette's
box) and, for an attack that names its striking layers (`strike`), `hit`: where the blade, fist or foot
reaches that frame. The game's sprite test holds every kit hitbox to that reach on the move's active
frames.

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

CANVAS = (2900, 1500)
# Where a source image's (0, 0) lands on the posing canvas: room on the left for falling backwards.
OFFSET = (1100, 200)


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


def pose_frame(rig, parts: dict[str, Image.Image], frame: dict, only: set[str] | None = None) -> Image.Image:
    """Compose one frame: every part in draw order, posed by the frame (a part's pose falls back to
    its group's, e.g. the head follows `body` unless the frame poses `head` itself).

    `only` composes just the named layers (part names, and "draw" / "draw_behind" for the frame's own
    code-drawn pieces): the striking layer an attack's hit box is measured from."""
    canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    hidden = set(frame.get("hide", []))
    # A rig with code-drawn arms gives resting arms (rest_arms(body_dy)) to any frame that doesn't
    # pose that layer itself, so idles, walks, hits and falls aren't armless. Resting arms never strike.
    rest = {}
    if only is None and hasattr(rig, "rest_arms"):
        rest = rig.rest_arms(frame.get("body", {}).get("dy", 0))
    # Code-drawn pieces on the far side of the body (the Coyote's gun arm) go down first.
    if only is None or "draw_behind" in only:
        for draw in frame.get("draw_behind", rest.get("draw_behind", [])):
            getattr(rig, draw["fn"])(canvas, OFFSET, **draw.get("args", {}))
    for name in sorted(rig.PARTS, key=lambda n: rig.PARTS[n]["z"]):
        if name in hidden or (only is not None and name not in only):
            continue
        spec = rig.PARTS[name]
        # A part's resting transform (`base`): how a separately rendered limb, drawn at its own scale,
        # is sized and placed onto the body before any animation moves it.
        pose = dict(spec.get("base", {}))
        for group in spec.get("follows", []):
            for key, value in frame.get(group, {}).items():
                pose[key] = pose.get(key, 0) + value
        for key, value in frame.get(name, {}).items():
            pose[key] = pose.get(key, 0) + value
        place(canvas, parts[name], pose, spec["pivot"])
    if only is None or "draw" in only:
        for draw in frame.get("draw", rest.get("draw", [])):
            getattr(rig, draw["fn"])(canvas, OFFSET, **draw.get("args", {}))
    # The whole figure at once (falls, knockdowns): rotate about a pivot in source pixels, then shift.
    whole = frame.get("whole")
    if whole:
        px, py = whole.get("pivot", (0, 0))
        centre = (OFFSET[0] + px, OFFSET[1] + py)
        turned = canvas.rotate(whole.get("angle", 0), resample=Image.Resampling.BICUBIC, center=centre)
        canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
        canvas.alpha_composite(turned, (whole.get("dx", 0), whole.get("dy", 0)))
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


def pack(frames: dict[str, list[Image.Image]]):
    """Shelf-pack: one row per animation, frames left to right; returns the atlas and {anim: [rect...]}."""
    width = max(sum(f.width for f in fs) for fs in frames.values())
    height = sum(max(f.height for f in fs) for fs in frames.values())
    atlas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    rects = {}
    y = 0
    for name, fs in frames.items():
        x = 0
        rects[name] = []
        for f in fs:
            atlas.alpha_composite(f, (x, y))
            rects[name].append({"x": x, "y": y, "w": f.width, "h": f.height})
            x += f.width
        y += max(f.height for f in fs)
    return atlas, rects


def save_atlas(atlas: Image.Image, path: Path, indexed: bool) -> None:
    """Save an atlas; the pixel style (at most a couple of dozen colours, alpha all-or-nothing) goes out as
    an exact indexed PNG, a third the size of RGBA with every pixel unchanged."""
    if not indexed:
        atlas.save(path)
        return
    rgba = np.asarray(atlas.convert("RGBA")).copy()
    rgba[rgba[..., 3] == 0] = 0
    colours, index = np.unique(rgba.reshape(-1, 4), axis=0, return_inverse=True)
    if len(colours) > 256:
        atlas.save(path)
        return
    out = Image.fromarray(index.reshape(rgba.shape[:2]).astype(np.uint8), "P")
    out.putpalette(colours[:, :3].astype(np.uint8).flatten().tolist())
    out.save(path, optimize=True, transparency=bytes(int(a) for a in colours[:, 3]))


def reach_box(layer: Image.Image, anchor_canvas: tuple[int, int], game_scale: float) -> dict | None:
    """Where an attack's striking layer reaches, in game units from the fighter's spot (x forward, y up
    from the ground), the same space as the kits' hitboxes; None when the layer is empty this frame."""
    b = layer.getchannel("A").point(lambda a: 255 if a > 96 else 0).getbbox()
    if not b:
        return None
    ax, ay = anchor_canvas
    return {
        "x": round((b[0] - ax) * game_scale),
        "y": round((ay - b[3]) * game_scale),
        "w": round((b[2] - b[0]) * game_scale),
        "h": round((b[3] - b[1]) * game_scale),
    }


def hurtbox(frame: Image.Image, anchor: tuple[int, int], scale: float) -> dict:
    """The silhouette's bounding box in game units relative to the anchor, y up from the ground: a
    starting hurtbox drawn from the art itself, for t-024's balance pass to tune per move."""
    b = frame.getchannel("A").getbbox() or (0, 0, 0, 0)
    ax, ay = anchor
    return {
        "x": round((b[0] - ax) / scale),
        "y": round((ay - b[3]) / scale),
        "w": round((b[2] - b[0]) / scale),
        "h": round((b[3] - b[1]) / scale),
    }


def main(slug: str, source_dir: str, out_dir: str) -> None:
    rig = importlib.import_module(f"rigs.{slug}")
    src, out = Path(source_dir), Path(out_dir)
    rig.SOURCE_DIR = src  # for rigs whose drawn pieces paste source art (the Coyote's sleeves)
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
    hd_scale = rig.HEIGHT * sc.HD_SCALE / figure_height
    game_scale = rig.HEIGHT / figure_height
    # An attack names its striking layers (`strike`: the blade arm, the kicking leg); each frame's reach
    # is measured from those alone, so the game can check its hitboxes against the art.
    anchor_canvas = (OFFSET[0] + rig.ANCHOR[0], OFFSET[1] + rig.ANCHOR[1])
    reach = {
        name: [reach_box(pose_frame(rig, parts, f, set(anim["strike"])), anchor_canvas, game_scale)
               for f in anim["frames"]]
        for name, anim in rig.ANIMATIONS.items() if anim.get("strike")
    }
    hd, game, anchors = {}, {}, {}
    for name, fs in raw.items():
        # Each animation is cropped on its own (a knockdown lies far wider than a stance), but its
        # frames share one box so they don't jitter, and the anchor is the fighter's spot on the ground.
        box = shared_box(fs)
        ax, ay = OFFSET[0] + rig.ANCHOR[0] - box[0], OFFSET[1] + rig.ANCHOR[1] - box[1]
        hd[name] = [sc.to_hd(f.crop(box), figure_height, rig.HEIGHT * sc.HD_SCALE) for f in fs]
        game[name] = [sc.to_game_size(f.crop(box), figure_height, rig.HEIGHT) for f in fs]
        anchors[name] = {"hd": (round(ax * hd_scale), round(ay * hd_scale)),
                         # outer_outline pads the pixel frames by one pixel on every side
                         "pixel": (round(ax * game_scale) + 1, round(ay * game_scale) + 1)}
    palette = sc.shared_palette([f for fs in game.values() for f in fs], rig.PALETTE_COLOURS)
    pixel = {n: [sc.outer_outline(sc.quantize(f, palette)) for f in fs] for n, fs in game.items()}

    out.mkdir(parents=True, exist_ok=True)
    for style, frames, scale in (("hd", hd, sc.HD_SCALE), ("pixel", pixel, 1)):
        atlas, rects = pack(frames)
        save_atlas(atlas, out / f"{slug}-{style}.png", style == "pixel")
        p2 = {n: [p2_recolour(f, rig.P2_RULES) for f in fs] for n, fs in frames.items()}
        save_atlas(pack(p2)[0], out / f"{slug}-p2-{style}.png", style == "pixel")
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
                        {**rect, "anchor": {"x": anchors[name][style][0], "y": anchors[name][style][1]},
                         "hurt": hurtbox(frames[name][i], anchors[name][style], scale),
                         **({"hit": reach[name][i]} if name in reach and reach[name][i] else {})}
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
