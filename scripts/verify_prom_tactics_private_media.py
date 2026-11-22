#!/usr/bin/env python3
"""Verify private Prom/Tactics render bytes without exporting or publishing them.

DONE in a Conductor ledger is only a receipt. This checker fetches each
ArtImage through Kind Robots' authenticated file endpoint, verifies the actual
image container and geometry, and reports only IDs and technical evidence.
It never writes or uploads image bytes. Visual composition still needs review.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml
from PIL import Image, ImageStat

Image.MAX_IMAGE_PIXELS = 50_000_000
MAX_BYTES = 12 * 1024 * 1024


class SameOriginRedirect(urllib.request.HTTPRedirectHandler):
    """Do not forward the production JWT to another origin on a 302."""

    def __init__(self, origin: str):
        self.origin = urllib.parse.urlsplit(origin).netloc

    def redirect_request(self, request, fp, code, msg, headers, newurl):
        destination = urllib.parse.urlsplit(newurl)
        if destination.scheme != "https" or destination.netloc != self.origin:
            raise ValueError("Image redirect leaves the approved HTTPS origin")
        return super().redirect_request(request, fp, code, msg, headers, newurl)


def ledger_rows(paths: list[str]) -> list[dict]:
    rows = []
    for filename in paths:
        document = yaml.safe_load(Path(filename).read_text(encoding="utf-8")) or {}
        if document.get("is_public") is not False:
            raise ValueError(f"{filename}: private proof requires is_public: false")
        for subject in document.get("subjects") or []:
            art = subject.get("art") or {}
            jobs = subject.get("jobs") or {}
            for lane in subject.get("lane", "").split(","):
                lane = lane.strip()
                if not lane:
                    continue
                outcome = art.get(lane) or {}
                job_id = jobs.get(lane)
                image_id = outcome.get("art_image_id")
                status = outcome.get("status") or "REQUESTED"
                if type(job_id) is not int or job_id <= 0:
                    stage = "requested"
                elif status == "DONE" and type(image_id) is int and image_id > 0:
                    stage = "done-receipt"
                elif status in {"RUNNING", "PROCESSING"}:
                    stage = "running"
                else:
                    stage = "accepted"
                rows.append({
                    "key": subject["key"],
                    "asset": subject["asset"],
                    "job_id": job_id if type(job_id) is int else None,
                    "image_id": image_id if type(image_id) is int else None,
                    "ledger_status": status,
                    "stage": stage,
                    "expected_size": subject.get("size", ""),
                    "verdict": str(subject.get("verdict") or ""),
                })
    if len({row["key"] for row in rows}) != len(rows):
        raise ValueError("Duplicate art keys would make proof ambiguous")
    return rows


def inspect_image(payload: bytes, expected_size: str) -> dict:
    if len(payload) < 100 or len(payload) > MAX_BYTES:
        raise ValueError("Empty or oversized media payload")
    with Image.open(io.BytesIO(payload)) as opened:
        opened.verify()
    with Image.open(io.BytesIO(payload)) as opened:
        if opened.format not in {"PNG", "JPEG", "WEBP"}:
            raise ValueError("Unexpected media container")
        width, height = opened.size
        if width < 256 or height < 256:
            raise ValueError("Media dimensions too small")
        if "x" in expected_size:
            expected_width, expected_height = map(int, expected_size.split("x"))
            expected_ratio = expected_width / expected_height
            actual_ratio = width / height
            if abs(actual_ratio / expected_ratio - 1) > 0.20:
                raise ValueError("Media composition ratio differs from request")
        thumbnail = opened.convert("RGB")
        thumbnail.thumbnail((48, 48))
        contrast = ImageStat.Stat(thumbnail.convert("L")).stddev[0]
        if contrast < 2:
            raise ValueError("Media appears blank or nearly monochrome")
        return {
            "width": width,
            "height": height,
            "format": opened.format,
            "bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "contrast": round(contrast, 2),
        }


def download_private(image_id: int, origin: str, token: str) -> bytes:
    origin = origin.rstrip("/")
    parts = urllib.parse.urlsplit(origin)
    if parts.scheme != "https" or not parts.netloc or parts.path:
        raise ValueError("KR_BASE_URL must be a bare HTTPS origin")
    url = f"{origin}/api/art/images/{image_id}/file"
    request = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}", "Accept": "image/webp,image/*"},
    )
    opener = urllib.request.build_opener(SameOriginRedirect(origin))
    with opener.open(request, timeout=45) as response:
        media_type = response.headers.get("content-type", "").split(";")[0]
        if not media_type.startswith("image/"):
            raise ValueError("Authenticated endpoint returned non-image content")
        data = response.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError("Private image exceeds maximum media size")
        return data


def probe(rows: list[dict], origin: str, token: str, downloader=download_private):
    verified = 0
    duplicates = {}
    for row in rows:
        if row["stage"] != "done-receipt":
            continue
        try:
            data = downloader(row["image_id"], origin, token)
            evidence = inspect_image(data, row["expected_size"])
            image_hash = evidence["sha256"]
            if image_hash in duplicates and duplicates[image_hash] != row["key"]:
                raise ValueError("Different art keys resolve to identical image bytes")
            duplicates[image_hash] = row["key"]
            row["stage"] = "media-verified"
            row["evidence"] = evidence
            verified += 1
        except urllib.error.HTTPError as error:
            row["stage"] = "media-unavailable"
            row["error"] = f"HTTP {error.code}"
        except (OSError, ValueError, urllib.error.URLError) as error:
            row["stage"] = "media-unavailable"
            row["error"] = type(error).__name__
    return verified


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledgers", nargs="+")
    parser.add_argument("--min-done", type=int, default=1)
    parser.add_argument("--report", help="JSON metadata only; never private image bytes")
    args = parser.parse_args(argv)
    token = os.environ.get("KR_API_TOKEN", "")
    if not token:
        raise SystemExit("KR_API_TOKEN is missing; authenticated proof not attempted")
    rows = ledger_rows(args.ledgers)
    receipt_count = sum(row["stage"] == "done-receipt" for row in rows)
    verified = probe(rows, os.environ.get("KR_BASE_URL", "https://kindrobots.org"), token)
    counts = {
        stage: sum(row["stage"] == stage for row in rows)
        for stage in sorted({row["stage"] for row in rows})
    }
    report = {
        "source": "authenticated ArtImage file bytes",
        "note": "Media verification is not artistic approval or attachment proof",
        "total": len(rows),
        "done_receipts": receipt_count,
        "byte_verified": verified,
        "reviewed": sum(row["verdict"].lower().startswith("keep") for row in rows),
        "counts": counts,
        "rows": rows,
    }
    if args.report:
        Path(args.report).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "rows"}, indent=2))
    for row in rows:
        if row["stage"] != "media-verified":
            print(f"{row['key']}: {row['stage']} {row.get('error', '')}")
    if receipt_count < args.min_done or verified != receipt_count:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
