"""The share gate: don't claim jobs this box cannot render.

2026-08-26 — alexandria rebooted, Silas-PC's SMB mappings went Unavailable, and
kr-relay claimed and failed 71 ArtJobs at ~5/min. ComfyUI still believed it had
the models (folder_paths caches its filename lists), so every claim reached
`node 3 (CLIPTextEncode): hostbuf_file_reader_read failed` and burned an
attempt. Relay heartbeat, /system_stats and pm2 status all stayed green
throughout.

These lock the gate's behaviour, including the parts that make it safe to ship:
it is opt-in, it caches, and it logs edges rather than every poll.
"""
import importlib
import os
import sys
import types
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HOME_SERVER = REPO / "ops" / "home-server"
# Unreadable by construction: the parent is a regular file, so nothing can
# create it later. A plain "/nonexistent-..." string is not safe -- an earlier
# draft of a sibling test called makedirs on one and brought it into existence,
# silently turning these assertions green against a share that now resolved.
DEAD_SHARE = str(HOME_SERVER / "relay_agent.py" / "ai" / "models")


def load_relay(**env):
    """Import relay_agent fresh with `env` applied, and capture its log lines."""
    saved = dict(os.environ)
    os.environ.update({k: v for k, v in env.items() if v is not None})
    for key, value in env.items():
        if value is None:
            os.environ.pop(key, None)
    sys.path.insert(0, str(HOME_SERVER))
    try:
        sys.modules.pop("relay_agent", None)
        relay = importlib.import_module("relay_agent")
    finally:
        sys.path.remove(str(HOME_SERVER))
        os.environ.clear()
        os.environ.update(saved)

    lines = []
    relay.log = lambda message: lines.append(str(message))
    relay.logged = lines
    return relay


class ShareProbeTests(unittest.TestCase):
    def test_probe_reads_a_real_directory(self):
        relay = load_relay(KR_SHARE_PROBE_PATH=str(HOME_SERVER))
        ok, detail = relay.probe_share(str(HOME_SERVER))
        self.assertTrue(ok)
        self.assertEqual(detail, "")

    def test_probe_reports_a_missing_directory(self):
        relay = load_relay(KR_SHARE_PROBE_PATH=DEAD_SHARE)
        ok, detail = relay.probe_share(DEAD_SHARE)
        self.assertFalse(ok)
        self.assertIn("Error", detail)

    def test_probe_reports_a_file_where_a_directory_belongs(self):
        """A stale mount can leave a name that stat()s but cannot be listed."""
        relay = load_relay(KR_SHARE_PROBE_PATH=str(HOME_SERVER))
        ok, detail = relay.probe_share(str(HOME_SERVER / "relay_agent.py"))
        self.assertFalse(ok)
        self.assertTrue(detail)

    def test_empty_directory_counts_as_available(self):
        """An empty share is mounted; scandir yielding nothing is not a fault."""
        import tempfile

        relay = load_relay(KR_SHARE_PROBE_PATH=str(HOME_SERVER))
        with tempfile.TemporaryDirectory() as empty:
            ok, detail = relay.probe_share(empty)
        self.assertTrue(ok)
        self.assertEqual(detail, "")

    def test_required_files_default_to_none(self):
        """Unset KR_SHARE_REQUIRED_FILES -> behaves exactly like before this existed."""
        relay = load_relay(
            KR_SHARE_PROBE_PATH=str(HOME_SERVER), KR_SHARE_REQUIRED_FILES=None
        )
        self.assertEqual(relay.KR_SHARE_REQUIRED_FILES, [])
        ok, detail = relay.probe_share(str(HOME_SERVER))
        self.assertTrue(ok)
        self.assertEqual(detail, "")

    def test_a_partially_readable_share_fails_on_a_missing_required_file(self):
        """2026-08-28: scandir found one entry; the file that mattered was not it.

        A directory that lists fine but is missing the one file a job actually
        needs must fail the gate, not pass it.
        """
        relay = load_relay(
            KR_SHARE_PROBE_PATH=str(HOME_SERVER),
            KR_SHARE_REQUIRED_FILES="vae/qwen_image_vae.safetensors",
        )
        # HOME_SERVER scandir's fine (this test file lives there) but has no
        # vae/ subdirectory at all -- the partially-readable-share shape.
        ok, detail = relay.probe_share(str(HOME_SERVER))
        self.assertFalse(ok)
        self.assertIn("vae/qwen_image_vae.safetensors", detail)

    def test_a_required_file_that_is_actually_present_passes(self):
        relay = load_relay(
            KR_SHARE_PROBE_PATH=str(HOME_SERVER),
            KR_SHARE_REQUIRED_FILES="relay_agent.py",
        )
        ok, detail = relay.probe_share(str(HOME_SERVER))
        self.assertTrue(ok)
        self.assertEqual(detail, "")

    def test_multiple_required_files_are_comma_separated(self):
        relay = load_relay(
            KR_SHARE_PROBE_PATH=str(HOME_SERVER),
            KR_SHARE_REQUIRED_FILES=" relay_agent.py , ecosystem.config.js ",
        )
        self.assertEqual(
            relay.KR_SHARE_REQUIRED_FILES,
            ["relay_agent.py", "ecosystem.config.js"],
        )
        ok, detail = relay.probe_share(str(HOME_SERVER))
        self.assertTrue(ok)


class ShareGateTests(unittest.TestCase):
    def test_gate_is_opt_in(self):
        """No probe path configured -> previous behaviour, always claim."""
        relay = load_relay(KR_SHARE_PROBE_PATH=None)
        self.assertEqual(relay.KR_SHARE_PROBE_PATH, "")
        self.assertTrue(relay.share_available())
        self.assertEqual(relay.logged, [])

    def test_available_share_permits_claiming(self):
        relay = load_relay(KR_SHARE_PROBE_PATH=str(HOME_SERVER))
        self.assertTrue(relay.share_available(now=1000.0))

    def test_missing_share_blocks_claiming(self):
        relay = load_relay(KR_SHARE_PROBE_PATH=DEAD_SHARE)
        self.assertFalse(relay.share_available(now=1000.0))

    def test_block_is_logged_once_not_every_poll(self):
        """A 2s poll loop must not emit a line every 2s while the NAS reboots."""
        relay = load_relay(
            KR_SHARE_PROBE_PATH=DEAD_SHARE,
            KR_SHARE_PROBE_SECONDS="30",
        )
        for tick in range(0, 300, 30):
            relay.share_available(now=1000.0 + tick)
        self.assertEqual(len(relay.logged), 1, relay.logged)
        self.assertIn("NOT claiming", relay.logged[0])

    def test_a_healthy_first_probe_says_nothing(self):
        """A clean start must not announce a recovery that never happened.

        The first armed run (2026-08-27) logged "is readable again - resuming
        claims" against a share that had never been down, because the initial
        reported state was None and `None is not True`. It read as an outage
        and told the operator to restart ComfyUI for nothing.
        """
        relay = load_relay(KR_SHARE_PROBE_PATH=str(HOME_SERVER))
        self.assertTrue(relay.share_available(now=1000.0))
        self.assertEqual(relay.logged, [])

    def test_a_failing_first_probe_still_warns(self):
        """The silent-first-probe rule must not swallow a genuine dead mount."""
        relay = load_relay(KR_SHARE_PROBE_PATH=DEAD_SHARE)
        self.assertFalse(relay.share_available(now=1000.0))
        self.assertEqual(len(relay.logged), 1, relay.logged)
        self.assertIn("NOT claiming", relay.logged[0])

    def test_recovery_is_logged_and_names_the_comfyui_restart(self):
        """Remapping the drive is not enough; folder_paths caches. Say so."""
        relay = load_relay(
            KR_SHARE_PROBE_PATH=DEAD_SHARE,
            KR_SHARE_PROBE_SECONDS="0",
        )
        self.assertFalse(relay.share_available(now=1000.0))
        relay.KR_SHARE_PROBE_PATH = str(HOME_SERVER)
        self.assertTrue(relay.share_available(now=1001.0))

        self.assertEqual(len(relay.logged), 2, relay.logged)
        self.assertIn("readable again", relay.logged[1])
        self.assertIn("restart", relay.logged[1].lower())
        self.assertIn("folder_paths", relay.logged[1])

    def test_result_is_cached_between_probes(self):
        """Don't stat() an SMB share on every 2s poll."""
        relay = load_relay(
            KR_SHARE_PROBE_PATH=str(HOME_SERVER), KR_SHARE_PROBE_SECONDS="30"
        )
        calls = []
        real = relay.probe_share
        relay.probe_share = lambda path: (calls.append(path), real(path))[1]

        relay.share_available(now=1000.0)
        relay.share_available(now=1005.0)
        relay.share_available(now=1029.0)
        self.assertEqual(len(calls), 1, calls)

        relay.share_available(now=1031.0)
        self.assertEqual(len(calls), 2, calls)

    def test_blocked_message_points_at_the_box_not_the_queue(self):
        relay = load_relay(KR_SHARE_PROBE_PATH=DEAD_SHARE)
        relay.share_available(now=1000.0)
        message = relay.logged[0]
        self.assertIn(DEAD_SHARE, message)
        self.assertIn("net use", message)
        self.assertIn("retry budget", message)

    def test_a_partially_readable_share_blocks_claiming_too(self):
        """The gate itself, not just probe_share, must catch a missing required file."""
        relay = load_relay(
            KR_SHARE_PROBE_PATH=str(HOME_SERVER),
            KR_SHARE_REQUIRED_FILES="vae/qwen_image_vae.safetensors",
        )
        self.assertFalse(relay.share_available(now=1000.0))
        self.assertEqual(len(relay.logged), 1, relay.logged)
        self.assertIn("vae/qwen_image_vae.safetensors", relay.logged[0])
        self.assertIn("NOT claiming", relay.logged[0])


if __name__ == "__main__":
    unittest.main()
