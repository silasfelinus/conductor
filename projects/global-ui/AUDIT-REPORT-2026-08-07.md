# Weekly Site Audit — 2026-08-07

Per `projects/global-ui/SITE-AUDIT-AGENT.md`, run under the self-assigning
`role: site-auditor` path (`scripts/select_role.py`), which flagged the audit as
overdue (previous report `AUDIT-REPORT-2026-08-02.md`, ~5 days old but the prior
day's cycles had higher-priority work; this is the first session since to reach
`site-auditor` in the role-priority order).

**Method:** cross-referenced all 27 `active` (per `project-overrides.yaml`)
conductor project roadmaps against `/home/user/kind_robots/` (API routes, Pinia
stores, Vue components, `prisma/schema.prisma`, page routes) using Glob/Grep only
— no live HTTP requests were made, no npm/pnpm builds run, no dev server started.
For conductor-internal projects (conductor, conductor-app, dream-cycle, brainstorm)
checked named scripts/docs against `/home/user/conductor` instead. Extracted named
component/store/route/model tokens from each roadmap and checked each against the
current `kind_robots` checkout, then hand-verified apparent misses against
surrounding roadmap context (task status, dated notes, later corrections) to
separate real gaps from historical narration.

Note on `project-overrides.yaml` since last week: no status flips observed; still
27 active projects (`interface-vision` and `davinci`, both reopened the prior
cycle, remain active).

## Summary

27 active projects checked. The large majority of roadmap-claimed surfaces exist
in code exactly as described. Found **six drift/gap cases** across three
projects (interface-vision, ruler-hooked, kind-robots) — in every case the
underlying functionality still works (Nuxt's flat auto-import tolerates the
folder move, or the feature was intentionally relocated to `abandonware/`), the
issue is only that a `done` task's closing note now points at a path that no
longer exists, which will misdirect a future reader searching by that path.

## Findings

### Path/filename drift (functionality intact, roadmap note points at the wrong or missing name)

1. **interface-vision** — t-001/t-002 (done) describe
   `components/storybook/storybook-mockups.vue` and a `/storybook-mockups` route
   as live; neither is found anywhere in kind_robots. t-024 (done, 2026-08-02)
   describes `components/pages/plan-projects-grid.vue` as an in-use component;
   it has since moved to `components/abandonware/conductor/plan-projects-grid.vue`.
   Filed **interface-vision/t-101** (ready, reversible) to confirm intent and add
   correction addenda.
2. **ruler-hooked** — t-012 (done, 2026-07-21) asserts
   `components/ruler-hooked/ruler-hooked-page.vue` is "structurally present and
   wired"; the file actually lives at `components/conductor/ruler-hooked-page.vue`
   (app still works via Nuxt's flat auto-import, only the documented path is
   wrong). The same task cites `components/navigation/swipe-deck.vue` and
   `components/butterfly/single-slider.vue` as reuse patterns and
   `stores/compositionStore.ts` as a reuse idiom — none exist under those names
   (`swipe-deck.vue` was never built, `single-slider.vue` now lives under
   `components/abandonware/butterfly/`, and `compositionStore.ts` never existed;
   `rulerHookedStore.ts` ships its own local-storage handling directly). Filed
   **ruler-hooked/t-013** (ready, reversible) to correct the note.
3. **kind-robots** — t-027's 2026-07-16 audit lists
   `components/butterfly/store-butterfly.vue` as a live file it checked; it has
   since moved to `components/abandonware/butterfly/store-butterfly.vue` with no
   roadmap task recording the relocation. Filed **kind-robots/t-055** (ready,
   reversible) to record the move.

### Confirmed-resolved (no action — verified NOT gaps despite initial extraction flagging them)

- `displayStore.ts`, `components/icons/kind-icons.vue`,
  `components/navigation/narrator-chat.vue`,
  `components/pages/conductor-art-gallery.vue`, `stores/linkStore.ts`,
  `components/art/art-reactions.vue`,
  `components/giftshop/social-publisher.vue`,
  `components/pages/serendipity-voice-page.vue` — all explicitly documented as
  deleted/renamed/corrected in their own roadmap tasks (interface-vision
  t-012/t-018/t-026/t-045, digital-storefront t-027, alexa-integration's t-012
  correction from last week's audit). Roadmap text matches reality.
- `newsfeed/t-004`'s note cites `stores/socialStore.ts` as an existing precedent
  alongside `stores/navStore.ts` — `navStore.ts` exists, `socialStore.ts` does
  not, but this is planning-text-overtaken-by-events (same class as last week's
  `ruler-hooked`/`compositionStore.ts` finding), not a live claim of a shipped
  file. Not filed.

## Projects with no checkable concrete surfaces this cycle / clean this cycle

`alexa-integration`, `animation-manager`, `appmaker`, `brainstorm`, `coat-dance`,
`coloring-book`, `conductor`, `conductor-app`, `davinci`, `digital-storefront`,
`dream-cycle`, `humboldt-scoop-cms`, `kindrobots-unraid`, `lora-ingestion`,
`media-watchlist`, `mermaids-of-venice`, `model-builder`, `mural-design`,
`music-mentor`, `newsfeed` (beyond the one non-actionable note above),
`storybook`, `taskmaster`, `wishmaster`, `ai-art-academy` — named surfaces exist
as described, or the roadmap is mostly prose-level milestones with little to
cross-reference.

## Follow-up tasks filed (3 of the allowed 3)

- `interface-vision/t-101` — reconcile t-001/t-002/t-024 closing notes with
  current kind_robots (storybook-mockups.vue, plan-projects-grid.vue).
- `ruler-hooked/t-013` — correct t-012's stale file paths
  (ruler-hooked-page.vue, swipe-deck.vue, single-slider.vue, compositionStore.ts).
- `kind-robots/t-055` — record store-butterfly.vue's relocation to
  `abandonware/` against t-027's file inventory.

## Boundaries observed

No live HTTP requests to kind-robots.vercel.app or any other host. No
`npm`/`pnpm` builds or dev server run. No changes to `main` directly (this
report + the three roadmap edits go out via PR). No `gate_human: true` task was
modified. No existing roadmap entry was edited or deleted — only new `ready`
tasks were added.
