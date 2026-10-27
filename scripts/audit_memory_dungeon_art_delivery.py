#!/usr/bin/env python3
"""Audit Memory Dungeon ArtJob renders AND delivered media, without enqueueing.

The live queue drained 227 accepted requests, so the permanent 525-request
ledger alone cannot prove the 752-job handoff. Historical receipts preserve
those 227 exact request/job/destination triples. A recorded ArtJob ID, a
request marked "done", and a DONE render are NOT proof of a delivered image.

Offline mode validates the complete immutable receipt inventory. --live
reads the existing ArtJob API and HEAD-checks each DONE image's exact media
destination. No writes to the API, request ledgers, or media server occur.
"""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
import json
from pathlib import Path
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import consume_art_queue as consumer  # noqa: E402

PREFIX = "memory-dungeon-saturate-"
DEST_PREFIX = "public/images/memory-dungeon/"
TARGET_REPO = "silasfelinus/kind_robots"
EXPECTED = 752
LEDGERS = (
    ROOT / "projects/memory-dungeon/art/DRAINED-SUBMISSION-RECEIPTS.yaml",
    ROOT / "projects/memory-dungeon/art/KNOWN-ART-REQUESTS.yaml",
)


def valid_destination(value: object) -> bool:
    if not isinstance(value, str) or not value.startswith(DEST_PREFIX):
        return False
    tail = value[len(DEST_PREFIX):]
    return bool(tail) and all(part not in ("", ".", "..") for part in tail.split("/")) and not any(
        char in tail for char in ("\\", "?", "#", "%", "\x00")
    ) and tail.endswith((".webp", ".png", ".jpg", ".jpeg"))


def load_receipts(ledgers: tuple[Path, ...] = LEDGERS, expected: int = EXPECTED) -> list[dict[str, Any]]:
    receipts: list[dict[str, Any]] = []
    ids: set[str] = set()
    jobs: set[int] = set()
    destinations: set[str] = set()
    for ledger in ledgers:
        data = yaml.safe_load(ledger.read_text(encoding="utf-8")) or {}
        rows = data.get("requests")
        if not isinstance(rows, list):
            raise ValueError(f"{ledger.name}: missing requests list")
        for row in rows:
            if not isinstance(row, dict):
                raise ValueError(f"{ledger.name}: non-object receipt")
            request_id = row.get("id")
            path = row.get("image_path")
            try:
                job_id = int(row.get("last_art_job_id") or 0)
            except (TypeError, ValueError) as error:
                raise ValueError(f"{ledger.name}: invalid job ID for {request_id}") from error
            if not isinstance(request_id, str) or not request_id.startswith(PREFIX):
                raise ValueError(f"{ledger.name}: unexpected request {request_id}")
            if job_id <= 0 or not valid_destination(path):
                raise ValueError(f"{ledger.name}: incomplete/unsafe receipt {request_id}")
            if request_id in ids or job_id in jobs or path in destinations:
                raise ValueError(f"{ledger.name}: duplicate request/job/destination {request_id}")
            ids.add(request_id)
            jobs.add(job_id)
            destinations.add(path)
            receipts.append({"id": request_id, "jobId": job_id, "imagePath": path})
    if len(receipts) != expected:
        raise ValueError(f"Expected {expected} durable Memory Dungeon receipts, found {len(receipts)}")
    return receipts


def job_identity(job: dict[str, Any]) -> tuple[str, str, str] | None:
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
    return (
        str(source.get("id") or ""),
        str(source.get("imagePath") or payload.get("imagePath") or ""),
        str(source.get("targetRepo") or payload.get("targetRepo") or ""),
    )


def assess_media_headers(headers: Any, created_at: object) -> str:
    """A live image needs image MIME and a timestamp no older than its ArtJob."""
    mime = str(headers.get("Content-Type") or "").split(";", 1)[0].strip().lower()
    if not mime.startswith("image/"):
        return "media_not_image"
    try:
        created = datetime.fromisoformat(str(created_at).replace("Z", "+00:00"))
        modified = parsedate_to_datetime(str(headers.get("Last-Modified") or ""))
        if created.tzinfo is None or modified.tzinfo is None:
            return "media_unproven"
        if modified.astimezone(timezone.utc) + timedelta(seconds=1) < created.astimezone(timezone.utc):
            return "media_stale"
    except (ValueError, TypeError, IndexError):
        return "media_unproven"
    return "delivered"


def probe_media(path: str, created_at: object) -> str:
    if not valid_destination(path):
        return "media_unsafe_path"
    origin = __import__("os").environ.get(
        "KR_MEDIA_ORIGIN", "https://media.acrocatranch.com"
    ).rstrip("/")
    url = origin + "/" + urllib.parse.quote(path.removeprefix("public/"), safe="/")
    request = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            if not 200 <= response.status < 300:
                return "media_unreachable"
            return assess_media_headers(response.headers, created_at)
    except (urllib.error.URLError, TimeoutError, OSError):
        return "media_unreachable"


def audit_jobs(
    receipts: list[dict[str, Any]],
    jobs: list[dict[str, Any]],
    media_probe: Callable[[str, object], str] = probe_media,
) -> dict[str, Any]:
    by_id: dict[int, dict[str, Any]] = {}
    for job in jobs:
        try:
            job_id = int(job.get("id") or 0)
        except (ValueError, TypeError):
            continue
        if job_id > 0:
            by_id[job_id] = job
    results: list[dict[str, Any]] = []
    probes: list[tuple[int, str, object]] = []
    for receipt in receipts:
        job = by_id.get(receipt["jobId"])
        status = "job_missing"
        art_image_id = None
        if job:
            identity = job_identity(job)
            if identity != (receipt["id"], receipt["imagePath"], TARGET_REPO):
                status = "job_identity_mismatch"
            else:
                state = str(job.get("status") or "").upper()
                try:
                    art_image_id = int(job.get("artImageId") or 0) or None
                except (ValueError, TypeError):
                    art_image_id = None
                if state in ("PENDING", "RUNNING", "FAILED", "CANCELLED"):
                    status = state.lower()
                elif state == "DONE":
                    status = "done_without_art_image"
                    if art_image_id:
                        status = "media_unreachable"
                        probes.append((len(results), receipt["imagePath"], job.get("createdAt")))
                else:
                    status = "unknown_job_state"
        results.append({**receipt, "artImageId": art_image_id, "status": status})
    # A stalled media host must not make 752 serial 12-second HEAD requests.
    # Keep the queue read-only and bound concurrent probes to a small pool.
    with ThreadPoolExecutor(max_workers=12) as pool:
        futures = {
            pool.submit(media_probe, path, created): index
            for index, path, created in probes
        }
        for future in as_completed(futures):
            try:
                results[futures[future]]["status"] = future.result()
            except Exception:  # Network/probe failure is not delivery proof.
                results[futures[future]]["status"] = "media_unreachable"
    counts = Counter(row["status"] for row in results)
    return {
        "total": len(receipts),
        "counts": dict(sorted(counts.items())),
        "delivered": counts["delivered"],
        "pendingReview": len(receipts) - counts["delivered"],
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="read ArtJobs and HEAD-check delivered images")
    parser.add_argument("--report", type=Path, help="write full JSON evidence to this local path")
    parser.add_argument("--require-delivered", action="store_true", help="fail until every receipt is verified")
    args = parser.parse_args()
    try:
        receipts = load_receipts()
        if args.live:
            if not consumer.KR_API_TOKEN:
                raise RuntimeError("KR_API_TOKEN unavailable; live audit not run")
            from reconcile_memory_dungeon_art_jobs import server_jobs
            report = audit_jobs(receipts, server_jobs())
        else:
            report = {"total": len(receipts), "submitted": len(receipts),
                      "delivery": "NOT CHECKED (offline inventory only)"}
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({key: value for key, value in report.items() if key != "results"}, sort_keys=True))
        if args.live:
            unresolved = [row for row in report["results"] if row["status"] != "delivered"]
            for row in unresolved[:20]:
                print(f"  {row['status']}: {row['id']} (ArtJob {row['jobId']})")
            if args.require_delivered and unresolved:
                return 2
        return 0
    except (OSError, yaml.YAMLError, ValueError, RuntimeError) as error:
        print(f"Memory Dungeon art delivery audit BLOCKED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
