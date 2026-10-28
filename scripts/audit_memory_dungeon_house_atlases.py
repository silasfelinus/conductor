#!/usr/bin/env python3
"""Validate the two dedicated House atlas requests and their durable ArtJob receipts.

This is a submission check, not proof of a completed render or accessible image.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "projects/memory-dungeon/art/HOUSE-ATLAS-REQUESTS.yaml"
EXPECTED = {
    "memory-dungeon-saturate-house-atlas-original-6x6":
        "public/images/memory-dungeon/house/maps/house-atlas.webp",
    "memory-dungeon-saturate-house-atlas-mirrored-6x6":
        "public/images/memory-dungeon/dark-briar/house/maps/house-atlas.webp",
}


def validate(data: dict, require_jobs: bool = False) -> dict[str, int | None]:
    rows = data.get("requests") or []
    if not isinstance(rows, list) or len(rows) != len(EXPECTED):
        raise ValueError("House atlas ledger must contain exactly two requests")
    receipts: dict[str, int | None] = {}
    for row in rows:
        if not isinstance(row, dict) or row.get("id") not in EXPECTED:
            raise ValueError("Unknown House atlas request")
        key = row["id"]
        if key in receipts or row.get("image_path") != EXPECTED[key]:
            raise ValueError(f"Duplicate or incorrect House atlas destination: {key}")
        if (row.get("target_repo") != "silasfelinus/kind_robots"
                or row.get("project_slug") != "memory-dungeon"
                or row.get("engine") != "krea2"
                or row.get("size") != "1024x1024"
                or len(str(row.get("prompt") or "")) < 100):
            raise ValueError(f"Incomplete House atlas production contract: {key}")
        raw_id = row.get("last_art_job_id")
        try:
            job_id = int(raw_id) if raw_id is not None else None
        except (TypeError, ValueError) as error:
            raise ValueError(f"Invalid House atlas ArtJob ID: {key}") from error
        if job_id is not None and job_id <= 0:
            raise ValueError(f"Invalid nonpositive House atlas ArtJob ID: {key}")
        if require_jobs and job_id is None:
            raise ValueError(f"Unsubmitted House atlas ArtJob: {key}")
        receipts[key] = job_id
    assigned = [job for job in receipts.values() if job is not None]
    if len(assigned) != len(set(assigned)):
        raise ValueError("Duplicate House atlas ArtJob ID")
    return receipts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-jobs", action="store_true")
    args = parser.parse_args()
    try:
        data = yaml.safe_load(LEDGER.read_text(encoding="utf-8")) or {}
        receipts = validate(data, require_jobs=args.require_jobs)
    except (OSError, yaml.YAMLError, ValueError) as error:
        print(f"::error::House atlas art ledger invalid: {error}")
        return 1
    for key, job_id in receipts.items():
        print(f"{key}: ArtJob {job_id if job_id else 'PENDING'}")
    print("Submission contract verified; render, media HEAD and visual QA are separate gates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
