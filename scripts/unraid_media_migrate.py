#!/usr/bin/env python3
"""
unraid_media_migrate.py — RUN THIS ON THE SELF-HOSTED MEDIA BOX (Unraid).

Applies the image-file moves recorded by scripts/dream_slug_image_cleanup.py
(projects/dream-cycle/media-migration-manifest.json) to the real media store,
then regenerates collections.json + gallery.json so the CDN can still resolve
folders. The DB imagePath values were already PATCHed to the NEW paths by the
cleanup script; this makes the files sit where those paths now point.

Why here and not from CI: the image tree lives on the Unraid share
(/mnt/user/pc/kindrobots/images, served via media.acrocatranch.com). Vercel and
the conductor CI box cannot write to it — see kind_robots/docs/self-hosted-media.md.

Safe by construction:
  * DRY-RUN by default — prints every move; pass --apply to actually move.
  * Idempotent — if a file is already at its new path (and the old one is gone),
    the move is counted done and skipped. Never overwrites an existing dest.
  * Never deletes. Orphaned duplicate-card files (from the merged-away dreams)
    are only REPORTED, for you to remove by hand if you want.

Usage (on the box, with the manifest copied over or the repo checked out):
  python3 unraid_media_migrate.py --manifest media-migration-manifest.json
  python3 unraid_media_migrate.py --manifest media-migration-manifest.json --apply
  KR_IMAGES_ROOT=/mnt/z/kindrobots/images python3 unraid_media_migrate.py --apply
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

IMAGE_EXTS = {".webp", ".png", ".jpg", ".jpeg"}
# The public URL prefix that maps to the media root. imagePath
# "/images/dreams/x.webp" is the file "<root>/dreams/x.webp".
URL_PREFIX = "/images/"
DEFAULT_ROOT = os.environ.get("KR_IMAGES_ROOT", "/mnt/user/pc/kindrobots/images")


def rel(url_path: str) -> str:
    p = url_path
    if p.startswith(URL_PREFIX):
        p = p[len(URL_PREFIX):]
    return p.lstrip("/")


def apply_moves(moves: list[dict], root: Path, apply: bool) -> dict:
    stats = {"moved": 0, "already": 0, "missing": 0, "conflict": 0, "orphan": 0}
    touched_dirs: set[Path] = set()
    for m in moves:
        kind, old, new = m.get("kind"), m.get("old"), m.get("new")
        if not old:
            continue
        src = root / rel(old)
        if not new:  # orphan (a merged-away duplicate's card) — report only
            if src.exists():
                print(f"  ORPHAN (leftover, not deleting): {src}")
                stats["orphan"] += 1
            continue
        dst = root / rel(new)
        if dst.exists() and not src.exists():
            stats["already"] += 1
            continue
        if not src.exists():
            print(f"  MISSING source, cannot move: {src}  (-> {dst})")
            stats["missing"] += 1
            continue
        if dst.exists():
            print(f"  CONFLICT dest exists, skipping: {dst}  (from {src})")
            stats["conflict"] += 1
            continue
        print(f"  {'MOVE ' if apply else '[dry] '}{src}  ->  {dst}")
        if apply:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
        touched_dirs.add(dst.parent)
        touched_dirs.add(src.parent)
        stats["moved"] += 1
    return stats


def has_images(d: Path) -> bool:
    return d.is_dir() and any(
        f.is_file() and f.suffix.lower() in IMAGE_EXTS for f in d.iterdir())


def regen_gallery(folder: Path, apply: bool) -> None:
    if not folder.exists():
        return
    names = sorted(f.name for f in folder.iterdir()
                   if f.is_file() and f.suffix.lower() in IMAGE_EXTS)
    if not names:
        return
    if apply:
        (folder / "gallery.json").write_text(json.dumps(names) + "\n")


def regen_collections(root: Path, apply: bool) -> dict:
    """collections.json: slug -> path relative to images root. Precedence nested >
    flat > artcollections, matching scripts/distribute_images.py exactly."""
    if not root.exists():
        return {}
    index: dict[str, str] = {}
    legacy = root / "artcollections"
    if legacy.is_dir():
        for d in sorted(legacy.iterdir()):
            if has_images(d):
                index[d.name] = f"artcollections/{d.name}"
    for d in sorted(root.iterdir()):
        if d.is_dir() and d.name != "artcollections" and has_images(d):
            index[d.name] = d.name
    for ctx in sorted(root.iterdir()):
        if not ctx.is_dir() or ctx.name == "artcollections":
            continue
        for d in sorted(ctx.iterdir()):
            if has_images(d):
                index[d.name] = f"{ctx.name}/{d.name}"
    if apply:
        (root / "collections.json").write_text(
            json.dumps(index, indent=2, sort_keys=True) + "\n")
    return index


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="media-migration-manifest.json")
    ap.add_argument("--root", default=DEFAULT_ROOT,
                    help=f"media images root (default {DEFAULT_ROOT}, or $KR_IMAGES_ROOT)")
    ap.add_argument("--apply", action="store_true", help="actually move (default: dry-run)")
    args = ap.parse_args()

    root = Path(args.root)
    man = json.loads(Path(args.manifest).read_text())
    moves = man.get("moves", [])
    print(f"{'APPLY' if args.apply else 'DRY-RUN'} · root={root} · {len(moves)} move(s)")
    if not root.exists():
        print(f"!! images root {root} not found — set --root or $KR_IMAGES_ROOT to the "
              f"Unraid share (e.g. /mnt/z/kindrobots/images).", file=sys.stderr)
        if args.apply:
            return 2

    stats = apply_moves(moves, root, args.apply)

    # regenerate manifests for every folder that gained files, plus the index
    print("Regenerating gallery.json / collections.json ...")
    for d in sorted({root / rel(m["new"]) for m in moves if m.get("new")}):
        regen_gallery(d.parent, args.apply)
    idx = regen_collections(root, args.apply)
    print(f"  collections.json: {len(idx)} folder(s){'' if args.apply else ' [dry]'}")
    print(f"\n{stats}")
    if not args.apply:
        print("Dry-run only. Re-run with --apply to move the files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
