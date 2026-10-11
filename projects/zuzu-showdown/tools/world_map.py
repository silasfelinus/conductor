"""zuzu-showdown t-029: ship the painted wasteland map to the game.

art/T029-WORLD-MAP.yaml holds three seeds of the map; pick the one whose landmarks sit closest to the
game's pins (kind_robots utils/zuzuShowdown/worldMap.ts PLACES), and tune PLACES to it. This writes what
the game's two render styles load, cover-cropped to 16:9:

    GAME_DIR/wasteland-pixel.png   480x270, quantized to a small palette
    GAME_DIR/wasteland-hd.webp     4x that, lossy WebP
    INDEX                          {"shipped": true, ...}, which the game imports (worldMap.json); until
                                   it says shipped, the game draws the map in ink

    python projects/zuzu-showdown/tools/world_map.py SOURCE_DIR GAME_DIR INDEX KEY [LANE]

KEY is the picked ledger key (wasteland-map-2); LANE the render lane to take it from (default
krea2-map: the house lane painted a scene with a figure in it, not a map, 2026-10-11). SOURCE_DIR holds the art as <art_image_id>.png
(method_a_process.py's cache layout); missing ones are downloaded into it.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
LEDGER = HERE.parent / "art" / "T029-WORLD-MAP.yaml"

SIZE = (480, 270)
HD_SCALE = 4
COLOURS = 64
QUALITY = 84


def main(source_dir: str, game_dir: str, index_path: str, key: str, lane: str = "krea2-map") -> None:
    src, out = Path(source_dir), Path(game_dir)
    out.mkdir(parents=True, exist_ok=True)
    ledger = yaml.safe_load(LEDGER.read_text())
    subject = next((s for s in ledger["subjects"] if s["key"] == key), None)
    if subject is None:
        sys.exit(f"no subject {key!r} in {LEDGER.name}")
    art = (subject.get("art") or {}).get(lane) or {}
    if art.get("status") != "DONE" or not art.get("art_image_id"):
        sys.exit(f"{key} [{lane}] has not rendered ({art.get('status')})")
    art_id = art["art_image_id"]
    path = src / f"{art_id}.png"
    if not path.exists():
        sys.path.insert(0, str(HERE))
        import method_a_process

        method_a_process.download(art_id, src)
    image = Image.open(path).convert("RGB")
    w, h = SIZE
    hd = ImageOps.fit(image, (w * HD_SCALE, h * HD_SCALE), method=Image.Resampling.LANCZOS)
    hd.save(out / "wasteland-hd.webp", "WEBP", quality=QUALITY, method=6)
    pixel = ImageOps.fit(image, SIZE, method=Image.Resampling.LANCZOS).quantize(
        colors=COLOURS, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pixel.save(out / "wasteland-pixel.png", optimize=True)
    index = {"shipped": True, "ledger_key": key, "lane": lane, "art_image_id": art_id}
    Path(index_path).write_text(json.dumps(index, indent=2) + "\n")
    print(json.dumps(index))


if __name__ == "__main__":
    main(*sys.argv[1:6])
