"""Contract and failure-mode tests for private Tactics gameplay media delivery."""

from __future__ import annotations

import io
import urllib.error
import urllib.request

import pytest
from PIL import Image

from scripts.verify_tactics_runtime_media import (
    SameOriginRedirect,
    average_thumbnail_delta,
    check_visibility,
    read_game_image,
    retry_transient,
    runtime_url,
    verify,
)


def sample_png():
    buffer = io.BytesIO()
    Image.new("RGB", (256, 256), (42, 95, 153)).save(buffer, "PNG")
    return buffer.getvalue()


class FakeResponse(io.BytesIO):
    def __init__(self, data=b"", content_type="image/png"):
        super().__init__(data)
        self.headers = {"content-type": content_type}


class FakeOpener:
    def __init__(self, data=b"", anonymous_code=None, content_type="image/png"):
        self.data = data
        self.anonymous_code = anonymous_code
        self.content_type = content_type
        self.calls = []

    def open(self, request, timeout):
        self.calls.append((request.full_url, request.get_header("Authorization")))
        if not request.get_header("Authorization") and self.anonymous_code:
            raise urllib.error.HTTPError(
                request.full_url, self.anonymous_code, "Forbidden", {}, None
            )
        return FakeResponse(self.data, self.content_type)


def test_game_path_reads_real_image_with_bearer_and_nothing_public():
    fake = FakeOpener(sample_png())
    image = read_game_image(277786, "https://kindrobots.org", "test-only", fake)
    assert image.size == (256, 256)
    assert fake.calls == [
        ("https://kindrobots.org/api/art/images/277786/file", "Bearer test-only")
    ]


def test_wrong_content_type_is_not_reported_as_delivery():
    fake = FakeOpener(b'{"statusCode":401}', content_type="application/json")
    with pytest.raises(ValueError, match="did not return image"):
        read_game_image(277786, "https://kindrobots.org", "test-only", fake)


def test_private_art_is_denied_to_anonymous_but_public_art_loads():
    private = FakeOpener(anonymous_code=403)
    assert (
        check_visibility(277786, "https://kindrobots.org", False, private)
        == "PRIVATE_DENIED"
    )
    assert private.calls[0][1] is None
    public = FakeOpener(sample_png())
    assert (
        check_visibility(277786, "https://kindrobots.org", True, public)
        == "PUBLIC_OK"
    )
    with pytest.raises(PermissionError, match="Private art visible"):
        check_visibility(277786, "https://kindrobots.org", False, public)


def test_cross_origin_and_http_redirects_cannot_leak_api_token():
    req = urllib.request.Request(
        "https://kindrobots.org/api/art/images/277786/file",
        headers={"Authorization": "Bearer should-not-leak"},
    )
    handler = SameOriginRedirect()
    for target in [
        "https://example.net/secret.png",
        "http://kindrobots.org/file.png",
    ]:
        with pytest.raises(ValueError, match="Cross-origin"):
            handler.redirect_request(req, None, 302, "Moved", {}, target)


def test_runtime_origin_must_be_https_without_userinfo():
    for origin in ["http://kindrobots.org", "https://x:y@kindrobots.org", ""]:
        with pytest.raises(ValueError, match="trusted HTTPS"):
            runtime_url(origin, 277786)


def test_pixel_compare_allows_transcode_but_rejects_wrong_image():
    source = Image.new("RGB", (256, 256), (42, 95, 153))
    assert average_thumbnail_delta(source, source.copy()) == 0
    corrupt = Image.new("RGB", (256, 256), (220, 3, 6))
    assert average_thumbnail_delta(source, corrupt) > 18
    with pytest.raises(ValueError, match="dimensions differ"):
        average_thumbnail_delta(source, Image.new("RGB", (128, 256)))


def test_reconciles_job_and_image_and_sanitizes_failures():
    entries = [
        {"key": "burrow-warning", "job_id": 74393, "image_id": 277786},
        {"key": "phase-warning", "job_id": 74397, "image_id": 277790},
    ]

    def load_runtime(image_id):
        if image_id == 277790:
            raise RuntimeError("Bearer secret-token https://private.example/media")
        return Image.new("RGB", (256, 256))

    good, failed = verify(
        entries,
        read_reference=lambda _image_id: Image.new("RGB", (256, 256)),
        read_runtime=load_runtime,
        visibility=lambda _image_id, _public: "PRIVATE_DENIED",
        fetch_public=lambda _image_id: False,
    )
    assert good == [
        ("burrow-warning", 74393, 277786, (256, 256), "PRIVATE_DENIED")
    ]
    assert failed == [("phase-warning", 277790, "RuntimeError")]
    assert not any("secret-token" in str(f) for f in failed)


def test_metadata_visibility_must_be_boolean():
    entries = [{"key": "k", "job_id": 1, "image_id": 2}]
    ok, failed = verify(
        entries,
        lambda _: Image.new("RGB", (256, 256)),
        lambda _: Image.new("RGB", (256, 256)),
        lambda *_: "PRIVATE_DENIED",
        lambda _: None,
    )
    assert ok == []
    assert failed == [("k", 2, "ValueError")]

def test_transient_429_and_source_metadata_503_recover_without_new_artjobs():
    attempts = []
    pauses = []

    def fetch():
        attempts.append(len(attempts))
        if len(attempts) == 1:
            raise RuntimeError("ArtImage 258175: HTTP 503, no imagePath")
        if len(attempts) == 2:
            raise urllib.error.HTTPError(
                "https://kindrobots.org/api/art/images/258175/file",
                429,
                "Too Many Requests",
                {},
                None,
            )
        return "verified"

    assert retry_transient(fetch, pause=pauses.append) == "verified"
    assert len(attempts) == 3
    assert pauses == [2, 4]


def test_persistent_404_and_bad_image_are_not_retried():
    for error in [
        urllib.error.HTTPError("https://kindrobots.org/file", 404, "Missing", {}, None),
        ValueError("Gameplay image differs from its source"),
        RuntimeError("ArtImage 258175: HTTP 404, no imagePath"),
    ]:
        calls = []
        with pytest.raises(type(error)):
            retry_transient(
                lambda: (calls.append(1), (_ for _ in ()).throw(error))[1],
                pause=lambda _: (_ for _ in ()).throw(AssertionError("slept")),
            )
        assert calls == [1]


def test_verifier_recovers_transient_reference_and_game_url_failures():
    calls = {"source": 0, "runtime": 0, "policy": 0}

    def retry_now(action):
        return retry_transient(action, pause=lambda _: None)

    def source(_):
        calls["source"] += 1
        if calls["source"] == 1:
            raise RuntimeError("ArtImage 258175: HTTP 429, no imagePath")
        return Image.new("RGB", (256, 256))

    def runtime(_):
        calls["runtime"] += 1
        if calls["runtime"] == 1:
            raise urllib.error.HTTPError(
                "https://kindrobots.org/file", 503, "Unavailable", {}, None
            )
        return Image.new("RGB", (256, 256))

    def visibility(_, public):
        calls["policy"] += 1
        assert public is False
        if calls["policy"] == 1:
            raise urllib.error.HTTPError(
                "https://kindrobots.org/file", 429, "Throttled", {}, None
            )
        return "PRIVATE_DENIED"

    good, failed = verify(
        [{"key": "magic-discipline-hero", "job_id": 50768, "image_id": 258175}],
        source,
        runtime,
        visibility,
        lambda _: False,
        retry=retry_now,
    )
    assert failed == []
    assert len(good) == 1
    assert calls == {"source": 2, "runtime": 2, "policy": 2}
