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

Follows the house LLM pattern (scripts/curate_art.py, build_conductor_summary.py):
raw urllib to the Anthropic Messages API, ANTHROPIC_API_KEY from the environment,
schema-constrained JSON output. With no key (or --sample) it renders a built-in
sample proposal instead of calling the API, so the digest/rendering path stays
verifiable and the morning workflow soft-no-ops rather than erroring.

Env:
  ANTHROPIC_API_KEY    required for real generation; without it, --sample only
  DREAM_PROPOSAL_MODEL model id (default claude-opus-4-8)

Usage:
  python scripts/build_dream_proposal.py                 # generate + write today's file
  python scripts/build_dream_proposal.py --dry-run       # print markdown, don't write
  python scripts/build_dream_proposal.py --sample --dry-run   # built-in sample, no API
  python scripts/build_dream_proposal.py --theme "coastal noir"  # optional steer
"""

from __future__ import annotations

import argparse
import datetime
import glob
import json
import os
import re
import sys
import urllib.error
import urllib.request
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

MODEL = os.environ.get("DREAM_PROPOSAL_MODEL", "claude-opus-4-8").strip()
API_URL = "https://api.anthropic.com/v1/messages"
REPO = "silasfelinus/conductor"
DEFAULT_BRANCH = "main"
RARITIES = ["COMMON", "UNCOMMON", "RARE", "EPIC", "LEGENDARY"]

PROPOSAL_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "slug": {"type": "string"},
        "idea": {"type": "string"},
        "vibe": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "line": {"type": "string"},
            },
            "required": ["title", "line"],
            "additionalProperties": False,
        },
        "locations": {
            "type": "array",
            "minItems": 2,
            "maxItems": 2,
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "known_for": {"type": "string"},
                    "local_rule": {"type": "string"},
                    "best_scene": {"type": "string"},
                    "art_direction": {"type": "string"},
                },
                "required": ["title", "known_for", "local_rule", "best_scene", "art_direction"],
                "additionalProperties": False,
            },
        },
        "characters": {
            "type": "array",
            "minItems": 3,
            "maxItems": 3,
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "role_drive": {"type": "string"},
                    "carries": {"type": "string"},
                    "complication": {"type": "string"},
                    "look": {"type": "string"},
                },
                "required": ["name", "role_drive", "carries", "complication", "look"],
                "additionalProperties": False,
            },
        },
        "rewards": {
            "type": "array",
            "minItems": 2,
            "maxItems": 2,
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "reward_type": {"type": "string", "enum": ["SKILL", "ITEM"]},
                    "rarity": {"type": "string", "enum": RARITIES},
                    "grants": {"type": "string"},
                    "best_used_when": {"type": "string"},
                    "catch": {"type": "string"},
                },
                "required": ["name", "reward_type", "rarity", "grants", "best_used_when", "catch"],
                "additionalProperties": False,
            },
        },
        "scenarios": {
            "type": "array",
            "minItems": 1,
            "maxItems": 2,
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "setup": {"type": "string"},
                },
                "required": ["title", "setup"],
                "additionalProperties": False,
            },
        },
        "narrator": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "voice": {"type": "string"},
                "personality": {"type": "string"},
                "appears_as": {"type": "string"},
                "best_for": {"type": "string"},
                "expressions": {"type": "string"},
                "topics": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["name", "voice", "personality", "appears_as", "best_for", "expressions", "topics"],
            "additionalProperties": False,
        },
    },
    "required": ["title", "slug", "idea", "vibe", "locations", "characters", "rewards", "scenarios", "narrator"],
    "additionalProperties": False,
}

RUBRIC = """\
You are Conductor's dream author, inventing tomorrow's "starter dream" for the
Kind Robots site — a warm, imaginative AI art + roleplay platform. Invent ONE
self-consistent world: two connected places, a shared mood, a small cast, a
host, and two fitting rewards. Aim for cozy wonder with an edge — specific,
tactile, a little strange, never generic fantasy filler.

Produce exactly:
- title + slug (kebab-case, 2-4 words, unique — must not reuse an existing one listed below)
- idea: 2-4 sentences on what this world is and why someone wants to spend time here
- vibe: a GENRE dream (title + one line) that both locations share
- locations: EXACTLY 2 places in this one world, each with known_for / local_rule /
  best_scene / art_direction (a concrete visual brief a text-to-image model can render)
- characters: EXACTLY 3 who inhabit it, each with role_drive / carries / complication / look
- rewards: EXACTLY 2 that fit the world — one reward_type SKILL (an ability/technique)
  and one reward_type ITEM (a tangible object). Give each a rarity and a real catch.
- scenarios: 1-2 setups wiring the locations, vibe, and cast together
- narrator: ONE bot who hosts this dream — name, voice, personality, appears_as, best_for,
  an expression note (NEUTRAL + a few emotions), and 2-3 topic ideas

Every element must belong to the SAME world and reinforce the vibe. Return ONLY
the JSON object matching the schema."""

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


def call_llm(api_key: str, theme: str, avoid: set[str]) -> dict[str, Any]:
    avoid_line = ", ".join(sorted(avoid)) or "(none yet)"
    steer = f"\n\nOptional steer for today's world: {theme}." if theme else ""
    prompt = (
        f"{RUBRIC}{steer}\n\nSlugs already used (do NOT reuse or closely echo): {avoid_line}"
    )
    body = json.dumps({
        "model": MODEL,
        "max_tokens": 4096,
        "thinking": {"type": "adaptive"},
        "output_config": {
            "effort": "medium",
            "format": {"type": "json_schema", "schema": PROPOSAL_SCHEMA},
        },
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
    }).encode()
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        payload = json.loads(resp.read())
    text = next((b.get("text", "") for b in payload.get("content", [])
                 if b.get("type") == "text"), "")
    return json.loads(text)


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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="print markdown, don't write the file")
    ap.add_argument("--sample", action="store_true", help="use the built-in sample proposal (no API call)")
    ap.add_argument("--theme", default="", help="optional one-line steer for today's world")
    ap.add_argument("--date", default=None, help="override proposal date (YYYY-MM-DD, Pacific)")
    args = ap.parse_args()

    proposal_date = args.date or datetime.datetime.now(_TZ).date().isoformat()
    avoid = existing_slugs()
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()

    if args.sample or not api_key:
        if not args.sample:
            print("ANTHROPIC_API_KEY not set — using the built-in sample proposal.", file=sys.stderr)
        proposal = normalize(json.loads(json.dumps(SAMPLE_PROPOSAL)), avoid)
    else:
        try:
            proposal = normalize(call_llm(api_key, args.theme, avoid), avoid)
        except Exception as error:  # noqa: BLE001 - soft-fail so the morning run survives
            print(f"Proposal generation failed: {error}", file=sys.stderr)
            return 0

    markdown = render_markdown(proposal, proposal_date)
    filename = f"{proposal_date}-{proposal['slug']}.md"

    if args.dry_run:
        print(markdown)
        print(f"\n# would write: projects/dream-cycle/backlog/{filename}", file=sys.stderr)
        print(f"# edit link: {edit_link(filename)}", file=sys.stderr)
        return 0

    dest = BACKLOG / filename
    dest.write_text(markdown, encoding="utf-8")
    print(f"Wrote {dest.relative_to(ROOT)}")
    print(f"Edit link: {edit_link(filename)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
