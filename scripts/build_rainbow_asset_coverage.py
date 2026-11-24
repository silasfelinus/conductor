#!/usr/bin/env python3
"""Rainbow Bullet Hell Space Princess asset coverage ledger (t-042, issue #4146 section 6).

Starts from what actually ships in kind_robots (every file under public/rainbow-princess-*) and joins each to its
provenance: the art ledger subject whose ``asset`` names it (ArtJob, ArtImage, verdict), the CAST-MANIFEST row,
or the Fever Dream review decision for a doodle twin. It also records whether the game's code names the file
(by its published path stem), so a shipped-but-unwired picture shows up.

    python scripts/build_rainbow_asset_coverage.py --kind-robots ../kind_robots          # write the ledger
    python scripts/build_rainbow_asset_coverage.py --kind-robots ../kind_robots --check  # exit 1 on drift

Writes projects/rainbow-bullet-hell-space-princess/ASSET-COVERAGE.md.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects" / "rainbow-bullet-hell-space-princess"
OUT = PROJECT / "ASSET-COVERAGE.md"
PUBLIC_DIRS = ("rainbow-princess-art", "rainbow-princess-audio", "rainbow-princess-video", "rainbow-princess-portraits")
CODE_DIRS = ("utils/arcade", "pages", "components/arcade", "scripts/rainbow-score")


def ledger_assets() -> dict[str, dict]:
    """Published path (no extension, under public/) -> provenance from the art ledgers."""
    found: dict[str, dict] = {}
    for path in sorted((PROJECT / "art").glob("*.yaml")):
        try:
            data = yaml.safe_load(path.read_text())
        except yaml.YAMLError:
            continue
        if not isinstance(data, dict):
            continue
        for subject in data.get("subjects") or []:
            assets = [str(a).strip().strip("/") for a in (subject.get("shipped_as") or [])]
            asset = str(subject.get("asset") or "").strip().strip("/")
            key = str(subject.get("key") or "")
            # The Fever Dream sets name their subjects doodle-<folder>-<name>[-r2]: that is the doodle path.
            match = re.fullmatch(r"doodle-(ships|bosses|enemies|pickups|stages|comms|cutins|portraits)-(.+?)(?:-r\d+)?", key)
            if match:
                assets.append(f"rainbow-princess-art/doodle/{match.group(1)}/{match.group(2)}")
            if asset:
                assets.append(asset)
            if not assets:
                continue
            art = subject.get("art") or {}
            images = [v.get("art_image_id") for v in art.values() if isinstance(v, dict) and v.get("art_image_id")]
            jobs = [j for j in (subject.get("jobs") or {}).values() if j]
            verdict = str(subject.get("verdict") or "").split(":", 1)[0].strip()
            entry = {
                "ledger": path.name,
                "key": subject.get("key"),
                "images": images,
                "jobs": jobs,
                "verdict": verdict,
            }
            # A kept take (or one listed as shipped) wins over a held or rejected one for the same path.
            for each in assets:
                shipped = each in [str(a).strip().strip("/") for a in (subject.get("shipped_as") or [])]
                if each not in found or shipped or (verdict == "keep" and found[each]["verdict"] != "keep"):
                    found[each] = {**entry, "verdict": verdict or ("keep" if shipped else "")}
    return found


def manifest_assets() -> dict[str, dict]:
    """Published path -> provenance from CAST-MANIFEST (pilot portraits, comms, cut-ins, ships)."""
    found: dict[str, dict] = {}
    path = PROJECT / "art" / "CAST-MANIFEST.yaml"
    if not path.exists():
        return found
    for match in re.finditer(
        r"path: public/(\S+?)\.\w+\n(?:.*\n){0,2}?\s+art_image_id: (\d+)\n\s+ledger: (\S+)", path.read_text()
    ):
        found[match.group(1)] = {"ledger": match.group(3), "key": "CAST-MANIFEST", "images": [int(match.group(2))],
                                 "jobs": [], "verdict": "keep"}
    return found


def review_decisions() -> dict[str, str]:
    """Fever Dream review decisions by art path (e.g. enemies/picket)."""
    path = PROJECT / "art" / "DOODLE-SET-1-REVIEW.yaml"
    if not path.exists():
        return {}
    decisions = (yaml.safe_load(path.read_text()) or {}).get("decisions") or {}
    out = {}
    for rel, decision in decisions.items():
        out[str(rel)] = next(iter(decision)) if isinstance(decision, dict) else str(decision)
    return out


def code_text(kind_robots: Path) -> str:
    chunks = []
    for rel in CODE_DIRS:
        base = kind_robots / rel
        if base.exists():
            for file in base.rglob("*"):
                if file.suffix in {".ts", ".vue", ".mjs", ".py"} and file.is_file():
                    chunks.append(file.read_text(errors="ignore"))
    return "\n".join(chunks)


def wired(rel: str, code: str) -> bool:
    """Whether the code names this file: its path stem, its folder-relative stem, or its bare name."""
    stem = rel.rsplit(".", 1)[0]
    parts = stem.split("/")
    art = "/".join(parts[1:])
    art = art.removeprefix("doodle/")
    name = parts[-1]
    folder = parts[-2] if len(parts) > 1 else ""
    if art and art in code:
        return True
    # Paths built from a folder and a key (`stages/${stage}-fore`, `ships/${key}`): the bare key and its folder.
    base = re.split(r"-(?:phase\d|fore|card|far|mid|near|sky|idle|hit|victory|flight|boss)$", name)[0]
    return f"'{base}'" in code and (folder in code or parts[0] in code)


def build(kind_robots: Path) -> tuple[str, dict]:
    ledgers = {**manifest_assets(), **ledger_assets()}
    reviews = review_decisions()
    code = code_text(kind_robots)
    rows = []
    for public in PUBLIC_DIRS:
        base = kind_robots / "public" / public
        if not base.exists():
            continue
        for file in sorted(base.rglob("*")):
            if not file.is_file() or file.suffix not in {".webp", ".png", ".mp3", ".mp4", ".webm"}:
                continue
            rel = file.relative_to(kind_robots / "public").as_posix()
            stem = rel.rsplit(".", 1)[0]
            prov = ledgers.get(stem) or ledgers.get(stem.replace("/doodle/", "/"))
            art_rel = "/".join(stem.split("/")[1:])
            twin_of = art_rel[len("doodle/"):] if art_rel.startswith("doodle/") else None
            review = reviews.get(twin_of or art_rel, "")
            source = (
                f"{prov['ledger']} `{prov['key']}`" if prov
                else f"Fever twin of `{twin_of}` ({review})" if twin_of and review
                else "offline orchestra (scripts/rainbow-score)" if public == "rainbow-princess-audio"
                else "legacy round (provenance in kind_robots code comments)"
            )
            images = ", ".join(str(i) for i in prov["images"]) if prov else ""
            jobs = ", ".join(str(j) for j in prov["jobs"]) if prov else ""
            rows.append({
                "path": rel, "source": source, "images": images, "jobs": jobs,
                "verdict": (prov or {}).get("verdict") or review, "wired": wired(rel, code),
                "kb": round(file.stat().st_size / 1024),
            })
    summary = {
        "files": len(rows),
        "ledger_provenance": sum(not r["source"].startswith("legacy") for r in rows),
        "with_art_image": sum(bool(r["images"]) for r in rows),
        "wired": sum(r["wired"] for r in rows),
    }
    lines = [
        "# Rainbow asset coverage ledger",
        "",
        (
            "Generated by `scripts/build_rainbow_asset_coverage.py` from what ships in kind_robots "
            "`public/rainbow-princess-*` (issue #4146 section 6, t-042). Each file is joined to its art ledger "
            "subject (ArtJob, ArtImage, review verdict), its CAST-MANIFEST row or its Fever Dream review decision, "
            "and checked for a reference in the game's code. Regenerate after an art PR merges; `--check` fails "
            "on drift."
        ),
        "",
        (
            f"**{summary['files']} shipped files** · {summary['ledger_provenance']} traced to a ledger, manifest "
            f"or review · {summary['with_art_image']} with an ArtImage id · {summary['wired']} named by the game's code."
        ),
        "",
        "| Published file | Source | ArtImage | ArtJob | Verdict | Wired | KB |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        lines.append(
            f"| `{r['path']}` | {r['source']} | {r['images']} | {r['jobs']} | {r['verdict']} | "
            f"{'yes' if r['wired'] else 'NO'} | {r['kb']} |"
        )
    return "\n".join(lines) + "\n", summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--kind-robots", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    text, summary = build(args.kind_robots)
    if args.check:
        current = OUT.read_text() if OUT.exists() else ""
        if current != text:
            print("ASSET-COVERAGE.md is out of date; regenerate it", file=sys.stderr)
            return 1
        return 0
    OUT.write_text(text)
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
