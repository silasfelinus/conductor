#!/usr/bin/env python3
"""Reject Hoshimori Krea2 prompt shapes known to fail before enqueueing ArtJobs.

A successful local ledger/receipt audit must not hide a production HTTP 422.
Keep this check specific to the e07/e08 style-proof lane: other engines may
support negative conditioning or physical card/poster layouts.
"""
from __future__ import annotations

import re

_NEGATIVE_TEXT = re.compile(
    r"\b(?:no|without|avoid|exclude|omit)\s+(?:visible\s+)?"
    r"(?:text|lettering|words|typography|labels|letters)\b",
    re.IGNORECASE,
)
_PHYSICAL_FORMAT = re.compile(
    r"\b(?:card|poster|book\s+cover)\s+(?:art|illustration|design)\b",
    re.IGNORECASE,
)


def validate_prompt(prompt: object, subject: str) -> None:
    if not isinstance(prompt, str) or len(prompt.strip()) < 120:
        raise ValueError(f"Missing production prompt for {subject}")
    if _NEGATIVE_TEXT.search(prompt):
        raise ValueError(
            f"Krea2 prompt text-exclusion wording rejected for {subject}; "
            "describe bare, unmarked surfaces affirmatively"
        )
    if _PHYSICAL_FORMAT.search(prompt):
        raise ValueError(
            f"Krea2 prompt physical-format wording rejected for {subject}; "
            "describe the depicted scene rather than a printed card or poster"
        )
