"""Canon checks for four private Asha Venkataraman repaint candidates."""

from pathlib import Path

import yaml

from scripts.art_ledger_authoring import ledger_problems
from scripts.art_ledger_receipts import receipt_problems
from scripts.repair_negation_art_prompts import violations

LEDGER = (
    Path(__file__).resolve().parents[1]
    / "projects/comet-city-academy/art/CANON-ASHA-FOUR-ARM-REPAINT-2026-11-21.yaml"
)
EXPECTED = {
    "asha-four-arm-hero-rescue-river",
    "asha-four-arm-hero-dance-shelter",
    "asha-four-arm-villain-quartermaster",
    "asha-four-arm-villain-confiscation",
}


def test_four_private_unique_repaint_requests_are_prepared_for_submission():
    data = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
    assert data["project_slug"] == "comet-city-academy"
    assert data["auto_submit"] is True
    assert data["is_public"] is False
    assert data["is_mature"] is False
    assert data["priority"] >= 750
    assert data["lanes"][0]["engine"] == "krea2"
    assert data["lanes"][0]["prompt"] == "prose"
    assert len(data["subjects"]) == 4
    assert {s["key"] for s in data["subjects"]} == EXPECTED
    assert len({s["seed"] for s in data["subjects"]}) == 4
    assert len({s["asset"] for s in data["subjects"]}) == 4
    for subject in data["subjects"]:
        assert subject["lane"] == "krea2"
        assert subject["size"] == "1344x768"
        assert subject["asset"].startswith(
            "comet-city-academy/identities/mutant-discipline/repaint/"
        )
        # Auto Art Generate writes durable ArtJob and ArtImage receipts here
        # after submission. Both a draft and a rendered cell must stay valid.
        assert receipt_problems(subject) == [], subject["key"]
        prose = subject["prompt_prose"]
        assert len(prose) >= 500, subject["key"]
        assert "four" in prose.lower(), subject["key"]
        assert "arms" in prose.lower(), subject["key"]
        assert "lower" in prose.lower(), subject["key"]
        assert "hand" in prose.lower(), subject["key"]
        assert not violations(prose), (subject["key"], violations(prose))
    assert ledger_problems(data) == []


def test_both_outcome_roles_receive_two_distinct_candidates():
    data = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
    assets = [row["asset"] for row in data["subjects"]]
    assert sum("/hero-" in asset for asset in assets) == 2
    assert sum("/villain-" in asset for asset in assets) == 2
    assert {row["seed"] for row in data["subjects"]} == set(range(9344101, 9344105))
