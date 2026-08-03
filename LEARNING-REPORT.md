# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-03T21:15:57Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **490**
- Outcomes: blocked: 13, cancelled: 1, done: 476
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
| conductor | 60 | 100% |
| conductor-app | 2 | 100% |
| davinci | 2 | 100% |
| digital-storefront | 24 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| interface-vision | 47 | 100% |
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
| software | 475 | 99% |

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

- 2026-08-03 `conductor/t-096` — A task selector that only checks status/claimability (run_worker.py's find_ready_task, used by select_role.py) let interface-vision/t-017 -- an umbrella sweep whose own note already said every bucket but one was delegated to t-058 -- get claimed anyway, wasting a session's cycle. Two independent "pick next ready task" implementations (run_worker.py and next_ready_task.py) had already drifted once before this fix; when a roadmap task can legitimately delegate its remaining scope to a named sibling, encode that relationship as a structured field (remaining_scope_task) that every selector checks, not just prose in the note that only a human or a careful session catches by reading the full history.
- 2026-08-03 `interface-vision/t-075` — A kaizen task filed from a filename match alone ("character-flip-card.vue" looks like it should share butterfly-flip.vue's bug) can be wrong -- this file turned out to be an unrelated 900-line dashboard with a stale copy-pasted header comment from a similarly-named file. Verify the actual file content disproves or confirms the premise before writing any fix; closing a task with a corrected note and no diff is the right outcome when the premise does not hold, not a failure. Reading the disproven file also surfaced a real, unrelated bug (CharacterFlipCard has zero defineProps and silently ignores its character prop) -- filed separately as t-076 rather than folded into this task's diff, keeping scope discipline even for an accidental discovery.
- 2026-08-03 `interface-vision/t-017` — A component with both a 3D-flip mode and a fade mode needs a fundamentally different scroll-ownership fix per mode: flip mode already v-if-excludes the inactive face (never double-scrolls), but fade mode renders both faces simultaneously for the opacity transition, so a static overflow-y-auto on both faces gives two live scroll regions at once. Toggle overflowY per face on the same state (isFlipped) that drives the fade, rather than assuming one static class covers both modes. Other flip/fade-card components (e.g. character-flip-card.vue) likely share the same latent bug -- filed t-075 to check.
- 2026-08-03 `interface-vision/t-061` — Two mutually-exclusive v-if/v-else branches gated by a fixed-per-session flag (admin vs. non-admin) are the same SHAPE A pattern as tab switches -- hoist one shared kr-scroll wrapper above the pair instead of each branch declaring its own overflow-y-auto.
- 2026-08-03 `interface-vision/t-055` — Source-text layout verifiers must accept Vue's supported component-tag casing conventions; regression fixtures should exercise component-rooted templates rather than only native lowercase HTML roots.
- 2026-08-03 `interface-vision/t-043` — The existing generic user-owned section pattern extended cleanly to Facet and Project; use each store's mine-filtered fetch action so the dashboard does not depend on an unrelated gallery having loaded first.
- 2026-08-03 `interface-vision/t-067` — Put root-surface markers on the literal opening template element; a styled nested wrapper is invisible to rootClassList and can waste a sweep even when it looks like the page root.
- 2026-08-03 `interface-vision/t-016` — A task note framed as a from-scratch decision plus implementation ("needs a prisma migration plus a re-seed check") can already be most of the way done by prior work -- a quick research pass before diving in found the FacetKind/FacetTaxonomy collapse was already load-bearing infrastructure (a prior PR had made taxonomy authoritative and kind write-derived), narrowing the real remaining scope to a bounded, mechanical consolidation PR instead of a full schema migration. Splitting the genuinely destructive half (dropping the physical column) into its own irreversible-stakes task (t-072) rather than attempting it in the same pass kept the landed PR reversible and auto-mergeable.
- 2026-08-03 `interface-vision/t-048` — A task released as actionable/stale (blocked on an unrelated component not yet migrated) can become trivially doable again once other, unrelated work lands -- re-verify the live premise from code before trusting a stale roadmap note, rather than assuming a prior session's blocker still holds.
- 2026-08-03 `interface-vision/t-057` — When a task's own verification instruction assumes infrastructure (a PR preview) that a repo-wide config (vercel.json) silently excludes for the exact branch prefix agent sessions use, the fallback isn't to skip verification -- it's to verify what CAN be checked (CI, structural reasoning about the change's own properties) and be explicit in the roadmap/PR about what's still open, rather than silently declaring full verification done.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-03T21:15:57Z_
