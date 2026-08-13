import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "repair_failed_kindrobots_artjobs.py"
spec = importlib.util.spec_from_file_location("repair_failed_kindrobots_artjobs", SCRIPT)
repair = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(repair)


def test_failure_diagnostic_is_prompt_free_and_bounded():
    job = {
        "id": 9000,
        "engine": "COMFY",
        "error": "x" * 1500,
        "payload": {"promptString": "SECRET PROMPT SHOULD NOT APPEAR"},
    }
    diagnostic = repair.failure_diagnostic(job)
    assert diagnostic.startswith("ArtJob 9000: engine=COMFY; error=")
    assert "SECRET PROMPT" not in diagnostic
    assert diagnostic.endswith("…")
    assert len(diagnostic) < repair.DIAGNOSTIC_ERROR_LIMIT + 100


def test_failure_diagnostic_collapses_error_whitespace():
    diagnostic = repair.failure_diagnostic(
        {"id": 9001, "engine": "A1111", "error": "connection\n refused\t now"}
    )
    assert diagnostic == "ArtJob 9001: engine=A1111; error=connection refused now"


def test_repair_reasons_remains_default_deny_for_unrelated_failure():
    job = {
        "id": 42,
        "engine": "COMFY",
        "error": "ComfyUI value_not_in_list",
        "payload": {
            "targetRepo": repair.KIND_ROBOTS_REPO,
            "imagePath": "public/images/example.webp",
            "promptString": "a clear illustration of a lighthouse",
        },
    }
    assert repair.repair_reasons(job) == []


def test_duplicate_cleanup_keeps_first_when_statuses_tie():
    first = {"id": 8276, "status": "PENDING"}
    second = {"id": 8277, "status": "PENDING"}
    assert repair.choose_duplicate_keeper(first, second) is first


def test_duplicate_cleanup_keeps_running_over_pending():
    first = {"id": 8276, "status": "PENDING"}
    second = {"id": 8277, "status": "RUNNING"}
    assert repair.choose_duplicate_keeper(first, second) is second


def test_duplicate_cleanup_keeps_done_over_running():
    first = {"id": 8278, "status": "DONE"}
    second = {"id": 8279, "status": "RUNNING"}
    assert repair.choose_duplicate_keeper(first, second) is first


def test_duplicate_cleanup_prefers_pending_over_failed():
    first = {"id": 8278, "status": "FAILED"}
    second = {"id": 8279, "status": "PENDING"}
    assert repair.choose_duplicate_keeper(first, second) is second
