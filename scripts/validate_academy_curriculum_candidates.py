#!/usr/bin/env python3
"""Validate changed AI Art Academy curriculum candidates."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CANDIDATE_ROOT = Path("projects/ai-art-academy/docs/curriculum-candidates")
SENSITIVE_MARKER = "academy-cultural-context: required"
EXEMPT_MARKER = "academy-cultural-context: not-applicable"
SENSITIVE_TERMS = (
    "african diaspora",
    "black cultural",
    "harlem renaissance",
    "indigenous",
    "native american",
    "first nations",
    "mughal",
    "persian miniature",
    "japanese",
    "ukiyo-e",
    "islamic art",
    "maori",
    "aboriginal",
    "latinx",
    "chicano",
    "chicana",
)


def is_candidate(path: Path) -> bool:
    try:
        path.relative_to(CANDIDATE_ROOT)
    except ValueError:
        return False
    return path.suffix.lower() == ".md" and path.name.upper() != "README.MD"


def is_culturally_sensitive(text: str) -> bool:
    lowered = text.lower()
    if EXEMPT_MARKER in lowered:
        return False
    if SENSITIVE_MARKER in lowered:
        return True
    return any(term in lowered for term in SENSITIVE_TERMS)


def section(text: str, heading_pattern: str) -> str | None:
    match = re.search(
        rf"^##\s+(?:{heading_pattern})\s*$\n(?P<body>.*?)(?=^##\s+|\Z)",
        text,
        flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    return match.group("body").strip() if match else None


def validate_text(text: str) -> list[str]:
    if not is_culturally_sensitive(text):
        return []

    errors: list[str] = []
    artist_section = section(text, r"Artists? for historical study|Artists?|Historical artists?")
    if not artist_section or not re.search(r"Rights boundary\s*:", artist_section, re.IGNORECASE):
        errors.append("missing artist-level `Rights boundary:` guidance")

    policy_section = section(text, r"Public-domain and generation policy|Rights and generation policy")
    if not policy_section:
        errors.append("missing `## Public-domain and generation policy` section")
    else:
        required_policy_signals = (
            (r"do not include.*artist names?|exclude.*artist names?", "protected artist-name exclusion"),
            (r"item-level|specific artwork|each work", "item-level display-rights review"),
            (r"negative|do not prompt|do not reduce|avoid", "negative generation guidance"),
        )
        for pattern, label in required_policy_signals:
            if not re.search(pattern, policy_section, re.IGNORECASE | re.DOTALL):
                errors.append(f"generation policy missing {label}")

    remix_section = section(text, r"Movement-level remix configuration|Remix configuration")
    if not remix_section or "negative_guidance:" not in remix_section:
        errors.append("remix configuration missing `negative_guidance:` list")

    checklist = section(text, r"Promotion checklist")
    if not checklist:
        errors.append("missing `## Promotion checklist` section")
    else:
        checklist_signals = (
            (r"rights|reusable|license", "rights verification item"),
            (r"reviewer|representation|cultural-history", "representation review item"),
            (r"artist name|named artist", "protected artist-name item"),
        )
        for pattern, label in checklist_signals:
            if not re.search(pattern, checklist, re.IGNORECASE):
                errors.append(f"promotion checklist missing {label}")

    return errors


def validate_path(path: Path) -> list[str]:
    if not path.is_file() or not is_candidate(path):
        return []
    return validate_text(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args()

    paths = args.paths or sorted(CANDIDATE_ROOT.glob("*.md"))
    failures: list[str] = []
    checked = 0
    for path in paths:
        if not path.is_file() or not is_candidate(path):
            continue
        checked += 1
        for error in validate_path(path):
            failures.append(f"{path}: {error}")

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}", file=sys.stderr)
        return 1

    print(f"OK: {checked} changed curriculum candidate file(s) validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
