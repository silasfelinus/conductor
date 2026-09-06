import json
import shutil
import subprocess
from pathlib import Path

import pytest


HELPER = Path(__file__).resolve().parents[1] / "ops" / "home-server" / "pm2-jlist-snapshot.js"
NODE = shutil.which("node")


def run_helper(payload: str) -> subprocess.CompletedProcess[str]:
    if NODE is None:
        pytest.skip("node is not available in this test environment")
    return subprocess.run(
        [NODE, str(HELPER)],
        input=payload,
        text=True,
        capture_output=True,
        check=False,
    )


def test_projects_only_safe_pm2_fields_when_environment_keys_differ_only_by_case():
    payload = json.dumps(
        [
            {
                "name": "comfyui",
                "pid": 123,
                "pm2_env": {
                    "status": "online",
                    "env": {
                        "username": "lower-case-value",
                        "USERNAME": "upper-case-value",
                    },
                },
            }
        ]
    )

    result = run_helper(payload)

    assert result.returncode == 0, result.stderr
    # restart_time/unstable_restarts were added 2026-09-02 so the watchdog can
    # detect a crash loop, which status alone cannot express. pid was added
    # 2026-09-06 so it can also answer "is the process holding port 8188 the one
    # pm2 is supervising?" -- the diagnosis a crash loop caused by a port
    # collision needs. The projection is still an explicit allowlist -- that is
    # the point of this test -- so the env (and its username/USERNAME collision)
    # must stay out of it.
    assert json.loads(result.stdout) == [
        {
            "name": "comfyui",
            "pid": 123,
            "pm2_env": {
                "status": "online",
                "restart_time": None,
                "unstable_restarts": None,
            },
        }
    ]
    assert "username" not in result.stdout.lower()


def test_missing_or_unusable_pid_becomes_null():
    # pm2 omits pid for an app it is running no process for (a stopped or
    # errored one) and has been seen to report it as a string. Either way the
    # watchdog must get null rather than a value it would compare against a
    # real port owner and wrongly call a match.
    payload = json.dumps(
        [
            {"name": "comfyui", "pm2_env": {"status": "errored"}},
            {"name": "kr-relay", "pid": "4242", "pm2_env": {"status": "online"}},
        ]
    )

    result = run_helper(payload)

    assert result.returncode == 0, result.stderr
    snapshot = json.loads(result.stdout)
    assert [entry["pid"] for entry in snapshot] == [None, None]


def test_rejects_invalid_pm2_json():
    result = run_helper("{not-json")

    assert result.returncode == 2
    assert "pm2 jlist snapshot parse failed" in result.stderr
    assert result.stdout == ""


def test_rejects_non_array_pm2_json():
    result = run_helper('{"name":"comfyui"}')

    assert result.returncode == 2
    assert "did not return a JSON array" in result.stderr
