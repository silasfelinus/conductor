from scripts.coloring_queue_status import summarize_queue


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
    assert summary["retry_safe"] is True


def test_semantic_gate_errors_make_retry_unsafe():
    summary = summarize_queue(
        queue(
            [
                {
                    "slot": 1,
                    "id": "mr-001",
                    "status": "pending",
                    "semantic_gate_error": "job 2474 timed out after 600s (still queued/running)",
                    "semantic_gate_error_at": "2026-07-26T12:18:00Z",
                }
            ]
        ),
        "monster-recast",
    )

    assert summary["pending_with_semantic_gate_error"] == 1
    assert summary["pending_without_semantic_gate_error"] == 0
    assert summary["retry_safe"] is False


def test_duplicate_job_ids_are_reported():
    summary = summarize_queue(
        queue(
            [
                {"slot": 1, "id": "mr-001", "status": "pending", "semantic_gate_error": "job 2474 timed out"},
                {"slot": 2, "id": "mr-002", "status": "pending", "semantic_gate_error": "job 2474 timed out"},
            ]
        ),
        "monster-recast",
    )

    assert summary["duplicate_semantic_gate_job_ids"] == [2474]
    assert summary["retry_safe"] is False


def test_unknown_book_raises_value_error():
    try:
        summarize_queue(queue([]), "missing")
    except ValueError as error:
        assert str(error) == "book not found: missing"
    else:
        raise AssertionError("expected ValueError")
