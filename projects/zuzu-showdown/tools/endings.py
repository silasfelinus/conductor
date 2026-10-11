"""zuzu-showdown t-021: ship the arcade ending stills to the game.

art/T021-ENDINGS.yaml holds two Kontext stills per fighter, set where their story ends after the door
shuts. This turns every rendered one into what the game's two render styles load, full screen behind
the ending's line (arcadeScreens.ts drawEndingScreen):

    GAME_DIR/<key>-pixel.png   480x270, quantized to a small palette (sits with the sprites)
    GAME_DIR/<key>-hd.webp     4x that, lossy WebP
    INDEX                      the stills that exist, for the game to import (endings.json)

<key> is the ledger key (zuzu-ending-1), which is also the file arcade.ts ENDINGS names. A still whose
art has not rendered, or was rejected and is being rerolled, is left out, and the game shows the
fighter's victory portrait in its place.

    python projects/zuzu-showdown/tools/endings.py SOURCE_DIR GAME_DIR INDEX

SOURCE_DIR holds the art as <art_image_id>.png (method_a_process.py's cache layout); missing ones are
downloaded into it.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
LEDGER = HERE.parent / "art" / "T021-ENDINGS.yaml"

SIZE = (480, 270)
HD_SCALE = 4
COLOURS = 64
QUALITY = 82


def main(source_dir: str, game_dir: str, index_path: str) -> None:
    src, out = Path(source_dir), Path(game_dir)
    out.mkdir(parents=True, exist_ok=True)
    ledger = yaml.safe_load(LEDGER.read_text())
    shipped: list[str] = []
    skipped: list[str] = []
    for subject in ledger["subjects"]:
        art = (subject.get("art") or {}).get("kontext-endings") or {}
        key = subject["key"]
        if art.get("status") != "DONE" or not art.get("art_image_id"):
            skipped.append(key)
            continue
        art_id = art["art_image_id"]
        path = src / f"{art_id}.png"
        if not path.exists():
            sys.path.insert(0, str(HERE))
            import method_a_process

            method_a_process.download(art_id, src)
        image = Image.open(path).convert("RGB")
        if subject.get("display_mirror"):
            image = ImageOps.mirror(image)
        w, h = SIZE
        hd = ImageOps.fit(image, (w * HD_SCALE, h * HD_SCALE), method=Image.Resampling.LANCZOS)
        hd.save(out / f"{key}-hd.webp", "WEBP", quality=QUALITY, method=6)
        pixel = ImageOps.fit(image, SIZE, method=Image.Resampling.LANCZOS).quantize(
            colors=COLOURS, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        pixel.save(out / f"{key}-pixel.png", optimize=True)
        shipped.append(key)
    Path(index_path).write_text(json.dumps(sorted(shipped), indent=2) + "\n")
    print(json.dumps({"endings": len(shipped), "skipped": skipped}))


if __name__ == "__main__":
    main(*sys.argv[1:4])
