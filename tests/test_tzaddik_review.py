import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = ROOT / "scripts" / "tzaddik_review.py"

spec = importlib.util.spec_from_file_location("tzaddik_review", MODULE_PATH)
tr = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = tr
spec.loader.exec_module(tr)


def _valid_entry(name, **overrides):
    entry = {
        "name": name,
        "region": "Nowhere",
        "domain": "testing",
        "pitch": "A pitch.",
        "wikipedia": "https://en.wikipedia.org/wiki/Test",
        "review_note": "No documented controversy.",
        "tags": ["Education"],
    }
    entry.update(overrides)
    return entry


def _write_docket(tmp_path, date, living_names, memorial_names):
    # tzaddik_review.py only reads parsed dockets, so short lists (not the real
    # 10/10 shape build_tzaddik_discovery.py's own validation requires) are fine here.
    payload = {
        "date": date,
        "living": [dict(_valid_entry(n), _status="living") for n in living_names],
        "memorial": [dict(_valid_entry(n), _status="deceased") for n in memorial_names],
    }
    out_path = tmp_path / f"{date}.md"
    out_path.write_text(tr.btd.render_docket(payload), encoding="utf-8")
    return out_path


def _setup(tmp_path, monkeypatch, living=("Ada Lovelace",), memorial=("Grace Hopper",)):
    monkeypatch.setattr(tr.btd, "DISCOVERY_DIR", tmp_path)
    decisions_path = tmp_path / "discovery-decisions.yaml"
    monkeypatch.setattr(tr, "DECISIONS_PATH", decisions_path)
    _write_docket(tmp_path, "2099-01-01", living, memorial)
    return decisions_path


def test_all_entries_tags_docket_date(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    entries = tr.all_entries()
    dates = {e["date"] for e in entries}
    names = {e["name"] for e in entries}
    assert dates == {"2099-01-01"}
    assert names == {"Ada Lovelace", "Grace Hopper"}


def test_pending_entries_empty_ledger_returns_everything(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    pending = tr.pending_entries()
    assert {e["name"] for e in pending} == {"Ada Lovelace", "Grace Hopper"}


def test_decide_unknown_name_errors(tmp_path, monkeypatch, capsys):
    _setup(tmp_path, monkeypatch)
    rc = tr.decide("Nobody At All", "approved", None)
    assert rc == 1
    assert "does not appear" in capsys.readouterr().err


def test_decide_invalid_decision_errors(tmp_path, monkeypatch, capsys):
    _setup(tmp_path, monkeypatch)
    rc = tr.decide("Ada Lovelace", "maybe", None)
    assert rc == 2


def test_decide_records_and_persists(tmp_path, monkeypatch):
    decisions_path = _setup(tmp_path, monkeypatch)
    rc = tr.decide("Ada Lovelace", "approved", "Great case.", decided_by="silas")
    assert rc == 0
    assert decisions_path.exists()

    decisions = tr.load_decisions()
    record = decisions[tr._norm("Ada Lovelace")]
    assert record["decision"] == "approved"
    assert record["note"] == "Great case."
    assert record["decided_by"] == "silas"
    assert record["docket_date"] == "2099-01-01"


def test_decide_is_idempotent_overwrite(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    tr.decide("Ada Lovelace", "deferred", None)
    tr.decide("Ada Lovelace", "approved", "Changed my mind.")
    decisions = tr.load_decisions()
    record = decisions[tr._norm("Ada Lovelace")]
    assert record["decision"] == "approved"
    assert record["note"] == "Changed my mind."
    assert len(decisions) == 1


def test_decided_name_drops_out_of_pending(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    tr.decide("Ada Lovelace", "rejected", None)
    pending = tr.pending_entries()
    assert {e["name"] for e in pending} == {"Grace Hopper"}


def test_check_reports_pending_and_exits_nonzero(tmp_path, monkeypatch, capsys):
    _setup(tmp_path, monkeypatch)
    rc = tr.check()
    out = capsys.readouterr().out
    assert rc == 1
    assert "Pending: 2" in out


def test_check_exits_zero_when_all_decided(tmp_path, monkeypatch, capsys):
    _setup(tmp_path, monkeypatch)
    tr.decide("Ada Lovelace", "approved", None)
    tr.decide("Grace Hopper", "rejected", None)
    rc = tr.check()
    out = capsys.readouterr().out
    assert rc == 0
    assert "Pending: 0" in out


def test_check_with_no_dockets_reports_nothing(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(tr.btd, "DISCOVERY_DIR", tmp_path)
    monkeypatch.setattr(tr, "DECISIONS_PATH", tmp_path / "discovery-decisions.yaml")
    rc = tr.check()
    assert rc == 0
    assert "No discovery dockets found" in capsys.readouterr().out


def test_show_unknown_name_errors(tmp_path, monkeypatch, capsys):
    _setup(tmp_path, monkeypatch)
    rc = tr.show("Nobody At All")
    assert rc == 1


def test_show_known_name_reports_pending_then_decision(tmp_path, monkeypatch, capsys):
    _setup(tmp_path, monkeypatch)
    rc = tr.show("Ada Lovelace")
    assert rc == 0
    assert "PENDING" in capsys.readouterr().out

    tr.decide("Ada Lovelace", "approved", "Solid case.")
    rc = tr.show("Ada Lovelace")
    assert rc == 0
    out = capsys.readouterr().out
    assert "approved" in out
    assert "Solid case." in out


def test_name_matching_is_case_and_whitespace_insensitive(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    rc = tr.decide("  ada   lovelace ", "approved", None)
    assert rc == 0
    pending = tr.pending_entries()
    assert {e["name"] for e in pending} == {"Grace Hopper"}
