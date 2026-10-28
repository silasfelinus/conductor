"""House atlas production request and receipt integrity regressions."""
import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_memory_dungeon_house_atlases import EXPECTED, LEDGER, audit_delivery, validate  # noqa: E402


class HouseAtlasArtTests(unittest.TestCase):
    def test_two_distinct_authored_krea2_requests(self):
        data = yaml.safe_load(LEDGER.read_text())
        receipts = validate(data)
        self.assertEqual(set(receipts), set(EXPECTED))
        self.assertTrue(all(job is None or job > 0 for job in receipts.values()))

    def test_rejects_wrong_destination_and_duplicate(self):
        data = yaml.safe_load(LEDGER.read_text())
        data["requests"][0]["image_path"] = "public/images/memory-dungeon/other.webp"
        with self.assertRaisesRegex(ValueError, "destination"):
            validate(data)
        data = yaml.safe_load(LEDGER.read_text())
        data["requests"][1]["id"] = data["requests"][0]["id"]
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            validate(data)

    def test_only_durable_positive_ids_satisfy_submission_gate(self):
        data = yaml.safe_load(LEDGER.read_text())
        data["requests"][0].pop("last_art_job_id", None)
        with self.assertRaisesRegex(ValueError, "Unsubmitted"):
            validate(data, require_jobs=True)
        data["requests"][0]["last_art_job_id"] = 46501
        data["requests"][1]["last_art_job_id"] = 46502
        self.assertEqual(len(validate(data, require_jobs=True)), 2)
        data["requests"][1]["last_art_job_id"] = "not-an-id"
        with self.assertRaisesRegex(ValueError, "Invalid"):
            validate(data, require_jobs=True)


    def test_live_audit_proves_exact_jobs_and_fresh_image_media(self):
        data = yaml.safe_load(LEDGER.read_text())
        calls = []
        jobs = []
        for row in data["requests"]:
            jobs.append({
                "id": row["last_art_job_id"],
                "status": "DONE",
                "artImageId": row["last_art_job_id"] + 1000,
                "createdAt": "2026-10-28T10:00:00Z",
                "payload": {"conductorRequest": {
                    "id": row["id"],
                    "imagePath": row["image_path"],
                    "targetRepo": row["target_repo"],
                }},
            })
        def head(path, created):
            calls.append((path, created))
            return "delivered"
        report = audit_delivery(data, jobs, head)
        self.assertEqual(report["total"], 2)
        self.assertEqual(report["delivered"], 2)
        self.assertEqual({row["jobId"] for row in report["results"]}, {50365, 50366})
        self.assertEqual({path for path, _ in calls}, set(EXPECTED.values()))

    def test_live_audit_does_not_conflate_render_and_delivery(self):
        data = yaml.safe_load(LEDGER.read_text())
        original, mirrored = data["requests"]
        jobs = [
            {
                "id": original["last_art_job_id"],
                "status": "RUNNING",
                "payload": {"conductorRequest": {
                    "id": original["id"], "imagePath": original["image_path"],
                    "targetRepo": original["target_repo"],
                }},
            },
            {
                "id": mirrored["last_art_job_id"],
                "status": "DONE",
                "artImageId": 555,
                "createdAt": "2026-10-28T10:00:00Z",
                "payload": {"conductorRequest": {
                    "id": mirrored["id"], "imagePath": mirrored["image_path"],
                    "targetRepo": mirrored["target_repo"],
                }},
            },
        ]
        report = audit_delivery(data, jobs, lambda *_: "media_unreachable")
        self.assertEqual([row["status"] for row in report["results"]],
                         ["running", "media_unreachable"])
        self.assertEqual(report["delivered"], 0)
        jobs[1]["payload"]["conductorRequest"]["imagePath"] = original["image_path"]
        report = audit_delivery(data, jobs, lambda *_: self.fail("wrong job must not HEAD"))
        self.assertEqual(report["results"][1]["status"], "job_identity_mismatch")

    def test_delivery_audit_requires_both_real_job_ids(self):
        data = yaml.safe_load(LEDGER.read_text())
        data["requests"][1].pop("last_art_job_id")
        with self.assertRaisesRegex(ValueError, "Unsubmitted"):
            audit_delivery(data, [], lambda *_: self.fail("no HEAD"))


if __name__ == "__main__":
    unittest.main()
