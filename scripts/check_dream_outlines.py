#!/usr/bin/env python3
"""Offline buildability checks for dream-cycle backlog outlines.

Legacy/manual outlines follow specs/dream.md's multi-character shape. Daily proposals
with ``proposal-data.seed_facets.version >= 2`` follow the deterministic six-asset
contract: one vibe, one location, one character, one item, one skill, and one scenario.
"""

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
RARITIES = {"COMMON", "UNCOMMON", "RARE", "EPIC", "LEGENDARY", "MYTHIC"}
BUILDABLE_STATUSES = {"outline", "approved"}
SEED_CONTRACT_DATE = "2026-07-25"

SECTION_KEYS = [
    ("idea", "idea"),
    ("location", "location"),
    ("vibe", "vibe"),
    ("characters", "character"),
    ("rewards", "reward"),
    ("scenarios", "scenario"),
]


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


def is_placeholder(body: str) -> bool:
    stripped = body.strip()
    if len(stripped) < 15:
        return True
    lines = [line.strip() for line in stripped.splitlines() if line.strip()]
    return bool(lines) and all(line.startswith("- (") for line in lines)


def count_entries(body: str) -> int:
    return sum(
        1
        for line in body.splitlines()
        if re.match(r"^[-*]\s+\S", line) and not line.startswith("- (")
    )


def _rarities_present(body: str) -> set[str]:
    upper = body.upper()
    return {rarity for rarity in RARITIES if re.search(rf"\b{rarity}\b", upper)}


def _seed_contract_applies(frontmatter: dict[str, Any]) -> bool:
    raw = frontmatter.get("proposal_date") or frontmatter.get("created")
    return bool(raw and str(raw) >= SEED_CONTRACT_DATE)


def _labeled_value(body: str, *labels: str) -> Optional[str]:
    for label in labels:
        match = re.search(
            rf"^[-*]\s+\*\*{re.escape(label)}:\*\*\s*(.+?)\s*$",
            body,
            re.IGNORECASE | re.MULTILINE,
        )
        if match:
            return match.group(1).strip()
    return None


def _check_creative_seeds(name: str, sections: dict[str, str]) -> list[Finding]:
    body = find_section(sections, "creative seed")
    if body is None or is_placeholder(body):
        return [Finding(name, "seed-missing", "no complete 'Creative seeds' section (genres, occupation, animal/species, fusion)")]

    findings: list[Finding] = []
    genres = _labeled_value(body, "Genres", "Genre")
    if not genres:
        findings.append(Finding(name, "seed-genres", "missing Genres value"))
    else:
        parts = [part for part in re.split(r"\s*(?:\+|,)\s*", genres) if part.strip()]
        if not 1 <= len(parts) <= 2:
            findings.append(Finding(name, "seed-genres", f"{len(parts)} genre seed(s); expected 1–2"))
    if not _labeled_value(body, "Occupation"):
        findings.append(Finding(name, "seed-occupation", "missing Occupation value"))
    if not _labeled_value(body, "Animal / species", "Animal/species", "Species"):
        findings.append(Finding(name, "seed-species", "missing Animal / species value"))
    fusion = _labeled_value(body, "Fusion")
    if not fusion or len(fusion) < 25:
        findings.append(Finding(name, "seed-fusion", "Fusion must explain concrete consequences of all three seeds"))
    return findings


def _is_six_asset_proposal(data: Optional[dict[str, Any]]) -> bool:
    facets = (data or {}).get("seed_facets")
    return isinstance(facets, dict) and int(facets.get("version") or 0) >= 2


def _check_six_asset(name: str, data: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []

    def require_count(field: str, expected: int) -> list[Any]:
        value = data.get(field)
        items = value if isinstance(value, list) else []
        if len(items) != expected:
            findings.append(Finding(name, f"six-asset-{field}", f"{len(items)} {field}; expected exactly {expected}"))
        return items

    vibe = data.get("vibe")
    if not isinstance(vibe, dict) or not vibe.get("title") or not vibe.get("line"):
        findings.append(Finding(name, "six-asset-vibe", "missing complete vibe"))
    require_count("locations", 1)
    require_count("characters", 1)
    rewards = require_count("rewards", 2)
    reward_types = {str(item.get("reward_type", "")).upper() for item in rewards if isinstance(item, dict)}
    if reward_types != {"ITEM", "SKILL"}:
        findings.append(Finding(name, "six-asset-rewards", "rewards must contain exactly one ITEM and one SKILL"))
    require_count("scenarios", 1)

    facets = data.get("seed_facets")
    elements = facets.get("elements") if isinstance(facets, dict) else None
    expected = {"vibe", "location", "character", "reward_item", "reward_skill", "scenario"}
    if not isinstance(elements, dict) or not expected.issubset(elements):
        findings.append(Finding(name, "seed-facets", "seed_facets.elements must cover all six assets"))
    return findings


def check_outline(path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)
    if str(frontmatter.get("type", "")).strip() != "dream":
        return []
    if str(frontmatter.get("status", "")).strip().lower() not in BUILDABLE_STATUSES:
        return []

    name = path.name
    data = parse_data_block(text, "proposal-data")
    if _is_six_asset_proposal(data):
        return _check_six_asset(name, data or {})

    findings: list[Finding] = []
    sections = split_sections(text)
    bodies: dict[str, Optional[str]] = {}
    for concept, keyword in SECTION_KEYS:
        body = find_section(sections, keyword)
        bodies[concept] = body
        if body is None:
            findings.append(Finding(name, "missing-section", f"no '{concept}' section"))

    narrator_flag = str(frontmatter.get("narrator", "")).strip().strip("'\"").lower()
    narrator_body = find_section(sections, "narrator")
    if narrator_flag in ("yes", "true") and narrator_body is None:
        findings.append(Finding(name, "missing-section", "no 'narrator' section"))

    if _seed_contract_applies(frontmatter):
        findings.extend(_check_creative_seeds(name, sections))

    for concept in ("idea", "location", "vibe"):
        body = bodies.get(concept)
        if body is not None and is_placeholder(body):
            findings.append(Finding(name, "empty-section", f"'{concept}' section is empty/placeholder"))

    characters = bodies.get("characters")
    if characters is not None:
        count = count_entries(characters)
        if not 2 <= count <= 5:
            findings.append(Finding(name, "characters-count", f"{count} character(s); expected 2–5"))

    rewards = bodies.get("rewards")
    if rewards is not None:
        count = count_entries(rewards)
        if not 2 <= count <= 8:
            findings.append(Finding(name, "rewards-count", f"{count} reward(s); expected 2–8"))
        if count >= 3 and len(_rarities_present(rewards)) < 2:
            findings.append(Finding(name, "rewards-rarity", f"{count} rewards but fewer than 2 distinct rarity tiers"))

    scenarios = bodies.get("scenarios")
    if scenarios is not None:
        count = count_entries(scenarios)
        if not 1 <= count <= 3:
            findings.append(Finding(name, "scenarios-count", f"{count} scenario(s); expected 1–3"))

    if narrator_flag in ("yes", "true"):
        if narrator_body is None or is_placeholder(narrator_body) or "narrator: no" in narrator_body.lower():
            findings.append(Finding(name, "narrator-missing", "narrator: yes but no real narrator block"))
    elif narrator_flag not in ("no", "false"):
        findings.append(Finding(name, "narrator-flag", f"narrator frontmatter is {narrator_flag!r}; expected yes or no"))
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
        print("All dream outlines are buildable per specs/dream.md.")
    else:
        print(f"Dream outline problems ({len(findings)} finding(s)):\n")
        grouped: dict[str, list[Finding]] = {}
        for finding in findings:
            grouped.setdefault(finding.outline, []).append(finding)
        for outline, items in grouped.items():
            print(f"{outline}:")
            for finding in items:
                print(finding.line())
            print()
        print("Fix: complete the outline per specs/dream.md, then re-run this check.")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
