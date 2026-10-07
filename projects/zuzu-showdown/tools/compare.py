"""zuzu-showdown t-007: put the three methods side by side, frame-synced.

Reads the strips the three method scripts wrote (<a|b|c>-<anim>-strip.png at PREVIEW_SCALE, frame
count known per animation), and writes, per animation, compare-<anim>.gif (A | B | C playing in step)
and compare-<anim>.png (the first frame of each), on the dusk-orange of the game's desert stage, so
the sprites are judged where they will actually be seen.

    python projects/zuzu-showdown/tools/compare.py IN_DIR OUT_DIR
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sprite_common as sc

FRAMES = {"idle": 4, "walk": 6, "hp": 5}
METHODS = [("a", "A  Kontext re-pose"), ("b", "B  cutout rig"), ("c", "C  hand pixel")]
DUSK = (206, 112, 52)
SKY = (36, 30, 46)
GAP = 16
LABEL = 22


def split(strip: Image.Image, count: int) -> list[Image.Image]:
    width = strip.width // count
    return [strip.crop((i * width, 0, (i + 1) * width, strip.height)) for i in range(count)]


def recolour(frame: Image.Image) -> Image.Image:
    """The strips were written on the dark preview backdrop; swap it for the stage's dusk."""
    rgb = frame.convert("RGB")
    out = Image.new("RGB", rgb.size, DUSK)
    px, mp = rgb.load(), out.load()
    for y in range(rgb.height):
        for x in range(rgb.width):
            if px[x, y] != SKY:
                mp[x, y] = px[x, y]
    return out


def main(in_dir: str, out_dir: str) -> None:
    src, out = Path(in_dir), Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for anim, count in FRAMES.items():
        paths = [src / key / f"{key}-{anim}-strip.png" for key, _ in METHODS]
        missing = [p.name for p in paths if not p.exists()]
        if missing:
            print(f"{anim}: waiting on {', '.join(missing)}")
            continue
        columns = [[recolour(f) for f in split(Image.open(p), count)] for p in paths]
        cell_w = max(c[0].width for c in columns)
        cell_h = max(c[0].height for c in columns)
        size = (len(columns) * cell_w + (len(columns) + 1) * GAP, cell_h + LABEL + 2 * GAP)
        sheets = []
        for i in range(count):
            sheet = Image.new("RGB", size, (24, 20, 28))
            draw = ImageDraw.Draw(sheet)
            for j, ((_, label), column) in enumerate(zip(METHODS, columns)):
                x = GAP + j * (cell_w + GAP)
                draw.text((x, GAP // 2), label, fill=(240, 230, 210))
                frame = column[i]
                cell = Image.new("RGB", (cell_w, cell_h), DUSK)
                cell.paste(frame, ((cell_w - frame.width) // 2, cell_h - frame.height))
                sheet.paste(cell, (x, LABEL + GAP))
            sheets.append(sheet)
        sheets[0].save(out / f"compare-{anim}.png")
        sheets[0].save(out / f"compare-{anim}.gif", save_all=True, append_images=sheets[1:],
                       duration=round(1000 / sc.FPS[anim]), loop=0)
        print(out / f"compare-{anim}.gif")


if __name__ == "__main__":
    main(*sys.argv[1:3])
