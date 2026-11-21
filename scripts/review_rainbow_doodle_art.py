#!/usr/bin/env python3
"""Build private, before/after contact sheets for Rainbow DOODLE-SET-2.

All 35 completed ArtJobs must still be inspected. This tool never changes the
keeper decisions, shipped sprites, or gameplay. A green-margin check is only
an aid to human visual inspection, never an automatic artistic approval.

python scripts/review_rainbow_doodle_art.py --kind-robots ../kind_robots
python scripts/review_rainbow_doodle_art.py --kind-robots ../kind_robots --offline
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent))
import export_rainbow_doodle_art as exporter

LEDGER = exporter.PROJECT / "art/DOODLE-SET-2.yaml"
OUTPUT = Path(".cache/rainbow-doodle-review")
SPRITE_FOLDERS = {"ships", "enemies", "bosses", "pickups"}
COLUMN_WIDTH = 244
IMAGE_HEIGHT = 190
CAPTION_HEIGHT = 56
BACKGROUND = (28, 18, 48)


def group_for(rel: str) -> str:
    folder = rel.split("/", 1)[0]
    return "cast" if folder in {"comms", "portraits"} else folder


def clear_green_border(image: Image.Image) -> bool:
    """A warning signal, not an art verdict: the outer rim should be green."""
    rgb = image.convert("RGB")
    width, height = rgb.size
    if width < 4 or height < 4:
        return False
    pixels = rgb.load()
    edge = (
        [(x, 0) for x in range(width)]
        + [(x, height - 1) for x in range(width)]
        + [(0, y) for y in range(1, height - 1)]
        + [(width - 1, y) for y in range(1, height - 1)]
    )
    greens = 0
    for x, y in edge:
        r, g, b = pixels[x, y]
        if g > 120 and g > r * 1.4 and g > b * 1.4:
            greens += 1
    return greens / len(edge) >= 0.95


def tile(image: Image.Image, *, colour=BACKGROUND) -> Image.Image:
    """Preserve aspect ratio, transparency, and the actual uncropped border."""
    cell = Image.new("RGBA", (COLUMN_WIDTH, IMAGE_HEIGHT), (*colour, 255))
    thumb = ImageOps.contain(
        image.convert("RGBA"), (COLUMN_WIDTH - 16, IMAGE_HEIGHT - 12),
        Image.Resampling.LANCZOS,
    )
    cell.alpha_composite(
        thumb, ((cell.width - thumb.width) // 2, (cell.height - thumb.height) // 2)
    )
    return cell.convert("RGB")


def load_render(subjects: list[dict], subject: dict, cache: Path, offline: bool) -> Path:
    image_id = exporter.finished_id(subject)
    if not image_id:
        raise RuntimeError(f"{subject['asset']}: no finished ArtImage")
    rel = subject["asset"].split("/doodle/", 1)[1]
    cached = cache / f"{rel}-{image_id}.png"
    if offline:
        if not cached.is_file():
            raise FileNotFoundError(f"{subject['asset']}: missing cached ArtImage {image_id}")
        return cached
    rendered = exporter.render_path(subjects, rel, cache)
    if rendered is None:
        raise RuntimeError(f"{subject['asset']}: render could not be retrieved")
    return rendered


def draw_group(
    rows: list[tuple[dict, Image.Image, Image.Image, Image.Image | None, str]],
    destination: Path,
) -> None:
    """Each row: shipped classic, raw re-render, keyed sprite (when relevant)."""
    row_height = IMAGE_HEIGHT + CAPTION_HEIGHT
    sheet = Image.new("RGB", (3 * COLUMN_WIDTH, len(rows) * row_height), BACKGROUND)
    pen = ImageDraw.Draw(sheet)
    for index, (entry, classic, render, keyed, edge_status) in enumerate(rows):
        top = index * row_height
        for column, image in enumerate((classic, render, keyed)):
            if image is not None:
                sheet.paste(tile(image), (column * COLUMN_WIDTH, top))
        rel = entry["asset"].split("/doodle/", 1)[1]
        label = rel if len(rel) <= 43 else rel[:40] + "..."
        pen.text((8, top + IMAGE_HEIGHT + 2), label, fill="#ffffff")
        pen.text(
            (8, top + IMAGE_HEIGHT + 22),
            f"Job {entry['job_id']} / Image {entry['art_image_id']} / {edge_status}",
            fill="#f8bfdc" if edge_status == "edge-risk" else "#b7eccc",
        )
        if index == 0:
            pen.text((COLUMN_WIDTH + 8, top + 8), "NEW RENDER", fill="#ffffff")
            if keyed is not None:
                pen.text((2 * COLUMN_WIDTH + 8, top + 8), "KEYED", fill="#ffffff")
    destination.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(destination, "WEBP", quality=86)


def generate_review(
    kind_robots: Path,
    output: Path,
    cache: Path,
    *,
    offline: bool = False,
    ledger: Path = LEDGER,
) -> dict:
    subjects = yaml.safe_load(ledger.read_text())["subjects"]
    if not subjects:
        raise RuntimeError("Rainbow doodle review ledger is empty")
    groups: dict[str, list] = {}
    report: list[dict] = []
    for subject in subjects:
        asset = subject["asset"]
        if not asset.startswith(f"{exporter.ART}/doodle/"):
            raise ValueError(f"unexpected art target: {asset}")
        rel = asset.split("/doodle/", 1)[1]
        image_id = exporter.finished_id(subject)
        if not image_id:
            raise RuntimeError(f"{rel}: not DONE; review cannot be complete")
        classic_path = exporter.classic_file(kind_robots, rel)
        if not classic_path.is_file():
            raise FileNotFoundError(f"{rel}: missing shipped classic {classic_path}")
        raw = load_render(subjects, subject, cache, offline)
        with Image.open(classic_path) as src:
            classic = src.convert("RGBA")
        with Image.open(raw) as src:
            rendered = src.convert("RGB")
        sprite = rel.split("/", 1)[0] in SPRITE_FOLDERS
        border = (
            "clear-border" if clear_green_border(rendered) else "edge-risk"
        ) if sprite else "not-a-sprite"
        keyed = exporter.key_green(rendered) if sprite else None
        group = group_for(rel)
        job_id = next(
            (job for job in (subject.get("jobs") or {}).values() if job), None
        )
        entry = {
            "asset": asset,
            "art_job_id": job_id,
            "art_image_id": image_id,
            "source_image_id": subject.get("source_image_id"),
            "review_group": group,
            "edge_check": border,
            "verdict": "PENDING_VISUAL_INSPECTION",
        }
        groups.setdefault(group, []).append(
            (
                {"asset": asset, "job_id": job_id, "art_image_id": image_id},
                classic, rendered, keyed, border,
            )
        )
        report.append(entry)
    output.mkdir(parents=True, exist_ok=True)
    for group, rows in groups.items():
        draw_group(rows, output / f"{group}.webp")
    manifest = {
        "project": "rainbow-bullet-hell-space-princess",
        "source_ledger": str(ledger),
        "status": "PENDING_VISUAL_INSPECTION",
        "sheets": sorted(f"{name}.webp" for name in groups),
        "assets": report,
    }
    (output / "visual-review.yaml").write_text(
        yaml.safe_dump(manifest, sort_keys=False)
    )
    return manifest


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind-robots", default="../kind_robots")
    parser.add_argument("--output-dir", default=str(OUTPUT))
    parser.add_argument("--cache", default=".cache/rainbow-doodle")
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args(argv)
    manifest = generate_review(
        Path(args.kind_robots), Path(args.output_dir),
        Path(args.cache), offline=args.offline,
    )
    print(
        f"{len(manifest['assets'])} ArtImages for visual review in {args.output_dir}; "
        "no keeper verdicts changed"
    )
    edge_risks = [
        entry for entry in manifest["assets"] if entry["edge_check"] == "edge-risk"
    ]
    print(f"{len(edge_risks)} edge-risk sprite(s) need visual inspection:")
    for entry in edge_risks:
        rel = entry["asset"].split("/doodle/", 1)[1]
        print(f"  {rel} (ArtImage {entry['art_image_id']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
