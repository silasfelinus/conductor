"""Offline tests for byte-level Shifting Desks manual art verification."""
import hashlib
import io
from PIL import Image
from scripts.verify_shifting_desks_manual_intake import verify_image, verify_manifest


def fixture():
    data = io.BytesIO()
    Image.new("RGB", (24, 36), (40, 90, 120)).save(data, "WEBP")
    blob = data.getvalue()
    row = {"path": "mutations/example.webp", "sha256": hashlib.sha256(blob).hexdigest(),
           "width": 24, "height": 36}
    return row, blob


class FakeResponse:
    status = 200
    headers = {"Content-Type": "image/webp", "Last-Modified": "Tue, 17 Nov 2026 22:30:00 GMT"}

    def __init__(self, blob):
        self.blob = blob

    def read(self, limit=None):
        return self.blob

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return None


def test_matching_image_reports_real_sha_and_dimensions():
    row, blob = fixture()
    def opener(req, timeout):
        assert req.full_url.endswith("/images/shifting-desks/mutations/example.webp")
        assert timeout == 2
        return FakeResponse(blob)
    result = verify_image(row, "https://kindrobots.org", timeout=2, opener=opener)
    assert result["state"] == "match"
    assert result["dimensions"] == [24, 36]


def test_stale_served_image_is_never_accepted():
    row, blob = fixture()
    row["sha256"] = "a" * 64
    result = verify_image(row, "https://kindrobots.org", opener=lambda *_args, **_kwargs: FakeResponse(blob))
    assert result["state"] == "unverified"
    assert "differ" in result["reason"]


def test_unreadable_file_fails_closed():
    row, _ = fixture()
    result = verify_image(row, "https://kindrobots.org", opener=lambda *_args, **_kwargs: FakeResponse(b"error page"))
    assert result["state"] == "unverified"


def test_fourteen_unique_expected_and_no_art_approval():
    row, blob = fixture()
    rows = [{**row, "path": f"mutations/example-{i}.webp"} for i in range(14)]
    result = verify_manifest({"images": rows}, "https://kindrobots.org",
        opener=lambda *_args, **_kwargs: FakeResponse(blob))
    assert result["ready"]
    assert result["matched"] == 14
    assert "not editorial art acceptance" in result["meaning"]
