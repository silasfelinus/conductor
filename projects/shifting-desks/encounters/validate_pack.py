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

Hidden Test Results (t-022): outcomes may carry `grades` (obedience, empathy,
ingenuity, spite; nonzero integers in -2..2). Every encounter card grades on at
least one choice, and every pack grades each axis upward somewhere. Grades stay
hidden during play, so only a department review may gate a route on one
(`requires.grade`), and the gate must be reachable: no higher than the best
grade a player can collect on one card per location, in this department and
every department above it.

Restructuring (t-023): every department below the surface declares
`restructurings`, the memos that reshape its map as the player arrives. Each one
eliminates a location, merges two into a single draw, adds a second card from a
location, or changes nothing, always with a written reason. `when` names
outcomes or flags from the departments above (any one matches); the first match
applies, and exactly one memo with `when: null` comes last as the default.

Endings (t-014): ENDINGS.json covers every outcome of the bottom floor's review
(except its fallback) with a board ending, has exactly one default elimination
ending, keys secret endings and epilogue variants only on flags some pack
grants, and gives every epilogue complete sentences and a contract-clean image
prompt. FLAG-MAP.json is generated from the packs (`--flag-map`) and must match
them: every flag, where it is granted and where it is read.

Window shifts (t-016): a pack may declare one `window_shift`, a Papers, Please desk
shift at one of its locations. The day's memo lists 2-4 rules; each of 3-5
applicants shows documents, and a document may break one rule. Every applicant
offers exactly two certain stamps, `approve` and `deny`. Stamping against the memo
always carries Suspicion (PAL audits every stamp), every rule is broken by someone,
at least one applicant is clean, and at least one by-the-book stamp costs Empathy:
the memo is never simply the kind thing to do.

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
NON_PACK_FILES = {"DECKS.json", "ENDINGS.json", "FLAG-MAP.json"}
ENDING_KINDS = {"board", "elimination", "secret"}
FAVOR_KINDS = {"force-success", "effects", "ignore-requirement", "bonus"}
MUTATION_KINDS = {"reroll", "auto-success", "bonus", "restore-composure"}
REQUIRE_KEYS = {"clearance", "flag", "forms", "grade"}
GRADES = ("obedience", "empathy", "ingenuity", "spite")
VERDICT_AXES = set(GRADES) | {"balanced"}
RESTRUCTURE_LOCATIONS = {"eliminate": 1, "merge": 2, "add": 1, "none": 0}
ART_STATUSES = {"design-only", "verified-repository-art", "approved-ArtImage"}
# The public path kind_robots stationArt() serves; link_art.py writes it from the art ledgers.
ART_REF = re.compile(r"/images/shifting-desks/[a-z0-9-]+(/[a-z0-9-]+)*\.webp")
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


WINDOW_STAMPS = ("approve", "deny")


def window_applicants(pack: dict) -> list[dict]:
    shift = pack.get("window_shift")
    if not isinstance(shift, dict):
        return []
    return [a for a in shift.get("applicants") or [] if isinstance(a, dict)]


def by_the_book(applicant: dict) -> str:
    """The stamp the day's memo demands: deny anyone whose documents break a rule."""
    broken = [d for d in applicant.get("documents") or [] if isinstance(d, dict) and d.get("breaks")]
    return "deny" if broken else "approve"


def granted_flags(pack: dict) -> set[str]:
    """Every flag any encounter, window applicant or boss choice in `pack` can add."""
    flags: set[str] = set()
    boss = pack.get("boss") if isinstance(pack.get("boss"), dict) else {}
    choices = [ch for enc in pack.get("encounters") or [] for ch in enc.get("choices") or []]
    choices += [ch for a in window_applicants(pack) for ch in a.get("choices") or []]
    choices += boss.get("choices") or []
    for ch in choices:
        for key in ("success", "failure"):
            flags.update((ch.get(key) or {}).get("add_flags") or [])
    return flags


def grade_reach(pack: dict) -> dict[str, int]:
    """Most of each grade one pass through `pack` can earn: one card per location, then the review."""
    def best(choices, axis):
        top = 0
        for ch in choices or []:
            for key in ("success", "failure"):
                grades = (ch.get(key) or {}).get("grades") or {}
                value = grades.get(axis, 0) if isinstance(grades, dict) else 0
                if isinstance(value, int):
                    top = max(top, value)
        return top

    encounters = {e.get("id"): e for e in pack.get("encounters") or []}
    boss = pack.get("boss") if isinstance(pack.get("boss"), dict) else {}
    reach = {}
    for axis in GRADES:
        total = 0
        for loc in pack.get("locations") or []:
            cards = [encounters[i] for i in loc.get("encounter_ids") or [] if i in encounters]
            total += max((best(c.get("choices"), axis) for c in cards), default=0)
        total += sum(best(a.get("choices"), axis) for a in window_applicants(pack))
        reach[axis] = total + best(boss.get("choices"), axis)
    return reach


def earlier_grade_reach(path: Path, order: int | None) -> dict[str, int]:
    """Grade reach summed over sibling packs whose department.order is lower than `order`."""
    reach = {axis: 0 for axis in GRADES}
    if order is None:
        return reach
    for sibling in pack_paths([], path.parent):
        if sibling.resolve() == path.resolve():
            continue
        try:
            other = json.loads(sibling.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        other_order = _department_order(other)
        if other_order is not None and other_order < order:
            for axis, value in grade_reach(other).items():
                reach[axis] += value
    return reach


def earlier_department_outcomes(path: Path, order: int | None) -> set[str]:
    """Department outcome ids declared by sibling packs above this one."""
    outcomes: set[str] = set()
    if order is None:
        return outcomes
    for sibling in pack_paths([], path.parent):
        if sibling.resolve() == path.resolve():
            continue
        try:
            other = json.loads(sibling.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        other_order = _department_order(other)
        if other_order is not None and other_order < order:
            boss = other.get("boss") if isinstance(other.get("boss"), dict) else {}
            outcomes |= {o.get("id") for o in boss.get("department_outcomes") or []}
    return outcomes


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
        grades = out.get("grades")
        if grades is not None:
            if not isinstance(grades, dict) or not grades:
                self.err(f"{where}.grades", "must be a non-empty object when present")
            else:
                for k, v in grades.items():
                    if k not in GRADES:
                        self.err(f"{where}.grades", f"unknown grade {k!r} (allowed: {list(GRADES)})")
                    elif not isinstance(v, int) or isinstance(v, bool) or v == 0 or not -2 <= v <= 2:
                        self.err(f"{where}.grades", f"{k} must be a nonzero integer in -2..2, got {v!r}")
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
        if art.get("status") == "verified-repository-art" and not ART_REF.fullmatch(str(art.get("art_ref"))):
            self.err(where, "verified-repository-art needs art_ref /images/shifting-desks/<path>.webp (link_art.py)")
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
            elif "grade" in req:
                gate = req["grade"]
                if boss_outcomes is None:
                    self.err(f"{where}.requires.grade", "grades stay hidden during play; only a department review may gate on one")
                if (not isinstance(gate, dict) or len(gate) != 1 or set(gate) - set(GRADES)
                        or not all(isinstance(v, int) and not isinstance(v, bool) and 1 <= v <= 6 for v in gate.values())):
                    self.err(f"{where}.requires.grade", f"must name one grade from {list(GRADES)} with a minimum of 1-6")
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
    grade_gates: list[tuple[str, str, int]] = []
    graded_up: set[str] = set()

    def graded(choices) -> bool:
        any_grade = False
        for ch in choices:
            for key in ("success", "failure"):
                grades = (ch.get(key) or {}).get("grades")
                if isinstance(grades, dict) and grades:
                    any_grade = True
                    graded_up.update(k for k, v in grades.items() if isinstance(v, int) and v > 0)
        return any_grade

    def collect(where, choices):
        for ch in choices:
            for key in ("success", "failure"):
                out = ch.get(key) or {}
                all_added.update(out.get("add_flags") or [])
            req = ch.get("requires") or {}
            if isinstance(req, dict) and "flag" in req:
                required_flags.append((f"{where}.{ch.get('id')}", req["flag"]))
            gate = req.get("grade") if isinstance(req, dict) else None
            if isinstance(gate, dict):
                for axis, minimum in gate.items():
                    if axis in GRADES and isinstance(minimum, int):
                        grade_gates.append((f"{where}.{ch.get('id')}", axis, minimum))

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
        if not graded(choices):
            c.err(w, "no choice grades the player; every card feeds the hidden Test Results (t-022)")
        collect(w, choices)

    if pack.get("window_shift") is not None:
        check_window_shift(c, pack, set(by_id), graded, collect)

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
        graded(choices)
        collect(w, choices)

    if earlier_flags is None:
        earlier_flags = earlier_department_flags(path, _department_order(pack))
    check_restructurings(c, pack, earlier_flags, earlier_department_outcomes(path, _department_order(pack)))
    for where, flag in required_flags:
        if flag not in all_added and flag not in earlier_flags:
            c.err(where, f"requires flag {flag!r} that nothing in this pack grants "
                  "(nor any pack with a lower department.order)")

    if encounters:
        for axis in GRADES:
            if axis not in graded_up:
                c.err("encounters", f"no outcome raises {axis}; every pack grades all four Test Results upward somewhere")
    if grade_gates:
        reach = grade_reach(pack)
        above = earlier_grade_reach(path, _department_order(pack))
        for where, axis, minimum in grade_gates:
            available = reach[axis] + above[axis]
            if minimum > available:
                c.err(where, f"requires {axis} {minimum}, but a run can earn at most {available} by this review")

    return c.errors


def check_window_shift(c: "Checker", pack: dict, encounter_ids: set[str], graded, collect) -> None:
    shift = pack.get("window_shift")
    w = "window_shift"
    if not isinstance(shift, dict):
        c.err(w, "must be an object when present")
        return
    c.slug(f"{w}.id", shift.get("id"))
    c.text(f"{w}.title", shift.get("title"), 5, 64)
    c.text(f"{w}.flavor_text", shift.get("flavor_text"), 90, 700)
    c.art(f"{w}.art", shift.get("art"))
    locations = {loc.get("location_id") for loc in pack.get("locations") or []}
    if shift.get("location_id") not in locations:
        c.err(w, f"location_id {shift.get('location_id')!r} is not a location in this pack")
    memo = shift.get("memo") or {}
    c.text(f"{w}.memo.title", memo.get("title"), 5, 80)
    rules = memo.get("rules") or []
    rule_ids = [r.get("id") for r in rules if isinstance(r, dict)]
    if not 2 <= len(rules) <= 4 or len(set(rule_ids)) != len(rules):
        c.err(f"{w}.memo.rules", "needs 2-4 rules with unique ids")
    for r in rules:
        c.slug(f"{w}.memo.rules.id", r.get("id"))
        c.text(f"{w}.memo.rules[{r.get('id')}].text", r.get("text"), 15, 140)
    applicants = shift.get("applicants") or []
    if not 3 <= len(applicants) <= 5:
        c.err(f"{w}.applicants", "a shift sees 3-5 applicants")
    seen: set[str] = set()
    broken_rules: set[str] = set()
    stamps = {"approve": 0, "deny": 0}
    bite = False
    for a in applicants:
        aid = a.get("id")
        aw = f"{w}.applicants[{aid}]"
        c.slug(f"{aw}.id", aid)
        if aid in seen or aid in encounter_ids:
            c.err(aw, "applicant ids must be unique and differ from encounter ids")
        seen.add(aid)
        c.text(f"{aw}.name", a.get("name"), 3, 48)
        c.text(f"{aw}.request", a.get("request"), 15, 160)
        c.text(f"{aw}.plea", a.get("plea"), 20, 300)
        c.art(f"{aw}.art", a.get("art"))
        documents = a.get("documents") or []
        if not 2 <= len(documents) <= 4:
            c.err(aw, "needs 2-4 documents")
        breaks = []
        for d in documents:
            c.text(f"{aw}.documents.label", d.get("label"), 3, 40)
            c.text(f"{aw}.documents.value", d.get("value"), 2, 80)
            if d.get("breaks") is not None:
                if d["breaks"] not in rule_ids:
                    c.err(aw, f"document breaks unknown rule {d['breaks']!r}")
                breaks.append(d["breaks"])
        if len(breaks) > 1:
            c.err(aw, "an applicant breaks at most one rule, so the shift reads at a glance")
        broken_rules.update(breaks)
        choices = a.get("choices") or []
        if sorted(ch.get("id") for ch in choices) != sorted(WINDOW_STAMPS):
            c.err(aw, "offers exactly two stamps: approve and deny")
            continue
        book = by_the_book(a)
        stamps[book] += 1
        for ch in choices:
            cw = f"{aw}.choices[{ch.get('id')}]"
            c.choice(cw, ch)
            if ch.get("roll") is not None or ch.get("requires") is not None:
                c.err(cw, "a stamp is certain and open to everyone: roll and requires are null")
            effects = (ch.get("success") or {}).get("effects") or {}
            grades = (ch.get("success") or {}).get("grades") or {}
            if ch.get("id") != book and (effects.get("suspicion") or 0) < 1:
                c.err(cw, "stamping against the memo must raise Suspicion (PAL audits every stamp)")
            if ch.get("id") == book and (grades.get("empathy") or 0) < 0:
                bite = True
        if not graded(choices):
            c.err(aw, "no stamp grades the player")
        collect(aw, choices)
    for rid in rule_ids:
        if rid not in broken_rules:
            c.err(f"{w}.memo.rules[{rid}]", "no applicant breaks this rule, so it never matters")
    if applicants and not stamps["approve"]:
        c.err(f"{w}.applicants", "at least one applicant must be clean (the memo says approve)")
    if applicants and not stamps["deny"]:
        c.err(f"{w}.applicants", "at least one applicant must break a rule")
    if applicants and not bite:
        c.err(f"{w}.applicants", "at least one by-the-book stamp must cost Empathy; the memo is never simply kind")


def check_restructurings(c: "Checker", pack: dict, earlier_flags: set[str], earlier_outcomes: set[str]) -> None:
    order = _department_order(pack)
    items = pack.get("restructurings")
    if order == 1:
        if items:
            c.err("restructurings", "the surface department has nothing above it to restructure from")
        return
    if not isinstance(items, list) or not items:
        c.err("restructurings", "every department below the surface needs Restructuring memos (DESIGN-BRIEF Rules v1)")
        return
    location_ids = {loc.get("location_id") for loc in pack.get("locations") or []}
    seen: set[str] = set()
    for i, item in enumerate(items):
        w = f"restructurings[{item.get('id') if isinstance(item, dict) else i}]"
        if not isinstance(item, dict):
            c.err(w, "must be an object")
            continue
        c.slug(f"{w}.id", item.get("id"))
        if item.get("id") in seen:
            c.err(w, "ids must be unique")
        seen.add(item.get("id"))
        kind = item.get("kind")
        if kind not in RESTRUCTURE_LOCATIONS:
            c.err(w, f"kind must be one of {sorted(RESTRUCTURE_LOCATIONS)}")
            continue
        locs = item.get("location_ids")
        if not isinstance(locs, list) or len(locs) != RESTRUCTURE_LOCATIONS[kind] or len(set(locs)) != len(locs):
            c.err(w, f"a {kind} memo names exactly {RESTRUCTURE_LOCATIONS[kind]} distinct location(s)")
        else:
            for loc in locs:
                if loc not in location_ids:
                    c.err(w, f"unknown location {loc!r}")
        if kind == "merge":
            c.text(f"{w}.title", item.get("title"), 5, 48)
        elif kind == "add" and item.get("title") is not None:
            c.text(f"{w}.title", item.get("title"), 5, 48)
        reason = item.get("reason")
        c.text(f"{w}.reason", reason, 40, 300)
        if isinstance(reason, str) and not reason.rstrip().endswith((".", "!", "?")):
            c.err(f"{w}.reason", "must be complete sentences")
        when = item.get("when", "missing")
        last = i == len(items) - 1
        if when is None:
            if not last:
                c.err(w, "the default memo (when: null) must come last")
            continue
        if last:
            c.err(w, "the last memo must be the default (when: null)")
        if not isinstance(when, dict) or set(when) - {"outcomes", "flags"}:
            c.err(f"{w}.when", "must be null or an object with outcomes and/or flags")
            continue
        outcomes = when.get("outcomes") or []
        flags = when.get("flags") or []
        if not outcomes and not flags:
            c.err(f"{w}.when", "names no outcome or flag; use when: null for the default")
        for o in outcomes:
            if o not in earlier_outcomes:
                c.err(f"{w}.when", f"outcome {o!r} is not a department outcome above this one")
        for f in flags:
            if f not in earlier_flags:
                c.err(f"{w}.when", f"flag {f!r} is not granted by any department above this one")


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
    results = decks.get("test_results")
    if not isinstance(results, dict):
        errors.append("DECKS: test_results is required (hidden Test Results, t-022)")
        return errors
    axes = {a.get("id"): a for a in results.get("axes") or [] if isinstance(a, dict)}
    if set(axes) != set(GRADES):
        errors.append(f"DECKS: test_results.axes must be exactly {list(GRADES)}")
    for aid, axis in axes.items():
        for key in ("title", "high", "low"):
            value = axis.get(key)
            if not isinstance(value, str) or len(value.strip()) < (3 if key == "title" else 30):
                errors.append(f"DECKS: test_results axis {aid!r} needs {key}")
    verdicts = {v.get("axis"): v for v in results.get("verdicts") or [] if isinstance(v, dict)}
    if set(verdicts) != VERDICT_AXES:
        errors.append(f"DECKS: test_results.verdicts must cover {sorted(VERDICT_AXES)}")
    for vid, verdict in verdicts.items():
        if not isinstance(verdict.get("title"), str) or len(verdict["title"].strip()) < 3:
            errors.append(f"DECKS: test_results verdict {vid!r} needs a title")
        text = verdict.get("text")
        if not isinstance(text, str) or len(text.strip()) < 60 or not text.rstrip().endswith((".", "!", "?")):
            errors.append(f"DECKS: test_results verdict {vid!r} needs complete-sentence text of at least 60 chars")
    return errors


def _loaded(packs: list[Path]) -> list[tuple[Path, dict]]:
    out = []
    for p in packs:
        try:
            out.append((p, json.loads(p.read_text(encoding="utf-8"))))
        except (OSError, json.JSONDecodeError):
            continue
    return sorted(out, key=lambda pp: _department_order(pp[1]) or 0)


def validate_endings(path: Path, packs: list[Path]) -> list[str]:
    errors: list[str] = []
    doc = json.loads(path.read_text(encoding="utf-8"))
    loaded = _loaded(packs)
    if not loaded:
        return ["ENDINGS: no department packs to check against"]
    granted: set[str] = set()
    for _, pack in loaded:
        granted |= granted_flags(pack)
    bottom = loaded[-1][1]
    boss = bottom.get("boss") or {}
    outcome_ids = [o.get("id") for o in boss.get("department_outcomes") or []]
    endings = doc.get("endings") or []
    if len(endings) < 10:
        errors.append(f"ENDINGS: need at least ten endings, have {len(endings)}")
    ids = [e.get("id") for e in endings]
    if len(set(ids)) != len(ids):
        errors.append("ENDINGS: ending ids must be unique")
    board_outcomes = set()
    defaults = 0
    for e in endings:
        w = f"ENDINGS: {e.get('id')!r}"
        if e.get("kind") not in ENDING_KINDS:
            errors.append(f"{w} kind must be one of {sorted(ENDING_KINDS)}")
            continue
        trig = e.get("trigger") or {}
        if e["kind"] == "board":
            oid = trig.get("department_outcome")
            if oid not in outcome_ids:
                errors.append(f"{w} must name an outcome of {boss.get('id')!r}")
            board_outcomes.add(oid)
        else:
            if trig.get("status") != "eliminated":
                errors.append(f"{w} elimination endings trigger on status 'eliminated'")
            flag = trig.get("flag")
            if flag is None:
                defaults += 1
                if e["kind"] == "secret":
                    errors.append(f"{w} a secret ending needs a flag")
            elif flag not in granted:
                errors.append(f"{w} keys on flag {flag!r}, which no pack grants")
        epi = e.get("epilogue") or {}
        if not isinstance(epi.get("title"), str) or len(epi["title"].strip()) < 3:
            errors.append(f"{w} epilogue needs a title")
        text = epi.get("text")
        if not isinstance(text, str) or text.count(". ") < 1 or not text.rstrip().endswith((".", "!", "?")):
            errors.append(f"{w} epilogue needs at least two complete sentences")
        for problem in prompt_errors(epi.get("art_prompt")):
            errors.append(f"{w} epilogue art_prompt: {problem}")
        for v in e.get("variants") or []:
            if v.get("when_flag") not in granted:
                errors.append(f"{w} variant keys on {v.get('when_flag')!r}, which no pack grants")
            vt = v.get("text")
            if not isinstance(vt, str) or not vt.rstrip().endswith((".", "!", "?")):
                errors.append(f"{w} variant text must be a complete sentence")
    for oid in outcome_ids:
        if oid not in board_outcomes:
            errors.append(f"ENDINGS: outcome {oid!r} of {boss.get('id')!r} has no ending")
    if defaults != 1:
        errors.append(f"ENDINGS: need exactly one default elimination ending, have {defaults}")
    return errors


def flag_map(packs: list[Path], endings_path: Path | None = None) -> dict:
    """Every flag: which pack/card/choice grants it and which reads it (requires, Restructuring, societies, endings)."""
    flags: dict[str, dict[str, list[str]]] = {}

    def entry(f):
        return flags.setdefault(f, {"granted_by": [], "read_by": []})

    for _, pack in _loaded(packs):
        dept = (pack.get("department") or {}).get("id")
        boss = pack.get("boss") if isinstance(pack.get("boss"), dict) else {}
        cards = (pack.get("encounters") or []) + window_applicants(pack) + ([boss] if boss else [])
        for card in cards:
            for ch in card.get("choices") or []:
                where = f"{dept}/{card.get('id')}/{ch.get('id')}"
                for key in ("success", "failure"):
                    for f in (ch.get(key) or {}).get("add_flags") or []:
                        if where not in entry(f)["granted_by"]:
                            entry(f)["granted_by"].append(where)
                req = ch.get("requires") or {}
                if isinstance(req, dict) and req.get("flag"):
                    entry(req["flag"])["read_by"].append(f"{where} (requires)")
        for m in pack.get("restructurings") or []:
            for f in ((m.get("when") or {}).get("flags") or []):
                entry(f)["read_by"].append(f"{dept} restructuring {m.get('id')}")
    decks_path = packs[0].parent / "DECKS.json" if packs else None
    if decks_path and decks_path.exists():
        decks = json.loads(decks_path.read_text(encoding="utf-8"))
        for soc in decks.get("societies") or []:
            for key in ("objectives", "betrayals"):
                for dept, fl in (soc.get(key) or {}).items():
                    for f in fl:
                        entry(f)["read_by"].append(f"society {soc.get('id')} {key[:-1]} ({dept})")
    if endings_path and endings_path.exists():
        doc = json.loads(endings_path.read_text(encoding="utf-8"))
        for e in doc.get("endings") or []:
            f = (e.get("trigger") or {}).get("flag")
            if f:
                entry(f)["read_by"].append(f"ending {e.get('id')} (trigger)")
            for v in e.get("variants") or []:
                entry(v.get("when_flag"))["read_by"].append(f"ending {e.get('id')} (variant)")
    return {"schema_version": 1, "generated_by": "validate_pack.py --flag-map", "flags": dict(sorted(flags.items()))}


def flag_map_errors(packs: list[Path], directory: Path = HERE) -> list[str]:
    errors = []
    current = flag_map(packs, directory / "ENDINGS.json")
    for f, info in current["flags"].items():
        if info["read_by"] and not info["granted_by"]:
            errors.append(f"FLAG-MAP: {f!r} is read ({info['read_by'][0]}) but granted by no pack")
    committed = directory / "FLAG-MAP.json"
    if not committed.exists() or json.loads(committed.read_text(encoding="utf-8")) != current:
        errors.append("FLAG-MAP: FLAG-MAP.json is stale; regenerate with `validate_pack.py --flag-map`")
    return errors


def main(argv: list[str]) -> int:
    if argv == ["--flag-map"]:
        packs = pack_paths([])
        (HERE / "FLAG-MAP.json").write_text(
            json.dumps(flag_map(packs, HERE / "ENDINGS.json"), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("wrote FLAG-MAP.json")
        return 0
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
            print(f"OK {decks.name}: job titles, societies, mutations and Test Results check out")
    endings = HERE / "ENDINGS.json"
    if not argv and endings.exists():
        ending_errors = validate_endings(endings, paths) + flag_map_errors(paths)
        errors.extend(ending_errors)
        if not ending_errors:
            print(f"OK {endings.name} and FLAG-MAP.json: every ending covered, every flag accounted for")
    for e in errors:
        print(e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
