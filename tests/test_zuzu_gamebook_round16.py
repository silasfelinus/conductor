"""Prevent screenshot-reported Zuzu scenes from falling out of the actual ArtJob queue."""
from collections import Counter
from pathlib import Path

import yaml

from scripts import enqueue_art_requests as enqueue
from scripts import sweep_art_ledgers as sweep


LEDGER = Path(__file__).resolve().parents[1] / "projects/zuzu-gamebook/art/ROUND-16-SCENE-FIDELITY.yaml"


def test_round_16_is_a_real_automatic_arthemy_submission():
    data = yaml.safe_load(LEDGER.read_text())
    assert sweep.is_auto_ledger(data)
    assert data["cast_loras"] is False
    assert data["is_public"] is False and data["is_mature"] is False
    assert data["series"] == "zuzu-koala-assassin"
    assert len(data["lanes"]) == 1
    lane = data["lanes"][0]
    assert lane["key"] == "arthemy-house"
    assert lane["engine"] == "comfy"
    assert lane["checkpoint"] == "Illustrious/arthemyWesternArt_v30.safetensors"
    assert lane["prompt"] == "tags"

    subjects = data["subjects"]
    assert len(subjects) == 9
    assert Counter(s["section"] for s in subjects) == {
        "a2-bell-view": 3,
        "a2-gift": 3,
        "a4-bloom": 3,
    }
    assert len({s["key"] for s in subjects}) == 9
    assert len({s["seed"] for s in subjects}) == 9

    for subject in subjects:
        req = enqueue.build_request(data, lane, subject)
        assert req["engine"] == "comfy"
        assert req["checkpoint"] == lane["checkpoint"]
        assert req["projectSlug"] == "zuzu-gamebook"
        assert req["isPublic"] is False
        assert req["isMature"] is False
        assert req["steps"] == 30 and req["cfg"] == 5
        assert req["negativePrompt"]
        assert len(req["promptString"]) > 200
        if subject["section"] == "a2-bell-view":
            assert (req["width"], req["height"]) == (1344, 768)
            assert "bell" in req["promptString"].lower()
            assert any(word in req["promptString"].lower() for word in ("tiny", "small"))
            assert "tower" in req["promptString"].lower()
        elif subject["section"] == "a2-gift":
            assert (req["width"], req["height"]) == (896, 1152)
            assert "waterskin" in req["promptString"].lower() or "canteen" in req["promptString"].lower() or "water pouch" in req["promptString"].lower()
            assert "nail" in req["promptString"].lower()
            assert "scrat" in req["promptString"].lower() or "gouge" in req["promptString"].lower()
        else:
            assert (req["width"], req["height"]) == (1344, 768)
            assert "flower" in req["promptString"].lower()
            assert "violet" in req["promptString"].lower()
            assert "rain" in req["promptString"].lower() or "wet" in req["promptString"].lower()

    # The runner writes subject.jobs when it has genuinely accepted the ArtJobs.
    # Do not infer submission from the existence of this file or pretend these IDs exist.
    assert all(isinstance(s.get("jobs", {}), dict) for s in subjects)
