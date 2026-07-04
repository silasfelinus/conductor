# Project Creation Surfaces — Spec

Generated: 2026-06-30
Task: kind-robots/t-004

---

## The Invariant

In all cases: `Dream.slug === conductor project directory name`

This is the universal join key. A project exists when both (a) a `roadmap.yaml` at `projects/<slug>/` and (b) a `Dream` with `dreamType: PROJECT` and `slug: <slug>` exist. Either can come first; the system reconciles them.

---

## Surface 1: Conductor File Format

**How a new `roadmap.yaml` triggers Dream creation**

### Flow

1. Worker or Silas creates `projects/<slug>/roadmap.yaml` in the conductor repo (via PR or direct commit)
2. The conductor CI or end-of-cycle sync script (`scripts/sync_projects_to_dreams.py`) runs
3. Sync script reads `project-overrides.yaml` for active slugs
4. For each active slug where no matching `Dream` exists (i.e. `GET /api/dreams?slug=<slug>&dreamType=PROJECT` returns empty), it calls `POST /api/dreams` with:
   ```json
   {
     "dreamType": "PROJECT",
     "slug": "<slug>",
     "title": "<roadmap project: field>",
     "description": "<roadmap notes_from_silas first paragraph>",
     "projectStatus": "ACTIVE"
   }
   ```
5. Sync script logs the creation and continues

**Who writes the Dream:** The sync script, run server-side or as a conductor CI step.  
**Who writes the roadmap:** Worker (by PR) or Silas (direct).  
**Slug enforcement:** The directory name IS the slug; no separate slug field is needed in roadmap.yaml.

### Constraints
- The sync script must never delete a Dream; only create or update
- If a Dream already exists with the same slug (different dreamType), the sync skips it and logs a warning

---

## Surface 2: Kind Robots Front-End

**How a UI action creates a new project**

### Flow

1. Silas (or an authorized user) opens the Kind Robots workspace UI and selects "New Project"
2. UI prompts for: project name (→ `title`), short description, and confirms the derived `slug` (auto-generated from title, editable)
3. On submit, UI calls `POST /api/dreams` with `dreamType: PROJECT`, `slug`, `title`, `description`
4. The API creates the Dream record
5. The API (or a Dream creation webhook) automatically creates a Todo for the Worker:
   ```json
   {
     "title": "Scaffold conductor project for <slug>",
     "description": "New PROJECT Dream created with slug '<slug>'. Create projects/<slug>/roadmap.yaml with at least one ready task.",
     "category": "AGENT",
     "priority": "HIGH"
   }
   ```
6. Worker picks up the Todo in the next cycle and creates `projects/<slug>/roadmap.yaml`
7. Next sync run creates or confirms the Dream ↔ roadmap link

**Who writes the Dream:** User via UI → `POST /api/dreams`  
**Who writes the roadmap:** Worker, triggered by the Auto-Todo in step 5  
**Slug enforcement:** UI derives slug from title (lowercase, hyphenated); user can override before submit

### Pitch needed
- The auto-Todo on Dream creation (step 5) is not yet implemented. This requires either a webhook or a post-create hook in the Dream API route. Pitch: "Add auto-Todo on PROJECT Dream creation" to kind-robots pitches.

---

## Surface 3: LLM (Wishmaster or Other Bots)

**How a bot creates a new project from a wish or instruction**

### Flow

1. User sends a wish or instruction to Wishmaster (or another authorized bot): "Start a new project for a podcast website"
2. Bot parses intent: output type = PROJECT, extracts `title` and `description`
3. Bot derives a slug from the title (lowercase, hyphenated, unique check via `GET /api/dreams?slug=<slug>`)
4. If slug is unique: bot calls `POST /api/dreams` with `dreamType: PROJECT`, `slug`, `title`, `description`
5. Same auto-Todo as Surface 2 step 5 is created
6. Bot confirms to the user: "Started project 'podcast-website'. The Worker will scaffold the roadmap next cycle."

**Who writes the Dream:** Bot via `POST /api/dreams` using bot's JWT  
**Who writes the roadmap:** Worker, triggered by the Auto-Todo  
**Slug enforcement:** Bot generates slug, checks uniqueness, retries with suffix if collision (e.g. `podcast-website-2`)

### Auth requirement
- The bot must have a user JWT with permission to create Dreams (any logged-in user can create public Dreams)
- The bot must NOT directly write to the conductor repo; it uses the Auto-Todo → Worker pattern

### Pitch needed
- Same auto-Todo on PROJECT Dream creation (same pitch as Surface 2)
- Wishmaster needs a slug-uniqueness check helper

---

## Reconciliation (Any Surface)

The sync script (`scripts/sync_projects_to_dreams.py`) is the reconciler:

| Situation | Action |
|---|---|
| `roadmap.yaml` exists, no Dream | Create Dream via POST /api/dreams |
| Dream exists, no `roadmap.yaml` | Log warning; Worker Todo triggers scaffold |
| Both exist, slug matches | Update Dream fields from roadmap (title, description, projectStatus) |
| Slug mismatch | Log error; do not rename either side; flag for Silas |

The reconciler runs:
- At the end of every Worker cycle
- As a CI step on PRs that touch `projects/` or `project-overrides.yaml`

---

## Summary Table

| Surface | Who creates Dream | Who creates roadmap | Trigger for other side |
|---|---|---|---|
| Conductor file | sync_projects_to_dreams.py | Worker or Silas | Dream created automatically on next sync |
| Kind Robots front-end | User via UI | Worker (via Auto-Todo) | Auto-Todo created on Dream creation |
| LLM (Wishmaster) | Bot via API | Worker (via Auto-Todo) | Auto-Todo created on Dream creation |

---

## Decisions (Silas, 2026-07-04)

1. **Auto-Todo on Dream creation**: server-side hook in the Dream API route. DECIDED.

2. **Who can create PROJECT Dreams?** Unlimited creation for any authenticated user —
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
