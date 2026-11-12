#!/usr/bin/env python3
"""Build evidence-only contact sheets of *actual* Shifting Desks rendered media.

No image is approved by this program. The latest ledger row per destination is
the authority for which render needs review. Save previews, filenames, prompts
and HTTP evidence in an Actions artifact so an editor can judge KEEP or REDO.
"""
from __future__ import annotations

import argparse
import io
import json
import math
import urllib.error
import urllib.request
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont, ImageOps

ART = Path(__file__).resolve().parent
HOST = "https://media.acrocatranch.com/images/shifting-desks/"
PREFIX = "kind_robots public/images/shifting-desks/"


def latest_unreviewed(art_dir: Path = ART, only_round: int | None = None) -> list[dict]:
    rows: dict[str, dict] = {}
    for ledger in sorted(
        art_dir.glob("ROUND-*.yaml"),
        key=lambda path: int(path.stem.split("-")[-1]),
    ):
        number = int(ledger.stem.split("-")[-1])
        data = yaml.safe_load(ledger.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        for row in data.get("subjects") or []:
            if not isinstance(row, dict):
                continue
            target = str(row.get("target_path") or "")
            if not target.startswith(PREFIX) or not target.endswith(".webp"):
                continue
            rows[target] = {**row, "_round": number, "_target": target}
    return [
        row for row in rows.values()
        if not str(row.get("verdict") or "").lower().startswith("keep")
        and (only_round is None or row["_round"] == only_round)
    ]


def image_from_media(row: dict, timeout: int = 20) -> tuple[Image.Image | None, dict]:
    target = row["_target"][len(PREFIX):]
    url = HOST + target
    if ".." in target or not target.replace("-", "").replace("_", "").replace(".", "").replace("/", "").isalnum():
        return None, {"error": "unsafe image path"}
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "KindRobots-ShiftingDesks-VisualQA/1.0"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            mime = response.headers.get("Content-Type", "").split(";")[0].strip()
            data = response.read(2_500_001)
            info = {
                "http": response.status,
                "mime": mime,
                "bytes": len(data),
                "last_modified": response.headers.get("Last-Modified"),
            }
        if mime != "image/webp" or len(data) < 1024 or len(data) > 2_500_000:
            return None, {**info, "error": "invalid media content"}
        img = Image.open(io.BytesIO(data))
        img.load()
        if img.width < 256 or img.height < 256:
            return None, {**info, "error": "unexpected dimensions"}
        return img.convert("RGB"), {**info, "dimensions": [img.width, img.height]}
    except (urllib.error.URLError, OSError, ValueError) as exc:
        return None, {"error": type(exc).__name__}


def build_sheet(entries: list[dict], out: Path, index: int) -> None:
    columns, rows = 4, math.ceil(len(entries) / 4)
    cell_w, cell_h = 340, 490
    sheet = Image.new("RGB", (columns * cell_w, rows * cell_h + 55), "#e7dfd3")
    draw = ImageDraw.Draw(sheet)
    draw.text((14, 14), f"SHIFTING DESKS / UNREVIEWED ART / PAGE {index + 1}", fill="#191919")
    for j, entry in enumerate(entries):
        x = (j % columns) * cell_w
        y = (j // columns) * cell_h + 55
        img = entry.get("_image")
        if img:
            fitted = ImageOps.contain(img, (cell_w - 12, 422))
            sheet.paste(fitted, (x + (cell_w - fitted.width) // 2, y + 2))
        else:
            draw.rectangle((x + 5, y + 5, x + cell_w - 5, y + 420), outline="#b02020", width=4)
            draw.text((x + 14, y + 20), "MISSING / UNREADABLE", fill="#b02020")
        label = f"{entry.get('_round')} / {entry.get('key')}"
        draw.text((x + 10, y + 433), label[:49], fill="#151515")
        draw.text((x + 10, y + 455), f"#{entry['_index']:03} {entry.get('status')} {entry.get('art_job_id')}", fill="#424242")
    sheet.save(out, quality=85, optimize=True)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--round", type=int, default=None)
    p.add_argument("--limit", type=int, default=None)
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    previews = args.out / "previews"
    previews.mkdir(exist_ok=True)
    entries = latest_unreviewed(only_round=args.round)
    if args.limit:
        entries = entries[:args.limit]
    records = []
    for n, row in enumerate(entries, start=1):
        img, evidence = image_from_media(row)
        row["_image"] = img
        row["_index"] = n
        if img:
            img.save(previews / f"{n:03}-{row.get('key')}.jpg", quality=85)
        records.append({
            "number": n,
            "key": row.get("key"),
            "round": row["_round"],
            "path": row["_target"],
            "prompt": row.get("prompt", ""),
            "status": row.get("status", ""),
            "verdict": row.get("verdict"),
            "job_id": row.get("art_job_id"),
            "image_id": row.get("art_image_id"),
            "evidence": evidence,
        })
        if n % 24 == 0:
            print(f"Downloaded {n}/{len(entries)} images", flush=True)
    for i in range(0, len(entries), 12):
        build_sheet(entries[i:i+12], args.out / f"contact-{i//12+1:02}.jpg", i//12)
    (args.out / "manifest.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    summary = {
        "selected": len(entries),
        "received": sum(1 for row in entries if row["_image"] is not None),
        "missing": sum(1 for row in entries if row["_image"] is None),
        "pages": math.ceil(len(entries) / 12),
    }
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary), flush=True)
    return 0 if summary["received"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
