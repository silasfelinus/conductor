#!/usr/bin/env python3
"""Install Conductor's two secret guards as USER-level Claude Code hooks.

`.claude/settings.json` only loads when a session's project directory IS this
repo. A multi-repo cloud session rooted at `/home/user` (conductor, kind_robots,
... side by side) never loads it, so every Bash call in that session ran with no
guard at all. Installing into `~/.claude/settings.json` covers every session in
the container, whichever directory it started in.

Copies `block_secret_dump.py` and `redact_bash_output.py` into `~/.claude/hooks/`
and merges a PreToolUse entry for each into `~/.claude/settings.json`, keeping
anything else already there. Idempotent: re-running it refreshes the copies and
never duplicates an entry.

Run it from the environment's setup script so it lands before Claude Code starts:

    python3 /home/user/conductor/scripts/install_secret_hooks.py || true

Hooks are read when a session starts, so installing mid-session protects the
NEXT session, not the current one.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HOOKS = {
    "block_secret_dump.py": "Bash|Read|Grep",
    "redact_bash_output.py": "Bash",
}


def install(home: Path) -> list[str]:
    target = home / ".claude" / "hooks"
    target.mkdir(parents=True, exist_ok=True)
    settings_path = home / ".claude" / "settings.json"
    try:
        settings = json.loads(settings_path.read_text())
    except (OSError, ValueError):
        settings = {}
    pre = settings.setdefault("hooks", {}).setdefault("PreToolUse", [])
    changed = []
    for name, matcher in HOOKS.items():
        dest = target / name
        shutil.copy2(REPO / ".claude" / "hooks" / name, dest)
        dest.chmod(0o755)
        command = 'python3 "%s"' % dest
        present = any(
            name in hook.get("command", "") for entry in pre for hook in entry.get("hooks", [])
        )
        if not present:
            pre.append({"matcher": matcher, "hooks": [{"type": "command", "command": command, "timeout": 10}]})
            changed.append(name)
    settings_path.write_text(json.dumps(settings, indent=2) + "\n")
    return changed


def main() -> int:
    changed = install(Path.home())
    print("secret hooks installed at user level" + (": added " + ", ".join(changed) if changed else " (already wired)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
