#!/usr/bin/env python3
"""daily_pitches.py -- the daily project-pitch docket: five new project ideas per day.

Silas, 2026-10-02: Kind Robots has a lot of features locked behind LLM API access, while
image generation and authoring tokens are plentiful. Every day's digest therefore carries
FIVE new project pitches, biased toward things anyone can use with zero tokens at runtime
(games, toys, pre-written content, pre-generated art).

Flow (sessions author, Silas decides):
  1. A session runs `--brief`, then writes pitches/daily/<pacific-date>.yaml (five pitches).
  2. `--check` validates it (five, >= 3 zero-LLM, deduped against projects, pitches and
     earlier days); `--materialize` writes one pitches/<date>-<slug>.md per pitch with
     `status: awaiting-silas`. Those files ARE the decision record: the Kind Robots project
     page already lists and votes on pitches/*.md.
  3. The digest shows the five (plus any still-undecided earlier ones) with signed Approve /
     Pass links (scripts/pitch_links.py). Silas decides by clicking, or on the project page.
  4. An approved pitch is scaffolded into a project with scripts/intake.py by the next
     session (`--approved` lists approved pitches that have no project yet).

Arcade games (Silas, 2026-10-06): a pitch may carry `target: kr-arcade` (any existing project
slug works the same way). It is then a new cabinet for the Kind Robots Arcade, not a new project:
it materializes with `project-target: kr-arcade`, and once approved `--approved` says to add it to
projects/kr-arcade/games.yaml rather than scaffold it with intake.py.

Usage:
    python scripts/daily_pitches.py --brief                       # what to avoid + the rules
    python scripts/daily_pitches.py --check [--date YYYY-MM-DD]   # docket exists, valid, materialized
    python scripts/daily_pitches.py --materialize [--date ...]    # write pitches/<date>-<slug>.md
    python scripts/daily_pitches.py --payload [--date ...]        # JSON for the digest
    python scripts/daily_pitches.py --pending                     # undecided pitches, newest first
    python scripts/daily_pitches.py --approved                    # approved, not yet a project
    python scripts/daily_pitches.py --decide STEM approved|rejected   # same effect as the email link

Exit codes: 0 ok, 1 missing/invalid docket (author one), 2 unresolved (bad arguments).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
DAILY_DIR = ROOT / "pitches" / "daily"

PITCHES_PER_DAY = 5
MIN_ZERO_LLM = 3  # at least this many of the five must need no LLM at runtime
CARRY_OVER_LIMIT = 5  # undecided pitches from earlier days still shown in the digest
VALID_DECISIONS = ("approved", "rejected")
LLM_AT_RUNTIME = ("none", "optional", "required")
EFFORTS = ("small", "medium", "large")
REQUIRED = ("slug", "title", "hook", "llm_at_runtime", "effort", "art_plan", "first_slice")
ARCADE_PROJECT = "kr-arcade"
MAX_TARGETED = 2  # pitches aimed at an existing project (arcade cabinets) per day; the rest stay new projects
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MIN_HOOK_WORDS = 15
PENDING_STATUS = "awaiting-silas"


def pacific_today() -> str:
    return (datetime.now(timezone.utc) - timedelta(hours=8)).strftime("%Y-%m-%d")


def docket_path(date: str) -> Path:
    return DAILY_DIR / f"{date}.yaml"


def load_docket(date: str) -> dict[str, Any] | None:
    path = docket_path(date)
    if not path.exists():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def all_docket_dates() -> list[str]:
    return sorted(p.stem for p in DAILY_DIR.glob("????-??-??.yaml"))


def stem(date: str, slug: str) -> str:
    return f"{date}-{slug}"


def pitch_file(date: str, slug: str) -> Path:
    return ROOT / "pitches" / f"{stem(date, slug)}.md"


def read_status(path: Path) -> str:
    """The pitch file's `status:` (the single decision record); awaiting-silas when absent."""
    if not path.exists():
        return PENDING_STATUS
    match = re.search(r"^status:\s*([^#\n]*)", path.read_text(encoding="utf-8"), re.MULTILINE)
    return (match.group(1).strip() if match else "") or PENDING_STATUS


def modifications(path: Path) -> str:
    """Silas's approve-with-changes notes (the pitch file's modifications section), or ''."""
    notes: list[str] = []
    inside = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## Silas's modifications"
        elif inside:
            notes.append(line)
    return " ".join(" ".join(notes).split())


def decision_label(status: str) -> str:
    if status == PENDING_STATUS:
        return "pending"
    return "rejected" if status in ("rejected", "passed", "declined") else status


def existing_slugs(exclude_materialized: bool = True) -> set[str]:
    """Slugs that already exist as projects or hand-written (non-docket) pitch files."""
    slugs = {p.name for p in (ROOT / "projects").iterdir() if p.is_dir()}
    docket_stems = {
        stem(d, p.get("slug", ""))
        for d in all_docket_dates()
        for p in (load_docket(d) or {}).get("pitches", [])
        if isinstance(p, dict)
    }
    for path in (ROOT / "pitches").glob("*.md"):
        if exclude_materialized and path.stem in docket_stems:
            continue
        slugs.add(re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem))
    return slugs | arcade_game_slugs()


def arcade_game_slugs() -> set[str]:
    """Games already in the Arcade's queue (projects/kr-arcade/games.yaml), so a pitch never repeats one."""
    path = ROOT / "projects" / ARCADE_PROJECT / "games.yaml"
    if not path.exists():
        return set()
    games = (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("games") or []
    return {str(g.get("slug")) for g in games if isinstance(g, dict) and g.get("slug")}


def target_of(pitch: dict[str, Any]) -> str:
    return str(pitch.get("target") or "").strip()


def validate(date: str, docket: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    pitches = docket.get("pitches")
    if not isinstance(pitches, list) or len(pitches) != PITCHES_PER_DAY:
        return [f"{date}: needs exactly {PITCHES_PER_DAY} pitches, found "
                f"{len(pitches) if isinstance(pitches, list) else 'none'}"]
    prior: set[str] = set()
    for other in all_docket_dates():
        if other != date:
            prior |= {p.get("slug", "") for p in (load_docket(other) or {}).get("pitches", []) if isinstance(p, dict)}
    taken = existing_slugs()
    seen: set[str] = set()
    zero_llm = 0
    targeted = 0
    for i, pitch in enumerate(pitches, 1):
        where = f"{date} pitch {i}"
        if not isinstance(pitch, dict):
            errors.append(f"{where}: must be a mapping")
            continue
        for key in REQUIRED:
            if not str(pitch.get(key) or "").strip():
                errors.append(f"{where}: missing '{key}'")
        slug = str(pitch.get("slug") or "")
        where = f"{where} ({slug or '?'})"
        if slug and not SLUG_RE.match(slug):
            errors.append(f"{where}: slug must be lowercase-hyphenated")
        if slug in seen:
            errors.append(f"{where}: duplicate slug inside the day")
        seen.add(slug)
        if slug in prior:
            errors.append(f"{where}: slug already pitched on an earlier day")
        # Once materialized, the pitch is already part of the system (and may even be a project).
        if slug in taken and not pitch_file(date, slug).exists():
            errors.append(f"{where}: slug already exists as a project or pitch")
        if str(pitch.get("llm_at_runtime")) not in LLM_AT_RUNTIME:
            errors.append(f"{where}: llm_at_runtime must be one of {LLM_AT_RUNTIME}")
        if pitch.get("llm_at_runtime") == "none":
            zero_llm += 1
        target = target_of(pitch)
        if target:
            targeted += 1
            if not (ROOT / "projects" / target).is_dir():
                errors.append(f"{where}: target '{target}' is not an existing project")
        if str(pitch.get("effort")) not in EFFORTS:
            errors.append(f"{where}: effort must be one of {EFFORTS}")
        if len(str(pitch.get("hook") or "").split()) < MIN_HOOK_WORDS:
            errors.append(f"{where}: hook needs at least {MIN_HOOK_WORDS} words (a complete idea, not a label)")
    if targeted > MAX_TARGETED:
        errors.append(f"{date}: at most {MAX_TARGETED} of {PITCHES_PER_DAY} pitches may carry a target "
                      f"(found {targeted}); the rest pitch new projects")
    if zero_llm < MIN_ZERO_LLM:
        errors.append(f"{date}: at least {MIN_ZERO_LLM} of {PITCHES_PER_DAY} pitches must be llm_at_runtime: none "
                      f"(found {zero_llm})")
    return errors


def pitch_markdown(date: str, pitch: dict[str, Any]) -> str:
    """Render one docket pitch in the canonical pitch template (AGENTS.md)."""
    hook = " ".join(str(pitch["hook"]).split())
    llm = {
        "none": "It needs no LLM at runtime, so it is free for every visitor.",
        "optional": "An LLM can enrich it but is not required at runtime.",
        "required": "It needs an LLM at runtime.",
    }[str(pitch["llm_at_runtime"])]
    why = f"{llm} Art plan: {' '.join(str(pitch['art_plan']).split())}"
    return (
        f"# Pitch: {pitch['title']}\n"
        f"date: {date}\n"
        f"project-target: {target_of(pitch) or 'new'}\n"
        f"status: {PENDING_STATUS}\n\n"
        f"## The idea\n{hook}\n\n"
        f"## Why it's worth doing\n{why}\n\n"
        f"## Rough effort\n{pitch['effort']}\n\n"
        f"## Suggested first task\n{' '.join(str(pitch['first_slice']).split())}\n"
    )


def materialize(date: str) -> list[Path]:
    """Write pitches/<date>-<slug>.md for each docket pitch; never overwrite (status is the decision)."""
    written = []
    for pitch in (load_docket(date) or {}).get("pitches", []):
        path = pitch_file(date, pitch["slug"])
        if not path.exists():
            path.write_text(pitch_markdown(date, pitch), encoding="utf-8")
            written.append(path)
    return written


def _rows(date: str) -> list[dict[str, Any]]:
    rows = []
    for pitch in (load_docket(date) or {}).get("pitches", []):
        record = dict(pitch)
        record["date"] = date
        record["stem"] = stem(date, pitch["slug"])
        record["decision"] = decision_label(read_status(pitch_file(date, pitch["slug"])))
        rows.append(record)
    return rows


def pending_all() -> list[dict[str, Any]]:
    return [r for d in reversed(all_docket_dates()) for r in _rows(d) if r["decision"] == "pending"]


def payload(date: str) -> dict[str, Any] | None:
    """Today's five, plus undecided pitches still waiting from earlier days."""
    if load_docket(date) is None:
        return None
    today = _rows(date)
    carried = [r for r in pending_all() if r["date"] != date][:CARRY_OVER_LIMIT]
    return {"date": date, "pitches": today, "carried_over": carried}


def cmd_brief() -> int:
    print(f"Daily pitch docket brief ({pacific_today()}): author pitches/daily/{pacific_today()}.yaml")
    print(f"\nRules: exactly {PITCHES_PER_DAY} pitches; >= {MIN_ZERO_LLM} with llm_at_runtime: none; each hook a "
          f"complete idea of >= {MIN_HOOK_WORDS} words; effort small|medium|large.")
    print("Theme: free-to-play, no LLM at runtime; sessions pre-author words and pre-generate art. Mix kinds "
          "(games, toys, tools, story/content, art collections). Extend what ships; no SaaS filler, nothing "
          "needing licensing review.")
    print(f"Arcade: up to {MAX_TARGETED} of the five may be Kind Robots arcade cabinets for the Arcade tab -- set "
          f"`target: {ARCADE_PROJECT}`. Riff on a golden-age classic's mechanics (never its name, sprites or "
          f"levels), name the classic in the hook, and keep it achievable: intro splash, rising difficulty, a "
          f"leaderboard score. Already queued: projects/{ARCADE_PROJECT}/games.yaml (listed below).")
    print("Fields per pitch: slug (lowercase-hyphenated), title, hook, llm_at_runtime, effort, art_plan, first_slice"
          f"; optional target ({ARCADE_PROJECT} for an arcade cabinet)")
    print("\nDo NOT repeat any of these (projects, pitches, earlier daily slugs):")
    taken = sorted(existing_slugs(exclude_materialized=False))
    print("  " + ", ".join(taken))
    print("\nThen: python scripts/daily_pitches.py --check && python scripts/daily_pitches.py --materialize")
    return 0


def cmd_check(date: str) -> int:
    docket = load_docket(date)
    if docket is None:
        print(f"daily_pitches: no docket for {date}; run `python scripts/daily_pitches.py --brief` and author "
              f"pitches/daily/{date}.yaml ({PITCHES_PER_DAY} pitches, >= {MIN_ZERO_LLM} with llm_at_runtime: none)")
        return 1
    errors = validate(date, docket)
    missing = [p["slug"] for p in docket.get("pitches", []) if isinstance(p, dict)
               and "slug" in p and not pitch_file(date, p["slug"]).exists()]
    if missing and not errors:
        errors.append(f"{date}: not materialized ({len(missing)} pitch file(s) missing); "
                      f"run `python scripts/daily_pitches.py --materialize --date {date}`")
    if errors:
        print(f"daily_pitches: {date} docket invalid")
        for error in errors:
            print("  - " + error)
        return 1
    today_pending = sum(1 for r in _rows(date) if r["decision"] == "pending")
    print(f"daily_pitches: {date} docket ok ({PITCHES_PER_DAY} pitches, {today_pending} undecided today; "
          f"{len(pending_all())} undecided overall)")
    return 0


def cmd_materialize(date: str) -> int:
    code = 0
    docket = load_docket(date)
    if docket is None:
        print(f"no docket for {date}", file=sys.stderr)
        return 1
    errors = validate(date, docket)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    written = materialize(date)
    print(f"materialized {len(written)} pitch file(s) for {date}" + "".join(f"\n  {p.name}" for p in written))
    return code


def cmd_pending() -> int:
    rows = pending_all()
    if not rows:
        print("daily_pitches: nothing pending")
        return 0
    for row in rows:
        print(f"{row['stem']}  [{row['effort']}, llm:{row['llm_at_runtime']}]  {row['title']}")
    return 0


def cmd_approved() -> int:
    """Approved pitches that have not become a project yet (the next session scaffolds them)."""
    projects = {p.name for p in (ROOT / "projects").iterdir() if p.is_dir()}
    games = arcade_game_slugs()
    todo = [r for d in all_docket_dates() for r in _rows(d) if r["decision"] == "approved"
            and r["slug"] not in projects and not (target_of(r) and r["slug"] in games)]
    for row in todo:
        target = target_of(row)
        if target == ARCADE_PROJECT:
            print(f"{row['stem']}  {row['title']}  -> add to projects/{ARCADE_PROJECT}/games.yaml as status: queued, "
                  f"source: pitches/{row['stem']}.md, ahead of the first queued catalog game (no intake.py)")
        elif target:
            print(f"{row['stem']}  {row['title']}  -> add as a ready task in projects/{target}/roadmap.yaml "
                  f"(no intake.py)")
        else:
            print(f"{row['stem']}  {row['title']}  -> python scripts/intake.py {row['slug']} --kind software "
                  f"--title \"{row['title']}\" --goal \"...\" --repo silasfelinus/kind_robots")
        mods = modifications(pitch_file(row["date"], row["slug"]))
        if mods:
            print(f"    APPROVED WITH CHANGES (fold these into the project goal): {mods}")
    if not todo:
        print("daily_pitches: no approved pitch is waiting for a project")
    return 0


def cmd_decide(pitch_stem: str, decision: str) -> int:
    if decision not in VALID_DECISIONS:
        print(f"decision must be one of {VALID_DECISIONS}", file=sys.stderr)
        return 2
    path = ROOT / "pitches" / f"{pitch_stem}.md"
    if not path.exists():
        print(f"unknown pitch: {pitch_stem}", file=sys.stderr)
        return 2
    text = path.read_text(encoding="utf-8")
    line = f"status: {decision}"
    if re.search(r"^status:", text, re.MULTILINE):
        text = re.sub(r"^status:.*$", line, text, count=1, flags=re.MULTILINE)
    else:
        # A hand-written record with no `status:` line (2026-08-11-retire-wonderlab.md) used to make
        # this a silent no-op, so the pitch stayed awaiting-silas however often it was approved.
        anchor = (re.search(r"^project-target:.*$", text, re.MULTILINE)
                  or re.search(r"^# .*$", text, re.MULTILINE))
        text = text[:anchor.end()] + "\n" + line + text[anchor.end():] if anchor else f"{line}\n{text}"
    path.write_text(text, encoding="utf-8")
    print(f"recorded {pitch_stem}: {read_status(path)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--date", default=pacific_today())
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--brief", action="store_true")
    group.add_argument("--check", action="store_true")
    group.add_argument("--materialize", action="store_true")
    group.add_argument("--payload", action="store_true")
    group.add_argument("--pending", action="store_true")
    group.add_argument("--approved", action="store_true")
    group.add_argument("--decide", nargs=2, metavar=("STEM", "DECISION"))
    args = parser.parse_args()
    if args.brief:
        return cmd_brief()
    if args.check:
        return cmd_check(args.date)
    if args.materialize:
        return cmd_materialize(args.date)
    if args.payload:
        print(json.dumps(payload(args.date)))
        return 0
    if args.pending:
        return cmd_pending()
    if args.approved:
        return cmd_approved()
    return cmd_decide(args.decide[0], args.decide[1])


if __name__ == "__main__":
    sys.exit(main())
