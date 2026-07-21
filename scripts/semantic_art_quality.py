#!/usr/bin/env python3
"""Fail-closed semantic quality checks for production art pipelines."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

try:
    import curate_art
except ModuleNotFoundError:
    from scripts import curate_art

DEFAULT_MIN_SCORE = int(os.environ.get("COLOR_ART_MIN_SEMANTIC_SCORE", "75"))
DEFAULT_MAX_ATTEMPTS = int(os.environ.get("COLOR_ART_MAX_SEMANTIC_ATTEMPTS", "3"))


def assess_semantic_file(
    path: Path,
    scene_prompt: str,
    min_score: int = DEFAULT_MIN_SCORE,
) -> tuple[bool, dict[str, Any]]:
    """Judge subject fidelity and brief compliance with the shared curator rubric.

    Production callers must not silently degrade to mechanical-only validation. A
    missing vision credential or an API failure raises, leaving the source item
    pending for a later run.
    """

    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is required for the production semantic art gate"
        )

    verdict = curate_art.call_vision(
        api_key,
        path,
        "color",
        scene_prompt,
        [],
        rubric=curate_art.RUBRIC,
        schema=curate_art.VERDICT_SCHEMA,
    )

    score = int(verdict.get("score") or 0)
    subject_match = verdict.get("subject_match") is True
    on_brief = verdict.get("on_brief") is True
    verdict_name = str(verdict.get("verdict") or "reject").strip().lower()
    reasons = [str(reason) for reason in verdict.get("reasons") or []]

    accepted = (
        subject_match
        and on_brief
        and score >= min_score
        and verdict_name != "reject"
    )

    if not subject_match:
        reasons.insert(0, "requested subjects or scene are absent")
    if not on_brief:
        reasons.insert(0, "render is off the requested visual brief")
    if score < min_score:
        reasons.insert(0, f"semantic score {score} is below minimum {min_score}")
    if verdict_name == "reject" and not reasons:
        reasons.append("semantic reviewer rejected the render")

    normalized = {
        "model": curate_art.MODEL,
        "score": score,
        "verdict": verdict_name,
        "subject_match": subject_match,
        "on_brief": on_brief,
        "line_art_valid": verdict.get("line_art_valid") is True,
        "camp_reads": verdict.get("camp_reads") is True,
        "horror_reads": verdict.get("horror_reads") is True,
        "anatomy_ok": verdict.get("anatomy_ok") is True,
        "matches_approved_bar": verdict.get("matches_approved_bar") is True,
        "reasons": list(dict.fromkeys(reasons)),
        "min_score": min_score,
    }
    return accepted, normalized


def next_retry_seed(seed: int, semantic_attempt: int) -> int:
    """Return a deterministic new seed for a bounded semantic retry."""

    base = max(0, int(seed))
    attempt = max(1, int(semantic_attempt))
    return (base + 104_729 + attempt * 7_919) % 2_147_483_647


def literal_retry_prompt(
    scene_prompt: str,
    title: str,
    semantic_attempt: int,
) -> str:
    """Add compact literal guidance after a subject-fidelity rejection."""

    attempt = max(1, int(semantic_attempt))
    label = " ".join(str(title or "the requested scene").split())
    guidance = (
        f" Literal subject-fidelity retry {attempt}: visibly depict {label} as the "
        "dominant scene. Preserve every named person, creature, count, relationship, "
        "action, and setting from the opening prompt. Do not replace the subjects with "
        "abstract architecture, a cosmic landscape, a symbolic poster, or a lone generic "
        "figure. Make the requested cast immediately countable and unmistakable."
    )
    return " ".join((scene_prompt + guidance).split())
