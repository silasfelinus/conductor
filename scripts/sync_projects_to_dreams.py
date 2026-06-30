#!/usr/bin/env python3
"""
sync_projects_to_dreams.py — Upsert conductor projects as Dreams in kind_robots.

For each active project in project-overrides.yaml, reads its roadmap.yaml and
calls the kind_robots API to create or update a Dream with dreamType PROJECT,
using the project slug as the canonical join key.

Run at the END of every Worker cycle, after task work is complete.

Requires: KR_API_TOKEN env var (a valid kind_robots JWT for Silas's account)
API base: https://kind-robots.vercel.app

Status mapping:
  conductor active  → kind_robots ACTIVE
  conductor paused  → kind_robots PAUSED
  conductor finished → kind_robots DONE
  conductor retired  → kind_robots ARCHIVED

Exit codes: 0 = success, 1 = fatal config error
Stdout: one line per project — CREATED / UPDATED / SKIPPED / ERROR
"""

import json
import os
import sys
import urllib.error
import urllib.request
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


def find_dream_by_slug(slug, token):
    try:
        body = kr_request("GET", f"/dreams?slug={slug}", token)
        dreams = body.get("data", [])
        for d in dreams:
            if d.get("slug") == slug:
                return d
        return None
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


def build_dream_payload(slug, override, roadmap):
    title = roadmap.get("project", slug).replace("-", " ").title() if roadmap else slug
    notes = roadmap.get("notes_from_silas", "") if roadmap else ""
    description = first_paragraph(notes) or f"Conductor project: {slug}"

    conductor_status = override.get("status", "active")
    kr_status = CONDUCTOR_TO_KR_STATUS.get(conductor_status, "ACTIVE")

    return {
        "slug": slug,
        "title": title,
        "description": description,
        "dreamType": "PROJECT",
        "projectStatus": kr_status,
    }


def sync_project(slug, override, token):
    roadmap = load_roadmap(slug)
    payload = build_dream_payload(slug, override, roadmap)

    try:
        existing = find_dream_by_slug(slug, token)
    except Exception as e:
        print(f"  {slug}: ERROR checking existence — {e}")
        return

    try:
        if existing:
            dream_id = existing.get("id")
            kr_request("PATCH", f"/dreams/{dream_id}", token, payload)
            print(f"  {slug}: UPDATED (id={dream_id})")
        else:
            result = kr_request("POST", "/dreams", token, payload)
            new_id = result.get("data", {}).get("id", "?")
            print(f"  {slug}: CREATED (id={new_id})")
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        print(f"  {slug}: ERROR {e.code} — {body[:200]}")
    except Exception as e:
        print(f"  {slug}: ERROR — {e}")


def main():
    token = os.environ.get("KR_API_TOKEN", "").strip()
    if not token:
        print("⚠️  KR_API_TOKEN not set — skipping sync.", file=sys.stderr)
        print("Set KR_API_TOKEN to a valid kind_robots JWT and re-run.")
        return

    overrides = load_overrides()
    active = [o for o in overrides if o.get("status") == "active"]

    print(f"sync_projects_to_dreams: syncing {len(active)} active projects")
    for override in active:
        slug = override.get("slug")
        if not slug:
            continue
        sync_project(slug, override, token)
    print("done.")


if __name__ == "__main__":
    main()
