#!/usr/bin/env python3
"""Private catalog-candidate contract: six Daily Dream + four Zuzu/Emperor models.

New supplemental objects are locations/settings and characters only. They do not
change a game's playable scenarios, rewards, roster, branching or roadmap.
Historical v3 fourteen-asset bundles remain readable but are not auto-built.
"""
from __future__ import annotations

from typing import Any

try:
    import daily_dream_v3_contract as legacy
except ModuleNotFoundError:
    from scripts import daily_dream_v3_contract as legacy

BUNDLE_VERSION = 4
CUTOVER_DAY = "2026-11-14"
DREAM_SLOTS = legacy.DREAM_SLOTS
ZUZU_SLOTS = (
    "zuzu_location_1", "zuzu_location_2",
    "zuzu_character_1", "zuzu_character_2",
)
FACET_SLOTS = DREAM_SLOTS + ZUZU_SLOTS
ZUZU_COUNTS = {"locations": 2, "characters": 2}
PROJECT_TARGETS = legacy.PROJECT_TARGETS
CHECKPOINT_FAMILIES = legacy.CHECKPOINT_FAMILIES
COPY_FIELDS = legacy.COPY_FIELDS


def is_v4_day(day: str) -> bool:
    return day >= CUTOVER_DAY


def asset_manifest(proposal: dict[str, Any]) -> list[legacy.BundleAsset]:
    """The v3 manifest helper is compatible with the strict 6+4 shape."""
    return legacy.asset_manifest(proposal)


def _present(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_v4(proposal: Any) -> list[str]:
    if not isinstance(proposal, dict):
        return ["proposal must be an object"]
    errors: list[str] = []
    if proposal.get("bundle_version") != BUNDLE_VERSION:
        errors.append("bundle_version must be 4")
    for field in ("title", "slug", "idea"):
        if not _present(proposal.get(field)):
            errors.append(f"missing {field}")
    vibe = proposal.get("vibe")
    if not isinstance(vibe, dict) or any(
        not _present(vibe.get(field)) for field in ("title", "line", "art_direction")
    ):
        errors.append("the original complete Daily Dream vibe is required")
    elif vibe.get("project_target") or vibe.get("checkpoint_family"):
        errors.append("the original Dream must not inherit Zuzu art")

    seed = proposal.get("seed_facets")
    elements = seed.get("elements") if isinstance(seed, dict) else None
    if not isinstance(seed, dict) or seed.get("version") != 4:
        errors.append("seed_facets.version must be exactly 4")
    if not isinstance(elements, dict) or set(elements) != set(FACET_SLOTS):
        errors.append("seed_facets.elements must contain exactly ten slots")
        elements = {}
    for slot in FACET_SLOTS:
        facets = elements.get(slot)
        if not isinstance(facets, list) or not facets or any(
            not isinstance(f, dict)
            or not _present(f.get("title"))
            or not _present(f.get("taxonomy"))
            or not (_present(f.get("slug")) or isinstance(f.get("id"), int))
            for f in facets
        ):
            errors.append(f"seed_facets.elements.{slot} requires registered Facets")

    for kind, count in legacy.DREAM_COUNTS.items():
        rows = proposal.get(kind)
        if not isinstance(rows, list) or len(rows) != count:
            errors.append(f"dream.{kind} needs exactly {count} originals")
            continue
        for i, row in enumerate(rows):
            if not isinstance(row, dict):
                errors.append(f"dream.{kind}[{i}] must be an object")
                continue
            for field in COPY_FIELDS[kind]:
                if not _present(row.get(field)):
                    errors.append(f"dream.{kind}[{i}] missing {field}")
            if row.get("linked_to_vibe") is False:
                errors.append(f"dream.{kind}[{i}] must link to its own Dream")
            if row.get("checkpoint_family") or row.get("project_target"):
                errors.append(f"dream.{kind}[{i}] must retain Dream art style")
    original_rewards = proposal.get("rewards", [])
    if len(original_rewards) == 2 and sorted(
        str(row.get("reward_type", "")).upper()
        for row in original_rewards if isinstance(row, dict)
    ) != ["ITEM", "SKILL"]:
        errors.append("the original Daily Dream still needs ITEM and SKILL")
    scenarios = proposal.get("scenarios", [])
    if len(scenarios) == 1 and isinstance(scenarios[0], dict) and isinstance(vibe, dict):
        setup = str(scenarios[0].get("setup") or "").casefold()
        names = [vibe.get("title")]
        for kind, field in (("locations", "title"), ("characters", "name")):
            rows = proposal.get(kind, [])
            if rows and isinstance(rows[0], dict):
                names.append(rows[0].get(field))
        for name in names:
            if _present(name) and str(name).casefold() not in setup:
                errors.append(f"original Dream scenario must mention {name}")

    zuzu = proposal.get("zuzu_assets")
    if not isinstance(zuzu, dict) or set(zuzu) != set(ZUZU_COUNTS):
        errors.append("zuzu_assets may contain only locations and characters")
        zuzu = {}
    forbidden = (
        "dreamIds", "dreamId", "dream_id", "world_dream_id",
        "worldDreamId", "parentDreamId", "fromDreamId",
        "toDreamId", "location_dream_id", "linked_to_vibe",
        "scenarioIds", "rewardIds", "gameplayId",
    )
    for kind, count in ZUZU_COUNTS.items():
        rows = zuzu.get(kind)
        if not isinstance(rows, list) or len(rows) != count:
            errors.append(f"zuzu.{kind} must have exactly {count} candidates")
            continue
        owners = []
        for i, row in enumerate(rows):
            if not isinstance(row, dict):
                errors.append(f"zuzu.{kind}[{i}] must be an object")
                continue
            for field in COPY_FIELDS[kind]:
                if not _present(row.get(field)):
                    errors.append(f"zuzu.{kind}[{i}] missing {field}")
            owner = str(row.get("project_target") or "")
            owners.append(owner)
            if owner not in PROJECT_TARGETS:
                errors.append(f"zuzu.{kind}[{i}] needs a valid project_target")
            if str(row.get("checkpoint_family") or "").lower() not in CHECKPOINT_FAMILIES:
                errors.append(f"zuzu.{kind}[{i}] needs an Arthemy/Illustrious checkpoint")
            if any(row.get(field) for field in forbidden):
                errors.append(f"zuzu.{kind}[{i}] may not join a game or Dream")
        if sorted(owners) != sorted(PROJECT_TARGETS):
            errors.append(f"zuzu.{kind} needs one candidate per project")

    if proposal.get("narrator"):
        errors.append("Daily Dream does not create a narrator")
    manifest = asset_manifest(proposal)
    if len(manifest) != 10 or len({asset.slot for asset in manifest}) != 10:
        errors.append("ten unique asset slots are required")
    if sum(asset.linked_to_vibe for asset in manifest) != 5:
        errors.append("the five original Dream satellites must remain linked")
    if any(asset.lane == "zuzu" and asset.linked_to_vibe for asset in manifest):
        errors.append("catalog candidates must not link to the random Dream")
    return errors
