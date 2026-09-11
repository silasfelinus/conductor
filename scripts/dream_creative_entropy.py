#!/usr/bin/env python3
"""History-aware creative entropy helpers for the Daily Dream generator.

The Daily Dream is supposed to be an idea engine. Independent random draws and lexical
anti-echo checks are not enough for that job: a generator can use different nouns while
repeating the same obligation economy, grief machinery, countdown structure, title
shape, or visual grammar. This module keeps the higher-level rules small, inspectable,
and evidence-driven.

It deliberately does not try to be a universal story ontology. Families are added only
when the built catalog demonstrates a recurring groove.
"""
from __future__ import annotations

import hashlib
import re
from typing import Any, Iterable

ENTROPY_VERSION = 2
RECENT_FACET_LOOKBACK = 5
RECENT_STRUCTURE_LOOKBACK = 5
RECENT_INVENTION_LOOKBACK = 8

_WORD = re.compile(r"[a-z]+")
_DISTINCTIVE = re.compile(r"[a-z]{5,}")
_THE_X_Y_TITLE = re.compile(r"^the\s+[^\s]+\s+[^\s]+$", re.IGNORECASE)

STOPWORDS = {
    "about", "after", "again", "against", "along", "another", "around", "because",
    "before", "being", "between", "could", "every", "first", "from", "their", "there",
    "these", "thing", "through", "under", "until", "where", "while", "whose", "world",
    "would", "someone", "something", "today", "facet", "facets", "character", "location",
    "reward", "scenario", "dream", "story", "person", "people",
}

SEMANTIC_FAMILIES: dict[str, dict[str, object]] = {
    "debt-obligation": {
        "label": "debt / obligation / tally economy",
        "markers": {
            "debt", "debts", "debtor", "creditor", "owe", "owes", "owed", "owing", "repay", "repays",
            "repayment", "obligation", "obligations", "tally", "tallies", "balance",
            "balanced", "due", "dues", "collect", "collects", "collection", "claim",
            "claims", "bargain", "bargains", "accounting", "accountant",
        },
        "anchors": {
            "debt", "debts", "debtor", "creditor", "owe", "owes", "owed", "owing",
            "repay", "repays", "repayment", "obligation", "obligations", "tally",
            "tallies", "due", "dues", "accounting", "accountant",
        },
        "facet_markers": {
            "debt", "debtor", "creditor", "obligation", "accounting", "accountant",
            "tally", "bargain", "contract",
        },
    },
    "correspondence-contract": {
        "label": "letters / missives / contracts as story machinery",
        # One recent world is enough to cool this family. It is a very specific carrier
        # of plot information, and the catalog had learned to reach for it far more often
        # than its narrative usefulness justified.
        "minimum_sources": 1,
        "markers": {
            "letter", "letters", "missive", "missives", "correspondence", "contract",
            "contracts", "treaty", "treaties", "covenant", "covenants", "oath", "oaths",
            "vow", "vows", "notary", "notaries", "notarized", "signature", "signatures",
            "signer", "signers", "writ", "writs", "charter", "charters",
        },
        "anchors": {
            "letter", "letters", "missive", "missives", "correspondence", "contract",
            "contracts", "treaty", "treaties", "covenant", "covenants", "oath", "oaths",
            "notary", "notaries", "notarized", "signature", "signatures", "writ", "writs",
        },
        "facet_markers": {
            "letter", "missive", "correspondence", "contract", "treaty", "covenant", "oath",
            "vow", "notary", "signature", "writ", "charter",
        },
    },
    "grief-memory": {
        "label": "grief / regret / memory as world machinery",
        "markers": {
            "grief", "griefs", "grieve", "grieves", "grieving", "mourning", "mourn",
            "mourner", "mourners", "regret", "regrets", "sorrow", "sorrows", "loss",
            "losses", "memory", "memories", "remember", "remembers", "remembered",
            "forget", "forgotten", "bereavement", "memorial",
        },
        "anchors": {
            "grief", "griefs", "grieve", "grieves", "grieving", "mourning", "mourn",
            "mourner", "mourners", "regret", "regrets", "sorrow", "sorrows",
            "bereavement",
        },
        "facet_markers": {
            "grief", "mourning", "mourner", "regret", "sorrow", "memory", "memorial",
            "bereavement",
        },
    },
}

DEADLINE_PATTERNS = (
    re.compile(r"\b(?:one|single)\s+(?:[a-z-]+\s+){0,2}(?:night|day|hour|tide|shift|season|week)\b"),
    re.compile(r"\b\d+\s+(?:minutes?|hours?|days?|nights?|weeks?)\b"),
    re.compile(r"\bby\s+(?:dawn|dusk|sunrise|sunset|midnight|morning|nightfall)\b"),
    re.compile(r"\bbefore\b.{0,90}\b(?:arrives?|reaches?|closes?|opens?|runs? out|wakes?|falls?|returns?|catches?|burns?|breaks?|dies?|ends?|comes?|collects?|finds?|notices?|detects?|works? out)\b"),
    re.compile(r"\b(?:race|races|racing|countdown|deadline)\b"),
)
DEADLINE_FACET_MARKERS = {
    "race", "racing", "competition", "competitive", "tournament", "countdown", "timed",
    "speedrun", "survival", "chase",
}

TITLE_DIRECTIONS = (
    "Do not lead with 'The'. Prefer a setting-native proper noun, coined place, or in-world term that could only belong to this premise.",
    "Use an active construction: a verb, action, or event rather than an adjective-plus-noun object label.",
    "Use a short clause or sentence that someone in the world could plausibly say; let the title carry voice rather than taxonomy.",
    "Use a relationship or possessive construction centered on a person, creature, promise, feud, family, or bond.",
    "Use a number, duration, measure, date, or count that matters physically in the premise; do not turn it into a deadline by default.",
    "Use a bare proper name or place-name without a decorative fantasy adjective. Let context make it strange.",
    "Use one concrete sensory image of three or more words. Avoid the recurring 'The [adjective/noun] [noun]' silhouette.",
    "Use one strong single word or pronounceable compound. Avoid generic fantasy noun-mashing and avoid recycling recent title roots.",
)

STRUCTURAL_DIRECTIONS = (
    "No countdown today. Let curiosity, choice, consequence, or desire move the story without 'one night', 'one tide', 'before X', a chase clock, or a looming deadline.",
    "Make the Character a lens rather than the sole operator. Let a community, creature, ecosystem, crowd, or place have agency that cannot be reduced to one specialist doing a job.",
    "Center creation, birth, invention, courtship, play, celebration, or discovery rather than repair, rescue, maintenance, certification, or keeping a system running.",
    "Begin after the event another story would call the climax. Make aftermath, interpretation, adaptation, or an unexpected new normal the dramatic engine.",
    "Keep the stakes intimate and specific. One room, relationship, household, body, or routine can matter without becoming an institution-wide emergency.",
    "Let ecology, anatomy, weather, appetite, migration, terrain, or nonhuman behavior create the story. Avoid offices, guilds, agencies, orders, and professional procedure unless a Facet explicitly demands them.",
    "Build around play: a game, festival, performance, prank, ritual, hobby, sport, or communal pastime can become strange without needing catastrophe or a villain.",
    "Use ensemble agency. The required single Character is our viewpoint card, not proof that one lone expert must personally solve the world's problem.",
    "Center an irreversible transformation without pursuit. Let characters negotiate becoming, metamorphosis, aging, scale change, merging, splitting, or altered senses rather than fleeing hunters.",
    "Allow unresolved wonder. The premise may change what people believe or choose without supplying an antagonist, a hidden conspiracy, or a problem that must be solved.",
)

VISUAL_DIRECTIONS = (
    "Favor hard daylight, crisp shadows, and ordinary non-glowing materials. Do not use faint bioluminescence as the automatic signal that the world is magical.",
    "Avoid the recurring brass instrument / patched coat / dim glow toolkit unless a Facet truly asks for it. Find the world's signature shapes in different materials and objects.",
    "Go monumental and spacious: one dominant landform, machine, organism, or architectural volume with people small in the frame and very little decorative clutter.",
    "Go intimate and materially ordinary: domestic clutter, food, fabric, plastic, wood, dirt, fingerprints, wear, and close physical scale rather than mystical infrastructure.",
    "Let biology dominate the image language: membranes, fur, roots, shells, wet surfaces, growth, scars, molts, pollen, teeth, feathers, or other embodied textures.",
    "Let clean synthetic design dominate: ceramic, polymer, glass, printed composites, bright utility surfaces, modular geometry, or mass-produced objects instead of antique fantasy hardware.",
    "Make weather or atmosphere the main visual event: wind, dust, heat shimmer, snow load, rain sheets, fog banks, ash, pollen, or changing sky should reshape the scene physically.",
    "Use celebratory abundance: bold daylight, crowds or swarms with purpose, oversized props, food, banners, motion, and saturated material variety rather than another lonely figure in a dim workspace.",
)


def _words(text: object) -> list[str]:
    return _WORD.findall(str(text or "").casefold())


def facet_key(facet: object) -> str:
    if not isinstance(facet, dict):
        return ""
    value = facet.get("slug") or facet.get("title") or facet.get("canonicalValue") or ""
    return re.sub(r"[^a-z0-9]+", "-", str(value).casefold()).strip("-")


def apply_recent_facet_cooldown(
    pool: list[dict[str, Any]],
    spent_keys: Iterable[str],
    *,
    minimum: int = 1,
) -> list[dict[str, Any]]:
    """Prefer Facets absent from the recent sequence, with a safe thin-pool fallback."""
    spent = {str(key).casefold() for key in spent_keys if key}
    if not spent:
        return pool
    filtered = [facet for facet in pool if facet_key(facet) not in spent]
    return filtered if len(filtered) >= minimum else pool


def _facet_family_words(facet: object) -> set[str]:
    if not isinstance(facet, dict):
        return set()
    return set(
        _words(
            " ".join(
                str(facet.get(key) or "")
                for key in ("title", "slug", "canonicalValue", "description")
            )
        )
    )


def facet_requests_family(facet: object, family: str) -> bool:
    """Whether one seed Facet itself points into a saturated semantic story family."""
    markers = SEMANTIC_FAMILIES[family]["facet_markers"]
    return bool(_facet_family_words(facet) & markers)  # type: ignore[arg-type]


def apply_semantic_family_cooldown(
    pool: list[dict[str, Any]],
    saturated: Iterable[str],
    *,
    minimum: int = 1,
) -> list[dict[str, Any]]:
    """Prefer seed Facets that do not re-request a recently saturated story engine."""
    active = {family for family in saturated if family in SEMANTIC_FAMILIES}
    if not active:
        return pool
    filtered = [
        facet
        for facet in pool
        if not any(facet_requests_family(facet, family) for family in active)
    ]
    return filtered if len(filtered) >= minimum else pool


def story_core_text(proposal: object) -> str:
    """Flatten story-bearing fields while excluding Rewards, art prose, and seed metadata.

    Reward catches are intentionally excluded: the schema requires every Reward to have a cost,
    and counting those costs would make obligation look more central than the actual story is.
    """
    if not isinstance(proposal, dict):
        return ""
    values: list[str] = []

    def add(value: object) -> None:
        if isinstance(value, str) and value.strip():
            values.append(value)

    add(proposal.get("title"))
    add(proposal.get("idea"))
    vibe = proposal.get("vibe")
    if isinstance(vibe, dict):
        add(vibe.get("title")); add(vibe.get("line"))
    for location in proposal.get("locations") or []:
        if isinstance(location, dict):
            for key in ("title", "known_for", "local_rule", "best_scene"):
                add(location.get(key))
    for character in proposal.get("characters") or []:
        if isinstance(character, dict):
            for key in ("name", "role_drive", "complication"):
                add(character.get(key))
    for scenario in proposal.get("scenarios") or []:
        if isinstance(scenario, dict):
            add(scenario.get("title")); add(scenario.get("setup"))
    return " ".join(values)


def family_hit_count(text: object, family: str) -> int:
    markers = SEMANTIC_FAMILIES[family]["markers"]
    return sum(1 for word in _words(text) if word in markers)  # type: ignore[operator]


def families_in_text(text: object, *, minimum_hits: int = 2) -> set[str]:
    words = _words(text)
    found: set[str] = set()
    for family, spec in SEMANTIC_FAMILIES.items():
        anchors = spec.get("anchors") or spec["markers"]
        if not any(word in anchors for word in words):
            continue
        if family_hit_count(text, family) >= minimum_hits:
            found.add(family)
    return found


def saturated_families(
    texts: Iterable[str],
    *,
    minimum_sources: int = 2,
    minimum_hits: int = 2,
) -> set[str]:
    counts = {family: 0 for family in SEMANTIC_FAMILIES}
    for text in texts:
        for family in families_in_text(text, minimum_hits=minimum_hits):
            counts[family] += 1
    return {
        family
        for family, count in counts.items()
        if count >= int(SEMANTIC_FAMILIES[family].get("minimum_sources", minimum_sources))
    }


def _drawn_facet_text(seed_facets: object) -> str:
    """Only Facets selected from the catalog, never today's newly invented Facets."""
    if not isinstance(seed_facets, dict):
        return ""
    rows: list[dict[str, Any]] = []
    umbrella = seed_facets.get("umbrella")
    shared = seed_facets.get("shared")
    extras = seed_facets.get("extra_genres")
    if isinstance(umbrella, dict):
        rows.extend(row for row in (umbrella.get("genres") or []) if isinstance(row, dict))
        for key in ("creature", "wildcard"):
            if isinstance(umbrella.get(key), dict): rows.append(umbrella[key])
    if isinstance(shared, dict):
        for row in shared.values():
            if isinstance(row, dict): rows.append(row)
    if isinstance(extras, dict):
        rows.extend(row for row in extras.values() if isinstance(row, dict))
    return " ".join(
        " ".join(str(row.get(key) or "") for key in ("title", "slug", "canonicalValue"))
        for row in rows
    ).casefold()


def facets_request_family(seed_facets: object, family: str) -> bool:
    words = set(_words(_drawn_facet_text(seed_facets)))
    markers = SEMANTIC_FAMILIES[family]["facet_markers"]
    return bool(words & markers)  # type: ignore[arg-type]


def story_family_complaints(
    proposal: object,
    recent_story_texts: list[str],
    seed_facets: object,
) -> list[str]:
    """Reject a demonstrated semantic groove only after it is already saturated."""
    recent = recent_story_texts[-RECENT_STRUCTURE_LOOKBACK:]
    saturated = saturated_families(recent)
    candidate = story_core_text(proposal)
    candidate_families = families_in_text(candidate)
    complaints: list[str] = []
    for family in sorted(candidate_families & saturated):
        if facets_request_family(seed_facets, family):
            continue
        label = SEMANTIC_FAMILIES[family]["label"]
        complaints.append(
            f"story reuses the recently saturated {label} machinery even though today's drawn "
            "Facets do not request it; change the causal engine, stakes, and social physics rather "
            "than renaming the same economy"
        )
    return complaints


def title_shape_complaints(proposal: object) -> list[str]:
    """Reject the catalog's overused three-word ``The X Y`` title silhouette."""
    if not isinstance(proposal, dict):
        return []
    title = str(proposal.get("title") or "").strip().rstrip(".!?")
    if not _THE_X_Y_TITLE.fullmatch(title):
        return []
    return [
        f"dream title {title!r} uses the over-repeated 'The X Y' silhouette; choose a different "
        "construction such as a proper name, active phrase, clause, relationship, sensory image, "
        "or strong single word rather than another 'The [modifier] [noun]' title"
    ]


def is_deadline_story(text: object) -> bool:
    folded = str(text or "").casefold()
    return any(pattern.search(folded) for pattern in DEADLINE_PATTERNS)


def facets_request_deadline(seed_facets: object) -> bool:
    words = set(_words(_drawn_facet_text(seed_facets)))
    return bool(words & DEADLINE_FACET_MARKERS)


def structural_repetition_complaints(
    proposal: object,
    recent_story_texts: list[str],
    seed_facets: object,
) -> list[str]:
    recent = recent_story_texts[-RECENT_STRUCTURE_LOOKBACK:]
    deadline_count = sum(is_deadline_story(text) for text in recent)
    if (
        deadline_count >= 3
        and is_deadline_story(story_core_text(proposal))
        and not facets_request_deadline(seed_facets)
    ):
        return [
            "story repeats the recent countdown/deadline skeleton; at least three of the last five "
            "worlds already used explicit time pressure, so rebuild this one around choice, "
            "discovery, relationship, aftermath, play, transformation, or another non-clock engine"
        ]
    return []


def _facet_text(facet: object) -> str:
    if not isinstance(facet, dict):
        return ""
    return " ".join(
        str(facet.get(key) or "")
        for key in ("title", "slug", "description")
    )


def _terms(text: object) -> set[str]:
    return {
        word
        for word in _DISTINCTIVE.findall(str(text or "").casefold())
        if word not in STOPWORDS
    }


def invented_facet_complaints(
    invented: object,
    recent_story_texts: list[str],
    recent_invented_facets: list[dict[str, Any]],
) -> list[str]:
    """Keep today's local trope from becoming tomorrow's reusable catalog seed."""
    if not isinstance(invented, list):
        return []
    history_sources = list(recent_story_texts[-RECENT_INVENTION_LOOKBACK:])
    history_sources.extend(_facet_text(facet) for facet in recent_invented_facets)
    saturated = saturated_families(history_sources, minimum_sources=2, minimum_hits=1)
    complaints: list[str] = []

    prior_texts = [_facet_text(facet) for facet in recent_invented_facets]
    for facet in invented:
        if not isinstance(facet, dict):
            continue
        text = _facet_text(facet)
        for family in sorted(saturated):
            if family_hit_count(text, family) < 1:
                continue
            label = SEMANTIC_FAMILIES[family]["label"]
            complaints.append(
                f"invented Facet {facet.get('title')!r} would persist the recently saturated "
                f"{label} groove into the reusable catalog; invent a concept that opens a "
                "different future story-space instead of naming today's recurring trope"
            )

        candidate_terms = _terms(text)
        for prior in prior_texts:
            prior_terms = _terms(prior)
            if not candidate_terms or not prior_terms:
                continue
            shared = candidate_terms & prior_terms
            union = candidate_terms | prior_terms
            similarity = len(shared) / len(union) if union else 0.0
            if len(shared) >= 3 and similarity >= 0.30:
                examples = ", ".join(sorted(shared)[:5])
                complaints.append(
                    f"invented Facet {facet.get('title')!r} substantially echoes a recent invented "
                    f"Facet ({examples}); create a more orthogonal primitive rather than a sibling label"
                )
                break
    return complaints


def _pick(day: str, salt: str, values: tuple[str, ...]) -> str:
    digest = hashlib.sha256(f"{salt}:{day}".encode()).digest()
    return values[int.from_bytes(digest[:4], "big") % len(values)]


def title_direction(day: str) -> str:
    return _pick(day, "title-shape", TITLE_DIRECTIONS)


def structural_direction(day: str) -> str:
    return _pick(day, "story-contrast", STRUCTURAL_DIRECTIONS)


def visual_direction(day: str) -> str:
    return _pick(day, "visual-contrast", VISUAL_DIRECTIONS)
