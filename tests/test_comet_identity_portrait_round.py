"""Prom of Doom identity portraits: source-backed, safe to enqueue, never fake delivery.

This test exercises the production enqueue script's real dry-run path without
credentials or image generation. The asset roster is the 48 existing origin x
affinity signatures plus two legacy guest slots, not 50 different people.
"""
from pathlib import Path
import re

import yaml
from scripts import enqueue_art_requests as enqueue
from scripts.repair_negation_art_prompts import violations


ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "projects/comet-city-academy/art/IDENTITY-PORTRAITS-ROUND-1.yaml"
ORIGINS = {"accident", "mutant", "tech", "magic", "alien", "psychic"}
AFFINITIES = {"fire", "air", "earth", "water", "discipline", "genius", "birthright", "social"}
GUEST_SLOTS = {"animal-technical-training", "stellar-navigation"}


def _ledger():
    return yaml.safe_load(LEDGER.read_text())


def test_exact_student_slots_are_canonically_named_and_deduplicated():
    ledger = _ledger()
    assert ledger["auto_submit"] is True
    assert ledger["status"] == "awaiting-submission"
    assert len(ledger["lanes"]) == 1
    assert ledger["lanes"][0]["engine"] == "krea2"
    subjects = ledger["subjects"]
    assert len(subjects) == 50
    assert {item["entity"] for item in subjects} == (
        {f"{origin}-{affinity}" for origin in ORIGINS for affinity in AFFINITIES} | GUEST_SLOTS
    )
    assert len({item["key"] for item in subjects}) == 50
    assert len({item["asset"] for item in subjects}) == 50
    assert len({item["prompt_prose"] for item in subjects}) == 50
    assert sum(item["title"] == "Zuzu student portrait" for item in subjects) == 2
    assert all(item["size"] == "832x1216" for item in subjects)
    assert all(
        item["asset"] == f"comet-city-academy/identities/{item['entity']}/student"
        for item in subjects
    )
    # The ledger describes intended renders. Job ids and delivery claims only
    # appear when the real queue and exporter have confirmed them.
    assert all(not item.get("jobs") and not item.get("art") for item in subjects)


def test_image_prompts_are_literally_paintable_without_names_or_negation():
    for subject in _ledger()["subjects"]:
        prompt = subject["prompt_prose"]
        name = subject["title"].removesuffix(" student portrait")
        assert name not in prompt, subject["key"]
        assert 200 < len(prompt) < 1350, subject["key"]
        assert "Hand-painted comic illustration with bold ink outlines" in prompt
        assert not re.search(r"\b(?:no|not|never|without|unless|text|lettering|logo)\b", prompt, re.I)
        assert not violations(prompt), subject["key"]
        # A request really goes to the intended Krea 2 pipeline and size.
        body = enqueue.build_request(_ledger(), _ledger()["lanes"][0], subject)
        assert body["engine"] == "krea2"
        assert body["projectSlug"] == "comet-city-academy"
        assert (body["width"], body["height"]) == (832, 1216)


def test_zuzu_is_the_same_physical_person_in_core_and_legacy_guest_scenes():
    people = {s["entity"]: s for s in _ledger()["subjects"]}
    core = people["alien-discipline"]["prompt_prose"]
    guest = people["animal-technical-training"]["prompt_prose"]
    look = core.split(". ", 1)[0]
    assert guest.startswith(look + ". ")
    assert "rust-red weird-west desert duster" in core
    assert "vaulting box" in guest and "academy training gym" in guest
    assert "desk far taller" in core


def test_real_enqueue_script_dry_run(capsys):
    assert enqueue.main([str(LEDGER)]) == 0
    stdout = capsys.readouterr().out
    assert "DRY RUN: 50 of 50 cells would be submitted" in stdout
    assert stdout.count("[krea2-student]") == 50
    assert "REJECTED" not in stdout
