#!/usr/bin/env python3
"""
media_migrate.py — move the dream/facet image files to match the DB.

Run this from ANY machine on Silas's network that can WRITE to the kindrobots
images share — you do NOT have to be on the Unraid box. The images live on the
Unraid NAS (served via media.acrocatranch.com) but are reachable as a share:

  * from the conductor box (Windows):   Z:\kindrobots\images
  * from the conductor box (WSL/Linux): /mnt/z/kindrobots/images   <- default
  * on the Unraid box itself:           /mnt/user/pc/kindrobots/images

Point --root (or $KR_IMAGES_ROOT) at whichever applies. See
kind_robots/docs/self-hosted-media.md. Vercel and the conductor CI box cannot
write to the share, which is why this step is manual.

It applies the moves recorded by scripts/dream_slug_image_cleanup.py
(projects/dream-cycle/media-migration-manifest.json), then regenerates
collections.json + gallery.json so the CDN can still resolve folders. The DB
imagePath values were already PATCHed to the NEW paths by the cleanup script;
this makes the files sit where those paths now point.

Safe by construction:
  * DRY-RUN by default — prints every move; pass --apply to actually move.
  * Idempotent — if a file is already at its new path (and the old one is gone),
    the move is counted done and skipped. Never overwrites an existing dest.
  * Never deletes. Orphaned duplicate-card files (from the merged-away dreams)
    are only REPORTED, for you to remove by hand if you want.

Usage (from the conductor checkout, over the Z: share):
  python3 scripts/media_migrate.py                                    # dry-run
  python3 scripts/media_migrate.py --apply                            # move (WSL default root)
  python3 scripts/media_migrate.py --root Z:\\kindrobots\\images --apply   # Windows
  KR_IMAGES_ROOT=/mnt/z/kindrobots/images python3 scripts/media_migrate.py --apply

Or copied standalone onto the media box (script + manifest in one folder):
  python3 media_migrate.py --apply
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
# Find the manifest whether the script runs inside the repo OR was copied out
# standalone next to the manifest (e.g. dropped straight onto the media box).
_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parent
_MANIFEST_CANDIDATES = [
    _REPO_ROOT / "projects" / "dream-cycle" / "media-migration-manifest.json",
    _SCRIPT_DIR / "media-migration-manifest.json",   # copied beside the script
    Path.cwd() / "media-migration-manifest.json",     # or into the CWD
]
DEFAULT_MANIFEST = next(
    (c for c in _MANIFEST_CANDIDATES if c.exists()), _MANIFEST_CANDIDATES[0])
# The kindrobots images share as seen from the conductor box under WSL. Override
# with --root (Windows: Z:\kindrobots\images) or $KR_IMAGES_ROOT (Unraid-local:
# /mnt/user/pc/kindrobots/images).
_ROOT_CANDIDATES = [
    "/mnt/z/kindrobots/images",         # conductor box, WSL mount of Z:
    "Z:/kindrobots/images",             # conductor box, native Windows
    "/mnt/user/pc/kindrobots/images",   # on the Unraid box itself
]
DEFAULT_ROOT = os.environ.get(
    "KR_IMAGES_ROOT",
    next((c for c in _ROOT_CANDIDATES if Path(c).exists()), _ROOT_CANDIDATES[0]),
)


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

        # Non-destructive copy (kind "copy"): place a pitch-sheet card from
        # /images/sheets/<slug>.webp as the dream folder's canonical
        # <slug>-card.webp without removing the original. Runs before the folder
        # moves in the manifest so this real card wins over the ensure_dream_card
        # fallback. Skips if the card is already there.
        if kind == "copy":
            if dst.exists():
                stats["already"] += 1
                continue
            print(f"  {'COPY ' if apply else '[dry] COPY '}{src}  ->  {dst}")
            if apply:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(src), str(dst))
            stats["moved"] += 1
            continue

        # Whole-folder relocation (kind "folder", or the source is a directory):
        # a misplaced collection folder like /images/the-lantern-greenhouse-collection
        # -> /images/dreams/lantern-greenhouse. Merge into an existing dest folder
        # rather than fail, and never overwrite a file already there.
        if kind == "folder" or src.is_dir():
            print(f"  {'FOLDER' if apply else '[dry] FOLDER'} {src}  ->  {dst}")
            if apply:
                dst.mkdir(parents=True, exist_ok=True)
                for item in list(src.iterdir()):
                    target = dst / item.name
                    if target.exists():
                        print(f"    keep existing, skip: {target.name}")
                        continue
                    shutil.move(str(item), str(target))
                # remove the now-empty (or manifest/leftover-only) source dir
                remaining = [p for p in src.iterdir()]
                if not remaining:
                    src.rmdir()
                else:
                    print(f"    left {len(remaining)} item(s) in {src} (name clash)")
                # For a dream collection, the DB PitchSheet points at
                # <slug>/<slug>-card.webp. The folder's files are arbitrarily
                # named, so guarantee that canonical card exists by copying the
                # best candidate image (keeps the original too).
                if dst.parent.name == "dreams":
                    ensure_dream_card(dst)
            touched_dirs.add(dst)
            stats["moved"] += 1
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


_CARD_PREFERENCE = ("card", "hero", "key", "cover", "title", "main", "dream")


def ensure_dream_card(folder: Path) -> None:
    """Make sure <folder>/<slug>-card.webp exists (the DB PitchSheet path) by
    copying the most card-like image in the folder. No-op if it already exists
    or the folder has no images."""
    slug = folder.name
    target = folder / f"{slug}-card.webp"
    if target.exists():
        return
    imgs = sorted(f for f in folder.iterdir()
                  if f.is_file() and f.suffix.lower() in IMAGE_EXTS)
    if not imgs:
        return
    best = None
    for pref in _CARD_PREFERENCE:
        best = next((f for f in imgs if pref in f.stem.lower()), None)
        if best:
            break
    best = best or imgs[0]
    shutil.copy2(str(best), str(target))
    print(f"    card: copied {best.name} -> {target.name}")


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
    ap.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    ap.add_argument("--root", default=DEFAULT_ROOT,
                    help=f"media images root (default {DEFAULT_ROOT}, or $KR_IMAGES_ROOT)")
    ap.add_argument("--apply", action="store_true", help="actually move (default: dry-run)")
    args = ap.parse_args()

    root = Path(args.root)
    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"!! manifest not found: {manifest_path}\n"
              f"   Pass --manifest, or drop media-migration-manifest.json next to "
              f"this script.", file=sys.stderr)
        return 2
    man = json.loads(manifest_path.read_text())
    moves = man.get("moves", [])
    print(f"{'APPLY' if args.apply else 'DRY-RUN'} · root={root} · {len(moves)} move(s)")
    if not root.exists():
        print(f"!! images root {root} not found. Point --root or $KR_IMAGES_ROOT at the "
              f"kindrobots images share — one of:", file=sys.stderr)
        for c in _ROOT_CANDIDATES:
            print(f"     {c}", file=sys.stderr)
        if args.apply:
            return 2

    stats = apply_moves(moves, root, args.apply)

    # Regenerate manifests only on --apply. The dry-run skips this: walking the
    # whole 2000+ file tree to preview collections.json is slow over a network
    # mount and changes nothing. For a folder move the new path IS the folder;
    # for a file move it's the file, so regen its parent.
    if args.apply:
        print("Regenerating gallery.json / collections.json ...")
        regen_targets = set()
        for m in moves:
            if not m.get("new"):
                continue
            d = root / rel(m["new"])
            regen_targets.add(d if (m.get("kind") == "folder" or d.is_dir()) else d.parent)
        for d in sorted(regen_targets):
            regen_gallery(d, True)
        idx = regen_collections(root, True)
        print(f"  collections.json: {len(idx)} folder(s)")

    print(f"\n{stats}")
    if not args.apply:
        print("Dry-run only (manifest + collections.json regen skipped). "
              "Re-run with --apply to move the files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
