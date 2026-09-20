"""Guard: no ops/home-server/*.ps1 script may call `pm2 restart|stop comfyui`
directly, outside the shared lib/Restart-ComfySupervised.ps1 handoff.

conductor/t-184 (2026-09-20) found exactly this gap by hand: restore-shares.ps1
called `& pm2 restart comfyui` directly after remapping shares at logon,
bypassing the stop/reap-verified-pids/verify-port-free/start sequence that
PR #4869 built into Restart-Supervised to close the two-engines-fighting-
over-8188 race. conductor/t-185 extracted that function (and its helpers)
into lib/Restart-ComfySupervised.ps1 so both healthcheck.ps1 and
restore-shares.ps1 could share it -- but nothing stopped a *future* script,
or a new call added straight into an existing one, from reintroducing a
direct call the same way. This is that "next manual audit" turned into CI.

lib/Restart-ComfySupervised.ps1 itself is exempt: its own `& pm2 restart
$name` / `& pm2 stop $name` calls are the shared implementation the rest of
this guard exists to force everything else through, and they are
parameterized (never a literal `comfyui`), so they would not trip the
pattern below anyway -- the exclusion is here for clarity, not because it is
load-bearing.
"""
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HOME_SERVER = REPO / "ops" / "home-server"
SHARED_LIB = HOME_SERVER / "lib" / "Restart-ComfySupervised.ps1"

# Recursive (conductor/t-185's own lesson, test_the_checker_recurses_into_subfolders):
# a non-recursive glob would silently stop covering a .ps1 moved into a subfolder.
PS1_FILES = sorted(HOME_SERVER.rglob("*.ps1"))

DIRECT_CALL = re.compile(r"pm2(\.cmd)?\s+(restart|stop)\s+comfyui\b", re.IGNORECASE)


def find_direct_calls(text):
    """Return (lineno, line) pairs for a direct pm2 restart/stop comfyui call.

    Skips comment-only lines -- several files legitimately reference the old
    `pm2 restart comfyui` shape in prose explaining why they no longer call it
    that way (healthcheck.ps1, lib/Restart-ComfySupervised.ps1's own header).
    """
    offenders = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("#"):
            continue
        if DIRECT_CALL.search(line):
            offenders.append((lineno, line.strip()))
    return offenders


class Pm2ComfyuiDirectCallGuardTests(unittest.TestCase):
    def test_ps1_files_were_found(self):
        """A glob that silently matches nothing would pass every test below."""
        self.assertTrue(PS1_FILES, "no .ps1 files found under ops/home-server")

    def test_shared_lib_exists(self):
        self.assertTrue(
            SHARED_LIB.is_file(),
            f"expected {SHARED_LIB} -- this guard's exclusion list is stale",
        )

    def test_no_direct_pm2_restart_or_stop_comfyui_outside_shared_lib(self):
        offenders = []
        for path in PS1_FILES:
            if path == SHARED_LIB:
                continue
            for lineno, line in find_direct_calls(
                path.read_text(encoding="utf-8")
            ):
                offenders.append(f"{path.relative_to(REPO)}:{lineno}: {line}")
        self.assertEqual(
            offenders, [],
            "direct `pm2 restart|stop comfyui` bypasses the safe stop/reap/"
            "verify/start handoff in lib/Restart-ComfySupervised.ps1 -- route "
            "through Restart-Supervised instead:\n" + "\n".join(offenders),
        )

    def test_the_guard_itself_catches_a_reintroduced_direct_call(self):
        """Self-test: prove find_direct_calls() actually fires, not just that
        today's files happen to be clean."""
        sample = (
            "Write-Log 'remapped shares, restarting render backend'\n"
            "& pm2 restart comfyui | Out-Null\n"
        )
        offenders = find_direct_calls(sample)
        self.assertEqual(offenders, [(2, "& pm2 restart comfyui | Out-Null")])

    def test_the_guard_ignores_comment_only_references(self):
        sample = "# used to call `pm2 restart comfyui` directly, no longer does\n"
        self.assertEqual(find_direct_calls(sample), [])

    def test_the_guard_catches_pm2_cmd_variant(self):
        sample = "& pm2.cmd stop comfyui\n"
        offenders = find_direct_calls(sample)
        self.assertEqual(offenders, [(1, "& pm2.cmd stop comfyui")])


if __name__ == "__main__":
    unittest.main()
