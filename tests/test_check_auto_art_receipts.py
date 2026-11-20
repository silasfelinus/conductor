"""Receipt audit covers missing, recent, partial and complete ArtJob ledgers."""

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_auto_art_receipts import missing_receipts


def ledger(tmp_path, jobs=None):
    root = tmp_path
    path = root / "projects" / "demo" / "art" / "ROUND.yaml"
    path.parent.mkdir(parents=True)
    path.write_text(yaml.safe_dump({
        "auto_submit": True,
        "lanes": [{"key": "krea2"}],
        "subjects": [{"key": "hero", "jobs": jobs or {}}],
    }))
    return path


def test_old_ledger_without_receipts_is_flagged(tmp_path, monkeypatch):
    path = ledger(tmp_path)
    monkeypatch.setattr("check_auto_art_receipts.last_commit_timestamp", lambda *args: 100)
    assert missing_receipts(path, now=100 + 25 * 3600, root=tmp_path)
    assert not missing_receipts(path, now=100 + 23 * 3600, root=tmp_path)


def test_recorded_receipt_is_not_flagged(tmp_path, monkeypatch):
    path = ledger(tmp_path, {"krea2": 50549})
    monkeypatch.setattr("check_auto_art_receipts.last_commit_timestamp", lambda *args: 100)
    assert not missing_receipts(path, now=100 + 48 * 3600, root=tmp_path)
