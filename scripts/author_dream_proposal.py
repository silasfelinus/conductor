#!/usr/bin/env python3
"""
author_dream_proposal.py — write the day's daily-dream proposal without waiting
for a human-triggered session to notice it is missing.

Silas, 2026-08-09: "I'm not sure why the next dreams aren't written the turn the
digest is sent, or a step later if there isn't enough process. As progress goes,
that's very high on automated tasks or should be."

He is right, and the reason was mundane: every piece existed except the glue.
`build_dream_proposal.py --brief` produces the deterministic Facet seed plan and
`--from-json` validates and writes the finished bundle, but the step in between —
actually authoring the six assets — lived only in CLAUDE.md's session-startup
checklist. So a proposal appeared when a session happened to run and happened to
notice, and on a day with no session, no dream. daily-digest.yml sent the email
and stopped.

This closes that. It runs the brief, asks Claude for the six assets as JSON,
merges the seed plan back in unchanged, and hands the result to the same
validator a human-authored proposal goes through. Nothing about the contract is
relaxed for being automated: same required fields, same "exactly one ITEM and one
SKILL", same rule that the scenario names the vibe, location, and character.

    python scripts/author_dream_proposal.py                # today, Pacific
    python scripts/author_dream_proposal.py --dry-run      # print, write nothing
    python scripts/author_dream_proposal.py --date 2026-08-09

Exit codes: 0 wrote (or a proposal already existed — this is idempotent and safe
to run on every digest), 1 could not author one. Requires ANTHROPIC_API_KEY, the
same secret hourly-conductor.yml already uses for build_conductor_summary.py.
Without it the script says so and exits 1 rather than writing a stub: a hollow
proposal is worse than a missing one, because the missing one still gets noticed.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import build_dream_proposal as dreams  # noqa: E402

API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"
# Sonnet by default, not Opus. This is scheduled daily spend, and the guard in
# tests/test_no_unreviewed_model_spend.py exists because unattended model calls
# compound quietly. Sonnet is a real step up from the Haiku the hourly summary
# uses, which matters here — the output becomes six database objects and the art
# prompts for all of them. Set DREAM_AUTHOR_MODEL=claude-opus-5 if the bundles
# come out flat and the cost is worth it.
MODEL = os.environ.get("DREAM_AUTHOR_MODEL", "claude-sonnet-5")
MAX_TOKENS = 4000
# One retry, fed the parser/validator's own complaints. The validator returns
# precise, actionable messages ("scenario setup must name the location: X"),
# which is exactly the shape a model can fix — but a second failure means
# something is wrong with the prompt or the model, and looping burns tokens to
# no purpose.
MAX_ATTEMPTS = 2

REPO_ROOT = Path(__file__).resolve().parents[1]
DREAM_BACKLOG_DIR = REPO_ROOT / "projects" / "dream-cycle" / "backlog"
HISTORY_CATEGORIES = ("dreams", "locations", "characters", "rewards", "scenarios")
HISTORY_PROPOSAL_LIMIT = 45
HISTORY_PROMPT_LIMIT = 20

NAMING_DIRECTIONS = (
    "Use a grounded two-part name with an ordinary, non-compound family name; "
    "the world can be strange without the name announcing it.",
    "Use a one-token mononym, nickname, or callsign that sounds lived-in rather "
    "than deliberately edgy.",
    "Use a three-part name or a name with an initial; keep the surname plausible "
    "rather than ornamental or compound-built.",
    "Use a speculative one- or two-token name, but avoid clipped X-heavy first "
    "names and avoid English noun+noun fantasy surnames.",
    "Use an understated conventional full name. Do not literalize the character's "
    "species, occupation, personality, or magic in the name.",
)

SYSTEM_PROMPT = """You are the creative generator for Kind Robots' daily dream \
cycle. You write one coherent six-asset bundle per day: a dream vibe, a dream \
location, a Character, an ITEM Reward, a SKILL Reward, and a Scenario.

Return ONLY a JSON object. No prose, no markdown fence, no commentary.

Shape:
{
  "title": str, "slug": "kebab-case", "idea": str,
  "vibe": {"title": str, "line": str, "art_direction": str},
  "locations": [{"title","known_for","local_rule","best_scene","art_direction"}],
  "characters": [{"name","role_drive","carries","complication","look"}],
  "rewards": [
    {"name","reward_type":"ITEM","rarity","grants","best_used_when","catch","look"},
    {"name","reward_type":"SKILL","rarity","grants","best_used_when","catch","look"}
  ],
  "scenarios": [{"title","setup"}]
}

Exactly one location, one character, two rewards (one ITEM, one SKILL), one \
scenario. No narrator. rarity is one of COMMON, UNCOMMON, RARE, EPIC, LEGENDARY.

Naming is part of the creative variation, not decorative filler. Recent names \
are supplied in the user prompt; treat their distinctive words, roots, sounds, \
and constructions as spent vocabulary, not as a palette to remix. In particular, \
do not default to a clipped fantasy first name plus a whimsical compound surname. \
If a recent character was named "Vex Thistlewick", then "Vexa Thistlemaw" is \
not a fresh name. Vary register and structure across days: ordinary names, \
mononyms, callsigns, multi-part names, and genuinely setting-native speculative \
names can all belong here. Do not manufacture pseudo-ethnic names by vaguely \
imitating a real culture; if using a real-world naming tradition, use a plausible \
name rather than syllable salad. Names should fit the character without simply \
spelling out their species, job, personality, material, or genre Facets.

The same anti-echo rule applies to dream, location, reward, and scenario titles. \
A new title may share ordinary glue words, but should not recycle the distinctive \
noun pair or signature construction of a recent title.

Every `look` and `art_direction` string is fed straight to an image model. Write \
what is physically visible — material, shape, scale, colour, wear, how light \
falls — not what the thing does. "A dented tin ladle the length of a forearm, \
its bowl worn to mirror-bright, handle wrapped in salt-stiffened cord" is \
usable; "it surfaces the hidden fortune buried in a person" is not. A Reward's \
`look` describes an object or a visible effect, never a person: a Reward whose \
look described what it did once rendered as a crowd of strangers and no object.

Do not write conditional instructions an image model cannot evaluate ("include \
robots only when the scene calls for them", "when any figures appear..."). \
Decide, and state one outcome. Do not name a physical format — no "trading card \
illustration", "book cover", "comic panel" — you are describing a scene, not a \
printed object. Do not pile up text exclusions; say nothing about text at all.

Author the scenario LAST, and its `setup` must name the vibe title, the location \
title, and the character name literally."""


def _proposal_data(text: str) -> dict:
    match = re.search(r"<!--\s*proposal-data\s*\n(.*?)\n-->", text, re.DOTALL)
    if not match:
        return {}
    try:
        payload = json.loads(match.group(1))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _append_unique(values: list[str], value) -> None:
    if not isinstance(value, str):
        return
    clean = value.strip()
    if clean and clean not in values:
        values.append(clean)


def _names_from_proposal(text: str) -> dict[str, list[str]]:
    """Collect the names the digest can surface from one proposal file."""
    out = {category: [] for category in HISTORY_CATEGORIES}
    data = _proposal_data(text)

    _append_unique(out["dreams"], data.get("title"))
    vibe = data.get("vibe")
    if isinstance(vibe, dict):
        _append_unique(out["dreams"], vibe.get("title"))

    for row in data.get("locations") or []:
        if isinstance(row, dict):
            _append_unique(out["locations"], row.get("title"))
    for row in data.get("characters") or []:
        if isinstance(row, dict):
            _append_unique(out["characters"], row.get("name"))
    for row in data.get("rewards") or []:
        if isinstance(row, dict):
            _append_unique(out["rewards"], row.get("name"))
    for row in data.get("scenarios") or []:
        if isinstance(row, dict):
            _append_unique(out["scenarios"], row.get("title"))

    # Older daily proposals may predate proposal-data. Preserve character memory
    # anyway because character-name recurrence is the costly failure mode here.
    if not out["characters"]:
        match = re.search(
            r"^## Character \(1\)\s*\n-\s+\*\*(.+?)\*\*\s+[—-]",
            text,
            re.MULTILINE,
        )
        if match:
            _append_unique(out["characters"], match.group(1))
    return out


def recent_name_history(
    day: str,
    proposal_limit: int = HISTORY_PROPOSAL_LIMIT,
    backlog_dir: Path | str | None = None,
) -> dict[str, list[str]]:
    """Read names from recent proposals before `day`, newest names last.

    The backlog is already the durable source behind the digest, so this adds no
    database or provider dependency. Missing or malformed history degrades to an
    empty list rather than blocking the day's proposal.
    """
    root = Path(backlog_dir) if backlog_dir is not None else DREAM_BACKLOG_DIR
    history = {category: [] for category in HISTORY_CATEGORIES}
    if not root.exists():
        return history

    paths = [
        path
        for path in sorted(root.glob("20??-??-??-*.md"))
        if path.name[:10] < day
    ][-proposal_limit:]

    for path in paths:
        try:
            names = _names_from_proposal(path.read_text(encoding="utf-8"))
        except OSError:
            continue
        for category in HISTORY_CATEGORIES:
            for name in names[category]:
                _append_unique(history[category], name)
    return history


def naming_direction(day: str) -> str:
    """Rotate name structure deterministically instead of finding one new rut."""
    try:
        ordinal = datetime.date.fromisoformat(day).toordinal()
    except ValueError:
        ordinal = sum(ord(char) for char in day)
    return NAMING_DIRECTIONS[ordinal % len(NAMING_DIRECTIONS)]


def _name_words(name: str) -> list[str]:
    return re.findall(r"[a-z]+", str(name).casefold())


def _edit_distance(left: str, right: str) -> int:
    if left == right:
        return 0
    if not left:
        return len(right)
    if not right:
        return len(left)
    previous = list(range(len(right) + 1))
    for i, char_left in enumerate(left, 1):
        current = [i]
        for j, char_right in enumerate(right, 1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[j] + 1,
                    previous[j - 1] + (char_left != char_right),
                )
            )
        previous = current
    return previous[-1]


def _near_word(left: str, right: str) -> bool:
    if left == right:
        return True
    if min(len(left), len(right)) < 3 or abs(len(left) - len(right)) > 1:
        return False
    return _edit_distance(left, right) <= 1


def _common_prefix_length(left: str, right: str) -> int:
    length = 0
    for a, b in zip(left, right):
        if a != b:
            break
        length += 1
    return length


def name_diversity_complaints(name: str, recent_names: list[str]) -> list[str]:
    """Reject the high-signal repeats a prompt alone is bad at noticing.

    This intentionally does not attempt to score whether a name is "creative".
    It catches concrete archive echoes: exact names, reused/near-reused given
    names, and distinctive long surname roots such as Thistlewick/Thistlemaw.
    """
    words = _name_words(name)
    if not words:
        return []

    normalized = " ".join(words)
    first = words[0]
    last = words[-1] if len(words) > 1 else ""
    complaints: list[str] = []

    for recent in recent_names:
        recent_words = _name_words(recent)
        if not recent_words:
            continue
        if normalized == " ".join(recent_words):
            complaints.append(
                f"character name {name!r} exactly repeats recent name {recent!r}; "
                "choose a genuinely different name"
            )
            return complaints

    for recent in recent_names:
        recent_words = _name_words(recent)
        if not recent_words:
            continue
        recent_first = recent_words[0]
        if _near_word(first, recent_first):
            complaints.append(
                f"character given name {first!r} repeats or nearly repeats recent "
                f"name {recent!r}; choose a different given-name root"
            )
            break

    if last:
        for recent in recent_names:
            recent_words = _name_words(recent)
            if len(recent_words) < 2:
                continue
            recent_last = recent_words[-1]
            if (
                min(len(last), len(recent_last)) >= 6
                and _common_prefix_length(last, recent_last) >= 6
            ):
                complaints.append(
                    f"character surname {last!r} echoes the distinctive root of "
                    f"recent name {recent!r}; choose a different surname construction"
                )
                break
    return complaints


def _brief_prompt(brief: dict, history: dict[str, list[str]] | None = None) -> str:
    facets = json.dumps(brief["seed_facets"], ensure_ascii=False, indent=2)
    rules = "\n".join(f"- {line}" for line in brief.get("instructions", []))
    history = history or {category: [] for category in HISTORY_CATEGORIES}
    history_lines = []
    for category in HISTORY_CATEGORIES:
        values = history.get(category) or []
        if values:
            history_lines.append(
                f"- {category.title()}: " + "; ".join(values[-HISTORY_PROMPT_LIMIT:])
            )
    history_text = "\n".join(history_lines) or "- No recent naming history available."
    direction = naming_direction(str(brief["proposal_date"]))

    return (
        f"Compose the daily dream bundle for {brief['proposal_date']}.\n\n"
        f"These Facets are the creative constraints. The umbrella genres and "
        f"creature govern the whole bundle; each element's own Facet list "
        f"governs that element. Use them — do not ignore one because it is "
        f"awkward, that friction is the point.\n\n{facets}\n\n"
        f"House rules:\n{rules}\n\n"
        "Recent naming history, oldest to newest. These are spent vocabulary and "
        "construction patterns, not inspiration to remix:\n"
        f"{history_text}\n\n"
        f"Character naming direction for today: {direction}\n"
        "This direction is deliberately rotated by date. Follow its structural "
        "shape while still fitting the character and setting.\n\n"
        f"Return the JSON object only."
    )


def call_claude(prompt: str, system: str, api_key: str, timeout: float = 120.0) -> str:
    body = json.dumps(
        {
            "model": MODEL,
            "max_tokens": MAX_TOKENS,
            "system": system,
            "messages": [{"role": "user", "content": prompt}],
        }
    ).encode()
    request = urllib.request.Request(API_URL, data=body, method="POST")
    request.add_header("content-type", "application/json")
    request.add_header("x-api-key", api_key)
    request.add_header("anthropic-version", API_VERSION)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode())
    blocks = payload.get("content") or []
    text = "".join(b.get("text", "") for b in blocks if isinstance(b, dict))
    if not text.strip():
        raise RuntimeError("Claude returned an empty completion.")
    return text


def parse_json_object(text: str) -> dict:
    """Tolerate a fenced or chatty reply without accepting a truncated one."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
        if cleaned.rstrip().endswith("```"):
            cleaned = cleaned.rstrip()[: -3]
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("no JSON object in the completion")
    return json.loads(cleaned[start : end + 1])


def author(day: str, api_key: str, verbose: bool = True) -> dict:
    brief = dreams.build_brief(day)
    history = recent_name_history(day)
    prompt = _brief_prompt(brief, history)
    complaints: list[str] = []

    for attempt in range(1, MAX_ATTEMPTS + 1):
        ask = prompt
        if complaints:
            ask += (
                "\n\nYour previous attempt failed validation:\n"
                + "\n".join(f"- {c}" for c in complaints)
                + "\n\nReturn a corrected JSON object addressing every point."
            )
        if verbose:
            print(f"authoring {day} (attempt {attempt}/{MAX_ATTEMPTS})", file=sys.stderr)

        try:
            proposal = parse_json_object(call_claude(ask, SYSTEM_PROMPT, api_key))
        except (ValueError, json.JSONDecodeError) as error:
            complaints = [f"completion was not valid JSON: {error}"]
            if verbose:
                print("  rejected: " + complaints[0], file=sys.stderr)
            continue

        # The seed plan is ours, not the model's — it is validated against the
        # live Facet catalog and must survive verbatim. Overwrite rather than
        # trust: a model that helpfully "tidied" the Facets would pass its own
        # bundle while silently detaching it from the catalog.
        proposal["seed_facets"] = brief["seed_facets"]
        proposal.pop("narrator", None)

        normalized = dreams.normalize(proposal, dreams.existing_slugs())
        complaints = dreams.validate_proposal(normalized)
        characters = proposal.get("characters") or []
        if characters and isinstance(characters[0], dict):
            complaints.extend(
                name_diversity_complaints(
                    characters[0].get("name", ""), history.get("characters", [])
                )
            )
        if not complaints:
            return proposal
        if verbose:
            print(
                "  rejected: " + "; ".join(complaints[:5]),
                file=sys.stderr,
            )

    raise RuntimeError(
        "Could not author a valid proposal after "
        f"{MAX_ATTEMPTS} attempts: {'; '.join(complaints)}"
    )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", help="Pacific date override (YYYY-MM-DD)")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print the rendered markdown without writing it",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="author even if the date already has a proposal",
    )
    parser.add_argument(
        "--no-fetch",
        action="store_true",
        help="skip the origin/main duplicate check",
    )
    args = parser.parse_args(argv)

    day = args.date or dreams._target_date()

    # Idempotent by design: this runs on every digest, and most of the time the
    # honest answer is "already done". Exit 0 so a scheduled caller does not
    # treat a healthy day as a failure.
    if not args.force:
        exists = dreams.proposal_exists_for(day)
        if not exists and not args.no_fetch and dreams.fetch_main():
            exists = dreams.remote_proposal_for(day) is not None
        if exists:
            print(f"Proposal for {day} already exists; nothing to author.")
            return 0

    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        print(
            "ANTHROPIC_API_KEY is required to author a dream proposal. "
            "Refusing to write a placeholder — a hollow proposal reads as done "
            "and stops anyone noticing the real one is missing.",
            file=sys.stderr,
        )
        return 1

    try:
        proposal = author(day, api_key)
    except (
        urllib.error.URLError,
        RuntimeError,
        ValueError,
        json.JSONDecodeError,
    ) as error:
        print(f"Could not author the {day} proposal: {error}", file=sys.stderr)
        return 1

    path = dreams.write_proposal(
        proposal,
        date=day,
        fetch=not args.no_fetch,
        dry_run=args.dry_run,
        force=args.force,
    )
    return 0 if path else 1


if __name__ == "__main__":
    raise SystemExit(main())