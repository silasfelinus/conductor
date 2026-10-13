"""zuzu-showdown t-008: ship the portraits to the game.

art/T008-PORTRAITS.yaml holds four Kontext portraits per fighter on a plain dark ground: the select-screen
bust (square), the VS-screen half-body slam, the victory portrait and the beaten portrait (tall). This
turns every rendered one into what the game's two render styles load, sized for where the screens draw
them (screens.ts):

    GAME_DIR/<file>-<kind>-pixel.png   game resolution, quantized to a small palette (sits with the sprites)
    GAME_DIR/<file>-<kind>-hd.webp     4x that, lossy WebP
    GAME_DIR/<file>-<kind>.json        metadata: the ArtImage, the ledger key, whether it was mirrored
    INDEX                              which portraits exist, for the game to import (portraits.json)

<file> is the rig's short name (coyote for coyote-vagrant, as sprites.ts spriteFile). A portrait whose
art has not rendered, or was rejected and is being rerolled, is left out and the game draws the fighter's
sprite in its place. `display_mirror` subjects (the Coyote's knife drawn on the wrong wrist) are flipped.

    python projects/zuzu-showdown/tools/portraits.py SOURCE_DIR GAME_DIR INDEX

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
LEDGER = HERE.parent / "art" / "T008-PORTRAITS.yaml"

# Game pixels per portrait kind (screens.ts): the bust fills a select card; the tall ones stand as tall
# as the VS screen's fighters.
SIZES = {"bust": (50, 50), "vs": (104, 152), "victory": (104, 152), "beaten": (104, 152)}
HD_SCALE = 4
COLOURS = 40
QUALITY = 82

# Ledger entity -> the rig's file name (sprites.ts RIG_NAMES).
FILES = {
    "zuzu": "zuzu",
    "coyote-vagrant": "coyote",
    "the-abbess": "abbess",
    "the-siblings": "siblings",
    "storm-crow": "crow",
    "river-croc": "croc",
    "hyena-matriarch": "hyena",
    "old-komodo": "komodo",
    "swamp-witch": "witch",
    "jeffery-mittens": "mittens",
}


def fit(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Cover-crop to the target aspect (keeping the top, where the face is) and resize."""
    return ImageOps.fit(image, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.2))


def main(source_dir: str, game_dir: str, index_path: str) -> None:
    src, out = Path(source_dir), Path(game_dir)
    out.mkdir(parents=True, exist_ok=True)
    ledger = yaml.safe_load(LEDGER.read_text())
    index: dict[str, dict[str, dict]] = {}
    skipped = []
    for subject in ledger["subjects"]:
        art = (subject.get("art") or {}).get("kontext-portraits") or {}
        entity, kind = subject["entity"], subject["key"].rsplit("-", 1)[1]
        if art.get("status") != "DONE" or not art.get("art_image_id"):
            skipped.append(subject["key"])
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
        w, h = SIZES[kind]
        name = f"{FILES[entity]}-{kind}"
        hd = fit(image, (w * HD_SCALE, h * HD_SCALE))
        hd.save(out / f"{name}-hd.webp", "WEBP", quality=QUALITY, method=6)
        pixel = fit(image, (w, h)).quantize(colors=COLOURS, method=Image.Quantize.MEDIANCUT,
                                            dither=Image.Dither.NONE)
        pixel.save(out / f"{name}-pixel.png", optimize=True)
        meta = {"fighter": entity, "kind": kind, "w": w, "h": h, "hd_scale": HD_SCALE,
                "art_image_id": art_id, "ledger_key": subject["key"],
                "mirrored": bool(subject.get("display_mirror"))}
        (out / f"{name}.json").write_text(json.dumps(meta, indent=2) + "\n")
        index.setdefault(entity, {})[kind] = {"file": name, "w": w, "h": h}
    Path(index_path).write_text(json.dumps(index, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"portraits": sum(len(v) for v in index.values()), "skipped": skipped}))


if __name__ == "__main__":
    main(*sys.argv[1:4])
