"""t-072: a pinned manifest + ledger fixture.

A drift between the Kind Robots runtime path manifest and the audit's
builder_reachable totals (for example a renamed manifest key, a media-path
prefix change, or a classification rule change) fails here instead of
silently reclassifying shipped assets as unreferenced.
"""
import json
import shutil
from pathlib import Path

from scripts.audit_emperor_art_inventory import inventory

FIXTURE = Path(__file__).parent / "fixtures" / "emperor_art_inventory"


def test_pinned_fixture_counts(tmp_path):
    ledgers = tmp_path / "ledgers"
    ledgers.mkdir()
    shutil.copy(FIXTURE / "ledger.yaml", ledgers / "FIXTURE.yaml")
    app = tmp_path / "app"
    (app / "utils/emperorOfDust").mkdir(parents=True)
    for rel in json.loads((FIXTURE / "shipped.json").read_text()):
        path = app / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"RIFF\x00\x00\x00\x00WEBP")
    report = inventory(ledgers, app, FIXTURE / "runtime-paths.json")
    expected = json.loads((FIXTURE / "expected-summary.json").read_text())
    actual = {key: report["summary"][key] for key in expected}
    assert actual == expected
    classes = {row["asset"]: row["reference_class"] for row in report["assets"]}
    assert classes["chance-events/rain/care"] == "builder_reachable"
    assert classes["playbook/orphan-preview"] == "unreferenced"
    # Cast art resolves under public/emperor-of-dust/cast/ (2026-11-21 fix).
    exported = {row["asset"]: row["exported"] for row in report["assets"]}
    assert exported["followers/F001/portrait/neutral"] is True
