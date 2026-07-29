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


def test_record_semantic_gate_error_stamps_job_id_when_missing(tmp_path, monkeypatch):
    # t-035: a fresh submission's ArtJob completes and renders, but
    # validate_candidate() then fails on something unrelated to the render (e.g. no
    # ANTHROPIC_API_KEY). The raw error message has no job reference in it, so
    # without stamping one on, referenced_job_id() can never recover the
    # already-completed render and every future pass is forced into a genuine
    # duplicate resubmission.
    queue_file = tmp_path / "color-art-jobs.yaml"
    queue_file.write_text(
        yaml.safe_dump(
            {
                "defaults": {},
                "books": [
                    {
                        "slug": "monster-recast",
                        "entries": [{"id": "mr-018", "status": "pending", "title": "Blocked"}],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(mod, "QUEUE_FILE", queue_file)

    mod.record_semantic_gate_error(
        entry(queue_id="mr-018"),
        RuntimeError("ANTHROPIC_API_KEY is required for the production semantic art gate"),
        job_id=3001,
    )

    stored = yaml.safe_load(queue_file.read_text())["books"][0]["entries"][0]["semantic_gate_error"]
    assert stored == "job 3001: ANTHROPIC_API_KEY is required for the production semantic art gate"
    assert mod.referenced_job_id({"semantic_gate_error": stored}) == 3001


def test_record_semantic_gate_error_does_not_double_stamp_an_existing_job_reference(tmp_path, monkeypatch):
    # A message that already names a job (e.g. the wait_for_job() timeout text)
    # must not get a second, different job_id prepended -- that would make
    # referenced_job_id() resolve to the wrong ArtJob.
    queue_file = tmp_path / "color-art-jobs.yaml"
    queue_file.write_text(
        yaml.safe_dump(
            {
                "defaults": {},
                "books": [
                    {
                        "slug": "monster-recast",
                        "entries": [{"id": "mr-018", "status": "pending", "title": "Blocked"}],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(mod, "QUEUE_FILE", queue_file)

    mod.record_semantic_gate_error(
        entry(queue_id="mr-018"),
        RuntimeError("job 2751 timed out after 600s (still queued/running)"),
        job_id=9999,
    )

    stored = yaml.safe_load(queue_file.read_text())["books"][0]["entries"][0]["semantic_gate_error"]
    assert stored == "job 2751 timed out after 600s (still queued/running)"
    assert mod.referenced_job_id({"semantic_gate_error": stored}) == 2751


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


def test_dry_run_with_ids_bounds_pass_to_exactly_those_entries(monkeypatch, tmp_path, capsys):
    # Regression: a plain --limit takes the next N pending entries in queue-slot
    # order, which mixes recovery-eligible entries (a stuck job to reconcile) with
    # entries blocked on something else entirely (e.g. a missing ANTHROPIC_API_KEY,
    # which --live would then retry as a brand-new, likely-to-fail-again enqueue).
    # --ids must let a caller bound a run to exactly the recovery_batch reported by
    # scripts/coloring_queue_status.py, skipping every other pending entry even
    # when it sits earlier in queue order.
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
                                "title": "Blocked On Fresh Submission",
                                "prompt": "A vampire family portrait",
                                "image_path": "projects/coloring-book/sets/monster-recast/generated/mr-001.webp",
                                "semantic_gate_error": "ANTHROPIC_API_KEY is required for the production semantic art gate",
                            },
                            {
                                "id": "mr-016",
                                "status": "pending",
                                "title": "Recovery Candidate",
                                "prompt": "A werewolf family portrait",
                                "image_path": "projects/coloring-book/sets/monster-recast/generated/mr-016.webp",
                                "semantic_gate_error": "job 2751 timed out after 600s (still queued/running)",
                            },
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(mod, "QUEUE_FILE", queue_file)
    monkeypatch.setattr(
        "sys.argv", ["consume_coloring_book_color_art.py", "--book", "monster-recast", "--ids", "mr-016"]
    )

    exit_code = mod.main()

    assert exit_code == 0
    out = capsys.readouterr().out
    assert "1 of 2 pending" in out
    assert "ids=['mr-016']" in out
    assert "mr-001" not in out


def test_live_fresh_submission_failure_stamps_job_id_for_future_recovery(monkeypatch, tmp_path, capsys):
    # t-035: a *fresh* submission (no prior job reference at all -- distinct from
    # the recovery-path regression above) enqueues, waits, and renders
    # successfully, but validate_candidate() then fails (e.g. no
    # ANTHROPIC_API_KEY). Before this fix the recorded semantic_gate_error had no
    # "job N" text, so referenced_job_id() could never find the already-completed
    # render on a later pass -- only a genuine (duplicate-risking) resubmission was
    # possible. The newly submitted ArtJob's id must now end up recoverable.
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
                                "id": "mr-018",
                                "status": "pending",
                                "title": "Fresh Submission",
                                "prompt": "A mummy family portrait",
                                "image_path": "projects/coloring-book/sets/monster-recast/generated/mr-018.webp",
                            }
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(mod, "QUEUE_FILE", queue_file)
    monkeypatch.setattr(mod, "target_path", lambda entry: tmp_path / "candidate.webp")
    monkeypatch.setattr(mod.consumer, "KR_API_TOKEN", "token")
    monkeypatch.setattr(mod, "enqueue", lambda entry: (3001, False))
    monkeypatch.setattr(mod.consumer, "wait_for_job", lambda job_id, timeout: {"artImageId": 555})
    monkeypatch.setattr(mod.consumer, "fetch_image_b64", lambda art_image_id: "aGVsbG8=")

    def fake_save_result(entry, image_b64):
        destination = tmp_path / "candidate.webp"
        destination.write_bytes(b"stub")
        return destination

    monkeypatch.setattr(mod, "save_result", fake_save_result)

    def fake_validate_candidate(entry, destination):
        raise RuntimeError("ANTHROPIC_API_KEY is required for the production semantic art gate")

    monkeypatch.setattr(mod, "validate_candidate", fake_validate_candidate)
    monkeypatch.setattr(
        "sys.argv", ["consume_coloring_book_color_art.py", "--live", "--book", "monster-recast", "--ids", "mr-018"]
    )

    exit_code = mod.main()

    assert exit_code == 1
    stderr = capsys.readouterr().err
    assert "FAILED" in stderr

    _queue, entries = mod.build_entries("monster-recast")
    stored_error = entries[0]["semantic_gate_error"]
    assert stored_error == "job 3001: ANTHROPIC_API_KEY is required for the production semantic art gate"
    assert mod.referenced_job_id(entries[0]) == 3001


def test_live_recovery_blocked_by_missing_semantic_credential_preserves_job_reference(monkeypatch, tmp_path, capsys):
    # Regression (found running t-032 live 2026-07-28): a live recovery pass with
    # no ANTHROPIC_API_KEY reconciles a completed ArtJob's image without
    # submitting a duplicate, but validate_candidate still fails (the semantic
    # gate itself requires the credential). The generic except-block handler used
    # to overwrite the entry's semantic_gate_error with that failure message,
    # erasing the "job N timed out" text a future recovery pass parses via
    # referenced_job_id() -- without it, the next pass sees no job to recover and
    # submits a genuine duplicate ArtJob for the same already-completed render.
    # The original recoverable reference must survive this specific failure mode.
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
                                "id": "mr-016",
                                "status": "pending",
                                "title": "Recovery Candidate",
                                "prompt": "A werewolf family portrait",
                                "image_path": "projects/coloring-book/sets/monster-recast/generated/mr-016.webp",
                                "semantic_gate_error": "job 2751 timed out after 600s (still queued/running)",
                                "semantic_gate_error_at": "2026-07-28T10:58:59Z",
                            }
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(mod, "QUEUE_FILE", queue_file)
    monkeypatch.setattr(mod, "target_path", lambda entry: tmp_path / "candidate.webp")
    monkeypatch.setattr(mod.consumer, "KR_API_TOKEN", "token")
    monkeypatch.setattr(
        mod.consumer,
        "http_json",
        lambda method, url: (
            200,
            {
                "success": True,
                "data": {
                    "job": {
                        "status": "DONE",
                        "artImageId": 555,
                        "payload": {"attempt": {"conceptId": "mr-016", "seed": 840016}},
                    }
                },
            },
        ),
    )
    monkeypatch.setattr(mod.consumer, "fetch_image_b64", lambda art_image_id: "aGVsbG8=")

    def fake_save_result(entry, image_b64):
        destination = tmp_path / "candidate.webp"
        destination.write_bytes(b"stub")
        return destination

    monkeypatch.setattr(mod, "save_result", fake_save_result)

    def fake_validate_candidate(entry, destination):
        raise RuntimeError("ANTHROPIC_API_KEY is required for the production semantic art gate")

    monkeypatch.setattr(mod, "validate_candidate", fake_validate_candidate)

    def fail_enqueue(entry):
        raise AssertionError("must not submit a duplicate ArtJob")

    monkeypatch.setattr(mod, "enqueue", fail_enqueue)
    monkeypatch.setattr(
        "sys.argv", ["consume_coloring_book_color_art.py", "--live", "--book", "monster-recast", "--ids", "mr-016"]
    )

    exit_code = mod.main()

    assert exit_code == 1
    stderr = capsys.readouterr().err
    assert "RECOVERY UNVERIFIED" in stderr

    _queue, entries = mod.build_entries("monster-recast")
    assert entries[0]["semantic_gate_error"] == "job 2751 timed out after 600s (still queued/running)"


def _recovery_queue_file(tmp_path, queue_id="mr-016"):
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
                                "id": queue_id,
                                "status": "pending",
                                "title": "Recovery Candidate",
                                "prompt": "A werewolf family portrait",
                                "image_path": f"projects/coloring-book/sets/monster-recast/generated/{queue_id}.webp",
                                "semantic_gate_error": "job 2751 timed out after 600s (still queued/running)",
                                "semantic_gate_error_at": "2026-07-28T10:58:59Z",
                            }
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return queue_file


def test_live_recovery_blocked_by_missing_local_dependency_preserves_job_reference(monkeypatch, tmp_path, capsys):
    # Regression (found running t-022 live 2026-07-29): the sandbox that ran a
    # recovery pass had no Pillow installed, so save_result() raised while
    # converting the already-fetched, already-completed render to WebP -- a
    # local-environment problem, not evidence the ArtJob itself is bad. The old
    # except-block guard only preserved the job reference for messages
    # containing "ANTHROPIC_API_KEY", so this failure mode overwrote
    # semantic_gate_error with a bare "Pillow is required..." string carrying no
    # job id. The very next pass (once Pillow was installed) then found nothing
    # to recover and submitted a genuine duplicate ArtJob against the render
    # backend for an image that had already rendered successfully.
    queue_file = _recovery_queue_file(tmp_path)
    monkeypatch.setattr(mod, "QUEUE_FILE", queue_file)
    monkeypatch.setattr(mod, "target_path", lambda entry: tmp_path / "candidate.webp")
    monkeypatch.setattr(mod.consumer, "KR_API_TOKEN", "token")
    monkeypatch.setattr(
        mod.consumer,
        "http_json",
        lambda method, url: (
            200,
            {
                "success": True,
                "data": {
                    "job": {
                        "status": "DONE",
                        "artImageId": 555,
                        "payload": {"attempt": {"conceptId": "mr-016", "seed": 840016}},
                    }
                },
            },
        ),
    )
    monkeypatch.setattr(mod.consumer, "fetch_image_b64", lambda art_image_id: "aGVsbG8=")

    def fake_save_result(entry, image_b64):
        raise RuntimeError("Pillow is required for WebP output.")

    monkeypatch.setattr(mod, "save_result", fake_save_result)

    def fail_enqueue(entry):
        raise AssertionError("must not submit a duplicate ArtJob")

    monkeypatch.setattr(mod, "enqueue", fail_enqueue)
    monkeypatch.setattr(
        "sys.argv", ["consume_coloring_book_color_art.py", "--live", "--book", "monster-recast", "--ids", "mr-016"]
    )

    exit_code = mod.main()

    assert exit_code == 1
    stderr = capsys.readouterr().err
    assert "RECOVERY UNVERIFIED" in stderr

    _queue, entries = mod.build_entries("monster-recast")
    assert entries[0]["semantic_gate_error"] == "job 2751 timed out after 600s (still queued/running)"


def test_live_recovery_blocked_by_network_error_checking_status_preserves_job_reference(
    monkeypatch, tmp_path, capsys
):
    # Regression (found running t-022 live 2026-07-29, same session as the
    # Pillow case above): the GET that checks a stuck job's live status can
    # itself hit a transient network error (observed:
    # "<urlopen error [Errno 104] Connection reset by peer>") before recovery
    # ever learns whether the job succeeded. This must not be treated as
    # evidence the job is dead either -- only RecoveryAbandoned (a job the
    # backend has positively reported as FAILED/CANCELLED/mismatched) should
    # clear the reference.
    queue_file = _recovery_queue_file(tmp_path)
    monkeypatch.setattr(mod, "QUEUE_FILE", queue_file)
    monkeypatch.setattr(mod, "target_path", lambda entry: tmp_path / "candidate.webp")
    monkeypatch.setattr(mod.consumer, "KR_API_TOKEN", "token")

    def flaky_http_json(method, url):
        raise OSError("[Errno 104] Connection reset by peer")

    monkeypatch.setattr(mod.consumer, "http_json", flaky_http_json)

    def fail_enqueue(entry):
        raise AssertionError("must not submit a duplicate ArtJob")

    monkeypatch.setattr(mod, "enqueue", fail_enqueue)
    monkeypatch.setattr(
        "sys.argv", ["consume_coloring_book_color_art.py", "--live", "--book", "monster-recast", "--ids", "mr-016"]
    )

    exit_code = mod.main()

    assert exit_code == 1
    stderr = capsys.readouterr().err
    assert "RECOVERY UNVERIFIED" in stderr

    _queue, entries = mod.build_entries("monster-recast")
    assert entries[0]["semantic_gate_error"] == "job 2751 timed out after 600s (still queued/running)"


def test_live_recovery_of_genuinely_failed_job_still_clears_reference(monkeypatch, tmp_path, capsys):
    # The flip side of the two regressions above: when recover_timed_out_job()
    # positively determines the job failed on the backend (RecoveryAbandoned),
    # the reference SHOULD be cleared so the next pass submits fresh instead of
    # retrying a job that will never succeed.
    queue_file = _recovery_queue_file(tmp_path)
    monkeypatch.setattr(mod, "QUEUE_FILE", queue_file)
    monkeypatch.setattr(mod, "target_path", lambda entry: tmp_path / "candidate.webp")
    monkeypatch.setattr(mod.consumer, "KR_API_TOKEN", "token")
    monkeypatch.setattr(
        mod.consumer,
        "http_json",
        lambda method, url: (200, {"success": True, "data": {"job": {"status": "FAILED", "error": "boom"}}}),
    )

    def fail_enqueue(entry):
        raise AssertionError("must not submit a duplicate ArtJob")

    monkeypatch.setattr(mod, "enqueue", fail_enqueue)
    monkeypatch.setattr(
        "sys.argv", ["consume_coloring_book_color_art.py", "--live", "--book", "monster-recast", "--ids", "mr-016"]
    )

    exit_code = mod.main()

    assert exit_code == 1
    stderr = capsys.readouterr().err
    assert "FAILED" in stderr
    assert "RECOVERY UNVERIFIED" not in stderr

    _queue, entries = mod.build_entries("monster-recast")
    assert entries[0]["semantic_gate_error"] == "job 2751 FAILED: boom"
