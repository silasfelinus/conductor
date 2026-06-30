#!/usr/bin/env python3
"""
build_kaizen.py — generate KAIZEN.md from roadmaps.

Usage:
    python scripts/build_kaizen.py [--dry-run] [--output PATH]

For each active project emits:
  1. KAIZEN PROMPT — the single most impactful action Silas can take right now
  2. HONEY-DO LIST — all other Silas-only unblocks (not agent-workable)

Priority order for kaizen prompt:
  1. needs-human tasks (waiting for Silas input/review)
  2. gate_human: true tasks with approved_by_human: false (not waiting)
  3. blocked tasks with passes >= 3 (stuck, need Silas to unblock)
  4. claimed tasks with no recent update (stale, may need Silas nudge)

Output: KAIZEN.md at repo root (or --output path).
"""

import argparse
import pathlib
import sys
from datetime import datetime, timezone

import yaml


# ---------------------------------------------------------------------------
# Roadmap helpers (shared with build_pr_triage.py)
# ---------------------------------------------------------------------------

PROJECTS_DIR = pathlib.Path("projects")
OVERRIDES_FILE = pathlib.Path("project-overrides.yaml")

STALE_DAYS = 3  # claimed tasks older than this are flagged as stale


def load_overrides() -> dict:
    if not OVERRIDES_FILE.exists():
        return {}
    raw = yaml.safe_load(OVERRIDES_FILE.read_text()) or {}
    entries = raw.get("overrides") or raw.get("projects")
    if isinstance(entries, list):
        return {e["slug"]: e for e in entries if isinstance(e, dict) and "slug" in e}
    if isinstance(entries, dict):
        return entries
    return {k: v for k, v in raw.items() if isinstance(v, dict)} if isinstance(raw, dict) else {}


def active_slugs(overrides: dict) -> list:
    return [
        slug
        for slug, cfg in overrides.items()
        if isinstance(cfg, dict) and cfg.get("status") == "active"
    ]


def load_roadmap(slug: str) -> dict | None:
    f = PROJECTS_DIR / slug / "roadmap.yaml"
    if not f.exists():
        return None
    try:
        return yaml.safe_load(f.read_text()) or {}
    except yaml.YAMLError:
        return None


def days_since(ts_str: str | None) -> float | None:
    if not ts_str:
        return None
    try:
        ts = datetime.fromisoformat(str(ts_str).replace("Z", "+00:00"))
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        return (now - ts).total_seconds() / 86400
    except (ValueError, TypeError):
        return None


# ---------------------------------------------------------------------------
# Per-project kaizen logic
# ---------------------------------------------------------------------------

def classify_tasks(roadmap: dict) -> dict:
    """Classify tasks into buckets by priority for Silas attention."""
    needs_human = []
    pending_gates = []
    stuck_blocked = []
    stale_claimed = []

    for t in roadmap.get("tasks", []):
        if not isinstance(t, dict):
            continue
        status = t.get("status", "")

        if status == "needs-human":
            needs_human.append(t)
            continue

        if (
            t.get("gate_human") is True
            and not t.get("approved_by_human", False)
            and status not in ("waiting", "done", "needs-human")
        ):
            pending_gates.append(t)
            continue

        if status == "blocked" and (t.get("passes") or 0) >= 3:
            stuck_blocked.append(t)
            continue

        if status in ("claimed", "in-progress"):
            age = days_since(t.get("updated"))
            if age is not None and age >= STALE_DAYS:
                stale_claimed.append(t)

    return {
        "needs_human": needs_human,
        "pending_gates": pending_gates,
        "stuck_blocked": stuck_blocked,
        "stale_claimed": stale_claimed,
    }


def task_label(slug: str, t: dict) -> str:
    tid = t.get("id", "?")
    title = t.get("title", "?")[:60]
    return f"{slug}/{tid} ({title})"


def kaizen_prompt(slug: str, buckets: dict, roadmap: dict) -> str | None:
    """Return the single highest-priority kaizen action sentence for this project."""
    if buckets["needs_human"]:
        t = buckets["needs_human"][0]
        tid = t.get("id", "?")
        title = t.get("title", "?")[:60]
        return f'Review {slug}/{tid} — "{title}" is waiting for your input in docs/ or projects/{slug}/.'

    if buckets["pending_gates"]:
        t = buckets["pending_gates"][0]
        tid = t.get("id", "?")
        title = t.get("title", "?")[:60]
        return f'Approve {slug}/{tid} — "{title}" is gated on your sign-off before the Worker can continue.'

    if buckets["stuck_blocked"]:
        t = buckets["stuck_blocked"][0]
        tid = t.get("id", "?")
        passes = t.get("passes", 0)
        title = t.get("title", "?")[:60]
        return f'Unblock {slug}/{tid} — "{title}" has passed {passes} times without resolution; decide whether to change scope or cancel.'

    if buckets["stale_claimed"]:
        t = buckets["stale_claimed"][0]
        tid = t.get("id", "?")
        age = days_since(t.get("updated"))
        days_str = f"{age:.0f}" if age is not None else "?"
        title = t.get("title", "?")[:60]
        return f'Check in on {slug}/{tid} — "{title}" has been claimed for {days_str}d with no update; Worker may be stuck.'

    return None


def honey_do_items(slug: str, buckets: dict) -> list[str]:
    """Return all Silas-only unblocks (excluding the top kaizen item already shown)."""
    items: list[str] = []
    first = True

    # needs-human: first one becomes the kaizen prompt; rest go to honey-do
    for t in buckets["needs_human"]:
        if first:
            first = False
            continue
        tid = t.get("id", "?")
        title = t.get("title", "?")[:60]
        items.append(f"Review and respond to `{slug}/{tid}` — {title}")

    # pending gates
    gate_first = True
    for t in buckets["pending_gates"]:
        if gate_first and not buckets["needs_human"]:
            gate_first = False
            continue  # already used as kaizen prompt
        gate_first = False
        tid = t.get("id", "?")
        title = t.get("title", "?")[:60]
        items.append(f"Approve or reject `{slug}/{tid}` — {title}")

    # stuck blocked
    sb_first = True
    for t in buckets["stuck_blocked"]:
        if sb_first and not buckets["needs_human"] and not buckets["pending_gates"]:
            sb_first = False
            continue
        sb_first = False
        tid = t.get("id", "?")
        title = t.get("title", "?")[:60]
        passes = t.get("passes", 0)
        items.append(f"Resolve or cancel `{slug}/{tid}` (pass {passes}) — {title}")

    # stale claimed
    sc_first = True
    for t in buckets["stale_claimed"]:
        if sc_first and not buckets["needs_human"] and not buckets["pending_gates"] and not buckets["stuck_blocked"]:
            sc_first = False
            continue
        sc_first = False
        tid = t.get("id", "?")
        title = t.get("title", "?")[:60]
        age = days_since(t.get("updated"))
        days_str = f"{age:.0f}" if age is not None else "?"
        items.append(f"Follow up on `{slug}/{tid}` ({days_str}d stale) — {title}")

    return items


# ---------------------------------------------------------------------------
# Report assembly
# ---------------------------------------------------------------------------

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_report(slugs: list[str], roadmaps: dict[str, dict]) -> str:
    lines: list[str] = []
    ts = now_iso()

    lines.append("# KAIZEN.md — Silas action queue")
    lines.append("")
    lines.append(f"Generated: {ts}")
    lines.append("")
    lines.append(
        "Each active project's top action for Silas, followed by its full honey-do list. "
        "Agent-workable items are excluded — these are human-only gates."
    )
    lines.append("")

    # -----------------------------------------------------------------------
    # Top kaizen section: one per project, sorted by priority level
    # -----------------------------------------------------------------------
    all_kaizens: list[tuple[int, str, str]] = []

    for slug in sorted(slugs):
        road = roadmaps.get(slug, {})
        if not road:
            continue
        buckets = classify_tasks(road)
        prompt = kaizen_prompt(slug, buckets, road)
        if prompt:
            # Priority score: needs_human=0, pending_gates=1, stuck=2, stale=3
            if buckets["needs_human"]:
                score = 0
            elif buckets["pending_gates"]:
                score = 1
            elif buckets["stuck_blocked"]:
                score = 2
            else:
                score = 3
            all_kaizens.append((score, slug, prompt))

    lines.append("## Top action per project")
    lines.append("")

    if not all_kaizens:
        lines.append("_No pending Silas actions across active projects. All clear!_")
    else:
        lines.append("| Priority | Project | Action |")
        lines.append("|---|---|---|")
        priority_labels = {0: "🔴 needs review", 1: "🟡 needs approval", 2: "🔵 stuck", 3: "⚪ stale"}
        for score, slug, prompt in sorted(all_kaizens):
            label = priority_labels.get(score, "?")
            lines.append(f"| {label} | {slug} | {prompt} |")

    lines.append("")

    # -----------------------------------------------------------------------
    # Per-project honey-do sections
    # -----------------------------------------------------------------------
    lines.append("## Per-project honey-do lists")
    lines.append("")

    any_items = False

    for slug in sorted(slugs):
        road = roadmaps.get(slug, {})
        if not road:
            continue
        buckets = classify_tasks(road)
        items = honey_do_items(slug, buckets)
        kaizen = kaizen_prompt(slug, buckets, road)

        if not kaizen and not items:
            continue  # no Silas actions needed for this project

        any_items = True
        project_title = road.get("project", slug)
        lines.append(f"### {project_title} (`{slug}`)")
        lines.append("")

        if kaizen:
            lines.append(f"**Top action:** {kaizen}")
            lines.append("")

        if items:
            lines.append("Also needs Silas:")
            lines.append("")
            for item in items:
                lines.append(f"- [ ] {item}")
            lines.append("")
        else:
            lines.append("_No additional honey-do items._")
            lines.append("")

    if not any_items:
        lines.append("_No Silas actions needed across any active project._")
        lines.append("")

    lines.append("---")
    lines.append(f"_Auto-generated by `scripts/build_kaizen.py` at {ts}_")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Build KAIZEN.md")
    parser.add_argument("--dry-run", action="store_true", help="Print report; do not write file")
    parser.add_argument("--output", default="KAIZEN.md", help="Output file path (default: KAIZEN.md)")
    args = parser.parse_args()

    overrides = load_overrides()
    slugs = active_slugs(overrides)

    if not slugs:
        print("WARNING: No active slugs found in project-overrides.yaml", file=sys.stderr)

    roadmaps: dict[str, dict] = {}
    for slug in slugs:
        rd = load_roadmap(slug)
        if rd:
            roadmaps[slug] = rd

    report = build_report(slugs, roadmaps)

    if args.dry_run:
        print(report)
    else:
        out = pathlib.Path(args.output)
        out.write_text(report)
        print(f"Written: {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
