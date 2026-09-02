from pathlib import Path

from scripts.check_hostbuf_failure import hostbuf_failure_count


WORKFLOW = Path(".github/workflows/render-hostbuf-sentinel.yml")


def test_hostbuf_failure_count_prefers_api_signature_groups():
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


def test_hostbuf_failure_count_is_zero_when_signature_absent():
    assert hostbuf_failure_count({"recentFailed": []}) == 0


def test_hostbuf_workflow_installs_runtime_dependency():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "python -m pip install PyYAML" in workflow


def test_hostbuf_workflow_uses_current_production_api_base():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "KR_BASE_URL: https://kind-robots.vercel.app" in workflow
    assert "KR_BASE_URL: https://kindrobots.org" not in workflow
