#!/usr/bin/env python3
"""Export finished Crystal Street art-round renders into kind_robots.

crystal-street t-003. A round ledger (projects/crystal-street/art/ROUND-*.yaml) names each subject's
runtime path in ``asset`` (``villains/frieda-krueger-poster``, ``companions/raven-happy``,
``locations/library``...). This writes each finished ArtImage to
``<kind_robots>/public/crystal-street/<asset>.webp``, the path the game already looks for before it
falls back to its code-drawn scene (never under /images, which Alexandria mounts over). Files are
downscaled to at most ``--max-edge`` pixels and saved as WebP so the repo stays light.

``--sheet OUT.jpg`` instead writes a labelled contact sheet of every finished render, for review.

Usage:
    python scripts/export_crystal_street_art.py projects/crystal-street/art/ROUND-1.yaml --sheet /tmp/sheet.jpg
    python scripts/export_crystal_street_art.py projects/crystal-street/art/ROUND-1.yaml --kind-robots ../kind_robots

Environment: KR_API_TOKEN, KR_BASE_URL (default https://kindrobots.org).
"""

from __future__ import annotations

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_shifting_lands_cards import finished, load_image  # noqa: E402


def fit(image, max_edge):
    """The image scaled down so its longer edge is at most max_edge."""
    if max(image.size) <= max_edge:
        return image
    scale = max_edge / max(image.size)
    size = (round(image.width * scale), round(image.height * scale))
    return image.resize(size, Image.LANCZOS)


def contact_sheet(subjects, out, thumb=(240, 300)):
    cells = [(s, finished(s)) for s in subjects if finished(s)]
    cols = 8
    rows = max(1, (len(cells) + cols - 1) // cols)
    sheet = Image.new("RGB", (cols * thumb[0], rows * (thumb[1] + 16)), "white")
    draw = ImageDraw.Draw(sheet)
    with ThreadPoolExecutor(max_workers=6) as pool:
        images = list(pool.map(lambda cell: load_image(cell[1]), cells))
    for index, ((subject, _), image) in enumerate(zip(cells, images)):
        image.thumbnail(thumb)
        x, y = (index % cols) * thumb[0], (index // cols) * (thumb[1] + 16)
        sheet.paste(image, (x, y))
        draw.text((x + 3, y + thumb[1] + 2), subject["asset"][:38], fill="black")
    sheet.save(out, quality=70)
    print(f"{len(cells)} renders -> {out}")


def export(subjects, kind_robots, max_edge):
    root = Path(kind_robots) / "public" / "crystal-street"
    todo = [s for s in subjects if finished(s) and s.get("asset")]

    def write(subject):
        dest = root / f"{subject['asset']}.webp"
        dest.parent.mkdir(parents=True, exist_ok=True)
        fit(load_image(finished(subject)), max_edge).save(
            dest, "WEBP", quality=80, method=6
        )
        return subject["asset"]

    with ThreadPoolExecutor(max_workers=6) as pool:
        written = sorted(pool.map(write, todo))
    for asset in written:
        print(asset)
    print(f"{len(written)} renders exported to {root}", file=sys.stderr)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("ledger")
    parser.add_argument(
        "--sheet", help="write a contact sheet of finished renders instead of exporting"
    )
    parser.add_argument("--kind-robots", default="../kind_robots")
    parser.add_argument("--max-edge", type=int, default=1024)
    args = parser.parse_args(argv)
    subjects = yaml.safe_load(Path(args.ledger).read_text())["subjects"]
    if args.sheet:
        contact_sheet(subjects, args.sheet)
    else:
        export(subjects, args.kind_robots, args.max_edge)


if __name__ == "__main__":
    main()
