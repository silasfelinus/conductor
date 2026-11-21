"""Chapter-nine scene requests stay specific, unique and unsubmitted until verified."""
from pathlib import Path

import yaml

from scripts.art_ledger_authoring import ledger_problems
from scripts.repair_negation_art_prompts import violations


LEDGER = (
    Path(__file__).resolve().parent.parent
    / "projects/game-of-captains/art/ACT-THREE-CHAPTER-NINE-SCENES-ROUND-1.yaml"
)


def test_chapter_nine_scene_ledger_has_twelve_distinct_paintable_subjects():
    ledger = yaml.safe_load(LEDGER.read_text())
    subjects = ledger["subjects"]
    assert ledger["project_slug"] == "game-of-captains"
    assert ledger["auto_submit"] is True
    assert ledger["is_public"] is False
    assert ledger["is_mature"] is False
    assert len(subjects) == 12
    assert len({subject["key"] for subject in subjects}) == 12
    assert len({subject["asset"] for subject in subjects}) == 12
    assert len({subject["seed"] for subject in subjects}) == 12
    assert all(subject["asset"] == f'game-of-captains/chapter-nine/{subject["key"]}' for subject in subjects)
    assert all(subject["size"] == "1344x768" for subject in subjects)
    assert all("red" in subject["prompt_prose"].lower() or "scarlet" in subject["prompt_prose"].lower() or "crimson" in subject["prompt_prose"].lower() for subject in subjects)
    assert all("alien" in subject["prompt_prose"].lower() for subject in subjects)
    assert all(not violations(subject["prompt_prose"]) for subject in subjects)
    assert ledger_problems(ledger) == []


def test_chapter_nine_paintings_have_distinct_story_action():
    ledger = yaml.safe_load(LEDGER.read_text())
    by_key = {subject["key"]: subject["prompt_prose"].lower() for subject in ledger["subjects"]}
    for key, prop in {
        "inquiry-reveal": "retired lifeboat pilot",
        "inquiry-testify": "dozen different witnesses",
        "inquiry-independent": "separate copies",
        "inquiry-withhold": "broadcast microphone",
        "windglass-exodus-reveal": "folded blankets",
        "windglass-exodus-sealed": "sealed cylinder",
        "windglass-exodus-verify": "outer safety seals",
        "windglass-exodus-open": "refugee parent",
        "deposit-copy-reveal": "six delicate arms",
        "deposit-copy-truth": "brass balance",
        "deposit-copy-compare": "contradictory physical diagrams",
        "deposit-copy-rewrite": "counterfeit book",
    }.items():
        assert prop in by_key[key], key



def test_chapter_nine_submitted_jobs_are_traceable_without_fake_acceptance():
    """Submitted renders must never masquerade as inspected, delivered art."""
    ledger = yaml.safe_load(LEDGER.read_text())
    subjects = ledger["subjects"]
    job_ids = []
    for subject in subjects:
        assert set(subject["jobs"]) == {"krea2"}
        job_id = subject["jobs"]["krea2"]
        assert isinstance(job_id, int) and job_id > 0
        job_ids.append(job_id)

        art = subject["art"]["krea2"]
        assert art["status"] in {"PENDING", "REJECTED", "ACCEPTED"}
        if art["status"] == "PENDING":
            assert art["art_image_id"] is None
        elif art["status"] == "ACCEPTED":
            assert isinstance(art["art_image_id"], int)
            assert art["art_image_id"] > 0

    assert len(set(job_ids)) == len(subjects)
