# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-22T06:01:52Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1112**
- Outcomes: blocked: 18, cancelled: 2, done: 1092
- Success rate: **98%**
- Average passes on successful tasks: **0.2**

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
| lora-ingestion | 3 | 100% |
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
| storybook | 36 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1095 | 99% |

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

- 2026-09-22 `conductor/t-190` — Implemented the zero-diff-close audit hint itself (roadmap_deps.zero_diff_close_hint, wired into run_worker.find_ready_task and next_ready_task.first_ready_task): an advisory audit_candidate/audit_candidate_reason field on the picked ready task, flagged when a done depends_on dependency's note mentions the ready task's own id. select_role.py inherits it for free via build_queue_summary(). Clean first-pass -- the pattern was already fully specified by the kaizen note itself (t-031/t-033), same "sibling task already proved the pattern" shape the note describes.
- 2026-09-22 `butterfly-gallery/t-035` — STEP-1-style async-dependency tasks (poll an ArtJob, act once DONE) go from not-yet-actionable to fully shippable in one pass once the upstream condition clears -- this task went claim -> verify DONE -> resolve artImageId -> splice -> full verify suite -> merged PR in a single session with zero back-and-forth, because the acceptance criteria and implementation pattern were already fully specified by the sibling task (t-033) it was explicitly modeled on. Confirms the t-190 kaizen (from t-031, same session): when a task's own note names the exact pattern a prior sibling task already proved, implementation is close to mechanical -- worth checking for that note-linkage before assuming a task needs open-ended design work.
- 2026-09-22 `butterfly-gallery/t-031` — A gating audit task can close with zero diff when the dependency it was waiting on (t-033) already implemented the exact requirement in its own PR -- t-033's runway splice used IntersectionObserver + document.hidden + prefers-reduced-motion with a v-if unmount (not a CSS class toggle) specifically because its own note named t-031's acceptance criteria up front. Worth checking whether an upstream task already absorbed a downstream audit task's requirement before assuming the audit still needs new code.
- 2026-09-22 `butterfly-gallery/t-033` — A ready roadmap task can get its real implementation merged by a concurrent, repo-scoped session (here kind_robots#2964) without that session ever touching the conductor roadmap task it belongs to. check_pr_merged_drift.py only audits claimed/review tasks, so a ready task whose implementation lands via a different repo's session sits stale until a later sweep's STEP-1-style recheck happens to notice the local kind_robots checkout has moved past what the roadmap note assumed. Worth checking the target repo's own recent commits/PRs, not just the live render queue, when a task's note describes external async work that might have completed.
- 2026-09-22 `animation-manager/t-018` — When an animation build ships, promote its canonical PITCHES.yaml entry and record build provenance in the same cycle; verify canonical state before adding a second repair for an already-fixed bookkeeping gap.
- 2026-09-22 `dream-cycle/t-032` — Before wiring a checker into a new call site from a task note's field list, trace the actual code path (build_dream_records.py's per-element art_prompt calls) rather than trusting the note verbatim -- three of the seven named fields (best_used_when, catch, local_rule) never reach an art_prompt at all and would have been false positives.
- 2026-09-22 `dream-cycle/t-031` — Two independent test files asserting the same workflow-yaml policy can silently diverge if only one is edited later; route both through one shared assertion helper (tests/<module>.py, not test_-prefixed so pytest won't collect it) so the policy can only change in one place.
- 2026-09-21 `storybook/t-061` — Shared slug-to-card resolution removes duplicated deep-link lookup logic while keeping gate behavior in one load-bearing helper; update literal contract guards in the same scoped refactor when they intentionally pin the old implementation shape.
- 2026-09-21 `storybook/t-060` — t-059's implementation sketch (lift board into storybookRunStore, capture it in playAgain() before leaveRun() clears the run, seed StorybookTable from it via the same per-slot deck lookups seedFromQuery() uses) held up exactly as written -- the one real design decision it left open was WHERE the capture could actually happen. playAgain() runs on the Ending screen, long after the Table (and its local board ref) has unmounted, so the board has to be recorded earlier, at the moment openStory() actually succeeds, not read fresh at playAgain() time. A future task inheriting a sketch written before the surrounding component lifecycle was traced should re-verify each named call site is still mounted/alive at the point the sketch assumes, not just implement the call graph as literally stated.
- 2026-09-21 `storybook/t-059` — When a task's own note offers a scoped, safe path (correct a misleading comment/label) alongside a larger, design-dependent path (implement real persistence behavior), an unattended scheduled session should take the scoped path rather than invent unreviewed product behavior -- storybook/t-059's note explicitly sanctioned this ("if board retention isn't meant to ship yet, correct the comment instead"), which made the call low-risk. A future cycle should treat the task's own concrete implementation sketch (lift board into storybookRunStore, seed StorybookTable from it via the same seedFromQuery() lookup pattern) as the starting point if board retention becomes something Silas actually wants shipped.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-22T06:01:52Z_
