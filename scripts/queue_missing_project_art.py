#!/usr/bin/env python3
"""
queue_missing_project_art.py — build a dry-run art generation batch for project assets.

Reads projects/art-prompts.yaml, checks the image_path values under images:, and writes
projects/art-generate.yaml with up to --limit missing icon/card/hero requests.

Active entries already present in art-generate.yaml are preserved. This matters for manual
replacement batches: an automated missing-art refresh must not erase a pending retry merely
because the old target file still exists.

This script never calls the live art generator. It only creates a local queue file that
can be consumed by consume_art_queue.py or copied into the human image-generation workflow.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
PROMPT_CATALOG = ROOT / "projects" / "art-prompts.yaml"
OUTPUT_QUEUE = ROOT / "projects" / "art-generate.yaml"
PROJECT_IMAGE_REPO = "silasfelinus/conductor"
VARIANT_ORDER = ("icon", "card", "hero")
ACTIVE_QUEUE_STATUSES = {"pending", "queued", "running", "processing"}
DEFAULT_PROJECT_ART_ENGINE = (
    os.environ.get("PROJECT_ART_DEFAULT_ENGINE")
    or os.environ.get("PROJECT_ART_DEFAULT_MODEL")
    or "krea2"
).strip() or "krea2"


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Missing prompt catalog: {path}")
    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    if not isinstance(raw, dict):
        raise SystemExit(f"YAML file must contain a mapping: {path}")
    return raw


def is_pending_asset(asset: dict[str, Any]) -> bool:
    return str(asset.get("status", "pending")).lower() == "pending"


def iter_missing_project_assets(catalog: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    projects = catalog.get("images") or []
    if not isinstance(projects, list):
        raise SystemExit("projects/art-prompts.yaml images: must be a list")

    for project_entry in projects:
        if not isinstance(project_entry, dict):
            continue
        slug = project_entry.get("project")
        if not isinstance(slug, str) or not slug:
            continue

        for variant in VARIANT_ORDER:
            asset = project_entry.get(variant)
            if not isinstance(asset, dict) or not is_pending_asset(asset):
                continue

            image_path = asset.get("image_path")
            prompt = asset.get("prompt")
            size = asset.get("size")
            if not isinstance(image_path, str) or not isinstance(prompt, str):
                continue

            target = ROOT / image_path
            if target.exists():
                continue

            entry = {
                "project": slug,
                "variant": variant,
                "target_repo": PROJECT_IMAGE_REPO,
                "image_path": image_path,
                "size": str(size or default_size_for_variant(variant)),
                "status": "pending",
                "prompt": " ".join(prompt.split()),
            }
            engine = asset.get("engine") or asset.get("model") or DEFAULT_PROJECT_ART_ENGINE
            entry["engine"] = str(engine).strip() or DEFAULT_PROJECT_ART_ENGINE
            entries.append(entry)

    return entries


def load_active_queue_entries(path: Path) -> list[dict[str, Any]]:
    """Return only in-flight entries from an existing generated queue.

    Completed/failed history is intentionally not preserved: once a consumer marks a retry
    done, the next refresh may remove it. Pending work, however, must survive an automated
    refresh even when its target file already exists and is being intentionally replaced.
    """
    if not path.exists():
        return []

    raw = load_yaml(path)
    batch = raw.get("batch")
    if not isinstance(batch, dict):
        return []
    entries = batch.get("entries")
    if not isinstance(entries, list):
        return []

    active: list[dict[str, Any]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        status = str(entry.get("status", "pending")).strip().lower()
        if status in ACTIVE_QUEUE_STATUSES:
            active.append(dict(entry))
    return active


def queue_identity(entry: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(entry.get("target_repo") or PROJECT_IMAGE_REPO).strip(),
        str(entry.get("image_path") or "").strip(),
        str(entry.get("variant") or "image").strip().lower(),
    )


def merge_queue_entries(
    active_entries: list[dict[str, Any]],
    generated_entries: list[dict[str, Any]],
    limit: int,
) -> list[dict[str, Any]]:
    """Preserve all active work, then fill remaining capacity with newly missing assets."""
    merged: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()

    for entry in active_entries:
        identity = queue_identity(entry)
        if not identity[1] or identity in seen:
            continue
        seen.add(identity)
        merged.append(entry)

    remaining = max(0, limit - len(merged))
    for entry in generated_entries:
        if remaining <= 0:
            break
        identity = queue_identity(entry)
        if not identity[1] or identity in seen:
            continue
        seen.add(identity)
        merged.append(entry)
        remaining -= 1

    return merged


def default_size_for_variant(variant: str) -> str:
    if variant == "icon":
        return "256x256"
    if variant == "card":
        return "512x768"
    if variant == "hero":
        return "1280x720"
    return "1024x1024"


def write_queue(entries: list[dict[str, Any]], output_path: Path) -> None:
    output = {
        "generated_by": "scripts/queue_missing_project_art.py",
        "mode": "dry-run",
        "description": (
            "Concrete project image requests ready for generation; active retries are "
            "preserved until the consumer marks them complete."
        ),
        "batch": {"entries": entries},
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(output, handle, sort_keys=False, allow_unicode=True, width=100)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build projects/art-generate.yaml from missing project icon/card/hero assets."
    )
    parser.add_argument(
        "--limit", type=int, default=10, help="Maximum total queued images to write."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_QUEUE,
        help="Queue file to write. Defaults to projects/art-generate.yaml.",
    )
    parser.add_argument(
        "--replace-active",
        action="store_true",
        help="Discard existing active queue entries instead of preserving them.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help=(
            "Do not write; print the number of missing project assets and return non-zero "
            "if any exist."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.limit < 1:
        raise SystemExit("--limit must be at least 1")

    catalog = load_yaml(PROMPT_CATALOG)
    missing = iter_missing_project_assets(catalog)

    if args.check:
        print(f"missing_project_assets={len(missing)}")
        for entry in missing[: args.limit]:
            print(f"{entry['project']} {entry['variant']} {entry['image_path']}")
        return 1 if missing else 0

    active = [] if args.replace_active else load_active_queue_entries(args.output)
    queued = merge_queue_entries(active, missing, args.limit)
    write_queue(queued, args.output)

    preserved_identities = {
        queue_identity(entry) for entry in active if queue_identity(entry)[1]
    }
    preserved_count = sum(
        1 for entry in queued if queue_identity(entry) in preserved_identities
    )
    added_count = len(queued) - preserved_count
    print(
        f"Queued {len(queued)} project assets in {args.output.relative_to(ROOT)} "
        f"({preserved_count} active preserved, {added_count} newly added, "
        f"{len(missing)} currently missing)."
    )
    if preserved_count > args.limit:
        print("Active retries exceeded --limit and were preserved rather than silently dropped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
