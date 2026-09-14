import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "coloring_proposal_status.py"
SPEC = importlib.util.spec_from_file_location("coloring_proposal_status", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def _queue_doc(status: str) -> dict:
    entries = [
        {
            "slot": slot,
            "id": f"x-{slot:03d}",
            "status": "pending",
            "image_path": f"generated/x-{slot:03d}.webp",
            "source_ref": "example-book.yaml#x",
        }
        for slot in range(1, 37)
    ]
    # Give the first entry the status under test.
    entries[0]["status"] = status
    return {
        "batch_policy": {"worker_pass_size": 18},
        "books": [{"slug": "example-book", "entries": entries}],
    }


class ColoringProposalStatusQueueTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.original_path = MODULE.COLOR_QUEUE_PATH

    def tearDown(self) -> None:
        MODULE.COLOR_QUEUE_PATH = self.original_path
        self.temp.cleanup()

    def _write_and_load(self, status: str):
        path = self.root / "color-art-jobs.yaml"
        with path.open("w", encoding="utf-8") as handle:
            MODULE.yaml.safe_dump(_queue_doc(status), handle)
        MODULE.COLOR_QUEUE_PATH = path
        return MODULE.load_color_queue()

    def test_needs_review_is_a_recognized_queue_status(self) -> None:
        # consume_coloring_book_color_art.py's bounded-retry policy legitimately
        # sets a queue entry to "needs_review" once render_attempts is exhausted
        # (see coloring-book/t-022 cycle 7, mr-008) -- the status reporter must
        # not flag that as a structural error.
        errors, by_id, by_book = self._write_and_load("needs_review")

        status_errors = [e for e in errors if "invalid color queue status" in e]
        self.assertEqual(status_errors, [])
        self.assertEqual(by_book["example-book"]["needs_review"], 1)
        self.assertEqual(by_id["x-001"]["status"], "needs_review")

    def test_unknown_status_is_still_flagged(self) -> None:
        errors, _by_id, _by_book = self._write_and_load("bogus_status")

        self.assertTrue(
            any("invalid color queue status" in error for error in errors),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
