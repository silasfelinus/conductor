#!/usr/bin/env python3
"""
sync_projects.py — Upsert conductor projects as first-class Projects in kind_robots.

For each active project in project-overrides.yaml, reads its roadmap.yaml and
calls the kind_robots /api/projects endpoints to create or update a Project,
using conductorSlug as the canonical join key. (Replaces the retired
sync_projects_to_dreams.py: Dreams no longer carry project state — the Dream
model split into Dream / Project / Facet in July 2026.)

Run at the END of every Worker cycle, after task work is complete.

Requires: KR_API_TOKEN env var (a valid kind_robots JWT for Silas's account)
API base: https://kind-robots.vercel.app

Status mapping:
  conductor active   → kind_robots ACTIVE
  conductor paused   → kind_robots PAUSED
  conductor finished → kind_robots DONE
  conductor retired  → kind_robots ARCHIVED

Priority mapping (project-overrides.yaml):
  low → LOW, normal → NORMAL, high/urgent → HIGH

Exit codes: 0 = success, 1 = fatal config error
Stdout: one line per project — CREATED / UPDATED / SKIPPED / ERROR
"""

import json
import os
import sys
import urllib.error
import urllib.request
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
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def find_project_by_slug(slug, token):
    """GET /api/projects/{key} resolves both slug and conductorSlug."""
    try:
        body = kr_request("GET", f"/projects/{slug}", token)
        return body.get("data")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def load_overrides():
    if not OVERRIDES_FILE.exists():
        print(f"❌ {OVERRIDES_FILE} not found", file=sys.stderr)
        sys.exit(1)
    with open(OVERRIDES_FILE) as f:
        doc = yaml.safe_load(f)
    return doc.get("overrides", [])


def load_roadmap(slug):
    path = PROJECTS_DIR / slug / "roadmap.yaml"
    if not path.exists():
        return None
    with open(path) as f:
        return yaml.safe_load(f)


def first_paragraph(text):
    if not text:
        return ""
    paragraphs = [p.strip() for p in str(text).split("\n\n") if p.strip()]
    return paragraphs[0] if paragraphs else str(text).strip()


def build_project_payload(slug, override, roadmap):
    title = roadmap.get("project", slug).replace("-", " ").title() if roadmap else slug
    notes = roadmap.get("notes_from_silas", "") if roadmap else ""
    description = first_paragraph(notes) or f"Conductor project: {slug}"

    conductor_status = override.get("status", "active")
    kr_status = CONDUCTOR_TO_KR_STATUS.get(conductor_status, "ACTIVE")
    conductor_priority = str(override.get("priority", "normal")).lower()
    kr_priority = CONDUCTOR_TO_KR_PRIORITY.get(conductor_priority, "NORMAL")

    return {
        "title": title,
        "description": description,
        "conductorSlug": slug,
        "status": kr_status,
        "priority": kr_priority,
        "lastSyncedAt": datetime.now(timezone.utc).isoformat(),
    }


def sync_project(slug, override, token):
    """Upsert one project. Returns True on success, False on any error."""
    roadmap = load_roadmap(slug)
    payload = build_project_payload(slug, override, roadmap)

    try:
        existing = find_project_by_slug(slug, token)
    except urllib.error.HTTPError as e:
        print(f"  {slug}: ERROR {e.code} checking existence — {e}")
        return False
    except Exception as e:
        print(f"  {slug}: ERROR checking existence — {e}")
        return False

    try:
        if existing:
            project_id = existing.get("id")
            kr_request("PATCH", f"/projects/{project_id}", token, payload)
            print(f"  {slug}: UPDATED (id={project_id})")
        else:
            # slug only on create: the KR-side slug stays user-editable after
            # that; conductorSlug remains the stable join key.
            result = kr_request("POST", "/projects", token, {**payload, "slug": slug})
            new_id = result.get("data", {}).get("id", "?")
            print(f"  {slug}: CREATED (id={new_id})")
        return True
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        print(f"  {slug}: ERROR {e.code} — {body[:200]}")
        if e.code == 401:
            print(
                "  ^ 401 from kind_robots: KR_API_TOKEN is invalid or expired. "
                "Mint a fresh JWT and update the secret.",
                file=sys.stderr,
            )
        return False
    except Exception as e:
        print(f"  {slug}: ERROR — {e}")
        return False


def main():
    token = os.environ.get("KR_API_TOKEN", "").strip()
    if not token:
        print("⚠️  KR_API_TOKEN not set — skipping sync.", file=sys.stderr)
        print("Set KR_API_TOKEN to a valid kind_robots JWT and re-run.")
        return

    overrides = load_overrides()
    active = [o for o in overrides if o.get("status") == "active"]

    print(f"sync_projects: syncing {len(active)} active projects")
    failures = 0
    for override in active:
        slug = override.get("slug")
        if not slug:
            continue
        if not sync_project(slug, override, token):
            failures += 1

    if failures:
        # Exit nonzero so CI goes red instead of masking a broken bridge —
        # the pre-cutover sync failed green for weeks because errors were
        # only visible in per-line output.
        print(f"done with {failures}/{len(active)} failures.")
        sys.exit(1)
    print("done.")


if __name__ == "__main__":
    main()
