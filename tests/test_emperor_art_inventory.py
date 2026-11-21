import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.audit_emperor_art_inventory import inventory


class EmperorArtInventoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.ledgers = self.root / "ledgers"
        self.ledgers.mkdir()
        self.app = self.root / "app"
        (self.app / "utils/emperorOfDust").mkdir(parents=True)

    def ledger(self, filename, subjects):
        (self.ledgers / filename).write_text(
            yaml.safe_dump({"subjects": subjects}), encoding="utf-8")

    def subject(self, key, asset, job, image, status="DONE"):
        return {"key": key, "asset": asset, "jobs": {"house": job},
                "art": {"house": {"status": status, "art_image_id": image}}}

    def test_deduplicates_rerolls_and_flags_conflicting_images(self):
        self.ledger("a.yaml", [self.subject("a", "quests/foo", 10, 20)])
        self.ledger("b.yaml", [self.subject("b", "quests/foo", 11, 21)])
        result = inventory(self.ledgers)
        self.assertEqual(result["summary"]["unique_assets"], 1)
        self.assertEqual(result["summary"]["conflicting_image_ids"], 1)
        self.assertEqual(result["assets"][0]["job_ids"], ["10", "11"])
        self.assertIsNone(result["assets"][0]["exported"])

    def test_distinguishes_done_from_export_and_static_reference(self):
        self.ledger("a.yaml", [self.subject("a", "quests/foo", 10, 20),
                               self.subject("b", "quests/bar", 11, 21)])
        media = self.app / "public/emperor-of-dust/quests"
        media.mkdir(parents=True)
        (media / "foo.webp").write_bytes(b"RIFFfakeWEBP")
        (self.app / "utils/emperorOfDust/art.ts").write_text(
            '"/emperor-of-dust/quests/foo.webp"', encoding="utf-8")
        result = inventory(self.ledgers, self.app)
        self.assertEqual(result["summary"]["with_done_image_no_export"], 1)
        self.assertEqual(result["summary"]["exported_without_static_reference"], 0)
        self.assertTrue(result["assets"][1]["exported"])

    def test_flags_export_without_static_reference(self):
        self.ledger("a.yaml", [self.subject("a", "rooms/a", 10, 20)])
        media = self.app / "public/emperor-of-dust/rooms"
        media.mkdir(parents=True)
        (media / "a.webp").write_bytes(b"RIFFfakeWEBP")
        self.assertEqual(inventory(self.ledgers, self.app)["summary"]
                         ["exported_without_static_reference"], 1)

    def test_non_webp_file_is_not_an_export(self):
        self.ledger("a.yaml", [self.subject("a", "rooms/a", 10, 20)])
        media = self.app / "public/emperor-of-dust/rooms"
        media.mkdir(parents=True)
        (media / "a.webp").write_bytes(b"<html>not an image</html>")
        report = inventory(self.ledgers, self.app)
        self.assertFalse(report["assets"][0]["exported"])
        self.assertEqual(report["summary"]["with_done_image_no_export"], 1)

    def test_ignores_files_unrelated_to_emperor(self):
        self.ledger("a.yaml", [self.subject("a", "rooms/a", 10, 20)])
        media = self.app / "public/emperor-of-dust/rooms"
        media.mkdir(parents=True)
        (media / "a.webp").write_bytes(b"RIFF\x00\x00\x00\x00WEBP")
        (self.app / "pages").mkdir()
        (self.app / "pages/other.vue").write_text('"rooms/a"', encoding="utf-8")
        report = inventory(self.ledgers, self.app)
        self.assertEqual(report["summary"]["exported_without_static_reference"], 1)

    def test_missing_jobs_not_counted_as_done(self):
        self.ledger("a.yaml", [{"key": "new", "asset": "endings/new"}])
        report = inventory(self.ledgers)
        self.assertEqual(report["summary"]["without_done_image"], 1)
        self.assertEqual(report["assets"][0]["render_records"][0]["status"], "NOT_SUBMITTED")

    def test_rejects_path_traversal(self):
        self.ledger("a.yaml", [{"key": "bad", "asset": "../secret"}])
        with self.assertRaises(ValueError):
            inventory(self.ledgers, self.app)


if __name__ == "__main__":
    unittest.main()
