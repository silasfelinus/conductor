# Weekly Site Audit — 2026-09-23

Read-and-report run per `projects/global-ui/SITE-AUDIT-AGENT.md`. No live HTTP requests, git
mutations against `kind_robots`, or npm/pnpm builds were run; all cross-checks used
Glob/Grep/direct file reads against a local read-only checkout of `/home/user/kind_robots/`
(fast-forwarded to `origin/main`@`3e667b3`, 2026-09-22T23:54Z, before scanning). The only writes
are this report and one new roadmap task.

## Scope

Active projects per `project-overrides.yaml` (`status: active`, cross-checked fresh this
session): **22** — appmaker, art-archive, butterfly-gallery, coat-dance, coloring-book,
conductor, conductor-app, cthulhuquarium, digital-storefront, humboldt-scoop-cms, kind-economy,
kind-robots, kindrobots-unraid, lora-ingestion, mandarin-tutor, media-watchlist, model-builder,
rainbow-butterflies, ruler-hooked, scene-animator, storybook, text-generation.

Three more than the 2026-09-16 audit's 19: `art-archive`, `butterfly-gallery`, and
`mandarin-tutor` all flipped to `active` in the intervening week (per-project rationale is
recorded in `project-overrides.yaml`, not repeated here). All 22 have a
`projects/<slug>/roadmap.yaml`.

## Method

For each of the 22 active roadmaps, statically extracted every `server/api/**/*.ts`,
`server/utils/**/*.ts`, `components/**/*.vue`, `stores/**/*.ts`, `pages/**/*.vue`, and
`utils/**/*.ts` path mentioned anywhere in the roadmap text (285 raw path mentions,
de-duplicated per project) and checked each against the current `/home/user/kind_robots/`
checkout. Every "missing" hit was then read in its roadmap context (not just path-existence)
before being counted as a real gap, same discipline as the prior four audits. Also ran the
directory-level orphan pass: every top-level `components/*` (46 dirs) and `server/api/*` (66
dirs) directory checked against the full text of *all* roadmaps (active and inactive, 285
mentions across the corpus), to catch backend/UI surfaces with zero roadmap coverage anywhere.

## Gaps

**None new.** Every apparent "missing" hit from the static scan (7 across 6 projects) resolved
to one of:

- **Already tracked and closed correctly** (repeat findings from prior audits, re-verified
  still accurate): `kind-robots/t-095` (`components/abandonware/butterfly/store-butterfly.vue`,
  the directory disappearance) and `kind-robots/t-103` (`character-flip-card.vue`, orphaned
  duplicate) are both `status: done`, and the files genuinely don't exist in the current
  checkout — resolution still holds a week later.
- **Already-known non-finding, re-verified**: `kind-robots/t-051`
  (`server/api/conductor/curate-request.post.ts`) is `status: done`; the task title itself IS
  the "investigate the disappearance" record, not a live surface claim.
  `digital-storefront/t-036` (`server/api/store/checkout.post.ts`, `status: done`) already
  corrected this to the real path (`server/api/stripe/checkout.post.ts`) on 2026-08-02; the
  "missing" hit is the task's own title documenting the correction.
- **Regex false positive, `utils/scripts/verifyXyz.ts`**: a generic placeholder name in a
  `kind-robots` task note describing a whole class of narrow textual-checker scripts ("matching
  the existing `utils/scripts/verifyXyz.ts` pattern"), not a literal path — same as every prior
  audit.
- **New this week — same false-positive shape, one level deeper**:
  `kind-robots`'s note on `character-flip-card.vue` (t-103) also mentions
  `components/content/characters/character-interact.vue` in the same paragraph, contrasting it
  with the *real, current* file at `components/characters/character-interact.vue` (55 lines,
  confirmed present). The note is explicit that the `content/characters/` path is the deleted
  pre-split original being discussed for contrast, not a live claim — read in full before
  counting, this resolves the same way as the `verifyXyz.ts` case: the regex matched a path
  named *inside a note explaining why that exact path is gone*.
- **Deliberate, already-self-documented renames (both in newly-active projects)**:
  `art-archive`'s `pages/admin/art-archive.vue` moved to `pages/art-archive.vue` via
  kind_robots#2926 (2026-09-20) — the roadmap's own "ROUTE UPDATE 2026-09-20" note names the
  move and the new nav placement; the new path exists, confirmed. `mandarin-tutor`'s
  `pages/play/mandarin.vue` moved to `pages/play/mandarin/index.vue` (plus a sibling
  `learn/<key>` route) as part of a documented restructure; the new path exists, confirmed.
  Both are exactly the "roadmap already caught up with its own rename" pattern the 2026-09-16
  audit found for the `taskmaster` retirement — not a gap, a correctly-self-corrected roadmap.
- **Expected fallout of the already-documented `taskmaster` retirement** (unchanged from last
  audit): `appmaker`'s `components/taskmaster/taskmaster-sample-tasks.vue` and `storybook`'s
  `stores/taskmasterStore.ts` are both historical-architecture mentions inside investigative
  notes, predating taskmaster's 2026-09-14 merge into storybook.

The ecosystem's self-auditing loop continues to hold up under a third independent check —
including the two brand-new active projects (`art-archive`, `mandarin-tutor`) each having
already self-corrected their own roadmap after a real file move, before this audit ever looked.

## Orphans noticed

Directory-level pass (46 `components/*` dirs, 66 `server/api/*` dirs) found every
`components/*` top-level directory referenced somewhere in the roadmap corpus — zero orphans
there, same as 2026-09-16. Three `server/api/*` directories were not: `botcafe`, `newsletter`,
`dream-relations`. `botcafe` and `newsletter` read as belonging to already-`finished` projects
(brainstorm, newsfeed) and are out of the active-project scope this audit covers — unchanged
from last week. `agent-credentials`, last week's genuine orphan, no longer appears: it's now
tracked in `rainbow-butterflies/roadmap.yaml` (t-053, filed by the 2026-09-16 audit) — the loop
closing on its own finding, confirmed.

**`dream-relations` is a genuine new orphan**: `server/api/dream-relations/index.get.ts`
(list), `index.post.ts` (create), and `[id].delete.ts` (revoke) implement the `DreamRelation`
Prisma model (`prisma/schema.prisma`) — typed edges between two `Dream` rows with a
`relationType` — guarded by `requireApiUser`, and it isn't a dead/speculative surface: it's
wired into real UI (`components/dreams/dream-relationship-gallery.vue`,
`components/dreams/dream-narration.vue`, `components/navigation/workspace-narrator.vue`,
`stores/dailyDreamArchiveStore.ts`). None of that is named anywhere in `dream-cycle`'s roadmap
(the project that otherwise owns Dream-related surfaces), despite `dream-cycle` being the
project with by far the heaviest Dream-domain roadmap text in the whole corpus. Read all three
handlers — the surface looks complete and correctly guarded, same as every genuine orphan this
audit series has found so far; this is a documentation gap, not a code defect.
`dream-cycle` is `continuous` lifecycle (not in this week's `active` scan set), but the orphan
pass deliberately checks the *full* roadmap corpus (active + inactive/continuous) for exactly
this reason, and the fix belongs with the project that actually owns the surface.

## Proposed follow-up tasks (1 of up to 3)

1. **dream-cycle/t-033** — "Add roadmap tracking for the `server/api/dream-relations/` surface
   (DreamRelation CRUD)" — `status: ready`, `stakes: reversible`, `owner: null`. Landed in
   `projects/dream-cycle/roadmap.yaml`, milestone m2 (TIGHTEN — API audit), alongside the
   project's other API-surface documentation work.

Only one task was filed — same judgment as the prior two audits: every path-level "gap" from
the static scan investigated to an already-resolved, already-expected, or false-positive state,
and the directory-level pass turned up exactly one genuine, previously untracked surface.

## Summary

22 active projects in scope (up from 19 last week — `art-archive`, `butterfly-gallery`, and
`mandarin-tutor` newly active). All 22 were fully cross-checked against
`/home/user/kind_robots/`. Zero new path-level gaps — every apparent miss traced to an
already-closed audit finding, a deliberate and already-self-documented rename, or a regex false
positive (including a new one-level-deeper case: a note explaining a deletion that names the
deleted path). One new orphan found and filed: `dream-cycle/t-033` for the untracked
`dream-relations` API surface. Last week's genuine orphan (`agent-credentials`) confirmed closed
by its own filed task.
