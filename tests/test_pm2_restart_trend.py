from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME_SERVER = ROOT / "ops" / "home-server"
SCRIPT = HOME_SERVER / "check-pm2-restart-trend.ps1"


def _source() -> str:
    return SCRIPT.read_text(encoding="utf-8")


def _code() -> str:
    """Source with whole-line comments removed.

    These files carry long incident narratives that quote the broken code they
    replaced, so a bare `"<bad pattern>" not in source` check trips on the
    explanation rather than on a regression.
    """
    return "\n".join(
        line for line in _source().splitlines() if not line.lstrip().startswith("#")
    )


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
    assert "$process.pm2_env.restart_time" in _code()
    assert "[int]$WindowHours = 168" in source
    assert "[int]$WindowRestartDelta = 10" in source
    assert "[int]$AbsoluteRestartThreshold = 25" in source


def test_restart_trend_reads_the_path_the_projection_actually_emits() -> None:
    """Derive the expected field path from pm2-jlist-snapshot.js rather than
    restating it, so the two files cannot drift apart again.

    2026-09-20: this check read `$process.restart_time` -- the top level, where
    the projection has never put it. PowerShell yields $null for a missing
    property instead of raising and [int]$null is 0, so every app scored 0
    restarts: 0 never reaches the absolute threshold (25) and a 0-0 delta never
    reaches the trend threshold (10). The check had never advised once, on a box
    that reached 89 restarts. The previous version of this test asserted the
    broken path was present, which pinned the bug in place.
    """
    import json
    import subprocess

    projected = json.loads(
        subprocess.run(
            ["node", str(HOME_SERVER / "pm2-jlist-snapshot.js")],
            input=json.dumps(
                [{"name": "comfyui", "pm2_env": {"status": "online", "restart_time": 89}}]
            ),
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    )[0]

    assert "restart_time" not in projected, "projection must not expose it at the top level"
    assert projected["pm2_env"]["restart_time"] == 89

    code = _code()
    assert "$process.pm2_env.restart_time" in code
    assert "$process.restart_time" not in code, "the top-level read always yields 0"


def test_restart_trend_persists_baseline_and_deduplicates_alerts() -> None:
    source = _source()
    assert "baseline_restart_time" in source
    assert "baseline_at" in source
    assert "last_alert_restart_time" in source
    assert "Set-Content -LiteralPath $StatePath" in source
    assert "$restarts -gt [int]$entry.last_alert_restart_time" in source


def test_watchdog_tick_runs_restart_trend_without_making_it_health_critical() -> None:
    runner = (HOME_SERVER / "healthcheck-runner.ps1").read_text(encoding="utf-8")
    wrapper = (HOME_SERVER / "healthcheck-hidden.vbs").read_text(encoding="utf-8")
    assert "& $healthcheck" in runner
    assert "& $restartTrend" in runner
    assert "try {" in runner and "catch {" in runner
    assert "healthcheck-runner.ps1" in wrapper

def test_restart_trend_enumerates_the_snapshot_the_way_healthcheck_does() -> None:
    """Windows PowerShell 5.1's ConvertFrom-Json emits a JSON array as ONE
    object instead of enumerating it, so `foreach` over the result binds
    $process to the whole array and every $process.<field> is member
    enumeration returning Object[].

    2026-09-20 on a four-app box: `[int]$process.restart_time` read a property
    no element had, member-enumerated to nothing, and [int]$null scored 0
    restarts for everything -- silently. Correcting the path to
    pm2_env.restart_time then read all four values at once and the [int] cast
    threw, surfacing only because healthcheck-runner.ps1 wraps this in
    try/catch.

    healthcheck.ps1 consumes the same helper and has always piped it through
    ForEach-Object. Derive the requirement from that file rather than restating
    it, so the working pattern and this one cannot diverge.
    """
    healthcheck = (HOME_SERVER / "healthcheck.ps1").read_text(encoding="utf-8")
    assert "$pm2List | ForEach-Object" in healthcheck, (
        "healthcheck.ps1 changed how it enumerates the snapshot; re-derive this rule"
    )

    assert "ConvertFrom-Json | ForEach-Object" in _code(), (
        "a bare ConvertFrom-Json does not enumerate a JSON array under PowerShell 5.1"
    )


def test_restart_trend_never_throws_on_an_unexpected_shape() -> None:
    """The whole check is thrown away by one bad cast, and the runner's
    try/catch is the only thing that kept that from taking the watchdog with
    it. Skip the app and say so instead."""
    code = _code()
    assert "$rawRestarts -is [array]" in code
    assert "[int]$process.pm2_env.restart_time" not in code, (
        "cast the extracted scalar, not the member-enumeration result"
    )
