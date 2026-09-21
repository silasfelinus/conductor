from pathlib import Path


SCRIPT = Path("ops/home-server/check-pm2-service-readiness.ps1")


def source() -> str:
    return SCRIPT.read_text(encoding="utf-8")


def test_service_preflight_is_read_only_and_checks_shared_pm2_home():
    text = source()
    assert "C:\\ProgramData\\pm2\\home" in text
    assert "dump.pm2" in text
    assert "pm2 jlist" in text
    for mutator in ("pm2 start", "pm2 stop", "pm2 restart", "pm2 delete", "pm2 save"):
        assert mutator not in text


def test_service_preflight_rejects_mapped_drive_dependency():
    text = source()
    assert "KR_SHARE_ROOT" in text
    assert "StartsWith('\\\\')" in text
    assert "StartsWith('//')" in text
    assert "ai\\models" in text


def test_service_preflight_pins_watchdog_visible_apps():
    text = source()
    assert "$names -contains 'comfyui'" in text
    assert "$names -contains 'kr-relay'" in text
    assert "Do not switch pm2 to session 0 yet" in text
