#!/usr/bin/env python3
"""
check_dream_outlines.py — CI preflight: is each dream backlog outline buildable?

The dream-cycle build loop (t-006) turns a `type: dream` backlog outline into real
kind_robots records following `specs/dream.md`. If an outline is missing a required
piece — no vibe, too few characters, rewards with no rarity spread, a `narrator: yes`
with no narrator block — the loop can't build it cleanly, and today that's only
caught when a build actually runs (which needs live API egress). This preflight
catches it offline, in CI, the way `check_scheduler_drift.py` guards coloring-book
cards.

Read-only, no API calls. For each buildable dream outline (`type: dream`, status
`outline`/`approved`), it checks the structure `specs/dream.md` requires and exits
non-zero with a readable per-file report if any outline is not buildable.

Both outline shapes are accepted (matched by heading keyword, not exact text):
- seed shape:  ## Location dream / ## Characters (2-4) / ## Rewards (3-6)
- daily shape: ## Locations (2) / ## Characters (3) / ## Rewards (2 — one skill…)

Requirements per outline:
  * sections present: idea, location(s), vibe/genre, characters, rewards, scenarios, narrator
  * idea / location / vibe / narrator: non-placeholder prose
  * characters: 2–5 entries
  * rewards: 2–8 entries; if ≥3, at least 2 distinct rarities (a spread)
  * scenarios: 1–3 entries
  * narrator: `narrator: yes` → a real narrator block; `narrator: no` → fine (skips cleanly)

Usage:
  python scripts/check_dream_outlines.py            # check the real backlog, exit 1 on problems
  python scripts/check_dream_outlines.py --json     # machine-readable findings
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

# (concept, heading-keyword) — first section whose heading contains the keyword.
SECTION_KEYS = [
    ("idea", "idea"),
    ("location", "location"),
    ("vibe", "vibe"),          # "Vibe / genre dream"
    ("characters", "character"),
    ("rewards", "reward"),
    ("scenarios", "scenario"),
    ("narrator", "narrator"),
]

# Ranges (inclusive) for the counted sections.
CHAR_MIN, CHAR_MAX = 2, 5
REWARD_MIN, REWARD_MAX = 2, 8
SCENARIO_MIN, SCENARIO_MAX = 1, 3


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
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def split_sections(text: str) -> dict[str, str]:
    """Map each `## Heading` to its body text (up to the next `## `)."""
    body = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
    sections: dict[str, str] = {}
    parts = re.split(r"^##\s+(.+?)\s*$", body, flags=re.MULTILINE)
    # parts[0] is preamble; then alternating (heading, body)
    for i in range(1, len(parts) - 1, 2):
        sections[parts[i].strip().lower()] = parts[i + 1]
    return sections


def find_section(sections: dict[str, str], keyword: str) -> Optional[str]:
    for heading, body in sections.items():
        if keyword in heading:
            return body
    return None


def is_placeholder(body: str) -> bool:
    stripped = body.strip()
    if len(stripped) < 15:
        return True
    # a section that is only the template's parenthetical placeholder bullet
    non_empty = [ln for ln in stripped.splitlines() if ln.strip()]
    return all(ln.strip().startswith("- (") or not ln.strip() for ln in non_empty)


def count_entries(body: str) -> int:
    """Count top-level list entries, ignoring template placeholder bullets `- (…`."""
    n = 0
    for line in body.splitlines():
        s = line.strip()
        if re.match(r"^[-*]\s+\S", s) and not s.startswith("- ("):
            # only top-level bullets (not deeper indentation)
            if not line.startswith((" ", "\t")) or line[: len(line) - len(line.lstrip())] == "":
                n += 1
    return n


def _rarities_present(body: str) -> set[str]:
    up = body.upper()
    return {r for r in RARITIES if re.search(rf"\b{r}\b", up)}


def check_outline(path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if str(fm.get("type", "")).strip() != "dream":
        return []
    status = str(fm.get("status", "")).strip().lower()
    if status not in BUILDABLE_STATUSES:
        return []  # parked/vetoed/built are not the loop's concern

    name = path.name
    findings: list[Finding] = []
    sections = split_sections(text)
    bodies: dict[str, Optional[str]] = {}
    for concept, keyword in SECTION_KEYS:
        body = find_section(sections, keyword)
        bodies[concept] = body
        if body is None:
            findings.append(Finding(name, "missing-section", f"no '{concept}' section"))

    # Prose sections must have real content.
    for concept in ("idea", "location", "vibe"):
        body = bodies.get(concept)
        if body is not None and is_placeholder(body):
            findings.append(Finding(name, "empty-section", f"'{concept}' section is empty/placeholder"))

    # Characters: 2–5 entries.
    cbody = bodies.get("characters")
    if cbody is not None:
        n = count_entries(cbody)
        if not (CHAR_MIN <= n <= CHAR_MAX):
            findings.append(Finding(name, "characters-count",
                                    f"{n} character(s); expected {CHAR_MIN}–{CHAR_MAX}"))

    # Rewards: 2–8 entries; rarity spread if ≥3.
    rbody = bodies.get("rewards")
    if rbody is not None:
        n = count_entries(rbody)
        if not (REWARD_MIN <= n <= REWARD_MAX):
            findings.append(Finding(name, "rewards-count",
                                    f"{n} reward(s); expected {REWARD_MIN}–{REWARD_MAX}"))
        rarities = _rarities_present(rbody)
        if n >= 3 and len(rarities) < 2:
            findings.append(Finding(name, "rewards-rarity",
                                    f"{n} rewards but {len(rarities)} distinct rarity tier(s); "
                                    "need a spread (≥2)"))

    # Scenarios: 1–3 entries.
    sbody = bodies.get("scenarios")
    if sbody is not None:
        n = count_entries(sbody)
        if not (SCENARIO_MIN <= n <= SCENARIO_MAX):
            findings.append(Finding(name, "scenarios-count",
                                    f"{n} scenario(s); expected {SCENARIO_MIN}–{SCENARIO_MAX}"))

    # Narrator: yes → real block; no → clean skip is fine.
    narrator_flag = str(fm.get("narrator", "")).strip().strip("'\"").lower()
    nbody = bodies.get("narrator")
    if narrator_flag in ("yes", "true"):
        if nbody is None or is_placeholder(nbody) or "narrator: no" in nbody.lower():
            findings.append(Finding(name, "narrator-missing",
                                    "narrator: yes but no real narrator block "
                                    "(name/voice/expressions)"))
    elif narrator_flag not in ("no", "false"):
        findings.append(Finding(name, "narrator-flag",
                                f"narrator frontmatter is {narrator_flag!r}; expected yes or no"))

    return findings


def collect(backlog_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(backlog_dir.glob("*.md")):
        if path.name.startswith("_") or path.name == "README.md":
            continue
        findings.extend(check_outline(path))
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--backlog-dir", type=Path, default=DEFAULT_BACKLOG,
                    help=f"dream-cycle backlog directory (default: {DEFAULT_BACKLOG})")
    ap.add_argument("--json", action="store_true", help="print findings as JSON")
    args = ap.parse_args()

    if not args.backlog_dir.exists():
        print(f"ERROR: backlog dir not found: {args.backlog_dir}", file=sys.stderr)
        return 2

    findings = collect(args.backlog_dir)

    if args.json:
        print(json.dumps([f.as_dict() for f in findings], indent=2))
    elif not findings:
        print("All dream outlines are buildable per specs/dream.md.")
    else:
        print(f"Dream outline problems ({len(findings)} finding(s)):\n")
        by_file: dict[str, list[Finding]] = {}
        for f in findings:
            by_file.setdefault(f.outline, []).append(f)
        for outline, items in by_file.items():
            print(f"{outline}:")
            for f in items:
                print(f.line())
            print()
        print("Fix: complete the outline per specs/dream.md, then re-run this check.")

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
