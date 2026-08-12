#!/usr/bin/env python3
"""
challenge_submit.py — bridge between conductor agent runs and the Challenge Center
(silasfelinus/kind_robots' /api/challenges surface).

Two-step CLI flow:

  1. Fetch a challenge's prompt and print it (nothing else on stdout, so it pipes
     cleanly to an agent):

       python scripts/challenge_submit.py <challenge-slug> > prompt.txt

  2. Once the agent has produced its answer, submit it as this contender's entry
     and see where it lands on the leaderboard:

       python scripts/challenge_submit.py <challenge-slug> --output answer.txt
       agent-run < prompt.txt | python scripts/challenge_submit.py <challenge-slug> --output -

Without --output, the script only fetches the challenge and prints promptText —
it makes no submission. With --output, it POSTs a ChallengeSubmission for
--contender (default conductor-claude) and prints the created submission id plus
this contender's current leaderboard standing.

Env:
  KR_API_TOKEN   required for --output (Bearer token: Server.apiKey or admin JWT)
  KR_BASE_URL    default https://kindrobots.org

Usage:
  python scripts/challenge_submit.py <challenge-slug> [--contender conductor-claude]
      [--variant-key default] [--output <file>|-] [--prompt-used TEXT] [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kindrobots.org").rstrip("/")
KR_API_TOKEN = os.environ.get("KR_API_TOKEN", "").strip()

DEFAULT_CONTENDER = "conductor-claude"
DEFAULT_VARIANT_KEY = "default"


class ChallengeSubmitError(Exception):
    pass


def http_json(method: str, url: str, token: str = "", body: dict | None = None, timeout: int = 30):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode() or "null")
    except urllib.error.HTTPError as e:
        try:
            payload = json.loads(e.read().decode() or "null")
        except (ValueError, OSError):
            payload = None
        return e.code, payload
    except urllib.error.URLError as e:
        raise ChallengeSubmitError(f"could not reach {url}: {e.reason}") from e


def fetch_challenge(base_url: str, slug: str) -> dict:
    status, body = http_json("GET", f"{base_url}/api/challenges/{slug}")
    if status == 404:
        raise ChallengeSubmitError(f"challenge {slug!r} not found")
    if status != 200 or not body or not body.get("success"):
        message = (body or {}).get("message", f"HTTP {status}")
        raise ChallengeSubmitError(f"failed to fetch challenge {slug!r}: {message}")
    return body["data"]


def submit_challenge(
    base_url: str,
    token: str,
    slug: str,
    contender_slug: str,
    variant_key: str,
    output_text: str,
    prompt_used: str | None = None,
) -> dict:
    if not token:
        raise ChallengeSubmitError("KR_API_TOKEN is required to submit a challenge entry")

    payload = {
        "contenderSlug": contender_slug,
        "variantKey": variant_key,
        "outputText": output_text,
    }
    if prompt_used:
        payload["promptUsed"] = prompt_used

    status, body = http_json(
        "POST", f"{base_url}/api/challenges/{slug}/submissions", token=token, body=payload
    )
    if status == 409:
        message = (body or {}).get("message", "duplicate submission")
        raise ChallengeSubmitError(f"submission rejected: {message}")
    if status != 201 or not body or not body.get("success"):
        message = (body or {}).get("message", f"HTTP {status}")
        raise ChallengeSubmitError(f"failed to submit to challenge {slug!r}: {message}")
    return body["data"]


def fetch_leaderboard(base_url: str, slug: str) -> list[dict]:
    status, body = http_json("GET", f"{base_url}/api/challenges/{slug}/leaderboard")
    if status != 200 or not body or not body.get("success"):
        message = (body or {}).get("message", f"HTTP {status}")
        raise ChallengeSubmitError(f"failed to fetch leaderboard for {slug!r}: {message}")
    return body["data"]["leaderboard"]


def find_standing(leaderboard: list[dict], contender_slug: str) -> tuple[int, dict] | None:
    for rank, entry in enumerate(leaderboard, start=1):
        if entry.get("slug") == contender_slug:
            return rank, entry
    return None


def read_output(path: str) -> str:
    if path == "-":
        text = sys.stdin.read()
    else:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    text = text.strip()
    if not text:
        raise ChallengeSubmitError(f"no output text read from {path!r}")
    return text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug", help="challenge slug")
    parser.add_argument("--contender", default=DEFAULT_CONTENDER, help=f"contender slug (default: {DEFAULT_CONTENDER})")
    parser.add_argument("--variant-key", default=DEFAULT_VARIANT_KEY, help=f"variant key (default: {DEFAULT_VARIANT_KEY})")
    parser.add_argument("--output", metavar="FILE", help="file containing the agent's output, or '-' for stdin. Omit to only fetch and print the prompt.")
    parser.add_argument("--prompt-used", metavar="TEXT", help="override promptUsed sent with the submission (defaults to the challenge's promptText)")
    parser.add_argument("--kr-base-url", default=KR_BASE_URL, help="override KR_BASE_URL")
    parser.add_argument("--dry-run", action="store_true", help="do everything except the POST; print what would be submitted")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    base_url = args.kr_base_url.rstrip("/")

    try:
        challenge = fetch_challenge(base_url, args.slug)

        if args.output is None:
            print(f"# {challenge.get('title', args.slug)} ({challenge.get('challengeType', 'UNKNOWN')})", file=sys.stderr)
            print(challenge["promptText"])
            return 0

        output_text = read_output(args.output)
        prompt_used = args.prompt_used or challenge.get("promptText")

        if args.dry_run:
            print(
                f"DRY RUN: would submit {len(output_text)} chars as {args.contender} "
                f"(variant={args.variant_key!r}) to {args.slug!r}",
                file=sys.stderr,
            )
            return 0

        submission = submit_challenge(
            base_url,
            KR_API_TOKEN,
            args.slug,
            args.contender,
            args.variant_key,
            output_text,
            prompt_used=prompt_used,
        )
        print(f"Submission #{submission['id']} created for {args.contender} on {args.slug!r} (variant {args.variant_key!r}).")

        leaderboard = fetch_leaderboard(base_url, args.slug)
        standing = find_standing(leaderboard, args.contender)
        if standing is None:
            print("Leaderboard standing: not yet ranked.")
        else:
            rank, entry = standing
            score = entry.get("score", {})
            print(
                f"Leaderboard standing: #{rank} of {len(leaderboard)} "
                f"— net score {score.get('netScore', 0)} ({score.get('votes', 0)} votes)."
            )
        return 0
    except ChallengeSubmitError as error:
        print(f"❌ {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
