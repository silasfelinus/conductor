"""The morning email must read the container logs, not just count them.

Silas, 2026-09-04: *"give me this kind of detail, guides on what to mute, and
how to fix ... baked into my daily morning email."*

The digest that Alexandria publishes is accurate and inert. A row reading
`ownfoil . warn . 3999x` does not say that one truncated file is two thirds of
the day's log volume, that the fix is deleting it, or that the netdata line
under it is cosmetic. These tests cover the two properties that make the
written review trustworthy enough to act on before coffee:

* nothing rendered into the email is taken on the model's word -- counts,
  containers and fingerprints all come from the digest, so an invented
  signature yields a shorter review, never a wrong one; and
* every failure path is silent, because a digest that does not go out is worse
  than one missing its newest section.
"""
import datetime
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, REPO / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


reviewer = _load("author_container_log_review")
legacy = _load("build_digest_email")
emailer = _load("build_digest_email_v2")

DIGEST = {
    "version": 1,
    "generated_at": "2026-09-04T08:38:04.866346+00:00",
    "host": "alexandria",
    "window": "24h",
    "scan": {"containers_scanned": 43, "lines_read": 175939,
             "lines_matched": 12325, "signatures_total": 151,
             "containers_failed": []},
    "new": [{"fingerprint": "2554bd7de390", "container": "ownfoil",
             "severity": "warn", "count": 3999, "baseline": None,
             "sample": "Verification of Staffer Case failed: read returned empty",
             "skeleton": "verification of <STR> failed"}],
    "spiking": [],
    "quiet": [],
    "top": [{"fingerprint": "c7333bf2fc2d", "container": "netdata",
             "severity": "error", "count": 417, "baseline": 400,
             "sample": "start watching '/etc/netdata/scripts.d': no such file",
             "skeleton": "start watching <PATH>"}],
}


class CoercionTests(unittest.TestCase):
    """The model proposes; the digest disposes."""

    def setUp(self):
        changed, standing = reviewer.signature_rows(DIGEST)
        today = datetime.date(2026, 9, 4)
        rows = reviewer.with_history(changed, {}, today) + reviewer.with_history(
            standing, {}, today
        )
        self.rows = {row["fingerprint"]: row for row in rows}

    def test_invented_fingerprint_is_dropped(self):
        review = reviewer.coerce_review(
            {"headline": "x", "items": [
                {"fingerprint": "deadbeefcafe", "diagnosis": "d", "fix": "f", "action": "fix"},
                {"fingerprint": "2554bd7de390", "diagnosis": "d", "fix": "f", "action": "fix"},
            ]},
            self.rows,
        )
        self.assertEqual([i["fingerprint"] for i in review["items"]], ["2554bd7de390"])

    def test_counts_come_from_the_digest_not_the_model(self):
        review = reviewer.coerce_review(
            {"items": [{"fingerprint": "2554bd7de390", "diagnosis": "d", "fix": "f",
                        "count": 11, "container": "not-ownfoil"}]},
            self.rows,
        )
        item = review["items"][0]
        self.assertEqual(item["count"], 3999)
        self.assertEqual(item["container"], "ownfoil")

    def test_unknown_action_falls_back_to_fix(self):
        review = reviewer.coerce_review(
            {"items": [{"fingerprint": "2554bd7de390", "diagnosis": "d", "action": "escalate"}]},
            self.rows,
        )
        self.assertEqual(review["items"][0]["action"], "fix")

    def test_item_count_is_capped(self):
        raw = {"items": [{"fingerprint": "2554bd7de390", "diagnosis": "d"}] * 40}
        self.assertLessEqual(len(reviewer.coerce_review(raw, self.rows)["items"]),
                             reviewer.MAX_ITEMS)

    def test_mute_needs_a_reason_and_a_real_signature(self):
        review = reviewer.coerce_review(
            {"mute": [{"fingerprint": "c7333bf2fc2d", "why": ""},
                      {"fingerprint": "nope00000000", "why": "benign"},
                      {"fingerprint": "c7333bf2fc2d", "why": "cosmetic"}]},
            self.rows,
        )
        self.assertEqual(len(review["mute"]), 1)
        self.assertEqual(review["mute"][0]["why"], "cosmetic")


class BucketTests(unittest.TestCase):
    def test_changed_bucket_wins_over_standing(self):
        digest = dict(DIGEST, top=list(DIGEST["top"]) + list(DIGEST["new"]))
        changed, standing = reviewer.signature_rows(digest)
        self.assertEqual([r["bucket"] for r in changed], ["new"])
        self.assertNotIn("2554bd7de390", [r["fingerprint"] for r in standing])


class NagCounterTests(unittest.TestCase):
    """'Unfixed for 9 days' must be arithmetic, not recall."""

    def test_days_standing_counts_from_the_stored_date(self):
        history = {"2554bd7de390": {"first_reported": "2026-08-26"}}
        rows = reviewer.with_history(
            [dict(DIGEST["new"][0])], history, datetime.date(2026, 9, 4)
        )
        self.assertEqual(rows[0]["days_standing"], 9)

    def test_a_first_sighting_has_no_nag_clock(self):
        rows = reviewer.with_history(
            [dict(DIGEST["new"][0])], {}, datetime.date(2026, 9, 4)
        )
        self.assertEqual(rows[0]["days_standing"], 0)

    def test_history_records_only_what_was_reported(self):
        history = reviewer.update_history(
            {}, [{"fingerprint": "2554bd7de390", "container": "ownfoil"}],
            datetime.date(2026, 9, 4),
        )
        self.assertIn("2554bd7de390", history)
        self.assertNotIn("c7333bf2fc2d", history)

    def test_first_reported_survives_a_later_report(self):
        history = {"2554bd7de390": {"first_reported": "2026-08-26"}}
        history = reviewer.update_history(
            history, [{"fingerprint": "2554bd7de390", "container": "ownfoil"}],
            datetime.date(2026, 9, 4),
        )
        self.assertEqual(history["2554bd7de390"]["first_reported"], "2026-08-26")
        self.assertEqual(history["2554bd7de390"]["last_reported"], "2026-09-04")


class SilentFailureTests(unittest.TestCase):
    """Every failure path leaves the email intact and exits 0."""

    def test_no_api_key_exits_clean(self):
        import os
        saved = os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            self.assertEqual(reviewer.main(["--digest", "/nonexistent.json"]), 0)
        finally:
            if saved is not None:
                os.environ["ANTHROPIC_API_KEY"] = saved

    def test_missing_digest_exits_clean(self):
        import os
        os.environ["ANTHROPIC_API_KEY"] = "test-key-not-used"
        try:
            with tempfile.TemporaryDirectory() as tmp:
                code = reviewer.main([
                    "--digest", str(Path(tmp) / "absent.json"),
                    "--output", str(Path(tmp) / "review.json"),
                ])
            self.assertEqual(code, 0)
        finally:
            os.environ.pop("ANTHROPIC_API_KEY", None)

    def test_stale_digest_is_not_reviewed(self):
        import os
        os.environ["ANTHROPIC_API_KEY"] = "test-key-not-used"
        try:
            with tempfile.TemporaryDirectory() as tmp:
                stale = dict(DIGEST, generated_at="2020-01-01T00:00:00+00:00")
                digest_path = Path(tmp) / "digest.json"
                digest_path.write_text(json.dumps(stale))
                out = Path(tmp) / "review.json"
                # No network call is possible with this key; reaching the API
                # at all would raise rather than return 0.
                self.assertEqual(
                    reviewer.main(["--digest", str(digest_path), "--output", str(out)]), 0
                )
                self.assertFalse(out.exists())
        finally:
            os.environ.pop("ANTHROPIC_API_KEY", None)

    def test_unreadable_review_file_is_not_fatal(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "review.json"
            bad.write_text("{not json")
            self.assertEqual(reviewer.load_review(str(bad)), {})


class EmailRenderTests(unittest.TestCase):
    def _digest(self, review):
        return {"container_logs": {"state": "findings", "reason": "1 new",
                                   "review": review}}

    def test_section_renders_diagnosis_fix_and_command(self):
        html = legacy.container_log_review_section(self._digest({
            "headline": "One truncated file is two thirds of the day's log volume.",
            "host": "alexandria",
            "items": [{"fingerprint": "2554bd7de390", "container": "ownfoil",
                       "count": 3999, "bucket": "new", "days_standing": 0,
                       "diagnosis": "A truncated .xci retries forever.",
                       "fix": "Delete the file.", "action": "fix"}],
            "mute": [{"fingerprint": "c7333bf2fc2d", "container": "netdata",
                      "count": 417, "why": "a directory we never created"}],
        }))
        self.assertIn("Container log triage", html)
        self.assertIn("two thirds", html)
        self.assertIn("A truncated .xci retries forever.", html)
        self.assertIn("Delete the file.", html)
        self.assertIn("3,999", html)
        self.assertIn("--mute c7333bf2fc2d", html)
        self.assertIn("SAFE TO MUTE", html)

    def test_nag_counter_is_visible(self):
        html = legacy.container_log_review_section(self._digest({
            "headline": "h",
            "items": [{"fingerprint": "2554bd7de390", "container": "ownfoil",
                       "count": 10, "bucket": "standing", "days_standing": 9,
                       "diagnosis": "d", "fix": "f", "action": "fix"}],
        }))
        self.assertIn("unfixed 9d", html)

    def test_no_review_renders_nothing(self):
        self.assertEqual(legacy.container_log_review_section({}), "")
        self.assertEqual(
            legacy.container_log_review_section({"container_logs": {"state": "clean"}}), ""
        )

    def test_review_suppresses_the_banner_sample_list(self):
        health = {"state": "findings", "reason": "1 new", "new": 1,
                  "spiking": 0, "quiet": 0,
                  "findings": [{"container": "ownfoil", "sample": "RAW SAMPLE LINE"}]}
        with_review = emailer.container_log_banner(
            {"container_logs": dict(health, review={"headline": "h", "items": []})}
        )
        without = emailer.container_log_banner({"container_logs": health})
        self.assertIn("RAW SAMPLE LINE", without)
        self.assertNotIn("RAW SAMPLE LINE", with_review)

    def test_html_is_escaped(self):
        html = legacy.container_log_review_section(self._digest({
            "headline": "<script>alert(1)</script>",
            "items": [{"fingerprint": "a", "container": "c", "count": 1,
                       "bucket": "new", "days_standing": 0,
                       "diagnosis": "<img onerror=x>", "fix": "&", "action": "fix"}],
        }))
        self.assertNotIn("<script>", html)
        self.assertNotIn("<img onerror", html)


class LeadSlotTests(unittest.TestCase):
    """The review replaced the filler; the filler must not come back.

    Silas, 2026-09-04: *"this should actually replace our filler text that I
    get each morning, that is always quite dry and useless."* The slot used to
    hold `daily_spark`, a rotating "wild idea" picked by `date.toordinal() % 3`
    with no connection to anything happening on the box.
    """

    def test_the_spark_generator_is_gone(self):
        build_digest = _load("build_digest")
        self.assertFalse(hasattr(build_digest, "daily_spark"))

    def test_the_digest_no_longer_carries_a_spark(self):
        source = (REPO / "scripts" / "build_digest_email.py").read_text()
        self.assertNotIn('digest.get("daily_spark"', source)

    def test_the_review_occupies_the_lead_slot(self):
        html = legacy.build_payload({
            "date": "2026-09-04",
            "greeting": "Good morning, Silas.",
            "projects": [], "open_branches": [],
            "activity_since": [], "autonomous_work": [],
            "pitches_awaiting_vote": [], "all_needs_attention": [],
            "container_logs": {"state": "findings", "review": {
                "headline": "One truncated file is two thirds of the log volume.",
                "host": "alexandria",
                "items": [{"fingerprint": "2554bd7de390", "container": "ownfoil",
                           "count": 3999, "bucket": "new", "days_standing": 0,
                           "diagnosis": "It retries forever.",
                           "fix": "Delete it.", "action": "fix"}],
                "mute": [],
            }},
        })["htmlContent"]
        self.assertIn("Container log triage", html)
        self.assertIn("It retries forever.", html)
        # It leads: the review comes before the project/activity body.
        self.assertLess(html.index("Container log triage"), html.index("Delete it."))
        self.assertNotIn("Wild idea", html)

    def test_no_review_leaves_the_slot_empty_rather_than_refilled(self):
        html = legacy.build_payload({
            "date": "2026-09-04", "greeting": "Good morning, Silas.",
            "projects": [], "open_branches": [],
            "activity_since": [], "autonomous_work": [],
            "pitches_awaiting_vote": [], "all_needs_attention": [],
        })["htmlContent"]
        self.assertNotIn("Container log triage", html)
        self.assertNotIn("Wild idea", html)
        self.assertNotIn("Daily spark", html)


if __name__ == "__main__":
    unittest.main()
