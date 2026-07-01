#!/usr/bin/env python3
"""
request_art.py — Conductor art request wrapper for kind_robots

Wraps POST /api/conductor/art-request (fire-and-forget queue).
This is the preferred conductor-to-kind_robots path because conductor
holds KR_API_TOKEN (admin API key), not a user JWT or user apiKey.

Endpoint contract (from docs/art-api.md):
  POST /api/conductor/art-request
  Auth: X-KR-API-Token: <KR_API_TOKEN>
  Body: { src, pageUrl?, alt?, label?, variant?, prompt? }
  Response: { success, message, entry: { src, label, variant, prompt } }

Usage examples:

  # Dry-run (default) — print payload, do not send:
  python scripts/request_art.py \\
    --prompt "A glowing robot with a paintbrush, clean icon style" \\
    --project-slug pinball-hero \\
    --variant icon \\
    --width 512 --height 512

  # Live mode — send the request (requires KR_API_TOKEN in env):
  python scripts/request_art.py \\
    --prompt "A glowing robot with a paintbrush, clean icon style" \\
    --project-slug pinball-hero \\
    --variant icon \\
    --no-dry-run

  # Write response JSON to a file:
  python scripts/request_art.py \\
    --prompt "..." --project-slug pinball-hero \\
    --no-dry-run --output-json /tmp/art-response.json

Environment variables:
  KR_API_TOKEN   Admin API key for kind_robots (required in live mode)
  KR_BASE_URL    Base URL for kind_robots API (default: https://www.kindrobots.org)
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_BASE_URL = "https://www.kindrobots.org"
ENDPOINT_PATH = "/api/conductor/art-request"

# Conductor-owned image root — images for projects live here relative to
# the kind_robots CDN or static-file server.
PROJECT_IMAGE_ROOT = "projects/images"


# ---------------------------------------------------------------------------
# Payload builder
# ---------------------------------------------------------------------------


def build_payload(
    prompt: str,
    project_slug: str | None,
    width: int | None,
    height: int | None,
    variant: str | None,
    label: str | None,
    alt: str | None,
    page_url: str | None,
    src: str | None,
) -> dict:
    """
    Build the JSON payload for POST /api/conductor/art-request.

    The endpoint expects at minimum a `src` field (target image path).
    When --project-slug is given, derive `src` from the slug and variant.
    The caller may also pass --src directly to override.
    """
    # Derive src from project slug + variant when not explicitly given.
    if src is None and project_slug:
        variant_suffix = variant or "icon"
        slug_lower = project_slug.lower().replace(" ", "-")
        filename = f"{slug_lower}-{variant_suffix}.webp"
        src = f"{PROJECT_IMAGE_ROOT}/{filename}"

    if src is None:
        # Fallback: use a generic placeholder so the payload is always valid.
        src = f"{PROJECT_IMAGE_ROOT}/unknown-image.webp"

    payload: dict = {"src": src}

    if prompt:
        payload["prompt"] = prompt

    if project_slug:
        # Use project slug as the label if no explicit label was given.
        payload["label"] = label or project_slug

    if alt:
        payload["alt"] = alt

    if variant:
        payload["variant"] = variant

    if page_url:
        payload["pageUrl"] = page_url
    elif project_slug:
        # Derive a sensible pageUrl from the slug.
        payload["pageUrl"] = f"/{project_slug.lower().replace(' ', '-')}"

    # Width/height are not part of the /api/conductor/art-request contract
    # (that endpoint queues, not generates), but we embed them in the prompt
    # annotation so the human reviewer has the size intent.
    if width and height and "prompt" in payload:
        payload["_dimensions_hint"] = f"{width}x{height}"
    elif width and height:
        payload["_dimensions_hint"] = f"{width}x{height}"

    return payload


# ---------------------------------------------------------------------------
# HTTP sender
# ---------------------------------------------------------------------------


def send_request(payload: dict, base_url: str, api_token: str) -> dict:
    """
    POST payload to /api/conductor/art-request.
    Returns the parsed JSON response dict.
    Raises SystemExit on network or HTTP error.
    """
    url = base_url.rstrip("/") + ENDPOINT_PATH
    body = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-KR-API-Token": api_token,
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8") if exc.fp else ""
        print(f"[request_art] HTTP error {exc.code}: {raw}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as exc:
        print(f"[request_art] Network error: {exc.reason}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"[request_art] Could not parse response JSON: {exc}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="request_art.py",
        description=(
            "Conductor wrapper for POST /api/conductor/art-request.\n"
            "Defaults to dry-run mode — prints payload without sending."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Core content args
    parser.add_argument(
        "--prompt",
        required=True,
        metavar="TEXT",
        help="Image generation prompt.",
    )
    parser.add_argument(
        "--project-slug",
        metavar="SLUG",
        default=None,
        help=(
            "Project slug (e.g. 'pinball-hero'). Used to derive src path and "
            "pageUrl when not given explicitly."
        ),
    )

    # Dimension args (stored as hints — not in the queue endpoint contract)
    parser.add_argument("--width", type=int, default=None, metavar="W", help="Intended width in pixels.")
    parser.add_argument("--height", type=int, default=None, metavar="H", help="Intended height in pixels.")

    # Optional metadata
    parser.add_argument(
        "--variant",
        choices=["icon", "card", "hero"],
        default=None,
        metavar="VARIANT",
        help="Image variant: icon | card | hero.",
    )
    parser.add_argument("--label", default=None, metavar="LABEL", help="Human-readable label for this image.")
    parser.add_argument("--alt", default=None, metavar="ALT", help="Alt text for the image.")
    parser.add_argument("--page-url", default=None, metavar="URL", help="Page URL where the image is used.")
    parser.add_argument(
        "--src",
        default=None,
        metavar="PATH",
        help="Override the derived src image path.",
    )

    # Mode control
    dry_run_group = parser.add_mutually_exclusive_group()
    dry_run_group.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        default=True,
        help="Print payload without sending (default).",
    )
    dry_run_group.add_argument(
        "--no-dry-run",
        dest="dry_run",
        action="store_false",
        help="Send the actual request (requires KR_API_TOKEN in env).",
    )

    # Output
    parser.add_argument(
        "--output-json",
        metavar="PATH",
        default=None,
        help="Write response JSON to this file path (live mode only).",
    )
    parser.add_argument(
        "--base-url",
        metavar="URL",
        default=None,
        help=f"Override kind_robots base URL (default: env KR_BASE_URL or {DEFAULT_BASE_URL}).",
    )

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    # Resolve base URL: explicit arg > env > default
    base_url = args.base_url or os.environ.get("KR_BASE_URL", DEFAULT_BASE_URL)

    # Build the payload regardless of mode.
    payload = build_payload(
        prompt=args.prompt,
        project_slug=args.project_slug,
        width=args.width,
        height=args.height,
        variant=args.variant,
        label=args.label,
        alt=args.alt,
        page_url=args.page_url,
        src=args.src,
    )

    if args.dry_run:
        print("[request_art] DRY-RUN — payload (not sent):")
        print(json.dumps(payload, indent=2))
        print(f"\n[request_art] Would POST to: {base_url.rstrip('/')}{ENDPOINT_PATH}")
        print("[request_art] Auth header: X-KR-API-Token: <KR_API_TOKEN from env>")
        return 0

    # --- Live mode ---

    api_token = os.environ.get("KR_API_TOKEN", "")
    if not api_token:
        print(
            "[request_art] ERROR: KR_API_TOKEN is not set in the environment.\n"
            "Export it before running in live mode:\n"
            "  export KR_API_TOKEN=<your-admin-token>",
            file=sys.stderr,
        )
        return 1

    print(f"[request_art] Sending request to {base_url.rstrip('/')}{ENDPOINT_PATH} ...")
    response = send_request(payload, base_url, api_token)
    response_json = json.dumps(response, indent=2)

    print("[request_art] Response:")
    print(response_json)

    if args.output_json:
        out_path = Path(args.output_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(response_json + "\n", encoding="utf-8")
        print(f"[request_art] Response written to: {out_path}")

    if not response.get("success"):
        print("[request_art] WARNING: Response indicates failure (success=false).", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
