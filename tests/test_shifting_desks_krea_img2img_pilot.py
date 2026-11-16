"""The completed private Krea2 edit pilot is failed and cannot silently resubmit."""
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
    assert not is_auto_ledger(ledger), "reviewed REDO candidates must not resubmit"
    assert ledger["auto_submit"] is False
    assert ledger["round"] == "shifting-desks-krea-img2img-pilot-1"
    assert ledger["status"] == "reviewed-3-redo-requires-localized-edits"
    assert ledger["task"] == "t-032"
    assert ledger["is_public"] is False
    assert ledger["cast_loras"] is False
    rows = list(enq.iter_cells(ledger))
    assert len(rows) == 3
    expected = {
        "rear-eyes": (69448, 273605),
        "living-doors": (69449, 273606),
        "three-arm-tank": (69450, 273607),
    }
    for subject, lane in rows:
        assert subject["source_image_id"] == SOURCES[subject["key"]]
        assert subject["source_verdict"] == "REDO"
        assert subject["pass"] and subject["fail"]
        assert 0.6 <= subject["denoise"] <= 0.72
        assert "target_path" not in subject
        assert "entity_art" not in subject
        job_id, art_id = expected[subject["key"]]
        assert subject["jobs"] == {lane["key"]: job_id}
        record = subject["art"][lane["key"]]
        assert record["status"] == "DONE"
        assert record["art_image_id"] == art_id
        assert record["verdict"] == "REDO"
        assert record["evidence_artifact_id"] == 14210147265
        assert "ArtImage" in record["review_note"]
        assert lane["engine"] == "krea2"
        assert lane["steps"] == 8
        assert lane["cfg"] == 1
        body = enq.build_request(ledger, lane, subject, "data:image/png;base64,YWJj")
        assert body["engine"] == "krea2"
        assert body["sourceImageBase64"] == "data:image/png;base64,YWJj"
        assert body["denoise"] == subject["denoise"]
        assert body["isPublic"] is False
