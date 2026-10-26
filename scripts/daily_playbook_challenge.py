#!/usr/bin/env python3
"""Author and render exactly three evolving, proposal-only daily game pitches.

No new projects, artwork, paid LLM calls or automatic approvals. Immutable
Pacific-dated snapshots plus curated full-history memory give concepts lineage.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

import playbook_pitch_memory as memory

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
    "friendship_illustrations", "romance_illustrations",
    "villain_illustrations", "transformation_illustrations",
    "finale_frames", "interface_art",
)
TEXT_FIELDS = (
    "opening_scenes", "encounter_scenes", "friendship_scenes",
    "romance_scenes", "villain_scenes", "finale_scripts",
)
SPOT_FIELDS = ("stage", "seeded_state", "text_variation", "image_variation", "consequence")

# A genre is the foundation of a playable world, not simply a decorative mechanic.
# This is human guidance, not a closed enum: future genre gaps can be added.
ALREADY_COVERED_GENRES = (
    "Weird West / anthropomorphic fable", "post-apocalyptic survival",
    "superhero origins and graduation", "slice of life / relationship drama",
    "theatre of place and community", "dark-humor bureaucracy",
    "psychedelic surrealism",
)
PRIORITY_GENRE_GAPS = (
    "Family-friendly literary wonderland / children's mythic adventure",
    "High-technology cyberpunk and transhuman selfhood",
    "Metaphysical heaven/hell and eternal soul-judgment simulation",
)


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
    if not isinstance(pitches, list) or len(pitches) != 3:
        return errors + ["pitches must contain exactly three evolving game concepts"]
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
        elif slug in known or (slug in seen and pitch.get("mode") != "expand"):
            errors.append(f"{prefix}: duplicate or existing game slug {slug}")
        else:
            seen.add(slug)
        title = str(pitch.get("title") or "").strip().casefold()
        title_key = "title:" + re.sub(r"[^a-z0-9]+", "-", title).strip("-")
        if title_key in seen and pitch.get("mode") != "expand":
            errors.append(f"{prefix}: duplicate concept title {pitch.get('title')}")
        else:
            seen.add(title_key)
        for field in ("title", "hook", "genre_pillar", "genre_gap", "audience",
                      "world_scope", "emotional_promise", "core_loop",
                      "unique_mechanic", "opening_choices",
                      "novelty_against_existing"):
            if not isinstance(pitch.get(field), str) or len(pitch[field].strip()) < 20:
                errors.append(f"{prefix}: {field} needs substantive text")
        systems = pitch.get("signature_systems")
        if not isinstance(systems, list) or len(systems) < 3 or any(
            not isinstance(s, str) or len(s.strip()) < 35 for s in systems
        ):
            errors.append(f"{prefix}: at least three substantive genre-defining systems required")
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
    try:
        index = memory.build_index(DOCKETS, before=date)
        errors.extend(memory.verify_lineage(date, pitches, index))
    except (OSError, yaml.YAMLError, ValueError, TypeError, KeyError) as exc:
        errors.append(f"persistent concept memory could not be verified: {exc}")
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
                    title = str(pitch.get("title") or "").strip().casefold()
                    slugs.add("title:" + re.sub(r"[^a-z0-9]+", "-", title).strip("-"))
        except (OSError, yaml.YAMLError, AttributeError, TypeError):
            continue
    return slugs


def payload(date: str) -> dict:
    path = path_for(date)
    if not path.exists():
        return {"date": date, "status": "missing", "pitches": []}
    try:
        docket = yaml.safe_load(path.read_text(encoding="utf-8"))
        errors = validate(date, docket)
        if errors:
            return {"date": date, "status": "invalid", "pitches": [], "errors": errors}
        result = []
        for pitch in docket["pitches"]:
            result.append({**pitch, "units": compute_units(pitch)})
        return {"date": date, "status": "ready", "pitches": result}
    except (OSError, yaml.YAMLError, ValueError, TypeError) as exc:
        return {"date": date, "status": "invalid", "pitches": [], "errors": [str(exc)]}


def brief(date: str) -> str:
    index = memory.build_index(DOCKETS, before=date)
    games = "\n".join(f"- {name}: {loop}" for name, loop in EXISTING_PLAYBOOKS.items())
    covered = ", ".join(ALREADY_COVERED_GENRES)
    gaps = "\n".join(f"- {name}" for name in PRIORITY_GENRE_GAPS)
    return (
        f"Daily evolving-playbook pitch challenge for {date} PT. Draft exactly THREE substantive concepts to "
        f"pitches/playbook-challenges/{date}.yaml. Review the live Kind Robots "
        "utils/playbook/games.ts and current Conductor active-project DESIGN-BRIEFs first; "
        "do not clone their core loops.\n"
        f"Known baseline:\n{games}\n"
        f"ALREADY represented genre families: {covered}.\n"
        f"Current high-value MISSING genre paradigms:\n{gaps}\n"
        "FIRST select a missing, expansive genre pillar, its audience, world scope "
        "and emotional promise; invent at least three substantial genre-defining "
        "systems and multiple acts. A charming isolated mechanic or theme mash-up "
        "is not enough. Prioritize worlds big enough to sustain a full game and "
        "differentiate them structurally from existing titles. Children\'s adventures "
        "use original whimsical voices, read-aloud accessibility, friendship arcs "
        "and safe stakes, NEVER forced romance or horror. Cyberpunk must make "
        "cybernetics, body autonomy, identity continuity and social consequences "
        "mechanical, not only visual. Afterlife games must let the player judge "
        "souls and bear consequences for eternal outcomes, with meaningful "
        "evidence, bias and appeal mechanics. No imitation of protected characters.\n"
        "CHOOSE each slot deliberately: mode=new (a genuinely missing genre pillar), "
        "mode=expand (same stable concept_id and slug; point parents at ONE older dated "
        "version) or mode=meld (NEW concept_id and slug; cite at least TWO dated ancestor "
        "versions from different concepts and explain why the merger improves gameplay). "
        "Each pitch needs concept_id, mode, parents, evolution, preserve, challenge and "
        "at least two actionable next_questions. Build on the strongest lines, no "
        "cosmetic rewording. Keep the full version tree and editorial memory intact; "
        "a prior idea may appear again ONLY as an explicit expansion. Never reintroduce "
        "a rejected idea without editorial reactivation. Since a prior concept exists, "
        "at least ONE of today's three must be expansion or fusion. Meld only when "
        "the combined genre and system work is stronger, never for quota. Consult "
        "pitches/playbook-challenges/MEMORY.yaml for what to keep or avoid. "
        "Each pitch needs: a distinct core loop and novelty comparison; explicit opening "
        "character choices; disjoint playable/NPC/follower cast counts and portraits per "
        "person (base, 2+ expressions/injury where appropriate); maps, opening-choice, "
        "scene, friendship, optional romance, villain, transformation, finale and UI "
        "image counts; text units for openings, "
        "encounters, romance, villain and finales; at least 3 concrete intersections "
        "between seed/RNG, generated or authored prose, art selection/generation, and "
        "consequential game state. Count actual render targets, not vaguely 'lots of art'. "
        "No real ArtJobs, projects, API billing, or sends. No unlabelled repeat of earlier pitches. "
        "Keep the five existing shipped-project upgrades and Daily Dream independent.\n"
        memory.memory_summary(index) + "\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--brief", action="store_true")
    group.add_argument("--check", action="store_true")
    group.add_argument("--payload", action="store_true")
    group.add_argument("--memory", action="store_true", help="print full history and editorial shelf JSON")
    parser.add_argument("--date", default=pacific_today())
    args = parser.parse_args()
    try:
        path_for(args.date)
    except ValueError as exc:
        parser.error(str(exc))
    if args.brief:
        print(brief(args.date))
        return 0
    if args.memory:
        print(json.dumps(memory.build_index(DOCKETS), indent=2, ensure_ascii=False))
        return 0
    result = payload(args.date)
    if args.payload:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    if result["status"] != "ready":
        print(json.dumps(result, indent=2), file=__import__("sys").stderr)
        return 1
    print(f"{args.date}: {len(result['pitches'])} evolving playbook pitches validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
