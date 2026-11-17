"""The V7 encoder is a render-deciding input to stable ArtJob request keys."""
from pathlib import Path

import yaml

from scripts.art_request_key import ledger_cell_key


def test_legacy_source_preserving_key_is_stable_without_encoder_field():
    lane = {"key": "sdxl-targeted-local", "engine": "sdxl-targeted", "steps": 8}
    subject = {
        "key": "three-arm-tank", "source_image_id": 273631,
        "prompt_prose": "an extra arm holds the pen",
    }
    first = ledger_cell_key("projects/shifting-desks/art/pilot.yaml", lane, subject)
    assert first == ledger_cell_key(
        "projects/shifting-desks/art/pilot.yaml", dict(lane), dict(subject)
    )
    assert first.startswith("conductor:ledger:")


def test_changing_encoder_alters_key_without_change_to_prompt_or_source():
    lane = {"key": "sdxl-masked-vae", "engine": "sdxl-targeted", "steps": 8}
    subject = {
        "key": "third-arm", "source_image_id": 273631,
        "prompt_prose": "move orange pen from old hand into the third hand",
    }
    path = "projects/shifting-desks/art/private.yaml"
    original = ledger_cell_key(path, lane, subject)
    opted = ledger_cell_key(path, {**lane, "inpaint_encoding": "masked-vae"}, subject)
    changed = ledger_cell_key(path, {**lane, "inpaint_encoding": "source-preserving"}, subject)
    subject_override = ledger_cell_key(
        path, lane, {**subject, "inpaint_encoding": "masked-vae"}
    )
    assert len({original, opted, changed, subject_override}) == 4
    assert opted == ledger_cell_key(
        path, {**lane, "inpaint_encoding": "masked-vae"},
        {**subject, "art": {"sdxl-masked-vae": {"verdict": "KEEP"}}},
    )


def test_v7_key_is_unique_and_feather_hotfix_remains_not_published():
    path = Path(__file__).resolve().parents[1] / (
        "projects/shifting-desks/art/SDXL-MASKED-VAE-CORRECTION-PILOT-2.yaml"
    )
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    subject, lane = data["subjects"][0], data["lanes"][0]
    assert data["is_public"] is False
    assert data["auto_submit"] is False
    assert data["status"] == "reviewed-redo"
    assert subject["art"][lane["key"]]["verdict"] == "REDO"
    assert lane["inpaint_encoding"] == "masked-vae"
    assert data["masked_vae_feather_repair"]["backend_pr"] == 5273
    repair = data["masked_vae_feather_repair"]
    assert repair["live_verification"] in {
        "awaiting-alexandria", "verified-production"
    }
    if repair["live_verification"] == "verified-production":
        assert repair.get("live_commit")
    job = (subject.get("jobs") or {}).get(lane["key"])
    assert job is None or job > 0
    request_key = ledger_cell_key(
        str(path.relative_to(Path(__file__).resolve().parents[1])), lane, subject
    )
    assert "sdxl-masked-vae" in request_key
