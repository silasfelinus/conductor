"""zuzu-showdown t-010: the fighter rig (the t-007 recommendation, method B grown up).

A fighter is a config module in tools/rigs/<slug>.py: where each body part is cut from its HD source art
(polygon, pivot, draw order), how each animation poses those parts frame by frame, and the P2 colour
swaps. This script poses every frame at HD, then writes, per style:

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

from PIL import Image, ImageDraw, ImageOps

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sprite_common as sc

CANVAS = (1600, 1500)
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
    angle = pose.get("angle", 0)
    moved = part.rotate(angle, resample=Image.Resampling.BICUBIC, center=tuple(pivot)) if angle else part
    canvas.alpha_composite(moved, (OFFSET[0] + pose.get("dx", 0), OFFSET[1] + pose.get("dy", 0)))


def pose_frame(rig, parts: dict[str, Image.Image], frame: dict) -> Image.Image:
    """Compose one frame: every part in draw order, posed by the frame (a part's pose falls back to
    its group's, e.g. the head follows `body` unless the frame poses `head` itself)."""
    canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    hidden = set(frame.get("hide", []))
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


def p2_recolour(frame: Image.Image, palette: Image.Image, swaps: dict[int, tuple[int, int, int]]) -> Image.Image:
    """Shift every pixel whose nearest palette entry is swapped by that entry's colour delta, so HD
    shading survives the swap (pixel frames, already palette colours, map exactly)."""
    if not swaps:
        return frame
    entries = palette.getpalette()[: 3 * 256]
    index = frame.convert("RGB").quantize(palette=palette, dither=Image.Dither.NONE)
    src, idx = frame.load(), index.load()
    out = frame.copy()
    dst = out.load()
    deltas = {i: tuple(c - entries[3 * i + k] for k, c in enumerate(rgb)) for i, rgb in swaps.items()}
    for y in range(frame.height):
        for x in range(frame.width):
            r, g, b, a = src[x, y]
            d = deltas.get(idx[x, y]) if a else None
            if d:
                dst[x, y] = (max(0, min(255, r + d[0])), max(0, min(255, g + d[1])), max(0, min(255, b + d[2])), a)
    return out


def nearest_index(palette: Image.Image, rgb) -> int:
    probe = Image.new("RGB", (1, 1), tuple(rgb)).quantize(palette=palette, dither=Image.Dither.NONE)
    return probe.getpixel((0, 0))


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
    ref = sources[(rig.REFERENCE["art"], rig.REFERENCE.get("mirror", False))]
    figure_height = sc.crop_to_content(ref).height

    raw = {name: [pose_frame(rig, parts, f) for f in anim["frames"]] for name, anim in rig.ANIMATIONS.items()}
    box = shared_box([f for fs in raw.values() for f in fs])
    hd = {n: [sc.to_hd(f.crop(box), figure_height, rig.HEIGHT * sc.HD_SCALE) for f in fs] for n, fs in raw.items()}
    game = {n: [sc.to_game_size(f.crop(box), figure_height, rig.HEIGHT) for f in fs] for n, fs in raw.items()}
    palette = sc.shared_palette([f for fs in game.values() for f in fs], rig.PALETTE_COLOURS)
    pixel = {n: [sc.outer_outline(sc.quantize(f, palette)) for f in fs] for n, fs in game.items()}
    swaps = {nearest_index(palette, base): alt for base, alt in rig.P2_SWAPS}

    out.mkdir(parents=True, exist_ok=True)
    for style, frames, scale in (("hd", hd, sc.HD_SCALE), ("pixel", pixel, 1)):
        atlas, rects = pack(frames, scale)
        atlas.save(out / f"{slug}-{style}.png")
        p2 = {n: [p2_recolour(f, palette, swaps) for f in fs] for n, fs in frames.items()}
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
                sc.write_hd_gif(fs, out / "preview", f"{name}-hd", rig.ANIMATIONS[name]["fps"])
    print(json.dumps({
        "fighter": slug,
        "animations": {n: len(fs) for n, fs in hd.items()},
        "pixel_colours": sc.palette_size([f for fs in pixel.values() for f in fs]),
        "p2_swaps": len(swaps),
    }))


if __name__ == "__main__":
    main(*sys.argv[1:4])
