from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

PROJECT_LIFECYCLE_STATUSES = ("active", "continuous", "paused", "finished", "retired")
WORKABLE_PROJECT_STATUSES = ("active", "continuous")


def load_project_overrides(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    entries = data.get("overrides") or []
    if isinstance(entries, dict):
        return {str(slug): cfg for slug, cfg in entries.items() if isinstance(cfg, dict)}
    if isinstance(entries, list):
        return {
            str(entry["slug"]): entry
            for entry in entries
            if isinstance(entry, dict) and isinstance(entry.get("slug"), str)
        }
    return {}


def lifecycle_status(overrides: dict[str, dict[str, Any]], slug: str) -> str:
    value = str(overrides.get(slug, {}).get("status", "active"))
    return value if value in PROJECT_LIFECYCLE_STATUSES else "active"


def ordered_workable_slugs(order: list[str], overrides: dict[str, dict[str, Any]]) -> list[str]:
    known = set(overrides)
    ordered = [slug for slug in order if slug in known]
    ordered += sorted(slug for slug in known if slug not in set(ordered))
    active = [slug for slug in ordered if lifecycle_status(overrides, slug) == "active"]
    continuous = [slug for slug in ordered if lifecycle_status(overrides, slug) == "continuous"]
    return [*active, *continuous]
