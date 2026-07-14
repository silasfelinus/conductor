#!/usr/bin/env python3
"""
build_dream_proposal.py — generate tomorrow's "starter dream" proposal.

Each morning the digest surfaces a proposal for the next day's auto-created
output: a self-consistent slice of a world with a tight, standardized cast —

  * 3 characters
  * 2 locations (sharing one vibe/genre)
  * 1 narrator bot
  * 2 rewards — one skill-related (rewardType: SKILL), one item-related (ITEM)
  * 1-2 scenarios

The proposal is written as a dream-cycle backlog outline
(projects/dream-cycle/backlog/<date>-<slug>.md, using _template-proposal.md's
shape) so the existing creation loop can pick it up and build it, and so Silas
can steer it by editing the file's `## Notes from Silas` section — the
comment/edit link the digest points at.

THE AUTHOR IS THE SWEEPING LLM AGENT ITSELF (Silas, 2026-07-14): no API keys,
no scripted model calls anywhere in this path. This script is only the
validator/renderer/writer the agent hands its proposal to. The sweep duty:

  1. python scripts/build_dream_proposal.py --check      # exit 1 = missing
  2. python scripts/build_dream_proposal.py --brief      # the authoring spec
  3. (the agent invents the starter dream and emits the JSON itself)
  4. python scripts/build_dream_proposal.py --from-json proposal.json

The write is guarded (no-op if the date already has a proposal), the JSON is
validated (exact counts, one SKILL + one ITEM reward), and the slug is
de-duplicated against the backlog + SHIPPED ledger. `--sample` writes a
built-in example so the render/digest path stays verifiable in tests.

Usage:
  python scripts/build_dream_proposal.py --check              # is today's written?
  python scripts/build_dream_proposal.py --brief              # print the authoring brief
  python scripts/build_dream_proposal.py --from-json p.json   # validate + write (or - for stdin)
  python scripts/build_dream_proposal.py --from-json - --dry-run   # preview markdown
  python scripts/build_dream_proposal.py --sample --dry-run   # built-in sample
"""

from __future__ import annotations

import argparse
import datetime
import glob
import json
import re
import sys
from pathlib import Path
from typing import Any, Optional

import yaml

try:
    from zoneinfo import ZoneInfo
    _TZ = ZoneInfo("America/Los_Angeles")
except ImportError:  # pragma: no cover - Python < 3.9 fallback
    _TZ = datetime.timezone(datetime.timedelta(hours=-7))

ROOT = Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "projects" / "dream-cycle" / "backlog"
SHIPPED = ROOT / "projects" / "dream-cycle" / "SHIPPED.md"

REPO = "silasfelinus/conductor"
DEFAULT_BRANCH = "main"

BRIEF = """\
You are Conductor's dream author, inventing today's "starter dream" for the
Kind Robots site — a warm, imaginative AI art + roleplay platform. Invent ONE
self-consistent world: two connected places, a shared mood, a small cast, a
host, and two fitting rewards. Aim for cozy wonder with an edge — specific,
tactile, a little strange, never generic fantasy filler.

Produce exactly (as a JSON object, then pass it to --from-json):
- title + slug (kebab-case, 2-4 words, unique — must not reuse a slug listed below)
- idea: 2-4 sentences on what this world is and why someone wants to spend time here
- vibe: {title, line} — a GENRE dream that both locations share
- locations: EXACTLY 2 places in this one world, each with title / known_for /
  local_rule / best_scene / art_direction (a concrete visual brief a
  text-to-image model can render)
- characters: EXACTLY 3 who inhabit it, each with name / role_drive / carries /
  complication / look
- rewards: EXACTLY 2 that fit the world — one reward_type SKILL (an
  ability/technique) and one reward_type ITEM (a tangible object). Each with
  name / rarity (COMMON|UNCOMMON|RARE|EPIC|LEGENDARY) / grants /
  best_used_when / catch.
- scenarios: 1-2 of {title, setup} wiring the locations, vibe, and cast together
- narrator: ONE bot who hosts this dream — name / voice / personality /
  appears_as / best_for / expressions (NEUTRAL + a few emotions) /
  topics (2-3 strings)

Every element must belong to the SAME world and reinforce the vibe."""


# Required shape for an agent-authored proposal (see BRIEF / SAMPLE_PROPOSAL).
REQUIRED_COUNTS = {"locations": 2, "characters": 3, "rewards": 2}
REQUIRED_FIELDS = {
    "locations": ["title", "known_for", "local_rule", "best_scene", "art_direction"],
    "characters": ["name", "role_drive", "carries", "complication", "look"],
    "rewards": ["name", "reward_type", "rarity", "grants", "best_used_when", "catch"],
    "scenarios": ["title", "setup"],
}


def validate_proposal(p: Any) -> list[str]:
    """Light structural validation of an agent-authored proposal. Returns problems."""
    problems: list[str] = []
    if not isinstance(p, dict):
        return ["proposal must be a JSON object"]
    for key in ("title", "idea"):
        if not str(p.get(key, "")).strip():
            problems.append(f"missing {key}")
    vibe = p.get("vibe")
    if not (isinstance(vibe, dict) and str(vibe.get("title", "")).strip()
            and str(vibe.get("line", "")).strip()):
        problems.append("vibe must be an object with title + line")
    for key, count in REQUIRED_COUNTS.items():
        items = p.get(key)
        if not (isinstance(items, list) and len(items) == count):
            problems.append(f"{key} must be a list of exactly {count}")
            continue
        for i, item in enumerate(items):
            for field in REQUIRED_FIELDS[key]:
                if not (isinstance(item, dict) and str(item.get(field, "")).strip()):
                    problems.append(f"{key}[{i}] missing {field}")
    scenarios = p.get("scenarios")
    if not (isinstance(scenarios, list) and 1 <= len(scenarios) <= 2):
        problems.append("scenarios must be a list of 1-2")
    else:
        for i, sc in enumerate(scenarios):
            for field in REQUIRED_FIELDS["scenarios"]:
                if not (isinstance(sc, dict) and str(sc.get(field, "")).strip()):
                    problems.append(f"scenarios[{i}] missing {field}")
    nar = p.get("narrator")
    if not isinstance(nar, dict):
        problems.append("narrator must be an object")
    else:
        for field in ("name", "voice", "personality", "appears_as", "best_for", "expressions"):
            if not str(nar.get(field, "")).strip():
                problems.append(f"narrator missing {field}")
        if not (isinstance(nar.get("topics"), list) and nar["topics"]):
            problems.append("narrator.topics must be a non-empty list")
    types = sorted(str(r.get("reward_type", "")).upper()
                   for r in (p.get("rewards") or []) if isinstance(r, dict))
    if types and types != ["ITEM", "SKILL"]:
        # normalize() can repair two-of-a-kind, but flag anything else odd
        if set(types) - {"SKILL", "ITEM"}:
            problems.append("reward_type values must be SKILL or ITEM")
    return problems

SAMPLE_PROPOSAL: dict[str, Any] = {
    "title": "The Kelpwick Lantern Post",
    "slug": "kelpwick-lantern-post",
    "idea": (
        "A drowned mail-village on stilts where letters are delivered by trained "
        "cuttlefish and the lamplight never quite goes out. People come to send a "
        "message they could never say aloud — and to see which ones the tide "
        "answers. Cozy, salt-damp, a little haunted."
    ),
    "vibe": {
        "title": "Tidewrit Melancholy",
        "line": "Gentle longing and lamplit patience; low stakes, deep feeling, everything a little waterlogged.",
    },
    "locations": [
        {
            "title": "The Lantern Post",
            "known_for": "the last dry post office, its counter worn smooth by a century of trembling hands.",
            "local_rule": "You may only send a letter you're afraid to send.",
            "best_scene": "midnight sorting, when the undelivered mail glows faintly on the racks.",
            "art_direction": "warm amber lantern glow on wet weathered wood, brass sorting slots, rain on glass, dusk teal shadows, cozy and melancholy.",
        },
        {
            "title": "The Cuttle Roost",
            "known_for": "the rookery where courier cuttlefish are raised and read their routes in ink.",
            "local_rule": "Never rush a courier — a hurried letter arrives wrong.",
            "best_scene": "dawn launch, a hundred cuttlefish unspooling into the grey water at once.",
            "art_direction": "bioluminescent teal-and-violet cuttlefish in a wooden roost over dark water, soft dawn fog, ink-stained ropes, tender and strange.",
        },
    ],
    "characters": [
        {
            "name": "Postmistress Wren Ollow",
            "role_drive": "keeper of the Lantern Post; wants every honest letter delivered before she retires.",
            "carries": "a ring of keys that no longer fit any door.",
            "complication": "she has one undelivered letter of her own she cannot bring herself to send.",
            "look": "elderly, oilcloth coat, lantern-scarred hands, a gull feather behind one ear.",
        },
        {
            "name": "Semi the Courier",
            "role_drive": "a young cuttlefish-tender who dreams of riding the tide out past the map.",
            "carries": "a waterproof satchel of letters he's memorized but never read.",
            "complication": "he can hear what the cuttlefish feel, and it's making him seasick with everyone's secrets.",
            "look": "teenager, ink-stained sleeves, rubber waders, a cuttlefish curled on his shoulder.",
        },
        {
            "name": "The Return-to-Sender",
            "role_drive": "a hooded figure who collects letters the tide refuses to deliver.",
            "carries": "an umbrella that has never once been opened.",
            "complication": "no one is sure if they're a person, a rumor, or the sea being polite.",
            "look": "tall, dripping oilskin, face in shadow, barnacles where buttons should be.",
        },
    ],
    "rewards": [
        {
            "name": "Tidewrit Fluency",
            "reward_type": "SKILL",
            "rarity": "RARE",
            "grants": "the ability to read a letter's true feeling regardless of its words.",
            "best_used_when": "someone is lying kindly to protect you.",
            "catch": "you can no longer un-know what a smile is hiding.",
        },
        {
            "name": "The Never-Opened Umbrella",
            "reward_type": "ITEM",
            "rarity": "LEGENDARY",
            "grants": "shelter from any one storm, of weather or of the heart.",
            "best_used_when": "the moment you'd rather not face has finally arrived.",
            "catch": "it works exactly once, and only if you've never peeked inside.",
        },
    ],
    "scenarios": [
        {
            "title": "The Letter She Kept",
            "setup": "Wren finally asks the player to deliver her own undelivered letter — but the address is a place that sank years ago, and only the Return-to-Sender knows the way.",
        },
        {
            "title": "The Seasick Courier",
            "setup": "Semi is drowning in the cuttlefishes' borrowed secrets; the player must help him sort what's his to carry from what isn't, before the dawn launch.",
        },
    ],
    "narrator": {
        "name": "Postmistress Wren Ollow",
        "voice": "unhurried, fond, speaks in tide-and-postage metaphors.",
        "personality": "patient, wry, quietly heartbroken and endlessly kind.",
        "appears_as": "a lantern-lit portrait at the sorting counter.",
        "best_for": "letter-writing prompts, gentle confessions, slow mysteries.",
        "expressions": "NEUTRAL plus LOVING, THINKING, WISTFUL, SURPRISED, and a WHISPERING action for undelivered secrets.",
        "topics": ["Letters of the Post (lore)", "The Tide's Answers (mystery)", "Ask Wren (advice)"],
    },
}


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return re.sub(r"-{2,}", "-", s) or "starter-dream"


def existing_slugs() -> set[str]:
    """Slugs already used by backlog outlines and shipped creations — avoid dupes."""
    slugs: set[str] = set()
    for path in glob.glob(str(BACKLOG / "*.md")):
        name = Path(path).name
        if name.startswith("_") or name == "README.md":
            continue
        try:
            text = Path(path).read_text(encoding="utf-8")
        except OSError:
            continue
        m = re.search(r"^slug:\s*(.+)$", text, re.MULTILINE)
        if m:
            slugs.add(m.group(1).strip())
        # also treat the dated filename tail as a used slug
        slugs.add(re.sub(r"^\d{4}-\d{2}-\d{2}-", "", Path(path).stem))
    if SHIPPED.exists():
        for m in re.finditer(r"\b([a-z0-9]+(?:-[a-z0-9]+)+)\b", SHIPPED.read_text(encoding="utf-8")):
            slugs.add(m.group(1))
    return slugs


def normalize(p: dict[str, Any], avoid: set[str]) -> dict[str, Any]:
    """Enforce the tight contract the LLM may fudge: one SKILL + one ITEM, unique slug."""
    p.setdefault("slug", slugify(p.get("title", "starter-dream")))
    p["slug"] = slugify(p["slug"])
    base = p["slug"]
    n = 2
    while p["slug"] in avoid:
        p["slug"] = f"{base}-{n}"
        n += 1
    rewards = p.get("rewards", [])[:2]
    types = [str(r.get("reward_type", "")).upper() for r in rewards]
    # Guarantee one of each type when the model returns two of a kind.
    if len(rewards) == 2 and types[0] == types[1]:
        rewards[1]["reward_type"] = "ITEM" if types[0] == "SKILL" else "SKILL"
    p["rewards"] = rewards
    return p


def _line(*parts: str) -> str:
    return " ".join(part for part in parts if part).strip()


def render_markdown(p: dict[str, Any], proposal_date: str) -> str:
    fm = {
        "slug": p["slug"],
        "title": p["title"],
        "type": "dream",
        "status": "outline",
        "priority": "normal",
        "narrator": "yes",
        "created": proposal_date,
        "proposal": True,
        "proposal_date": proposal_date,
        "built_pr": None,
    }
    front = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip()

    loc_lines = "\n".join(
        f"- **{l['title']}** — known for {l['known_for']} "
        f"Local rule: {l['local_rule']} Best scene: {l['best_scene']} "
        f"Art: {l['art_direction']}"
        for l in p["locations"]
    )
    char_lines = "\n".join(
        f"- **{c['name']}** — {c['role_drive']} Carries {c['carries']} "
        f"Complication: {c['complication']} Look: {c['look']}"
        for c in p["characters"]
    )
    reward_lines = "\n".join(
        f"- **{r['name']}** ({r['reward_type']}, {r['rarity']}) — {r['grants']} "
        f"Best used when {r['best_used_when']} The catch: {r['catch']}"
        for r in p["rewards"]
    )
    scenario_lines = "\n".join(
        f"- **{s['title']}** — {s['setup']}" for s in p["scenarios"]
    )
    nar = p["narrator"]
    nar_topics = "; ".join(nar.get("topics", []))
    nar_block = _line(
        f"**{nar['name']}** as narrator bot:", nar["voice"],
        f"Personality: {nar['personality']}", f"Appears as: {nar['appears_as']}",
        f"Best for: {nar['best_for']}", f"Expressions: {nar['expressions']}",
        f"Topics/threads: {nar_topics}.",
    )

    return f"""---
{front}
---

## The idea
{p['idea']}

## Vibe / genre dream
**{p['vibe']['title']}** — GENRE. {p['vibe']['line']}

## Locations (2)
{loc_lines}

## Characters (3)
{char_lines}

## Rewards (2 — one skill, one item)
{reward_lines}

## Scenarios (1-2)
{scenario_lines}

## Narrator
{nar_block}

## Notes from Silas
- (leave notes here — agents fold them in before building and never edit this section)

## Build log
- {proposal_date} | proposed | auto-generated daily proposal

<!-- proposal-data
{json.dumps(p, ensure_ascii=False)}
-->
"""


def edit_link(filename: str) -> str:
    return (
        f"https://github.com/{REPO}/blob/{DEFAULT_BRANCH}/"
        f"projects/dream-cycle/backlog/{filename}#notes-from-silas"
    )


def _target_date(date: Optional[str] = None) -> str:
    return date or datetime.datetime.now(_TZ).date().isoformat()


def proposal_exists_for(date: str) -> bool:
    """True if a daily proposal for `date` is already in the backlog (skip regen)."""
    for path in glob.glob(str(BACKLOG / "*.md")):
        name = Path(path).name
        if name.startswith("_") or name == "README.md":
            continue
        try:
            text = Path(path).read_text(encoding="utf-8")
        except OSError:
            continue
        m = re.search(r"^proposal_date:\s*(.+)$", text, re.MULTILINE)
        if m and m.group(1).strip().strip("'\"") == date:
            return True
    return False


def _write(proposal: dict[str, Any], date: str, dry_run: bool) -> Optional[Path]:
    markdown = render_markdown(proposal, date)
    filename = f"{date}-{proposal['slug']}.md"
    if dry_run:
        print(markdown)
        print(f"\n# would write: projects/dream-cycle/backlog/{filename}", file=sys.stderr)
        print(f"# edit link: {edit_link(filename)}", file=sys.stderr)
        return BACKLOG / filename  # the would-be path (nothing written)
    dest = BACKLOG / filename
    dest.write_text(markdown, encoding="utf-8")
    print(f"Wrote {dest.relative_to(ROOT)}")
    print(f"Edit link: {edit_link(filename)}")
    return dest


def print_brief() -> None:
    """Print the authoring brief for the sweeping agent (spec + slugs to avoid)."""
    avoid = ", ".join(sorted(existing_slugs())) or "(none yet)"
    print(BRIEF)
    print(f"\nSlugs already used (do NOT reuse or closely echo): {avoid}")
    print("\nWhen your JSON is ready:  python scripts/build_dream_proposal.py --from-json <file|->")


def write_proposal(proposal: dict[str, Any], date: Optional[str] = None,
                   dry_run: bool = False, force: bool = False) -> Optional[Path]:
    """Validate + normalize an agent-authored proposal and write today's file.

    Guarded: no-op (with a message) if `date` already has a proposal, unless
    force. Returns the written path, or None."""
    date = _target_date(date)
    problems = validate_proposal(proposal)
    if problems:
        print("Proposal JSON is invalid:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return None
    if proposal_exists_for(date) and not force:
        print(f"Proposal for {date} already exists — not writing (use --force to override).",
              file=sys.stderr)
        return None
    proposal = normalize(json.loads(json.dumps(proposal)), existing_slugs())
    return _write(proposal, date, dry_run)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="exit 0 if today's proposal exists, 1 if the agent should author one")
    ap.add_argument("--brief", action="store_true",
                    help="print the authoring brief (spec + slugs to avoid) for the agent")
    ap.add_argument("--from-json", default=None, metavar="FILE",
                    help="agent-authored proposal JSON to validate + write ('-' for stdin)")
    ap.add_argument("--force", action="store_true",
                    help="write even if the date already has a proposal")
    ap.add_argument("--dry-run", action="store_true", help="print markdown, don't write the file")
    ap.add_argument("--sample", action="store_true",
                    help="write the built-in sample proposal (testing; bypasses the guard)")
    ap.add_argument("--date", default=None, help="override proposal date (YYYY-MM-DD, Pacific)")
    args = ap.parse_args()

    date = _target_date(args.date)

    if args.check:
        if proposal_exists_for(date):
            print(f"Proposal for {date} exists.")
            return 0
        print(f"No proposal for {date} — author one: run --brief for the spec, "
              f"then --from-json to write it.")
        return 1

    if args.brief:
        print_brief()
        return 0

    if args.sample:
        # Testing/demo path: always render the built-in sample, guard bypassed.
        proposal = normalize(json.loads(json.dumps(SAMPLE_PROPOSAL)), existing_slugs())
        _write(proposal, date, args.dry_run)
        return 0

    if args.from_json:
        try:
            raw = sys.stdin.read() if args.from_json == "-" else Path(args.from_json).read_text(encoding="utf-8")
            proposal = json.loads(raw)
        except (OSError, json.JSONDecodeError) as error:
            print(f"Could not read proposal JSON: {error}", file=sys.stderr)
            return 1
        written = write_proposal(proposal, date=date, dry_run=args.dry_run,
                                 force=args.force)
        return 0 if written else 1

    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
