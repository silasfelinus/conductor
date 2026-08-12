# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-12T05:30:04Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **592**
- Outcomes: blocked: 13, cancelled: 1, done: 578
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
| digital-storefront | 29 | 100% |
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
| model-builder | 56 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 9 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 576 | 99% |

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

- 2026-08-12 `model-builder/t-029` — verifyModelBuilderCompletionGate.ts's post-await stage-write scanner only matches direct `item.stages.KEY = ...` assignments in async functions -- it can't see a write that happens indirectly through a synchronous helper call like approveStage() (bracket-notation write inside its own body). autoBuildItem() slipped an unconditional approveStage() call past that existing guard for exactly this reason, silently re-approving a stage a concurrent Edit click had just marked stale mid-await. A new narrow per-call-site guard (verifyModelBuilderAutoBuildApprovalRaceGuard.ts) closed this instance; the completion-gate scanner itself would be more robust generalized to flag any approveStage/rejectStage call after an await with no adjacent status check, rather than needing a new file per call site each time this shape recurs.

- 2026-08-12 `model-builder/t-029` — A prior session's branch-medic flag (stranded worker/model-builder-t-029-20260811-c4a91f, real tested fix never turned into a PR) was picked up and opened as PR #1792 by a later session, then reviewed/merged cleanly by this one -- the cross-session rescue handoff described in AGENTS.md's branch-medic role worked end-to-end without any direct coordination between the three sessions involved.
- 2026-08-11 `digital-storefront/t-005` — Routine state reconciliation (checking a PR referenced by a hard-gated needs-human task, not because anything prompted it) found Silas had already merged kind_robots #1668 himself -- decisive objective evidence per docs/state-reconciliation.md that he'd answered the gate's own multiple-choice question. But the merge only covered 4 of the 5 originally-flagged routes; a fifth (rewards/random.get.ts) still had the identical unfiltered-access gap. Closing a human gate on "the human acted" evidence still needs a scope check against the gate's own original list -- a partial fix that matches the merged precedent exactly is safe to finish without going back for a second decision, since the policy call was already made, but silently marking the whole task done on the merge alone would have left a real gap open while reporting it closed.

- 2026-08-11 `model-builder/t-029` — An Explore subagent given an explicit list of every bug class already fixed this same day (two singleton-clearing fixes plus an aria-pressed fix) and told to read the actual store/component code rather than trust a summary found a genuinely different bug shape: three textareas bound to local component refs that only pushed to the store on @change (blur), so the store's own "don't clobber a newer edit" guard in draftText() -- which only compares against the store's value -- couldn't see text the user was still mid-typing. The fix (disable the textarea while its own field is drafting) mirrors a gate already present one UI element over (the "Draft with AI" button), which is often a good signal that an adjacent, un-gated control was simply missed rather than intentionally left open.

- 2026-08-11 `model-builder/t-029` — A stranded worker/* branch (aria-pressed accessibility fix on the recipe-chip selector) had no PR -- the review-claim protocol worked cleanly end to end: posted a REVIEWING marker, waited out all 15 exact-head checks, merged kind_robots #1784. Worth reinforcing: rescuing a stranded branch this way is cheaper than re-deriving the same fix from scratch, and posting the marker first avoided any risk of a concurrent session reviewing the same PR.
- 2026-08-11 `storybook/t-010` — An Explore subagent reading the Storybook store/composables/components directly (not just filenames) found a real soft-lock: answerCurrentBeat() recorded the reader's answer before weaveBeat() generated the next scene, so a failed generation call left the answer committed with no way to retry (awaitingAnswer requires no answer yet, canFinish requires >= 2 beats -- both false right after a failed opening-beat answer). Fixed by awaiting weaveBeat()'s result and rolling the answer/branchHistory entry back on failure. Also worth recording: the repo's capture-group-guard CI check flagged the new guard script's own `match.exec()` result being indexed after an `assert.ok(match, ...)` check rather than one of its four recognized guard shapes (optional chaining, `if (!match) return`, default-destructure, or `match!`) -- assert-based narrowing isn't one of them, so a plain `if (!match) throw` is the safe default for any new `.exec()`/`.match()` call site in this repo, not just assert.ok.

- 2026-08-11 `model-builder/t-029` — An Explore subagent re-scanning the full component/store surface against an explicit exclusion list of every bug class prior cycles already fixed (rather than a fresh, unscoped read) found resetRun() leaking the exact store-wide in-flight-singleton bug resetAll() was fixed for (PR #1778) through a second, more commonly-clicked path ("New run", cancelRun()) the existing guard didn't cover. When a fix closes one entry point to a shared-state bug, checking for sibling entry points to the same state (not just new bug classes) is worth a dedicated pass -- the guard here was scoped to the function name, not the underlying invariant, so it silently missed the twin.

- 2026-08-11 `interface-vision/t-104` — Slice 43 of the general-layout-pass kr-note conversion: a genuinely fresh repo-wide grep for the exact hand-rolled rounded-2xl border border-{status}/40 bg-{status}/10 p-4 text-{status} shape (rather than continuing from slice 42's leftover candidate list) found the pool down to exactly two remaining live candidates (giftshop-manager.vue, wonderlab-review-rollout.vue), both converted clean. Explicitly re-verifying with a fresh sweep rather than assuming a stale list is exhaustive (or empty) is worth the cost each time the candidate pool is this close to zero -- a session that only trusts the last note's leftovers risks stopping early or re-checking already-excluded files.

- 2026-08-11 `storybook/t-013` — A bounded-slice task that keeps re-arming to ready across several same-day cycles (three prior PRs: #1740, #1741, #1745) is not necessarily still open -- read the component directly against the task's own stated scope before assuming there is always another slice. Here the wizard's remaining plain field (one textarea) was the entire gap; a ten-line diff closed it, and the task's own note had already flagged this as a likely stopping point. Checking cheaply (grep the shared picker components for kr-panel-flat, read the one remaining section) before claiming avoided a fifth guessed-scope PR.
- 2026-08-11 `coat-dance/t-002` — A content-kind task that already reached needs-human can come back with the human's reply embedded in the note itself (via Kind Robots For You) rather than a roadmap-field edit -- check the tail of the note for an unprocessed human reply before assuming a status: ready/needs-human mismatch is drift. Here Silas had already approved the tool picks and asked a direct follow-up question; the task just needed the follow-up answered and its own pre-written "set status: ready on t-003 yourself" instruction carried out, not a new research pass.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-12T05:30:04Z_
