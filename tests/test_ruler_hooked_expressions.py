"""The expression queue must cover every canonical presenter in each mood."""
import unittest

from scripts.build_ruler_hooked_art_queue import (
    CAST_LOOK,
    assert_contract,
    expression_entries,
)


class RulerHookedExpressionQueueTests(unittest.TestCase):
    def test_all_cast_faces_are_queued_at_high_priority(self):
        cast = [{"slug": slug, "name": slug} for slug in CAST_LOOK]
        rows = expression_entries(cast)
        self.assertEqual(len(rows), 4 * (len(cast) + 1))
        self.assertEqual(len(rows), 48)
        self.assertEqual(len({row["id"] for row in rows}), 48)
        self.assertEqual(
            {
                row["id"].removeprefix("ruler-hooked-expression-steward-quill-")
                for row in rows
                if row["id"].startswith("ruler-hooked-expression-steward-quill-")
            },
            {"neutral", "pleased", "concerned", "alarmed"},
        )
        for row in rows:
            self.assertEqual(row["priority"], 1000)
            self.assertEqual(row["engine"], "krea2")
            self.assertEqual(row["size"], "768x1024")
            self.assertEqual(row["lane"], "expression")
            self.assertTrue(row["image_path"].endswith(".webp"))
            self.assertIn("psychedelic rainbow", row["prompt"])
            self.assertIn("screenprint", row["prompt"])
        assert_contract(rows)


if __name__ == "__main__":
    unittest.main()
