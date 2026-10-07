"""zuzu-showdown t-018: check matchups.yaml is complete and every line fits the rules.

    python projects/zuzu-showdown/tools/check_matchups.py

Every unordered pair of the roster and every mirror has one entry (36). Each entry has a 2-3 line intro
spoken by its two fighters, and a win quote for each fighter in it (64 in all, counting mirrors once).
The boss has an intro line for every fighter. Every line is under 60 characters (two pixel-font lines at
480 px) and uses no banned term (VIDEO-GUARDRAILS.md). Zuzu says silence or at most three words; the
croc only makes sounds or *actions*. Exits 1 on any failure, listing them all.
"""

from __future__ import annotations

import re
import sys
from itertools import combinations_with_replacement
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent.parent
MAX_CHARS = 60
BANNED = ["human", "humans", "humanity", "mankind", "people", "pharmacy", "great wall", "skyscraper",
          "highway", "billboard", "road sign", "english lettering"]
CROC_SOUND = re.compile(r"^(?:\*[^*]+\*|[HSRGhsrg.!]+|\s)+$")


def check(matchups: dict, roster: list[str]) -> list[str]:
    errors: list[str] = []
    lines: list[tuple[str, str]] = []
    seen: dict[tuple[str, str], int] = {}
    for entry in matchups.get("matchups", []):
        pair = tuple(sorted(entry["pair"], key=roster.index))
        seen[pair] = seen.get(pair, 0) + 1
        for slug in pair:
            if slug not in roster:
                errors.append(f"{pair}: {slug} is not on the roster")
        intro = entry.get("intro") or []
        if not 2 <= len(intro) <= 3:
            errors.append(f"{pair}: intro has {len(intro)} lines (2-3)")
        for turn in intro:
            if turn["speaker"] not in pair:
                errors.append(f"{pair}: {turn['speaker']} speaks in someone else's intro")
            lines.append((turn["speaker"], turn["line"]))
        win = entry.get("win") or {}
        if sorted(win) != sorted(dict.fromkeys(pair)):
            errors.append(f"{pair}: win quotes for {sorted(win)}, expected {sorted(dict.fromkeys(pair))}")
        lines.extend(win.items())
    for pair in combinations_with_replacement(roster, 2):
        count = seen.get(pair, 0)
        if count != 1:
            errors.append(f"{pair}: {count} entries (expected 1)")
    boss = (matchups.get("boss") or {}).get("intro") or {}
    for slug in roster:
        if slug not in boss:
            errors.append(f"boss: no intro line for {slug}")
    lines.extend(boss.items())
    for speaker, line in lines:
        if len(line) >= MAX_CHARS:
            errors.append(f"{speaker}: {len(line)} chars: {line!r}")
        low = line.lower()
        for term in BANNED:
            if re.search(rf"\b{re.escape(term)}\b", low):
                errors.append(f"{speaker}: banned term {term!r}: {line!r}")
        if speaker == "zuzu" and line.strip(" .!?") and len(line.replace("...", " ").split()) > 3:
            errors.append(f"zuzu says more than three words: {line!r}")
        if speaker == "river-croc" and not CROC_SOUND.match(line):
            errors.append(f"river-croc speaks words: {line!r}")
    return errors


def main() -> int:
    roster = [f["slug"] for f in yaml.safe_load((HERE / "fighters.yaml").read_text())["fighters"]]
    matchups = yaml.safe_load((HERE / "matchups.yaml").read_text())
    errors = check(matchups, roster)
    entries = len(matchups.get("matchups", []))
    quotes = sum(len(e.get("win") or {}) for e in matchups.get("matchups", []))
    if errors:
        print(f"matchups.yaml: {len(errors)} problem(s)")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"matchups.yaml OK: {entries} matchups, {quotes} win quotes, {len(roster)} boss intros")
    return 0


if __name__ == "__main__":
    sys.exit(main())
