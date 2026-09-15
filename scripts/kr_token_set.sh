#!/usr/bin/env bash
# kr_token_set.sh — the shell-safe way to check whether KR_API_TOKEN is set,
# without ever printing its value.
#
# Background (conductor/t-116): two independent sessions (root TALKBACK.md,
# 2026-08-12 and 2026-08-13 ~02:26 UTC) each hand-typed the same broken probe
# before calling a production admin API:
#
#   echo "KR_API_TOKEN set: ${KR_API_TOKEN:+yes}${KR_API_TOKEN:-no}"
#
# `${VAR:-no}` substitutes the *live value* once the var is already set (the
# `:-` fallback only applies when the var is unset/empty) — so that "no" isn't
# a literal fallback string once KR_API_TOKEN has a value, it's the token
# itself, printed straight into the session's own tool-output transcript.
# Both instances were sandbox-only (never committed or transmitted externally)
# but still a real leak into a place it doesn't need to be. The correct
# pattern uses `-n`/`-z`, which only ever test presence and never expand the
# variable into output.
#
# Usage:
#   source scripts/kr_token_set.sh          # prints "KR_API_TOKEN: set" or "KR_API_TOKEN: not set"
#   scripts/kr_token_set.sh && echo ready   # exit 0 if set, exit 1 if not — safe in an `if`/`&&`
#
# Never echo, log, or otherwise print "$KR_API_TOKEN" itself. This script
# only ever reports presence/absence.
#
# `source`d vs executed both have to end this shell's involvement the same
# way: `exit` inside a *sourced* script terminates the caller's whole shell,
# not just this script — so `source scripts/kr_token_set.sh; <next command>`
# silently never runs <next command> (conductor, 2026-09-15: discovered when
# a scheduled session's own `source ... ; python3 ...` one-liner produced no
# output at all — the token check killed the shell before the python call).
# `(return 0 2>/dev/null)` succeeds only when this file is being sourced (a
# bare `return` outside a function/sourced script is a no-op error), which is
# how we tell the two cases apart at runtime.
if (return 0 2>/dev/null); then
  sourced=1
else
  sourced=0
fi

if [ -n "${KR_API_TOKEN:-}" ]; then
  echo "KR_API_TOKEN: set"
  status=0
else
  echo "KR_API_TOKEN: not set"
  status=1
fi

if [ "$sourced" -eq 1 ]; then
  return "$status"
else
  exit "$status"
fi
