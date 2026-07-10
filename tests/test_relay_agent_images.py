"""Tests for relay_agent.py's COMFY input-image support (Hair Studio /
kontext enqueue jobs): entry validation, data-URL handling, and the
multipart body posted to ComfyUI's /upload/image."""

import base64
import importlib.util
from pathlib import Path

import pytest

RELAY_PATH = Path(__file__).resolve().parents[1] / "ops" / "home-server" / "relay_agent.py"

spec = importlib.util.spec_from_file_location("relay_agent", RELAY_PATH)
relay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(relay)

PNG_BYTES = b"\x89PNG\r\n\x1a\nfakepixels"
PNG_B64 = base64.b64encode(PNG_BYTES).decode()


def test_decode_image_entry_accepts_raw_base64():
    name, raw = relay.decode_image_entry({"name": "photo.png", "imageData": PNG_B64})
    assert name == "photo.png"
    assert raw == PNG_BYTES


def test_decode_image_entry_strips_data_url_prefix():
    entry = {"name": "photo.jpg", "imageData": f"data:image/jpeg;base64,{PNG_B64}"}
    _, raw = relay.decode_image_entry(entry)
    assert raw == PNG_BYTES


@pytest.mark.parametrize(
    "entry",
    [
        {},
        None,
        {"name": "photo.png"},
        {"imageData": PNG_B64},
        {"name": "", "imageData": PNG_B64},
        {"name": "photo.png", "imageData": ""},
    ],
)
def test_decode_image_entry_rejects_incomplete_entries(entry):
    with pytest.raises(ValueError):
        relay.decode_image_entry(entry)


def test_build_image_upload_request_shapes_comfy_multipart():
    body, content_type = relay.build_image_upload_request(
        "photo.png", PNG_BYTES, "testboundary"
    )

    assert content_type == "multipart/form-data; boundary=testboundary"
    assert body.startswith(b"--testboundary\r\n")
    assert body.endswith(b"--testboundary--\r\n")
    assert b'name="image"; filename="photo.png"' in body
    assert b"Content-Type: image/png" in body
    assert PNG_BYTES in body
    # ComfyUI needs the file routed to its input folder, replacing stale copies.
    assert b'name="type"\r\n\r\ninput\r\n' in body
    assert b'name="overwrite"\r\n\r\ntrue\r\n' in body


def test_build_image_upload_request_maps_jpg_mime():
    body, _ = relay.build_image_upload_request("photo.jpg", PNG_BYTES, "b")
    assert b"Content-Type: image/jpeg" in body


def test_upload_comfy_input_images_rejects_non_list():
    with pytest.raises(ValueError):
        relay.upload_comfy_input_images({"images": {"name": "x"}})


def test_upload_comfy_input_images_noop_without_images():
    # No images key at all — legacy text-to-image jobs must pass untouched.
    relay.upload_comfy_input_images({"workflow": {"1": {}}})


def test_upload_comfy_input_images_posts_each_image(monkeypatch):
    posted = []

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return b'{"name": "photo.png"}'

    def fake_urlopen(req, timeout=0):
        posted.append(req)
        return FakeResponse()

    monkeypatch.setattr(relay.urllib.request, "urlopen", fake_urlopen)

    relay.upload_comfy_input_images(
        {"images": [{"name": "photo.png", "imageData": PNG_B64}]}
    )

    assert len(posted) == 1
    request = posted[0]
    assert request.full_url.endswith("/upload/image")
    assert request.get_method() == "POST"
    assert PNG_BYTES in request.data


def test_upload_comfy_input_images_raises_on_bad_upload(monkeypatch):
    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return b"{}"

    monkeypatch.setattr(
        relay.urllib.request, "urlopen", lambda req, timeout=0: FakeResponse()
    )

    with pytest.raises(RuntimeError):
        relay.upload_comfy_input_images(
            {"images": [{"name": "photo.png", "imageData": PNG_B64}]}
        )


def test_claim_job_declares_input_image_support(monkeypatch):
    captured = {}

    def fake_http_json(method, url, body=None, bearer=None, timeout=60):
        captured["method"] = method
        captured["url"] = url
        captured["body"] = body
        return 200, {"success": True, "data": {"job": None}}

    monkeypatch.setattr(relay, "http_json", fake_http_json)

    assert relay.claim_job() is None
    assert captured["method"] == "POST"
    assert captured["url"].endswith("/api/art/queue/claim")
    # The capability handshake keeps stale agents from claiming image jobs.
    assert captured["body"]["supportsInputImages"] is True
