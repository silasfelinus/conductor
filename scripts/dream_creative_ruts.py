#!/usr/bin/env python3
"""Shared motif-rut vocabulary for Daily Dream creative validation and catalog audit.

`author_dream_proposal.story_diversity_complaints` has guarded exactly one rut since
August 2026: bureaucracy/record-keeping. The freshness remaster (conductor issue #3184)
named the rest of the historical grooves out loud — archives, cozy markets and
workshops, towers and lighthouses, repeated occupational archetypes, and whimsical
noun-compound surname factories — so both the live contract and the catalog audit read
them from one place instead of two drifting copies.

Two deliberate design choices keep this from over-blocking:

* A family is only a complaint when the day's Facets did not actually ask for it. A
  Bureaucratic Fantasy Facet is allowed to produce a permit office on purpose.
* Outside bureaucracy (which stays a whole-text guard, unchanged), families only
  complain when the motif reaches a *name* — a vibe, location, scenario, reward, or
  character name. A lighthouse mentioned in passing is scenery; "The Lighthouse of
  Small Regrets" is the rut.
"""
from __future__ import annotations

import re
from typing import Iterable

# Nouns that keep reappearing as ornamental fantasy surnames. The naming directions in
# author_dream_proposal already ask for plausible family names; this is the detector for
# when that instruction quietly stops being followed.
WHIMSY_SURNAME_MARKERS = {
    "amber", "ash", "bell", "birch", "bramble", "briar", "brine", "cinder", "clove",
    "cobble", "copper", "crow", "dusk", "ember", "fable", "fathom", "feather", "fen",
    "fern", "flint", "frost", "gale", "glass", "gloam", "harrow", "hazel", "heather",
    "hollow", "kettle", "lantern", "lark", "marrow", "mist", "moss", "nettle", "quill",
    "raven", "reed", "rook", "rush", "salt", "sable", "silver", "sorrel", "sparrow",
    "stone", "storm", "thistle", "thorn", "tide", "vale", "vellum", "wick", "willow",
    "wren",
}

# Rank/title prefixes that turn a cast into the same civil service twice over.
HONORIFIC_MARKERS = {
    "undersecretary", "secretary", "deputy", "assistant", "superintendent",
    "inspector", "commissioner", "registrar", "notary", "warden", "steward",
    "chancellor", "administrator", "adjutant", "clerk",
}

RUT_FAMILIES: dict[str, dict[str, object]] = {
    "bureaucracy": {
        "label": "bureaucracy / record-keeping",
        "scope": "text",
        "markers": {
            "ledger", "ledgers", "filing", "file", "files", "permit", "permits",
            "registry", "register", "quota", "quotas", "charter", "requisition",
            "requisitions", "clerk", "clerks", "bureau", "paperwork", "accounting",
            "bookkeeping", "tally", "office", "docket", "dossier", "affidavit",
            "bylaw", "ordinance", "invoice", "receipt", "census", "stamp", "stamps",
            "notary", "ministry", "department", "commission", "warrant",
        },
        "facet_markers": {
            "bureaucracy", "bureaucratic", "administration", "administrative",
            "legal", "courtroom", "diplomat", "diplomacy",
        },
    },
    "archive": {
        "label": "archive / library / recordkeeping vault",
        "scope": "name",
        "markers": {
            "archive", "archives", "archivist", "library", "libraries", "librarian",
            "scriptorium", "stacks", "annals", "chronicle", "chronicles", "catalogue",
            "index", "repository", "codex",
        },
        "facet_markers": {
            "archive", "archives", "archivist", "archive-horror", "library",
            "librarian", "historian", "scholar", "records",
        },
    },
    "cozy-market": {
        "label": "cozy market / workshop / shopfront",
        "scope": "name",
        "markers": {
            "market", "markets", "marketplace", "bazaar", "stall", "stalls",
            "emporium", "boutique", "teahouse", "tearoom", "bakery", "cafe",
            "tavern", "inn", "apothecary", "workshop", "atelier", "cottage",
            "parlour", "parlor", "shoppe",
        },
        "facet_markers": {
            "cozy", "cozy-mystery", "slice-of-life", "culinary", "merchant",
            "baker", "shopkeeper", "chef", "innkeeper", "trader", "market",
        },
    },
    "tower-beacon": {
        "label": "tower / lighthouse / beacon spire",
        "scope": "name",
        "markers": {
            "tower", "towers", "lighthouse", "lighthouses", "spire", "spires",
            "belfry", "campanile", "minaret", "watchtower", "beacon", "beacons",
            "obelisk",
        },
        # "spire" earns its place here: Spire Crystal is a MATERIAL Facet, so a day that
        # draws it is *asking* for spires and should not then be scored for having them.
        "facet_markers": {"lighthouse", "tower", "beacon", "watchtower", "monk", "spire"},
    },
    "occupational-archetype": {
        "label": "repeated occupational archetype",
        "scope": "name",
        "markers": {
            "concierge", "courier", "cartographer", "keeper", "keepers", "warden",
            "steward", "curator", "inspector", "auditor", "apprentice", "custodian",
            "ferryman", "lamplighter", "scribe", "herald", "tinker", "tinkerer",
            "mender", "undertaker", "collector",
        },
        "facet_markers": set(),  # occupation Facets are matched by slug, see facets_request
    },
}

# A few markers are ordinary English outside the rut ("choir stalls" is furniture,
# "a market of ideas" is a metaphor). They only count when the surrounding text also
# carries the motif they belong to.
CONTEXT_REQUIRED: dict[str, set[str]] = {
    "stall": {"market", "markets", "vendor", "vendors", "merchant", "trade", "trader",
              "wares", "shop", "haggle", "bazaar"},
    "stalls": {"market", "markets", "vendor", "vendors", "merchant", "trade", "trader",
               "wares", "shop", "haggle", "bazaar"},
    "index": {"archive", "archives", "catalogue", "library", "record", "records"},
    "commission": {"bureau", "office", "permit", "charter", "clerk", "ministry"},
    "seal": {"stamp", "charter", "permit", "document", "wax"},
}

_WORD = re.compile(r"[a-z]+")


def _words(text: object) -> set[str]:
    return set(_WORD.findall(str(text or "").casefold()))


def _gated(hits: set[str], words: set[str]) -> set[str]:
    """Drop context-required markers whose supporting vocabulary is absent."""
    return {
        hit
        for hit in hits
        if hit not in CONTEXT_REQUIRED or (words & CONTEXT_REQUIRED[hit])
    }


def family_hits(text: object, family: str) -> set[str]:
    """Marker words from one family present in `text`."""
    words = _words(text)
    markers = RUT_FAMILIES[family]["markers"]
    return _gated(words & markers, words)  # type: ignore[operator]


def motif_hits(text: object) -> dict[str, set[str]]:
    """Every family with at least one marker present in `text`."""
    found: dict[str, set[str]] = {}
    words = _words(text)
    for family, spec in RUT_FAMILIES.items():
        hits = _gated(words & spec["markers"], words)  # type: ignore[operator]
        if hits:
            found[family] = hits
    return found


def facets_request(family: str, facet_text: object) -> bool:
    """True when the day's Facets legitimately asked for this motif."""
    spec = RUT_FAMILIES[family]
    facet_words = _words(facet_text)
    if facet_words & spec["facet_markers"]:  # type: ignore[operator]
        return True
    if family == "occupational-archetype":
        # An OCCUPATION Facet naming the archetype is the Facet doing its job.
        return bool(facet_words & spec["markers"])  # type: ignore[operator]
    return False


def surname_factory_complaint(name: str) -> str | None:
    """Flag ornamental noun-compound surnames (`Wren Thistlewick`, `Mara Emberfall`)."""
    parts = [part for part in re.split(r"[^A-Za-z'-]+", str(name or "")) if part]
    if len(parts) < 2:
        return None
    surname = parts[-1].casefold()
    if surname in WHIMSY_SURNAME_MARKERS:
        return f"surname {parts[-1]!r} is a bare nature/object noun"
    for marker in sorted(WHIMSY_SURNAME_MARKERS):
        if len(marker) < 4 or len(surname) <= len(marker):
            continue
        if surname.startswith(marker) or surname.endswith(marker):
            return (
                f"surname {parts[-1]!r} is built from the recurring noun stem "
                f"{marker!r}"
            )
    return None


def honorific_hits(names: Iterable[str]) -> set[str]:
    """Civil-service rank prefixes used as character titles."""
    found: set[str] = set()
    for name in names:
        found |= _words(name) & HONORIFIC_MARKERS
    return found


def name_rut_complaints(names: Iterable[str], facet_text: object) -> list[str]:
    """Name-scoped rut complaints for the live creative contract.

    Bureaucracy keeps its existing whole-text guard in author_dream_proposal; this
    covers the families the remaster added, and only when a motif has reached a name.
    """
    joined = " ".join(str(name or "") for name in names)
    complaints: list[str] = []
    for family, spec in RUT_FAMILIES.items():
        if spec["scope"] != "name":
            continue
        joined_words = _words(joined)
        hits = _gated(joined_words & spec["markers"], joined_words)  # type: ignore[operator]
        if not hits or facets_request(family, facet_text):
            continue
        examples = ", ".join(sorted(hits)[:4])
        complaints.append(
            f"named assets fall back into the overused {spec['label']} motif "
            f"({examples}) even though today's Facets do not request it; rename and "
            "rebuild the premise around what the Facets actually asked for"
        )
    return complaints
