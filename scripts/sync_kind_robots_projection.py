#!/usr/bin/env python3
"""Push a raw, commit-stamped Conductor snapshot into Kind Robots.

Conductor owns coordination state. Kind Robots stores this payload as a
materialized read model and normalizes it with its own parser. The script never
reads from Kind Robots before writing and never imports presentation metadata
back into Conductor.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_API_BASE = "https://kindrobots.org"
MAX_PAYLOAD_BYTES = 4_000_000


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def source_commit_sha() -> str:
    github_sha = os.environ.get("GITHUB_SHA", "").strip()
    if github_sha:
        return github_sha
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def text_map(directory: Path, pattern: str) -> dict[str, str]:
    if not directory.exists():
        return {}
    return {
        path.name: read_text(path)
        for path in sorted(directory.glob(pattern))
        if path.is_file()
    }


def roadmap_map() -> dict[str, str]:
    projects_dir = ROOT / "projects"
    roadmaps: dict[str, str] = {}
    for path in sorted(projects_dir.glob("*/roadmap.yaml")):
        if path.parent.name == "_template":
            continue
        roadmaps[path.parent.name] = read_text(path)
    return roadmaps


def image_versions() -> dict[str, str]:
    images_dir = ROOT / "projects" / "images"
    if not images_dir.exists():
        return {}
    versions: dict[str, str] = {}
    for path in sorted(images_dir.iterdir()):
        if not path.is_file():
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        versions[path.name] = digest
    return versions


def build_snapshot() -> dict[str, Any]:
    return {
        "version": 1,
        "sourceRepo": "silasfelinus/conductor",
        "sourceRef": "main",
        "sourceCommitSha": source_commit_sha(),
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "registryYaml": read_text(ROOT / "project-overrides.yaml"),
        "roadmaps": roadmap_map(),
        "pitches": text_map(ROOT / "pitches", "*.md"),
        "imageVersions": image_versions(),
    }


def encoded_snapshot(snapshot: dict[str, Any]) -> bytes:
    payload = json.dumps(snapshot, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )
    if len(payload) > MAX_PAYLOAD_BYTES:
        raise RuntimeError(
            f"projection payload is {len(payload)} bytes; limit is {MAX_PAYLOAD_BYTES}"
        )
    return payload


def post_snapshot(api_base: str, token: str, payload: bytes) -> dict[str, Any]:
    endpoint = f"{api_base.rstrip('/')}/api/conductor/sync"
    request = urllib.request.Request(
        endpoint,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "conductor-projection-sync/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Kind Robots sync failed: HTTP {error.code}: {body}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"Kind Robots sync failed: {error.reason}") from error

    parsed = json.loads(body)
    if not parsed.get("success"):
        raise RuntimeError(f"Kind Robots rejected projection: {body}")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Build and validate the snapshot without sending it.",
    )
    parser.add_argument(
        "--api-base",
        default=os.environ.get("KR_API_BASE", DEFAULT_API_BASE),
    )
    args = parser.parse_args()

    snapshot = build_snapshot()
    payload = encoded_snapshot(snapshot)
    summary = {
        "sourceCommitSha": snapshot["sourceCommitSha"],
        "roadmaps": len(snapshot["roadmaps"]),
        "pitches": len(snapshot["pitches"]),
        "images": len(snapshot["imageVersions"]),
        "payloadBytes": len(payload),
    }

    if args.check:
        print(json.dumps(summary, indent=2))
        return 0

    token = os.environ.get("KR_API_TOKEN", "").strip()
    if not token:
        print("KR_API_TOKEN is not set; skipping Kind Robots projection sync")
        return 0

    result = post_snapshot(args.api_base, token, payload)
    print(json.dumps({**summary, "result": result.get("data")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
