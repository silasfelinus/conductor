"""Private fidelity pilot capture must preserve provenance and keep queued work pending."""
import importlib.util
from pathlib import Path

import pytest

pytest.importorskip("PIL")

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "projects/shifting-desks/art/build_recovery_sheets.py"
spec = importlib.util.spec_from_file_location("shifting_recovery_sheets", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_v1_historical_pilot_is_not_replaced_by_v2():
    old = list(module.pilot_rows(1))
    assert len(old) == 6
    assert all(row["_round"] == "PILOT-V1" for row in old)
    assert all(row["status"] == "DONE" and row["image"] for row in old)


def test_v2_subject_only_pilot_has_three_isolated_queued_jobs():
    rows = list(module.pilot_rows(2))
    assert len(rows) == 3
    assert {row["key"] for row in rows} == {
        "rear-eyes--krea-prose",
        "living-corridor--krea-prose",
        "mutation-tank--krea-prose",
    }
    assert {row["job"] for row in rows} == {69090, 69091, 69092}
    assert all(row["_round"] == "PILOT-V2" for row in rows)
    assert all(row["pass"] and row["fail"] for row in rows)
    assert all(row["verdict"] == "REDO" for row in rows)
    assert all(row["review_note"] and "ArtImage" in row["review_note"] for row in rows)
    assert {row["evidence_artifact_id"] for row in rows} == {14164533392}


def test_pending_v2_jobs_cannot_be_passed_off_as_delivered(monkeypatch):
    rows = list(module.pilot_rows(2))
    monkeypatch.setattr(module, "fetch_source_image", lambda _: (_ for _ in ()).throw(AssertionError("unexpected media fetch")))
    for row in rows:
        if row["status"] == "PENDING":
            image, evidence = module.capture_pilot(row)
            assert image is None
            assert "DONE" in evidence["error"]


def test_unknown_pilot_version_fails_closed():
    with pytest.raises(ValueError, match="unsupported"):
        list(module.pilot_rows(6))


def test_done_pilot_artimages_cannot_disappear_from_review_artifact():
    good = {
        "pilot_v1_captured": 6, "pilot_v1_recorded_done": 6,
        "pilot_v1_done_missing_image": 0,
        "pilot_v2_captured": 3, "pilot_v2_recorded_done": 3,
        "pilot_v2_done_missing_image": 0,
        "pilot_v3_captured": 3, "pilot_v3_recorded_done": 3,
        "pilot_v3_done_missing_image": 0,
        "pilot_v4_captured": 0, "pilot_v4_recorded_done": 0,
        "pilot_v4_done_missing_image": 0,
        "pilot_v5_captured": 0, "pilot_v5_recorded_done": 0,
        "pilot_v5_done_missing_image": 0,
    }
    assert module.pilot_capture_errors(good) == []
    missing = {**good, "pilot_v2_captured": 2}
    assert module.pilot_capture_errors(missing) == [
        "pilot_v2: captured 2/3 delivered ArtImages"
    ]
    missing_id = {**good, "pilot_v1_done_missing_image": 1}
    assert module.pilot_capture_errors(missing_id) == [
        "pilot_v1: DONE ArtJob missing an ArtImage ID"
    ]


def test_queued_pilot_is_not_counted_as_a_failed_delivery():
    report = {
        "pilot_v1_captured": 6, "pilot_v1_recorded_done": 6,
        "pilot_v1_done_missing_image": 0,
        "pilot_v2_captured": 2, "pilot_v2_recorded_done": 2,
        "pilot_v2_done_missing_image": 0,
        "pilot_v3_captured": 3, "pilot_v3_recorded_done": 3,
        "pilot_v3_done_missing_image": 0,
        "pilot_v4_captured": 0, "pilot_v4_recorded_done": 0,
        "pilot_v4_done_missing_image": 0,
        "pilot_v5_captured": 0, "pilot_v5_recorded_done": 0,
        "pilot_v5_done_missing_image": 0,
    }
    assert module.pilot_capture_errors(report) == []


def test_v3_sdxl_img2img_pilot_records_all_three_rendered_sources():
    """Every new DONE img2img candidate must appear with verifiable source lineage."""
    rows = list(module.pilot_rows(3))
    assert len(rows) == 3
    assert {row["key"] for row in rows} == {
        "rear-eyes-edit--dreamshaper-turbo-i2i",
        "living-doors-edit--dreamshaper-turbo-i2i",
        "three-arm-tank-edit--dreamshaper-turbo-i2i",
    }
    assert {row["job"] for row in rows} == {69431, 69432, 69433}
    assert {row["image"] for row in rows} == {273305, 273306, 273307}
    assert {row["source_image_id"] for row in rows} == {
        271721, 271722, 271723,
    }
    assert {row["source_art_job_id"] for row in rows} == {
        69090, 69091, 69092,
    }
    assert all(row["status"] == "DONE" for row in rows)
    assert all(row["verdict"] == "REDO" for row in rows)
    assert all(row["pass"] and row["fail"] for row in rows)
    assert all("ArtImage" in row["review_note"] for row in rows)
    assert {row["evidence_artifact_id"] for row in rows} == {
        14189401216,
    }
    assert all(row["denoise"] > 0 for row in rows)
    assert all(row["checkpoint"].endswith(".safetensors") for row in rows)
    assert all(row["asset"].startswith("shifting-desks/private-") for row in rows)
    assert all(row["_round"] == "PILOT-V3" for row in rows)


def test_img2img_done_image_missing_from_evidence_is_blocking():
    report = {
        "pilot_v1_captured": 6, "pilot_v1_recorded_done": 6,
        "pilot_v1_done_missing_image": 0,
        "pilot_v2_captured": 3, "pilot_v2_recorded_done": 3,
        "pilot_v2_done_missing_image": 0,
        "pilot_v3_captured": 2, "pilot_v3_recorded_done": 3,
        "pilot_v3_done_missing_image": 0,
        "pilot_v4_captured": 0, "pilot_v4_recorded_done": 0,
        "pilot_v4_done_missing_image": 0,
        "pilot_v5_captured": 0, "pilot_v5_recorded_done": 0,
        "pilot_v5_done_missing_image": 0,
    }
    assert module.pilot_capture_errors(report) == [
        "pilot_v3: captured 2/3 delivered ArtImages"
    ]


def test_v4_krea_img2img_pilot_is_private_source_referenced_and_replay_safe():
    rows = list(module.pilot_rows(4))
    assert len(rows) == 3
    assert {row["key"] for row in rows} == {
        "rear-eyes--krea2-source-edit",
        "living-doors--krea2-source-edit",
        "three-arm-tank--krea2-source-edit",
    }
    assert {row["source_image_id"] for row in rows} == {
        271721, 271722, 271723,
    }
    assert {row["source_art_job_id"] for row in rows} == {
        69090, 69091, 69092,
    }
    assert all(row["_round"] == "PILOT-V4" for row in rows)
    assert all(row["pass"] and row["fail"] for row in rows)
    assert all(row["lane"] == "krea2-source-edit" for row in rows)
    assert all(row["checkpoint"] is None for row in rows)
    assert all(0.6 <= row["denoise"] <= 0.72 for row in rows)
    assert all(row["asset"].startswith("shifting-desks/private-") for row in rows)
    assert all(row["job"] is None or row["job"] > 0 for row in rows)
    assert all(row["image"] is None or row["image"] > 0 for row in rows)
    assert all(row["verdict"] in (None, "KEEP", "REDO") for row in rows)


def test_v4_finished_art_without_image_is_not_marked_captured():
    report = {
        "pilot_v1_captured": 6, "pilot_v1_recorded_done": 6,
        "pilot_v1_done_missing_image": 0,
        "pilot_v2_captured": 3, "pilot_v2_recorded_done": 3,
        "pilot_v2_done_missing_image": 0,
        "pilot_v3_captured": 3, "pilot_v3_recorded_done": 3,
        "pilot_v3_done_missing_image": 0,
        "pilot_v4_captured": 1, "pilot_v4_recorded_done": 2,
        "pilot_v4_done_missing_image": 1,
    }
    assert module.pilot_capture_errors(report) == [
        "pilot_v4: captured 1/2 delivered ArtImages",
        "pilot_v4: DONE ArtJob missing an ArtImage ID",
    ]


def test_visual_review_runs_after_art_sweep_status_checkpoints_skip_ci():
    workflow = (
        ROOT / ".github/workflows/shifting-desks-art-visual-review.yml"
    ).read_text(encoding="utf-8")
    assert "workflow_run:" in workflow
    assert 'workflows: ["Auto Art Generate"]' in workflow
    assert "github.event.workflow_run.head_branch == 'main'" in workflow
    assert '"projects/shifting-desks/art/KREA-IMG2IMG-CORRECTION-PILOT-1.yaml"' in workflow


def test_v5_masked_kontext_candidate_capture_preserves_edit_regions():
    rows = list(module.pilot_rows(5))
    assert len(rows) == 3
    assert {row["key"] for row in rows} == {
        "rear-eyes--kontext-localized",
        "living-doors--kontext-localized",
        "three-arm-tank--kontext-localized",
    }
    assert {row["source_image_id"] for row in rows} == {
        273605, 273606, 273607,
    }
    assert {row["source_art_job_id"] for row in rows} == {
        69448, 69449, 69450,
    }
    assert all(row["_round"] == "PILOT-V5" for row in rows)
    assert all(row["pass"] and row["fail"] for row in rows)
    assert all(row["mask_box"] for row in rows)
    assert {len(row["mask_box"]) for row in rows} == {1, 2, 3}
    assert all(row["job"] is None or row["job"] > 0 for row in rows)
    assert all(row["image"] is None or row["image"] > 0 for row in rows)
    assert all(row["verdict"] in (None, "KEEP", "REDO") for row in rows)


def test_v5_finished_image_without_pixels_is_a_review_error():
    report = {
        "pilot_v1_captured": 6, "pilot_v1_recorded_done": 6,
        "pilot_v1_done_missing_image": 0,
        "pilot_v2_captured": 3, "pilot_v2_recorded_done": 3,
        "pilot_v2_done_missing_image": 0,
        "pilot_v3_captured": 3, "pilot_v3_recorded_done": 3,
        "pilot_v3_done_missing_image": 0,
        "pilot_v4_captured": 3, "pilot_v4_recorded_done": 3,
        "pilot_v4_done_missing_image": 0,
        "pilot_v5_captured": 2, "pilot_v5_recorded_done": 3,
        "pilot_v5_done_missing_image": 0,
    }
    assert module.pilot_capture_errors(report) == [
        "pilot_v5: captured 2/3 delivered ArtImages"
    ]
