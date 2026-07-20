#!/usr/bin/env python3
"""send_alert_brevo.py — one-off operational alert email via Brevo.

Reuses the same Brevo transactional-email path and secrets as the daily digest
(send_digest_brevo.py) so no new provider or secret is needed:

  BREVO_API_KEY              (required)
  ALERT_TO   or DIGEST_TO    (required — recipient)
  ALERT_FROM or DIGEST_FROM  (required — verified Brevo sender)
  ALERT_TO_NAME  / DIGEST_TO_NAME    (optional)
  ALERT_FROM_NAME/ DIGEST_FROM_NAME  (optional)

Unlike the digest sender this takes its subject/body inline, for short
"the render box is down" / "comfyui was hung, restarted it" notices.

Usage:
  python scripts/send_alert_brevo.py --subject "Render box down" --body "..."
  echo "long body" | python scripts/send_alert_brevo.py --subject "..." --body -
  python scripts/send_alert_brevo.py --subject x --body y --dry-run   # print, don't send
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

BREVO_URL = "https://api.brevo.com/v3/smtp/email"


def _env(*names, default=None):
    """First set env var among names, else default."""
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return default


def build_payload(subject, body):
    """Assemble the Brevo request payload from env + args. Raises on missing config."""
    api_key = os.environ.get("BREVO_API_KEY")
    to_email = _env("ALERT_TO", "DIGEST_TO")
    from_email = _env("ALERT_FROM", "DIGEST_FROM")

    missing = [
        name
        for name, value in (
            ("BREVO_API_KEY", api_key),
            ("ALERT_TO/DIGEST_TO", to_email),
            ("ALERT_FROM/DIGEST_FROM", from_email),
        )
        if not value
    ]
    if missing:
        raise SystemExit(
            "Missing alert email configuration: "
            + ", ".join(missing)
            + " (set them as env vars / GitHub Actions secrets)."
        )

    payload = {
        "subject": subject,
        "textContent": body,
        "sender": {
            "email": from_email,
            "name": _env("ALERT_FROM_NAME", "DIGEST_FROM_NAME", default="Conductor Ops"),
        },
        "to": [
            {
                "email": to_email,
                "name": _env("ALERT_TO_NAME", "DIGEST_TO_NAME", default="Silas"),
            }
        ],
    }
    return api_key, payload


def send_alert(subject, body, dry_run=False):
    """Send (or, when dry_run, print) the alert. Returns 0 on success."""
    api_key, payload = build_payload(subject, body)

    if dry_run:
        print(json.dumps(payload, indent=2))
        return 0

    request = urllib.request.Request(
        BREVO_URL,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
            "api" + "-key": api_key,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            print(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        print(f"Brevo alert failed with HTTP {error.code}: {detail}", file=sys.stderr)
        return 1
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        print(f"Brevo alert could not be sent: {error}", file=sys.stderr)
        return 1
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body", required=True, help="body text, or '-' to read stdin")
    parser.add_argument("--dry-run", action="store_true", help="print the payload without sending")
    args = parser.parse_args()

    body = sys.stdin.read() if args.body == "-" else args.body
    return send_alert(args.subject, body, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
