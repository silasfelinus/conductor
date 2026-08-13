import importlib.util
from pathlib import Path

import pytest

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


def test_incident_retry_plan_is_exact_and_presets_obsolete_a1111_to_krea2():
    plan = repair.incident_retry_plan(
        {
            "id": 8116,
            "engine": "A1111",
            "error": "<urlopen error [WinError 10061] actively refused>",
        }
    )
    assert plan is not None
    assert plan["body"]["preset"] == "krea2"
    assert plan["body"]["mode"] == "NEW_OUTPUT"


def test_incident_retry_plan_preserves_kontext_workflow_for_lora_probe():
    plan = repair.incident_retry_plan(
        {
            "id": 7622,
            "engine": "COMFY",
            "error": "lora_name: 'Kontext/SFW/acrylic.safetensors' not in list",
        }
    )
    assert plan is not None
    assert "preset" not in plan["body"]
    assert plan["body"]["refreshSeed"] is False


def test_incident_retry_plan_fails_closed_if_reviewed_row_drifted():
    with pytest.raises(RuntimeError, match="refusing automatic retry"):
        repair.incident_retry_plan(
            {
                "id": 7623,
                "engine": "COMFY",
                "error": "a different failure entirely",
            }
        )


def test_incident_retry_plan_ignores_unreviewed_ids():
    assert repair.incident_retry_plan(
        {"id": 9999, "engine": "COMFY", "error": "value_not_in_list"}
    ) is None
