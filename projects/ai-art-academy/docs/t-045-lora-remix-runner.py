#!/usr/bin/env python3
"""One-off runner for ai-art-academy/t-045.

Re-runs the Kontext LoRA arm for the 5 style-remix-configs.yaml styles that
already carry a recorded loraPath/loraTrigger/loraWeight and a real
relay-cataloged file (impressionism, illuminated-manuscript, watercolor,
oil-painting, pop-art), against the same fixed reference image (ArtJob 2604
/ ArtImage 12777, docs/t-004-remix-evidence/_reference.webp) and remix seed
(909090) used for each style's prompt-only arm -- apples-to-apples per the
task note.

Uses the same production path style-remix-configs.yaml documents:
POST /api/art/enqueue {engine: "kontext", promptString, sourceImageBase64,
loraName, loraStrength} -> buildKontextWorkflow.

Environment:
  KR_API_TOKEN   required
  KR_BASE_URL    default https://kindrobots.org

Usage:
  python t-045-lora-remix-runner.py --enqueue-only   # fire all 5, print job ids
  python t-045-lora-remix-runner.py --poll <ids>     # poll until terminal, save images
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

DOCS_DIR = Path(__file__).parent
REFERENCE_IMAGE = DOCS_DIR / "t-004-remix-evidence" / "_reference.webp"
RESULTS_FILE = DOCS_DIR / "t-045-lora-arm-results.json"

KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kindrobots.org").rstrip("/")
KR_API_TOKEN = os.environ.get("KR_API_TOKEN", "").strip()
SEED = 909090

STYLES = [
    {
        "style_slug": "impressionism",
        "loraPath": "FLUX/impressionist.safetensors",
        "loraTrigger": "Turn this image into the Impressionist style.",
        "loraWeight": 1.0,
    },
    {
        "style_slug": "illuminated-manuscript",
        "loraPath": "FLUX/manuscript_illustration_kontext.safetensors",
        "loraTrigger": "Turn this image into the Medieval Manuscript style.",
        "loraWeight": 1.0,
    },
    {
        "style_slug": "watercolor",
        "loraPath": "FLUX/watercolor.safetensors",
        "loraTrigger": "Turn this image into the Watercolor style.",
        "loraWeight": 1.0,
    },
    {
        "style_slug": "oil-painting",
        "loraPath": "FLUX/flux1-kt_oil_painting_lora_v2.safetensors",
        "loraTrigger": "Turn this image into the Oil Painting style.",
        "loraWeight": 1.0,
    },
    {
        "style_slug": "pop-art",
        "loraPath": "Kontext/SFW/popart.safetensors",
        "loraTrigger": "Turn this image into the Pop Art style.",
        "loraWeight": 1.0,
    },
]


def http_json(method, url, body=None, timeout=60):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if KR_API_TOKEN:
        req.add_header("Authorization", f"Bearer {KR_API_TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode() or "null")
    except urllib.error.HTTPError as e:
        try:
            payload = json.loads(e.read().decode() or "null")
        except (ValueError, OSError):
            payload = None
        return e.code, payload


def image_data_url(path: Path) -> str:
    suffix = path.suffix.lower()
    media = {
        ".webp": "image/webp",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
    }.get(suffix, "image/png")
    return f"data:{media};base64,{base64.b64encode(path.read_bytes()).decode()}"


def enqueue_all():
    if not KR_API_TOKEN:
        print("KR_API_TOKEN is required", file=sys.stderr)
        sys.exit(2)
    if not REFERENCE_IMAGE.exists():
        print(f"missing reference image: {REFERENCE_IMAGE}", file=sys.stderr)
        sys.exit(2)
    source_b64 = image_data_url(REFERENCE_IMAGE)
    results = {}
    for style in STYLES:
        body = {
            "engine": "kontext",
            "promptString": style["loraTrigger"],
            "sourceImageBase64": source_b64,
            "loraName": style["loraPath"],
            "loraStrength": style["loraWeight"],
            "seed": SEED,
            "projectSlug": "ai-art-academy",
            "designer": "AI Art Academy t-045 LoRA re-run",
            "isPublic": False,
            "priority": 1,
        }
        status, resp = http_json("POST", f"{KR_BASE_URL}/api/art/enqueue", body)
        entry = {"style_slug": style["style_slug"], "loraPath": style["loraPath"]}
        if status not in (200, 201) or not resp or not resp.get("success"):
            entry["enqueue_error"] = f"HTTP {status}: {resp}"
            print(f"FAILED to enqueue {style['style_slug']}: HTTP {status}: {resp}")
        else:
            job_id = int(resp["data"]["jobId"])
            entry["job_id"] = job_id
            entry["status"] = "PENDING"
            print(f"enqueued {style['style_slug']} -> job {job_id}")
        results[style["style_slug"]] = entry
    RESULTS_FILE.write_text(json.dumps(results, indent=2))
    print(f"wrote {RESULTS_FILE}")


def poll_all(timeout_seconds=1800, interval=15):
    if not RESULTS_FILE.exists():
        print("no results file -- run --enqueue-only first", file=sys.stderr)
        sys.exit(2)
    results = json.loads(RESULTS_FILE.read_text())
    deadline = time.time() + timeout_seconds
    pending = {
        slug: entry
        for slug, entry in results.items()
        if entry.get("job_id") and entry.get("status") not in ("DONE", "FAILED", "CANCELLED")
    }
    while pending and time.time() < deadline:
        for slug in list(pending.keys()):
            entry = results[slug]
            status, resp = http_json(
                "GET", f"{KR_BASE_URL}/api/art/queue/{entry['job_id']}", timeout=30
            )
            if status != 200 or not resp or not resp.get("success"):
                continue
            job = resp["data"]["job"]
            job_status = job.get("status")
            entry["status"] = job_status
            if job_status == "DONE":
                entry["art_image_id"] = job.get("artImageId")
                pending.pop(slug, None)
                print(f"{slug}: DONE artImageId={entry['art_image_id']}")
            elif job_status in ("FAILED", "CANCELLED"):
                entry["error"] = job.get("error")
                pending.pop(slug, None)
                print(f"{slug}: {job_status} error={entry['error']}")
        RESULTS_FILE.write_text(json.dumps(results, indent=2))
        if pending:
            time.sleep(interval)
    if pending:
        print(f"TIMED OUT waiting on: {list(pending.keys())}")
    RESULTS_FILE.write_text(json.dumps(results, indent=2))
    print(f"wrote {RESULTS_FILE}")


def download_images():
    results = json.loads(RESULTS_FILE.read_text())
    out_dir = DOCS_DIR / "t-045-lora-evidence"
    out_dir.mkdir(exist_ok=True)
    for slug, entry in results.items():
        art_image_id = entry.get("art_image_id")
        if not art_image_id:
            continue
        status, resp = http_json(
            "GET",
            f"{KR_BASE_URL}/api/art/image/{art_image_id}?includeImageData=true",
            timeout=120,
        )
        if status != 200 or not resp:
            print(f"{slug}: image fetch failed HTTP {status}")
            continue
        record = resp.get("data") or {}
        image_b64 = record.get("imageData")
        if not image_b64:
            print(f"{slug}: no imageData")
            continue
        out_path = out_dir / f"{slug}-lora.webp"
        out_path.write_bytes(base64.b64decode(image_b64))
        print(f"{slug}: saved {out_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--enqueue-only", action="store_true")
    parser.add_argument("--poll", action="store_true")
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args()
    if args.enqueue_only:
        enqueue_all()
    elif args.poll:
        poll_all(timeout_seconds=args.timeout)
    elif args.download:
        download_images()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
