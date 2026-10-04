#!/usr/bin/env python3
"""Send the prepared daily digest email through Brevo with bounded retries."""
from __future__ import annotations

import base64
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any


BREVO_URL = "https://api.brevo.com/v3/smtp/email"
DIRECT_LINKS_ATTACHMENT = "conductor-direct-links.html"
DIRECT_LINKS_NOTICE_MARKER = 'data-conductor-direct-links-backup="1"'
MAX_ATTEMPTS = 3
RETRY_DELAYS_SECONDS = (2.0, 5.0)
RETRYABLE_HTTP_CODES = {408, 425, 429, 500, 502, 503, 504}
HTTP_HREF_RE = re.compile(r"""href\s*=\s*["'](https?://[^"']+)["']""", re.IGNORECASE)


def _direct_http_links(payload: dict[str, Any]) -> list[str]:
    """Return unique direct HTTP(S) destinations from the prepared HTML."""
    source = str(payload.get("htmlContent") or "")
    seen: set[str] = set()
    links: list[str] = []
    for raw_href in HTTP_HREF_RE.findall(source):
        href = html.unescape(raw_href).strip()
        if href and href not in seen:
            seen.add(href)
            links.append(href)
    return links


def _direct_links_attachment_content(links: Sequence[str]) -> bytes:
    """Build a tiny standalone HTML backup whose hrefs Brevo cannot rewrite."""
    items = "".join(
        f'<li style="margin:0 0 12px"><a href="{html.escape(link, quote=True)}">'
        f'{html.escape(link)}</a></li>'
        for link in links
    )
    document = (
        "<!doctype html><html><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        "<title>Conductor direct links</title></head>"
        "<body style=\"font-family:system-ui,-apple-system,sans-serif;max-width:760px;"
        "margin:32px auto;padding:0 18px;color:#111827\">"
        "<h1>Conductor direct links</h1>"
        "<p>This file is attached before Brevo processes the message. If a button in the "
        "email was replaced by a Brevo tracking redirect, use the matching direct destination "
        "below instead.</p>"
        f"<ol>{items}</ol></body></html>"
    )
    return document.encode("utf-8")


def attach_direct_links_backup(payload: dict[str, Any]) -> dict[str, Any]:
    """Attach an unmodified direct-link page so provider rewriting cannot strand the digest."""
    links = _direct_http_links(payload)
    if not links:
        return payload

    attachments = payload.setdefault("attachment", [])
    if not any(
        isinstance(item, dict) and item.get("name") == DIRECT_LINKS_ATTACHMENT
        for item in attachments
    ):
        encoded = base64.b64encode(_direct_links_attachment_content(links)).decode("ascii")
        attachments.append({"name": DIRECT_LINKS_ATTACHMENT, "content": encoded})

    html_content = str(payload.get("htmlContent") or "")
    if DIRECT_LINKS_NOTICE_MARKER not in html_content:
        notice = (
            f'<p {DIRECT_LINKS_NOTICE_MARKER} style="max-width:660px;padding:9px 12px;'
            'border-left:4px solid #7e22ce;background:#faf5ff;color:#581c87;font-size:12px">'
            '<strong>Direct-link backup attached.</strong> If Brevo rewrites a button into a '
            f'broken tracking URL, open <code>{DIRECT_LINKS_ATTACHMENT}</code> for the original '
            'destinations.</p>'
        )
        payload["htmlContent"] = notice + html_content

    return payload


def configure_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Attach sender, recipient, and a provider-independent direct-link backup."""
    payload["sender"] = {
        "email": os.environ["DIGEST_FROM"],
        "name": os.environ.get("DIGEST_FROM_NAME") or "Conductor",
    }
    payload["to"] = [
        {
            "email": os.environ["DIGEST_TO"],
            "name": os.environ.get("DIGEST_TO_NAME") or "Silas",
            # Brevo only honors this field when the account-level per-contact
            # tracking-consent feature is enabled. Keep it as the desired
            # privacy policy, but never treat it as a delivery guarantee.
            "contactPixelTrackingConsent": False,
        }
    ]

    # 2026-10-04 delivered-message evidence proved that putting
    # X-Mailin-Track-Click/Open in the API payload merely copied those headers
    # into the final MIME message while Brevo still rewrote every href through
    # sendibt2.com. Do not reintroduce that false guarantee. The attachment is
    # base64 message data, so its original URLs survive provider link rewriting.
    attach_direct_links_backup(payload)
    return payload


def ensure_idempotency_key(payload: dict[str, Any]) -> str:
    """Add one stable Brevo idempotency key for every retry of this payload."""
    headers = payload.setdefault("headers", {})
    existing = headers.get("Idempotency-Key")
    if existing:
        return str(existing)

    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:32]
    key = f"conductor-digest-{digest}"
    headers["Idempotency-Key"] = key
    return key


def _is_duplicate_idempotency_response(body: str) -> bool:
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError:
        return False

    code = str(parsed.get("code") or "").lower()
    message = str(parsed.get("message") or "").lower()
    return code == "duplicate_parameter" and "idempot" in message


def _retry_delay(
    error: urllib.error.HTTPError | None,
    attempt: int,
    retry_delays: Sequence[float],
) -> float:
    if error is not None and error.headers is not None:
        retry_after = error.headers.get("Retry-After")
        if retry_after:
            try:
                return max(0.0, min(float(retry_after), 60.0))
            except ValueError:
                pass

    index = min(attempt - 1, len(retry_delays) - 1)
    return retry_delays[index] if retry_delays else 0.0


def send_payload(
    payload: dict[str, Any],
    api_key: str,
    *,
    max_attempts: int = MAX_ATTEMPTS,
    retry_delays: Sequence[float] = RETRY_DELAYS_SECONDS,
    timeout: float = 30.0,
    urlopen: Callable[..., Any] | None = None,
    sleep: Callable[[float], None] | None = None,
) -> int:
    """Send one payload, retrying only transient failures with duplicate protection."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    opener = urlopen or urllib.request.urlopen
    sleeper = sleep or time.sleep
    idempotency_key = ensure_idempotency_key(payload)
    request_body = json.dumps(payload).encode("utf-8")
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "api-key": api_key,
    }

    for attempt in range(1, max_attempts + 1):
        request = urllib.request.Request(
            BREVO_URL,
            data=request_body,
            method="POST",
            headers=headers,
        )

        try:
            with opener(request, timeout=timeout) as response:
                print(response.read().decode("utf-8"))
                return 0
        except urllib.error.HTTPError as error:
            error_body = error.read().decode("utf-8", errors="replace")
            if _is_duplicate_idempotency_response(error_body):
                print(
                    "Brevo confirmed this idempotency key was already accepted; "
                    "treating the digest as sent."
                )
                return 0

            retryable = error.code in RETRYABLE_HTTP_CODES or 500 <= error.code <= 599
            if not retryable or attempt >= max_attempts:
                print(
                    f"Brevo email request failed with HTTP {error.code}: {error_body}",
                    file=sys.stderr,
                )
                return 1

            delay = _retry_delay(error, attempt, retry_delays)
            print(
                f"Brevo transient HTTP {error.code} on attempt {attempt}/{max_attempts}; "
                f"retrying in {delay:g}s with idempotency key {idempotency_key}.",
                file=sys.stderr,
            )
            sleeper(delay)
        except (urllib.error.URLError, TimeoutError) as error:
            if attempt >= max_attempts:
                print(
                    f"Brevo email request failed after {attempt} attempts: {error}",
                    file=sys.stderr,
                )
                return 1

            delay = _retry_delay(None, attempt, retry_delays)
            print(
                f"Brevo network failure on attempt {attempt}/{max_attempts}: {error}; "
                f"retrying in {delay:g}s with idempotency key {idempotency_key}.",
                file=sys.stderr,
            )
            sleeper(delay)

    return 1


def main() -> int:
    payload_path = Path(sys.argv[1] if len(sys.argv) > 1 else "digest-email.json")
    required = ["BREVO_API_KEY", "DIGEST_TO", "DIGEST_FROM"]
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        print("Missing required digest configuration: " + ", ".join(missing), file=sys.stderr)
        print("Add these as GitHub Actions repository secrets before running daily-digest.", file=sys.stderr)
        return 1

    with payload_path.open(encoding="utf-8") as payload_file:
        payload = json.load(payload_file)

    configure_payload(payload)
    return send_payload(payload, os.environ["BREVO_API_KEY"])


if __name__ == "__main__":
    raise SystemExit(main())
