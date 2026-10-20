#!/usr/bin/env python3
"""Export Ecotone's art-standard renders into kind_robots, one folder per art style.

weird-humboldt t-042. Silas (2026-10-20): every story card, every choice outcome and every ending gets its own
picture, in each of four styles (Z-Image Turbo, Krea 2, Arthemy, Nova Comic). The ledger
(projects/weird-humboldt/art/ART-STANDARD.yaml) renders each subject once per lane, and the lane key is the
style id. This writes every finished render to
``<kind_robots>/public/ecotone/styles/<lane>/<asset>.webp`` (git-tracked; never under /images, which
Alexandria mounts over) and rewrites ``utils/ecotone/artManifest.ts`` from what is on disk, so the game
lists exactly the pictures it ships.

A subject can hold back a lane's render with ``withdrawn: {<lane>: reason}``. The file is removed, and the
picture falls back in the game to the default style's render, then the card's shared art.

Usage:
    python scripts/export_ecotone_art.py LEDGER --kind-robots ../kind_robots      # export new renders
    python scripts/export_ecotone_art.py LEDGER --kind-robots ../kind_robots --manifest-only

Environment: KR_API_TOKEN, KR_BASE_URL (default https://kindrobots.org).
"""

from __future__ import annotations

import argparse
import io
import sys
import urllib.request
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

SIZE = (1344, 768)
STYLES_DIR = Path("public") / "ecotone" / "styles"
MANIFEST = Path("utils") / "ecotone" / "artManifest.ts"
MANIFEST_HEADER = """// Written by conductor scripts/export_ecotone_art.py from the art-standard
// ledger (projects/weird-humboldt/art/ART-STANDARD.yaml): the pictures each
// art style has rendered, by asset key, served from
// /ecotone/styles/<style>/<key>.webp. Do not edit by hand.

import type { EcotoneArtStyle } from './artStyles'
"""


def finished_cells(subjects):
    """(subject, lane, art_image_id) for every DONE render that is not withdrawn."""
    for subject in subjects:
        withdrawn = subject.get("withdrawn") or {}
        for lane, art in (subject.get("art") or {}).items():
            if lane in withdrawn:
                continue
            if (art or {}).get("status") == "DONE" and art.get("art_image_id"):
                yield subject, lane, art["art_image_id"]


def target(kind_robots, lane, asset):
    return Path(kind_robots) / STYLES_DIR / lane / f"{asset}.webp"


def load_image(art_image_id):
    """The render's bytes. Ledger art is private, so its file is fetched with the API token."""
    import consume_art_queue_core as core
    from PIL import Image

    status, resp = core.http_json("GET", f"{core.KR_BASE_URL}/api/art/image/{art_image_id}")
    image_path = ((resp or {}).get("data") or {}).get("imagePath") if status == 200 else None
    if not image_path:
        raise RuntimeError(f"ArtImage {art_image_id}: HTTP {status}, no imagePath")
    request = urllib.request.Request(f"{core.KR_BASE_URL}{image_path}")
    request.add_header("Authorization", f"Bearer {core.KR_API_TOKEN}")
    with urllib.request.urlopen(request, timeout=180) as file_resp:
        return Image.open(io.BytesIO(file_resp.read())).convert("RGB")


def write_render(image_id, path):
    """Fetch one render, fit it to the scene size and save it as WebP."""
    from PIL import Image

    image = load_image(image_id)
    if image.size != SIZE:
        image = image.resize(SIZE, Image.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "WEBP", quality=78, method=6)


def export(subjects, kind_robots, write=write_render):
    """Remove withdrawn renders, write each finished one not yet on disk; returns how many were written."""
    written = 0
    for subject in subjects:
        for lane in subject.get("withdrawn") or {}:
            path = target(kind_robots, lane, subject["asset"])
            if path.exists():
                path.unlink()
                print(f"withdrew {lane} {subject['asset']}", file=sys.stderr)
    for subject, lane, image_id in finished_cells(subjects):
        path = target(kind_robots, lane, subject["asset"])
        if path.exists():
            continue
        write(image_id, path)
        written += 1
    return written


def shipped(kind_robots):
    """{style: [asset, ...]} for every render on disk."""
    root = Path(kind_robots) / STYLES_DIR
    styles = {}
    if root.is_dir():
        for style_dir in sorted(p for p in root.iterdir() if p.is_dir()):
            assets = sorted(
                str(f.relative_to(style_dir).with_suffix("")).replace("\\", "/")
                for f in style_dir.rglob("*.webp")
            )
            if assets:
                styles[style_dir.name] = assets
    return styles


def render_manifest(styles):
    lines = [MANIFEST_HEADER, "export const ECOTONE_STYLE_ART: Partial<", "  Record<EcotoneArtStyle, readonly string[]>"]
    if not styles:
        return "\n".join(lines + ["> = {}", ""])
    lines.append("> = {")
    for style, assets in sorted(styles.items()):
        lines.append(f"  {style}: [")
        lines.extend(f"    '{asset}'," for asset in assets)
        lines.append("  ],")
    lines.append("}")
    return "\n".join(lines) + "\n"


def write_manifest(kind_robots):
    styles = shipped(kind_robots)
    manifest = Path(kind_robots) / MANIFEST
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(render_manifest(styles))
    return styles


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("ledger")
    parser.add_argument("--kind-robots", default="../kind_robots")
    parser.add_argument("--manifest-only", action="store_true", help="rewrite the manifest from disk, fetch nothing")
    args = parser.parse_args(argv)
    subjects = yaml.safe_load(Path(args.ledger).read_text())["subjects"]
    if not args.manifest_only:
        written = export(subjects, args.kind_robots)
        print(f"{written} new renders exported", file=sys.stderr)
    styles = write_manifest(args.kind_robots)
    for style, assets in sorted(styles.items()):
        print(f"{style}: {len(assets)} pictures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
