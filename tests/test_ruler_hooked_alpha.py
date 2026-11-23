"""WebP alpha/header and image-ledger boundaries for ruler-hooked/t-070."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.audit_ruler_hooked_alpha import (
    audit,
    delivered_region_requests,
    inspect,
    webp_alpha,
)


def header(chunk: bytes, payload: bytes) -> bytes:
    return (
        b"RIFF"
        + (12 + len(payload)).to_bytes(4, "little")
        + b"WEBP"
        + chunk
        + len(payload).to_bytes(4, "little")
        + payload
    )


class WebpAlphaTests(unittest.TestCase):
    def test_extended_alpha_bit_is_required(self):
        self.assertEqual(webp_alpha(header(b"VP8X", b"\x10" + b"\0" * 9)), "alpha")
        self.assertEqual(webp_alpha(header(b"VP8X", b"\x00" + b"\0" * 9)), "opaque")

    def test_lossless_alpha_bit_is_required(self):
        alpha = b"\x2f" + (1 << 28).to_bytes(4, "little")
        plain = b"\x2f" + (0).to_bytes(4, "little")
        self.assertEqual(webp_alpha(header(b"VP8L", alpha)), "alpha")
        self.assertEqual(webp_alpha(header(b"VP8L", plain)), "opaque")

    def test_lossy_and_bad_webp(self):
        self.assertEqual(webp_alpha(header(b"VP8 ", b"\x00" * 10)), "opaque")
        self.assertEqual(webp_alpha(b"NOT A WEBP"), "invalid")
        self.assertEqual(webp_alpha(header(b"VP8L", b"\x00" * 5)), "invalid")

    def test_only_delivered_ruler_layers_are_scanned(self):
        manifest = """
requests:
- id: ruler-hooked-layer-sky-open-day
  project_slug: ruler-hooked
  lane: layer
  status: done
  source_url: https://media.acrocatranch.com/images/ruler-hooked/sky-open-day.webp
- id: ruler-hooked-layer-lake-clear
  project_slug: ruler-hooked
  lane: layer
  status: pending
- id: ruler-hooked-expression-quill
  project_slug: ruler-hooked
  lane: expression
  status: done
- id: cthulhu-layer
  project_slug: cthulhuquarium
  lane: layer
  status: done
"""
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "art.yaml"
            path.write_text(manifest, encoding="utf-8")
            rows = delivered_region_requests(path)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["id"], "ruler-hooked-layer-sky-open-day")
            report = audit(path, remote=False)
            self.assertEqual(report["total"], 1)
            self.assertEqual(report["counts"]["unavailable"], 1)

    def test_reject_untrusted_host_before_network(self):
        row = {
            "id": "unsafe",
            "source_url": "https://example.org/images/ruler-hooked/a.webp",
        }
        self.assertEqual(inspect(row, remote=True)["result"], "invalid-url")


if __name__ == "__main__":
    unittest.main()
