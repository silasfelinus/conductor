# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-04T05:53:32Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **504**
- Outcomes: blocked: 13, cancelled: 1, done: 490
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
| interface-vision | 61 | 100% |
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
| software | 489 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 9 |
| actionable | 9 |
| transient | 8 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `quality` — 9 occurrences; look for the shared cause across its records
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `transient` — 8 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-04 `interface-vision/t-026` — Deleting a bespoke duplicate component in favor of a shared canonical one (Silas's "one source ... kill the others" pick, resolving an A/B mockup) needs a full-repo grep for the deleted file's name, not just its obvious call site. Two silent-breakage risks turned up that a component-only diff would have missed: a DOM-scraping client plugin (project-art-prompt-suggest.client.ts) that keyed its button-injection logic on the deleted component's specific textarea maxlength and a <code> element it rendered -- fixed by gating on the shared component's entityType prop instead of brittle per-entity DOM shape -- and a GitHub Actions workflow (entity-art-manager-contract.yml) whose trigger `paths:` list still named the deleted file, caught by CI's verifyWorkflowPaths.ts after merge-adjacent push rather than before. Also worth noting: placing a new UI panel *before* an existing one in a component's template silently changes which element a `querySelector('img')`-style DOM heuristic elsewhere in the codebase picks up first -- moved the new panel after the existing one specifically to keep that heuristic pointed at the right image.
- 2026-08-04 `interface-vision/t-076` — A "needs a real design decision" task with two named options (rewrite the broken component, or swap in an already-correct one) resolved fast once the already-correct option's actual prop contract was read in full: character-card.vue already did everything option (a) would have had to build (a real character prop, no side-effecting store init, grid-proven usage), so option (b) collapsed to a small, mechanical swap. The type system caught a real latent gap the swap needed to resolve (a curated Pick<Character,...> relation missing two fields the target component's full prop type required) -- something the previous component's total absence of prop typing had let go unnoticed indefinitely. When a task's own note offers "use an existing correct component instead" as an option, read that component's actual prop surface before assuming a rewrite is the only path -- the smaller fix is often already built.
- 2026-08-04 `interface-vision/t-051` — A three-surface migration task (reward/character/scenario-interact) was scoped correctly for "what's left" but not for "what fits in one pass." Splitting after landing the first surface (character-interact, kind_robots PR #1400) into t-087/t-088 for the remaining two, rather than trying all three in one diff, kept each PR small, independently verifiable, and reviewable -- and let the roadmap track real partial progress instead of one task note growing indefinitely across sessions. When a task note already enumerates N similarly-sized remaining items, file it as N tasks up front rather than one task that will need a mid-flight split.

- 2026-08-04 `interface-vision/t-050` — A "retire component X, fold into shared component Y" task can resolve correctly with zero code changes when the premise doesn't survive a full read: the task's own note said kr-narrator-stage was imported by "every other surface," but grep found exactly two real consumers, and grafting the remaining Dreams-specific chrome (card flip, emoji bursts, musings toast, pin) onto it would have more than doubled a 189-line shared component for those two consumers' benefit. When a retirement/consolidation task's justification rests on an unverified breadth claim ("every surface," "the shared X"), verify the actual consumer count with grep before implementing the merge -- the corrected count can flip the right answer from "fold it in" to "leave it alone."
- 2026-08-04 `interface-vision/t-064` — A task tracking N/M sub-item progress (5 cards converging onto a shared body) had its note fall one merge behind reality: reward-card had already migrated in a prior session/PR with no note update recording it, so the task read as 2 items remaining when only 1 actually was. Caught by checking the merged tree directly (grep for the new import) rather than trusting the note's own count. When landing one item of an N/M tracked task, update the note's count even if the task can't close yet.
- 2026-08-04 `interface-vision/t-045` — A plain repo-wide grep for a deleted component's filename missed a real dependency: verifyWonderLabInteractionDisplayFixtures.ts read smart-nav.vue's source directly via fs.readFile to assert on its prop contract, which only surfaced as an ENOENT in the "Contract verifiers" CI job, not in any local grep or vue-tsc/eslint pass. Before deleting a component with WonderLab preview fixture coverage, grep the utils/scripts/verifyWonderLab*.ts files specifically for readFile calls against that component's path, not just import/reference greps.
- 2026-08-04 `interface-vision/t-080` — Task title covered two symmetric entities (Reward + Scenario isPublic/isMature toggles) but the PR only implemented one; split the remainder into t-082 rather than either blocking the merged half or silently closing the task as fully done. Titles spanning multiple entities should be split into per-entity tasks at claim time to avoid this ambiguity recurring.
- 2026-08-04 `interface-vision/t-042` — Before building a "creation flow" task from scratch, check the note's own predicted building blocks against the current codebase first -- the Facet half of this task (facet-profile-editor.vue + facetProfileForm.ts feeding a create form) had already shipped via an unrelated commit by the time this task was worked, so the actual remaining scope was half the size the note described. Only the Project half needed new UI; the store/API layer (createProject()) was already complete on both sides.
- 2026-08-04 `interface-vision/t-036` — When a task note gives you the exact CI-side validator to reuse client-side (navManifest.ts here), mirror its field-construction one-to-one rather than approximating -- the isomorphic-by-design comment in the module was the signal that a straight port, not a reinterpretation, was correct. Also: a component gated requiredRole: ADMIN cannot be visually verified from an agent sandbox without admin credentials -- typecheck plus the same CI script the component now reuses is the honest substitute, and it belongs explicitly in the PR flags rather than silently skipped. Separately: an automated close-task-event can land on main between opening a manual close_task.py PR and merging it -- check task-events/ and the live roadmap status again immediately before merging a close-out, not just once before opening it, or the merge 405s on a conflict against a transition that already happened.
- 2026-08-03 `interface-vision/t-035` — A registry helper (getModelCards()) existing, exporting cleanly, and being independently correct is not evidence it is wired in -- grep call sites, not just definitions, whenever a task note says a function "is defined but never called anywhere." pageStore.cards had two isX() type-guard branches that looked exhaustive but silently fell through to a channel-tab fallback for every string cards: value; the missing branch was a single conditional, but nothing in the type system or existing tests flagged the dead code path.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-04T05:53:32Z_
