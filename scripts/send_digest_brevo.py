#!/usr/bin/env python3
"""Send the prepared daily digest email through Brevo with bounded retries."""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any


BREVO_URL = "https://api.brevo.com/v3/smtp/email"
MAX_ATTEMPTS = 3
RETRY_DELAYS_SECONDS = (2.0, 5.0)
RETRYABLE_HTTP_CODES = {408, 425, 429, 500, 502, 503, 504}


def configure_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Attach the configured sender and recipient to a prepared email payload."""
    payload["sender"] = {
        "email": os.environ["DIGEST_FROM"],
        "name": os.environ.get("DIGEST_FROM_NAME") or "Conductor",
    }
    payload["to"] = [
        {
            "email": os.environ["DIGEST_TO"],
            "name": os.environ.get("DIGEST_TO_NAME") or "Silas",
        }
    ]
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
