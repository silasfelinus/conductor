"""Adversarial read-only Hoshimori queue-claim diagnostics."""
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_memory_dungeon_hoshimori_relay import (  # noqa: E402
    analyze, fetch_pending_queue, receipt_index,
)

NOW = datetime(2026, 10, 31, 15, 0, tzinfo=timezone.utc)
REQUEST = "memory-dungeon-hoshimori-e07-style-pip-portrait"
PATH = "public/images/memory-dungeon/hoshimori/e07/style-proofs/pip-portrait.webp"
RECEIPTS = {52110: (REQUEST, PATH)}


def job(*, status="PENDING", attempts=0, request=REQUEST, path=PATH):
    return {
        "id": 52110, "status": status, "attempts": attempts, "engine": "COMFY",
        "payload": {"conductorRequest": {
            "id": request, "imagePath": path,
            "targetRepo": "silasfelinus/kind_robots",
        }},
    }


def agent(*, minutes_ago=1, engines=None):
    return {
        "agentId": "kr-relay-test",
        "lastSeenAt": (NOW - timedelta(minutes=minutes_ago)).isoformat(),
        "engines": ["COMFY"] if engines is None else engines,
        "supportsInputImages": True,
    }


def inspect(*, jobs=None, paused=False, agents=None, global_pending=None):
    return analyze(
        RECEIPTS, [job()] if jobs is None else jobs,
        paused=paused, agents=agents,
        stats={"queueDepth": {"PENDING": 500, "RUNNING": 0}},
        global_pending=global_pending,
        now=NOW,
    )


class HoshimoriRelayTriageTests(unittest.TestCase):
    def test_canonical_twenty_receipts_are_present(self):
        self.assertEqual(len(receipt_index()), 20)

    def test_paused_is_definitive_even_with_healthy_relay(self):
        report = inspect(paused=True, agents=[agent()])
        self.assertEqual(report["verdict"], "queue_paused")
        self.assertTrue(any("PAUSED" in b for b in report["blockers"]))
        self.assertEqual(report["style_states"]["pending"], 1)

    def test_exhausted_pending_is_not_claimable(self):
        report = inspect(jobs=[job(attempts=3)], agents=[agent()])
        self.assertEqual(report["verdict"], "all_pending_attempts_exhausted")
        self.assertEqual(report["pending_attempts_exhausted_ids"], [52110])
        self.assertEqual(report["pending_with_attempts_remaining"], 0)

    def test_missing_poll_registry_is_inconclusive_not_dead_relay(self):
        report = inspect(agents=[])
        self.assertEqual(report["verdict"], "claim_poll_unobserved_not_proven_down")
        self.assertEqual(report["relay_claim_poll"]["telemetry"], "unobserved_ephemeral")
        self.assertNotIn("down", report["blockers"][0].lower())

    def test_stale_poll_does_not_count_as_live(self):
        report = inspect(agents=[agent(minutes_ago=6)])
        self.assertEqual(report["relay_claim_poll"]["fresh_pollers"], 0)
        self.assertEqual(report["verdict"], "claim_poll_unobserved_not_proven_down")

    def test_non_comfy_poller_is_not_eligible_evidence(self):
        report = inspect(agents=[agent(engines=["A1111"])])
        self.assertEqual(report["verdict"], "comfy_claim_capability_unobserved")
        self.assertEqual(report["relay_claim_poll"]["fresh_comfy_pollers"], 0)

    def test_first_page_starvation_is_a_bounded_observation(self):
        pending = {
            "jobs": [{"id": i} for i in range(1, 201)],
            "pagination": {"totalCount": 500},
        }
        report = inspect(agents=[agent()], global_pending=pending)
        self.assertEqual(report["verdict"], "behind_first_global_pending_page")
        self.assertTrue(report["global_pending_sample"]["none_in_first_page"])
        self.assertEqual(report["global_pending_sample"]["global_pending_total"], 500)

    def test_visible_pending_job_needs_claim_trace_not_resubmission(self):
        pending = {
            "jobs": [{"id": 500}, {"id": 52110}],
            "pagination": {"totalCount": 2},
        }
        report = inspect(agents=[agent()], global_pending=pending)
        self.assertEqual(report["verdict"], "eligible_pending_needs_relay_claim_trace")
        self.assertEqual(report["global_pending_sample"]["first_hoshimori_position"], 2)
        self.assertEqual(report["pending_with_attempts_remaining"], 1)

    def test_mismatched_receipt_is_never_counted_as_pending(self):
        report = inspect(jobs=[job(request="forged")], agents=[agent()])
        self.assertEqual(report["verdict"], "receipt_integrity_blocker")
        self.assertEqual(report["style_states"]["identity_mismatch"], 1)
        self.assertEqual(report["style_states"]["pending"], 0)

    def test_done_job_is_not_a_delivered_image_claim(self):
        report = inspect(jobs=[job(status="DONE")], agents=[agent()])
        self.assertEqual(report["style_states"]["done"], 1)
        self.assertEqual(report["pending_with_attempts_remaining"], 0)
        self.assertNotIn("delivered", report["style_states"])

    def test_complete_queue_reveals_exact_comfy_runway_not_global_rank(self):
        first = [
            {"id": i, "priority": 100, "engine": "A1111", "attempts": 0}
            for i in range(1, 201)
        ]
        last = [
            {"id": 52110, "priority": 0, "engine": "COMFY", "attempts": 0}
        ]
        pages = {
            1: {"jobs": first, "pagination": {
                "page": 1, "pageSize": 200, "totalCount": 201,
                "hasNextPage": True,
            }},
            2: {"jobs": last, "pagination": {
                "page": 2, "pageSize": 200, "totalCount": 201,
                "hasNextPage": False,
            }},
        }
        snapshot = fetch_pending_queue(pages.get)
        report = inspect(agents=[agent()], global_pending=snapshot)
        self.assertEqual(report["global_pending_sample"]["first_hoshimori_position"], 201)
        self.assertTrue(report["global_pending_sample"]["complete_snapshot"])
        self.assertTrue(report["global_pending_sample"]["none_in_first_page"])
        self.assertEqual(report["global_pending_sample"]["comfy_pending_with_attempts_remaining"], 1)
        self.assertEqual(
            report["global_pending_sample"]["hoshimori_priority_runway"],
            [{"job_id": 52110, "global_pending_rank": 201,
              "comfy_attempt_rank": 1, "priority": 0}],
        )
        self.assertIn("cannot prove", report["global_pending_sample"]["note"])

    def test_incomplete_page_never_becomes_exact_rank(self):
        page = {"jobs": [{"id": 1, "priority": 0}], "pagination": {
            "page": 1, "pageSize": 200, "totalCount": 2,
            "hasNextPage": False,
        }}
        with self.assertRaisesRegex(ValueError, "incomplete"):
            fetch_pending_queue(lambda _: page)

    def test_priority_order_drift_is_rejected(self):
        page = {"jobs": [
            {"id": 1, "priority": 0}, {"id": 2, "priority": 10}
        ], "pagination": {
            "page": 1, "pageSize": 200, "totalCount": 2,
            "hasNextPage": False,
        }}
        with self.assertRaisesRegex(ValueError, "ordering"):
            fetch_pending_queue(lambda _: page)

    def test_duplicate_pending_job_is_rejected(self):
        page = {"jobs": [
            {"id": 1, "priority": 0}, {"id": 1, "priority": 0}
        ], "pagination": {
            "page": 1, "pageSize": 200, "totalCount": 2,
            "hasNextPage": False,
        }}
        with self.assertRaisesRegex(ValueError, "duplicate"):
            fetch_pending_queue(lambda _: page)

    def test_failed_next_page_never_returns_partial_queue(self):
        first = {"jobs": [
            {"id": i, "priority": 0} for i in range(1, 201)
        ], "pagination": {
            "page": 1, "pageSize": 200, "totalCount": 201,
            "hasNextPage": True,
        }}
        with self.assertRaisesRegex(RuntimeError, "page 2 unavailable"):
            fetch_pending_queue(lambda page: first if page == 1 else None)

    def test_inconsistent_pagination_total_is_rejected(self):
        first = {"jobs": [
            {"id": i, "priority": 1} for i in range(1, 201)
        ], "pagination": {
            "page": 1, "pageSize": 200, "totalCount": 201,
            "hasNextPage": True,
        }}
        second = {"jobs": [{"id": 201, "priority": 0}], "pagination": {
            "page": 2, "pageSize": 200, "totalCount": 202,
            "hasNextPage": False,
        }}
        with self.assertRaisesRegex(ValueError, "pagination changed"):
            fetch_pending_queue(lambda page: first if page == 1 else second)


if __name__ == "__main__":
    unittest.main()
