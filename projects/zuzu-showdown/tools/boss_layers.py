"""zuzu-showdown t-021: ship The Thing Behind the Door's layers to the game.

The boss is never drawn whole (fighters.yaml boss.look): a door of starry dark at the edge of the Thin
Place, and what comes through it. art/T021-BOSS-PARTS.yaml holds the parts Kontext re-drew from the
picked door (243506): a rising tentacle, a sweeping tentacle, a grasping tentacle and the eye, each on a
plain light ground. This keys that ground out (a flood from the image's edges, so light spots inside a
part survive), crops each part to what is left, and writes what the game's two render styles load:

    GAME_DIR/<layer>-pixel.png   game resolution, quantized (alpha kept)
    GAME_DIR/<layer>-hd.webp     HD_SCALE times that
    INDEX                        the layers and their game sizes, for the game to import (boss.json)

The door itself ships as the framed panel cropped from 243506 (its pale pillars are part of it, so it
is not keyed).

    python projects/zuzu-showdown/tools/boss_layers.py SOURCE_DIR GAME_DIR INDEX

SOURCE_DIR holds the art as <art_image_id>.png (method_a_process.py's cache layout); missing ones are
downloaded into it.
"""

from __future__ import annotations

import json
import sys
from collections import deque
from pathlib import Path

import yaml
from PIL import Image

HERE = Path(__file__).resolve().parent
LEDGER = HERE.parent / "art" / "T021-BOSS-PARTS.yaml"
DOOR_ID = 243506
# The door panel in 243506: its pillars and the starry dark between them.
DOOR_BOX = (240, 0, 978, 832)

# Game pixels per layer: the door stands taller than any fighter; the tentacles are sized to the hits
# they draw (boss.ts), the eye to its phase-three hurtbox.
SIZES = {
    "door": (133, 150),
    "tentacle-rise": (64, 112),
    "tentacle-sweep": (190, 76),
    "tentacle-grasp": (80, 116),
    "eye": (72, 48),
}
KEYS = {
    "boss-tentacle-rise": "tentacle-rise",
    "boss-tentacle-sweep": "tentacle-sweep",
    "boss-tentacle-grasp": "tentacle-grasp",
    "boss-eye": "eye",
}
HD_SCALE = 3
COLOURS = 48
QUALITY = 84
# A ground pixel: light and nearly grey.
GROUND_LUMA = 205
GROUND_CHROMA = 28


def source(src: Path, art_id: int) -> Image.Image:
    path = src / f"{art_id}.png"
    if not path.exists():
        sys.path.insert(0, str(HERE))
        import method_a_process

        method_a_process.download(art_id, src)
    return Image.open(path).convert("RGBA")


def key_ground(image: Image.Image) -> Image.Image:
    """Clear the light ground connected to the image's edges."""
    rgba = image.copy()
    w, h = rgba.size
    px = rgba.load()

    def ground(x: int, y: int) -> bool:
        r, g, b, _ = px[x, y]
        return (r + g + b) / 3 >= GROUND_LUMA and max(r, g, b) - min(r, g, b) <= GROUND_CHROMA

    seen = bytearray(w * h)
    queue: deque[tuple[int, int]] = deque()
    for x in range(w):
        queue.extend(((x, 0), (x, h - 1)))
    for y in range(h):
        queue.extend(((0, y), (w - 1, y)))
    while queue:
        x, y = queue.popleft()
        i = y * w + x
        if seen[i] or not ground(x, y):
            continue
        seen[i] = 1
        px[x, y] = (0, 0, 0, 0)
        if x > 0:
            queue.append((x - 1, y))
        if x < w - 1:
            queue.append((x + 1, y))
        if y > 0:
            queue.append((x, y - 1))
        if y < h - 1:
            queue.append((x, y + 1))
    return rgba


def fit(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Scale to fit `size` keeping the aspect, centred on a transparent canvas of exactly `size`."""
    w, h = size
    scale = min(w / image.width, h / image.height)
    part = image.resize((max(1, round(image.width * scale)), max(1, round(image.height * scale))),
                        Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    canvas.paste(part, ((w - part.width) // 2, h - part.height), part)
    return canvas


def write(out: Path, name: str, image: Image.Image) -> None:
    w, h = SIZES[name]
    hd = fit(image, (w * HD_SCALE, h * HD_SCALE))
    hd.save(out / f"{name}-hd.webp", "WEBP", quality=QUALITY, method=6)
    pixel = fit(image, (w, h))
    alpha = pixel.getchannel("A").point(lambda a: 255 if a >= 128 else 0)
    pixel = pixel.convert("RGB").quantize(colors=COLOURS, method=Image.Quantize.MEDIANCUT,
                                          dither=Image.Dither.NONE).convert("RGBA")
    pixel.putalpha(alpha)
    pixel.save(out / f"{name}-pixel.png", optimize=True)


def main(source_dir: str, game_dir: str, index_path: str) -> None:
    src, out = Path(source_dir), Path(game_dir)
    out.mkdir(parents=True, exist_ok=True)
    ledger = yaml.safe_load(LEDGER.read_text())
    layers: dict[str, dict[str, int]] = {}
    write(out, "door", source(src, DOOR_ID).crop(DOOR_BOX))
    layers["door"] = {"w": SIZES["door"][0], "h": SIZES["door"][1]}
    skipped = []
    for subject in ledger["subjects"]:
        art = (subject.get("art") or {}).get("kontext-parts") or {}
        name = KEYS.get(subject["key"])
        if not name or art.get("status") != "DONE" or not art.get("art_image_id"):
            skipped.append(subject["key"])
            continue
        keyed = key_ground(source(src, art["art_image_id"]))
        box = keyed.getchannel("A").getbbox()
        write(out, name, keyed.crop(box) if box else keyed)
        layers[name] = {"w": SIZES[name][0], "h": SIZES[name][1]}
    Path(index_path).write_text(json.dumps(layers, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"layers": sorted(layers), "skipped": skipped}))


if __name__ == "__main__":
    main(*sys.argv[1:4])
