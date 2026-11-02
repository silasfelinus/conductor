"""Source-backed Hoshimori e07 gallery reveal plan; no ArtJob or runtime-unlock claim."""
from collections import Counter
from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "projects/memory-dungeon/art"
BRIEFS = ART / "HOSHIMORI-E07-GALLERY-BRIEFS.yaml"
PLAN = ART / "HOSHIMORI-E07-GALLERY-UNLOCK-PLAN.yaml"

# Verified against kind_robots/utils/memoryDungeon/hoshimoriWarm.ts at
# source blob 696ca900c3ba56c65d9c10451d476a06e3360a2b; update deliberately if the runtime source changes.
SITE_SNAPSHOT = {
    "1,1": ("Vesper’s Childhood Footbridge", ("seat", "listen")),
    "2,2": ("Pip’s Ledger House", ("trace", "protect")),
    "4,3": ("The Red Oven", ("question", "serve")),
    "3,3": ("The Guest Registry", ("witness", "anonymous")),
    "2,4": ("The Tanuki’s Honest Market", ("audit", "trade")),
    "6,4": ("The Kappa’s Ferry Ledger", ("return", "labor")),
    "3,4": ("The Umbrella Workshop", ("mend", "release")),
    "5,5": ("The Borrowed Hearth", ("host", "measure")),
    "7,1": ("The Tengu’s Weather Desk", ("pay", "signal")),
    "6,7": ("Stone Steps of the Oni", ("water", "plan")),
    "4,1": ("The Orchard of Unfinished Maps", ("repair", "mark")),
    "3,8": ("The Paper Shadow Theatre", ("ask", "perform")),
    "8,8": ("The South Watch Assembly", ("consent", "open")),
    "4,7": ("The River Archive", ("copy", "seal")),
    "2,6": ("The Lantern Refuge", ("shelter", "witness")),
    "8,1": ("The Observatory of Unsent Names", ("ask", "erase")),
    "3,7": ("The Mirror Pond", ("question", "protect")),
    "7,8": ("The Oathboat Landing", ("witness", "decline")),
    "4,4": ("The Road Vesper Sold", ("witness", "depart")),
    "1,2": ("The Lantern Stall", ("tend", "borrow")),
    "1,3": ("The Returning Slippers", ("return", "record")),
    "2,3": ("The Night-Crew Photograph", ("question", "hold")),
    "7,5": ("The Difficult Call", ("inquire", "respect")),
    "6,5": ("The Orchard Tithe", ("challenge", "compensate")),
    "6,6": ("The Moss-Stair Census", ("invite", "refuse")),
    "7,6": ("The Snowbell Relay", ("signal", "wait")),
    "7,7": ("The Kindness Tax", ("challenge", "relief")),
}


class HoshimoriGalleryUnlockPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.briefs = yaml.safe_load(BRIEFS.read_text(encoding="utf-8"))
        cls.plan = yaml.safe_load(PLAN.read_text(encoding="utf-8"))
        cls.entries = cls.plan["entries"]

    def test_budget_and_explicit_non_delivery(self):
        self.assertEqual(self.plan["version"], 1)
        self.assertEqual(self.plan["project"], "memory-dungeon")
        self.assertEqual(self.plan["world"], "e07")
        self.assertEqual(self.plan["stage"], "unlock_plan_only")
        self.assertEqual(self.plan["art_delivery"], "unverified")
        self.assertEqual(self.plan["source_manifest"], BRIEFS.name)
        self.assertEqual(self.plan["save_source"], "memory-dungeon-hoshimori-e07-v1")
        self.assertEqual(self.plan["wave_sizes"], [6, 7, 8, 9])
        self.assertEqual(len(self.entries), 32)
        self.assertEqual(len({item["id"] for item in self.entries}), 32)

    def test_exact_brief_identity_and_source_site_choice_contract(self):
        for face, item in zip(self.briefs["faces"], self.entries, strict=True):
            with self.subTest(face=face["id"]):
                self.assertEqual(item["id"], face["id"])
                self.assertEqual(item["category"], face["category"])
                self.assertEqual(item["site_key"], face["site_key"])
                title, choices = SITE_SNAPSHOT[item["site_key"]]
                self.assertEqual(face["source_title"], title)
                self.assertEqual(tuple(item["any_site_choice"]), choices)
                self.assertEqual(len(choices), 2)
                self.assertNotIn("visited", item)
                self.assertNotIn("delivered", item)
                self.assertNotIn("art_job_id", item)

    def test_four_local_waves_and_two_distinct_cross_realm_cards(self):
        local, collaborations = self.entries[:30], self.entries[30:]
        self.assertEqual(dict(Counter(x["wave"] for x in local)), {1: 6, 2: 7, 3: 8, 4: 9})
        self.assertTrue(all(x["category"] != "collaboration" for x in local))
        self.assertTrue(all("requires_earned_cross_realm" not in x for x in local))
        self.assertEqual([x["wave"] for x in collaborations], ["collaboration"] * 2)
        self.assertEqual([x["requires_earned_cross_realm"] for x in collaborations], ["e05", "e03"])
        self.assertEqual([x["category"] for x in collaborations], ["collaboration"] * 2)

    def test_fixed_earth_photos_are_not_awarded_by_choice_alone(self):
        for item in self.entries:
            with self.subTest(face=item["id"]):
                self.assertEqual(item.get("requires_earned_photo", False), item["site_key"] in {"2,3", "7,5"})
                self.assertTrue(set(item).issubset({
                    "id", "category", "wave", "site_key", "any_site_choice",
                    "requires_earned_photo", "requires_earned_cross_realm",
                }))


if __name__ == "__main__":
    unittest.main()
