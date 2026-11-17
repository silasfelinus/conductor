"""V7 may submit once, privately, only after production masked-VAE preflight."""
from pathlib import Path

import yaml

from scripts import enqueue_art_requests as enqueue
from scripts.sweep_art_ledgers import is_auto_ledger

ART = Path(__file__).resolve().parents[1] / "projects/shifting-desks/art"
V6 = ART / "SDXL-TARGETED-CORRECTION-PILOT-1.yaml"
V7 = ART / "SDXL-MASKED-VAE-CORRECTION-PILOT-2.yaml"


def test_v7_is_private_and_auto_enabled_after_verified_backend_deployment():
    previous = yaml.safe_load(V6.read_text(encoding="utf-8"))
    data = yaml.safe_load(V7.read_text(encoding="utf-8"))
    assert previous["subjects"][0]["art"]["sdxl-targeted-local"]["verdict"] == "REDO"
    assert data["auto_submit"] is True
    assert is_auto_ledger(data)
    assert data["deployment_verification"]["backend_merge_commit"].startswith("6c897c72")
    assert data["deployment_verification"]["live_commit"].startswith("1d43a4ed")
    assert data["deployment_verification"]["probe_run_id"] == 44025707717
    assert data["is_public"] is False
    assert data["status"] == "ready-for-private-submission"
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


def _mask_data(fill="white"):
    import base64
    import io
    from PIL import Image, ImageDraw

    mask = Image.new("RGB", (64, 64), "black")
    if fill == "white":
        ImageDraw.Draw(mask).rectangle((16, 16, 47, 47), fill="white")
    elif fill == "escaped":
        mask = Image.new("RGB", (64, 64), "white")
    raw = io.BytesIO()
    mask.save(raw, "PNG")
    return "data:image/png;base64," + base64.b64encode(raw.getvalue()).decode()


def _preview_reply(encoding="masked-vae", hard="white", soft="white"):
    return 200, {
        "success": True,
        "data": {
            "previewOnly": True,
            "inpaintEncoding": encoding,
            "mode": "crop",
            "width": 64,
            "height": 64,
            "crop": {"x": 0, "y": 0, "width": 64, "height": 64},
            "noiseMaskData": _mask_data(hard),
            "compositeMaskData": _mask_data(soft),
        },
    }


def test_live_preflight_confirms_echo_and_usable_masks_without_creating_job():
    body = {"inpaintEncoding": "masked-vae", "mode": "crop", "requestKey": "v7"}
    observed = []

    def post(payload):
        observed.append(payload)
        return _preview_reply()

    verified = enqueue.verify_masked_vae_preview(body, post)
    assert verified["mask_size"] == (64, 64)
    assert len(observed) == 1
    assert observed[0]["previewOnly"] is True
    assert observed[0]["requestKey"] == "v7"
    assert body.get("previewOnly") is None


def test_missing_encoder_echo_empty_mask_or_escaping_soft_mask_blocks_submission():
    import pytest
    body = {"inpaintEncoding": "masked-vae", "mode": "crop"}
    for reply in (
        _preview_reply(encoding="source-preserving"),
        _preview_reply(encoding=None),
        _preview_reply(hard="blank"),
        _preview_reply(soft="blank"),
        _preview_reply(soft="escaped"),
        (500, {"message": "unavailable"}),
    ):
        with pytest.raises(ValueError):
            enqueue.verify_masked_vae_preview(body, lambda _body, reply=reply: reply)


def test_failed_live_preflight_does_not_enqueue_artjob(tmp_path, monkeypatch):
    from PIL import Image
    import base64
    import io

    image = Image.new("RGB", (64, 64), "#718f51")
    raw = io.BytesIO()
    image.save(raw, "PNG")
    source = "data:image/png;base64," + base64.b64encode(raw.getvalue()).decode()
    data = {
        "round": "unit-test-v7",
        "project_slug": "shifting-desks",
        "is_public": False,
        "lanes": [{
            "engine": "sdxl-targeted", "key": "masked-vae", "prompt": "prose",
            "checkpoint": "SDXL/model.safetensors", "inpaint_encoding": "masked-vae",
            "mode": "crop",
        }],
        "subjects": [{
            "key": "third-arm", "source_image_id": 273631, "size": "64x64",
            "prompt_prose": "One worker with three properly attached arms",
            "targets": [{"type": "box", "box": [0.25, 0.25, 0.75, 0.75]}],
            "jobs": {},
        }],
    }
    path = tmp_path / "v7-test.yaml"
    path.write_text(yaml.safe_dump(data))
    monkeypatch.setattr(enqueue, "contract_rules", lambda cells, live=None: [[] for _ in cells])
    monkeypatch.setattr(enqueue, "ledger_problems", lambda ledger, only_unsubmitted=False: [])
    sent = []

    def reject_preview(body):
        sent.append(body)
        assert body.get("previewOnly") is True
        return _preview_reply(encoding="source-preserving")

    result = enqueue.submit(
        path, "", data, [(data["subjects"][0], data["lanes"][0])],
        post=reject_preview, fetch_source=lambda _id: source,
    )
    assert result == (0, 1)
    assert len(sent) == 1
    assert data["subjects"][0]["jobs"] == {}

    sent.clear()

    def accept_preview_then_queue(body):
        sent.append(body)
        return _preview_reply() if body.get("previewOnly") else (
            201, {"data": {"jobId": 70007}}
        )

    result = enqueue.submit(
        path, "", data, [(data["subjects"][0], data["lanes"][0])],
        post=accept_preview_then_queue, fetch_source=lambda _id: source,
    )
    assert result == (1, 0)
    assert len(sent) == 2
    assert sent[0]["previewOnly"] is True
    assert sent[1].get("previewOnly") is None
    assert data["subjects"][0]["jobs"]["masked-vae"] == 70007
    assert enqueue.submit(
        path, "", data, [(data["subjects"][0], data["lanes"][0])],
        post=accept_preview_then_queue, fetch_source=lambda _id: source,
    ) == (0, 0)
    assert len(sent) == 2
