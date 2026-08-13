import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "repair_failed_kindrobots_artjobs.py"
spec = importlib.util.spec_from_file_location("repair_failed_kindrobots_artjobs", SCRIPT)
repair = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(repair)


def test_failure_diagnostic_is_prompt_free_and_bounded():
    job = {
        "id": 7622,
        "engine": "COMFY",
        "error": "x" * 1500,
        "payload": {"promptString": "SECRET PROMPT SHOULD NOT APPEAR"},
    }
    diagnostic = repair.failure_diagnostic(job)
    assert diagnostic.startswith("ArtJob 7622: engine=COMFY; error=")
    assert "SECRET PROMPT" not in diagnostic
    assert diagnostic.endswith("…")
    assert len(diagnostic) < repair.DIAGNOSTIC_ERROR_LIMIT + 100


def test_failure_diagnostic_collapses_error_whitespace():
    diagnostic = repair.failure_diagnostic(
        {"id": 8116, "engine": "A1111", "error": "connection\n refused\t now"}
    )
    assert diagnostic == "ArtJob 8116: engine=A1111; error=connection refused now"


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
