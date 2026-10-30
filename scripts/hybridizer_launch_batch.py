#!/usr/bin/env python3
"""Trickle the curated launch hybrids into Kind Robots and verify every delivered image.

WHY THIS EXISTS. hybridizer/t-007 asks for 4,000 pre-generated public hybrids, scheduled in
batches with immutable pair keys and explicit provenance, counting delivered images rather
than submitted prompts. Kind Robots' admin-only POST /api/hybridizer/batch queues at most 60
launch renders at a time below every other ArtJob's priority, so this script just keeps that
window full and records what actually arrived:

1. Refresh: for ledger entries not yet READY, read the public fusion status endpoint (which
   also reconciles delivery server-side). A READY entry is only marked verified after its
   image URL answers 200 with an image content type.
2. Submit: post the next unsubmitted pairs from projects/hybridizer/LAUNCH-PAIRS.json in
   batches of 50 until the server reports the pending window is full (DEFERRED).

Ledger: projects/hybridizer/art/LAUNCH-LEDGER.json, keyed by canonical "left+right" pair key.

Environment: KR_API_TOKEN (an admin token with generation:art), KR_BASE_URL (default
https://kindrobots.org). Exit 2 when the token is missing so a sweep reads it as unresolved.

Usage:
    python scripts/hybridizer_launch_batch.py              # refresh + submit
    python scripts/hybridizer_launch_batch.py --dry-run    # validate the next batch only
    python scripts/hybridizer_launch_batch.py --summary    # print ledger progress, no network
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAIRS = ROOT / "projects" / "hybridizer" / "LAUNCH-PAIRS.json"
LEDGER = ROOT / "projects" / "hybridizer" / "art" / "LAUNCH-LEDGER.json"
BATCH = 50
TERMINAL = {"READY", "FAILED", "CANCELLED", "REJECTED"}


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def pair_key(pair) -> str:
    left, right = sorted(pair)
    return f"{left}+{right}"


def load_ledger() -> dict:
    if LEDGER.exists():
        return json.loads(LEDGER.read_text())
    return {"version": 1, "entries": {}}


def save_ledger(ledger: dict) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(ledger, indent=1, sort_keys=True) + "\n")


def summary(ledger: dict, total: int) -> dict:
    counts: dict[str, int] = {}
    for entry in ledger["entries"].values():
        counts[entry.get("status", "?")] = counts.get(entry.get("status", "?"), 0) + 1
    verified = sum(1 for e in ledger["entries"].values() if e.get("verifiedAt"))
    return {"target": total, "submitted": len(ledger["entries"]), "verified": verified, "byStatus": counts}


class Api:
    def __init__(self, base: str, token: str):
        self.base = base.rstrip("/")
        self.token = token

    def call(self, method: str, path: str, body: dict | None = None) -> dict:
        data = json.dumps(body).encode() if body is not None else None
        request = urllib.request.Request(self.base + path, data=data, method=method)
        request.add_header("Authorization", f"Bearer {self.token}")
        request.add_header("Accept", "application/json")
        if data is not None:
            request.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as error:
            try:
                return json.loads(error.read().decode())
            except Exception:
                return {"success": False, "statusCode": error.code, "message": str(error)}

    def image_ok(self, path: str) -> bool:
        url = path if path.startswith("http") else self.base + path
        request = urllib.request.Request(url, method="GET")
        request.add_header("Range", "bytes=0-1023")
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                kind = response.headers.get("Content-Type", "")
                return response.status in (200, 206) and kind.startswith("image/")
        except Exception:
            return False


def refresh(api: Api, ledger: dict, limit: int) -> int:
    changed = 0
    open_entries = [
        (key, e) for key, e in ledger["entries"].items()
        if e.get("fusionId") and not e.get("verifiedAt") and e.get("status") not in {"REJECTED", "CANCELLED"}
    ]
    for key, entry in open_entries[:limit]:
        result = api.call("GET", f"/api/hybridizer/fusions/{entry['fusionId']}/status")
        data = result.get("data") or {}
        if not result.get("success") or not data:
            continue
        status = data.get("status") or entry.get("status")
        if status != entry.get("status"):
            entry["status"] = status
            changed += 1
        if status == "READY" and data.get("imagePath"):
            entry["imagePath"] = data["imagePath"]
            entry["artImageId"] = data.get("artImageId")
            if api.image_ok(data["imagePath"]):
                entry["verifiedAt"] = now()
                changed += 1
    return changed


def submit(api: Api, ledger: dict, pairs: list, max_batches: int, dry_run: bool) -> dict:
    todo = [p for p in pairs if pair_key(p) not in ledger["entries"]]
    report = {"queued": 0, "deferred": 0, "rejected": 0, "batches": 0}
    for start in range(0, len(todo), BATCH):
        if report["batches"] >= max_batches:
            break
        chunk = todo[start:start + BATCH]
        result = api.call("POST", "/api/hybridizer/batch", {"pairs": chunk, "dryRun": dry_run})
        report["batches"] += 1
        if not result.get("success"):
            report["error"] = result.get("message") or str(result.get("statusCode"))
            break
        full = False
        for row in result["data"]["results"]:
            status = row["status"]
            if status in {"DEFERRED", "WOULD_QUEUE"}:
                report["deferred" if status == "DEFERRED" else "queued"] += 1
                full = full or status == "DEFERRED"
                continue
            if status == "REJECTED":
                report["rejected"] += 1
            else:
                report["queued"] += 1
            if not dry_run:
                key = pair_key(row["pairKey"].split("+"))
                ledger["entries"][key] = {
                    "fusionId": row.get("fusionId"),
                    "title": row.get("title"),
                    "artJobId": row.get("artJobId"),
                    "status": "QUEUED" if status in {"QUEUED", "LINKED", "PENDING", "RUNNING"} else status,
                    "submittedAt": now(),
                    **({"error": row["error"]} if row.get("error") else {}),
                }
        if full or dry_run:
            break
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--max-batches", type=int, default=4)
    parser.add_argument("--refresh-limit", type=int, default=400)
    args = parser.parse_args()

    pairs = json.loads(PAIRS.read_text())["pairs"]
    ledger = load_ledger()
    if args.summary:
        print(json.dumps(summary(ledger, len(pairs))))
        return 0
    token = os.environ.get("KR_API_TOKEN", "").strip()
    if not token:
        print("KR_API_TOKEN is not set; cannot reach Kind Robots.", file=sys.stderr)
        return 2
    api = Api(os.environ.get("KR_BASE_URL", "https://kindrobots.org"), token)

    refreshed = 0 if args.dry_run else refresh(api, ledger, args.refresh_limit)
    report = submit(api, ledger, pairs, args.max_batches, args.dry_run)
    if not args.dry_run:
        save_ledger(ledger)
    print(json.dumps({"refreshed": refreshed, "submit": report, "progress": summary(ledger, len(pairs))}))
    return 1 if report.get("error") else 0


if __name__ == "__main__":
    raise SystemExit(main())
