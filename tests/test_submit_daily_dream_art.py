import scripts.submit_daily_dream_art as submit


def test_positive_job_id_accepts_only_positive_integers():
    assert submit.positive_job_id(8123) == 8123
    assert submit.positive_job_id("8124") == 8124
    assert submit.positive_job_id(0) is None
    assert submit.positive_job_id(-1) is None
    assert submit.positive_job_id("nope") is None


def test_daily_dream_source_matching_is_tolerant():
    assert submit.is_daily_dream_request({"source": "dream-cycle"})
    assert submit.is_daily_dream_request({"source": " Dream-Cycle "})
    assert not submit.is_daily_dream_request({"source": "kind-robots-missing-image"})


def test_pending_selector_excludes_other_sources_and_completed_rows():
    entries = [
        {"id": "dream-a", "source": "dream-cycle", "status": "pending"},
        {"id": "dream-b", "source": "dream-cycle"},
        {"id": "dream-done", "source": "dream-cycle", "status": "done"},
        {"id": "repair", "source": "kind-robots-missing-image", "status": "pending"},
    ]
    assert [row["id"] for row in submit.pending_daily_dream_requests(entries)] == [
        "dream-a",
        "dream-b",
    ]
