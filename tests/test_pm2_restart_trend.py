from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "ops" / "home-server" / "check-pm2-restart-trend.ps1"


def _source() -> str:
    return SCRIPT.read_text(encoding="utf-8")


def test_restart_trend_check_is_advisory_only() -> None:
    source = _source()
    assert "severity = 'advisory'" in source
    assert "signal = 'pm2-restart-trend'" in source
    assert "pm2 restart" not in source.lower()
    assert "pm2 delete" not in source.lower()
    assert "pm2 stop" not in source.lower()


def test_restart_trend_uses_normalized_restart_time_and_slow_window() -> None:
    source = _source()
    assert "pm2-jlist-snapshot.js" in source
    assert "[int]$process.restart_time" in source
    assert "[int]$WindowHours = 168" in source
    assert "[int]$WindowRestartDelta = 10" in source
    assert "[int]$AbsoluteRestartThreshold = 25" in source


def test_restart_trend_persists_baseline_and_deduplicates_alerts() -> None:
    source = _source()
    assert "baseline_restart_time" in source
    assert "baseline_at" in source
    assert "last_alert_restart_time" in source
    assert "Set-Content -LiteralPath $StatePath" in source
    assert "$restarts -gt [int]$entry.last_alert_restart_time" in source
