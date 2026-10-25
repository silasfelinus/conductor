"""The real day-30 Prom of Doom is mandatory and illustrated in Krea 2.

This checks canonical authored content, not yet the Kind Robots runtime. Runtime
playthrough coverage is a separate production gate.
"""
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
STORY = ROOT / "projects/comet-city-academy/content/PROM-OF-DOOM-FINALE-ROUND-1.json"
LEDGER = ROOT / "projects/comet-city-academy/art/PROM-OF-DOOM-FINALE-ROUND-1.yaml"


def test_real_prom_of_doom_is_a_day_thirty_mandatory_scenario():
    story = json.loads(STORY.read_text(encoding="utf-8"))
    assert story["project_slug"] == "comet-city-academy"
    assert story["content_stage"] == "authored-not-yet-runtime-integrated"
    assert story["mandatory_real_prom"] is True
    assert story["never_replace_with_rehearsal"] is True
    assert story["prom_day"] == 30
    assert story["episode_29"]["day"] == 29
    assert story["episode_30"]["day"] == 30
    assert story["episode_30"]["title"] == "PROM OF DOOM"
    assert story["episode_30"]["mandatory"] is True
    assert story["episode_30"]["can_skip"] is False
    assert story["episode_30"]["has_fallback"] is True
    assert "actual dance" in story["episode_30"]["physical_event"]
    assert len(story["episode_30"]["scripted_beats"]) >= 5
    assert len(story["episode_30"]["villain_adapters"]) >= 3
    assert len(set(v["id"] for v in story["episode_30"]["villain_adapters"])) == len(story["episode_30"]["villain_adapters"])
    assert len(story["episode_30"]["choices"]) >= 4
    assert len(story["endings"]) >= 4
    for episode in (story["episode_29"], story["episode_30"]):
        assert len(episode["choices"]) >= 3
        for choice in episode["choices"]:
            assert choice["cost"] and choice["check"]["difficulty"] >= 1
            assert choice["success"]["flags"] and choice["failure"]["flags"]
            assert choice["success"]["flags"] != choice["failure"]["flags"]
            assert len(choice["success"]["narrative"]) >= 100
            assert len(choice["failure"]["narrative"]) >= 100
            assert choice["success"]["callback"] and choice["failure"]["callback"]
    assert len({x["id"] for x in story["endings"]}) == len(story["endings"])
    for ending in story["endings"]:
        assert ending["cost"] and ending["requires_any"]
        assert len(ending["narrative"]) >= 100


def test_krea_prom_art_has_unique_plate_for_each_state():
    story = json.loads(STORY.read_text(encoding="utf-8"))
    ledger = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
    assert ledger["auto_submit"] is True
    assert ledger["project_slug"] == "comet-city-academy"
    assert len(ledger["lanes"]) == 1
    assert ledger["lanes"][0]["engine"] == "krea2"
    expected = {beat["key"]: beat["scene"] for beat in story["key_moments"]}
    for episode in (story["episode_29"], story["episode_30"]):
        for choice in episode["choices"]:
            for tier in ("success", "failure"):
                expected[f'{episode["id"]}-{choice["id"]}-{tier}'] = choice[tier]["art"]["scene"]
    expected.update({ending["id"]: ending["art"]["scene"] for ending in story["endings"]})
    assert len(expected) == 21
    subjects = ledger["subjects"]
    actual = {subject["key"]: subject for subject in subjects}
    assert len(subjects) == len(actual) == len(expected)
    for key, scene in expected.items():
        subject = actual[key]
        assert subject["lane"] == "krea2"
        assert subject["asset"] == f"comet-city-academy/prom-of-doom/{key}"
        assert subject["size"] == "1344x768"
        assert subject["prompt_prose"] == scene
        assert not subject.get("jobs"), "An absent ArtJob ID must never be invented"
