"""Homepage art stays individualized and slots stay discoverable in Advert Studio."""

import re
from pathlib import Path

import pytest
import yaml

from scripts.enqueue_art_requests import cell_request_key, iter_cells
from scripts.art_ledger_authoring import ledger_problems

LEDGER_PATH = Path("projects/interface-vision/art/HOMEPAGE-IDENTITIES-2026-11-17.yaml")


def test_eight_different_pieces_have_a_single_eligible_render_lane():
    ledger = yaml.safe_load(LEDGER_PATH.read_text())
    assert ledger["auto_submit"] is True
    assert ledger["project_slug"] == "adverts"
    assert len(ledger["subjects"]) == 8
    assert len(list(iter_cells(ledger))) == 8
    assert not ledger_problems(ledger)
    assert len({item["prompt_prose"] for item in ledger["subjects"]}) == 8
    assert len({item["seed"] for item in ledger["subjects"]}) == 8
    slots = [item["advert_slot"] for item in ledger["subjects"] if item.get("advert_slot")]
    assert len(slots) == len(set(slots)) == 7


def test_slot_requests_use_advert_studio_request_keys():
    ledger = yaml.safe_load(LEDGER_PATH.read_text())
    path = LEDGER_PATH.as_posix()
    for subject, lane in iter_cells(ledger):
        key = cell_request_key(path, ledger, lane, subject)
        if slot := subject.get("advert_slot"):
            assert re.fullmatch(r"advert-studio:adverts/[a-z0-9-]+/hero@[a-f0-9]{12}", key)
            assert key.startswith(f"advert-studio:{slot}@")
        else:
            assert key.startswith("conductor:ledger:")


def test_slot_keys_change_when_prompts_change():
    ledger = yaml.safe_load(LEDGER_PATH.read_text())
    subject, lane = next(iter_cells(ledger))
    before = cell_request_key("round.yaml", ledger, lane, subject)
    changed = dict(subject, prompt_prose=subject["prompt_prose"] + " Extra lantern light.")
    after = cell_request_key("round.yaml", ledger, lane, changed)
    assert before != after


def test_advert_slot_only_allowed_in_adverts_project():
    ledger = yaml.safe_load(LEDGER_PATH.read_text())
    subject, lane = next(iter_cells(ledger))
    with pytest.raises(ValueError, match="Invalid Advert Studio art slot"):
        cell_request_key("round.yaml", {**ledger, "project_slug": "other"}, lane, subject)
    with pytest.raises(ValueError, match="Invalid Advert Studio art slot"):
        cell_request_key("round.yaml", ledger, lane, {**subject, "advert_slot": "adverts/../hero"})
