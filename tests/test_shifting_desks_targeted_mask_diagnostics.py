"""Real masked-edit diagnostic measurements must fail closed on bad masks."""
import importlib.util
from pathlib import Path

import pytest

pytest.importorskip("PIL")
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "targeted_probe", ROOT / "projects/shifting-desks/art/diagnose_targeted_edit.py"
)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


def setup_case(edit=True):
    source = Image.new("RGB", (128, 128), "#527891")
    changed = source.copy()
    if edit:
        ImageDraw.Draw(changed).rectangle((40, 40, 71, 71), fill="#ff1122")
    mask = Image.new("L", (80, 80), 0)
    ImageDraw.Draw(mask).rectangle((32, 32, 63, 63), fill=255)
    crop = {"x": 8, "y": 8, "width": 80, "height": 80}
    return source, changed, mask, crop


def test_significant_local_change_inside_mask_only():
    source, changed, mask, crop = setup_case()
    summary = probe.metrics(source, changed, mask, mask, crop)
    assert summary["mask_pixels"] == 1024
    assert summary["inside_changed_fraction_at_16"] == 1.0
    assert summary["outside_changed_fraction_at_16"] == 0.0
    assert summary["nontrivial_edit"] is True


def test_identical_images_not_a_successful_edit():
    source, _, mask, crop = setup_case()
    summary = probe.metrics(source, source, mask, mask, crop)
    assert summary["inside_changed_fraction_at_16"] == 0
    assert summary["nontrivial_edit"] is False


def test_blank_mask_fails_instead_of_counting_render():
    source, changed, _, crop = setup_case()
    blank = Image.new("L", (80, 80), 0)
    with pytest.raises(ValueError, match="nonempty"):
        probe.metrics(source, changed, blank, blank, crop)


def test_feather_cannot_exceed_hard_mask():
    source, changed, hard, crop = setup_case()
    soft = Image.new("L", (80, 80), 255)
    with pytest.raises(ValueError, match="escapes"):
        probe.metrics(source, changed, hard, soft, crop)


def test_crop_cannot_escape_source_frame():
    source, changed, mask, _ = setup_case()
    with pytest.raises(ValueError, match="bounds"):
        probe.metrics(source, changed, mask, mask,
                      {"x": 120, "y": 120, "width": 80, "height": 80})


def test_fully_black_composite_is_reported_as_no_effective_edit_region():
    source, changed, hard, crop = setup_case()
    empty = Image.new("L", hard.size, 0)
    report = probe.metrics(source, changed, hard, empty, crop)
    assert report["mask_pixels"] == 1024
    assert report["soft_mask_pixels"] == 0
    assert report["soft_mask_fraction_of_hard"] == 0.0


def test_soft_mask_reports_nonzero_editable_interior():
    source, changed, hard, crop = setup_case()
    report = probe.metrics(source, changed, hard, hard, crop)
    assert report["mask_pixels"] == report["soft_mask_pixels"] == 1024
    assert report["soft_mask_fraction_of_hard"] == 1.0


def test_v7_pending_is_explicit_and_never_fetches_or_claims_done(tmp_path, monkeypatch):
    import json
    import sys
    import yaml

    ledger = {
        "lanes": [{"key": "sdxl-masked-vae"}],
        "subjects": [{
            "key": "third-arm",
            "source_image_id": 273631,
            "jobs": {},
            "art": {},
        }],
    }
    (tmp_path / "SDXL-MASKED-VAE-CORRECTION-PILOT-2.yaml").write_text(
        yaml.safe_dump(ledger), encoding="utf-8"
    )
    out = tmp_path / "evidence"
    monkeypatch.setattr(probe, "ART", tmp_path)
    monkeypatch.setattr(
        sys, "argv",
        ["diagnose_targeted_edit.py", "--out", str(out), "--pilot-version", "7"],
    )
    assert probe.main() == 0
    data = json.loads((out / "diagnostic.json").read_text())
    assert data["pilot_version"] == 7
    assert data["status"] == "pending"
    assert data["art_job_id"] is None
    assert data["art_image_id"] is None
