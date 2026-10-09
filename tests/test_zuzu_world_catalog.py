"""Contract checks for the machine-readable, cross-project Zuzu world index."""
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
CATALOG = ROOT / "worlds" / "zuzu" / "catalog.json"


class ZuzuWorldCatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(CATALOG.read_text(encoding="utf-8"))

    def test_single_world_identity_and_ordered_canon(self):
        self.assertEqual(self.data["schema_version"], 1)
        self.assertEqual(self.data["world"]["id"], "zuzu")
        sources = self.data["canon_sources"]
        self.assertEqual([item["id"] for item in sources[:3]], [
            "book-one", "cast-picks", "video-guardrails"])
        self.assertEqual(sources[-1]["authority"], "archive-only")

    def test_all_project_and_source_paths_exist(self):
        project_sources = []
        for record in self.data["canon_sources"]:
            project_sources.append(record["path"])
        for record in self.data["productions"]:
            self.assertTrue((ROOT / "projects" / record["project"] / "roadmap.yaml").is_file(),
                            record["project"])
            project_sources.extend(record["source_paths"])
        project_sources.extend(item["source_path"] for item in self.data["asset_references"])
        project_sources.extend(item["path"] for item in self.data["pipeline_resources"])
        for path in project_sources:
            self.assertFalse(path.startswith("/") or ".." in pathlib.PurePosixPath(path).parts, path)
            self.assertTrue((ROOT / path).is_file(), path)

    def test_keys_and_verified_art_ids_are_unique(self):
        for section, key in (("canon_sources", "id"), ("productions", "id"),
                             ("asset_references", "key"), ("pipeline_resources", "id")):
            items = [item[key] for item in self.data[section]]
            self.assertEqual(len(items), len(set(items)), section)
        art = self.data["asset_references"]
        self.assertEqual(len({item["id"] for item in art}), len(art))
        self.assertTrue(all(item["model"] == "ArtImage" and
                            isinstance(item["id"], int) and item["id"] > 0
                            for item in art))

    def test_unverified_runtime_models_are_not_invented(self):
        records = self.data["runtime_model_discovery"]
        self.assertEqual(len({item["model"] for item in records}), len(records))
        for item in records:
            self.assertIsInstance(item["stable_ids"], list)
            self.assertTrue(all(isinstance(i, int) for i in item["stable_ids"]))
            if item["status"] in ("not-audited", "join-by-conductorSlug"):
                self.assertEqual(item["stable_ids"], [], item["model"])
        self.assertEqual(next(item for item in records if item["model"] == "Dream")["status"],
                         "legacy-inspiration")


if __name__ == "__main__":
    unittest.main()
