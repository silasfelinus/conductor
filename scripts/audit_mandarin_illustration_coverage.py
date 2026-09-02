#!/usr/bin/env python3
"""Audit actual Krea 2 (v2) illustration coverage for the Mandarin Tutor core catalog.

mandarin-tutor/t-010's goal is "reach and audit" coverage: t-005/queue_mandarin_tutor_art.py
and submit_mandarin_tutor_artjobs.py already make sure every catalog entry that needs a v2
illustration has a durable ArtJob queued (the "reach" half). This script is the "audit" half
-- it answers, independent of ArtJob/queue bookkeeping, whether the *rendered image actually
exists* on the media origin for every `strategy: illustrate` manifest entry.

Why not trust ArtJob status instead? ArtJob rows can drift from reality in both directions
(duplicate enqueues, a relay that writes the file but the status update is lost, a later
manual re-render). The only ground truth for "is this card illustrated" is the media origin
itself -- so this probes `https://media.acrocatranch.com/<imageUrl>` directly with HEAD,
exactly like drain_failed_art_backlog.py's target_media_state, and reports present/absent/
unknown per entry. `glyph-only` entries are excluded -- they intentionally have no image.

Usage:
    python scripts/audit_mandarin_illustration_coverage.py [--manifest-file PATH] [--workers N]

Requires no token -- the media origin serves static files unauthenticated. Uses the local
manifest snapshot (projects/mandarin-tutor/art-manifest.json) by default so this never
depends on kindrobots.org being reachable; pass --fetch to refresh it from the live
/api/mandarin/art-manifest first (same fetch queue_mandarin_tutor_art.py uses).
"""

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT = ROOT / "projects" / "mandarin-tutor" / "art-manifest.json"
TIMEOUT_SECONDS = 8

sys.path.insert(0, str(ROOT / "scripts"))
from queue_mandarin_tutor_art import (  # noqa: E402
    fetch_manifest,
    probe_media_state,
    validate_manifest,
)


def load_entries(manifest_file: str | None, do_fetch: bool) -> list[dict[str, Any]]:
    if do_fetch:
        manifest = fetch_manifest()
    elif manifest_file:
        payload = json.loads(Path(manifest_file).read_text(encoding="utf-8"))
        manifest = payload.get("data") if isinstance(payload, dict) and "data" in payload else payload
    else:
        manifest = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    return validate_manifest(manifest)


def probe(entry: dict[str, Any]) -> tuple[dict[str, Any], str]:
    return entry, probe_media_state(entry, timeout=TIMEOUT_SECONDS)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--manifest-file", help="Audit a saved manifest instead of the committed snapshot")
    parser.add_argument("--fetch", action="store_true", help="Refresh from the live /api/mandarin/art-manifest first")
    parser.add_argument("--workers", type=int, default=12, help="Concurrent HEAD probes (default 12)")
    parser.add_argument("--list-missing", action="store_true", help="Print every absent/unknown cardKey")
    args = parser.parse_args()

    entries = load_entries(args.manifest_file, args.fetch)
    illustrated = [e for e in entries if e.get("strategy") == "illustrate"]
    glyph_only = len(entries) - len(illustrated)

    results: dict[str, list[dict[str, Any]]] = {"present": [], "absent": [], "unknown": []}
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(probe, e) for e in illustrated]
        for future in as_completed(futures):
            entry, state = future.result()
            results[state].append(entry)

    total = len(illustrated)
    present = len(results["present"])
    absent = len(results["absent"])
    unknown = len(results["unknown"])
    pct = (present / total * 100) if total else 100.0

    print(f"Mandarin Tutor v2 illustration coverage: {present}/{total} rendered ({pct:.1f}%)")
    print(f"  present: {present}")
    print(f"  absent:  {absent}")
    print(f"  unknown: {unknown} (media origin unreachable/ambiguous -- not counted as missing)")
    print(f"  glyph-only (excluded, no image expected): {glyph_only}")

    if args.list_missing:
        for state in ("absent", "unknown"):
            for entry in sorted(results[state], key=lambda e: e.get("cardKey", "")):
                print(f"  [{state}] {entry.get('cardKey')}  {entry.get('imageUrl')}")

    return 0 if absent == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
