# Shared-layer reuse map

Static audit completed 2026-07-19 of `silasfelinus/kind_robots` (schema + `components/`,
`stores/`, `scripts/` in this repo) against the ownership table in `DESIGN-BRIEF.md` and
the six "duplication risks to audit first" it lists. Builds on `ASSET-COVERAGE-MATRIX.md`
(t-003), `FRONTEND-SURFACE-MAP.md`/`TAB-INTEGRATION.md` (t-007/t-008), and
`BOT-PARITY-SPEC.md` (t-004) rather than re-deriving them. Per `DESIGN-BRIEF.md`'s
non-goals, this does not implement fixes — `t-006` routes confirmed gaps into small
tasks on the owning project's roadmap.

Method: read `prisma/schema.prisma` model-by-model against the primitives list in
`t-005`'s note (galleries, project menus, narrator threads, pack/content permissions,
task surfaces, roadmap milestones, ArtCollections, bot images, project metadata), then
grepped `components/` and `scripts/` for the areas the schema alone couldn't confirm.
Live app behavior, DB row counts, and anything needing a running server were out of
scope — filesystem/schema-verifiable only, same limitation `ASSET-COVERAGE-MATRIX.md`
already documents.

## Ownership table

| Primitive | Canonical owner | Duplication found? | Confidence |
| --- | --- | --- | --- |
| Project identity/metadata | `Project` model (own top-level table, not a `Dream`) | No — `DreamType` enum re-verified to have no `PROJECT` value; single row per project, joined by `conductorSlug` | High |
| Agent task queue | Conductor `roadmap.yaml` | No | High |
| User-facing one-off tasks | `Todo` model (`category: AGENT\|KAIZEN\|HONEYDO\|DESIRED_FEATURE`) | No — cleanly separate from roadmap tasks (no dependency graph, archives on done, already documented in `AGENTS.md`'s Todos section) | High |
| Friendly project progress | `Project.goal` (text only) | **Gap, not duplication** — no milestone-level data reaches the DB at all (see below) | High |
| Project navigation/menu (bot-driven) | `NarratorThread.starterPrompts` | No — single mechanism per `BOT-PARITY-SPEC.md` §4; no competing per-project menu table found in schema | High |
| Project navigation (tabs/routes) | `dashboardConfigs` in `stores/helpers/dashboardHelper.ts` | No — single registry per `TAB-INTEGRATION.md` | Medium (not re-audited beyond confirming the file exists and is the one `TAB-INTEGRATION.md` names) |
| Bot avatar/expression images | `Bot.avatarImage` + `ExpressionMedia` | No | High |
| Inspiration/gallery images | `ArtCollection` + `ArtImage` | No, single model | High |
| **Record-grid display components ("galleries")** | none — ad hoc per model | **Yes — confirmed** | High |
| **Content visibility / sharing** | none yet — pending Grant-model pitch | **Yes — confirmed, already documented** | High |

## Confirmed duplication: gallery components

`components/` has 22 files matching `*-gallery.vue` (`art-gallery.vue`,
`character-gallery.vue`, `dream-gallery.vue`, `reward-gallery.vue`, `bot-gallery.vue`,
`scenario-gallery.vue`, `server-gallery.vue`, `checkpoint-gallery.vue`,
`theme-gallery.vue`, `achievement-gallery.vue`, `icon-gallery.vue`,
`friend-gallery.vue`, `chat-gallery.vue`, and others), each independently implementing
the same shape rather than composing a shared base:

- `character-gallery.vue`, `reward-gallery.vue`, and `dream-gallery.vue` each define
  their own `variant` prop (`grid` / `row` / `dropdown` / `dashboard` / …), their own
  `filtered<Model>` computed list, and near-identical
  `grid-template-columns: repeat(auto-fill, minmax(...))` CSS — checked directly by
  grep, not inferred.
- `components/ui/ui-gallery.vue` is **not** a shared base despite the name — it's
  global-ui's living style-guide page (the DaisyUI kitchen sink at `/ui`), a different
  sense of "gallery" entirely. None of the model-specific gallery components import or
  extend it.
- Scale: `art-gallery.vue` (1624 lines), `dream-gallery.vue` (1035 lines),
  `character-gallery.vue` (717 lines), `reward-gallery.vue` (676 lines) — each large
  enough that the duplicated filter/variant/grid logic is a real maintenance cost, not
  a trivial coincidence.

**Recommendation:** a `global-ui` task to extract a generic record-gallery
composable/component (grid/row/dropdown variant switch, search/filter slot, empty-state
slot) that model-specific galleries wrap instead of reimplementing. Do not attempt this
as one big-bang refactor of all 22 files — route it as a `global-ui` primitive plus an
opt-in migration path, so existing galleries aren't forced to change in the same PR that
introduces the shared component.

## Confirmed gap (not duplication): roadmap milestones don't reach the DB

`DESIGN-BRIEF.md`'s ownership table lists "Project `goal` and roadmap milestones" as the
friendly-progress layer, but `scripts/sync_projects.py` (`build_project_payload`) only
ever sends `goal` (plus `title`/`description`/`status`/`priority`/`liveUrl`/`channelKey`/
`tabKey`/`repoUrl`) — there is no `milestones` field on the `Project` Prisma model and
no per-milestone data leaves this repo today. This isn't two owners competing (only
`roadmap.yaml` has milestone data at all), it's a real front-end capability gap: nothing
in kind_robots can currently render "3 of 6 milestones complete" for a project — only
the single free-text `goal` blurb. Flagging for `t-006` rather than speculatively adding
a schema field here, since a milestone-progress UI feature should be scoped and owned by
whichever project (`kind-robots` or `global-ui`) actually wants to build that display.

## Confirmed duplication risk: content visibility / sharing

Already fully documented in `projects/kind-robots/SHARING-SPEC.md` (2026-07-16) — this
audit independently re-verified its two headline facts against the current schema
rather than taking them on faith:

- No `Grant`/`Permission`/`Share`/`ACL` model exists. Re-grepped `prisma/schema.prisma`
  for `isPublic` and it still appears on 19+ models (`ArtImage`, `ArtCollection`, `Bot`,
  `Character`, `Chat`, `Dream`, `Project`, `Facet`, `NarratorTopic`, `Resource`,
  `Reward`, `Scenario`, `Server`, `Theme`, `User`, and more) — binary owner-or-everyone,
  no middle state.
- `Project` (this audit's own focus) carries the same pattern: a bare `isPublic Boolean
  @default(true)` with no grant/ACL relation.

This is the single most load-bearing duplication risk in the ecosystem: `packmaker`
(DLC packs) and `digital-storefront` both have tasks explicitly blocked/waiting on the
Grant-model design landing (see `SHARING-SPEC.md`'s "Origin" section and
`CONTROL.md`'s 2026-07-17 pitch note). **Recommendation: do not let this audit's
`t-006` spin up a second sharing design** — the design work already exists and is
further along than anything this task would produce. `t-006` should route straight to
prioritizing the pitch's approval, not re-litigating the model shape.

## Areas checked with no action needed

- **Bot images** — `ExpressionMedia` (20-slot emotion/action set, unique per
  `[botId, expressionKey]`) is the only portrait storage found; no competing per-bot
  image table. Matches `BOT-PARITY-SPEC.md` exactly.
- **Project ↔ bot linkage** — `Project.managerBotId → Bot.id` is the only project-bot
  FK in the schema; no parallel "project assistant" table.
- **Task surfaces** — `Todo.category` (`AGENT`/`KAIZEN`/`HONEYDO`/`DESIRED_FEATURE`) is
  a personal/interrupt-style list distinct in shape (no dependency graph, no milestone
  grouping, archives on completion) from Conductor's `roadmap.yaml` task queue. Already
  correctly separated per `AGENTS.md`'s Todos section — no fix needed, just worth
  recording here so a future audit doesn't flag it as a false positive.
- **ArtCollections/inspiration images** — single `ArtCollection` model, already the
  documented canonical owner; the only duplication touching this area is the gallery
  *component* pattern above, not the underlying data model.

## Follow-ups for t-006

1. `global-ui`: extract a shared record-gallery primitive (grid/row/dropdown variants +
   filter/empty-state slots); migrate existing `*-gallery.vue` files opportunistically,
   not all at once.
2. `kind-robots` (or wherever `SHARING-SPEC.md`'s pitch is tracked): prioritize getting
   the Grant-model pitch in front of Silas for approval — `packmaker`/
   `digital-storefront` tasks are already blocked on it, and this audit found nothing
   that changes the spec's own recommended shape.
3. Optional, lower priority: if a project wants milestone-level progress in the
   front end (not just the `goal` text), that project should scope a small task to add
   a synced `milestones` field/endpoint rather than assuming one already exists.
