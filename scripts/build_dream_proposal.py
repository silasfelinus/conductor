#!/usr/bin/env python3
"""Create a deterministic Facet-seeded six-asset daily dream proposal."""
from __future__ import annotations

import argparse, copy, hashlib, json, random, re, subprocess, sys
import urllib.error, urllib.parse, urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo
import yaml

ROOT = Path(__file__).resolve().parent.parent
BACKLOG = ROOT / "projects/dream-cycle/backlog"
KR_BASE_URL = "https://kindrobots.org"
PACIFIC = ZoneInfo("America/Los_Angeles")

# Network-free keys known to exist in the live catalog. The sidecar resolves slugs.
FALLBACK_FACETS = {
 "GENRE": ["artificial-intelligence|Artificial Intelligence", "horror-comedy|Horror Comedy",
   "bureaucratic-fantasy|Bureaucratic Fantasy", "archive-horror|Archive Horror",
   "absurdist-comedy|Absurdist Comedy", "cartoon-noir|Cartoon Noir", "biopunk|Biopunk",
   "anachronism-mystery|Anachronism Mystery", "academic-eldritch|Academic Eldritch", "carnival|Carnival"],
 "ANIMAL": ["capybara|Capybara", "axolotl|Axolotl", "cassowary|Cassowary", "binturong|Binturong", "atlantic-puffin|Atlantic Puffin"],
 "SPECIES": ["catfolk|Catfolk", "birdfolk|Birdfolk", "android|Android", "changeling|Changeling", "butterfly|Butterfly"],
 "OCCUPATION": ["alien-biologist|Alien Biologist", "accountant|Accountant", "cactus-wrangler|Cactus Wrangler", "chaos-consultant|Chaos Consultant", "accidental-diplomat|Accidental Diplomat"],
 "MATERIAL": ["aether-silk|Aether Silk", "astral-ore|Astral Ore", "bone-glass|Bone Glass", "ancient-marble|Ancient Marble", "arcane-silver|Arcane Silver"],
 "PERSONALITY": ["bookworm|Bookworm", "cautious|Cautious", "charismatic|Charismatic", "analytical|Analytical", "personality-buoyant|Buoyant"],
 # Rotation pool. Silas, 2026-09-02: "(rotating which kind of facets we grab
 # from and which ones we create)". The six above were the whole seed vocabulary
 # for every dream ever built, which is why so many bundles read alike -- a
 # genre pair plus a creature plus a job, forever. These widen what a day can be
 # seeded from. Fallbacks stay short on purpose: they exist so an offline run
 # still produces a valid bundle, not to be a second catalog.
 "ARCHETYPE": ["trickster|Trickster", "caretaker|Caretaker", "reluctant-heir|Reluctant Heir", "quiet-professional|Quiet Professional", "false-authority|False Authority"],
 "QUIRK": ["counts-under-breath|Counts Under Breath", "keeps-receipts|Keeps Receipts", "never-sits-down|Never Sits Down", "narrates-own-actions|Narrates Own Actions", "collects-broken-things|Collects Broken Things"],
 "THEME": ["debt|Debt", "inheritance|Inheritance", "quarantine|Quarantine", "restoration|Restoration", "succession|Succession"],
 "STYLE": ["woodblock|Woodblock", "tintype|Tintype", "risograph|Risograph", "stained-glass|Stained Glass", "chalk-pastel|Chalk Pastel"],
 "SETTING": ["tidal-flat|Tidal Flat", "night-market|Night Market", "shuttered-observatory|Shuttered Observatory", "company-town|Company Town", "cable-ferry|Cable Ferry"],
 "BACKSTORY": ["demoted|Demoted", "raised-by-committee|Raised By Committee", "sole-survivor|Sole Survivor", "bought-out|Bought Out", "returned-late|Returned Late"],
 "ROLE": ["witness|Witness", "fixer|Fixer", "understudy|Understudy", "inspector|Inspector", "courier|Courier"],
 "ALIGNMENT": ["lawful-tired|Lawful Tired", "chaotic-kind|Chaotic Kind", "neutral-stubborn|Neutral Stubborn", "loyal-to-a-fault|Loyal To A Fault", "principled-broke|Principled Broke"],
}

# The genre pair is the umbrella every element inherits, so GENRE is drawn every
# day and is not part of the rotation. These are the slots that rotate.
CREATURE_TAXONOMIES = ("ANIMAL", "SPECIES")
FLAVOUR_TAXONOMIES = ("OCCUPATION", "PERSONALITY", "ARCHETYPE", "QUIRK",
                      "THEME", "SETTING", "BACKSTORY", "ROLE", "ALIGNMENT", "STYLE")

# WHERE A NEW FACET MAY BE INVENTED, and where it may not.
#
# Silas, 2026-09-02: "I would like each dream to include 1-2 new facets ... they
# should be different and fill a gap that we don't have."
#
# This list is the one real judgement call in that feature, so it is written
# down rather than inferred. Everything here is creative VOCABULARY -- a word
# the fiction can be built out of, where a new entry widens what a dream can be.
#
# Deliberately absent, and why:
#   DREAM_TYPE, REWARD_TYPE, RARITY, BOT_TYPE  structural enums that mirror
#     database types. Inventing one invents a schema value, not a story idea,
#     and several have zero randomizable rows precisely because they are
#     dispatch keys rather than flavour.
#   GENDER      identity vocabulary. Not a gap for a nightly script to fill on
#     its own initiative.
#   COLOR       a nearly closed set, already 180 deep.
#   ART_DIRECTION, PROMPT_ENHANCEMENT  render instructions aimed at Krea 2, not
#     at the fiction. A bad entry here degrades every image that picks it up.
INVENTABLE_TAXONOMIES = ("GENRE", "ANIMAL", "SPECIES", "OCCUPATION", "MATERIAL",
                         "PERSONALITY", "ARCHETYPE", "QUIRK", "THEME", "STYLE",
                         "SETTING", "BACKSTORY", "ROLE", "ALIGNMENT")
FIELDS = {
 "location": ("title", "known_for", "local_rule", "best_scene", "art_direction"),
 "character": ("name", "role_drive", "carries", "complication", "look"),
 # `look` is required as of 2026-08-08. Without it a Reward's only visual input
 # was what it *does* ("surfaces the hidden fortune buried in a person"), which
 # gives Krea 2 nothing to draw and lets the style tail take over the subject —
 # that is how item-tidefortune-ladle rendered as a crowd of people.
 "reward": ("name", "reward_type", "rarity", "grants", "best_used_when", "catch", "look"),
 "scenario": ("title", "setup"),
}


def _target_date(now: datetime | None = None) -> str:
    now = now or datetime.now(PACIFIC)
    if now.tzinfo is None: now = now.replace(tzinfo=PACIFIC)
    return now.astimezone(PACIFIC).date().isoformat()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-") or "daily-dream"


def _clean(raw: dict[str, Any]) -> dict[str, Any]:
    out = {"title": str(raw.get("title") or raw.get("canonicalValue") or raw.get("slug") or "").strip(),
           "slug": str(raw.get("slug") or "").strip(),
           "taxonomy": str(raw.get("taxonomy") or "").upper(),
           "randomWeight": max(float(raw.get("randomWeight") or 1), .0001)}
    if isinstance(raw.get("id"), int): out["id"] = raw["id"]
    if raw.get("canonicalValue"): out["canonicalValue"] = str(raw["canonicalValue"])
    return out


def _fallback(taxonomy: str) -> list[dict[str, Any]]:
    return [_clean({"slug": pair.split("|", 1)[0], "title": pair.split("|", 1)[1], "taxonomy": taxonomy})
            for pair in FALLBACK_FACETS[taxonomy]]


def fetch_live_facets(taxonomy: str, timeout: int = 12) -> list[dict[str, Any]] | None:
    found, skip, take = [], 0, 250
    while True:
        url = f"{KR_BASE_URL}/api/facets?" + urllib.parse.urlencode({"taxonomy": taxonomy, "take": take, "skip": skip})
        req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "conductor-daily-dream/2"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as res: payload = json.loads(res.read())
        except (OSError, ValueError, urllib.error.URLError): return None
        rows = payload.get("data") if isinstance(payload, dict) else None
        if not isinstance(rows, list): return None
        for row in rows:
            if not isinstance(row, dict) or row.get("isActive") is False or row.get("isPublic") is False: continue
            if row.get("isRandomizable") is False or float(row.get("randomWeight") or 0) <= 0: continue
            facet = _clean(row)
            if facet["title"] and facet["slug"]: found.append(facet)
        if len(rows) < take: break
        skip += take
    return list({row["slug"].casefold(): row for row in found}.values()) or None


def fetch_facet_catalog() -> tuple[dict[str, list[dict[str, Any]]], str]:
    catalog, live = {}, True
    for taxonomy in FALLBACK_FACETS:
        rows = fetch_live_facets(taxonomy)
        if not rows: rows, live = _fallback(taxonomy), False
        catalog[taxonomy] = rows
    return catalog, "live" if live else "mixed-fallback"


def _draw(rng: random.Random, pool: list[dict[str, Any]], count: int = 1) -> list[dict[str, Any]]:
    if len(pool) < count: raise ValueError(f"Facet pool has {len(pool)} entries; {count} required")
    left, chosen = list(pool), []
    for _ in range(count):
        pick = copy.deepcopy(rng.choices(left, weights=[max(float(x.get("randomWeight") or 1), .0001) for x in left], k=1)[0])
        chosen.append(pick); left = [x for x in left if x["slug"].casefold() != pick["slug"].casefold()]
    return chosen


def plan_inventions(
    rng: random.Random,
    catalog: dict[str, list[dict[str, Any]]],
    seeded_taxonomies: set[str],
    count: int = 2,
) -> list[dict[str, Any]]:
    """Pick the taxonomies today's two brand-new Facets should fill.

    Silas, 2026-09-02: "they should be different and fill a gap that we don't
    have. There are SO many areas this could fill."

    A gap is measurable, so it is measured rather than asserted: weight is
    inverse to how deep the taxonomy already is. Against the live catalog on
    2026-09-02 that is SETTING at 11 rows and ROLE at 19 against PERSONALITY at
    206 and GENRE at 176 -- so a new SETTING is roughly eighteen times likelier
    than a new PERSONALITY, without ever making PERSONALITY impossible.

    Taxonomies already seeding today are pushed to the back, so the day both
    draws from and invents into different corners -- Silas: "(rotating which
    kind of facets we grab from and which ones we create)". They stay eligible
    rather than banned, because on a day that seeds from four thin taxonomies
    there may be nothing thinner left.
    """
    pool = [t for t in INVENTABLE_TAXONOMIES if t in catalog]
    if not pool: return []

    chosen: list[dict[str, Any]] = []
    # Every element a new Facet can be attached to, cycled so two inventions
    # never both land on the same asset and go unused by the rest of the bundle.
    slots = ("character", "location", "scenario", "reward_item", "reward_skill")
    for index in range(min(count, len(pool))):
        weights = []
        for taxonomy in pool:
            depth = max(len(catalog.get(taxonomy) or []), 1)
            weight = 1.0 / depth
            if taxonomy in seeded_taxonomies: weight *= 0.25
            weights.append(weight)
        taxonomy = rng.choices(pool, weights=weights, k=1)[0]
        pool = [t for t in pool if t != taxonomy]
        chosen.append({
            "taxonomy": taxonomy,
            "catalog_depth": len(catalog.get(taxonomy) or []),
            # Two elements each, so an invented Facet is never a decoration that
            # appears once and never recurs in the bundle.
            "assign_to": [slots[(index * 2) % len(slots)], slots[(index * 2 + 1) % len(slots)]],
        })
    return chosen


def facet_seed_plan(day: str, catalog: dict[str, list[dict[str, Any]]] | None = None) -> dict[str, Any]:
    source = "provided"
    if catalog is None: catalog, source = fetch_facet_catalog()
    seed = int.from_bytes(hashlib.sha256(f"daily-dream-v2:{day}".encode()).digest()[:8], "big")
    rng = random.Random(seed); genres = _draw(rng, catalog["GENRE"], 7)

    # ROTATED, not fixed. Every dream ever built drew its non-genre seeds from
    # the same three taxonomies (OCCUPATION, MATERIAL, PERSONALITY), which is a
    # large part of why bundles rhymed with each other. The creature slot and
    # the two flavour slots now rotate across the wider pool.
    creature_tax = rng.choice([t for t in CREATURE_TAXONOMIES if catalog.get(t)] or ["ANIMAL"])
    flavour_pool = [t for t in FLAVOUR_TAXONOMIES if catalog.get(t)]
    flavour_taxes = rng.sample(flavour_pool, min(2, len(flavour_pool))) if flavour_pool else ["OCCUPATION"]
    while len(flavour_taxes) < 2: flavour_taxes.append(flavour_taxes[0])

    creature = _draw(rng, catalog[creature_tax])[0]
    # `wildcard` and `shared.personality` keep their names: several consumers
    # (the digest, render_markdown, the creative contract) read them by key, and
    # what rotates is which taxonomy fills them, not what they are called.
    occupation = _draw(rng, catalog[flavour_taxes[0]])[0]
    personality = _draw(rng, catalog[flavour_taxes[1]])[0]
    material = _draw(rng, catalog["MATERIAL"])[0]
    umbrella = genres[:2]
    extras = dict(zip(("location", "character", "reward_item", "reward_skill", "scenario"), genres[2:]))
    elements = {
      "vibe": [*umbrella, creature, occupation],
      "location": [*umbrella, extras["location"], creature, material],
      "character": [*umbrella, extras["character"], creature, occupation, personality],
      "reward_item": [*umbrella, extras["reward_item"], material],
      "reward_skill": [*umbrella, extras["reward_skill"], occupation],
      "scenario": [*umbrella, extras["scenario"], extras["location"], extras["character"], creature],
    }
    seeded = {"GENRE", creature_tax, "MATERIAL", *flavour_taxes}
    return {"version": 2, "date": day, "deterministic_seed": seed, "catalog_source": source,
      "umbrella": {"genres": umbrella, "creature": creature, "wildcard": occupation,
                   "wildcard_role": flavour_taxes[0].lower()},
      "shared": {"material": material, "personality": personality},
      "seeded_taxonomies": sorted(seeded),
      "invent": plan_inventions(rng, catalog, seeded),
      "extra_genres": extras, "elements": elements}


def _invention_instructions(seeds: dict[str, Any]) -> list[str]:
    """The three-phase order Silas specified for authoring a bundle.

    Silas, 2026-09-02: "proposal, we pull from previous facets to create a
    general vibe, draft 2 new facets to fill in gaps, and THEN create the other
    elements." The order is the point -- inventing after the vibe means the new
    Facets answer a premise that already exists, and inventing BEFORE the other
    five means those five can actually be built out of them. A new Facet drafted
    last would be a label stuck on a finished bundle.
    """
    invent = seeds.get("invent") if isinstance(seeds.get("invent"), list) else []
    if not invent: return []

    lines = [
        "AUTHOR IN THREE PHASES, in this order.",
        "PHASE 1 — the vibe. Build it from the existing Facets in seed_facets.elements.vibe. "
        "This is the premise everything else answers to.",
        f"PHASE 2 — invent exactly {len(invent)} brand-new Facets, before writing any other element. "
        "Return them as `seed_facets.invented`, each an object with title, slug, taxonomy, "
        "description, and art_prompt. They must NOT already exist in the catalog: a new Facet "
        "is a concept the catalog has no word for, not a synonym of one it has. "
        "Check them against the Facets you were given and against the obvious near-misses.",
    ]
    for entry in invent:
        taxonomy = entry.get("taxonomy")
        depth = entry.get("catalog_depth")
        targets = ", ".join(entry.get("assign_to") or [])
        lines.append(
            f"  - one {taxonomy} Facet (the catalog holds only {depth} of these, which is why "
            f"it is today's gap). Add it to seed_facets.elements for: {targets}."
        )
    lines += [
        "A Facet is vocabulary, not a plot. `title` is one to three words. `description` is one "
        "or two complete sentences saying what the concept IS and what it costs or complicates -- "
        "the same register as the Facets you were handed, which read like "
        "'A protagonist transported into another world and required to function there. Knowledge "
        "from the prior world is the advantage; homesickness is the price.'",
        "`art_prompt` must describe something visible, since it is what renders the Facet's own "
        "card. Follow the same rule as `look`: material, shape, scale, colour, wear, light.",
        "PHASE 3 — now write the location, character, ITEM, SKILL and scenario, using the invented "
        "Facets as real constraints on the elements they were assigned to, not as decoration.",
    ]
    return lines


def build_brief(day: str | None = None, catalog=None) -> dict[str, Any]:
    day = day or _target_date(); seeds = facet_seed_plan(day, catalog)
    return {"proposal_date": day, "seed_facets": seeds,
      "instructions": [*_invention_instructions(seeds),
        "Create one coherent bundle under the vibe, not unrelated mini-pitches.",
        "Return exactly one location, one character, one ITEM, one SKILL, and one scenario; no narrator.",
        "Use the Facets as creative constraints and persist seed_facets unchanged, "
        "except for adding `invented` and listing those new Facets in the elements they "
        "were assigned to.",
        "Author scenario last and name the vibe, location, and character in its setup.",
        "Every `look` and `art_direction` field feeds Krea 2 directly. Write what is "
        "physically visible — material, shape, scale, colour, wear, how light hits it — "
        "not what the thing does. 'A dented tin ladle the length of a forearm, its bowl "
        "worn to mirror-bright, handle wrapped in salt-stiffened cord' is usable; "
        "'it surfaces hidden fortune' is not.",
        "A reward's `look` must describe an object or a visible effect, never a person. "
        "For a SKILL, describe the visible signature of the technique in use."],
      "required_counts": {"vibe": 1, "locations": 1, "characters": 1, "reward_item": 1, "reward_skill": 1, "scenarios": 1}}


# Card copy is mixed-typography otherwise: the model writes " -- " for a dash in
# some fields and a real em-dash in others, and the two land side by side in one
# email (2026-08-31: The Continental Courtship showed " -- " directly above The
# Deep Shift's proper em-dashes). Purely presentational and semantics-free, so it
# is normalised deterministically here rather than by asking a model to rewrite
# good prose. `look`/`art_direction` are excluded as Krea prompt material.
TYPOGRAPHY_SUBS = ((re.compile(r"\s--\s"), " — "),)
_TYPOGRAPHY_SKIP_KEYS = {"look", "art_direction", "slug", "title", "name", "reward_type", "rarity"}


def normalize_typography(value: Any) -> Any:
    """Apply presentational text fixes to card copy, leaving structure untouched."""
    if isinstance(value, str):
        for pattern, replacement in TYPOGRAPHY_SUBS:
            value = pattern.sub(replacement, value)
        return value
    if isinstance(value, list):
        return [normalize_typography(item) for item in value]
    if isinstance(value, dict):
        return {
            key: (item if key in _TYPOGRAPHY_SKIP_KEYS else normalize_typography(item))
            for key, item in value.items()
        }
    return value


def normalize(proposal: dict[str, Any], avoid: set[str] | None = None) -> dict[str, Any]:
    out = normalize_typography(copy.deepcopy(proposal)); out["title"] = str(out.get("title") or "Untitled Daily Dream").strip()
    base = slugify(out.get("slug") or out["title"]); used = {x.casefold() for x in (avoid or set())}; out["slug"] = base
    n = 2
    while out["slug"].casefold() in used: out["slug"], n = f"{base}-{n}", n + 1
    for reward in out.get("rewards", []) if isinstance(out.get("rewards"), list) else []:
        if isinstance(reward, dict):
            reward["reward_type"] = str(reward.get("reward_type") or "").strip().upper()
    out.pop("narrator", None)
    return out


def _text(value: Any) -> bool: return isinstance(value, str) and bool(value.strip())


def _lookup_key(value: Any) -> str:
    """Mirror of Kind Robots' normalizeFacetLookupKey, for novelty checks.

    Deliberately the same shape as the server's: alphanumerics only, folded.
    "Night Market", "night-market" and "nightmarket" are one concept, and a
    novelty check that missed that would let the cycle mint a duplicate under a
    slightly different punctuation every night.
    """
    return re.sub(r"[^a-z0-9]+", "", str(value or "").casefold())


def validate_inventions(seeds: dict[str, Any]) -> list[str]:
    """Check today's brand-new Facets are actually new, and actually usable.

    Silas asked for Facets that are "different and fill a gap that we don't
    have", which is two separate requirements: novel, and in the taxonomy the
    plan said was thin. Both are checkable here, before anything is written to
    the catalog, which is the only cheap place to catch them -- a duplicate that
    reaches /api/facets is a row someone has to merge back out later.
    """
    plan = seeds.get("invent") if isinstance(seeds.get("invent"), list) else []
    if not plan: return []

    invented = seeds.get("invented")
    if not isinstance(invented, list) or len(invented) != len(plan):
        return [f"seed_facets.invented must be a list of exactly {len(plan)} new Facets"]

    bad: list[str] = []

    # The Facets the author was HANDED, read from the PLAN rather than from the
    # elements. The elements are the wrong source in both directions: an
    # invention is required to appear there, so a valid one collides with its
    # own entry, and excluding the invented keys to fix that would excuse an
    # invention that duplicates a seed exactly. The plan's own draws -- the
    # genre pair, the creature, the two flavour picks, the material, the five
    # extra genres -- are precisely "what the catalog already has that we gave
    # you", and nothing the author writes can edit them.
    existing: set[str] = set()
    umbrella = seeds.get("umbrella") if isinstance(seeds.get("umbrella"), dict) else {}
    shared = seeds.get("shared") if isinstance(seeds.get("shared"), dict) else {}
    extras = seeds.get("extra_genres") if isinstance(seeds.get("extra_genres"), dict) else {}
    drawn: list[Any] = [
        *(umbrella.get("genres") or []),
        umbrella.get("creature"), umbrella.get("wildcard"),
        shared.get("material"), shared.get("personality"),
        *extras.values(),
    ]
    for facet in drawn:
        if isinstance(facet, dict):
            key = _lookup_key(facet.get("slug") or facet.get("title"))
            if key: existing.add(key)

    wanted = [str(entry.get("taxonomy")) for entry in plan]
    for index, facet in enumerate(invented):
        where = f"seed_facets.invented[{index}]"
        if not isinstance(facet, dict): bad.append(f"{where} must be an object"); continue
        for field in ("title", "slug", "taxonomy", "description", "art_prompt"):
            if not _text(facet.get(field)): bad.append(f"{where} missing {field}")
        taxonomy = str(facet.get("taxonomy") or "").upper()
        if taxonomy and taxonomy not in wanted:
            bad.append(f"{where} taxonomy {taxonomy} is not one of today's gaps: {wanted}")
        if taxonomy and taxonomy not in INVENTABLE_TAXONOMIES:
            bad.append(f"{where} taxonomy {taxonomy} is not inventable")
        key = _lookup_key(facet.get("slug") or facet.get("title"))
        if key and key in existing:
            bad.append(f"{where} duplicates a Facet already in play: {facet.get('slug')}")
        if key: existing.add(key)
        if _text(facet.get("slug")) and slugify(str(facet["slug"])) != str(facet["slug"]).strip().casefold():
            bad.append(f"{where} slug must be lower-case and hyphenated: {facet.get('slug')}")

    # Each invention has to actually reach the elements it was planned for,
    # otherwise it is created in the catalog and then linked to nothing.
    elements = seeds.get("elements") if isinstance(seeds.get("elements"), dict) else {}
    for entry, facet in zip(plan, invented):
        if not isinstance(facet, dict): continue
        key = _lookup_key(facet.get("slug") or facet.get("title"))
        for target in entry.get("assign_to") or []:
            rows = elements.get(target)
            keys = {_lookup_key(f.get("slug") or f.get("title"))
                    for f in rows if isinstance(f, dict)} if isinstance(rows, list) else set()
            if key not in keys:
                bad.append(f"invented Facet {facet.get('slug')} is missing from seed_facets.elements.{target}")
    return bad


def validate_proposal(proposal: Any) -> list[str]:
    if not isinstance(proposal, dict): return ["proposal must be an object"]
    bad = []
    for field in ("title", "slug", "idea"):
        if not _text(proposal.get(field)): bad.append(f"missing {field}")
    for label, obj, fields in [("vibe", proposal.get("vibe"), ("title", "line", "art_direction"))]:
        if not isinstance(obj, dict): bad.append(f"{label} must be an object")
        else:
            for field in fields:
                if not _text(obj.get(field)): bad.append(f"{label} missing {field}")
    for key, count, kind in (("locations",1,"location"),("characters",1,"character"),("rewards",2,"reward"),("scenarios",1,"scenario")):
        rows = proposal.get(key)
        if not isinstance(rows, list) or len(rows) != count: bad.append(f"{key} must be a list of exactly {count}"); continue
        for i, row in enumerate(rows):
            if not isinstance(row, dict): bad.append(f"{key}[{i}] must be an object"); continue
            for field in FIELDS[kind]:
                if not _text(row.get(field)): bad.append(f"{key}[{i}] missing {field}")
    rewards = proposal.get("rewards") if isinstance(proposal.get("rewards"), list) else []
    if sorted(str(x.get("reward_type") or "").upper() for x in rewards if isinstance(x, dict)) != ["ITEM","SKILL"]:
        bad.append("rewards must contain exactly one ITEM and one SKILL")
    if proposal.get("narrator"): bad.append("narrator is not part of the six-asset daily bundle")
    seeds = proposal.get("seed_facets"); elements = seeds.get("elements") if isinstance(seeds, dict) else None
    if not isinstance(seeds, dict): bad.append("seed_facets must be an object")
    elif not isinstance(seeds.get("umbrella",{}).get("genres"), list) or len(seeds["umbrella"]["genres"]) != 2:
        bad.append("seed_facets.umbrella.genres must contain exactly 2 Facets")
    if not isinstance(elements, dict): bad.append("seed_facets.elements must be an object")
    else:
        for key in ("vibe","location","character","reward_item","reward_skill","scenario"):
            if not isinstance(elements.get(key), list) or not elements[key]: bad.append(f"seed_facets.elements.{key} must be a non-empty list")
            else:
                for facet in elements[key]:
                    if not isinstance(facet, dict) or not _text(facet.get("title")) or not _text(facet.get("taxonomy")) or not (_text(facet.get("slug")) or isinstance(facet.get("id"), int)):
                        bad.append(f"seed_facets.elements.{key} contains an invalid Facet")
    if isinstance(seeds, dict): bad += validate_inventions(seeds)
    if all(isinstance(proposal.get(k), list) and proposal[k] for k in ("locations","characters","scenarios")) and isinstance(proposal.get("vibe"), dict):
        setup = str(proposal["scenarios"][0].get("setup") or "").casefold()
        for label, name in (("vibe",proposal["vibe"].get("title")),("location",proposal["locations"][0].get("title")),("character",proposal["characters"][0].get("name"))):
            if _text(name) and str(name).casefold() not in setup: bad.append(f"scenario setup must name the {label}: {name}")
    return bad


def _frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8"); end = text.find("\n---\n", 4)
    if not text.startswith("---\n") or end < 0: return {}
    value = yaml.safe_load(text[4:end]); return value if isinstance(value, dict) else {}


def _files(): return sorted(BACKLOG.glob("*.md")) if BACKLOG.exists() else []
def proposal_exists_for(day: str) -> bool: return any(str(_frontmatter(p).get("proposal_date") or "") == day for p in _files())
def existing_slugs() -> set[str]: return {str(_frontmatter(p).get("slug")) for p in _files() if _frontmatter(p).get("slug")}


# How many unbuilt proposals are enough. The builder drains one a day, so this is
# roughly "days of runway" -- deep enough to absorb a failed digest run or a
# blocked build, shallow enough that the docket stays fresh and reviewable.
# Silas, 2026-08-31: "we don't need to spend effort writing new proposals if we
# have a backlog (though a 5 day or so buffer seems reasonable, just in case)."
TARGET_BUFFER_DAYS = 5


def unbuilt_backlog() -> list[str]:
    """Proposal dates authored but not yet built, oldest first — the build docket.

    Legacy pre-v2 outlines carry `proposal: false` and are idea inventory rather
    than docket entries, so they are excluded. `_template-proposal.md` is also
    excluded despite carrying `proposal: true` and a 2026-01-01 placeholder date
    — the same skip build_dream_records.find_proposals() applies, without which
    the template silently inflates the docket by one and stops authoring a day
    early.
    """
    days: list[str] = []
    for path in _files():
        if path.name.startswith("_") or path.name == "README.md":
            continue
        fm = _frontmatter(path)
        if not fm.get("proposal"):
            continue
        if re.search(r"<!--\s*built-data", path.read_text(encoding="utf-8")):
            continue
        days.append(str(fm.get("proposal_date") or fm.get("created") or path.name[:10]))
    return sorted(days)


def fetch_main(quiet: bool=True) -> bool:
    try: return subprocess.run(["git","fetch","origin","main"],cwd=ROOT,check=False,capture_output=quiet,text=True).returncode == 0
    except OSError: return False


def remote_proposal_for(day: str) -> str | None:
    try:
        names = subprocess.run(["git","ls-tree","-r","--name-only","origin/main","--","projects/dream-cycle/backlog"],cwd=ROOT,capture_output=True,text=True).stdout
        for name in names.splitlines():
            shown = subprocess.run(["git","show",f"origin/main:{name}"],cwd=ROOT,capture_output=True,text=True)
            if shown.returncode == 0 and re.search(rf"(?m)^proposal_date:\s*['\"]?{re.escape(day)}['\"]?\s*$", shown.stdout): return Path(name).name
    except OSError: pass
    return None


def _titles(values): return " · ".join(str(x.get("title") or x.get("slug")) for x in values)


def render_markdown(p: dict[str, Any], day: str) -> str:
    s=p["seed_facets"]; e=s["elements"]; loc=p["locations"][0]; ch=p["characters"][0]; sc=p["scenarios"][0]
    item=next(x for x in p["rewards"] if x["reward_type"]=="ITEM"); skill=next(x for x in p["rewards"] if x["reward_type"]=="SKILL")
    lines=["---",f"slug: {p['slug']}",f"title: {p['title']}","type: dream","status: outline","priority: normal","narrator: 'no'",f"created: '{day}'","proposal: true",f"proposal_date: '{day}'","built_pr: null","---","","## Seed Facets",
      f"- **Deterministic seed:** `{s.get('deterministic_seed')}` ({s.get('catalog_source','unknown')} catalog)",
      *[f"- **{label}:** {_titles(e[key])}" for label,key in (("Dream vibe","vibe"),("Dream location","location"),("Character","character"),("Reward item","reward_item"),("Reward skill","reward_skill"),("Scenario","scenario"))],
      # The new Facets get their own section rather than blending into the
      # seed list above: what the catalog gained today is the part worth being
      # able to find later, and it is invisible once it reads like a seed.
      *([""] + ["## New Facets (invented for this dream)"] +
        [f"- **{f.get('title')}** (`{f.get('slug')}`, {f.get('taxonomy')}) — {f.get('description')}"
         for f in s.get("invented") or []]
        if s.get("invented") else []),
      "","## The idea",p["idea"],"","## Dream vibe (1)",f"**{p['vibe']['title']}** — {p['vibe']['line']}",f"Art: {p['vibe']['art_direction']}","","## Dream location (1)",f"- **{loc['title']}** — {loc['known_for']} Local rule: {loc['local_rule']} Best scene: {loc['best_scene']} Art: {loc['art_direction']}","","## Character (1)",f"- **{ch['name']}** — {ch['role_drive']} {ch['carries']} Complication: {ch['complication']} Look: {ch['look']}","","## Reward item (1)",f"- **{item['name']}** (ITEM, {item['rarity']}) — {item['grants']} Best used when: {item['best_used_when']} The catch: {item['catch']} Look: {item['look']}","","## Reward skill (1)",f"- **{skill['name']}** (SKILL, {skill['rarity']}) — {skill['grants']} Best used when: {skill['best_used_when']} The catch: {skill['catch']} Look: {skill['look']}","","## Scenario (1, authored last)",f"- **{sc['title']}** — {sc['setup']}","","## Notes from Silas","- (leave notes here — agents fold them in before building and never edit this section)","","## Build log",f"- {day} | proposed | deterministic Facet-seeded six-asset bundle","","<!-- proposal-data",json.dumps(p,ensure_ascii=False,sort_keys=True),"-->",""]
    return "\n".join(lines)


def write_proposal(proposal: dict[str, Any], *, date: str|None=None, fetch: bool=True,
                   dry_run: bool=False, force: bool=False) -> Path|None:
    day=date or _target_date()
    if not force and (proposal_exists_for(day) or (fetch and fetch_main() and remote_proposal_for(day))):
        print(f"Proposal already exists for {day}; refusing duplicate.",file=sys.stderr); return None
    proposal=normalize(proposal,existing_slugs()); bad=validate_proposal(proposal)
    if bad: raise ValueError("Invalid proposal:\n- " + "\n- ".join(bad))
    path=BACKLOG/f"{day}-{proposal['slug']}.md"; rendered=render_markdown(proposal,day)
    if dry_run:
        print(rendered); print(f"# would write: {path}", file=sys.stderr); return path
    BACKLOG.mkdir(parents=True,exist_ok=True); path.write_text(rendered,encoding="utf-8"); print(path); return path


def main(argv=None) -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check",action="store_true",help="exit 0 if the date has a proposal, otherwise 1")
    ap.add_argument("--brief",action="store_true",help="print the authoring brief and Facet seed")
    ap.add_argument("--from-json",metavar="FILE",help="validate and write JSON ('-' for stdin)")
    ap.add_argument("--sample",action="store_true",help="render or write the built-in sample")
    ap.add_argument("--date",help="override Pacific date (YYYY-MM-DD)")
    ap.add_argument("--fetch",action="store_true",help="with --check, consult fresh origin/main")
    ap.add_argument("--no-fetch",action="store_true",help="skip the origin/main write guard")
    ap.add_argument("--dry-run",action="store_true",help="print markdown without writing")
    ap.add_argument("--force",action="store_true",help="write even if the date exists")
    a=ap.parse_args(argv); day=a.date or _target_date()
    if a.check:
        # The docket, not the calendar, is what "healthy" means now: authoring
        # pauses while the buffer is deep, so a missing proposal dated today is
        # expected and is not a failure. An EMPTY docket is the real alarm --
        # that is the state where tomorrow has nothing to build.
        if a.fetch: fetch_main()
        backlog=unbuilt_backlog()
        if not backlog:
            print("Dream docket is EMPTY: nothing is queued to build. "
                  "Run --brief, author the six-asset JSON, then pass it to --from-json.")
            return 1
        span=f"{backlog[0]}..{backlog[-1]}" if len(backlog) > 1 else backlog[0]
        note=("" if len(backlog) >= TARGET_BUFFER_DAYS
              else f" Below the {TARGET_BUFFER_DAYS}-day buffer; author ONE proposal this session (--brief, then --from-json).")
        print(f"Dream docket holds {len(backlog)} unbuilt proposal(s) ({span}).{note}")
        return 0
    if a.brief: print(json.dumps(build_brief(day),indent=2,ensure_ascii=False)); return 0
    if a.sample:
        return 0 if write_proposal(copy.deepcopy(SAMPLE_PROPOSAL),date=day,fetch=False,
                                   dry_run=a.dry_run,force=True) else 1
    if a.from_json:
        try:
            raw=sys.stdin.read() if a.from_json=="-" else Path(a.from_json).read_text(encoding="utf-8")
            proposal=json.loads(raw)
        except (OSError,json.JSONDecodeError) as error:
            print(f"Could not read proposal JSON: {error}",file=sys.stderr); return 1
        proposal.setdefault("seed_facets",facet_seed_plan(day))
        return 0 if write_proposal(proposal,date=day,fetch=not a.no_fetch,
                                   dry_run=a.dry_run,force=a.force) else 1
    ap.error("choose --check, --brief, --from-json, or --sample"); return 2


def _sample() -> dict[str,Any]:
    # Every user-facing prose field here is a complete sentence on purpose: this
    # sample is the worked example of the card-copy contract enforced by
    # dream_prose_quality.complaints(). `look`/`art_direction` stay as visual
    # noun phrases because they feed Krea, not cards.
    return {"title":"Prism Appeal","slug":"prism-appeal",
      "idea":"A courthouse refracts every spoken testimony into living color, forcing witnesses to watch their answers physically rebuild the room around them.",
      "vibe":{"title":"The Kindly Cross-Examination","line":"Every answer changes the room that asked it.","art_direction":"A luminous impossible courthouse."},
      "locations":[{"title":"The Refracted Court",
        "known_for":"Its prismatic chambers turn spoken testimony into color that stains the walls until a case is settled.",
        "local_rule":"No witness may repeat a hue that their own testimony has already changed.",
        "best_scene":"A disputed childhood memory turns the courtroom black while every exit quietly moves to a new wall.",
        "art_direction":"prismatic courtroom"}],
      "characters":[{"name":"Mara Venn",
        "role_drive":"She is trying to protect an engineered witness whose testimony the court has already begun to erase.",
        "carries":"A cracked spectrum lens rides at her hip, still holding a sliver of her own deleted testimony.",
        "complication":"The lens holds the testimony she was made to withdraw, and using it in open court would expose her.",
        "look":"mantis-shrimp advocate in a midnight suit"}],
      "rewards":[{"name":"Verdict Lens","reward_type":"ITEM","rarity":"RARE",
        "grants":"It reveals the single entry that a record is missing.",
        "best_used_when":"A story arrives suspiciously clean and complete, with no loose ends.",
        "catch":"The omission it surfaces always turns out to be your own.",
        "look":"a palm-sized brass loupe with a cracked prismatic lens, verdigris in the knurling"},
        {"name":"Chromatic Recall","reward_type":"SKILL","rarity":"UNCOMMON",
        "grants":"It reconstructs a lost memory from the colors the room kept.",
        "best_used_when":"The official records have already been altered beyond what anyone will admit.",
        "catch":"The original emotion returns with the memory, at full strength.",
        "look":"ribbons of banded colour unspooling out of empty air above a bare table"}],
      "scenarios":[{"title":"The Color of Perjury","setup":"In The Kindly Cross-Examination at The Refracted Court, Mara Venn defends a witness whose testimony turned the chamber black."}],
      "seed_facets":_sample_seeds()}


def _sample_seeds() -> dict[str, Any]:
    """The sample's seed plan, with today's two inventions actually filled in.

    The sample is the worked example of the contract, so it has to satisfy it:
    a plan that names two gaps and a proposal that leaves `invented` empty is
    exactly what validate_inventions rejects. Written generically from whatever
    plan_inventions picked rather than hardcoded, so this keeps working when the
    rotation lands on different taxonomies.
    """
    catalog = {k: _fallback(k) for k in FALLBACK_FACETS}
    seeds = facet_seed_plan("2026-07-31", catalog)

    invented = []
    for index, entry in enumerate(seeds.get("invent") or []):
        taxonomy = str(entry.get("taxonomy") or "GENRE")
        title = ("Sealed Docket", "Held In Contempt")[index % 2]
        facet = {
            "title": title, "slug": slugify(title), "taxonomy": taxonomy,
            "description": (
                "A matter the record acknowledges but will not open. "
                "Everyone may cite it; nobody may read it."
                if index % 2 == 0 else
                "A standing refusal that costs its holder something every day it lasts. "
                "It buys time and spends standing."
            ),
            "art_prompt": (
                "A wax-sealed court folder, edges furred with handling, "
                "the seal unbroken and slightly melted."
                if index % 2 == 0 else
                "An empty witness chair turned to face the wall, brass nameplate unscrewed."
            ),
        }
        invented.append(facet)
        for target in entry.get("assign_to") or []:
            seeds["elements"].setdefault(target, []).append(copy.deepcopy(facet))

    seeds["invented"] = invented
    return seeds


SAMPLE_PROPOSAL=_sample()

if __name__ == "__main__": raise SystemExit(main())