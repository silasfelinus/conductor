import importlib.util
import sys
from pathlib import Path


def load_relay_media_module(monkeypatch):
    home_server = Path(__file__).parents[1] / "ops" / "home-server"
    monkeypatch.syspath_prepend(str(home_server))
    sys.modules.pop("relay_media_agent", None)
    sys.modules.pop("relay_agent", None)
    spec = importlib.util.spec_from_file_location(
        "relay_media_agent", home_server / "relay_media_agent.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_log_media_roots_reports_each_configured_root(monkeypatch):
    relay_media = load_relay_media_module(monkeypatch)
    monkeypatch.setattr(relay_media, "MEDIA_ROOT_VALUE", "/srv/kindrobots/images")
    monkeypatch.setattr(relay_media, "REWARDS_ROOT_VALUE", "/srv/kindrobots/rewards")

    logged = []
    monkeypatch.setattr(relay_media.relay, "log", logged.append)

    relay_media.log_media_roots()

    assert len(logged) == 2
    images_line, rewards_line = logged
    assert "images" in images_line
    assert "configured" in images_line
    assert "not configured" not in images_line
    assert "/srv/kindrobots/images" in images_line
    assert "rewards" in rewards_line
    assert "configured" in rewards_line
    assert "not configured" not in rewards_line
    assert "/srv/kindrobots/rewards" in rewards_line


def test_log_media_roots_reports_each_missing_root_with_env_hint(monkeypatch):
    relay_media = load_relay_media_module(monkeypatch)
    monkeypatch.setattr(relay_media, "MEDIA_ROOT_VALUE", "")
    monkeypatch.setattr(relay_media, "REWARDS_ROOT_VALUE", "")

    logged = []
    monkeypatch.setattr(relay_media.relay, "log", logged.append)

    relay_media.log_media_roots()

    assert len(logged) == 2
    images_line, rewards_line = logged
    assert "images" in images_line
    assert "not configured" in images_line
    assert "KR_MEDIA_IMAGES_DIR" in images_line
    assert "rewards" in rewards_line
    assert "not configured" in rewards_line
    assert "KR_MEDIA_REWARDS_DIR" in rewards_line


def test_log_media_roots_handles_mixed_configuration(monkeypatch):
    relay_media = load_relay_media_module(monkeypatch)
    monkeypatch.setattr(relay_media, "MEDIA_ROOT_VALUE", "/srv/kindrobots/images")
    monkeypatch.setattr(relay_media, "REWARDS_ROOT_VALUE", "")

    logged = []
    monkeypatch.setattr(relay_media.relay, "log", logged.append)

    relay_media.log_media_roots()

    assert len(logged) == 2
    images_line, rewards_line = logged
    assert "not configured" not in images_line
    assert "not configured" in rewards_line


def test_main_entrypoint_logs_media_roots_before_starting_lora_watcher(monkeypatch):
    """``__main__`` must call ``log_media_roots()`` before
    ``start_lora_watcher()`` so a misconfigured box is visible in the logs
    immediately at process startup, alongside the existing lora-watcher
    enabled/disabled log line."""
    home_server = Path(__file__).parents[1] / "ops" / "home-server"
    source = (home_server / "relay_media_agent.py").read_text(encoding="utf-8")

    main_block = source.split('if __name__ == "__main__":', 1)[1]
    log_roots_index = main_block.index("log_media_roots()")
    start_watcher_index = main_block.index("start_lora_watcher()")
    assert log_roots_index < start_watcher_index
