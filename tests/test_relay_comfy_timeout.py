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


def test_queue_state_finds_running_and_pending_prompts(monkeypatch):
    relay_media = load_relay_media_module(monkeypatch)

    queue = {
        "queue_running": [[1, "running-id", {}, {"client_id": "one"}]],
        "queue_pending": [[2, "pending-id", {}, {"client_id": "two"}]],
    }
    monkeypatch.setattr(
        relay_media.relay,
        "http_json",
        lambda *_args, **_kwargs: (200, queue),
    )

    assert relay_media.comfy_prompt_queue_state("running-id") == "running"
    assert relay_media.comfy_prompt_queue_state("pending-id") == "pending"
    assert relay_media.comfy_prompt_queue_state("missing-id") == "absent"


def test_queue_state_is_unknown_when_probe_fails(monkeypatch):
    relay_media = load_relay_media_module(monkeypatch)

    def fail_probe(*_args, **_kwargs):
        raise TimeoutError("queue probe timed out")

    monkeypatch.setattr(relay_media.relay, "http_json", fail_probe)
    assert relay_media.comfy_prompt_queue_state("prompt-123") == "unknown"


def test_payload_timeout_overrides_relay_fallback(monkeypatch):
    relay_media = load_relay_media_module(monkeypatch)
    monkeypatch.setattr(relay_media.relay, "GEN_TIMEOUT", 7200)

    assert relay_media.generation_timeout_seconds({"timeoutSeconds": 5400}) == 5400
    assert relay_media.generation_timeout_seconds({}) == 7200
    assert relay_media.generation_timeout_seconds({"timeoutSeconds": 5}) == 7200
    assert relay_media.generation_timeout_seconds({"timeoutSeconds": True}) == 7200


def test_active_prompt_continues_past_soft_timeout(monkeypatch):
    relay_media = load_relay_media_module(monkeypatch)
    payload = {
        "workflow": {"1": {"class_type": "TestNode", "inputs": {}}},
        "media": "video",
        "timeoutSeconds": 60,
        "_relayClientId": "test-client",
    }
    history_calls = 0
    sentinel = {"data_b64": "done", "file_type": "webp", "is_video": True}

    def fake_http_json(method, url, *args, **kwargs):
        nonlocal history_calls
        if method == "POST" and url.endswith("/prompt"):
            return 200, {"prompt_id": "prompt-123"}
        if method == "GET" and url.endswith("/history/prompt-123"):
            history_calls += 1
            if history_calls == 1:
                return 200, {}
            return 200, {
                "prompt-123": {
                    "outputs": {"save": {"images": []}},
                    "status": {"status_str": "success"},
                }
            }
        if method == "GET" and url.endswith("/queue"):
            return 200, {
                "queue_running": [[1, "prompt-123", {}, {"client_id": "test-client"}]],
                "queue_pending": [],
            }
        raise AssertionError(f"unexpected call: {method} {url}")

    times = iter([0.0, 61.0])
    monkeypatch.setattr(relay_media.time, "time", lambda: next(times))
    monkeypatch.setattr(relay_media.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(relay_media.relay, "http_json", fake_http_json)
    monkeypatch.setattr(relay_media.relay, "upload_comfy_input_images", lambda _payload: None)
    monkeypatch.setattr(relay_media.relay, "align_workflow_asset_names", lambda _workflow: [])
    monkeypatch.setattr(relay_media.relay, "extract_comfy_output", lambda *_a, **_k: sentinel)

    assert relay_media.run_comfy_with_recovery(payload) == sentinel
    assert history_calls == 2
