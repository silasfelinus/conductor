#!/bin/bash
set -euo pipefail

# Only run in remote Claude Code sessions.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi
cd "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}"

# Preserve the security bootstrap, including sessions rooted outside this repo.
python3 scripts/install_secret_hooks.py >/dev/null 2>&1 || true

# No roadmap, TALKBACK, PR, or network scan here: the live selector already
# owns those signals. Explicitly assigned work does not need a selector run.
python3 - <<'PYEOF'
import json
import subprocess

def git(*args):
    return subprocess.check_output(
        ["git", *args], text=True, stderr=subprocess.DEVNULL, timeout=5
    ).strip()

try:
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    state = "DIRTY" if git("status", "--porcelain", "--untracked-files=normal") else "clean"
    checkout = f"Checkout: {branch[:120]} ({state})."
except (OSError, subprocess.SubprocessError):
    checkout = "Checkout state unavailable; verify before writing."

message = (
    f"{checkout} Use AGENTS.md once. For explicit work, load only the selected role "
    "and project/task. Otherwise run scripts/select_role.py once for live priorities "
    "and open PRs; investigate only actionable exceptions. STATUS.md is advisory. "
    "Read the current task and verify ownership before writes. "
    "Run targeted session_sweep.py checks only for stale or failed signals."
)
print(json.dumps({"message": message}))
PYEOF
