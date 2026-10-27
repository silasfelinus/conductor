"""Read-only Memory Dungeon ArtJob receipt and delivery proof regressions."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_memory_dungeon_art_delivery import (  # noqa: E402
    EXPECTED,
    assess_media_headers,
    audit_jobs,
    job_identity,
    load_receipts,
    valid_destination,
)


def receipt(key="memory-dungeon-saturate-test", job_id=45570,
            path="public/images/memory-dungeon/test.webp"):
    return {"id": key, "jobId": job_id, "imagePath": path}


def job(row, status="DONE", art_image_id=3001, path=None, request_id=None):
    return {
        "id": row["jobId"],
        "status": status,
        "createdAt": "2026-10-26T01:00:00.500Z",
        "artImageId": art_image_id,
        "payload": {"conductorRequest": {
            "id": request_id or row["id"],
            "targetRepo": "silasfelinus/kind_robots",
            "imagePath": path or row["imagePath"],
        }},
    }


class MemoryDungeonDeliveryAuditTests(unittest.TestCase):
    def test_all_752_accepted_jobs_survive_live_queue_drain(self):
        rows = load_receipts()
        self.assertEqual(len(rows), EXPECTED)
        self.assertEqual(len({r["id"] for r in rows}), EXPECTED)
        self.assertEqual(len({r["jobId"] for r in rows}), EXPECTED)
        self.assertEqual(len({r["imagePath"] for r in rows}), EXPECTED)
        self.assertEqual(len([r for r in rows if r["jobId"] <= 0]), 0)

    def test_rejects_unsafe_paths_and_incomplete_manifest(self):
        self.assertTrue(valid_destination("public/images/memory-dungeon/a.webp"))
        for bad in (
            "public/images/other/a.webp",
            "public/images/memory-dungeon/../secret.webp",
            "public/images/memory-dungeon/a?url=secret.webp",
            "public/images/memory-dungeon/a\\b.webp",
            "public/images/memory-dungeon/a.txt",
        ):
            self.assertFalse(valid_destination(bad), bad)
        with self.assertRaisesRegex(ValueError, "Expected 753"):
            load_receipts(expected=753)

    def test_statuses_distinguish_submission_render_and_delivery(self):
        states = ["PENDING", "RUNNING", "FAILED", "CANCELLED", "DONE", "DONE"]
        rows = [receipt(f"memory-dungeon-saturate-{n}", 45000 + n,
                        f"public/images/memory-dungeon/{n}.webp") for n in range(6)]
        jobs = [job(row, state, None if n == 4 else 3000 + n)
                for n, (row, state) in enumerate(zip(rows, states))]
        calls = []
        def media_probe(path, created):
            calls.append(path)
            return "delivered"
        report = audit_jobs(rows, jobs, media_probe)
        self.assertEqual([x["status"] for x in report["results"]],
                         ["pending", "running", "failed", "cancelled",
                          "done_without_art_image", "delivered"])
        self.assertEqual(calls, [rows[-1]["imagePath"]])
        self.assertEqual(report["delivered"], 1)

    def test_mismatched_id_or_destination_is_not_delivered(self):
        row = receipt()
        for mismatched in (job(row, path="public/images/memory-dungeon/other.webp"),
                           job(row, request_id="memory-dungeon-saturate-other")):
            report = audit_jobs([row], [mismatched], lambda *_: self.fail("No media probe"))
            self.assertEqual(report["results"][0]["status"], "job_identity_mismatch")
        self.assertEqual(audit_jobs([row], [], lambda *_: self.fail("No probe"))["results"][0]["status"],
                         "job_missing")
        self.assertEqual(job_identity({"payload": "{bad json"}), None)

    def test_media_must_be_image_from_this_job_not_stale_asset(self):
        created = "2026-10-26T01:00:00.500Z"
        headers = {"Content-Type": "image/webp",
                   "Last-Modified": "Mon, 26 Oct 2026 01:00:01 GMT"}
        self.assertEqual(assess_media_headers(headers, created), "delivered")
        self.assertEqual(assess_media_headers(
            {**headers, "Content-Type": "text/html"}, created), "media_not_image")
        self.assertEqual(assess_media_headers(
            {**headers, "Last-Modified": "Sun, 25 Oct 2026 01:00:00 GMT"}, created), "media_stale")
        self.assertEqual(assess_media_headers(
            {"Content-Type": "image/webp"}, created), "media_unproven")
        self.assertEqual(assess_media_headers(headers, None), "media_unproven")


if __name__ == "__main__":
    unittest.main()
