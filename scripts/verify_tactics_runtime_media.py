#!/usr/bin/env python3
"""Prove that Tactics' private ArtImage receipts work through the *game* URL.

The original media-checking job checks authenticated source files. This adds an
independent check for the route used by the actual Vue ArtImage store:
GET /api/art/images/<id>/file. It compares decoded media to its recorded
source, validates expected anonymous access, and never exposes image bytes,
media URLs, headers or token strings in logs. Read-only: never submits ArtJobs.
"""

from __future__ import annotations

import argparse
import io
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

if __package__:
    from .verify_prom_tactics_media import candidates
else:
    from verify_prom_tactics_media import candidates


RETRYABLE_HTTP_CODES = frozenset({429, 500, 502, 503, 504})


class TransientMediaError(RuntimeError):
    """A retryable server response, without recording private URL details."""


class SameOriginRedirect(urllib.request.HTTPRedirectHandler):
    """Reject redirects that might forward the production bearer credential."""

    def redirect_request(self, request, fp, code, msg, headers, newurl):
        original = urllib.parse.urlsplit(request.full_url)
        target = urllib.parse.urlsplit(newurl)
        if (
            target.scheme != original.scheme
            or target.netloc.lower() != original.netloc.lower()
            or target.scheme != "https"
        ):
            raise ValueError("Cross-origin or insecure media redirect rejected")
        return super().redirect_request(request, fp, code, msg, headers, newurl)


def make_opener():
    return urllib.request.build_opener(SameOriginRedirect)


def runtime_url(base_url: str, image_id: int) -> str:
    url = urllib.parse.urlsplit(base_url)
    if url.scheme != "https" or not url.netloc or url.username or url.password:
        raise ValueError("Runtime media base URL must be trusted HTTPS origin")
    return f"{url.scheme}://{url.netloc}/api/art/images/{image_id}/file"


def read_game_image(image_id: int, base_url: str, token: str, opener=None):
    if not token:
        raise ValueError("Missing production API credential")
    request = urllib.request.Request(
        runtime_url(base_url, image_id),
        headers={"Authorization": f"Bearer {token}"},
    )
    client = opener or make_opener()
    with client.open(request, timeout=120) as response:
        content_type = response.headers.get("content-type", "").lower()
        if not content_type.startswith("image/"):
            raise ValueError("Gameplay route did not return image media")
        image = Image.open(io.BytesIO(response.read()))
        image.load()
        return image.convert("RGB")


def check_visibility(image_id: int, base_url: str, public: bool, opener=None):
    """A private image must not be readable through the game URL anonymously."""
    client = opener or make_opener()
    request = urllib.request.Request(runtime_url(base_url, image_id))
    try:
        with client.open(request, timeout=30) as response:
            if not public:
                raise PermissionError("Private art visible to anonymous caller")
            if not response.headers.get("content-type", "").lower().startswith(
                "image/"
            ):
                raise ValueError("Public art returned non-image media")
            return "PUBLIC_OK"
    except urllib.error.HTTPError as error:
        if not public and error.code in (403, 404):
            return "PRIVATE_DENIED"
        if error.code in RETRYABLE_HTTP_CODES:
            raise
        raise ValueError("Unexpected anonymous gameplay media status") from None


def average_thumbnail_delta(a: Image.Image, b: Image.Image) -> float:
    """Permit WebP transcoding while catching broken/stale/wrong ArtImage media."""
    if a.size != b.size:
        raise ValueError("Source and gameplay image dimensions differ")
    size = (64, 64)
    first = a.convert("RGB").resize(size, Image.Resampling.LANCZOS)
    second = b.convert("RGB").resize(size, Image.Resampling.LANCZOS)
    differences = ImageChops.difference(first, second)
    return sum(ImageStat.Stat(differences).mean) / 3


def retry_transient(action, *, pause=time.sleep, attempts=4):
    """Retry transient media/API failures, never bad pixels, privacy, or 4xx IDs.

    The source loader reports non-200 metadata as RuntimeError("HTTP NNN"),
    while the browser URL and anonymous check raise HTTPError directly.
    Bounded exponential backoff avoids re-submitting an ArtJob or mistaking
    production throttling for lost artwork. Callers print exception *types*
    only, never URLs, headers or response bodies.
    """
    for index in range(attempts):
        try:
            return action()
        except Exception as error:
            if isinstance(error, urllib.error.HTTPError):
                transient = error.code in RETRYABLE_HTTP_CODES
            elif isinstance(error, (urllib.error.URLError, TimeoutError, ConnectionError)):
                transient = True
            elif isinstance(error, TransientMediaError):
                transient = True
            elif isinstance(error, RuntimeError):
                transient = bool(
                    re.search(r"\bHTTP (?:429|500|502|503|504)\b", str(error))
                )
            else:
                transient = False
            if not transient or index == attempts - 1:
                raise
            pause(2 ** (index + 1))
    raise AssertionError("unreachable retry loop")


def verify(
    entries,
    read_reference,
    read_runtime,
    visibility,
    fetch_public,
    *,
    retry=retry_transient,
    pace_seconds=0,
    pause=time.sleep,
):
    passed, failed = [], []
    for entry in entries:
        try:
            image_id = entry["image_id"]
            source = retry(lambda: read_reference(image_id))
            runtime = retry(lambda: read_runtime(image_id))
            delta = average_thumbnail_delta(source, runtime)
            if delta > 18:
                raise ValueError("Gameplay image differs from its source")
            public = retry(lambda: fetch_public(image_id))
            if type(public) is not bool:
                raise ValueError("ArtImage visibility metadata missing")
            status = retry(lambda: visibility(image_id, public))
            if status != ("PUBLIC_OK" if public else "PRIVATE_DENIED"):
                raise PermissionError("Unexpected anonymous media access")
            passed.append(
                (entry["key"], entry["job_id"], image_id, runtime.size, status)
            )
        except Exception as exc:
            # Do not log str(exc): HTTP and network errors can contain signed
            # image paths, private URLs and authorization headers.
            failed.append((entry["key"], entry["image_id"], type(exc).__name__))
        finally:
            if pace_seconds > 0:
                pause(pace_seconds)
    return passed, failed


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--require-count", type=int, default=12)
    parser.add_argument("--pace-seconds", type=float, default=0.25)
    args = parser.parse_args(argv)
    entries = candidates([args.ledger])
    if len(entries) != args.require_count:
        print(
            f"RECEIPT_COUNT_MISMATCH actual={len(entries)} "
            f"expected={args.require_count}"
        )
        return 1

    import consume_art_queue_core as core
    from export_shifting_lands_cards import load_image

    if not core.KR_API_TOKEN:
        print("ERROR Missing private API credential")
        return 1

    def fetch_public(image_id):
        status, payload = core.http_json(
            "GET", f"{core.KR_BASE_URL}/api/art/image/{image_id}"
        )
        if status in RETRYABLE_HTTP_CODES:
            raise TransientMediaError("Transient ArtImage metadata response")
        if status != 200:
            raise ValueError("ArtImage metadata cannot be fetched")
        return ((payload or {}).get("data") or {}).get("isPublic")

    passed, failed = verify(
        entries,
        read_reference=load_image,
        read_runtime=lambda image_id: read_game_image(
            image_id, core.KR_BASE_URL, core.KR_API_TOKEN
        ),
        visibility=lambda image_id, public: check_visibility(
            image_id, core.KR_BASE_URL, public
        ),
        fetch_public=fetch_public,
        pace_seconds=max(0.0, args.pace_seconds),
    )
    print(f"RUNTIME_MEDIA_VERIFIED={len(passed)}")
    print(f"RUNTIME_MEDIA_FAILED={len(failed)}")
    for key, job_id, image_id, (width, height), access in passed:
        print(
            f"GAME_PATH_OK key={key} job={job_id} image={image_id} "
            f"size={width}x{height} anonymous={access}"
        )
    for key, image_id, reason in failed:
        print(f"GAME_PATH_FAILED key={key} image={image_id} reason={reason}")
    return 1 if failed or not entries else 0


if __name__ == "__main__":
    sys.exit(main())
