#!/usr/bin/env python3
"""Daily Dream proposal builder with history-aware creative-entropy policy.

The stable builder implementation lives in ``build_dream_proposal_core.py``.  This
entrypoint executes that implementation in this module namespace, then overlays the small
set of policy functions that need catalog history: recent-Facet cooldowns, invention
originality checks, and per-day structural/title/visual contrast directions.

Keeping the overlay here means every existing import and CLI keeps the same canonical
``scripts.build_dream_proposal`` module, including tests that monkeypatch module globals
such as ``BACKLOG``.
"""
from pathlib import Path as _BootstrapPath

_BOOTSTRAP_NAME = __name__
_CORE_PATH = _BootstrapPath(__file__).with_name("build_dream_proposal_core.py")
_CORE_SOURCE = _CORE_PATH.read_text(encoding="utf-8")

# Execute the stable implementation in *this* module's globals so old monkeypatch/test
# semantics remain intact. Suppress its __main__ footer until the overlay is installed.
globals()["__name__"] = "build_dream_proposal"
exec(compile(_CORE_SOURCE, str(_CORE_PATH), "exec"), globals(), globals())
globals()["__name__"] = _BOOTSTRAP_NAME

try:
    import dream_creative_entropy as creative_entropy  # noqa: E402
except ModuleNotFoundError:  # imported as scripts.build_dream_proposal in pytest
    from scripts import dream_creative_entropy as creative_entropy  # noqa: E402

_ORIGINAL_INVENTION_INSTRUCTIONS = _invention_instructions
_ORIGINAL_VALIDATE_INVENTIONS = validate_inventions
_ORIGINAL_VALIDATE_PROPOSAL = validate_proposal
_ORIGINAL_BUILD_BRIEF = build_brief

CREATIVE_ENTROPY_VERSION = creative_entropy.ENTROPY_VERSION
RECENT_FACET_LOOKBACK = creative_entropy.RECENT_FACET_LOOKBACK


def _recent_proposals(
    day: str,
    *,
    backlog_dir: Path | str | None = None,
    lookback: int = RECENT_FACET_LOOKBACK,
) -> list[dict[str, Any]]:
    """Return recent authored proposal payloads, oldest to newest."""
    root = Path(backlog_dir) if backlog_dir is not None else BACKLOG
    if not root.exists() or lookback <= 0:
        return []
    paths = [
        path
        for path in sorted(root.glob("20??-??-??-*.md"))
        if path.name[:10] < day
    ][-lookback:]
    proposals_out: list[dict[str, Any]] = []
    for path in paths:
        try:
            proposal = _proposal_data(path.read_text(encoding="utf-8"))
        except OSError:
            continue
        if proposal:
            proposals_out.append(proposal)
    return proposals_out


def recent_facet_slugs(
    day: str,
    *,
    backlog_dir: Path | str | None = None,
    lookback: int = RECENT_FACET_LOOKBACK,
) -> set[str]:
    """Facet identities spent by the recent curated sequence.

    The old planner prevented duplicates *inside* one draw but allowed the same high-weight
    Facet to return tomorrow. For a daily idea engine that is the wrong unit of novelty.
    """
    spent: set[str] = set()
    for proposal in _recent_proposals(day, backlog_dir=backlog_dir, lookback=lookback):
        elements = (proposal.get("seed_facets") or {}).get("elements") or {}
        if not isinstance(elements, dict):
            continue
        for rows in elements.values():
            if not isinstance(rows, list):
                continue
            for facet in rows:
                key = creative_entropy.facet_key(facet)
                if key:
                    spent.add(key)
    return spent


def recent_story_texts(
    day: str,
    *,
    backlog_dir: Path | str | None = None,
    lookback: int = creative_entropy.RECENT_INVENTION_LOOKBACK,
) -> list[str]:
    return [
        creative_entropy.story_core_text(proposal)
        for proposal in _recent_proposals(day, backlog_dir=backlog_dir, lookback=lookback)
    ]


def recent_invented_facets(
    day: str,
    *,
    backlog_dir: Path | str | None = None,
    lookback: int = creative_entropy.RECENT_INVENTION_LOOKBACK,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for proposal in _recent_proposals(day, backlog_dir=backlog_dir, lookback=lookback):
        invented = (proposal.get("seed_facets") or {}).get("invented")
        if not isinstance(invented, list):
            continue
        rows.extend(facet for facet in invented if isinstance(facet, dict))
    return rows


def _eligible_pool(
    pool: list[dict[str, Any]],
    active_theme_cooldowns: set[str],
    spent_facets: set[str],
    saturated_story_families: set[str],
    *,
    minimum: int,
) -> list[dict[str, Any]]:
    themed = theme_diversity.apply_seed_cooldowns(
        pool, active_theme_cooldowns, minimum=minimum
    )
    fresh = creative_entropy.apply_recent_facet_cooldown(
        themed, spent_facets, minimum=minimum
    )
    return creative_entropy.apply_semantic_family_cooldown(
        fresh, saturated_story_families, minimum=minimum
    )


def facet_seed_plan(
    day: str,
    catalog: dict[str, list[dict[str, Any]]] | None = None,
    cooldowns: set[str] | None = None,
    spent_facets: set[str] | None = None,
    saturated_story_families: set[str] | None = None,
) -> dict[str, Any]:
    """Build today's deterministic plan from pools that remember the recent sequence."""
    source = "provided"
    if catalog is None:
        catalog, source = fetch_facet_catalog()
    active_cooldowns = recent_theme_cooldowns(day) if cooldowns is None else set(cooldowns)
    recent_spent = recent_facet_slugs(day) if spent_facets is None else set(spent_facets)
    recent_story = recent_story_texts(day)
    saturated = (
        creative_entropy.saturated_families(
            recent_story[-creative_entropy.RECENT_STRUCTURE_LOOKBACK:]
        )
        if saturated_story_families is None
        else set(saturated_story_families)
    )

    seed = int.from_bytes(
        hashlib.sha256(f"daily-dream-v2:{day}".encode()).digest()[:8], "big"
    )
    rng = random.Random(seed)

    genre_pool = _eligible_pool(
        catalog["GENRE"], active_cooldowns, recent_spent, saturated, minimum=7
    )
    genres = _draw(rng, genre_pool, 7)

    creature_tax = rng.choice(
        [taxonomy for taxonomy in CREATURE_TAXONOMIES if catalog.get(taxonomy)]
        or ["ANIMAL"]
    )
    flavour_pool = [taxonomy for taxonomy in FLAVOUR_TAXONOMIES if catalog.get(taxonomy)]
    flavour_taxes = (
        rng.sample(flavour_pool, min(2, len(flavour_pool)))
        if flavour_pool
        else ["OCCUPATION"]
    )
    while len(flavour_taxes) < 2:
        flavour_taxes.append(flavour_taxes[0])

    creature = _draw(
        rng,
        _eligible_pool(
            catalog[creature_tax], active_cooldowns, recent_spent, saturated, minimum=1
        ),
    )[0]
    occupation = _draw(
        rng,
        _eligible_pool(
            catalog[flavour_taxes[0]], active_cooldowns, recent_spent, saturated, minimum=1
        ),
    )[0]
    personality = _draw(
        rng,
        _eligible_pool(
            catalog[flavour_taxes[1]], active_cooldowns, recent_spent, saturated, minimum=1
        ),
    )[0]
    material_pool = creative_entropy.apply_recent_facet_cooldown(
        catalog["MATERIAL"], recent_spent, minimum=1
    )
    material = _draw(
        rng,
        creative_entropy.apply_semantic_family_cooldown(
            material_pool, saturated, minimum=1
        ),
    )[0]

    umbrella = genres[:2]
    extras = dict(
        zip(
            ("location", "character", "reward_item", "reward_skill", "scenario"),
            genres[2:],
        )
    )
    elements = {
        "vibe": [*umbrella, creature, occupation],
        "location": [*umbrella, extras["location"], creature, material],
        "character": [*umbrella, extras["character"], creature, occupation, personality],
        "reward_item": [*umbrella, extras["reward_item"], material],
        "reward_skill": [*umbrella, extras["reward_skill"], occupation],
        "scenario": [
            *umbrella,
            extras["scenario"],
            extras["location"],
            extras["character"],
            creature,
        ],
    }
    seeded = {"GENRE", creature_tax, "MATERIAL", *flavour_taxes}
    return {
        "version": 2,
        "creative_entropy_version": CREATIVE_ENTROPY_VERSION,
        "date": day,
        "deterministic_seed": seed,
        "catalog_source": source,
        "umbrella": {
            "genres": umbrella,
            "creature": creature,
            "wildcard": occupation,
            "wildcard_role": flavour_taxes[0].lower(),
        },
        "shared": {"material": material, "personality": personality},
        "seeded_taxonomies": sorted(seeded),
        "invent": plan_inventions(rng, catalog, seeded),
        "extra_genres": extras,
        "elements": elements,
    }


def _invention_instructions(seeds: dict[str, Any]) -> list[str]:
    lines = _ORIGINAL_INVENTION_INSTRUCTIONS(seeds)
    if not lines:
        return lines
    guardrails = [
        "INVENTION ORIGINALITY — the two new Facets become reusable catalog vocabulary, "
        "so judge them as seeds for FUTURE worlds, not labels for today's plot. A good invented "
        "Facet opens several unrelated premises; it does not merely name today's debt, grief, "
        "bureaucratic procedure, job title, deadline, or signature object.",
        "Do not crystallize recent Daily Dream habits into the Facet catalog. If the recent "
        "worlds have been preoccupied with obligation/tallies, grief/memory, letters/contracts, "
        "civic procedure, specialist maintenance, or another repeated engine, invent sideways "
        "into genuinely different conceptual territory even when today's story touches it.",
    ]
    for index, line in enumerate(lines):
        if line.startswith("PHASE 3"):
            return [*lines[:index], *guardrails, *lines[index:]]
    return [*lines, *guardrails]


def build_brief(day: str | None = None, catalog=None) -> dict[str, Any]:
    brief = _ORIGINAL_BUILD_BRIEF(day, catalog)
    proposal_day = str(brief["proposal_date"])
    brief["instructions"].extend(
        [
            "THE SCHEMA IS STORAGE SHAPE, NOT PLOT SHAPE. `local_rule` does not have to "
            "be the conflict, `carries` does not have to be a professional tool, a Reward "
            "catch does not have to be a curse, and the required Scenario does not require "
            "a countdown. One Character card does not mean one lone specialist must solve everything.",
            "Do not default to 'has one night', 'one tide', 'three days', 'before dawn', "
            "'before X arrives', or another clock unless today's Facets specifically make timing "
            "the interesting idea. Deadlines are one story shape, not the definition of stakes.",
            "Letters, missives, contracts, treaties, vows, signatures, and similar documents are "
            "also a demonstrated rut. Do not use them as the automatic carrier of mystery, stakes, "
            "or world rules; when that family is recent, the seed planner cools Facets that would "
            "pull the story back into it.",
            "TITLE SHAPE IS ENFORCED: do not use the three-word 'The X Y' silhouette. It has "
            "appeared too often in the catalog and will fail validation even if the nouns are new.",
            f"STRUCTURAL CONTRAST FOR TODAY: {creative_entropy.structural_direction(proposal_day)}",
            f"TITLE CONSTRUCTION FOR TODAY: {creative_entropy.title_direction(proposal_day)}",
            f"VISUAL CONTRAST FOR TODAY: {creative_entropy.visual_direction(proposal_day)}",
        ]
    )
    return brief


def validate_inventions(seeds: dict[str, Any]) -> list[str]:
    bad = _ORIGINAL_VALIDATE_INVENTIONS(seeds)
    if int(seeds.get("creative_entropy_version") or 0) < CREATIVE_ENTROPY_VERSION:
        return bad
    day = str(seeds.get("date") or "")
    if not day:
        return bad
    bad.extend(
        creative_entropy.invented_facet_complaints(
            seeds.get("invented"),
            recent_story_texts(day),
            recent_invented_facets(day),
        )
    )
    return bad


def validate_proposal(proposal: Any) -> list[str]:
    bad = _ORIGINAL_VALIDATE_PROPOSAL(proposal)
    if not isinstance(proposal, dict):
        return bad
    seeds = proposal.get("seed_facets")
    if not isinstance(seeds, dict):
        return bad
    if int(seeds.get("creative_entropy_version") or 0) < CREATIVE_ENTROPY_VERSION:
        return bad
    day = str(seeds.get("date") or "")
    if not day:
        return bad
    recent = recent_story_texts(day)
    bad.extend(creative_entropy.story_family_complaints(proposal, recent, seeds))
    bad.extend(creative_entropy.structural_repetition_complaints(proposal, recent, seeds))
    bad.extend(creative_entropy.title_shape_complaints(proposal))
    return bad


if _BOOTSTRAP_NAME == "__main__":
    raise SystemExit(main())
