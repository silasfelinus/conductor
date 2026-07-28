from scripts.coloring_queue_status import summarize_queue


def queue(entries):
    return {
        "batch_policy": {"worker_pass_size": 2},
        "books": [{"slug": "monster-recast", "entries": entries}],
    }


def recommendation(entries):
    return summarize_queue(queue(entries), "monster-recast")["recommended_action"]


def test_recommends_integrity_repair_before_any_processing():
    assert (
        recommendation(
            [
                {"slot": 1, "id": "mr-001", "status": "pending"},
                {"slot": 1, "id": "mr-002", "status": "pending"},
            ]
        )
        == "repair-queue-integrity"
    )


def test_recommends_recovering_existing_jobs_before_fresh_submissions():
    assert (
        recommendation(
            [
                {"slot": 1, "id": "mr-001", "status": "pending", "semantic_gate_error": "job 2474 timed out"},
                {"slot": 2, "id": "mr-002", "status": "pending"},
            ]
        )
        == "recover-existing-jobs"
    )


def test_recommends_resolving_enqueue_errors_without_job_ids():
    assert (
        recommendation(
            [
                {
                    "slot": 1,
                    "id": "mr-001",
                    "status": "pending",
                    "semantic_gate_error": "enqueue failed: HTTP 503",
                }
            ]
        )
        == "resolve-fresh-submission-errors"
    )


def test_recommends_fresh_batch_only_for_clean_pending_entries():
    assert recommendation([{"slot": 1, "id": "mr-001", "status": "pending"}]) == "submit-next-batch"


def test_recommends_complete_when_no_entries_are_pending():
    assert recommendation([{"slot": 1, "id": "mr-001", "status": "approved"}]) == "complete"
