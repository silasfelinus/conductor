"""Shifting Desks art queue retirement keeps evidence without inventing delivery."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_workspace
from shifting_desks_round_evidence import preserve_completed_submissions


REQUEST_ID = "shifting-desks-r13-sample"
DEST = "public/images/shifting-desks/cards/sample.webp"
LEDGER = """# Preserve the art-direction comment and original prompt.
round: shifting-desks-13
subjects:
- key: sample
  request_id: shifting-desks-r13-sample
  target_path: kind_robots public/images/shifting-desks/cards/sample.webp
  prompt: 'A cheerful beige abyss'
  seed: 63001
  status: requested
  art_job_id: null
  art_image_id: null
  verdict: null
"""


def request(status="done", job_id=42163, dest=DEST, request_id=REQUEST_ID):
    return {
        "id": request_id,
        "target_repo": "silasfelinus/kind_robots",
        "image_path": dest,
        "status": status,
        "last_art_job_id": job_id,
    }


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / "ROUND-13.yaml"
        self.path.write_text(LEDGER, encoding="utf-8")

    def parsed(self):
        return yaml.safe_load(self.path.read_text(encoding="utf-8"))["subjects"][0]

    def test_completed_submission_records_job_without_fake_delivery_or_verdict(self):
        blocked = preserve_completed_submissions([request()], art_dir=self.root)
        self.assertEqual(blocked, {REQUEST_ID})
        row = self.parsed()
        self.assertEqual(row["art_job_id"], 42163)
        self.assertEqual(row["status"], "requested")
        self.assertIsNone(row["art_image_id"])
        self.assertIsNone(row["verdict"])
        self.assertIn("# Preserve the art-direction comment", self.path.read_text())
        self.assertIn("A cheerful beige abyss", self.path.read_text())
        self.assertIn("seed: 63001", self.path.read_text())

    def test_pending_request_is_untouched(self):
        blocked = preserve_completed_submissions([request(status="pending")], art_dir=self.root)
        self.assertEqual(blocked, set())
        self.assertEqual(self.path.read_text(), LEDGER)

    def test_missing_id_or_wrong_destination_never_retires(self):
        for entry in (
            request(job_id=None),
            request(dest="public/images/shifting-desks/cards/other.webp"),
            request(request_id="shifting-desks-r13-unknown"),
        ):
            with self.subTest(entry=entry):
                self.assertEqual(preserve_completed_submissions([entry], art_dir=self.root), {entry["id"]})
                self.assertEqual(self.path.read_text(), LEDGER)

    def test_idempotent_and_conflicting_submission_not_overwritten(self):
        self.assertEqual(preserve_completed_submissions([request()], art_dir=self.root), {REQUEST_ID})
        original = self.path.read_text()
        self.assertEqual(preserve_completed_submissions([request()], art_dir=self.root), {REQUEST_ID})
        self.assertEqual(self.path.read_text(), original)
        self.assertEqual(preserve_completed_submissions([request(job_id=99999)], art_dir=self.root), {REQUEST_ID})
        self.assertEqual(self.path.read_text(), original)

    def test_verified_image_and_media_evidence_allow_retirement(self):
        delivered = LEDGER.replace("status: requested", "status: delivered")
        delivered = delivered.replace("art_job_id: null", "art_job_id: 42163")
        delivered = delivered.replace("art_image_id: null", "art_image_id: 252101")
        delivered = delivered.replace("  verdict: null", "  delivery_check: 'ArtJob 42163 DONE; HEAD 200 image/webp and newer Last-Modified'\n  verdict: null")
        self.path.write_text(delivered, encoding="utf-8")
        self.assertEqual(preserve_completed_submissions([request()], art_dir=self.root), set())
        self.assertEqual(self.path.read_text(), delivered)

    def test_concurrent_edit_stops_before_write(self):
        def competing_editor(path):
            path.write_text(LEDGER + "# concurrent editor\n", encoding="utf-8")

        with self.assertRaisesRegex(RuntimeError, "changed concurrently"):
            preserve_completed_submissions(
                [request()], art_dir=self.root, before_write=competing_editor
            )
        self.assertEqual(self.path.read_text(), LEDGER + "# concurrent editor\n")

    def test_unverified_done_request_stays_done_not_requeued(self):
        with mock.patch("shifting_desks_round_evidence.preserve_completed_submissions", return_value={REQUEST_ID}):
            normalized = build_workspace.normalize_art_requests({"requests": [request(job_id=None)]})
        self.assertEqual(len(normalized), 1)
        self.assertEqual(normalized[0]["status"], "done")
        self.assertIsNone(normalized[0]["last_art_job_id"])


if __name__ == "__main__":
    unittest.main()
