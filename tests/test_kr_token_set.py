"""Regression test for scripts/kr_token_set.sh.

The script is documented (AGENTS.md) as the safe way to check whether
KR_API_TOKEN is set: `source scripts/kr_token_set.sh` before running a
command that needs the token. Sourcing a script that calls plain `exit`
terminates the *calling* shell outright, silently discarding any command
chained after the `source` in the same invocation (conductor, 2026-09-15).
This pins the fix: sourcing must return to the caller, not exit it, in
both the token-set and token-unset cases, while `exit` (with the correct
status) must still fire when the script is executed directly.
"""

import subprocess
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "kr_token_set.sh"


def run_sourced(token_set: bool) -> subprocess.CompletedProcess:
    env_line = "export KR_API_TOKEN=dummy" if token_set else "unset KR_API_TOKEN"
    script = f"""
{env_line}
source '{SCRIPT}'
echo "REACHED_AFTER_SOURCE status=$?"
"""
    return subprocess.run(
        ["bash", "-c", script], capture_output=True, text=True, timeout=10
    )


def run_executed(token_set: bool) -> subprocess.CompletedProcess:
    env_line = "export KR_API_TOKEN=dummy" if token_set else "unset KR_API_TOKEN"
    script = f"""
{env_line}
'{SCRIPT}'
echo "exit=$?"
"""
    return subprocess.run(
        ["bash", "-c", script], capture_output=True, text=True, timeout=10
    )


class TestKrTokenSetSourcing(unittest.TestCase):
    def test_sourced_with_token_returns_to_caller(self):
        result = run_sourced(token_set=True)
        self.assertIn("KR_API_TOKEN: set", result.stdout)
        self.assertIn("REACHED_AFTER_SOURCE status=0", result.stdout)

    def test_sourced_without_token_returns_to_caller(self):
        result = run_sourced(token_set=False)
        self.assertIn("KR_API_TOKEN: not set", result.stdout)
        self.assertIn("REACHED_AFTER_SOURCE status=1", result.stdout)

    def test_executed_with_token_exits_zero(self):
        result = run_executed(token_set=True)
        self.assertIn("KR_API_TOKEN: set", result.stdout)
        self.assertIn("exit=0", result.stdout)

    def test_executed_without_token_exits_nonzero(self):
        result = run_executed(token_set=False)
        self.assertIn("KR_API_TOKEN: not set", result.stdout)
        self.assertIn("exit=1", result.stdout)

    def test_never_prints_token_value(self):
        result = run_sourced(token_set=True)
        self.assertNotIn("dummy", result.stdout)
        self.assertNotIn("dummy", result.stderr)


if __name__ == "__main__":
    unittest.main()
