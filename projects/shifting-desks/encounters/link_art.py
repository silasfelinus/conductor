#!/usr/bin/env python3
"""
link_art.py: link every illustrated slot in the Shifting Desks encounter packs
to the render the game actually shows.

The game never reads art_ref: kind_robots `stationArt()` (utils/shiftingDesks/
rules.ts) derives each image path from ids, so a card can be illustrated on the
live site while its pack still says `design-only`. That is how all 163 slots sat
unlinked after rounds 1-12 delivered (t-015, 2026-10-20 PT). This script makes
the packs agree with the art ledgers in ../art/ROUND-*.yaml:

- every slot maps to the path `stationArt()` builds for it: encounter and review
  cards `cards/<dept>/<id>`, locations `locations/<id>`, the department arrival
  `departments/<dept>`, window desks and applicants `window/<id>`;
- the latest ledger row for that path decides the link: `delivered` with an
  explicit `keep` verdict links it (`verified-repository-art`, art_ref = the
  public path); anything else (requested, rendered, unreviewed, sent back) leaves it
  `design-only` with art_ref null until the re-render lands and is reviewed.

The ledger row, not art.brief, is the record of what rendered: rounds 1-6
expanded each brief with cast and house-style detail before submitting it.

    python projects/shifting-desks/encounters/link_art.py           # report, exit 1 on drift
    python projects/shifting-desks/encounters/link_art.py --write   # apply links
    python projects/shifting-desks/encounters/link_art.py --probe   # also GET each linked image

Exit 0 = packs agree with the ledgers, 1 = drift listed (or a probe failed).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ART_DIR = HERE.parent / "art"
PACKS = ["ORIENTATION-12.json", "RECORDS-12.json", "TOY-DIVISION-12.json", "WELLNESS-12.json", "SUBLEVEL-ZERO-12.json"]
LINKED = "verified-repository-art"
UNLINKED = "design-only"
REPO_PREFIX = "kind_robots public"
MEDIA = "https://media.acrocatranch.com"


def round_number(path: Path) -> int:
    return int(re.search(r"ROUND-(\d+)\.yaml$", path.name).group(1))


def ledger_index(art_dir: Path = ART_DIR) -> dict[str, dict]:
    """Public image path -> the latest round's row for it (later rounds re-render earlier ones)."""
    index: dict[str, dict] = {}
    for path in sorted(art_dir.glob("ROUND-*.yaml"), key=round_number):
        ledger = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for row in ledger.get("subjects") or []:
            target = str(row.get("target_path") or "")
            if target.startswith(REPO_PREFIX):
                index[target[len(REPO_PREFIX):].strip()] = {**row, "_round": path.name}
    return index


def slots(pack: dict):
    """(label, art object, the path kind_robots stationArt() requests for it)."""
    dept = pack["department"]["id"]
    yield f"department {dept}", pack["department"]["arrival_art"], f"/images/shifting-desks/departments/{dept}.webp"
    for loc in pack.get("locations") or []:
        yield f"location {loc['location_id']}", loc["art"], f"/images/shifting-desks/locations/{loc['location_id']}.webp"
    for card in pack.get("encounters") or []:
        yield f"card {card['id']}", card["art"], f"/images/shifting-desks/cards/{dept}/{card['id']}.webp"
    boss = pack["boss"]
    yield f"review {boss['id']}", boss["art"], f"/images/shifting-desks/cards/{dept}/{boss['id']}.webp"
    shift = pack.get("window_shift")
    if shift:
        yield f"window {shift['id']}", shift["art"], f"/images/shifting-desks/window/{shift['id']}.webp"
        for applicant in shift.get("applicants") or []:
            yield f"applicant {applicant['id']}", applicant["art"], f"/images/shifting-desks/window/{applicant['id']}.webp"


def accepted(row: dict | None) -> bool:
    return bool(row) and row.get("status") == "delivered" and str(row.get("verdict") or "").strip().lower().startswith("keep")


def reconcile(pack: dict, index: dict[str, dict], write: bool = False) -> tuple[list[str], list[str]]:
    """Return (problems, linked public paths); with write=True, fix status/art_ref in place."""
    problems: list[str] = []
    linked: list[str] = []
    dept = pack["department"]["id"]
    for label, art, path in slots(pack):
        where = f"{dept}: {label}"
        row = index.get(path)
        if row is None:
            problems.append(f"{where}: no art ledger row renders {path}")
            continue
        want = (LINKED, path) if accepted(row) else (UNLINKED, None)
        if want[0] == LINKED:
            linked.append(path)
        if (art.get("status"), art.get("art_ref")) != want:
            if write:
                art["status"], art["art_ref"] = want
            else:
                state = f"{row['_round']} {row.get('key')} {row.get('status')}"
                if str(row.get("verdict") or "").startswith("redo"):
                    state += ", sent back"
                problems.append(f"{where}: is {art.get('status')}/{art.get('art_ref')}, ledger says {want[0]} ({state})")
    return problems, linked


def probe(path: str) -> str | None:
    try:
        with urllib.request.urlopen(urllib.request.Request(MEDIA + path, method="HEAD"), timeout=20) as res:
            kind = res.headers.get("Content-Type", "")
            return None if res.status == 200 and kind.startswith("image/") else f"{res.status} {kind}"
    except Exception as error:  # noqa: BLE001 - any failure is a finding
        return str(error)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--write", action="store_true", help="apply status/art_ref links to the packs")
    ap.add_argument("--probe", action="store_true", help="GET every linked image from the media host")
    args = ap.parse_args(argv)

    index = ledger_index()
    problems: list[str] = []
    linked: list[str] = []
    total = 0
    for name in PACKS:
        path = HERE / name
        pack = json.loads(path.read_text(encoding="utf-8"))
        total += sum(1 for _ in slots(pack))
        found, done = reconcile(pack, index, write=args.write)
        problems += found
        linked += done
        if args.write:
            path.write_text(json.dumps(pack, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.write:
        problems = [p for p in problems if " is " not in p]
    if args.probe:
        problems += [f"probe {p}: {err}" for p in linked if (err := probe(p))]
    for problem in problems:
        print(problem)
    print(f"art links: {len(linked)}/{total} slots linked to accepted renders, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
