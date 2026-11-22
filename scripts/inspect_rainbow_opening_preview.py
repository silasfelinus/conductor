#!/usr/bin/env python3
"""Review an eight-shot Rainbow opening cut without publishing its media.

This does not replace visual acceptance: it produces a private contact sheet,
per-shot ArtJob receipts, format checks and a chroma-green warning for review.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import subprocess
import sys
from pathlib import Path

import yaml
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts import export_rainbow_opening as opening


def shot_timeline():
    elapsed = 0
    shots = []
    for key, beats in opening.DOODLE_SHOTS:
        start = elapsed * 60 / opening.BPM
        duration = beats * 60 / opening.BPM
        shots.append({"key": key, "start": start, "duration": duration})
        elapsed += beats
    if elapsed != 44:
        raise ValueError(f"Rainbow intro expected 44 beats, got {elapsed}")
    return shots


def validated_receipts(ledger):
    opening.validate_shot_coverage(ledger)
    if ledger.get("round") != opening.DOODLE_ROUND:
        raise ValueError("wrong opening ledger round")
    subjects = {shot["key"]: shot for shot in ledger["subjects"]}
    receipts = []
    for entry in shot_timeline():
        shot = subjects[entry["key"]]
        art = (shot.get("art") or {}).get("wan-mp4") or {}
        job = (shot.get("jobs") or {}).get("wan-mp4")
        image = art.get("art_image_id")
        if art.get("status") != "DONE" or type(job) is not int or type(image) is not int:
            raise ValueError(f"{entry['key']}: WAN clip not DONE with durable ArtJob and ArtImage")
        if job <= 0 or image <= 0:
            raise ValueError(f"{entry['key']}: invalid ArtJob or ArtImage")
        receipts.append({**entry, "art_job_id": job, "art_image_id": image})
    return receipts


def chroma_green_fraction(image):
    sample = image.convert("RGB").resize((160, 90))
    pixels = list(sample.getdata())
    bright_green = sum(
        1 for red, green, blue in pixels
        if green > 130 and green > 1.45 * red and green > 1.35 * blue
    )
    return round(bright_green / len(pixels), 4)


def video_frame(path, second):
    command = [
        "ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
        "-ss", f"{second:.3f}", "-i", str(path), "-frames:v", "1",
        "-vf", "scale=320:180", "-f", "image2pipe", "-vcodec", "png", "-",
    ]
    payload = subprocess.run(
        command, check=True, capture_output=True, timeout=45,
    ).stdout
    if not payload:
        raise RuntimeError(f"no frame at {second:.3f} seconds")
    with Image.open(io.BytesIO(payload)) as img:
        return img.convert("RGB")


def file_sha256(path):
    checksum = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            checksum.update(chunk)
    return checksum.hexdigest()


def inspect(video, ledger, output):
    receipts = validated_receipts(yaml.safe_load(ledger.read_text()))
    opening.verify_encoded_media(video, 15.0, require_audio=True)

    frames = []
    warnings = []
    for shot in receipts:
        midpoint = shot["start"] + shot["duration"] / 2
        frames.append(video_frame(video, midpoint))

    dolphin = next(shot for shot in receipts if shot["key"] == "intro-dolphin-armada")
    samples = [
        chroma_green_fraction(video_frame(
            video, dolphin["start"] + dolphin["duration"] * fraction,
        ))
        for fraction in (0.2, 0.5, 0.8)
    ]
    if max(samples) > 0.4:
        warnings.append(
            f"intro-dolphin-armada: dominant chroma-green frame ({max(samples):.1%})"
        )

    sheet = Image.new("RGB", (4 * 320, 2 * 204), "#120b26")
    draw = ImageDraw.Draw(sheet)
    for index, (shot, frame) in enumerate(zip(receipts, frames)):
        x = index % 4 * 320
        y = index // 4 * 204
        sheet.paste(frame, (x, y))
        draw.text(
            (x + 6, y + 184), shot["key"],
            fill="#f7d5ff",
        )
    output.mkdir(parents=True, exist_ok=True)
    sheet.save(output / "opening-contact-sheet.webp", "WEBP", quality=90)
    poster = video.with_name(f"{video.stem}-poster.webp")
    webm = video.with_suffix(".webm")
    if not poster.is_file() or not webm.is_file():
        raise ValueError("preview missing WebM or poster output")
    report = {
        "automated_review_passed": not warnings,
        "visual_acceptance_pending": True,
        "soundtrack_art_job_id": opening.TRACK_JOB_ID,
        "seconds": 15.0,
        "shots": receipts,
        "dolphin_chroma_green_fractions": samples,
        "warnings": warnings,
        "files_sha256": {
            path.name: file_sha256(path)
            for path in (video, webm, poster)
        },
    }
    (output / "opening-review.json").write_text(
        json.dumps(report, indent=2) + "\n",
    )
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", required=True, type=Path)
    parser.add_argument("--ledger", type=Path, default=opening.LEDGER)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    report = inspect(args.video, args.ledger, args.out)
    print(
        f"Rainbow opening: {len(report['shots'])}/8 WAN receipts; "
        f"green samples {report['dolphin_chroma_green_fractions']}; "
        f"warnings {len(report['warnings'])}"
    )
    return 0 if report["automated_review_passed"] else 2


if __name__ == "__main__":
    sys.exit(main())
