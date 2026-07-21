# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-21T19:12:12Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **326**
- Outcomes: blocked: 12, done: 314
- Success rate: **96%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 35 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 8 | 100% |
| animation-studio | 1 | 100% |
| appmaker | 5 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 13 | 100% |
| conductor | 45 | 100% |
| conductor-app | 2 | 100% |
| digital-storefront | 12 | 100% |
| dream-cycle | 14 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 30 | 97% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 4 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 29 | 100% |
| mural-design | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 1 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 11 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 311 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 6 |
| actionable | 6 |
| transient | 4 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `quality` — 6 occurrences; look for the shared cause across its records
- failure category `actionable` — 6 occurrences; look for the shared cause across its records
- failure category `transient` — 4 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-21 `ai-art-academy/t-036` — A recurring rotation task (t-010) can strand a green, unmerged kind_robots PR at session end if the completion checklist only names the terminal-state requirement generically instead of listing 'poll CI and merge (or explicitly park) before the cycle ends' as its own explicit bullet -- this had already happened twice (PR #942, PR #814) under slightly different framings before it was made an explicit, lane-agnostic checklist item. When a recurring task's own history shows the same failure shape twice, generalize the fix beyond the specific lane/step where it was first noticed, since the underlying gap (an implicit 'PR opened' being mistaken for 'cycle done') can recur on any lane that opens a PR.
- 2026-07-21 `conductor-app/t-012` — Before assuming a feature needs new backend endpoints, check what the existing API already returns/accepts -- GET /api/dreams/:id already embedded up to 12 linked ArtCollections with up to 12 ArtImages each, and POST /api/conductor/art-request already existed pre-built and admin-gated, so the whole task (ArtCollection browsing + admin art-request form) was pure Flutter client work with zero kind_robots changes needed. Also: a sandboxed toolchain pinned to a fixed version can silently drift stale against CI's unpinned 'stable' channel and produce false-positive analyze errors (including on files never touched this cycle) -- when a fresh error appears on pre-existing code, suspect the toolchain version before the diff, and verify against the actual current stable before trusting the result.
- 2026-07-21 `conductor/t-075` — A reused coarse hour/rotation-label session id never breaks claim_task.py's correctness (it keys on project/task), but it does corrupt the audit trail when two concurrent sessions pick the same label within the same hour, making one session's TALKBACK/claimed_by history look like it belongs to another. Prefer a full ISO timestamp with seconds plus a task-specific suffix, or a random token, over a coarse label string.
- 2026-07-21 `kind-robots/t-042` — A new static-source contract test is only trustworthy once it's been proven to actually catch the pattern it claims to guard against -- write a synthetic violating sample first (cover edge cases like nested generics that could produce false negatives in a bracket-depth parser), confirm it fails as expected, then remove the sample and confirm the real codebase passes clean. Testing only the 'passes on real code' direction would have missed a parser bug that let violations through silently.
- 2026-07-21 `appmaker/t-009` — A cryptic CI type error in a file the task never touched is not automatically 'pre-existing and unrelated' -- it can be a genuine, if indirect, regression the diff triggered (here: 2 new server/api/** route files grew the typed $fetch route-key union just enough to push vue-tsc's TS2589 recursion limit on unrelated call sites). A same-tree local repro without the diff isn't conclusive either, since sandbox vs real CI can diverge -- cross-check against the base commit's actual CI history before concluding a failure is pre-existing. Root-causing (pinning $fetch's R generic, 12 files) was cheap once understood and is a durable fix, versus a band-aid on the one file CI happened to name first.
- 2026-07-21 `ruler-hooked/t-007` — A task can outlive its own blocker without anyone noticing: t-007's completion condition (PR #328 merged AND t-012 landing the playable screen meeting all four DESIGN-BRIEF m2 exit criteria) had been fully satisfied since t-012 merged earlier the same day, but t-007 itself still sat at status: ready/claimed pending someone to actually check and flip it. When a task's note already states an explicit, checkable completion condition, re-verify it directly (fresh checkout, self-tests, full typecheck) before assuming more code work is needed -- sometimes the task is closing bookkeeping, not new implementation.
- 2026-07-21 `ruler-hooked/t-012` — A task's retry_context can go stale when a human merges the referenced PR directly, bypassing the normal reject->retry->re-review loop (t-012's retry_context described a pass-1 rejection of kind_robots PR #329 written at 21:55Z on 2026-07-16, but Silas merged that same PR 9 minutes later at 22:04:56Z). Before acting on any retry_context for a cross-repo task, check whether the referenced PR already merged and re-verify against current target-repo main first -- don't assume a recorded rejection is still live. See conductor/t-074 (kaizen task filed this cycle) for the AGENTS.md doc fix.
- 2026-07-21 `media-watchlist/t-011` — Confirmed the same pattern as t-010's lesson: with the top of priority.yaml blocked on external infra (ai-art-academy t-019/t-035 need at least one landed thumbnail or a live relay; kind-robots t-033 was already rechecked clean 4x this same day), a small self-contained kaizen task one project down the list (server route + schema field already shipped, only the UI control missing) lands clean first pass with zero design ambiguity. Also: a chained `git fetch && git checkout <branch> && git pull` in one Bash call can get SIGTERM'd by the tool's 2-minute timeout mid-checkout on a repo with a large/rewritten history (kind_robots had just force-updated origin/main), leaving the working tree with hundreds of stray unstaged deletions/modifications/untracked files even though HEAD never actually moved. Recovery was safe here only because `git status` was checked immediately and confirmed nothing was staged and the tree had been clean moments before -- `git checkout -- .` + `git clean -fd` cleanly restored it. Split multi-step git network operations into separate, shorter Bash calls (or raise the timeout) instead of chaining them, so a slow fetch/checkout can't silently corrupt working-tree state mid-operation.
- 2026-07-21 `media-watchlist/t-010` — When most of the priority queue is blocked (art relay down, live Comfy box unreachable, daily creative-loop caps already used today), a kaizen task with a fully self-contained spec (write route + UI panel, no external service dependency) is the highest-value pick -- media-watchlist/t-010 landed clean first pass because BROWSE-UX.md already fully specified the UI/API contract and the schema fields existed from t-008, leaving zero open design questions.
- 2026-07-21 `conductor/t-028` — A stale-claim task with no PR/TALKBACK evidence of prior implementation work is safe to reclaim once past CLAIM_TTL_MINUTES via claim_task.py, but check the free-standing conflict risk on the follow-up status commit -- a direct-to-main claim commit (or its auto STATUS.md refresh) landing between a session's local edit and its push produces a real (not auto-gen-only) roadmap.yaml conflict on the task's own claimed_by/claimed_at/updated fields, since the session's local copy still shows the old stale values. Also: flutter test's first cold AOT compile can exceed several minutes in a CPU-constrained sandbox even though flutter analyze/pub get complete in under 20s -- budget for that gap rather than treating a slow flutter test as a broken toolchain.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-21T19:12:12Z_
