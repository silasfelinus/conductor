"""Exactly fourteen rejected Classic scenes must have source-referenced Krea plans.

The eleven follow-up corrections are staged, NOT auto-submitted. The first
three Krea jobs 69448-69450 must receive real image verdicts before activation.
"""
from pathlib import Path

import yaml

from scripts import enqueue_art_requests as enq
from scripts.sweep_art_ledgers import is_auto_ledger

ART = Path(__file__).resolve().parents[1] / "projects/shifting-desks/art"
FIRST = ART / "KREA-IMG2IMG-CORRECTION-PILOT-1.yaml"
REMAINING = ART / "KREA-IMG2IMG-CORRECTION-PILOT-2.yaml"
ROUND19 = ART / "ROUND-19.yaml"
FIRST_TO_CLASSIC = {
    "rear-eyes": "mutation-eyes-in-the-back-of-your-head",
    "living-doors": "wellness",
    "three-arm-tank": "mutation-suite",
}


def test_draft_covers_exactly_the_eleven_classic_redos_not_in_first_pilot():
    first = yaml.safe_load(FIRST.read_text(encoding="utf-8"))
    later = yaml.safe_load(REMAINING.read_text(encoding="utf-8"))
    classic = yaml.safe_load(ROUND19.read_text(encoding="utf-8"))
    first_classic = set(FIRST_TO_CLASSIC.values())
    all_keys = {row["key"] for row in classic["subjects"]}
    draft_keys = {row["key"] for row in later["subjects"]}
    assert len(classic["subjects"]) == 14
    assert len(first["subjects"]) == len(first_classic) == 3
    assert len(later["subjects"]) == len(draft_keys) == 11
    assert all_keys == first_classic | draft_keys
    assert not (first_classic & draft_keys)
    assert all(
        str(row.get("verdict", "")).lower().startswith("redo:")
        for row in classic["subjects"]
    )


def test_remaining_source_images_match_delivered_classic_round19_not_prototypes():
    later = yaml.safe_load(REMAINING.read_text(encoding="utf-8"))
    classic = yaml.safe_load(ROUND19.read_text(encoding="utf-8"))
    source_map = {
        row["key"]: row["art_image_id"] for row in classic["subjects"]
    }
    assert not is_auto_ledger(later)
    assert later["auto_submit"] is False
    assert later["status"] == "staged-awaiting-localized-inpaint"
    assert later["is_public"] is False
    assert later["task"] == "t-032"
    assert later["cast_loras"] is False
    assert len(later["lanes"]) == 1
    lane = later["lanes"][0]
    assert lane["engine"] == "krea2"
    assert lane["steps"] == 8 and lane["cfg"] == 1
    for row in later["subjects"]:
        assert row["source_round"] == 19
        assert row["source_verdict"] == "REDO"
        assert row["source_image_id"] == source_map[row["key"]]
        assert isinstance(row["source_image_id"], int)
        assert row["size"] and 0.5 <= row["denoise"] <= 0.75
        assert row["pass"] and row["fail"] and row["prompt_prose"]
        assert row["jobs"] == {} and row["art"] == {}
        assert "target_path" not in row and "entity_art" not in row
        body = enq.build_request(
            later, lane, row, "data:image/webp;base64,YWJj"
        )
        assert body["engine"] == "krea2"
        assert body["sourceImageBase64"] == "data:image/webp;base64,YWJj"
        assert body["denoise"] == row["denoise"]
        assert body["isPublic"] is False
