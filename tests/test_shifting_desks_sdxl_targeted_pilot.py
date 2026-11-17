"""Private SDXL target pilot follows proven two-KEEP, one-REDO V5 image review."""
from pathlib import Path

import yaml

from scripts import enqueue_art_requests as enq
from scripts.sweep_art_ledgers import is_auto_ledger

ART = Path(__file__).resolve().parents[1] / "projects/shifting-desks/art"
V5 = ART / "KONTEXT-MASKED-CORRECTION-PILOT-1.yaml"
TARGET = ART / "SDXL-TARGETED-CORRECTION-PILOT-1.yaml"


def test_only_rejected_third_arm_awaits_strict_pixel_targeting():
    prior = yaml.safe_load(V5.read_text(encoding="utf-8"))
    verdicts = {
        subject["key"]: subject["art"]["kontext-localized"]
        for subject in prior["subjects"]
    }
    assert {k: v["verdict"] for k, v in verdicts.items()} == {
        "rear-eyes": "KEEP", "living-doors": "KEEP", "three-arm-tank": "REDO"
    }
    assert {v["art_image_id"] for v in verdicts.values()} == {
        273629, 273630, 273631
    }
    assert not is_auto_ledger(prior)
    data = yaml.safe_load(TARGET.read_text(encoding="utf-8"))
    assert is_auto_ledger(data)
    assert data["auto_submit"] is True
    assert data["status"] == "ready-for-private-submission"
    verification = data["deployment_verification"]
    assert verification["live_commit"] == "7edbe1d35c4b05bf20fc2ef033488512c87d82f0"
    assert verification["backend_merge_commit"] == "b514d9973415129d33d99d45c4b67ccbba4590ad"
    assert verification["workflow_run_id"] == 44000603006
    assert verification["workflow_job_id"] == 133763393689
    assert data["is_public"] is False
    assert len(data["subjects"]) == len(data["lanes"]) == 1
    subject, lane = data["subjects"][0], data["lanes"][0]
    assert lane["engine"] == "sdxl-targeted"
    assert subject["key"] == "three-arm-tank"
    assert subject["source_image_id"] == verdicts["three-arm-tank"]["art_image_id"]
    assert subject["source_art_job_id"] == 69458
    assert subject["source_evidence_artifact_id"] == 14213687064
    assert subject["source_verdict"] == "REDO"
    assert lane["mode"] == "crop"
    assert lane["steps"] == 8 and lane["cfg"] == 2
    assert subject["targets"][0]["type"] == "box"
    assert 0 < subject["targets"][0]["bleedPx"] <= 96
    assert 0 <= subject["targets"][0]["featherPx"] <= 48
    assert "target_path" not in subject and "entity_art" not in subject
    body = enq.build_targeted_request(
        data, lane, subject, "data:image/png;base64,YWJj"
    )
    assert body["imageData"].startswith("data:image/png")
    assert body["targets"] == subject["targets"]
    assert body["isPublic"] is False
    assert enq.request_url(body).endswith("/api/art/inpaint-targets")
