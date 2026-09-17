from scripts.coloring_queue_status import has_missing_file, requirement_satisfied, summarize_queue


def queue(entries):
    return {
        "batch_policy": {"worker_pass_size": 2},
        "books": [{"slug": "monster-recast", "entries": entries}],
    }


def test_summarizes_statuses_and_next_batch():
    summary = summarize_queue(
        queue(
            [
                {"slot": 1, "id": "mr-001", "status": "pending"},
                {"slot": 2, "id": "mr-002", "status": "approved"},
                {"slot": 3, "id": "mr-003", "status": "pending"},
            ]
        ),
        "monster-recast",
    )

    assert summary["statuses"] == {"approved": 1, "pending": 2}
    assert [entry["id"] for entry in summary["next_batch"]] == ["mr-001", "mr-003"]
    assert summary["blocked_pending"] == []
    assert summary["recovery_candidates"] == []
    assert summary["recovery_batch"] == []
    assert summary["recovery_actionable"] is False
    assert summary["recovery_actionable_count"] == 0
    assert summary["fresh_submission_blocked"] == []
    assert summary["queue_integrity_safe"] is True
    assert summary["recovery_safe"] is True
    assert summary["retry_safe"] is True
    assert summary["actionable"] is True
    assert summary["actionable_count"] == 2
    assert summary["recommended_action"] == "submit-next-batch"


def test_render_gate_errors_are_classified_for_recovery_or_fresh_submission():
    summary = summarize_queue(
        queue(
            [
                {
                    "slot": 1,
                    "id": "mr-001",
                    "status": "pending",
                    "render_gate_error": "job 2474 timed out after 600s (still queued/running)",
                    "render_gate_error_at": "2026-07-26T12:18:00Z",
                },
                {
                    "slot": 2,
                    "id": "mr-002",
                    "status": "pending",
                    "render_gate_error": "enqueue failed: HTTP 503 Database connection was temporarily unavailable",
                },
                {"slot": 3, "id": "mr-003", "status": "pending"},
                {"slot": 4, "id": "mr-004", "status": "pending"},
            ]
        ),
        "monster-recast",
    )

    assert summary["pending_with_render_gate_error"] == 2
    assert summary["pending_without_render_gate_error"] == 2
    assert [entry["id"] for entry in summary["next_batch"]] == ["mr-003", "mr-004"]
    assert [entry["id"] for entry in summary["blocked_pending"]] == ["mr-001", "mr-002"]
    assert [entry["id"] for entry in summary["recovery_candidates"]] == ["mr-001"]
    assert summary["recovery_candidates"][0]["render_gate_job_id"] == 2474
    assert summary["recovery_candidate_count"] == 1
    assert [entry["id"] for entry in summary["recovery_batch"]] == ["mr-001"]
    assert summary["recovery_actionable"] is True
    assert summary["recovery_actionable_count"] == 1
    assert [entry["id"] for entry in summary["fresh_submission_blocked"]] == ["mr-002"]
    assert summary["fresh_submission_blocked_count"] == 1
    assert summary["recovery_safe"] is True
    assert summary["retry_safe"] is False
    assert summary["actionable"] is False
    assert summary["actionable_count"] == 0
    assert summary["recommended_action"] == "recover-existing-jobs"


def test_recovery_batch_is_bounded_by_worker_pass_size():
    summary = summarize_queue(
        queue(
            [
                {"slot": 1, "id": "mr-001", "status": "pending", "render_gate_error": "job 2474 timed out"},
                {"slot": 2, "id": "mr-002", "status": "pending", "render_gate_error": "job 2475 timed out"},
                {"slot": 3, "id": "mr-003", "status": "pending", "render_gate_error": "job 2476 timed out"},
            ]
        ),
        "monster-recast",
    )

    assert summary["recovery_candidate_count"] == 3
    assert [entry["id"] for entry in summary["recovery_batch"]] == ["mr-001", "mr-002"]
    assert summary["recovery_actionable"] is True
    assert summary["recovery_actionable_count"] == 2


def test_duplicate_job_ids_make_recovery_unsafe():
    summary = summarize_queue(
        queue(
            [
                {"slot": 1, "id": "mr-001", "status": "pending", "render_gate_error": "Job #2474 timed out"},
                {"slot": 2, "id": "mr-002", "status": "pending", "render_gate_error": "job 2474 still running"},
            ]
        ),
        "monster-recast",
    )

    assert summary["duplicate_render_gate_job_ids"] == [2474]
    assert summary["next_batch"] == []
    assert summary["recovery_safe"] is False
    assert summary["recovery_candidate_count"] == 0
    assert summary["recovery_batch"] == []
    assert summary["recovery_actionable"] is False
    assert summary["recovery_actionable_count"] == 0
    assert summary["retry_safe"] is False
    assert summary["actionable"] is False
    assert summary["actionable_count"] == 0
    assert summary["recommended_action"] == "repair-queue-integrity"


def test_duplicate_entry_ids_make_queue_unsafe():
    summary = summarize_queue(
        queue(
            [
                {"slot": 1, "id": "mr-001", "status": "pending"},
                {"slot": 2, "id": "mr-001", "status": "pending"},
            ]
        ),
        "monster-recast",
    )

    assert summary["duplicate_entry_ids"] == ["mr-001"]
    assert summary["duplicate_slots"] == []
    assert summary["queue_integrity_safe"] is False
    assert summary["recovery_safe"] is False
    assert summary["retry_safe"] is False
    assert summary["actionable"] is False


def test_duplicate_slots_make_queue_unsafe():
    summary = summarize_queue(
        queue(
            [
                {"slot": 1, "id": "mr-001", "status": "pending"},
                {"slot": 1, "id": "mr-002", "status": "pending"},
            ]
        ),
        "monster-recast",
    )

    assert summary["duplicate_entry_ids"] == []
    assert summary["duplicate_slots"] == [1]
    assert summary["queue_integrity_safe"] is False
    assert summary["recovery_safe"] is False
    assert summary["retry_safe"] is False
    assert summary["actionable"] is False


def test_empty_safe_queue_is_not_actionable():
    summary = summarize_queue(queue([{"slot": 1, "id": "mr-001", "status": "approved"}]), "monster-recast")

    assert summary["retry_safe"] is True
    assert summary["next_batch"] == []
    assert summary["actionable"] is False
    assert summary["actionable_count"] == 0
    assert summary["recovery_candidate_count"] == 0
    assert summary["recovery_batch"] == []
    assert summary["recovery_actionable"] is False
    assert summary["recommended_action"] == "complete"


def test_recommended_action_requirement_matches_exactly():
    summary = {"recommended_action": "recover-existing-jobs"}

    assert requirement_satisfied(summary, None) is True
    assert requirement_satisfied(summary, "recover-existing-jobs") is True
    assert requirement_satisfied(summary, "submit-next-batch") is False


def test_batch_size_must_be_positive():
    try:
        summarize_queue(queue([]), "monster-recast", batch_size=-1)
    except ValueError as error:
        assert str(error) == "batch size must be at least 1"
    else:
        raise AssertionError("expected ValueError")


def test_unknown_book_raises_value_error():
    try:
        summarize_queue(queue([]), "missing")
    except ValueError as error:
        assert str(error) == "book not found: missing"
    else:
        raise AssertionError("expected ValueError")


def test_no_path_field_is_not_flagged_as_missing():
    # Mirrors real fixtures/tests elsewhere in this file that omit
    # image_path/rendered_path entirely -- nothing to check means no finding,
    # not a false positive.
    assert has_missing_file({"status": "approved"}) is False
    assert has_missing_file({"status": "needs_review"}) is False


def test_pending_entry_with_no_file_yet_is_not_flagged():
    # A `pending` entry is never expected to have a rendered file yet.
    assert has_missing_file({"status": "pending", "image_path": "/nonexistent/path.webp"}) is False


def test_resolved_entry_with_existing_file_is_not_flagged(tmp_path):
    real_file = tmp_path / "mr-001-color.webp"
    real_file.write_bytes(b"fake")
    assert has_missing_file({"status": "done", "rendered_path": str(real_file)}) is False


def test_resolved_entry_with_missing_file_is_flagged(tmp_path):
    missing = tmp_path / "mr-008-game-mistress.webp"
    for status in ("needs_review", "done"):
        assert has_missing_file({"status": status, "image_path": str(missing)}) is True


def test_approved_entry_with_missing_queue_path_is_not_flagged(tmp_path):
    # Once accepted, proposals.yaml's accepted.color is authoritative and may
    # legitimately diverge from this queue entry's own (now-stale) path --
    # see the RESOLVED_STATUSES_EXPECTING_A_FILE comment for the real
    # mr-002/mr-003/mr-004 case this guards against.
    missing = tmp_path / "renamed-away.webp"
    assert has_missing_file({"status": "approved", "image_path": str(missing)}) is False


def test_summarize_queue_reports_missing_file_entries(tmp_path):
    missing = tmp_path / "mr-008-game-mistress.webp"
    summary = summarize_queue(
        queue(
            [
                {"slot": 8, "id": "mr-008", "status": "needs_review", "image_path": str(missing)},
                {"slot": 9, "id": "mr-009", "status": "approved"},
            ]
        ),
        "monster-recast",
    )

    assert summary["missing_file_count"] == 1
    assert [entry["id"] for entry in summary["missing_file_entries"]] == ["mr-008"]
    assert summary["missing_file_entries"][0]["referenced_path"] == str(missing)
    assert summary["recommended_action"] == "repair-missing-file"


def test_require_no_missing_files_flag_via_recommended_action():
    summary = {"recommended_action": "repair-missing-file"}
    assert requirement_satisfied(summary, "repair-missing-file") is True
    assert requirement_satisfied(summary, "complete") is False
