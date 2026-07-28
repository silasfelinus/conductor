from pathlib import Path

import pytest
import yaml

from scripts import consume_coloring_book_color_art as mod


def entry(**overrides):
    value = {
        "set": "monster-recast",
        "concept_id": "mr-001",
        "queue_id": "mr-001",
        "image_path": "projects/coloring-book/sets/monster-recast/generated/color-proposals-v1/mr-001.webp",
        "scene_prompt": "A vampire family portrait",
        "prompt_fingerprint": "abc123",
        "semantic_gate_error": "job 2702 timed out after 600s (still queued/running)",
    }
    value.update(overrides)
    return value


def test_referenced_job_id_extracts_id_from_timeout_message():
    assert mod.referenced_job_id(entry()) == 2702


def test_referenced_job_id_returns_none_without_a_job_reference():
    assert mod.referenced_job_id(entry(semantic_gate_error="enqueue failed: HTTP 503 ...")) is None


def test_referenced_job_id_returns_none_without_any_error():
    assert mod.referenced_job_id(entry(semantic_gate_error=None)) is None


def test_recover_still_running_job_returns_none_without_mutating_anything(monkeypatch):
    monkeypatch.setattr(
        mod.consumer,
        "http_json",
        lambda method, url: (200, {"success": True, "data": {"job": {"status": "RUNNING"}}}),
    )

    result = mod.recover_timed_out_job(entry(), 2702)

    assert result is None


def test_recover_done_job_fetches_existing_image_instead_of_enqueueing(monkeypatch, tmp_path):
    job = {
        "status": "DONE",
        "artImageId": 12938,
        "payload": {
            "attempt": {"conceptId": "mr-001", "seed": 317488864},
        },
    }
    monkeypatch.setattr(
        mod.consumer,
        "http_json",
        lambda method, url: (200, {"success": True, "data": {"job": job}}),
    )
    monkeypatch.setattr(mod.consumer, "fetch_image_b64", lambda art_image_id: "aGVsbG8=")

    def fake_enqueue(entry):
        raise AssertionError("recovery must not enqueue a duplicate ArtJob")

    monkeypatch.setattr(mod, "enqueue", fake_enqueue)
    monkeypatch.setattr(mod, "save_result", lambda entry, image_b64: tmp_path / "candidate.webp")
    monkeypatch.setattr(mod, "validate_candidate", lambda entry, destination: (True, {"score": 91}))

    item = entry()
    accepted, semantic = mod.recover_timed_out_job(item, 2702)

    assert accepted is True
    assert semantic == {"score": 91}
    assert item["art_image_id"] == 12938
    assert item["resolved_seed"] == 317488864


def test_recover_rejects_job_belonging_to_a_different_concept(monkeypatch):
    job = {
        "status": "DONE",
        "artImageId": 999,
        "payload": {"attempt": {"conceptId": "mr-002"}},
    }
    monkeypatch.setattr(
        mod.consumer,
        "http_json",
        lambda method, url: (200, {"success": True, "data": {"job": job}}),
    )

    with pytest.raises(RuntimeError, match="belongs to concept"):
        mod.recover_timed_out_job(entry(), 2702)


def test_recover_raises_for_failed_job(monkeypatch):
    job = {"status": "FAILED", "error": "boom"}
    monkeypatch.setattr(
        mod.consumer,
        "http_json",
        lambda method, url: (200, {"success": True, "data": {"job": job}}),
    )

    with pytest.raises(RuntimeError, match="FAILED"):
        mod.recover_timed_out_job(entry(), 2702)


def test_recover_returns_none_on_unreachable_backend(monkeypatch):
    monkeypatch.setattr(mod.consumer, "http_json", lambda method, url: (503, None))

    assert mod.recover_timed_out_job(entry(), 2702) is None


def test_build_entries_carries_semantic_gate_error_onto_the_consumption_entry(monkeypatch, tmp_path):
    # Regression: build_entries() previously only copied a fixed allowlist of
    # fields from the raw queue source onto the entry used by main()'s loop,
    # silently dropping semantic_gate_error. referenced_job_id(entry) then
    # always saw None in production, so recover_timed_out_job() never fired
    # and a live run submitted a genuine duplicate ArtJob for a concept whose
    # prior job had already completed (mr-001 -> job 2715 alongside the
    # already-DONE job 2702, caught live 2026-07-27).
    queue_file = tmp_path / "color-art-jobs.yaml"
    queue_file.write_text(
        yaml.safe_dump(
            {
                "defaults": {},
                "books": [
                    {
                        "slug": "monster-recast",
                        "entries": [
                            {
                                "id": "mr-001",
                                "status": "pending",
                                "title": "Perfect Woman",
                                "prompt": "A vampire family portrait",
                                "image_path": "projects/coloring-book/sets/monster-recast/generated/mr-001.webp",
                                "semantic_gate_error": "job 2702 timed out after 600s (still queued/running)",
                                "semantic_gate_error_at": "2026-07-27T13:51:38Z",
                            }
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(mod, "QUEUE_FILE", queue_file)

    _queue, entries = mod.build_entries("monster-recast")

    assert len(entries) == 1
    assert mod.referenced_job_id(entries[0]) == 2702
