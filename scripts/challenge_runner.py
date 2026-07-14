#!/usr/bin/env python3
"""
challenge_runner.py — auto-participate in Challenge Center challenges.

For each OPEN challenge conductor-claude (or another contender) hasn't already
entered, builds the challenge prompt, calls the Claude API for an answer, and
submits it via the same submission flow as challenge_submit.py.

Scope: only TEXT and REASONING challenges are handled here — their submissions
are plain outputText, which is all challenge_submit.py's --output flow
supports. ART challenges need a generated ArtImage (see the separate
scripts/curate_art.py pipeline) and CHARACTER/SCENARIO challenges need a KR
Character/Scenario record created first; both are skipped with a note rather
than attempted.

Usage:
  python scripts/challenge_runner.py [--all]
  python scripts/challenge_runner.py --challenge <slug>
  python scripts/challenge_runner.py --all --dry-run

Steps per challenge:
  1. Fetch open challenges from the KR API (or a single challenge via --challenge).
  2. Skip challenge types this runner doesn't handle, and skip challenges the
     contender already has a submission for.
  3. Build the challenge prompt from promptText plus a short system framing.
  4. Call the Claude API for the answer.
  5. Submit the output via the shared challenge_submit helpers.
  6. Print a summary: challenges attempted, submissions created, skipped, errors.

Designed to run on a schedule (e.g. nightly cron via the AGENTS.md todo mechanism).

Env:
  ANTHROPIC_API_KEY       required to generate an answer (skip with --dry-run)
  KR_API_TOKEN            required to submit (see challenge_submit.py)
  KR_BASE_URL             default https://kind-robots.vercel.app
  CHALLENGE_RUNNER_MODEL  default claude-sonnet-5
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Import via the "scripts" package (not a bare "challenge_submit" module) so this
# module resolves to the same sys.modules entry whether run directly (python
# scripts/challenge_runner.py) or imported in tests (import scripts.challenge_runner)
# -- a mismatch here would give tests two separate challenge_submit module objects,
# silently defeating monkeypatch.setattr(challenge_submit, ...).
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts import challenge_submit as cs  # noqa: E402

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = os.environ.get("CHALLENGE_RUNNER_MODEL", "claude-sonnet-5").strip()

# Challenge types whose submission is plain outputText. CHARACTER/SCENARIO
# submissions link to a KR Character/Scenario record (not yet wired here);
# ART submissions link to a generated ArtImage (separate pipeline).
HANDLED_TYPES = {"TEXT", "REASONING"}

SYSTEM_PROMPT = (
    "You are conductor-claude, an autonomous agent contending in Kind Robots' "
    "Challenge Center arena. Read the challenge prompt and produce your best "
    "direct entry. Output ONLY the entry itself -- no preamble, no "
    "meta-commentary about being an AI, no restating the prompt."
)


class ChallengeRunnerError(Exception):
    pass


def fetch_open_challenges(base_url: str) -> list[dict]:
    status, body = cs.http_json("GET", f"{base_url}/api/challenges?status=OPEN")
    if status != 200 or not body or not body.get("success"):
        message = (body or {}).get("message", f"HTTP {status}")
        raise ChallengeRunnerError(f"failed to fetch open challenges: {message}")
    return body["data"]


def already_submitted(base_url: str, slug: str, contender_slug: str) -> bool:
    leaderboard = cs.fetch_leaderboard(base_url, slug)
    return cs.find_standing(leaderboard, contender_slug) is not None


def generate_answer(prompt_text: str, api_key: str) -> str:
    body = json.dumps(
        {
            "model": MODEL,
            "max_tokens": 1024,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": prompt_text}],
        }
    ).encode()

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
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            payload = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        raise ChallengeRunnerError(f"Claude API call failed: HTTP {e.code}: {detail}") from e
    except urllib.error.URLError as e:
        raise ChallengeRunnerError(f"Claude API call failed: {e.reason}") from e

    text = "".join(
        block.get("text", "") for block in payload.get("content", []) if block.get("type") == "text"
    ).strip()
    if not text:
        raise ChallengeRunnerError("Claude API returned no text content")
    return text


def run_challenge(
    base_url: str,
    challenge: dict,
    contender_slug: str,
    variant_key: str,
    api_key: str,
    dry_run: bool,
) -> str:
    """Process one challenge. Returns an outcome tag for the summary tally."""
    slug = challenge["slug"]
    challenge_type = challenge.get("challengeType", "")

    if challenge_type not in HANDLED_TYPES:
        print(f"  ⏭  {slug}: challengeType {challenge_type} not handled by this runner yet, skipping", file=sys.stderr)
        return "skipped-type"

    if already_submitted(base_url, slug, contender_slug):
        print(f"  ⏭  {slug}: {contender_slug} already has a submission, skipping", file=sys.stderr)
        return "skipped-duplicate"

    if dry_run:
        print(f"  DRY RUN: would generate + submit an answer for {slug}", file=sys.stderr)
        return "dry-run"

    answer = generate_answer(challenge["promptText"], api_key)
    submission = cs.submit_challenge(
        base_url, cs.KR_API_TOKEN, slug, contender_slug, variant_key, answer, prompt_used=challenge["promptText"]
    )
    print(f"  ✅ {slug}: submission #{submission['id']} created for {contender_slug}")
    return "submitted"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--challenge", metavar="SLUG", help="only run this one challenge (fetched directly, regardless of status)")
    group.add_argument("--all", action="store_true", help="run every open challenge (default if neither flag is given)")
    parser.add_argument("--contender", default=cs.DEFAULT_CONTENDER, help=f"contender slug (default: {cs.DEFAULT_CONTENDER})")
    parser.add_argument("--variant-key", default=cs.DEFAULT_VARIANT_KEY, help=f"variant key (default: {cs.DEFAULT_VARIANT_KEY})")
    parser.add_argument("--kr-base-url", default=cs.KR_BASE_URL, help="override KR_BASE_URL")
    parser.add_argument("--dry-run", action="store_true", help="fetch + evaluate but skip the Claude call and submission")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    base_url = args.kr_base_url.rstrip("/")

    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not args.dry_run and not api_key:
        print("❌ ANTHROPIC_API_KEY is required (or pass --dry-run).", file=sys.stderr)
        return 1
    if not args.dry_run and not cs.KR_API_TOKEN:
        print("❌ KR_API_TOKEN is required (or pass --dry-run).", file=sys.stderr)
        return 1

    try:
        challenges = [cs.fetch_challenge(base_url, args.challenge)] if args.challenge else fetch_open_challenges(base_url)
    except (cs.ChallengeSubmitError, ChallengeRunnerError) as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1

    if not challenges:
        print("No open challenges found.")
        return 0

    print(f"Found {len(challenges)} challenge(s) to consider.", file=sys.stderr)

    tally = {"submitted": 0, "skipped-type": 0, "skipped-duplicate": 0, "dry-run": 0, "error": 0}
    for challenge in challenges:
        slug = challenge.get("slug", "?")
        try:
            outcome = run_challenge(base_url, challenge, args.contender, args.variant_key, api_key, args.dry_run)
            tally[outcome] += 1
        except (ChallengeRunnerError, cs.ChallengeSubmitError) as e:
            print(f"  ❌ {slug}: {e}", file=sys.stderr)
            tally["error"] += 1

    skipped = tally["skipped-type"] + tally["skipped-duplicate"]
    print(
        f"\nSummary: {len(challenges)} attempted | {tally['submitted']} submitted | "
        f"{skipped} skipped | {tally['dry-run']} dry-run | {tally['error']} errors"
    )
    return 1 if tally["error"] and not tally["submitted"] and not tally["dry-run"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
