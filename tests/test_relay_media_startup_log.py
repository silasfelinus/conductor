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


def test_log_media_roots_reports_the_configured_root(monkeypatch):
    relay_media = load_relay_media_module(monkeypatch)
    monkeypatch.setattr(relay_media, "MEDIA_ROOT_VALUE", "/srv/kindrobots/images")

    logged = []
    monkeypatch.setattr(relay_media.relay, "log", logged.append)
    relay_media.log_media_roots()

    # Exactly one root. The second line this used to emit ("media root
    # 'rewards' not configured") described config that should never have
    # existed -- rewards live in a folder under the images root.
    assert len(logged) == 1
    assert "configured" in logged[0]
    assert "not configured" not in logged[0]
    assert "/srv/kindrobots/images" in logged[0]
    assert "rewards" not in logged[0].lower()


def test_log_media_roots_reports_a_missing_root_with_env_hint(monkeypatch):
    relay_media = load_relay_media_module(monkeypatch)
    monkeypatch.setattr(relay_media, "MEDIA_ROOT_VALUE", "")

    logged = []
    monkeypatch.setattr(relay_media.relay, "log", logged.append)
    relay_media.log_media_roots()

    assert len(logged) == 1
    assert "not configured" in logged[0]
    assert "KR_MEDIA_IMAGES_DIR" in logged[0]


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
