#!/bin/bash
set -euo pipefail

# Only run in remote Claude Code sessions
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}"

# Collect startup sweep via Python (handles YAML parsing + JSON output)
python3 - <<'PYEOF'
import subprocess, sys, json, os
from pathlib import Path

root = Path(os.environ.get("CLAUDE_PROJECT_DIR", subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"], text=True).strip()))

lines = ["=== CONDUCTOR STARTUP SWEEP ===", ""]

# Git state
try:
    branch = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True, cwd=root).strip()
    status = subprocess.check_output(
        ["git", "status", "--short"], text=True, cwd=root).strip()
    log = subprocess.check_output(
        ["git", "log", "--oneline", "-5"], text=True, cwd=root).strip()
    tree_state = "clean" if not status else "DIRTY"
    lines += [f"Branch: {branch}  ({tree_state})", ""]
    lines += ["Git log (last 5):", log, ""]
except Exception as e:
    lines += [f"Git error: {e}", ""]

# Roadmap scan
try:
    import yaml
    ready, needs_human, claimed = [], [], []
    for rmap in sorted(root.glob("projects/*/roadmap.yaml")):
        proj = rmap.parent.name
        with open(rmap) as f:
            data = yaml.safe_load(f)
        for task in data.get("tasks", []):
            s = task.get("status", "")
            entry = f"  [{proj}/{task.get('id','?')}] {task.get('title','')}"
            if s == "ready":
                ready.append(entry)
            elif s == "needs-human":
                needs_human.append(entry)
            elif s == "claimed":
                claimed.append(entry)

    def section(title, items):
        if items:
            return [f"Roadmap — {title}:"] + items + [""]
        return [f"Roadmap — {title}: none", ""]

    lines += section("Ready tasks", ready)
    lines += section("Needs-human gates", needs_human)
    lines += section("Claimed tasks", claimed)
except Exception as e:
    lines += [f"Roadmap scan error: {e}", ""]

# TALKBACK.md tail
talkback = root / "TALKBACK.md"
try:
    text = talkback.read_text()
    tail = "\n".join(text.splitlines()[-30:])
    if tail.strip():
        lines += ["TALKBACK.md (last 30 lines):", tail, ""]
    else:
        lines += ["TALKBACK.md: empty", ""]
except Exception as e:
    lines += [f"TALKBACK error: {e}", ""]

# Open PRs (worker/* and claude/* branches) — CLAUDE.md step 3
try:
    import urllib.request
    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        req = urllib.request.Request(
            "https://api.github.com/repos/silasfelinus/conductor/pulls?state=open&per_page=20",
            headers={"Authorization": f"token {token}",
                     "Accept": "application/vnd.github.v3+json"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            prs = json.loads(resp.read())
        agent_prs = [
            f"  #{p['number']} [{p['head']['ref']}] {p['title']}"
            for p in prs if p["head"]["ref"].startswith(("worker/", "claude/"))
        ]
        lines += ["Open agent PRs (worker/* / claude/*):"]
        lines += agent_prs if agent_prs else ["  none"]
        lines += [""]
    else:
        lines += ["Open agent PRs: GITHUB_TOKEN not set — skipped", ""]
except Exception as e:
    lines += [f"Open PRs check error: {e}", ""]

flutter_home = Path(os.environ.get("FLUTTER_HOME", str(Path.home() / ".flutter")))
flutter_bin = flutter_home / "bin" / "flutter"
if flutter_bin.exists():
    lines += [f"Flutter SDK: already provisioned at {flutter_home}.", ""]
else:
    lines += [
        "Flutter SDK: not yet provisioned this session. If a task touches apps/* "
        "(Flutter), run `source scripts/provision_flutter.sh` first (~1-2 min, "
        "one-time download) so `flutter analyze`/`flutter test` can actually verify "
        "the change instead of relying on inspection alone (conductor/t-028).",
        "",
    ]

lines += ["NOTE: Read AGENTS.md for the full operating manual before responding."]
lines += ["=== END SWEEP ==="]

print(json.dumps({"message": "\n".join(lines)}))
PYEOF
