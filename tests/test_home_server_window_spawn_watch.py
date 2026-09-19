"""Structural guards for watch-window-spawn.ps1 and the popup triage docs.

The script cannot be executed here (no PowerShell, no Windows, no Task
Scheduler), so these lock the properties that make it safe and useful:

  * ASCII-only, for the same PowerShell 5.1 codepage reason its header states.
  * Command lines are redacted before they reach the log. AGENTS.md hard rule 15
    is about commands handed to a human who pastes the output back -- this script
    exists to be run by Silas and its log is meant to be read, so an unredacted
    `--civitai-token` in a process command line would be the exact leak that rule
    describes.
  * The README no longer documents the popup-producing registration form. That
    snippet is what put a console window on the desktop every 5 minutes while
    healthcheck-hidden.vbs sat unused in the same folder.
"""
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HOME_SERVER = REPO / "ops" / "home-server"
WATCHER = HOME_SERVER / "watch-window-spawn.ps1"
README = HOME_SERVER / "README.md"
VBS = HOME_SERVER / "healthcheck-hidden.vbs"


class WatcherScriptTests(unittest.TestCase):
    def setUp(self):
        self.raw = WATCHER.read_bytes()
        self.text = WATCHER.read_text(encoding="utf-8")

    def test_ascii_only(self):
        bad = [(i, b) for i, b in enumerate(self.raw) if b > 127]
        self.assertEqual(bad, [], f"non-ASCII bytes at {bad[:5]}")

    def test_braces_and_parens_balance(self):
        body = "\n".join(
            line for line in self.text.splitlines()
            if not line.lstrip().startswith("#")
        )
        # Naive, but enough to catch a truncated or half-edited block.
        self.assertEqual(body.count("{"), body.count("}"))
        self.assertEqual(body.count("("), body.count(")"))

    def test_every_logged_command_line_is_redacted(self):
        """No path may reach the log with a raw CommandLine."""
        self.assertIn("function Remove-Secret", self.text)
        # The three places a command line enters the log: the process info
        # cache, the scheduled-task dump, and nothing else.
        self.assertIn("Command   = Remove-Secret ([string]$cim.CommandLine)", self.text)
        self.assertIn("Remove-Secret ([string]$line).Trim()", self.text)
        # A raw CommandLine must never be assigned or printed unredacted.
        for match in re.finditer(r"\$\w+\.CommandLine", self.text):
            line_start = self.text.rfind("\n", 0, match.start()) + 1
            line = self.text[line_start:self.text.find("\n", match.start())]
            if line.lstrip().startswith("#"):
                continue
            self.assertIn(
                "Remove-Secret", line,
                f"unredacted CommandLine reaches the log: {line.strip()}",
            )

    def test_redaction_covers_the_credentials_this_box_actually_passes(self):
        """lora_import_agent.py redacts these in its own logging for a reason."""
        pattern = re.search(
            r"'\(\?i\)\(-\{1,2\}\(\?:(?P<flags>[^)]*)\)",
            self.text,
        )
        self.assertIsNotNone(pattern, "flag-style redaction regex not found")
        flags = pattern.group("flags")
        for expected in ("civitai-token", "api-key", "token", "password", "secret"):
            self.assertIn(expected, flags)
        # Env-style KEY=VALUE, which is how KR_API_TOKEN and BREVO_API_KEY appear.
        self.assertIn("TOKEN|KEY|SECRET|PASSWORD|PASSWD", self.text)

    def test_it_detects_windows_rather_than_inferring_them(self):
        """A popup is one new conhost.exe; that is the whole measurement."""
        self.assertIn("conhost.exe", self.text)
        self.assertIn("POPUP:", self.text)
        # SessionID distinguishes "on the desktop" from "structurally invisible",
        # which is what makes the session-0 advice checkable.
        self.assertIn("session $sessionId", self.text)

    def test_it_says_so_when_it_may_miss_a_flash(self):
        """The unprivileged fallback polls, so it can miss a 200ms console.

        Silently downgrading to it would produce a clean log for a box that is
        still popping windows -- the same "absence of evidence read as evidence
        of absence" failure the engine-heartbeat and container-log checks exist
        to prevent.
        """
        self.assertIn("Win32_ProcessStartTrace", self.text)
        self.assertIn("__InstanceCreationEvent", self.text)
        self.assertIn("POLLED", self.text)


class PopupTriageDocsTests(unittest.TestCase):
    def setUp(self):
        self.text = README.read_text(encoding="utf-8")

    def test_the_wrapper_exists_and_is_what_the_readme_registers(self):
        self.assertTrue(VBS.exists(), "healthcheck-hidden.vbs is missing")
        self.assertIn("healthcheck-hidden.vbs", self.text)

    def test_the_readme_no_longer_registers_the_popup_form(self):
        """The bug this fixes: the documented snippet caused the popups."""
        register = re.search(
            r"schtasks /Create /SC MINUTE /MO 5 /TN \"AI-Backends-Healthcheck\".*?```",
            self.text,
            re.S,
        )
        self.assertIsNotNone(register, "healthcheck registration snippet not found")
        snippet = register.group(0)
        self.assertIn("healthcheck-hidden.vbs", snippet)
        self.assertNotIn(
            "-File", snippet,
            "registration still points powershell.exe at the .ps1, which pops a "
            "console window on every tick",
        )

    def test_the_session_zero_shortcut_carries_its_watchdog_blind_warning(self):
        """Switching logon type is the tempting fix and can blind the watchdog.

        pm2's daemon is per-user (2026-08-27), so this must never be recommended
        without the check that the next tick still sees the apps.
        """
        self.assertIn("WATCHDOG BLIND", self.text)
        # Anchor on the new warning specifically. The README has a pre-existing,
        # unrelated passage about the same logon type (drive-letter mapping under
        # "Why you cannot just have a service fix this for you"), and matching
        # the first occurrence tested that one instead of this one.
        idx = self.text.index('Do **not** "fix" the popup by switching')
        window = self.text[idx:idx + 1200]
        self.assertIn("per-user", window)
        self.assertIn("NONE VISIBLE", window)

    def test_the_triage_section_starts_with_the_cheap_correlation(self):
        """The heartbeat line already answers this without any new tooling."""
        idx = self.text.index("Triage: two cmd windows pop up")
        # Wide enough to span the RESOLVED root-cause block added 2026-09-19
        # ahead of the original triage steps.
        section = self.text[idx:idx + 9000]
        self.assertIn("healthcheck.log", section)
        self.assertIn("tick as", section)
        # The anchoring gotcha: a real 5-minute tick need not land on :00/:05.
        self.assertIn("05:26", section)
        self.assertIn("watch-window-spawn.ps1", section)

    def test_the_wrapper_is_not_claimed_to_hide_what_it_does_not(self):
        """The false claim this file shipped on 2026-09-19 and then measured.

        The original text asserted that healthcheck-hidden.vbs's
        `shell.Run(..., 0, True)` hides PowerShell "and every child it shells
        out to". A 15-minute watch caught all three ticks of a task registered
        to the wrapper opening TWO visible session-1 consoles each -- the
        watchdog's own, and its Start-Job child's -- with the default terminal
        already set to Windows Console Host, so the terminal application was
        ruled out rather than assumed.

        Pinned because an untested claim in a runbook is worse than no claim:
        it stops the next reader from measuring.
        """
        self.assertNotIn(
            "so PowerShell and every child it shells out to (pm2.cmd, node.exe) run\non a hidden console",
            self.text,
            "the measured-false hiding claim is back in the README",
        )
        self.assertIn("MEASURED 2026-09-19, and it does NOT hide the console", self.text)
        # The session-0 evidence is what makes the logon-type advice checkable.
        self.assertIn("session 0 - session 0, not visible", self.text)

    def test_the_triage_section_records_the_confirmed_root_cause(self):
        """The popups were a parse error, not a scheduling quirk.

        Without this the section reads as an open question and the next person
        re-derives an 11-day outage from scratch.
        """
        idx = self.text.index("Triage: two cmd windows pop up")
        section = self.text[idx:idx + 9000]
        self.assertIn("parse error", section)
        self.assertIn("2147942401", section)
        self.assertIn("2026-09-08 00:36", section)


if __name__ == "__main__":
    unittest.main()
