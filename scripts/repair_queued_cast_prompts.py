#!/usr/bin/env python3
"""Strip the crowd-summoning casting clause from pending ArtJob prompts.

Companion to `scripts/dream_art_prompts.py`. That module fixes prompts written
from today onward; this one drains the jobs already sitting in the queue that
would reproduce the bug when they render.

The clause in question — "cast characters naturally across many species, ages,
body sizes, body shapes, gender presentations, and levels of conventional
attractiveness; include robots only when the subject or scene explicitly calls
for them" — was appended to every prompt by the Kind Robots enqueue path. It
reads as an instruction, but Krea 2 renders it as subject matter: a crowd. On a
prompt for a ladle, a tuning fork, or a dashboard, that crowd replaces the
subject entirely.

For each pending job carrying the clause this script decides one of two things:

  * the prompt already describes people (a character portrait, a scene with a
    cast) → the clause is rewritten to the narrower, cast-only wording, keeping
    the inclusivity intent where it actually applies; or
  * the prompt describes an object, tool, place, or interface → the clause is
    replaced with an explicit unpeopled direction.

The classification is a keyword heuristic over the prompt's *subject* clause,
so `--apply` prints every decision and `--dry-run` (the default) is the way to
audit it before committing.

Usage:
  python scripts/repair_queued_cast_prompts.py
  python scripts/repair_queued_cast_prompts.py --apply
  python scripts/repair_queued_cast_prompts.py --apply --project dream-cycle

Environment:
  KR_API_TOKEN   required (admin or server key)
  KR_BASE_URL    defaults to https://kind-robots.vercel.app
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
# `slugify` drops a leading article per specs/SLUG-POLICY.md ("The Second Verse"
# -> second-verse), which is what the queued imagePaths were built from; a naive
# slugify never matches them. Import it rather than re-deriving the rule.
from build_dream_records import slugify  # noqa: E402
from dream_art_prompts import (  # noqa: E402
    character_prompt,
    location_prompt,
    reward_prompt,
    scenario_prompt,
    world_prompt,
)

ROOT = Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "projects" / "dream-cycle" / "backlog"

KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kind-robots.vercel.app").rstrip("/")
KR_API_TOKEN = os.environ.get("KR_API_TOKEN", "").strip()

# The full house block, as `replaceVagueArtDirection` used to emit it, anchored
# on both ends of the block. An earlier version used a lazy `[^;]*?`
# with a `(?=[,;])` lookahead, which stopped at the first comma after "species"
# and left "ages, body sizes, ... conventional attractiveness" stranded in the
# prompt — the crowd would have rendered anyway.
CAST_CLAUSE = re.compile(
    r"[,;]?\s*cast characters naturally across many species"
    r"(?:.*?conventional attractiveness)?"
    r"(?:\s*;\s*include robots only when the subject or scene "
    r"explicitly calls for them)?",
    re.I,
)

CAST_REPLACEMENT = (
    "cast the people who appear naturally across many species, ages, body sizes, "
    "body shapes, and gender presentations"
)
UNPEOPLED_REPLACEMENT = (
    "an unpeopled frame — the subject stands alone with no bystanders, "
    "onlookers, or crowd"
)

# Subjects that are objects by definition. These win over PEOPLE_WORDS, because
# a reward blurb routinely mentions the people it affects ("maps the social
# hierarchy of any closed community") without any of them belonging in frame —
# which is exactly the confusion that produced the crowds in the first place.
OBJECT_SUBJECTS = re.compile(
    r"\b(treasure-card|ability card|item card|reward card|app-icon|product shot|"
    r"still life|one object alone in frame)\b|\((?:ITEM|SKILL)\)",
    re.I,
)

# Words that mean the frame genuinely holds people. Checked against the subject
# clause only (the text before the style tail), never the whole prompt — the
# tail itself is what we are trying to neutralise.
PEOPLE_WORDS = re.compile(
    r"\b(character|portrait|figure|person|people|crowd|team|crew|family|players?|"
    r"operators?|companions?|audience|congregation|gathering|community|"
    r"adventurers?|shoppers?|workers?|narrator|cast|celebrat\w*|"
    r"scene art|establishing scene)\b",
    re.I,
)


DREAM_IMAGE_PATH = re.compile(
    r"^public/images/dreams/(?P<dream>[^/]+)/(?P<element>.+?)-card\.(?:webp|png|jpg)$")

# Rewards also get a canonical image outside the per-dream folder. Jobs writing
# here were built by the page-asset path, so their prompts carry site navigation
# chrome ("Human gates, pitch proposals, notifications...") instead of the
# reward. Rebuild those from the proposal too.
REWARD_IMAGE_PATH = re.compile(
    r"^public/images/rewards/(?P<type>item|skill)/(?P=type)-(?P<element>.+?)\.(?:webp|png|jpg)$",
    re.I)


def _reward_prompt_for(image_path: str) -> Optional[str]:
    match = REWARD_IMAGE_PATH.match(image_path or "")
    if not match:
        return None
    element = match.group("element")
    for proposal in _proposals():
        vibe = proposal.get("vibe") or {}
        for reward in proposal.get("rewards") or []:
            if slugify(reward.get("name", "")) != element:
                continue
            if str(reward.get("reward_type", "")).lower() != match.group("type").lower():
                continue
            return reward_prompt(reward.get("name", ""), reward.get("reward_type", "ITEM"),
                                 reward.get("look", ""), reward.get("grants", ""),
                                 reward.get("rarity", ""), proposal.get("title", ""),
                                 vibe.get("line", ""))
    return None


def _proposals() -> list[dict[str, Any]]:
    found = []
    for path in sorted(BACKLOG.glob("*.md")):
        match = re.search(r"<!-- proposal-data\n(.*?)\n-->",
                          path.read_text(encoding="utf-8"), re.S)
        if not match:
            continue
        try:
            found.append(json.loads(match.group(1)))
        except json.JSONDecodeError:
            continue
    return found


def dream_cycle_prompt(image_path: str) -> Optional[str]:
    """Rebuild a queued dream-cycle prompt from its proposal.

    A dream-cycle job writes to `public/images/dreams/<dream>/<element>-card.webp`
    and is later attached to the real record. Stripping the casting clause from
    such a job would leave the *other* half of the bug in place — a subject
    clause with no physical description. Rebuilding from the proposal applies
    exactly the same rules a fresh build would.
    """
    from_reward_path = _reward_prompt_for(image_path)
    if from_reward_path:
        return from_reward_path

    match = DREAM_IMAGE_PATH.match(image_path or "")
    if not match:
        return None
    dream_slug, element = match.group("dream"), match.group("element")

    for proposal in _proposals():
        if slugify(proposal.get("slug") or "") != dream_slug:
            continue
        title = proposal.get("title", "")
        vibe = proposal.get("vibe") or {}
        line = vibe.get("line", "")

        if element == dream_slug:
            return world_prompt(title, proposal.get("idea", ""), line,
                                vibe.get("art_direction", ""))
        for loc in proposal.get("locations") or []:
            if slugify(loc.get("title", "")) == element:
                return location_prompt(loc.get("title", ""), loc.get("art_direction", ""),
                                       loc.get("known_for", ""), loc.get("best_scene", ""),
                                       title, line)
        for char in proposal.get("characters") or []:
            if slugify(char.get("name", "")) == element:
                return character_prompt(char.get("name", ""), char.get("look", ""),
                                        char.get("role_drive", ""), char.get("carries", ""),
                                        title, line)
        for reward in proposal.get("rewards") or []:
            if slugify(reward.get("name", "")) == element:
                return reward_prompt(reward.get("name", ""), reward.get("reward_type", "ITEM"),
                                     reward.get("look", ""), reward.get("grants", ""),
                                     reward.get("rarity", ""), title, line)
        for scenario in proposal.get("scenarios") or []:
            if f"{slugify(scenario.get('title', ''))}-scenario" == element:
                locations = ", ".join(l.get("title", "") for l in proposal.get("locations") or [])
                return scenario_prompt(scenario.get("title", ""), scenario.get("setup", ""),
                                       locations, title, line)
    return None


def http_json(method: str, url: str, body: Any = None,
              timeout: int = 90) -> tuple[int, Any]:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if KR_API_TOKEN:
        req.add_header("Authorization", f"Bearer {KR_API_TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode() or "null")
    except urllib.error.HTTPError as error:
        try:
            payload = json.loads(error.read().decode() or "null")
        except (ValueError, OSError):
            payload = None
        return error.code, payload
    except (OSError, ValueError) as error:
        return 0, {"message": str(error)}


def pending_jobs(project: Optional[str]) -> list[dict[str, Any]]:
    jobs: list[dict[str, Any]] = []
    page = 1
    while True:
        query = f"status=PENDING&pageSize=200&page={page}"
        if project:
            query += f"&projectSlug={project}"
        status, payload = http_json("GET", f"{KR_BASE_URL}/api/art/queue?{query}")
        if status != 200:
            raise SystemExit(f"Could not list the queue ({status}): {str(payload)[:200]}")
        data = payload.get("data") or {}
        jobs.extend(data.get("jobs") or [])
        pagination = data.get("pagination") or {}
        if page >= int(pagination.get("pageCount") or 1):
            return jobs
        page += 1


def job_prompt(job: dict[str, Any]) -> str:
    payload = job.get("payload") or {}
    return str(payload.get("promptString") or payload.get("basePromptString") or "")


def subject_clause(prompt: str) -> str:
    """Everything before the house style tail — i.e. what is actually depicted."""
    cut = re.search(r"detailed mature western animation", prompt, re.I)
    return prompt[: cut.start()] if cut else prompt


def rewrite(prompt: str, image_path: str = "") -> tuple[str, str]:
    """Return (new_prompt, verdict) where verdict explains the treatment."""
    rebuilt = dream_cycle_prompt(image_path)
    if rebuilt:
        return rebuilt, "REBUILT"

    subject = subject_clause(prompt)
    has_people = bool(PEOPLE_WORDS.search(subject)) and not OBJECT_SUBJECTS.search(subject)
    replacement = CAST_REPLACEMENT if has_people else UNPEOPLED_REPLACEMENT
    new = CAST_CLAUSE.sub(f", {replacement}", prompt, count=1)
    # Collapse any doubled separators the substitution leaves behind.
    new = re.sub(r"\s*,\s*,", ",", new)
    new = re.sub(r"\s+", " ", new).strip().strip(",").strip()
    return new, ("KEEP CAST" if has_people else "UNPEOPLED")


def apply_edit(job_id: int, prompt: str) -> bool:
    status, payload = http_json(
        "POST", f"{KR_BASE_URL}/api/art/queue/{job_id}/edit",
        {"overrides": {"promptString": prompt}})
    if status not in (200, 201):
        print(f"  edit FAILED {status} job/{job_id}: {str(payload)[:200]}", file=sys.stderr)
        return False
    return True


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true",
                        help="write the rewritten prompts (default is a dry run)")
    parser.add_argument("--project", help="restrict to one projectSlug")
    args = parser.parse_args(argv)

    if not KR_API_TOKEN:
        print("KR_API_TOKEN is required.", file=sys.stderr)
        return 2

    jobs = pending_jobs(args.project)
    affected = [job for job in jobs if CAST_CLAUSE.search(job_prompt(job))]
    print(f"{len(affected)} of {len(jobs)} pending job(s) carry the casting clause.\n")
    if not affected:
        return 0

    edited = 0
    for job in affected:
        prompt = job_prompt(job)
        image_path = str((job.get("payload") or {}).get("imagePath") or "")
        new_prompt, verdict = rewrite(prompt, image_path)
        print(f"[{job['id']}] {verdict:9} {job.get('projectSlug') or '(no project)'}")
        print(f"  subject: {subject_clause(new_prompt)[:150].strip()}")
        if new_prompt == prompt:
            print("  ! substitution made no change; skipping", file=sys.stderr)
            continue
        if args.apply and apply_edit(job["id"], new_prompt):
            edited += 1
            print("  rewritten")

    if args.apply:
        print(f"\nRewrote {edited} of {len(affected)} job prompt(s).")
    else:
        print(f"\nDry run. Re-run with --apply to rewrite {len(affected)} job prompt(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
