# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-21T00:57:50Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1090**
- Outcomes: blocked: 18, cancelled: 2, done: 1070
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
| art-archive | 32 | 100% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| butterfly-gallery | 29 | 93% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 39 | 100% |
| conductor | 126 | 100% |
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
| interface-vision | 140 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 10 | 100% |
| kind-robots | 67 | 99% |
| kindrobots-unraid | 9 | 100% |
| lora-ingestion | 3 | 100% |
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
| ruler-hooked | 17 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 30 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1073 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 39 |
| transient | 17 |
| actionable | 17 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 39 occurrences; look for the shared cause across its records
- failure category `transient` — 17 occurrences; look for the shared cause across its records
- failure category `actionable` — 17 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-20 `conductor/t-186` — A "grep every *.ps1 for a banned direct-call shape" regression guard needs a self-test proving it actually fires on a synthetic reintroduction, not just that today's files happen to be clean -- otherwise a regex that silently stops matching (a refactor, an escaping mistake) looks identical to "the gap stays closed" until the next manual audit finds it the hard way again. Comment-only references to the banned pattern (several files here legitimately explain in prose why they no longer call it that way) also need an explicit skip, or the guard flags its own documentation.
- 2026-09-20 `conductor/t-185` — Moving a pinned function out of one file into a shared, dot-sourced library is safe to do blind-to-runtime (no PowerShell available in this sandbox) as long as every consumer of the moved code is re-verified structurally: not just "does the new file parse" but "does each caller still have every free variable/function the moved code references in scope at the point it dot-sources the library" (here: Write-Log, $comfyDir, $comfyPython). Equally important: a file moved into a new subdirectory can silently drop out of a checker that globs non-recursively even when the CI *workflow's* own path-trigger filter still fires on it -- the workflow ran, reported green, and would have kept doing so while quietly no longer checking the one file that just moved. Grep for every place a repo re-derives "which files does this check cover" (a Get-ChildItem, a glob(), an rglob()) whenever adding a subdirectory to a previously-flat file layout, not just the CI trigger definition.
- 2026-09-20 `conductor/t-184` — When a task's own scope note offers a binary choice ("route it through X, or document why it's a deliberate exception") and a real gap is found that isn't actually deliberate, a third outcome -- document the gap honestly as a known, tracked issue and file a properly- scoped follow-up task -- is often the right call, especially when the "correct" fix (here: extracting a function pinned by source-contract tests out of a production Windows watchdog script) can't be behaviorally verified in a sandbox with no PowerShell, only syntax-checked by CI after the fact.
- 2026-09-20 `ruler-hooked/t-034` — When a "simulate the economy" task's live game has a skill-dependent success/failure step (here: the timing-bar minigame's LANDED/ESCAPED outcome) with no fixed probability anywhere in the data, don't invent a number to fill the gap -- define the simulation's unit of time around the step that IS fully data-driven (one resolved catch, not one cast attempt) and say so explicitly in the file. A `--check-drift` mode that regex-diffs a hand-synced data file against its live TypeScript source, self-tested by injecting a real mismatch and confirming it's caught, is worth adding whenever a design/simulation layer duplicates numbers a developer could otherwise edit in only one of the two places by mistake.
- 2026-09-20 `ruler-hooked/t-029` — A game's existing closed Effect grammar (counters/sliders/flags, additive and reducer-applied) is usually wide enough to carry a brand-new subsystem (here: a spendable currency, gear ownership, and kingdom investment) with zero save-shape changes -- check for that reuse before reaching for a new save field or a bespoke mutation path. Also: when a value must feed a purely-derived function that's called from multiple sites (game logic AND the Vue display, here timingProfileFor), snapshot it onto the state object at construction time rather than threading it as a new parameter everywhere -- every existing call site picks it up for free and the visual/logic paths can't diverge.
- 2026-09-20 `interface-vision/t-137` — A per-bucket ratchet that compares only aggregate COUNT (not membership) lets a same-bucket substitution slip through silently; when entries are stable identifiers with no natural churn (bare file paths, unlike ESLint's line:column), add an explicit membership check alongside the count check rather than assuming count-only is sufficient everywhere the shared ratchetBaseline.ts pattern is reused.
- 2026-09-20 `ruler-hooked/t-028` — Reused an existing Prisma model (Character/ExpressionMedia) instead of inventing a parallel portrait/expression schema, per the task's explicit instruction to build on the audit's character-parity item -- worth checking for an already-fitting model before adding new columns/tables on any 'we need a character system' task. Separately: running `prettier --write` on an edited file reformats the WHOLE file, not just the touched lines; several ruler-hooked files were already prettier-non-compliant on main before this task, so a naive --write pass would have bundled a large unrelated reflow into the diff. Checked each edited file's original formatting via `git show HEAD:<file>` before trusting --write's output, and reverted/reapplied surgically where it over-reformatted -- worth doing this check by default on any repo where prettier compliance isn't already a green baseline.
- 2026-09-20 `interface-vision/t-139` — Clean first-pass follow-on from t-138: mirroring an already-established, already-CI-verified pattern (character-card.vue/reward-card.vue's pending-prop wiring) onto sibling components, and running the specific architecture/contract scripts the prior cycle's failure had already named (verify-project-architecture.mjs, verifyGalleryAdoption.ts, verifyNarrativeKit.ts) before pushing rather than after, avoided repeating the same CI round-trip. Also correctly recognized when the pattern did NOT apply (server-card.vue has no art plate) instead of forcing a fit -- worth noting as a positive example of scope discipline for future 'do the same thing on N siblings' tasks.
- 2026-09-20 `interface-vision/t-138` — A local eslint/prettier/vue-tsc-clean pass is not the same as a repo-architecture-clean pass -- the first CI push placed a new composable at root composables/ (forbidden by verify-project-architecture.mjs) and had a Facets surface reference the wrong art-request mechanism (caught by verifyFacetCatalogMaintenance.ts's ArtJob-vs-YAML assertion), neither of which vue-tsc/eslint/prettier would ever catch. Both were real, CI only found them because the coordinating session polled check runs directly rather than trusting the worker subagent's own 'verified' claim; fixed in one follow-up push and merged clean on the second CI run. Kaizen -- before wiring a new shared composable/store into an unfamiliar surface, grep for the repo's own architecture-contract script (verify-project-architecture.mjs / verify*Contract.ts naming pattern here) and run it locally first, not just the generic lint/type suite.
- 2026-09-20 `conductor/t-179` — A command-prohibition contract test that does a bare substring match ('pm2 restart' not in source.lower()) against a whole script file will keep tripping on harmless advisory prose that happens to contain both words contiguously (two separate Write-Warning messages did, in two separate retry passes) -- match actual command-invocation syntax instead of any co-occurrence of the words, or a trivial wording fix keeps re-triggering the same false positive at a different line.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-21T00:57:50Z_
