"""A slow-booting engine cannot be judged on a stopwatch the tick is holding.

2026-09-20, from the alert Silas received:

    The comfyui backend stopped answering http://127.0.0.1:8188/system_stats;
    the watchdog ran 'pm2 restart comfyui' at 2026-09-20 14:27:57 but it is
    still not responding.

From healthcheck.log, the replacement was launched at 14:27:44 and the email
went out at 14:27:57 -- thirteen seconds later, against an engine whose
measured boot is ~234 seconds. The old code slept 8 seconds, probed once, and
called anything that did not answer "restart did not recover". For this app
that answer was structurally always the same, so the verdict carried no
information and the alert cried wolf on every watchdog restart.

The real cause that day was ordinary: Silas was copying ~2,200 LoRA files off
the model share, so ComfyUI's boot-time folder_paths scan crawled. The right
response was to leave the app stopped, which a false DOWN alert actively
obscures.

Recovery is now judged on a LATER tick by the startup-grace and progress logic
that already knows how to wait, and DOWN is sent only once a restart has been
given a full grace and still failed.

PowerShell cannot run in CI, so these lock the structure the fix depends on.
"""
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HEALTHCHECK = REPO / "ops" / "home-server" / "healthcheck.ps1"

MEASURED_BOOT_SECONDS = 234


def _code(text: str) -> str:
    """Drop whole-line comments.

    This file documents the broken code it replaced, so a bare
    `"<old string>" not in source` check matches the explanation rather than a
    regression. Exactly this bit the restart-trend tests earlier the same day.
    """
    return "\n".join(
        line for line in text.splitlines() if not line.lstrip().startswith("#")
    )


class RestartVerdictTests(unittest.TestCase):
    def setUp(self):
        self.source = HEALTHCHECK.read_text(encoding="utf-8")

    def _restart_block(self):
        start = self.source.index("health probe failed ($($t.Url)) - restarting via pm2")
        return self.source[start : start + 4000]

    def test_no_stopwatch_verdict_after_the_restart(self):
        """Nothing in the restart path may sleep a few seconds and then decide
        whether a minutes-long boot succeeded."""
        block = self._restart_block()
        sleeps = re.findall(r"Start-Sleep -Seconds (\d+)", block)
        for seconds in sleeps:
            self.assertGreater(
                int(seconds) * 1,
                MEASURED_BOOT_SECONDS,
                "a sleep shorter than a boot cannot decide recovery; judge on a later tick",
            )

    def test_the_verdict_is_deferred_to_a_later_tick(self):
        block = self._restart_block()
        self.assertIn("$pendingKey", block)
        self.assertIn("restartpending_", block)
        self.assertIn("judged on a later tick", block)

    def test_down_is_only_sent_after_a_restart_was_given_a_real_chance(self):
        """The old alert fired on the first restart. It must now require that a
        PREVIOUS watchdog restart already failed."""
        block = self._restart_block()
        down = block.index("DOWN: $($t.Name) on $hostName")
        guard = block[:down]
        self.assertIn("$priorPending", guard)
        # The OLD subject line exactly. The replacement reads "a previous
        # watchdog restart did not recover it", which legitimately contains the
        # shorter phrase - so match the full old subject, not a fragment of it.
        self.assertNotIn(
            "$hostName - restart did not recover",
            _code(block),
            "the unconditional first-restart DOWN alert is back",
        )

    def test_a_recovered_engine_clears_the_pending_verdict(self):
        """Otherwise the next real failure reads as a repeat and alerts wrongly."""
        self.assertIn("RECOVERED: $($t.Name) on $hostName is answering again", self.source)
        recovered = self.source.index("the watchdog restart at $pendingSince recovered it")
        window = self.source[recovered : recovered + 400]
        self.assertIn("$alertState[$pendingKey] = ''", window)

    def test_the_down_alert_names_the_share_and_the_stop_remedy(self):
        """A boot that hangs rather than crashes leaves no error line, and the
        correct move is to stop the app rather than let it cycle."""
        block = self._restart_block()
        self.assertIn("folder_paths", block)
        self.assertIn("pm2 stop", block)


class ElseStyleTests(unittest.TestCase):
    def test_no_newline_else(self):
        """PowerShell parses `}` / newline / `else` inconsistently enough that
        this file uses `} else {` throughout; a parse error here takes the whole
        watchdog down silently (2026-09-19, eleven days dead)."""
        source = HEALTHCHECK.read_text(encoding="utf-8")
        self.assertEqual(
            len(re.findall(r"^\s*else\s*\{", source, re.M)),
            0,
            "put else on the closing brace, as the rest of this file does",
        )


if __name__ == "__main__":
    unittest.main()
