# Slug Parity Audit: Conductor Projects vs. Kind Robots Dreams

**Audit date:** 2026-07-01
**Task:** kind-robots/t-003
**Auditor:** Worker (automated)

---

## Overview

The slug is the universal key linking conductor projects to kind_robots Dreams.
Every conductor project must have a matching kind_robots Dream of `dreamType: PROJECT`
sharing the same slug. This document audits that parity.

**Source of truth for conductor projects:** `project-overrides.yaml`
**Source of truth for kind_robots Dreams:** `https://kind-robots.vercel.app/api/dreams?dreamType=PROJECT`
**Sync tool:** `scripts/sync_projects_to_dreams.py`

---

## Limitation: API Not Verified

`KR_API_TOKEN` was not available in this session. Actual Dream existence in kind_robots
**cannot be verified** from this document alone. This audit documents what SHOULD exist
based on `project-overrides.yaml`. To confirm actual parity, run:

```bash
KR_API_TOKEN=<your-token> python scripts/sync_projects_to_dreams.py
```

---

## Status Mapping (conductor → kind_robots)

| Conductor status | kind_robots `projectStatus` |
|------------------|-----------------------------|
| `active`         | `ACTIVE`                    |
| `paused`         | `PAUSED`                    |
| `finished`       | `DONE`                      |
| `retired`        | `ARCHIVED`                  |

---

## Full Project List from project-overrides.yaml

### Active Projects

Each active project SHOULD have a Dream with `dreamType: PROJECT`, matching `slug`, and `projectStatus: ACTIVE`.

| Slug                    | Priority | roadmap.yaml exists? | Expected Dream slug         | Expected projectStatus |
|-------------------------|----------|----------------------|-----------------------------|------------------------|
| conductor               | normal   | yes                  | `conductor`                 | ACTIVE                 |
| kind-robots             | normal   | yes                  | `kind-robots`               | ACTIVE                 |
| global-ui               | normal   | yes                  | `global-ui`                 | ACTIVE                 |
| humboldt-scoop          | normal   | yes                  | `humboldt-scoop`            | ACTIVE                 |
| humboldt-scoop-cms      | normal   | yes                  | `humboldt-scoop-cms`        | ACTIVE                 |
| digital-storefront      | normal   | yes                  | `digital-storefront`        | ACTIVE                 |
| brainstorm              | normal   | yes                  | `brainstorm`                | ACTIVE                 |
| sketchy                 | normal   | yes                  | `sketchy`                   | ACTIVE                 |
| pinball-hero            | normal   | yes                  | `pinball-hero`              | ACTIVE                 |
| art-generator-connect   | normal   | yes                  | `art-generator-connect`     | ACTIVE                 |
| storymaker              | normal   | yes                  | `storymaker`                | ACTIVE                 |
| media-watchlist         | normal   | yes                  | `media-watchlist`           | ACTIVE                 |
| conductor-app           | normal   | yes                  | `conductor-app`             | ACTIVE                 |
| alexa-integration       | normal   | yes                  | `alexa-integration`         | ACTIVE                 |
| career-transition       | normal   | yes                  | `career-transition`         | ACTIVE                 |
| engagement              | normal   | yes                  | `engagement`                | ACTIVE                 |
| wishmaster              | normal   | yes                  | `wishmaster`                | ACTIVE                 |

**Count:** 17 active projects

### Paused Projects

Each paused project SHOULD have a Dream with `dreamType: PROJECT`, matching `slug`, and `projectStatus: PAUSED`.

| Slug                | Priority | roadmap.yaml exists? | Expected Dream slug     | Expected projectStatus |
|---------------------|----------|----------------------|-------------------------|------------------------|
| approval-portal     | low      | yes                  | `approval-portal`       | PAUSED                 |
| mermaids-of-venice  | low      | yes                  | `mermaids-of-venice`    | PAUSED                 |
| coat-dance          | low      | yes                  | `coat-dance`            | PAUSED                 |

**Count:** 3 paused projects

---

## Orphan Files in projects/ (not in project-overrides.yaml)

The following entries exist under `projects/` but are NOT in `project-overrides.yaml`.
They do NOT need a Dream — they are utility files or unregistered:

| Entry              | Type   | Notes                                               |
|--------------------|--------|-----------------------------------------------------|
| `_template/`       | dir    | Scaffold template — intentionally unregistered       |
| `images/`          | dir    | Shared image assets — not a project                 |
| `process/`         | dir    | Internal process docs — not a project               |
| `art-generate.yaml`| file   | Standalone YAML file — not a project directory       |
| `art-prompts.yaml` | file   | Standalone YAML file — not a project directory       |
| `priority.yaml`    | file   | Internal priority file — not a project directory     |

None of these should have matching Dreams.

---

## Risk Flags: Slug Naming Inconsistencies

### Hyphen vs. Underscore Risk

All conductor slugs use **hyphens** (`-`). kind_robots URLs and the Prisma schema
may handle slugs with special characters differently. Risky slugs to double-check:

| Slug                   | Risk                                                                 |
|------------------------|----------------------------------------------------------------------|
| `humboldt-scoop-cms`   | Three-segment slug — confirm Dream.slug accepts multi-hyphen values  |
| `art-generator-connect`| Three-segment slug — same concern                                    |
| `alexa-integration`    | External platform name in slug — stable, no concern                  |
| `mermaids-of-venice`   | Three-segment slug with "of" — confirm slug uniqueness constraints   |

### Slug Collision Risk

No two slugs in `project-overrides.yaml` are similar enough to collide, but check:

- `humboldt-scoop` vs. `humboldt-scoop-cms` — these are intentionally distinct,
  confirm the kind_robots API does not perform prefix matching that could confuse them.
- `conductor` vs. `conductor-app` — same concern: distinct slugs for the conductor
  automation project vs. the Nuxt app. Verify both Dreams exist and are distinct.

### Orphan YAML: art-generate.yaml / art-prompts.yaml

`projects/art-generate.yaml` and `projects/art-prompts.yaml` sit at the projects root
as flat files — not inside a directory. If `art-generator-connect` is meant to cover
this domain, confirm no stale Dreams exist with slug `art-generate` or `art-prompts`.

---

## Expected Dream Structure (per project)

For any active project, the Dream upserted by `sync_projects_to_dreams.py` will have:

```json
{
  "slug": "<conductor-project-slug>",
  "title": "<Title Cased From Slug>",
  "description": "<first paragraph of roadmap.yaml notes_from_silas, or fallback>",
  "dreamType": "PROJECT",
  "projectStatus": "ACTIVE"
}
```

The script derives `title` by replacing hyphens with spaces and title-casing.
Example: `art-generator-connect` → `Art Generator Connect`.

---

## Reconciliation Checklist

- [ ] Ensure `KR_API_TOKEN` is set in your environment
- [ ] Run `python scripts/sync_projects_to_dreams.py` to upsert all 17 active projects
- [ ] Verify paused projects also have Dreams with `projectStatus: PAUSED`
  (the sync script currently only syncs active projects — see script line 156;
  **action item:** extend script or manually upsert paused projects if needed)
- [ ] After sync, spot-check these higher-risk slugs in the kind_robots UI:
  - `humboldt-scoop-cms`
  - `art-generator-connect`
  - `mermaids-of-venice`
  - `conductor` vs. `conductor-app` (confirm both exist as distinct Dreams)
- [ ] Confirm no stale Dreams exist for `art-generate` or `art-prompts`
- [ ] Approve this audit and set `approved_by_human: true` on kind-robots/t-003
  to unblock kind-robots/t-004 (project creation surfaces spec)

---

## Note on Paused Projects and the Sync Script

`sync_projects_to_dreams.py` (line 156) filters to **active** projects only:

```python
active = [o for o in overrides if o.get("status") == "active"]
```

This means paused projects (`approval-portal`, `mermaids-of-venice`, `coat-dance`)
are **not automatically synced**. Two options:

1. Manually upsert the three paused Dreams with `projectStatus: PAUSED`
2. Extend `sync_projects_to_dreams.py` to also sync non-retired projects
   (active + paused) and set the appropriate status

Recommend option 2 as a follow-on task so all registered projects maintain parity.

---

*Generated by Worker agent | kind-robots/t-003 | 2026-07-01*
