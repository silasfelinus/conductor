"""Hoshimori e08 horror ArtJob request, provenance and workflow regressions."""
from copy import deepcopy
from pathlib import Path
import sys
import re
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_memory_dungeon_hoshimori_horror_style import (  # noqa: E402
    CATEGORIES, LEDGER, PREFIX, audit_delivery, validate,
)


class HoshimoriHorrorStyleTests(unittest.TestCase):
    def setUp(self):
        self.data = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))

    def with_receipts(self):
        data = deepcopy(self.data)
        for index, row in enumerate(data["requests"]):
            row["last_art_job_id"] = 65001 + index
        return data

    def test_ten_distinct_horror_proofs_preserve_world_and_subject_contract(self):
        receipts = validate(self.data)
        self.assertEqual(set(receipts), set(CATEGORIES))
        rows = self.data["requests"]
        self.assertEqual(len(rows), 10)
        self.assertEqual(len({r["image_path"] for r in rows}), 10)
        self.assertTrue(all(r["page_url"].endswith("/play/memory") for r in rows))
        self.assertTrue(all("/hoshimori/e08/style-proofs/" in r["image_path"] for r in rows))
        self.assertEqual(sum(r["category"] == "portrait" for r in rows), 2)
        self.assertEqual(sum(r["category"] == "yokai" for r in rows), 2)
        self.assertTrue(any("Vesper" in r["prompt"] for r in rows))
        self.assertTrue(any("Scylla" in r["prompt"] for r in rows))
        self.assertTrue(all("Junji Ito" not in r["prompt"] for r in rows))

    def test_positive_art_prompts_avoid_inert_negative_text_instructions(self):
        for row in self.data["requests"]:
            with self.subTest(request=row["id"]):
                self.assertIsNone(re.search(
                    r"\bno\s+(?:text|lettering|words|typography)\b",
                    row["prompt"], re.IGNORECASE,
                ))
                self.assertIn("every surface bare and unmarked", row["prompt"])

    def test_preflight_rejects_production_422_prompt_shapes(self):
        for phrase in (
            "no text", "without lettering", "avoid visible typography",
            "card illustration", "poster art", "book cover design",
        ):
            with self.subTest(phrase=phrase):
                data = deepcopy(self.data)
                data["requests"][0]["prompt"] += " " + phrase
                with self.assertRaisesRegex(ValueError, "Krea2 prompt"):
                    validate(data)

    def test_warm_and_horror_jobs_have_no_colliding_request_or_media_ids(self):
        warm_path = ROOT / "projects/memory-dungeon/art/HOSHIMORI-WARM-STYLE-PROOFS.yaml"
        warm = yaml.safe_load(warm_path.read_text(encoding="utf-8"))["requests"]
        horror = self.data["requests"]
        self.assertFalse({r["id"] for r in warm} & {r["id"] for r in horror})
        self.assertFalse({r["image_path"] for r in warm} & {r["image_path"] for r in horror})
        self.assertTrue(all(r["id"].startswith(PREFIX) for r in horror))

    def test_receipts_reject_missing_duplicate_or_wrong_destination(self):
        unsubmitted = deepcopy(self.data)
        for row in unsubmitted["requests"]:
            row.pop("last_art_job_id", None)
        with self.assertRaisesRegex(ValueError, "Unsubmitted"):
            validate(unsubmitted, require_jobs=True)
        data = self.with_receipts()
        self.assertEqual(len(validate(data, require_jobs=True)), 10)
        data["requests"][9]["last_art_job_id"] = data["requests"][0]["last_art_job_id"]
        with self.assertRaisesRegex(ValueError, "Duplicate ArtJob"):
            validate(data, require_jobs=True)
        data = self.with_receipts()
        data["requests"][1]["image_path"] = data["requests"][0]["image_path"]
        with self.assertRaisesRegex(ValueError, "destination"):
            validate(data)
        data = self.with_receipts()
        data["requests"][2]["target_repo"] = "silasfelinus/conductor"
        with self.assertRaisesRegex(ValueError, "repository"):
            validate(data)
        data = self.with_receipts()
        data["requests"][3]["id"] = data["requests"][0]["id"]
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            validate(data)

    def test_live_audit_requires_identity_artimage_and_fresh_media(self):
        data = self.with_receipts()
        jobs = [
            {
                "id": row["last_art_job_id"],
                "status": "DONE",
                "artImageId": row["last_art_job_id"] + 1000,
                "createdAt": "2026-10-30T10:00:00Z",
                "payload": {"conductorRequest": {
                    "id": row["id"],
                    "imagePath": row["image_path"],
                    "targetRepo": row["target_repo"],
                }},
            }
            for row in data["requests"]
        ]
        report = audit_delivery(data, jobs, lambda *_: "delivered")
        self.assertEqual(report["total"], 10)
        self.assertEqual(report["delivered"], 10)
        jobs[0]["payload"]["conductorRequest"]["imagePath"] = data["requests"][1]["image_path"]
        jobs[1].pop("artImageId")
        report = audit_delivery(data, jobs, lambda *_: "media_stale")
        self.assertEqual(report["delivered"], 0)
        self.assertEqual(report["results"][0]["status"], "job_identity_mismatch")
        self.assertEqual(report["results"][1]["status"], "done_without_art_image")

    def test_workflow_submits_and_checkpoints_before_long_render(self):
        workflow = yaml.safe_load((ROOT / ".github/workflows/auto-art-generate.yml").read_text())
        steps = workflow["jobs"]["generate"]["steps"]
        submit = next(s for s in steps if s.get("id") == "memory_dungeon_hoshimori_horror_submit")
        preflight = next(s for s in steps if s.get("name") ==
                         "Verify Memory Dungeon art submission contracts")
        self.assertLess(steps.index(preflight), steps.index(submit))
        receipt = next(s for s in steps if s.get("id") == "memory_dungeon_hoshimori_horror_receipts")
        delivery = next(s for s in steps if s.get("id") == "memory_dungeon_hoshimori_horror_delivery")
        checkpoint = next(s for s in steps if s.get("name") ==
                          "Checkpoint Memory Dungeon ArtJob IDs before rendering")
        self.assertIn("--submit-only", submit["run"])
        self.assertIn("HOSHIMORI-HORROR-STYLE-PROOFS.yaml", submit["run"])
        self.assertIn("KR_API_TOKEN", submit["env"])
        self.assertIn("HOSHIMORI-HORROR-STYLE-PROOFS.yaml", checkpoint["run"])
        self.assertLess(steps.index(submit), steps.index(checkpoint))
        self.assertLess(steps.index(checkpoint), steps.index(receipt))
        self.assertIn("--require-jobs", receipt["run"])
        self.assertIn("--live", delivery["run"])
        self.assertTrue(delivery["continue-on-error"])
        self.assertLess(steps.index(receipt), steps.index(delivery))
        status = next(s for s in steps if s.get("name") ==
                      "Checkpoint Hoshimori horror style delivery status before rendering")
        self.assertIn("HOSHIMORI-HORROR-STYLE-STATUS.json", status["run"])
        self.assertLess(steps.index(delivery), steps.index(status))


if __name__ == "__main__":
    unittest.main()
