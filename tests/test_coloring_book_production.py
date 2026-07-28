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

    def test_relative_to_set_normalizes_repo_paths(self) -> None:
        self.assertEqual(
            MODULE.relative_to_set(
                "kind-robots",
                "projects/coloring-book/sets/kind-robots/generated/bw/kr-001-bw.webp",
            ),
            "generated/bw/kr-001-bw.webp",
        )


if __name__ == "__main__":
    unittest.main()
