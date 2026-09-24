# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-24T22:08:00Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1142**
- Outcomes: blocked: 19, cancelled: 2, done: 1121
- Success rate: **98%**
- Average passes on successful tasks: **0.3**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 19 | 95% |
| animation-studio | 2 | 50% |
| appmaker | 11 | 100% |
| approval-portal | 2 | 0% |
| art-archive | 34 | 100% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| butterfly-gallery | 32 | 94% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 39 | 100% |
| conductor | 134 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 28 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 140 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 11 | 100% |
| kind-robots | 70 | 99% |
| kindrobots-unraid | 9 | 100% |
| lora-ingestion | 11 | 100% |
| mandarin-tutor | 14 | 93% |
| media-watchlist | 12 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 85 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 21 | 100% |
| ruler-hooked | 23 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 42 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1125 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 42 |
| transient | 17 |
| actionable | 17 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 42 occurrences; look for the shared cause across its records
- failure category `transient` — 17 occurrences; look for the shared cause across its records
- failure category `actionable` — 17 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-24 `ruler-hooked/t-030` — For image-led game-state views, reuse the canonical composited scene and live ContentBundle/save data rather than creating a second visual/state representation; container-responsive auto-fit grids also satisfy the layout contract better than viewport breakpoints inside reusable components.
- 2026-09-24 `kind-robots/t-119` — Gallery controls can exist yet be unreachable when a parent suppresses the child header; surface cross-view state at the owning page level. Also treat supportedServer as a loader lane, not a training-family guarantee, and preserve HUMAN LoRA classifications when repairing inferred categories.
- 2026-09-24 `kind-robots/t-118` — Source-image support belongs in the generator capability matrix rather than as an SDXL-only UI special case. Directory-based checkpoint lineage is more reliable than Resource.generation for imported checkpoints.
- 2026-09-24 `storybook/t-067` — This is the third occurrence of the same stale-post-cleanup-reference pattern (t-037's own guard deletion, then t-066, then this task) -- grepping the FULL deleted-filename list against every surviving file, not just the file(s) a task title implies, is what actually finds the next hit: the real one this cycle was in a .ts guard for a completely different feature (verifyStorybookActiveStoryResumeGuard.ts), not another *DeepLinkGuard.mjs sibling. Filed t-068 to make this mechanical instead of relying on a third manual sweep.
- 2026-09-23 `dream-cycle/t-033` — The weekly site audit's orphan-directory pass correctly found server/api/dream-relations/ was undocumented, but its 'wired into real UI' read was wrong -- always trace named consumer files' actual fetch/import calls (not just their filenames appearing near the feature) before repeating an audit's wiring claim. Here, the named UI files only read DreamRelation via a Prisma include on a different endpoint, and a repo-wide grep for the write endpoints and prisma.dreamRelation.create/upsert found zero callers anywhere -- the CRUD surface is fully built and guarded but currently has no caller at all, live or seeded.
- 2026-09-23 `storybook/t-066` — Clean first-pass kaizen fix: a stale-comment cleanup task is fast to verify fully (guard's own test + prettier + a repo-wide grep for the deleted filenames) even without a full local eslint environment -- worth doing that full grep sweep rather than trusting the single file diff, since a header comment mentioning a deleted file can easily have a sibling reference elsewhere in the same file.
- 2026-09-23 `animation-manager/t-019-followup` — Two worker/* branches (worker/animation-manager-t019-final, superseded, and worker/animation-manager-t019-digest-final, the cleaned-up final version) sat with a merged PR (#5136) that select_role.py's own scan missed on the run that found the branches -- always re-check list_pull_requests by head branch before opening a new PR from an existing worker/* branch, since a PR can exist even when the role-selection script reports zero reviewable PRs.
- 2026-09-23 `animation-manager/t-021` — Three straight passes failed on lint/format ratchet gates, not the actual helper design (which was accepted as correct from pass 1) -- pass 1 was ESLint escape/regex issues, pass 2 was Prettier on both new files, pass 3 was Prettier on only one of the two new files (a partial fix, not a fresh regression). A connector-only Worker session retrying a ratchet failure needs to actually run `npm run test:lint-ratchet && npm run test:prettier-ratchet` locally after its fix and read the output, not just apply a plausible-looking `prettier --write`/manual edit and repush blind -- the same gate class recurring three times on two small new files suggests the retry loop wasn't verifying its own fix before pushing.
- 2026-09-23 `conductor/t-194` — check_priority_queue_starvation.py's shape (advisory, local-YAML-only, project_lifecycle-scoped, JSON+render dual output) is a reusable template for a new roadmap-health check -- following it exactly (rather than inventing new conventions) kept this addition small and immediately legible against the rest of scripts/check_*.py.
- 2026-09-23 `ruler-hooked/t-038` — build_ruler_hooked_art_queue.py's card lane had been silently staging every request at the wrong image_path (public/images/ruler-hooked/cards/<id>.webp with a cards/ subdirectory and no card- prefix) against cardArtPath()'s actual contract (public/images/ruler-hooked/card-<id>.webp, no subdirectory) since the lane was written -- caught only by reading the consuming component (cardArt.ts) directly rather than trusting the producing script's own naming. A staging script and its consumer having independently-plausible-looking but silently mismatched path conventions is a class of bug that unit tests over the staging script alone would never catch, since it never reads the consumer; worth checking both ends of any asset-path contract when adding a new art-queue lane, not just validating the producer's own output shape.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-24T22:08:00Z_
