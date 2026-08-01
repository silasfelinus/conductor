import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "manage_coloring_book_cover.py"
SPEC = importlib.util.spec_from_file_location("manage_coloring_book_cover", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ColoringBookCoverTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.original_set_dir = MODULE.set_dir
        MODULE.set_dir = lambda book: self.root / book

    def tearDown(self) -> None:
        MODULE.set_dir = self.original_set_dir
        self.temp.cleanup()

    def write_ledger(self, book: str, cover_text: str) -> Path:
        path = self.root / book / "proposals.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"""schema_version: 2
book:
  slug: {book}
cover:
{cover_text}proposals:
- slot: 1
  id: example-001
""",
            encoding="utf-8",
        )
        return path

    def test_queue_has_three_complete_cover_prompts(self) -> None:
        queue = yaml.safe_load(MODULE.QUEUE_FILE.read_text(encoding="utf-8"))
        covers = queue["covers"]
        self.assertEqual(
            [cover["book_slug"] for cover in covers],
            ["monster-recast", "hollywood-recast", "kind-robots"],
        )
        for cover in covers:
            with self.subTest(book=cover["book_slug"]):
                self.assertGreater(len(MODULE.clean(cover["prompt"])), 200)
                self.assertTrue(str(cover["image_path"]).endswith("-cover.webp"))
                self.assertEqual(cover["status"], "pending")

    def test_replace_inline_cover_pair_value(self) -> None:
        path = self.write_ledger(
            "monster-recast",
            "  prompt: {text: null, ref: null}\n"
            "  inspirations: []\n"
            "  accepted: {color: null, bw: null}\n"
            "  final: {color: null, bw: null}\n"
            "  notes: []\n",
        )
        MODULE.replace_ledger_cover_value(
            "monster-recast",
            "accepted",
            "generated/cover/monster-recast-cover.webp",
        )
        content = path.read_text(encoding="utf-8")
        self.assertIn(
            'accepted: {color: "generated/cover/monster-recast-cover.webp", bw: null}',
            content,
        )
        self.assertIn("final: {color: null, bw: null}", content)

    def test_replace_block_cover_pair_value(self) -> None:
        path = self.write_ledger(
            "kind-robots",
            "  prompt:\n"
            "    text: null\n"
            "    ref: null\n"
            "  inspirations: []\n"
            "  accepted:\n"
            "    color: null\n"
            "    bw: null\n"
            "  final:\n"
            "    color: null\n"
            "    bw: null\n"
            "  notes: []\n",
        )
        MODULE.replace_ledger_cover_value(
            "kind-robots",
            "final",
            "approved/kind-robots-cover.webp",
        )
        content = path.read_text(encoding="utf-8")
        self.assertIn('    color: "approved/kind-robots-cover.webp"', content)
        self.assertIn("    bw: null", content)

    def test_safe_source_rejects_cross_set_and_traversal(self) -> None:
        for value in (
            "../cover.webp",
            "/tmp/cover.webp",
            "projects/coloring-book/sets/kind-robots/approved/cover.webp",
            "approved/cover.txt",
        ):
            with self.subTest(value=value):
                with self.assertRaises(RuntimeError):
                    MODULE.safe_source("monster-recast", value)

    def test_accept_cover_promotes_exact_reviewed_path(self) -> None:
        queue = {
            "covers": [
                {
                    "book_slug": "kind-robots",
                    "prompt": "A sufficiently detailed cover prompt for semantic review.",
                    "status": "done",
                    "rendered_path": "projects/coloring-book/sets/kind-robots/generated/cover/kind-robots-cover.webp",
                }
            ]
        }
        path = self.root / "kind-robots" / "generated" / "cover" / "kind-robots-cover.webp"
        path.parent.mkdir(parents=True)
        path.write_bytes(b"image")
        with (
            patch.object(MODULE, "load_yaml", return_value=queue),
            patch.object(MODULE, "mechanical", return_value=(True, [], {})),
            patch.object(MODULE, "replace_ledger_cover_value") as replace,
            patch.object(MODULE, "write_queue") as write,
        ):
            accepted = MODULE.accept_cover("kind-robots")

        self.assertTrue(accepted)
        cover = queue["covers"][0]
        self.assertEqual(cover["status"], "approved")
        self.assertEqual(
            cover["accepted_path"],
            "generated/cover/kind-robots-cover.webp",
        )
        replace.assert_called_once_with(
            "kind-robots",
            "accepted",
            "generated/cover/kind-robots-cover.webp",
        )
        write.assert_called_once()

    def test_accept_consults_no_model(self) -> None:
        """A human ran `--accept`. Nothing may re-litigate that decision."""
        self.assertFalse(
            hasattr(MODULE, "semantic"),
            "the vision gate must not come back -- cover quality is a human call",
        )

    def test_mechanical_failure_still_blocks_acceptance(self) -> None:
        queue = {
            "covers": [
                {
                    "book_slug": "kind-robots",
                    "prompt": "A sufficiently detailed cover prompt.",
                    "status": "done",
                    "rendered_path": "projects/coloring-book/sets/kind-robots/generated/cover/kind-robots-cover.webp",
                }
            ]
        }
        path = self.root / "kind-robots" / "generated" / "cover" / "kind-robots-cover.webp"
        path.parent.mkdir(parents=True)
        path.write_bytes(b"image")

        with (
            patch.object(MODULE, "load_yaml", return_value=queue),
            patch.object(MODULE, "mechanical", return_value=(False, ["blank frame"], {})),
            patch.object(MODULE, "replace_ledger_cover_value") as replace,
            patch.object(MODULE, "write_queue") as write,
        ):
            accepted = MODULE.accept_cover("kind-robots")

        self.assertFalse(accepted)
        self.assertEqual(queue["covers"][0]["status"], "needs_review")
        self.assertNotIn("accepted_path", queue["covers"][0])
        replace.assert_not_called()
        write.assert_called_once()
