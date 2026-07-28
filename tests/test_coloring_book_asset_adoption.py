import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "adopt_coloring_book_asset.py"
SPEC = importlib.util.spec_from_file_location("adopt_coloring_book_asset", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ColoringBookAssetAdoptionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.original_set_dir = MODULE.production.set_dir
        MODULE.production.set_dir = lambda _book: self.root

    def tearDown(self) -> None:
        MODULE.production.set_dir = self.original_set_dir
        self.temp.cleanup()

    def test_safe_source_accepts_only_existing_set_images(self) -> None:
        image = self.root / "approved" / "legacy.webp"
        image.parent.mkdir(parents=True)
        image.write_bytes(b"image")

        relative, absolute = MODULE.safe_source(
            "monster-recast",
            "projects/coloring-book/sets/monster-recast/approved/legacy.webp",
        )

        self.assertEqual(relative, "approved/legacy.webp")
        self.assertEqual(absolute, image.resolve())

    def test_safe_source_rejects_escape_and_external_paths(self) -> None:
        for source in (
            "../legacy.webp",
            "/tmp/legacy.webp",
            "kind_robots:public/legacy.webp",
            "projects/coloring-book/sets/kind-robots/approved/legacy.webp",
            "approved/legacy.txt",
        ):
            with self.subTest(source=source):
                with self.assertRaises(RuntimeError):
                    MODULE.safe_source("monster-recast", source)

    def test_adopt_color_records_human_selected_asset_without_fake_artjob(self) -> None:
        queue_entry = {"status": "pending"}
        proposal = {"accepted": {"color": None, "bw": None}}
        queue = {"books": []}
        ledger = {"proposals": []}
        source = self.root / "approved" / "legacy.webp"

        with (
            patch.object(
                MODULE,
                "safe_source",
                return_value=("approved/legacy.webp", source),
            ),
            patch.object(MODULE.production, "mechanical_check"),
            patch.object(
                MODULE.production,
                "load_yaml",
                side_effect=[queue, ledger],
            ),
            patch.object(
                MODULE.production,
                "find_queue_entry",
                return_value=queue_entry,
            ),
            patch.object(
                MODULE.production,
                "find_proposal",
                return_value=proposal,
            ),
            patch.object(MODULE.production, "replace_ledger_pair_value") as replace,
            patch.object(MODULE.production, "write_yaml") as write,
        ):
            MODULE.adopt_color("monster-recast", "mr-001", "approved/legacy.webp")

        self.assertEqual(proposal["accepted"]["color"], "approved/legacy.webp")
        self.assertEqual(queue_entry["status"], "approved")
        self.assertEqual(
            queue_entry["rendered_path"],
            "projects/coloring-book/sets/monster-recast/approved/legacy.webp",
        )
        self.assertFalse(queue_entry["lock_seed"])
        self.assertNotIn("art_image_id", queue_entry)
        replace.assert_called_once()
        write.assert_called_once()

    def test_adopt_bw_records_review_instead_of_accepting_failed_pair(self) -> None:
        queue_entry = {"status": "approved"}
        proposal = {"accepted": {"color": "approved/color.webp", "bw": None}}
        queue = {"books": []}
        ledger = {"proposals": []}
        source = self.root / "approved" / "bw.webp"
        color = self.root / "approved" / "color.webp"
        semantic = {
            "model": "reviewer",
            "score": 42,
            "verdict": "revise",
            "reasons": ["composition changed"],
        }

        with (
            patch.object(
                MODULE,
                "safe_source",
                return_value=("approved/bw.webp", source),
            ),
            patch.object(MODULE.production, "mechanical_check"),
            patch.object(
                MODULE.production,
                "load_yaml",
                side_effect=[queue, ledger],
            ),
            patch.object(
                MODULE.production,
                "find_queue_entry",
                return_value=queue_entry,
            ),
            patch.object(
                MODULE.production,
                "find_proposal",
                return_value=proposal,
            ),
            patch.object(
                MODULE.production,
                "absolute_set_path",
                return_value=color,
            ),
            patch.object(Path, "is_file", return_value=True),
            patch.object(
                MODULE.production,
                "pair_vision",
                return_value=(False, semantic),
            ),
            patch.object(MODULE.production, "write_yaml") as write,
        ):
            adopted = MODULE.adopt_bw(
                "monster-recast",
                "mr-001",
                "approved/bw.webp",
            )

        self.assertFalse(adopted)
        self.assertIsNone(proposal["accepted"]["bw"])
        self.assertEqual(queue_entry["bw_status"], "needs_review")
        self.assertEqual(queue_entry["pair_status"], "needs_review")
        self.assertEqual(queue_entry["bw_semantic_score"], 42)
        write.assert_called_once()


if __name__ == "__main__":
    unittest.main()
