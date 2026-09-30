# Weekly Site Audit — 2026-09-30

Read-and-report run per `projects/global-ui/SITE-AUDIT-AGENT.md`. No live HTTP requests, npm/pnpm
builds, or kind_robots mutations. Cross-checks used static path extraction and grep against the
local read-only checkout of `/home/user/kind_robots/` (`origin/main`@`cff316b`, 2026-09-29).
The only writes are this report.

## Scope

Active projects per `project-overrides.yaml`: **22** — kindrobots-unraid, conductor, kind-robots,
text-generation, humboldt-scoop-cms, model-builder, digital-storefront, storybook, media-watchlist,
conductor-app, coat-dance, appmaker, ruler-hooked, lora-ingestion, kind-economy, cthulhuquarium,
scene-animator, mandarin-tutor, rainbow-butterflies, art-archive, butterfly-gallery,
tzaddik-gallery. All have a roadmap. (`tzaddik-gallery` is new to the active set since 2026-09-23.)

## Method

For each active roadmap, extracted every `server/api|server/utils|components|stores|pages|utils`
`.ts`/`.vue` path mentioned and checked it exists. Each miss was read in roadmap context before
being counted. Also ran a directory-level orphan pass over `components/*` and `server/api/*`
against the full roadmap corpus.

## Gaps

**None new.** All 15 apparent misses across 7 projects resolve to already-known shapes:

- **Deliberate retirement, already tracked**: `components/pages/mission-accrual-page.vue`,
  `server/utils/missionAccrual.ts`, `utils/scripts/verifyMissionAccrual.test.ts`
  (kind-robots, kind-economy) — retired by kind_robots#2669 / #3008; roadmap notes name the removal.
- **Deliberate removal, self-documented**: `server/utils/artArchiveMediaPaths.ts` (art-archive) —
  removed by kind_robots#3006; the roadmap cites it only as a forbidden pattern.
- **Deliberate rename, roadmap already caught up**: `pages/admin/art-archive.vue` ->
  `pages/art-archive.vue`; `pages/play/mandarin.vue` -> `pages/play/mandarin/index.vue`.
- **Notes explaining a deletion / prior audit findings** (unchanged): `store-butterfly.vue`,
  `character-flip-card.vue`, `components/content/characters/character-interact.vue`,
  `curate-request.post.ts`, `server/api/store/checkout.post.ts` (corrected to
  `server/api/stripe/checkout.post.ts`), `stores/taskmasterStore.ts`,
  `components/taskmaster/taskmaster-sample-tasks.vue`.
- **Regex false positives**: `utils/scripts/verifyXyz.ts` (placeholder) and
  `utils/scripts/verifyStorybookPageChoiceGroupGuard.ts` (storybook note listing guards slated for
  deletion in the legacy storybook-page teardown — a planned-deletion list, not a live claim).

## Orphans noticed

`components/*`: every top-level directory is referenced somewhere in the corpus. `server/api/*`:
`botcafe` and `newsletter` still belong to already-`finished` projects (unchanged). Last week's
orphan `dream-relations` is now closed by `dream-cycle/t-033` (`status: done`). A looser
route-name grep (`/api/<dir>`) lists ~25 further `server/api` directories with no literal route
mention (e.g. `rewards`, `karma`, `mana`, `grants`, `todos`, `forum`); this grep is noisy because
roadmaps usually name the domain model rather than the route path, so none were filed — see
follow-up below.

## Proposed follow-up tasks (0 of up to 3)

None filed. Same judgment as prior weeks: every path-level gap was already resolved or a false
positive, and the one genuine orphan from last week is closed. The literal-route-name orphan list
above needs a model-name-aware pass to separate real coverage gaps from vocabulary mismatch; a
follow-up audit can refine that before any task is filed.

## Summary

22 active projects cross-checked. Zero new gaps, zero new tasks. Prior findings
(`agent-credentials`, `dream-relations`) confirmed closed by their filed tasks.
