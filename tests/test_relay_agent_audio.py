"""Tests for the relay's audio support (music-video/t-011).

kind_robots queues ACE-Step song jobs as COMFY ArtJobs with payload.media
"audio" and only releases them to a relay that advertises supportsAudio
(music-video/t-020). These cover the relay half: advertising the capability,
finding the SaveAudioAdvanced mp3 under history outputs[node]["audio"],
uploading it with its real fileType and isPublic false, keeping the local copy
an .mp3 rather than a re-encoded .webp, and the live relay_media_agent path
asking for audio rather than an image.

An unpatched relay does not fail loudly: it looks for an image, and either
reports "no output" or stores the song as a png. Every assertion here guards
one of those silent outcomes.
"""

import base64
import importlib.util
import sys
from pathlib import Path

import pytest

HOME_SERVER = Path(__file__).resolve().parents[1] / "ops" / "home-server"
RELAY_PATH = HOME_SERVER / "relay_agent.py"

spec = importlib.util.spec_from_file_location("relay_agent_audio_under_test", RELAY_PATH)
relay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(relay)

MP3_BYTES = b"ID3\x04\x00\x00\x00\x00\x00\x00fakesong"
MP3_B64 = base64.b64encode(MP3_BYTES).decode()

# The shape ComfyUI's history reports for SaveAudioAdvanced, beside a preview
# image some graphs also emit.
SONG_OUTPUTS = {
    "9": {"images": [{"filename": "preview_00001.png", "subfolder": "", "type": "temp"}]},
    "10": {
        "audio": [
            {"filename": "musicvideo_00001_.mp3", "subfolder": "audio", "type": "output"}
        ]
    },
}


def test_audio_filenames_are_their_own_kind():
    assert relay.is_audio_filename("musicvideo_00001_.mp3")
    assert relay.is_audio_filename("take.FLAC")
    assert relay.is_audio_filename("take.ogg")
    assert not relay.is_audio_filename("clip.mp4")
    assert not relay.is_audio_filename("")
    assert relay.filename_kind("song.mp3") == "audio"
    assert relay.filename_kind("clip.webm") == "video"
    assert relay.filename_kind("still.png") == "image"


def test_payload_media_kind_defaults_to_image():
    assert relay.payload_media_kind({"media": "audio"}) == "audio"
    assert relay.payload_media_kind({"media": " Video "}) == "video"
    assert relay.payload_media_kind({"media": "hologram"}) == "image"
    assert relay.payload_media_kind({}) == "image"
    assert relay.payload_media_kind(None) == "image"


def test_find_output_file_locates_audio_and_skips_preview_image():
    found = relay.find_output_file(SONG_OUTPUTS, "audio")
    assert found == {
        "filename": "musicvideo_00001_.mp3",
        "subfolder": "audio",
        "type": "output",
    }


def test_image_and_video_searches_never_pick_up_the_song():
    audio_only = {"10": SONG_OUTPUTS["10"]}
    assert relay.find_output_file(audio_only, want_video=False) is None
    assert relay.find_output_file(audio_only, want_video=True) is None
    assert relay.find_output_file(audio_only, "image") is None


def test_extract_comfy_output_audio(monkeypatch):
    monkeypatch.setattr(relay, "download_comfy_file", lambda meta: MP3_BYTES)
    result = relay.extract_comfy_output(SONG_OUTPUTS, "audio", prompt_id="p-1")
    assert result["data_b64"] == MP3_B64
    assert result["file_type"] == "mp3"
    assert result["is_audio"] is True
    assert result["is_video"] is False
    assert result["comfy"]["prompt_id"] == "p-1"
    assert result["comfy"]["output"]["subfolder"] == "audio"


def test_extract_comfy_output_still_accepts_the_historical_bool(monkeypatch):
    monkeypatch.setattr(relay, "download_comfy_file", lambda meta: b"png")
    outputs = {"9": SONG_OUTPUTS["9"]}
    result = relay.extract_comfy_output(outputs, want_video=False)
    assert result["file_type"] == "png"
    assert result["is_audio"] is False
    assert result["is_video"] is False


def test_claim_advertises_audio_support(monkeypatch):
    captured = {}

    def fake_http_json(method, url, body=None, bearer=None, timeout=60):
        captured["url"] = url
        captured["body"] = body
        return 204, None

    monkeypatch.setattr(relay, "http_json", fake_http_json)
    relay.claim_job()
    assert captured["url"].endswith("/api/art/queue/claim")
    assert captured["body"]["supportsAudio"] is True
    assert captured["body"]["supportsInputImages"] is True


def test_upload_result_sends_audio_private_with_its_file_type(monkeypatch):
    captured = {}

    def fake_http_json(method, url, body=None, bearer=None, timeout=60):
        captured["body"] = body
        return 201, {"success": True, "data": {"id": 777}}

    monkeypatch.setattr(relay, "http_json", fake_http_json)
    job = {"id": 9, "payload": {"promptString": "synth rock, male lead vocals", "media": "audio"}}
    media = {"data_b64": MP3_B64, "file_type": "mp3", "is_video": False, "is_audio": True}

    assert relay.upload_result(job, media) == 777
    assert captured["body"]["fileType"] == "mp3"
    assert captured["body"]["isPublic"] is False
    assert captured["body"]["promptString"] == "synth rock, male lead vocals"


def capture_image_upload(monkeypatch, payload):
    captured = {}

    def fake_http_json(method, url, body=None, bearer=None, timeout=60):
        captured["body"] = body
        return 201, {"success": True, "data": {"id": 778}}

    monkeypatch.setattr(relay, "http_json", fake_http_json)
    media = {"data_b64": MP3_B64, "file_type": "png", "is_video": False}
    relay.upload_result({"id": 10, "payload": payload}, media)
    return captured["body"]


def test_upload_result_stages_image_with_the_jobs_visibility(monkeypatch):
    body = capture_image_upload(
        monkeypatch,
        {"promptString": "a robot", "save": {"isMature": True, "isPublic": False}},
    )
    assert body["isMature"] is True
    assert body["isPublic"] is False

    body = capture_image_upload(
        monkeypatch,
        {"promptString": "a robot", "save": {"isMature": False, "isPublic": True}},
    )
    assert body["isMature"] is False
    assert body["isPublic"] is True


def test_upload_result_stages_image_private_without_a_save_block(monkeypatch):
    body = capture_image_upload(monkeypatch, {"promptString": "a robot"})
    assert body["isPublic"] is False
    assert body["isMature"] is False


def test_local_copy_keeps_audio_bytes_as_mp3(monkeypatch, tmp_path):
    monkeypatch.setattr(relay, "KR_LOCAL_IMAGES_DIR", str(tmp_path))

    def never_reencode(raw):
        raise AssertionError("audio must not go through the webp encoder")

    monkeypatch.setattr(relay, "encode_webp", never_reencode)
    media = {"data_b64": MP3_B64, "file_type": "mp3", "is_audio": True}
    relay.write_local_copy({"id": 11, "payload": {}}, 501, media)
    written = tmp_path / "sdxl" / "sdxl-501.mp3"
    assert written.read_bytes() == MP3_BYTES


def test_media_kind_label():
    assert relay.media_kind_label({"is_audio": True}) == "audio"
    assert relay.media_kind_label({"is_video": True}) == "video"
    assert relay.media_kind_label({}) == "image"


def load_relay_media_module(monkeypatch):
    monkeypatch.syspath_prepend(str(HOME_SERVER))
    sys.modules.pop("relay_media_agent", None)
    sys.modules.pop("relay_agent", None)
    media_spec = importlib.util.spec_from_file_location(
        "relay_media_agent", HOME_SERVER / "relay_media_agent.py"
    )
    module = importlib.util.module_from_spec(media_spec)
    assert media_spec.loader is not None
    media_spec.loader.exec_module(module)
    return module


def test_live_relay_asks_comfy_history_for_audio(monkeypatch):
    """relay_media_agent replaces relay.run_comfy and recomputes the wanted
    kind itself; it must ask for audio, not fall back to image."""
    relay_media = load_relay_media_module(monkeypatch)
    payload = {
        "workflow": {"1": {"class_type": "TestNode", "inputs": {}}},
        "media": "audio",
        "timeoutSeconds": 600,
        "_relayClientId": "test-client",
    }
    asked = []
    sentinel = {"data_b64": MP3_B64, "file_type": "mp3", "is_audio": True}

    def fake_http_json(method, url, *args, **kwargs):
        if method == "POST" and url.endswith("/prompt"):
            return 200, {"prompt_id": "prompt-a"}
        if method == "GET" and url.endswith("/history/prompt-a"):
            return 200, {"prompt-a": {"outputs": SONG_OUTPUTS, "status": {}}}
        raise AssertionError(f"unexpected call: {method} {url}")

    def fake_extract(outputs, want, prompt_id=None):
        asked.append(want)
        return sentinel

    monkeypatch.setattr(relay_media.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(relay_media.relay, "http_json", fake_http_json)
    monkeypatch.setattr(relay_media.relay, "upload_comfy_input_images", lambda _p: None)
    monkeypatch.setattr(relay_media.relay, "align_workflow_asset_names", lambda _w: [])
    monkeypatch.setattr(relay_media.relay, "extract_comfy_output", fake_extract)

    assert relay_media.run_comfy_with_recovery(payload) == sentinel
    assert asked == ["audio"]


def test_direct_media_refuses_audio(monkeypatch, tmp_path):
    relay_media = load_relay_media_module(monkeypatch)
    monkeypatch.setattr(relay_media, "MEDIA_ROOT_VALUE", str(tmp_path))
    job = {
        "id": 12,
        "payload": {
            "targetRepo": relay_media.KIND_ROBOTS_REPO,
            "imagePath": "public/images/songs/theme.mp3",
        },
    }
    media = {"data_b64": MP3_B64, "file_type": "mp3", "is_audio": True}
    with pytest.raises(ValueError, match="never written"):
        relay_media.write_direct_media(job, media)
    assert not (tmp_path / "songs" / "theme.mp3").exists()
