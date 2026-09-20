"""The PowerShell parse check must actually cover every .ps1, with 5.1.

Context: healthcheck.ps1 had a parse error from 2026-09-08 to 2026-09-19 and the
render box's watchdog did nothing the entire time. No Linux-hosted check could
see it -- a parse error needs a real parser, and the runners are Linux. The
`PowerShell syntax` workflow closes that, but only while three things hold, and
each of them is a quiet way for the check to stop checking:

1. It runs on Windows with `shell: powershell` (Windows PowerShell 5.1). `pwsh`
   is PowerShell 7 and accepts syntax 5.1 rejects, so switching would let the
   exact original bug class through while still reporting green.
2. Its paths filter covers where the .ps1 files actually live. A .ps1 added
   outside `ops/home-server/` would never trigger the workflow, and nothing
   would say so.
3. The checker it invokes exists and refuses to pass on an empty file list.
"""
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
WORKFLOW = REPO / ".github" / "workflows" / "powershell-syntax.yml"
CHECKER = REPO / "ops" / "home-server" / "Test-PowerShellSyntax.ps1"


def _repo_ps1_files():
    return sorted(
        p.relative_to(REPO).as_posix()
        for p in REPO.rglob("*.ps1")
        if ".git" not in p.parts and "node_modules" not in p.parts
    )


class PowerShellSyntaxWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.doc = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
        # PyYAML parses the `on:` key as the boolean True.
        self.triggers = self.doc.get("on", self.doc.get(True))
        self.job = self.doc["jobs"]["parse"]

    def test_runs_on_windows(self):
        self.assertIn("windows", str(self.job["runs-on"]).lower())

    def test_parses_with_windows_powershell_51_not_pwsh(self):
        """`pwsh` would be PowerShell 7, which is not what the box runs."""
        shells = [s.get("shell") for s in self.job["steps"] if "shell" in s]
        self.assertIn("powershell", shells)
        self.assertNotIn(
            "pwsh", shells,
            "pwsh is PowerShell 7; the render box runs Windows PowerShell 5.1, "
            "and 7 accepts syntax 5.1 rejects",
        )

    def test_it_invokes_the_checker_that_exists(self):
        self.assertTrue(CHECKER.exists(), f"missing checker: {CHECKER}")
        runs = " ".join(s.get("run", "") for s in self.job["steps"])
        self.assertIn("Test-PowerShellSyntax.ps1", runs)

    def test_the_checker_refuses_to_pass_on_an_empty_file_list(self):
        """Otherwise a moved folder turns the check into a permanent green."""
        text = CHECKER.read_text(encoding="utf-8")
        self.assertIn("NO .ps1 FILES FOUND", text)
        self.assertIn("ParseFile", text)

    def test_the_checker_recurses_into_subfolders(self):
        """conductor/t-185: lib/Restart-ComfySupervised.ps1 lives one level
        below ops/home-server/. The workflow's own paths filter still
        triggers on it (ops/home-server/**.ps1), but the checker's own
        Get-ChildItem call must also descend into subfolders, or a .ps1 moved
        into one is a silent, permanently-green coverage hole even while the
        workflow keeps running."""
        text = CHECKER.read_text(encoding="utf-8")
        self.assertIn("-Recurse", text)

    def test_the_paths_filter_covers_every_ps1_in_the_repo(self):
        """The filter is a cost control; it must not become a coverage hole."""
        ps1_files = _repo_ps1_files()
        self.assertTrue(ps1_files, "no .ps1 files found in the repo at all")

        covered_prefixes = set()
        for event in ("push", "pull_request"):
            for pattern in self.triggers[event]["paths"]:
                if pattern.endswith(".ps1"):
                    covered_prefixes.add(pattern.split("**")[0])

        self.assertTrue(covered_prefixes, "no .ps1 path patterns in the filter")

        uncovered = [
            f for f in ps1_files
            if not any(f.startswith(prefix) for prefix in covered_prefixes)
        ]
        self.assertEqual(
            uncovered, [],
            "these .ps1 files would never trigger the parse check:\n  "
            + "\n  ".join(uncovered)
            + f"\nfilter covers: {sorted(covered_prefixes)}",
        )

    def test_the_workflow_itself_retriggers_the_check(self):
        for event in ("push", "pull_request"):
            self.assertIn(
                ".github/workflows/powershell-syntax.yml",
                self.triggers[event]["paths"],
            )


if __name__ == "__main__":
    unittest.main()
