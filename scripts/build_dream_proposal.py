#!/usr/bin/env python3
"""
build_dream_proposal.py — generate tomorrow's "starter dream" proposal.

Each morning the digest surfaces a proposal for the next day's auto-created
output: a self-consistent slice of a world with a tight, standardized cast —

  * creative seeds chosen first: 1-2 genres + 1 occupation + 1 animal/species
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

The write is guarded twice (no-op if the date already has a proposal in the
local tree, AND a fresh origin/main re-check right before writing so a proposal
a concurrent session already landed there aborts this write — dream-cycle/t-014),
the JSON is validated (creative seeds, exact counts, one SKILL + one ITEM
reward), and the slug is de-duplicated against the backlog + SHIPPED ledger.
`--sample` writes a built-in example so the render/digest path stays verifiable
in tests.

Concurrent-session race (why the origin/main re-check exists): two sweeps in the
same window both ran --check, both saw "no proposal yet" in their own working
trees, and both authored one for the same Pacific date with DIFFERENT slugs — so
the slug-dedup never fired (2026-07-14, see projects/dream-cycle/TALKBACK.md).
The write path now re-checks fresh origin/main immediately before writing, the
same way claim_task.py re-checks before it claims. Best-effort: with no reachable
origin the check degrades to local-only rather than blocking the run. Callers in
the hourly sweep should additionally pull before --check and push right after
--from-json to shrink the window further.

Usage:
  python scripts/build_dream_proposal.py --check              # is today's written? (add --fetch to consult origin/main)
  python scripts/build_dream_proposal.py --brief              # print the authoring brief
  python scripts/build_dream_proposal.py --from-json p.json   # validate + write (or - for stdin)
  python scripts/build_dream_proposal.py --from-json - --dry-run   # preview markdown
  python scripts/build_dream_proposal.py --from-json p.json --no-fetch   # skip the origin re-check (offline)
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

BACKLOG_RELPATH = "projects/dream-cycle/backlog"
REMOTE_REF = "origin/main"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from git_plumbing import GitError, read_file_at_ref, run_git  # noqa: E402

BRIEF = """\
You are Conductor's dream author, inventing today's "starter dream" for the
Kind Robots site — an imaginative AI art + roleplay platform.

SEED FIRST (Silas, 2026-07-24). Before inventing a title, location, tower,
building, vibe, cast, or plot, choose:
- 1-2 actual STORY GENRES. Mood words such as cozy, mystical, whimsical, or
  melancholy are not genres by themselves.
- 1 specific OCCUPATION, trade, duty, or vocation with tools, routines,
  pressures, and conflicts.
- 1 ANIMAL OR SPECIES whose body, senses, movement, needs, communication, or
  culture has consequences.

Fuse those ingredients before inventing the world. Each seed must materially
change at least two parts of the result: conflict/scenarios, work/economy,
character bodies or senses, location rules, rewards, or art direction. If a
seed can be deleted without substantially changing the Dream, the concept
fails. Record the choices and the fusion explanation in `creative_seeds`.

Do NOT default to another enchanted lighthouse, mystical bell tower, magical
archive, cozy market, lantern-lit workshop, or vaguely whimsical tower with
renamed nouns. Architecture is a consequence of the seed fusion, not the idea
starter.

Invent ONE self-consistent world: two connected places, a shared genre-bearing
vibe, a small cast, a host, and two fitting rewards. Specific, tactile, wild,
and coherent — never generic fantasy filler or random-word soup.

VARIETY IS THE JOB (Silas, 2026-07-20). Every day must feel like a DIFFERENT
GENRE from the recent ones — not another warm-lantern-and-brass-robots cozy
dream. Warmth is a house value, not a genre: reach it through noir, cosmic
horror, hard sci-fi, western, heist, folk-horror, cyberpunk, myth, absurdist
comedy, sports, courtroom drama, disaster, spy thriller — wherever today's
GENRE SPARK (printed below) points. A new vibe each day means a new *genre
feel*, not a new label on the same mood. Do NOT echo the vibe, palette,
setting-type, occupation family, species family, or character archetypes of the
recently-used dreams listed below, and do NOT reuse or near-repeat any recent
character name (no second "Pip").

SLUGS (full rules: projects/dream-cycle/specs/SLUG-POLICY.md):
- kebab-case, PREFER 2 WORDS. Avoid 3+ words unless every word earns clarity.
- NO leading "the-" (wrecks alphabetical indexing) — except a genuine two-word
  proper name like "the-marrow". Never a 3+ word "the-…" slug.
- The world slug is the through-line: every element and its art reuse it.

Produce exactly (as a JSON object, then pass it to --from-json):
- creative_seeds: {
    genres: ARRAY of exactly 1-2 non-empty story genres,
    occupation: one specific non-empty occupation,
    species: one non-empty animal/species choice,
    fusion: 1-3 sentences explaining concrete consequences of all three seeds
  }
- title + slug (kebab-case, prefer 2 words, unique — must not reuse a slug below)
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

Every element must belong to the SAME world and visibly follow from the seed
fusion."""


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

    seeds = p.get("creative_seeds")
    if not isinstance(seeds, dict):
        problems.append("creative_seeds must be an object")
    else:
        genres = seeds.get("genres")
        if not (isinstance(genres, list) and 1 <= len(genres) <= 2
                and all(str(genre).strip() for genre in genres)):
            problems.append("creative_seeds.genres must be a list of exactly 1-2 non-empty genres")
        elif len({str(genre).strip().lower() for genre in genres}) != len(genres):
            problems.append("creative_seeds.genres must not contain duplicates")
        for field in ("occupation", "species", "fusion"):
            if not str(seeds.get(field, "")).strip():
                problems.append(f"creative_seeds missing {field}")

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
    "creative_seeds": {
        "genres": ["courtroom drama", "biopunk"],
        "occupation": "public defender",
        "species": "mantis shrimp",
        "fusion": (
            "Mantis-shrimp polarized vision makes color admissible evidence, while public "
            "defense structures the cast and conflicts. Biopunk turns the reef itself into "
            "living legal machinery that can mutate testimony."
        ),
    },
    "title": "Prism Appeal",
    "slug": "prism-appeal",
    "idea": (
        "In a reef-city where crimes are reconstructed as polarized-light displays, a "
        "mantis-shrimp public defender represents creatures whose colors have been edited "
        "by living evidence. Visitors come to argue impossible cases, read truths invisible "
        "to ordinary eyes, and decide whether a memory can be guilty."
    ),
    "vibe": {
        "title": "Chromatic Legal Thriller",
        "line": "Fast objections, biological evidence, and dazzling courtroom reversals where seeing more colors creates more doubt.",
    },
    "locations": [
        {
            "title": "The Spectrum Court",
            "known_for": "hearings projected through twelve channels of polarized light that only some species can perceive.",
            "local_rule": "No testimony is admissible until every present species receives a translation it can physically sense.",
            "best_scene": "Cella freezes a verdict by revealing a hidden thirteenth color in the prosecution's reconstruction.",
            "art_direction": "underwater biopunk courtroom grown from coral ribs, mantis shrimp advocates flashing polarized colors, layered spectral light, tense legal drama, no fantasy tower.",
        },
        {
            "title": "The Evidence Reef",
            "known_for": "living exhibits that regrow damaged memories as coral branches and sometimes invent details to survive.",
            "local_rule": "Evidence may be questioned, fed, or cross-examined, but never harvested after midnight.",
            "best_scene": "a witness memory molts into a new shape while the defense team races to preserve its original colors.",
            "art_direction": "labyrinthine living reef archive, translucent memory coral, forensic divers, mantis shrimp color signals, clinical biopunk texture, high visual contrast.",
        },
    ],
    "characters": [
        {
            "name": "Cella Nineflash",
            "role_drive": "mantis-shrimp public defender determined to prove that perception differences are not deception.",
            "carries": "a fan of neutral-density filters used to reveal suppressed color testimony.",
            "complication": "her strike reflex fires whenever a witness lies, which the court treats as prejudicial theater.",
            "look": "compact mantis shrimp in a tailored pressure harness, rotating stalk eyes, twelve-color legal sash, scarred striking clubs kept formally folded.",
        },
        {
            "name": "Clerk Inkline",
            "role_drive": "cuttlefish court clerk who wants every ruling translated into patterns all reef species can understand.",
            "carries": "a stenography mantle that records speech as moving skin color.",
            "complication": "the mantle has begun inserting dissenting opinions no judge remembers dictating.",
            "look": "broad cuttlefish body in a black clerk's collar, chromatophore text rippling across the arms, ink-stained document satchel.",
        },
        {
            "name": "Toma Grey",
            "role_drive": "human forensic diver and defense investigator searching for the technician who altered his color vision.",
            "carries": "a cracked multispectral visor that labels colors he can no longer see.",
            "complication": "the visor may be the prosecution's missing evidence and is slowly learning to testify on its own.",
            "look": "weathered diver in patched pressure cloth, one luminous visor lens, evidence tags braided through silver hair.",
        },
    ],
    "rewards": [
        {
            "name": "Objection Flash",
            "reward_type": "SKILL",
            "rarity": "RARE",
            "grants": "the ability to expose one hidden sensory channel in a claim, illusion, or memory.",
            "best_used_when": "everyone agrees on what happened a little too quickly.",
            "catch": "you also reveal one uncomfortable detail that supports the opposing side.",
        },
        {
            "name": "Precedent Carapace",
            "reward_type": "ITEM",
            "rarity": "EPIC",
            "grants": "a molted shell plate that can replay the strongest argument ever made nearby.",
            "best_used_when": "you need authority in a place whose rules are changing beneath you.",
            "catch": "the precedent repeats exactly, including the flaw that eventually overturned it.",
        },
    ],
    "scenarios": [
        {
            "title": "The Color That Testified",
            "setup": "A forbidden wavelength appears in the Evidence Reef and accuses Cella's client; the player must cross-examine a color no one can agree they saw.",
        },
        {
            "title": "Appeal of the Molting Witness",
            "setup": "The court's key memory coral changes species mid-hearing, forcing the cast to decide whether its previous testimony still belongs to the same witness.",
        },
    ],
    "narrator": {
        "name": "Clerk Inkline",
        "voice": "precise, breathy, and dryly amused, with legal citations displayed as shifting skin patterns.",
        "personality": "methodical, skeptical, secretly delighted by a beautifully constructed objection.",
        "appears_as": "a cuttlefish clerk hovering beside a living stenography rail.",
        "best_for": "case briefs, sensory puzzles, moral arguments, and explaining reef law without pretending it is sensible.",
        "expressions": "NEUTRAL plus THINKING, SURPRISED, ANXIOUS, PROUD, DISGUSTED, and a FACEPALMING action when procedure collapses.",
        "topics": ["Reef Precedents (lore)", "Evidence That Bites (mystery)", "Ask the Clerk (advice)"],
    },
}


_LEADING_ARTICLES = ("the-", "a-", "an-")


def slugify(text: str) -> str:
    """kebab-case per specs/SLUG-POLICY.md — drops a leading article unless doing
    so leaves a single bare word (so `the-marrow` survives, `the-comet-market`
    becomes `comet-market`)."""
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    for art in _LEADING_ARTICLES:
        if s.startswith(art):
            rest = s[len(art):]
            if rest and "-" in rest:
                s = rest
            break
    return s or "starter-dream"


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

    seeds = p["creative_seeds"]
    genres = " + ".join(str(genre).strip() for genre in seeds["genres"])
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

## Creative seeds
- **Genres:** {genres}
- **Occupation:** {seeds['occupation']}
- **Animal / species:** {seeds['species']}
- **Fusion:** {seeds['fusion']}

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


def _proposal_date_in_text(text: str) -> Optional[str]:
    """The `proposal_date` frontmatter value in a backlog file's text, or None."""
    m = re.search(r"^proposal_date:\s*(.+)$", text, re.MULTILINE)
    return m.group(1).strip().strip("'\"") if m else None


def proposal_exists_for(date: str) -> bool:
    """True if a daily proposal for `date` is already in the LOCAL backlog (skip regen)."""
    for path in glob.glob(str(BACKLOG / "*.md")):
        name = Path(path).name
        if name.startswith("_") or name == "README.md":
            continue
        try:
            text = Path(path).read_text(encoding="utf-8")
        except OSError:
            continue
        if _proposal_date_in_text(text) == date:
            return True
    return False


def fetch_main(quiet: bool = True) -> bool:
    """Best-effort `git fetch origin main`.

    Returns True if origin/main was refreshed, False if there's no reachable origin
    (offline, no remote configured, sandbox with no network) — in which case callers
    degrade to the local-only check rather than failing the whole run.
    """
    args = ["fetch", "origin", "main"] + (["-q"] if quiet else [])
    try:
        run_git(ROOT, *args)
        return True
    except GitError:
        return False


def _backlog_files_at_ref(ref: str) -> list[str]:
    """Repo-relative paths of committed backlog outline files at `ref` (skips
    templates/README). Returns [] if the ref or path doesn't exist there."""
    try:
        out = run_git(ROOT, "ls-tree", "-r", "--name-only", ref, "--", BACKLOG_RELPATH)
    except GitError:
        return []
    files: list[str] = []
    for line in out.splitlines():
        line = line.strip()
        if not line.endswith(".md"):
            continue
        name = Path(line).name
        if name.startswith("_") or name == "README.md":
            continue
        files.append(line)
    return files


def remote_proposal_for(date: str, ref: str = REMOTE_REF) -> Optional[str]:
    """Filename of a proposal for `date` already committed at `ref` (origin/main),
    or None.

    This is the concurrent-session guard (dream-cycle/t-014): the local-working-tree
    check in proposal_exists_for() cannot see a proposal that ANOTHER session already
    authored and landed on origin/main between this session's --check and its write.
    Because the two sessions pick DIFFERENT slugs for the SAME Pacific date, the
    slug-dedup guard (existing_slugs) never catches the collision — only a same-date
    check against fresh origin/main does. Mirrors claim_task.py's fetch-fresh recheck.
    """
    for path in _backlog_files_at_ref(ref):
        text = read_file_at_ref(ROOT, ref, path)
        if text is not None and _proposal_date_in_text(text) == date:
            return Path(path).name
    return None


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


# Distant genre/tone families to rotate through, so the daily dream stops
# converging on one cozy-lantern mood. The brief surfaces a date-seeded few as the
# day's "genre spark" — a push away from yesterday, not a hard constraint.
GENRE_FAMILIES = [
    "hardboiled noir", "cosmic/eldritch horror", "hard science fiction",
    "weird western", "high-stakes heist", "folk horror", "cyberpunk",
    "mythic epic", "absurdist comedy", "underdog sports", "courtroom drama",
    "disaster/survival", "spy thriller", "gothic romance", "dieselpunk",
    "post-apocalyptic", "screwball farce", "haunted procedural",
    "swashbuckling adventure", "solarpunk", "silent-film slapstick",
    "biopunk/body horror", "space opera", "carnival/circus grotesque",
    "hardscrabble frontier", "psychedelic surrealism", "wuxia",
    "cozy mystery (but make the genre feel unmistakable)",
]


def _recent_proposals(limit: int = 6) -> list[str]:
    """The most recent dated proposal backlog files, newest first."""
    dated = sorted(
        (p for p in glob.glob(str(BACKLOG / "20*-*.md"))),
        key=lambda p: Path(p).name, reverse=True,
    )
    return dated[:limit]


def recent_vibes_and_names(limit: int = 6) -> tuple[list[str], list[str]]:
    """Pull vibe lines and character names from recent proposals so the brief can
    tell the author what NOT to echo (addresses 'everything feels the same' and
    the duplicate 'Pip' character names, Silas 2026-07-20)."""
    vibes: list[str] = []
    names: list[str] = []
    for path in _recent_proposals(limit):
        try:
            text = Path(path).read_text(encoding="utf-8")
        except OSError:
            continue
        m = re.search(r"^## Vibe / genre dream\s*\n\*\*(.+?)\*\*", text, re.MULTILINE)
        if m:
            vibes.append(m.group(1).strip())
        for cm in re.finditer(r"^- \*\*(.+?)\*\*", text, re.MULTILINE):
            frag = cm.group(1).strip()
            # character bullets read "Name — role…"; keep the short leading name
            name = frag.split(" — ")[0].split("(")[0].strip()
            if name and len(name) <= 40:
                names.append(name)
    # de-dup, keep order
    return list(dict.fromkeys(vibes)), list(dict.fromkeys(names))


def _genre_spark(date: str) -> list[str]:
    """A deterministic-by-date pick of distant genre families for the day."""
    seed = sum(ord(c) for c in date)
    return [GENRE_FAMILIES[(seed + i * 7) % len(GENRE_FAMILIES)] for i in range(3)]


def print_brief() -> None:
    """Print the authoring brief for the sweeping agent (spec + slugs/vibes to avoid)."""
    avoid = ", ".join(sorted(existing_slugs())) or "(none yet)"
    vibes, names = recent_vibes_and_names()
    spark = _genre_spark(_target_date())
    print(BRIEF)
    print(f"\nGENRE SPARK for today (choose 1-2, or go somewhere just as far): "
          f"{', '.join(spark)}.")
    print("Choose the OCCUPATION and ANIMAL/SPECIES before inventing the location; "
          "do not let either become decorative garnish.")
    print(f"Recently-used vibes — do NOT echo their genre/mood: "
          f"{', '.join(vibes) or '(none yet)'}")
    print(f"Recently-used names/titles — do NOT reuse or near-repeat: "
          f"{', '.join(names[:30]) or '(none yet)'}")
    print(f"\nSlugs already used (do NOT reuse or closely echo): {avoid}")
    print("\nWhen your JSON is ready:  python scripts/build_dream_proposal.py --from-json <file|->")


def write_proposal(proposal: dict[str, Any], date: Optional[str] = None,
                   dry_run: bool = False, force: bool = False,
                   fetch: bool = True) -> Optional[Path]:
    """Validate + normalize an agent-authored proposal and write today's file.

    Guarded twice: no-op (with a message) if `date` already has a proposal in the
    LOCAL working tree, and — unless `fetch` is off or `dry_run`/`force` — re-checks
    fresh `origin/main` immediately before writing so a proposal another concurrent
    session landed there since this session's --check aborts this write instead of
    creating a second same-date proposal (dream-cycle/t-014). Returns the written
    path, or None.
    """
    date = _target_date(date)
    problems = validate_proposal(proposal)
    if problems:
        print("Proposal JSON is invalid:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return None
    if proposal_exists_for(date) and not force:
        print(f"Proposal for {date} already exists locally — not writing (use --force to override).",
              file=sys.stderr)
        return None
    # Concurrent-session guard: re-check origin/main fresh, the way claim_task.py
    # re-checks before it writes a claim. Best-effort — if there's no reachable
    # origin (offline/sandbox), fetch_main() returns False and we fall back to the
    # local check above rather than blocking the run.
    if fetch and not force and not dry_run and fetch_main():
        landed = remote_proposal_for(date)
        if landed:
            print(
                f"Proposal for {date} already landed on origin/main ({landed}) since "
                "--check ran — another session beat this one. Not writing; re-run --check "
                "(and fold in its Notes from Silas before building).",
                file=sys.stderr,
            )
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
    ap.add_argument("--fetch", action="store_true",
                    help="with --check: also consult fresh origin/main (catches a proposal a "
                         "concurrent session already landed but that isn't in this working tree yet)")
    ap.add_argument("--no-fetch", action="store_true",
                    help="with --from-json: skip the origin/main concurrent-session re-check "
                         "(offline/local-only writes)")
    args = ap.parse_args()

    date = _target_date(args.date)

    if args.check:
        exists = proposal_exists_for(date)
        if not exists and args.fetch and fetch_main():
            exists = remote_proposal_for(date) is not None
        if exists:
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
                                 force=args.force, fetch=not args.no_fetch)
        return 0 if written else 1

    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
