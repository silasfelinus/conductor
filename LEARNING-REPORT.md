# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-11T17:48:07Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **585**
- Outcomes: blocked: 13, cancelled: 1, done: 571
- Success rate: **98%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 64 | 98% |
| alexa-integration | 2 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 6 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 9 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 72 | 100% |
| conductor-app | 2 | 100% |
| davinci | 3 | 100% |
| digital-storefront | 28 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| interface-vision | 83 | 100% |
| kind-robots | 49 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 51 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 8 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 569 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 12 |
| actionable | 9 |
| transient | 9 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 12 occurrences; look for the shared cause across its records
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `transient` — 9 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-11 `interface-vision/t-104` — Slice 43 of the general-layout-pass kr-note conversion: a genuinely fresh repo-wide grep for the exact hand-rolled rounded-2xl border border-{status}/40 bg-{status}/10 p-4 text-{status} shape (rather than continuing from slice 42's leftover candidate list) found the pool down to exactly two remaining live candidates (giftshop-manager.vue, wonderlab-review-rollout.vue), both converted clean. Explicitly re-verifying with a fresh sweep rather than assuming a stale list is exhaustive (or empty) is worth the cost each time the candidate pool is this close to zero -- a session that only trusts the last note's leftovers risks stopping early or re-checking already-excluded files.

- 2026-08-11 `storybook/t-013` — A bounded-slice task that keeps re-arming to ready across several same-day cycles (three prior PRs: #1740, #1741, #1745) is not necessarily still open -- read the component directly against the task's own stated scope before assuming there is always another slice. Here the wizard's remaining plain field (one textarea) was the entire gap; a ten-line diff closed it, and the task's own note had already flagged this as a likely stopping point. Checking cheaply (grep the shared picker components for kr-panel-flat, read the one remaining section) before claiming avoided a fifth guessed-scope PR.
- 2026-08-11 `coat-dance/t-002` — A content-kind task that already reached needs-human can come back with the human's reply embedded in the note itself (via Kind Robots For You) rather than a roadmap-field edit -- check the tail of the note for an unprocessed human reply before assuming a status: ready/needs-human mismatch is drift. Here Silas had already approved the tool picks and asked a direct follow-up question; the task just needed the follow-up answered and its own pre-written "set status: ready on t-003 yourself" instruction carried out, not a new research pass.
- 2026-08-11 `taskmaster/t-003` — A "delivery verification" check that only tests ArtJob/DB completion status or a git-ignored local checkout can never catch a wrong-but-present file at the destination -- it has to HEAD+fetch the actual public media origin (media.acrocatranch.com for kind_robots) and, ideally, spot-check content against intent. This task sat blocked for two weeks on a real infra gap (no confirmed delivery precedent), but once conductor PR #2047 fixed destination-preservation and KR_API_TOKEN happened to be present, the missing piece was a live check against the true delivery target, not another generation attempt -- and that same live check surfaced an unrelated pre-existing wrong asset that every completion-status-only check had missed for two weeks.
- 2026-08-11 `storybook/t-012` — Keep drag gestures additive to an already-accessible control path: native mouse drag can live on the card artwork while a dedicated touch handle uses Pointer Events, avoiding both mouse-only drag and accidental drags from the role buttons.
- 2026-08-11 `storybook/t-019` — When a task spec says a contract should "feed a synthetic value through the component's logic," check whether that logic lives only inline in a Vue SFC's <script setup> -- if so, extract it into a small pure exported function first so the contract genuinely executes the logic (and a future edit that re-inlines it fails loudly) rather than falling back to a source-string-match style that only proves the keyword is present nearby.
- 2026-08-10 `davinci/t-023` — A long-running interactive flow (life run, quest, playthrough) needs a UI-level exit affordance from day one, not just a resolve-screen reset -- this one shipped with only a manually-cleared localStorage key as the real "abandon" path for weeks before the gap was caught. Reusing the existing reset function (playAgain) behind a window.confirm kept the fix to ~20 lines with no new state.
- 2026-08-10 `model-builder/t-040` — Pair server-side stale-write protection with matching client affordance guards when a conflicting action is known: the server preserves correctness, while the UI prevents users from entering the race in the first place.
- 2026-08-10 `model-builder/t-029` — items/[id]/commit.post.ts fetched the build item once at the top of the request and built the final stageStatuses write from that request-start snapshot, even though the write in between (promoteAsset/updateText/createRecord+linkSourceToTarget, the last inside a multi-step prisma.$transaction) can be slow -- and nothing blocks the client from reopening another already-approved stage (a fast PATCH /items/:id) while the commit POST is in flight, so the stale-snapshot final write could silently clobber that concurrent edit back to 'approved'. A distinct bug class from the ~30 prior client-side store races this recurring task has found: a server-side stale-snapshot full-object overwrite across a slow awaited write. Worth checking any route that reads a record early and writes a computed blob back late for the same shape -- re-read immediately before the final write rather than trusting the request-start snapshot.

- 2026-08-10 `storybook/t-011` — A strict WonderLab preview-audit CI check treats every new component with required props as a regression until it gets a fixture or skip reason -- even one extracted purely to avoid tripling markup in the same PR that adds it. Budget for that check whenever a component split introduces a new required-prop component; caught mid-PR via the subscribed PR-activity webhook rather than a manual poll, which is the faster signal path for a session's own open PR.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-11T17:48:07Z_
