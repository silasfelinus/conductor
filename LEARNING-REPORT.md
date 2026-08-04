# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-04T00:29:00Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **496**
- Outcomes: blocked: 13, cancelled: 1, done: 482
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
| interface-vision | 53 | 100% |
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
| software | 481 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 9 |
| actionable | 9 |
| transient | 8 |
| scope | 1 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `quality` — 9 occurrences; look for the shared cause across its records
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `transient` — 8 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-04 `interface-vision/t-036` — When a task note gives you the exact CI-side validator to reuse client-side (navManifest.ts here), mirror its field-construction one-to-one rather than approximating -- the isomorphic-by-design comment in the module was the signal that a straight port, not a reinterpretation, was correct. Also: a component gated requiredRole: ADMIN cannot be visually verified from an agent sandbox without admin credentials -- typecheck plus the same CI script the component now reuses is the honest substitute, and it belongs explicitly in the PR flags rather than silently skipped. Separately: an automated close-task-event can land on main between opening a manual close_task.py PR and merging it -- check task-events/ and the live roadmap status again immediately before merging a close-out, not just once before opening it, or the merge 405s on a conflict against a transition that already happened.
- 2026-08-03 `interface-vision/t-035` — A registry helper (getModelCards()) existing, exporting cleanly, and being independently correct is not evidence it is wired in -- grep call sites, not just definitions, whenever a task note says a function "is defined but never called anywhere." pageStore.cards had two isX() type-guard branches that looked exhaustive but silently fell through to a channel-tab fallback for every string cards: value; the missing branch was a single conditional, but nothing in the type system or existing tests flagged the dead code path.
- 2026-08-03 `interface-vision/t-034` — Once a warning baseline reaches zero, promote the invariant to an error and reuse the same predicate the runtime uses. Keeping a separate validator recreates drift even when both implementations look trivial.
- 2026-08-03 `interface-vision/t-028` — Salvaged from the implementing session's own close-out PR (conductor #1636, opened but never merged -- superseded by this session's reconciliation before it landed). That session hit a real task-ID collision mid-work: its own new task got numbered t-078, but a concurrent session claimed t-078 for an unrelated mobile workspace-header fix and merged first, so GitHub reported the PR unmergeable. Recovered per the documented rotation-collision protocol -- merged current main, kept main's t-078 untouched, renumbered the new task to t-079 via next_free_task_id.py, and verified the diff was scoped to only the intended change before re-pushing. No lost work on either side, no force-push. Filed here as a second confirmed real-world instance of the task-ID collision failure mode the rotation-collision protocol exists to catch.

- 2026-08-03 `interface-vision/t-028` — Closed as done during this session's state-reconciliation pass: the task's own note already documented that its scope had been deliberately narrowed to a schema-only landable core (kind_robots PR #1381, confirmed merged), with the remaining wiring split into a dependent follow-on (t-079). The roadmap had been left at status: review rather than done after the bookkeeping PR merged, which also meant t-079 (depends_on: t-028) was marked status: ready despite its dependency not showing done -- both corrected together. check_pr_merged_drift.py's own connectivity limitation in this sandbox (raw urllib 403s on api.github.com) means it cannot verify referenced PR numbers itself and always exits non-zero for this class of task; the fix is to verify via GitHub MCP tools (as CLAUDE.md's own runbook says) rather than treating every drift-check non-zero exit as unresolved.

- 2026-08-03 `interface-vision/t-032` — Naively calling a store's existing updateX(id, updates) action with only the single field being toggled ({ allowReviews: bool }) is unsafe unless you've read the payload-building function it calls first: rewardStore's toRewardPayload() and scenarioStore's toScenarioPayload() both rebuild the ENTIRE PATCH payload from whatever partial object is passed in, filling missing fields with defaults (toRewardPayload defaults a missing name to '', toScenarioPayload defaults missing intros to '[]') -- a naive single-field patch would have silently wiped the reward's name or the scenario's intros on toggle. Bot's and Character's equivalent payload builders are plain spreads, so a single-field patch is safe there but not elsewhere; the two families look identical from the call site and are not safe to treat the same without reading the payload builder itself. Also found and fixed a real latent bug this way: toRewardPayload's field whitelist was missing allowReviews entirely, so the API-side field t-011 already shipped could never actually be set from the reward edit form even before this task, a silent no-op nobody had noticed.

- 2026-08-03 `conductor/t-096` — A task selector that only checks status/claimability (run_worker.py's find_ready_task, used by select_role.py) let interface-vision/t-017 -- an umbrella sweep whose own note already said every bucket but one was delegated to t-058 -- get claimed anyway, wasting a session's cycle. Two independent "pick next ready task" implementations (run_worker.py and next_ready_task.py) had already drifted once before this fix; when a roadmap task can legitimately delegate its remaining scope to a named sibling, encode that relationship as a structured field (remaining_scope_task) that every selector checks, not just prose in the note that only a human or a careful session catches by reading the full history.
- 2026-08-03 `interface-vision/t-075` — A kaizen task filed from a filename match alone ("character-flip-card.vue" looks like it should share butterfly-flip.vue's bug) can be wrong -- this file turned out to be an unrelated 900-line dashboard with a stale copy-pasted header comment from a similarly-named file. Verify the actual file content disproves or confirms the premise before writing any fix; closing a task with a corrected note and no diff is the right outcome when the premise does not hold, not a failure. Reading the disproven file also surfaced a real, unrelated bug (CharacterFlipCard has zero defineProps and silently ignores its character prop) -- filed separately as t-076 rather than folded into this task's diff, keeping scope discipline even for an accidental discovery.
- 2026-08-03 `interface-vision/t-017` — A component with both a 3D-flip mode and a fade mode needs a fundamentally different scroll-ownership fix per mode: flip mode already v-if-excludes the inactive face (never double-scrolls), but fade mode renders both faces simultaneously for the opacity transition, so a static overflow-y-auto on both faces gives two live scroll regions at once. Toggle overflowY per face on the same state (isFlipped) that drives the fade, rather than assuming one static class covers both modes. Other flip/fade-card components (e.g. character-flip-card.vue) likely share the same latent bug -- filed t-075 to check.
- 2026-08-03 `interface-vision/t-061` — Two mutually-exclusive v-if/v-else branches gated by a fixed-per-session flag (admin vs. non-admin) are the same SHAPE A pattern as tab switches -- hoist one shared kr-scroll wrapper above the pair instead of each branch declaring its own overflow-y-auto.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-04T00:29:00Z_
