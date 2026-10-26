"""Proof contract for the authored Warp ethics, consequences and Krea 2 art.

The authored content is not yet merged into Kind Robots runtime. Never count
queued/recorded Krea jobs as verified delivered images.
"""

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
STORY = ROOT / "projects/game-of-captains/content/CONSEQUENCES-ROUND-1.json"
LEDGER = ROOT / "projects/game-of-captains/art/CONSEQUENCES-ROUND-1.yaml"


def read():
    story = json.loads(STORY.read_text(encoding="utf-8"))
    ledger = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
    return story, ledger


def test_warp_encounters_are_nontrivial_with_no_dead_end_failure():
    story, _ = read()
    assert story["project_slug"] == "game-of-captains"
    assert story["display_name"] == "This Means Warp"
    assert story["content_stage"] == "authored-not-yet-runtime-integrated"
    assert len(story["episodes"]) == 3
    assert [e["act"] for e in story["episodes"]] == [1, 2, 3]
    assert len(story["endings"]) == 3
    crew = {"pell", "vela", "tess", "rue", "mox", "jex"}
    all_flags = set()
    for episode in story["episodes"]:
        assert episode["once_only"]
        assert episode["opening"] and len(episode["opening"]) > 300
        assert episode["conflict"] and episode["antagonist_signals"]
        assert {"auditor", "moth", "curdle"} == set(episode["antagonist_signals"])
        assert set(episode["crew_focus"]) <= crew
        assert len(episode["choices"]) == 3
        assert len({c["id"] for c in episode["choices"]}) == 3
        for choice in episode["choices"]:
            assert len(choice["cost"]) > 45
            assert choice["check"]["difficulty"] in range(1, 10)
            for kind in ("success", "failure"):
                result = choice[kind]
                assert len(result["narrative"]) > 220
                assert len(result["art"]["scene"]) > 240
                assert len(result["callback"]) >= 65
                assert result["delta"] and result["flags"]
                all_flags.update(result["flags"])
            assert set(choice["success"]["flags"]) != set(choice["failure"]["flags"])
            assert choice["success"]["art"]["scene"] != choice["failure"]["art"]["scene"]

    for ending in story["endings"]:
        assert ending["requires_all"]
        assert all(f in all_flags for f in ending["requires_all"]), ending["id"]
        assert len(ending["narrative"]) > 300
        assert len(ending["cost"]) > 100
        assert len(ending["art"]["scene"]) > 240
    assert len({e["id"] for e in story["endings"]}) == 3

    # Endings need an actual sequence of *compatible* choices and results.
    # A player can choose only one outcome from each once-only encounter.
    from itertools import product

    episode_results = [
        [set(c[tier]["flags"]) for c in episode["choices"] for tier in ("success", "failure")]
        for episode in story["episodes"]
    ]
    for ending in story["endings"]:
        needed = set(ending["requires_all"])
        assert any(needed <= set().union(*combination) for combination in product(*episode_results)), ending["id"]


def test_each_warp_consequence_has_a_literal_illustration_request():
    story, ledger = read()
    assert ledger["project_slug"] == story["project_slug"]
    assert ledger["auto_submit"] is True
    assert len(ledger["lanes"]) == 1
    assert ledger["lanes"][0]["engine"] == "krea2"
    expected = {}
    for ep in story["episodes"]:
        for choice in ep["choices"]:
            for tier in ("success", "failure"):
                expected[f'{ep["id"]}-{choice["id"]}-{tier}'] = choice[tier]["art"]["scene"]
    for ending in story["endings"]:
        expected[ending["id"]] = ending["art"]["scene"]
    assert len(expected) == 21

    subjects = ledger["subjects"]
    actual = {subject["key"]: subject for subject in subjects}
    assert len(actual) == len(subjects) == len(expected)
    assert set(actual) == set(expected)
    for key, prompt in expected.items():
        row = actual[key]
        assert row["lane"] == "krea2"
        assert row["asset"] == f"game-of-captains/consequences/{key}"
        assert row["size"] == "1344x768"
        assert row["prompt_prose"] == prompt
        assert isinstance(row["seed"], int)
        assert isinstance(row.get("jobs", {}), dict), "jobs may only be assigned by the generator"
