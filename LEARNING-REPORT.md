# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-23T20:09:39Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **735**
- Outcomes: blocked: 15, cancelled: 1, done: 719
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
| brainstorm | 22 | 95% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 79 | 100% |
| conductor-app | 4 | 100% |
| davinci | 7 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 83 | 100% |
| kapowarr | 47 | 100% |
| kind-economy | 6 | 100% |
| kind-robots | 50 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 78 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 14 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 719 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 14 |
| actionable | 10 |
| transient | 9 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 14 occurrences; look for the shared cause across its records
- failure category `actionable` — 10 occurrences; look for the shared cause across its records
- failure category `transient` — 9 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-23 `davinci/t-025` — Before scoping a 'extract the shared pattern between these two call sites' refactor, grep the WHOLE repo for the symbol being extracted, not just the two sites already named in the task note -- a third, byte-for-byte identical call site (taskmasterStore.ts) existed and was missed by hand-picking files instead of searching, only caught because a repo-owned contract test (verifyNarrativeArtPersistence.mjs) enforced the two stores stay in lockstep and failed CI. Also: running `prettier --write` on a whole pre-existing file to fix one targeted edit's formatting can reformat large unrelated regions if the file was already prettier-noncompliant before the change (confirmed via git stash/checkout) -- restore the pristine file and apply only the intended edit via a scoped replace, never a full-file --write, when touching a file the task doesn't already fully own.
- 2026-08-23 `brainstorm/t-028` — Following an already-established adapter pattern (Character/Scenario) end to end -- registry entry, gated CTA, contract-script assertion, workflow path trigger -- landed clean first pass with zero findings; the pattern itself, not novel judgment, was the main risk-reducer.
- 2026-08-23 `model-builder/t-029` — Cycle 57's fix covered three places that swap state.run for a different run (goToStep /selectSource, openRun's two branches, resumeRun's branch) without clearing the in-flight singletons resetRun/resetAll already clear -- but only checked whether each call site clears the singletons, not whether the RESPONSE feeding that call site could itself be stale. resumeRun() has exactly one call site (a component's onMounted) yet was still racy, because unmounting a Vue component does not cancel its in-flight promises: navigating away and back before a slow resumeRun() resolves creates a second concurrent call against the same Pinia singleton, and the older call's stale response can land after the newer one already resolved and the user moved on. Lesson for future cycles: "this function's call site is singular / not button-driven" is not the same guarantee as "this function cannot run twice concurrently" -- component remounts (navigation, not just explicit user clicks) are a second, easy-to-miss source of concurrent async calls against a shared store, and any async chain writing shared state on completion needs a request-ticket guard regardless of how simple its trigger looks.

- 2026-08-23 `conductor/t-123` — Kaizen from an earlier same-day session's mermaids-of-venice/t-013 wasted claim (conductor#2720). Added scripts/daily_gate.py, detecting a task whose note declares an explicit "Pacific calendar day" daily-gate contract and already records an outcome for today's Pacific date, and wired the skip into both task-selection paths -- next_ready_task.py's first_ready_task AND run_worker.py's find_ready_task. The second wiring mattered most: select_role.py's underlying "worker" recommendation (the path that actually surfaced the stale t-013 pick in the first place) calls build_queue_summary() -> find_ready_task(), not next_ready_task.py -- a fix scoped only to the connector-only picker would have left the real collision path unpatched. Lesson: when a kaizen task names "the sweep step" as the target, check which of the repo's (sometimes more than one) selection implementations that step actually calls before assuming a single shared module covers it.

- 2026-08-23 `model-builder/t-029` — Cycle 56's note flagged that its repo-wide model-builder-reference grep, diffed against every file this task's history had named as read, was itself worth re-running -- but a directory glob (components/model-builder/**) had been silently treated as "covered" without any individual cycle ever naming every file inside it. model-builder-manager.vue (the top-level page component) had never actually been read in 56 cycles despite matching that glob. Reading it found it clean, but tracing the run-lifecycle functions it orchestrates (startRun/openRun/resumeRun) surfaced a real bug: three more places swap the active run for a different one the same way resetRun()/resetAll() do, but never called their in-flight-singleton-clearing logic, reproducing the exact stale-busy-indicator bug those two were already fixed for. Lesson for future cycles: a directory-glob "already covered" check is not the same as per-file coverage -- cross-check individual filenames against the cumulative note history, not just the glob pattern. Also, when a file traced this way reads clean, the bug may be in a function it *calls into* rather than the file itself; tracing outward from a clean file is a distinct, useful search strategy from re-reading a file's own body. Also confirmed: extracting a shared helper to reduce duplication across the four fix sites broke two pre-existing narrow-textual-checker guards that were pinned to the literal inline shape -- inlining the fix at each site (matching the existing pattern) instead of refactoring was the lower-risk choice once existing guards are keyed to literal text shape, not just behavior.

- 2026-08-22 `model-builder/t-029` — A session determined its own role as `worker` via select_role.py but then ran claim_task.py with `--owner reviewer` out of habit -- Reviewer is hard-barred from claiming tasks at all, so this was a real (if quickly self-caught) process violation, not just cosmetic metadata. Fixed via a tiny follow-up PR (#2688) correcting only the owner field before any implementation work proceeded. Lesson for future cycles: double-check `--owner` matches the session's live select_role.py recommendation before calling claim_task.py, not after the push already landed on origin/main.

- 2026-08-22 `appmaker/t-012` — apps.get.ts's pending-scaffold reader only ever recognized one of AppMaker's two self-serve scaffold flows' Todo titles (the monorepo flow's "Scaffold new app '...'", never the external-repo GitHub-integration flow's "Scaffold external app '...' via AppMaker GitHub integration") -- both the Prisma query's title filter and the extraction regex needed updating together, since fixing only one still silently drops the other flow's real, open Todos from the UI. Same "an endpoint reachable via direct API call, even with no front-end wired up yet, is still worth defending" precedent the prior cycle set for this exact pair of routes' slug-collision guard -- when two routes share a naming convention a downstream reader depends on, audit every reader against every writer, not just the one the current UI happens to call.

- 2026-08-22 `model-builder/t-029` — Cycle 46: closed the exact gap cycle 45's own kaizen note flagged as left open -- pitch/fieldsDraft/promptDraft were capped at MAX_DRAFT_TEXT_LENGTH on the item PATCH path but not on the run CREATE route's own items mapping, even though both write the same @db.Text columns. A cap added at one write path for a shared field is only half the fix until every other write path into that same column is audited too -- the same "one-way-clear-gap" shape as cycle 41/42's lastAutoBuildOutcome/statusMessage bugs, just for a validation cap instead of a state-clearing call. Importing the shared constant (MAX_DRAFT_TEXT_LENGTH) rather than hardcoding a second copy of the same number, plus a guard script asserting the import is actually used, is what keeps two independent write paths for the same column from drifting apart again silently.

- 2026-08-22 `model-builder/t-029` — Cycle 42: the same one-way-clear-gap defect shape from cycle 41 (lastAutoBuildOutcome) recurred in a completely different ephemeral field -- state.statusMessage/statusTone, the global status banner -- because eight mutating functions (approveStage, rejectStage, reopenStage, updatePitch, updateFields, updatePrompt, batchSetField, batchApproveStage) never called the store's own clearStatus() at the start of a fresh attempt, even though seven siblings already did. A single well-known bug class is worth checking function-by- function across an entire store rather than assuming one comprehensive fix closes the category -- the fix pattern (call an existing clear helper at the start of every mutating path, not just the ones that happened to need it last time) generalizes directly. Also reconfirmed (4th independent instance) that a delegated background agent's "waiting on a CI timer" self-report is not a real block -- the coordinating session must poll CI itself and merge, then explicitly tell the sub-agent to stop via SendMessage. Promoted this from a per-cycle TALKBACK observation to AGENTS.md hard safety rule 13.

- 2026-08-22 `model-builder/t-029` — Cycle 41: an ephemeral, client-only status field (BuildItem.lastAutoBuildOutcome) that a badge reads but no repair path ever clears is the same defect shape as cycle 30's stray in-progress marker -- any UI flag set as a side effect of one code path needs an explicit audit of every OTHER path that can legitimately supersede it (manual edit, AI redraft, single-item commit), not just the path that originally set it. Also: verifying a fix by running the full sibling test suite is worth doing even when it feels like overkill -- it surfaced a second, unrelated, pre-existing latent bug (a guard script's own comment-blind brace scanner) that this cycle's unrelated edits happened to expose as a false failure; treating a sibling guard's confusing break as evidence of a bug in that guard's own tooling, not as evidence the new change was wrong, was the right call.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-23T20:09:39Z_
