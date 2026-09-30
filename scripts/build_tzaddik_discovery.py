#!/usr/bin/env python3
"""build_tzaddik_discovery.py -- Daily Tzaddik discovery docket pipeline (tzaddik-gallery/t-014).

DESIGN-BRIEF.md's "Daily discovery roster" section calls for a research pipeline
"inspired by Daily Dream": each Pacific day the project prepares 20 sourced
suggestions (10 living, 10 deceased), each with a pitch, Wikipedia provenance,
review note, region, and controlled editorial tags, deduplicated against
canonical membership and everyone already suggested.

Unlike Daily Dream, a Tzaddik docket has no separate propose/build phases --
DESIGN-BRIEF.md's contract is "prepared and available for Silas to review", so a
docket file *is* the deliverable the moment it is written; tzaddik-gallery/t-015
(a review surface) and t-016 (the recurring daily cycle) are separate, later
tasks. This script only owns the mechanical parts a script can safely own:
tracking what has already been suggested (dedup), validating a candidate batch
against DESIGN-BRIEF.md's contract, and rendering the docket file in the
established format from projects/tzaddik-gallery/discovery/2026-09-26.md (the
first, hand-authored docket). The actual research/sourcing/writing is done by
whatever session invokes --from-json, the same division of labor
build_dream_proposal.py uses for dream proposals.

Usage:
    python scripts/build_tzaddik_discovery.py --check
    python scripts/build_tzaddik_discovery.py --brief [--date YYYY-MM-DD]
    python scripts/build_tzaddik_discovery.py --from-json <path> [--force]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
DISCOVERY_DIR = ROOT / "projects" / "tzaddik-gallery" / "discovery"
SEED_SETS_PATH = ROOT / "projects" / "tzaddik-gallery" / "seed-sets.yaml"
BLACKLIST_PATH = ROOT / "projects" / "tzaddik-gallery" / "blacklist.yaml"

REQUIRED_PER_STATUS = 10

# Verbatim from DESIGN-BRIEF.md's "Tags and browsing taxonomy" controlled set.
CONTROLLED_TAGS = [
    "Politics",
    "Pop Culture",
    "Humanitarian",
    "Science & Medicine",
    "Education",
    "Environment",
    "Civil Rights & Justice",
    "Peace & Diplomacy",
    "Community & Mutual Aid",
    "Arts & Culture",
    "Journalism & Truth",
    "Courage & Rescue",
]

REQUIRED_ENTRY_FIELDS = ("name", "region", "domain", "pitch", "wikipedia", "review_note", "tags")

META_RE = re.compile(r"<!--\s*tzaddik-meta:\s*(\{.*?\})\s*-->")
HEADING_RE = re.compile(r"^### (.+?) — (.+?) — (.+)$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _pacific_today() -> str:
    # No zoneinfo dependency in this sandbox's minimal Python install is guaranteed;
    # Pacific is UTC-7/UTC-8. Using UTC-8 (standard time) as the stable, documented
    # approximation the rest of this repo's Pacific-date helpers also accept.
    return (datetime.now(timezone.utc) - timedelta(hours=8)).strftime("%Y-%m-%d")


def _files() -> list[Path]:
    if not DISCOVERY_DIR.exists():
        return []
    return sorted(p for p in DISCOVERY_DIR.glob("*.md"))


def parse_docket(path: Path) -> dict[str, Any]:
    """Extract the date and every person entry from a docket file.

    Tolerant of hand-authored dockets (like 2026-09-26.md) that predate the
    tzaddik-meta comment: entries without it still contribute their name to
    dedup, just without tags/status metadata.
    """
    text = path.read_text(encoding="utf-8")
    date_match = DATE_RE.match(path.stem)
    date = path.stem if date_match else None

    entries: list[dict[str, Any]] = []
    section = None
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip() == "## Living suggestions":
            section = "living"
        elif line.strip() == "## Memorial suggestions":
            section = "deceased"
        heading = HEADING_RE.match(line)
        if heading and section:
            name, region, domain = heading.groups()
            entry: dict[str, Any] = {
                "name": name.strip(),
                "region": region.strip(),
                "domain": domain.strip(),
                "status": section,
                "tags": [],
            }
            # Scan forward to the next heading/section for a meta comment.
            j = i + 1
            while j < len(lines) and not HEADING_RE.match(lines[j]) and not lines[j].startswith("## "):
                meta = META_RE.search(lines[j])
                if meta:
                    try:
                        parsed = json.loads(meta.group(1))
                    except json.JSONDecodeError:
                        parsed = {}
                    if isinstance(parsed, dict):
                        entry["tags"] = parsed.get("tags", [])
                j += 1
            entries.append(entry)
        i += 1
    return {"date": date, "path": path, "entries": entries}


def all_dockets() -> list[dict[str, Any]]:
    return [parse_docket(p) for p in _files()]


def _seed_set_names() -> set[str]:
    if not SEED_SETS_PATH.exists():
        return set()
    data = yaml.safe_load(SEED_SETS_PATH.read_text(encoding="utf-8")) or {}
    names: set[str] = set()
    for bucket in ("living", "memorial"):
        for person in data.get(bucket, []) or []:
            if isinstance(person, dict) and person.get("name"):
                names.add(str(person["name"]))
    return names


def excluded_names() -> set[str]:
    """Every name that has already been suggested or accepted, for dedup.

    Covers canonical/accepted seed-set membership plus everyone appearing in any
    prior discovery docket, matching DESIGN-BRIEF.md's "dedupe state against
    canonical, historical, pending, rejected, deferred, and recently suggested
    people": every docketed name stays in this pool permanently regardless of
    what Silas later decides (approved/rejected/deferred, tracked in
    projects/tzaddik-gallery/discovery-decisions.yaml by tzaddik_review.py, t-015)
    -- once suggested, a name is never re-suggested, so a rejection can't
    immediately boomerang back into a future docket.
    """
    names = set(_seed_set_names())
    for docket in all_dockets():
        for entry in docket["entries"]:
            names.add(entry["name"])
    return names


def _norm(name: str) -> str:
    return re.sub(r"\s+", " ", name.strip()).casefold()


def blacklist_key(name: str) -> str:
    """Accent-, case-, and punctuation-insensitive key for blacklist matching.

    "Ghandi", "César Chávez", and "J.K. Rowling" must all hit their entries, so
    this is looser than _norm (which dedup uses and keeps exact spellings).
    """
    decomposed = unicodedata.normalize("NFKD", name)
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "", stripped.casefold())


def load_blacklist() -> dict[str, str]:
    """Map every blacklisted name/alias key to its canonical entry name.

    projects/tzaddik-gallery/blacklist.yaml (Silas, 2026-09-30) lists people
    who must never be nominated. A missing file means an empty blacklist.
    """
    if not BLACKLIST_PATH.exists():
        return {}
    data = yaml.safe_load(BLACKLIST_PATH.read_text(encoding="utf-8")) or {}
    result: dict[str, str] = {}
    for entry in data.get("entries", []) or []:
        if not isinstance(entry, dict) or not entry.get("name"):
            continue
        canonical = str(entry["name"])
        for alias in [canonical, *(entry.get("aliases") or [])]:
            key = blacklist_key(str(alias))
            if key:
                result[key] = canonical
    return result


def blacklisted_as(name: str, blacklist: dict[str, str] | None = None) -> str | None:
    """Return the blacklist entry a name matches, or None."""
    table = load_blacklist() if blacklist is None else blacklist
    return table.get(blacklist_key(name))


def check() -> int:
    dockets = all_dockets()
    if not dockets:
        print("No discovery dockets found yet -- the pipeline has never produced one.")
        return 1
    dated = sorted((d for d in dockets if d["date"]), key=lambda d: d["date"])
    latest_label = dated[-1]["date"] if dated else "none (no dated dockets yet)"
    total_names = len(excluded_names())
    print(f"{len(dockets)} discovery docket(s) on file, most recent: {latest_label}.")
    print(f"{total_names} distinct name(s) already suggested or accepted (dedup pool).")
    counts: dict[str, int] = {}
    for docket in dockets:
        for entry in docket["entries"]:
            for tag in entry.get("tags") or []:
                counts[tag] = counts.get(tag, 0) + 1
    if counts:
        print("Tag distribution across all dockets so far:")
        for tag, n in sorted(counts.items(), key=lambda kv: -kv[1]):
            print(f"  {tag}: {n}")
    else:
        print("No tag metadata recorded yet (pre-pipeline dockets predate tzaddik-meta comments).")
    return 0


def brief(date: str | None) -> int:
    date = date or _pacific_today()
    if not DATE_RE.match(date):
        print(f"error: --date must be YYYY-MM-DD, got {date!r}", file=sys.stderr)
        return 2
    payload = {
        "date": date,
        "required": {"living": REQUIRED_PER_STATUS, "deceased": REQUIRED_PER_STATUS},
        "controlled_tags": CONTROLLED_TAGS,
        "excluded_names": sorted(excluded_names()),
        "blacklisted_names": sorted(set(load_blacklist().values())),
        "entry_fields": list(REQUIRED_ENTRY_FIELDS),
        "instructions": (
            "Research exactly 10 living and 10 deceased candidates not in "
            "excluded_names or blacklisted_names (and no one with a comparable "
            "record: abuse, enslavement, atrocity, bigotry campaigns, fraud). Favor breadth beyond US/Anglosphere celebrity per "
            "DESIGN-BRIEF.md's 'Escaping the Anglosphere gravity well'. Each "
            "entry needs a real Wikipedia URL, a concrete sourced pitch, a "
            "review_note flagging meaningful documented controversy/objections "
            "(or explicitly noting none found), region/domain context, and 1+ "
            "tags drawn only from controlled_tags. Write the batch as JSON: "
            '{"date": ..., "living": [10 entries], "memorial": [10 entries]} '
            "and pass it to --from-json."
        ),
    }
    print(json.dumps(payload, indent=2))
    return 0


def _validate_entry(
    entry: dict[str, Any],
    index: int,
    status: str,
    seen: set[str],
    excluded: set[str],
    blacklist: dict[str, str] | None = None,
) -> list[str]:
    errors = []
    prefix = f"{status}[{index}]"
    for field in REQUIRED_ENTRY_FIELDS:
        if field == "tags":
            continue
        if not str(entry.get(field, "")).strip():
            errors.append(f"{prefix}: missing/empty '{field}'")
    tags = entry.get("tags")
    if not tags or not isinstance(tags, list):
        errors.append(f"{prefix}: 'tags' must be a non-empty list")
    else:
        bad = [t for t in tags if t not in CONTROLLED_TAGS]
        if bad:
            errors.append(f"{prefix}: tag(s) not in the controlled vocabulary: {bad}")
    name = str(entry.get("name", "")).strip()
    if name:
        key = _norm(name)
        if key in seen:
            errors.append(f"{prefix}: duplicate name within this batch: {name!r}")
        seen.add(key)
        if key in excluded:
            errors.append(f"{prefix}: {name!r} was already suggested or accepted (dedup violation)")
        match = blacklisted_as(name, blacklist or {})
        if match:
            errors.append(f"{prefix}: {name!r} is on the blacklist (as {match!r}); see blacklist.yaml")
    wiki = str(entry.get("wikipedia", ""))
    if wiki and not wiki.startswith("http"):
        errors.append(f"{prefix}: 'wikipedia' does not look like a URL: {wiki!r}")
    return errors


def validate_batch(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    date = payload.get("date")
    if not date or not DATE_RE.match(str(date)):
        errors.append(f"'date' must be YYYY-MM-DD, got {date!r}")

    living = payload.get("living")
    memorial = payload.get("memorial")
    if not isinstance(living, list) or len(living) != REQUIRED_PER_STATUS:
        errors.append(f"'living' must be a list of exactly {REQUIRED_PER_STATUS} entries")
        living = living if isinstance(living, list) else []
    if not isinstance(memorial, list) or len(memorial) != REQUIRED_PER_STATUS:
        errors.append(f"'memorial' must be a list of exactly {REQUIRED_PER_STATUS} entries")
        memorial = memorial if isinstance(memorial, list) else []

    excluded = excluded_names()
    excluded_norm = {_norm(n) for n in excluded}
    blacklist = load_blacklist()
    seen: set[str] = set()
    for i, entry in enumerate(living):
        errors.extend(_validate_entry(entry, i, "living", seen, excluded_norm, blacklist))
    for i, entry in enumerate(memorial):
        errors.extend(_validate_entry(entry, i, "memorial", seen, excluded_norm, blacklist))
    return errors


def render_docket(payload: dict[str, Any]) -> str:
    date = payload["date"]
    lines = [f"# Daily Tzaddik discovery docket — {date}", ""]
    lines.append(
        "Automated pipeline output (scripts/build_tzaddik_discovery.py). These are "
        "**suggestions for Silas to vet**, not canonical members. Wikipedia is the "
        "default source; every candidate still needs the normal ingest-time "
        "living/deceased verification, image provenance check, and controversy review."
    )
    lines.append("")

    def render_section(title: str, entries: list[dict[str, Any]]) -> None:
        lines.append(f"## {title}")
        lines.append("")
        for entry in entries:
            lines.append(f"### {entry['name']} — {entry['region']} — {entry['domain']}")
            meta = json.dumps({"status": entry.get("_status"), "tags": entry.get("tags", [])})
            lines.append(f"<!-- tzaddik-meta: {meta} -->")
            lines.append(f"**Pitch:** {entry['pitch']}")
            lines.append("")
            lines.append(f"**Wikipedia:** {entry['wikipedia']}")
            lines.append("")
            lines.append(f"**Review note:** {entry['review_note']}")
            lines.append("")

    for entry in payload["living"]:
        entry["_status"] = "living"
    for entry in payload["memorial"]:
        entry["_status"] = "deceased"

    render_section("Living suggestions", payload["living"])
    render_section("Memorial suggestions", payload["memorial"])
    return "\n".join(lines).rstrip() + "\n"


def from_json(path: Path, force: bool) -> int:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: could not read/parse {path}: {exc}", file=sys.stderr)
        return 2
    if not isinstance(payload, dict):
        print("error: top-level JSON must be an object", file=sys.stderr)
        return 2

    errors = validate_batch(payload)
    if errors:
        print("Batch failed validation:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    date = payload["date"]
    out_path = DISCOVERY_DIR / f"{date}.md"
    if out_path.exists() and not force:
        print(f"error: {out_path} already exists (use --force to overwrite)", file=sys.stderr)
        return 3

    DISCOVERY_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_docket(payload), encoding="utf-8")
    print(f"Wrote {out_path} (10 living + 10 memorial suggestions).")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true", help="Report docket buffer/dedup state")
    group.add_argument("--brief", action="store_true", help="Print a JSON authoring brief")
    group.add_argument("--from-json", metavar="PATH", help="Validate and write a docket from a JSON batch")
    parser.add_argument("--date", help="Pacific date (YYYY-MM-DD) for --brief; defaults to today")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing docket for --from-json")
    args = parser.parse_args(argv)

    if args.check:
        return check()
    if args.brief:
        return brief(args.date)
    return from_json(Path(args.from_json), args.force)


if __name__ == "__main__":
    raise SystemExit(main())
