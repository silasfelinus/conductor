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
    assert summary["blocked_pending"] == []
    assert summary["retry_safe"] is True


def test_semantic_gate_errors_are_blocked_and_excluded_from_next_batch():
    summary = summarize_queue(
        queue(
            [
                {
                    "slot": 1,
                    "id": "mr-001",
                    "status": "pending",
                    "semantic_gate_error": "job 2474 timed out after 600s (still queued/running)",
                    "semantic_gate_error_at": "2026-07-26T12:18:00Z",
                },
                {"slot": 2, "id": "mr-002", "status": "pending"},
                {"slot": 3, "id": "mr-003", "status": "pending"},
            ]
        ),
        "monster-recast",
    )

    assert summary["pending_with_semantic_gate_error"] == 1
    assert summary["pending_without_semantic_gate_error"] == 2
    assert [entry["id"] for entry in summary["next_batch"]] == ["mr-002", "mr-003"]
    assert [entry["id"] for entry in summary["blocked_pending"]] == ["mr-001"]
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
    assert summary["next_batch"] == []
    assert summary["retry_safe"] is False


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
