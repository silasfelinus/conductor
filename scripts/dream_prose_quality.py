#!/usr/bin/env python3
"""User-facing prose quality guardrails for Daily Dream authoring and revisions.

The canonical proposal schema intentionally stores several pieces of card copy in
small structured fields. Structural validation only proves those fields exist; it
does not prove that a person will see a readable sentence when a UI renders one
of them directly. Keep this policy separate from the historical schema so older
already-authored proposals remain buildable while every new author/revision path
can reject telegraphic copy.
"""
from __future__ import annotations

import re
from typing import Any


def _word_count(value: str) -> int:
    return len(re.findall(r"\b[\w’'-]+\b", value, flags=re.UNICODE))


def _first_letter(value: str) -> str:
    return next((char for char in value if char.isalpha()), "")


def _check(label: str, value: Any, minimum_words: int) -> list[str]:
    if not isinstance(value, str) or not value.strip():
        return []  # structural validation owns missing-field errors

    text = value.strip()
    problems: list[str] = []
    words = _word_count(text)
    if words < minimum_words:
        problems.append(
            f"{label} is too terse ({words} words; need at least {minimum_words}) and must explain itself as card copy"
        )

    first = _first_letter(text)
    if first and not first.isupper():
        problems.append(f"{label} must begin as a properly capitalized sentence")

    if not re.search(r"[.!?][\"'”’)]*$", text):
        problems.append(f"{label} must end with sentence punctuation")
    return problems


def complaints(proposal: Any) -> list[str]:
    """Return human-readable complaints for prose that is too fragmentary for UI cards."""
    if not isinstance(proposal, dict):
        return []

    vibe = proposal.get("vibe") if isinstance(proposal.get("vibe"), dict) else {}
    locations = proposal.get("locations") if isinstance(proposal.get("locations"), list) else []
    location = locations[0] if locations and isinstance(locations[0], dict) else {}
    scenarios = proposal.get("scenarios") if isinstance(proposal.get("scenarios"), list) else []
    scenario = scenarios[0] if scenarios and isinstance(scenarios[0], dict) else {}

    checks = (
        ("idea", proposal.get("idea"), 14),
        ("vibe.line", vibe.get("line"), 8),
        ("locations[0].known_for", location.get("known_for"), 10),
        ("locations[0].local_rule", location.get("local_rule"), 8),
        ("locations[0].best_scene", location.get("best_scene"), 10),
        ("scenarios[0].setup", scenario.get("setup"), 14),
    )
    problems: list[str] = []
    for label, value, minimum_words in checks:
        problems.extend(_check(label, value, minimum_words))
    return problems
