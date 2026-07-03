# AppMaker — Project Brief

Date: 2026-07-02
Status: awaiting Silas's approval (appmaker/t-001)
Source: Silas's direction, in-session. This brief records that direction and the
architecture it implies; approve t-001 to unlock the build tasks.

## What it is

AppMaker is the app factory built on top of the conductor system: a manager and
creator of apps. Conductor coordinates projects generally; AppMaker is the
specialization for shipping many apps — create an app, develop it through the
Worker/Reviewer loop, test it in CI, and walk it to the stores. "Effectively a
conductor project manager, but focused on apps."

## The three surfaces

1. **kind_robots front-end** (primary — how Silas expects to use it day to day):
   an AppMaker page in the workspace to browse apps, create a new one, and see
   each app's build/test/release state.
2. **The AppMaker app itself**: a mobile surface built on the conductor_app
   foundation (same server modes, same auth model) for managing apps on the go.
3. **The conductor repo** as the workshop where the code actually lives.

## Repo layout

Each app gets its own folder inside the conductor repo:

```
apps/
  <slug>/        one self-contained app project (Flutter or otherwise)
```

Creating an app produces three artifacts sharing one slug (the slug-parity rule):
- `apps/<slug>/` — the code workspace
- `projects/<slug>/roadmap.yaml` — the conductor project that drives agent work
- a kind_robots Dream (dreamType PROJECT, same slug) — identity/display record

A scaffolder script (`scripts/new_app.py`, appmaker/t-002) creates all three
pieces plus ART-PROMPTS entries, so "make a lot of these" is one command — and
the kind_robots front-end can trigger it by creating an AGENT todo.

Note: the existing conductor app lives at `app/` (grandfathered). Open question
for Silas: migrate it to `apps/conductor/` for uniformity once CI paths are
updated, or leave it.

## GitHub integration — permission-based git

Two phases, matching who's using it:

**Phase 1 (Silas's own apps, now):** apps live in the conductor monorepo. The
existing permission model already covers it: Worker pushes only `worker/*`
branches, PRs into main, Reviewer merges reversible software changes, humans
gate releases. Per-app path scoping can be added with CODEOWNERS if needed.

**Phase 2 (multi-user / hosted):** other users' apps cannot live in
silasfelinus/conductor. Permission-based git means each user connects their own
GitHub with explicitly scoped credentials — a GitHub App installation (or
fine-grained PAT) limited to the specific repos they choose. AppMaker scaffolds
into *their* repo and drives agent work there with only the permissions
granted. An app can also "graduate" from the monorepo to its own repo, with
AppMaker keeping the slug → repo mapping. Credential storage is server-side,
encrypted, never in any client binary (same rule as conductor-app auth).

The permission model design (which credential mechanism, token storage, repo
mapping schema) is appmaker/t-003.

## What AppMaker manages per app

- Identity: slug, Dream, icon/card/hero art
- Roadmap: milestones/tasks the Worker/Reviewer cycle executes
- Code: the `apps/<slug>/` folder (or external repo in phase 2)
- Quality: per-app CI (the app-ci.yml pattern generalizes to `apps/**`)
- Release: store-readiness checklists, always `needs-human` before submission

## Open questions for Silas (answer in t-001 approval note)

1. Migrate `app/` → `apps/conductor/` now, later, or never?
2. Phase 2 credential mechanism preference: GitHub App (recommended — per-repo
   install, revocable, no expiry management) vs fine-grained PATs?
3. Should app creation from the kind_robots page be self-serve for members on
   the hosted tier, or admin-only until AppMaker matures?
