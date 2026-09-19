"""Guard against `"$var:"` inside a double-quoted PowerShell string.

This is a PARSE error, not a runtime one, so it does not fail the line it is on
-- it stops the whole file from loading. `healthcheck.ps1` carried three of them
and the render box's watchdog silently did nothing from 2026-09-08 00:36 until
2026-09-19: every 5-minute trigger launched, PowerShell refused to parse the
script, the action returned exit code 1 (Task Scheduler logged
`2147942401` = `HRESULT_FROM_WIN32(1)`), and the log recorded nothing at all
because no line of the script ever executed. Task Scheduler went on reporting a
healthy NextRunTime throughout.

PowerShell reads `$name:` as a scope- or drive-qualified variable, the same
syntax as `$env:PATH` or `$script:foo`. Only the qualifiers below are real; any
other identifier before the colon raises
`InvalidVariableReferenceWithDrive`. The fix is `${name}:`, which delimits the
variable so the colon is literal text.

The sibling guards in test_home_server_share_watchdog.py check ASCII-only bytes
and brace balance. Neither catches this, because the file is valid ASCII and
perfectly balanced -- it just does not parse.
"""
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PS1_FILES = sorted((REPO / "ops" / "home-server").glob("*.ps1"))

# Scope modifiers and PowerShell drive qualifiers that legitimately precede a
# colon in a variable reference.
VALID_QUALIFIERS = {
    "env", "script", "global", "local", "private", "using",
    "variable", "function", "alias", "workflow",
}

QUALIFIED = re.compile(r"\$([A-Za-z_][A-Za-z0-9_]*):")


class PowerShellInterpolationTests(unittest.TestCase):
    def test_ps1_files_were_found(self):
        """A glob that silently matches nothing would pass every test below."""
        self.assertTrue(PS1_FILES, "no .ps1 files found under ops/home-server")

    def test_no_undelimited_variable_before_a_colon(self):
        offenders = []
        for path in PS1_FILES:
            for lineno, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                if line.lstrip().startswith("#"):
                    continue
                for match in QUALIFIED.finditer(line):
                    if match.group(1).lower() in VALID_QUALIFIERS:
                        continue
                    offenders.append(
                        f"{path.name}:{lineno}: {match.group(0)} -- "
                        f"use ${{{match.group(1)}}}: instead\n    {line.strip()}"
                    )
        self.assertEqual(
            offenders, [],
            "undelimited $var: parses as a qualified variable and breaks the "
            "WHOLE file:\n" + "\n".join(offenders),
        )

    def test_the_three_healthcheck_lines_stay_fixed(self):
        """The exact regression: Restart-Supervised's orphan-sweep logging."""
        text = (REPO / "ops" / "home-server" / "healthcheck.ps1").read_text(
            encoding="utf-8"
        )
        self.assertNotIn('"$name:', text)
        self.assertEqual(text.count('"${name}:'), 3)


if __name__ == "__main__":
    unittest.main()
