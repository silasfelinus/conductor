"""The LoRA import watcher must outlive a NAS reboot.

2026-08-26 — kr-relay's embedded lora-import thread died at startup with

    File "lora_import_agent.py", line 346, in watch_loop
      os.makedirs(LORA_IMPORT_DIR, exist_ok=True)
    FileNotFoundError: [WinError 67] The network name cannot be found: 'Z:/'

That makedirs sat *above* the loop, outside the `except Exception` that guards
every poll. Python kills only the offending thread, so kr-relay carried on
claiming and rendering with no importer, no log line, and no heartbeat change.
It stayed dead until the whole relay was restarted hours later.

Two defences, one test file: the call moved inside the guarded body, and the
thread now runs under a supervisor so *any* future escape is loud and
temporary rather than silent and permanent.
"""
import importlib
import sys
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
HOME_SERVER = REPO / "ops" / "home-server"
# A path whose *parent is a regular file*: makedirs cannot traverse it and
# cannot create it either. "/nonexistent/..." is the wrong fixture -- makedirs
# happily builds the whole chain when the process can write the root, so the
# test passed while proving nothing (caught 2026-08-26 writing these).
DEAD_SHARE = str(HOME_SERVER / "relay_agent.py" / "Lora" / "import")


class Stop(Exception):
    """Sentinel: break out of an intentionally infinite loop."""


def load(name):
    sys.path.insert(0, str(HOME_SERVER))
    try:
        sys.modules.pop(name, None)
        return importlib.import_module(name)
    finally:
        sys.path.remove(str(HOME_SERVER))


class WatchLoopSurvivesDeadShareTests(unittest.TestCase):
    def setUp(self):
        self.lora = load("lora_import_agent")
        self.logged = []
        self.lora.log = lambda message: self.logged.append(str(message))
        self.lora.LORA_IMPORT_DIR = DEAD_SHARE
        self.lora.LORA_ROOT = str(HOME_SERVER / "relay_agent.py" / "Lora")
        # Hermetic: the real one reaches kindrobots.org and the 401 it logs
        # looks exactly like the caught error we are asserting on.
        self.lora.claim_and_download = lambda: None

    def _patch_sleep(self, fake):
        patcher = mock.patch.object(time, "sleep", fake)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_dead_share_at_startup_does_not_kill_the_thread(self):
        """The original bug: FileNotFoundError escaped watch_loop entirely."""
        sleeps = []

        def fake_sleep(seconds):
            sleeps.append(seconds)
            raise Stop

        self._patch_sleep(fake_sleep)
        with self.assertRaises(Stop):
            self.lora.watch_loop()

        # Reaching the sleep means the loop body caught the OSError and is
        # going round again -- not that the thread unwound.
        self.assertEqual(len(sleeps), 1)
        self.assertTrue(
            any("error" in line.lower() for line in self.logged),
            f"expected a caught-error line, got {self.logged}",
        )

    def test_the_error_is_reported_not_swallowed(self):
        def fake_sleep(_seconds):
            raise Stop

        self._patch_sleep(fake_sleep)
        with self.assertRaises(Stop):
            self.lora.watch_loop()

        errors = [line for line in self.logged if line.startswith("error:")]
        self.assertEqual(len(errors), 1, self.logged)
        self.assertIn("relay_agent.py", errors[0])

    def test_watch_start_is_announced_before_touching_the_share(self):
        """The 'watching ...' line must not depend on the share being up."""
        def fake_sleep(_seconds):
            raise Stop

        self._patch_sleep(fake_sleep)
        with self.assertRaises(Stop):
            self.lora.watch_loop()
        self.assertTrue(self.logged[0].startswith("watching "), self.logged)


class SupervisorTests(unittest.TestCase):
    def setUp(self):
        load("relay_agent")
        self.media = load("relay_media_agent")
        self.logged = []
        self.media.relay.log = lambda message: self.logged.append(str(message))

    def _patch(self, target, name, value):
        """Patch and guarantee restoration.

        `import time` / `import threading` bind the shared module object, so a
        bare `module.time.sleep = fake` is a process-wide mutation that outlives
        the test. Doing exactly that here broke an unrelated warm-up test three
        files away (2026-08-26).
        """
        patcher = mock.patch.object(target, name, value)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_a_crashing_watch_loop_is_restarted(self):
        calls = []

        def exploding_watch_loop():
            calls.append(1)
            raise FileNotFoundError(
                "[WinError 67] The network name cannot be found: 'Z:/'"
            )

        def fake_sleep(_seconds):
            if len(calls) >= 3:
                raise Stop

        self.media.lora.watch_loop = exploding_watch_loop
        self._patch(time, "sleep", fake_sleep)

        with self.assertRaises(Stop):
            self.media._supervised_lora_watch()

        self.assertEqual(len(calls), 3, "watcher should have been restarted")
        crashes = [line for line in self.logged if "crashed" in line]
        self.assertEqual(len(crashes), 3, self.logged)
        self.assertIn("WinError 67", crashes[0])
        self.assertTrue(any("restarting in" in line for line in self.logged))

    def test_a_watch_loop_that_returns_is_also_restarted(self):
        """watch_loop is infinite by contract; returning is itself a fault."""
        calls = []

        def returning_watch_loop():
            calls.append(1)

        def fake_sleep(_seconds):
            if len(calls) >= 2:
                raise Stop

        self.media.lora.watch_loop = returning_watch_loop
        self._patch(time, "sleep", fake_sleep)

        with self.assertRaises(Stop):
            self.media._supervised_lora_watch()

        self.assertTrue(
            any("returned on its own" in line for line in self.logged),
            self.logged,
        )

    def test_start_lora_watcher_uses_the_supervisor_not_the_raw_loop(self):
        """Regression guard: the thread target must stay wrapped."""
        started = {}

        class FakeThread:
            def __init__(self, target=None, name=None, daemon=None):
                started["target"] = target
                started["name"] = name

            def start(self):
                started["started"] = True

        self.media.lora.missing_config = lambda: []
        self._patch(threading, "Thread", FakeThread)
        self.media.start_lora_watcher()

        self.assertTrue(started.get("started"))
        self.assertEqual(started["name"], "lora-import")
        self.assertIs(started["target"], self.media._supervised_lora_watch)

    def test_missing_config_still_skips_the_watcher_quietly(self):
        self.media.lora.missing_config = lambda: ["LORA_ROOT"]
        self.media.start_lora_watcher()
        self.assertTrue(
            any("disabled" in line for line in self.logged), self.logged
        )


if __name__ == "__main__":
    unittest.main()
