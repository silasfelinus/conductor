"""A superseded historical review round should not fail the art evidence job."""
import importlib.util
import json
import sys
from pathlib import Path


MODULE = Path(__file__).resolve().parents[1] / "projects/shifting-desks/art/build_review_sheets.py"


def load():
    spec = importlib.util.spec_from_file_location("shifting_desks_build_review_sheets", MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_superseded_round_is_clean_empty_report(tmp_path, monkeypatch):
    mod = load()
    monkeypatch.setattr(mod, "latest_unreviewed", lambda only_round=None: [])
    monkeypatch.setattr(sys, "argv", ["build_review_sheets.py", "--round", "19", "--out", str(tmp_path)])
    assert mod.main() == 0
    assert json.loads((tmp_path / "summary.json").read_text()) == {
        "selected": 0, "received": 0, "missing": 0, "pages": 0,
    }
    assert json.loads((tmp_path / "manifest.json").read_text()) == []


def test_unscoped_empty_evidence_remains_failure(tmp_path, monkeypatch):
    mod = load()
    monkeypatch.setattr(mod, "latest_unreviewed", lambda only_round=None: [])
    monkeypatch.setattr(sys, "argv", ["build_review_sheets.py", "--out", str(tmp_path)])
    assert mod.main() == 1
