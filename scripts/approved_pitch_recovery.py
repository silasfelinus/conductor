#!/usr/bin/env python3
"""Idempotently backfill approved PRE-cutover daily pitches into active build work.

Does not generate art, call Kind Robots, publish a route, or approve a release.
The post-2026-10-12 daily DELIVERY process remains owned by daily_project_deliveries.py.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

import daily_pitches as pitches
import intake

ROOT = Path(__file__).resolve().parent.parent
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True)
class RecoveryResult:
    stem: str
    target: str
    result: str


def approved_legacy_rows() -> list[dict]:
    """Use the materialized pitch decision, never an unapproved docket flag."""
    rows = []
    for date in pitches.all_docket_dates():
        if date >= pitches.EXPANSION_START:
            continue
        for row in pitches._rows(date):
            if row["decision"] != "approved":
                continue
            if not SLUG.fullmatch(str(row.get("slug", ""))):
                raise ValueError(f"invalid approved pitch slug: {row.get('slug')!r}")
            source = pitches.pitch_file(date, row["slug"])
            if not source.is_file():
                raise ValueError(f"approved pitch without decision file: {source}")
            rows.append(row)
    return rows


def _source(row: dict) -> str:
    return f"pitches/{row['stem']}.md"


def _next_task_id(text: str) -> str:
    ids = [int(n) for n in re.findall(r"(?m)^  - id: t-(\d+)\s*$", text)]
    return f"t-{max(ids, default=0) + 1:03d}"


def _quoted(text: str) -> str:
    return json.dumps(str(text).strip(), ensure_ascii=False)


def _append_task(path: Path, *, title: str, source: str, note: str,
                 depends_on: str | None = None, milestone: str | None = None) -> bool:
    original = path.read_text(encoding="utf-8")
    if source in original:
        return False
    parsed = yaml.safe_load(original)
    if not isinstance(parsed, dict) or not isinstance(parsed.get("tasks"), list):
        raise ValueError(f"not a valid task roadmap: {path}")
    milestones = parsed.get("milestones") or []
    selected = milestone or (str(milestones[-1]["id"]) if milestones else "m1")
    task_id = _next_task_id(original)
    block = (
        f"\n  - id: {task_id}\n"
        f"    milestone: {selected}\n"
        f"    title: {_quoted(title)}\n"
        "    status: ready\n"
        "    owner: null\n"
        "    passes: 0\n"
        "    stakes: reversible\n"
        f"    source_pitch: {_quoted(source)}\n"
        f"    note: {_quoted(note)}\n"
    )
    if depends_on:
        block += f"    depends_on: {depends_on}\n"
    path.write_text(original.rstrip("\n") + "\n" + block, encoding="utf-8")
    return True


def _ensure_standalone_tasks(row: dict) -> bool:
    slug, source = row["slug"], _source(row)
    roadmap = ROOT / "projects" / slug / "roadmap.yaml"
    if not roadmap.exists():
        raise ValueError(f"expected project scaffold: {roadmap}")
    text = roadmap.read_text(encoding="utf-8")
    parsed = yaml.safe_load(text) or {}
    if parsed.get("project") != slug:
        raise ValueError(f"project identity mismatch for {slug}")

    tasks = [task for task in parsed.get("tasks", []) if isinstance(task, dict)]
    if not tasks:
        raise ValueError(f"scaffold has no tasks: {slug}")
    milestones = [m.get("id") for m in parsed.get("milestones", [])
                  if isinstance(m, dict) and m.get("id")]
    if not milestones:
        raise ValueError(f"scaffold has no milestones: {slug}")

    followups = [
        (
            "Build an actual admin-only interactive preview",
            "Implement the first executable interaction under an /admin/ route, "
            "with an ADMIN tab, contextual tutorial, server authorization, and targeted tests. "
            "A scaffold or status URL is NOT a preview.",
        ),
        (
            "Implement the first playable or usable content slice and art",
            "Produce genuine mechanics/content and queue or reuse verified art through "
            "the normal no-unapproved-spend pipeline; test the experience, not only metadata.",
        ),
        (
            "Polish, verify and request explicit Play promotion",
            "Review phone/tablet/desktop usability, art relevance and functional checks. "
            "Only after a working build and owner approval may a public /play route launch; "
            "publishing and outward-facing operations remain human-gated.",
        ),
    ]
    # A pitch reference in t-003 is evidence of ONE slice, not proof that its
    # admin preview, art and release checks all exist. Match work per slice.
    existing = {
        str(task.get("title")): str(task.get("id"))
        for task in tasks
        if task.get("source_pitch") == source
    }
    implementation = next(
        (
            task for task in tasks
            if source in str(task.get("note", ""))
            and str(task.get("milestone")) == "m2"
            and any(word in str(task.get("title", "")).lower()
                    for word in ("ship", "build", "implement", "playable"))
        ),
        None,
    )
    added = ""
    ids: list[str] = []
    for index, (title, note) in enumerate(followups):
        prior = existing.get(title)
        if not prior and index == 1 and implementation:
            prior = str(implementation["id"])
        if prior:
            ids.append(prior)
            continue
        task_id = _next_task_id(text + added)
        milestone = ("m2" if index < 2 else "m3")
        if milestone not in milestones:
            milestone = str(milestones[-1])
        added += (
            f"\n  - id: {task_id}\n"
            f"    milestone: {milestone}\n"
            f"    title: {_quoted(title)}\n"
            "    status: ready\n"
            "    owner: null\n"
            "    passes: 0\n"
            "    stakes: reversible\n"
            f"    source_pitch: {_quoted(source)}\n"
            f"    note: {_quoted(note + ' Pitch: ' + row.get('hook', ''))}\n"
        )
        if ids and index == 2:
            # Polish waits for playable content, not only for the UI scaffold.
            added += f"    depends_on: {ids[-1]}\n"
        ids.append(task_id)
    if not added:
        return False
    roadmap.write_text(text.rstrip("\n") + "\n" + added, encoding="utf-8")
    return True


def _queue_arcade(row: dict) -> bool:
    path = ROOT / "projects" / "kr-arcade" / "games.yaml"
    original = path.read_text(encoding="utf-8")
    games = (yaml.safe_load(original) or {}).get("games", [])
    if any(g.get("slug") == row["slug"] for g in games if isinstance(g, dict)):
        return False
    source = _source(row)
    if source in original:
        return False
    if not re.search(r"(?m)^games:\s*$", original):
        raise ValueError("arcade games.yaml lacks the games list")

    block = (
        f"  - slug: {row['slug']}\n"
        f"    title: {_quoted(row['title'])}\n"
        "    status: queued\n"
        f"    effort: {row.get('effort', 'medium')}\n"
        f"    source: {_quoted(source)}\n"
        f"    hook: {_quoted(row.get('hook', ''))}\n"
        f"    challenge: {_quoted(row.get('first_slice', 'Build a playable first slice.'))}\n"
    )
    lines = original.splitlines(keepends=True)
    insert_at = None
    for index, line in enumerate(lines):
        if not line.startswith("  - slug: "):
            continue
        next_index = next(
            (j for j in range(index + 1, len(lines)) if lines[j].startswith("  - slug: ")),
            len(lines),
        )
        if any(re.match(r"^\s+status:\s*queued\s*$", item) for item in lines[index:next_index]):
            insert_at = index
            break
    if insert_at is None:
        insert_at = len(lines)
    lines.insert(insert_at, block)
    path.write_text("".join(lines), encoding="utf-8")
    return True


def recover_one(row: dict) -> RecoveryResult:
    source = _source(row)
    target = pitches.target_of(row)
    if target and target != "new":
        if target == "kr-arcade":
            changed = _queue_arcade(row)
        else:
            roadmap = ROOT / "projects" / target / "roadmap.yaml"
            if not roadmap.is_file():
                raise ValueError(f"approved pitch points to missing target {target}: {source}")
            changed = _append_task(
                roadmap,
                title=f"Implement approved pitch: {row['title']}",
                source=source,
                note=(
                    f"Build and test the approved addition from {source}, "
                    "with working implementation and verified art if appropriate. "
                    "Keep public promotion human-gated. "
                    f"First slice: {row.get('first_slice', '')}"
                ),
            )
        return RecoveryResult(row["stem"], target, "queued" if changed else "already-linked")

    slug = row["slug"]
    project = ROOT / "projects" / slug
    if not project.exists():
        intake.main([
            slug, "--kind", "software", "--title", str(row["title"]),
            "--goal", str(row.get("hook", "")),
            "--desc", str(row.get("hook", "")),
            "--repo", "silasfelinus/kind_robots",
        ])
    changed = _ensure_standalone_tasks(row)
    return RecoveryResult(row["stem"], slug, "queued" if changed else "already-linked")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true",
                        help="Create registered projects or add actionable tasks; default reports only")
    args = parser.parse_args()
    rows = approved_legacy_rows()
    if not args.apply:
        print(json.dumps([
            {"stem": r["stem"], "target": pitches.target_of(r) or r["slug"]}
            for r in rows
        ], indent=2))
        return 0
    results = [recover_one(row) for row in rows]
    print(json.dumps([r.__dict__ for r in results], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
