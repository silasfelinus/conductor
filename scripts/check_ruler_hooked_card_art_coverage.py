#!/usr/bin/env python3
"""Guard the art-request ledger for authored Ruler Hooked quest cards.

The card IDs live in kind_robots. Painting requests live in Conductor.
This deliberately checks request coverage, not job delivery or visual quality:
a pending request satisfies the guard but is still NOT a finished asset.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

CARD_ID = re.compile(r"^ {10}id: '([a-z0-9-]+)',?\s*$", re.MULTILINE)
CARD_ART = re.compile(r"^ {10}art: '([^']+)',?\s*$", re.MULTILINE)


def card_art_contract(source: str) -> tuple[set[str], list[str]]:
    """Read only card-level IDs, not nested choice, arc or deck IDs."""
    source = source.split("\n  endings: [", 1)[0]
    matches = list(CARD_ID.finditer(source))
    errors: list[str] = []
    cards: set[str] = set()
    for index, match in enumerate(matches):
        card_id = match.group(1)
        if card_id in cards:
            errors.append(f"duplicate quest card ID: {card_id}")
        cards.add(card_id)
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        chunk = source[match.end() : end].split("choices: [", 1)[0]
        found = CARD_ART.search(chunk)
        expected = f"card-{card_id}"
        if found is None or found.group(1) != expected:
            errors.append(f"{card_id}: art key must be {expected}")
    if not cards:
        errors.append("no card-level IDs found; check content.ts format")
    return cards, errors


def request_coverage(cards: set[str], ledger: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(ledger, dict) or not isinstance(ledger.get("requests"), list):
        return ["art-prompts.yaml has no requests list"]
    requests = ledger["requests"]
    by_id: dict[str, list[dict]] = {}
    for row in requests:
        if not isinstance(row, dict):
            continue
        key = row.get("id")
        if isinstance(key, str) and key.startswith("ruler-hooked-card-"):
            by_id.setdefault(key, []).append(row)

    for card_id in sorted(cards):
        key = f"ruler-hooked-card-{card_id}"
        matching = by_id.get(key, [])
        if not matching:
            errors.append(f"{card_id}: missing art request {key}")
            continue
        if len(matching) > 1:
            errors.append(f"{card_id}: duplicate art request {key}")
        expected_path = f"public/images/ruler-hooked/card-{card_id}.webp"
        for row in matching:
            if row.get("image_path") != expected_path:
                errors.append(
                    f"{card_id}: expected image_path {expected_path}, got {row.get('image_path')}"
                )
            if row.get("target_repo") != "silasfelinus/kind_robots":
                errors.append(f"{card_id}: request target_repo must be kind_robots")
    return errors


def validate(content_path: Path, queue_path: Path) -> tuple[int, list[str]]:
    cards, errors = card_art_contract(content_path.read_text(encoding="utf-8"))
    ledger = yaml.safe_load(queue_path.read_text(encoding="utf-8"))
    errors.extend(request_coverage(cards, ledger))
    return len(cards), errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content", type=Path, required=True)
    parser.add_argument("--queue", type=Path, required=True)
    args = parser.parse_args()
    card_count, errors = validate(args.content, args.queue)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"FAIL: {len(errors)} ruler-hooked card/art coverage errors")
        return 1
    print(f"OK: {card_count} ruler-hooked quest cards have matching art requests")
    print("NOTE: pending ledger requests are not rendered/verified paintings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
