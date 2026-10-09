"""Source contract for the modular five-land Zuzu board-game design."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "projects/zuzu-shifting-lands"
WORLD = ROOT / "worlds/zuzu"


class ShiftingLandsContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((GAME / "WORLD-DECKS.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((WORLD / "catalog.json").read_text(encoding="utf-8"))

    def test_registered_and_has_all_five_lands(self):
        self.assertEqual(self.manifest["world_id"], "zuzu")
        self.assertEqual(self.manifest["conductor_project"], "zuzu-shifting-lands")
        production = [p for p in self.catalog["productions"] if p["project"] == "zuzu-shifting-lands"]
        self.assertEqual(len(production), 1)
        self.assertEqual(production[0]["role"], "noncanonical-procedural-trails")
        self.assertEqual(len(self.manifest["lands"]), 5)
        self.assertEqual([land["chapter"] for land in self.manifest["lands"]], [1, 2, 3, 4, 5])
        self.assertEqual(self.manifest["journey"]["encounters_per_land"], 3)
        for land in self.manifest["lands"]:
            with self.subTest(land=land["id"]):
                self.assertEqual(len(land["locations"]), 3)
                self.assertEqual(len({item["id"] for item in land["locations"]}), 3)
                self.assertTrue(land["major_challenge"]["id"])
                self.assertGreaterEqual(len(land["major_challenge"]["outcome_modes"]), 3)

    def test_species_and_roles_are_distinct_taxonomies(self):
        pools = self.manifest["facet_pools"]
        species = {entry["key"]: entry for entry in pools["species"]}
        roles = {entry["key"]: entry for entry in pools["roles"]}
        self.assertEqual(set(species).intersection(roles), set())
        self.assertTrue(all(entry["taxonomy"] == "SPECIES" for entry in species.values()))
        self.assertTrue(all(entry["taxonomy"] in ("OCCUPATION", "ROLE", "ARCHETYPE")
                            for entry in roles.values()))
        self.assertGreater(len(pools["dispositions"]), 3)
        # First-land pool allows both identities and roles to vary independently.
        home = self.manifest["lands"][0]
        self.assertIn("rabbit", home["species"])
        self.assertIn("otter", home["species"])
        self.assertIn("homesteader", home["roles"])
        self.assertIn("caretaker", home["roles"])
        self.assertFalse(any("disposition" in entry or "alignment" in entry for entry in species.values()))
        self.assertFalse(any("disposition" in entry or "alignment" in entry for entry in roles.values()))

    def test_setting_and_sources_have_open_fictional_spoilers(self):
        self.assertTrue((WORLD / "WORLD-GUIDE.md").is_file())
        self.assertEqual(
            next(s for s in self.catalog["canon_sources"] if s["id"] == "world-guide")["authority"],
            "silas-directed-setting",
        )
        self.assertEqual(self.manifest["editorial_rules"]["known_named_characters"].startswith("Only"), True)
        self.assertIn("Fictional plot spoilers belong in GitHub",
                      self.manifest["editorial_rules"]["secrets"])
        self.assertEqual(self.manifest["lands"][0]["major_challenge"]["boss_source"],
                         "worlds/zuzu/WORLD-GUIDE.md")
        self.assertEqual(self.manifest["lands"][0]["major_challenge"]["label"], "The Abbess")
        self.assertEqual({entry["id"] for entry in self.manifest["world_mysteries"]},
                         {"lost-humanity", "abbess-cosmic-rites"})
        self.assertIn("No GitHub spoiler embargo", (WORLD / "WORLD-GUIDE.md").read_text(encoding="utf-8"))
        self.assertEqual(self.manifest["status"], "design-manifest-not-imported")
        self.assertTrue((GAME / "DESIGN-BRIEF.md").is_file())
        self.assertTrue((GAME / "roadmap.yaml").is_file())


if __name__ == "__main__":
    unittest.main()
