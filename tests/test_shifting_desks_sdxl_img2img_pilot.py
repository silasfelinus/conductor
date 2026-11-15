"""Private Shifting Desks Turbo img2img pilot must never overwrite Classic artwork."""
from pathlib import Path

import yaml

from scripts import enqueue_art_requests as enq
from scripts.sweep_art_ledgers import is_auto_ledger

LEDGER = (
    Path(__file__).resolve().parents[1]
    / "projects/shifting-desks/art/SDXL-IMG2IMG-CORRECTION-PILOT-1.yaml"
)
SOURCES = {
    "rear-eyes-edit": 271721,
    "living-doors-edit": 271722,
    "three-arm-tank-edit": 271723,
}


def test_private_sdxl_turbo_pilot_builds_genuine_image_to_image_jobs():
    ledger = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
    assert is_auto_ledger(ledger), "the shared sweep must discover this ledger"
    assert ledger["project_slug"] == "shifting-desks"
    assert ledger["task"] == "t-032"
    assert ledger["is_public"] is False
    assert ledger["is_mature"] is False
    assert ledger["cast_loras"] is False
    assert set(item["key"] for item in ledger["subjects"]) == set(SOURCES)

    cells = list(enq.iter_cells(ledger))
    assert len(cells) == 3
    for subject, lane in cells:
        assert subject["source_image_id"] == SOURCES[subject["key"]]
        assert subject["source_verdict"] == "REDO"
        assert "jobs" not in subject, "no fabricated ArtJob IDs"
        assert "target_path" not in subject, "private trials cannot overwrite live art"
        assert "entity_art" not in subject, "private trials cannot attach to live records"
        assert "media_url" not in subject, "no live destination for unapproved artwork"
        assert 0.75 <= subject["denoise"] <= 0.85
        assert subject["pass"] and subject["fail"]

        assert lane["engine"] == "sdxl-img2img"
        assert lane["steps"] == 8, "use the fast Turbo path, never Kontext"
        assert "Turbo" in lane["checkpoint"]
        body = enq.build_request(
            ledger, lane, subject, source_image="data:image/png;base64,YWJj"
        )
        assert body["engine"] == "sdxl-img2img"
        assert body["checkpoint"] == lane["checkpoint"]
        assert body["sourceImageBase64"].startswith("data:image/")
        assert body["denoise"] == subject["denoise"]
        assert body["steps"] == 8
        assert body["cfg"] == 2
        assert body["isPublic"] is False
        assert body["projectSlug"] == "shifting-desks"
        assert "entityArt" not in body
        assert "targetRepo" not in body
        assert "imagePath" not in body
