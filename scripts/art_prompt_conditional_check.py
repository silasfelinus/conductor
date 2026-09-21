#!/usr/bin/env python3
"""Shared conditional-instruction detector for art prompts.

Diffusion models render words; they cannot evaluate a condition. Kind Robots'
own server-side contract (kind_robots' server/utils/artPromptContract.ts)
rejects a prompt containing this shape at ArtJob submission time with HTTP 422
[conditional-instruction] -- but that is the last possible moment to catch it,
after a prompt has already been authored, queued, and (for a scheduled
pipeline like Daily Dream) left stuck re-failing on every run until a human
notices (dream-cycle/t-028: the-drowned-compact/t-2026-09-09's Split Vow
reward sat this way for two failed daily-digest runs).

This module is the one place the conditional-instruction pattern list lives
in Python, mirroring kind_robots' CONDITIONAL_PATTERNS so every builder that
assembles a submittable art_prompt can fail loudly at its own build time
instead of silently at submit time. `build_ruler_hooked_art_queue.py` and
`build_dream_records.py` both import from here rather than each keeping (or
drifting from) their own copy of the regex.
"""
from __future__ import annotations

import re

CONDITIONAL_PATTERNS = [
    r"\bonly (?:when|if)\b",
    r"\bwhen (?:the )?(?:subject|scene|context)\b",
    r"\b(?:if|unless) (?:the )?(?:subject|scene|context|prompt)\b",
    r"\bwhere (?:appropriate|relevant|applicable)\b",
    r"\bas (?:needed|appropriate)\b",
    # Scoped to a cast noun plus a presence verb, so ordinary prose that
    # happens to say "when" about people is untouched: "a market at dusk
    # when people light the lanterns" describes a scene; "when people
    # appear" hands the model a decision it cannot make.
    r"\b(?:when|if|where|whenever|unless)\s+(?:any\s+|some\s+|the\s+|no\s+)?"
    r"(?:figures?|people|persons?|characters?|humans?|robots?|creatures?|bystanders?|"
    r"crowds?|onlookers?)\s+(?:do\s+|are\s+|is\s+)?"
    r"(?:appear|present|shown|show up|included|visible|featured|depicted)\b",
]


def conditional_instruction_violations(prompt: str) -> list[str]:
    """Every conditional-instruction phrase kind_robots' contract would reject."""
    found: list[str] = []
    for pattern in CONDITIONAL_PATTERNS:
        match = re.search(pattern, prompt, re.I)
        if match:
            found.append(f"conditional-instruction: {match.group(0)!r}")
    return found
