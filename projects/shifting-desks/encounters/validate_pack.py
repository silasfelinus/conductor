#!/usr/bin/env python3
"""
validate_pack.py: contract check for Shifting Desks encounter packs.

Shifting Desks forks Zuzu: Shifting Lands' authored-encounter pack v1
(projects/zuzu-shifting-lands/encounters/ENCOUNTER-PACK.schema.json) for an
office-dystopia game. ENCOUNTER-PACK.schema.json next to this file documents
the shape; this script is the CI authority because the pytest job installs only
pytest + pyyaml (no jsonschema).

Beyond shape it enforces the project's core design rule, NO CLEAN WINS
(DESIGN-BRIEF.md): for every choice, the up-front cost plus the *success*
outcome must contain at least one harmful meter effect. Even winning hurts.
It also enforces Silas's chosen emphasis: at least half of a pack's cards are
tagged conspiracy, psych-test or paperwork.

A choice's `requires.flag` must be grantable: by a choice in the same pack, or
by a pack with a lower `department.order` (flags carry forward as the player
descends, so Records & Forms may pay off a flag granted in Orientation).

Usage:
  python projects/shifting-desks/encounters/validate_pack.py            # every *.json pack here
  python projects/shifting-desks/encounters/validate_pack.py PACK.json  # one pack
Exit 0 = every pack valid, 1 = errors (printed one per line).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

SKILLS = {"compliance", "initiative", "discretion", "rapport", "tinkering", "vigilance"}
# meter -> sign of a harmful delta
METERS = {"composure": -1, "clearance": -1, "suspicion": +1, "successors": -1, "forms": -1}
TARGETS = {7, 9, 11}
POLARITIES = {"good", "bad", "mixed"}
TAGS = {
    "satire", "psych-test", "deathtrap", "creature", "conspiracy",
    "toy", "mutant", "callback", "sacrifice", "paperwork",
}
# Silas, 2026-10-12 PT: secret societies & traitors and paperwork & psych tests lead.
LEAD_TAGS = {"conspiracy", "psych-test", "paperwork"}
LEAD_SHARE_MIN = 0.5
NON_PACK_FILES = {"DECKS.json"}
FAVOR_KINDS = {"force-success", "effects", "ignore-requirement", "bonus"}
MUTATION_KINDS = {"reroll", "auto-success", "bonus", "restore-composure"}
REQUIRE_KEYS = {"clearance", "flag", "forms"}
ART_STATUSES = {"design-only", "verified-repository-art", "approved-ArtImage"}
ART_SUFFIX = "every surface bare and unmarked"
# Kind Robots art-prompt contract: positive phrasing only (scripts/repair_negation_art_prompts.py).
NEGATION_RE = re.compile(r"\b(no|not|never|without|none|nothing|avoid|don't|isn't)\b", re.I)
# Ported from kind_robots server/utils/artPromptContract.ts (FORMAT_PATTERNS and
# ART_DIRECTION_JARGON_PATTERNS): words that make the image model paint lettering
# or a framed format instead of a scene. Art-medic PR #6094 had to strip "poster"
# from these briefs after the live contract rejected them.
CONTRACT_PATTERNS = [
    re.compile(r"\b(?:trading[- ])?card (?:illustration|artwork|composition|art)\b", re.I),
    re.compile(r"\b(?:treasure|ability|item|reward)[- ]card\b", re.I),
    re.compile(r"\b(?:movie |film |book )?(?:poster|book cover|magazine cover|album cover)\b(?!\s+(?:composition|framing|layout|crop))", re.I),
    re.compile(r"\bcomic (?:page|panel|strip)\b", re.I),
    re.compile(r"\bconcrete\s+(?:focal\s+)?subject\b", re.I),
    re.compile(r"\biconic\s+scene\b", re.I),
    re.compile(r"\b(?:unmistakable|clean)\s+silhouette\b", re.I),
    re.compile(r"\bthumbnail\s+readability\b", re.I),
    re.compile(r"\blegible at thumbnail size\b", re.I),
    re.compile(r"\bsubject separation\b", re.I),
    re.compile(r"\b(?:readable|legible|clearly\s+readable|easily\s+read)\s+(?:tools?|labels?|signs?|instruments?|markings?|details?|iconography|symbols?)\b", re.I),
]


def prompt_errors(text) -> list[str]:
    """Every station's image prompt: present, house suffix, positive-only, contract-clean."""
    if not isinstance(text, str) or len(text.strip()) < 50:
        return ["needs an image prompt of at least 50 chars (Silas: every station needs an image)"]
    out = []
    if not text.rstrip(". ").endswith(ART_SUFFIX):
        out.append(f"must end with '{ART_SUFFIX}'")
    m = NEGATION_RE.search(text)
    if m:
        out.append(f"negation {m.group(0)!r}; art prompts are positive-only")
    for pat in CONTRACT_PATTERNS:
        hit = pat.search(text)
        if hit:
            out.append(f"art-contract vocabulary {hit.group(0)!r} paints lettering or a framed format")
    return out
SLUG_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
RULES = {
    "selection": "seeded-weighted-eligible-without-replacement",
    "seed_persisted": True,
    "revisit_policy": "same-recorded-encounter-no-free-reroll",
    "dice": "2d6+skill+modifier-vs-target",
    "no_clean_wins": True,
}


def is_harmful(effects: dict) -> bool:
    return any(v * METERS[k] > 0 for k, v in effects.items() if k in METERS)


def granted_flags(pack: dict) -> set[str]:
    """Every flag any encounter or boss choice in `pack` can add."""
    flags: set[str] = set()
    boss = pack.get("boss") if isinstance(pack.get("boss"), dict) else {}
    choices = [ch for enc in pack.get("encounters") or [] for ch in enc.get("choices") or []]
    choices += boss.get("choices") or []
    for ch in choices:
        for key in ("success", "failure"):
            flags.update((ch.get(key) or {}).get("add_flags") or [])
    return flags


def _department_order(pack: dict) -> int | None:
    order = (pack.get("department") or {}).get("order")
    return order if isinstance(order, int) and not isinstance(order, bool) else None


def earlier_department_flags(path: Path, order: int | None) -> set[str]:
    """Flags granted by sibling packs whose department.order is lower than `order`."""
    if order is None:
        return set()
    flags: set[str] = set()
    for sibling in pack_paths([], path.parent):
        if sibling.resolve() == path.resolve():
            continue
        try:
            other = json.loads(sibling.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue  # reported when that pack is validated on its own
        other_order = _department_order(other)
        if other_order is not None and other_order < order:
            flags |= granted_flags(other)
    return flags


class Checker:
    def __init__(self, name: str):
        self.name = name
        self.errors: list[str] = []

    def err(self, where: str, msg: str) -> None:
        self.errors.append(f"{self.name}: {where}: {msg}")

    def text(self, where, value, lo, hi=None):
        if not isinstance(value, str) or len(value.strip()) < lo:
            self.err(where, f"needs a string of at least {lo} chars")
        elif hi is not None and len(value) > hi:
            self.err(where, f"is {len(value)} chars, max {hi}")

    def slug(self, where, value):
        if not isinstance(value, str) or not SLUG_RE.match(value):
            self.err(where, f"{value!r} is not a kebab-case slug")

    def effects(self, where, eff):
        if not isinstance(eff, dict):
            self.err(where, "effects must be an object")
            return
        for k, v in eff.items():
            if k not in METERS:
                self.err(where, f"unknown meter {k!r} (allowed: {sorted(METERS)})")
            elif not isinstance(v, int) or isinstance(v, bool) or v == 0 or not -3 <= v <= 3:
                self.err(where, f"{k} must be a nonzero integer in -3..3, got {v!r}")

    def outcome(self, where, out, boss_outcomes=None):
        if not isinstance(out, dict):
            self.err(where, "outcome must be an object")
            return
        self.text(f"{where}.text", out.get("text"), 40, 500)
        self.effects(f"{where}.effects", out.get("effects", None))
        for key in ("add_flags", "remove_flags"):
            flags = out.get(key)
            if not isinstance(flags, list):
                self.err(where, f"{key} must be a list")
                continue
            for f in flags:
                self.slug(f"{where}.{key}", f)
        if not isinstance(out.get("map_effect"), str) or not out.get("map_effect"):
            self.err(where, "map_effect must be 'none' or a written reason")
        if boss_outcomes is not None:
            if out.get("department_outcome") not in boss_outcomes:
                self.err(where, f"department_outcome {out.get('department_outcome')!r} is not declared")

    def roll(self, where, roll):
        if roll is None:
            return
        if not isinstance(roll, dict):
            self.err(where, "roll must be null or an object")
            return
        if roll.get("dice_count") != 2 or roll.get("die_sides") != 6:
            self.err(where, "rolls are 2d6")
        if roll.get("skill") not in SKILLS:
            self.err(where, f"skill {roll.get('skill')!r} not in {sorted(SKILLS)}")
        if not isinstance(roll.get("modifier"), int):
            self.err(where, "modifier must be an integer")
        if roll.get("target") not in TARGETS:
            self.err(where, f"target must be one of {sorted(TARGETS)}")

    def art(self, where, art, cast_required=True):
        if not isinstance(art, dict):
            self.err(where, "art must be an object")
            return
        if art.get("status") not in ART_STATUSES:
            self.err(where, f"status must be one of {sorted(ART_STATUSES)}")
        if art.get("status") == "design-only" and art.get("art_ref") is not None:
            self.err(where, "design-only art must have art_ref null")
        for problem in prompt_errors(art.get("brief")):
            self.err(f"{where}.brief", problem)
        if cast_required is False:
            return
        cast = art.get("cast")
        if not isinstance(cast, list) or not cast:
            self.err(where, "cast must be a non-empty list")
            return
        for i, actor in enumerate(cast):
            w = f"{where}.cast[{i}]"
            self.slug(f"{w}.identity", actor.get("identity"))
            self.text(f"{w}.kind", actor.get("kind"), 3)
            self.text(f"{w}.role", actor.get("role"), 3)
            self.text(f"{w}.visual_description", actor.get("visual_description"), 20)

    def choice(self, where, ch, boss_outcomes=None):
        self.slug(f"{where}.id", ch.get("id"))
        self.text(f"{where}.label", ch.get("label"), 3, 60)
        self.text(f"{where}.intent", ch.get("intent"), 10)
        self.text(f"{where}.risk_hint", ch.get("risk_hint"), 10)
        req = ch.get("requires")
        if req is not None:
            if not isinstance(req, dict) or not req or set(req) - REQUIRE_KEYS:
                self.err(f"{where}.requires", f"must be null or an object with keys from {sorted(REQUIRE_KEYS)}")
        cost = ch.get("cost")
        self.effects(f"{where}.cost", cost)
        roll = ch.get("roll", "missing")
        if roll == "missing":
            self.err(where, "roll key is required (null for a certain outcome)")
            roll = None
        self.roll(f"{where}.roll", roll)
        self.outcome(f"{where}.success", ch.get("success"), boss_outcomes)
        failure = ch.get("failure", "missing")
        if roll is not None:
            self.outcome(f"{where}.failure", failure, boss_outcomes)
        elif failure is not None:
            self.err(where, "a choice without a roll must have failure: null")
        # NO CLEAN WINS: even the best result of every choice costs something.
        success_eff = (ch.get("success") or {}).get("effects") or {}
        if isinstance(cost, dict) and isinstance(success_eff, dict):
            if not (is_harmful(cost) or is_harmful(success_eff)):
                self.err(where, "clean win: cost + success has no harmful effect (DESIGN-BRIEF 'no clean wins')")


def validate_pack(path: Path, earlier_flags: set[str] | None = None) -> list[str]:
    """Validate one pack.

    `earlier_flags` are flags the player may already carry from lower departments. When
    omitted, they are collected from sibling packs in the same directory whose
    department.order is lower than this pack's.
    """
    c = Checker(path.name)
    try:
        pack = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path.name}: unreadable JSON: {exc}"]

    if pack.get("schema_version") != 1:
        c.err("schema_version", "must be 1")
    if pack.get("project") != "shifting-desks":
        c.err("project", "must be 'shifting-desks'")
    if pack.get("status") != "draft-not-imported":
        c.err("status", "must be 'draft-not-imported' until a versioned import exists")
    dept = pack.get("department") or {}
    c.slug("department.id", dept.get("id"))
    c.art("department.arrival_art", dept.get("arrival_art"), cast_required=False)
    c.text("department.title", dept.get("title"), 3)
    if not isinstance(dept.get("order"), int) or not 1 <= dept.get("order", 0) <= 5:
        c.err("department.order", "must be 1..5")

    rules = pack.get("rules") or {}
    for key, want in RULES.items():
        if rules.get(key) != want:
            c.err(f"rules.{key}", f"must be {want!r}")
    min_per = rules.get("encounters_per_location_min")
    if not isinstance(min_per, int) or min_per < 2:
        c.err("rules.encounters_per_location_min", "must be an integer >= 2")
        min_per = 2

    encounters = pack.get("encounters") or []
    by_id = {}
    for i, enc in enumerate(encounters):
        eid = enc.get("id")
        if eid in by_id:
            c.err(f"encounters[{i}]", f"duplicate id {eid!r}")
        by_id[eid] = enc

    locations = pack.get("locations") or []
    if not locations:
        c.err("locations", "at least one location is required")
    placed: dict[str, str] = {}
    for loc in locations:
        lid = loc.get("location_id")
        c.slug("locations.location_id", lid)
        c.text(f"locations[{lid}].title", loc.get("title"), 3)
        c.text(f"locations[{lid}].description", loc.get("description"), 20)
        c.art(f"locations[{lid}].art", loc.get("art"), cast_required=False)
        ids = loc.get("encounter_ids") or []
        if len(ids) < min_per or len(set(ids)) != len(ids):
            c.err(f"locations[{lid}]", f"needs at least {min_per} unique encounter_ids")
        for eid in ids:
            if eid not in by_id:
                c.err(f"locations[{lid}]", f"unknown encounter {eid!r}")
            elif by_id[eid].get("location_id") != lid:
                c.err(f"locations[{lid}]", f"{eid!r} declares location {by_id[eid].get('location_id')!r}")
            if eid in placed:
                c.err(f"locations[{lid}]", f"{eid!r} already placed in {placed[eid]!r}")
            placed[eid] = lid
    for eid in by_id:
        if eid not in placed:
            c.err(f"encounters[{eid}]", "is not in any location pool")

    all_added: set[str] = set()
    required_flags: list[tuple[str, str]] = []

    def collect(where, choices):
        for ch in choices:
            for key in ("success", "failure"):
                out = ch.get(key) or {}
                all_added.update(out.get("add_flags") or [])
            req = ch.get("requires") or {}
            if isinstance(req, dict) and "flag" in req:
                required_flags.append((f"{where}.{ch.get('id')}", req["flag"]))

    for enc in encounters:
        w = f"encounters[{enc.get('id')}]"
        c.slug(f"{w}.id", enc.get("id"))
        c.text(f"{w}.title", enc.get("title"), 5, 64)
        c.text(f"{w}.flavor_text", enc.get("flavor_text"), 90, 700)
        if enc.get("polarity") not in POLARITIES:
            c.err(w, f"polarity must be one of {sorted(POLARITIES)}")
        tags = enc.get("tags")
        if not isinstance(tags, list) or not tags or set(tags) - TAGS:
            c.err(w, f"tags must be a non-empty list from {sorted(TAGS)}")
        if not isinstance(enc.get("weight"), int) or not 1 <= enc.get("weight", 0) <= 9:
            c.err(w, "weight must be 1..9")
        if enc.get("unique_per_run") is not True or enc.get("first_visit_only") is not True:
            c.err(w, "unique_per_run and first_visit_only must be true")
        if not isinstance(enc.get("witnessed"), bool):
            c.err(w, "witnessed must be true/false (Mutation use costs Suspicion when witnessed)")
        cb = enc.get("callback")
        if cb is not None:
            c.text(f"{w}.callback", cb, 20)
        if "callback" in (tags or []) and cb is None:
            c.err(w, "a callback-tagged card must explain its homage in callback")
        c.art(f"{w}.art", enc.get("art"))
        choices = enc.get("choices") or []
        if not 2 <= len(choices) <= 4:
            c.err(w, "needs 2-4 choices")
        if len({ch.get("id") for ch in choices}) != len(choices):
            c.err(w, "choice ids must be unique within the card")
        for ch in choices:
            c.choice(f"{w}.choices[{ch.get('id')}]", ch)
        c.text(f"{w}.developer_note", enc.get("developer_note"), 20)
        collect(w, choices)

    if encounters:
        lead = sum(1 for e in encounters if LEAD_TAGS & set(e.get("tags") or []))
        if lead < LEAD_SHARE_MIN * len(encounters):
            c.err("encounters", f"only {lead}/{len(encounters)} cards carry a lead tag "
                  f"{sorted(LEAD_TAGS)}; at least half must (Silas's 2026-10-12 emphasis)")

    boss = pack.get("boss")
    if not isinstance(boss, dict):
        c.err("boss", "each department pack needs a boss review card")
    else:
        w = f"boss[{boss.get('id')}]"
        if boss.get("id") != dept.get("boss_id"):
            c.err(w, "boss.id must equal department.boss_id")
        c.text(f"{w}.title", boss.get("title"), 5, 64)
        c.text(f"{w}.flavor_text", boss.get("flavor_text"), 90, 700)
        c.art(f"{w}.art", boss.get("art"))
        outcomes = boss.get("department_outcomes") or []
        outcome_ids = {o.get("id") for o in outcomes}
        if len(outcome_ids) < 3:
            c.err(w, "needs at least 3 distinct department_outcomes")
        for o in outcomes:
            c.slug(f"{w}.department_outcomes", o.get("id"))
            c.text(f"{w}.department_outcomes[{o.get('id')}].summary", o.get("summary"), 20)
        choices = boss.get("choices") or []
        if len(choices) < 3:
            c.err(w, "a boss review needs at least 3 routes")
        for ch in choices:
            c.choice(f"{w}.choices[{ch.get('id')}]", ch, outcome_ids)
        reached = {
            (ch.get(k) or {}).get("department_outcome")
            for ch in choices for k in ("success", "failure")
        }
        for oid in outcome_ids - reached:
            c.err(w, f"department_outcome {oid!r} is unreachable")
        unconditional = [ch for ch in choices if not ch.get("requires")]
        if not unconditional:
            c.err(w, "at least one boss route must have no requirement")
        c.text(f"{w}.developer_note", boss.get("developer_note"), 20)
        collect(w, choices)

    if earlier_flags is None:
        earlier_flags = earlier_department_flags(path, _department_order(pack))
    for where, flag in required_flags:
        if flag not in all_added and flag not in earlier_flags:
            c.err(where, f"requires flag {flag!r} that nothing in this pack grants "
                  "(nor any pack with a lower department.order)")

    return c.errors


def pack_paths(args: list[str], directory: Path = HERE) -> list[Path]:
    if args:
        return [Path(a) for a in args]
    return sorted(
        p for p in directory.glob("*.json")
        if not p.name.endswith(".schema.json") and p.name not in NON_PACK_FILES
    )


def validate_decks(path: Path, packs: list[Path]) -> list[str]:
    """DECKS.json: job titles, societies and mutations, checked against the packs' flags."""
    errors: list[str] = []
    decks = json.loads(path.read_text(encoding="utf-8"))
    granted: set[str] = set()
    for p in packs:
        granted |= granted_flags(json.loads(p.read_text(encoding="utf-8")))
    jobs = decks.get("job_titles") or []
    if len(jobs) < 3:
        errors.append("DECKS: need at least 3 job titles")
    for group, items in (("job", jobs), ("society", decks.get("societies") or []), ("mutation", decks.get("mutations") or [])):
        for item in items:
            for problem in prompt_errors(item.get("art_prompt")):
                errors.append(f"DECKS: {group} {item.get('id')!r} art_prompt: {problem}")
    for job in jobs:
        skills = job.get("skills") or {}
        if set(skills) != SKILLS or sum(skills.values()) != 6 or not all(0 <= v <= 3 for v in skills.values()):
            errors.append(f"DECKS: job {job.get('id')!r} needs all six skills, each 0-3, summing to 6")
    societies = decks.get("societies") or []
    if len(societies) < 6:
        errors.append("DECKS: need at least 6 societies")
    for soc in societies:
        sid = soc.get("id")
        for key in ("objectives", "betrayals"):
            for dept, flags in (soc.get(key) or {}).items():
                if not flags:
                    errors.append(f"DECKS: {sid} {key}.{dept} is empty")
                for f in flags:
                    if f not in granted:
                        errors.append(f"DECKS: {sid} {key}.{dept} names {f!r}, which no pack grants")
        if (soc.get("favor") or {}).get("kind") not in FAVOR_KINDS:
            errors.append(f"DECKS: {sid} favor kind must be one of {sorted(FAVOR_KINDS)}")
        reward = soc.get("reward") or {}
        if not reward or set(reward) - set(METERS):
            errors.append(f"DECKS: {sid} reward must be meter effects")
    mutations = decks.get("mutations") or []
    if len(mutations) < 8:
        errors.append("DECKS: need at least 8 mutations")
    for mut in mutations:
        if mut.get("kind") not in MUTATION_KINDS:
            errors.append(f"DECKS: mutation {mut.get('id')!r} kind must be one of {sorted(MUTATION_KINDS)}")
        for s in mut.get("skills") or []:
            if s not in SKILLS:
                errors.append(f"DECKS: mutation {mut.get('id')!r} names unknown skill {s!r}")
    return errors


def main(argv: list[str]) -> int:
    paths = pack_paths(argv)
    errors: list[str] = []
    for p in paths:
        errs = validate_pack(p)
        errors.extend(errs)
        if not errs:
            pack = json.loads(p.read_text(encoding="utf-8"))
            pol = {k: 0 for k in sorted(POLARITIES)}
            for enc in pack["encounters"]:
                pol[enc["polarity"]] += 1
            print(f"OK {p.name}: {len(pack['encounters'])} encounters, "
                  f"{len(pack['locations'])} locations, polarity {pol}, "
                  f"boss {pack['boss']['id']} with {len(pack['boss']['choices'])} routes")
    decks = HERE / "DECKS.json"
    if not argv and decks.exists():
        deck_errors = validate_decks(decks, paths)
        errors.extend(deck_errors)
        if not deck_errors:
            print(f"OK {decks.name}: job titles, societies and mutations reference granted flags")
    for e in errors:
        print(e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
