# Project Creation Surfaces — Spec

Generated: 2026-06-30
Updated: 2026-07-12 — rewritten for the Dream / Project / Facet split. Project
records are now the first-class kind_robots `Project` model at `/api/projects`;
Dreams no longer carry project state (dreamType PROJECT was removed).
Updated: 2026-08-10 — added Surfaces 4-6 (AppMaker's two self-serve routes and
Model Builder's promotion path), all found undocumented by kind-robots/t-058's
m3 gap audit; corrected Surface 1's endpoint and Surfaces 2/3's stale
"auto-Todo not yet implemented" notes to match current code. Docs-only pass —
no route code changed. Task: kind-robots/t-059.
Task: kind-robots/t-004

---

## The Invariant

In all cases: `Project.conductorSlug === conductor project directory name`

This is the universal join key. A project exists when both (a) a `roadmap.yaml` at `projects/<slug>/` and (b) a kind_robots `Project` with `conductorSlug: <slug>` exist. Either can come first; the system reconciles them. (`Project.slug` starts equal to the conductor slug but stays user-editable on the KR side; `conductorSlug` is the stable key.)

---

## Surface 1: Conductor File Format

**How a new `roadmap.yaml` triggers Project creation**

### Flow (current, corrected 2026-08-10 — see note below)

1. Worker or Silas creates `projects/<slug>/roadmap.yaml` in the conductor repo (via PR or direct commit)
2. `scripts/sync_kind_robots_projection.py` builds a single `ConductorProjectionSnapshot`
   (every active-project's slug/title/goal/status/priority/etc, per `project-overrides.yaml`)
   and POSTs it whole to `POST /api/conductor/sync` (`server/api/conductor/sync.post.ts`,
   admin-only via `requireAdminApiUser`)
3. The route matches each snapshot project against existing `Project` rows by
   `conductorSlug` OR `slug`; a slug matched to more than one row, or to a
   `conductorSlug` already linked elsewhere, is a `409` (logged, not silently skipped)
4. No match → `tx.project.create()` with `conductorSlug: project.slug` (slug = conductorSlug
   on create, exactly like the old per-project flow)
5. Match found → `tx.project.update()`: `status`/`priority`/`isActive`/`lastSyncedAt` refresh;
   an `ARCHIVED` status also clears `liveUrl`/`channelKey`/`tabKey`

**Who writes the Project:** The sync script's target route, run server-side or as a conductor CI step.  
**Who writes the roadmap:** Worker (by PR) or Silas (direct).  
**Slug enforcement:** The directory name IS the slug; no separate slug field is needed in roadmap.yaml.

### Constraints
- The sync route must never delete a Project; only create or update
- Existing Projects are updated in place — the KR-side `slug` is only set on create so user edits survive

### Note (2026-08-10)
This section originally described `scripts/sync_projects.py` calling `POST /api/projects`
once per new slug. That script and per-project call pattern are superseded by
`scripts/sync_kind_robots_projection.py` → `POST /api/conductor/sync`'s single-payload
bulk upsert (same invariant, same `conductorSlug` join key, different transport). Found
stale while auditing surfaces for kind-robots/t-059; corrected here as a docs-only fix,
no route code touched.

---

## Surface 2: Kind Robots Front-End

**How a UI action creates a new project**

### Flow

1. Silas (or an authorized user) opens the Kind Robots workspace UI and selects "New Project"
2. UI prompts for: project name (→ `title`), short description, and confirms the derived `slug` (auto-generated from title, editable)
3. On submit, UI calls `POST /api/projects` with `slug`, `title`, `description`
4. The API creates the Project record
5. The API (or a Project creation webhook) automatically creates a Todo for the Worker:
   ```json
   {
     "title": "Scaffold conductor project for <slug>",
     "description": "New Project created with slug '<slug>'. Create projects/<slug>/roadmap.yaml with at least one ready task.",
     "category": "AGENT",
     "priority": "HIGH"
   }
   ```
6. Worker picks up the Todo in the next cycle and creates `projects/<slug>/roadmap.yaml`
7. Next sync run confirms the Project ↔ roadmap link and stamps `conductorSlug`/`lastSyncedAt`

**Who writes the Project:** User via UI → `POST /api/projects`  
**Who writes the roadmap:** Worker, triggered by the Auto-Todo in step 5  
**Slug enforcement:** UI derives slug from title (lowercase, hyphenated); user can override before submit

### Implemented (was "Pitch needed", corrected 2026-08-10)
The auto-Todo on Project creation (step 5) IS implemented: `server/api/projects/index.post.ts`
wraps the create in `createProjectWithScaffoldTodo()`, which creates the `Project` and an
`OPEN`/`HIGH`/`AGENT` `Todo` (via the shared `projectScaffoldTodoContent()` helper in
`server/utils/projectDirectWrite.ts`) in one transaction, filed under the worker account
(`BETA_ADMIN_USER_ID`) and scoped to the new Project. A stale-DB-connection fallback
(`upsertProjectDirect`) does the same insert directly over a raw connection, guarded by a
`WHERE NOT EXISTS` so a retry can't double-file the Todo. Found stale while auditing surfaces
for kind-robots/t-059; corrected here as a docs-only fix, no route code touched.

---

## Surface 3: LLM (Wishmaster or Other Bots)

**How a bot creates a new project from a wish or instruction**

### Flow

1. User sends a wish or instruction to Wishmaster (or another authorized bot): "Start a new project for a podcast website"
2. Bot parses intent: output type = PROJECT, extracts `title` and `description`
3. Bot derives a slug from the title (lowercase, hyphenated, unique check via `GET /api/projects/<slug>` → expect 404)
4. If slug is unique: bot calls `POST /api/projects` with `slug`, `title`, `description`
5. Same auto-Todo as Surface 2 step 5 is created
6. Bot confirms to the user: "Started project 'podcast-website'. The Worker will scaffold the roadmap next cycle."

**Who writes the Project:** Bot via `POST /api/projects` using bot's JWT  
**Who writes the roadmap:** Worker, triggered by the Auto-Todo  
**Slug enforcement:** Bot generates slug, checks uniqueness, retries with suffix if collision (e.g. `podcast-website-2`)

### Auth requirement
- The bot must have a user JWT with permission to create Projects (creation is uncapped, but the active-project cap applies to ACTIVE/PAUSED status — see enforceProjectCap)
- The bot must NOT directly write to the conductor repo; it uses the Auto-Todo → Worker pattern

### Pitch needed
- ~~Auto-Todo on Project creation~~ — implemented; see Surface 2's note (2026-08-10)
- Wishmaster needs a slug-uniqueness check helper (still open)

### Note (2026-08-10)
Wishmaster's live/retired status is currently disputed and unresolved — see
`projects/wishmaster/roadmap.yaml` t-004 (hard `needs-human`). This surface's
description is left as originally written pending that decision; do not treat
either state as confirmed from this doc alone.

---

## Surface 4: AppMaker Self-Serve (Monorepo Scaffold)

**How a user's AppMaker request creates a new project inside this monorepo**

### Flow

1. Authenticated user `POST`s to `/api/appmaker/scaffold-request`
   (`server/api/appmaker/scaffold-request.post.ts`) with `title` (required, ≤200 chars),
   optional `slug` (else derived by the route's own `slugify()`), optional `description`
   (≤1000 chars)
2. Route independently checks slug uniqueness against both `Project` (`slug` OR
   `conductorSlug`) and `Dream` — `409` on collision
3. `enforceProjectCap` runs (same cap function as Surface 2/3)
4. In one transaction: creates `Project` (`conductorSlug: slug`, `isPublic: true`,
   `isActive: true`, owned by the requesting user — not the worker account) and an
   `OPEN`/`NORMAL`/`AGENT` `Todo` filed under the worker account, containing a
   shell-quoted `python scripts/new_app.py <slug> --title '<title>' [--description '<description>']`
   command for the Worker to run next cycle
5. Returns `201` with `projectId`, `slug`, `todoId`

**Who writes the Project:** User via UI → `POST /api/appmaker/scaffold-request`  
**Who writes the roadmap:** Worker, running the Todo's `scripts/new_app.py` command  
**Slug enforcement:** Route's own `SLUG_RE`/`slugify()`, independent of Surface 2/3's route

### Notes
- This is a distinct collision-check implementation from `POST /api/projects` (Surface
  2/3) and from Surface 5 below — three separately-maintained slug/uniqueness checks
  doing the same job. Consolidating them is the scope of the pitch at
  `pitches/2026-08-10-kind-robots-slug-integrity.md` (kind-robots/t-061), not this doc pass.
- Found undocumented by kind-robots/t-058's m3 gap audit. Added here (kind-robots/t-059).

---

## Surface 5: AppMaker Self-Serve (External GitHub Repo)

**How a user's AppMaker request creates a new project backed by a repo they already
granted the GitHub App, instead of scaffolding into this monorepo**

### Flow

1. Authenticated user `POST`s to `/api/appmaker/github/create-app`
   (`server/api/appmaker/github/create-app.post.ts`) with `installationId`, `owner`,
   `repo`, optional `subPath`, `title`, optional `slug`, optional `description`
2. Route verifies the `GithubInstallation` belongs to the requesting user, isn't
   suspended, and that GitHub currently reports `owner/repo` as granted to it
   (`listInstallationRepositories` — never trusts client-supplied owner/repo alone)
3. Checks slug uniqueness against `Project` (`slug` OR `conductorSlug`), `Dream`, and
   `AppRepo` (`slug_userId` composite) — `409` on any collision
4. `enforceProjectCap` runs
5. In one transaction: creates `Project` (same shape as Surface 4) plus an `AppRepo`
   row (`owner`/`repo`/`subPath`/`installationId`), and an `OPEN`/`NORMAL`/`AGENT`
   `Todo` under the worker account asking it to call
   `POST /api/appmaker/github/scaffold` with the new `appRepoId`
6. Returns `201`

**Who writes the Project:** User via UI → `POST /api/appmaker/github/create-app`  
**Who writes the roadmap:** Worker, via the Todo's follow-up `scaffold` call  
**Slug enforcement:** Same route-local `SLUG_RE`/`slugify()` pattern as Surface 4, plus
the `AppRepo` collision check

### Notes
- A third independently-maintained slug/uniqueness check — see Surface 4's note on
  kind-robots/t-061.
- Found undocumented by kind-robots/t-058's m3 gap audit. Added here (kind-robots/t-059).

---

## Surface 6: Model Builder Promotion (Slugless Orphan Project)

**How committing a Model Builder draft item whose `type` is `Project` creates a Project
row — the one path that does NOT follow the slug-parity invariant**

### Flow

1. A Model Builder item of `type: 'Project'` reaches commit
   (`server/api/model-builder/items/[id]/commit.post.ts`)
2. Its `createRecord()` branch for `case 'Project'` calls
   `tx.project.create({ data: { title: name, pitch: text, userId, isPublic: false,
   isActive: false, ...projectFields(fields) } })` — **no `slug` and no
   `conductorSlug` are set at all**
3. The resulting `Project` has no conductor-side counterpart and cannot be matched by
   Surface 1's sync route (which joins on `conductorSlug`/`slug`); it is private
   (`isPublic: false`) and inactive (`isActive: false`) by construction

**Who writes the Project:** The committing user, via Model Builder's generic promotion
path — not a dedicated "new project" UI  
**Who writes the roadmap:** Nobody automatically; this Project has no conductor slug to
scaffold against  
**Slug enforcement:** None. This is the one surface that does not honor the
`Project.conductorSlug === conductor project directory name` invariant from the top of
this doc.

### Notes
- This is a real, live, reachable code path (Model Builder is a shipped feature), but it
  produces Projects that sit outside the parity system this doc otherwise describes —
  they're inert (private/inactive) unless something later assigns them a slug by hand.
- Whether this should stay slugless-by-design, gain a slug on promotion, or be blocked
  entirely for `type: 'Project'` is a product decision, not a docs question — tracked
  as part of the pitch at `pitches/2026-08-10-kind-robots-slug-integrity.md`
  (kind-robots/t-061). This section only documents current behavior.
- Found undocumented by kind-robots/t-058's m3 gap audit. Added here (kind-robots/t-059).

---

## Reconciliation (Any Surface)

The sync route (`server/api/conductor/sync.post.ts`, driven by
`scripts/sync_kind_robots_projection.py`) is the reconciler:

| Situation | Action |
|---|---|
| `roadmap.yaml` exists, no Project | Create Project via `POST /api/conductor/sync` |
| Project exists, no `roadmap.yaml` | Log warning; Worker Todo triggers scaffold |
| Both exist, conductorSlug matches | Update Project fields from roadmap/overrides (title, description, status, priority, lastSyncedAt) |
| Slug mismatch | Log error; do not rename either side; flag for Silas |

The reconciler runs:
- At the end of every Worker cycle
- As a CI step on PRs that touch `projects/` or `project-overrides.yaml`

---

## Summary Table

| Surface | Who creates Project | Who creates roadmap | Trigger for other side |
|---|---|---|---|
| 1. Conductor file | `sync_kind_robots_projection.py` → `/api/conductor/sync` | Worker or Silas | Project created/updated automatically on next sync |
| 2. Kind Robots front-end | User via UI → `POST /api/projects` | Worker (via Auto-Todo) | Auto-Todo created on Project creation |
| 3. LLM (Wishmaster) | Bot via API → `POST /api/projects` | Worker (via Auto-Todo) | Auto-Todo created on Project creation |
| 4. AppMaker self-serve (monorepo) | User via UI → `POST /api/appmaker/scaffold-request` | Worker (via Todo → `scripts/new_app.py`) | Todo files `scripts/new_app.py` command |
| 5. AppMaker self-serve (external repo) | User via UI → `POST /api/appmaker/github/create-app` | Worker (via Todo → `POST /api/appmaker/github/scaffold`) | Todo files the follow-up scaffold call |
| 6. Model Builder promotion | Committing user → `commit.post.ts` `createRecord('Project')` | Nobody automatically (no slug) | None — orphan, outside slug parity |

---

## Decisions (Silas, 2026-07-04)

1. **Auto-Todo on Project creation**: server-side hook in the Project API route. DECIDED (pre-split wording: "Dream API route").

2. **Who can create Projects?** Unlimited creation for any authenticated user —
   no cap and no role restriction on *creating* projects. The metered thing is not
   creation but **processing**: getting our servers/agents to handle a project's
   updates is a separate, computed charge based on how much processing is expected
   and how often (paid or free tokens on our infrastructure, or the user brings
   their own server/generator and pays nothing). The general "what happens when the
   bots find us" abuse problem is acknowledged but explicitly NOT solved at this
   surface — creation is not where the limitation belongs. DECIDED.

3. **Slug collision handling**: return 409 and prompt for a different slug. DECIDED.

   **Slug naming guideline (Silas)**: two-word slugs are preferred
   (`challenge-center`, `recipe-box`, `coat-dance`). Not a rule — one word or
   three-plus is fine when it genuinely fits — but surfaces that derive slugs
   (UI auto-generation, bot slug derivation) should aim for two words.

4. **roadmap.yaml scaffold template**: DECIDED (Silas, 2026-07-04). Three standard
   milestones mapping the creative lifecycle (outline → brainstorm → roadmap →
   actualization/adjustment → testing → aesthetic polish → completion/delivery):

     - **m1 SHAPE** — outline the idea, gather brainstorms/inspiration, write the
       design brief.
     - **m2 BUILD** — actualize, adjust as reality pushes back, test as you go.
     - **m3 POLISH & SHIP** — aesthetic polish, performance, completion and
       delivery. Outward-facing steps stay human-gated (hard).

   **The scope gate does not block development** (Silas, 2026-07-04): when a new
   project arrives, agents take the idea, build out the design brief, and START
   WORKING immediately. Silas always wants a prompt to establish and confirm
   scope — but as a soft, parallel checkpoint, never a stop sign. Re-establishing
   from a corrected idea is cheap; agents and processing are plentiful; the bias
   is toward making things happen.

   Scaffold ships with m1/m2/m3 and two starter tasks:
     - t-001 "Write the design brief and start building" — ready, NOT gated
     - t-002 "Confirm scope with Silas" — soft needs-human, no dependents; when
       Silas responds, fold his direction into the roadmap and keep moving
