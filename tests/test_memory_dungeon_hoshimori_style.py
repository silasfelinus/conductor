"""Hoshimori first-stage production art receipt and pipeline regressions."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_memory_dungeon_hoshimori_style import (  # noqa: E402
    CATEGORIES, LEDGER, validate,
)


class HoshimoriWarmStyleTests(unittest.TestCase):
    def setUp(self):
        self.data = yaml.safe_load(LEDGER.read_text())

    def test_eight_private_canon_grounded_samples_are_distinct(self):
        receipts = validate(self.data)
        self.assertEqual(set(receipts), set(CATEGORIES))
        self.assertEqual(len(receipts), 8)
        self.assertEqual(len({r["image_path"] for r in self.data["requests"]}), 8)
        self.assertTrue(all(r["page_url"].endswith("/play/memory") for r in self.data["requests"]))
        self.assertTrue(all("hoshimori/e07/style-proofs/" in r["image_path"] for r in self.data["requests"]))

    def test_rejects_duplicate_id_or_path_and_cross_project_destination(self):
        data = deepcopy(self.data)
        data["requests"][1]["id"] = data["requests"][0]["id"]
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            validate(data)
        data = deepcopy(self.data)
        data["requests"][1]["image_path"] = data["requests"][0]["image_path"]
        with self.assertRaisesRegex(ValueError, "destination"):
            validate(data)
        data = deepcopy(self.data)
        data["requests"][0]["target_repo"] = "silasfelinus/conductor"
        with self.assertRaisesRegex(ValueError, "repository"):
            validate(data)

    def test_submission_gate_needs_eight_unique_positive_artjob_ids(self):
        data = deepcopy(self.data)
        with self.assertRaisesRegex(ValueError, "Unsubmitted"):
            validate(data, require_jobs=True)
        for index, row in enumerate(data["requests"]):
            row["last_art_job_id"] = 60001 + index
        self.assertEqual(len(validate(data, require_jobs=True)), 8)
        data["requests"][7]["last_art_job_id"] = data["requests"][0]["last_art_job_id"]
        with self.assertRaisesRegex(ValueError, "Duplicate ArtJob"):
            validate(data, require_jobs=True)
        data["requests"][7]["last_art_job_id"] = -1
        with self.assertRaisesRegex(ValueError, "Invalid ArtJob"):
            validate(data, require_jobs=True)

    def test_workflow_submits_checkpoints_and_audits_before_render(self):
        workflow = yaml.safe_load((ROOT / ".github/workflows/auto-art-generate.yml").read_text())
        steps = workflow["jobs"]["generate"]["steps"]
        submit = next(s for s in steps if s.get("id") == "memory_dungeon_hoshimori_style_submit")
        self.assertIn("--submit-only", submit["run"])
        self.assertIn("HOSHIMORI-WARM-STYLE-PROOFS.yaml", submit["run"])
        self.assertIn("KR_API_TOKEN", submit["env"])
        checkpoint = next(s for s in steps if s.get("name") ==
                          "Checkpoint Memory Dungeon ArtJob IDs before rendering")
        self.assertIn("HOSHIMORI-WARM-STYLE-PROOFS.yaml", checkpoint["run"])
        audit = next(s for s in steps if s.get("id") == "memory_dungeon_hoshimori_style_receipts")
        self.assertIn("--require-jobs", audit["run"])
        self.assertIn("audit_memory_dungeon_hoshimori_style.py", audit["run"])
        self.assertLess(steps.index(submit), steps.index(checkpoint))
        self.assertLess(steps.index(checkpoint), steps.index(audit))


if __name__ == "__main__":
    unittest.main()
