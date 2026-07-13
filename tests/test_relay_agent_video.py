"""Tests for relay_agent.py's COMFY video support (image-to-video LTX/WAN
jobs from kind_robots' /api/art/enqueue): locating the SaveVideo clip in
Comfy history, extracting it with the right fileType, and passing that
fileType through to /api/art/save-generated so the ArtImage plays back as a
clip instead of a still."""

import base64
import importlib.util
from pathlib import Path

RELAY_PATH = Path(__file__).resolve().parents[1] / "ops" / "home-server" / "relay_agent.py"

spec = importlib.util.spec_from_file_location("relay_agent", RELAY_PATH)
relay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(relay)

MP4_BYTES = b"\x00\x00\x00\x18ftypmp42fakeclip"
MP4_B64 = base64.b64encode(MP4_BYTES).decode()


def test_is_video_filename_matches_clip_extensions():
    assert relay.is_video_filename("kindrobots_ltx_image2video_00001.mp4")
    assert relay.is_video_filename("clip.webm")
    assert relay.is_video_filename("clip.MOV")
    assert not relay.is_video_filename("still.png")
    assert not relay.is_video_filename("")


def test_file_extension_is_lowercase_and_dotless():
    assert relay.file_extension("a/b/clip.MP4") == "mp4"
    assert relay.file_extension("still.PNG") == "png"
    assert relay.file_extension("noext") == ""


def test_find_output_file_locates_video_ignoring_stills():
    # SaveVideo output can nest the clip under a build-specific key; the scan
    # is structural, so a stray still in another node must not shadow it.
    outputs = {
        "319": {"images": [{"filename": "preview.png", "subfolder": "", "type": "temp"}]},
        "341": {
            "images": [
                {"filename": "video/clip_00001.mp4", "subfolder": "video", "type": "output"}
            ]
        },
    }
    found = relay.find_output_file(outputs, want_video=True)
    assert found == {
        "filename": "video/clip_00001.mp4",
        "subfolder": "video",
        "type": "output",
    }


def test_find_output_file_wants_image_skips_video():
    outputs = {"341": {"gifs": [{"filename": "clip.webm", "type": "output"}]}}
    assert relay.find_output_file(outputs, want_video=False) is None


def test_find_output_file_returns_none_when_absent():
    assert relay.find_output_file({}, want_video=True) is None
    assert relay.find_output_file({"1": {"images": []}}, want_video=True) is None


def test_extract_comfy_output_video(monkeypatch):
    monkeypatch.setattr(relay, "download_comfy_file", lambda meta: MP4_B64)
    outputs = {"341": {"images": [{"filename": "clip.mp4", "type": "output"}]}}

    result = relay.extract_comfy_output(outputs, want_video=True)

    assert result == {"data_b64": MP4_B64, "file_type": "mp4", "is_video": True}


def test_extract_comfy_output_video_falls_back_to_mp4(monkeypatch):
    # A SaveVideo output missing an extension should still be treated as mp4.
    monkeypatch.setattr(relay, "download_comfy_file", lambda meta: MP4_B64)
    outputs = {"341": {"images": [{"filename": "clip.webm", "type": "output"}]}}

    result = relay.extract_comfy_output(outputs, want_video=True)
    assert result["file_type"] == "webm"
    assert result["is_video"] is True


def test_extract_comfy_output_image(monkeypatch):
    monkeypatch.setattr(relay, "download_comfy_file", lambda meta: "cGl4ZWxz")
    outputs = {"9": {"images": [{"filename": "art.png", "type": "output"}]}}

    result = relay.extract_comfy_output(outputs, want_video=False)
    assert result == {"data_b64": "cGl4ZWxz", "file_type": "png", "is_video": False}


def test_extract_comfy_output_not_ready_returns_none(monkeypatch):
    monkeypatch.setattr(relay, "download_comfy_file", lambda meta: MP4_B64)
    assert relay.extract_comfy_output({}, want_video=True) is None


def test_upload_result_forwards_video_file_type(monkeypatch):
    captured = {}

    def fake_http_json(method, url, body=None, bearer=None, timeout=60):
        captured["url"] = url
        captured["body"] = body
        return 201, {"success": True, "data": {"id": 4242}}

    monkeypatch.setattr(relay, "http_json", fake_http_json)

    job = {"id": 7, "payload": {"promptString": "wink and grin", "media": "video"}}
    media = {"data_b64": MP4_B64, "file_type": "mp4", "is_video": True}

    art_image_id = relay.upload_result(job, media)

    assert art_image_id == 4242
    assert captured["url"].endswith("/api/art/save-generated")
    assert captured["body"]["fileType"] == "mp4"
    assert captured["body"]["imageBase64"] == MP4_B64
    assert captured["body"]["promptString"] == "wink and grin"
