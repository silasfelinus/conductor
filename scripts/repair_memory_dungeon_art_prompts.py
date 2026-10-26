#!/usr/bin/env python3
"""Repair known nonliteral composition wording in Memory Dungeon's art ledgers.

Only the memory-dungeon-saturate request blocks are touched. Preserve every other
request, identifier, destination, and existing ArtJob association byte-for-byte.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGERS = (
    ROOT / "projects/art-prompts.yaml",
    ROOT / "projects/memory-dungeon/art/KNOWN-ART-REQUESTS.yaml",
)
PREFIX = "memory-dungeon-saturate-"
REPLACEMENTS = (
    ("horizontal scenic frame", "wide landscape illustration"),
    ("wide single frame", "wide environmental composition"),
    ("Square frame", "Square composition"),
    ("cinematic frame", "cinematic composition"),
    ("single-frame reveal", "one-scene reveal"),
    ("single frame", "single illustration"),
)


def repair_text(text: str) -> tuple[str, int]:
    sections = re.split(r"(?=^- id:\s)", text, flags=re.MULTILINE)
    changed = 0
    for index, section in enumerate(sections):
        if not re.match(r'^- id:\s*["\']?memory-dungeon-saturate-', section):
            continue
        revised = section
        for old, new in REPLACEMENTS:
            revised = revised.replace(old, new)
        if revised != section:
            changed += 1
            sections[index] = revised
    return "".join(sections), changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    total = 0
    for ledger in LEDGERS:
        if not ledger.is_file():
            raise SystemExit(f"Required Memory Dungeon art ledger missing: {ledger}")
        before = ledger.read_text()
        after, count = repair_text(before)
        total += count
        print(f"{ledger.relative_to(ROOT)}: {count} corrected request prompt(s)")
        if args.write and after != before:
            ledger.write_text(after)
    print(f"{total} prompts corrected; {'saved' if args.write else 'dry run'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
