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
import json
import os
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
# One retry, fed the validator's own complaints. The validator returns precise,
# actionable messages ("scenario setup must name the location: X"), which is
# exactly the shape a model can fix — but a second failure means something is
# wrong with the prompt or the model, and looping burns tokens to no purpose.
MAX_ATTEMPTS = 2

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


def _brief_prompt(brief: dict) -> str:
    facets = json.dumps(brief["seed_facets"], ensure_ascii=False, indent=2)
    rules = "\n".join(f"- {line}" for line in brief.get("instructions", []))
    return (
        f"Compose the daily dream bundle for {brief['proposal_date']}.\n\n"
        f"These Facets are the creative constraints. The umbrella genres and "
        f"creature govern the whole bundle; each element's own Facet list "
        f"governs that element. Use them — do not ignore one because it is "
        f"awkward, that friction is the point.\n\n{facets}\n\n"
        f"House rules:\n{rules}\n\n"
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
    prompt = _brief_prompt(brief)
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

        proposal = parse_json_object(call_claude(ask, SYSTEM_PROMPT, api_key))
        # The seed plan is ours, not the model's — it is validated against the
        # live Facet catalog and must survive verbatim. Overwrite rather than
        # trust: a model that helpfully "tidied" the Facets would pass its own
        # bundle while silently detaching it from the catalog.
        proposal["seed_facets"] = brief["seed_facets"]
        proposal.pop("narrator", None)

        complaints = dreams.validate_proposal(
            dreams.normalize(proposal, dreams.existing_slugs())
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
