# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-01T04:39:08Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **437**
- Outcomes: blocked: 13, cancelled: 1, done: 423
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
| dream-cycle | 18 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| kind-robots | 39 | 97% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 46 | 100% |
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
| software | 422 | 99% |

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

- 2026-07-31 `dream-cycle/t-022` — Keep operational CLI commands and agent startup instructions under regression tests when a generator contract is rewritten.
- 2026-08-01 `model-builder/t-037` — When a guard clause and a genuine failure path share one return value (autoBuildItem's `false` covered both "another action already owns this item" and "a stage actually failed"), any caller that tallies outcomes across many calls (batchAutoBuild/autoBuildRun's "N/total committed" summary) loses the distinction and reports a busy-but-fine item the same as a broken one. Widening the return type to name each outcome explicitly (here, a three-way 'committed' | 'skipped' | 'failed' instead of a boolean) fixes it at the source instead of adding a second out-of-band flag the caller has to remember to check.

- 2026-08-01 `model-builder/t-029` — A same-item reentrancy guard (autoBuildItem vs itself, PR #1223) is only half the concurrency picture when a "do everything" action (Auto) and several "do one thing" manual actions (Generate candidate/Draft with AI/Execute commit) can both reach the same underlying operation for the same item. Guarding the automatic path against itself doesn't guard it against a manual path already in flight -- the automatic path just sees the stage as "not yet approved" and proceeds, firing a second concurrent request. When a store has both a batch/auto entry point and matching manual single-stage entry points into the same underlying calls, check for a cross-guard (auto vs. manual in-flight state) in addition to the obvious self-vs-self guard.

- 2026-07-31 `model-builder/t-029` — Extended the isGenerating/isQueued gate class (PR #900) with a subtler variant: isQueued read item.artJobId, but the async regenerate path sets item.queueState synchronously and item.artJobId only after two awaited network round-trips resolve, leaving a real window where the gate read false during a genuine in-flight regenerate. When a store documents two fields for the same async operation (an immediate synchronous progress flag vs. a value only available after I/O resolves), a UI gate checking the wrong one is easy to miss because both fields end up true/set for most of the operation's lifetime -- only the initial network-latency window exposes the gap. Worth grepping for this pattern (a gate reading a post-await field when a pre-await field exists for the same purpose) across other async store actions with a similar two-field shape.

- 2026-07-31 `davinci/t-016` — Two source-of-truth divergences found in one sweep, both invisible to status counts. (1) The kind_robots Projects board computed progress from milestone status alone while conductor's build_status.py falls back to the task ratio; since agents close tasks but rarely flip milestones, 16 of 43 projects showed 0% against real values up to 100%. The board looked plausible rather than broken, which is why it survived -- the 27 correct rows made the 16 wrong ones read as genuinely-unstarted work. Lesson: when the same number is computed in two repos, the parity check belongs in CI from the start; a transcription of the other side's formula asserted against fixtures is cheap and catches drift that no amount of reading either implementation alone would surface. (2) davinci was flipped `finished` while its central gap sat unfiled, because the task whose output was a spec deliberately deferred filing the build task it specced. "All tasks done" and "project done" diverge exactly at spec-only closures. A spec task that defers its own implementation should file the follow-up before going done, even as a stub -- otherwise the deferral exists only in prose inside a note field, where every lifecycle check is structurally blind to it. Also confirmed a third instance of the roadmap-scan-without-lifecycle-join bug class, this time in build_conductor_summary.py's fetch_roadmaps(): it was surfacing retired approval-portal tasks under ACTION NEEDED every cycle. CLAUDE.md documents this bug for the human sweep; the automated builder had it independently. Fixing it removed 15 phantom needs-human gates. Worth auditing every glob("projects/*/roadmap.yaml") caller rather than waiting for a fourth.

- 2026-07-29 `model-builder/t-029` — Checking a prior cycle's specific unticketed lead first (this time, batchApproveStage's possible isStageEditable gap) before starting a broad re-read is an efficient variant of the exclusion-list pattern: it closed the lead out cleanly (confirmed already-safe) and freed the rest of the cycle to find a genuinely new bug (autoBuildItem() approving PITCH/FIELDS_AND_PROMPTS with empty content when draftText() fails). Separately, this cycle nearly reverted its own claim_task.py claim: set_task_field.py was run against a stale local roadmap checkout immediately after claim_task.py's direct-to- origin/main push, which would have silently clobbered the claim if committed blind -- caught by diffing against origin/main before pushing, per this file's own repeated "fetch before you push" guidance. A session that calls claim_task.py (or any direct-to-main script) should fetch/rebase locally before its next roadmap edit in the same cycle, not just before the final close-out push.

- 2026-07-29 `model-builder/t-029` — Extended the review-gate-bypass bug class (already fixed for canApproveAssets, batchDraftField/batchSetField, and previewCommit) to the single-item draftText() path: the Approve button for PITCH/FIELDS_AND_PROMPTS has no isDrafting gate, so a stage can be approved while its own AI draft is still resolving, and the draft would silently overwrite the approved content with no re-review. This task's note (67+ PROGRESS/REVIEWED entries) is now the same note-bloat shape the immediately preceding LEARNING.yaml entry describes for coloring-book/t-037 -- worth the same run-log.md extraction next cycle, before it slows down reading/diffing the roadmap further.
- 2026-07-29 `coloring-book/t-037` — Note-bloat extraction (moving a recurring task's accumulated RAN/incident history out of the roadmap note: field into a dedicated run-log.md, per the ai-art-academy/t-010 precedent) is now a proven, repeatable pattern for any long-running recurring task whose note has grown large enough to slow down reading/diffing the roadmap -- verify the move with a byte-identical diff check before trimming the original, and add a run_log: pointer field rather than just prose, so a script can find the log mechanically later.
- 2026-07-29 `taskmaster/t-002` — kind_robots PR #1157 merged clean on first pass, all 11 checks green including the project-specific "Taskmaster checkpoint contract" -- confirming in advance that the contract verifiers only assert against stores/taskmasterStore.ts and components/pages/taskmaster-page.vue content (not stores/todoStore.ts, the actual file touched) avoided a wasted CI round trip on a fix that was never going to trip those specific checks.
- 2026-07-29 `taskmaster/t-001` — The audit surfaced a real, silent regression rather than a documentation gap: a Serendipity->Taskmaster rename left stores/todoStore.ts's AGENT-todo badging heuristic matching the pre-rename icon/title/description shapes only, so every Taskmaster-created needs-human todo since the rename silently miscategorized with no error. Renames that touch generated-content shape (icons, title/description prefixes used elsewhere as string-matched classifiers) need a grep for every consumer of the old string shape, not just the producer -- an audit task that reads the producer in isolation would have reported this capability as "present and working" when it was actually broken for every row created after the rename.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-01T04:39:08Z_
