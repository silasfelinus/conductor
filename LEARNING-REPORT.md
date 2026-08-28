# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-28T12:33:55Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **808**
- Outcomes: blocked: 16, cancelled: 1, done: 791
- Success rate: **98%**
- Average passes on successful tasks: **0.1**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 70 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 9 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 25 | 96% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 83 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 37 | 97% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 86 | 100% |
| kapowarr | 48 | 100% |
| kind-economy | 6 | 100% |
| kind-robots | 53 | 98% |
| kindrobots-unraid | 5 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 9 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 79 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 10 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 16 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 792 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 14 |
| actionable | 12 |
| transient | 11 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 14 occurrences; look for the shared cause across its records
- failure category `actionable` — 12 occurrences; look for the shared cause across its records
- failure category `transient` — 11 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-28 `cthulhuquarium/t-060` — Extracting a shared useOneShotReveal() composable for revealedUnlock/Hatch/Breed (kind_robots#2180) kept every external ref/function name on the store unchanged, so no component needed touching -- confirming a presentation-only refactor is genuinely presentation-only by checking call-site signatures, not just behavior, avoids a should-have-been-a-no-op PR accidentally growing scope.
- 2026-08-28 `cthulhuquarium/t-059` — Reusing an existing formatting idiom (formatBestStats()/BEST_STAT_LABELS, t-031) instead of inventing a parallel one kept the diff to a single small helper (tankStockStatsLine()) that reshapes TankStock's stat<Name> fields into the same BestiaryStatBlock shape the Ichthyonomicon already consumes. Worth flagging as its own kaizen (t-062) rather than scope-creeping into this task: making an individual's rolled stats visible for the first time immediately raises the follow-on question a player will actually ask -- "what would this sell for?" -- which the Sell button still doesn't answer despite the price already varying per individual (sellPrice() in aquariumEconomy.ts). Noticing a UI change makes a previously-invisible economic question visible is a useful generic signal for kaizen filing, distinct from noticing a code-shape duplication.
- 2026-08-28 `cthulhuquarium/t-057` — A task that reads as UI-only ("show a countdown") can be blocked on a small, shared infrastructure gap: performFetch() (stores/utils.ts) silently dropped every response's `meta` object, and at least 17 server routes already return one. Worth checking whether a "just read this field" task's data is actually reachable before assuming the store layer already exposes it -- the fix here (an optional second generic on ApiResponse<T, M>, purely additive/backward-compatible) was small, but skipping that check would have meant reaching for a server-side workaround (a second field on `data`, or a new endpoint) that the task's own note explicitly said wasn't needed.
- 2026-08-28 `cthulhuquarium/t-056` — A repeated-shape kaizen (three near-identical one-shot-signal refs) is worth pausing on before extracting: the task named three call sites (bestiaryJustCompleted, milestoneToastQueue, finaleJustTriggered), but a fourth near-identical trio (revealedUnlock/revealedHatch/revealedBreed, a typed-payload variant of the same shape) was sitting right next to it in the same file. Scoping the extraction to exactly what the task named (rather than also folding in the sibling pattern) kept the diff small and reviewable, but the sibling was worth filing as its own immediate kaizen (t-060) rather than a speculative "if a fourth shows up" -- it already had three instances, the same threshold that triggered this task in the first place.
- 2026-08-28 `cthulhuquarium/t-055` — A task can bundle two deliverables in different repos without saying so explicitly -- here, a store/UI change (in-scope) plus content authoring in silasfelinus/cthulhuquarium, a GitHub repo entirely outside this session's access (not just connector-blocked within an in-scope repo, and not locally cloned). When a target repo isn't accessible at all, don't guess at its content from memory or skip that half silently -- split the task, land what's actually landable, and write a concrete handoff doc naming the exact repo, fields, and script for whoever has access next. Worth checking a task's own note for "and author/write/edit X" clauses naming a different project before claiming, since those are the ones most likely to span a repo this session can't reach.
- 2026-08-28 `mandarin-tutor/t-019` — A same-session kaizen filed off a just-merged task can be picked up immediately if it's the only ready work left in a leading-priority project -- no need to wait for a future cycle when the follow-up is small, mechanical, and reuses the pattern already verified.
- 2026-08-28 `mandarin-tutor/t-018` — When a shared notice ref (artNotice) backs multiple template call sites, check every call site before assuming one render location suffices -- and a task note's suggested "clear on the same trigger as X" can be wrong if X itself has no real clear trigger; verify the cited precedent actually holds before copying its pattern.
- 2026-08-28 `cthulhuquarium/t-050` — A kaizen task filed against a specific call site (purchaseSpeciesForUser) can be fully subsumed by later, unrelated-looking dependency work (t-029's breeding creation, t-041's egg hatching) that happens to wire the same helper for its own reasons -- always grep for every call site of the thing the task asks you to add (here: every AquariumStock-creating transaction) before writing new code, since the task may already be done.
- 2026-08-28 `cthulhuquarium/t-030` — t-031's currentlyOwned flag and dead "Re-order" button, and t-029's rolled stat* columns, were both built ahead of time specifically for this task -- t-030 landed as almost pure wiring (rotateShopStock + sellPrice, both pure functions in aquariumEconomy.ts) with zero migration, exactly as t-032's schema-first discipline intended. The one design risk this task's own note called out by name (rotating stock + selling creating a quiet permanent loss of access) was already fully solved by t-031's Ichthyonomicon before this task started -- confirms that flagging a trap in a task note AND building its fix into an earlier, unrelated-looking task (t-031) is a pattern worth repeating when a later task's safety depends on state a dependency already tracks.
- 2026-08-28 `cthulhuquarium/t-053` — t-018/t-028's justCompletedBestiary/firedMilestones purchase-response signals sat server-complete with zero frontend consumer for a full cycle -- the server-side gate (slot-cap increase, AquariumEvent log) working correctly gave no visible signal that the UI half was still missing. Worth periodically diffing a store's typed response interfaces against what the server actually returns, not just what the store currently reads off it.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-28T12:33:55Z_
