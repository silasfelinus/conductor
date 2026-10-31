"""Adversarial contracts for Hoshimori's non-submitting 64-face readiness audit."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_memory_dungeon_hoshimori_gallery_readiness import (  # noqa: E402
    ART, WORLDS, audit, load_report,
)


def fixtures():
    manifests, ledgers, snapshots = {}, {}, {}
    for world, (gallery, ledger, snapshot, _) in WORLDS.items():
        manifests[world] = yaml.safe_load((ART / gallery).read_text(encoding="utf-8"))
        ledgers[world] = yaml.safe_load((ART / ledger).read_text(encoding="utf-8"))
        snapshots[world] = json.loads((ART / snapshot).read_text(encoding="utf-8"))
    return manifests, ledgers, snapshots


class HoshimoriGalleryReadinessTests(unittest.TestCase):
    def setUp(self):
        self.manifests, self.ledgers, self.snapshots = fixtures()

    def test_real_committed_inventory_is_authored_not_delivered(self):
        report = load_report()
        self.assertEqual(report["gallery_briefs"], 64)
        self.assertEqual(report["gallery_artjobs"], 0)
        self.assertEqual(report["gallery_delivered_images"], 0)
        self.assertEqual(report["style_artjobs"], 20)
        self.assertFalse(report["ready_for_gallery_submission"])
        self.assertEqual(report["source"], "committed_snapshot_not_live")
        self.assertEqual(len(report["blockers"]), 3)

    def test_gallery_duplicate_destination_fails(self):
        faces = self.manifests["e07"]["faces"]
        faces[1]["image_path"] = faces[0]["image_path"]
        with self.assertRaisesRegex(ValueError, "destination"):
            audit(self.manifests, self.ledgers, self.snapshots)

    def test_gallery_cannot_claim_a_job_or_auto_submit(self):
        self.manifests["e08"]["faces"][0]["last_art_job_id"] = 999999
        with self.assertRaisesRegex(ValueError, "invented"):
            audit(self.manifests, self.ledgers, self.snapshots)
        del self.manifests["e08"]["faces"][0]["last_art_job_id"]
        self.manifests["e08"]["auto_submit"] = True
        with self.assertRaisesRegex(ValueError, "authoring-only"):
            audit(self.manifests, self.ledgers, self.snapshots)

    def test_missing_cross_realm_pair_and_prompt_rejection(self):
        face = self.manifests["e07"]["faces"][31]
        del face["cross_realm"]
        with self.assertRaisesRegex(ValueError, "collaboration"):
            audit(self.manifests, self.ledgers, self.snapshots)
        face["cross_realm"] = "e03"
        face["prompt"] += " A card illustration with no text."
        with self.assertRaisesRegex(ValueError, "Krea2"):
            audit(self.manifests, self.ledgers, self.snapshots)

    def test_style_snapshot_cannot_substitute_another_job(self):
        self.snapshots["e08"]["results"][0]["jobId"] = 52108
        with self.assertRaisesRegex(ValueError, "receipt mismatch"):
            audit(self.manifests, self.ledgers, self.snapshots)

    def test_style_snapshot_rejects_forged_delivery_without_artimage(self):
        snapshot = self.snapshots["e07"]
        row = snapshot["results"][0]
        row["status"] = "delivered"
        row["artImageId"] = None
        snapshot["counts"] = {"delivered": 1, "pending": 9}
        snapshot["delivered"] = 1
        snapshot["pendingReview"] = 9
        with self.assertRaisesRegex(ValueError, "without ArtImage"):
            audit(self.manifests, self.ledgers, self.snapshots)

    def test_style_snapshot_rejects_forged_totals(self):
        self.snapshots["e08"]["delivered"] = 10
        with self.assertRaisesRegex(ValueError, "inconsistent"):
            audit(self.manifests, self.ledgers, self.snapshots)

    def test_receipts_must_be_durable_and_unique(self):
        self.ledgers["e07"]["requests"][1]["last_art_job_id"] = (
            self.ledgers["e07"]["requests"][0]["last_art_job_id"]
        )
        with self.assertRaisesRegex(ValueError, "Duplicate ArtJob"):
            audit(self.manifests, self.ledgers, self.snapshots)

    def test_missing_style_snapshot_is_not_success(self):
        self.snapshots["e08"]["results"].pop()
        with self.assertRaisesRegex(ValueError, "ten-row"):
            audit(self.manifests, self.ledgers, self.snapshots)


if __name__ == "__main__":
    unittest.main()
