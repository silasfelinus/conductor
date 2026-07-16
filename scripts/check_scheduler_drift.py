#!/usr/bin/env python3
"""
check_scheduler_drift.py — CI guard: dream-cycle scheduler cards vs. home-set reality.

A dream-cycle backlog card of `type: coloring-book` is a *scheduler card* — a
steering surface that names a home set in projects/coloring-book/sets/<slug>/ and
summarizes its state (approved-pair list, content rating, concept-pool size,
parked/active). Because that summary is hand-maintained prose, it drifts out of
sync with the home set's real files (approved/manifest.yaml, README.md) as the set
advances. Before this check, catching drift meant a manual audit pass (kaizen from
coloring-book PR #339).

This script diffs each card against its home set and exits non-zero with a readable
summary when they disagree, so drift is caught in CI rather than by eye. It is
read-only: it never edits a card or a set.

Checks (only run when both sides expose the fact — missing data is skipped, not
failed, to avoid false positives on early-stage or parked cards):
  * home_set present + folder exists (broken pointer on an active card is an error)
  * approved-pair count + names: every label in approved/manifest.yaml's
    confirmed_approvals must be named in the card, and any count the card states
    ("Three approved master pairs…") must equal the manifest's real count
  * content rating: a rating token in the card must match the home README's
    `content-rating:` line
  * concept-pool size: an "N-concept … pool" figure in the card must match the
    home README's declared pool size

Usage:
  python scripts/check_scheduler_drift.py            # check the real backlog, exit 1 on drift
  python scripts/check_scheduler_drift.py --json     # machine-readable findings
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

WORD_NUMBERS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
}

# Rating tokens, ordered so an explicit rating (PG-13/R/mature) wins over the
# broad "all-ages"/"PG" — a card that says "PG-13 … NOT all-ages" is rated PG-13.
RATING_TOKENS = ["pg-13", "pg13", "r-rated", "mature", "all-ages", "all ages", "pg"]


class Finding:
    """One card/home-set disagreement. `severity` is 'error' (broken/active) or
    'drift' (card summary stale); both fail CI, but the label aids triage."""

    def __init__(self, card: str, kind: str, detail: str, severity: str = "drift"):
        self.card = card
        self.kind = kind
        self.detail = detail
        self.severity = severity

    def as_dict(self) -> dict[str, str]:
        return {"card": self.card, "kind": self.kind, "detail": self.detail,
                "severity": self.severity}

    def line(self) -> str:
        return f"  [{self.severity}] {self.kind}: {self.detail}"


def parse_frontmatter(text: str) -> dict[str, Any]:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def body_after_frontmatter(text: str) -> str:
    m = re.match(r"^---\n.*?\n---\n(.*)$", text, re.DOTALL)
    return m.group(1) if m else text


def word_or_int(token: str) -> Optional[int]:
    token = token.strip().lower()
    if token.isdigit():
        return int(token)
    return WORD_NUMBERS.get(token)


def extract_rating(text: str) -> Optional[str]:
    """The rating token a document claims, or None. Skips negated mentions
    ("NOT all-ages") so a card can rule a rating out without being read as it."""
    low = text.lower()
    for tok in RATING_TOKENS:
        for m in re.finditer(re.escape(tok), low):
            preceding = low[max(0, m.start() - 8):m.start()]
            if re.search(r"\bnot\b[\s]+$", preceding):
                continue  # e.g. "not all-ages" — an exclusion, not the rating
            return {"pg13": "pg-13", "all ages": "all-ages"}.get(tok, tok)
    return None


def extract_pool_size(text: str) -> Optional[int]:
    m = re.search(r"(\d+)\s*-\s*concept", text, re.IGNORECASE)
    return int(m.group(1)) if m else None


def _manifest_labels(home_dir: Path) -> Optional[list[str]]:
    """Approved-pair labels from approved/manifest.yaml, or None if there's no
    manifest (a set with no approvals yet — nothing to compare)."""
    manifest = home_dir / "approved" / "manifest.yaml"
    if not manifest.exists():
        return None
    data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
    approvals = data.get("confirmed_approvals")
    if not isinstance(approvals, list):
        return []
    return [str(a.get("label")).strip() for a in approvals
            if isinstance(a, dict) and a.get("label")]


def check_approved_pairs(card: str, body: str, home_dir: Path, findings: list[Finding]) -> None:
    try:
        labels = _manifest_labels(home_dir)
    except yaml.YAMLError as exc:
        findings.append(Finding(card, "manifest-unreadable",
                                f"approved/manifest.yaml did not parse: {exc}", "error"))
        return
    if labels is None:
        return  # no approvals recorded yet
    low = body.lower()

    # A stated count ("Three approved master pairs…") must match the real count.
    m = re.search(r"([A-Za-z]+|\d+)\s+approved\s+(?:master\s+)?pairs?", body, re.IGNORECASE)
    if m:
        claimed = word_or_int(m.group(1))
        if claimed is not None and claimed != len(labels):
            findings.append(Finding(
                card, "approved-pair-count",
                f"card states {m.group(1)!r} approved pair(s); "
                f"manifest confirms {len(labels)}"))

    # Every manifest-approved pair must be named in the card (catches a new
    # approval that the card wasn't updated to reflect).
    missing = [lbl for lbl in labels if lbl.lower() not in low]
    if missing:
        findings.append(Finding(
            card, "approved-pair-names",
            f"approved pair(s) in manifest but not named in card: {', '.join(missing)}"))


def check_rating(card: str, body: str, home_dir: Path, findings: list[Finding]) -> None:
    readme = home_dir / "README.md"
    if not readme.exists():
        return
    rm = re.search(r"^content-rating:\s*(.+)$", readme.read_text(encoding="utf-8"),
                   re.MULTILINE | re.IGNORECASE)
    if not rm:
        return
    home_rating = extract_rating(rm.group(1))
    card_rating = extract_rating(body)
    if home_rating and card_rating and home_rating != card_rating:
        findings.append(Finding(
            card, "rating",
            f"card rating {card_rating!r} != home README {home_rating!r}"))


def check_pool_size(card: str, body: str, home_dir: Path, findings: list[Finding]) -> None:
    readme = home_dir / "README.md"
    if not readme.exists():
        return
    home_pool = extract_pool_size(readme.read_text(encoding="utf-8"))
    card_pool = extract_pool_size(body)
    if home_pool and card_pool and home_pool != card_pool:
        findings.append(Finding(
            card, "concept-pool",
            f"card cites {card_pool}-concept pool; home README declares {home_pool}"))


def check_card(path: Path, repo_root: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if str(fm.get("type", "")).strip() != "coloring-book":
        return []  # only coloring-book cards delegate to a home set
    card = path.name
    body = body_after_frontmatter(text)
    status = str(fm.get("status", "")).strip().lower()
    findings: list[Finding] = []

    home_set = fm.get("home_set")
    if not home_set or str(home_set).strip().lower() in ("null", "none", ""):
        if status in ("approved", "building", "built"):
            findings.append(Finding(card, "no-home-set",
                                    f"status={status!r} but no home_set is set", "error"))
        return findings

    home_dir = (repo_root / str(home_set).strip()).resolve()
    if not home_dir.exists():
        sev = "drift" if status in ("parked", "outline", "vetoed") else "error"
        findings.append(Finding(card, "home-set-missing",
                                f"home_set {home_set!r} does not exist", sev))
        return findings

    check_approved_pairs(card, body, home_dir, findings)
    check_rating(card, body, home_dir, findings)
    check_pool_size(card, body, home_dir, findings)
    return findings


def collect(backlog_dir: Path, repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(backlog_dir.glob("*.md")):
        if path.name.startswith("_") or path.name == "README.md":
            continue
        findings.extend(check_card(path, repo_root))
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--backlog-dir", type=Path, default=DEFAULT_BACKLOG,
                    help=f"dream-cycle backlog directory (default: {DEFAULT_BACKLOG})")
    ap.add_argument("--repo-root", type=Path, default=ROOT,
                    help="repo root used to resolve each card's home_set path")
    ap.add_argument("--json", action="store_true", help="print findings as JSON")
    args = ap.parse_args()

    if not args.backlog_dir.exists():
        print(f"ERROR: backlog dir not found: {args.backlog_dir}", file=sys.stderr)
        return 2

    findings = collect(args.backlog_dir, args.repo_root)

    if args.json:
        print(json.dumps([f.as_dict() for f in findings], indent=2))
    else:
        if not findings:
            print("Scheduler cards are in sync with their home sets. No drift.")
        else:
            print(f"Scheduler-card drift detected ({len(findings)} finding(s)):\n")
            by_card: dict[str, list[Finding]] = {}
            for f in findings:
                by_card.setdefault(f.card, []).append(f)
            for card, items in by_card.items():
                print(f"{card}:")
                for f in items:
                    print(f.line())
                print()
            print("Fix: update the card's summary to match its home set (or the home "
                  "set if the card is right), then re-run this check.")

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
