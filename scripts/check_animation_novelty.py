#!/usr/bin/env python3
"""
check_animation_novelty.py — keyword-overlap novelty check for animation-manager pitches.

Kaizen from Reviewer's t-001/t-002/t-003 review (conductor PR #494, TALKBACK 2026-07-14):
SPEC.md requires each pitch in PITCHES.yaml to self-report a `novelty` comparison against
the existing catalog, but nothing verified that claim mechanically. This compares a
pitch's `technique` and `surprise` text against every other pitch's equivalents using
simple keyword overlap (Jaccard similarity over a stopword-filtered token set) and flags
pairs above a threshold.

This is advisory, not an auto-reject: a high score means "a human or agent should look at
these two before build," not "this pitch is invalid." Two pitches can legitimately share
technique (e.g. both using Canvas particle emitters) while being visually distinct.

Read-only, no API calls, no egress.

Usage:
  python scripts/check_animation_novelty.py                  # scan all pitches, report collisions
  python scripts/check_animation_novelty.py --pitch <id>     # check one pitch against the rest
  python scripts/check_animation_novelty.py --threshold 0.3  # override the default 0.2 cutoff
  python scripts/check_animation_novelty.py --json           # machine-readable findings
  python scripts/check_animation_novelty.py --strict         # exit 1 if any collision is flagged
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PITCHES = ROOT / "projects" / "animation-manager" / "PITCHES.yaml"

DEFAULT_THRESHOLD = 0.2
MIN_TOKEN_LEN = 4

STOPWORDS = {
    "a", "an", "the", "of", "and", "or", "with", "into", "onto", "through", "across",
    "over", "under", "between", "as", "is", "are", "be", "been", "being", "that",
    "this", "these", "those", "it", "its", "their", "his", "her", "they", "them",
    "one", "two", "using", "use", "uses", "used", "rather", "than", "not", "no",
    "so", "to", "for", "on", "in", "at", "by", "from", "up", "down", "out", "about",
    "more", "most", "less", "least", "very", "just", "only", "also", "each", "every",
    "any", "all", "both", "which", "who", "whom", "where", "when", "while", "if",
    "then",
}


class Collision:
    def __init__(self, pitch_id: str, other_id: str, score: float, shared: set[str]):
        self.pitch_id = pitch_id
        self.other_id = other_id
        self.score = score
        self.shared = shared

    def as_dict(self) -> dict[str, Any]:
        return {
            "pitch": self.pitch_id,
            "collides_with": self.other_id,
            "score": round(self.score, 3),
            "shared_keywords": sorted(self.shared),
        }

    def line(self) -> str:
        keywords = ", ".join(sorted(self.shared)) or "(none)"
        return (
            f"  {self.pitch_id} ~ {self.other_id}: score={self.score:.2f} "
            f"shared=[{keywords}]"
        )


def tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z']+", (text or "").lower())
    return {w for w in words if len(w) >= MIN_TOKEN_LEN and w not in STOPWORDS}


def pitch_signature(pitch: dict[str, Any]) -> set[str]:
    return tokenize(f"{pitch.get('technique') or ''} {pitch.get('surprise') or ''}")


def jaccard(a: set[str], b: set[str]) -> tuple[float, set[str]]:
    if not a or not b:
        return 0.0, set()
    shared = a & b
    union = a | b
    return (len(shared) / len(union) if union else 0.0), shared


def load_pitches(path: Path) -> list[dict[str, Any]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    pitches = data.get("pitches") or []
    if not isinstance(pitches, list):
        raise ValueError(f"{path}: 'pitches' is not a list")
    return pitches


def find_collisions(
    pitches: list[dict[str, Any]], threshold: float, only_id: str | None = None
) -> list[Collision]:
    signatures = {p["id"]: pitch_signature(p) for p in pitches}
    ids = [p["id"] for p in pitches]
    collisions: list[Collision] = []
    for i, a_id in enumerate(ids):
        if only_id is not None and a_id != only_id:
            continue
        for b_id in ids[i + 1 :]:
            score, shared = jaccard(signatures[a_id], signatures[b_id])
            if score >= threshold:
                collisions.append(Collision(a_id, b_id, score, shared))
    collisions.sort(key=lambda c: c.score, reverse=True)
    return collisions


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pitches", type=Path, default=DEFAULT_PITCHES,
                         help="Path to PITCHES.yaml (default: animation-manager's)")
    parser.add_argument("--pitch", default=None,
                         help="Only check this pitch id against every other pitch")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                         help=f"Jaccard similarity cutoff to flag (default {DEFAULT_THRESHOLD})")
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    parser.add_argument("--strict", action="store_true",
                         help="Exit 1 if any collision is flagged (default: advisory, exit 0)")
    args = parser.parse_args(argv)

    pitches = load_pitches(args.pitches)

    if args.pitch is not None and args.pitch not in {p["id"] for p in pitches}:
        print(f"error: no pitch with id {args.pitch!r} in {args.pitches}", file=sys.stderr)
        return 2

    collisions = find_collisions(pitches, args.threshold, only_id=args.pitch)

    if args.json:
        print(json.dumps([c.as_dict() for c in collisions], indent=2))
    elif collisions:
        print(f"Novelty check: {len(collisions)} pair(s) at or above threshold {args.threshold}:")
        for c in collisions:
            print(c.line())
        print("Advisory only — review flagged pairs for genuine visual/mechanical overlap "
              "before build; a shared technique alone is not disqualifying.")
    else:
        scope = f"pitch {args.pitch!r}" if args.pitch else f"all {len(pitches)} pitches"
        print(f"Novelty check: no collisions at or above threshold {args.threshold} ({scope}).")

    if args.strict and collisions:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
