"""Structural guards for healthcheck.ps1 and extra_model_paths.yaml.

Neither can be executed here (no PowerShell, no Windows, no Z: share), so
these lock the properties that were load-bearing in the 2026-08-25/26 outages
and that a well-meaning edit would quietly undo.
"""
import re
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
PS1 = REPO / "ops" / "home-server" / "healthcheck.ps1"
YML = REPO / "ops" / "home-server" / "extra_model_paths.yaml"


class HealthcheckScriptTests(unittest.TestCase):
    def setUp(self):
        self.raw = PS1.read_bytes()
        self.text = PS1.read_text(encoding="utf-8")

    def test_ascii_only(self):
        """The script's own header demands this, and for a real reason.

        Windows PowerShell 5.1 reads a no-BOM script as the system ANSI
        codepage, so a single em-dash or smart quote inside a string literal
        corrupts parsing of the whole file.
        """
        bad = [(i, b) for i, b in enumerate(self.raw) if b > 127]
        self.assertEqual(bad, [], f"non-ASCII bytes at {bad[:5]}")

    def test_braces_and_parens_balance(self):
        self.assertEqual(self.text.count("{"), self.text.count("}"))
        self.assertEqual(self.text.count("("), self.text.count(")"))

    def test_share_watchdog_runs_before_the_render_watchdog(self):
        """Ordering is the whole design.

        The render watchdog reads $shareOk. If the share block ran after it,
        $shareOk would be unset and the guard would silently pass, restarting
        comfyui into a dead mount -- the exact behaviour this replaces.
        """
        share = self.text.index("--- Share watchdog")
        render = self.text.index("--- Render-failure watchdog")
        self.assertLess(share, render)
        self.assertLess(share, self.text.index("foreach ($t in $targets)"))

    def test_render_restart_is_suppressed_while_the_share_is_down(self):
        self.assertIn("if (-not $shareOk) {", self.text)
        guard = self.text.index("if (-not $shareOk) {", self.text.index("--- Render-failure watchdog"))
        restart = self.text.index("Test-AlertDue $alertState 'render-watchdog-restart'")
        self.assertLess(guard, restart, "the $shareOk guard must precede the restart branch")

    def test_share_probe_enumerates_rather_than_stat_ing(self):
        """Test-Path is satisfied by a stale SMB handle that fails every read."""
        body = self.text[self.text.index("function Test-ShareReadable"):]
        body = body[: body.index("function Repair-ShareMapping")]
        # Comments here explain *why* Test-Path is wrong, so strip them before
        # asserting the code does not actually call it.
        code = "\n".join(
            line for line in body.splitlines() if not line.lstrip().startswith("#")
        )
        self.assertIn("Get-ChildItem", code)
        self.assertNotIn("Test-Path", code)

    def test_recovery_restarts_comfyui_for_the_folder_paths_cache(self):
        """Remapping the drive is not enough; the cache survives the outage."""
        self.assertIn("share is back - restarting comfyui", self.text)
        self.assertIn("folder_paths", self.text)

    def test_net_use_cannot_block_on_a_credential_prompt(self):
        """A Task Scheduler run has no console to answer a username prompt."""
        for call in re.findall(r'"net use [^"]*"', self.text):
            self.assertIn("< NUL", call, f"unredirected stdin in: {call}")

    def test_pm2_is_read_once_not_per_target(self):
        """Three `pm2 jlist` calls per tick, each able to fail silently."""
        code = [
            line for line in self.text.splitlines()
            if not line.lstrip().startswith("#")
        ]
        calls = sum(line.count("& pm2 jlist") for line in code)
        self.assertEqual(calls, 1, "pm2 must be read once per tick")

    def test_an_invisible_pm2_is_loud_not_silent(self):
        """The bug that made this watchdog useless.

        `pm2 jlist` returning nothing looked identical to "the app is
        deliberately stopped", so on 2026-08-27 the task ran every 5 minutes
        and exited 0 while ComfyUI was dead. pm2's daemon is per-user and the
        task may not share the session or the PATH.
        """
        self.assertIn("$pm2Visible", self.text)
        self.assertIn("WATCHDOG BLIND", self.text)
        blind = self.text.index("if (-not $pm2Visible) {")
        loop = self.text.index("foreach ($t in $targets)")
        self.assertLess(blind, loop, "the blindness check must precede the loop")

        # And the loop itself must bail, not just the alert above it.
        body = self.text[loop : self.text.index("--- Render-failure watchdog")]
        self.assertIn(
            "if (-not $pm2Visible) { continue }",
            body,
            "the target loop must skip when pm2 is invisible",
        )

    def test_every_tick_writes_a_heartbeat(self):
        """A silent log cannot answer 'did the watchdog actually run?'."""
        self.assertIn('Write-Log "tick as $($env:USERNAME)', self.text)

    def test_the_heartbeat_log_is_trimmed(self):
        self.assertIn("function Trim-Log", self.text)
        self.assertTrue(self.text.rstrip().endswith("Trim-Log"))

    def test_share_state_is_persisted_both_ways(self):
        self.assertIn("$alertState['share_state'] = 'ok'", self.text)
        self.assertIn("$alertState['share_state'] = 'down'", self.text)

    def test_down_alert_is_cooldown_gated(self):
        self.assertIn("Test-AlertDue $alertState 'share-watchdog'", self.text)


class ExtraModelPathsTests(unittest.TestCase):
    def setUp(self):
        self.doc = yaml.safe_load(YML.read_text(encoding="utf-8"))
        self.comfy = self.doc["comfyui"]
        self.keys = {
            k: v.split()
            for k, v in self.comfy.items()
            if isinstance(v, str) and k != "base_path"
        }

    def test_parses_and_has_a_base_path(self):
        self.assertIn("base_path", self.comfy)
        self.assertTrue(self.comfy["base_path"])

    def test_no_case_insensitive_duplicates_within_a_key(self):
        """SMB is case-insensitive, so models/VAE and models/vae are one dir.

        Declaring both made ComfyUI scan it twice and list every file twice in
        the node dropdowns. Each path here is a directory scan across SMB on
        every folder_paths refresh -- the same I/O that fails first when the
        mount degrades.
        """
        for key, paths in self.keys.items():
            lowered = [p.lower() for p in paths]
            dupes = {p for p in lowered if lowered.count(p) > 1}
            self.assertEqual(dupes, set(), f"{key} declares {dupes} more than once")

    def test_no_singular_model_typo(self):
        """`model/LLM` (singular) silently resolved to nothing for months."""
        for key, paths in self.keys.items():
            for path in paths:
                self.assertFalse(
                    path.startswith("model/"),
                    f"{key}: {path!r} should be 'models/', not 'model/'",
                )

    def test_paths_use_forward_slashes(self):
        for key, paths in self.keys.items():
            for path in paths:
                self.assertNotIn("\\", path, f"{key}: {path!r}")

    def test_clip_alias_and_text_encoders_agree(self):
        """node 3 (CLIPTextEncode) resolves through the legacy `clip` key."""
        self.assertIn("models/text_encoders", self.keys["clip"])
        self.assertIn("models/text_encoders", self.keys["text_encoders"])

    def test_every_key_declares_at_least_one_path(self):
        for key, paths in self.keys.items():
            self.assertTrue(paths, f"{key} declares no paths")


if __name__ == "__main__":
    unittest.main()
