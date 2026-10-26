#!/usr/bin/env python3
"""Export finished art-round renders into kind_robots and rewrite the game's art manifest.

WHY THIS EXISTS. Round ledgers (projects/<project>/art/*.yaml) record each render's ArtImage id,
but a game only shows a picture once the file ships under kind_robots ``public/`` and the game's
manifest lists it. Emperor of Dust's secret followers F021-F025, This Means Warp's crew portraits
and Capes & Tassels' front-end art all sat DONE in their ledgers and invisible in play
(2026-10-26: the Playbook Forge ledger reads them as "rendered but not wired"). This is the one
exporter for any game whose ledger names the runtime path in ``asset``; Ecotone keeps its own
per-style exporter (export_ecotone_art.py).

Each finished subject is written to ``<kind_robots>/public/<prefix>/<asset>.webp`` (``--prefix``
may be empty when the asset already starts with the game's folder). Existing files are kept
unless ``--force``. With ``--manifest`` the named TypeScript array is rebuilt from every .webp
under ``public/<manifest-root>``, so the game lists exactly the files it ships: an existing
``export const NAME ... = [ ... ]`` block is replaced in place (the rest of the file is kept),
otherwise a new file is written.

Usage:
    python scripts/export_round_art.py projects/emperor-of-dust/art/SECRET-FOLLOWERS-ROUND-1.yaml \\
        --kind-robots ../kind_robots --prefix emperor-of-dust --only 'followers/F02[1-5]/' \\
        --manifest utils/emperorOfDust/fortress/castArt.ts --manifest-root emperor-of-dust/cast \\
        --manifest-const CAST_ART
    python scripts/export_round_art.py projects/game-of-captains/art/*.yaml --kind-robots ../kind_robots \\
        --manifest utils/gameOfCaptains/artManifest.ts --manifest-root game-of-captains \\
        --manifest-const WARP_ART
    python scripts/export_round_art.py LEDGER --dry-run      # list what would be written

Environment: KR_API_TOKEN, KR_BASE_URL (default https://kindrobots.org).
"""

from __future__ import annotations

import argparse
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))


def finished(subject):
    """The subject's finished ArtImage id from whichever lane rendered it, or None."""
    for art in (subject.get("art") or {}).values():
        if (art or {}).get("status") == "DONE" and art.get("art_image_id"):
            return art["art_image_id"]
    return None


def target(kind_robots, prefix, asset):
    parts = [p for p in (prefix.strip("/"), asset.strip("/")) if p]
    return Path(kind_robots) / "public" / ("/".join(parts) + ".webp")


def plan(subjects, kind_robots, prefix, only=None, force=False):
    """(subject, image id, destination) for every finished subject that still needs a file."""
    pattern = re.compile(only) if only else None
    out = []
    for subject in subjects:
        asset = subject.get("asset")
        image_id = finished(subject)
        if not asset or not image_id or (pattern and not pattern.search(asset)):
            continue
        dest = target(kind_robots, prefix, asset)
        if dest.exists() and not force:
            continue
        out.append((subject, image_id, dest))
    return out


def manifest_entries(kind_robots, root):
    base = Path(kind_robots) / "public" / root.strip("/")
    return sorted(str(p.relative_to(base).with_suffix("")) for p in base.rglob("*.webp"))


def render_array(name, entries):
    lines = [f"export const {name}: readonly string[] = ["]
    lines += [f"  '{entry}'," for entry in entries]
    lines.append("]")
    return "\n".join(lines)


def write_manifest(path, name, entries, header):
    """Replace NAME's array in place when the file has one, else write a fresh manifest file."""
    block = render_array(name, entries)
    if path.exists():
        text = path.read_text()
        pattern = re.compile(
            rf"export const {re.escape(name)}\s*:[^=]*=\s*\[.*?\n\]", re.DOTALL
        )
        if pattern.search(text):
            path.write_text(pattern.sub(lambda _m: block, text, count=1))
            return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{header.rstrip()}\n\n{block}\n")


def fit(image, max_edge):
    from PIL import Image

    if max(image.size) <= max_edge:
        return image
    scale = max_edge / max(image.size)
    return image.resize(
        (round(image.width * scale), round(image.height * scale)), Image.LANCZOS
    )


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("ledgers", nargs="+")
    parser.add_argument("--kind-robots", default="../kind_robots")
    parser.add_argument("--prefix", default="", help="folder under public/ the assets live in")
    parser.add_argument("--only", help="regex an asset must match to export")
    parser.add_argument("--max-edge", type=int, default=1344)
    parser.add_argument("--force", action="store_true", help="overwrite files that exist")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--manifest", help="TypeScript file, relative to kind_robots")
    parser.add_argument("--manifest-root", help="folder under public/ the manifest lists")
    parser.add_argument("--manifest-const", default="ART")
    args = parser.parse_args(argv)

    subjects = []
    for ledger in args.ledgers:
        subjects += yaml.safe_load(Path(ledger).read_text()).get("subjects") or []
    todo = plan(subjects, args.kind_robots, args.prefix, args.only, args.force)
    if args.dry_run:
        for subject, image_id, dest in todo:
            print(f"{image_id}\t{dest}")
        print(f"{len(todo)} renders would be exported", file=sys.stderr)
        return 0

    from export_shifting_lands_cards import load_image

    def write(item):
        _subject, image_id, dest = item
        dest.parent.mkdir(parents=True, exist_ok=True)
        fit(load_image(image_id), args.max_edge).save(dest, "WEBP", quality=82, method=6)
        return str(dest)

    with ThreadPoolExecutor(max_workers=6) as pool:
        for written in sorted(pool.map(write, todo)):
            print(written)
    print(f"{len(todo)} renders exported", file=sys.stderr)

    if args.manifest:
        if not args.manifest_root:
            parser.error("--manifest needs --manifest-root")
        entries = manifest_entries(args.kind_robots, args.manifest_root)
        header = (
            "// Written by conductor scripts/export_round_art.py: every render shipped under\n"
            f"// public/{args.manifest_root.strip('/')}/<entry>.webp. Re-run the export; do not edit by hand."
        )
        write_manifest(
            Path(args.kind_robots) / args.manifest, args.manifest_const, entries, header
        )
        print(f"{args.manifest}: {len(entries)} entries", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
