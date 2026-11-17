"""Staged V7 must be private, distinct, and opt into masked-source VAE."""
from pathlib import Path

import yaml

from scripts import enqueue_art_requests as enqueue
from scripts.sweep_art_ledgers import is_auto_ledger

ART = Path(__file__).resolve().parents[1] / "projects/shifting-desks/art"
V6 = ART / "SDXL-TARGETED-CORRECTION-PILOT-1.yaml"
V7 = ART / "SDXL-MASKED-VAE-CORRECTION-PILOT-2.yaml"


def test_v7_is_staged_only_until_backend_is_deployed():
    previous = yaml.safe_load(V6.read_text(encoding="utf-8"))
    data = yaml.safe_load(V7.read_text(encoding="utf-8"))
    assert previous["subjects"][0]["art"]["sdxl-targeted-local"]["verdict"] == "REDO"
    assert data["auto_submit"] is False
    assert not is_auto_ledger(data)
    assert data["is_public"] is False
    assert data["status"] == "staged-awaiting-masked-vae-deployment"
    assert data["project_slug"] == "shifting-desks"
    assert len(data["subjects"]) == len(data["lanes"]) == 1


def test_v7_has_independent_request_key_and_correct_arm_movement():
    data = yaml.safe_load(V7.read_text(encoding="utf-8"))
    subject, lane = data["subjects"][0], data["lanes"][0]
    assert lane["engine"] == "sdxl-targeted"
    assert lane["inpaint_encoding"] == "masked-vae"
    assert subject["source_image_id"] == 273631
    assert subject["prior_failed_art_job_id"] == 69681
    assert subject["prior_failed_art_image_id"] == 274183
    assert subject["seed"] != 932821
    assert len(subject["targets"]) == 2
    assert subject["jobs"] == {}
    assert subject["art"] == {}
    assert "target_path" not in subject
    assert "entity_art" not in subject
    assert "pen" in subject["pass"].lower()
    assert "three" in subject["pass"].lower()


def test_v7_request_is_private_and_forwards_inpaint_strategy():
    data = yaml.safe_load(V7.read_text(encoding="utf-8"))
    subject, lane = data["subjects"][0], data["lanes"][0]
    body = enqueue.build_targeted_request(
        data, lane, subject, "data:image/png;base64,YWJj"
    )
    assert body["inpaintEncoding"] == "masked-vae"
    assert body["targets"] == subject["targets"]
    assert body["isPublic"] is False
    assert body["denoise"] == 0.95
    assert enqueue.request_url(body).endswith("/api/art/inpaint-targets")


def test_v6_legacy_request_remains_source_preserving():
    data = yaml.safe_load(V6.read_text(encoding="utf-8"))
    subject, lane = data["subjects"][0], data["lanes"][0]
    body = enqueue.build_targeted_request(
        data, lane, subject, "data:image/png;base64,YWJj"
    )
    assert body["inpaintEncoding"] == "source-preserving"
