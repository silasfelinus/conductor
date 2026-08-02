#!/usr/bin/env python3
"""Validate Daily Dream proposals and legacy idea inventory without network calls."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Optional

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BACKLOG = ROOT / "projects" / "dream-cycle" / "backlog"
ELIGIBLE_STATUSES = {"outline", "approved"}
VALID_RARITIES = {"COMMON", "UNCOMMON", "RARE", "EPIC", "LEGENDARY", "MYTHIC"}
REQUIRED_FACET_KEYS = {
    "vibe", "location", "character", "reward_item", "reward_skill", "scenario"
}


class Finding:
    def __init__(self, outline: str, kind: str, detail: str):
        self.outline = outline
        self.kind = kind
        self.detail = detail

    def as_dict(self) -> dict[str, str]:
        return {"outline": self.outline, "kind": self.kind, "detail": self.detail}

    def line(self) -> str:
        return f"  {self.kind}: {self.detail}"


def parse_frontmatter(text: str) -> dict[str, Any]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def parse_data_block(text: str, name: str) -> Optional[dict[str, Any]]:
    match = re.search(rf"<!--\s*{re.escape(name)}\s*\n(.*?)\n-->", text, re.DOTALL)
    if not match:
        return None
    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def split_sections(text: str) -> dict[str, str]:
    body = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
    parts = re.split(r"^##\s+(.+?)\s*$", body, flags=re.MULTILINE)
    return {
        parts[index].strip().lower(): parts[index + 1]
        for index in range(1, len(parts) - 1, 2)
    }


def find_section(sections: dict[str, str], keyword: str) -> Optional[str]:
    return next((body for heading, body in sections.items() if keyword in heading), None)


def is_placeholder(body: Optional[str]) -> bool:
    if body is None:
        return True
    stripped = body.strip()
    if len(stripped) < 15:
        return True
    lines = [line.strip() for line in stripped.splitlines() if line.strip()]
    return bool(lines) and all(line.startswith("- (") for line in lines)


def _canonical_errors(data: Optional[dict[str, Any]]) -> list[str]:
    if not isinstance(data, dict):
        return ["missing or invalid proposal-data block"]
    errors: list[str] = []
    facets = data.get("seed_facets")
    if not isinstance(facets, dict) or int(facets.get("version") or 0) < 2:
        errors.append("seed_facets.version must be at least 2")
    elements = facets.get("elements") if isinstance(facets, dict) else None
    if not isinstance(elements, dict) or not REQUIRED_FACET_KEYS.issubset(elements):
        errors.append("seed_facets.elements must cover all six assets")

    vibe = data.get("vibe")
    if not isinstance(vibe, dict) or not vibe.get("title") or not vibe.get("line"):
        errors.append("exactly one complete vibe is required")

    for field, count in (("locations", 1), ("characters", 1), ("rewards", 2), ("scenarios", 1)):
        value = data.get(field)
        actual = len(value) if isinstance(value, list) else 0
        if actual != count:
            errors.append(f"{field} has {actual}; expected exactly {count}")

    rewards = data.get("rewards") if isinstance(data.get("rewards"), list) else []
    types = {
        str(item.get("reward_type", "")).upper()
        for item in rewards if isinstance(item, dict)
    }
    if types != {"ITEM", "SKILL"}:
        errors.append("rewards must contain exactly one ITEM and one SKILL")
    for item in rewards:
        if isinstance(item, dict) and str(item.get("rarity", "")).upper() not in VALID_RARITIES:
            errors.append(f"invalid reward rarity: {item.get('rarity')!r}")

    if data.get("narrator"):
        errors.append("Daily Dream proposals must not contain a narrator")
    return errors


def check_outline(path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)
    if str(frontmatter.get("type", "")).strip() != "dream":
        return []

    name = path.name
    status = str(frontmatter.get("status", "outline")).strip().lower()
    proposal = bool(frontmatter.get("proposal"))
    if proposal:
        if status not in ELIGIBLE_STATUSES:
            return []
        findings = [
            Finding(name, "proposal-contract", detail)
            for detail in _canonical_errors(parse_data_block(text, "proposal-data"))
        ]
        narrator_flag = str(frontmatter.get("narrator", "no")).strip().lower()
        if narrator_flag not in {"no", "false", "none", ""}:
            findings.append(Finding(name, "proposal-narrator", "frontmatter must not enable a narrator"))
        return findings

    findings: list[Finding] = []
    if status == "building":
        findings.append(
            Finding(name, "legacy-building", "non-proposal Dream files are idea inventory and cannot be building")
        )
    sections = split_sections(text)
    idea = find_section(sections, "idea")
    if is_placeholder(idea):
        findings.append(Finding(name, "idea-missing", "legacy idea inventory needs a usable 'The idea' section"))
    if find_section(sections, "notes from silas") is None:
        findings.append(Finding(name, "notes-missing", "legacy idea inventory needs a Notes from Silas section"))
    return findings


def collect(backlog_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(backlog_dir.glob("*.md")):
        if path.name.startswith("_") or path.name == "README.md":
            continue
        findings.extend(check_outline(path))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backlog-dir", type=Path, default=DEFAULT_BACKLOG)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.backlog_dir.exists():
        print(f"ERROR: backlog dir not found: {args.backlog_dir}", file=sys.stderr)
        return 2
    findings = collect(args.backlog_dir)
    if args.json:
        print(json.dumps([finding.as_dict() for finding in findings], indent=2))
    elif not findings:
        print("Daily Dream proposal and legacy idea-inventory contracts are clean.")
    else:
        print(f"Dream-cycle contract problems ({len(findings)} finding(s)):\n")
        grouped: dict[str, list[Finding]] = {}
        for finding in findings:
            grouped.setdefault(finding.outline, []).append(finding)
        for outline, items in grouped.items():
            print(f"{outline}:")
            for finding in items:
                print(finding.line())
            print()
        print("Fix the proposal or demote it to non-proposal idea inventory, then re-run this check.")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
