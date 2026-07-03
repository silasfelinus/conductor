#!/usr/bin/env python3
"""
queue_missing_project_art.py — build a dry-run art generation batch for missing project assets.

Reads projects/art-prompts.yaml, checks the image_path values under images:, and writes
projects/art-generate.yaml with up to --limit missing icon/card/hero requests.

This script never calls the live art generator. It only creates a local queue file that
can be copied into the human image-generation workflow or passed to request_art.py later.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
PROMPT_CATALOG = ROOT / "projects" / "art-prompts.yaml"
OUTPUT_QUEUE = ROOT / "projects" / "art-generate.yaml"
PROJECT_IMAGE_REPO = "silasfelinus/conductor"
VARIANT_ORDER = ("icon", "card", "hero")


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Missing prompt catalog: {path}")
    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    if not isinstance(raw, dict):
        raise SystemExit(f"Prompt catalog must be a YAML mapping: {path}")
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

            entries.append(
                {
                    "project": slug,
                    "variant": variant,
                    "target_repo": PROJECT_IMAGE_REPO,
                    "image_path": image_path,
                    "size": str(size or default_size_for_variant(variant)),
                    "status": "pending",
                    "prompt": " ".join(prompt.split()),
                }
            )

    return entries


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
        "description": "Concrete project image requests ready for manual generation; no live API was called.",
        "images": entries,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(output, handle, sort_keys=False, allow_unicode=True, width=100)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build projects/art-generate.yaml from missing project icon/card/hero assets."
    )
    parser.add_argument("--limit", type=int, default=10, help="Maximum queued images to write.")
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_QUEUE,
        help="Queue file to write. Defaults to projects/art-generate.yaml.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Do not write; print the number of missing project assets and return non-zero if any exist.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.limit < 1:
        raise SystemExit("--limit must be at least 1")

    catalog = load_yaml(PROMPT_CATALOG)
    missing = iter_missing_project_assets(catalog)
    queued = missing[: args.limit]

    if args.check:
        print(f"missing_project_assets={len(missing)}")
        for entry in queued:
            print(f"{entry['project']} {entry['variant']} {entry['image_path']}")
        return 1 if missing else 0

    write_queue(queued, args.output)
    print(f"Queued {len(queued)} of {len(missing)} missing project assets in {args.output.relative_to(ROOT)}")
    if missing and len(queued) < len(missing):
        print(f"Run again after generating this batch; {len(missing) - len(queued)} assets remain.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
