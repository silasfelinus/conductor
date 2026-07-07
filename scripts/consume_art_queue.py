#!/usr/bin/env python3
"""
consume_art_queue.py — submit approved art-generate.yaml entries to the
kind_robots ArtJob queue and land the results in projects/process/.

Closes the autonomous art loop (art-generator-connect t-012):

  projects/art-generate.yaml (approved batch)
    -> POST {KR}/api/art/queue          (one job per entry)
    -> poll GET {KR}/api/art/queue/{id} (relay renders on the home box)
    -> GET  {KR}/api/art/image/{artImageId}?includeImageData=true
    -> projects/process/{basename}      (distribute_images.py routes from there)

Dry-run by default: prints what would be queued and touches nothing.
The first live run is human-gated (Silas approves; see roadmap t-012).

Environment:
  KR_API_TOKEN   required for --live (machine auth: user apiKey or admin token)
  KR_BASE_URL    default https://kind-robots.vercel.app

Usage:
  python scripts/consume_art_queue.py                    # dry run
  python scripts/consume_art_queue.py --live             # queue + wait + download
  python scripts/consume_art_queue.py --live --limit 3   # first 3 entries only

Output files: results are PNG (what the engines emit). If Pillow is
installed they are converted to the .webp filename the entry names;
otherwise they are saved as .png next to that name with a warning, for
manual conversion before distribute_images.py runs.
"""

import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
ART_GENERATE_FILE = ROOT / "projects" / "art-generate.yaml"
PROCESS_DIR = ROOT / "projects" / "process"

KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kind-robots.vercel.app").rstrip("/")
KR_API_TOKEN = os.environ.get("KR_API_TOKEN", "").strip()

POLL_SECONDS = 5

# Generation quality defaults. Each is overridable per art-generate.yaml entry
# (steps, cfg, sampler, negative_prompt, seed, engine) so a batch can spend
# more on hero key art than on throwaway icons. Keys emitted below are
# KR-style; the home relay's run_a1111 consumes them directly.
DEFAULT_ENGINE = "A1111"
DEFAULT_STEPS = 30
DEFAULT_CFG = 7
# A broad quality/cleanliness negative. The prompts already say "no text, no
# watermark, no collage"; this reinforces that on the sampler side and knocks
# back the usual SD failure modes (bad anatomy, artifacts, borders).
DEFAULT_NEGATIVE_PROMPT = (
    "text, watermark, signature, logo, caption, letters, words, "
    "blurry, low quality, lowres, jpeg artifacts, deformed, disfigured, "
    "extra limbs, bad anatomy, bad hands, cropped, out of frame, "
    "collage, frame, border, ugly, grainy"
)


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


def parse_size(size, default=(1024, 1024)):
    """'1280x720' -> (1280, 720); tolerates junk by falling back."""
    m = re.match(r"^\s*(\d+)\s*[xX]\s*(\d+)\s*$", str(size or ""))
    if not m:
        return default
    return int(m.group(1)), int(m.group(2))


def entry_to_job(entry):
    """Map an art-generate.yaml entry to an ArtJob enqueue body.

    Quality knobs (steps, cfg, negative prompt, sampler, seed) default to the
    module constants and may be overridden per entry. The optional knobs
    (sampler, seed) are only sent when the entry sets them, so the relay keeps
    its own safe defaults (sampler "Euler a", random seed) otherwise."""
    width, height = parse_size(entry.get("size"))

    payload = {
        "promptString": " ".join(str(entry.get("prompt") or "").split()),
        "negativePrompt": " ".join(
            str(entry.get("negative_prompt") or DEFAULT_NEGATIVE_PROMPT).split()
        ),
        "width": width,
        "height": height,
        "steps": int(entry.get("steps") or DEFAULT_STEPS),
        "cfg": entry.get("cfg", DEFAULT_CFG),
        # the relay's local fast path files its copy under the
        # project's collection folder
        "collection": entry.get("project") or "comfy",
    }

    # Optional per-entry knobs: only send when set, so an untouched batch runs
    # on the relay's proven defaults rather than a possibly-unsupported sampler.
    if entry.get("sampler"):
        payload["sampler"] = str(entry["sampler"])
    if entry.get("seed") is not None:
        payload["seed"] = entry["seed"]

    return {
        "engine": str(entry.get("engine") or DEFAULT_ENGINE).upper(),
        "projectSlug": entry.get("project") or None,
        "payload": payload,
    }


def load_entries():
    if not ART_GENERATE_FILE.exists():
        return []
    data = yaml.safe_load(ART_GENERATE_FILE.read_text()) or {}
    # Canonical shape is batch.entries. Tolerate a legacy top-level `images:`
    # list too, so a batch written by an older queue_missing_project_art.py
    # (or one already sitting on disk) is still consumed rather than silently
    # skipped.
    entries = (data.get("batch") or {}).get("entries") or data.get("images") or []
    return [
        e
        for e in entries
        if isinstance(e, dict) and e.get("prompt") and e.get("image_path")
    ]


def save_result(entry, image_b64):
    """Write the finished image into projects/process/ under the entry's
    basename — converted to webp when Pillow is available, else as .png."""
    PROCESS_DIR.mkdir(parents=True, exist_ok=True)
    target_name = Path(entry["image_path"]).name
    png_bytes = base64.b64decode(image_b64)

    if target_name.lower().endswith(".webp"):
        try:
            import io

            from PIL import Image  # optional dependency

            img = Image.open(io.BytesIO(png_bytes))
            out = PROCESS_DIR / target_name
            img.save(out, "WEBP", quality=90)
            return out, None
        except ImportError:
            out = PROCESS_DIR / (Path(target_name).stem + ".png")
            out.write_bytes(png_bytes)
            return out, (
                "Pillow not installed - saved PNG; convert to "
                f"{target_name} before running distribute_images.py"
            )

    out = PROCESS_DIR / target_name
    out.write_bytes(png_bytes)
    return out, None


def enqueue(job_body):
    status, resp = http_json("POST", f"{KR_BASE_URL}/api/art/queue", job_body)
    if status != 201 or not resp or not resp.get("success"):
        raise RuntimeError(f"enqueue failed: HTTP {status} {resp and resp.get('message')}")
    return resp["data"]["job"]["id"]


def wait_for_job(job_id, timeout):
    deadline = time.time() + timeout
    while time.time() < deadline:
        status, resp = http_json("GET", f"{KR_BASE_URL}/api/art/queue/{job_id}")
        if status == 200 and resp and resp.get("success"):
            job = resp["data"]["job"]
            if job["status"] == "DONE":
                return job
            if job["status"] in ("FAILED", "CANCELLED"):
                raise RuntimeError(f"job {job_id} {job['status']}: {job.get('error')}")
        time.sleep(POLL_SECONDS)
    raise RuntimeError(f"job {job_id} timed out after {timeout}s (still queued/running)")


def fetch_image_b64(art_image_id):
    status, resp = http_json(
        "GET",
        f"{KR_BASE_URL}/api/art/image/{art_image_id}?includeImageData=true",
        timeout=180,
    )
    if status != 200 or not resp:
        raise RuntimeError(f"image fetch failed: HTTP {status}")
    record = resp.get("data") or {}
    image_b64 = record.get("imageData")
    if not image_b64:
        raise RuntimeError(f"ArtImage {art_image_id} has no imageData")
    return image_b64


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="actually queue and download")
    parser.add_argument("--limit", type=int, default=0, help="max entries this run (0 = all)")
    parser.add_argument("--timeout", type=int, default=600, help="seconds to wait per job")
    args = parser.parse_args()

    entries = load_entries()
    if args.limit > 0:
        entries = entries[: args.limit]

    if not entries:
        print("No approved entries in projects/art-generate.yaml - nothing to do.")
        return 0

    print(f"{'LIVE' if args.live else 'DRY RUN'}: {len(entries)} entr{'y' if len(entries) == 1 else 'ies'} via {KR_BASE_URL}\n")

    if not args.live:
        for entry in entries:
            job = entry_to_job(entry)
            print(
                f"  would queue {entry['image_path']}"
                f"  [{job['payload']['width']}x{job['payload']['height']}]"
                f"  {job['payload']['steps']}steps"
                f"  \"{job['payload']['promptString'][:60]}\""
            )
        print("\nRe-run with --live to queue for real (requires KR_API_TOKEN).")
        return 0

    if not KR_API_TOKEN:
        print("KR_API_TOKEN is required for --live.", file=sys.stderr)
        return 1

    failures = 0
    for entry in entries:
        name = entry["image_path"]
        try:
            job_id = enqueue(entry_to_job(entry))
            print(f"  queued job {job_id} for {name} - waiting...")
            job = wait_for_job(job_id, args.timeout)
            image_b64 = fetch_image_b64(job["artImageId"])
            out, warning = save_result(entry, image_b64)
            print(f"  DONE {name} -> {out.relative_to(ROOT)} (ArtImage {job['artImageId']})")
            if warning:
                print(f"    WARNING: {warning}")
        except Exception as e:  # noqa: BLE001 - keep draining the batch
            failures += 1
            print(f"  FAILED {name}: {e}", file=sys.stderr)

    print(
        f"\n{len(entries) - failures}/{len(entries)} succeeded."
        + ("" if failures else " Next: python scripts/distribute_images.py --dry-run")
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
