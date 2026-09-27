"""The output redactor has to mask a secret whatever shape printed it.

`block_secret_dump.py` refuses the command shapes that already leaked, and every
incident since it was written has been a new shape -- most recently a Python
`getattr(module, "KR_API_TOKEN", ...)` diagnostic (root TALKBACK.md,
2026-09-27). This layer masks the VALUE instead, so each fixture below runs a
real wrapped command in bash with a fake token in its environment and asserts
the token never reaches the output, while the command's exit status, stderr,
and working-directory changes all survive the wrapper.
"""

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
HOOK = REPO_ROOT / ".claude" / "hooks" / "redact_bash_output.py"
FAKE = "fakeTok3n0123456789abcdef0123456789"


def _load():
    spec = importlib.util.spec_from_file_location("redact_bash_output", HOOK)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


redactor = _load()


def _run_wrapped(command, tmp_path, suffix=""):
    wrapped = redactor.wrap(command, str(HOOK))
    env = {"PATH": os.environ["PATH"], "HOME": str(tmp_path), "KR_API_TOKEN": FAKE}
    return subprocess.run(
        ["bash", "-c", wrapped + suffix],
        env=env,
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )


LEAKS = [
    'echo "KR_API_TOKEN set: ${KR_API_TOKEN:+yes}${KR_API_TOKEN:-no}"',
    "export",
    "env",
    "printenv KR_API_TOKEN >&2",
    f'{sys.executable} -c "import os; print(getattr(os, \'environ\').get(\'KR_API_TOKEN\', \'NOATTR\'))"',
    "cat <<X\n$KR_API_TOKEN\nX",
    'echo "prefix-${KR_API_TOKEN}-suffix"; exit 4',
]


@pytest.mark.parametrize("command", LEAKS)
def test_the_value_never_reaches_the_output(command, tmp_path):
    result = _run_wrapped(command, tmp_path)
    output = result.stdout + result.stderr
    assert FAKE not in output
    assert "[REDACTED:KR_API_TOKEN]" in output or command in {"export", "env"}


def test_a_dotenv_value_is_masked_even_when_it_is_not_in_the_environment(tmp_path):
    (tmp_path / ".env").write_text("DATABASE_URL='mysql://u:hunter2hunter2@db/x'\nPORT=3000\n")
    result = _run_wrapped("echo mysql://u:hunter2hunter2@db/x port 3000", tmp_path)
    assert "hunter2" not in result.stdout
    assert "[REDACTED:DATABASE_URL]" in result.stdout
    assert "3000" in result.stdout


@pytest.mark.parametrize("command,status", [("true", 0), ("false", 1), ("(exit 7)", 7)])
def test_the_exit_status_survives(command, status, tmp_path):
    assert _run_wrapped(command, tmp_path).returncode == status


def test_cd_and_a_trailing_comment_still_work(tmp_path):
    (tmp_path / "sub").mkdir()
    result = _run_wrapped("cd sub  # trailing comment", tmp_path, suffix="\npwd")
    assert result.stdout.strip().endswith("/sub")


def test_ordinary_output_is_untouched(tmp_path):
    result = _run_wrapped("seq 1 5000 | tail -1; echo err >&2", tmp_path)
    assert result.stdout.split() == ["5000", "err"]


def test_the_hook_rewrites_the_command_without_deciding_permission():
    payload = {"tool_name": "Bash", "tool_input": {"command": "ls", "description": "d"}}
    out = redactor.hook(payload, str(HOOK))["hookSpecificOutput"]
    assert out["hookEventName"] == "PreToolUse"
    assert "permissionDecision" not in out
    assert out["updatedInput"]["description"] == "d"
    assert out["updatedInput"]["command"].startswith("{ ls\n}")


def test_it_never_wraps_twice_or_touches_other_tools():
    wrapped = redactor.wrap("ls", str(HOOK))
    assert redactor.hook({"tool_name": "Bash", "tool_input": {"command": wrapped}}, str(HOOK)) is None
    assert redactor.hook({"tool_name": "Read", "tool_input": {"file_path": "x"}}, str(HOOK)) is None


@pytest.mark.parametrize("payload", ["", "not json", "[]"])
def test_unparseable_input_fails_open(payload):
    result = subprocess.run(
        [sys.executable, str(HOOK)], input=payload, capture_output=True, text=True, check=False
    )
    assert result.returncode == 0
    assert result.stdout == ""


def test_the_kill_switch_leaves_commands_alone():
    result = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps({"tool_name": "Bash", "tool_input": {"command": "ls"}}),
        env={**os.environ, "CONDUCTOR_REDACT_OUTPUT": "0"},
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout == ""


def test_settings_json_wires_the_redactor_up():
    settings = json.loads((REPO_ROOT / ".claude" / "settings.json").read_text())
    commands = [
        hook["command"]
        for entry in settings["hooks"]["PreToolUse"]
        if "Bash" in entry.get("matcher", "")
        for hook in entry["hooks"]
    ]
    assert any("redact_bash_output.py" in command for command in commands), commands


def test_the_hook_is_executable():
    assert HOOK.stat().st_mode & 0o111


def test_the_user_level_installer_is_idempotent_and_keeps_other_settings(tmp_path):
    spec = importlib.util.spec_from_file_location(
        "install_secret_hooks", REPO_ROOT / "scripts" / "install_secret_hooks.py"
    )
    installer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(installer)
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "settings.json").write_text('{"model": "keep-me"}')
    assert installer.install(tmp_path) == ["block_secret_dump.py", "redact_bash_output.py"]
    assert installer.install(tmp_path) == []
    settings = json.loads((tmp_path / ".claude" / "settings.json").read_text())
    assert settings["model"] == "keep-me"
    assert len(settings["hooks"]["PreToolUse"]) == 2
    assert (tmp_path / ".claude" / "hooks" / "redact_bash_output.py").stat().st_mode & 0o111
