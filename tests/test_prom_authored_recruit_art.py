"""Contract for the four previously authored, not-yet-recruited Prom companions."""

from pathlib import Path

import yaml


LEDGER = (
    Path(__file__).resolve().parents[1]
    / "projects/comet-city-academy/art/AUTHORED-RECRUITS-PORTRAITS-2026-11-20.yaml"
)
RECRUITS = {
    "vesna-duarte": "Vesna Duarte",
    "bram-kowalczyk": "Bram Kowalczyk",
    "femi-ilunga": "Femi Ilunga",
    "cyrus-adeyemi": "Cyrus Adeyemi",
}


def test_authored_recruit_portraits_are_private_and_canon_consistent():
    ledger = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
    assert ledger["project_slug"] == "comet-city-academy"
    assert ledger["auto_submit"] is True
    assert ledger["is_public"] is False
    assert ledger["is_mature"] is False
    assert ledger["lanes"][0]["engine"] == "krea2"

    subjects = ledger["subjects"]
    assert len(subjects) == 8
    assert len({subject["key"] for subject in subjects}) == 8
    assert len({subject["asset"] for subject in subjects}) == 8
    assert len({subject["seed"] for subject in subjects}) == 8

    for slug, name in RECRUITS.items():
        for state in ("neutral", "injured"):
            matches = [
                subject
                for subject in subjects
                if subject["key"] == f"recruit-{slug}-{state}"
            ]
            assert len(matches) == 1
            subject = matches[0]
            assert subject["asset"] == f"comet-city-academy/recruits/{slug}/{state}"
            assert name in subject["title"]
            assert name in subject["prompt_prose"]
            assert subject["size"] == "768x1024"
            assert "jobs" not in subject
            assert "art" not in subject
