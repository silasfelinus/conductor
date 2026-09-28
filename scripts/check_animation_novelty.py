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

By default this is read-only with no API calls or egress, exactly as before. Kaizen from
t-007's 2026-09-28 cycle (animation-manager t-024): PITCHES.yaml-only comparison could not
catch kaleidoscope-bloom colliding with the already-shipped, pre-pitch-pipeline
kaleidoscope-effect.vue catalog entry, because that entry never went through PITCHES.yaml
at all. `--check-catalog` opts into an additional, explicit-only comparison against
kind_robots' stores/animationCatalog.ts (fetched via the GitHub Contents API, same pattern
as check_vendored_scanner_parity.py) so a pitch can also collide-check against everything
already shipped, not only against other pitches.

Usage:
  python scripts/check_animation_novelty.py                  # scan all pitches, report collisions
  python scripts/check_animation_novelty.py --pitch <id>     # check one pitch against the rest
  python scripts/check_animation_novelty.py --threshold 0.3  # override the default 0.2 cutoff
  python scripts/check_animation_novelty.py --json           # machine-readable findings
  python scripts/check_animation_novelty.py --strict         # exit 1 if any collision is flagged
  python scripts/check_animation_novelty.py --check-catalog  # also diff against the shipped catalog

Exit codes (only when --check-catalog is passed):
  0 = fetched the catalog cleanly (collisions, if any, are still advisory)
  2 = could not fetch the catalog (missing GITHUB_TOKEN/GH_TOKEN, or a network/API failure) --
      unresolved, not "no collisions", same convention as check_vendored_scanner_parity.py
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PITCHES = ROOT / "projects" / "animation-manager" / "PITCHES.yaml"

DEFAULT_THRESHOLD = 0.2
MIN_TOKEN_LEN = 4

KIND_ROBOTS_REPO = "silasfelinus/kind_robots"
CATALOG_PATH = "stores/animationCatalog.ts"
DEFAULT_CATALOG_REF = "main"

CATALOG_ARRAY_START_RE = re.compile(r"ANIMATION_EFFECTS\s*=\s*\[")
CATALOG_FIELD_RE_TEMPLATE = r"{field}:\s*(['\"])(.*?)(?<!\\)\1"

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


def catalog_pitch_signature(pitch: dict[str, Any]) -> set[str]:
    """Signature used only for the pitch-vs-shipped-catalog comparison.

    Deliberately built from `title` + `novelty` rather than `pitch_signature`'s
    `technique` + `surprise`: a pitch's own novelty writeup is where it names
    the concept it believes is new (and, per the catalog spec, a title like
    kind_robots' "Kaleidoscope" catalog label commonly recurs in a colliding
    pitch's own title even when its technique/surprise prose never uses the
    word at all -- kaleidoscope-bloom's own technique/surprise section never
    says "kaleidoscope", which is exactly why the t-024 incident this
    comparison exists for slipped past `pitch_signature`/`find_collisions`).
    """
    return tokenize(f"{pitch.get('title') or ''} {pitch.get('novelty') or ''}")


def jaccard(a: set[str], b: set[str]) -> tuple[float, set[str]]:
    if not a or not b:
        return 0.0, set()
    shared = a & b
    union = a | b
    return (len(shared) / len(union) if union else 0.0), shared


def overlap_coefficient(a: set[str], b: set[str]) -> tuple[float, set[str]]:
    """Szymkiewicz-Simpson overlap coefficient: |A∩B| / min(|A|, |B|).

    Used for the pitch-vs-catalog comparison instead of `jaccard()` because the
    two sides are wildly different sizes -- a catalog tooltip is a handful of
    words, a pitch's title+novelty text can be dozens. Jaccard's union-sized
    denominator makes even an exact-word hit (e.g. both sides literally saying
    "kaleidoscope") score near zero once the longer side dilutes the union,
    which is exactly why the kaleidoscope-bloom/kaleidoscope-effect collision
    this check exists to catch would otherwise go unflagged. Overlap
    coefficient instead asks "how much of the *smaller* (catalog) side's
    vocabulary shows up in the pitch," which stays meaningful regardless of
    how long the pitch's own novelty prose runs.
    """
    if not a or not b:
        return 0.0, set()
    shared = a & b
    return (len(shared) / min(len(a), len(b))), shared


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


def github_token() -> str | None:
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


def fetch_kind_robots_catalog_source(ref: str, token: str | None) -> tuple[str | None, str | None]:
    """(source_text, error). error is None on success."""
    url = (
        f"https://api.github.com/repos/{KIND_ROBOTS_REPO}/contents/{CATALOG_PATH}"
        f"?ref={urllib.parse.quote(ref)}"
    )
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "conductor-check-animation-novelty/1.0",
    }
    if token:
        headers["Authorization"] = f"token {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        return None, f"HTTP {exc.code} fetching {CATALOG_PATH}"
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return None, f"network error fetching {CATALOG_PATH}: {exc}"

    encoding = body.get("encoding")
    content = body.get("content")
    if encoding != "base64" or content is None:
        return None, f"unexpected contents API response shape for {CATALOG_PATH}"
    try:
        return base64.b64decode(content).decode("utf-8"), None
    except (ValueError, TypeError, UnicodeDecodeError) as exc:
        return None, f"failed to decode content for {CATALOG_PATH}: {exc}"


def _split_top_level_objects(array_body: str) -> list[str]:
    """Split a `[ {...}, {...}, ... ]` array body into each `{...}` object's
    own source text, tracking brace depth so a value that itself contains
    braces (none do today, but nothing guarantees that stays true) can never
    split an object in half."""
    blocks: list[str] = []
    depth = 0
    buf: list[str] = []
    for ch in array_body:
        if ch == "{":
            depth += 1
        if depth > 0:
            buf.append(ch)
        if ch == "}":
            depth -= 1
            if depth == 0:
                blocks.append("".join(buf))
                buf = []
    return blocks


def _extract_field(block: str, field: str) -> str | None:
    match = re.search(CATALOG_FIELD_RE_TEMPLATE.format(field=re.escape(field)), block, re.DOTALL)
    return match.group(2) if match else None


def parse_catalog_entries(source: str) -> list[dict[str, str]]:
    """Parse kind_robots' stores/animationCatalog.ts ANIMATION_EFFECTS array into
    [{id, label, tooltip}, ...]. This is a small hand-rolled TS-object-literal
    reader, not a general JS parser -- it only needs to survive this one file's
    shape (a flat array of flat object literals with quoted string values)."""
    match = CATALOG_ARRAY_START_RE.search(source)
    if not match:
        raise ValueError("could not find 'ANIMATION_EFFECTS = [' in catalog source")
    array_body = source[match.end():]
    entries: list[dict[str, str]] = []
    for block in _split_top_level_objects(array_body):
        entry_id = _extract_field(block, "id")
        if not entry_id:
            continue
        entries.append({
            "id": entry_id,
            "label": _extract_field(block, "label") or "",
            "tooltip": _extract_field(block, "tooltip") or "",
        })
    return entries


def catalog_signature(entry: dict[str, str]) -> set[str]:
    return tokenize(f"{entry.get('label') or ''} {entry.get('tooltip') or ''}")


def find_catalog_collisions(
    pitches: list[dict[str, Any]],
    catalog_entries: list[dict[str, str]],
    threshold: float,
    only_id: str | None = None,
) -> list[Collision]:
    pitch_signatures = {p["id"]: catalog_pitch_signature(p) for p in pitches}
    catalog_signatures = {e["id"]: catalog_signature(e) for e in catalog_entries}
    collisions: list[Collision] = []
    for pitch_id, sig in pitch_signatures.items():
        if only_id is not None and pitch_id != only_id:
            continue
        for entry_id, entry_sig in catalog_signatures.items():
            score, shared = overlap_coefficient(sig, entry_sig)
            if score >= threshold:
                collisions.append(Collision(pitch_id, f"catalog:{entry_id}", score, shared))
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
    parser.add_argument("--check-catalog", action="store_true",
                         help="Also diff pitches against kind_robots' shipped animation catalog "
                              "(requires GITHUB_TOKEN/GH_TOKEN; opt-in, not part of the default "
                              "zero-egress check)")
    parser.add_argument("--catalog-ref", default=DEFAULT_CATALOG_REF,
                         help=f"kind_robots ref to read the catalog from (default {DEFAULT_CATALOG_REF!r})")
    args = parser.parse_args(argv)

    pitches = load_pitches(args.pitches)

    if args.pitch is not None and args.pitch not in {p["id"] for p in pitches}:
        print(f"error: no pitch with id {args.pitch!r} in {args.pitches}", file=sys.stderr)
        return 2

    collisions = find_collisions(pitches, args.threshold, only_id=args.pitch)
    catalog_collisions: list[Collision] = []
    catalog_error: str | None = None

    if args.check_catalog:
        token = github_token()
        if not token:
            catalog_error = (
                "GITHUB_TOKEN/GH_TOKEN not set -- cannot read kind_robots' "
                f"{CATALOG_PATH} (kind_robots is a private repo)"
            )
        else:
            source, fetch_error = fetch_kind_robots_catalog_source(args.catalog_ref, token)
            if fetch_error:
                catalog_error = fetch_error
            else:
                try:
                    catalog_entries = parse_catalog_entries(source or "")
                except ValueError as exc:
                    catalog_error = str(exc)
                else:
                    catalog_collisions = find_catalog_collisions(
                        pitches, catalog_entries, args.threshold, only_id=args.pitch
                    )

    if args.json:
        if args.check_catalog:
            output: Any = {
                "pitch_collisions": [c.as_dict() for c in collisions],
                "catalog_collisions": [c.as_dict() for c in catalog_collisions],
                "catalog_error": catalog_error,
            }
        else:
            # Unchanged shape from before --check-catalog existed: a plain list.
            output = [c.as_dict() for c in collisions]
        print(json.dumps(output, indent=2))
    else:
        if collisions:
            print(f"Novelty check: {len(collisions)} pair(s) at or above threshold {args.threshold}:")
            for c in collisions:
                print(c.line())
            print("Advisory only — review flagged pairs for genuine visual/mechanical overlap "
                  "before build; a shared technique alone is not disqualifying.")
        else:
            scope = f"pitch {args.pitch!r}" if args.pitch else f"all {len(pitches)} pitches"
            print(f"Novelty check: no collisions at or above threshold {args.threshold} ({scope}).")

        if args.check_catalog:
            if catalog_error:
                print(f"Catalog check: could not verify -- {catalog_error}", file=sys.stderr)
            elif catalog_collisions:
                print(f"Catalog check: {len(catalog_collisions)} pitch/catalog collision(s) "
                      f"at or above threshold {args.threshold}:")
                for c in catalog_collisions:
                    print(c.line())
                print("Advisory only — a shared concept under a different technique is not "
                      "automatically disqualifying, but review before build.")
            else:
                print("Catalog check: no collisions against the shipped catalog.")

    if args.check_catalog and catalog_error:
        return 2
    if args.strict and (collisions or catalog_collisions):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
