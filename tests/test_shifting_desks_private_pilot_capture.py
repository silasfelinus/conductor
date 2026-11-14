"""Private fidelity pilot capture must preserve provenance and keep queued work pending."""
import importlib.util
from pathlib import Path

import pytest

pytest.importorskip("PIL")

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "projects/shifting-desks/art/build_recovery_sheets.py"
spec = importlib.util.spec_from_file_location("shifting_recovery_sheets", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_v1_historical_pilot_is_not_replaced_by_v2():
    old = list(module.pilot_rows(1))
    assert len(old) == 6
    assert all(row["_round"] == "PILOT-V1" for row in old)
    assert all(row["status"] == "DONE" and row["image"] for row in old)


def test_v2_subject_only_pilot_has_three_isolated_queued_jobs():
    rows = list(module.pilot_rows(2))
    assert len(rows) == 3
    assert {row["key"] for row in rows} == {
        "rear-eyes--krea-prose",
        "living-corridor--krea-prose",
        "mutation-tank--krea-prose",
    }
    assert {row["job"] for row in rows} == {69090, 69091, 69092}
    assert all(row["_round"] == "PILOT-V2" for row in rows)
    assert all(row["pass"] and row["fail"] for row in rows)


def test_pending_v2_jobs_cannot_be_passed_off_as_delivered(monkeypatch):
    rows = list(module.pilot_rows(2))
    monkeypatch.setattr(module, "fetch_source_image", lambda _: (_ for _ in ()).throw(AssertionError("unexpected media fetch")))
    for row in rows:
        if row["status"] == "PENDING":
            image, evidence = module.capture_pilot(row)
            assert image is None
            assert "DONE" in evidence["error"]


def test_unknown_pilot_version_fails_closed():
    with pytest.raises(ValueError, match="unsupported"):
        list(module.pilot_rows(3))
