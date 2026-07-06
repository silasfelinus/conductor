# Superkate Services Calculator — PROJECT Dream Sync Handoff

Date: 2026-07-06  
Task: `superkate-services-calculator/t-001`  
Status: connector-blocked handoff

## Purpose

This task exists to enforce slug parity between Conductor and Kind Robots. The Conductor project slug is `superkate-services-calculator`; Kind Robots should have a matching PROJECT Dream with the same slug so the workspace, Dream UI, and agent roadmap all point at the same app identity.

## Required Dream record

Create or verify a Kind Robots Dream with:

- `slug`: `superkate-services-calculator`
- `dreamType`: `PROJECT`
- `projectStatus`: `ACTIVE`
- `priority`: `HIGH`
- Friendly title/name: `Superkate Services Calculator`
- Goal: private appointment services calculator for Hair by Superkate
- Waypoints, if supported by the sync path:
  - Finalize MVP and security baseline
  - Build customer and appointment persistence
  - Add appointment search and receipt preparation
  - Polish the dark purple/teal salon UI
  - Prepare private handoff without app-store submission

## Canonical path

Prefer the repository script:

```bash
python scripts/sync_projects_to_dreams.py
```

That script is the canonical Conductor-to-Dream bridge described in `CONTROL.md`. It should upsert PROJECT Dreams from active Conductor projects by slug and preserve roadmap YAML as the authoritative task source.

## Alternate API path

If the script is unavailable, use the Kind Robots API directly to upsert the PROJECT Dream. The API action should be authenticated with `KR_API_TOKEN` or the current approved machine-auth mechanism. Do not commit the token. Do not create a second source of truth or add redundant foreign-key fields; the slug is the join key.

## Verification checklist

After the sync/API write, verify:

1. A PROJECT Dream exists for `superkate-services-calculator`.
2. The Dream is active and visible to the workspace project surface.
3. No duplicate PROJECT Dream exists with a variant slug such as `superkate-services` or `hair-by-superkate`.
4. Conductor `projects/superkate-services-calculator/roadmap.yaml` remains the authoritative task queue.
5. Kind Robots Dream `goal` and `waypoints` are display/voice state only, not a replacement roadmap.

## What blocked direct completion here

This manual Worker run used the GitHub connector only. The connector can edit repository files and PRs, but cannot execute `python scripts/sync_projects_to_dreams.py`, cannot read local environment variables, and does not have access to `KR_API_TOKEN` or the Kind Robots runtime. Because the task is specifically an external database/API sync, marking it `done` from this run would be dishonest. Tiny goblin avoided.

## Next action

Run the sync script from a full Worker/runtime environment with `KR_API_TOKEN`, or perform the authenticated Kind Robots API upsert manually. Once verified, update this task in `projects/superkate-services-calculator/roadmap.yaml` to `done` with a note identifying the successful sync path.
