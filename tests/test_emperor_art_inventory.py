import json
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

    def test_prefix_asset_is_not_mistaken_for_longer_path(self):
        self.ledger("a.yaml", [self.subject("short", "rooms/a", 10, 20),
                               self.subject("long", "rooms/ab", 11, 21)])
        (self.app / "utils/emperorOfDust/rooms.ts").write_text(
            'const image = "/emperor-of-dust/rooms/ab.webp"', encoding="utf-8")
        report = inventory(self.ledgers, self.app)
        by_asset = {entry["asset"]: entry for entry in report["assets"]}
        self.assertEqual(by_asset["rooms/a"]["reference_files"], [])
        self.assertEqual(by_asset["rooms/ab"]["reference_class"], "static")

    def test_dynamic_chance_builder_is_candidate_not_static_reference(self):
        self.ledger("a.yaml", [self.subject("choice", "chance-events/rain/collect", 10, 20)])
        source = self.app / "utils/emperorOfDust/fortress"
        source.mkdir(parents=True)
        (source / "chanceArt.ts").write_text(
            'export function chanceArtCandidates(eventId, choiceId) { '
            'return emperorMediaArtUrl(`chance-events/${eventId}/${choiceId}`) }',
            encoding="utf-8")
        media = self.app / "public/emperor-of-dust/chance-events/rain"
        media.mkdir(parents=True)
        (media / "collect.webp").write_bytes(b"RIFF\x00\x00\x00\x00WEBP")
        report = inventory(self.ledgers, self.app)
        asset = report["assets"][0]
        self.assertEqual(asset["reference_class"], "runtime_candidate")
        self.assertEqual(asset["reference_files"], [])
        self.assertEqual(report["summary"]["exported_runtime_candidates"], 1)
        self.assertEqual(report["summary"]["exported_without_known_reference"], 0)

    def test_missing_builder_does_not_imply_runtime_reference(self):
        self.ledger("a.yaml", [self.subject("choice", "chance-events/rain/collect", 10, 20)])
        report = inventory(self.ledgers, self.app)
        self.assertEqual(report["assets"][0]["reference_class"], "unreferenced")

    def test_partial_builder_symbol_does_not_count_as_runtime_reference(self):
        self.ledger("a.yaml", [self.subject("choice", "chance-events/rain/collect", 10, 20)])
        source = self.app / "utils/emperorOfDust/fortress"
        source.mkdir(parents=True)
        (source / "chanceArt.ts").write_text("const chanceArtCandidatesExtra = true", encoding="utf-8")
        report = inventory(self.ledgers, self.app)
        self.assertEqual(report["assets"][0]["reference_class"], "unreferenced")

    def manifest(self, runtime, static=()):
        path = self.root / "editorial-art-runtime-paths.json"
        path.write_text(json.dumps({
            "version": 1,
            "runtime_asset_paths": list(runtime),
            "static_asset_paths": list(static),
        }), encoding="utf-8")
        return path

    def test_exact_builder_path_promotes_without_lying_about_delivery(self):
        self.ledger("a.yaml", [
            self.subject("hit", "chance-events/rain/collect", 10, 20),
            self.subject("miss", "chance-events/rain/refuse", 11, 21),
        ])
        media = self.app / "public/emperor-of-dust/chance-events/rain"
        media.mkdir(parents=True)
        (media / "collect.webp").write_bytes(b"RIFF\x00\x00\x00\x00WEBP")
        manifest = self.manifest(["chance-events/rain/collect"])
        report = inventory(self.ledgers, self.app, manifest)
        by_asset = {row["asset"]: row for row in report["assets"]}
        hit = by_asset["chance-events/rain/collect"]
        self.assertEqual(hit["reference_class"], "builder_reachable")
        self.assertTrue(hit["exported"])
        self.assertFalse(by_asset["chance-events/rain/refuse"]["exported"])
        self.assertEqual(by_asset["chance-events/rain/refuse"]
                         ["reference_class"], "unreferenced")
        self.assertEqual(report["summary"]["exported_builder_reachable"], 1)
        self.assertTrue(report["summary"]["runtime_manifest_available"])

    def test_reachable_unexported_done_art_stays_unshipped(self):
        self.ledger("a.yaml", [
            self.subject("ending", "endings/bell-restored", 68220, 270430),
        ])
        report = inventory(
            self.ledgers, self.app,
            self.manifest(["endings/bell-restored"]),
        )
        self.assertEqual(report["assets"][0]["reference_class"],
                         "builder_reachable")
        self.assertFalse(report["assets"][0]["exported"])
        self.assertEqual(report["summary"]["with_done_image_no_export"], 1)
        self.assertEqual(report["summary"]
                         ["done_builder_reachable_without_export"], 1)

    def test_manifest_is_exact_not_prefix_or_regex(self):
        self.ledger("a.yaml", [
            self.subject("a", "rooms/a", 10, 20),
            self.subject("ab", "rooms/ab", 11, 21),
        ])
        report = inventory(self.ledgers, self.app,
                           self.manifest([], ["rooms/ab"]))
        by_asset = {row["asset"]: row for row in report["assets"]}
        self.assertEqual(by_asset["rooms/a"]["reference_class"], "unreferenced")
        self.assertEqual(by_asset["rooms/ab"]["reference_class"],
                         "builder_reachable")

    def test_exact_manifest_suppresses_unproven_builder_heuristic(self):
        self.ledger("a.yaml", [
            self.subject("unused", "chance-events/rain/unknown", 10, 20),
        ])
        builder = self.app / "utils/emperorOfDust/fortress/chanceArt.ts"
        builder.parent.mkdir(parents=True, exist_ok=True)
        builder.write_text(
            "function chanceArtCandidates(eventId, choiceId) {}",
            encoding="utf-8",
        )
        report = inventory(
            self.ledgers, self.app,
            self.manifest(["chance-events/rain/collect"]),
        )
        self.assertEqual(
            report["assets"][0]["runtime_reference_candidates"],
            ["utils/emperorOfDust/fortress/chanceArt.ts"],
        )
        self.assertEqual(
            report["assets"][0]["reference_class"], "unreferenced",
        )

    def test_invalid_runtime_manifest_fails_closed(self):
        self.ledger("a.yaml", [self.subject("a", "rooms/a", 10, 20)])
        malformed = self.manifest(["../../secret"])
        with self.assertRaises(ValueError):
            inventory(self.ledgers, self.app, malformed)

    def test_rejects_path_traversal(self):
        self.ledger("a.yaml", [{"key": "bad", "asset": "../secret"}])
        with self.assertRaises(ValueError):
            inventory(self.ledgers, self.app)


if __name__ == "__main__":
    unittest.main()


def test_cast_assets_resolve_under_cast_folder():
    """2026-11-21: followers/ and npcs/ ledger assets ship under public/emperor-of-dust/cast/."""
    from scripts.audit_emperor_art_inventory import media_path

    assert media_path("followers/F001/portrait/neutral") == (
        "public/emperor-of-dust/cast/followers/F001/portrait/neutral.webp")
    assert media_path("npcs/aldous-hopper/illustrated/neutral") == (
        "public/emperor-of-dust/cast/npcs/aldous-hopper/illustrated/neutral.webp")
    assert media_path("endings/long-night") == "public/emperor-of-dust/endings/long-night.webp"
