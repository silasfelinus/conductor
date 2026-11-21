"""Contracts for Hybridizer's curated launch-hybrid list and its trickle submitter (t-007)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import hybridizer_launch_batch as batch  # noqa: E402
import hybridizer_launch_pairs as pairs  # noqa: E402

CATALOG = ROOT / "projects" / "hybridizer" / "STARTER-CATALOG.json"


class LaunchPairsTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads(CATALOG.read_text())
        self.committed = json.loads(pairs.OUT.read_text())

    def test_committed_list_is_reproducible(self):
        self.assertEqual(pairs.build(self.catalog), self.committed)

    def test_four_thousand_unique_canonical_starter_pairs(self):
        keys = {entry["key"] for entry in self.catalog["entries"]}
        listed = [tuple(p) for p in self.committed["pairs"]]
        self.assertEqual(len(listed), 4000)
        self.assertEqual(len(set(listed)), 4000)
        for left, right in listed:
            self.assertLess(left, right)
            self.assertIn(left, keys)
            self.assertIn(right, keys)

    def test_coverage_favours_animals_and_reaches_every_starter(self):
        counts = self.committed["counts"]
        self.assertEqual(counts["animal-animal"], 2000)
        self.assertEqual(sum(counts.values()), 4000)
        self.assertGreaterEqual(self.committed["ingredientUsage"]["min"], 20)

    def test_showcase_leads_and_every_batch_mixes_categories(self):
        self.assertEqual(self.committed["pairs"][0], ["banana", "cat"])
        groups = {e["key"]: pairs.group_of(e) for e in self.catalog["entries"]}
        for start in range(0, 4000, 50):
            chunk = self.committed["pairs"][start:start + 50]
            kinds = {pairs.category(groups[a], groups[b]) for a, b in chunk}
            self.assertGreaterEqual(len(kinds), 3, f"batch at {start} lacks variety")


class FakeApi:
    def __init__(self, cap_after):
        self.cap_after = cap_after
        self.posted = []

    def call(self, method, path, body=None):
        if method == "POST":
            self.posted.append(body)
            rows = []
            earlier = sum(len(b["pairs"]) for b in self.posted[:-1])
            for left, right in body["pairs"]:
                status = "DEFERRED" if earlier + len(rows) >= self.cap_after else "QUEUED"
                rows.append({
                    "pairKey": f"{left}+{right}",
                    "fusionId": None if status == "DEFERRED" else "f" * 64,
                    "title": "T",
                    "artJobId": None if status == "DEFERRED" else 1,
                    "status": status,
                })
            return {"success": True, "data": {"results": rows}}
        return {"success": True, "data": {"status": "READY", "imagePath": "/art/x.webp", "artImageId": 7}}

    def image_ok(self, path):
        return path == "/art/x.webp"


class CurationApi:
    def __init__(self, full=False, old=False, live_job=None):
        self.full = full
        self.old = old
        self.live_job = live_job
        self.posted = []

    def call(self, method, path, body=None):
        if method == "GET" and path.endswith("/status"):
            return {"success": True, "data": {"status": "QUEUED", "artJobId": self.live_job} if self.live_job else {}}
        if method == "GET":
            return {"success": True, "data": {"versions": [], "canEdit": True, **({} if self.old else {"canReroll": False})}}
        if self.full:
            return {"success": False, "statusCode": 429, "message": "window full"}
        self.posted.append((path, body))
        return {"success": True, "data": {"jobId": 99, "status": "QUEUED", "mode": "curation"}}


class SubmitterTests(unittest.TestCase):
    def test_deferred_pairs_stay_unsubmitted_and_window_stops(self):
        ledger = {"version": 1, "entries": {}}
        api = FakeApi(cap_after=60)
        listed = json.loads(pairs.OUT.read_text())["pairs"]
        report = batch.submit(api, ledger, listed, max_batches=4, dry_run=False)
        self.assertEqual(report["queued"], 60)
        self.assertEqual(len(ledger["entries"]), 60)
        self.assertEqual(report["batches"], 2, "a DEFERRED row ends the run")
        again = batch.submit(FakeApi(cap_after=0), ledger, listed, max_batches=1, dry_run=False)
        self.assertEqual(again["deferred"], 50)
        self.assertEqual(len(ledger["entries"]), 60, "deferred pairs are retried later, not recorded")

    def test_ready_is_only_verified_after_the_image_answers(self):
        ledger = {"version": 1, "entries": {"a+b": {"fusionId": "f" * 64, "status": "QUEUED"}}}
        batch.refresh(FakeApi(cap_after=0), ledger, limit=10)
        entry = ledger["entries"]["a+b"]
        self.assertEqual(entry["status"], "READY")
        self.assertIn("verifiedAt", entry)

    def test_curation_fail_is_resubmitted_once_and_unverified(self):
        ledger = {"version": 1, "entries": {
            "a+b": {"fusionId": "f" * 64, "status": "READY", "artImageId": 5, "verifiedAt": "x"},
            "a+c": {"fusionId": "e" * 64, "status": "QUEUED"},
        }}
        rows = [(1, "a+b", {"verdict": "FAIL", "reason": "two-creatures"}),
                (1, "a+c", {"verdict": "FAIL", "reason": "one-only"}),
                (1, "zz+zz", {"verdict": "FAIL", "reason": "one-only"})]
        api = CurationApi()
        report = batch.resubmit_curation(api, ledger, rows, limit=10)
        self.assertEqual(report["resubmitted"], 1)
        self.assertEqual(api.posted, [("/api/hybridizer/fusions/" + "f" * 64 + "/resubmit", {"curation": True})])
        entry = ledger["entries"]["a+b"]
        self.assertNotIn("verifiedAt", entry, "a curated-out image no longer counts as verified")
        self.assertEqual(entry["curation"]["rejectedArtImageId"], 5)
        self.assertEqual(entry["curation"]["resubmitJobId"], 99)
        again = batch.resubmit_curation(api, ledger, rows, limit=10)
        self.assertEqual(again["resubmitted"], 0, "each round resubmits a pair at most once")

    def test_curation_stops_when_window_full(self):
        ledger = {"version": 1, "entries": {
            k: {"fusionId": "f" * 64, "status": "READY", "artImageId": 5} for k in ("a+b", "a+c")}}
        rows = [(1, k, {"verdict": "FAIL"}) for k in ("a+b", "a+c")]
        report = batch.resubmit_curation(CurationApi(full=True), ledger, rows, limit=10)
        self.assertTrue(report["windowFull"])
        self.assertEqual(report["resubmitted"], 0)
        self.assertNotIn("curation", ledger["entries"]["a+b"])

    def test_curation_adopts_an_existing_newer_job_instead_of_resubmitting(self):
        ledger = {"version": 1, "entries": {
            "a+b": {"fusionId": "f" * 64, "status": "QUEUED", "artJobId": 10, "artImageId": 5, "verifiedAt": "x"}}}
        api = CurationApi(live_job=77)
        report = batch.resubmit_curation(api, ledger, [(1, "a+b", {"verdict": "FAIL", "artImageId": 5})], limit=10)
        self.assertEqual(report.get("adopted"), 1)
        self.assertEqual(report["resubmitted"], 0)
        self.assertEqual(api.posted, [], "a pair already re-rendering is never resubmitted")
        entry = ledger["entries"]["a+b"]
        self.assertEqual(entry["curation"]["resubmitJobId"], 77)
        self.assertEqual(entry["curation"]["rejectedArtImageId"], 5)
        self.assertNotIn("verifiedAt", entry)

    def test_curation_waits_for_the_deployed_server(self):
        ledger = {"version": 1, "entries": {"a+b": {"fusionId": "f" * 64, "status": "READY", "artImageId": 5}}}
        api = CurationApi(old=True)
        report = batch.resubmit_curation(api, ledger, [(1, "a+b", {"verdict": "FAIL"})], limit=10)
        self.assertTrue(report["serverNotReady"])
        self.assertEqual(api.posted, [], "nothing is posted to a server without curation mode")

    def test_refresh_does_not_reverify_the_rejected_image(self):
        ledger = {"version": 1, "entries": {"a+b": {
            "fusionId": "f" * 64, "status": "QUEUED", "curation": {"round": 1, "rejectedArtImageId": 7}}}}
        batch.refresh(FakeApi(cap_after=0), ledger, limit=10)
        self.assertNotIn("verifiedAt", ledger["entries"]["a+b"])

    def test_committed_curation_rounds_match_the_ledger(self):
        rows = batch.load_curation()
        ledger = batch.load_ledger()["entries"]
        for _round, key, verdict in rows:
            self.assertIn(key, ledger, f"{key} is not a launch pair")
            self.assertIn(verdict.get("reason"), {"one-only", "two-creatures", "missing-ingredient", "other"})

    def test_missing_token_is_unresolved(self):
        with tempfile.TemporaryDirectory() as temp, mock.patch.dict("os.environ", {"KR_API_TOKEN": ""}), \
                mock.patch.object(batch, "LEDGER", Path(temp) / "ledger.json"), \
                mock.patch.object(sys, "argv", ["hybridizer_launch_batch.py"]):
            self.assertEqual(batch.main(), 2)


if __name__ == "__main__":
    unittest.main()
