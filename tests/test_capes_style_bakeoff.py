"""Capes house-style gate: six subjects x six deliberate non-furry-first lanes."""
from pathlib import Path

import yaml

from scripts.enqueue_art_requests import build_request, compose_prompt

LEDGER = Path(__file__).resolve().parents[1] / "projects/comet-city-academy/art/CAPES-WESTERN-STYLE-CHECK-ROUND-1.yaml"


def test_capes_style_check_six_by_six_and_engine_formulas():
    data = yaml.safe_load(LEDGER.read_text())
    lanes, subjects = data["lanes"], data["subjects"]
    assert data["auto_submit"] is False
    assert data["is_public"] is False
    assert data["priority"] == 900
    assert len(subjects) == len(lanes) == 6
    assert len({lane["key"] for lane in lanes}) == 6
    assert len({subject["key"] for subject in subjects}) == 6
    assert len({subject["seed"] for subject in subjects}) == 6
    assert {lane["key"] for lane in lanes} == {
        "krea2", "arthemy", "nova-comic", "illustrij", "dreamshaper", "unstable"
    }
    assert {lane["engine"] for lane in lanes} == {"krea2", "comfy"}
    for lane in lanes:
        label = (lane.get("checkpoint") or lane["key"]).lower()
        assert not any(word in label for word in ("pony", "furry", "flux"))
        if lane["key"] == "krea2":
            assert lane["prompt"] == "prose"
            assert "checkpoint" not in lane
        if lane.get("checkpoint"):
            assert lane["prompt"] in ("tags", "prose")
    cells = []
    for subject in subjects:
        assert subject["asset"].startswith("comet-city-academy/style-check-v1/")
        assert "prompt_prose" in subject and "prompt_tags" in subject
        assert subject.get("jobs") == {}
        for lane in lanes:
            request = build_request(data, lane, subject)
            assert request["projectSlug"] == "comet-city-academy"
            assert request["designer"] == "Capes Style Check 2026-10-29"
            assert request["priority"] == 900
            assert request["isPublic"] is False
            assert request["seed"] == subject["seed"]
            assert request["promptString"] == compose_prompt(lane, subject)
            assert request["width"] > 0 and request["height"] > 0
            cells.append((subject["key"], lane["key"]))
    assert len(set(cells)) == 36


def test_capes_scoring_subjects_cover_real_asset_categories():
    data = yaml.safe_load(LEDGER.read_text())
    subjects = {item["key"]: item for item in data["subjects"]}
    assert set(subjects) == {
        "cornerstone-hero", "backdraft-villain", "warren-wreckers",
        "mags-hardpan", "science-lab", "firewall-standee"
    }
    assert subjects["science-lab"]["size"] == "1344x768"
    assert subjects["firewall-standee"]["size"] == "1536x768"
    assert all(subject["negative"] for subject in subjects.values())
