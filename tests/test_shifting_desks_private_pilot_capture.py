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
        list(module.pilot_rows(8))


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
        "pilot_v5_captured": 0, "pilot_v5_recorded_done": 0,
        "pilot_v5_done_missing_image": 0,
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
    assert '"projects/shifting-desks/art/KONTEXT-MASKED-CORRECTION-PILOT-1.yaml"' in workflow
    assert '"projects/shifting-desks/art/SDXL-TARGETED-CORRECTION-PILOT-1.yaml"' in workflow
    assert '"projects/shifting-desks/art/SDXL-MASKED-VAE-CORRECTION-PILOT-2.yaml"' in workflow


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


def test_v6_sdxl_targeted_pilot_has_rendered_source_and_mask():
    rows = list(module.pilot_rows(6))
    assert len(rows) == 1
    (row,) = rows
    assert row["_round"] == "PILOT-V6"
    assert row["key"] == "three-arm-tank--sdxl-targeted-local"
    assert row["job"] == 69681
    assert row["image"] == 274183
    assert row["status"] == "DONE"
    assert row["verdict"] == "REDO"
    assert row["evidence_artifact_id"] == 14293774749
    assert "two arms" in row["review_note"]
    assert row["source_image_id"] == 273631
    assert row["source_art_job_id"] == 69458
    assert row["mask_box"] == [[0.36, 0.58, 0.70, 0.80]]
    assert row["target_regions"][0]["bleedPx"] == 16
    assert row["target_regions"][0]["featherPx"] == 10
    assert row["checkpoint"].endswith(".safetensors")
    assert row["pass"] and row["fail"]
    assert row["asset"].startswith("shifting-desks/private-")


def test_v6_requires_full_image_evidence_not_merely_a_done_status():
    recorded = {
        "pilot_v6_captured": 0,
        "pilot_v6_recorded_done": 1,
        "pilot_v6_done_missing_image": 0,
    }
    assert module.pilot_capture_errors(recorded) == [
        "pilot_v6: captured 0/1 delivered ArtImages"
    ]
    recorded["pilot_v6_captured"] = 1
    assert module.pilot_capture_errors(recorded) == []


def test_v7_masked_vae_capture_is_private_and_artjob_provenanced():
    rows = list(module.pilot_rows(7))
    assert len(rows) == 1
    (row,) = rows
    assert row["_round"] == "PILOT-V7"
    assert row["key"] == "three-arm-tank-recomposition--sdxl-masked-vae"
    assert row["source_image_id"] == 273631
    assert row["source_art_job_id"] == 69458
    assert row["mask_box"] == [
        [0.18, 0.25, 0.42, 0.50],
        [0.34, 0.53, 0.72, 0.78],
    ]
    assert len(row["target_regions"]) == 2
    assert row["checkpoint"].endswith(".safetensors")
    assert row["pass"] and row["fail"]
    assert row["asset"].startswith("shifting-desks/private-")
    assert row["job"] is None or row["job"] > 0
    assert row["image"] is None or row["image"] > 0
    assert row["job"] == 69726
    assert row["image"] == 274359
    assert row["status"] == "DONE"
    assert row["verdict"] == "REDO"
    assert row["evidence_artifact_id"] == 14345505662
    assert "only TWO attached arms" in row["review_note"]
    assert "composition failed" in row["review_note"]


def test_v7_completed_image_missing_pixel_evidence_is_blocking():
    report = {
        "pilot_v7_recorded_done": 1,
        "pilot_v7_captured": 0,
        "pilot_v7_done_missing_image": 0,
    }
    assert module.pilot_capture_errors(report) == [
        "pilot_v7: captured 0/1 delivered ArtImages"
    ]
    report["pilot_v7_captured"] = 1
    assert module.pilot_capture_errors(report) == []

def test_targeted_pixel_capture_flags_a_real_near_no_op(monkeypatch):
    import base64
    import io
    from PIL import Image

    original = Image.new("RGB", (80, 80), "#527891")
    buffer = io.BytesIO()
    original.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    monkeypatch.setattr(
        module, "fetch_source_image",
        lambda _: "data:image/png;base64," + encoded,
    )
    row = {
        "_round": "PILOT-V6",
        "source_image_id": 273631,
        "target_regions": [{
            "type": "box", "box": [0.25, 0.25, 0.75, 0.75],
            "bleedPx": 0,
        }],
    }
    delta = module.targeted_pixel_delta(row, original.copy())
    assert delta["assessment"] == "REDO_NO_OP"
    assert delta["mean_absolute_rgb_in_mask"] == 0
    assert delta["changed_fraction_at_16_in_mask"] == 0
    assert delta["near_no_op"] is True

    improved = original.copy()
    for x in range(30, 50):
        for y in range(30, 50):
            improved.putpixel((x, y), (240, 50, 75))
    report = module.targeted_pixel_delta(row, improved)
    assert report["assessment"] == "VISUAL_REVIEW_REQUIRED"
    assert report["mean_absolute_rgb_in_mask"] > 3
    assert report["changed_fraction_at_16_in_mask"] > 0.1
    assert report["near_no_op"] is False
    assert "KEEP" in report["note"]


def test_targeted_pixel_capture_fails_closed_without_valid_mask():
    row = {
        "_round": "PILOT-V7",
        "source_image_id": 273631,
        "target_regions": [{"type": "polygon", "points": []}],
    }
    from PIL import Image
    result = module.targeted_pixel_delta(row, Image.new("RGB", (80, 80)))
    assert result["assessment"] == "UNVERIFIED"
    assert module.pilot_capture_errors({
        "pilot_v7_pixel_unverified": 1,
    }) == ["pilot_v7: delivered edit lacks measured source pixels"]
