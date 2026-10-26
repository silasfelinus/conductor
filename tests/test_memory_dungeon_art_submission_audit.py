"""Regression tests for uncapped, auditable Memory Dungeon ArtJob handoff."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.audit_memory_dungeon_art_submission import positive_job_id, summarize


class MemoryArtSubmissionAuditTests(unittest.TestCase):
    def test_positive_ids_only(self):
        for value in (None, "", 0, "0", -1, "no"):
            self.assertFalse(positive_job_id(value))
        self.assertTrue(positive_job_id("45670"))

    def test_counts_all_rows_without_pagination_or_a_150_job_cap(self):
        with TemporaryDirectory() as d:
            root = Path(d)
            first = root / "first.yaml"
            second = root / "second.yaml"
            def ledger(start, count, recorded):
                rows = []
                for i in range(start, start + count):
                    rows.append(f"- id: memory-dungeon-saturate-{i}\n  status: pending\n" +
                                (f"  last_art_job_id: {i + 40000}\n" if i < start + recorded else ""))
                return "requests:\n" + "".join(rows)
            first.write_text(ledger(0, 227, 227))
            second.write_text(ledger(227, 525, 525))
            report = summarize((first, second))
            self.assertEqual(report["total"], 752)
            self.assertEqual(report["submitted"], 752)
            self.assertEqual(report["unresolved"], [])
            self.assertEqual(report["duplicate_ids"], [])

    def test_partial_submission_exposes_missing_jobs(self):
        with TemporaryDirectory() as d:
            path = Path(d) / "one.yaml"
            path.write_text("""requests:
- id: memory-dungeon-saturate-one
  status: pending
  last_art_job_id: 45800
- id: memory-dungeon-saturate-two
  status: pending
- id: memory-dungeon-saturate-three
  status: done
- id: unrelated-project
  status: pending
""")
            report = summarize((path,))
            self.assertEqual(report["total"], 3)
            self.assertEqual(report["submitted"], 1)
            self.assertEqual(report["satisfied_without_job"], 1)
            self.assertEqual(report["unresolved"], ["memory-dungeon-saturate-two"])

    def test_duplicate_request_ids_cannot_pass(self):
        with TemporaryDirectory() as d:
            path = Path(d) / "one.yaml"
            path.write_text("""requests:
- id: memory-dungeon-saturate-one
  last_art_job_id: 123
- id: memory-dungeon-saturate-one
  last_art_job_id: 124
""")
            report = summarize((path,))
            self.assertEqual(report["duplicate_ids"], ["memory-dungeon-saturate-one"])


if __name__ == "__main__":
    unittest.main()
