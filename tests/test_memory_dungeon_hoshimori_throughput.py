"""Adversarial tests for read-only DONE-update throughput evidence."""
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_memory_dungeon_hoshimori_throughput import (  # noqa: E402
    analyze_throughput, fetch_recent_done,
)

NOW = datetime(2026, 10, 31, 20, tzinfo=timezone.utc)


def done(job_id, age_hours, engine="COMFY", *, status="DONE"):
    return {
        "id": job_id, "status": status, "engine": engine,
        "updatedAt": (NOW - timedelta(hours=age_hours)).isoformat(),
    }


def page(rows, *, total=None, page_no=1, next_page=False):
    return {"jobs": rows, "pagination": {
        "page": page_no, "pageSize": 200,
        "totalCount": len(rows) if total is None else total,
        "hasNextPage": next_page,
    }}


def stats(**overrides):
    result = {
        "windowHours": 24,
        "staleRunningCount": 1,
        "imagesCreatedInWindow": 17,
        "latestDoneAt": (NOW - timedelta(minutes=30)).isoformat(),
        "imagesByServer": [{"serverName": "Comfy", "count": 7}],
    }
    result.update(overrides)
    return result


class HoshimoriThroughputTests(unittest.TestCase):
    def test_recent_done_is_not_confused_with_art_image_delivery(self):
        rows = [done(4, .5), done(3, 3), done(2, 23, "A1111"), done(1, 25)]
        snapshot = fetch_recent_done(lambda _: page(rows), now=NOW)
        report = analyze_throughput(stats(), snapshot, now=NOW)
        self.assertTrue(report["exact_window_inventory"])
        self.assertEqual(report["done_rows_updated_in_window"],
                         {"1h": 1, "6h": 2, "24h": 3})
        self.assertEqual(report["comfy_done_rows_updated_in_window"],
                         {"1h": 1, "6h": 2, "24h": 2})
        self.assertEqual(report["art_images_created_in_24h_all_sources"], 17)
        self.assertEqual(report["stale_running_count"], 1)
        self.assertIn("not an exact render-completion", report["interpretation"])

    def test_no_done_rows_means_no_proven_recent_activity(self):
        snapshot = fetch_recent_done(lambda _: page([]), now=NOW)
        report = analyze_throughput(stats(latestDoneAt=None), snapshot, now=NOW)
        self.assertEqual(report["done_rows_updated_in_window"]["24h"], 0)
        self.assertIsNone(report["latest_done_updated_at"])
        self.assertTrue(report["exact_window_inventory"])

    def test_multi_page_window_is_exact_only_when_older_row_found(self):
        first = [done(i, 1) for i in range(400, 200, -1)]
        second = [done(200, 26)]
        snapshot = fetch_recent_done(
            lambda p: page(first, total=201, next_page=True) if p == 1
            else page(second, total=201, page_no=2),
            now=NOW,
        )
        self.assertEqual(snapshot["sampled"], 201)
        self.assertEqual(len(snapshot["jobs"]), 200)
        self.assertTrue(snapshot["complete_window"])

    def test_bounded_pages_never_pretend_to_be_exhaustive(self):
        first = [done(i, 1) for i in range(400, 200, -1)]
        snapshot = fetch_recent_done(
            lambda _: page(first, total=400, next_page=True),
            now=NOW, max_pages=1,
        )
        self.assertFalse(snapshot["complete_window"])
        self.assertEqual(snapshot["sampled"], 200)
        report = analyze_throughput(stats(), snapshot, now=NOW)
        self.assertIn("lower bounds", report["interpretation"])

    def test_duplicate_or_out_of_order_done_rows_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            fetch_recent_done(lambda _: page([done(3, 1), done(3, 1)]), now=NOW)
        with self.assertRaisesRegex(ValueError, "ordering"):
            fetch_recent_done(lambda _: page([done(2, 2), done(3, 1)]), now=NOW)

    def test_missing_or_future_timestamps_fail_closed(self):
        missing = done(3, 1)
        del missing["updatedAt"]
        with self.assertRaisesRegex(ValueError, "timestamp"):
            fetch_recent_done(lambda _: page([missing]), now=NOW)
        with self.assertRaisesRegex(ValueError, "future"):
            fetch_recent_done(lambda _: page([done(3, -2)]), now=NOW)

    def test_page_drift_or_missing_page_cannot_be_reported_as_throughput(self):
        first = [done(i, 1) for i in range(400, 200, -1)]
        with self.assertRaisesRegex(RuntimeError, "page 2 unavailable"):
            fetch_recent_done(
                lambda p: page(first, total=201, next_page=True) if p == 1 else None,
                now=NOW,
            )
        with self.assertRaisesRegex(ValueError, "pagination changed"):
            fetch_recent_done(
                lambda p: page(first, total=201, next_page=True) if p == 1
                else page([done(200, 26)], total=202, page_no=2),
                now=NOW,
            )

    def test_full_stats_required_not_summary_stub(self):
        snapshot = {"jobs": [], "sampled": 0, "complete_window": True}
        with self.assertRaisesRegex(ValueError, "full 24-hour"):
            analyze_throughput(stats(windowHours=6), snapshot, now=NOW)
        with self.assertRaisesRegex(ValueError, "staleRunningCount"):
            analyze_throughput(stats(staleRunningCount=None), snapshot, now=NOW)
        with self.assertRaisesRegex(ValueError, "latest DONE"):
            analyze_throughput(stats(latestDoneAt="not-a-date"), snapshot, now=NOW)


if __name__ == "__main__":
    unittest.main()
