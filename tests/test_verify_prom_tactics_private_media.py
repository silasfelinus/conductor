import io
import sys
import urllib.request
from pathlib import Path

import pytest
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import verify_prom_tactics_private_media as proof


def painted_bytes(size=(768, 768)):
    image = Image.new("RGB", size, "navy")
    draw = ImageDraw.Draw(image)
    draw.rectangle((10, 10, size[0] // 2, size[1] // 2), fill="orange")
    dest = io.BytesIO()
    image.save(dest, "PNG")
    return dest.getvalue()


def ledger(tmp_path, status="DONE", image_id=277786, job_id=74393):
    file = tmp_path / "private.yaml"
    file.write_text(
        "is_public: false\n"
        "subjects:\n"
        "- key: evt-warning\n"
        "  asset: every-villain-tactics/henchmen/tells/warning\n"
        "  lane: krea2\n"
        "  size: 768x768\n"
        f"  jobs: {{krea2: {job_id}}}\n"
        f"  art: {{krea2: {{status: {status}, art_image_id: {image_id}}}}}\n"
    )
    return file


def test_done_receipt_is_not_byte_verification(tmp_path):
    rows = proof.ledger_rows([str(ledger(tmp_path))])
    assert rows[0]["stage"] == "done-receipt"
    assert rows[0]["job_id"] == 74393
    assert rows[0]["image_id"] == 277786
    assert proof.probe(rows, "https://kindrobots.org", "test", lambda *_: painted_bytes()) == 1
    assert rows[0]["stage"] == "media-verified"
    assert rows[0]["evidence"]["width"] == 768


def test_status_lookup_error_preserves_accepted_job_without_claiming_render(tmp_path):
    rows = proof.ledger_rows([str(ledger(tmp_path, "HTTP502", "null"))])
    assert rows[0]["stage"] == "accepted"
    assert rows[0]["job_id"] == 74393
    assert rows[0]["image_id"] is None
    assert proof.probe(rows, "https://kindrobots.org", "test", lambda *_: b"") == 0


def test_unsubmitted_is_not_accepted(tmp_path):
    rows = proof.ledger_rows([str(ledger(tmp_path, "REQUESTED", "null", "null"))])
    assert rows[0]["stage"] == "requested"


def test_image_validation_rejects_corrupt_blank_and_wrong_aspect():
    for payload, geometry in [
        (b"html-not-an-image" * 25, "768x768"),
        (io.BytesIO(), "768x768"),
        (painted_bytes((768, 768)), "1344x768"),
    ]:
        data = payload.getvalue() if hasattr(payload, "getvalue") else payload
        with pytest.raises((OSError, ValueError)):
            proof.inspect_image(data, geometry)
    blank = io.BytesIO()
    Image.new("RGB", (768, 768), "white").save(blank, "PNG")
    with pytest.raises(ValueError, match="monochrome"):
        proof.inspect_image(blank.getvalue(), "768x768")


def test_private_media_redirect_cannot_leak_jwt():
    guard = proof.SameOriginRedirect("https://kindrobots.org")
    request = urllib.request.Request(
        "https://kindrobots.org/api/art/images/277786/file",
        headers={"Authorization": "Bearer not-a-real-token"},
    )
    for destination in [
        "http://kindrobots.org/storage/277786.webp",
        "https://other.invalid/storage/277786.webp",
    ]:
        with pytest.raises(ValueError, match="redirect"):
            guard.redirect_request(request, None, 302, "found", {}, destination)


def test_duplicate_bytes_do_not_count_as_two_distinct_paintings(tmp_path):
    source = ledger(tmp_path)
    rows = proof.ledger_rows([str(source)])
    second = dict(rows[0], key="other-art-slot", image_id=277787)
    rows.append(second)
    assert proof.probe(rows, "https://kindrobots.org", "test", lambda *_: painted_bytes()) == 1
    assert rows[1]["stage"] == "media-unavailable"
    assert rows[1]["error"] == "ValueError"


def test_private_art_only_and_unique_keys(tmp_path):
    source = ledger(tmp_path)
    source.write_text(source.read_text().replace("is_public: false", "is_public: true"))
    with pytest.raises(ValueError, match="private proof"):
        proof.ledger_rows([str(source)])
