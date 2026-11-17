#!/usr/bin/env python3
"""Private SDXL targeted-edit diagnostics: no new ArtJobs and no KEEP decisions."""
from __future__ import annotations

import argparse
import base64
import io
import json
import sys
from pathlib import Path

import yaml
from PIL import Image, ImageChops, ImageDraw, ImageStat

ART = Path(__file__).resolve().parent
ROOT = ART.parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from enqueue_art_requests import (  # noqa: E402
    build_targeted_request, compose_source, fetch_source_image, core,
)


def decode_image(data: str) -> Image.Image:
    if not isinstance(data, str) or not data.startswith("data:image/"):
        raise ValueError("Expected an authenticated image data URL")
    raw = base64.b64decode(data.split(",", 1)[1], validate=True)
    image = Image.open(io.BytesIO(raw))
    image.load()
    return image


def position_mask(image: Image.Image, crop: dict, size: tuple[int, int]) -> Image.Image:
    x, y, w, h = (int(crop[key]) for key in ("x", "y", "width", "height"))
    if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > size[0] or y + h > size[1]:
        raise ValueError("Invalid crop bounds for original image")
    if image.width < w or image.height < h:
        raise ValueError("Mask smaller than reported crop")
    canvas = Image.new("L", size, 0)
    canvas.paste(image.convert("L").crop((0, 0, w, h)), (x, y))
    return canvas


def metrics(source: Image.Image, edited: Image.Image, hard: Image.Image,
            soft: Image.Image, crop: dict) -> dict:
    source, edited = source.convert("RGB"), edited.convert("RGB")
    if source.size != edited.size:
        raise ValueError("Original and edit must have identical dimensions")
    hard_full = position_mask(hard, crop, source.size)
    soft_full = position_mask(soft, crop, source.size)
    if ImageChops.subtract(soft_full, hard_full).getbbox():
        raise ValueError("Soft mask escapes pixel-locked hard mask")
    masked = hard_full.point(lambda x: 255 if x >= 128 else 0)
    count = masked.histogram()[255]
    if not count or count == source.width * source.height:
        raise ValueError("Target mask must be nonempty and not cover entire image")
    diff = ImageChops.difference(source, edited)
    r, g, b = diff.split()
    significant = ImageChops.lighter(ImageChops.lighter(r, g), b).point(
        lambda x: 255 if x >= 16 else 0
    )
    in_changed = ImageChops.multiply(significant, masked).histogram()[255]
    outside = ImageChops.invert(masked)
    out_changed = ImageChops.multiply(significant, outside).histogram()[255]
    return {
        "size": list(source.size),
        "mask_pixels": count,
        "mask_fraction": round(count / (source.width * source.height), 6),
        "inside_changed_fraction_at_16": round(in_changed / count, 6),
        "outside_changed_fraction_at_16": round(
            out_changed / (source.width * source.height - count), 6
        ),
        "inside_mean_absolute_rgb": [round(v, 3) for v in ImageStat.Stat(diff, mask=masked).mean],
        "outside_mean_absolute_rgb": [round(v, 3) for v in ImageStat.Stat(diff, mask=outside).mean],
        "nontrivial_edit": in_changed / count >= 0.02,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    ledger = yaml.safe_load((ART / "SDXL-TARGETED-CORRECTION-PILOT-1.yaml").read_text())
    subject, lane = ledger["subjects"][0], ledger["lanes"][0]
    job = subject.get("jobs", {}).get(lane["key"])
    art = subject.get("art", {}).get(lane["key"], {})
    if not job or art.get("status") != "DONE" or not art.get("art_image_id"):
        raise ValueError("Targeted V6 ArtJob and ArtImage must be completed")
    source_data = compose_source(subject, fetch_source_image)
    source = decode_image(source_data)
    edited = decode_image(fetch_source_image(art["art_image_id"]))
    request = build_targeted_request(ledger, lane, subject, source_data)
    request["previewOnly"] = True
    status, response = core.http_json(
        "POST", core.KR_BASE_URL.rstrip("/") + "/api/art/inpaint-targets",
        request, timeout=90,
    )
    data = response.get("data", {}) if isinstance(response, dict) else {}
    if status != 200 or not data.get("previewOnly"):
        raise RuntimeError(f"previewOnly failed: HTTP {status}")
    crop = data["crop"]
    hard, soft = decode_image(data["noiseMaskData"]), decode_image(data["compositeMaskData"])
    summary = metrics(source, edited, hard, soft, crop)
    summary.update({
        "art_job_id": job,
        "art_image_id": art["art_image_id"],
        "source_image_id": subject["source_image_id"],
        "crop": crop,
        "source_hash": data["sourceHash"],
        "editorial_verdict": art.get("verdict"),
        "note": "Mask/pixel evidence only; nontrivial change does not imply art acceptance",
    })
    (args.out / "diagnostic.json").write_text(json.dumps(summary, indent=2) + "\n")
    position_mask(hard, crop, source.size).save(args.out / "hard-mask.png")
    position_mask(soft, crop, source.size).save(args.out / "soft-mask.png")
    overlay = edited.convert("RGB")
    draw = ImageDraw.Draw(overlay)
    x, y, w, h = (int(crop[k]) for k in ("x", "y", "width", "height"))
    draw.rectangle((x, y, x + w, y + h), outline="#ea2a22", width=4)
    overlay.save(args.out / "output-crop.jpg", quality=90)
    print(json.dumps({k: v for k, v in summary.items() if k != "source_hash"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
