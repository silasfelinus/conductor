# Weekly Site Audit — 2026-11-25

Read-and-report run per `projects/global-ui/SITE-AUDIT-AGENT.md`. No live HTTP requests, builds or
kind_robots mutations. Static path extraction + grep against the local checkout of
`/home/user/kind_robots/` (`main`@`8e17dd2c`, 2026-11-24; 169 commits since the shallow root on
2026-11-23). Writes: this report only.

## Scope

Active/continuous projects per `project-overrides.yaml`: **29** (down from 35 — brainstorm,
zuzu-gamebook, slime-city, emperor-of-dust and others are no longer active and were skipped). Same
three passes as last week:

1. Every `server/api|server/utils|components|stores|pages|utils|composables` `.ts`/`.vue` path named
   in a roadmap task — checked for existence.
2. Every `/api/...` route named in an open task (`ready`/`claimed`/`review`/`waiting`/`needs-human`)
   — matched against `server/api/**` (dynamic segments and method suffixes allowed).
3. Utils importer check — no newly named utils this week.

## Gaps

5 apparent misses across 4 projects; **none is real**:

- [every-villain-tactics] t-018 (`review`) `/api/art/images/{id}/file` — scanner artifact from the
  `{id}` brace placeholder; `server/api/art/images/` exists and serves the route.
- [interface-vision] `components/storybook/storybook-mockups.vue` (t-001),
  `utils/scripts/auditWonderLabPreviews.ts` (t-094), [playbook-kit]
  `utils/playbookKit/games/thisMeansWarp.ts` (t-002, renamed Space Couch), [ruler-hooked]
  `ruler-hooked-timing-bar.vue` (t-033) — all `done`, carried over, historical (see 2026-11-11 and
  2026-11-18 reports).

## Orphans

Surfaces added to `pages/`, `server/api/` and `stores/` since the 2026-11-23 shallow root:

- `server/api/ruler-hooked/account-save.{get,put}.ts`, `stores/rulerHookedAccountStore.ts` —
  private account reign backup/restore; traced to ruler-hooked t-067 (note: "explicit private account
  backup and restore of reign slots and scrapbook").
- `stores/rulerHookedDisplayStore.ts` — reading-comfort preferences, kind_robots#5723, ruler-hooked
  t-067.

No orphan needs a task.

## Proposed follow-up tasks (0 of up to 3)

None filed: no real gap. The standing kaizen (commit the three-pass scan as a script) stays unfiled
while `global-ui` and `conductor` remain `finished`.

## Summary

29 active projects cross-checked. Zero real gaps, zero orphans, zero tasks filed.
