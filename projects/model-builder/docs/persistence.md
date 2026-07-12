# Model Builder — durable run persistence (t-004)

**Repo:** `kind_robots` · **PR:** #188 · **Date:** 2026-07-12
**Directed by:** Silas (full vertical slice, merge when CI green)

Model Builder runs were client-only (`localStorage`). This lands the durable
orchestration schema, the run/item APIs, and swaps the store onto them — so a
run now resumes across devices and sessions. Advances milestone **m2** and
realizes the core of roadmap **t-004** (and the persistence half of t-014).

## Schema (additive — `prisma/model-builder.prisma`)

Four tables, migration `20260712120000_add_model_builder_tables`:

- **ModelBuildRun** — owner (`userId` scalar), status, source type/id/label +
  `sourceSnapshot` (JSON), recipe key/version, `selections`/`usageInfo` (JSON),
  cancellation.
- **ModelBuildItem** — belongs to a run; output key, action
  (CREATE/UPDATE/ASSET_ONLY), generation kind, quantity index, `stageStatuses`
  (the four-gate map, JSON), pitch/fields/prompt drafts, `targetType`/`targetId`
  for eventual writes, `idempotencyKey` (unique) for the future commit, artImageId.
- **ModelBuildArtifact** — a generated output with provenance
  (provider/model/seed/prompt/dims/workflow), draft vs promoted path, review state.
- **ModelBuildRevision** — append-only history; each draft edit records
  previous/next payloads + actor.

Design choices: external references (`userId`, `sourceId`, `artImageId`,
`targetId`) are **plain scalar `Int` columns with no foreign key**, so the tables
stay self-contained and additive — no reverse-relation edits to `User`/`ArtImage`.
The only FKs are the internal run→item→artifact/revision chain, which **cascades
on delete**. Catalog-coupled fields (`sourceType`, `recipeKey`, `outputKey`,
`generation`) are `VarChar`, not enums, so evolving the front-end recipe catalog
needs no migration. The migration is four `CREATE TABLE`s + internal FKs only.

## API (`server/api/model-builder/*`)

Mirrors `server/api/projects` idioms (`requireApiUser`, owner/admin guard,
`{ success, data, message }` envelope, JSON tri-state):

- `runs/` — list (mine) · create (run + nested items) · get · patch
  (status/cancel) · delete (cascade).
- `items/[id]` PATCH — stage + draft updates; auto-appends a revision on draft
  change.
- `items/[id]/artifacts` POST — record a generated artifact.

## Store

`modelBuilderStore` mutates locally (optimistic) then persists in the background.
`startRun` POSTs a durable run; `resumeRun` rehydrates the remembered or newest
non-cancelled run; stage/draft edits PATCH the item; generate records an
artifact. The `BuildRun`/`BuildItem` shapes are unchanged, so the components were
untouched.

## Boundaries / still deferred

- **COMMIT stays preview-only** — the durable canonical create/update/link/promote
  and DRAFT_EARLY target rows are t-013/t-015, still gated.
- Text/plan/video/3D generation kinds (t-012) remain unwired.
- No public revisions API (revisions are written server-side).

## Verification

- Pre-merge: CI `prisma generate` (schema validity) + whole-project `vue-tsc`
  (routes + store) + Vercel preview build.
- Post-merge (manual, prod): create a run → reload → resumes from server;
  generate → artifact row; second session sees the run.
