"""Live submissions must match authoring ledgers; fulfilled rows may leave the queue."""
import copy
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from repair_negation_art_prompts import violations  # noqa: E402


def check_submission_copies(requests, subjects):
    ids = [row["id"] for row in requests]
    assert len(ids) == len(set(ids)), "duplicate submission request"
    for subject in subjects:
        assert not violations(subject["prompt"]), subject["request_id"]
    for request in requests:
        matches = [subject for subject in subjects if subject["request_id"] == request["id"]]
        assert len(matches) == 1, ("missing or duplicate authoring subject", request["id"])
        subject = matches[0]
        assert " ".join(subject["prompt"].split()) == " ".join(request["prompt"].split()), request["id"]
        for field in ("engine", "size", "seed"):
            assert subject[field] == request[field], (request["id"], field)


def test_shifting_desks_rounds_match_submission_queue():
    requests = yaml.safe_load((ROOT / "projects/art-prompts.yaml").read_text())["requests"]
    requests = [row for row in requests if str(row.get("id", "")).startswith("shifting-desks-r")]
    subjects = []
    for ledger in sorted((ROOT / "projects/shifting-desks/art").glob("ROUND-*.yaml")):
        subjects.extend(yaml.safe_load(ledger.read_text())["subjects"])
    # build_workspace.py prunes completed submissions after the consumer fulfills them.
    # The round ledger remains durable history, not a demand to submit retired art again.
    check_submission_copies(requests, subjects)


@pytest.fixture
def queued_subject():
    subject = {"request_id": "shifting-desks-r2-example", "prompt": "A brass desk lamp, every surface bare and unmarked",
               "engine": "krea2", "size": "832x1248", "seed": 52001}
    request = {"id": subject["request_id"], **{key: value for key, value in subject.items() if key != "request_id"}}
    return request, subject


def test_fulfilled_request_can_leave_queue(queued_subject):
    request, subject = queued_subject
    check_submission_copies([request], [subject])
    check_submission_copies([], [subject])


@pytest.mark.parametrize("field", ["prompt", "engine", "size", "seed"])
def test_live_submission_drift_is_rejected(queued_subject, field):
    request, subject = queued_subject
    changed = copy.deepcopy(request)
    changed[field] = "changed"
    with pytest.raises(AssertionError):
        check_submission_copies([changed], [subject])


def test_duplicate_live_submission_is_rejected(queued_subject):
    request, subject = queued_subject
    with pytest.raises(AssertionError, match="duplicate submission request"):
        check_submission_copies([request, request], [subject])


@pytest.mark.parametrize("duplicate", [False, True])
def test_live_submission_requires_one_authoring_subject(queued_subject, duplicate):
    request, subject = queued_subject
    with pytest.raises(AssertionError, match="authoring subject"):
        check_submission_copies([request], [subject, subject] if duplicate else [])
