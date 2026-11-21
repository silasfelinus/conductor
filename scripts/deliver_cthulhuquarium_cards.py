#!/usr/bin/env python3
"""
deliver_cthulhuquarium_cards.py -- bring finished Cthulhuquarium book-card renders into kind_robots.

The book cards (the species' plates in the Ichthyonomicon, the creatures room and the reveal) are
bundled in kind_robots as assets/images/cthulhuquarium/cthulhuquarium-fish-<slug>.webp, with a
byte-identical copy in public/cthulhuquarium-plates/ for the Playbook, adverts and the monster
PATCH allow-list (cthulhuquarium/t-065). They never had a canon pipeline of their own, so a card
re-render goes through a conductor ledger (art/REDESIGNED-CARDS-1.yaml, t-110) and this script.

For each subject of the ledger whose job is DONE (run `enqueue_art_requests.py LEDGER --status`
first so the ledger carries art_image_id), it fetches the image with the same authenticated path
the art queue uses, saves it at 512x512 like every other card, and writes both copies. It also
saves a contact sheet (old card | new card) to review before committing.

Usage:
    python3 scripts/deliver_cthulhuquarium_cards.py projects/cthulhuquarium/art/REDESIGNED-CARDS-1.yaml \\
        --kind-robots ../kind_robots [--sheet /tmp/cards.png] [--only slug ...]
"""

from __future__ import annotations

import argparse
import base64
import io
import sys
from pathlib import Path

import yaml
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import consume_art_queue_core as core  # noqa: E402

CARD_SIZE = 512


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("ledger")
    parser.add_argument("--kind-robots", required=True)
    parser.add_argument("--sheet")
    parser.add_argument("--only", nargs="*")
    args = parser.parse_args()

    kr = Path(args.kind_robots).resolve()
    root = kr / "assets/images/cthulhuquarium"
    public = kr / "public/cthulhuquarium-plates"
    ledger = yaml.safe_load(Path(args.ledger).read_text())
    pairs: list[tuple[str, Image.Image | None, Image.Image]] = []
    delivered = waiting = 0
    for subject in ledger.get("subjects") or []:
        slug = subject["key"]
        if args.only and slug not in args.only:
            continue
        art = (subject.get("art") or {}).get(subject.get("lane")) or {}
        image_id = art.get("art_image_id")
        if art.get("status") != "DONE" or not image_id:
            waiting += 1
            continue
        data = base64.b64decode(core.fetch_image_b64(image_id))
        image = Image.open(io.BytesIO(data)).convert("RGB")
        image.thumbnail((CARD_SIZE, CARD_SIZE), Image.LANCZOS)
        if image.size != (CARD_SIZE, CARD_SIZE):
            canvas = Image.new("RGB", (CARD_SIZE, CARD_SIZE), (245, 240, 228))
            canvas.paste(image, ((CARD_SIZE - image.width) // 2, (CARD_SIZE - image.height) // 2))
            image = canvas
        name = f"cthulhuquarium-fish-{slug}.webp"
        old_path = root / name
        old = Image.open(old_path).convert("RGB") if old_path.exists() else None
        image.save(root / name, "WEBP", quality=82, method=6)
        public.mkdir(parents=True, exist_ok=True)
        (public / name).write_bytes((root / name).read_bytes())
        pairs.append((slug, old, image))
        delivered += 1
        print(f"  delivered {slug} (ArtImage {image_id})", flush=True)

    if args.sheet and pairs:
        cell, cols = 200, 4
        rows = (len(pairs) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * (2 * cell + 12), rows * (cell + 18)), (18, 24, 26))
        draw = ImageDraw.Draw(sheet)
        for index, (slug, old, new) in enumerate(pairs):
            x, y = (index % cols) * (2 * cell + 12), (index // cols) * (cell + 18)
            for offset, picture in enumerate((old, new)):
                if picture is None:
                    continue
                thumb = picture.copy()
                thumb.thumbnail((cell, cell))
                sheet.paste(thumb, (x + offset * cell, y))
            draw.text((x + 2, y + cell + 2), slug[:34], fill=(230, 220, 190))
        sheet.save(args.sheet)
        print(f"contact sheet: {args.sheet}")
    print(f"delivered {delivered}, still rendering {waiting}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
