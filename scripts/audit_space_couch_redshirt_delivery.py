#!/usr/bin/env python3
"""Audit Space Couch redshirt art delivery without accepting unreviewed renders.

Run against a checked-out kind_robots tree. A DONE ArtJob is never evidence
that its original image passed visual curation or reached the public directory.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

KINDS = ("portraits", "secret-powers")
WEBP_MAGIC = b"RIFF"
WEBP_FORMAT = b"WEBP"


def inspect(root: Path) -> dict:
    """Return missing and invalid delivered files, never inferred ArtJob states."""
    findings = {"missing": [], "invalid": [], "delivered": []}
    for kind in KINDS:
        for number in range(1, 101):
            relative = f"public/game-of-captains/redshirts/{kind}/rs-{number:03d}.webp"
            path = root / relative
            if not path.is_file():
                findings["missing"].append(relative)
                continue
            with path.open("rb") as stream:
                header = stream.read(12)
            if (
                len(header) != 12
                or header[:4] != WEBP_MAGIC
                or header[8:12] != WEBP_FORMAT
                or path.stat().st_size <= 12
            ):
                findings["invalid"].append(relative)
                continue
            findings["delivered"].append(relative)
    findings["total"] = 200
    findings["delivered_count"] = len(findings["delivered"])
    findings["complete"] = findings["delivered_count"] == findings["total"]
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind_robots", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.kind_robots.is_dir():
        parser.error("kind_robots must be an existing checkout directory")
    result = inspect(args.kind_robots)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Redshirt WebP files: {result['delivered_count']}/200")
        for label in ("missing", "invalid"):
            for path in result[label]:
                print(f"{label.upper()}: {path}")
    return 0 if result["complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
