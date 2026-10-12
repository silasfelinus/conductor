#!/usr/bin/env python3
"""Produce a separate, catalog-backed Facet plan for the eight Zuzu extras.

Never copy the random Daily Dream's umbrella/creature/genre facets onto the
game projects. The original six use their established entropy-seeded plan.
"""
from __future__ import annotations

import copy
import hashlib
import random
from typing import Any

try:
    from daily_dream_v3_contract import FACET_SLOTS, PROJECT_TARGETS
except ModuleNotFoundError:  # scripts.* package imports from pytest
    from scripts.daily_dream_v3_contract import FACET_SLOTS, PROJECT_TARGETS

CUTOVER_DAY = "2026-10-13"
ZU_SLOTS = FACET_SLOTS[6:]
ZUZU_TAXONOMIES = ("THEME", "SETTING", "ROLE", "MATERIAL")


def is_v3_day(day: str) -> bool:
    return day >= CUTOVER_DAY


def _id(row: dict[str, Any]) -> str:
    return str(row.get("slug") or row.get("id") or row.get("title") or "").strip().casefold()


def extend_brief(brief: dict[str, Any], catalog: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    """Return a 14-slot authoring brief; no invented/unregistered Facet identifiers.

    Use separate daily salt and catalog draws. The Zuzu constraints are coherent
    across projects but deliberately NOT derived from the random world's Facets.
    """
    out = copy.deepcopy(brief)
    seed = out["seed_facets"]
    elements = seed["elements"]
    if not all(isinstance(elements.get(s), list) and elements[s] for s in FACET_SLOTS[:6]):
        raise ValueError("original six Facet slots are incomplete")
    spent = {_id(f) for slot in FACET_SLOTS[:6]
             for f in elements[slot] if isinstance(f, dict)}
    day = str(out["proposal_date"])
    for index, slot in enumerate(ZU_SLOTS):
        owner = PROJECT_TARGETS[index % 2] if "reward" not in slot else (
            "zuzu-gamebook" if slot == "zuzu_reward_item" else "emperor-of-dust"
        )
        digest = hashlib.sha256(f"zuzu-extra-facets-v3:{day}:{owner}:{slot}".encode()).digest()
        rng = random.Random(int.from_bytes(digest[:8], "big"))
        pool: list[dict[str, Any]] = []
        for taxonomy in ZUZU_TAXONOMIES:
            rows = catalog.get(taxonomy) or []
            pool += [row for row in rows
                     if isinstance(row, dict) and row.get("title")
                     and row.get("taxonomy") and (row.get("slug") or row.get("id"))
                     and _id(row) not in spent]
        # A seeded slot requires at least one genuine catalog-backed Facet.
        # Do not inject random daily-world Facets or bogus slugs as a fallback.
        if not pool:
            raise ValueError(f"no independent registered Zuzu Facets for {slot}")
        unique = {(_id(row), str(row.get("taxonomy"))): row for row in pool}
        selected = rng.sample(list(unique.values()), k=min(2, len(unique)))
        elements[slot] = copy.deepcopy(selected)
    seed["version"] = 3
    out["bundle_version"] = 3
    out["required_counts"] = {
        "vibe": 1, "locations": 1, "characters": 1,
        "reward_item": 1, "reward_skill": 1, "scenarios": 1,
        "zuzu_locations": 2, "zuzu_characters": 2,
        "zuzu_rewards": 2, "zuzu_scenarios": 2,
    }
    out["instructions"].extend([
        "IN ADDITION to the original complete six linked Daily Dream creations, write "
        "EIGHT unlinked Zuzu-world creations in zuzu_assets: two locations, two "
        "characters, two rewards (one ITEM and one SKILL), two moral-choice scenarios.",
        "The random Daily Dream original Facets, visual theme, characters, and world "
        "MUST NOT appear in Zuzu extras. Zuzu Facet slots are independently drawn "
        "from real Kind Robots catalog Facets, not the day's random Dream umbrella.",
        "Each kind has one zuzu-gamebook and one emperor-of-dust asset, labeled by "
        "project_target. Each row has checkpoint_family arthemy or illustrious.",
        "Gamebook: Zuzu Koala Assassin is an Edo-style samurai traveler in an "
        "anthropomorphic Weird West. Branching choices, skills, flags and story "
        "consequences. Respect established worldbuilding; do not invent random humans.",
        "Emperor of Dust: use the fixed Ash, Brass & the Last Hundred Days art/world "
        "pitch. Pre-Zuzu kingdom, an abstract numerical Horde, named follower leaders, "
        "injury more common than death, scarce supplies and faction bargains.",
        "Each Zuzu scenario needs at least two defensible moral options with label, "
        "tradeoff, immediate_consequence and later_consequence, not a good/evil coin flip.",
        "Art directions for Zuzu should describe active Illustrious/Arthemy checkpoint "
        "subjects; do not repurpose the unique Daily Dream's Krea art direction.",
    ])
    return out


def assign_zuzu_provenance(proposal: dict[str, Any]) -> dict[str, Any]:
    """Canonical slot order and checkpoint family are authoring policy, not model whim."""
    extras = proposal.get("zuzu_assets")
    if not isinstance(extras, dict):
        return proposal
    for kind in ("locations", "characters", "rewards", "scenarios"):
        rows = extras.get(kind)
        if not isinstance(rows, list) or len(rows) != 2:
            continue
        for index, row in enumerate(rows):
            if not isinstance(row, dict):
                continue
            owner = ("zuzu-gamebook" if index == 0 else "emperor-of-dust")
            # Reward ITEM belongs to Gamebook and SKILL to Emperor, regardless
            # of the model's ordering; the validator checks uniqueness.
            if kind == "rewards":
                owner = "zuzu-gamebook" if str(row.get("reward_type") or "").upper() == "ITEM" else "emperor-of-dust"
            row["project_target"] = owner
            row["checkpoint_family"] = ("arthemy" if owner == "zuzu-gamebook" else "illustrious")
    return proposal
