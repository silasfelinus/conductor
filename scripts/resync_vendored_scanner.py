#!/usr/bin/env python3
"""
resync_vendored_scanner.py — automate the vendored LoRA/model scanner re-sync
that ops/home-server/lora-catalog/PROVENANCE.md still documented as a manual
`cp` + hand-edited note.

Kaizen from lora-ingestion/t-014 (Worker, 2026-09-23): check_vendored_scanner_parity.py
detects drift between the vendored copies in ops/home-server/lora-catalog/ and their
kind_robots originals at scripts/lora-catalog/, but fixing it was still a manual `cp`
plus a hand-written "Re-synced" line in PROVENANCE.md. This script does both steps:
fetch the current kind_robots original via the same GitHub Contents API the parity
checker uses, write it over the local vendored copy, and append a dated "Re-synced"
note to PROVENANCE.md.

It does not commit or push anything -- review the diff
(`git diff ops/home-server/lora-catalog/ ops/home-server/lora-catalog/PROVENANCE.md`)
and commit normally, same as any other change. Run check_vendored_scanner_parity.py
afterward to confirm the drift is gone.

Usage:
  python scripts/resync_vendored_scanner.py --file scan_loras.py
  python scripts/resync_vendored_scanner.py --file scan_loras.py --reason "adds the XYZ field"
  python scripts/resync_vendored_scanner.py --file scan_loras.py --ref <branch-or-sha> --dry-run

Requires: GITHUB_TOKEN (or GH_TOKEN) env var -- kind_robots is private, same as
check_vendored_scanner_parity.py.

Exit codes:
  0 = success -- the vendored copy now matches (a write happened, or it already did)
  2 = could not fetch the original (missing token, network failure, bad response) or
      an unknown --file
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_vendored_scanner_parity import (
    TRACKED_FILES,
    VENDOR_DIR,
    fetch_kind_robots_file,
    github_token,
)

PROVENANCE_PATH = ROOT / "ops" / "home-server" / "lora-catalog" / "PROVENANCE.md"


def resync(
    file_name: str,
    ref: str = "main",
    reason: str | None = None,
    token: str | None = None,
    vendor_dir: Path | None = None,
    provenance_path: Path | None = None,
    fetcher=None,
    dry_run: bool = False,
    today: str | None = None,
) -> dict[str, Any]:
    vendor_dir = vendor_dir or VENDOR_DIR
    provenance_path = provenance_path or PROVENANCE_PATH
    fetcher = fetcher or fetch_kind_robots_file
    token = token if token is not None else github_token()

    if file_name not in TRACKED_FILES:
        return {
            "ok": False,
            "error": f"unknown file {file_name!r}; tracked files are {sorted(TRACKED_FILES)}",
        }

    if not token:
        return {
            "ok": False,
            "error": "GITHUB_TOKEN/GH_TOKEN not set -- kind_robots is private, cannot fetch the original",
        }

    source_relative = TRACKED_FILES[file_name]
    original_bytes, error = fetcher(source_relative, ref, token)
    if error is not None:
        return {"ok": False, "error": error}

    vendored_path = vendor_dir / file_name
    current_bytes = vendored_path.read_bytes() if vendored_path.exists() else None
    if current_bytes == original_bytes:
        return {"ok": True, "changed": False, "file": file_name}

    note_date = today or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    reason_text = f" for {reason}" if reason else ""
    note_line = f"\nRe-synced {note_date} (`{file_name}`){reason_text}. Source: kind_robots@{ref}.\n"

    if not dry_run:
        vendor_dir.mkdir(parents=True, exist_ok=True)
        vendored_path.write_bytes(original_bytes)
        with provenance_path.open("a", encoding="utf-8") as fh:
            fh.write(note_line)

    return {
        "ok": True,
        "changed": True,
        "file": file_name,
        "vendored_path": str(vendored_path),
        "provenance_path": str(provenance_path),
        "note": note_line.strip(),
        "dry_run": dry_run,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--file", required=True, choices=sorted(TRACKED_FILES), help="vendored file to re-sync"
    )
    parser.add_argument("--reason", default=None, help="short reason recorded in the PROVENANCE.md note")
    parser.add_argument("--ref", default="main", help="kind_robots ref to sync from (default: main)")
    parser.add_argument(
        "--dry-run", action="store_true", help="report what would change without writing anything"
    )
    args = parser.parse_args()

    result = resync(file_name=args.file, ref=args.ref, reason=args.reason, dry_run=args.dry_run)

    if not result["ok"]:
        print(f"ERROR: {result['error']}")
        sys.exit(2)

    if not result["changed"]:
        print(f"{args.file} already matches kind_robots@{args.ref} -- nothing to do.")
        sys.exit(0)

    verb = "Would re-sync" if args.dry_run else "Re-synced"
    print(f"{verb} {args.file} from kind_robots@{args.ref}.")
    if not args.dry_run:
        print(f"Updated {result['vendored_path']} and appended a note to {result['provenance_path']}.")
        print(f"Note: {result['note']}")
    sys.exit(0)


if __name__ == "__main__":
    main()
