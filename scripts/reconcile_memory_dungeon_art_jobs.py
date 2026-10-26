#!/usr/bin/env python3
"""Adopt existing Memory Dungeon ArtJobs before re-submitting an interrupted batch.

A cancelled long-running GitHub workflow lost last_art_job_id fields even though
the API had accepted and sometimes rendered those jobs. Recover by the immutable
conductorRequest.id AND exact destination, not by a new random render seed.
Fail closed on pagination/API errors to avoid duplicate GPU work.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import consume_art_queue as consumer  # noqa: E402
import consume_art_requests as requests  # noqa: E402

LEDGERS = (
    ROOT / "projects/art-prompts.yaml",
    ROOT / "projects/memory-dungeon/art/KNOWN-ART-REQUESTS.yaml",
)
PREFIX = "memory-dungeon-saturate-"
PROJECT = "memory-dungeon"


def job_identity(job: dict[str, Any]) -> tuple[str, str] | None:
    if job.get("status") not in ("PENDING", "RUNNING", "DONE"):
        return None
    payload = job.get("payload") or {}
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except ValueError:
            return None
    if not isinstance(payload, dict):
        return None
    source = payload.get("conductorRequest") or {}
    if not isinstance(source, dict):
        return None
    request_id = str(source.get("id") or "")
    image_path = str(source.get("imagePath") or payload.get("imagePath") or "")
    if not request_id.startswith(PREFIX) or not image_path:
        return None
    if source.get("targetRepo") != "silasfelinus/kind_robots":
        return None
    return request_id, image_path


def index_existing_jobs(jobs: list[dict[str, Any]]) -> dict[tuple[str, str], int]:
    found: dict[tuple[str, str], int] = {}
    for job in jobs:
        key = job_identity(job)
        try:
            job_id = int(job.get("id") or 0)
        except (ValueError, TypeError):
            continue
        if key and job_id > found.get(key, 0):
            found[key] = job_id
    return found


def server_jobs() -> list[dict[str, Any]]:
    jobs: list[dict[str, Any]] = []
    for page in range(1, 101):
        url = f"{consumer.KR_BASE_URL}/api/art/queue?projectSlug={PROJECT}&pageSize=200&page={page}"
        status, envelope = consumer.http_json("GET", url, timeout=45)
        if status != 200 or not isinstance(envelope, dict) or not envelope.get("success"):
            raise RuntimeError(f"ArtJob list failed on page {page} (HTTP {status}); refusing to resubmit")
        data = envelope.get("data") or {}
        batch = data.get("jobs")
        pagination = data.get("pagination") or {}
        if not isinstance(batch, list) or not isinstance(pagination, dict):
            raise RuntimeError("ArtJob list omitted pagination; refusing to resubmit")
        jobs.extend(batch)
        if not pagination.get("hasNextPage"):
            return jobs
    raise RuntimeError("ArtJob pagination exceeded 100 pages; refusing to resubmit")


def reconcile_text(text: str, existing: dict[tuple[str, str], int]) -> tuple[str, int]:
    data = yaml.safe_load(text) or {}
    recovered = 0
    for entry in data.get("requests") or []:
        if not isinstance(entry, dict) or not str(entry.get("id") or "").startswith(PREFIX):
            continue
        if str(entry.get("status") or "pending").lower() != "pending":
            continue
        if entry.get("force") is True or requests.positive_job_id(entry.get("last_art_job_id")):
            continue
        key = (entry["id"], str(entry.get("image_path") or ""))
        job_id = existing.get(key)
        if job_id:
            text, changed = requests.set_request_field(text, entry["id"], "last_art_job_id", job_id)
            recovered += int(changed)
    return text, recovered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="persist recovered IDs")
    args = parser.parse_args()
    if not consumer.KR_API_TOKEN:
        print("KR_API_TOKEN required for ArtJob reconciliation", file=sys.stderr)
        return 1
    try:
        existing = index_existing_jobs(server_jobs())
    except Exception as error:
        print(f"Memory Dungeon reconciliation blocked: {error}", file=sys.stderr)
        return 1
    recovered = 0
    for ledger in LEDGERS:
        if not ledger.is_file():
            print(f"Required ledger missing: {ledger}", file=sys.stderr)
            return 1
        before = ledger.read_text()
        after, count = reconcile_text(before, existing)
        recovered += count
        print(f"{ledger.relative_to(ROOT)}: {count} existing ArtJob ID(s) recovered")
        if args.live and before != after:
            ledger.write_text(after)
    print(f"Memory Dungeon: {len(existing)} server request identities, {recovered} recovered ledger rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
