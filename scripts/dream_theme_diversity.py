#!/usr/bin/env python3
"""Semantic-ish theme guards for Daily Dream world variety.

The Daily Dream author already compares recent vocabulary, but vocabulary overlap is a
poor detector for world-scale repetition. A reef, a floating flotilla, and a drowned
chancery can share almost no distinctive words while still being the same broad habitat
choice three days running.

Keep this module deliberately small and inspectable. It is not a universal ontology. It
captures theme families that have produced a demonstrated recurring rut and gives both
the Facet planner and the author validator the same definition of that rut.
"""
from __future__ import annotations

import re
from typing import Any, Iterable

AQUATIC_WORLD_FAMILY = "aquatic-world"
AQUATIC_WORLD_MIN_HITS = 3

# Strong world/setting signals. A single ordinary water reference is harmless; the live
# guard requires several distinct markers before calling the whole premise aquatic.
AQUATIC_WORLD_MARKERS = {
    "anchor", "anchors", "aquatic", "coral", "corals", "coastal", "dock", "docks",
    "drowned", "drowning", "estuary", "flood", "flooded", "floodline", "flotilla",
    "harbor", "harbour", "kelp", "lagoon", "marine", "marina", "maritime", "nautical",
    "ocean", "oceanic", "oceans", "reef", "reefs", "sea", "seas", "seawater", "shoal",
    "shoals", "shoreline", "submerged", "surf", "tidal", "tide", "tideline", "tides",
    "underwater", "water", "waterline",
}

# These Facets really do ask for an aquatic world. Creature Facets are intentionally not
# here: an otter, manatee, shark, or shrimp constrains anatomy and life support, not the
# geography and civic architecture of everybody else in the setting.
AQUATIC_EXPLICIT_FACET_MARKERS = {
    "aquatic", "coastal", "marine", "maritime", "nautical", "ocean", "oceanic",
    "seafaring", "subaquatic", "tidal", "tidepool", "undersea", "underwater",
}
AQUATIC_EXPLICIT_FACET_PHRASES = {
    "the big blue", "tidal flat", "open ocean", "ocean world", "underwater city",
}

# Seed cooldowns are stronger than author exemptions. After an aquatic world ships, we
# prefer a non-aquatic creature too, because four consecutive draws of Big Blue -> manatee
# -> otter -> hammerhead proved that independent random dates can still make a terrible
# curated sequence.
AQUATIC_CREATURE_MARKERS = {
    "axolotl", "crab", "dolphin", "eel", "fish", "jellyfish", "lobster", "manatee",
    "manta", "octopus", "otter", "penguin", "puffin", "ray", "seal", "seahorse", "shark",
    "shrimp", "squid", "turtle", "walrus", "whale",
}
AQUATIC_SEED_PHRASES = AQUATIC_EXPLICIT_FACET_PHRASES | {
    "cable ferry", "mantis shrimp", "hammerhead shark", "sea otter", "tidal flat",
}

_WORD = re.compile(r"[a-z]+")


def _words(text: object) -> set[str]:
    return set(_WORD.findall(str(text or "").casefold()))


def aquatic_world_hits(text: object) -> set[str]:
    """Return distinct strong aquatic setting markers present in creative text."""
    return _words(text) & AQUATIC_WORLD_MARKERS


def is_aquatic_world(text: object) -> bool:
    """True only when several distinct setting signals make water world-scale."""
    return len(aquatic_world_hits(text)) >= AQUATIC_WORLD_MIN_HITS


def _facet_rows(seed_facets: object) -> Iterable[dict[str, Any]]:
    """Yield actual assigned Facets, excluding metadata such as cooldown labels."""
    if not isinstance(seed_facets, dict):
        return []
    elements = seed_facets.get("elements")
    if not isinstance(elements, dict):
        return []
    seen: set[tuple[str, str]] = set()
    rows: list[dict[str, Any]] = []
    for values in elements.values():
        if not isinstance(values, list):
            continue
        for facet in values:
            if not isinstance(facet, dict):
                continue
            key = (str(facet.get("taxonomy") or ""), str(facet.get("slug") or facet.get("title") or ""))
            if key in seen:
                continue
            seen.add(key)
            rows.append(facet)
    return rows


def _facet_text(facet: dict[str, Any]) -> str:
    return " ".join(
        str(facet.get(key) or "")
        for key in ("title", "slug", "canonicalValue", "taxonomy")
    ).casefold().replace("-", " ")


def facet_explicitly_requests_aquatic_world(facet: dict[str, Any]) -> bool:
    """Whether one Facet is a genuine world/habitat request rather than a creature."""
    text = _facet_text(facet)
    words = _words(text)
    return bool(words & AQUATIC_EXPLICIT_FACET_MARKERS) or any(
        phrase in text for phrase in AQUATIC_EXPLICIT_FACET_PHRASES
    )


def facets_explicitly_request_aquatic_world(seed_facets: object) -> bool:
    """Whether the assigned seed Facets legitimately ask the author for an aquatic world."""
    return any(facet_explicitly_requests_aquatic_world(facet) for facet in _facet_rows(seed_facets))


def facet_is_aquatic_seed(facet: dict[str, Any]) -> bool:
    """Whether this Facet should be avoided during a recent-aquatic cooldown."""
    text = _facet_text(facet)
    if facet_explicitly_requests_aquatic_world(facet):
        return True
    if any(phrase in text for phrase in AQUATIC_SEED_PHRASES):
        return True
    taxonomy = str(facet.get("taxonomy") or "").upper()
    return taxonomy in {"ANIMAL", "SPECIES"} and bool(_words(text) & AQUATIC_CREATURE_MARKERS)


def apply_seed_cooldowns(
    pool: list[dict[str, Any]],
    cooldowns: Iterable[str],
    *,
    minimum: int = 1,
) -> list[dict[str, Any]]:
    """Prefer non-rut Facets while preserving enough candidates to complete a draw."""
    active = set(cooldowns)
    if AQUATIC_WORLD_FAMILY not in active:
        return pool
    filtered = [facet for facet in pool if not facet_is_aquatic_seed(facet)]
    return filtered if len(filtered) >= minimum else pool


def proposal_creative_text(proposal: object) -> str:
    """Flatten authored content while excluding seed metadata that would self-trigger guards."""
    if not isinstance(proposal, dict):
        return ""
    values: list[str] = []

    def collect(value: object) -> None:
        if isinstance(value, str):
            values.append(value)
        elif isinstance(value, list):
            for item in value:
                collect(item)
        elif isinstance(value, dict):
            for key, item in value.items():
                if key in {"seed_facets", "built_data"}:
                    continue
                collect(item)

    for key, value in proposal.items():
        if key in {"seed_facets", "built_data"}:
            continue
        collect(value)
    return " ".join(values)


def proposal_is_aquatic_world(proposal: object) -> bool:
    return is_aquatic_world(proposal_creative_text(proposal))
