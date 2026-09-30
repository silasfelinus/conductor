#!/bin/bash
set -euo pipefail

# Only run in remote Claude Code sessions
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}"

# Mirror the secret guards to user level so the NEXT session in this container is
# covered even if it is rooted outside this repo (scripts/install_secret_hooks.py).
python3 scripts/install_secret_hooks.py >/dev/null 2>&1 || true

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

# Roadmap scan. The lifecycle registry controls which roadmaps are actionable.
try:
    import yaml
    overrides_path = root / "project-overrides.yaml"
    overrides = yaml.safe_load(overrides_path.read_text()) or {}
    active_projects = {
        entry.get("slug")
        for entry in overrides.get("overrides", [])
        if isinstance(entry, dict) and entry.get("status", "active") == "active"
    }
    ready, needs_human, claimed = [], [], []
    for rmap in sorted(root.glob("projects/*/roadmap.yaml")):
        proj = rmap.parent.name
        if proj not in active_projects:
            continue
        with open(rmap) as f:
            data = yaml.safe_load(f) or {}
        for task in data.get("tasks", []):
            s = task.get("status", "")
            entry = f"  [{proj}/{task.get('id','?')}] {task.get('title','')}"
            if s == "ready":
                ready.append(entry)
            elif s == "needs-human":
                needs_human.append(entry)
            elif s == "claimed":
                claimed.append(entry)

    # Token essentialization (2026-09-30): this message lands in every session's
    # context, so list only what a session acts on directly. Needs-human detail
    # (50+ lines) is audit_human_gates.py's job via scripts/session_sweep.py;
    # here it is one per-project count line.
    def section(title, items, cap=15):
        if not items:
            return [f"Roadmap — {title}: none", ""]
        shown = items[:cap]
        more = [f"  ... {len(items) - cap} more"] if len(items) > cap else []
        return [f"Roadmap — {title} ({len(items)}):"] + shown + more + [""]

    lines += section("Ready tasks", ready)
    if needs_human:
        from collections import Counter
        per = Counter(e.split("[", 1)[1].split("/", 1)[0] for e in needs_human)
        lines += [f"Roadmap — Needs-human gates ({len(needs_human)}): "
                  + ", ".join(f"{k} {v}" for k, v in sorted(per.items()))
                  + "  (detail: python scripts/audit_human_gates.py)", ""]
    else:
        lines += ["Roadmap — Needs-human gates: none", ""]
    lines += section("Claimed tasks", claimed)
except Exception as e:
    lines += [f"Roadmap scan error: {e}", ""]

# TALKBACK.md tail
talkback = root / "TALKBACK.md"
try:
    # TALKBACK.md is >1MB; show only the headings of the latest entries, not
    # their bodies. Read an entry in full only when its heading needs action.
    with open(talkback, "rb") as fh:
        fh.seek(0, 2)
        fh.seek(max(0, fh.tell() - 60000))
        text = fh.read().decode("utf-8", "replace")
    heads = [l for l in text.splitlines() if l.startswith("## ")][-6:]
    if heads:
        lines += ["TALKBACK.md latest entry headings (read an entry only if it needs action; "
                  "never read the whole file — `tail -n 80 TALKBACK.md`):"] + [f"  {h[3:]}" for h in heads] + [""]
    else:
        lines += ["TALKBACK.md: no recent entries", ""]
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
            for p in prs if p["head"]["ref"].startswith(("worker/", "claude/", "agent/"))
        ]
        lines += ["Open agent PRs (worker/* / claude/* / agent/*):"]
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

lines += [
    "SOURCE OF TRUTH: Read SOURCE_OF_TRUTH.md. Conductor owns coordination; "
    "Kind Robots owns presentation/application state and stores only a projected read model.",
    "NOTE: Read AGENTS.md (core) and docs/state-reconciliation.md before responding; "
    "then run `python scripts/session_sweep.py` for all reconciliation checks in one call. "
    "Load only the role playbook select_role.py names (docs/agents/roles/).",
]
lines += ["=== END SWEEP ==="]

print(json.dumps({"message": "\n".join(lines)}))
PYEOF
