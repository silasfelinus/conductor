#!/usr/bin/env python3
"""Run one Challenge Center prompt across a matrix of registered contenders.

The matchup specification may be inline JSON or a JSON/YAML file::

    contenders:
      - contender: claude-fable
      - contender: claude-opus
      - contender: openai-gpt
        settings: {temperature: 1.0}
      - contender: conductor-claude
        variantKey: detailed
        promptSuffix: "Include concrete sensory detail."

Contender provider/model/generator defaults come from Kind Robots' ``/api/contenders``
endpoint. Per-entry settings override ``defaultSettings``. TEXT and REASONING entries
call Anthropic or OpenAI directly. ART entries call the Kind Robots generation surface;
local A1111/Comfy jobs are enqueued and polled until they have a real ``artImageId``.
Unavailable credentials or unsupported backends skip only that contender.

Usage:
    python scripts/challenge_matchup.py <challenge-slug> --spec matchup.yaml
    python scripts/challenge_matchup.py <challenge-slug> --spec '{"contenders": [...]}'
    python scripts/challenge_matchup.py <challenge-slug> --spec matchup.yaml --dry-run

Environment:
    KR_API_TOKEN       required for generation/submission
    KR_BASE_URL        default https://kindrobots.org
    KR_USER_ID         required only by the synchronous OpenAI Images KR endpoint
    ANTHROPIC_API_KEY  required by claude-api contenders
    OPENAI_API_KEY     required by openai-api text contenders
    CHALLENGE_MATCHUP_OPENAI_MODEL       fallback gpt-4o-mini
    CHALLENGE_MATCHUP_ANTHROPIC_MODEL    fallback claude-sonnet-5
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - repository CI installs PyYAML
    yaml = None

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts import challenge_submit as cs  # noqa: E402

ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_ANTHROPIC_MODEL = os.environ.get(
    "CHALLENGE_MATCHUP_ANTHROPIC_MODEL", "claude-sonnet-5"
).strip()
DEFAULT_OPENAI_MODEL = os.environ.get(
    "CHALLENGE_MATCHUP_OPENAI_MODEL", "gpt-4o-mini"
).strip()
TEXT_TYPES = {"TEXT", "REASONING"}
ART_GENERATORS = {
    # Historical contender name; Conductor's art lane is Comfy-only.
    "art-sd": "krea2",
    "comfy-flux": "flux",
    "comfy-sdxl": "comfy",
    "comfy-krea2": "krea2",
    "comfy-flux2": "flux2",
    # accept the bare engine names too, so a contender's generator can just be
    # the engine the /api/art/enqueue dispatcher expects
    "krea2": "krea2",
    "flux2": "flux2",
    "sdxl": "comfy",
    "flux": "flux",
}


class ChallengeMatchupError(Exception):
    pass


def as_mapping(value: Any, label: str) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ChallengeMatchupError(f"{label} must be a mapping")
    return dict(value)


def load_matchup_spec(source: str) -> dict[str, Any]:
    text: str
    candidate = Path(source)
    if candidate.is_file():
        text = candidate.read_text(encoding="utf-8")
        suffix = candidate.suffix.lower()
    else:
        text = source
        suffix = ".json"

    try:
        if suffix == ".json" or text.lstrip().startswith(("{", "[")):
            data = json.loads(text)
        else:
            if yaml is None:
                raise ChallengeMatchupError("PyYAML is required to load YAML matchup specs")
            data = yaml.safe_load(text)
    except (ValueError, OSError) as error:
        raise ChallengeMatchupError(f"could not parse matchup spec: {error}") from error

    if isinstance(data, list):
        data = {"contenders": data}
    if not isinstance(data, dict):
        raise ChallengeMatchupError("matchup spec must be a mapping or contender list")
    contenders = data.get("contenders")
    if not isinstance(contenders, list) or not contenders:
        raise ChallengeMatchupError("matchup spec requires a non-empty contenders list")
    for index, entry in enumerate(contenders, start=1):
        if not isinstance(entry, dict) or not str(entry.get("contender", "")).strip():
            raise ChallengeMatchupError(f"contenders[{index}] requires a contender slug")
    return data


def fetch_contenders(base_url: str) -> dict[str, dict[str, Any]]:
    status, body = cs.http_json("GET", f"{base_url}/api/contenders")
    if status != 200 or not body or not body.get("success"):
        message = (body or {}).get("message", f"HTTP {status}")
        raise ChallengeMatchupError(f"failed to fetch contenders: {message}")
    rows = body.get("data")
    if not isinstance(rows, list):
        raise ChallengeMatchupError("contender API returned malformed data")
    return {
        str(row["slug"]): row
        for row in rows
        if isinstance(row, dict) and isinstance(row.get("slug"), str)
    }


def merge_settings(defaults: Any, overrides: Any) -> dict[str, Any]:
    merged = as_mapping(defaults, "contender defaultSettings")
    merged.update(as_mapping(overrides, "entry settings"))
    return merged


def build_prompt(base_prompt: str, entry: dict[str, Any]) -> str:
    override = entry.get("prompt") or entry.get("promptOverride")
    prompt = str(override if override is not None else base_prompt).strip()
    prefix = str(entry.get("promptPrefix") or "").strip()
    suffix = str(entry.get("promptSuffix") or "").strip()
    pieces = [piece for piece in (prefix, prompt, suffix) if piece]
    if not pieces:
        raise ChallengeMatchupError("resolved prompt is empty")
    return "\n\n".join(pieces)


def request_json(
    url: str,
    body: dict[str, Any],
    headers: dict[str, str],
    timeout: int = 120,
) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as error:
        detail = error.read().decode(errors="replace")
        raise ChallengeMatchupError(f"backend call failed: HTTP {error.code}: {detail}") from error
    except urllib.error.URLError as error:
        raise ChallengeMatchupError(f"backend call failed: {error.reason}") from error
    if not isinstance(payload, dict):
        raise ChallengeMatchupError("backend returned malformed JSON")
    return payload


def generate_anthropic(
    prompt: str, contender: dict[str, Any], settings: dict[str, Any], api_key: str
) -> str:
    model = str(contender.get("model") or settings.get("model") or DEFAULT_ANTHROPIC_MODEL)
    body: dict[str, Any] = {
        "model": model,
        "max_tokens": int(settings.get("max_tokens", settings.get("maxTokens", 1024))),
        "messages": [{"role": "user", "content": prompt}],
    }
    if "temperature" in settings:
        body["temperature"] = float(settings["temperature"])
    system = settings.get("system")
    if system:
        body["system"] = str(system)
    payload = request_json(
        ANTHROPIC_URL,
        body,
        {"x-api-key": api_key, "anthropic-version": "2023-06-01"},
    )
    text = "".join(
        str(block.get("text", ""))
        for block in payload.get("content", [])
        if isinstance(block, dict) and block.get("type") == "text"
    ).strip()
    if not text:
        raise ChallengeMatchupError("Anthropic returned no text content")
    return text


def generate_openai(
    prompt: str, contender: dict[str, Any], settings: dict[str, Any], api_key: str
) -> str:
    model = str(contender.get("model") or settings.get("model") or DEFAULT_OPENAI_MODEL)
    body: dict[str, Any] = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }
    if "temperature" in settings:
        body["temperature"] = float(settings["temperature"])
    max_tokens = settings.get("max_tokens", settings.get("maxTokens"))
    if max_tokens is not None:
        body["max_tokens"] = int(max_tokens)
    payload = request_json(
        OPENAI_CHAT_URL,
        body,
        {"Authorization": f"Bearer {api_key}"},
    )
    try:
        text = payload["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, AttributeError, TypeError) as error:
        raise ChallengeMatchupError("OpenAI returned no text content") from error
    if not text:
        raise ChallengeMatchupError("OpenAI returned no text content")
    return text


def enqueue_art(
    base_url: str,
    token: str,
    prompt: str,
    generator: str,
    settings: dict[str, Any],
    poll_seconds: float,
    timeout_seconds: float,
) -> int:
    engine = ART_GENERATORS[generator]
    allowed = {
        "negativePrompt",
        "checkpoint",
        "sampler",
        "scheduler",
        "steps",
        "cfg",
        "cfgHalf",
        "guidance",
        "denoise",
        "seed",
        "width",
        "height",
        "variant",
        "serverId",
        "serverName",
        "priority",
        # new-engine knobs: optional style LoRA (krea2/flux2/comfy) and Flux.2's
        # structured JSON prompt
        "loraName",
        "loraStrength",
        "jsonPrompt",
    }
    payload = {
        "engine": engine,
        "promptString": prompt,
        "projectSlug": "challenge-center",
        "designer": "Challenge Center matchup runner",
        "isPublic": False,
        **{key: value for key, value in settings.items() if key in allowed},
    }
    status, body = cs.http_json(
        "POST", f"{base_url}/api/art/enqueue", token=token, body=payload, timeout=60
    )
    if status != 201 or not body or not body.get("success"):
        message = (body or {}).get("message", f"HTTP {status}")
        raise ChallengeMatchupError(f"failed to enqueue {generator} art: {message}")
    job_id = int(body["data"]["jobId"])
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        status, polled = cs.http_json(
            "GET", f"{base_url}/api/art/queue/{job_id}", token=token, timeout=30
        )
        if status != 200 or not polled or not polled.get("success"):
            message = (polled or {}).get("message", f"HTTP {status}")
            raise ChallengeMatchupError(f"failed to poll art job {job_id}: {message}")
        job = polled["data"]["job"]
        job_status = str(job.get("status", ""))
        if job_status == "DONE":
            art_image_id = job.get("artImageId")
            if not isinstance(art_image_id, int) or art_image_id <= 0:
                raise ChallengeMatchupError(f"art job {job_id} completed without artImageId")
            return art_image_id
        if job_status == "FAILED":
            raise ChallengeMatchupError(
                f"art job {job_id} failed: {job.get('error') or 'unknown error'}"
            )
        time.sleep(poll_seconds)
    raise ChallengeMatchupError(
        f"art job {job_id} did not complete within {timeout_seconds:g} seconds"
    )


def generate_openai_image(
    base_url: str,
    token: str,
    prompt: str,
    settings: dict[str, Any],
) -> int:
    user_id = settings.get("userId") or os.environ.get("KR_USER_ID")
    try:
        user_id = int(user_id)
    except (TypeError, ValueError) as error:
        raise ChallengeMatchupError(
            "KR_USER_ID (or settings.userId) is required for the OpenAI Images contender"
        ) from error
    allowed = {"model", "size", "quality", "background", "outputFormat", "serverId", "serverName"}
    payload = {
        "promptString": prompt,
        "userId": user_id,
        "designer": "Challenge Center matchup runner",
        "isPublic": False,
        **{key: value for key, value in settings.items() if key in allowed},
    }
    status, body = cs.http_json(
        "POST",
        f"{base_url}/api/chats/openai/images/generate",
        token=token,
        body=payload,
        timeout=180,
    )
    if status != 201 or not body or not body.get("success"):
        message = (body or {}).get("message", f"HTTP {status}")
        raise ChallengeMatchupError(f"OpenAI image generation failed: {message}")
    art_image_id = body.get("data", {}).get("id")
    if not isinstance(art_image_id, int) or art_image_id <= 0:
        raise ChallengeMatchupError("OpenAI image generation returned no ArtImage id")
    return art_image_id


def submit_entry(
    base_url: str,
    token: str,
    challenge_slug: str,
    contender_slug: str,
    variant_key: str,
    prompt_used: str,
    settings: dict[str, Any],
    random_selections: dict[str, Any],
    *,
    output_text: str | None = None,
    art_image_id: int | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "contenderSlug": contender_slug,
        "variantKey": variant_key,
        "promptUsed": prompt_used,
        "settings": settings,
        "randomSelections": random_selections,
    }
    if output_text is not None:
        payload["outputText"] = output_text
    if art_image_id is not None:
        payload["artImageId"] = art_image_id
    status, body = cs.http_json(
        "POST",
        f"{base_url}/api/challenges/{challenge_slug}/submissions",
        token=token,
        body=payload,
        timeout=60,
    )
    if status == 409:
        raise ChallengeMatchupError(
            f"duplicate submission: {(body or {}).get('message', 'variant already exists')}"
        )
    if status != 201 or not body or not body.get("success"):
        message = (body or {}).get("message", f"HTTP {status}")
        raise ChallengeMatchupError(f"submission failed: {message}")
    return body["data"]


def run_entry(
    base_url: str,
    token: str,
    challenge: dict[str, Any],
    contender: dict[str, Any],
    entry: dict[str, Any],
    *,
    anthropic_key: str,
    openai_key: str,
    dry_run: bool,
    poll_seconds: float,
    timeout_seconds: float,
) -> dict[str, Any]:
    slug = str(contender["slug"])
    generator = str(contender.get("generator") or "")
    challenge_type = str(challenge.get("challengeType") or "").upper()
    settings = merge_settings(contender.get("defaultSettings"), entry.get("settings"))
    random_selections = as_mapping(entry.get("randomSelections"), "randomSelections")
    prompt = build_prompt(str(challenge.get("promptText") or ""), entry)
    variant_key = str(entry.get("variantKey") or "default").strip()
    if not variant_key:
        raise ChallengeMatchupError("variantKey cannot be empty")

    result = {
        "contender": slug,
        "variant": variant_key,
        "generator": generator,
        "status": "planned" if dry_run else "submitted",
        "submissionId": None,
    }
    if dry_run:
        return result

    output_text: str | None = None
    art_image_id: int | None = None
    if challenge_type in TEXT_TYPES:
        if generator == "claude-api":
            if not anthropic_key:
                return {**result, "status": "skipped", "reason": "missing ANTHROPIC_API_KEY"}
            output_text = generate_anthropic(prompt, contender, settings, anthropic_key)
        elif generator == "openai-api":
            if not openai_key:
                return {**result, "status": "skipped", "reason": "missing OPENAI_API_KEY"}
            output_text = generate_openai(prompt, contender, settings, openai_key)
        else:
            return {**result, "status": "skipped", "reason": f"unsupported text backend {generator!r}"}
    elif challenge_type == "ART":
        if generator in ART_GENERATORS:
            art_image_id = enqueue_art(
                base_url,
                token,
                prompt,
                generator,
                settings,
                poll_seconds,
                timeout_seconds,
            )
        elif generator == "openai-images":
            art_image_id = generate_openai_image(base_url, token, prompt, settings)
        else:
            return {**result, "status": "skipped", "reason": f"unsupported art backend {generator!r}"}
    else:
        return {
            **result,
            "status": "skipped",
            "reason": f"challenge type {challenge_type or 'UNKNOWN'} is not supported",
        }

    submission = submit_entry(
        base_url,
        token,
        str(challenge["slug"]),
        slug,
        variant_key,
        prompt,
        settings,
        random_selections,
        output_text=output_text,
        art_image_id=art_image_id,
    )
    result["submissionId"] = submission.get("id")
    if art_image_id is not None:
        result["artImageId"] = art_image_id
    return result


def print_summary(results: list[dict[str, Any]]) -> None:
    headers = ("CONTENDER", "VARIANT", "GENERATOR", "STATUS", "SUBMISSION", "DETAIL")
    rows = []
    for result in results:
        rows.append(
            (
                str(result.get("contender", "")),
                str(result.get("variant", "")),
                str(result.get("generator", "")),
                str(result.get("status", "")),
                str(result.get("submissionId") or "-"),
                str(result.get("reason") or (f"ArtImage {result['artImageId']}" if result.get("artImageId") else "")),
            )
        )
    widths = [max(len(headers[i]), *(len(row[i]) for row in rows)) for i in range(len(headers))]
    print("  ".join(headers[i].ljust(widths[i]) for i in range(len(headers))))
    print("  ".join("-" * width for width in widths))
    for row in rows:
        print("  ".join(row[i].ljust(widths[i]) for i in range(len(row))))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug", help="challenge slug")
    parser.add_argument("--spec", required=True, help="inline JSON or path to JSON/YAML matchup spec")
    parser.add_argument("--kr-base-url", default=cs.KR_BASE_URL, help="override KR_BASE_URL")
    parser.add_argument("--dry-run", action="store_true", help="resolve and display entries without generation or submission")
    parser.add_argument("--poll-seconds", type=float, default=2.0, help="art job polling interval")
    parser.add_argument("--timeout-seconds", type=float, default=600.0, help="per-art-job timeout")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    base_url = args.kr_base_url.rstrip("/")
    token = os.environ.get("KR_API_TOKEN", cs.KR_API_TOKEN).strip()
    if not args.dry_run and not token:
        print("❌ KR_API_TOKEN is required (or pass --dry-run).", file=sys.stderr)
        return 1
    try:
        spec = load_matchup_spec(args.spec)
        challenge = cs.fetch_challenge(base_url, args.slug)
        contenders = fetch_contenders(base_url)
        results: list[dict[str, Any]] = []
        for entry in spec["contenders"]:
            slug = str(entry["contender"]).strip()
            contender = contenders.get(slug)
            if contender is None:
                results.append(
                    {"contender": slug, "variant": entry.get("variantKey", "default"), "generator": "", "status": "skipped", "reason": "contender not found"}
                )
                continue
            try:
                results.append(
                    run_entry(
                        base_url,
                        token,
                        challenge,
                        contender,
                        entry,
                        anthropic_key=os.environ.get("ANTHROPIC_API_KEY", "").strip(),
                        openai_key=os.environ.get("OPENAI_API_KEY", "").strip(),
                        dry_run=args.dry_run,
                        poll_seconds=max(args.poll_seconds, 0),
                        timeout_seconds=max(args.timeout_seconds, 1),
                    )
                )
            except ChallengeMatchupError as error:
                results.append(
                    {"contender": slug, "variant": entry.get("variantKey", "default"), "generator": contender.get("generator", ""), "status": "error", "reason": str(error)}
                )
        print_summary(results)
        submitted = sum(result["status"] == "submitted" for result in results)
        planned = sum(result["status"] == "planned" for result in results)
        skipped = sum(result["status"] == "skipped" for result in results)
        errors = sum(result["status"] == "error" for result in results)
        print(f"\nSummary: {len(results)} entries | {submitted} submitted | {planned} planned | {skipped} skipped | {errors} errors")
        return 1 if errors and not submitted and not planned else 0
    except (ChallengeMatchupError, cs.ChallengeSubmitError) as error:
        print(f"❌ {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
