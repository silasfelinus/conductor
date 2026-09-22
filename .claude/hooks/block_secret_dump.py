#!/usr/bin/env python3
"""PreToolUse guard: refuse a Bash command that can print a secret into the transcript.

Four sessions have now leaked a live `KR_API_TOKEN` into their own tool output
(root TALKBACK.md 2026-08-12, 2026-08-13, 2026-09-16, 2026-09-21). Every one of
them knew the rule -- AGENTS.md hard rule 15 and `scripts/kr_token_set.sh` both
spell it out, and the 2026-09-16 session cited the earlier incidents in its own
commit messages while authoring the leak. Knowing the rule is demonstrably not
enough, so this refuses the command instead of relying on the author to notice.

The three shapes that actually happened:

  echo "KR_API_TOKEN set: ${KR_API_TOKEN:+yes}${KR_API_TOKEN:-no}" | sed 's/=.*/x/'
      `${VAR:-no}` substitutes the *live value* once VAR is set -- the `:-`
      fallback only applies when it is unset. The `sed` was meant to redact but
      targeted a `KEY=value` shape this string never had, so it passed through.

  export $(grep -q KR_API_TOKEN <<< "$(env)" && true)
      `grep -q` prints nothing and `&& true` adds nothing, so the substitution
      evaluated to empty and the line collapsed to a bare `export` -- which is
      bash's own way of listing every exported variable as `declare -x N="v"`.

  grep -n '^MIGRATION_DATABASE_URL=' .env
      Handed to Silas to run. His paste was not the leak; the command was.

So the deny rules below are deliberately shaped around what a command can PRINT,
not around whether it mentions a secret. `curl -H "Authorization: Bearer
$KR_API_TOKEN"` sends the value to a socket and is left alone; `echo` of the
same expansion is refused. A redaction pipeline downstream never rescues a
segment -- that is exactly what failed in 2026-09-16.

Input is the PreToolUse hook JSON on stdin. A refusal prints a `deny` decision
and exits 0; anything else prints nothing and exits 0, leaving the normal
permission flow untouched. Unparseable input fails open on purpose: a guard that
bricks every Bash call when its stdin shape changes is worse than the leak it
prevents, and the other layers (hard rule 15, kr_token_set.sh) still stand.

This file never echoes the command back. It names the construct it matched --
a variable name, a flag, a path -- and nothing to the right of an `=`.
"""

from __future__ import annotations

import json
import re
import sys

# --- what counts as a secret -------------------------------------------------

# Names this repo actually holds. Kept explicit because some of them (KR_API_TOKEN
# aside) would not be caught by the substring rule below.
KNOWN_SECRET_NAMES = {
    "ANTHROPIC_API_KEY",
    "BREVO_API_KEY",
    "CIVITAI_TOKEN",
    "GH_TOKEN",
    "GITHUB_TOKEN",
    "KR_API_TOKEN",
    "KR_CIVITAI_TOKEN",
    "MIGRATION_DATABASE_URL",
    "DATABASE_URL",
    "OPENAI_API_KEY",
}

# Substrings that make a name secret-shaped whatever it is called. This is the
# part that covers a credential nobody has added to the set above yet.
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


def is_secret_name(name: str) -> bool:
    upper = name.upper()
    if upper in KNOWN_SECRET_NAMES:
        return True
    return any(part in upper for part in SECRET_SUBSTRINGS)


# --- shell shredding ---------------------------------------------------------

OPERATOR_CHARS = ";\n|&()`"
SEGMENT_SPLIT = re.compile(f"[{re.escape(OPERATOR_CHARS)}]")
SHELL_WRAPPERS = {"bash", "sh", "zsh", "dash", "ksh"}
# Words that stand in front of the real command without changing what it does.
PREFIX_WORDS = {
    "builtin",
    "command",
    "do",
    "doas",
    "else",
    "eval",
    "exec",
    "if",
    "nohup",
    "stdbuf",
    "sudo",
    "then",
    "time",
    "xargs",
}
ASSIGNMENT = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)=")


def mask_operators_in_quotes(command: str) -> str:
    """Blank shell operators that sit inside quotes, so they don't split a segment.

    `git commit -m "fix; export broken"` is one command, not two, and the second
    half is not a bare `export`. Only the operator characters are blanked --
    everything else inside the quotes stays readable, because the word and
    expansion checks below still need to see it.
    """
    out = []
    quote = ""
    for char in command:
        if quote:
            if char == quote:
                quote = ""
            elif char in OPERATOR_CHARS:
                out.append(" ")
                continue
        elif char in "\"'":
            quote = char
        out.append(char)
    return "".join(out)


def segments(command: str) -> list[str]:
    """Every run of the command that has its own leading word.

    `$(` is flattened to `(` first, so the inside of a substitution becomes a
    segment in its own right -- which is how the bare `env` in
    `export $(... <<< "$(env)" ...)` gets seen at all.
    """
    flattened = mask_operators_in_quotes(command).replace("$(", "(")
    return [part for part in SEGMENT_SPLIT.split(flattened) if part.strip()]


def words(segment: str) -> list[str]:
    """Whitespace-split, with quote characters stripped off each word."""
    return [word.strip("\"'") for word in segment.split()]


def head_and_operands(segment: str) -> tuple[str, list[str]]:
    """The segment's command word and its operands, past any prefix noise."""
    rest = words(segment)
    while rest:
        word = rest[0]
        if word in PREFIX_WORDS or ASSIGNMENT.match(word):
            rest = rest[1:]
            continue
        return word.rsplit("/", 1)[-1], rest[1:]
    return "", []


def inline_scripts(segment: str) -> list[str]:
    """Payloads of `bash -c '<script>'`, which would otherwise hide a bare export."""
    head, operands = head_and_operands(segment)
    if head not in SHELL_WRAPPERS:
        return []
    found = []
    for index, operand in enumerate(operands):
        if operand.startswith("-") and "c" in operand.lstrip("-"):
            found.extend(operands[index + 1 :])
            break
    return found


# --- expansions --------------------------------------------------------------

BRACED = re.compile(r"\$\{([#!]?)([A-Za-z_][A-Za-z0-9_]*)([^}]*)\}")
BARE = re.compile(r"\$([A-Za-z_][A-Za-z0-9_]*)")
# `[ -n "$VAR" ]` and `[ -z "$VAR" ]` test presence without ever expanding the
# value into output. This is the pattern kr_token_set.sh recommends, so it has to
# keep working.
SAFE_TEST_TAIL = re.compile(r"-[nz]\s+[\"']?$")


def leaking_expansions(text: str) -> list[str]:
    """Secret expansions in `text` that yield the value rather than a stand-in."""
    found = []
    for match in BRACED.finditer(text):
        sigil, name, rest = match.group(1), match.group(2), match.group(3)
        if not is_secret_name(name):
            continue
        if sigil == "#":
            continue  # ${#VAR} is the length, never the value
        if rest.startswith(("+", ":+")):
            continue  # ${VAR:+alt} is the alternate, never the value
        if SAFE_TEST_TAIL.search(text[: match.start()]):
            continue
        found.append("${%s%s}" % (name, rest))
    for match in BARE.finditer(text):
        name = match.group(1)
        if not is_secret_name(name):
            continue
        if text[match.start() - 1 : match.start()] == "{":
            continue  # already counted by the braced pass
        if SAFE_TEST_TAIL.search(text[: match.start()]):
            continue
        found.append("$" + name)
    return found


# --- dotenv files ------------------------------------------------------------

DOTENV_PATH = re.compile(r"(?:[\w./~-]*/)?\.env(?:\.[A-Za-z0-9_-]+)?")
DOTENV_SAFE_SUFFIXES = (
    ".example",
    ".sample",
    ".template",
    ".dist",
    ".defaults",
    ".schema",
)
PRINTING_COMMANDS = {
    "awk",
    "base64",
    "bat",
    "cat",
    "echo",
    "head",
    "less",
    "logger",
    "more",
    "nl",
    "od",
    "print",
    "printf",
    "sed",
    "strings",
    "tac",
    "tail",
    "tee",
    "write",
    "xxd",
}
GREP_COMMANDS = {"egrep", "fgrep", "grep", "rg", "ug", "zgrep"}
# grep flags that report a match without reprinting the line it matched
GREP_QUIET_FLAGS = ("q", "c", "l", "L")
# The redaction hard rule 15 prescribes for reading a config line. Trusting a
# downstream filter is what failed in 2026-09-16 -- but it failed because the
# redacted text was a bare token with no `=` in it, so the substitution had
# nothing to match. Every line in a dotenv file is `NAME=value`, so here the
# match is structural rather than hopeful. That is the whole difference, and it
# is why this allowance stops at dotenv greps and never reaches an expansion.
DOTENV_REDACTION = re.compile(r"\bsed\b[^|;]*\bs([/|@#,])=\.\*\1")


def dotenv_paths(segment: str) -> list[str]:
    hits = []
    for word in words(segment):
        for match in DOTENV_PATH.finditer(word):
            path = match.group(0)
            if path.lower().endswith(DOTENV_SAFE_SUFFIXES):
                continue
            hits.append(path)
    return hits


def grep_is_quiet(operands: list[str]) -> bool:
    for operand in operands:
        if operand.startswith("--"):
            if operand.lstrip("-") in {"quiet", "silent", "count", "files-with-matches", "files-without-match"}:
                return True
        elif operand.startswith("-") and any(flag in operand[1:] for flag in GREP_QUIET_FLAGS):
            return True
    return False


# --- the rules ---------------------------------------------------------------

ALTERNATIVE = (
    "Safe alternatives: `scripts/kr_token_set.sh` (or `[ -n \"$VAR\" ]`) for presence, "
    "`${VAR:+PRESENT}` for a stand-in, `grep -c '^NAME=' .env` for a count, "
    "`source .env` to load without printing, and reading `os.environ` inside a "
    "python script for anything that needs the value. See AGENTS.md hard rule 15."
)


def check_segment(segment: str, redacted: bool = False) -> str | None:
    """The reason this segment is refused, or None.

    `redacted` says the wider command pipes into the `=`-anchored `sed` that hard
    rule 15 prescribes, which only ever relaxes the dotenv-grep rule below.
    """
    head, operands = head_and_operands(segment)
    positional = [word for word in operands if not word.startswith("-")]

    if head in {"export", "declare", "typeset"}:
        assignments = [word for word in operands if ASSIGNMENT.match(word)]
        flags = [word for word in operands if word.startswith("-")]
        if not assignments:
            what = "a bare `%s`" % head if not operands else "`%s` with no literal NAME=value" % head
            return (
                "%s prints every exported variable as `declare -x NAME=\"value\"`, "
                "secrets included. This is the 2026-09-21 leak exactly: "
                "`export $(grep -q ... && true)` collapsed to a bare `export` because "
                "the substitution evaluated to empty." % what.capitalize()
            )
        if len(assignments) + len(flags) != len(operands):
            return (
                "`%s` here has an operand that is not a literal NAME=value, so it may "
                "expand to nothing and dump the whole environment." % head
            )
        named = [ASSIGNMENT.match(word).group(1) for word in assignments]
        leaked = [name for name in named if is_secret_name(name)]
        if leaked:
            return (
                "Assigning %s inline writes the value into this transcript. Set it in "
                "`.env` or the container environment instead." % ", ".join(sorted(leaked))
            )

    if head == "env" and not positional:
        return (
            "`env` with no command to run prints the whole environment, secrets "
            "included. `env -u NAME <command>` is fine; a bare `env` is not."
        )

    if head == "printenv":
        if not positional:
            return "`printenv` with no variable named prints the whole environment."
        leaked = [word for word in positional if is_secret_name(word)]
        if leaked:
            return "`printenv %s` prints the value straight into this transcript." % leaked[0]

    if head == "set" and not operands:
        return (
            "A bare `set` prints every shell variable and function, secrets included. "
            "`set -euo pipefail` and friends are fine."
        )

    leaks = leaking_expansions(segment)
    if leaks:
        if head in PRINTING_COMMANDS:
            return (
                "`%s` would print %s, which expands to the live value. A `sed`/`tr` "
                "redaction downstream does not rescue this -- that is precisely how "
                "the 2026-09-16 leak got through. %s" % (head, leaks[0], ALTERNATIVE)
            )
        if "<<<" in segment:
            return (
                "The here-string feeds %s -- the live value -- to `%s`, which prints "
                "it. %s" % (leaks[0], head or "a command", ALTERNATIVE)
            )

    env_files = dotenv_paths(segment)
    if env_files:
        if head in PRINTING_COMMANDS:
            return (
                "`%s %s` prints credential lines verbatim. %s"
                % (head, env_files[0], ALTERNATIVE)
            )
        if head in GREP_COMMANDS and not grep_is_quiet(operands) and not redacted:
            return (
                "A value-printing grep of `%s` is the 2026-08-25 incident in hard rule "
                "15 -- `grep -n '^MIGRATION_DATABASE_URL=' .env` printed a live "
                "production password. Use `grep -c` for a count, or append "
                "`| sed 's/=.*/=<redacted>/'`." % env_files[0]
            )
    return None


def check(command: str, depth: int = 0) -> str | None:
    redacted = bool(DOTENV_REDACTION.search(command))
    for segment in segments(command):
        reason = check_segment(segment, redacted=redacted)
        if reason:
            return reason
        if depth < 3:
            for script in inline_scripts(segment):
                reason = check(script, depth + 1)
                if reason:
                    return reason
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        if payload.get("tool_name") != "Bash":
            return 0
        command = payload.get("tool_input", {}).get("command") or ""
    except Exception:
        return 0  # fail open; see the module docstring

    reason = check(command)
    if not reason:
        return 0

    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "Blocked by .claude/hooks/block_secret_dump.py. " + reason,
            }
        },
        sys.stdout,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
