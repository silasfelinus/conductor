#!/usr/bin/env python3
"""Create a deterministic Facet-seeded six-asset daily dream proposal."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import random
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import yaml

ROOT = Path(__file__).resolve().parent.parent
BACKLOG = ROOT / "projects/dream-cycle/backlog"
KR_BASE_URL = "https://kind-robots.vercel.app"
PACIFIC = ZoneInfo("America/Los_Angeles")

# Network-free keys known to exist in the live catalog. The sidecar resolves slugs.
FALLBACK_FACETS = {
    "GENRE": [
        "artificial-intelligence|Artificial Intelligence",
        "horror-comedy|Horror Comedy",
        "bureaucratic-fantasy|Bureaucratic Fantasy",
        "archive-horror|Archive Horror",
        "absurdist-comedy|Absurdist Comedy",
        "cartoon-noir|Cartoon Noir",
        "biopunk|Biopunk",
        "anachronism-mystery|Anachronism Mystery",
        "academic-eldritch|Academic Eldritch",
        "carnival|Carnival",
    ],
    "ANIMAL": [
        "capybara|Capybara",
        "axolotl|Axolotl",
        "cassowary|Cassowary",
        "binturong|Binturong",
        "atlantic-puffin|Atlantic Puffin",
    ],
    "SPECIES": [
        "catfolk|Catfolk",
        "birdfolk|Birdfolk",
        "android|Android",
        "changeling|Changeling",
        "butterfly|Butterfly",
    ],
    "OCCUPATION": [
        "alien-biologist|Alien Biologist",
        "accountant|Accountant",
        "cactus-wrangler|Cactus Wrangler",
        "chaos-consultant|Chaos Consultant",
        "accidental-diplomat|Accidental Diplomat",
    ],
    "MATERIAL": [
        "aether-silk|Aether Silk",
        "astral-ore|Astral Ore",
        "bone-glass|Bone Glass",
        "ancient-marble|Ancient Marble",
        "arcane-silver|Arcane Silver",
    ],
    "PERSONALITY": [
        "bookworm|Bookworm",
        "cautious|Cautious",
        "charismatic|Charismatic",
        "analytical|Analytical",
        "personality-buoyant|Buoyant",
    ],
}
FIELDS = {
    "location": (
        "title",
        "known_for",
        "local_rule",
        "best_scene",
        "art_direction",
    ),
    "character": (
        "name",
        "role_drive",
        "carries",
        "complication",
        "look",
    ),
    "reward": (
        "name",
        "reward_type",
        "rarity",
        "grants",
        "best_used_when",
        "catch",
    ),
    "scenario": ("title", "setup"),
}


def _target_date(now: datetime | None = None) -> str:
    now = now or datetime.now(PACIFIC)
    if now.tzinfo is None:
        now = now.replace(tzinfo=PACIFIC)
    return now.astimezone(PACIFIC).date().isoformat()


def slugify(value: str) -> str:
    return (
        re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")
        or "daily-dream"
    )


def _clean(raw: dict[str, Any]) -> dict[str, Any]:
    out = {
        "title": str(
            raw.get("title")
            or raw.get("canonicalValue")
            or raw.get("slug")
            or ""
        ).strip(),
        "slug": str(raw.get("slug") or "").strip(),
        "taxonomy": str(raw.get("taxonomy") or "").upper(),
        "randomWeight": max(float(raw.get("randomWeight") or 1), 0.0001),
    }
    if isinstance(raw.get("id"), int):
        out["id"] = raw["id"]
    if raw.get("canonicalValue"):
        out["canonicalValue"] = str(raw["canonicalValue"])
    return out


def _fallback(taxonomy: str) -> list[dict[str, Any]]:
    return [
        _clean(
            {
                "slug": pair.split("|", 1)[0],
                "title": pair.split("|", 1)[1],
                "taxonomy": taxonomy,
            }
        )
        for pair in FALLBACK_FACETS[taxonomy]
    ]


def fetch_live_facets(
    taxonomy: str, timeout: int = 12
) -> list[dict[str, Any]] | None:
    found: list[dict[str, Any]] = []
    skip = 0
    take = 250
    while True:
        url = f"{KR_BASE_URL}/api/facets?" + urllib.parse.urlencode(
            {"taxonomy": taxonomy, "take": take, "skip": skip}
        )
        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "conductor-daily-dream/2",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = json.loads(response.read())
        except (OSError, ValueError, urllib.error.URLError):
            return None
        rows = payload.get("data") if isinstance(payload, dict) else None
        if not isinstance(rows, list):
            return None
        for row in rows:
            if (
                not isinstance(row, dict)
                or row.get("isActive") is False
                or row.get("isPublic") is False
            ):
                continue
            if (
                row.get("isRandomizable") is False
                or float(row.get("randomWeight") or 0) <= 0
            ):
                continue
            facet = _clean(row)
            if facet["title"] and facet["slug"]:
                found.append(facet)
        if len(rows) < take:
            break
        skip += take
    return list(
        {row["slug"].casefold(): row for row in found}.values()
    ) or None


def fetch_facet_catalog() -> tuple[dict[str, list[dict[str, Any]]], str]:
    catalog: dict[str, list[dict[str, Any]]] = {}
    live = True
    for taxonomy in FALLBACK_FACETS:
        rows = fetch_live_facets(taxonomy)
        if not rows:
            rows = _fallback(taxonomy)
            live = False
        catalog[taxonomy] = rows
    return catalog, "live" if live else "mixed-fallback"


def _draw(
    rng: random.Random,
    pool: list[dict[str, Any]],
    count: int = 1,
) -> list[dict[str, Any]]:
    if len(pool) < count:
        raise ValueError(f"Facet pool has {len(pool)} entries; {count} required")
    left = list(pool)
    chosen: list[dict[str, Any]] = []
    for _ in range(count):
        pick = copy.deepcopy(
            rng.choices(
                left,
                weights=[
                    max(float(entry.get("randomWeight") or 1), 0.0001)
                    for entry in left
                ],
                k=1,
            )[0]
        )
        chosen.append(pick)
        left = [
            entry
            for entry in left
            if entry["slug"].casefold() != pick["slug"].casefold()
        ]
    return chosen


def facet_seed_plan(
    day: str,
    catalog: dict[str, list[dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    source = "provided"
    if catalog is None:
        catalog, source = fetch_facet_catalog()
    seed = int.from_bytes(
        hashlib.sha256(f"daily-dream-v2:{day}".encode()).digest()[:8],
        "big",
    )
    rng = random.Random(seed)
    genres = _draw(rng, catalog["GENRE"], 7)
    creature = _draw(rng, catalog["ANIMAL"] + catalog["SPECIES"])[0]
    occupation = _draw(rng, catalog["OCCUPATION"])[0]
    material = _draw(rng, catalog["MATERIAL"])[0]
    personality = _draw(rng, catalog["PERSONALITY"])[0]
    umbrella = genres[:2]
    extras = dict(
        zip(
            (
                "location",
                "character",
                "reward_item",
                "reward_skill",
                "scenario",
            ),
            genres[2:],
        )
    )
    elements = {
        "vibe": [*umbrella, creature, occupation],
        "location": [*umbrella, extras["location"], creature, material],
        "character": [
            *umbrella,
            extras["character"],
            creature,
            occupation,
            personality,
        ],
        "reward_item": [*umbrella, extras["reward_item"], material],
        "reward_skill": [*umbrella, extras["reward_skill"], occupation],
        "scenario": [
            *umbrella,
            extras["scenario"],
            extras["location"],
            extras["character"],
            creature,
        ],
    }
    return {
        "version": 2,
        "date": day,
        "deterministic_seed": seed,
        "catalog_source": source,
        "umbrella": {
            "genres": umbrella,
            "creature": creature,
            "wildcard": occupation,
            "wildcard_role": "occupation",
        },
        "shared": {"material": material, "personality": personality},
        "extra_genres": extras,
        "elements": elements,
    }


def build_brief(
    day: str | None = None,
    catalog: dict[str, list[dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    day = day or _target_date()
    seeds = facet_seed_plan(day, catalog)
    return {
        "proposal_date": day,
        "seed_facets": seeds,
        "instructions": [
            "Create one coherent bundle under the vibe, not unrelated mini-pitches.",
            "Return exactly one location, one character, one ITEM, one SKILL, and one scenario; no narrator.",
            "Use the Facets as creative constraints and persist seed_facets unchanged.",
            "Author the scenario last and name the vibe, location, and character in its setup.",
        ],
        "required_counts": {
            "vibe": 1,
            "locations": 1,
            "characters": 1,
            "reward_item": 1,
            "reward_skill": 1,
            "scenarios": 1,
        },
    }


def normalize(
    proposal: dict[str, Any], avoid: set[str] | None = None
) -> dict[str, Any]:
    out = copy.deepcopy(proposal)
    out["title"] = str(
        out.get("title") or "Untitled Daily Dream"
    ).strip()
    base = slugify(out.get("slug") or out["title"])
    used = {entry.casefold() for entry in (avoid or set())}
    out["slug"] = base
    suffix = 2
    while out["slug"].casefold() in used:
        out["slug"] = f"{base}-{suffix}"
        suffix += 1

    rewards = out.get("rewards")
    if isinstance(rewards, list):
        for reward in rewards:
            if isinstance(reward, dict):
                reward["reward_type"] = str(
                    reward.get("reward_type") or ""
                ).strip().upper()

    out.pop("narrator", None)
    return out


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_proposal(proposal: Any) -> list[str]:
    if not isinstance(proposal, dict):
        return ["proposal must be an object"]
    problems: list[str] = []
    for field in ("title", "slug", "idea"):
        if not _text(proposal.get(field)):
            problems.append(f"missing {field}")

    vibe = proposal.get("vibe")
    if not isinstance(vibe, dict):
        problems.append("vibe must be an object")
    else:
        for field in ("title", "line", "art_direction"):
            if not _text(vibe.get(field)):
                problems.append(f"vibe missing {field}")

    for key, count, kind in (
        ("locations", 1, "location"),
        ("characters", 1, "character"),
        ("rewards", 2, "reward"),
        ("scenarios", 1, "scenario"),
    ):
        rows = proposal.get(key)
        if not isinstance(rows, list) or len(rows) != count:
            problems.append(f"{key} must be a list of exactly {count}")
            continue
        for index, row in enumerate(rows):
            if not isinstance(row, dict):
                problems.append(f"{key}[{index}] must be an object")
                continue
            for field in FIELDS[kind]:
                if not _text(row.get(field)):
                    problems.append(f"{key}[{index}] missing {field}")

    rewards = (
        proposal.get("rewards")
        if isinstance(proposal.get("rewards"), list)
        else []
    )
    reward_types = sorted(
        str(row.get("reward_type") or "").upper()
        for row in rewards
        if isinstance(row, dict)
    )
    if reward_types != ["ITEM", "SKILL"]:
        problems.append("rewards must contain exactly one ITEM and one SKILL")

    if proposal.get("narrator"):
        problems.append("narrator is not part of the six-asset daily bundle")

    seed_facets = proposal.get("seed_facets")
    elements = (
        seed_facets.get("elements")
        if isinstance(seed_facets, dict)
        else None
    )
    if not isinstance(seed_facets, dict):
        problems.append("seed_facets must be an object")
    elif (
        not isinstance(seed_facets.get("umbrella", {}).get("genres"), list)
        or len(seed_facets["umbrella"]["genres"]) != 2
    ):
        problems.append(
            "seed_facets.umbrella.genres must contain exactly 2 Facets"
        )
    if not isinstance(elements, dict):
        problems.append("seed_facets.elements must be an object")
    else:
        for key in (
            "vibe",
            "location",
            "character",
            "reward_item",
            "reward_skill",
            "scenario",
        ):
            if (
                not isinstance(elements.get(key), list)
                or not elements[key]
            ):
                problems.append(
                    f"seed_facets.elements.{key} must be a non-empty list"
                )
                continue
            for facet in elements[key]:
                if (
                    not isinstance(facet, dict)
                    or not _text(facet.get("title"))
                    or not _text(facet.get("taxonomy"))
                    or not (
                        _text(facet.get("slug"))
                        or isinstance(facet.get("id"), int)
                    )
                ):
                    problems.append(
                        f"seed_facets.elements.{key} contains an invalid Facet"
                    )

    if (
        all(
            isinstance(proposal.get(key), list) and proposal[key]
            for key in ("locations", "characters", "scenarios")
        )
        and isinstance(vibe, dict)
    ):
        setup = str(
            proposal["scenarios"][0].get("setup") or ""
        ).casefold()
        for label, name in (
            ("vibe", vibe.get("title")),
            ("location", proposal["locations"][0].get("title")),
            ("character", proposal["characters"][0].get("name")),
        ):
            if _text(name) and str(name).casefold() not in setup:
                problems.append(
                    f"scenario setup must name the {label}: {name}"
                )
    return problems


def _frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    end = text.find("\n---\n", 4)
    if not text.startswith("---\n") or end < 0:
        return {}
    value = yaml.safe_load(text[4:end])
    return value if isinstance(value, dict) else {}


def _files() -> list[Path]:
    return sorted(BACKLOG.glob("*.md")) if BACKLOG.exists() else []


def proposal_exists_for(day: str) -> bool:
    return any(
        str(_frontmatter(path).get("proposal_date") or "") == day
        for path in _files()
    )


def existing_slugs() -> set[str]:
    return {
        str(_frontmatter(path).get("slug"))
        for path in _files()
        if _frontmatter(path).get("slug")
    }


def fetch_main(quiet: bool = True) -> bool:
    try:
        return (
            subprocess.run(
                ["git", "fetch", "origin", "main"],
                cwd=ROOT,
                check=False,
                capture_output=quiet,
                text=True,
            ).returncode
            == 0
        )
    except OSError:
        return False


def remote_proposal_for(day: str) -> str | None:
    try:
        names = subprocess.run(
            [
                "git",
                "ls-tree",
                "-r",
                "--name-only",
                "origin/main",
                "--",
                "projects/dream-cycle/backlog",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        ).stdout
        for name in names.splitlines():
            shown = subprocess.run(
                ["git", "show", f"origin/main:{name}"],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            if shown.returncode == 0 and re.search(
                rf"(?m)^proposal_date:\s*['\"]?{re.escape(day)}['\"]?\s*$",
                shown.stdout,
            ):
                return Path(name).name
    except OSError:
        pass
    return None


def _titles(values: list[dict[str, Any]]) -> str:
    return " · ".join(
        str(value.get("title") or value.get("slug")) for value in values
    )


def render_markdown(proposal: dict[str, Any], day: str) -> str:
    seed_facets = proposal["seed_facets"]
    elements = seed_facets["elements"]
    location = proposal["locations"][0]
    character = proposal["characters"][0]
    scenario = proposal["scenarios"][0]
    item = next(
        reward
        for reward in proposal["rewards"]
        if reward["reward_type"] == "ITEM"
    )
    skill = next(
        reward
        for reward in proposal["rewards"]
        if reward["reward_type"] == "SKILL"
    )
    lines = [
        "---",
        f"slug: {proposal['slug']}",
        f"title: {proposal['title']}",
        "type: dream",
        "status: outline",
        "priority: normal",
        "narrator: 'no'",
        f"created: '{day}'",
        "proposal: true",
        f"proposal_date: '{day}'",
        "built_pr: null",
        "---",
        "",
        "## Seed Facets",
        (
            f"- **Deterministic seed:** "
            f"`{seed_facets.get('deterministic_seed')}` "
            f"({seed_facets.get('catalog_source', 'unknown')} catalog)"
        ),
        *[
            f"- **{label}:** {_titles(elements[key])}"
            for label, key in (
                ("Dream vibe", "vibe"),
                ("Dream location", "location"),
                ("Character", "character"),
                ("Reward item", "reward_item"),
                ("Reward skill", "reward_skill"),
                ("Scenario", "scenario"),
            )
        ],
        "",
        "## The idea",
        proposal["idea"],
        "",
        "## Dream vibe (1)",
        f"**{proposal['vibe']['title']}** — {proposal['vibe']['line']}",
        f"Art: {proposal['vibe']['art_direction']}",
        "",
        "## Dream location (1)",
        (
            f"- **{location['title']}** — known for "
            f"{location['known_for']}. Local rule: {location['local_rule']}. "
            f"Best scene: {location['best_scene']}. "
            f"Art: {location['art_direction']}"
        ),
        "",
        "## Character (1)",
        (
            f"- **{character['name']}** — {character['role_drive']}. "
            f"Carries {character['carries']}. "
            f"Complication: {character['complication']}. "
            f"Look: {character['look']}"
        ),
        "",
        "## Reward item (1)",
        (
            f"- **{item['name']}** (ITEM, {item['rarity']}) — "
            f"{item['grants']}. Best used when {item['best_used_when']}. "
            f"The catch: {item['catch']}"
        ),
        "",
        "## Reward skill (1)",
        (
            f"- **{skill['name']}** (SKILL, {skill['rarity']}) — "
            f"{skill['grants']}. Best used when {skill['best_used_when']}. "
            f"The catch: {skill['catch']}"
        ),
        "",
        "## Scenario (1, authored last)",
        f"- **{scenario['title']}** — {scenario['setup']}",
        "",
        "## Notes from Silas",
        (
            "- (leave notes here — agents fold them in before building "
            "and never edit this section)"
        ),
        "",
        "## Build log",
        (
            f"- {day} | proposed | deterministic Facet-seeded "
            "six-asset bundle"
        ),
        "",
        "<!-- proposal-data",
        json.dumps(proposal, ensure_ascii=False, sort_keys=True),
        "-->",
        "",
    ]
    return "\n".join(lines)


def write_proposal(
    proposal: dict[str, Any],
    *,
    date: str | None = None,
    fetch: bool = True,
    dry_run: bool = False,
    force: bool = False,
) -> Path | None:
    day = date or _target_date()
    if not force and (
        proposal_exists_for(day)
        or (fetch and fetch_main() and remote_proposal_for(day))
    ):
        print(
            f"Proposal already exists for {day}; refusing duplicate.",
            file=sys.stderr,
        )
        return None

    normalized = normalize(proposal, existing_slugs())
    problems = validate_proposal(normalized)
    if problems:
        raise ValueError("Invalid proposal:\n- " + "\n- ".join(problems))

    path = BACKLOG / f"{day}-{normalized['slug']}.md"
    rendered = render_markdown(normalized, day)
    if dry_run:
        print(rendered)
        print(f"# would write: {path}", file=sys.stderr)
        return path

    BACKLOG.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered, encoding="utf-8")
    print(path)
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 0 if the date already has a proposal, otherwise 1",
    )
    parser.add_argument(
        "--brief",
        action="store_true",
        help="print the six-asset authoring brief and deterministic Facet seed",
    )
    parser.add_argument(
        "--from-json",
        metavar="FILE",
        help="validate and write an authored proposal JSON ('-' for stdin)",
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="render or write the built-in six-asset sample",
    )
    parser.add_argument("--date", help="override Pacific date (YYYY-MM-DD)")
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="with --check, consult a freshly fetched origin/main",
    )
    parser.add_argument(
        "--no-fetch",
        action="store_true",
        help="with --from-json, skip the origin/main race check",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print markdown without writing a backlog file",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="write even when the date already has a proposal",
    )
    args = parser.parse_args(argv)
    day = args.date or _target_date()

    if args.check:
        exists = proposal_exists_for(day)
        if not exists and args.fetch and fetch_main():
            exists = remote_proposal_for(day) is not None
        if exists:
            print(f"Proposal for {day} exists.")
            return 0
        print(
            f"No proposal for {day}. Run --brief, author the six-asset JSON, "
            "then pass it to --from-json."
        )
        return 1

    if args.brief:
        print(json.dumps(build_brief(day), indent=2, ensure_ascii=False))
        return 0

    if args.sample:
        written = write_proposal(
            copy.deepcopy(SAMPLE_PROPOSAL),
            date=day,
            fetch=False,
            dry_run=args.dry_run,
            force=True,
        )
        return 0 if written else 1

    if args.from_json:
        try:
            raw = (
                sys.stdin.read()
                if args.from_json == "-"
                else Path(args.from_json).read_text(encoding="utf-8")
            )
            proposal = json.loads(raw)
        except (OSError, json.JSONDecodeError) as error:
            print(f"Could not read proposal JSON: {error}", file=sys.stderr)
            return 1
        proposal.setdefault("seed_facets", facet_seed_plan(day))
        written = write_proposal(
            proposal,
            date=day,
            fetch=not args.no_fetch,
            dry_run=args.dry_run,
            force=args.force,
        )
        return 0 if written else 1

    parser.error("choose --check, --brief, --from-json, or --sample")
    return 2


def _sample() -> dict[str, Any]:
    catalog = {
        taxonomy: _fallback(taxonomy) for taxonomy in FALLBACK_FACETS
    }
    return {
        "title": "Prism Appeal",
        "slug": "prism-appeal",
        "idea": "A courthouse refracts testimony into living color.",
        "vibe": {
            "title": "The Kindly Cross-Examination",
            "line": "Every answer changes the room that asked it.",
            "art_direction": "A luminous impossible courthouse.",
        },
        "locations": [
            {
                "title": "The Refracted Court",
                "known_for": "colored testimony",
                "local_rule": "no statement repeats a hue",
                "best_scene": "a disputed memory changes the room",
                "art_direction": "prismatic courtroom",
            }
        ],
        "characters": [
            {
                "name": "Mara Venn",
                "role_drive": "protect an engineered witness",
                "carries": "a cracked spectrum lens",
                "complication": "it contains her deleted testimony",
                "look": "mantis-shrimp advocate in a midnight suit",
            }
        ],
        "rewards": [
            {
                "name": "Verdict Lens",
                "reward_type": "ITEM",
                "rarity": "RARE",
                "grants": "reveals omissions",
                "best_used_when": "a story is too neat",
                "catch": "it reveals yours",
            },
            {
                "name": "Chromatic Recall",
                "reward_type": "SKILL",
                "rarity": "UNCOMMON",
                "grants": "reconstructs memory from color",
                "best_used_when": "records were altered",
                "catch": "emotion returns",
            },
        ],
        "scenarios": [
            {
                "title": "The Color of Perjury",
                "setup": (
                    "In The Kindly Cross-Examination at The Refracted Court, "
                    "Mara Venn defends a witness whose testimony turned the "
                    "chamber black."
                ),
            }
        ],
        "seed_facets": facet_seed_plan("2026-07-31", catalog),
    }


SAMPLE_PROPOSAL = _sample()


if __name__ == "__main__":
    raise SystemExit(main())