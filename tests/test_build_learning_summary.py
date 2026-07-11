import subprocess
import sys
from pathlib import Path

import scripts.build_learning_summary as bls


SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "build_learning_summary.py"


def rec(**overrides):
    base = {
        "date": "2026-07-11",
        "project": "demo",
        "task": "t-001",
        "kind": "software",
        "stakes": "reversible",
        "passes": 0,
        "outcome": "done",
        "failure_category": None,
        "lesson": "",
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# Aggregation helpers
# ---------------------------------------------------------------------------

def test_success_rate_counts_done_over_closed():
    records = [rec(), rec(outcome="blocked"), rec(outcome="done"), rec(outcome="cancelled")]
    assert bls.success_rate(records) == 0.5


def test_success_rate_none_when_empty():
    assert bls.success_rate([]) is None


def test_average_passes_only_successful_tasks():
    records = [rec(passes=0), rec(passes=2), rec(outcome="blocked", passes=3)]
    assert bls.average_passes(records) == 1.0


def test_failure_category_counts_ignore_null_and_unknown():
    records = [
        rec(failure_category="quality"),
        rec(failure_category="quality"),
        rec(failure_category="transient"),
        rec(failure_category=None),
        rec(failure_category="not-a-category"),
    ]
    counts = bls.failure_category_counts(records)
    assert counts["quality"] == 2
    assert counts["transient"] == 1
    assert "not-a-category" not in counts
    assert None not in counts


# ---------------------------------------------------------------------------
# Kaizen targets
# ---------------------------------------------------------------------------

def test_kaizen_targets_flags_low_success_project():
    records = [
        rec(project="weak", outcome="blocked", failure_category="quality"),
        rec(project="weak", outcome="blocked", failure_category="quality"),
        rec(project="weak", outcome="done"),
        rec(project="strong", outcome="done"),
    ]
    targets = bls.kaizen_targets(records)
    assert any("`weak`" in t for t in targets)
    assert not any("`strong`" in t for t in targets)


def test_kaizen_targets_needs_min_records():
    # Only 2 records for the weak project — below TARGET_MIN_RECORDS, no target.
    records = [
        rec(project="weak", outcome="blocked", failure_category="quality"),
        rec(project="weak", outcome="blocked", failure_category="quality"),
    ]
    targets = bls.kaizen_targets(records)
    assert not any("project `weak`" in t for t in targets)


def test_kaizen_targets_flags_recurring_failure_category():
    records = [rec(outcome="blocked", failure_category="actionable") for _ in range(3)]
    targets = bls.kaizen_targets(records)
    assert any("`actionable`" in t for t in targets)


# ---------------------------------------------------------------------------
# Ledger loading
# ---------------------------------------------------------------------------

def test_load_records_missing_file(tmp_path):
    assert bls.load_records(tmp_path / "nope.yaml") == []


def test_load_records_empty_ledger(tmp_path):
    ledger = tmp_path / "LEARNING.yaml"
    ledger.write_text("records: []\n")
    assert bls.load_records(ledger) == []


def test_load_records_skips_non_dict_entries(tmp_path):
    ledger = tmp_path / "LEARNING.yaml"
    ledger.write_text("records:\n  - not-a-record\n  - {project: demo, task: t-001, outcome: done}\n")
    records = bls.load_records(ledger)
    assert len(records) == 1
    assert records[0]["project"] == "demo"


def test_load_records_invalid_yaml_returns_empty(tmp_path):
    ledger = tmp_path / "LEARNING.yaml"
    ledger.write_text("records: [unclosed\n")
    assert bls.load_records(ledger) == []


# ---------------------------------------------------------------------------
# Report assembly
# ---------------------------------------------------------------------------

def test_report_empty_ledger_is_graceful():
    report = bls.build_report([])
    assert "No records yet" in report
    assert "LEARNING-REPORT.md" in report


def test_report_contains_all_sections():
    records = [
        rec(lesson="reuse days_since from build_kaizen"),
        rec(project="other", outcome="blocked", failure_category="scope", passes=2),
    ]
    report = bls.build_report(records)
    for heading in ("## Overall", "## By project", "## By kind", "## Failure categories",
                    "## Kaizen targets", "## Recent lessons"):
        assert heading in report
    assert "reuse days_since from build_kaizen" in report
    assert "| scope | 1 |" in report


def test_report_recent_lessons_newest_first_and_capped():
    records = [
        rec(task=f"t-{i:03d}", lesson=f"lesson {i}", date=f"2026-07-{i:02d}")
        for i in range(1, 15)
    ]
    report = bls.build_report(records)
    assert "lesson 14" in report
    assert "lesson 4" not in report  # capped at RECENT_LESSONS (10)
    assert report.index("lesson 14") < report.index("lesson 5")  # newest first


# ---------------------------------------------------------------------------
# CLI smoke
# ---------------------------------------------------------------------------

def test_cli_dry_run_does_not_write(tmp_path):
    ledger = tmp_path / "LEARNING.yaml"
    ledger.write_text("records:\n  - {project: demo, task: t-001, kind: software, outcome: done, passes: 0}\n")
    out = tmp_path / "LEARNING-REPORT.md"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--dry-run", "--ledger", str(ledger), "--output", str(out)],
        capture_output=True, text=True, check=True,
    )
    assert "## Overall" in result.stdout
    assert not out.exists()


def test_cli_writes_output(tmp_path):
    ledger = tmp_path / "LEARNING.yaml"
    ledger.write_text("records: []\n")
    out = tmp_path / "LEARNING-REPORT.md"
    subprocess.run(
        [sys.executable, str(SCRIPT), "--ledger", str(ledger), "--output", str(out)],
        capture_output=True, text=True, check=True,
    )
    assert out.exists()
    assert "No records yet" in out.read_text()
