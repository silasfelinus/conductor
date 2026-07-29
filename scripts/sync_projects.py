#!/usr/bin/env python3
"""
sync_projects.py — Upsert tracked Conductor projects as first-class Projects in kind_robots.

For every recognized lifecycle entry in project-overrides.yaml, read its roadmap.yaml and
call the kind_robots /api/projects endpoints using conductorSlug as the canonical join key.
This includes active, paused, finished, and retired projects: lifecycle changes are part of
the sync contract, not a reason to skip synchronization.

Run at the END of every Worker cycle, after task work is complete.

Requires: KR_API_TOKEN env var (a valid kind_robots JWT for Silas's account)
API base: https://kind-robots.vercel.app

Status mapping:
  conductor active   → kind_robots ACTIVE
  conductor paused   → kind_robots PAUSED
  conductor finished → kind_robots DONE
  conductor retired  → kind_robots ARCHIVED (isActive=false)

Priority mapping (project-overrides.yaml):
  low → LOW, normal → NORMAL, high/urgent → HIGH

Exit codes: 0 = success, 1 = fatal config error
Stdout: one line per project — CREATED / UPDATED / SKIPPED / ERROR
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML not installed; run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).parent.parent
OVERRIDES_FILE = REPO_ROOT / "project-overrides.yaml"
PROJECTS_DIR = REPO_ROOT / "projects"
KR_API_BASE = "https://kind-robots.vercel.app/api"
TRANSIENT_HTTP_CODES = {429, 500, 502, 503, 504}
TRANSIENT_BODY_MARKERS = (
    "connection closed",
    "econnreset",
    "connection terminated",
    "connect timeout",
)
MAX_REQUEST_ATTEMPTS = 4

CONDUCTOR_TO_KR_STATUS = {
    "active": "ACTIVE",
    "paused": "PAUSED",
    "finished": "DONE",
    "retired": "ARCHIVED",
}

CONDUCTOR_TO_KR_PRIORITY = {
    "low": "LOW",
    "normal": "NORMAL",
    "high": "HIGH",
    "urgent": "HIGH",
}


def _looks_transient(body):
    text = body.decode(errors="replace").lower()
    return any(marker in text for marker in TRANSIENT_BODY_MARKERS)


def kr_request(method, path, token, payload=None):
    url = f"{KR_API_BASE}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    for attempt in range(1, MAX_REQUEST_ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as error:
            body = error.read()
            transient = error.code in TRANSIENT_HTTP_CODES or _looks_transient(body)
            if not transient or attempt == MAX_REQUEST_ATTEMPTS:
                error.read = lambda body=body: body
                raise
        except (urllib.error.URLError, TimeoutError):
            if attempt == MAX_REQUEST_ATTEMPTS:
                raise

        delay = 2 ** (attempt - 1)
        print(
            f"  transient {method} {path} failure; retrying in {delay}s "
            f"({attempt}/{MAX_REQUEST_ATTEMPTS})",
            file=sys.stderr,
        )
        time.sleep(delay)

    raise RuntimeError(f"{method} {path} exhausted retries")


def find_project_by_slug(slug, token):
    """GET /api/projects/{key} resolves both slug and conductorSlug."""
    try:
        body = kr_request("GET", f"/projects/{slug}", token)
        return body.get("data")
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise


def load_overrides():
    if not OVERRIDES_FILE.exists():
        print(f"❌ {OVERRIDES_FILE} not found", file=sys.stderr)
        sys.exit(1)
    with open(OVERRIDES_FILE, encoding="utf-8") as handle:
        doc = yaml.safe_load(handle) or {}
    return doc.get("overrides", [])


def synced_overrides(overrides):
    """Return every lifecycle entry the Kind Robots Project schema understands."""
    return [
        override
        for override in overrides
        if override.get("slug")
        and str(override.get("status", "active")).lower()
        in CONDUCTOR_TO_KR_STATUS
    ]


def load_roadmap(slug):
    path = PROJECTS_DIR / slug / "roadmap.yaml"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def first_paragraph(text):
    if not text:
        return ""
    paragraphs = [p.strip() for p in str(text).split("\n\n") if p.strip()]
    return paragraphs[0] if paragraphs else str(text).strip()


def build_project_payload(slug, override, roadmap):
    title = roadmap.get("project", slug).replace("-", " ").title() if roadmap else slug
    notes = roadmap.get("notes_from_silas", "") if roadmap else ""
    description = first_paragraph(notes) or f"Conductor project: {slug}"

    conductor_status = str(override.get("status", "active")).lower()
    kr_status = CONDUCTOR_TO_KR_STATUS.get(conductor_status, "ACTIVE")
    conductor_priority = str(override.get("priority", "normal")).lower()
    kr_priority = CONDUCTOR_TO_KR_PRIORITY.get(conductor_priority, "NORMAL")

    payload = {
        "title": title,
        "description": description,
        "conductorSlug": slug,
        "status": kr_status,
        "priority": kr_priority,
        "isActive": kr_status != "ARCHIVED",
        "lastSyncedAt": datetime.now(timezone.utc).isoformat(),
    }

    goal = roadmap.get("goal") if roadmap else None
    if isinstance(goal, str) and goal.strip():
        payload["goal"] = goal.strip()

    for field in ("liveUrl", "channelKey", "tabKey", "repoUrl"):
        value = override.get(field)
        if value is None and roadmap:
            value = roadmap.get(field)
        if isinstance(value, str) and value.strip():
            payload[field] = value.strip()

    return payload


def project_changed_fields(existing, payload):
    return [
        field
        for field, value in payload.items()
        if field != "lastSyncedAt" and existing.get(field) != value
    ]


def sync_project(slug, override, token):
    """Upsert one project. Returns True on success, False on any error."""
    roadmap = load_roadmap(slug)
    payload = build_project_payload(slug, override, roadmap)

    try:
        existing = find_project_by_slug(slug, token)
    except urllib.error.HTTPError as error:
        print(f"  {slug}: ERROR {error.code} checking existence — {error}")
        return False
    except Exception as error:
        print(f"  {slug}: ERROR checking existence — {error}")
        return False

    try:
        if existing:
            project_id = existing.get("id")
            changed_fields = project_changed_fields(existing, payload)
            if not changed_fields:
                print(f"  {slug}: UNCHANGED (id={project_id})")
                return True

            kr_request("PATCH", f"/projects/{project_id}", token, payload)
            fields = ", ".join(changed_fields)
            print(f"  {slug}: UPDATED (id={project_id}; fields={fields})")
        else:
            result = kr_request("POST", "/projects", token, {**payload, "slug": slug})
            new_id = result.get("data", {}).get("id", "?")
            print(f"  {slug}: CREATED (id={new_id})")
        return True
    except urllib.error.HTTPError as error:
        body = error.read().decode(errors="replace")
        print(f"  {slug}: ERROR {error.code} — {body[:200]}")
        if error.code == 401:
            print(
                "  ^ 401 from kind_robots: KR_API_TOKEN is invalid or expired. "
                "Mint a fresh JWT and update the secret.",
                file=sys.stderr,
            )
        return False
    except Exception as error:
        print(f"  {slug}: ERROR — {error}")
        return False


def main():
    token = os.environ.get("KR_API_TOKEN", "").strip()
    if not token:
        print("⚠️  KR_API_TOKEN not set — skipping sync.", file=sys.stderr)
        print("Set KR_API_TOKEN to a valid kind_robots JWT and re-run.")
        return

    overrides = synced_overrides(load_overrides())
    lifecycle_counts = Counter(
        str(override.get("status", "active")).lower() for override in overrides
    )
    summary = ", ".join(
        f"{status}={lifecycle_counts.get(status, 0)}"
        for status in CONDUCTOR_TO_KR_STATUS
    )
    print(f"sync_projects: syncing {len(overrides)} tracked projects ({summary})")

    failures = 0
    for override in overrides:
        slug = override.get("slug")
        if not sync_project(slug, override, token):
            failures += 1

    if failures:
        print(f"done with {failures}/{len(overrides)} failures.")
        sys.exit(1)
    print("done.")


if __name__ == "__main__":
    main()
