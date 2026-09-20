"""The orphan sweep must run in the states that CREATE orphans.

2026-09-20. ComfyUI restarted 89 times without pm2 ever giving up, while a
survivor from a failed kill held port 8188. From that day's healthcheck.log:

    12:26:03  comfyui: CRASH LOOPING - restart count climbed 82->86
    12:26:03  comfyui: nothing is listening on port 8188
    12:31:06  comfyui: ORPHAN SWEEP - killing engine pid 20492
    12:36:03  comfyui: pm2 status is 'waiting restart' - in transition

Two independent defects kept that loop alive, and both are locked here.

1. ORDERING. `Invoke-OrphanSweep` sat at the BOTTOM of the per-target loop,
   below four branches that `continue`: crash-looping, errored, stopped, and
   any status that is not 'online'. It therefore ran only when pm2 read
   'online' AND the restart counter was calm -- never in the states that
   actually produce orphans. The 12:31 sweep above fired by luck; 12:26 and
   12:36 skipped it entirely.

2. THE pid-0 EARLY RETURN. The sweep began `if (-not $expectedPid) { return }`,
   and pm2 reports pid 0 for the whole of 'waiting restart', which is most of a
   crash loop. So it stood down in precisely the state that stacks engines --
   and the stale engine it declined to kill was the thing blocking pm2's next
   start.

PowerShell cannot run in CI, so these lock the structure the fix depends on.
"""
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HEALTHCHECK = REPO / "ops" / "home-server" / "healthcheck.ps1"
ECOSYSTEM = REPO / "ops" / "home-server" / "ecosystem.config.js"

# The boot measured on 2026-09-20: 12:36:03 -> bind attempt 12:39:57.
MEASURED_BOOT_SECONDS = 234


class OrphanSweepOrderingTests(unittest.TestCase):
    def setUp(self):
        self.source = HEALTHCHECK.read_text(encoding="utf-8")

    def call_site(self):
        """The invocation inside the per-target loop, not the definition."""
        sites = [
            m.start()
            for m in re.finditer(r"^\s*Invoke-OrphanSweep \$t ", self.source, re.M)
        ]
        self.assertEqual(
            len(sites), 1, "expected exactly one sweep call inside the target loop"
        )
        return sites[0]

    def test_sweep_runs_before_the_crash_loop_branch(self):
        crash_loop = self.source.index("CRASH LOOPING - pm2 restart count climbed")
        self.assertLess(
            self.call_site(),
            crash_loop,
            "the sweep must run before the crash-loop branch, which continues past it",
        )

    def test_sweep_runs_before_every_branch_that_continues(self):
        """errored / stopped / not-online all `continue`, so all must come after."""
        for marker in (
            "pm2 has GIVEN UP restarting it",
            "deliberate, leaving it alone",
            "in transition, probing next tick",
        ):
            with self.subTest(branch=marker):
                self.assertLess(
                    self.call_site(),
                    self.source.index(marker),
                    f"the sweep must run before the branch logging {marker!r}",
                )

    def test_only_a_deliberate_stop_is_exempt(self):
        """A `pm2 stop` to free the GPU must never be fought; nothing else is
        allowed to gate the sweep."""
        guard = self.source[self.call_site() - 200 : self.call_site()]
        self.assertIn("-ne 'stopped'", guard)
        self.assertNotIn("-eq 'online'", guard)

    def test_sweep_does_not_stand_down_when_pm2_owns_no_engine(self):
        """pm2 reports pid 0 through 'waiting restart'. An early return there
        is the pid-0 hole."""
        body = self.source[self.source.index("function Invoke-OrphanSweep") :]
        body = body[: body.index("\nfunction ")]
        self.assertNotIn(
            "if (-not $expectedPid) { return }",
            body,
            "a falsy pm2 pid must not abort the sweep -- that is the crash-loop state",
        )
        self.assertIn("$keeperPid", body, "the sweep must track a preserve-pid explicitly")

    def test_grace_period_exceeds_a_real_boot(self):
        match = re.search(r"^\$orphanGraceMinutes = (\d+)", self.source, re.M)
        self.assertIsNotNone(match)
        grace_seconds = int(match.group(1)) * 60
        self.assertGreater(
            grace_seconds,
            MEASURED_BOOT_SECONDS,
            "a grace shorter than a boot sweeps engines that are merely still starting",
        )


class Pm2CalibrationTests(unittest.TestCase):
    """min_uptime below the boot time made the loop infinite: every doomed
    start scored STABLE, so pm2 never reached 'errored' -- the one state
    healthcheck.ps1 treats as its cue to reclaim the port."""

    def setUp(self):
        source = ECOSYSTEM.read_text(encoding="utf-8")
        block = source[source.index("name: 'comfyui'") :]
        self.block = block[: block.index("out_file")]

    def value(self, key):
        match = re.search(rf"^\s*{key}: (\d+),", self.block, re.M)
        self.assertIsNotNone(match, f"{key} not found in the comfyui app block")
        return int(match.group(1))

    def test_min_uptime_is_above_a_measured_boot(self):
        self.assertGreater(self.value("min_uptime") / 1000, MEASURED_BOOT_SECONDS)

    def test_pm2_gives_up_in_a_useful_amount_of_time(self):
        """Parking in 'errored' is the recovery cue, so it has to arrive while
        somebody still cares. 50 doomed boots is over three hours."""
        self.assertLessEqual(self.value("max_restarts"), 10)

    def test_kill_timeout_survives_a_slow_import(self):
        """A failed kill leaves the survivor that starts the whole loop."""
        self.assertGreaterEqual(self.value("kill_timeout") / 1000, 60)


if __name__ == "__main__":
    unittest.main()
