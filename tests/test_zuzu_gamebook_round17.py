"""Each revised Arthemy candidate must target the section's pictured object, not incidental buildings."""
from collections import Counter
from pathlib import Path

import yaml

from scripts import enqueue_art_requests as enq
from scripts import sweep_art_ledgers as sweep


LEDGER = Path(__file__).resolve().parents[1] / "projects/zuzu-gamebook/art/ROUND-17-SCENE-FIDELITY.yaml"


def test_round17_subject_first_arthemy_rerolls():
    data = yaml.safe_load(LEDGER.read_text())
    assert sweep.is_auto_ledger(data)
    assert data["cast_loras"] is False
    assert data["is_public"] is False
    assert data["series"] == "zuzu-koala-assassin"
    lane, = data["lanes"]
    assert lane["engine"] == "comfy"
    assert lane["checkpoint"] == "Illustrious/arthemyWesternArt_v30.safetensors"

    subjects = data["subjects"]
    assert len(subjects) == 9
    assert len({s["key"] for s in subjects}) == 9
    assert len({s["seed"] for s in subjects}) == 9
    assert Counter(s["section"] for s in subjects) == {
        "a2-bell-view": 3, "a2-gift": 3, "a4-bloom": 3,
    }

    for subject in subjects:
        request = enq.build_request(data, lane, subject)
        prompt = request["promptString"].lower()
        negative = request["negativePrompt"].lower()
        assert request["engine"] == "comfy"
        assert request["isPublic"] is False
        assert request["checkpoint"] == lane["checkpoint"]
        assert request["projectSlug"] == "zuzu-gamebook"
        assert "text" in negative and "person" in negative
        if subject["section"] == "a2-bell-view":
            assert request["width"] == 1344
            assert "bronze bell" in prompt
            assert "clapper" in prompt
            assert "corridor" in negative
        elif subject["section"] == "a2-gift":
            assert request["height"] == 1152
            assert "waterskin" in prompt or "leather water pouch" in prompt
            assert "nail" in prompt
            assert "portrait" in negative
        else:
            assert request["width"] == 1344
            assert "flower" in prompt and "violet" in prompt
            assert "cabin" in negative and "shrine" in negative
