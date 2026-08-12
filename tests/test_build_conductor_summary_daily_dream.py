import importlib
import json
from pathlib import Path

import scripts.build_conductor_summary as summary


def test_failed_daily_dream_is_forced_into_model_summary():
    outcome = {
        "status": "failed",
        "message": "filing-echidna: API calls failed",
        "retry": True,
    }

    rendered = summary.ensure_daily_dream_failure_is_visible(
        "## ALL CLEAR\nEverything is fine.\n\n**Stats:** 0 ready",
        outcome,
    )

    assert rendered.startswith("## ACTION NEEDED")
    assert "Daily-dream creation failed" in rendered
    assert "no completed bundle was recorded" in rendered


def test_daily_dream_status_file_preserves_machine_readable_outcome(tmp_path, monkeypatch):
    path = tmp_path / "daily-dream-status.json"
    monkeypatch.setattr(summary, "DAILY_DREAM_STATUS_PATH", str(path))
    outcome = {"status": "built", "proposal": "today.md", "art_requests": 6}

    summary.write_daily_dream_status(outcome)

    assert json.loads(path.read_text(encoding="utf-8")) == outcome


def test_report_only_daily_dream_accepts_summary_dry_run_keyword(monkeypatch):
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    monkeypatch.syspath_prepend(str(scripts_dir))
    report_only = importlib.import_module("build_conductor_summary_report_only")

    outcome = report_only.report_only_daily_dream(dry_run=True)

    assert outcome == {
        "status": "idle",
        "message": "Daily Dream creation is owned by the ordered daily-digest cycle.",
    }
