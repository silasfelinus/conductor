#!/usr/bin/env python3
"""
validate_fish.py — enforce the cthulhuquarium fish bible's schema contract
(cthulhuquarium/t-003, see projects/cthulhuquarium/fish/SCHEMA.md).

The bible is the source t-008's seed script reads to populate kind_robots
`Character` rows, and the source `economy.yaml`'s rivalry table keys against
(`diet_role`/`school_role`). A malformed entry there fails silently at seed
or runtime rather than at authoring time — this script is the authoring-time
check, mirroring how validate_roadmaps.py / check_roadmap_yaml.py catch
roadmap mistakes before they reach CI.

Checks, per species across every projects/cthulhuquarium/fish/*.yaml file:
  - every required field is present and non-empty (slug, name, tier, stats
    with all six sub-stats, diet_role, school_role, rivals, size, field_note,
    art_prompt, games)
  - `tier` and every `stats.*` value is one of the six Character.Rarity enum
    values (COMMON, UNCOMMON, RARE, EPIC, LEGENDARY, MYTHIC)
  - a species' `tier` matches the tier its containing file name declares
    (common.yaml holds only COMMON entries, etc.) — catches a copy-paste
    landing a species in the wrong file
  - `diet_role` in {predator, prey, neutral}, `school_role` in
    {school, anchor, solitary} — the exact vocabulary economy.yaml's
    `rivalry.emergent_rules` keys against
  - `slug` matches the lowercase-hyphenated convention and is unique across
    the ENTIRE bible (Character.slug is globally @unique, not per-file)
  - `evolves_to` (if present) names a slug that exists somewhere in the
    bible, and `evolution_kind` is `growth` or `breeding` whenever
    `evolves_to` is set — and is absent when it isn't (no orphaned axis)
  - `rivals` entries each name a slug that exists somewhere in the bible
  - `games` is a non-empty list drawn from the known shared-bestiary
    consumers (cthulhuquarium, ruler-hooked)
  - the bible as a whole carries at least 20 species (DESIGN-BRIEF's stated
    MVP bar) — reported as a warning, not a hard failure, so a genuinely
    in-progress authoring pass doesn't fail CI mid-edit; pass --require-20
    to make it a hard failure once the bible is meant to be complete.

Read-only: never edits a fish file. Exit 0 = clean, 1 = problems found.

Usage:
    python scripts/validate_fish.py
    python scripts/validate_fish.py --require-20
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("validate_fish: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
FISH_DIR = ROOT / "projects" / "cthulhuquarium" / "fish"

RARITY_VALUES = {"COMMON", "UNCOMMON", "RARE", "EPIC", "LEGENDARY", "MYTHIC"}
DIET_ROLES = {"predator", "prey", "neutral"}
SCHOOL_ROLES = {"school", "anchor", "solitary"}
EVOLUTION_KINDS = {"growth", "breeding"}
KNOWN_GAMES = {"cthulhuquarium", "ruler-hooked"}
REQUIRED_STATS = ("charm", "empathy", "grace", "luck", "might", "wits")
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MIN_SPECIES = 20


def load_all_fish():
    """[(file_path, tier_from_filename, entry_dict), ...] across fish/*.yaml."""
    entries = []
    errors = []
    if not FISH_DIR.is_dir():
        return entries, [f"fish bible directory not found: {FISH_DIR}"]

    for path in sorted(FISH_DIR.glob("*.yaml")):
        expected_tier = path.stem.upper()
        if expected_tier not in RARITY_VALUES:
            errors.append(f"{path.name}: filename doesn't match a known tier "
                           f"({', '.join(sorted(RARITY_VALUES))})")
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            errors.append(f"{path.name}: YAML parse error: {exc}")
            continue
        fish_list = data.get("fish")
        if not isinstance(fish_list, list):
            errors.append(f"{path.name}: expected a top-level `fish:` list")
            continue
        for entry in fish_list:
            entries.append((path.name, expected_tier, entry))
    return entries, errors


def validate_entry(filename, expected_tier, entry, all_slugs, errors):
    def fail(msg):
        slug = entry.get("slug", "<no slug>") if isinstance(entry, dict) else "<not a mapping>"
        errors.append(f"{filename} [{slug}]: {msg}")

    if not isinstance(entry, dict):
        errors.append(f"{filename}: entry is not a mapping: {entry!r}")
        return

    slug = entry.get("slug")
    if not slug or not isinstance(slug, str):
        fail("missing or empty `slug`")
    elif not SLUG_RE.match(slug):
        fail(f"slug {slug!r} must be lowercase, hyphenated, no spaces "
             f"(e.g. `goldfish-common`)")

    name = entry.get("name")
    if not name or not isinstance(name, str):
        fail("missing or empty `name`")

    tier = entry.get("tier")
    if tier not in RARITY_VALUES:
        fail(f"`tier` {tier!r} must be one of {sorted(RARITY_VALUES)}")
    elif tier != expected_tier:
        fail(f"`tier: {tier}` doesn't match its file ({filename} implies {expected_tier})")

    stats = entry.get("stats")
    if not isinstance(stats, dict):
        fail("missing or malformed `stats` mapping")
    else:
        for stat_name in REQUIRED_STATS:
            value = stats.get(stat_name)
            if value not in RARITY_VALUES:
                fail(f"stats.{stat_name} {value!r} must be one of {sorted(RARITY_VALUES)}")
        extra = set(stats) - set(REQUIRED_STATS)
        if extra:
            fail(f"stats has unexpected keys {sorted(extra)} — only "
                 f"{REQUIRED_STATS} map onto Character columns")

    diet_role = entry.get("diet_role")
    if diet_role not in DIET_ROLES:
        fail(f"`diet_role` {diet_role!r} must be one of {sorted(DIET_ROLES)}")

    school_role = entry.get("school_role")
    if school_role not in SCHOOL_ROLES:
        fail(f"`school_role` {school_role!r} must be one of {sorted(SCHOOL_ROLES)}")

    rivals = entry.get("rivals", [])
    if not isinstance(rivals, list):
        fail("`rivals` must be a list (use `[]` for none)")
    elif slug and slug in rivals:
        fail("`rivals` lists itself — a species cannot rival itself")

    size = entry.get("size")
    if not isinstance(size, int) or isinstance(size, bool) or size < 1:
        fail(f"`size` must be a positive integer, got {size!r}")

    evolves_to = entry.get("evolves_to")
    evolution_kind = entry.get("evolution_kind")
    if evolves_to is not None:
        if not isinstance(evolves_to, str) or not evolves_to:
            fail("`evolves_to` must be a non-empty slug string when present")
        if slug and evolves_to == slug:
            fail("`evolves_to` points at itself")
        if evolution_kind not in EVOLUTION_KINDS:
            fail(f"`evolution_kind` must be one of {sorted(EVOLUTION_KINDS)} "
                 f"when `evolves_to` is set, got {evolution_kind!r}")
    elif evolution_kind is not None:
        fail("`evolution_kind` set without `evolves_to` — remove one or the other")

    field_note = entry.get("field_note")
    if not field_note or not isinstance(field_note, str) or not field_note.strip():
        fail("missing or empty `field_note`")

    art_prompt = entry.get("art_prompt")
    if not art_prompt or not isinstance(art_prompt, str) or not art_prompt.strip():
        fail("missing or empty `art_prompt`")

    games = entry.get("games")
    if not isinstance(games, list) or not games:
        fail("`games` must be a non-empty list")
    else:
        unknown = [g for g in games if g not in KNOWN_GAMES]
        if unknown:
            fail(f"`games` names unknown consumer(s) {unknown} — known: {sorted(KNOWN_GAMES)}")


def validate_cross_references(entries, errors):
    all_slugs = {entry.get("slug") for _, _, entry in entries
                 if isinstance(entry, dict) and entry.get("slug")}

    for filename, _tier, entry in entries:
        if not isinstance(entry, dict):
            continue
        slug = entry.get("slug", "<no slug>")

        evolves_to = entry.get("evolves_to")
        if evolves_to and evolves_to not in all_slugs:
            errors.append(f"{filename} [{slug}]: `evolves_to: {evolves_to}` "
                           f"names a slug that doesn't exist in the bible")

        rivals = entry.get("rivals")
        if isinstance(rivals, list):
            for rival_slug in rivals:
                if rival_slug not in all_slugs:
                    errors.append(f"{filename} [{slug}]: `rivals` names "
                                   f"{rival_slug!r}, which doesn't exist in the bible")

    return all_slugs


def validate_slug_uniqueness(entries, errors):
    seen = {}
    for filename, _tier, entry in entries:
        if not isinstance(entry, dict):
            continue
        slug = entry.get("slug")
        if not slug:
            continue
        if slug in seen:
            errors.append(f"{filename} [{slug}]: duplicate slug, also used in "
                           f"{seen[slug]} — Character.slug is globally unique")
        else:
            seen[slug] = filename


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--require-20", action="store_true",
                         help="fail (not just warn) if fewer than 20 species are defined")
    args = parser.parse_args(argv)

    entries, errors = load_all_fish()

    for filename, expected_tier, entry in entries:
        validate_entry(filename, expected_tier, entry, None, errors)

    validate_slug_uniqueness(entries, errors)
    validate_cross_references(entries, errors)

    total = len(entries)
    if total < MIN_SPECIES:
        msg = (f"fish bible has {total} species, fewer than the DESIGN-BRIEF "
               f"MVP bar of {MIN_SPECIES}")
        if args.require_20:
            errors.append(msg)
        else:
            print(f"WARNING: {msg}", file=sys.stderr)

    if errors:
        print(f"validate_fish: {len(errors)} problem(s) found:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"validate_fish: {total} species across {len(list(FISH_DIR.glob('*.yaml')))} "
          f"tier files — all spec-compliant.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
