#!/usr/bin/env python3
"""Verify nine private Round-16 Arthemy deliveries and create an ephemeral review sheet.

No ArtImage URLs, tokens, full-resolution private binaries, or contact sheets are
committed to Git. This command never publishes or promotes a candidate.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import sys
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "projects/zuzu-gamebook/art/ROUND-16-SCENE-FIDELITY.yaml"
REQUIRED = {"a2-bell-view": (1344, 768), "a2-gift": (896, 1152), "a4-bloom": (1344, 768)}


def cells(data):
    """Reject a superficially DONE ledger that lacks real IDs or unique cells."""
    assert data.get("series") == "zuzu-koala-assassin"
    subjects = data.get("subjects") or []
    assert Counter(s.get("section") for s in subjects) == {key: 3 for key in REQUIRED}
    assert len({s["key"] for s in subjects}) == 9
    jobs = set()
    images = set()
    for subject in subjects:
        lane = subject.get("lane", "arthemy-house")
        art = (subject.get("art") or {}).get(lane) or {}
        job_id = (subject.get("jobs") or {}).get(lane)
        image_id = art.get("art_image_id")
        assert art.get("status") == "DONE", f"{subject['key']} is not DONE"
        assert isinstance(job_id, int) and job_id > 0
        assert isinstance(image_id, int) and image_id > 0
        assert job_id not in jobs and image_id not in images
        jobs.add(job_id)
        images.add(image_id)
        yield subject, job_id, image_id


def safe_media_url(base, path):
    """Only send the private viewer JWT back to the configured KR host."""
    if not isinstance(path, str) or not path.strip():
        raise ValueError("Missing ArtImage imagePath")
    url = urllib.parse.urljoin(base.rstrip("/") + "/", path)
    a, b = urllib.parse.urlsplit(base), urllib.parse.urlsplit(url)
    if b.scheme != "https" or (a.hostname, a.port) != (b.hostname, b.port):
        raise ValueError("ArtImage path points outside the authenticated Kind Robots origin")
    return url


def fetch_image(image_id, token, base):
    """Validate both metadata and the actually downloadable image bytes."""
    meta_url = f"{base.rstrip('/')}/api/art/image/{image_id}"
    request = urllib.request.Request(meta_url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(request, timeout=50) as response:
        metadata = json.load(response)
    data = metadata.get("data") or {}
    if not metadata.get("success") or data.get("id") != image_id:
        raise ValueError(f"ArtImage {image_id}: invalid metadata")
    request = urllib.request.Request(
        safe_media_url(base, data.get("imagePath")), headers={"Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        raw = response.read(12_000_000)
        if len(raw) >= 12_000_000:
            raise ValueError(f"ArtImage {image_id}: excessive media size")
    from PIL import Image

    with Image.open(io.BytesIO(raw)) as image:
        image.load()
        image_format = image.format
        rgb = image.convert("RGB")
    if image_format not in {"PNG", "JPEG", "WEBP"}:
        raise ValueError(f"ArtImage {image_id}: unexpected image format {image_format}")
    return rgb, hashlib.sha256(raw).hexdigest()


def review_sheet(loaded, output):
    """Three columns by three rows; labels stay within each candidate cell."""
    from PIL import Image, ImageDraw, ImageOps

    thumb = (390, 260)
    label_height = 42
    sheet = Image.new("RGB", (3 * thumb[0], 3 * (thumb[1] + label_height)), "#23252a")
    draw = ImageDraw.Draw(sheet)
    for idx, (subject, job_id, image_id, image, _) in enumerate(loaded):
        column, row = idx % 3, idx // 3
        x, y = column * thumb[0], row * (thumb[1] + label_height)
        fitted = ImageOps.contain(image, thumb, Image.Resampling.LANCZOS)
        sheet.paste(fitted, (x + (thumb[0] - fitted.width) // 2, y + (thumb[1] - fitted.height) // 2))
        draw.text((x + 9, y + thumb[1] + 3), f"{subject['section']} seed {subject['seed']}", fill="#ffffff")
        draw.text((x + 9, y + thumb[1] + 20), f"Job {job_id} / ArtImage {image_id}", fill="#b3bdc5")
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, "JPEG", quality=79, optimize=True)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--sheet", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)
    token = os.getenv("KR_API_TOKEN", "")
    base = os.getenv("KR_BASE_URL", "https://kindrobots.org")
    if not token:
        print("KR_API_TOKEN unavailable; no private images fetched", file=sys.stderr)
        return 2
    loaded = []
    for subject, job_id, image_id in cells(yaml.safe_load(args.ledger.read_text())):
        image, sha = fetch_image(image_id, token, base)
        expected = REQUIRED[subject["section"]]
        if image.size != expected:
            raise ValueError(f"{subject['key']}: expected {expected}, got {image.size}")
        loaded.append((subject, job_id, image_id, image, sha))
        print(f"{subject['key']}: job {job_id}, ArtImage {image_id}, "
              f"{image.width}x{image.height}, SHA256 {sha[:16]}, accessible")
    assert len(loaded) == 9
    review_sheet(loaded, args.sheet)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps({
        "round": "gamebook-16-scene-fidelity",
        "fetched": 9,
        "complete": True,
        "candidates": [
            {"section": s["section"], "seed": s["seed"], "artJobId": j,
             "artImageId": a, "width": image.width, "height": image.height,
             "sha256": sha, "verified": True, "editorialVerdict": "pending"}
            for s, j, a, image, sha in loaded
        ],
    }, indent=2) + "\n")
    print("Verified nine private ArtImage URLs and created local editorial review sheet")
    return 0


if __name__ == "__main__":
    sys.exit(main())
