"""zuzu-showdown t-011: a puppet's pose sheet (the Siblings' toddler).

A puppet is drawn beside its fighter from whole poses, not a rig: the toddler is never a hurtbox
(fighters.yaml children_rules), so he needs no boxes, only a pose for each of his sister's states. Each
pose is its own source image (art/T011-SIBLINGS-PARTS.yaml's toddler-* subjects). This keys out the
background, scales every pose by one factor (taken from his standing reference, so a duck is shorter
than a stand, as it should be), puts the anchor under his feet, and writes the same files as rig.py:

    OUT/<slug>-hd.png + <slug>-hd.json         HD atlas (4x game resolution) and frame map
    OUT/<slug>-pixel.png + <slug>-pixel.json   pixel atlas (game resolution, indexed palette, outline)
    OUT/<slug>-p2-hd.png, <slug>-p2-pixel.png  the P2 alternate colours

Each pose is an animation of one frame, named for the pose; the game picks it (sprites.ts puppetPlace).
Ship the HD sheet with `ship_hd.py sprites <slug> OUT GAME_DIR` like a fighter's.

    python projects/zuzu-showdown/tools/puppet.py SLUG SOURCE_DIR OUT_DIR

SOURCE_DIR holds the source art as <art_image_id>.png (method_a_process.py's cache layout).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rig  # noqa: E402
import sprite_common as sc  # noqa: E402

PUPPETS = {
    "toddler": {
        # Game pixels tall standing: his sister is 84, and he comes up to her chest.
        "height": 48,
        # His standing reference sheet (fighters.yaml's approved set), the scale for every pose.
        "reference": 242156,
        # Pose name -> art image id (T011-SIBLINGS-PARTS.yaml's toddler-<pose> subjects).
        "poses": {
            "stand": 243484,
            "duck": 243485,
            "throw": 243486,
            "proud": 243487,
            "wave": 243488,
            "raspberry": 243489,
        },
        # His fur takes the same P2 turn as his sister's (rigs/siblings.py P2_RULES), so they match.
        "p2_rules": [{"hue": (18, 44), "sat_min": 0.3, "val_min": 0.35, "shift": -14, "sat": 1.35}],
        "palette_colours": 20,
    },
}


def feet(image: Image.Image) -> tuple[int, int]:
    """Where he stands: the middle of the lowest rows of the figure, at its bottom edge."""
    alpha = image.getchannel("A")
    box = alpha.getbbox()
    if not box:
        return (image.width // 2, image.height)
    band = max(4, (box[3] - box[1]) // 12)
    low = alpha.crop((0, box[3] - band, image.width, box[3])).getbbox()
    x = (low[0] + low[2]) // 2 if low else (box[0] + box[2]) // 2
    return (x, box[3])


def main(slug: str, source_dir: str, out_dir: str) -> None:
    spec = PUPPETS[slug]
    src, out = Path(source_dir), Path(out_dir)
    # A pose whose art hasn't rendered yet is left out: the game draws the standing pose in its place.
    missing = [name for name, art in spec["poses"].items() if not art]
    if "stand" in missing:
        raise SystemExit(f"{slug}: no standing pose yet")
    if missing:
        print(f"{slug}: no art yet for {', '.join(missing)}; the game stands in with 'stand'", file=sys.stderr)
    poses = {name: art for name, art in spec["poses"].items() if art}
    figure_height = sc.crop_to_content(rig.load_source(src, spec["reference"], False)).height
    height = spec["height"]
    hd_scale = height * sc.HD_SCALE / figure_height
    game_scale = height / figure_height

    hd, game, anchors = {}, {}, {}
    for name, art in poses.items():
        source = rig.load_source(src, art, False)
        box = source.getchannel("A").getbbox()
        pose = source.crop(box)
        fx, fy = feet(pose)
        hd[name] = [sc.to_hd(pose, figure_height, height * sc.HD_SCALE)]
        game[name] = [sc.to_game_size(pose, figure_height, height)]
        anchors[name] = {"hd": (round(fx * hd_scale), round(fy * hd_scale)),
                         # outer_outline pads the pixel frames by one pixel on every side
                         "pixel": (round(fx * game_scale) + 1, round(fy * game_scale) + 1)}
    palette = sc.shared_palette([f for fs in game.values() for f in fs], spec["palette_colours"])
    pixel = {n: [sc.outer_outline(sc.quantize(f, palette)) for f in fs] for n, fs in game.items()}

    out.mkdir(parents=True, exist_ok=True)
    for style, frames, scale in (("hd", hd, sc.HD_SCALE), ("pixel", pixel, 1)):
        atlas, rects = rig.pack(frames)
        rig.save_atlas(atlas, out / f"{slug}-{style}.png", style == "pixel")
        p2 = {n: [rig.p2_recolour(f, spec["p2_rules"]) for f in fs] for n, fs in frames.items()}
        rig.save_atlas(rig.pack(p2)[0], out / f"{slug}-p2-{style}.png", style == "pixel")
        frame_map = {
            "fighter": slug,
            "style": style,
            "scale": scale,
            "height": height,
            "atlas": f"{slug}-{style}.png",
            "atlas_p2": f"{slug}-p2-{style}.png",
            # ship_hd.py's WebP drops the P2 atlas for these rules (the game recolours HD itself).
            **({"p2_rules": [{**r, "hue": list(r["hue"])} for r in spec["p2_rules"]]} if style == "hd" else {}),
            "animations": {
                name: {
                    "fps": 1,
                    "loop": False,
                    "frames": [{**rects[name][0],
                                "anchor": {"x": anchors[name][style][0], "y": anchors[name][style][1]}}],
                }
                for name in frames
            },
        }
        (out / f"{slug}-{style}.json").write_text(json.dumps(frame_map, indent=1) + "\n")
    print(json.dumps({
        "puppet": slug,
        "poses": {n: list(fs[0].size) for n, fs in pixel.items()},
        "pixel_colours": sc.palette_size([f for fs in pixel.values() for f in fs]),
    }))


if __name__ == "__main__":
    main(*sys.argv[1:4])
