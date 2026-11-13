#!/usr/bin/env python3
"""Read-only production cross-check for latest Shifting Desks Classic rerenders.

Only exact Conductor request IDs, target repository, destination and creation
time can establish a matching ArtJob. A previous 200 at the same path is NOT
delivery evidence. Never enqueue, overwrite media or alter art verdicts.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

from reconcile_delivery import fetch_jobs, job_request_id, matching_job, reconcile_row, timestamp

ROOT = Path(__file__).resolve().parents[3]
ART = Path(__file__).resolve().parent
ROUNDS = (13, 14, 15, 17, 19)


def latest_unmet(art_dir: Path = ART):
    latest = {}
    for number in ROUNDS:
        round_data = yaml.safe_load(
            (art_dir / f"ROUND-{number}.yaml").read_text(encoding="utf-8")
        )
        for item in round_data["subjects"]:
            latest[item["target_path"]] = {
                **item,
                "_round": number,
                "_requested_at": round_data["requested_at"],
            }
    return [row for row in latest.values() if row.get("status") != "delivered"]


def audit(rows, jobs, *, reconcile=reconcile_row):
    report = []
    for row in rows:
        requested_at = timestamp(row["_requested_at"])
        job = matching_job(row, jobs, requested_at)
        target = str(row["target_path"]).replace("kind_robots ", "").strip().lstrip("/")
        same_destination = [
            candidate for candidate in jobs
            if isinstance(candidate.get("payload"), dict)
            and str(candidate["payload"].get("imagePath") or "").strip().lstrip("/") == target
            and candidate["payload"].get("targetRepo") == "silasfelinus/kind_robots"
            and timestamp(candidate.get("createdAt"))
            and timestamp(candidate["createdAt"]) >= requested_at
        ]
        changes = reconcile(row, jobs, requested_at) if job else {}
        delivered = changes.get("status") == "delivered"
        report.append({
            "round": row["_round"],
            "key": row["key"],
            "request_id": row["request_id"],
            "target_path": row["target_path"],
            "ledger_status": row.get("status"),
            "job_id": job.get("id") if job else None,
            "job_status": job.get("status") if job else None,
            "image_id": job.get("artImageId") if job else None,
            "created_at": job.get("createdAt") if job else None,
            "verified_newer_delivery": delivered,
            "same_destination_after_request": [
                {
                    "job_id": candidate.get("id"),
                    "status": candidate.get("status"),
                    "image_id": candidate.get("artImageId"),
                    "request_id": job_request_id(candidate),
                    "created_at": candidate.get("createdAt"),
                }
                for candidate in same_destination
            ],
            "reconcile_result": changes,
        })
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="Write a detailed JSON diagnostic artifact")
    args = parser.parse_args()
    sys.path.insert(0, str(ROOT))
    from scripts import consume_art_queue_core as core

    if not core.KR_API_TOKEN:
        raise SystemExit("Production ArtJob read unavailable: KR_API_TOKEN not configured")
    rows = latest_unmet()
    jobs = fetch_jobs(core)
    report = audit(rows, jobs)
    summary = {
        "pending": len(report),
        "jobs_scanned": len(jobs),
        "same_destination_candidates": sum(
            len(row["same_destination_after_request"]) for row in report
        ),
        "exact_job_matches": sum(row["job_id"] is not None for row in report),
        "verified_newer_delivery": sum(row["verified_newer_delivery"] for row in report),
        "no_exact_job": sum(row["job_id"] is None for row in report),
    }
    print("Shifting Desks live art audit:", json.dumps(summary, sort_keys=True))
    for row in report:
        print(
            f"{row['request_id']}: "
            f"job={row['job_id']} status={row['job_status']} "
            f"image={row['image_id']} newer-delivery={row['verified_newer_delivery']}"
            f" same-destination-candidates={row['same_destination_after_request']}"
        )
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            json.dumps({"summary": summary, "requests": report}, indent=2) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
