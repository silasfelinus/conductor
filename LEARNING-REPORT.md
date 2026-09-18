# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-18T10:58:45Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1021**
- Outcomes: blocked: 16, cancelled: 1, done: 1004
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
| art-archive | 10 | 100% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| butterfly-gallery | 4 | 100% |
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
| software | 1004 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 29 |
| transient | 17 |
| actionable | 15 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 29 occurrences; look for the shared cause across its records
- failure category `transient` — 17 occurrences; look for the shared cause across its records
- failure category `actionable` — 15 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-18 `butterfly-gallery/t-005` — Extracting the pile/frame sections directly out of the t-003 placeholder page into two new presentational components (emit gestures up, no store mutation of their own) landed clean on the first pass by following narrative-cast-card.vue's established convention rather than inventing a new shape. Adding a store-owned topOfPile computed (sliced from the already-filtered visiblePile) kept the "only render the top of the stack" requirement testable and reusable, instead of duplicating the slice-and-filter logic inside the component. Touch/pointer drag-to-frame was deliberately left to the sibling task (t-020) that already owns that scope -- click (a real <button>, already keyboard-reachable) covers the non-drag path in the meantime, so nothing regressed.
- 2026-09-18 `butterfly-gallery/t-004` — Defining the read contract as a small interface (ButterflyGalleryFeedProvider. fetchPage) with one fixture implementation and a swappable module-level "active provider" landed clean and immediately exercised end-to-end (a real loadMore()/hasMore path in the store and page) rather than staying a paper contract nobody calls. Extending an existing type (ButterflyPileEntry) to satisfy a new task's field list is safe as long as every direct object-literal construction of that type (the fixtures file) is updated in the same PR -- vue-tsc catches a missed field immediately, but only if the fixtures are still plain object literals rather than already-cast `as ButterflyPileEntry`.
- 2026-09-18 `butterfly-gallery/t-003` — Matching an existing admin-page pattern (pages/admin/curation-studio.vue, pages/admin/lora-triage.vue: inline userStore.initialize() + v-else-if admin gate, no middleware) plus an existing composition-API store shape (stores/loraTriageStore.ts) let a brand-new route+store+state-machine land first-pass clean (vue-tsc, eslint, prettier, layout-contract) with zero CI rejections. Keeping the fixture data behind a single loadPile()/rescan() seam (stores/helpers/butterflyGalleryFixtures.ts) rather than inlining it in the store or page means the t-004 adapter swap only touches one file.
- 2026-09-18 `butterfly-gallery/t-002` — A Kind-Robots-authored project's Project row is auto-created by the conductor projection sync with conductorSlug already set, but its presentation fields (title/channelKey/tabKey/liveUrl/isPublic) start as placeholders/defaults and need a follow-up admin PATCH -- this is a live data fix via the existing admin API, not a code PR, for every new project's identity task.
- 2026-09-18 `art-archive/t-021` — Pass-1 rejection (TypeScript union-narrowing on ExtractedArchiveMetadata) was fixed correctly on retry within the same session/branch -- the Worker read retry_context and applied exactly the suggested guard rather than retrying blind. Third module in this project to independently discriminate the same metadata union; filed t-026 to extract a shared helper instead of waiting for a fourth recurrence.
- 2026-09-18 `art-archive/t-014` — Clean first-pass implementation, reviewed by a concurrent Reviewer session. The Worker independently applied the same DB-free-testability convention this session established earlier the same day for artArchiveReconcilerPlan.ts and artArchiveFileOps.ts (a zero-Prisma validator module for its own unit tests) without being told to -- a good sign the pattern is now legible from the codebase itself, not just from session-to-session TALKBACK notes.
- 2026-09-18 `art-archive/t-024` — Clean first-pass implementation. When a task depends on an existing CLI entrypoint but the task itself is "expose this over HTTP", extract the CLI's per-file loop/counting logic into a small shared function the new endpoint calls, rather than duplicating the loop a second time or rewriting the CLI to use a shared function too (which would risk breaking that CLI's own frozen regex-based contract test). Left the CLI untouched and its existing verifyImportArtArchive.mjs contract passing unmodified.
- 2026-09-18 `art-archive/t-008` — A unit test that imports a module needing Prisma will crash under this repo's contract-tests job, which runs without DATABASE_URL -- even if the test itself only calls a pure function from that module. The fix (applied here, matching applyArtArchiveResourceMatch.ts's existing precedent) is to keep any Prisma-free decision logic in its own module with zero Prisma import, so a pure-logic unit test can import it directly without dragging in the real client. Caught and fixed same-cycle before merge; no wasted review round since the fix landed on the same PR before a Reviewer ever saw the red check.
- 2026-09-18 `art-archive/t-007` — Clean first-pass implementation of high-confidence resource-provenance application: only writes ArtImage.checkpointResourceId/LoraResources from unique hash/exact-name matches, records ambiguous/suggested/unmatched evidence for later review instead of guessing, and skips resourceMatchLocked entries so a manual admin correction is never silently overwritten. Kaizen follow-on (surfacing match-quality candidates before auto-apply) was already filed as t-023, so no new kaizen task was needed on this close-out.
- 2026-09-18 `art-archive/t-022` — Clean pass. When a task note offers two implementation shapes ("a CLI script or an admin-gated endpoint"), picking one and filing the other as an explicit follow-on task (rather than silently treating the chosen option as if it fully satisfied the note, or scope-creeping to build both) keeps the task's actual delivered scope honest and visible in the roadmap.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-18T10:58:45Z_
