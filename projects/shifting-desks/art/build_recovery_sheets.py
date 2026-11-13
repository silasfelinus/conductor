#!/usr/bin/env python3
"""Capture current, independently delivered Classic art and private Western pilot images.

Writes review-only JPG previews, contact sheets, and a provenance manifest.
Never marks KEEP, updates images, submits ArtJobs or publishes the private pilot.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import email.utils
import io
import json
import sys
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageOps

ART = Path(__file__).resolve().parent
ROOT = ART.parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from build_review_sheets import image_from_media  # noqa: E402
from enqueue_art_requests import fetch_source_image  # noqa: E402

ROUNDS = (13, 14, 15, 17)
LIMIT = 2_500_000


def latest_classic():
    latest = {}
    for number in ROUNDS:
        data = yaml.safe_load((ART / f"ROUND-{number}.yaml").read_text(encoding="utf-8"))
        for row in data["subjects"]:
            latest[row["target_path"]] = {**row, "_round": number, "_target": row["target_path"]}
    return [row for row in latest.values() if not row.get("verdict")]


def current_media_evidence(row, evidence):
    """The freshly fetched media must be no older than the ledger's ArtJob-delivered media."""
    stamp = evidence.get("last_modified")
    report = str(row.get("delivery_check") or "")
    if str(row.get("status") or "").strip('"') != "delivered":
        return False
    if not stamp or "confirmed newer than ArtJob" not in report:
        return False
    try:
        now = email.utils.parsedate_to_datetime(stamp).astimezone(dt.timezone.utc)
        ledger_stamp = report.split("Last-Modified ", 1)[1].split(";", 1)[0]
        old = dt.datetime.fromisoformat(ledger_stamp).astimezone(dt.timezone.utc)
    except (IndexError, ValueError, TypeError):
        return False
    return now >= old


def pilot_rows():
    data = yaml.safe_load((ART / "SUBJECT-FIDELITY-PILOT-V1.yaml").read_text(encoding="utf-8"))
    for subject in data["subjects"]:
        for lane in data["lanes"]:
            key = lane["key"]
            job = (subject.get("jobs") or {}).get(key)
            art = (subject.get("art") or {}).get(key) or {}
            yield {
                "_round": "PILOT",
                "key": subject["key"] + "--" + key,
                "prompt": subject.get("prompt_tags") if lane.get("prompt") == "tags" else subject.get("prompt_prose"),
                "negative": subject.get("negative"),
                "job": job,
                "image": art.get("art_image_id"),
                "status": art.get("status", "not-recorded"),
                "lane": key,
            }


def capture_pilot(row):
    if row["status"] != "DONE" or not row["image"]:
        return None, {"error": "ArtJob not recorded as DONE with an ArtImage"}
    try:
        data_url = fetch_source_image(row["image"])
        mime, encoded = data_url.split(",", 1)
        raw = base64.b64decode(encoded, validate=True)
        if not mime.startswith("data:image/") or not 1024 <= len(raw) <= LIMIT:
            return None, {"error": "unexpected image content"}
        image = Image.open(io.BytesIO(raw))
        image.load()
        if image.width < 256 or image.height < 256:
            return None, {"error": "unexpected image dimensions"}
        return image.convert("RGB"), {"bytes": len(raw), "dimensions": [image.width, image.height]}
    except (OSError, RuntimeError, ValueError, TimeoutError) as exc:
        return None, {"error": type(exc).__name__}


def sheets(rows, directory, label):
    directory.mkdir(parents=True, exist_ok=True)
    previews = directory / "previews"
    previews.mkdir(exist_ok=True)
    records = []
    for i, row in enumerate(rows, 1):
        image = row.get("_image")
        if image:
            image.save(previews / f"{i:03}-{row['key']}.jpg", quality=91)
        records.append({k: v for k, v in row.items() if not k.startswith("_") or k == "_round"})
        records[-1]["number"] = i
    for start in range(0, len(rows), 12):
        batch = rows[start:start + 12]
        w, h = 400, 600
        result = Image.new("RGB", (w * 4, h * 3), "#e9e1d4")
        draw = ImageDraw.Draw(result)
        for n, row in enumerate(batch):
            x = (n % 4) * w
            y = (n // 4) * h
            if row.get("_image"):
                fitted = ImageOps.contain(row["_image"], (w - 18, h - 74))
                result.paste(fitted, (x + (w - fitted.width) // 2, y + 5))
            else:
                draw.rectangle((x + 5, y + 5, x + w - 5, y + h - 68), outline="#b32323", width=4)
                draw.text((x + 18, y + 20), "UNAVAILABLE / PENDING", fill="#9c1111")
            draw.text((x + 10, y + h - 63), f"{label} #{start+n+1:02d}: {row['key']}"[:64], fill="#151515")
            draw.text((x + 10, y + h - 39), f"ArtJob {row.get('job')} / ArtImage {row.get('image')}", fill="#494949")
        result.save(directory / f"contact-{start // 12 + 1:02d}.jpg", quality=92)
    (directory / "manifest.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    return sum(bool(r.get("_image")) for r in rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    classic = []
    for row in latest_classic():
        img, evidence = image_from_media(row)
        fresh = bool(img) and current_media_evidence(row, evidence)
        classic.append({
            "_round": row["_round"], "key": row["key"],
            "prompt": row.get("prompt"), "verdict": row.get("verdict"),
            "status": row.get("status"), "job": row.get("art_job_id"),
            "image": row.get("art_image_id"), "path": row.get("_target"),
            "evidence": evidence, "fresh": fresh, "_image": img if fresh else None,
        })
    private = []
    for row in pilot_rows():
        image, evidence = capture_pilot(row)
        private.append({**row, "evidence": evidence, "_image": image})
    c = sheets(classic, args.out / "classic", "CLASSIC")
    p = sheets(private, args.out / "pilot", "PILOT")
    summary = {"classic_captured_newer": c, "classic_expected": len(classic),
               "pilot_captured": p, "pilot_expected": len(private)}
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary), flush=True)
    return 0 if c == len(classic) and c == 20 else 1


if __name__ == "__main__":
    raise SystemExit(main())
