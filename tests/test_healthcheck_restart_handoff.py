"""Contract tests for serialized ComfyUI watchdog restarts.

The render host has repeatedly ended up with two ComfyUI engines fighting for
port 8188 because PM2 on Windows can return from a restart after its kill timed
out and immediately launch a replacement. The health watchdog used to start the
replacement first and reap the survivor eight seconds later. That made overlap
part of the recovery algorithm.

These tests are source-contract tests because the Linux test runner cannot
exercise Windows process control. The real PowerShell parser workflow separately
checks syntax on windows-latest.
"""

import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "ops" / "home-server" / "healthcheck.ps1"


class ComfyRestartHandoffTests(unittest.TestCase):
    def setUp(self):
        self.source = SCRIPT.read_text(encoding="utf-8")
        start = self.source.index("function Restart-Supervised($name) {")
        end = self.source.index("function Invoke-PortReclaim($target, $expectedPid) {")
        self.block = self.source[start:end]

    def test_comfy_stops_pm2_before_starting_the_replacement(self):
        stop = self.block.index("& pm2 stop $name")
        restart = self.block.rindex("& pm2 restart $name")
        self.assertLess(stop, restart)
        self.assertIn("REFUSING to start a replacement", self.block)

    def test_surviving_old_engines_are_reaped_before_replacement_launch(self):
        reap = self.block.index("force-killing surviving old engine")
        restart = self.block.rindex("& pm2 restart $name")
        self.assertLess(reap, restart)
        self.assertIn("Stop-Process -Id $oldPid -Force", self.block)

    def test_old_engine_death_is_verified_not_inferred_from_a_free_port(self):
        verify = self.block.index("$oldEnginesGone = $false")
        refusal = self.block.index("old ComfyUI pid(s) are still alive after cleanup")
        restart = self.block.rindex("& pm2 restart $name")
        self.assertLess(verify, refusal)
        self.assertLess(refusal, restart)
        self.assertIn("$remaining = @(Get-ComfyEnginePids $port)", self.block)

    def test_port_must_be_free_before_replacement_launch(self):
        port_check = self.block.index("$portReleased = $false")
        restart = self.block.rindex("& pm2 restart $name")
        self.assertLess(port_check, restart)
        self.assertIn("if (-not $portReleased)", self.block)
        self.assertIn("REFUSING safe restart - port $port is still occupied", self.block)

    def test_unrelated_port_owner_is_never_killed_or_started_over(self):
        self.assertIn(
            "port $port is held by unrelated pid $ownerPid; starting ComfyUI would only crash-loop",
            self.block,
        )
        owner_guard = self.block.index("if (Test-IsComfyEngine $owner $port)")
        refusal = self.block.index("starting ComfyUI would only crash-loop")
        restart = self.block.rindex("& pm2 restart $name")
        self.assertLess(owner_guard, refusal)
        self.assertLess(refusal, restart)

    def test_engine_process_filter_is_scoped_to_the_comfy_port(self):
        helper_start = self.source.index("function Get-ComfyEnginePids($port) {")
        helper_end = self.source.index("function Restart-Supervised($name) {")
        helper = self.source[helper_start:helper_end]
        self.assertIn("Test-IsComfyEngine $_ $port", helper)
        self.assertIn("--port", helper)

    def test_non_comfy_apps_keep_the_simple_pm2_restart_path(self):
        prefix = self.block[: self.block.index("$target = $targets")]
        self.assertIn("if ($name -ne 'comfyui')", prefix)
        self.assertIn("& pm2 restart $name", prefix)
        self.assertIn("return", prefix)

    def test_replacement_is_not_treated_as_ready_after_eight_seconds(self):
        self.assertIn("normal startup-grace logic owns readiness", self.block)
        self.assertIn("Start-Sleep -Seconds 8", self.block)
        self.assertNotIn("Invoke-WebRequest", self.block)


if __name__ == "__main__":
    unittest.main()
