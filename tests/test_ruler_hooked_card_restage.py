"""Ruler Hooked restaged card art keeps provenance until real renders arrive."""

from scripts import build_ruler_hooked_art_queue as queue


REVISED_CARD_IDS = {
    "river-commons-vote",
    "marina-family-charter",
    "water-rights-hearing",
    "weir-reckoning",
    "moat-reckoning",
    "treaty-reckoning",
    "marina-reckoning",
    "wedding-reckoning",
}


def test_restaged_cards_retain_original_art_job_provenance():
    rows = queue.staged_rows(queue.ART_PROMPTS.read_text(encoding="utf-8"))
    for card_id in REVISED_CARD_IDS:
        request = rows.get(f"ruler-hooked-card-{card_id}")
        if not request or request.get("status") != "pending":
            continue
        assert request.get("force") is True, card_id
        assert request.get("auto_submit") is True, card_id
        assert request.get("superseded_art_job_id"), card_id
        # Enqueue records the new job id while the request is still pending
        # (submitted, not yet rendered); it must never point back at the old job.
        assert request.get("last_art_job_id") != request.get("superseded_art_job_id"), card_id
        assert request.get("page_url") == queue.PAGE_URL, card_id
        assert "psychedelic rainbow" in request["prompt"], card_id


def test_ruler_hooked_art_queue_uses_canonical_play_route():
    assert queue.PAGE_URL == "https://kindrobots.org/play/ruler-hooked"
