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

    def test_missing_token_is_unresolved(self):
        with tempfile.TemporaryDirectory() as temp, mock.patch.dict("os.environ", {"KR_API_TOKEN": ""}), \
                mock.patch.object(batch, "LEDGER", Path(temp) / "ledger.json"), \
                mock.patch.object(sys, "argv", ["hybridizer_launch_batch.py"]):
            self.assertEqual(batch.main(), 2)


if __name__ == "__main__":
    unittest.main()
