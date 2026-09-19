"""A booting engine must not be restarted as though it were hung.

2026-09-19: this watchdog was repaired after 11 days dead and immediately drove
ComfyUI into a crash loop. pm2 reports an app `online` within seconds of
spawning the process, and the status check only skips NON-online states, so the
health probe ran against an engine that had not finished starting. ComfyUI took
167 seconds to come up that day (14:11:32 start; ComfyUI-Manager logged "All
startup tasks have been completed" at 14:14:19) against a probe budget of 20s
plus a 60s retry.

The restart that followed did not rescue a hung engine -- it killed a booting
one and started the boot over. The loop sustained itself: pm2's restart counter
went 779 -> 794 in 35 minutes, each restart re-ran ~60 custom nodes (each
spawning a desktop console, which is how it was noticed at all), and two engines
racing port 8188 meant the loser exited and was restarted again.

The watchdog already had this concept -- `$orphanGraceMinutes` spares a young
engine from the ORPHAN SWEEP -- but the probe-failure path had no equivalent,
which is exactly the inconsistency the live log caught:

    14:11:03  engine pid 25644 is not pm2's ... only 1.6 min old - inside the
              5-min grace, leaving it this tick
    14:11:14  health probe failed - restarting via pm2
"""
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "ops" / "home-server" / "healthcheck.ps1"


class StartupGraceTests(unittest.TestCase):
    def setUp(self):
        self.text = SCRIPT.read_text(encoding="utf-8")

    def test_the_grace_is_configurable_with_a_sane_default(self):
        """Must exceed a real ComfyUI boot; 167s was measured on the box."""
        self.assertIn("$engineStartupGraceMinutes = 5", self.text)
        self.assertIn("$env:ENGINE_STARTUP_GRACE_MINUTES", self.text)

    def test_a_young_engine_is_spared_before_any_restart(self):
        grace = self.text.index("-lt $engineStartupGraceMinutes")
        restart = self.text.index(
            'Write-Log "$($t.Name): health probe failed'
        )
        self.assertLess(
            grace, restart,
            "the age check must run BEFORE the restart, or it cannot prevent it",
        )

    def test_the_spared_path_continues_rather_than_restarting(self):
        block = self.text[self.text.index("A young engine is BOOTING"):]
        block = block[:block.index("health probe failed")]
        self.assertIn("still booting rather than hung", block)
        self.assertIn("continue", block)
        self.assertNotIn("Restart-Supervised", block)

    def test_it_reads_the_age_of_pm2s_own_engine(self):
        """Any other pid would measure an orphan, not the supervised process."""
        block = self.text[self.text.index("A young engine is BOOTING"):]
        block = block[:block.index("health probe failed")]
        self.assertIn('ProcessId = $pm2Pid', block)
        self.assertIn("CreationDate", block)

    def test_the_incident_is_recorded_where_the_next_reader_will_be(self):
        """A bare age check invites a future 'why is this here?' removal."""
        block = self.text[self.text.index("A young engine is BOOTING"):]
        block = block[:block.index("health probe failed")]
        self.assertIn("167", block)
        self.assertIn("779", block)

    def test_no_undelimited_variable_before_a_colon(self):
        """The 2026-09-08 parse error, re-checked on the lines just added."""
        offenders = []
        for lineno, line in enumerate(self.text.splitlines(), start=1):
            if line.lstrip().startswith("#"):
                continue
            for match in re.finditer(r"\$([A-Za-z_][A-Za-z0-9_]*):", line):
                if match.group(1).lower() in {
                    "env", "script", "global", "local", "private", "using",
                    "variable", "function", "alias", "workflow",
                }:
                    continue
                offenders.append(f"line {lineno}: {match.group(0)}")
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
