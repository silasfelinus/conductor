#!/usr/bin/env python3
"""
validate_pack_manifest.py — check a packmaker pack manifest against
projects/packmaker/packs/SCHEMA.md (schemaVersion 1).

Kaizen from packmaker/t-002: SCHEMA.md defines the shape of a pack manifest
but nothing checked a manifest against it besides manual review. This script
loads one or more projects/packmaker/packs/*.yaml files, checks required
top-level and per-item fields/enums, and exits non-zero with a clear message
on the first violations found.

Usage:
    python scripts/validate_pack_manifest.py                  # all packs/*.yaml
    python scripts/validate_pack_manifest.py path/to/pack.yaml [more.yaml ...]

Writes nothing; performs no generation, API calls, or database writes.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PACKS_DIR = ROOT / "projects" / "packmaker" / "packs"

SUPPORTED_SCHEMA_VERSIONS = {1}
VISIBILITY_VALUES = {"draft", "released"}
PRICE_HOOK_VALUES = {"free", "one-time", "dlc"}
ITEM_TYPE_VALUES = {"location", "genre", "character", "reward"}
ITEM_SHAPE_VALUES = {"dream", "facet", "character", "reward"}
DRAFT_PAYLOAD_REQUIRED_FIELDS = ("title", "description", "generationPrompt", "artPrompt")
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def is_slug(value: Any) -> bool:
    return isinstance(value, str) and bool(SLUG_RE.match(value))


def require(errors: list[str], prefix: str, condition: bool, message: str) -> None:
    if not condition:
        errors.append(f"{prefix}: {message}")


def validate_item(errors: list[str], prefix: str, item: Any, index: int) -> None:
    item_prefix = f"{prefix}: items[{index}]"
    if not isinstance(item, dict):
        errors.append(f"{item_prefix}: must be a mapping")
        return

    require(errors, item_prefix, is_slug(item.get("id")), "'id' must be a kebab-case string")
    require(
        errors,
        item_prefix,
        item.get("type") in ITEM_TYPE_VALUES,
        f"'type' must be one of {sorted(ITEM_TYPE_VALUES)}, got {item.get('type')!r}",
    )
    require(
        errors,
        item_prefix,
        item.get("itemShape") in ITEM_SHAPE_VALUES,
        f"'itemShape' must be one of {sorted(ITEM_SHAPE_VALUES)}, got {item.get('itemShape')!r}",
    )

    if "refId" in item:
        require(errors, item_prefix, isinstance(item.get("refId"), int), "'refId' must be an integer when present")

    draft_payload = item.get("draftPayload")
    if "refId" not in item:
        require(
            errors,
            item_prefix,
            isinstance(draft_payload, dict),
            "'draftPayload' is required while 'refId' is unset",
        )
    if isinstance(draft_payload, dict):
        for field in DRAFT_PAYLOAD_REQUIRED_FIELDS:
            require(
                errors,
                item_prefix,
                isinstance(draft_payload.get(field), str) and draft_payload.get(field).strip() != "",
                f"'draftPayload.{field}' must be a non-empty string",
            )

    if "notes" in item:
        require(errors, item_prefix, isinstance(item.get("notes"), str), "'notes' must be a string when present")


def validate_manifest(path: Path) -> list[str]:
    errors: list[str] = []
    prefix = str(path)

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"{prefix}: could not read file ({exc})"]

    try:
        doc = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        return [f"{prefix}: invalid YAML ({exc})"]

    if not isinstance(doc, dict):
        return [f"{prefix}: root must be a mapping"]

    require(
        errors,
        prefix,
        doc.get("schemaVersion") in SUPPORTED_SCHEMA_VERSIONS,
        f"'schemaVersion' must be one of {sorted(SUPPORTED_SCHEMA_VERSIONS)}, got {doc.get('schemaVersion')!r}",
    )

    require(errors, prefix, is_slug(doc.get("id")), "'id' must be a kebab-case string")

    for field in ("title", "description", "owner"):
        require(
            errors,
            prefix,
            isinstance(doc.get(field), str) and doc.get(field).strip() != "",
            f"'{field}' must be a non-empty string",
        )

    require(
        errors,
        prefix,
        doc.get("visibility") in VISIBILITY_VALUES,
        f"'visibility' must be one of {sorted(VISIBILITY_VALUES)}, got {doc.get('visibility')!r}",
    )

    price = doc.get("price")
    if not isinstance(price, dict):
        errors.append(f"{prefix}: 'price' must be a mapping")
    else:
        require(
            errors,
            prefix,
            price.get("hook") in PRICE_HOOK_VALUES,
            f"'price.hook' must be one of {sorted(PRICE_HOOK_VALUES)}, got {price.get('hook')!r}",
        )
        if "productSlug" in price:
            require(errors, prefix, isinstance(price.get("productSlug"), str), "'price.productSlug' must be a string when present")

    items = doc.get("items")
    if not isinstance(items, list) or not items:
        errors.append(f"{prefix}: 'items' must be a non-empty list")
    else:
        for index, item in enumerate(items):
            validate_item(errors, prefix, item, index)

    return errors


def resolve_targets(raw_paths: list[str]) -> list[Path]:
    if raw_paths:
        return [Path(p) for p in raw_paths]
    return sorted(PACKS_DIR.glob("*.yaml"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "paths",
        nargs="*",
        help="Pack manifest YAML file(s) to validate. Defaults to all projects/packmaker/packs/*.yaml.",
    )
    args = parser.parse_args(argv)

    targets = resolve_targets(args.paths)
    if not targets:
        print(f"No pack manifests found under {PACKS_DIR}", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    for path in targets:
        all_errors.extend(validate_manifest(path))

    if all_errors:
        for error in all_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"{len(all_errors)} error(s) across {len(targets)} manifest(s)", file=sys.stderr)
        return 1

    print(f"OK: {len(targets)} pack manifest(s) valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
