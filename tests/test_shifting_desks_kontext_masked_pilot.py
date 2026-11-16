"""The masked Shifting Desks pilot edits only evidence-backed missing details."""
import base64
import io
from pathlib import Path

import pytest
import yaml

from scripts import enqueue_art_requests as enq
from scripts.sweep_art_ledgers import is_auto_ledger

Image = pytest.importorskip("PIL.Image")
ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "projects/shifting-desks/art/KONTEXT-MASKED-CORRECTION-PILOT-1.yaml"
EXPECTED = {
    "rear-eyes": (273605, 69448, 2, "832x1216"),
    "living-doors": (273606, 69449, 3, "1216x832"),
    "three-arm-tank": (273607, 69450, 1, "832x1216"),
}


def test_masked_pilot_sources_are_real_krea_redos_and_private():
    data = yaml.safe_load(PATH.read_text(encoding="utf-8"))
    assert is_auto_ledger(data)
    assert data["auto_submit"] is True
    assert data["is_public"] is False
    assert data["task"] == "t-032"
    assert data["status"] == "queued-private-mask-guided-corrections"
    assert len(data["lanes"]) == 1
    lane = data["lanes"][0]
    assert lane["engine"] == "kontext"
    assert lane["steps"] == 16
    assert lane["guidance"] == 2.5
    subjects = data["subjects"]
    assert len(subjects) == len(EXPECTED) == 3
    assert {s["key"] for s in subjects} == set(EXPECTED)
    for subject in subjects:
        image_id, job_id, box_count, size = EXPECTED[subject["key"]]
        assert subject["source_image_id"] == image_id
        assert subject["source_art_job_id"] == job_id
        assert subject["source_verdict"] == "REDO"
        assert subject["size"] == size
        assert len(subject["mask_box"]) == box_count
        assert all(len(box) == 4 for box in subject["mask_box"])
        assert all(
            0 <= box[0] < box[2] <= 1 and 0 <= box[1] < box[3] <= 1
            for box in subject["mask_box"]
        )
        # Queued before submission; once the auto-ledger submits, the only
        # lane is kontext-localized with real job ids and render statuses.
        assert subject["jobs"] == {} or set(subject["jobs"]) == {"kontext-localized"}
        if subject["jobs"]:
            assert isinstance(subject["jobs"]["kontext-localized"], int)
            art = subject["art"]["kontext-localized"]
            assert art["status"] in {"PENDING", "RUNNING", "DONE", "FAILED"}
            assert art["status"] != "DONE" or isinstance(art["art_image_id"], int)
        else:
            assert subject["art"] == {}
        assert "target_path" not in subject
        assert "entity_art" not in subject
        assert subject["pass"] and subject["fail"] and subject["prompt_prose"]


def test_mask_is_restricted_to_user_visible_focal_regions():
    data = yaml.safe_load(PATH.read_text(encoding="utf-8"))
    lane = data["lanes"][0]
    source = Image.new("RGB", (120, 180), "gray")
    buf = io.BytesIO()
    source.save(buf, format="PNG")
    image_data = "data:image/png;base64," + base64.b64encode(
        buf.getvalue()
    ).decode("ascii")
    for subject in data["subjects"]:
        mask_url = enq.make_mask(image_data, subject["mask_box"])
        encoded = mask_url.split(",", 1)[1]
        mask = Image.open(io.BytesIO(base64.b64decode(encoded))).convert("RGB")
        assert mask.size == source.size
        assert mask.getpixel((0, 0)) == (0, 0, 0)
        assert mask.getpixel((119, 179)) == (0, 0, 0)
        for left, top, right, bottom in subject["mask_box"]:
            center = (int((left + right) / 2 * 120), int((top + bottom) / 2 * 180))
            assert mask.getpixel(center) == (255, 255, 255)
        body = enq.build_masked_request(data, lane, subject, image_data, mask_url)
        assert enq.request_url(body).endswith("/api/comfy/kontext/enqueue")
        assert body["imageData"] == image_data
        assert body["maskData"] == mask_url
        assert body["isPublic"] is False
        assert body["steps"] == 16
        assert body["guidance"] == 2.5
