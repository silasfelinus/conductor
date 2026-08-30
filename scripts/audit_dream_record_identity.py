#!/usr/bin/env python3
"""Detect built Daily Dream bundles that claim the same live entity row.

A built bundle owns exactly one world Dream, one location Dream, one Character,
two Rewards, and one Scenario. Revisions must update those rows in place for that
bundle only; the same `(model, id)` appearing in two different backlog bundles is
therefore a catalog identity collision and means live content can overwrite another
Dream's content.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "projects" / "dream-cycle" / "backlog"


def _block(text: str, name: str) -> dict[str, Any] | None:
    match = re.search(rf"<!--\s*{re.escape(name)}\s*\n(.*?)\n-->", text, re.DOTALL)
    if not match:
        return None
    value = json.loads(match.group(1))
    return value if isinstance(value, dict) else None


def _frontmatter(text: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*['\"]?([^'\"\n]+)['\"]?\s*$", text)
    return match.group(1).strip() if match else ""


def record_uses(backlog: Path = BACKLOG) -> dict[tuple[str, int], list[dict[str, str]]]:
    uses: dict[tuple[str, int], list[dict[str, str]]] = defaultdict(list)
    for path in sorted(backlog.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        built = _block(text, "built-data")
        if not built:
            continue
        records = built.get("records") or {}
        bundle = {
            "path": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
            "day": _frontmatter(text, "proposal_date") or path.name[:10],
            "title": _frontmatter(text, "title") or path.stem,
        }

        def add(model: str, row: Any, role: str) -> None:
            if not isinstance(row, dict) or not isinstance(row.get("id"), int):
                return
            uses[(model, row["id"])].append({**bundle, "role": role})

        add("Dream", records.get("world"), "world")
        for row in records.get("locations") or []:
            add("Dream", row, "location")
        for row in records.get("characters") or []:
            add("Character", row, "character")
        for row in records.get("rewards") or []:
            role = f"reward:{row.get('reward_type') or 'unknown'}"
            add("Reward", row, role)
        for row in records.get("scenarios") or []:
            add("Scenario", row, "scenario")
    return uses


def collisions(backlog: Path = BACKLOG) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (model, entity_id), bundles in sorted(record_uses(backlog).items()):
        distinct = {(row["path"], row["role"]) for row in bundles}
        if len(distinct) <= 1:
            continue
        rows.append({"model": model, "id": entity_id, "uses": bundles})
    return rows


def summary(backlog: Path = BACKLOG) -> dict[str, Any]:
    rows = collisions(backlog)
    affected = sorted({use["path"] for row in rows for use in row["uses"]})
    return {"collision_count": len(rows), "affected_bundles": affected, "collisions": rows}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    report = summary()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if args.strict and report["collision_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
