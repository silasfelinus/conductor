# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-02T14:37:02Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **469**
- Outcomes: blocked: 13, cancelled: 1, done: 455
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
| dream-cycle | 18 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| interface-vision | 28 | 100% |
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
| software | 454 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 9 |
| actionable | 9 |
| transient | 6 |
| scope | 1 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `quality` — 9 occurrences; look for the shared cause across its records
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `transient` — 6 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-02 `interface-vision/t-025` — New whole-repository conformance rules should first measure the live debt through CI, then record that exact result as a shrink-only baseline so future violations fail without pretending historical debt is new.
- 2026-08-02 `interface-vision/t-022` — Composition-aware contracts need the same ratchet strategy as file-local contracts: measure existing debt explicitly, block additions immediately, and let future sweeps shrink the baseline instead of making the first honest measurement unmergeable.
- 2026-08-02 `interface-vision/t-021` — Re-verifying flagged-orphan components before deletion (not trusting a prior audit's flag blind) caught two false positives with live contract usage.
- 2026-08-02 `interface-vision/t-039` — Contract verifiers should emit concise pass/fail output; diagnostic source bundles need a real consumer or an explicit verbose mode.
- 2026-08-02 `interface-vision/t-020` — Achievement rewards must be granted atomically through server-side karma and mana ledgers; direct client balance patches are neither authoritative nor permitted.
- 2026-08-02 `interface-vision/t-046` — Extending an already-shipped pattern (t-019's earned-karma batch fetch) to a new consumer went cleanly because the task note itself flagged the one real risk -- "check whether the gallery you pick actually has a tagged award path before wiring it" -- and following that check up front (grepping refType call sites in reactions/index.post.ts and prompts/generate.post.ts) confirmed ArtImage was safe before writing any UI code. Picking the highest-traffic *already-tagged* consumer over an arbitrary one avoided shipping an always-empty badge.

- 2026-08-02 `interface-vision/t-019` — A task titled "show earned karma/mana" surfaced a real data-attribution bug on investigation, not just a missing display layer: REACTION_RECEIVED karma awards were tagging the Reaction row's own id as refId instead of the reacted-on object's id, making per-object aggregation impossible regardless of any UI work. Also worth remembering: grep for whether a "mana equivalent" code path is actually live before building UI for it -- ManaReason had SOCIAL_REACTION/SOCIAL_SHARE defined but never awarded anywhere, so the honest move was shipping karma-only and saying so, not fabricating a mana number to match the task title.

- 2026-08-02 `interface-vision/t-018` — The task note's orphan-audit claim ("only 6 components use displayStore.ts") was wrong in a load-bearing way -- it missed memoryStore.ts (a store, not a component) reading displayStore.viewportSize to size the live, routed Memory Dungeon board, and kind-loader.vue calling displayStore.initialize() as real app-startup wiring. Investigating before deleting (grep ALL importers, not just the ones matching the expected shape) caught this before it shipped as a silent behavior regression; the store was left in place and split into its own follow-up task (t-045) instead of forced through under the cleanup label.

- 2026-08-02 `interface-vision/t-014` — A dedicated research pass (Explore agent surveying existing layout-contract examples, karma/mana/achievement plumbing already shipped by t-010, and the User schema) before writing any code meant zero rework: every new UI section reused an existing store/component instead of duplicating one, and the only schema change needed was a single additive nullable column (introDismissedAt) for the one genuinely new piece of state (intro dismissal). Deliberately scoped out extending user-galleries.vue to the remaining two object types (Facets/Projects) rather than let the task grow past its landable core -- filed as a kaizen suggestion instead.

- 2026-08-02 `interface-vision/t-014` — kind_robots PR #1292 (implemented and reviewed by a different session earlier in the day) went stale against main after this session merged the unrelated PR #1293 a few minutes later -- both PRs ran `prisma generate` independently against overlapping generated-client scaffolding (prisma/generated/prisma/internal/class.ts), producing a real textual conflict GitHub correctly flagged as `mergeable_state: dirty` despite a local `git merge-tree` dry run initially looking clean. Fix was mechanical and low-risk: merge main into the PR branch, let `prisma generate` regenerate the one conflicting file fresh rather than hand-resolving it, verify (prisma validate + vue-tsc clean), push, wait for CI, merge. Same class of "regenerate, don't hand-merge" fix as the STATUS.md/workspace.html auto-gen convention, just for kind_robots' generated Prisma client -- worth generalizing that convention beyond conductor's own auto-gen files.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-02T14:37:02Z_
