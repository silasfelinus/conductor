#!/usr/bin/env python3
"""
Consume the dedicated Monster Recast unapproved-concepts queue.

The compact queue stores concept IDs plus per-variant status. Scene prompts come
from art-modeler-request.yaml, so the production brief remains the source of
truth. Each pending color or black-and-white variant becomes a real kind_robots
ArtJob through the same client used by the main autonomous art workflow.

Color and BW use the same deterministic seed and scene prompt. These are paired
first-pass studies, not guaranteed source-image conversions; stage-two review
decides whether a BW candidate is faithful enough or needs Kontext refinement.
"""

from __future__ import annotations

import argparse
import base64
import io
import re
import sys
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).parent))
import consume_art_queue as consumer  # noqa: E402
import art_quality  # noqa: E402

ROOT = consumer.ROOT
SET_DIR = ROOT / "projects" / "coloring-book" / "sets" / "monster-recast"
QUEUE_FILE = SET_DIR / "unapproved-art-jobs.yaml"

# COLOR is applied as a SUFFIX (subject first, style after) so Flux weights the
# distinctive character/scene ahead of the house look — front-loading the style
# block was collapsing concepts into generic posters. See
# IMAGE-GEN-QUALITY-REVIEW.md 2a.
COLOR_SUFFIX = (
    " Render this as a finished Monster Recast colored graphic master, portrait 3:4: "
    "thick confident black contours, flat bounded color, hard-edged value shapes, high "
    "organized detail, strong silhouette, serious theatrical camp, physically coherent "
    "anatomy and contact points. One full-bleed image filling the frame edge to edge, no "
    "border, no framing panel, no comic panels, no collage, no contact sheet, no soft "
    "gradients or airbrush haze, and no readable text, logo, or watermark."
)

# BW is the one variant where the MEDIUM defines the deliverable, so it leads.
# The scene is described as subject matter to depict in ink; then the no-color
# rule is restated after the (color-laden) scene words. Negatives are inert on
# the Flux path (cfg=1), so every constraint here is stated positively. A
# colorfulness guard in the live path (art_quality.assess) rejects any BW render
# that still comes back in color — the exact mr-010/mr-013 failure.
BW_LEAD = (
    "Black-and-white ink line art for a teen-and-adult coloring book: pure white "
    "background, clean bold black outlines and varied medium interior line weight only, "
    "absolutely no color and no gray shading. Depict this subject entirely as uncolored "
    "black-outline line art — "
)
BW_TAIL = (
    " Draw every element as closed black-outline regions on a white page with NO color "
    "fills, NO shading, NO halftone, and NO dense crosshatching. Preserve the pose, body "
    "type, anatomy, perspective, costume detail, horror premise and theatrical-camp joke, "
    "with high detail on the face, hands, signature prop and creature texture. Fill the "
    "frame edge to edge — no border, no framing panel, no comic panels, no collage, no "
    "contact sheet, and no readable text, logo, or watermark."
)

CONCEPT_START = re.compile(r'^(\s*)-\s+id:\s*["\']?(mr-\d+)["\']?\s*$')
STATUS_LINE = re.compile(
    r'^(\s*)(color_status|bw_status):\s*["\']?[A-Za-z0-9_-]+["\']?\s*(#.*)?$'
)


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise RuntimeError(f"Expected YAML mapping: {path}")
    return data


def clean(value: Any) -> str:
    return " ".join(str(value or "").split())


def source_entries(source_path: Path) -> dict[str, dict[str, Any]]:
    data = load_yaml(source_path)
    entries = (data.get("batch") or {}).get("entries") or []
    return {
        str(entry["id"]): entry
        for entry in entries
        if isinstance(entry, dict) and entry.get("id") and entry.get("prompt")
    }


def build_entries() -> list[dict[str, Any]]:
    queue = load_yaml(QUEUE_FILE)
    source_path = ROOT / str(queue["source_manifest"])
    source_by_id = source_entries(source_path)
    defaults = queue.get("defaults") or {}
    concepts = queue.get("concepts") or []
    entries: list[dict[str, Any]] = []

    for concept in concepts:
        if not isinstance(concept, dict):
            continue

        concept_id = str(concept.get("id") or "")
        slug = str(concept.get("slug") or "")
        source = source_by_id.get(concept_id)

        if not concept_id or not slug or not source:
            raise RuntimeError(f"Missing source prompt for {concept_id or slug}")

        number = int(concept_id.split("-")[1])
        seed = 740000 + number
        title = clean(source.get("label"))
        scene_prompt = clean(source.get("prompt"))

        shared = {
            "project": "coloring-book",
            "set": "monster-recast",
            "concept_id": concept_id,
            "title": title,
            "target_repo": defaults.get("target_repo", "silasfelinus/conductor"),
            "size": str(defaults.get("size", "1024x1536")),
            "engine": str(defaults.get("engine", "flux")),
            "flux_variant": str(defaults.get("flux_variant", "dev")),
            "steps": int(defaults.get("steps", 36)),
            "guidance": float(defaults.get("guidance", 3.5)),
            "seed": seed,
            "pair_id": f"{concept_id}-{slug}",
            "source_file": str(queue["source_manifest"]),
        }

        if str(concept.get("color_status") or "pending").lower() == "pending":
            entries.append(
                {
                    "id": f"monster-recast-{concept_id}-color",
                    **shared,
                    "variant": "color",
                    "image_path": (
                        "projects/coloring-book/sets/monster-recast/generated/color/"
                        f"{concept_id}-{slug}.webp"
                    ),
                    "prompt": scene_prompt + COLOR_SUFFIX,
                }
            )

        if str(concept.get("bw_status") or "pending").lower() == "pending":
            entries.append(
                {
                    "id": f"monster-recast-{concept_id}-bw",
                    **shared,
                    "variant": "bw",
                    "image_path": (
                        "projects/coloring-book/sets/monster-recast/generated/bw/"
                        f"{concept_id}-{slug}.webp"
                    ),
                    "prompt": BW_LEAD + scene_prompt + BW_TAIL,
                }
            )

    return entries


def target_path(entry: dict[str, Any]) -> Path:
    return ROOT / str(entry["image_path"])


def set_variant_status(
    text: str,
    concept_id: str,
    variant: str,
    new_status: str,
) -> tuple[str, bool]:
    lines = text.splitlines(keepends=True)
    starts: list[tuple[int, str, str]] = []

    for index, line in enumerate(lines):
        match = CONCEPT_START.match(line)
        if match:
            starts.append((index, match.group(1), match.group(2)))

    field = f"{variant}_status"

    for position, (start, indent, found_id) in enumerate(starts):
        if found_id != concept_id:
            continue

        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)

        for index in range(start + 1, end):
            match = STATUS_LINE.match(lines[index])
            if match and match.group(2) == field:
                lines[index] = f"{match.group(1)}{field}: {new_status}\n"
                return "".join(lines), True

        lines.insert(start + 1, f"{indent}  {field}: {new_status}\n")
        return "".join(lines), True

    return text, False


def mark_done(entries: list[dict[str, Any]]) -> int:
    if not entries:
        return 0

    text = QUEUE_FILE.read_text(encoding="utf-8")
    changed = 0

    for entry in entries:
        text, did_change = set_variant_status(
            text,
            str(entry["concept_id"]),
            str(entry["variant"]),
            "done",
        )
        if did_change:
            changed += 1

    if changed:
        QUEUE_FILE.write_text(text, encoding="utf-8")

    return changed


def save_result(entry: dict[str, Any], image_b64: str) -> Path:
    destination = target_path(entry)
    destination.parent.mkdir(parents=True, exist_ok=True)
    image_bytes = base64.b64decode(image_b64)

    if destination.suffix.lower() == ".webp":
        try:
            from PIL import Image

            image = Image.open(io.BytesIO(image_bytes))
            image.save(destination, "WEBP", quality=92, method=6)
            return destination
        except ImportError as error:
            raise RuntimeError("Pillow is required for WebP output.") from error

    destination.write_bytes(image_bytes)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()

    pending = build_entries()
    already_present = [entry for entry in pending if target_path(entry).exists()]
    todo = [entry for entry in pending if not target_path(entry).exists()]

    if args.limit > 0:
        todo = todo[: args.limit]

    if already_present and args.live:
        mark_done(already_present)

    if not todo:
        print("No pending Monster Recast ArtJobs.")
        return 0

    print(
        f"{'LIVE' if args.live else 'DRY RUN'}: "
        f"{len(todo)} Monster Recast ArtJob(s) via {consumer.KR_BASE_URL}"
    )

    if not args.live:
        for entry in todo:
            job = consumer.entry_to_job(entry)
            print(
                f"  {entry['concept_id']} {entry['variant']} -> "
                f"{entry['image_path']} "
                f"[{job['payload']['width']}x{job['payload']['height']}] "
                f"seed={entry['seed']}"
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
            print(
                f"  queued ArtJob {job_id} for "
                f"{entry['concept_id']} {entry['variant']} - waiting..."
            )
            job = consumer.wait_for_job(job_id, args.timeout)
            image_b64 = consumer.fetch_image_b64(job["artImageId"])
            destination = save_result(entry, image_b64)

            # Objective quality guard: a "bw" render that came back colored, or a
            # blank/degenerate frame, is NOT a real deliverable. Reject it (move
            # aside, leave the variant pending) instead of marking it done and
            # letting it pollute the set — the mr-010/mr-013 failure mode.
            ok, reasons, _info = art_quality.assess_file(destination, str(entry["variant"]))
            if ok is False:
                rejected = destination.parent / "rejected" / destination.name
                rejected.parent.mkdir(parents=True, exist_ok=True)
                destination.replace(rejected)
                failures += 1
                print(
                    f"  REJECTED {entry['concept_id']} {entry['variant']}: "
                    f"{'; '.join(reasons)} -> {rejected.relative_to(ROOT)} "
                    "(left pending for re-render)",
                    file=sys.stderr,
                )
                continue
            if ok is None:
                print(f"    NOTE: {reasons[0]} — cannot verify this render")

            completed.append(entry)
            print(
                f"  DONE {entry['concept_id']} {entry['variant']} -> "
                f"{destination.relative_to(ROOT)} (ArtImage {job['artImageId']})"
            )
        except Exception as error:  # noqa: BLE001
            failures += 1
            print(
                f"  FAILED {entry['concept_id']} {entry['variant']}: {error}",
                file=sys.stderr,
            )

    marked = mark_done(completed)
    print(
        f"{len(todo) - failures}/{len(todo)} succeeded; "
        f"{marked} variant statuses marked done."
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
