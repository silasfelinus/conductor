"""Validate narrative choice/outcome art contracts for the new playbook batches.

These are authored candidate branches, not proof they are wired to game runtime.
A Krea image job is a request, not a delivered render.
"""

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def check_project(slug: str):
    story_path = ROOT / "projects" / slug / "content" / "CONSEQUENCES-ROUND-1.json"
    ledger_path = ROOT / "projects" / slug / "art" / "CONSEQUENCES-ROUND-1.yaml"
    story = json.loads(story_path.read_text(encoding="utf-8"))
    ledger = yaml.safe_load(ledger_path.read_text(encoding="utf-8"))
    assert story["project_slug"] == ledger["project_slug"] == slug
    assert story["content_stage"] == "authored-not-yet-runtime-integrated"
    assert ledger["auto_submit"] is True
    assert len(ledger["lanes"]) == 1
    assert ledger["lanes"][0]["engine"] == "krea2"
    assert len(story["encounters"]) == 3
    assert len(story["endings"]) == 3
    expected = set()
    for episode in story["encounters"]:
        assert episode["opening"] and episode["conflict"] and episode["villain_signal"]
        assert len(episode["choices"]) == 3
        for choice in episode["choices"]:
            assert choice["cost"] and choice["check"]["difficulty"] >= 1
            for result in ("success", "failure"):
                payload = choice[result]
                assert len(payload["narrative"]) >= 100
                assert payload["flags"] and payload["delta"] and payload["callback"]
                assert len(payload["art"]["scene"]) >= 120
                expected.add(f"{episode['id']}-{choice['id']}-{result}")
            assert choice["success"]["narrative"] != choice["failure"]["narrative"]
    for ending in story["endings"]:
        assert len(ending["epilogue"]) >= 130
        assert ending["requires"] and ending["cost"] and len(ending["art"]["scene"]) >= 120
        expected.add(ending["id"])
    keys = [subject["key"] for subject in ledger["subjects"]]
    assert len(keys) == len(set(keys)) == 21
    assert set(keys) == expected
    for subject in ledger["subjects"]:
        assert subject["lane"] == "krea2"
        assert subject["size"] in ("1344x768",)
        assert subject["prompt_prose"]
        assert subject["asset"].startswith(f"{slug}/consequences/")
        assert isinstance(subject.get("jobs", {}), dict), "jobs may only be assigned by the generator"


def test_capes_branch_art_and_finales():
    check_project("comet-city-academy")
