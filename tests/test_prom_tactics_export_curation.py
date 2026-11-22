"""Prom and Tactics renders require explicit approval before gameplay export."""

import json
import subprocess
import sys
from pathlib import Path

import yaml

from scripts.export_round_art import approved_for_export, audit, plan

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "scripts/export_round_art.py"


def _candidate(verdict=None):
    row = {
        "key": "canon-hero",
        "asset": "comet-city-academy/identities/mutant-discipline/hero",
        "lane": "krea2",
        "jobs": {"krea2": 76529},
        "art": {"krea2": {"status": "DONE", "art_image_id": 123456}},
    }
    if verdict:
        row["verdict"] = verdict
    return row


def test_approval_gate_distinguishes_done_keep_and_reject(tmp_path):
    candidate = _candidate()
    assert not approved_for_export(candidate, require_keep=True)
    assert audit([candidate], tmp_path, "", require_keep=True)["counts"] == {
        "curation-needed": 1
    }
    assert plan([candidate], tmp_path, "", require_keep=True) == []
    candidate["verdict"] = "keep: inspected canonical four arms"
    assert approved_for_export(candidate, require_keep=True)
    assert len(plan([candidate], tmp_path, "", require_keep=True)) == 1
    candidate["verdict"] = "reject: incorrect anatomy"
    assert not approved_for_export(candidate, require_keep=True)
    assert plan([candidate], tmp_path, "", require_keep=True) == []


def test_protected_project_cli_enforces_approval_without_flag(tmp_path):
    for project in ("comet-city-academy", "every-villain-tactics"):
        ledger = tmp_path / f"{project}.yaml"
        ledger.write_text(
            yaml.safe_dump({"project_slug": project, "subjects": [_candidate()]})
        )
        result = subprocess.run(
            [
                sys.executable,
                str(EXPORT),
                str(ledger),
                "--kind-robots",
                str(tmp_path),
                "--audit",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        report = json.loads(result.stdout)
        assert report["counts"] == {"curation-needed": 1}
        assert report["rows"][0]["art_image_id"] == 123456
        assert report["rows"][0]["art_job_ids"] == [76529]


def test_other_projects_preserve_existing_opt_in_behavior(tmp_path):
    ledger = tmp_path / "other.yaml"
    ledger.write_text(
        yaml.safe_dump({"project_slug": "game-of-captains", "subjects": [_candidate()]})
    )
    result = subprocess.run(
        [
            sys.executable,
            str(EXPORT),
            str(ledger),
            "--kind-robots",
            str(tmp_path),
            "--audit",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(result.stdout)["counts"] == {"export-ready": 1}
