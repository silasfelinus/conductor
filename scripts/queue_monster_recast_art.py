#!/usr/bin/env python3
"""Build individual full-color Monster Recast art jobs.

The Monster Recast source files remain authoritative:
- projects/coloring-book/sets/monster-recast/characters.yaml
- projects/coloring-book/sets/monster-recast/pages.yaml

This script expands those pitches into one concrete art-generate.yaml entry per
character concept, page composition, and cover. No collages or contact sheets.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SET_DIR = ROOT / "projects" / "coloring-book" / "sets" / "monster-recast"
CHARACTERS_FILE = SET_DIR / "characters.yaml"
PAGES_FILE = SET_DIR / "pages.yaml"
OUTPUT_FILE = ROOT / "projects" / "art-generate.yaml"
TARGET_REPO = "silasfelinus/conductor"
PROJECT = "coloring-book"
SIZE = "2048x2732"

# Medium/style block. Applied as a SUFFIX (subject first, style after) so Flux
# weights the distinctive character/scene ahead of the house look. Front-loading
# this block was collapsing non-cosmic concepts into generic posters (see
# IMAGE-GEN-QUALITY-REVIEW.md 2a). "full-bleed, edge to edge, no border" is
# stated positively because negatives are inert on the Flux path (cfg=1).
STYLE_SUFFIX = (
    "Render this as a premium full-color graphic-horror illustration for the Monster Recast "
    "coloring book: thick confident black outlines, extremely detailed but readable shapes, "
    "flat bounded color fills, hard-edged secondary color shapes instead of gradients, strong "
    "readable silhouette, serious theatrical camp, original character design. One single scene, "
    "one full-bleed image filling the whole frame edge to edge with no border, no framing panel, "
    "no comic panels, no collage, no contact sheet, and no readable text, logo, or watermark."
)


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise SystemExit(f"Expected a YAML mapping: {path}")
    return data


def clean(text: Any) -> str:
    return " ".join(str(text or "").split())


def character_map(characters: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        str(item.get("slug")): item
        for item in characters
        if isinstance(item, dict) and item.get("slug")
    }


def character_entry(character: dict[str, Any]) -> dict[str, Any]:
    slug = str(character["slug"])
    name = clean(character.get("name"))
    prompt = clean(character.get("artPrompt"))
    return {
        "project": PROJECT,
        "set": "monster-recast",
        "kind": "character-concept",
        "slug": slug,
        "title": name,
        "variant": "color",
        "target_repo": TARGET_REPO,
        "image_path": f"projects/coloring-book/sets/monster-recast/generated/color/characters/{slug}.webp",
        "size": SIZE,
        "status": "pending",
        "engine": "flux",
        "steps": 36,
        "prompt": f"{prompt} {STYLE_SUFFIX}",
        "source_file": "projects/coloring-book/sets/monster-recast/characters.yaml",
        "source_slug": slug,
    }


def page_character_context(slugs: list[str], by_slug: dict[str, dict[str, Any]]) -> str:
    details: list[str] = []
    for slug in slugs:
        item = by_slug.get(slug)
        if not item:
            continue
        details.append(clean(item.get("artPrompt")))
    return " ".join(details)


def page_entry(page: dict[str, Any], by_slug: dict[str, dict[str, Any]]) -> dict[str, Any]:
    slug = str(page["slug"])
    title = clean(page.get("title"))
    composition = clean(page.get("composition"))
    slugs = [str(value) for value in (page.get("characters") or [])]
    context = page_character_context(slugs, by_slug)
    prompt = (
        f"Full-color source illustration for the Monster Recast scene titled {title}. "
        f"Scene composition: {composition} Character design context: {context} {STYLE_SUFFIX}"
    )
    return {
        "project": PROJECT,
        "set": "monster-recast",
        "kind": "page-source",
        "slug": slug,
        "title": title,
        "variant": "color",
        "target_repo": TARGET_REPO,
        "image_path": f"projects/coloring-book/sets/monster-recast/generated/color/pages/{slug}.webp",
        "size": SIZE,
        "status": "pending",
        "engine": "flux",
        "steps": 36,
        "prompt": prompt,
        "source_file": "projects/coloring-book/sets/monster-recast/pages.yaml",
        "source_slug": slug,
        "characters": slugs,
    }


def cover_entry(cover: dict[str, Any]) -> dict[str, Any]:
    slug = str(cover.get("slug") or "monster-recast-cover")
    prompt = clean(cover.get("artPrompt"))
    return {
        "project": PROJECT,
        "set": "monster-recast",
        "kind": "cover-source",
        "slug": slug,
        "title": clean(cover.get("title") or "Monster Recast"),
        "variant": "color",
        "target_repo": TARGET_REPO,
        "image_path": f"projects/coloring-book/sets/monster-recast/generated/color/cover/{slug}.webp",
        "size": SIZE,
        "status": "pending",
        "engine": "flux",
        "steps": 40,
        "prompt": f"{prompt} {STYLE_SUFFIX}",
        "source_file": "projects/coloring-book/sets/monster-recast/pages.yaml",
        "source_slug": slug,
    }


def build_entries() -> list[dict[str, Any]]:
    characters_data = load_yaml(CHARACTERS_FILE)
    pages_data = load_yaml(PAGES_FILE)

    characters = [item for item in characters_data.get("characters", []) if isinstance(item, dict)]
    pages = [item for item in pages_data.get("pages", []) if isinstance(item, dict)]
    by_slug = character_map(characters)

    entries = [character_entry(item) for item in characters]
    cover = pages_data.get("cover")
    if isinstance(cover, dict):
        entries.append(cover_entry(cover))
    entries.extend(page_entry(item, by_slug) for item in pages)
    return entries


def merge_with_existing(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not OUTPUT_FILE.exists():
        return entries
    current = load_yaml(OUTPUT_FILE)
    existing = (current.get("batch") or {}).get("entries") or []
    kept = [
        item
        for item in existing
        if isinstance(item, dict)
        and not (item.get("project") == PROJECT and item.get("set") == "monster-recast")
    ]
    return kept + entries


def main() -> int:
    parser = argparse.ArgumentParser(description="Queue one full-color job per Monster Recast pitch.")
    parser.add_argument("--check", action="store_true", help="Print the expanded count without writing.")
    args = parser.parse_args()

    entries = build_entries()
    if args.check:
        kinds: dict[str, int] = {}
        for entry in entries:
            kind = str(entry["kind"])
            kinds[kind] = kinds.get(kind, 0) + 1
        print(f"monster_recast_jobs={len(entries)}")
        for kind, count in sorted(kinds.items()):
            print(f"{kind}={count}")
        return 0

    merged = merge_with_existing(entries)
    output = {
        "generated_by": "scripts/queue_monster_recast_art.py",
        "mode": "ready",
        "description": (
            "Executable art queue. Monster Recast entries are expanded individually from "
            "characters.yaml and pages.yaml; each entry creates one independent image."
        ),
        "batch": {"entries": merged},
    }
    OUTPUT_FILE.write_text(
        yaml.safe_dump(output, sort_keys=False, allow_unicode=True, width=110),
        encoding="utf-8",
    )
    print(f"Queued {len(entries)} individual Monster Recast color jobs in {OUTPUT_FILE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
