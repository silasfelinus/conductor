"""Cross-project Zuzu art-ledger and resource-submission contract."""
import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORLD = ROOT / "worlds" / "zuzu"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


class ZuzuWorldInventoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = read_json(WORLD / "catalog.json")
        cls.inventory = cls.catalog["asset_inventory"]

    def test_all_source_ledgers_are_indexed_without_losing_art_outputs(self):
        files = self.inventory["ledger_parts"]
        ledgers = []
        for path in files:
            shard = read_json(ROOT / path)
            self.assertEqual(shard["schema_version"], 1)
            ledgers.extend(shard["ledgers"])
        self.assertEqual(len(ledgers), self.inventory["source_ledger_count"])
        self.assertEqual(len({ledger["path"] for ledger in ledgers}), len(ledgers))
        assets, jobs = [], []
        for ledger in ledgers:
            source_path = ROOT / ledger["path"]
            self.assertTrue(source_path.is_file(), str(source_path))
            source_text = source_path.read_text(encoding="utf-8")
            original_ids = {int(x) for x in re.findall(r"\\bart_image_id:\\s*(\\d+)", source_text)}
            recorded_ids = set()
            for entry in ledger["entries"]:
                self.assertTrue(entry["key"], ledger["path"])
                for output in entry["outputs"]:
                    if output["id"] is not None:
                        recorded_ids.add(output["id"])
                        self.assertEqual(output["status"], "DONE")
                        assets.append(output["id"])
                jobs.extend(entry["jobs"])
            self.assertEqual(original_ids, recorded_ids, ledger["path"])
        self.assertEqual(len(assets), len(set(assets)))
        self.assertEqual(len(jobs), len(set(jobs)))
        self.assertEqual(len(assets), self.inventory["distinct_art_image_outputs"])
        self.assertEqual(len(jobs), self.inventory["distinct_artjob_references"])
        self.assertGreater(len(assets), 600)

    def test_video_exports_and_repaired_animation_provenance(self):
        d = read_json(ROOT / self.inventory["video_builds"])
        self.assertEqual({v["id"] for v in d["videos"]}, {5, 12})
        early = next(v for v in d["videos"] if v["id"] == 5)
        later = next(v for v in d["videos"] if v["id"] == 12)
        self.assertEqual(early["status"], "historic-review-only")
        self.assertEqual(later["final_art_image_id"], 243229)
        repaired = [a for a in later["animation_revisions"]
                    if a["status"] == "accepted-after-local-repair"]
        self.assertEqual(len(repaired), 1)
        self.assertEqual(repaired[0]["clip_art_image_id"], 243216)
        self.assertTrue((ROOT / repaired[0]["replacement_repo_asset"]).is_file())

    def test_resource_submissions_are_private_and_source_attributed(self):
        data = read_json(ROOT / self.catalog["resource_submission"]["path"])
        self.assertEqual(data["status"], "prepared-not-applied")
        for category, minimum in (("characters", 9), ("rewards", 5), ("scenarios", 5)):
            entries = data[category]
            self.assertGreaterEqual(len(entries), minimum)
            self.assertEqual(len({item["key"] for item in entries}), len(entries))
            for item in entries:
                self.assertTrue((ROOT / item["source_path"]).is_file())
                self.assertEqual(item["action"], "upsert-by-verified-identity-only")
                self.assertFalse(item["payload"]["isPublic"])
                self.assertFalse(item["payload"]["isMature"])
        self.assertEqual(len(data["model_resources"]), 5)
        self.assertIn("ZERO automatic canon authority", data["legacy_canon_policy"])

    def test_repository_media_manifest_is_not_mistaken_for_live_artimages(self):
        d = read_json(ROOT / self.inventory["git_media"])
        self.assertEqual(d["schema_version"], 1)
        self.assertEqual(len(d["groups"]), 4)
        paths = [p for g in d["groups"] for p in g["paths"]]
        self.assertEqual(len(paths), len(set((g["repo"], p) for g in d["groups"] for p in g["paths"])))
        self.assertGreater(len(paths), 90)


if __name__ == "__main__":
    unittest.main()
