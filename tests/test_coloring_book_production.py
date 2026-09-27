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
        self.original_queue_lock_file = MODULE.QUEUE_LOCK_FILE
        MODULE.QUEUE_LOCK_FILE = self.root / "color-art-jobs.yaml.lock"

    def tearDown(self) -> None:
        MODULE.ledger_path = self.original_ledger_path
        MODULE.QUEUE_LOCK_FILE = self.original_queue_lock_file
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
        original_write_queue_entry = MODULE.write_queue_entry
        MODULE.absolute_set_path = (
            lambda _book, value: color if "color" in value else bw
        )
        MODULE.mechanical_check = lambda _path, _variant: None
        MODULE.write_queue_entry = lambda _book, _proposal_id, _entry: None
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
            MODULE.write_queue_entry = original_write_queue_entry

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

    def test_queue_lock_refuses_concurrent_acquisition(self) -> None:
        # Regression test for coloring-book/t-049: two invocations racing against
        # the same QUEUE_FILE must not both proceed and silently clobber each
        # other's writes. The second acquisition attempt must fail fast rather
        # than block or succeed.
        with MODULE.queue_lock():
            self.assertTrue(MODULE.QUEUE_LOCK_FILE.exists())
            with self.assertRaises(RuntimeError) as ctx:
                with MODULE.queue_lock():
                    pass
        self.assertIn("already held", str(ctx.exception))

    def test_queue_lock_releases_on_exit_and_on_exception(self) -> None:
        with MODULE.queue_lock():
            pass
        # Lock released cleanly -- a fresh acquisition must succeed.
        with MODULE.queue_lock():
            pass

        with self.assertRaises(ValueError):
            with MODULE.queue_lock():
                raise ValueError("boom")
        # Lock released even though the body raised -- a fresh acquisition
        # must still succeed rather than staying held forever.
        with MODULE.queue_lock():
            pass

    def test_write_queue_entry_preserves_other_entries_byte_for_byte(self) -> None:
        # Regression test for coloring-book/t-052: write_queue_entry must
        # text-splice only the touched book/entry, leaving every other
        # book/entry -- including a sibling in the same book with its own
        # nested revision-history list, and an entry in an entirely
        # different book -- byte-for-byte untouched, instead of
        # re-serializing the whole in-memory queue tree the way
        # write_yaml(QUEUE_FILE, queue) used to.
        queue_file = self.root / "color-art-jobs.yaml"
        queue_file.write_text(
            """schema_version: 1
books:
- order: 1
  slug: monster-recast
  title: Monster Recast
  entries:
  - slot: 1
    id: mr-001
    status: done
    bw_revision_history:
    - requested_at: '2026-09-14T05:36:10Z'
      previous_status: done
      archived_path: null
  - slot: 2
    id: mr-002
    status: pending
- order: 2
  slug: kind-robots
  title: Kind Robots
  entries:
  - slot: 1
    id: kr-001
    status: done
""",
            encoding="utf-8",
        )
        original_queue_file = MODULE.QUEUE_FILE
        MODULE.QUEUE_FILE = queue_file
        try:
            before = queue_file.read_text(encoding="utf-8")
            mr001_block_before = before[before.index("  - slot: 1") : before.index("  - slot: 2")]
            book2_block_before = before[before.index("- order: 2") :]

            MODULE.write_queue_entry(
                "monster-recast",
                "mr-002",
                {
                    "slot": 2,
                    "id": "mr-002",
                    "status": "approved",
                    "approved_at": "2026-09-27T00:00:00Z",
                },
            )

            after = queue_file.read_text(encoding="utf-8")
        finally:
            MODULE.QUEUE_FILE = original_queue_file

        # The touched entry actually changed.
        self.assertIn("status: approved", after)
        self.assertIn("approved_at: '2026-09-27T00:00:00Z'", after)

        # Every other entry -- a sibling in the same book (with its own
        # nested list) and an entry in a different book -- is untouched.
        self.assertIn(mr001_block_before, after)
        self.assertIn(book2_block_before, after)

        parsed = MODULE.yaml.safe_load(after)
        self.assertEqual(parsed["books"][0]["entries"][1]["status"], "approved")
        self.assertEqual(parsed["books"][0]["entries"][0]["id"], "mr-001")
        self.assertEqual(parsed["books"][1]["slug"], "kind-robots")

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
