#!/usr/bin/env python3
"""Send a prepared digest payload over SMTP so its links arrive unmodified.

Brevo rewrites every href in transactional mail through its sendibt*.com click
tracker, and turning that off is not self-serve (support/Enterprise only). Four
sender-side attempts to stop it failed (conductor#5411, #5544, #5567 and the
direct-send artifact), and the only days Silas got direct links were days an
outside agent resent the digest through Gmail by hand. This is that Gmail send,
done deterministically by the workflow itself: plain SMTP relays the HTML
byte-for-byte, so the Kind Robots URLs the builder wrote are the URLs he clicks.

Configured by DIGEST_SMTP_USER and DIGEST_SMTP_PASSWORD (a Gmail app password).
When they are unset, send_digest_brevo.py keeps sending through Brevo exactly
as before.
"""
from __future__ import annotations

import base64
import mimetypes
import os
import smtplib
import sys
import time
from collections.abc import Callable
from email.message import EmailMessage
from email.utils import formataddr, make_msgid
from typing import Any


DEFAULT_SMTP_HOST = "smtp.gmail.com"
DEFAULT_SMTP_PORT = 465
MAX_ATTEMPTS = 2
RETRY_DELAY_SECONDS = 5.0
# The Brevo-only backup attachment exists because Brevo rewrites links; over
# SMTP the links are already direct, so the backup would only be clutter.
BREVO_ONLY_ATTACHMENTS = {"conductor-direct-links.html"}


def is_configured() -> bool:
    return bool(os.environ.get("DIGEST_SMTP_USER") and os.environ.get("DIGEST_SMTP_PASSWORD"))


def build_message(payload: dict[str, Any]) -> EmailMessage:
    """Build the MIME message from the Brevo-shaped payload the builders write."""
    user = os.environ["DIGEST_SMTP_USER"]
    from_address = os.environ.get("DIGEST_SMTP_FROM") or user
    from_name = os.environ.get("DIGEST_FROM_NAME") or "Conductor"
    to_address = os.environ["DIGEST_TO"]
    to_name = os.environ.get("DIGEST_TO_NAME") or "Silas"

    message = EmailMessage()
    message["Subject"] = str(payload.get("subject") or "Conductor digest")
    message["From"] = formataddr((from_name, from_address))
    message["To"] = formataddr((to_name, to_address))
    message["Message-ID"] = make_msgid(domain=from_address.rpartition("@")[2] or None)

    html_content = str(payload.get("htmlContent") or "")
    text_content = str(payload.get("textContent") or "")
    if text_content:
        message.set_content(text_content)
        if html_content:
            message.add_alternative(html_content, subtype="html")
    else:
        message.set_content(html_content, subtype="html")

    for item in payload.get("attachment") or []:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or "")
        content = item.get("content")
        if not name or not content or name in BREVO_ONLY_ATTACHMENTS:
            continue
        maintype, _, subtype = _guess_type(name).partition("/")
        message.add_attachment(
            base64.b64decode(content),
            maintype=maintype,
            subtype=subtype,
            filename=name,
        )
    return message


def _guess_type(name: str) -> str:
    guessed, _ = mimetypes.guess_type(name)
    return guessed or "application/octet-stream"


def send_payload(
    payload: dict[str, Any],
    *,
    max_attempts: int = MAX_ATTEMPTS,
    smtp_factory: Callable[..., Any] | None = None,
    sleep: Callable[[float], None] | None = None,
) -> int:
    """Send once over SMTP, retrying a dropped connection; 0 on success, 1 on failure."""
    host = os.environ.get("DIGEST_SMTP_HOST") or DEFAULT_SMTP_HOST
    port = int(os.environ.get("DIGEST_SMTP_PORT") or DEFAULT_SMTP_PORT)
    user = os.environ["DIGEST_SMTP_USER"]
    password = os.environ["DIGEST_SMTP_PASSWORD"]
    factory = smtp_factory or smtplib.SMTP_SSL
    sleeper = sleep or time.sleep
    message = build_message(payload)

    for attempt in range(1, max_attempts + 1):
        try:
            with factory(host, port, timeout=30) as smtp:
                smtp.login(user, password)
                smtp.send_message(message)
            print(f"Digest sent over SMTP via {host} to {message['To']}.")
            return 0
        except smtplib.SMTPAuthenticationError as error:
            # Retrying a rejected app password only risks locking the account.
            print(f"SMTP login to {host} was rejected: {error.smtp_code}", file=sys.stderr)
            return 1
        except (smtplib.SMTPException, OSError) as error:
            if attempt >= max_attempts:
                print(f"SMTP send via {host} failed after {attempt} attempts: {error}", file=sys.stderr)
                return 1
            print(
                f"SMTP send via {host} failed on attempt {attempt}/{max_attempts}: {error}; "
                f"retrying in {RETRY_DELAY_SECONDS:g}s.",
                file=sys.stderr,
            )
            sleeper(RETRY_DELAY_SECONDS)
    return 1
