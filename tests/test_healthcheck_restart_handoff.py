"""Contract tests for serialized ComfyUI watchdog restarts.

The render host has repeatedly ended up with two ComfyUI engines fighting for
port 8188 because PM2 on Windows can return from a restart after its kill timed
out and immediately launch a replacement. The health watchdog used to start the
replacement first and reap the survivor eight seconds later. That made overlap
part of the recovery algorithm.

These tests are source-contract tests because the Linux test runner cannot
exercise Windows process control. The real PowerShell parser workflow separately
checks syntax on windows-latest.

conductor/t-185 moved Restart-Supervised and its three helpers
(Get-PortListenerPid, Test-IsComfyEngine, Get-ComfyEnginePids) out of
healthcheck.ps1 into lib/Restart-ComfySupervised.ps1, shared with
restore-shares.ps1's own post-remap comfyui restart. These tests now read
the shared lib file rather than healthcheck.ps1 itself.
"""

import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "ops" / "home-server" / "lib" / "Restart-ComfySupervised.ps1"
HEALTHCHECK_SCRIPT = REPO / "ops" / "home-server" / "healthcheck.ps1"
RESTORE_SHARES_SCRIPT = REPO / "ops" / "home-server" / "restore-shares.ps1"


class ComfyRestartHandoffTests(unittest.TestCase):
    def setUp(self):
        self.source = SCRIPT.read_text(encoding="utf-8")
        start = self.source.index("function Restart-Supervised($name, $port) {")
        self.block = self.source[start:]

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
        helper_end = self.source.index("function Restart-Supervised($name, $port) {")
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

    def test_optional_port_falls_back_to_the_targets_lookup(self):
        # healthcheck.ps1's four call sites never pass $port, relying on the
        # original $targets-array lookup; restore-shares.ps1 (no $targets)
        # passes it explicitly. Both paths must still exist.
        self.assertIn("if ($port) {", self.block)
        self.assertIn("$port = [int]$port", self.block)
        self.assertIn("$target = $targets", self.block)

    def test_healthcheck_dot_sources_the_shared_lib_before_use(self):
        healthcheck_source = HEALTHCHECK_SCRIPT.read_text(encoding="utf-8")
        dot_source = healthcheck_source.index(
            "Join-Path $PSScriptRoot 'lib\\Restart-ComfySupervised.ps1'"
        )
        # Restart-Supervised/Test-IsComfyEngine/Get-ComfyEnginePids must no
        # longer be defined directly in healthcheck.ps1 -- they come from the
        # dot-sourced lib now.
        self.assertNotIn("function Restart-Supervised", healthcheck_source)
        self.assertNotIn("function Test-IsComfyEngine", healthcheck_source)
        self.assertNotIn("function Get-ComfyEnginePids", healthcheck_source)
        self.assertNotIn("function Get-PortListenerPid", healthcheck_source)
        # $comfyDir/$comfyPython (needed by Test-IsComfyEngine) and Write-Log
        # (needed by Restart-Supervised) must both be defined before the
        # dot-source, so the shared functions resolve them correctly.
        write_log = healthcheck_source.index("function Write-Log($msg) {")
        comfy_dir = healthcheck_source.index("$comfyDir = if ($env:COMFY_DIR)")
        comfy_python = healthcheck_source.index("$comfyPython = if ($env:COMFY_BASE_PYTHON)")
        self.assertLess(write_log, dot_source)
        self.assertLess(comfy_dir, dot_source)
        self.assertLess(comfy_python, dot_source)

    def test_lib_is_ascii_only(self):
        """Same reason as healthcheck.ps1's own guard: a no-BOM script is read
        as the system ANSI codepage by Windows PowerShell 5.1, so one non-ASCII
        byte in a string literal corrupts parsing of the whole file."""
        raw = SCRIPT.read_bytes()
        bad = [(i, b) for i, b in enumerate(raw) if b > 127]
        self.assertEqual(bad, [], f"non-ASCII bytes at {bad[:5]}")

    def test_lib_braces_and_parens_balance(self):
        self.assertEqual(self.source.count("{"), self.source.count("}"))
        self.assertEqual(self.source.count("("), self.source.count(")"))

    def test_restore_shares_routes_its_restart_through_the_shared_handoff(self):
        restore_source = RESTORE_SHARES_SCRIPT.read_text(encoding="utf-8")
        dot_source = restore_source.index(
            "Join-Path $PSScriptRoot 'lib\\Restart-ComfySupervised.ps1'"
        )
        write_log = restore_source.index("function Write-Log($msg) {")
        restart_call = restore_source.index("Restart-Supervised 'comfyui' 8188")
        self.assertLess(write_log, dot_source)
        self.assertLess(dot_source, restart_call)
        # The old direct-restart shape must be gone, not just supplemented.
        self.assertNotIn("& pm2 restart comfyui", restore_source)


if __name__ == "__main__":
    unittest.main()
