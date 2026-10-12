#!/usr/bin/env python3
"""Pure, network-free creative contract for the next Daily Dream bundle.

This module deliberately does NOT create Kind Robots objects or ArtJobs.
The v2 transaction remains the only live writer until its v3 replacement is
fully integrated and CI verifies every nine-record / nine-art boundary.

Version 3 contains one independent daily vibe and eight Zuzu-world assets,
explicitly divided between Zuzu Gamebook and Emperor of Dust. Historical v2
proposals are not migrated, reinterpreted or modified by this module.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

BUNDLE_VERSION = 3
PROJECT_TARGETS = ("zuzu-gamebook", "emperor-of-dust")
CHECKPOINT_FAMILIES = ("arthemy", "illustrious")
KIND_SLOTS = (
    ("vibe", None),
    ("location_1", "locations"),
    ("location_2", "locations"),
    ("character_1", "characters"),
    ("character_2", "characters"),
    ("reward_item", "rewards"),
    ("reward_skill", "rewards"),
    ("scenario_1", "scenarios"),
    ("scenario_2", "scenarios"),
)
FACET_SLOTS = tuple(slot for slot, _ in KIND_SLOTS)
EXPECTED_COUNTS = {"locations": 2, "characters": 2, "rewards": 2, "scenarios": 2}
COPY_FIELDS = {
    "locations": ("title", "known_for", "local_rule", "best_scene", "art_direction"),
    "characters": ("name", "role_drive", "carries", "complication", "look"),
    "rewards": ("name", "reward_type", "rarity", "grants", "best_used_when", "catch", "look"),
    "scenarios": ("title", "setup"),
}
REWARD_TYPES = ("ITEM", "SKILL")


@dataclass(frozen=True)
class BundleAsset:
    slot: str
    kind: str
    project_target: str | None
    checkpoint_family: str | None
    title: str

    @property
    def is_independent(self) -> bool:
        return self.project_target is None


def _present(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _rows(proposal: dict[str, Any], kind: str) -> list[dict[str, Any]]:
    rows = proposal.get(kind)
    return rows if isinstance(rows, list) else []


def _target(row: dict[str, Any]) -> str:
    return str(row.get("project_target") or "").strip()


def _checkpoint(row: dict[str, Any]) -> str:
    return str(row.get("checkpoint_family") or "").strip().lower()


def asset_manifest(proposal: dict[str, Any]) -> list[BundleAsset]:
    """Stable nine-slot plan consumed by eventual builder, Facets, art and digest.

    The vibe is NEVER a parent/project for the other eight assets. The manifest
    carries attribution but does not fabricate an unsupported database foreign key.
    The caller must run validate_v3() before trusting this manifest.
    """
    result: list[BundleAsset] = []
    vibe = proposal.get("vibe") or {}
    result.append(BundleAsset("vibe", "vibe", None, None, str(vibe.get("title") or "")))
    for kind, prefix, title_field in (
        ("locations", "location", "title"),
        ("characters", "character", "name"),
        ("rewards", "reward", "name"),
        ("scenarios", "scenario", "title"),
    ):
        for index, row in enumerate(_rows(proposal, kind), start=1):
            slot = (
                f"reward_{str(row.get('reward_type') or '').lower()}"
                if kind == "rewards" else f"{prefix}_{index}"
            )
            result.append(
                BundleAsset(
                    slot, kind, _target(row), _checkpoint(row),
                    str(row.get(title_field) or ""),
                )
            )
    return result


def validate_v3(proposal: Any) -> list[str]:
    """Validate explicit ownership, independent vibe and meaningful moral choices.

    In particular, every content category contributes one asset to EACH Zuzu
    project. A pitch cannot silently route all its characters to one game and
    leave the other with no daily material.
    """
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
        errors.append("one independent vibe is required")
    else:
        for field in ("title", "line", "art_direction"):
            if not _present(vibe.get(field)):
                errors.append(f"vibe missing {field}")
        if vibe.get("project_target"):
            errors.append("independent vibe must not target a Zuzu project")
        if vibe.get("checkpoint_family"):
            errors.append("independent vibe must not inherit a Zuzu checkpoint family")

    seeds = proposal.get("seed_facets")
    if not isinstance(seeds, dict) or int(seeds.get("version") or 0) < 3:
        errors.append("seed_facets.version must be at least 3")
        elements = {}
    else:
        elements = seeds.get("elements")
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
            errors.append(f"seed_facets.elements.{slot} contains an invalid Facet")
    # No subordinate asset inherits the daily vibe's umbrella. Deliberate
    # project-specific editorial briefs remain separate from the independent vibe.
    if isinstance(seeds, dict) and seeds.get("link_zuzu_to_vibe", False):
        errors.append("Zuzu objects must not be linked to the independent vibe")

    for kind, expected in EXPECTED_COUNTS.items():
        actual = len(_rows(proposal, kind))
        if actual != expected:
            errors.append(f"{kind} has {actual}; expected exactly {expected}")
            continue
        project_owners: list[str] = []
        for index, row in enumerate(_rows(proposal, kind)):
            where = f"{kind}[{index}]"
            if not isinstance(row, dict):
                errors.append(f"{where} must be an object")
                continue
            for field in COPY_FIELDS[kind]:
                if not _present(row.get(field)):
                    errors.append(f"{where} missing {field}")
            owner = _target(row)
            project_owners.append(owner)
            if owner not in PROJECT_TARGETS:
                errors.append(f"{where} must target zuzu-gamebook or emperor-of-dust")
            if _checkpoint(row) not in CHECKPOINT_FAMILIES:
                errors.append(f"{where} must use an Illustrious or Arthemy checkpoint family")
        if sorted(project_owners) != sorted(PROJECT_TARGETS):
            errors.append(f"{kind} must contain exactly one asset per Zuzu project")

    rewards = _rows(proposal, "rewards")
    if len(rewards) == 2 and sorted(
        str(row.get("reward_type") or "").upper()
        for row in rewards if isinstance(row, dict)
    ) != sorted(REWARD_TYPES):
        errors.append("rewards must contain one ITEM and one SKILL")
    for index, row in enumerate(_rows(proposal, "scenarios")):
        if not isinstance(row, dict):
            continue
        where = f"scenarios[{index}]"
        choices = row.get("choices")
        if not isinstance(choices, list) or len(choices) < 2:
            errors.append(f"{where} needs at least two moral choices")
            continue
        labels: list[str] = []
        for choice_index, choice in enumerate(choices):
            label = f"{where}.choices[{choice_index}]"
            if not isinstance(choice, dict):
                errors.append(f"{label} must be an object")
                continue
            for field in ("label", "tradeoff", "immediate_consequence", "later_consequence"):
                if not _present(choice.get(field)):
                    errors.append(f"{label} missing {field}")
            labels.append(str(choice.get("label") or "").strip().casefold())
        if len(set(labels)) != len(labels):
            errors.append(f"{where} moral choice labels must be distinct")

    if proposal.get("narrator"):
        errors.append("Daily Dream proposals must not create a narrator")
    manifest = asset_manifest(proposal) if isinstance(vibe, dict) else []
    if len(manifest) != 9 or len({a.slot for a in manifest}) != len(manifest):
        errors.append("nine unique asset slots are required for Facets and ArtJobs")
    return errors
