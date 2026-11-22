"""Source and coverage contracts for Rainbow Space Princess's new painted depths."""

import unittest
from pathlib import Path

import yaml

from scripts import art_ledger_authoring as authoring
from scripts.repair_negation_art_prompts import violations


ART = (
    Path(__file__).resolve().parents[1]
    / "projects/rainbow-bullet-hell-space-princess/art"
)


class RainbowStageDepthArtTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = yaml.safe_load(
            (ART / "DOODLE-STAGE-DEPTH-PLANES-2026-11-22.yaml").read_text()
        )
        cls.first_round = yaml.safe_load((ART / "DOODLE-SET-1.yaml").read_text())
        cls.review = yaml.safe_load(
            (ART / "DOODLE-SET-1-REVIEW.yaml").read_text()
        )["decisions"]

    def test_all_eight_main_acts_have_two_independent_depths(self):
        subjects = self.ledger["subjects"]
        keys = [subject["key"] for subject in subjects]
        self.assertEqual(len(keys), 16)
        self.assertEqual(len(set(keys)), len(keys))
        self.assertEqual(
            set(keys),
            {
                f"r9-s{act:02d}-{depth}"
                for act in range(1, 9)
                for depth in ("far", "mid")
            },
        )
        self.assertEqual(len({subject["seed"] for subject in subjects}), 16)
        self.assertEqual(
            {subject["lane"] for subject in subjects},
            {"kontext"},
        )

    def test_every_source_was_reviewer_approved_and_delivered(self):
        keepers = {}
        for subject in self.first_round["subjects"]:
            asset = subject.get("asset", "").removeprefix(
                "rainbow-princess-art/doodle/"
            )
            decision = self.review.get(asset)
            if decision != "keep" and not (
                isinstance(decision, dict) and "keep" in decision
            ):
                continue
            art = (subject.get("art") or {}).get(subject["lane"]) or {}
            if art.get("status") == "DONE":
                keepers[asset] = art.get("art_image_id")

        for subject in self.ledger["subjects"]:
            key = subject["key"]
            act = key.split("-")[1]
            source = f"stages/{act}-card"
            with self.subTest(key=key):
                self.assertIn(source, keepers)
                self.assertEqual(subject["source_image_id"], keepers[source])
                self.assertEqual(
                    subject["asset"],
                    f"rainbow-princess-art/doodle/stages/"
                    f"{act}-{key.split('-')[-1]}",
                )

    def test_art_workflow_persists_priority_receipts_before_general_sweep(self):
        workflow_path = (
            Path(__file__).resolve().parents[1]
            / ".github/workflows/auto-art-generate.yml"
        )
        workflow = yaml.safe_load(workflow_path.read_text())
        steps = workflow["jobs"]["generate"]["steps"]
        named = {step.get("name"): (index, step) for index, step in enumerate(steps)}
        priority = "Submit priority Rainbow stage-depth ArtJobs"
        checkpoint = "Checkpoint priority Rainbow stage-depth ArtJob IDs"
        general = "Sweep opted-in art ledgers"
        self.assertIn(priority, named)
        self.assertIn(checkpoint, named)
        self.assertIn(general, named)
        self.assertLess(named[priority][0], named[checkpoint][0])
        self.assertLess(named[checkpoint][0], named[general][0])
        command = named[priority][1]["run"]
        self.assertIn("enqueue_art_requests.py", command)
        self.assertIn("DOODLE-STAGE-DEPTH-PLANES-2026-11-22.yaml", command)
        self.assertIn("--live", command)
        self.assertIn("KR_API_TOKEN", named[priority][1]["env"])
        self.assertTrue(named[priority][1]["continue-on-error"])
        self.assertIn("checkpoint_art_state.sh", named[checkpoint][1]["run"])
        self.assertIn("always()", named[checkpoint][1]["if"])

    def test_high_priority_private_generation_and_readable_stage_planes(self):
        self.assertTrue(self.ledger["auto_submit"])
        self.assertEqual(self.ledger["priority"], 1000)
        self.assertFalse(self.ledger["is_public"])
        self.assertFalse(self.ledger["is_mature"])
        lane = self.ledger["lanes"][0]
        self.assertEqual(lane["engine"], "kontext")
        self.assertEqual(lane["key"], "kontext")
        for subject in self.ledger["subjects"]:
            with self.subTest(key=subject["key"]):
                self.assertEqual(subject["size"], "1344x768")
                prompt = subject["prompt_prose"].lower()
                self.assertIn("upper", prompt)
                self.assertIn("upper", prompt)
                self.assertGreater(len(prompt), 260)
                self.assertEqual(violations(prompt), [])
        self.assertEqual(authoring.ledger_problems(self.ledger), [])


if __name__ == "__main__":
    unittest.main()
