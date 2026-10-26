#!/usr/bin/env python3
"""Author, check, and serve the *new-game* playbook challenge in the Daily Digest.

This is a proposal-only lane: no new projects, artwork, paid LLM calls, or
automatic approval. Sessions write one Pacific-dated YAML docket, and the
morning renderer refuses to recycle yesterday's ideas as today's.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCKETS = ROOT / "pitches" / "playbook-challenges"
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# Six Playbook Studio adapters verified at kind_robots/utils/playbook/games.ts
# plus the two 2026-10-25 canon playbooks tracked in Conductor. When new
# playbooks arrive, update this review baseline. Authors must also inspect
# the live Studio registry and active project briefs before drafting.
EXISTING_PLAYBOOKS = {
    "ecotone": "Choice mystery / companions in supernatural Humboldt",
    "emperor-of-dust": "Throne and follower assignments over 100 days",
    "shifting-lands": "Illustrated territorial card board with consequential choices",
    "shifting-desks": "Office-dystopia route and choice adventure",
    "zuzu-gamebook": "Branching Weird West animal-fantasy gamebook",
    "crystal-street": "1980s suburban horror-comedy day/night adventure",
    "comet-city-academy": "Prom of Doom: 30-day superhero identities and relationships",
    "game-of-captains": "This Means Warp: comedy starship crew and away missions",
}
ART_FIELDS = (
    "maps", "opening_choice_images", "scene_illustrations",
    "romance_illustrations", "villain_illustrations",
    "finale_frames", "interface_art",
)
TEXT_FIELDS = (
    "opening_scenes", "encounter_scenes", "romance_scenes",
    "villain_scenes", "finale_scripts",
)
SPOT_FIELDS = ("stage", "seeded_state", "text_variation", "image_variation", "consequence")


def pacific_today() -> str:
    return datetime.now(ZoneInfo("America/Los_Angeles")).date().isoformat()


def path_for(date: str) -> Path:
    if not DATE_PATTERN.fullmatch(date):
        raise ValueError("date must be YYYY-MM-DD")
    return DOCKETS / f"{date}.yaml"


def compute_units(pitch: dict) -> dict:
    """One art unit is one distinct render target, NOT an API token or job guarantee.

    Cast categories must be disjoint, with recurring people counted once; a
    portrait unit is a single finished expression/frame. Text units are
    distinct authored beats, not token estimates and not runtime calls.
    """
    cast = pitch["cast"]
    production = pitch["production"]
    distinct_people = sum(cast[k] for k in ("playable", "npcs", "followers"))
    portraits = distinct_people * cast["portraits_per_person"]
    art = {"portraits": portraits, **{k: production[k] for k in ART_FIELDS}}
    text = {k: production[k] for k in TEXT_FIELDS}
    return {
        "unique_people": distinct_people,
        "art_breakdown": art,
        "art_units": sum(art.values()),
        "text_breakdown": text,
        "text_units": sum(text.values()),
        "image_generation_passes": sum(art.values()) * production["art_passes_per_image"],
        "text_authoring_passes": sum(text.values()) * production["text_passes_per_beat"],
        "total_planned_passes": (
            sum(art.values()) * production["art_passes_per_image"]
            + sum(text.values()) * production["text_passes_per_beat"]
        ),
    }


def validate(date: str, docket: object, previous: set[str] | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(docket, dict):
        return ["docket must be an object"]
    if docket.get("date") != date:
        errors.append("docket.date must match Pacific date")
    reviewed = docket.get("reviewed_playbooks")
    if not isinstance(reviewed, list) or set(reviewed) != set(EXISTING_PLAYBOOKS) or len(reviewed) != len(EXISTING_PLAYBOOKS):
        errors.append("reviewed_playbooks must identify all eight known playbooks once each")
    pitches = docket.get("pitches")
    if not isinstance(pitches, list) or not 1 <= len(pitches) <= 3:
        return errors + ["pitches must contain 1–3 new-game concepts"]
    seen = set(previous or ())
    known = set(EXISTING_PLAYBOOKS)
    for index, pitch in enumerate(pitches, 1):
        prefix = f"pitch {index}"
        if not isinstance(pitch, dict):
            errors.append(f"{prefix}: not an object")
            continue
        slug = pitch.get("slug")
        if not isinstance(slug, str) or not SLUG_PATTERN.fullmatch(slug):
            errors.append(f"{prefix}: invalid slug")
        elif slug in seen or slug in known:
            errors.append(f"{prefix}: duplicate or existing game slug {slug}")
        else:
            seen.add(slug)
        for field in ("title", "hook", "core_loop", "unique_mechanic", "opening_choices", "novelty_against_existing"):
            if not isinstance(pitch.get(field), str) or len(pitch[field].strip()) < 20:
                errors.append(f"{prefix}: {field} needs substantive text")
        if pitch.get("runtime_llm") not in ("none", "optional", "required"):
            errors.append(f"{prefix}: runtime_llm must be none, optional, or required")
        cast = pitch.get("cast")
        required_cast = ("playable", "npcs", "followers", "portraits_per_person")
        if not isinstance(cast, dict) or any(not isinstance(cast.get(k), int) or isinstance(cast.get(k), bool) or cast[k] < (2 if k == "portraits_per_person" else 0) for k in required_cast):
            errors.append(f"{prefix}: cast counts must be nonnegative and portraits_per_person >= 2")
            continue
        production = pitch.get("production")
        if not isinstance(production, dict) or any(not isinstance(production.get(k), int) or isinstance(production.get(k), bool) or production[k] < 0 for k in (*ART_FIELDS, *TEXT_FIELDS)):
            errors.append(f"{prefix}: production must give nonnegative integer counts for every art and text category")
            continue
        for field in ("art_passes_per_image", "text_passes_per_beat"):
            if not isinstance(production.get(field), int) or isinstance(production.get(field), bool) or not 1 <= production[field] <= 4:
                errors.append(f"{prefix}: {field} must be 1–4 model passes per deliverable")
        if cast["playable"] < 1 or production["maps"] < 1:
            errors.append(f"{prefix}: at least one playable opening and one map required")
        spots = pitch.get("collisions")
        if not isinstance(spots, list) or len(spots) < 3:
            errors.append(f"{prefix}: include at least three prose/art/randomness intersections")
        else:
            stages = set()
            for spot in spots:
                if not isinstance(spot, dict) or any(not isinstance(spot.get(k), str) or len(spot[k].strip()) < 10 for k in SPOT_FIELDS):
                    errors.append(f"{prefix}: each collision needs stage, seeded_state, text_variation, image_variation, consequence")
                    continue
                if spot["stage"] in stages:
                    errors.append(f"{prefix}: collision stages must be distinct")
                stages.add(spot["stage"])
    return errors


def historical_slugs(date: str) -> set[str]:
    slugs = set()
    for path in sorted(DOCKETS.glob("????-??-??.yaml")):
        if path.stem == date:
            continue
        try:
            body = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            for pitch in body.get("pitches", []):
                if isinstance(pitch, dict) and pitch.get("slug"):
                    slugs.add(str(pitch["slug"]))
        except (OSError, yaml.YAMLError, AttributeError, TypeError):
            continue
    return slugs


def payload(date: str) -> dict:
    path = path_for(date)
    if not path.exists():
        return {"date": date, "status": "missing", "pitches": []}
    try:
        docket = yaml.safe_load(path.read_text(encoding="utf-8"))
        errors = validate(date, docket, historical_slugs(date))
        if errors:
            return {"date": date, "status": "invalid", "pitches": [], "errors": errors}
        result = []
        for pitch in docket["pitches"]:
            result.append({**pitch, "units": compute_units(pitch)})
        return {"date": date, "status": "ready", "pitches": result}
    except (OSError, yaml.YAMLError, ValueError, TypeError) as exc:
        return {"date": date, "status": "invalid", "pitches": [], "errors": [str(exc)]}


def brief(date: str) -> str:
    recent = sorted(DOCKETS.glob("????-??-??.yaml"), reverse=True)[:7]
    prior = []
    for path in recent:
        try:
            body = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            prior += [f"{path.stem}: {p.get('title')} ({p.get('slug')})" for p in body.get("pitches", []) if isinstance(p, dict)]
        except (OSError, yaml.YAMLError, TypeError):
            pass
    games = "\n".join(f"- {name}: {loop}" for name, loop in EXISTING_PLAYBOOKS.items())
    return (
        f"Daily new-playbook pitch challenge for {date} PT. Draft 1–3 FRESH concepts to "
        f"pitches/playbook-challenges/{date}.yaml. Review the live Kind Robots "
        "utils/playbook/games.ts and current Conductor active-project DESIGN-BRIEFs first; "
        "do not clone their core loops.\n"
        f"Known baseline:\n{games}\n"
        "Each pitch needs: a distinct core loop and novelty comparison; explicit opening "
        "character choices; disjoint playable/NPC/follower cast counts and portraits per "
        "person (base, 2+ expressions/injury where appropriate); maps, opening-choice, "
        "scene, romance, villain, finale and UI image counts; text units for openings, "
        "encounters, romance, villain and finales; at least 3 concrete intersections "
        "between seed/RNG, generated or authored prose, art selection/generation, and "
        "consequential game state. Count actual render targets, not vaguely 'lots of art'. "
        "No real ArtJobs, projects, API billing, or sends. No repeat of earlier pitches. "
        "Keep the five existing shipped-project upgrades and Daily Dream independent.\n"
        "Past week's pitches to avoid:\n" + ("\n".join(prior) if prior else "(none)") + "\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--brief", action="store_true")
    group.add_argument("--check", action="store_true")
    group.add_argument("--payload", action="store_true")
    parser.add_argument("--date", default=pacific_today())
    args = parser.parse_args()
    try:
        path_for(args.date)
    except ValueError as exc:
        parser.error(str(exc))
    if args.brief:
        print(brief(args.date))
        return 0
    result = payload(args.date)
    if args.payload:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    if result["status"] != "ready":
        print(json.dumps(result, indent=2), file=__import__("sys").stderr)
        return 1
    print(f"{args.date}: {len(result['pitches'])} original playbook pitches validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
