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


def test_wait_for_daily_dream_jobs_uses_one_global_deadline():
    states = {
        101: [{"status": "QUEUED"}, {"status": "DONE"}],
        102: [{"status": "DONE"}],
        103: [{"status": "FAILED"}],
        104: [{"status": "RUNNING"}, {"status": "RUNNING"}],
    }
    now = [0.0]

    def fetch(job_id, timeout=10):
        rows = states[job_id]
        return rows.pop(0) if len(rows) > 1 else rows[0]

    def sleep(seconds):
        now[0] += seconds

    done, failed, pending = submit.wait_for_daily_dream_jobs(
        {job_id: str(job_id) for job_id in states},
        timeout=6,
        fetch_job=fetch,
        poll_seconds=5,
        sleeper=sleep,
        clock=lambda: now[0],
    )

    assert done == {101, 102}
    assert failed == {103: "FAILED"}
    assert pending == {104}
    assert now[0] == 6
