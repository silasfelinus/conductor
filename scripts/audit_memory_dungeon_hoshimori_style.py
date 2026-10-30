#!/usr/bin/env python3
"""Validate Hoshimori e07 style-proof destinations and durable ArtJob receipts.

A successful submission is not proof of a rendered ArtImage or accepted artwork.
Keep these eight private style samples distinct from the historical 752-job set.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "projects/memory-dungeon/art/HOSHIMORI-WARM-STYLE-PROOFS.yaml"
CATEGORIES = {
    "warm-overworld-map": ("map", "1024x1024"),
    "warm-red-oven-atlas": ("dungeon-atlas", "1024x1024"),
    "pip-portrait": ("portrait", "768x1024"),
    "oven-baker-portrait": ("portrait", "768x1024"),
    "kitsune-namekeeper": ("yokai", "768x1024"),
    "tanuki-trader": ("yokai", "768x1024"),
    "lantern-supper": ("scene", "1344x768"),
    "borrowed-hearth-card": ("card", "768x1024"),
}
PREFIX = "memory-dungeon-hoshimori-e07-style-"
DEST = "public/images/memory-dungeon/hoshimori/e07/style-proofs/"


def validate(data: dict, *, require_jobs: bool = False) -> dict[str, int | None]:
    rows = data.get("requests") if isinstance(data, dict) else None
    if not isinstance(rows, list) or len(rows) != len(CATEGORIES):
        raise ValueError("Expected exactly eight Hoshimori warm style requests")
    receipts: dict[str, int | None] = {}
    seen_paths: set[str] = set()
    seen_jobs: set[int] = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("Malformed style request")
        request_id = row.get("id")
        if not isinstance(request_id, str) or not request_id.startswith(PREFIX):
            raise ValueError("Unexpected Hoshimori request ID")
        slug = request_id.removeprefix(PREFIX)
        if slug not in CATEGORIES or slug in receipts:
            raise ValueError(f"Duplicate or unknown Hoshimori subject: {slug}")
        category, size = CATEGORIES[slug]
        expected_path = f"{DEST}{slug}.webp"
        if row.get("category") != category or row.get("size") != size:
            raise ValueError(f"Incorrect category or dimensions for {slug}")
        if (row.get("image_path") != expected_path
                or row.get("source_url") != expected_path.removeprefix("public")
                or expected_path in seen_paths):
            raise ValueError(f"Duplicate or incorrect destination for {slug}")
        seen_paths.add(expected_path)
        if row.get("target_repo") != "silasfelinus/kind_robots" or row.get("project_slug") != "memory-dungeon":
            raise ValueError(f"Incorrect repository/project for {slug}")
        if row.get("engine") != "krea2" or row.get("variant") != "image":
            raise ValueError(f"Incorrect render lane for {slug}")
        if len(str(row.get("prompt") or "").strip()) < 120:
            raise ValueError(f"Missing production prompt for {slug}")
        raw = row.get("last_art_job_id")
        if raw is None:
            if require_jobs:
                raise ValueError(f"Unsubmitted Hoshimori request: {slug}")
            receipts[slug] = None
            continue
        if isinstance(raw, bool) or not str(raw).isdigit() or int(raw) <= 0:
            raise ValueError(f"Invalid ArtJob ID for {slug}")
        job = int(raw)
        if job in seen_jobs:
            raise ValueError(f"Duplicate ArtJob ID: {job}")
        seen_jobs.add(job)
        receipts[slug] = job
    if set(receipts) != set(CATEGORIES):
        raise ValueError("Incomplete Hoshimori style coverage")
    return receipts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-jobs", action="store_true")
    args = parser.parse_args()
    receipts = validate(yaml.safe_load(LEDGER.read_text()), require_jobs=args.require_jobs)
    print(f"Hoshimori warm style: {sum(v is not None for v in receipts.values())}/8 durable ArtJob receipts")
    for slug, job in receipts.items():
        print(f"  {slug}: {job if job is not None else 'PENDING'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
