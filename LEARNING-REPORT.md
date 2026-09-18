# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-18T13:01:27Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1027**
- Outcomes: blocked: 16, cancelled: 1, done: 1010
- Success rate: **98%**
- Average passes on successful tasks: **0.2**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 14 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 11 | 100% |
| approval-portal | 2 | 0% |
| art-archive | 11 | 100% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| butterfly-gallery | 9 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 39 | 100% |
| conductor | 120 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 24 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 136 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 10 | 100% |
| kind-robots | 64 | 98% |
| kindrobots-unraid | 9 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 11 | 100% |
| media-watchlist | 12 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 85 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 21 | 100% |
| ruler-hooked | 14 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 29 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1010 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 30 |
| transient | 17 |
| actionable | 15 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 30 occurrences; look for the shared cause across its records
- failure category `transient` — 17 occurrences; look for the shared cause across its records
- failure category `actionable` — 15 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-18 `butterfly-gallery/t-009` — Reading the store's existing visiblePile filter logic before building any UI surfaced a real, previously-invisible bug: trash visibility was folded into matchState === 'missing' by the earlier t-003 scaffolding, but trashing an entry never touches matchState, so that path never actually revealed a real trashed entry (confirmed against the fixture data: entry 9005 is trashed:true, matchState:'matched'). Fixed by giving trash visibility its own filters.trashView dimension, decoupled from matchState, and adding direct unit coverage for the decoupling rather than assuming the old combined check was intentional just because it had shipped before.
- 2026-09-18 `art-archive/t-010` — Pass-1 rejection (kind_robots#2836) flagged two real, locally-reproduced defects in the new admin Art Archive browser -- a nonexistent userStore.isInitialized field (correct name: initialized) and a bare kr-select class with no matching tailwind.css primitive (kr-select-sm already existed and was the fix). The Worker's pass-2 retry addressed both directly and named them in the PR body; all 51 checks went green on the first re-run. Confirms retry_context written at rejection time is enough for a clean second pass when the failures are concrete and locally reproducible rather than ambiguous.
- 2026-09-18 `butterfly-gallery/t-007` — Extracting the field-level action rules into small, pure appliers (stores/helpers/butterflyGalleryActions.ts) before wiring them behind an injectable adapter made the whole task independently unit-testable via a plain tsx script (this repo has no vitest) without needing Pinia/component setup at all -- the store's existing sync setRating()/applyBinOutcome() mutated a plain object reference regardless of whether it was reactive, so the refactor into standalone functions cost nothing and paid for itself immediately in test coverage.
- 2026-09-18 `butterfly-gallery/t-010` — Verified against the merged file directly (grep for runway-slot/drop-funnel/ preset-bin/right-rail/pile-card/robot-animation-slot) rather than trusting the PR description alone before marking this milestone-3 task done -- the PR's own self-report matched what actually shipped, but checking the diff itself is what makes that confidence earned rather than assumed.
- 2026-09-18 `butterfly-gallery/t-008` — Same PR (kind_robots#2834) substantially implemented the right-rail Image Info panel ahead of its own roadmap task being claimed. Closed with two minor field-list gaps noted (no filename/title or dimensions in the compact view) rather than reopening or leaving it artificially at ready -- the note's core ask (compact panel + Details expand + Cleanup/Trash below it) is met, and gating done-ness on a cosmetic completeness nit would misrepresent the task's actual state.
- 2026-09-18 `butterfly-gallery/t-006` — Reconciled from kind_robots#2834 rather than implemented directly this cycle -- Silas built the full approved-stage composition himself in a live session that ran concurrently with this session's t-005 work, superseding t-005's narrower component-extraction approach and covering t-006/t-008/t-010's scope in one PR. The conflict this produced (both PRs touched pages/butterfly-gallery.vue, based on the same stale pre-t-005 commit) resolved cleanly by keeping the newer, more complete implementation and removing the now-orphaned t-005 components/store additions that nothing referenced. Worth a standing habit: when a design-lock/spec commit lands mid-task (visible via a fresh git log on the docs/roadmap repo), re-check for a matching implementation PR before assuming your own in-flight work is still the only game in town.
- 2026-09-18 `butterfly-gallery/t-005` — Extracting the pile/frame sections directly out of the t-003 placeholder page into two new presentational components (emit gestures up, no store mutation of their own) landed clean on the first pass by following narrative-cast-card.vue's established convention rather than inventing a new shape. Adding a store-owned topOfPile computed (sliced from the already-filtered visiblePile) kept the "only render the top of the stack" requirement testable and reusable, instead of duplicating the slice-and-filter logic inside the component. Touch/pointer drag-to-frame was deliberately left to the sibling task (t-020) that already owns that scope -- click (a real <button>, already keyboard-reachable) covers the non-drag path in the meantime, so nothing regressed.
- 2026-09-18 `butterfly-gallery/t-004` — Defining the read contract as a small interface (ButterflyGalleryFeedProvider. fetchPage) with one fixture implementation and a swappable module-level "active provider" landed clean and immediately exercised end-to-end (a real loadMore()/hasMore path in the store and page) rather than staying a paper contract nobody calls. Extending an existing type (ButterflyPileEntry) to satisfy a new task's field list is safe as long as every direct object-literal construction of that type (the fixtures file) is updated in the same PR -- vue-tsc catches a missed field immediately, but only if the fixtures are still plain object literals rather than already-cast `as ButterflyPileEntry`.
- 2026-09-18 `butterfly-gallery/t-003` — Matching an existing admin-page pattern (pages/admin/curation-studio.vue, pages/admin/lora-triage.vue: inline userStore.initialize() + v-else-if admin gate, no middleware) plus an existing composition-API store shape (stores/loraTriageStore.ts) let a brand-new route+store+state-machine land first-pass clean (vue-tsc, eslint, prettier, layout-contract) with zero CI rejections. Keeping the fixture data behind a single loadPile()/rescan() seam (stores/helpers/butterflyGalleryFixtures.ts) rather than inlining it in the store or page means the t-004 adapter swap only touches one file.
- 2026-09-18 `butterfly-gallery/t-002` — A Kind-Robots-authored project's Project row is auto-created by the conductor projection sync with conductorSlug already set, but its presentation fields (title/channelKey/tabKey/liveUrl/isPublic) start as placeholders/defaults and need a follow-up admin PATCH -- this is a live data fix via the existing admin API, not a code PR, for every new project's identity task.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-18T13:01:27Z_
