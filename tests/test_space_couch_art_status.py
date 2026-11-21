"""Space Couch art-ledger statuses must track the real queue and review states."""

from scripts.art_ledger_status import (
    ART_JOB_STATUSES,
    ART_LEDGER_STATUSES,
    CURATOR_STATUSES,
    is_visually_accepted,
    provenance_errors,
)
from scripts.enqueue_art_requests import TERMINAL_STATUSES


def _subject(status, image_id=None, job_id=74457):
    return {
        "jobs": {"krea2": job_id},
        "art": {"krea2": {"status": status, "art_image_id": image_id}},
    }


def test_queue_and_curator_states_have_distinct_canonical_meanings():
    assert ART_JOB_STATUSES == {
        "PENDING", "RUNNING", "DONE", "FAILED", "CANCELLED"
    }
    assert TERMINAL_STATUSES == ART_JOB_STATUSES - {"PENDING", "RUNNING"}
    assert CURATOR_STATUSES == {"ACCEPTED", "REJECTED"}
    assert ART_JOB_STATUSES.isdisjoint(CURATOR_STATUSES)
    assert ART_LEDGER_STATUSES == ART_JOB_STATUSES | CURATOR_STATUSES | {"ERROR"}


def test_each_queue_state_has_a_provenance_contract():
    for status in ("PENDING", "RUNNING", "FAILED", "CANCELLED", "ERROR"):
        assert provenance_errors(_subject(status), "krea2") == []
        assert provenance_errors(_subject(status, 277870), "krea2")
    assert provenance_errors(_subject("DONE", 277870), "krea2") == []
    assert provenance_errors(_subject("DONE"), "krea2")
    assert not is_visually_accepted(_subject("DONE", 277870), "krea2")


def test_curator_verdict_preserves_original_evidence():
    rejected = _subject("REJECTED", 277870)
    assert provenance_errors(rejected, "krea2") == []
    assert not is_visually_accepted(rejected, "krea2")
    assert provenance_errors(_subject("REJECTED"), "krea2") == []
    assert provenance_errors(_subject("ACCEPTED", 277870), "krea2") == []
    assert is_visually_accepted(_subject("ACCEPTED", 277870), "krea2")
    assert provenance_errors(_subject("ACCEPTED"), "krea2")


def test_invalid_statuses_and_ids_cannot_masquerade_as_delivered_art():
    assert provenance_errors(_subject("COMPLETE", 277870), "krea2")
    assert provenance_errors(_subject("DONE", True), "krea2")
    assert provenance_errors(_subject("DONE", -1), "krea2")
    assert provenance_errors(_subject("DONE", 277870, job_id=False), "krea2")
    assert provenance_errors({"jobs": {"krea2": 123}}, "krea2")
    assert not is_visually_accepted(_subject("ACCEPTED"), "krea2")
