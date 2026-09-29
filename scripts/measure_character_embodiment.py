#!/usr/bin/env python3
"""Measure how much Character `look` prose expresses the embodiment axes (dream-cycle/t-030).

Reads `characters[].look` from each dated proposal's proposal-data block under
projects/dream-cycle/backlog/ and counts the same axes t-029's baseline used, split
into records dated on/before --cutoff (baseline) and after it (post-axes). Advisory;
no network. Regex families are deliberately plain, matching the original pass.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BACKLOG = Path(__file__).resolve().parents[1] / "projects" / "dream-cycle" / "backlog"
DATED = re.compile(r"^(\d{4}-\d{2}-\d{2})-.*\.md$")
BLOCK = re.compile(r"<!-- proposal-data\n(.*?)\n-->", re.S)

AXES = {
    "hair mentioned": r"\b(hair|locks|curls|braids?|braided|mane|bald|shaved|dreadlocks|ponytail|bun|beard)\b",
    "long hair": r"\blong\b[^.]{0,30}\b(hair|locks|braids?|curls|mane)\b|\b(hair|locks|braids?)\b[^.]{0,20}\bto (her|his|their) (waist|hips|knees|shoulders)\b",
    "saturated hair colour": r"\b(pink|purple|violet|teal|turquoise|magenta|crimson|scarlet|cobalt|emerald|green|blue|orange|lavender)\b[^.]{0,25}\b(hair|locks|braids?|curls|mane)\b|\b(hair|locks|braids?|curls|mane)\b[^.]{0,25}\b(pink|purple|violet|teal|turquoise|magenta|crimson|scarlet|cobalt|emerald|green|blue|orange|lavender)\b",
    "explicit age": r"\b\d{1,3}[- ]year[- ]old\b|\b(in (her|his|their) (early |mid |late )?(teens|twenties|thirties|forties|fifties|sixties|seventies|eighties)|elderly|middle-aged|teenage|teenager|aged \d+|old man|old woman|young man|young woman|child|elder)\b",
    "human skin tone": r"\b(skin|complexion)\b|\b(brown|dark|olive|pale|tawny|umber|ebony|ochre|freckled)[- ]skinned\b|\b(brown|dark|olive|pale|tawny|umber|ebony|ochre) skin\b",
    "stated affect": r"\b(smil\w+|frown\w+|grin\w+|scowl\w+|weary|wary|tired|amused|solemn|serene|anxious|calm|stern|sullen|cheerful|guarded|haunted|expression|gaze)\b",
    "she/her": r"\b(she|her|hers)\b",
    "he/him": r"\b(he|him|his)\b",
    "they/them": r"\b(they|them|their|theirs)\b",
    "coat": r"\bcoat\b",
    "patched": r"\bpatch(ed|es|work)?\b",
    "character-sheet shape": r"\b\d{1,3}-year-old\b[^.]{0,40}\b(feminine|masculine|androgynous)\b",
}


def load(cutoff: str):
    base, new = [], []
    for p in sorted(BACKLOG.iterdir()):
        m = DATED.match(p.name)
        if not m:
            continue
        b = BLOCK.search(p.read_text(encoding="utf-8"))
        if not b:
            continue
        try:
            data = json.loads(b.group(1))
        except json.JSONDecodeError:
            continue
        for ch in data.get("characters", []):
            look = (ch.get("look") or "").lower()
            if look:
                (new if m.group(1) > cutoff else base).append((p.name, look))
    return base, new


def pct(rows, rx):
    if not rows:
        return 0.0
    r = re.compile(rx)
    return 100.0 * sum(1 for _, t in rows if r.search(t)) / len(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cutoff", default="2026-09-15", help="last baseline date (inclusive)")
    ap.add_argument("--min-new", type=int, default=20, help="minimum post-cutoff characters for a verdict")
    ap.add_argument("--show", type=int, default=0, help="print N post-cutoff look excerpts")
    a = ap.parse_args()
    base, new = load(a.cutoff)
    print(f"baseline characters: {len(base)}   post-{a.cutoff} characters: {len(new)}")
    print(f"{'axis':24} {'baseline':>9} {'post':>9}")
    for name, rx in AXES.items():
        print(f"{name:24} {pct(base, rx):8.1f}% {pct(new, rx):8.1f}%")
    for n, t in new[: a.show]:
        print(f"- {n}: {t[:260]}")
    if len(new) < a.min_new:
        print(f"SAMPLE TOO SMALL: {len(new)} < {a.min_new}; no verdict (per t-030).")
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
