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
    python scripts/export_round_art.py LEDGER --sheet /tmp/round.jpg  # review before export
    python scripts/export_round_art.py LEDGER --require-keep  # export only approved artwork

Environment: KR_API_TOKEN, KR_BASE_URL (default https://kindrobots.org).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path, PurePosixPath

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))


def curator_decision(subject):
    """Rejects outrank keep markers, regardless of whether stored on a lane."""
    verdict = str(subject.get("verdict") or "").strip().lower()
    states = {
        (art or {}).get("status")
        for art in (subject.get("art") or {}).values()
    }
    if verdict.startswith("reject") or "REJECTED" in states:
        return "reject"
    if verdict.startswith("keep") or "ACCEPTED" in states:
        return "keep"
    return None


def finished(subject):
    """A render ArtImage ID, including explicitly accepted curator records."""
    for art in (subject.get("art") or {}).values():
        if (art or {}).get("status") in {"DONE", "ACCEPTED"}:
            image_id = art.get("art_image_id")
            if type(image_id) is int and image_id > 0:
                return image_id
    return None

def target(kind_robots, prefix, asset):
    parts = [p for p in (prefix.strip("/"), str(asset).strip("/")) if p]
    for entry in parts:
        path = PurePosixPath(entry)
        if (
            "\\" in entry
            or entry.startswith("/")
            or any(piece in (".", "..") for piece in entry.split("/"))
            or path.is_absolute()
        ):
            raise ValueError(f"Unsafe art asset path: {entry!r}")
    if not parts:
        raise ValueError("Art asset path cannot be empty")
    return Path(kind_robots) / "public" / ("/".join(parts) + ".webp")


def is_valid_webp(path):
    """Check that an on-disk target is a nonempty WebP, not merely a filename."""
    try:
        if not path.is_file() or path.stat().st_size < 20:
            return False
        with path.open("rb") as stream:
            header = stream.read(12)
        return header[:4] == b"RIFF" and header[8:12] == b"WEBP"
    except OSError:
        return False


def audit(subjects, kind_robots, prefix, only=None, require_keep=False):
    """Offline per-render delivery report; never requires the production API token."""
    pattern = re.compile(only) if only else None
    rows = []
    for subject in subjects:
        asset = subject.get("asset")
        if not asset or (pattern and not pattern.search(str(asset))):
            continue
        destination = target(kind_robots, prefix, asset)
        image_id = finished(subject)
        decision = curator_decision(subject)
        if decision == "reject":
            state = "rejected"
        elif image_id is None:
            state = "render-pending"
        elif require_keep and decision != "keep":
            state = "curation-needed"
        elif is_valid_webp(destination):
            state = "shipped"
        elif destination.exists():
            state = "corrupt"
        else:
            state = "export-ready"
        jobs = subject.get("jobs") or {}
        rows.append({
            "asset": str(asset),
            "key": str(subject.get("key") or ""),
            "art_image_id": image_id,
            "art_job_ids": sorted(
                int(job) for job in jobs.values()
                if isinstance(job, int) or (isinstance(job, str) and job.isdigit())
            ),
            "state": state,
            "path": str(destination),
        })

    by_asset = {}
    for row in rows:
        if row["state"] not in ("rejected", "render-pending", "curation-needed"):
            by_asset.setdefault(row["asset"], set()).add(row["art_image_id"])
    collisions = {asset for asset, ids in by_asset.items() if len(ids) > 1}
    for row in rows:
        if row["asset"] in collisions and row["state"] not in (
            "rejected", "render-pending", "curation-needed"
        ):
            row["state"] = "collision"
    counts = {}
    for row in rows:
        counts[row["state"]] = counts.get(row["state"], 0) + 1
    return {"counts": dict(sorted(counts.items())), "total": len(rows), "rows": rows}


def approved_for_export(subject, require_keep=False):
    """Never export a rejected render; strict mode requires an explicit keeper verdict."""
    decision = curator_decision(subject)
    return decision == "keep" if require_keep else decision != "reject"


def plan(subjects, kind_robots, prefix, only=None, force=False, require_keep=False):
    """(subject, image id, destination) for every finished subject that still needs a file."""
    pattern = re.compile(only) if only else None
    out = []
    for subject in subjects:
        asset = subject.get("asset")
        image_id = finished(subject)
        if not asset or not image_id or (pattern and not pattern.search(asset)):
            continue
        if not approved_for_export(subject, require_keep=require_keep):
            continue
        dest = target(kind_robots, prefix, asset)
        if is_valid_webp(dest) and not force:
            continue
        out.append((subject, image_id, dest))
    unique = {}
    for subject, image_id, dest in out:
        previous = unique.get(dest)
        if previous and previous[1] != image_id:
            raise ValueError(
                f"Competing DONE renders for {dest}: ArtImages "
                f"{previous[1]} and {image_id}. Curate the ledger first."
            )
        unique[dest] = (subject, image_id, dest)
    return list(unique.values())


def manifest_entries(kind_robots, root):
    base = Path(kind_robots) / "public" / root.strip("/")
    return sorted(
        str(p.relative_to(base).with_suffix(""))
        for p in base.rglob("*.webp") if is_valid_webp(p)
    )


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
    parser.add_argument(
        "--audit", action="store_true",
        help="offline JSON report of shipped, missing, rejected and corrupt assets",
    )
    parser.add_argument(
        "--require-keep",
        action="store_true",
        help="export only subjects marked with a keep verdict; never export rejects",
    )
    parser.add_argument(
        "--sheet",
        help="make a labelled contact sheet for visual review; do not export any art",
    )
    parser.add_argument("--manifest", help="TypeScript file, relative to kind_robots")
    parser.add_argument("--manifest-root", help="folder under public/ the manifest lists")
    parser.add_argument("--manifest-const", default="ART")
    args = parser.parse_args(argv)

    subjects = []
    for ledger in args.ledgers:
        subjects += yaml.safe_load(Path(ledger).read_text()).get("subjects") or []
    if args.audit:
        print(json.dumps(
            audit(subjects, args.kind_robots, args.prefix, args.only,
                  require_keep=args.require_keep), indent=2, sort_keys=True,
        ))
        return 0
    if args.sheet:
        from export_crystal_street_art import contact_sheet

        candidates = [
            subject for subject in subjects
            if not args.only or re.search(args.only, subject.get("asset") or "")
        ]
        contact_sheet(candidates, args.sheet, thumb=(220, 145))
        return 0

    todo = plan(
        subjects, args.kind_robots, args.prefix, args.only, args.force,
        require_keep=args.require_keep,
    )
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
        if not is_valid_webp(dest):
            raise RuntimeError(f"ArtImage {image_id}: invalid WebP output {dest}")
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
