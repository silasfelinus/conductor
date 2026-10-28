#!/usr/bin/env python3
"""Validate the two dedicated House atlas requests and their durable ArtJob receipts.

This is a submission check, not proof of a completed render or accessible image.
"""
from __future__ import annotations

import argparse
import json
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



def audit_delivery(data: dict, jobs: list[dict], media_probe=None) -> dict:
    """Read-only status and media proof for exactly these two atlas receipts.

    Reuse the existing 752-image auditor's ArtJob identity and HEAD/Last-Modified
    rules, but never mix these two newer requests into its immutable baseline.
    """
    from audit_memory_dungeon_art_delivery import audit_jobs

    receipts = [
        {"id": key, "jobId": job_id, "imagePath": EXPECTED[key]}
        for key, job_id in validate(data, require_jobs=True).items()
    ]
    if media_probe is None:
        return audit_jobs(receipts, jobs)
    return audit_jobs(receipts, jobs, media_probe)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-jobs", action="store_true")
    parser.add_argument("--live", action="store_true",
                        help="read existing ArtJobs and HEAD-check their exact media URLs")
    parser.add_argument("--report", type=Path,
                        help="write machine-readable evidence (live mode only)")
    parser.add_argument("--require-delivered", action="store_true",
                        help="fail until both distinct ArtJobs and media HEADs prove delivery")
    args = parser.parse_args()
    if (args.require_delivered or args.report) and not args.live:
        parser.error("--report and --require-delivered require --live")
    try:
        data = yaml.safe_load(LEDGER.read_text(encoding="utf-8")) or {}
        receipts = validate(data, require_jobs=args.require_jobs or args.live)
        if args.live:
            import consume_art_queue as consumer
            from reconcile_memory_dungeon_art_jobs import server_jobs

            if not consumer.KR_API_TOKEN:
                raise RuntimeError("KR_API_TOKEN unavailable; no live delivery claim")
            report = audit_delivery(data, server_jobs())
            if args.report:
                args.report.parent.mkdir(parents=True, exist_ok=True)
                args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            print(json.dumps({key: value for key, value in report.items()
                              if key != "results"}, sort_keys=True))
            for row in report["results"]:
                print(f"  {row['status']}: {row['id']} (ArtJob {row['jobId']})")
            if args.require_delivered and report["delivered"] != len(EXPECTED):
                return 2
        else:
            for key, job_id in receipts.items():
                print(f"{key}: ArtJob {job_id if job_id else 'PENDING'}")
            print("Submission contract verified; live render/media QA not checked.")
        return 0
    except (OSError, yaml.YAMLError, ValueError, RuntimeError) as error:
        print(f"::error::House atlas audit blocked: {error}")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
