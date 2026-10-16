"""KR Relay VACE pilot integration regression, no actual GPU required."""
import importlib
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest


def setup_modules(monkeypatch):
    root = Path(__file__).resolve().parents[1] / "ops" / "home-server"
    monkeypatch.syspath_prepend(str(root))
    for name in ("vace_relay", "relay_media_agent", "relay_agent", "coat_dance_vace_worker"):
        sys.modules.pop(name, None)
    return importlib.import_module("vace_relay")


def test_relay_preflight_requires_models_and_no_additional_daemon(monkeypatch, tmp_path):
    vace = setup_modules(monkeypatch)
    monkeypatch.setattr(vace, "INPUT_ROOT", tmp_path)
    monkeypatch.setattr(vace.shutil, "which", lambda name: f"/bin/{name}")
    monkeypatch.setattr(vace.vace, "check_comfy", lambda base: True)
    assert vace.capable()
    assert vace._last_ok
    monkeypatch.setattr(vace, "_last_check", 0)
    monkeypatch.setattr(vace.vace, "check_comfy", lambda base: (_ for _ in ()).throw(
        RuntimeError("GPU model missing: wan2.1_vace_1.3B_fp16.safetensors")
    ))
    assert vace.capable() is False
    assert "GPU model missing" in vace._last_reason


def test_unavailable_ffmpeg_never_advertises_vace(monkeypatch, tmp_path):
    vace = setup_modules(monkeypatch)
    monkeypatch.setattr(vace, "INPUT_ROOT", tmp_path)
    monkeypatch.setattr(vace.shutil, "which", lambda name: None)
    assert vace.capable() is False
    assert "ffmpeg" in vace._last_reason


def test_relay_claim_declares_capability_only_from_preflight(monkeypatch):
    vace = setup_modules(monkeypatch)
    captured = []
    def fake_post(method, url, body, **kwargs):
        captured.append(body)
        return 200, {"success": True, "data": {"job": None}}
    monkeypatch.setattr(vace.relay, "http_json", fake_post)
    monkeypatch.setattr(vace.relay, "supports_video_restyle", lambda: False, raising=False)
    vace.relay.claim_job()
    assert captured[-1]["supportsVideoRestyle"] is False
    monkeypatch.setattr(vace.relay, "supports_video_restyle", lambda: True)
    vace.relay.claim_job()
    assert captured[-1]["supportsVideoRestyle"] is True


def test_vace_job_uses_existing_media_agent_dispatch(monkeypatch):
    vace = setup_modules(monkeypatch)
    wrapper = importlib.import_module("relay_media_agent")
    called = []
    monkeypatch.setattr(wrapper.vace_relay, "process", lambda job: called.append(job["id"]))
    monkeypatch.setattr(wrapper, "ORIGINAL_PROCESS", lambda job: pytest.fail("Legacy image path ran"))
    wrapper.process_with_media({"id": 39479, "payload": {"media": "video-restyle-vace"}})
    assert called == [39479]


def test_report_success_and_failure_are_owner_scoped_to_claim(monkeypatch):
    vace = setup_modules(monkeypatch)
    calls = []
    def fake_post(method, url, body, **kwargs):
        calls.append((url, body))
        return 200, {"success": True, "data": {"status": "PILOT_RUNNING"}}
    monkeypatch.setattr(vace.relay, "http_json", fake_post)
    key = "c927a107-ec44-4002-a862-3b7b65d3abe"
    vace._report(key, 39479, "progress", 2)
    assert calls[-1][0].endswith(f"/api/video-restyle/{key}/pilot/report")
    assert calls[-1][1]["artJobId"] == 39479
    assert calls[-1][1]["completedSegments"] == 2
    assert calls[-1][1]["agentId"] == vace.relay.AGENT_ID


def test_vace_renderer_uploads_result_and_does_not_complete_still_image(monkeypatch, tmp_path):
    vace = setup_modules(monkeypatch)
    monkeypatch.setattr(vace, "WORK_ROOT", tmp_path)
    monkeypatch.setattr(vace, "capable", lambda: True)
    monkeypatch.setattr(vace, "_source", lambda rid, aid, dest: dest.write_bytes(b"source"))
    reports = []
    monkeypatch.setattr(vace, "_report", lambda rid, aid, kind, completed, **kw: reports.append((kind, completed)))
    uploaded = []
    monkeypatch.setattr(vace, "_submit_video", lambda rid, aid, count, file: uploaded.append((count, file.read_bytes())))
    def fake_render(job_path, args):
        state = __import__("json").loads(job_path.read_text())
        (job_path.parent / "pilot.mp4").write_bytes(b"\x00\x00\x00\x18ftypmp42animated")
        state["status"] = "REVIEW"
        job_path.write_text(__import__("json").dumps(state))
    monkeypatch.setattr(vace.vace, "render", fake_render)
    job = {"id": 39479, "userId": 1, "payload": {
        "media": "video-restyle-vace",
        "videoRestyle": {
            "id": "c927a107-ec44-4002-a862-3b7b65d3abe",
            "phase": "pilot", "startSec": 158, "durationSec": 24, "totalSegments": 7,
        },
    }}
    vace.process(job)
    assert reports[0] == ("progress", 0)
    assert uploaded[0][0] == 7
    assert b"ftyp" in uploaded[0][1]
