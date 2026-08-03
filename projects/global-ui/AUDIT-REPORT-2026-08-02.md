# Weekly Site Audit — 2026-08-02

Per `projects/global-ui/SITE-AUDIT-AGENT.md`, second run under the self-assigning
`role: site-auditor` path (`scripts/select_role.py`). Previous report:
`AUDIT-REPORT-2026-07-26.md` (7 days old, now stale, triggering this run).

**Method:** cross-referenced all 26 `active` (per `project-overrides.yaml`)
conductor project roadmaps against `/home/user/kind_robots/` (API routes, Pinia
stores, Vue components, `prisma/schema.prisma`, page routes) using Glob/Grep only
— no live HTTP requests were made, no npm/pnpm builds run, no dev server started.
Extracted every explicit `server/api/**`, `stores/**`, `components/**`, `pages/**`
path-like token mentioned across all 26 roadmap files (~430 raw mentions, ~220
unique after dedup) and checked each against the current `kind_robots` checkout,
then hand-verified every apparent miss against surrounding roadmap context (task
status, dated notes, later corrections) to separate real gaps from historical
narration (e.g. a "done" task's note describing something that was *deliberately
deleted later*, already documented elsewhere in the same roadmap).

Note on `project-overrides.yaml` since last week: `global-ui` itself flipped
`finished` → its work is done (25/25 tasks); the design-system-adoption follow-on
reopened as the new `interface-vision` project (`status: active`, opened
2026-08-01), which is included in this audit. `davinci` was also reopened
(`active`, 2026-07-31). 26 active projects total this cycle (vs 31 last week) —
the delta is projects flipped to `finished`/`paused`/`retired` since, all
correctly excluded per `project-overrides.yaml`.

## Summary

26 active projects checked. As with last week, the large majority of
roadmap-claimed surfaces exist in code exactly as described. Found **one genuine,
previously-undocumented gap** (a "done" task's shipped file no longer exists, with
no removal note anywhere — unlike every other drift case found, which are already
self-documented), plus **two minor path/filename drift cases** (functionality
still exists, just under a different name/path than the roadmap note says). Also
confirmed one gap from last week's report (`dream-cycle/t-020`, the Daily Dream
page removal) is still correctly open and unresolved — not re-filed, already
tracked.

## Findings

### New gap — undocumented (no removal trail anywhere)

1. **kind-robots** — an 2026-07-14 task ("SHIPPED IN REVIEW") describes building
   `server/api/conductor/curate-request.post.ts` (an admin-gated bridge letting
   the ArtJob trainer panel submit curate requests from the front end). A later
   task (**conductor-app**, 2026-07-20) still references it as a live,
   already-secured endpoint. As of this audit the file does not exist anywhere
   in the current kind_robots checkout — confirmed via Glob/Grep; the only
   remaining trace is a historical comment in
   `utils/scripts/verifyConductorApiAuthGuards.ts` naming it as a past example
   of an accepted auth pattern. Unlike the two drift cases found last week
   (both of which have an explicit removing-migration/PR documented elsewhere
   in the same roadmap), **nothing documents why or when this file went away**.
   Filed **kind-robots/t-051** (ready, reversible) to investigate: confirm
   whether removal was deliberate (find the removing PR/migration, check
   whether the trainer panel's "Request curation" button now silently 404s)
   or whether this is an accidental regression needing a restore.

### Path/filename drift (functionality intact, roadmap note points at the wrong name)

2. **digital-storefront/t-031** — title and note both name the general
   multi-item cart checkout handler as `server/api/store/checkout.post.ts`.
   That file does not exist; `server/api/store/` holds
   `pod-checkout.post.ts`/`product-checkout.post.ts`/`entitlements.get.ts`/
   `download/` instead. The code the task actually describes (sets Stripe
   session `metadata.kind: 'giftshop_checkout'`) is at
   `server/api/stripe/checkout.post.ts` — confirmed by grepping for that exact
   metadata string. Filed **digital-storefront/t-036** (ready, reversible) to
   correct the note so a future reader searching `server/api/store/` for this
   handler doesn't come up empty.

3. **alexa-integration/t-012** — 2026-07-06 note describes shipping
   `components/pages/serendipity-voice-page.vue` at `/serendipity-voice`. That
   exact file no longer exists (`stores/serendipityVoiceStore.ts` does still
   exist). This is a real, already-explained rename, not a regression:
   `project-overrides.yaml`'s `serendipity` retirement note records that the
   story-weaving product which used to own the `/serendipity` name was renamed
   to Taskmaster, freeing the route for this project's voice surface (formerly
   at `/serendipity-voice`), reclaimed the same day via kind_robots commit
   `36a86bf` ("refactor: make Serendipity the canonical voice route"). The
   current file is `components/pages/serendipity-page.vue`. The rename is
   correctly reflected in `project-overrides.yaml` — only t-012's older note
   text is stale. Filed **alexa-integration/t-019** (ready, reversible) to
   update the note.

### Confirmed still-open, already-tracked (not re-filed)

- **dream-cycle/t-020** (filed by last week's audit) — corrects t-013's stale
  "shipped" note for the removed Daily Dream page
  (`components/pages/daily-dream-page.vue`). Re-confirmed this cycle: the file
  still does not exist (closest surviving surface is
  `components/dreams/daily-dream-generator.vue`, a different component). Task
  is still `status: ready`, unclaimed — correctly not duplicated here.

### Low-confidence / not filed

- **kind-robots** — one task's note references `stores/socialStore.ts` as a
  precedent pattern (dated 2026-07-16). The file no longer exists — most likely
  removed alongside `social-publisher.vue` by the same
  `remove_social_publishing` migration (2026-07-18, per digital-storefront/t-027),
  since the note predates that removal by two days. `stores/navStore.ts`, the
  other file the same note cites, does still exist. Historical reference in an
  already-`done` task; not actionable, not filed.
- **ruler-hooked** — an already-`done` task's original-plan text (superseded by
  the actual shipped implementation, confirmed working via a later task in the
  same roadmap) mentions reusing a `stores/compositionStore.ts` localStorage
  pattern that was never built under that name. The real implementation ships
  its own local-storage handling directly in `rulerHookedStore.ts` instead.
  Planning text overtaken by events, not a live gap.
- **newsfeed/t-018**'s note mentions `components/code/`, `components/composition/`,
  and `components/giftshop/social-publisher.vue` as "untracked leftover files"
  parked during that session's diff — explicitly described as pre-existing,
  unrelated cruft in the working tree at the time, not shipped surfaces. None
  exist in the current checkout. No action needed; the note already frames them
  as noise.
- **interface-vision** — several `note:` fields *describe deleting* things
  (`components/art/art-reactions.vue`, `stores/linkStore.ts`,
  `components/icons/kind-icons.vue`) as part of already-`done` cleanup tasks.
  These correctly don't exist — the notes are recording intentional removals,
  not claiming the files are live. Grepped as false-positive "gaps" initially;
  excluded after reading context.

### Orphans (code exists, not named in any active roadmap — informational only)

- `server/api/newsletter/`, `server/api/conversations/`, `server/api/contenders/`
  — no active project's roadmap mentions any of these.
- `components/characters/`, `components/tasks/`, `components/stages/`,
  `components/servers/`, `components/ui/`, `components/builder/` — same, no
  active-roadmap mention.
- `server/api/challenges/`, `server/api/karma/` — likely owned by
  `challenge-center`, which is `status: finished` in `project-overrides.yaml`
  (correctly out of this audit's active-project scope, not a true orphan).

None of the orphans indicate missing functionality — working code simply not
individually named in an active roadmap task. No action proposed.

## Projects with no checkable concrete surfaces this cycle

`brainstorm`, `kindrobots-unraid`, `humboldt-scoop-cms`, `mural-design`,
`storybook`, `wishmaster`, `taskmaster`, `dream-cycle` (only its already-known
gap above) — these roadmaps name few or no literal file paths (design docs,
infra, or prose-level milestones), so there was little to cross-reference beyond
what's covered above.

## Follow-up tasks filed (3 of the allowed 3)

- `kind-robots/t-051` — investigate/document the disappearance of
  `server/api/conductor/curate-request.post.ts` (no removal trail found).
- `digital-storefront/t-036` — correct t-031's note: the handler is at
  `server/api/stripe/checkout.post.ts`, not `server/api/store/checkout.post.ts`.
- `alexa-integration/t-019` — correct t-012's note: the page component is now
  `components/pages/serendipity-page.vue`, not `serendipity-voice-page.vue`.

## Boundaries observed

No live HTTP requests to kind-robots.vercel.app or any other host. No
`npm`/`pnpm` builds or dev server run. No changes to `main` directly (this
report + the three roadmap edits go out via PR). No `gate_human: true` task was
modified. No existing roadmap entry was edited or deleted — only new `ready`
tasks were added.
