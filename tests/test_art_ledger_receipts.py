"""Stop draft-only receipt assertions from breaking after Auto Art Generate runs.

The queue writes durable ArtJob/ArtImage receipts to ledgers in separate commits;
tests must accept both initial requests and later accepted/rendered states.
"""

import ast
from pathlib import Path

from scripts.art_ledger_receipts import receipt_problems

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
SUBJECT_NAMES = {"subject", "item", "row", "entry", "s"}


def forbidden_draft_assertions(source: str) -> list[int]:
    """Detect direct 'no receipts' asserts against production ledger subjects."""
    if "yaml.safe_load" not in source or "/art/" not in source:
        return []
    found = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Assert):
            continue
        expr = node.test
        if not isinstance(expr, ast.Compare) or len(expr.ops) != 1:
            continue
        if not isinstance(expr.ops[0], ast.NotIn):
            continue
        if not isinstance(expr.left, ast.Constant):
            continue
        if expr.left.value not in ("jobs", "art"):
            continue
        if not isinstance(expr.comparators[0], ast.Name):
            continue
        if expr.comparators[0].id in SUBJECT_NAMES:
            found.append(node.lineno)
    return found


def test_no_committed_art_ledger_test_assumes_receipts_never_appear():
    offenders = []
    for path in sorted(TESTS.rglob("test_*.py")):
        for line in forbidden_draft_assertions(path.read_text(encoding="utf-8")):
            offenders.append(f"{path.relative_to(ROOT)}:{line}")
    assert not offenders, (
        "Auto Art Generate adds receipt fields after submissions. "
        "Use scripts.art_ledger_receipts.receipt_problems(subject) "
        "to accept both unsubmitted and durable receipts: "
        + ", ".join(offenders)
    )


def test_meta_guard_catches_both_regressions_without_false_positives():
    bad = '''
import yaml
LEDGER = ROOT / "projects/comet-city-academy/art/FUTURE-ROUND.yaml"
ledger = yaml.safe_load(LEDGER.read_text())
for item in ledger["subjects"]:
    assert "jobs" not in item
    assert "art" not in item
    assert item["lane"] == "krea2"
'''
    assert forbidden_draft_assertions(bad) == [5, 6]
    safe = bad.replace('assert "jobs" not in item', 'assert receipt_problems(item) == []')
    safe = safe.replace('assert "art" not in item', 'assert item["lane"] == "krea2"')
    assert forbidden_draft_assertions(safe) == []


def test_draft_queued_and_done_receipts_are_distinct_valid_states():
    base = {"key": "result", "lane": "krea2"}
    assert receipt_problems(base) == []
    queued = {**base, "jobs": {"krea2": 76459}}
    assert receipt_problems(queued) == []
    pending = {
        **queued,
        "art": {"krea2": {"status": "PENDING", "art_image_id": None}},
    }
    assert receipt_problems(pending) == []
    done = {
        **queued,
        "art": {"krea2": {"status": "DONE", "art_image_id": 278333}},
    }
    assert receipt_problems(done) == []


def test_art_receipt_guard_rejects_false_done_and_wrong_lanes():
    base = {"key": "result", "lane": "krea2"}
    assert receipt_problems({**base, "jobs": {"other": 76459}})
    assert receipt_problems({**base, "jobs": {"krea2": "job-76459"}})
    assert receipt_problems(
        {**base, "jobs": {"krea2": 76459},
         "art": {"krea2": {"status": "DONE", "art_image_id": None}}}
    )
    assert receipt_problems(
        {**base, "art": {"krea2": {"status": "DONE", "art_image_id": 278333}}}
    )
