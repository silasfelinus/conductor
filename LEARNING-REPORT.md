# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-03T17:37:20Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **488**
- Outcomes: blocked: 13, cancelled: 1, done: 474
- Success rate: **97%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 55 | 98% |
| alexa-integration | 2 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 6 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 25 | 100% |
| conductor | 59 | 100% |
| conductor-app | 2 | 100% |
| davinci | 2 | 100% |
| digital-storefront | 24 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| interface-vision | 46 | 100% |
| kind-robots | 39 | 97% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 48 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 2 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 473 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 9 |
| actionable | 9 |
| transient | 7 |
| scope | 1 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `quality` — 9 occurrences; look for the shared cause across its records
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `transient` — 7 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-03 `interface-vision/t-017` — A component with both a 3D-flip mode and a fade mode needs a fundamentally different scroll-ownership fix per mode: flip mode already v-if-excludes the inactive face (never double-scrolls), but fade mode renders both faces simultaneously for the opacity transition, so a static overflow-y-auto on both faces gives two live scroll regions at once. Toggle overflowY per face on the same state (isFlipped) that drives the fade, rather than assuming one static class covers both modes. Other flip/fade-card components (e.g. character-flip-card.vue) likely share the same latent bug -- filed t-075 to check.
- 2026-08-03 `interface-vision/t-061` — Two mutually-exclusive v-if/v-else branches gated by a fixed-per-session flag (admin vs. non-admin) are the same SHAPE A pattern as tab switches -- hoist one shared kr-scroll wrapper above the pair instead of each branch declaring its own overflow-y-auto.
- 2026-08-03 `interface-vision/t-055` — Source-text layout verifiers must accept Vue's supported component-tag casing conventions; regression fixtures should exercise component-rooted templates rather than only native lowercase HTML roots.
- 2026-08-03 `interface-vision/t-043` — The existing generic user-owned section pattern extended cleanly to Facet and Project; use each store's mine-filtered fetch action so the dashboard does not depend on an unrelated gallery having loaded first.
- 2026-08-03 `interface-vision/t-067` — Put root-surface markers on the literal opening template element; a styled nested wrapper is invisible to rootClassList and can waste a sweep even when it looks like the page root.
- 2026-08-03 `interface-vision/t-016` — A task note framed as a from-scratch decision plus implementation ("needs a prisma migration plus a re-seed check") can already be most of the way done by prior work -- a quick research pass before diving in found the FacetKind/FacetTaxonomy collapse was already load-bearing infrastructure (a prior PR had made taxonomy authoritative and kind write-derived), narrowing the real remaining scope to a bounded, mechanical consolidation PR instead of a full schema migration. Splitting the genuinely destructive half (dropping the physical column) into its own irreversible-stakes task (t-072) rather than attempting it in the same pass kept the landed PR reversible and auto-mergeable.
- 2026-08-03 `interface-vision/t-048` — A task released as actionable/stale (blocked on an unrelated component not yet migrated) can become trivially doable again once other, unrelated work lands -- re-verify the live premise from code before trusting a stale roadmap note, rather than assuming a prior session's blocker still holds.
- 2026-08-03 `interface-vision/t-057` — When a task's own verification instruction assumes infrastructure (a PR preview) that a repo-wide config (vercel.json) silently excludes for the exact branch prefix agent sessions use, the fallback isn't to skip verification -- it's to verify what CAN be checked (CI, structural reasoning about the change's own properties) and be explicit in the roadmap/PR about what's still open, rather than silently declaring full verification done.
- 2026-08-03 `interface-vision/t-031` — The object-card divergence was concentrated in Dream's shell and the repeated card body, not five wholly bespoke cards; inspect shared wrappers before planning a broad convergence rewrite.
- 2026-08-03 `interface-vision/t-065` — The implementation half of this task (scripts/next_free_task_id.py, PR #1588) merged, but the task couldn't close because it was left with a queued rearm task-event that the processor rejected every run (`rearm requires recurring: true` -- t-065 isn't a recurring task). A connector-only session can't tell mid-task whether a target task is recurring without reading the live roadmap first; docs/github-connector-worker.md listed `rearm` and `ready` as interchangeable options with no mention of the recurring gate, so the wrong operation was a natural mistake, not carelessness. A concurrent session fixed the stuck event with the correct `operation: ready` while this session was independently mid-flight on the actual remaining work (wiring scripts/next_free_task_id.py into AGENTS.md's task-id-assignment call sites); rebasing onto that fix rather than duplicating it is what let both land cleanly. Documented the rearm-vs-ready distinction in docs/github-connector-worker.md so the next connector session doesn't repeat it.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-03T17:37:20Z_
