# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-22T16:04:58Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1116**
- Outcomes: blocked: 18, cancelled: 2, done: 1096
- Success rate: **98%**
- Average passes on successful tasks: **0.3**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 15 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 11 | 100% |
| approval-portal | 2 | 0% |
| art-archive | 32 | 100% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| butterfly-gallery | 32 | 94% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 39 | 100% |
| conductor | 131 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 27 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 140 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 10 | 100% |
| kind-robots | 67 | 99% |
| kindrobots-unraid | 9 | 100% |
| lora-ingestion | 6 | 100% |
| mandarin-tutor | 14 | 93% |
| media-watchlist | 12 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 85 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 21 | 100% |
| ruler-hooked | 21 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 37 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1099 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 39 |
| transient | 17 |
| actionable | 17 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 39 occurrences; look for the shared cause across its records
- failure category `transient` — 17 occurrences; look for the shared cause across its records
- failure category `actionable` — 17 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-22 `storybook/t-010` — A file paused behind an upstream dependency (2026-09-12/13 TALKBACK note: don't polish storybook-visual-setup.vue until t-034/t-035/t-036's card-driven redesign lands) can sit unrevisited for over a week after the pause condition is actually met -- t-034/t-035/t-036 finished 2026-09-13, but nobody re-checked this file until this cycle (2026-09-22). The fix itself (role="group" + aria-label on two ungrouped choice-button grids) matched a pattern already fixed five times elsewhere in the project, confirmed to fail pre-fix via a git-stash round trip on the component. Worth generalizing: a pause note tied to a dependency's completion needs the same kind of staleness check this repo already runs for claimed tasks and stale recurring tasks, or "paused pending X" quietly becomes "paused forever" once X actually lands.
- 2026-09-22 `lora-ingestion/t-012` — When a broad UI utility patch trips the lint ratchet, repair the newly introduced lint findings on the same branch and require exact-head Actions completion before treating the retry as done.
- 2026-09-22 `lora-ingestion/t-011` — Two sessions independently implemented the same kaizen-filed fix (PowerShell paths-filter quote-only regex) within a ~30 minute window -- kind_robots#2969 (this task's own OpenAI Worker cycle, single/double-quote fix) and kind_robots#2970 (a different session, broader single/double/bare-scalar fix with a backreference guard), #2970 merging first. Discovered via #2969's PR showing mergeable_state=dirty on review; closed #2969 as redundant with a comment naming the superseding PR rather than resolving a conflict Reviewer has no push access to fix on a worker/* branch. No lost work -- the standard git-conflict backstop caught the collision as designed, just surfaced through PR mergeability instead of a rejected push.
- 2026-09-22 `lora-ingestion/t-010` — A same-day Claude session (session_01HHrZmwjtwx3T7A7H94irfo) opened kind_robots#2967 (LoRA purpose typing + randomized art batches, Silas-directed, additive migration) and correctly stood down on the one red CI check rather than force-merging or silently ignoring it -- but a session that authors and reviews its own work has no second party to actually merge it once it stands down. A later scheduled Conductor sweep found the open, ready-to-merge PR, independently re-verified the "pre-existing, unrelated" claim (reproduced the regex/quoting bug directly against origin/main) and the migration's additive-only shape, then merged. Worth normalizing: an agent authoring a PR should still expect a distinct review/merge pass to pick it up promptly rather than assuming the standing-down comment alone gets it to main.
- 2026-09-22 `conductor/t-190` — Implemented the zero-diff-close audit hint itself (roadmap_deps.zero_diff_close_hint, wired into run_worker.find_ready_task and next_ready_task.first_ready_task): an advisory audit_candidate/audit_candidate_reason field on the picked ready task, flagged when a done depends_on dependency's note mentions the ready task's own id. select_role.py inherits it for free via build_queue_summary(). Clean first-pass -- the pattern was already fully specified by the kaizen note itself (t-031/t-033), same "sibling task already proved the pattern" shape the note describes.
- 2026-09-22 `butterfly-gallery/t-035` — STEP-1-style async-dependency tasks (poll an ArtJob, act once DONE) go from not-yet-actionable to fully shippable in one pass once the upstream condition clears -- this task went claim -> verify DONE -> resolve artImageId -> splice -> full verify suite -> merged PR in a single session with zero back-and-forth, because the acceptance criteria and implementation pattern were already fully specified by the sibling task (t-033) it was explicitly modeled on. Confirms the t-190 kaizen (from t-031, same session): when a task's own note names the exact pattern a prior sibling task already proved, implementation is close to mechanical -- worth checking for that note-linkage before assuming a task needs open-ended design work.
- 2026-09-22 `butterfly-gallery/t-031` — A gating audit task can close with zero diff when the dependency it was waiting on (t-033) already implemented the exact requirement in its own PR -- t-033's runway splice used IntersectionObserver + document.hidden + prefers-reduced-motion with a v-if unmount (not a CSS class toggle) specifically because its own note named t-031's acceptance criteria up front. Worth checking whether an upstream task already absorbed a downstream audit task's requirement before assuming the audit still needs new code.
- 2026-09-22 `butterfly-gallery/t-033` — A ready roadmap task can get its real implementation merged by a concurrent, repo-scoped session (here kind_robots#2964) without that session ever touching the conductor roadmap task it belongs to. check_pr_merged_drift.py only audits claimed/review tasks, so a ready task whose implementation lands via a different repo's session sits stale until a later sweep's STEP-1-style recheck happens to notice the local kind_robots checkout has moved past what the roadmap note assumed. Worth checking the target repo's own recent commits/PRs, not just the live render queue, when a task's note describes external async work that might have completed.
- 2026-09-22 `animation-manager/t-018` — When an animation build ships, promote its canonical PITCHES.yaml entry and record build provenance in the same cycle; verify canonical state before adding a second repair for an already-fixed bookkeeping gap.
- 2026-09-22 `dream-cycle/t-032` — Before wiring a checker into a new call site from a task note's field list, trace the actual code path (build_dream_records.py's per-element art_prompt calls) rather than trusting the note verbatim -- three of the seven named fields (best_used_when, catch, local_rule) never reach an art_prompt at all and would have been false positives.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-22T16:04:58Z_
