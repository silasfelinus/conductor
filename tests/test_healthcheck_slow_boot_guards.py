"""A slow boot must not make the watchdog fire early, or stop it firing at all.

Two failure shapes, both observed on this box, both caused by a guard whose
threshold was pinned to a boot time that moves.

EARLY FIRE (2026-09-19, in healthcheck.ps1's own comments): the watchdog was
repaired after 11 days dead and "immediately drove ComfyUI into a crash loop".
pm2 reports 'online' seconds after spawning, so the probe ran against an engine
still booting; past the startup grace a failed probe reads as "hung" and the
engine is restarted -- which does not rescue a booting engine, it kills one and
starts the boot over. ComfyUI took 167 seconds to come up that day. On
2026-09-20 it took 234, with 201.7s of that one custom node scanning ~2,200
LoRA files over SMB. A fixed grace only postpones this.

NEVER FIRES: $crashLoopRestarts needs 3 restarts INSIDE one 5-minute tick. At a
234-second boot pm2 manages about 1.25, so the per-tick gate is inversely
sensitive to boot time -- the slower the boot, the less likely it detects the
loop. It fired on 2026-09-20 only because that stretch cycled at ~75s.

PowerShell cannot run in CI, so these lock the structure the fixes depend on.
"""
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HEALTHCHECK = REPO / "ops" / "home-server" / "healthcheck.ps1"

MEASURED_BOOT_SECONDS = 234


class ProgressBasedGraceTests(unittest.TestCase):
    def setUp(self):
        self.source = HEALTHCHECK.read_text(encoding="utf-8")

    def test_progress_is_measured_by_io_not_only_cpu(self):
        """An engine blocked on an SMB read burns almost no CPU while its I/O
        counters climb. CPU alone cannot tell that from a wedge -- and the SMB
        walk is the whole reason the boot is slow."""
        body = self.source[self.source.index("function Get-EngineProgress") :]
        body = body[: body.index("\nfunction ")]
        for counter in ("ReadOperationCount", "WriteOperationCount", "OtherOperationCount"):
            with self.subTest(counter=counter):
                self.assertIn(counter, body)
        self.assertIn("KernelModeTime", body)

    def test_progress_is_sampled_before_the_branches_that_continue(self):
        """Without a baseline recorded on ticks that `continue` early, the
        comparison below has nothing to compare against."""
        self.assertLess(
            self.source.index("$nowProgress = Get-EngineProgress"),
            self.source.index("CRASH LOOPING - pm2 restart count climbed"),
        )

    def test_progress_comparison_requires_the_same_pid(self):
        """A changed pid means a restart happened, which says nothing about
        whether the current engine is doing work."""
        window = self.source[
            self.source.index("$nowProgress = Get-EngineProgress") : self.source.index(
                "$slowLoopKey"
            )
        ]
        self.assertIn("Split('|')[0]", window)

    def test_a_working_engine_past_the_grace_is_not_restarted(self):
        """The early-fire fix: past the floor, ask whether it is doing anything
        rather than how old it is."""
        probe = self.source[self.source.index("health probe failed") - 3000 :]
        guard = probe[: probe.index("health probe failed")]
        self.assertIn("$engineMadeProgress", guard)
        self.assertIn("$engineStartupCeilingMinutes", guard)

    def test_the_extension_is_bounded_by_a_ceiling_above_the_floor(self):
        """A livelock must not buy grace forever."""
        floor = int(re.search(r"^\$engineStartupGraceMinutes = (\d+)", self.source, re.M).group(1))
        ceiling = int(
            re.search(r"^\$engineStartupCeilingMinutes = (\d+)", self.source, re.M).group(1)
        )
        self.assertGreater(ceiling, floor)
        self.assertGreater(
            ceiling * 60,
            MEASURED_BOOT_SECONDS * 2,
            "the ceiling must clear a boot that runs well over the measured one",
        )


class SlowCrashLoopTests(unittest.TestCase):
    def setUp(self):
        self.source = HEALTHCHECK.read_text(encoding="utf-8")

    def test_the_crash_loop_branch_also_fires_on_a_slow_loop(self):
        match = re.search(
            r"^\s*if \(\$restartDelta -ge \$crashLoopRestarts.*$", self.source, re.M
        )
        self.assertIsNotNone(match, "the crash-loop branch condition moved")
        self.assertIn(
            "$slowLoopTripped",
            match.group(0),
            "a loop too slow for the per-tick gate is still a loop",
        )

    def test_consecutive_restarting_ticks_are_counted_and_reset(self):
        """An ordinary deploy restarts once: it must never accumulate."""
        window = self.source[
            self.source.index("$slowLoopKey") : self.source.index("CRASH LOOPING - pm2 restart")
        ]
        self.assertIn("$slowLoopCount++", window)
        self.assertIn("$slowLoopCount = 0", window)

    def test_the_slow_loop_threshold_spans_more_than_one_tick(self):
        threshold = int(re.search(r"^\$slowLoopTicks = (\d+)", self.source, re.M).group(1))
        self.assertGreaterEqual(
            threshold, 2, "one restarting tick is a deploy, not a loop"
        )


if __name__ == "__main__":
    unittest.main()
