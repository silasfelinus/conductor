"""Slime City Round 2 art must cover every authored faction-campaign fork.

A queued ledger is not a rendered image. This verifies source completeness, not delivery.
"""

from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "projects/slime-city/art/BLACKOUT-STORY-ROUND-2.yaml"
TEAMS = ("catgirls", "bloodfairies", "ironjaw", "riot", "undertow", "exchange")
ATTACKS = ("sword", "arrow", "spell", "claw", "bite", "blast")


class RoundTwoArtContract(unittest.TestCase):
    def test_complete_story_and_missing_founder_cards(self):
        data = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
        self.assertTrue(data["auto_submit"])
        self.assertFalse(data["is_public"])
        self.assertEqual(data["project_slug"], "slime-city")
        subjects = data["subjects"]
        self.assertEqual(len(subjects), 168)
        self.assertEqual(len({subject["key"] for subject in subjects}), 168)
        self.assertEqual(len({subject["asset"] for subject in subjects}), 168)
        self.assertEqual(len({subject["seed"] for subject in subjects}), 168)
        self.assertTrue(all(subject["lane"] == "krea2" for subject in subjects))
        self.assertTrue(all(subject["prompt_prose"].strip() for subject in subjects))
        by_entity = {}
        for subject in subjects:
            by_entity.setdefault(subject["entity"], []).append(subject)
        self.assertEqual(
            {entity: len(rows) for entity, rows in by_entity.items()},
            {
                "card-art": 24,
                "campaign-opening": 6,
                "campaign-scene": 30,
                "campaign-choice-result": 60,
                "campaign-defeat": 30,
                "campaign-ending": 12,
                "attack-icon": 6,
            },
        )
        keys = {subject["key"] for subject in subjects}
        for team in TEAMS:
            self.assertIn(f"slime-story-{team}-opening", keys)
            for ending in ("triumph", "compromise"):
                self.assertIn(f"slime-story-{team}-ending-{ending}", keys)
            for chapter in range(1, 6):
                prefix = f"slime-story-{team}-{chapter:02d}"
                for panel in ("scene", "conviction", "cunning", "defeat"):
                    self.assertIn(f"{prefix}-{panel}", keys)
        for family in ATTACKS:
            self.assertIn(f"slime-attack-{family}", keys)


if __name__ == "__main__":
    unittest.main()
