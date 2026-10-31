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
    ART, WORLDS, PILOT_LEDGER, ROUND2_LEDGER,
    audit, audit_live, audit_pilot_live, load_report,
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
        self.assertEqual(report["gallery_artjobs"], 8)
        self.assertEqual(report["gallery_unsubmitted"], 56)
        self.assertEqual(report["gallery_pilot"]["submitted"], 8)
        self.assertEqual(report["gallery_delivered_images"], 0)
        self.assertEqual(report["style_artjobs"], 20)
        self.assertFalse(report["ready_for_gallery_submission"])
        self.assertEqual(report["source"], "committed_snapshot_not_live")
        self.assertEqual(len(report["blockers"]), 4)

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

    def test_gallery_pilot_cannot_reuse_a_style_job_receipt(self):
        pilot = yaml.safe_load(PILOT_LEDGER.read_text(encoding="utf-8"))
        pilot["subjects"][0]["jobs"]["krea2"] = self.ledgers["e07"]["requests"][0]["last_art_job_id"]
        with self.assertRaisesRegex(ValueError, "reuses a style-proof"):
            audit(self.manifests, self.ledgers, self.snapshots, pilot=pilot)

    def test_pilot_job_identity_and_done_are_not_delivery(self):
        pilot = yaml.safe_load(PILOT_LEDGER.read_text(encoding="utf-8"))
        jobs = [
            {
                "id": subject["jobs"]["krea2"], "projectSlug": "memory-dungeon",
                "engine": "COMFY", "status": "PENDING",
                "payload": {"promptString": subject["prompt_prose"],
                            "save": {"isPublic": False, "isMature": False}},
            }
            for subject in pilot["subjects"]
        ]
        report = audit_pilot_live(pilot, jobs)
        self.assertEqual(report["counts"], {"pending": 8})
        self.assertEqual(report["delivered"], 0)

        jobs[0]["status"] = "DONE"
        jobs[0]["artImageId"] = 777777
        report = audit_pilot_live(pilot, jobs)
        self.assertEqual(report["counts"], {"done_media_unverified": 1, "pending": 7})
        self.assertEqual(report["delivered"], 0)

    def test_pilot_forged_project_or_prompt_fails_identity(self):
        pilot = yaml.safe_load(PILOT_LEDGER.read_text(encoding="utf-8"))
        first = pilot["subjects"][0]
        job = {
            "id": first["jobs"]["krea2"], "projectSlug": "unrelated-game",
            "engine": "COMFY", "status": "DONE", "artImageId": 123,
            "payload": {"promptString": first["prompt_prose"],
                        "save": {"isPublic": False, "isMature": False}},
        }
        report = audit_pilot_live(pilot, [job])
        self.assertEqual(report["counts"], {"identity_mismatch": 1, "job_missing": 7})
        job["projectSlug"] = "memory-dungeon"
        job["payload"]["promptString"] = "unrelated image"
        self.assertEqual(audit_pilot_live(pilot, [job])["counts"]["identity_mismatch"], 1)
        job["payload"]["promptString"] = first["prompt_prose"]
        job["payload"]["save"]["isPublic"] = True
        self.assertEqual(audit_pilot_live(pilot, [job])["counts"]["identity_mismatch"], 1)

    def test_pilot_duplicate_live_job_rows_fail_closed(self):
        pilot = yaml.safe_load(PILOT_LEDGER.read_text(encoding="utf-8"))
        job = {"id": pilot["subjects"][0]["jobs"]["krea2"]}
        with self.assertRaisesRegex(ValueError, "Duplicate live ArtJob"):
            audit_pilot_live(pilot, [job, dict(job)])

    def test_live_missing_jobs_cannot_pass_visual_gate(self):
        report = audit_live(
            self.manifests, self.ledgers, self.snapshots,
            jobs=[], heartbeat_state="silent",
        )
        self.assertEqual(report["live"]["style_not_delivered"], 20)
        self.assertEqual(report["live"]["style_proofs"]["e07"]["snapshot_delivered"], 0)
        self.assertFalse(report["ready_for_visual_review"])
        self.assertFalse(report["ready_for_gallery_submission"])

    def test_live_verified_style_proofs_require_visual_review_before_enqueue(self):
        jobs = []
        for world in WORLDS:
            for request in self.ledgers[world]["requests"]:
                jobs.append({
                    "id": request["last_art_job_id"],
                    "status": "DONE",
                    "artImageId": request["last_art_job_id"] + 100000,
                    "createdAt": "2026-10-30T00:00:00Z",
                    "payload": {"conductorRequest": {
                        "id": request["id"],
                        "imagePath": request["image_path"],
                        "targetRepo": "silasfelinus/kind_robots",
                    }},
                })
        report = audit_live(
            self.manifests, self.ledgers, self.snapshots,
            jobs=jobs, heartbeat_state="ok",
            media_probe=lambda _path, _created: "delivered",
        )
        self.assertEqual(report["live"]["style_delivered"], 20)
        self.assertTrue(report["ready_for_visual_review"])
        self.assertFalse(report["ready_for_gallery_submission"])
        self.assertEqual(report["gallery_artjobs"], 8)
        self.assertEqual(report["live"]["gallery_pilot"]["counts"]["job_missing"], 8)


    def test_second_pilot_is_counted_without_pretending_to_be_submitted(self):
        report = load_report()
        self.assertEqual(report["gallery_pilots"]["round1"]["submitted"], 8)
        self.assertEqual(report["gallery_pilots"]["round2"]["submitted"], 0)
        self.assertEqual(report["gallery_artjobs"], 8)
        self.assertEqual(report["gallery_unsubmitted"], 56)

    def test_cross_round_artjob_receipt_collision_is_rejected(self):
        round2 = yaml.safe_load(ROUND2_LEDGER.read_text(encoding="utf-8"))
        first = yaml.safe_load(PILOT_LEDGER.read_text(encoding="utf-8"))
        round2["subjects"][0]["jobs"] = {
            "krea2": first["subjects"][0]["jobs"]["krea2"]
        }
        with self.assertRaisesRegex(ValueError, "duplicate an ArtJob receipt"):
            audit(self.manifests, self.ledgers, self.snapshots, pilot2=round2)

    def test_second_pilot_receipt_counts_as_queued_not_delivered(self):
        round2 = yaml.safe_load(ROUND2_LEDGER.read_text(encoding="utf-8"))
        round2["subjects"][0]["jobs"] = {"krea2": 899001}
        round2["subjects"][0]["art"] = {
            "krea2": {"status": "PENDING", "art_image_id": None}
        }
        report = audit(self.manifests, self.ledgers, self.snapshots, pilot2=round2)
        self.assertEqual(report["gallery_artjobs"], 9)
        self.assertEqual(report["gallery_unsubmitted"], 55)
        self.assertEqual(report["gallery_delivered_images"], 0)
        live = audit_live(
            self.manifests, self.ledgers, self.snapshots,
            pilot2=round2, jobs=[], heartbeat_state="ok",
        )
        self.assertEqual(live["live"]["gallery_pilots"]["round2"]["counts"],
                         {"job_missing": 1, "unsubmitted": 7})
        self.assertFalse(live["ready_for_gallery_submission"])



if __name__ == "__main__":
    unittest.main()
