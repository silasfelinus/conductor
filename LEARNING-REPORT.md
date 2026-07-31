# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-31T20:54:31Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **434**
- Outcomes: blocked: 13, cancelled: 1, done: 420
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
| coloring-book | 23 | 100% |
| conductor | 59 | 100% |
| conductor-app | 2 | 100% |
| davinci | 2 | 100% |
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
| model-builder | 44 | 100% |
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
| software | 419 | 99% |

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

- 2026-07-31 `model-builder/t-029` — Extended the isGenerating/isQueued gate class (PR #900) with a subtler variant: isQueued read item.artJobId, but the async regenerate path sets item.queueState synchronously and item.artJobId only after two awaited network round-trips resolve, leaving a real window where the gate read false during a genuine in-flight regenerate. When a store documents two fields for the same async operation (an immediate synchronous progress flag vs. a value only available after I/O resolves), a UI gate checking the wrong one is easy to miss because both fields end up true/set for most of the operation's lifetime -- only the initial network-latency window exposes the gap. Worth grepping for this pattern (a gate reading a post-await field when a pre-await field exists for the same purpose) across other async store actions with a similar two-field shape.

- 2026-07-31 `davinci/t-016` — Two source-of-truth divergences found in one sweep, both invisible to status counts. (1) The kind_robots Projects board computed progress from milestone status alone while conductor's build_status.py falls back to the task ratio; since agents close tasks but rarely flip milestones, 16 of 43 projects showed 0% against real values up to 100%. The board looked plausible rather than broken, which is why it survived -- the 27 correct rows made the 16 wrong ones read as genuinely-unstarted work. Lesson: when the same number is computed in two repos, the parity check belongs in CI from the start; a transcription of the other side's formula asserted against fixtures is cheap and catches drift that no amount of reading either implementation alone would surface. (2) davinci was flipped `finished` while its central gap sat unfiled, because the task whose output was a spec deliberately deferred filing the build task it specced. "All tasks done" and "project done" diverge exactly at spec-only closures. A spec task that defers its own implementation should file the follow-up before going done, even as a stub -- otherwise the deferral exists only in prose inside a note field, where every lifecycle check is structurally blind to it. Also confirmed a third instance of the roadmap-scan-without-lifecycle-join bug class, this time in build_conductor_summary.py's fetch_roadmaps(): it was surfacing retired approval-portal tasks under ACTION NEEDED every cycle. CLAUDE.md documents this bug for the human sweep; the automated builder had it independently. Fixing it removed 15 phantom needs-human gates. Worth auditing every glob("projects/*/roadmap.yaml") caller rather than waiting for a fourth.

- 2026-07-29 `model-builder/t-029` — Checking a prior cycle's specific unticketed lead first (this time, batchApproveStage's possible isStageEditable gap) before starting a broad re-read is an efficient variant of the exclusion-list pattern: it closed the lead out cleanly (confirmed already-safe) and freed the rest of the cycle to find a genuinely new bug (autoBuildItem() approving PITCH/FIELDS_AND_PROMPTS with empty content when draftText() fails). Separately, this cycle nearly reverted its own claim_task.py claim: set_task_field.py was run against a stale local roadmap checkout immediately after claim_task.py's direct-to- origin/main push, which would have silently clobbered the claim if committed blind -- caught by diffing against origin/main before pushing, per this file's own repeated "fetch before you push" guidance. A session that calls claim_task.py (or any direct-to-main script) should fetch/rebase locally before its next roadmap edit in the same cycle, not just before the final close-out push.

- 2026-07-29 `model-builder/t-029` — Extended the review-gate-bypass bug class (already fixed for canApproveAssets, batchDraftField/batchSetField, and previewCommit) to the single-item draftText() path: the Approve button for PITCH/FIELDS_AND_PROMPTS has no isDrafting gate, so a stage can be approved while its own AI draft is still resolving, and the draft would silently overwrite the approved content with no re-review. This task's note (67+ PROGRESS/REVIEWED entries) is now the same note-bloat shape the immediately preceding LEARNING.yaml entry describes for coloring-book/t-037 -- worth the same run-log.md extraction next cycle, before it slows down reading/diffing the roadmap further.
- 2026-07-29 `coloring-book/t-037` — Note-bloat extraction (moving a recurring task's accumulated RAN/incident history out of the roadmap note: field into a dedicated run-log.md, per the ai-art-academy/t-010 precedent) is now a proven, repeatable pattern for any long-running recurring task whose note has grown large enough to slow down reading/diffing the roadmap -- verify the move with a byte-identical diff check before trimming the original, and add a run_log: pointer field rather than just prose, so a script can find the log mechanically later.
- 2026-07-29 `taskmaster/t-002` — kind_robots PR #1157 merged clean on first pass, all 11 checks green including the project-specific "Taskmaster checkpoint contract" -- confirming in advance that the contract verifiers only assert against stores/taskmasterStore.ts and components/pages/taskmaster-page.vue content (not stores/todoStore.ts, the actual file touched) avoided a wasted CI round trip on a fix that was never going to trip those specific checks.
- 2026-07-29 `taskmaster/t-001` — The audit surfaced a real, silent regression rather than a documentation gap: a Serendipity->Taskmaster rename left stores/todoStore.ts's AGENT-todo badging heuristic matching the pre-rename icon/title/description shapes only, so every Taskmaster-created needs-human todo since the rename silently miscategorized with no error. Renames that touch generated-content shape (icons, title/description prefixes used elsewhere as string-matched classifiers) need a grep for every consumer of the old string shape, not just the producer -- an audit task that reads the producer in isolation would have reported this capability as "present and working" when it was actually broken for every row created after the rename.
- 2026-07-29 `dream-cycle/t-019` — An unrelated-looking PR (#1399) had already landed both a fix and its matching tests for public/rewards/... path handling in relay_media_agent.py, all green -- but the tests locked in the same wrong assumption as the code (folding the reward-asset root into the images root instead of treating it as a real sibling directory), including a test explicitly named to assert away the correct sibling-root design. A passing, internally-consistent test suite is not proof a fix matches reality when the tests were written by the same reasoning that produced the bug -- cross-check against the actual external system (here: the target repo's real folder layout) before trusting "tests pass" as sufficient verification, especially when correcting or building on another agent's recent, already-merged work.
- 2026-07-29 `coloring-book/t-022` — recover_timed_out_job()'s except-block guard in consume_coloring_book_color_art.py only preserved a stuck job's "job N" reference when the failure text literally contained "ANTHROPIC_API_KEY" -- any other exception during a recovery attempt (missing local dependency, transient network error checking job status) silently destroyed the reference, forcing the next pass into a genuine duplicate ArtJob submission for an already-completed render. Same failure shape as the ai-art-academy/t-010 fauvism incident: "status implies delivered/dead" reasoning is too eager whenever a script decides to discard a recovery pointer. Fixed with a narrow RecoveryAbandoned exception marking only the backend-confirmed-dead cases; every other exception now preserves the reference unconditionally. General lesson: a recovery/reconciliation guard should default to "preserve the pointer," and require an explicit, backend-confirmed signal to discard it -- never infer "safe to discard" from matching one specific known error string.
- 2026-07-29 `conductor/t-095` — consume_art_requests.py's enqueue()->wait_for_job() gap: a submitted ArtJob's id was only ever printed to stdout, never persisted, before the (up to 600s) wait for completion -- so a timeout, FAILED/CANCELLED job, or killed process left no durable trace of which ArtJob had actually been submitted for a given request, exactly the shape of the ai-art-academy/t-010 fauvism incident (an id known only from a session's own prose, unrecoverable once out of context). Fixed by recording the id onto the request's own entry immediately after submission succeeds, before the blocking wait -- the general lesson: any script that submits an async job and then blocks waiting on it should persist the job id at submission time, not at completion time, so a timeout or crash mid-wait still leaves a recoverable trail. Separately confirmed via a new regression test that the non-zero-exit half of this kaizen was already correct; not every suspected two-part gap turns out to have two real parts.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-31T20:54:31Z_
