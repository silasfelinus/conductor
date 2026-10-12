#!/usr/bin/env python3
"""Pure, network-free contract for a future 14-asset Daily Dream build.

Keep the ORIGINAL six-asset Daily Dream as one connected, styled mini-world.
Add a separate eight-asset Zuzu allocation with no relations to that Dream.
This only validates future drafts and creates a deterministic manifest: it
does NOT create Kind Robots rows or ArtJobs or activate the v3 build path.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

BUNDLE_VERSION = 3
PROJECT_TARGETS = ("zuzu-gamebook", "emperor-of-dust")
CHECKPOINT_FAMILIES = ("arthemy", "illustrious")

DREAM_SLOTS = ("vibe", "location", "character", "reward_item", "reward_skill", "scenario")
ZUZU_SLOTS = (
    "zuzu_location_1", "zuzu_location_2",
    "zuzu_character_1", "zuzu_character_2",
    "zuzu_reward_item", "zuzu_reward_skill",
    "zuzu_scenario_1", "zuzu_scenario_2",
)
FACET_SLOTS = DREAM_SLOTS + ZUZU_SLOTS
DREAM_COUNTS = {"locations": 1, "characters": 1, "rewards": 2, "scenarios": 1}
ZUZU_COUNTS = {"locations": 2, "characters": 2, "rewards": 2, "scenarios": 2}
COPY_FIELDS = {
    "locations": ("title", "known_for", "local_rule", "best_scene", "art_direction"),
    "characters": ("name", "role_drive", "carries", "complication", "look"),
    "rewards": ("name", "reward_type", "rarity", "grants", "best_used_when", "catch", "look"),
    "scenarios": ("title", "setup"),
}
TITLE_FIELD = {"locations": "title", "characters": "name", "rewards": "name", "scenarios": "title"}
REWARD_TYPES = ("ITEM", "SKILL")


@dataclass(frozen=True)
class BundleAsset:
    slot: str
    kind: str
    lane: str
    linked_to_vibe: bool
    project_target: str | None
    checkpoint_family: str | None
    title: str


def _present(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _rows(parent: dict[str, Any], kind: str) -> list[Any]:
    value = parent.get(kind)
    return value if isinstance(value, list) else []


def _target(row: dict[str, Any]) -> str:
    return str(row.get("project_target") or "").strip()


def _checkpoint(row: dict[str, Any]) -> str:
    return str(row.get("checkpoint_family") or "").strip().lower()


def _slot(kind: str, index: int, row: dict[str, Any], lane: str) -> str:
    prefix = "zuzu_" if lane == "zuzu" else ""
    if kind == "rewards":
        return prefix + "reward_" + str(row.get("reward_type") or "").lower()
    return prefix + kind[:-1] + (f"_{index}" if lane == "zuzu" else "")


def asset_manifest(proposal: dict[str, Any]) -> list[BundleAsset]:
    """Stable 14-asset assignment for the eventual single transactional writer.

    Vibe is the Dream root, its five satellite records are linked to the world,
    and NONE of the eight Zuzu assets link to the unrelated daily world.
    Do not trust the manifest until validate_v3(proposal) returns no errors.
    """
    vibe = proposal.get("vibe")
    title = str(vibe.get("title") or "") if isinstance(vibe, dict) else ""
    result = [BundleAsset("vibe", "vibe", "dream", False, None, None, title)]
    zuzu = proposal.get("zuzu_assets")
    for lane, source in (("dream", proposal), ("zuzu", zuzu if isinstance(zuzu, dict) else {})):
        for kind in ZUZU_COUNTS:
            for index, row in enumerate(_rows(source, kind), start=1):
                if not isinstance(row, dict):
                    continue
                result.append(
                    BundleAsset(
                        slot=_slot(kind, index, row, lane),
                        kind=kind,
                        lane=lane,
                        linked_to_vibe=(lane == "dream"),
                        project_target=_target(row) if lane == "zuzu" else None,
                        checkpoint_family=_checkpoint(row) if lane == "zuzu" else None,
                        title=str(row.get(TITLE_FIELD[kind]) or ""),
                    )
                )
    return result


def validate_v3(proposal: Any) -> list[str]:
    """Reject wrong counts, cross-lane links and choice-free Zuzu scenarios."""
    if not isinstance(proposal, dict):
        return ["proposal must be an object"]
    errors: list[str] = []
    if proposal.get("bundle_version") != BUNDLE_VERSION:
        errors.append("bundle_version must be 3")
    for field in ("title", "slug", "idea"):
        if not _present(proposal.get(field)):
            errors.append(f"missing {field}")

    vibe = proposal.get("vibe")
    if not isinstance(vibe, dict):
        errors.append("one original daily vibe is required")
    else:
        for field in ("title", "line", "art_direction"):
            if not _present(vibe.get(field)):
                errors.append(f"vibe missing {field}")
        if vibe.get("project_target") or vibe.get("checkpoint_family"):
            errors.append("daily vibe must retain its original art identity, not a Zuzu project style")

    dream = proposal
    zuzu = proposal.get("zuzu_assets")
    if not isinstance(zuzu, dict):
        errors.append("zuzu_assets must be a separate object")
        zuzu = {}

    seed = proposal.get("seed_facets")
    try:
        version = int(seed.get("version") or 0) if isinstance(seed, dict) else 0
    except (ValueError, TypeError):
        version = 0
    if version < 3:
        errors.append("seed_facets.version must be at least 3")
    elements = seed.get("elements") if isinstance(seed, dict) else None
    if not isinstance(elements, dict):
        errors.append("seed_facets.elements must be an object")
        elements = {}
    for slot in FACET_SLOTS:
        facets = elements.get(slot)
        if not isinstance(facets, list) or not facets:
            errors.append(f"seed_facets.elements.{slot} must contain Facets")
        elif any(
            not isinstance(f, dict) or not _present(f.get("title"))
            or not _present(f.get("taxonomy"))
            or not (_present(f.get("slug")) or isinstance(f.get("id"), int))
            for f in facets
        ):
            errors.append(f"seed_facets.elements.{slot} contains invalid Facets")

    if isinstance(seed, dict) and seed.get("link_zuzu_to_vibe"):
        errors.append("Zuzu extras must not be linked to the daily vibe")
    if any(zuzu.get(field) for field in (
        "world_dream_id", "dream_id", "dreamIds", "dreamId", "worldDreamId",
        "parentDreamId", "fromDreamId", "toDreamId",
    )):
        errors.append("Zuzu extras must not inherit daily vibe Dream relations")

    for lane, source, expected in (
        ("dream", dream, DREAM_COUNTS), ("zuzu", zuzu, ZUZU_COUNTS)
    ):
        for kind, count in expected.items():
            rows = _rows(source, kind)
            if len(rows) != count:
                errors.append(f"{lane}.{kind} has {len(rows)}; expected exactly {count}")
                continue
            owners: list[str] = []
            for index, row in enumerate(rows):
                where = f"{lane}.{kind}[{index}]"
                if not isinstance(row, dict):
                    errors.append(f"{where} must be an object")
                    continue
                for field in COPY_FIELDS[kind]:
                    if not _present(row.get(field)):
                        errors.append(f"{where} missing {field}")
                if lane == "dream":
                    if row.get("project_target") or row.get("checkpoint_family"):
                        errors.append(f"{where} must inherit the daily vibe's art style, not Zuzu")
                    if row.get("linked_to_vibe") is False:
                        errors.append(f"{where} must link to the daily vibe")
                else:
                    owner = _target(row)
                    owners.append(owner)
                    if owner not in PROJECT_TARGETS:
                        errors.append(f"{where} must target zuzu-gamebook or emperor-of-dust")
                    if _checkpoint(row) not in CHECKPOINT_FAMILIES:
                        errors.append(f"{where} must use Arthemy or Illustrious")
                    # Reject ALL inbound relations on external author input,
                    # not merely dreamIds. The sole supported Zuzu relation is
                    # generated within the transaction: scenario -> its newly
                    # created Zuzu location, never to the random PITCH.
                    forbidden = (
                        "dreamIds", "dreamId", "dream_id", "dream_ids",
                        "world_dream_id", "worldDreamId", "parentDreamId",
                        "fromDreamId", "toDreamId", "location_dream_id",
                        "linked_to_vibe",
                    )
                    if any(row.get(field) for field in forbidden):
                        errors.append(f"{where} must not link to the daily vibe")
            if lane == "zuzu" and sorted(owners) != sorted(PROJECT_TARGETS):
                errors.append(f"zuzu.{kind} must give exactly one asset to each project")
            if kind == "rewards":
                types = sorted(
                    str(row.get("reward_type") or "").upper()
                    for row in rows if isinstance(row, dict)
                )
                if types != sorted(REWARD_TYPES):
                    errors.append(f"{lane}.rewards need one ITEM and one SKILL")

    # The original Daily Dream scene is part of its coherent mini-world.
    original_scenes = _rows(dream, "scenarios")
    if len(original_scenes) == 1 and isinstance(original_scenes[0], dict) and isinstance(vibe, dict):
        setup = str(original_scenes[0].get("setup") or "").casefold()
        named = (vibe.get("title"),)
        for source, field in (("locations", "title"), ("characters", "name")):
            rows = _rows(dream, source)
            if rows and isinstance(rows[0], dict):
                named += (rows[0].get(field),)
        for name in named:
            if _present(name) and str(name).casefold() not in setup:
                errors.append(f"dream scenario must reference the linked vibe/location/character: {name}")

    for i, row in enumerate(_rows(zuzu, "scenarios")):
        if not isinstance(row, dict):
            continue
        where = f"zuzu.scenarios[{i}]"
        choices = row.get("choices")
        if not isinstance(choices, list) or len(choices) < 2:
            errors.append(f"{where} needs at least two moral choices")
            continue
        labels: list[str] = []
        for j, choice in enumerate(choices):
            label = f"{where}.choices[{j}]"
            if not isinstance(choice, dict):
                errors.append(f"{label} must be an object")
                continue
            for field in ("label", "tradeoff", "immediate_consequence", "later_consequence"):
                if not _present(choice.get(field)):
                    errors.append(f"{label} missing {field}")
            labels.append(str(choice.get("label") or "").strip().casefold())
        if len(set(labels)) != len(labels):
            errors.append(f"{where} choice labels must be distinct")

    if proposal.get("narrator"):
        errors.append("Daily Dreams do not create a narrator")
    manifest = asset_manifest(proposal)
    if len(manifest) != 14 or len(set(a.slot for a in manifest)) != 14:
        errors.append("fourteen unique asset slots are required")
    if sum(a.linked_to_vibe for a in manifest) != 5:
        errors.append("five Dream satellites must link to the daily vibe")
    if any(a.lane == "zuzu" and (a.linked_to_vibe or not a.project_target) for a in manifest):
        errors.append("all eight Zuzu extras must have projects and no vibe links")
    return errors
