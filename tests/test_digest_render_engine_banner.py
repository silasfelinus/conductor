"""The daily digest must state render health, in the email, every day.

2026-09-02: ComfyUI was down ~24 hours and at least one digest went out during
the outage carrying no hint of it. The digest is the one message that reaches
Silas daily, so it is the natural backstop for every alarm that failed — but it
had no render section at all.

A green line every day matters as much as a red one: it is what makes the
absence of a red line mean something.
"""
import importlib.util
import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

SPEC = importlib.util.spec_from_file_location(
    "build_digest_email_v2", REPO / "scripts" / "build_digest_email_v2.py"
)
emailer = importlib.util.module_from_spec(SPEC)
sys.modules["build_digest_email_v2"] = emailer
SPEC.loader.exec_module(emailer)


class EngineBannerTests(unittest.TestCase):
    def test_healthy_banner_is_present_and_green(self):
        html = emailer.engine_banner(
            {"render_engine": {"state": "ok", "reason": "comfy-fast: heartbeat healthy 0.4 minutes ago."}}
        )
        self.assertIn("Render engine healthy", html)
        self.assertIn("#065f46", html)
        self.assertIn("heartbeat healthy", html)

    def test_down_banner_says_the_queue_is_not_draining(self):
        html = emailer.engine_banner({"render_engine": {"state": "down", "reason": "x"}})
        self.assertIn("DOWN", html)
        self.assertIn("not draining", html)
        self.assertIn("#ef4444", html)

    def test_silent_banner_is_distinct_from_down(self):
        """'No heartbeat' and 'heartbeat says down' need different remedies."""
        silent = emailer.engine_banner({"render_engine": {"state": "silent", "reason": "x"}})
        down = emailer.engine_banner({"render_engine": {"state": "down", "reason": "x"}})
        self.assertIn("SILENT", silent)
        self.assertNotEqual(silent, down)

    def test_unresolved_is_not_dressed_up_as_healthy(self):
        html = emailer.engine_banner({"render_engine": {"state": "unresolved", "reason": "no token"}})
        self.assertIn("unknown", html.lower())
        self.assertNotIn("#065f46", html)

    def test_an_unknown_state_falls_back_to_unresolved_not_healthy(self):
        html = emailer.engine_banner({"render_engine": {"state": "banana"}})
        self.assertIn("unknown", html.lower())

    def test_missing_section_renders_nothing_rather_than_crashing(self):
        """An older digest.json must still build an email."""
        self.assertEqual(emailer.engine_banner({}), "")
        self.assertEqual(emailer.engine_banner({"render_engine": None}), "")
        self.assertEqual(emailer.engine_banner({"render_engine": "down"}), "")

    def test_reason_text_is_escaped(self):
        html = emailer.engine_banner(
            {"render_engine": {"state": "down", "reason": "<script>alert(1)</script>"}}
        )
        self.assertNotIn("<script>", html)


class BuildPayloadTests(unittest.TestCase):
    """The banner has to survive the real assembly path, not just its own unit."""

    def minimal_digest(self, state="down"):
        return {
            "date": "2026-09-02",
            "greeting": "Good evening",
            "daily_spark": {"label": "✨ Daily spark", "text": "spark"},
            "tomorrow_proposal": None,
            "yesterday_output": None,
            "previous_dream_output": None,
            "current_dream_output": None,
            "daily_dream_page": "",
            "art_highlights": [],
            "new_creations": [],
            "commits_since": [],
            "merges_since": [],
            "activity_since": [],
            "autonomous_work": [],
            "projects": [],
            "all_needs_attention": [],
            "pitches_awaiting_vote": [],
            "open_branches": [],
            "render_engine": {"state": state, "reason": "comfy-fast: no heartbeat"},
        }

    def test_banner_leads_the_email_body(self):
        payload = emailer.build_payload(self.minimal_digest())
        html = payload["htmlContent"]
        self.assertIn("Render engine DOWN", html)
        self.assertLess(
            html.index("Render engine DOWN"),
            html.index("Conductor"),
            "render health must lead — a dream bundle whose art never rendered "
            "is not good news, and it should not take three screens to find out",
        )

    def test_a_digest_without_the_section_still_builds(self):
        digest = self.minimal_digest()
        del digest["render_engine"]
        payload = emailer.build_payload(digest)
        self.assertIn("htmlContent", payload)
        self.assertTrue(payload["htmlContent"].strip())


class DigestPayloadTests(unittest.TestCase):
    def test_build_digest_exposes_render_engine_and_never_raises(self):
        """No token in the test environment -> 'unresolved', not an exception."""
        import build_digest

        health = build_digest.render_engine_health()
        self.assertIsInstance(health, dict)
        self.assertIn(health["state"], {"ok", "down", "silent", "unresolved"})
        self.assertTrue(health["reason"])

    def test_validate_digest_accepts_the_new_key(self):
        """The new key must not trip the digest schema gate in CI."""
        import validate_digest

        self.assertNotIn("render_engine", getattr(validate_digest, "__doc__", "") or "")
        source = (REPO / "scripts" / "validate_digest.py").read_text()
        self.assertNotIn(
            '"render_engine"', source,
            "validate_digest must stay permissive about this optional section",
        )


if __name__ == "__main__":
    unittest.main()
