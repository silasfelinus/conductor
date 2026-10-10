"""zuzu-showdown t-027: ship the HD style's art to the game.

rig.py and stage.py write HD masters as RGBA PNG at 4x the game resolution, too heavy to serve as they
are (Zuzu's atlas is 8.5 MB, the Coyote's 16 MB and taller than any browser will decode). This turns
them into what the game's HD style loads:

    python projects/zuzu-showdown/tools/ship_hd.py sprites SLUG RIG_OUT_DIR GAME_DIR [--scale 3]
    python projects/zuzu-showdown/tools/ship_hd.py stage SLUG STAGE_OUT_DIR GAME_DIR

Sprites: every frame is resized to `--scale` (3x by default: the game supersamples HD at 3-5x, and 3x
art holds up there at half the bytes of 4x), repacked into rows no wider than MAX_WIDTH, and saved as
lossy WebP with full-quality alpha. The frame map keeps its game-unit boxes and gets its rects and
anchors rescaled. There is no P2 atlas: the frame map carries the rig's P2_RULES and the game recolours
the atlas itself when a mirror match needs it (the same HSV rule rig.py's p2_recolour applies), which
halves what HD costs to ship.

Stages: each layer and cutout goes out as WebP at the master's own 4x; the manifest's units are game
units already, so only its file names change.

GAME_DIR is the kind_robots public folder the files go to (public/zuzu-showdown-sprites or
public/zuzu-showdown-stages). Run prettier on the JSON there before committing.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

# WebP refuses anything over 16383 px a side; rows this wide keep both sides well under it.
MAX_WIDTH = 4096
QUALITY = 78


def save_webp(image: Image.Image, path: Path) -> int:
    image.save(path, "WEBP", quality=QUALITY, alpha_quality=100, method=6)
    return path.stat().st_size


def repack(frames: list[Image.Image]) -> tuple[Image.Image, list[dict]]:
    """Shelf-pack the frames in order, wrapping to a new row at MAX_WIDTH."""
    rects, x, y, row = [], 0, 0, 0
    for f in frames:
        if x and x + f.width > MAX_WIDTH:
            x, y, row = 0, y + row, 0
        rects.append({"x": x, "y": y, "w": f.width, "h": f.height})
        x += f.width
        row = max(row, f.height)
    atlas = Image.new("RGBA", (max(r["x"] + r["w"] for r in rects), y + row), (0, 0, 0, 0))
    for f, r in zip(frames, rects):
        atlas.alpha_composite(f, (r["x"], r["y"]))
    return atlas, rects


def ship_sprites(slug: str, rig_out: Path, game_dir: Path, scale: int) -> dict:
    sheet = json.loads((rig_out / f"{slug}-hd.json").read_text())
    master = Image.open(rig_out / sheet["atlas"]).convert("RGBA")
    ratio = scale / sheet["scale"]
    order, frames = [], []
    for name, anim in sheet["animations"].items():
        for i, fr in enumerate(anim["frames"]):
            crop = master.crop((fr["x"], fr["y"], fr["x"] + fr["w"], fr["y"] + fr["h"]))
            size = (max(1, round(fr["w"] * ratio)), max(1, round(fr["h"] * ratio)))
            frames.append(crop.resize(size, Image.Resampling.LANCZOS))
            order.append((name, i))
    atlas, rects = repack(frames)
    for (name, i), rect in zip(order, rects):
        fr = sheet["animations"][name]["frames"][i]
        anchor = fr["anchor"]
        fr.update(rect)
        fr["anchor"] = {"x": round(anchor["x"] * ratio), "y": round(anchor["y"] * ratio)}
    # A rig's P2 rules live in its config; a puppet sheet (puppet.py) carries its own.
    rules = sheet.get("p2_rules")
    if rules is None:
        rules = importlib.import_module(f"rigs.{slug}").P2_RULES
    sheet.update({
        "scale": scale,
        "atlas": f"{slug}-hd.webp",
        "atlas_p2": None,
        "p2_rules": [{**rule, "hue": list(rule["hue"])} for rule in rules],
    })
    game_dir.mkdir(parents=True, exist_ok=True)
    size = save_webp(atlas, game_dir / sheet["atlas"])
    (game_dir / f"{slug}-hd.json").write_text(json.dumps(sheet, indent=1) + "\n")
    return {"fighter": slug, "atlas": list(atlas.size), "bytes": size}


def ship_stage(slug: str, stage_out: Path, game_dir: Path) -> dict:
    manifest = json.loads((stage_out / f"{slug}-hd.json").read_text())
    total = 0
    game_dir.mkdir(parents=True, exist_ok=True)
    for item in manifest["layers"] + manifest["cutouts"]:
        name = Path(item["file"]).with_suffix(".webp").name
        total += save_webp(Image.open(stage_out / item["file"]).convert("RGBA"), game_dir / name)
        item["file"] = name
    (game_dir / f"{slug}-hd.json").write_text(json.dumps(manifest, indent=1) + "\n")
    return {"stage": slug, "bytes": total}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("kind", choices=["sprites", "stage"])
    parser.add_argument("slug")
    parser.add_argument("source", type=Path)
    parser.add_argument("game_dir", type=Path)
    parser.add_argument("--scale", type=int, default=3)
    args = parser.parse_args()
    if args.kind == "sprites":
        print(json.dumps(ship_sprites(args.slug, args.source, args.game_dir, args.scale)))
    else:
        print(json.dumps(ship_stage(args.slug, args.source, args.game_dir)))


if __name__ == "__main__":
    main()
