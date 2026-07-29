# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-29T18:16:22Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **429**
- Outcomes: blocked: 13, cancelled: 1, done: 415
- Success rate: **97%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 55 | 98% |
| alexa-integration | 2 | 100% |
| animation-manager | 12 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 6 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 23 | 100% |
| conductor | 59 | 100% |
| conductor-app | 2 | 100% |
| davinci | 1 | 100% |
| digital-storefront | 24 | 100% |
| dream-cycle | 17 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| kind-robots | 39 | 97% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 41 | 100% |
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
| software | 414 | 99% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 9 |
| quality | 7 |
| transient | 6 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `quality` — 7 occurrences; look for the shared cause across its records
- failure category `transient` — 6 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-29 `coloring-book/t-037` — Note-bloat extraction (moving a recurring task's accumulated RAN/incident history out of the roadmap note: field into a dedicated run-log.md, per the ai-art-academy/t-010 precedent) is now a proven, repeatable pattern for any long-running recurring task whose note has grown large enough to slow down reading/diffing the roadmap -- verify the move with a byte-identical diff check before trimming the original, and add a run_log: pointer field rather than just prose, so a script can find the log mechanically later.
- 2026-07-29 `taskmaster/t-002` — kind_robots PR #1157 merged clean on first pass, all 11 checks green including the project-specific "Taskmaster checkpoint contract" -- confirming in advance that the contract verifiers only assert against stores/taskmasterStore.ts and components/pages/taskmaster-page.vue content (not stores/todoStore.ts, the actual file touched) avoided a wasted CI round trip on a fix that was never going to trip those specific checks.
- 2026-07-29 `taskmaster/t-001` — The audit surfaced a real, silent regression rather than a documentation gap: a Serendipity->Taskmaster rename left stores/todoStore.ts's AGENT-todo badging heuristic matching the pre-rename icon/title/description shapes only, so every Taskmaster-created needs-human todo since the rename silently miscategorized with no error. Renames that touch generated-content shape (icons, title/description prefixes used elsewhere as string-matched classifiers) need a grep for every consumer of the old string shape, not just the producer -- an audit task that reads the producer in isolation would have reported this capability as "present and working" when it was actually broken for every row created after the rename.
- 2026-07-29 `dream-cycle/t-019` — An unrelated-looking PR (#1399) had already landed both a fix and its matching tests for public/rewards/... path handling in relay_media_agent.py, all green -- but the tests locked in the same wrong assumption as the code (folding the reward-asset root into the images root instead of treating it as a real sibling directory), including a test explicitly named to assert away the correct sibling-root design. A passing, internally-consistent test suite is not proof a fix matches reality when the tests were written by the same reasoning that produced the bug -- cross-check against the actual external system (here: the target repo's real folder layout) before trusting "tests pass" as sufficient verification, especially when correcting or building on another agent's recent, already-merged work.
- 2026-07-29 `coloring-book/t-022` — recover_timed_out_job()'s except-block guard in consume_coloring_book_color_art.py only preserved a stuck job's "job N" reference when the failure text literally contained "ANTHROPIC_API_KEY" -- any other exception during a recovery attempt (missing local dependency, transient network error checking job status) silently destroyed the reference, forcing the next pass into a genuine duplicate ArtJob submission for an already-completed render. Same failure shape as the ai-art-academy/t-010 fauvism incident: "status implies delivered/dead" reasoning is too eager whenever a script decides to discard a recovery pointer. Fixed with a narrow RecoveryAbandoned exception marking only the backend-confirmed-dead cases; every other exception now preserves the reference unconditionally. General lesson: a recovery/reconciliation guard should default to "preserve the pointer," and require an explicit, backend-confirmed signal to discard it -- never infer "safe to discard" from matching one specific known error string.
- 2026-07-29 `conductor/t-095` — consume_art_requests.py's enqueue()->wait_for_job() gap: a submitted ArtJob's id was only ever printed to stdout, never persisted, before the (up to 600s) wait for completion -- so a timeout, FAILED/CANCELLED job, or killed process left no durable trace of which ArtJob had actually been submitted for a given request, exactly the shape of the ai-art-academy/t-010 fauvism incident (an id known only from a session's own prose, unrecoverable once out of context). Fixed by recording the id onto the request's own entry immediately after submission succeeds, before the blocking wait -- the general lesson: any script that submits an async job and then blocks waiting on it should persist the job id at submission time, not at completion time, so a timeout or crash mid-wait still leaves a recoverable trail. Separately confirmed via a new regression test that the non-zero-exit half of this kaizen was already correct; not every suspected two-part gap turns out to have two real parts.
- 2026-07-29 `media-watchlist/t-006` — This recurring polish task's own note pointed at a stale kaizen (Month/Season filters) that t-012 and t-016 had already closed two cycles earlier -- re-implementing it blind would have been a pure no-op. Re-diffing BROWSE-UX.md against the live components before picking a slice caught the drift and surfaced a different, still-open gap (Entry Detail's "Related entries" section, §3) that the note never flagged. Kaizen: on a recurring task with a multi-cycle PROGRESS history, treat the latest PROGRESS note's "not done yet" list as a hypothesis to verify against current main, not a ready-made todo -- prior cycles closing kaizens out-of-band (via their own follow-on tasks) can leave the recurring task's own note pointing at already-finished work.

- 2026-07-29 `model-builder/t-029` — After ~20 cycles finding only client-side store races (singleton-ownership guards, watch-clobber bugs, cancelled-run checks), this cycle found a genuinely different bug class: the server-side commit route (server/api/model-builder/items/[id]/commit.post.ts) never checked item.stageStatuses before executing the durable write, so the entire PITCH->FIELDS_AND_PROMPTS->GENERATE_ASSETS->COMMIT human-approval gate was enforced only client-side and could be bypassed by a direct POST. Kaizen: when a recurring bug-hunt task has exhausted one layer of a feature (here, the Pinia store's in-memory races), the next productive lens is the layer below it (the server route trusting client-enforced invariants) rather than re-scanning the same layer for a smaller variant of the same bug shape.

- 2026-07-29 `appmaker/t-012` — This "polish and upgrade front-end" task type had been repeatedly re-picked across cycles with steps (1) art and (3) admin-Placements backfill blocked, and step (4) already marked "fully covered" by an earlier cycle -- risking each new pickup being a pure no-op. Dispatching a fresh Explore pass specifically hunting for bugs (not re-checking the same three blocked steps) found two real, previously-unfixed issues: a missing request-sequencing guard in appmaker-page.vue's refresh() (concurrent onMounted/button/post-create calls could let a stale response overwrite fresh state) and a conductorStore.fetchProjects(force=true) call that silently no-op'd whenever any other fetch was already in flight, defeating every one of its five call sites that pass force:true expecting a real refresh. Kaizen: for any "polish" task whose obvious steps are all blocked/done, a targeted bug-hunt Explore pass over the actual shipped code is a reliable way to find genuine, safe, reversible work instead of re-confirming the same blocker note again.

- 2026-07-29 `model-builder/t-029` — Manual read-through of an async completion handler found a real, previously-unfixed race: pollAsyncArtJob cleared item.artJobId (the item panel's only "still working" signal, via isQueued) before its own finalizeQueuedArtImage network round-trip. On a regenerate, this let canApproveAssets briefly evaluate true using the item's stale prior artImageId, so a premature "Keep this asset" click could lock the stage to 'approved' moments before the finishing render silently overwrote artImageId/imagePath underneath it -- a fourth instance of this file's recurring "review gate silently bypassed" bug class (after canApproveAssets' original isGenerating/isQueued gap, the batch-editor stage-approval gate, and the cancelled-run guard). Fixed with a narrow status==='approved' check before the image write, plus a new textual regression checker (verifyModelBuilderApprovedAssetGuard.ts) mirroring the existing cancelled-run-guard/completion-gate checkers. Kaizen: this bug class keeps recurring in modelBuilderStore.ts's async completion paths -- a future cycle should consider whether verifyModelBuilderCompletionGate.ts's static ungated-write scan can be generalized from item.stages.KEY writes to cover item.artImageId/item.imagePath too, so the next instance is caught automatically instead of needing another manual read-through to find.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-29T18:16:22Z_
