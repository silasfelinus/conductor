"""Ruler Hooked krea2 prompts never use "frame" or "picture" as composition words.

kind_robots' prompt contract rejects both on krea2 ([frame-noun] / [picture-noun]):
Krea paints the noun. Border Accordionfish's frame_override ("fully inside the
frame") passed every local check and only failed at enqueue with HTTP 422
(art-queue-health, 2026-11-23 PT). Catch it here instead.
"""

import re

from scripts import build_ruler_hooked_art_queue as queue

BANNED = re.compile(r"\b(frames?|picture)\b", re.IGNORECASE)


def test_ruler_hooked_krea_prompts_avoid_frame_and_picture_nouns():
    rows = queue.staged_rows(queue.ART_PROMPTS.read_text(encoding="utf-8"))
    offenders = sorted(
        request_id
        for request_id, request in rows.items()
        if request_id.startswith("ruler-hooked-")
        and request.get("engine") == "krea2"
        and request.get("status") == "pending"
        and BANNED.search(request.get("prompt") or "")
    )
    assert not offenders, f"frame/picture noun in krea2 prompt: {offenders}"
