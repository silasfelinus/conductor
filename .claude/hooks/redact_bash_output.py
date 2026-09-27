#!/usr/bin/env python3
"""PreToolUse hook: route every Bash command's output through a value-based redactor.

Why this exists alongside `block_secret_dump.py`
------------------------------------------------
`block_secret_dump.py` refuses the command SHAPES that have leaked a secret. It
has been extended after every incident, and every incident since has been a
shape nobody had listed yet:

  2026-08-12/13  echo "${KR_API_TOKEN:-no}"                      (t-116)
  2026-08-24     the same, in an ad hoc one-liner                (t-128)
  2026-09-16     ${VAR:+..}${VAR:-..} | sed that matched nothing
  2026-09-21     export $(grep -q ... && true)  -> bare `export` (t-189)
  2026-09-27     python3 -c "print(getattr(mod, 'KR_API_TOKEN', 'NOATTR'))"

A deny list over shapes can never be complete -- any language that can read an
environment variable can print one. So this hook stops caring how the value got
printed and removes the value itself: before the command runs, it is wrapped so
that stdout and stderr both pass through `redact_bash_output.py --filter`, which
replaces the literal value of every secret-shaped environment variable (and every
secret-shaped `NAME=value` line in the project's dotenv files) with
`[REDACTED:NAME]`. Whatever shape leaks next, the transcript sees the stand-in.

The wrapper
-----------
    { <original command>
    } > >(python3 <this file> --filter) 2>&1; __krr=$?; wait $! 2>/dev/null; (exit $__krr)

* A `{ ...; }` group with a redirection runs in the CURRENT shell, not a
  subshell, so `cd`, `export`, and the harness's own cwd tracking still work.
* The newline before `}` keeps trailing comments and heredoc terminators intact.
* `wait $!` lets the filter flush before the tool call returns; `(exit $__krr)`
  hands back the original command's exit status.
* stderr is merged into stdout, which is what the Bash tool shows anyway.

Failure posture
---------------
Unparseable hook input, or `CONDUCTOR_REDACT_OUTPUT=0` in the environment, leaves
the command untouched (fail open: a hook that bricks every Bash call is worse
than the leak it guards, and hard rule 15 plus the shape guard still stand). The
filter itself never raises out: on any internal error it passes bytes through
unchanged rather than swallow the command's output.

Never make this file print a secret. It prints variable NAMES only.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

MARKER = "--filter) 2>&1; __krr=$?"
MIN_SECRET_LEN = 8

KNOWN_SECRET_NAMES = {
    "ANTHROPIC_API_KEY",
    "BREVO_API_KEY",
    "CIVITAI_TOKEN",
    "DATABASE_URL",
    "GH_TOKEN",
    "GITHUB_TOKEN",
    "KR_API_TOKEN",
    "KR_CIVITAI_TOKEN",
    "KR_RELAY_TOKEN",
    "MIGRATION_DATABASE_URL",
    "OPENAI_API_KEY",
    "SERENDIPITY_KR_SERVICE_TOKEN",
}
SECRET_SUBSTRINGS = (
    "ACCESS_KEY",
    "API_KEY",
    "APIKEY",
    "AUTH_TOKEN",
    "CREDENTIAL",
    "PASSPHRASE",
    "PASSWD",
    "PASSWORD",
    "PRIVATE_KEY",
    "SECRET",
    "TOKEN",
)
# Secret-shaped names whose values are not secrets and are short/common enough
# that redacting them would mangle ordinary output.
NOT_SECRET = {"CLAUDE_CODE_OAUTH_TOKEN_FILE_DESCRIPTOR"}


def is_secret_name(name: str) -> bool:
    upper = name.upper()
    if upper in NOT_SECRET:
        return False
    if upper in KNOWN_SECRET_NAMES:
        return True
    return any(part in upper for part in SECRET_SUBSTRINGS)


# --- collecting the values to redact ----------------------------------------

DOTENV_LINE = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$")


def _dotenv_secrets(path: Path) -> dict[str, str]:
    found: dict[str, str] = {}
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return found
    for line in text.splitlines():
        match = DOTENV_LINE.match(line)
        if not match or not is_secret_name(match.group(1)):
            continue
        value = match.group(2)
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        found[match.group(1)] = value
    return found


def collect_secrets(environ=None, roots=None) -> list[tuple[bytes, str]]:
    """(value, name) pairs, longest value first so overlapping values mask fully."""
    environ = os.environ if environ is None else environ
    pairs: dict[str, str] = {}
    for name, value in environ.items():
        if is_secret_name(name):
            pairs.setdefault(value, name)
    if roots is None:
        roots = {Path.cwd()}
        project = environ.get("CLAUDE_PROJECT_DIR")
        if project:
            roots.add(Path(project))
    for root in roots:
        for candidate in list(root.glob(".env")) + list(root.glob(".env.*")) + list(root.glob(".secrets/*")):
            if candidate.name.endswith((".example", ".sample", ".template", ".dist", ".schema")):
                continue
            if candidate.is_file():
                for name, value in _dotenv_secrets(candidate).items():
                    pairs.setdefault(value, name)
    out = []
    for value, name in pairs.items():
        value = value.strip()
        if len(value) < MIN_SECRET_LEN:
            continue
        out.append((value.encode("utf-8", errors="surrogateescape"), name))
    out.sort(key=lambda pair: len(pair[0]), reverse=True)
    return out


def redact(data: bytes, secrets: list[tuple[bytes, str]]) -> bytes:
    for value, name in secrets:
        if value in data:
            data = data.replace(value, b"[REDACTED:" + name.encode() + b"]")
    return data


def run_filter() -> int:
    try:
        secrets = collect_secrets()
    except Exception:
        secrets = []
    inp, out = sys.stdin.buffer, sys.stdout.buffer
    for line in iter(inp.readline, b""):
        try:
            line = redact(line, secrets)
        except Exception:
            pass
        out.write(line)
        out.flush()
    return 0


# --- the hook ----------------------------------------------------------------


def wrap(command: str, hook_path: str) -> str:
    return (
        "{ %s\n} > >(python3 %s --filter) 2>&1; __krr=$?; wait $! 2>/dev/null; (exit $__krr)"
        % (command, json.dumps(hook_path))
    )


def hook(payload: dict, hook_path: str) -> dict | None:
    if payload.get("tool_name") != "Bash":
        return None
    tool_input = payload.get("tool_input") or {}
    command = tool_input.get("command") or ""
    if not command.strip() or MARKER in command:
        return None
    updated = dict(tool_input)
    updated["command"] = wrap(command, hook_path)
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "updatedInput": updated,
        }
    }


def main(argv: list[str]) -> int:
    if "--filter" in argv:
        return run_filter()
    if os.environ.get("CONDUCTOR_REDACT_OUTPUT") == "0":
        return 0
    try:
        payload = json.load(sys.stdin)
        result = hook(payload, str(Path(__file__).resolve()))
    except Exception:
        return 0
    if result:
        json.dump(result, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
