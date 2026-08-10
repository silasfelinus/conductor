import importlib.util
import unittest
import urllib.error
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "process_task_events.py"
SPEC = importlib.util.spec_from_file_location("process_task_events_pr_check", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class CheckPrMergedTests(unittest.TestCase):
    def test_404_reports_missing_or_invisible_pr_reference(self):
        original = MODULE.urllib.request.urlopen

        def raise_404(request, timeout=15):
            raise urllib.error.HTTPError(
                request.full_url,
                404,
                "Not Found",
                hdrs=None,
                fp=None,
            )

        MODULE.urllib.request.urlopen = raise_404
        try:
            with self.assertRaisesRegex(
                RuntimeError,
                r"verify_pr references silasfelinus/kind_robots#99999, but GitHub returned 404; "
                r"the PR or repository does not exist or is not visible to this token",
            ):
                MODULE.check_pr_merged("silasfelinus/kind_robots", 99999)
        finally:
            MODULE.urllib.request.urlopen = original

    def test_non_http_network_failure_keeps_reachability_error(self):
        original = MODULE.urllib.request.urlopen

        def fail_network(request, timeout=15):
            raise urllib.error.URLError("temporary resolver failure")

        MODULE.urllib.request.urlopen = fail_network
        try:
            with self.assertRaisesRegex(
                RuntimeError,
                r"could not reach GitHub API for silasfelinus/conductor#2033",
            ):
                MODULE.check_pr_merged("silasfelinus/conductor", 2033)
        finally:
            MODULE.urllib.request.urlopen = original


if __name__ == "__main__":
    unittest.main()
