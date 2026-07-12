# Model Builder — front-end scaffold handoff

**Repo:** `kind_robots`
**Branch:** `claude/model-generator-scaffold-lr3nhb`
**Date:** 2026-07-12
**Directed by:** Silas (session task: "scaffold the model-generator project… front end setup, if not fully manifested up to the media-generator")

This documents the first front-end slice of the Model Builder, landed directly
in `kind_robots`. It advances roadmap milestones **m1** (contract → concrete
recipe catalog) and **m2** (front-end workflow), and stands up the UI shell that
milestone **m4** (t-014) will wire to durable APIs.

## What landed

All in `kind_robots`, following house conventions (Pinia setup stores,
`performFetch`/`handleError`, daisyUI + Tailwind, `kind-icon:` set, Nuxt Content
page + auto-imported MDC component):

| File | Purpose |
|---|---|
| `stores/helpers/modelBuilderRecipes.ts` | Static catalog: the four gated stages, seven source types (with list endpoints + eligible recipes), five recipes, and the selectable output catalog — grounded in `PROJECT-BRIEF.md`'s recipe matrix. |
| `stores/modelBuilderStore.ts` | `modelBuilderStore` — source loading, recipe/output selection, BuildRun/BuildItem state, gated stage advancement with stale-invalidation, asset generation (delegated to the existing `artStore`), and localStorage resume. |
| `components/model-builder/model-builder-manager.vue` | Shell + step breadcrumb (Source → Recipe → Run) + status banner. Resumes an in-progress run on mount. |
| `components/model-builder/model-builder-source-picker.vue` | Source-type tabs + record grid, loaded live from `/api/{projects,characters,bots,facets,dreams,rewards,scenarios}`. |
| `components/model-builder/model-builder-recipe-selector.vue` | Recipe chips + selectable outputs with per-output quantity for batch/expansion items. |
| `components/model-builder/model-builder-progress-matrix.vue` | Row-per-item × column-per-stage status grid; selects a row into the stage panel. |
| `components/model-builder/model-builder-item-panel.vue` | The four-gate editor for one item: pitch, fields & prompts, generate assets, commit preview. |
| `content/model-builder.md` | The `/model-builder` route (`:model-builder-manager`). |

## How it maps to the roadmap

- **t-001 / t-003 (spec + recipe matrix)** — the recipe catalog encodes the
  source × recipe × output matrix from the brief as typed data the UI drives.
  The prose SPEC.md / RECIPES.md are still worth writing; this is the executable
  shape of them.
- **t-005 (front-end source picker + gated progress matrix)** — substantially
  realized: source picker, recipe/output selector, row-by-stage matrix, and the
  pitch/field/prompt/asset/commit editors all exist and are wired to
  `modelBuilderStore`.
- **t-014 (API, store, first UI slice)** — the store and UI slice exist and the
  GENERATE_ASSETS stage runs a **live** image generation through the existing
  art generator (`artStore.generateCurrentArt`) — this is the "up to the
  media-generator" wiring. The **durable** run APIs and idempotent final COMMIT
  are deliberately **not** built here (see below).

## Deliberate boundaries (what is NOT done — and why)

- **No durable BuildRun/BuildItem persistence.** Run state lives in
  `localStorage` for resume. Server-side orchestration records (t-004) and their
  APIs are a later milestone. No Prisma schema/migration was touched — consistent
  with hard-safety rule 10 and the "no unattended schema work" posture.
- **COMMIT is preview-only.** Approving the commit stage records the final diff;
  it does **not** run the durable create/update/link/promote. The real
  idempotent commit is t-013/t-015 and stays gated. Image assets generated in
  GENERATE_ASSETS *are* persisted as `ArtImage` rows by the existing art
  endpoint (private, `isPublic: false`), but promotion to a canonical model
  field is part of the un-built COMMIT.
- **Only image generation is wired.** `text`, `plan`, `video`, and `three-d`
  output kinds are catalogued and gated but show a "not wired yet" note at the
  generate step — they need the LLM/LTX/Hunyuan3D orchestration from t-012.

## Verification done

- Icon names validated against `assets/icons/*` (the `kind-icon` custom set).
- Component names checked against the global `pathPrefix: false` config —
  `<model-builder-*>` tags resolve by filename, mirroring `<builder-manager>`.
- Source list endpoints confirmed to return `{ success, data: [...] }`.

**Not verified:** full `vue-tsc` typecheck / eslint / a live browser run —
`node_modules` and the generated Prisma client are absent in this session's
environment. Worth a `npm run test` + `npm run dev` pass before merge, and a
click-through of a Character → Art Upgrade → hero run end to end.

## Suggested next tasks

1. Live-run verification: Character source → art-upgrade → generate a hero →
   confirm the ArtImage persists and resume survives a reload.
2. t-004: durable `ModelBuildRun`/`ModelBuildItem` schema + APIs so runs persist
   server-side and cross-device (replace the localStorage layer).
3. t-014 remainder: swap the store's client run state onto those APIs and add
   the real COMMIT execution (t-013) behind the existing human gate.
