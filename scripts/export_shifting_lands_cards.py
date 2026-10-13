#!/usr/bin/env python3
"""Export picked Shifting Lands card paintings from an art round into kind_robots.

zuzu-shifting-lands t-023/t-026. A round ledger (projects/zuzu-shifting-lands/art/ROUND-*.yaml) renders every card
twice; a reviewer marks the keeper with ``verdict: 'keep: ...'``. This writes each keeper's ArtImage to
``<kind_robots>/public/shifting-lands/cards/<card>.webp`` (git-tracked, never under /images, which Alexandria
mounts over) and prints the card ids for ``BESPOKE_CARDS`` in utils/shiftingLands/sceneArt.ts.
A subject carrying an ``outcome`` key (art round 2, t-028: one painting per choice and result) is written
to ``public/shifting-lands/outcomes/<outcome>.webp`` instead and listed for ``BESPOKE_OUTCOMES``.

``--sheet OUT.jpg`` instead writes a labelled contact sheet of every finished render, for review.

Usage:
    python scripts/export_shifting_lands_cards.py LEDGER --sheet /tmp/sheet.jpg [--only land]
    python scripts/export_shifting_lands_cards.py LEDGER --kind-robots ../kind_robots

Environment: KR_API_TOKEN, KR_BASE_URL (default https://kindrobots.org).
"""

from __future__ import annotations

import argparse
import io
import sys
import urllib.request
from pathlib import Path

import yaml
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import consume_art_queue_core as core

CARD_SIZE = (1344, 768)


def finished(subject):
    """The subject's finished ArtImage id, from whichever lane rendered it (house, or ROUND-3's house-i2i)."""
    for art in (subject.get("art") or {}).values():
        if (art or {}).get("status") == "DONE" and art.get("art_image_id"):
            return art["art_image_id"]
    return None


def load_image(art_image_id):
    """The render's bytes. Round art is private, so its file is fetched with the API token."""
    status, resp = core.http_json(
        "GET", f"{core.KR_BASE_URL}/api/art/image/{art_image_id}"
    )
    image_path = (
        ((resp or {}).get("data") or {}).get("imagePath") if status == 200 else None
    )
    if not image_path:
        raise RuntimeError(f"ArtImage {art_image_id}: HTTP {status}, no imagePath")
    request = urllib.request.Request(f"{core.KR_BASE_URL}{image_path}")
    request.add_header("Authorization", f"Bearer {core.KR_API_TOKEN}")
    with urllib.request.urlopen(request, timeout=180) as file_resp:
        return Image.open(io.BytesIO(file_resp.read())).convert("RGB")


def contact_sheet(subjects, out, thumb=(448, 256)):
    cells = [(s, finished(s)) for s in subjects if finished(s)]
    cols = 4
    rows = max(1, (len(cells) + cols - 1) // cols)
    sheet = Image.new("RGB", (cols * thumb[0], rows * (thumb[1] + 18)), "white")
    draw = ImageDraw.Draw(sheet)
    for index, (subject, image_id) in enumerate(cells):
        image = load_image(image_id)
        image.thumbnail(thumb)
        x, y = (index % cols) * thumb[0], (index // cols) * (thumb[1] + 18)
        sheet.paste(image, (x, y))
        draw.text((x + 3, y + thumb[1] + 3), subject["key"][4:60], fill="black")
    sheet.save(out, quality=72)
    print(f"{len(cells)} renders -> {out}")


def export_target(subject):
    """(folder, name) for a keeper: outcome plates go to outcomes/, card faces to cards/."""
    if subject.get("outcome"):
        return "outcomes", subject["outcome"]
    return "cards", subject["card"]


def export(subjects, kind_robots):
    root = Path(kind_robots) / "public" / "shifting-lands"
    written = {}
    for subject in subjects:
        if not str(subject.get("verdict") or "").startswith("keep") or not finished(
            subject
        ):
            continue
        folder, name = export_target(subject)
        dest = root / folder
        dest.mkdir(parents=True, exist_ok=True)
        image = load_image(finished(subject))
        if image.size != CARD_SIZE:
            image = image.resize(CARD_SIZE, Image.LANCZOS)
        image.save(dest / f"{name}.webp", "WEBP", quality=80, method=6)
        written.setdefault(folder, set()).add(name)
    for folder, names in sorted(written.items()):
        for name in sorted(names):
            print(name)
        print(f"{len(names)} {folder} exported to {root / folder}", file=sys.stderr)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("ledger")
    parser.add_argument(
        "--sheet", help="write a contact sheet of finished renders instead of exporting"
    )
    parser.add_argument(
        "--only",
        help="limit to one land (homestead, dustwater, tablelands, cave, verge)",
    )
    parser.add_argument("--kind-robots", default="../kind_robots")
    args = parser.parse_args(argv)
    subjects = yaml.safe_load(Path(args.ledger).read_text())["subjects"]
    if args.only:
        subjects = [s for s in subjects if s.get("land") == args.only]
    if args.sheet:
        contact_sheet(subjects, args.sheet)
    else:
        export(subjects, args.kind_robots)


if __name__ == "__main__":
    main()
