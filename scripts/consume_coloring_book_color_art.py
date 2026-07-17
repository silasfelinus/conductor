#!/usr/bin/env python3
"""Submit and retrieve canonical coloring-book COLOR proposal ArtJobs.

The queue contains all three 36-image books. A normal pass handles 18 color
proposals. Black-and-white work is deliberately excluded: BW is derived only
after Silas accepts a color composition.

Dry-run is the default. `--live` submits real kind_robots ArtJobs, waits for
results, saves them under each book's generated/color-proposals-v1 directory,
and marks only successfully landed renders as done.
"""

from __future__ import annotations

import argparse
import base64
import io
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).parent))
import art_quality  # noqa: E402
import consume_art_queue as consumer  # noqa: E402

ROOT = consumer.ROOT
QUEUE_FILE = ROOT / "projects" / "coloring-book" / "color-art-jobs.yaml"

COLOR_SUFFIX = (
    " Render this as a finished full-color coloring-book design master, portrait 2:3: "
    "one coherent full-bleed scene, thick confident black contours, crisp bounded color, "
    "hard-edged value shapes, high organized detail, strong readable silhouette, clear "
    "hands and contact points, and enough closed shapes to support a later faithful line-art "
    "conversion. Fill the frame edge to edge. No border, no comic panels, no collage, no "
    "contact sheet, no readable text, no watermark, no signature, no brand marks, no soft "
    "airbrush haze, and no painterly blur."
)

LOGO_SUFFIX = (
    " Render this as a finished full-color coloring-book design master, portrait 2:3: "
    "one coherent full-bleed scene, thick confident black contours, crisp bounded color, "
    "hard-edged value shapes, high organized detail, and a strong iconic silhouette. A "
    "recognizable emblem or mascot variation is allowed because this is the designated "
    "Kind Robots logo page, but include no readable words, letters, watermark, signature, "
    "border, comic panels, collage, contact sheet, soft airbrush haze, or painterly blur."
)


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise RuntimeError(f"Expected YAML mapping: {path}")
    return data


def clean(value: Any) -> str:
    return " ".join(str(value or "").split())


def find_source_prompt(source_ref: str) -> tuple[str, str]:
    path_text, sep, item_id = source_ref.partition("#")
    if not sep or not item_id:
        raise RuntimeError(f"Invalid source_ref: {source_ref}")
    path = ROOT / path_text
    doc = load_yaml(path)

    batch_entries = ((doc.get("batch") or {}).get("entries") or [])
    for entry in batch_entries:
        if isinstance(entry, dict) and str(entry.get("id")) == item_id:
            prompt = clean(entry.get("prompt"))
            if not prompt:
                raise RuntimeError(f"{source_ref}: source entry has no prompt")
            return clean(entry.get("label") or item_id), prompt

    proposals = doc.get("proposals") or []
    for proposal in proposals:
        if isinstance(proposal, dict) and str(proposal.get("id")) == item_id:
            prompt_obj = proposal.get("prompt") if isinstance(proposal.get("prompt"), dict) else {}
            prompt = clean(prompt_obj.get("text"))
            if not prompt:
                raise RuntimeError(f"{source_ref}: proposal has no direct prompt text")
            return clean(proposal.get("title") or item_id), prompt

    raise RuntimeError(f"{source_ref}: no matching entry")


def build_entries(book_filter: str | None = None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    queue = load_yaml(QUEUE_FILE)
    defaults = queue.get("defaults") if isinstance(queue.get("defaults"), dict) else {}
    books = queue.get("books") or []
    entries: list[dict[str, Any]] = []

    for book in books:
        if not isinstance(book, dict):
            continue
        book_slug = str(book.get("slug") or "")
        if book_filter and book_slug != book_filter:
            continue

        for source in book.get("entries") or []:
            if not isinstance(source, dict):
                continue
            status = str(source.get("status") or "pending").strip().lower()
            if status != "pending":
                continue

            title = clean(source.get("title"))
            scene_prompt = clean(source.get("prompt"))
            if source.get("source_ref"):
                resolved_title, resolved_prompt = find_source_prompt(str(source["source_ref"]))
                title = title or resolved_title
                scene_prompt = scene_prompt or resolved_prompt
            if not scene_prompt:
                raise RuntimeError(f"{book_slug}/{source.get('id')}: missing color prompt")

            suffix = LOGO_SUFFIX if source.get("allow_logo_emblem") else COLOR_SUFFIX
            entry = {
                "id": f"coloring-book-{book_slug}-{source['id']}-color",
                "queue_id": str(source["id"]),
                "project": "coloring-book",
                "set": book_slug,
                "concept_id": str(source["id"]),
                "title": title,
                "variant": "color",
                "image_path": str(source["image_path"]),
                "prompt": scene_prompt + suffix,
                "target_repo": defaults.get("target_repo", "silasfelinus/conductor"),
                "size": str(defaults.get("size", "1024x1536")),
                "engine": str(defaults.get("engine", "flux")),
                "flux_variant": str(defaults.get("flux_variant", "dev")),
                "steps": int(defaults.get("steps", 36)),
                "guidance": float(defaults.get("guidance", 3.5)),
                "seed": int(source.get("seed") or 0),
                "source_ref": source.get("source_ref"),
                "reference_images": source.get("reference_images") or [],
            }
            entries.append(entry)

    entries.sort(key=lambda item: (book_order(queue, str(item["set"])), slot_for(queue, str(item["queue_id"]))))
    return queue, entries


def book_order(queue: dict[str, Any], slug: str) -> int:
    for book in queue.get("books") or []:
        if isinstance(book, dict) and str(book.get("slug")) == slug:
            return int(book.get("order") or 999)
    return 999


def slot_for(queue: dict[str, Any], queue_id: str) -> int:
    for book in queue.get("books") or []:
        if not isinstance(book, dict):
            continue
        for entry in book.get("entries") or []:
            if isinstance(entry, dict) and str(entry.get("id")) == queue_id:
                return int(entry.get("slot") or 999)
    return 999


def target_path(entry: dict[str, Any]) -> Path:
    return ROOT / str(entry["image_path"])


def save_result(entry: dict[str, Any], image_b64: str) -> Path:
    destination = target_path(entry)
    destination.parent.mkdir(parents=True, exist_ok=True)
    image_bytes = base64.b64decode(image_b64)

    if destination.suffix.lower() == ".webp":
        try:
            from PIL import Image
        except ImportError as error:
            raise RuntimeError("Pillow is required for WebP output.") from error
        image = Image.open(io.BytesIO(image_bytes))
        image.save(destination, "WEBP", quality=92, method=6)
        return destination

    destination.write_bytes(image_bytes)
    return destination


def mark_done(completed: list[dict[str, Any]]) -> int:
    if not completed:
        return 0
    queue = load_yaml(QUEUE_FILE)
    by_id = {str(entry["queue_id"]): entry for entry in completed}
    changed = 0
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    for book in queue.get("books") or []:
        if not isinstance(book, dict):
            continue
        for entry in book.get("entries") or []:
            if not isinstance(entry, dict):
                continue
            done = by_id.get(str(entry.get("id")))
            if not done:
                continue
            entry["status"] = "done"
            entry["rendered_path"] = str(done["image_path"])
            if done.get("art_image_id") is not None:
                entry["art_image_id"] = int(done["art_image_id"])
            entry["completed_at"] = now
            changed += 1

    if changed:
        QUEUE_FILE.write_text(
            yaml.safe_dump(queue, sort_keys=False, allow_unicode=True, width=110),
            encoding="utf-8",
        )
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--limit", type=int, default=0, help="0 uses queue batch_policy.worker_pass_size")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--book", choices=("monster-recast", "hollywood-recast", "kind-robots"))
    args = parser.parse_args()

    queue, pending = build_entries(args.book)
    configured_limit = int(((queue.get("batch_policy") or {}).get("worker_pass_size")) or 18)
    limit = args.limit if args.limit > 0 else configured_limit

    already_present = [entry for entry in pending if target_path(entry).exists()]
    todo = [entry for entry in pending if not target_path(entry).exists()][:limit]

    if already_present and args.live:
        for entry in already_present:
            entry["art_image_id"] = None
        mark_done(already_present)

    if not todo:
        print("No pending coloring-book color ArtJobs.")
        return 0

    print(
        f"{'LIVE' if args.live else 'DRY RUN'}: {len(todo)} of {len(pending)} pending "
        f"color proposal ArtJob(s) via {consumer.KR_BASE_URL}; pass limit={limit}"
    )

    if not args.live:
        for entry in todo:
            job = consumer.entry_to_job(entry)
            refs = f" refs={len(entry.get('reference_images') or [])}" if entry.get("reference_images") else ""
            print(
                f"  {entry['set']}/{entry['concept_id']} -> {entry['image_path']} "
                f"[{job['payload']['width']}x{job['payload']['height']}] seed={entry['seed']}{refs}"
            )
        return 0

    if not consumer.KR_API_TOKEN:
        print("KR_API_TOKEN is required for --live.", file=sys.stderr)
        return 1

    completed: list[dict[str, Any]] = []
    failures = 0

    for entry in todo:
        try:
            job_id = consumer.enqueue(consumer.entry_to_job(entry))
            print(f"  queued ArtJob {job_id} for {entry['set']}/{entry['concept_id']} color - waiting...")
            job = consumer.wait_for_job(job_id, args.timeout)
            image_b64 = consumer.fetch_image_b64(job["artImageId"])
            destination = save_result(entry, image_b64)

            ok, reasons, _info = art_quality.assess_file(destination, "color")
            if ok is False:
                rejected = destination.parent / "rejected" / destination.name
                rejected.parent.mkdir(parents=True, exist_ok=True)
                destination.replace(rejected)
                failures += 1
                print(
                    f"  REJECTED {entry['set']}/{entry['concept_id']}: {'; '.join(reasons)} "
                    f"-> {rejected.relative_to(ROOT)} (left pending)",
                    file=sys.stderr,
                )
                continue
            if ok is None:
                print(f"    NOTE: {reasons[0]} — cannot fully verify this render")

            entry["art_image_id"] = int(job["artImageId"])
            completed.append(entry)
            print(
                f"  DONE {entry['set']}/{entry['concept_id']} -> "
                f"{destination.relative_to(ROOT)} (ArtImage {job['artImageId']})"
            )
        except Exception as error:  # noqa: BLE001
            failures += 1
            print(f"  FAILED {entry['set']}/{entry['concept_id']}: {error}", file=sys.stderr)

    marked = mark_done(completed)
    print(f"{len(todo) - failures}/{len(todo)} succeeded; {marked} queue entries marked done.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
