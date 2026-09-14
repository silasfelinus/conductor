from datetime import datetime, timezone
from pathlib import Path

from scripts.check_hostbuf_failure import hostbuf_failure_count, hostbuf_state


WORKFLOW = Path(".github/workflows/render-hostbuf-sentinel.yml")


def test_hostbuf_failure_count_prefers_api_signature_groups_without_window_metadata():
    data = {
        "recentFailed": [{"error": "unrelated"}],
        "failuresBySignature": [
            {"signature": "hostbuf-file-reader-read", "count": 3},
            {"signature": "workflow-error-other", "count": 1},
        ],
    }
    assert hostbuf_failure_count(data) == 3


def test_hostbuf_failure_count_falls_back_to_raw_recent_failures():
    data = {
        "recentFailed": [
            {"error": "Workflow error: hostbuf_file_reader_read failed", "projectSlug": "x"},
            {"error": "some other failure", "projectSlug": "y"},
        ]
    }
    assert hostbuf_failure_count(data) == 1


def test_hostbuf_failure_count_ignores_stale_failures_even_if_api_group_contains_them():
    data = {
        "since": "2026-09-13T20:00:00Z",
        "recentFailed": [
            {
                "error": "Workflow error: hostbuf_file_reader_read failed",
                "projectSlug": "x",
                "updatedAt": "2026-09-13T18:30:00Z",
            },
            {
                "error": "some other failure",
                "projectSlug": "y",
                "updatedAt": "2026-09-13T21:00:00Z",
            },
        ],
        "failuresBySignature": [
            {"signature": "hostbuf-file-reader-read", "count": 1},
        ],
    }
    assert hostbuf_failure_count(data) == 0


def test_hostbuf_failure_count_keeps_fresh_failures_inside_requested_window():
    data = {
        "since": "2026-09-13T20:00:00Z",
        "recentFailed": [
            {
                "error": "Workflow error: hostbuf_file_reader_read failed",
                "projectSlug": "x",
                "updatedAt": "2026-09-13T20:30:00Z",
            },
            {
                "error": "Workflow error: hostbuf_file_reader_read failed",
                "projectSlug": "x",
                "updatedAt": "2026-09-13T19:59:59Z",
            },
        ],
    }
    assert hostbuf_failure_count(data) == 1


def test_hostbuf_failure_count_is_zero_when_signature_absent():
    assert hostbuf_failure_count({"recentFailed": []}) == 0


def test_hostbuf_state_is_recovered_only_when_done_is_newer_than_failure():
    data = {
        "latestHostbufFailureAt": "2026-09-14T05:00:00Z",
        "latestDoneAt": "2026-09-14T05:01:00Z",
    }
    assert hostbuf_state(data) == "recovered"


def test_hostbuf_state_is_not_recovered_by_an_older_done_job():
    data = {
        "latestHostbufFailureAt": "2026-09-14T05:00:00Z",
        "latestDoneAt": "2026-09-14T04:59:59Z",
    }
    now = datetime(2026, 9, 14, 5, 30, tzinfo=timezone.utc)
    assert hostbuf_state(data, now=now) == "fresh-failure"


def test_hostbuf_state_becomes_unverified_not_clear_when_incident_ages_out_without_success():
    data = {
        "latestHostbufFailureAt": "2026-09-14T02:00:00Z",
        "latestDoneAt": "2026-09-14T01:59:00Z",
    }
    now = datetime(2026, 9, 14, 5, 0, tzinfo=timezone.utc)
    assert hostbuf_state(data, now=now) == "unverified"


def test_hostbuf_state_falls_back_to_recent_sample_before_api_fields_deploy():
    data = {
        "since": "2026-09-14T03:00:00Z",
        "recentFailed": [
            {
                "error": "Workflow error: hostbuf_file_reader_read failed",
                "updatedAt": "2026-09-14T04:00:00Z",
            }
        ],
    }
    assert hostbuf_state(data) == "fresh-failure"


def test_hostbuf_workflow_installs_runtime_dependency():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "python -m pip install PyYAML" in workflow


def test_hostbuf_workflow_uses_kindrobots_domain_not_vercel():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "KR_BASE_URL: https://kindrobots.org" in workflow
    assert "kind-robots.vercel.app" not in workflow
