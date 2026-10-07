# Weekly Site Audit — 2026-10-07

Read-and-report run per `projects/global-ui/SITE-AUDIT-AGENT.md`. No live HTTP requests, npm/pnpm
builds, or kind_robots mutations. Cross-checks used static path extraction and grep against the
local read-only checkout of `/home/user/kind_robots/` (`main`@`19375c3`, 2026-10-06).
The only writes are this report.

## Scope

Active projects per `project-overrides.yaml`: **33** (22 last week). All have a roadmap. New to the
active set: music-video, comic-creator, kr-solitaire, kr-adventures, kind-oracle, pocket-pet-robot,
evolve-rebel-button, comic-film, robot-mashup-flipbook, robot-sound-garden, kind-trivia-trail,
kind-lantern-garden, robot-species-sorting-quiz, kind-daily-riddle, zuzu-lair, kind-nonogram-gallery,
zuzu-showdown (some replace projects no longer active, e.g. lora-ingestion, scene-animator).

## Method

For each active roadmap, extracted every `server/api|server/utils|components|stores|pages|utils`
`.ts`/`.vue` path mentioned and checked it exists in kind_robots. Each miss was read in roadmap
context. Also ran a directory-level orphan pass over `components/*` and `server/api/*`.

## Gaps

**None new.** 10 apparent misses across 8 projects; 9 are identical to last week's already-explained
set (retired `mission-accrual-page.vue` / `missionAccrual.ts` / its test; removed
`artArchiveMediaPaths.ts`; renamed `pages/admin/art-archive.vue` and `pages/play/mandarin.vue`;
`curate-request.post.ts`, `store/checkout.post.ts`, `taskmasterStore.ts`,
`taskmaster-sample-tasks.vue` named in notes explaining deletions/corrections).

The one new miss is **not a gap**: `utils/comicFilmShots.ts` (comic-film) is the planned
deliverable of `comic-film/t-004` (`status: ready`), a not-yet-built pure util.

## Orphans noticed

The literal-name grep is still noisy: roadmaps name domain models/features rather than directory
paths, so `components/*` (e.g. `academy`, `arcade`, `comics`, `wonderlab`) and `server/api/*` (e.g.
`karma`, `mana`, `rewards`, `todos`, `forum`, `grants`, `social`) show as unreferenced while clearly
belonging to active or finished work. `botcafe` and `newsletter` remain tied to finished projects.
No new genuine orphan identified; a model-name-aware pass is still the prerequisite for filing any.

## Proposed follow-up tasks (0 of up to 3)

None filed — no path-level gap survived reading in context.

## Summary

33 active projects cross-checked. Zero new gaps, zero new tasks. Fast-growing active set
(+17 projects in a week) is covered by roadmaps whose referenced surfaces either exist or are
explicitly planned.
