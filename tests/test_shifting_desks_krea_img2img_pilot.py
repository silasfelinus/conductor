"""Krea2 correction pilot submits real private source edits after verified deployment."""
from pathlib import Path

import yaml

from scripts import enqueue_art_requests as enq
from scripts.sweep_art_ledgers import is_auto_ledger

LEDGER = Path(__file__).resolve().parents[1] / (
    "projects/shifting-desks/art/KREA-IMG2IMG-CORRECTION-PILOT-1.yaml"
)
SOURCES = {"rear-eyes": 271721, "living-doors": 271722, "three-arm-tank": 271723}


def test_krea_pilot_uses_real_reference_images_and_never_publishes():
    ledger = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
    assert is_auto_ledger(ledger), "verified live Krea backend enables private submission"
    assert ledger["auto_submit"] is True
    assert ledger["status"] == "queued-private-krea-img2img-pilot"
    assert ledger["task"] == "t-032"
    assert ledger["is_public"] is False
    assert ledger["cast_loras"] is False
    rows = list(enq.iter_cells(ledger))
    assert len(rows) == 3
    for subject, lane in rows:
        assert subject["source_image_id"] == SOURCES[subject["key"]]
        assert subject["source_verdict"] == "REDO"
        assert subject["pass"] and subject["fail"]
        assert 0.6 <= subject["denoise"] <= 0.72
        assert "target_path" not in subject
        assert "entity_art" not in subject
        recorded_jobs = subject.get("jobs") or {}
        assert set(recorded_jobs) <= {lane["key"]}
        assert all(isinstance(job_id, int) and job_id > 0 for job_id in recorded_jobs.values())
        for record in (subject.get("art") or {}).values():
            assert record.get("status") in {"PENDING", "RUNNING", "DONE", "FAILED", "REJECTED"}
            image_id = record.get("art_image_id")
            assert image_id is None or (isinstance(image_id, int) and image_id > 0)
        assert lane["engine"] == "krea2"
        assert lane["steps"] == 8
        assert lane["cfg"] == 1
        body = enq.build_request(ledger, lane, subject, "data:image/png;base64,YWJj")
        assert body["engine"] == "krea2"
        assert body["sourceImageBase64"] == "data:image/png;base64,YWJj"
        assert body["denoise"] == subject["denoise"]
        assert body["isPublic"] is False
