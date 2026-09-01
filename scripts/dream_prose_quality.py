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
# of it. The field therefore has exactly one job: describe the circumstance. Any
# clause asserting that the reward is useful spends the sentence restating the
# label instead, and the catalog shows the difference plainly -- "The loudest
# person in the room is not the injured one." against "A flooded ruin or coastal
# tunnel beneath the coliseum roots, searched for a smuggled escape route, is
# where this compass earns its keep."
#
# This is the fourth pass at the same defect, and the first that targets the
# defect rather than a phrasing. Round one banned the literal "use it when";
# round two banned "<verb> it when" but excluded openings starting with "It";
# round three caught "It works best when" with a two-word window, and the next
# authoring wrote "It proves most valuable when" -- three words -- straight
# through it. Worse, telling the repair model to avoid the opening frame just
# moved it to the end ("... is exactly the moment this ladle earns its keep"),
# so a leading-only check now has a documented way of being evaded by its own
# repair lane. Matching the self-referential usefulness CLAIM wherever it sits
# closes both ends at once.
_SELF_REFERENCE = (
    r"(?:it|this|these|that|the\s+[a-z][\w'-]*"
    r"|[A-Z][\w'-]*(?:\s+[A-Z][\w'-]*)?)"
)
_USEFULNESS_CLAIM = (
    r"(?:proves?\s+(?:most\s+)?(?:valuable|useful)|proves?\s+its\s+worth"
    r"|earns?\s+its\s+keep|works?\s+best|serves?\s+best|shines?"
    r"|is\s+most\s+(?:useful|valuable)|calls?\s+for\s+it|demands?\s+it"
    r"|belongs?|takes?\s+hold|was\s+made\s+for)"
)
SELF_PROMOTION_PATTERNS = (
    # Leading frame: "It proves most valuable when ...", "The shawl earns its
    # keep in ...", "The situation calls for it when ...".
    re.compile(rf"^{_SELF_REFERENCE}\s+(?:\w+\s+){{0,3}}?{_USEFULNESS_CLAIM}\b", re.IGNORECASE),
    # "The moment to invoke it is ..." -- the same frame with the claim implied.
    re.compile(r"^the\s+(?:moment|time|situation)\s+to\s+\w+\s+it\b", re.IGNORECASE),
    # The generic leading stutter this check has caught since round two: the
    # reward is the subject and the situation is deferred behind a
    # when/once/if. Kept alongside the claim list because it catches openings no
    # verb list anticipates ("This helps when ...", "It is best when ...").
    re.compile(r"^(?:it|this)\s+(?:\w+\s+){0,3}?(?:when|once|if|the\s+moment)\b", re.IGNORECASE),
    # Trailing frame: "... is exactly the moment this ladle earns its keep.",
    # "... is precisely the situation this was made for.", "... calls for it most."
    re.compile(
        rf"\bis\s+(?:exactly\s+|precisely\s+)?(?:the\s+moment|the\s+situation|when|where)\s+{_SELF_REFERENCE}"
        rf"|\b{_USEFULNESS_CLAIM}(?:\s+(?:most|best|especially))?\.?$",
        re.IGNORECASE,
    ),
)

# "Best used when: When there isn't enough to go around ..." -- the label
# already supplied the "when".
BEST_USED_WHEN_OPENERS = re.compile(r"^(?:when|whenever)\b", re.IGNORECASE)

# The field names a circumstance, not an action for the reader to take, so an
# opening imperative does not fit its own label: "Best used when: Study the
# bloom up close ...". Deliberately a closed list of verbs that are unambiguous
# in this position, with a guard against the same words used as subject nouns
# ("Watch is ...", "Study has ...").
IMPERATIVE_OPENERS = (
    re.compile(
        r"^(?:use|study|reach|call|rely|apply|deploy|invoke|bring|take|keep|check|look|watch|try|save)\s+"
        r"(?!is\b|are\b|was\b|were\b|has\b|have\b)",
        re.IGNORECASE,
    ),
    # "Reach for it when ...", "Turn to it once ...", "Rely on it when ...".
    # Generalizes over the verb rather than enumerating it, which is what the
    # closed list above cannot do.
    re.compile(
        r"^(?!it\b|this\b)\w+(?:\s+(?:on|for|to|upon))?\s+it\s+(?:when|once|if|the\s+moment)\b",
        re.IGNORECASE,
    ),
)

# Schema words leaking into copy a reader sees. "Under the vibe Paperwork for a
# God, Bramble Osei is mid-stamp ..." opens a scenario by naming our own field.
SCHEMA_VOCABULARY = re.compile(
    r"\b(?:(?:the|this)\s+(?:dream\s+)?vibe|(?:the|this)\s+facet"
    r"|the\s+proposal|the\s+bundle|reward\s+type)\b",
    re.IGNORECASE,
)

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
    text = value.strip()
    if field == "best_used_when":
        if any(pattern.search(text) for pattern in SELF_PROMOTION_PATTERNS):
            return [
                f"{label} spends the sentence claiming the reward is useful, which "
                "the 'Best used when' label already says; delete the claim and let "
                "the circumstance be the whole sentence"
            ]
        if BEST_USED_WHEN_OPENERS.match(text):
            return [
                f"{label} opens with 'when', which the label already supplied; start "
                "at the circumstance itself"
            ]
        if any(pattern.match(text) for pattern in IMPERATIVE_OPENERS):
            return [
                f"{label} is an instruction to the reader, not the circumstance the "
                "label names; describe the situation instead of telling someone what to do"
            ]
    opening = " ".join(re.findall(r"[\w’'-]+", value.casefold())[:ECHO_WINDOW_WORDS])
    for phrase in LABEL_ECHOES.get(field, ()):
        if phrase in opening:
            return [
                f"{label} restates its own label ({phrase!r}); the card already prints "
                "it, so write the value as a sentence that stands without the label"
            ]
    return []


def _schema_leak(label: str, value: Any) -> list[str]:
    """Flag our own field vocabulary appearing in copy a reader sees."""
    if not isinstance(value, str):
        return []
    match = SCHEMA_VOCABULARY.search(value)
    if not match:
        return []
    return [
        f"{label} names the schema out loud ({match.group(0)!r}); a reader sees the "
        "card, not our field names, so write it as ordinary prose"
    ]


def _borrowed_names(proposal: dict) -> list[str]:
    """Flag reward and location copy that hard-codes this bundle's character.

    Every asset is meant to be liftable into another story on its own. A reward
    whose text reads "It lets Bramble draft, stamp, and cross-reference ..." is
    welded to one character and cannot be. Scenarios are exempt by design --
    Silas, 2026-08-31: "scenarios are synthesis pieces that can name other
    objects" -- and so is the character's own copy.
    """
    names: set[str] = set()
    for row in proposal.get("characters") or []:
        if isinstance(row, dict):
            names.update(re.findall(r"[A-Z][a-z]{3,}", str(row.get("name") or "")))
    if not names:
        return []
    problems: list[str] = []
    # Only the card-copy fields, because a complaint is also the repair lane's
    # work order: a label it cannot resolve to a field path would be dropped on
    # the way in and still be there on the way out, deadlocking the batch.
    scoped = {
        "rewards": ("grants", "best_used_when", "catch"),
        "locations": ("known_for", "local_rule", "best_scene"),
    }
    for scope, rows in (("rewards", proposal.get("rewards")), ("locations", proposal.get("locations"))):
        for row in rows if isinstance(rows, list) else []:
            if not isinstance(row, dict):
                continue
            if scope == "rewards":
                kind = str(row.get("reward_type") or "").lower() or "reward"
            else:
                kind = "0"
            for field in scoped[scope]:
                text = row.get(field)
                if not isinstance(text, str):
                    continue
                hit = sorted(n for n in names if re.search(rf"\b{re.escape(n)}\b", text))
                if hit:
                    problems.append(
                        f"{scope}[{kind}].{field} hard-codes the character name "
                        f"({', '.join(hit)}); this asset has to read on its own in another "
                        "story, so describe the bearer generically"
                    )
    return problems


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
        problems.extend(_schema_leak(label, value))
        if label.endswith(".grants"):
            problems.extend(_padding(label, value))
    problems.extend(_vibe_echo(proposal))
    problems.extend(_borrowed_names(proposal))
    return problems
