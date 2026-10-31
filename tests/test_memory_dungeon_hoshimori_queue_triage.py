"""Hoshimori queue-age diagnostics must not inflate delivered artwork."""
from datetime import datetime, timezone
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from memory_dungeon_hoshimori_queue_triage import annotate_queue_age  # noqa: E402


class HoshimoriQueueTriageTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 31, 12, tzinfo=timezone.utc)

    def test_pending_age_boundaries_and_stable_report(self):
        hours = (5, 6, 23, 24, 71, 72)
        jobs = []
        rows = []
        for index, hour in enumerate(hours, 1):
            from datetime import timedelta
            jobs.append({"id": index, "createdAt": (self.now - timedelta(hours=hour)).isoformat()})
            rows.append({"jobId": index, "status": "pending"})
        report = annotate_queue_age(
            {"results": rows, "delivered": 0, "pendingReview": 6}, jobs, now=self.now
        )
        self.assertEqual(
            [r["queueAgeBand"] for r in rows],
            ["under_6h", "6h_to_24h", "6h_to_24h", "1d_to_3d", "1d_to_3d", "over_3d"],
        )
        self.assertEqual(report["queueTriage"]["pendingByAge"]["over_3d"], 1)
        self.assertEqual(report["delivered"], 0)
        self.assertEqual(report["pendingReview"], 6)
        self.assertNotIn("checkedAt", report)
        self.assertNotIn("queueAgeHours", rows[0])

    def test_missing_naive_future_and_invalid_timestamps_are_unknown(self):
        jobs = [
            {"id": 1}, {"id": 2, "createdAt": "2026-10-30T08:00:00"},
            {"id": 3, "createdAt": "bad"}, {"id": 4, "createdAt": "2026-11-01T00:00:00Z"},
        ]
        rows = [{"jobId": index, "status": "pending"} for index in range(1, 5)]
        report = annotate_queue_age({"results": rows}, jobs, now=self.now)
        self.assertEqual([r["queueAgeBand"] for r in rows], ["unknown"] * 4)
        self.assertEqual(report["queueTriage"]["pendingByAge"]["unknown"], 4)

    def test_only_verified_pending_or_running_states_get_bands(self):
        jobs = [
            {"id": 1, "createdAt": "2026-10-27T12:00:00Z"},
            {"id": 2, "createdAt": "2026-10-30T12:00:00Z"},
            {"id": 3, "createdAt": "2026-10-27T12:00:00Z"},
            {"id": 4, "createdAt": "2026-10-27T12:00:00Z"},
        ]
        rows = [
            {"jobId": 1, "status": "running"},
            {"jobId": 2, "status": "done_without_art_image"},
            {"jobId": 3, "status": "job_identity_mismatch"},
            {"jobId": 4, "status": "delivered"},
        ]
        report = annotate_queue_age({"results": rows, "delivered": 1}, jobs, now=self.now)
        self.assertEqual(rows[0]["queueAgeBand"], "over_3d")
        for row in rows[1:]:
            self.assertNotIn("queueAgeBand", row)
        self.assertEqual(report["queueTriage"]["runningByAge"]["over_3d"], 1)
        self.assertEqual(report["delivered"], 1)

    def test_timezone_offset_and_naive_now(self):
        rows = [{"jobId": 1, "status": "pending"}]
        jobs = [{"id": 1, "createdAt": "2026-10-31T04:00:00-07:00"}]
        annotate_queue_age({"results": rows}, jobs, now=self.now)
        self.assertEqual(rows[0]["queueAgeBand"], "under_6h")
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            annotate_queue_age({"results": []}, [], now=datetime(2026, 10, 31))


if __name__ == "__main__":
    unittest.main()
