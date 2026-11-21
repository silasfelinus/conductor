"""Space Couch final-choice outcome requests must exactly match the playable stories."""

from pathlib import Path

import yaml

from scripts.art_ledger_authoring import ledger_problems
from scripts.repair_negation_art_prompts import violations

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "projects/game-of-captains/art/ACT-THREE-CHAPTER-NINE-OUTCOMES-ROUND-1.yaml"

FINAL_CHOICES = {
    "warp-e8-windglass-exodus": (
        "carry-unopened-map",
        "inspect-route-with-escrow",
        "seize-public-passage-lane",
    ),
    "warp-e9-tellurian-deposit": (
        "publish-crew-corrections",
        "forensic-account-audit",
        "repair-roof-for-deposit",
    ),
}


def test_all_final_destinations_request_individually_painted_results():
    ledger = yaml.safe_load(LEDGER.read_text())
    subjects = ledger["subjects"]
    expected = {
        f"{episode}-{choice}-{outcome}"
        for episode, choices in FINAL_CHOICES.items()
        for choice in choices
        for outcome in ("success", "failure")
    }
    assert ledger["round"] == "space-couch-chapter-nine-outcomes-1"
    assert ledger["project_slug"] == "game-of-captains"
    assert ledger["auto_submit"] is True
    assert ledger["is_public"] is False
    assert ledger["is_mature"] is False
    assert len(subjects) == 12
    assert {subject["key"] for subject in subjects} == expected
    assert len({subject["asset"] for subject in subjects}) == 12
    assert len({subject["seed"] for subject in subjects}) == 12
    assert all(subject["size"] == "1344x768" for subject in subjects)
    assert all(subject["lane"] == "krea2" for subject in subjects)
    assert all(
        subject["asset"] == f'game-of-captains/consequences/{subject["key"]}'
        for subject in subjects
    )


def test_private_requests_do_not_claim_generated_or_accepted_art():
    ledger = yaml.safe_load(LEDGER.read_text())
    for subject in ledger["subjects"]:
        assert "jobs" not in subject
        assert "art" not in subject
        assert subject["entity"] == "encounter-outcome"
        description = subject["prompt_prose"].lower()
        assert len(description) >= 420, subject["key"]
        assert any(word in description for word in ("red", "scarlet", "crimson"))
        assert any(word in description for word in ("couch", "sofa"))
        assert "alien" in description
        assert any(word in description for word in ("bubble", "shield", "sphere", "oxygen"))
        assert not violations(subject["prompt_prose"]), subject["key"]
    assert ledger_problems(ledger) == []
