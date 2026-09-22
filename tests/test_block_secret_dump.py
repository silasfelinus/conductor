"""The PreToolUse guard has to refuse the leaks that already happened.

Four sessions printed a live `KR_API_TOKEN` into their own transcript
(root TALKBACK.md 2026-08-12, 2026-08-13, 2026-09-16, 2026-09-21), plus the
2026-08-25 `.env` grep that AGENTS.md hard rule 15 is written around. Each of
those exact command strings is a fixture below, because a guard that drifts off
the shapes that actually occurred is decoration.

The allow cases matter just as much. A guard that refuses
`[ -n "$KR_API_TOKEN" ]` -- the pattern `scripts/kr_token_set.sh` exists to
recommend -- teaches the next session to work around it, and a guard that gets
worked around protects nothing.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
HOOK = REPO_ROOT / ".claude" / "hooks" / "block_secret_dump.py"


def _load():
    spec = importlib.util.spec_from_file_location("block_secret_dump", HOOK)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


guard = _load()


# The commands that actually leaked, verbatim from TALKBACK.
INCIDENTS = {
    "2026-08-12/13 (t-116)": (
        'echo "KR_API_TOKEN set: ${KR_API_TOKEN:+yes}${KR_API_TOKEN:-no}"'
    ),
    "2026-09-16": (
        'source scripts/kr_token_set.sh; '
        'echo "KR_API_TOKEN set: ${KR_API_TOKEN:+yes}${KR_API_TOKEN:-no}" '
        "| sed 's/=.*/set-check-done/'"
    ),
    "2026-09-21": 'export $(grep -q KR_API_TOKEN <<< "$(env)" && true)',
    "2026-08-25 (hard rule 15)": "grep -n '^MIGRATION_DATABASE_URL=' .env",
}

BLOCKED = [
    # Whole-environment dumps, in every spelling.
    "export",
    "  export  ",
    "declare -x",
    "declare -p",
    "typeset -x",
    "env",
    "env -0",
    "printenv",
    "set",
    "X=$(env); echo ok",
    "bash -c 'export'",
    "sh -c \"printenv\"",
    # A single secret, printed.
    "printenv KR_API_TOKEN",
    "echo $KR_API_TOKEN",
    'echo "${KR_API_TOKEN}"',
    'echo "${KR_API_TOKEN:-no}"',
    'echo "${KR_API_TOKEN:0:8}"',  # a prefix is still the secret
    'printf "%s\\n" "${GITHUB_TOKEN}"',
    'sed s/x/y/ <<< "$CIVITAI_TOKEN"',
    'echo "$ANTHROPIC_API_KEY" > /tmp/k',
    # A secret written inline, which puts the value in the transcript.
    "export KR_API_TOKEN=REDACTED_IN_TEST",
    # Credential files, read out loud.
    "cat ../kind_robots/.env",
    "cat .env.local",
    "head -5 .env",
    "grep TOKEN .env",
    # A name nobody has added to the known set yet.
    "echo $SOME_NEW_SERVICE_TOKEN",
    'echo "${VAULT_PASSWORD}"',
]

ALLOWED = [
    "ls",
    "python scripts/audit_human_gates.py",
    "git commit -m 'fix; export broken'",  # an operator inside quotes is not an operator
    'echo "$HOME"',
    # Presence checks -- the whole point of kr_token_set.sh.
    'bash -c \'source scripts/kr_token_set.sh && [ -n "$KR_API_TOKEN" ] && echo PRESENT || echo ABSENT\'',
    '[ -z "$KR_API_TOKEN" ] && echo ABSENT',
    '[[ -n "${CIVITAI_TOKEN}" ]] && echo PRESENT',
    'echo "KR_API_TOKEN: ${KR_API_TOKEN:+PRESENT}"',  # the alternate, never the value
    'echo "${#KR_API_TOKEN}"',  # the length, never the value
    # Legitimate uses that never reach stdout.
    'curl -sS -H "Authorization: Bearer $KR_API_TOKEN" https://kindrobots.org/api/art',
    "env -u KR_API_TOKEN pytest tests/ -q",
    "export PYTHONPATH=.",
    "set -euo pipefail",
    "source ../kind_robots/.env",
    # Reading a credential file without printing a credential.
    "cat .env.example",
    "grep -c '^CIVITAI_TOKEN=' ../kind_robots/.env",
    "grep -q '^CIVITAI_TOKEN=' .env && echo PRESENT",
    "grep '^KR_API_TOKEN=' .env | sed 's/=.*/=<redacted>/'",
]


@pytest.mark.parametrize("label", sorted(INCIDENTS))
def test_every_command_that_actually_leaked_is_refused(label):
    assert guard.check(INCIDENTS[label]) is not None, label


@pytest.mark.parametrize("command", BLOCKED)
def test_blocked(command):
    assert guard.check(command) is not None


@pytest.mark.parametrize("command", ALLOWED)
def test_allowed(command):
    reason = guard.check(command)
    assert reason is None, reason


def test_the_refusal_says_what_to_do_instead():
    """A deny that doesn't name the alternative just gets worked around."""
    reason = guard.check('echo "${KR_API_TOKEN:-no}"')
    assert "kr_token_set.sh" in reason
    assert "hard rule 15" in reason


def test_a_refusal_never_repeats_the_assignment_it_refused():
    """The reason text is read back into the transcript -- it cannot carry a value."""
    reason = guard.check("export KR_API_TOKEN=s3cr3t-value-here")
    assert "s3cr3t" not in reason
    assert "KR_API_TOKEN" in reason


def _run(payload):
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=False,
    )


def test_the_hook_speaks_the_pretooluse_wire_format():
    result = _run({"tool_name": "Bash", "tool_input": {"command": "export"}})
    assert result.returncode == 0
    decision = json.loads(result.stdout)["hookSpecificOutput"]
    assert decision["hookEventName"] == "PreToolUse"
    assert decision["permissionDecision"] == "deny"
    assert decision["permissionDecisionReason"]


def test_an_allowed_command_says_nothing_at_all():
    """Silence leaves the normal permission flow in charge; an explicit
    `allow` would bypass the settings.json rules instead of deferring to them."""
    result = _run({"tool_name": "Bash", "tool_input": {"command": "ls -la"}})
    assert result.returncode == 0
    assert result.stdout == ""


def test_a_non_bash_tool_is_none_of_this_hooks_business():
    result = _run({"tool_name": "Read", "tool_input": {"file_path": "/etc/passwd"}})
    assert result.returncode == 0
    assert result.stdout == ""


@pytest.mark.parametrize("payload", ["", "not json", "[]", '{"tool_name": "Bash"}'])
def test_unparseable_input_fails_open(payload):
    """A guard that bricks every Bash call when its stdin shape changes is worse
    than the leak it prevents; hard rule 15 and kr_token_set.sh still stand."""
    result = subprocess.run(
        [sys.executable, str(HOOK)],
        input=payload,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout == ""


def test_settings_json_actually_wires_the_hook_up():
    """The detector being correct is worth nothing if nothing calls it."""
    settings = json.loads((REPO_ROOT / ".claude" / "settings.json").read_text())
    commands = [
        hook["command"]
        for entry in settings["hooks"]["PreToolUse"]
        if "Bash" in entry.get("matcher", "")
        for hook in entry["hooks"]
        if hook.get("type") == "command"
    ]
    assert any("block_secret_dump.py" in command for command in commands), commands


def test_the_hook_is_executable():
    assert HOOK.stat().st_mode & 0o111, "hook needs its exec bit to run as a command"
