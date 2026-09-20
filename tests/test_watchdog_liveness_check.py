"""Contract tests for check-watchdog-liveness.ps1 (conductor/t-180).

Neither this script nor a live Task Scheduler entry can be executed here (no
PowerShell, no Windows), so these lock the properties that make the check
actually catch the 2026-09-08..2026-09-19 incident it exists to prevent: a
watchdog that fires on schedule and fails every time (LastTaskResult
non-zero) or that never reaches its own tick line (a stale log), both of
which looked identical to healthy from Task Scheduler's own view.
"""
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HOME_SERVER = REPO / "ops" / "home-server"
SCRIPT = HOME_SERVER / "check-watchdog-liveness.ps1"
WRAPPER = HOME_SERVER / "check-watchdog-liveness-hidden.vbs"


def _source() -> str:
    return SCRIPT.read_text(encoding="utf-8")


def test_ascii_only() -> None:
    """Same reason as healthcheck.ps1: a no-BOM file parses as the system
    ANSI codepage under Windows PowerShell 5.1, so one stray non-ASCII byte
    in a string literal corrupts parsing of the WHOLE file -- the exact
    failure mode this script exists to detect in a sibling script."""
    bad = [(i, b) for i, b in enumerate(SCRIPT.read_bytes()) if b > 127]
    assert bad == [], f"non-ASCII bytes at {bad[:5]}"


def test_braces_and_parens_balance() -> None:
    text = _source()
    assert text.count("{") == text.count("}")
    assert text.count("(") == text.count(")")


def test_reads_last_task_result_and_log_write_age() -> None:
    source = _source()
    assert "Get-ScheduledTaskInfo" in source
    assert "LastTaskResult" in source
    assert "$logFile" in source
    assert "LastWriteTime" in source
    assert "[int]$staleMinutes = 30" in source or "$staleMinutes = 30" in source


def test_default_watched_task_name_matches_the_registered_task() -> None:
    """README.md registers the watchdog as AI-Backends-Healthcheck; if this
    default silently drifted from that name, the check would find no task
    and report a false "not found" against a perfectly real one."""
    source = _source()
    assert "'AI-Backends-Healthcheck'" in source
    readme = (HOME_SERVER / "README.md").read_text(encoding="utf-8")
    assert '"AI-Backends-Healthcheck"' in readme


def test_never_restarts_anything() -> None:
    """This is a detector, not a second watchdog -- it must not overlap
    healthcheck.ps1's own restart authority."""
    source = _source().lower()
    assert "restart-supervised" not in source
    assert "restart-service" not in source
    assert "stop-process" not in source
    assert "it does not restart anything" in _source().lower()


def test_uses_its_own_state_file_not_healthchecks() -> None:
    """A shared alert-state.json risks read/write contention with
    healthcheck.ps1's own 5-minute tick; this check owns a separate file."""
    source = _source()
    assert "watchdog-liveness-state.json" in source
    assert "alert-state.json" not in source


def test_alerts_are_deduplicated_and_clear_on_recovery() -> None:
    source = _source()
    assert "Test-LivenessAlertDue" in source
    assert "$cooldownMinutes = 60" in source
    assert "state.Remove('last_alert')" in source


def test_hidden_wrapper_points_at_the_liveness_script() -> None:
    wrapper = WRAPPER.read_text(encoding="utf-8")
    assert "check-watchdog-liveness.ps1" in wrapper
    assert "shell.Run(command, 0, True)" in wrapper
