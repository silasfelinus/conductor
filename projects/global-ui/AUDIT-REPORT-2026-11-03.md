# Weekly Site Audit — 2026-11-03

Read-and-report run per `projects/global-ui/SITE-AUDIT-AGENT.md`. No live HTTP requests, builds or
kind_robots mutations. Static path extraction + grep against the local checkout of
`/home/user/kind_robots/` (`main`@`a842b25`, 2026-11-02). Writes: this report and one roadmap task.

## Scope

Active/continuous projects per `project-overrides.yaml`: **34** (28 last week). Every
`server/api|server/utils|components|stores|pages|utils` `.ts`/`.vue` path named in each roadmap was
checked for existence.

## Gaps

4 apparent misses across 4 projects; one is real:

- [ruler-hooked] **REAL** `components/ruler-hooked/ruler-hooked-timing-bar.vue` — described as the
  fishing control in done tasks t-026/t-033, absent from code; `utils/rulerHooked/timingBar.ts`
  exists but only its selftests import it, and the encounter uses a plain tap button. Task filed.
- [playbook-kit] `utils/playbookKit/games/thisMeansWarp.ts` — planned output of ready t-002, not yet built.
- [emperor-of-dust] `stores/emperorOfDustStore.ts` — historical; now `emperorFortressStore.ts`. Carried over.
- [interface-vision] `components/storybook/storybook-mockups.vue`, `utils/scripts/auditWonderLabPreviews.ts`
  — historical / outside scanned set. Carried over.

## Orphans

Roadmaps name domain features rather than paths, so a literal orphan pass stays noisy; the one
concrete orphan is `timingBar.ts` above.

## Proposed follow-up tasks (1 of up to 3)

- ruler-hooked/t-053 — reconcile the timing bar (wire it in, or delete the dead util and fix notes).

## Summary

34 active projects cross-checked. One real gap, one task filed.
