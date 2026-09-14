import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "manage_coloring_book_production.py"
SPEC = importlib.util.spec_from_file_location("manage_coloring_book_production", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ColoringBookProductionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.ledger = self.root / "proposals.yaml"
        self.original_ledger_path = MODULE.ledger_path
        MODULE.ledger_path = lambda _book: self.ledger

    def tearDown(self) -> None:
        MODULE.ledger_path = self.original_ledger_path
        self.temp.cleanup()

    def test_replace_inline_pair_value_preserves_neighboring_proposals(self) -> None:
        self.ledger.write_text(
            """proposals:
- slot: 1
  id: mr-001
  accepted: {color: null, bw: null}
  final: {color: null, bw: null}
  notes: []
- slot: 2
  id: mr-002
  accepted: {color: old.webp, bw: null}
  final: {color: null, bw: null}
  notes: []
""",
            encoding="utf-8",
        )

        MODULE.replace_ledger_pair_value(
            "monster-recast",
            "mr-002",
            "accepted",
            "bw",
            "generated/bw/mr-002-bw.webp",
        )

        content = self.ledger.read_text(encoding="utf-8")
        self.assertIn(
            'accepted: {color: old.webp, bw: "generated/bw/mr-002-bw.webp"}',
            content,
        )
        self.assertIn("id: mr-001\n  accepted: {color: null, bw: null}", content)

    def test_replace_block_pair_value(self) -> None:
        self.ledger.write_text(
            """proposals:
- slot: 1
  id: kr-001
  accepted:
    color: null
    bw: null
  final:
    color: null
    bw: null
  notes: []
""",
            encoding="utf-8",
        )

        MODULE.replace_ledger_pair_value(
            "kind-robots",
            "kr-001",
            "final",
            "color",
            "generated/color/kr-001.webp",
        )

        content = self.ledger.read_text(encoding="utf-8")
        self.assertIn('    color: "generated/color/kr-001.webp"', content)
        self.assertIn("    bw: null", content)

    def test_finalize_pair_sets_semantic_score_from_queue_entry(self) -> None:
        # Regression test for a NameError that made every live finalize-pair call
        # crash (`semantic` was never defined in finalize_pair — a leftover
        # reference from consume_coloring_book_studio_request.py's local
        # `semantic` variable of the same name). The pair's semantic score is
        # recorded on the BW queue entry as `bw_semantic_score`, so finalize_pair
        # should read it from there instead of an undefined name.
        self.ledger.write_text(
            """proposals:
- slot: 1
  id: mr-002
  accepted: {color: color.webp, bw: bw.webp}
  final: {color: null, bw: null}
  notes: []
""",
            encoding="utf-8",
        )
        color = self.root / "color.webp"
        bw = self.root / "bw.webp"
        color.write_bytes(b"color-bytes")
        bw.write_bytes(b"bw-bytes")

        original_absolute_set_path = MODULE.absolute_set_path
        original_mechanical_check = MODULE.mechanical_check
        original_write_yaml = MODULE.write_yaml
        MODULE.absolute_set_path = (
            lambda _book, value: color if "color" in value else bw
        )
        MODULE.mechanical_check = lambda _path, _variant: None
        MODULE.write_yaml = lambda _path, _data: None
        try:
            queue_entry = {"id": "mr-002", "bw_semantic_score": 91}
            queue = {"books": [{"slug": "monster-recast", "entries": [queue_entry]}]}
            ledger = {
                "proposals": [
                    {
                        "id": "mr-002",
                        "accepted": {"color": "color.webp", "bw": "bw.webp"},
                        "final": {"color": None, "bw": None},
                    }
                ]
            }

            MODULE.finalize_pair("monster-recast", "mr-002", queue, ledger)
        finally:
            MODULE.absolute_set_path = original_absolute_set_path
            MODULE.mechanical_check = original_mechanical_check
            MODULE.write_yaml = original_write_yaml

        self.assertEqual(queue_entry["pair_status"], "final")
        self.assertEqual(queue_entry["pair_semantic_score"], 91)
        content = self.ledger.read_text(encoding="utf-8")
        self.assertIn('final: {color: "color.webp", bw: "bw.webp"}', content)

    def test_relative_to_set_normalizes_repo_paths(self) -> None:
        self.assertEqual(
            MODULE.relative_to_set(
                "kind-robots",
                "projects/coloring-book/sets/kind-robots/generated/bw/kr-001-bw.webp",
            ),
            "generated/bw/kr-001-bw.webp",
        )

    def test_mechanical_check_surfaces_pillow_fix_when_pil_unavailable(self) -> None:
        original_assess_file = MODULE.art_quality.assess_file
        MODULE.art_quality.assess_file = (
            lambda _path, _variant: (None, ["PIL unavailable — image guard skipped"], {})
        )
        try:
            with self.assertRaises(RuntimeError) as ctx:
                MODULE.mechanical_check(self.root / "candidate.webp", "bw")
        finally:
            MODULE.art_quality.assess_file = original_assess_file

        message = str(ctx.exception)
        self.assertIn("PIL unavailable", message)
        self.assertIn("pip3 install Pillow", message)
        self.assertIn("provision_kind_robots_deps.sh", message)

    def test_mechanical_check_still_raises_plain_reason_when_not_pil(self) -> None:
        original_assess_file = MODULE.art_quality.assess_file
        MODULE.art_quality.assess_file = (
            lambda _path, _variant: (None, ["image quality gate unavailable"], {})
        )
        try:
            with self.assertRaises(RuntimeError) as ctx:
                MODULE.mechanical_check(self.root / "candidate.webp", "bw")
        finally:
            MODULE.art_quality.assess_file = original_assess_file

        message = str(ctx.exception)
        self.assertEqual(message, "image quality gate unavailable")
        self.assertNotIn("pip3 install Pillow", message)

    def test_save_image_surfaces_pillow_fix_when_pil_unavailable(self) -> None:
        import builtins

        real_import = builtins.__import__

        def fake_import(name, *args, **kwargs):
            if name == "PIL" or name.startswith("PIL."):
                raise ImportError("No module named 'PIL'")
            return real_import(name, *args, **kwargs)

        image_b64 = MODULE.base64.b64encode(b"not-a-real-image").decode()
        target = self.root / "candidate.webp"

        builtins.__import__ = fake_import
        try:
            with self.assertRaises(RuntimeError) as ctx:
                MODULE.save_image(target, image_b64)
        finally:
            builtins.__import__ = real_import

        message = str(ctx.exception)
        self.assertIn("Pillow is required for WebP output", message)
        self.assertIn("pip3 install Pillow", message)
        self.assertIn("provision_kind_robots_deps.sh", message)


if __name__ == "__main__":
    unittest.main()
