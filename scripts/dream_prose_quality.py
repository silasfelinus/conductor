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


# Phrases that mean a field is restating a label printed right next to it,
# producing "Best scene: The best scene is ...". Keyed by the field's bare name
# and checked only against the opening of the value, so a later legitimate use of
# the same words is not flagged.
#
# Only fields that actually appear beside a label are listed. `known_for`,
# `local_rule` and `best_scene` are PitchSheet highlight values under "Known For"
# / "Local Rule" / "Best Scene"; `best_used_when` and `catch` follow explicit
# stems in the proposal markdown. Deliberately absent: `grants` ("It grants ..."
# is ordinary English, not an echo) and `carries`, whose only user-facing home is
# the unlabelled Character backstory, where "She carries a coil of rope" is
# exactly right — the redundancy there was the markdown template's "Carries:"
# label, which was removed rather than rewriting 28 bundles of good prose.
LABEL_ECHOES = {
    "known_for": ("known for",),
    "local_rule": ("local rule", "the rule here is", "the rule is"),
    "best_scene": ("best scene",),
    "complication": ("the complication is",),
    "best_used_when": ("best used when", "used when"),
    "catch": ("the catch is",),
}
ECHO_WINDOW_WORDS = 8

# `best_used_when` names a SITUATION; the card prints "Best used when:" in front
# of it. Any "<verb> it when ..." opening therefore stutters, not just the
# literal "use it when" this list originally spelled out -- the catalog was full
# of "Reach for it when", "Call on it when" and "Rely on it when", which the
# phrase list sailed past. Matching the construction instead of the phrasing is
# the difference between fixing an instance and fixing the class.
ECHO_PATTERNS = {
    "best_used_when": re.compile(
        r"^(?!it\b)\w+(?:\s+(?:on|for|to|upon))?\s+it\s+(?:when|once|if|the moment)\b",
        re.IGNORECASE,
    ),
}

# "It grants the ability to infer ..." is three words of scaffolding in front of
# the verb that matters. "It infers ..." says the same thing and reads better.
PADDING_PATTERN = re.compile(
    r"\b(?:grants|gives|confers|provides|bestows)\s+(?:the\s+|an?\s+)?"
    r"(?:ability|power|capacity|means|option)\s+to\b",
    re.IGNORECASE,
)

# The digest renders vibe.line and idea back to back in the vibe row, so an idea
# that opens by restating the line reads as immediate self-repetition:
# "The whole town's work is keeping one enormous thing asleep. A coastal town's
# whole economy is keeping one enormous sleeping thing asleep, and ..."
# Measured over the idea's opening only; a later callback is fine. Observed
# separation is wide -- offending bundles score 0.60-0.86, sound ones 0.00-0.12.
VIBE_ECHO_THRESHOLD = 0.5


def _significant_words(value: str) -> set[str]:
    return set(re.findall(r"[a-z]{4,}", value.lower()))


def _label_echo(label: str, value: Any) -> list[str]:
    """Flag copy whose opening restates its own field label."""
    if not isinstance(value, str) or not value.strip():
        return []
    field = label.rsplit(".", 1)[-1]
    pattern = ECHO_PATTERNS.get(field)
    if pattern is not None and pattern.match(value.strip()):
        return [
            f"{label} is written as an instruction to the reader rather than the "
            "situation the label names; drop the '<verb> it when' opening and state "
            "the circumstance on its own"
        ]
    opening = " ".join(re.findall(r"[\w’'-]+", value.casefold())[:ECHO_WINDOW_WORDS])
    for phrase in LABEL_ECHOES.get(field, ()):
        if phrase in opening:
            return [
                f"{label} restates its own label ({phrase!r}); the card already prints "
                "it, so write the value as a sentence that stands without the label"
            ]
    return []


def _padding(label: str, value: Any) -> list[str]:
    if isinstance(value, str) and PADDING_PATTERN.search(value):
        return [
            f"{label} pads the verb that matters behind 'grants the ability to'; "
            "say what it does directly"
        ]
    return []


def _vibe_echo(proposal: dict) -> list[str]:
    """Flag an idea whose opening restates the vibe line it is rendered beside."""
    line = str((proposal.get("vibe") or {}).get("line") or "").strip()
    idea = str(proposal.get("idea") or "").strip()
    if not line or not idea:
        return []
    line_words = _significant_words(line)
    if not line_words:
        return []
    opening = " ".join(idea.split()[: len(line.split()) + 4])
    shared = line_words & _significant_words(opening)
    if len(shared) / len(line_words) < VIBE_ECHO_THRESHOLD:
        return []
    return [
        "idea opens by restating vibe.line, which the digest prints immediately "
        f"above it ({', '.join(sorted(shared)[:5])}); let the idea carry the concrete "
        "premise the line only gestures at"
    ]


def _first_mapping(value: Any) -> dict:
    if not isinstance(value, list):
        return {}
    return next((row for row in value if isinstance(row, dict)), {})


def _reward_of_type(proposal: Any, wanted: str) -> dict:
    rewards = proposal.get("rewards") if isinstance(proposal.get("rewards"), list) else []
    for row in rewards:
        if isinstance(row, dict) and str(row.get("reward_type") or "").upper() == wanted:
            return row
    return {}


def complaints(proposal: Any) -> list[str]:
    """Return human-readable complaints for prose that is too fragmentary for UI cards."""
    if not isinstance(proposal, dict):
        return []

    vibe = proposal.get("vibe") if isinstance(proposal.get("vibe"), dict) else {}
    location = _first_mapping(proposal.get("locations"))
    character = _first_mapping(proposal.get("characters"))
    scenario = _first_mapping(proposal.get("scenarios"))
    item = _reward_of_type(proposal, "ITEM")
    skill = _reward_of_type(proposal, "SKILL")

    # `look` and `art_direction` are deliberately excluded: they are Krea prompt
    # material, not card copy, and are supposed to read as visual noun phrases.
    checks = [
        ("idea", proposal.get("idea"), 14),
        ("vibe.line", vibe.get("line"), 8),
        ("locations[0].known_for", location.get("known_for"), 10),
        ("locations[0].local_rule", location.get("local_rule"), 8),
        ("locations[0].best_scene", location.get("best_scene"), 10),
        ("characters[0].role_drive", character.get("role_drive"), 10),
        ("characters[0].carries", character.get("carries"), 8),
        ("characters[0].complication", character.get("complication"), 10),
        ("scenarios[0].setup", scenario.get("setup"), 14),
    ]
    for label, reward in (("item", item), ("skill", skill)):
        checks.extend(
            [
                (f"rewards[{label}].grants", reward.get("grants"), 8),
                (f"rewards[{label}].best_used_when", reward.get("best_used_when"), 8),
                (f"rewards[{label}].catch", reward.get("catch"), 8),
            ]
        )

    problems: list[str] = []
    for label, value, minimum_words in checks:
        problems.extend(_check(label, value, minimum_words))
        problems.extend(_label_echo(label, value))
        if label.endswith(".grants"):
            problems.extend(_padding(label, value))
    problems.extend(_vibe_echo(proposal))
    return problems
