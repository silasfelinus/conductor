#!/usr/bin/env python3
"""Deterministic retry helpers for art renders that failed the mechanical gate.

This module used to be ``semantic_art_quality`` and wrapped an Opus vision call
that scored every render against a written rubric. That gate is gone: quality
judgement is a human job (see AGENTS.md / the coloring-book run log). What
survives here is the mechanical-retry bookkeeping — reseeding a render that came
back blank, mis-sized, or otherwise structurally broken, which is an objective
failure a machine can and should catch for free via ``art_quality.assess_file``.

Nothing in this module calls an LLM or needs a credential.
"""

from __future__ import annotations

import os

# How many times a render may be re-attempted after a *mechanical* failure
# (blank frame, wrong aspect, unreadable file) before it is parked for a human.
# This is not a quality bar — a render that is structurally fine goes straight
# to human review on the first attempt, however ugly it may be.
MAX_RENDER_ATTEMPTS = int(os.environ.get("COLOR_ART_MAX_RENDER_ATTEMPTS", "3"))


def next_retry_seed(seed: int, attempt: int) -> int:
    """Return a deterministic new seed for a bounded mechanical retry."""

    base = max(0, int(seed))
    nth = max(1, int(attempt))
    return (base + 104_729 + nth * 7_919) % 2_147_483_647


def retry_prompt(
    scene_prompt: str,
    title: str,
    attempt: int,
    note: str | None = None,
) -> str:
    """Add compact guidance to a re-render.

    ``note`` carries a human REVISE comment through to the next render when one
    was given; without it this just restates the subject so a structurally
    failed attempt does not drift off the brief.
    """

    nth = max(1, int(attempt))
    label = " ".join(str(title or "the requested scene").split())
    guidance = (
        f" Re-render {nth}: visibly depict {label} as the dominant scene. "
        "Preserve every named person, creature, count, relationship, action, and "
        "setting from the opening prompt."
    )
    if note:
        guidance += " Reviewer note: " + " ".join(str(note).split())
    return " ".join((scene_prompt + guidance).split())
