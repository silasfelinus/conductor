"""Guard the first Every Villain Tactics private painted-arena art batch."""
from pathlib import Path

import yaml

from scripts.art_ledger_authoring import ledger_problems
from scripts.sweep_art_ledgers import is_auto_ledger, open_cells

LEDGER = Path(__file__).resolve().parents[1] / "projects/every-villain-tactics/art/TACTICAL-ARENAS-ROUND-1.yaml"
STORY_MAPS = {
    "evt-first-bell-auditorium",
    "evt-science-wing-lockdown",
    "evt-crosswalk-crisis",
    "evt-rooftop-broadcast",
    "evt-under-comet-breach",
    "evt-prom-night-finale",
}
PLAYABLE_ONESHOTS = {
    "evt-fountain-standoff",
    "evt-picnic-plaza",
    "evt-quarry-sub-basement",
    "evt-boiler-room-breach",
}
RESULTS = {"evt-first-bell-cleared", "evt-first-bell-failed"}


def load():
    return yaml.safe_load(LEDGER.read_text())


def test_private_production_queue_is_discoverable_and_safe():
    data = load()
    assert data["round"] == "every-villain-tactics-tactical-arenas-v1"
    assert data["project_slug"] == "every-villain-tactics"
    assert data["is_public"] is False
    assert data["is_mature"] is False
    assert data["cast_loras"] is False
    assert is_auto_ledger(data)
    assert len(data["lanes"]) == 1
    lane = data["lanes"][0]
    assert lane["key"] == "unstable-production"
    assert lane["engine"] == "comfy"
    assert lane["checkpoint"] == "SDXL/sdxlUnstableDiffusers_nihilmania.safetensors"
    assert (lane["steps"], lane["cfg"], lane["sampler"]) == (28, 7, "dpmpp_2m")


def test_tactical_scenes_cover_campaign_and_existing_one_shots_without_duplicates():
    data = load()
    subjects = data["subjects"]
    keys = [s["key"] for s in subjects]
    assets = [s["asset"] for s in subjects]
    seeds = [s["seed"] for s in subjects]
    assert len(subjects) == len(set(keys)) == len(set(assets)) == len(set(seeds)) == 12
    assert set(keys) == STORY_MAPS | PLAYABLE_ONESHOTS | RESULTS
    assert all(asset.startswith("every-villain-tactics/") for asset in assets)
    assert all(subject["lane"] == "unstable-production" for subject in subjects)
    assert all(0 <= subject["priority"] <= 1000 for subject in subjects)
    # The production sweep persists accepted ArtJob IDs into this same ledger.
    # The contract must continue to pass after submission, not only before it.
    for subject in subjects:
        jobs = subject.get("jobs") or {}
        assert set(jobs) <= {"unstable-production"}
        if "unstable-production" in jobs:
            assert isinstance(jobs["unstable-production"], int)
            assert jobs["unstable-production"] > 0
        assert subject["size"] == ("1344x768" if subject["key"] in RESULTS else "1152x768")
    assert all(len(subject["prompt_prose"]) > 250 for subject in subjects)
    assert all(subject["negative"] for subject in subjects)
    assert open_cells(data) == sum(not (subject.get("jobs") or {}).get("unstable-production") for subject in subjects)


def test_subject_specific_prompts_satisfy_quality_check():
    assert ledger_problems(load()) == []
