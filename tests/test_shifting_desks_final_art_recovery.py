"""Prevent the Shifting Desks final ending recovery from fabricating art delivery."""

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest import mock

import yaml

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "projects/shifting-desks/art/ROUND-17.yaml"
SCRIPT = ROOT / "projects/shifting-desks/art/reconcile_delivery.py"


def load_reconciler():
    spec = importlib.util.spec_from_file_location("shifting_desks_delivery", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ShiftingDesksFinalArtTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reconciler = load_reconciler()
        cls.round = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
        cls.row = cls.round["subjects"][0]

    def test_recovery_preserves_existing_work(self):
        self.assertEqual(self.round["round"], "shifting-desks-17")
        self.assertIn(44064, self.row["earlier_art_jobs"])
        self.assertIn(44065, self.row["earlier_art_jobs"])
        self.assertIn(252101, self.row["earlier_art_images"])
        self.assertIn(252102, self.row["earlier_art_images"])
        self.assertEqual(self.row["verdict"], None)
        self.assertIn(17, self.reconciler.ROUNDS)

    def test_missing_media_is_not_misreported_as_delivered(self):
        job = {
            "id": 98765,
            "status": "DONE",
            "artImageId": 76543,
            "createdAt": "2026-11-01T22:00:00Z",
            "idempotencyKey": self.row["request_id"],
            "payload": {
                "imagePath": "public/images/shifting-desks/endings/permanent-adjournment.webp",
                "targetRepo": "silasfelinus/kind_robots",
                "conductorRequest": {"id": self.row["request_id"]},
            },
        }
        requested = self.reconciler.timestamp(self.round["requested_at"])
        with mock.patch.object(self.reconciler, "probe_media", return_value=(None, "HTTP 404")):
            changes = self.reconciler.reconcile_row(
                self.row, [job], requested, probe=self.reconciler.probe_media
            )
        self.assertEqual(changes["status"], "rendered")
        self.assertEqual(changes["art_job_id"], 98765)
        self.assertEqual(changes["art_image_id"], 76543)
        self.assertNotIn("verdict", changes)

    def test_unknown_or_prior_job_cannot_mark_new_recovery_delivered(self):
        requested = self.reconciler.timestamp(self.round["requested_at"])
        old = {
            "id": 44064,
            "status": "DONE",
            "artImageId": 252101,
            "createdAt": "2026-10-23T12:00:00Z",
            "idempotencyKey": self.row["request_id"],
            "payload": {
                "imagePath": "public/images/shifting-desks/endings/permanent-adjournment.webp",
                "targetRepo": "silasfelinus/kind_robots",
                "conductorRequest": {"id": self.row["request_id"]},
            },
        }
        self.assertEqual(self.reconciler.reconcile_row(self.row, [old], requested), {})


if __name__ == "__main__":
    unittest.main()
