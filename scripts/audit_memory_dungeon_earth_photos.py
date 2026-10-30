#!/usr/bin/env python3
"""Verify the four playable Earth Chronicle photographs have durable ArtJob receipts.

This is a submission/identity gate, not proof of render completion or media delivery.
The independent 752-request baseline and the House atlas ledger are unaffected.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "projects/memory-dungeon/art/EARTH-PHOTO-REQUESTS.yaml"
EXPECTED = {
    "earth-01": "dismissal.webp",
    "earth-02": "gathering.webp",
    "earth-03": "earth-03.webp",
    "earth-04": "earth-04.webp",
}


def inspect(path: Path = LEDGER, require_jobs: bool = False) -> list[str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    rows = data.get("requests") if isinstance(data, dict) else None
    if not isinstance(rows, list):
        return ["Missing Earth photograph request list"]
    errors: list[str] = []
    seen: set[str] = set()
    jobs: set[int] = set()
    for row in rows:
        if not isinstance(row, dict):
            errors.append("Invalid Earth photograph request")
            continue
        photo_id = row.get("source_photo_id")
        request_id = row.get("id")
        if photo_id not in EXPECTED or photo_id in seen:
            errors.append(f"Unknown or duplicate photograph: {photo_id}")
            continue
        seen.add(photo_id)
        expected_request = f"memory-dungeon-saturate-earth-photo-{photo_id[-2:]}"
        expected_path = f"public/images/memory-dungeon/earth-photographs/{EXPECTED[photo_id]}"
        if request_id != expected_request:
            errors.append(f"{photo_id}: wrong durable request ID")
        if row.get("image_path") != expected_path:
            errors.append(f"{photo_id}: wrong media destination")
        if row.get("source_url") != expected_path.removeprefix("public"):
            errors.append(f"{photo_id}: wrong runtime URL")
        if row.get("target_repo") != "silasfelinus/kind_robots" or row.get("project_slug") != "memory-dungeon":
            errors.append(f"{photo_id}: wrong destination project")
        if row.get("engine") != "krea2" or row.get("variant") != "image" or row.get("size") != "1344x768":
            errors.append(f"{photo_id}: wrong production lane or dimensions")
        if not isinstance(row.get("prompt"), str) or len(row["prompt"]) < 100:
            errors.append(f"{photo_id}: missing detailed production prompt")
        job_id = row.get("last_art_job_id")
        if job_id is not None:
            if isinstance(job_id, bool) or not isinstance(job_id, int) or job_id <= 0 or job_id in jobs:
                errors.append(f"{photo_id}: invalid or reused ArtJob ID")
            else:
                jobs.add(job_id)
        else:
            if row.get("status") != "pending":
                errors.append(f"{photo_id}: no ArtJob ID but marked complete")
            if row.get("force") is not True:
                errors.append(
                    f"{photo_id}: missing ArtJob must force a traceable render"
                )
            if require_jobs:
                errors.append(f"{photo_id}: no durable ArtJob ID")
    for missing in sorted(set(EXPECTED) - seen):
        errors.append(f"Missing {missing}")
    if len(rows) != len(EXPECTED):
        errors.append(f"Expected exactly {len(EXPECTED)} playable photograph requests, found {len(rows)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-jobs", action="store_true")
    args = parser.parse_args()
    errors = inspect(require_jobs=args.require_jobs)
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print("Four Earth Chronicle destinations validated; ArtJob receipt gate " +
          ("passed" if args.require_jobs else "not requested") +
          ". Delivery and visual QA are separate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
