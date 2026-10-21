# Weekly Site Audit — 2026-10-21

Read-and-report run per `projects/global-ui/SITE-AUDIT-AGENT.md`. No live HTTP requests, npm/pnpm
builds, or kind_robots mutations. Cross-checks used static path extraction and grep against the
local read-only checkout of `/home/user/kind_robots/` (`main`@`8b4da1c`, 2026-10-20).
The only write is this report.

## Scope

Active/continuous projects per `project-overrides.yaml`: **28** (26 last week). All have a roadmap.

## Method

For each active roadmap, extracted every `server/api|server/utils|components|stores|pages|utils`
`.ts`/`.vue` path mentioned and checked it exists in kind_robots. Each miss was read in roadmap context.

## Gaps

**None.** 4 apparent misses across 3 projects, none a real gap:

- [emperor-of-dust] `stores/emperorOfDustStore.ts` — named in the done t-019 engine-rebuild note;
  the store is now `stores/emperorFortressStore.ts` (present, with tests). Historical reference.
- [interface-vision] `components/storybook/storybook-mockups.vue` — replaced by
  `storybook-collection/-ending/-life-run.vue` (present). Carried over from last week.
- [interface-vision] `utils/scripts/auditWonderLabPreviews.ts` — done-task note (PR #1434); lives
  outside the scanned path set. Carried over from last week.
- [zuzu-gamebook] `utils/zuzuGamebook/acts/act1-4.ts` — shorthand for `act1.ts`..`act4.ts`, all present.

## Orphans noticed

Same caveat as prior weeks: roadmaps name domain features rather than directory paths, so a
literal-name orphan pass is noisy. No new genuine orphan identified.

## Proposed follow-up tasks (0 of up to 3)

None filed — no path-level gap survived reading in context.

## Summary

28 active projects cross-checked. Zero gaps, zero new tasks.
