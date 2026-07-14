# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-14T14:33:36Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **33**
- Outcomes: done: 33
- Success rate: **100%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| alexa-integration | 1 | 100% |
| animation-manager | 4 | 100% |
| animation-studio | 1 | 100% |
| challenge-center | 5 | 100% |
| conductor | 4 | 100% |
| ecosystem-map | 2 | 100% |
| kind-robots | 2 | 100% |
| model-builder | 13 | 100% |
| newsfeed | 1 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 3 | 100% |
| software | 30 | 100% |

## Failure categories

| Category | Count |
|---|---|
| quality | 2 |
| actionable | 1 |

## Kaizen targets

_No systematic weaknesses above thresholds. Kaizen freely._

## Recent lessons

- 2026-07-14 `ecosystem-map/t-003` — Built the asset coverage matrix entirely from filesystem-verifiable sources (projects/images/, kind_robots' public/images/artcollections/, projects/art-prompts.yaml's structured `images:` list) rather than guessing at DB-only fields (project Dreams, liveUrl) -- explicitly flagged those as needing live-DB verification, mirroring FRONTEND-SURFACE-MAP.md's existing precedent for the same limitation. Cross-referenced FRONTEND-SURFACE-MAP.md's Class column for the mock-screenshot-needed judgment instead of re-deriving it, and marked the 11 projects that audit never covered as unclassified rather than guessing. Found 6 active projects (animation-manager, kindrobots-unraid, model-builder, mural-design, newsfeed, davinci-hero) with zero identity images and nothing queued to produce them.
- 2026-07-14 `ecosystem-map/t-001` — Roadmap/reality drift, not missing work: DESIGN-BRIEF.md was already a complete, substantial document (canonical ownership table, bot parity, visual asset parity, image approval gate, duplication risks, first deliverables) but the task was still status: ready. Worth a general habit -- before starting a 'write X.md' task, check whether X.md already exists and is actually done; roadmap status can lag a completed artifact same as it can lag a merged PR.
- 2026-07-14 `animation-manager/t-008` — Writing 'the animation verification script' SPEC.md already named required checking cross-file consistency, not just the catalog file itself: narratorHelper.ts's narratorAnimationAliases map and animationPreferenceStore.ts's DEFAULT_PREFERENCES both duplicate catalog ids as string literals with no compiler-enforced link back to animationCatalog.ts, so they're exactly the kind of thing that goes stale silently. Also had to model Nuxt's real filename-to-component-name resolution (splits on hyphen, underscore, AND dot — components/screenfx/fireworks.effect.vue resolves the same as a hyphenated file would) rather than assuming a literal id.vue match, which a naive exists-check would have gotten wrong. Found but did not fix an unrelated stale id (bubble-effect in displayStore.ts's legacy pre-centralization EffectId type, no matching catalog entry) — filed as t-010 rather than expanding this PR's diff.
- 2026-07-14 `model-builder/t-028` — The CI check the PR needed to pass (TypeScript Type Check) was already red on kind_robots main before this cycle touched anything — confirmed by pulling main's own latest workflow run for the same head sha rather than assuming the new PR's red check was caused by this change. Fixing the actual (unrelated, one-line) null-check bug in artjob-manager.vue on the same branch was faster and lower-risk than opening a second PR and waiting on a second review/merge cycle to unblock this one. Also: reused two existing conventions instead of inventing new ones (normalizeRarity/normalizeRewardType precedent in server/api/rewards/index.ts for choice-field validation style; the modelBuilderFields.ts single-source-of-field-truth module from t-024, extended rather than duplicated) — worth checking sibling API routes for an existing normalizer before writing a new one whenever a task touches enum-like fields.
- 2026-07-14 `animation-studio/t-003` — Stale bookkeeping: kind_robots PR #238 (Gravity Garden animation) merged 2026-07-14T07:40Z but the animation-studio roadmap task was left at status: review with no updated timestamp, only surfaced by scripts/audit_roadmaps.py's IN_PROGRESS_WITHOUT_TIMESTAMP warning. Verified merge state directly via pull_request_read before flipping to done rather than trusting the roadmap's stale status. animation-studio also appears to be the pre-animation-manager pilot project (animation-manager PR #494 duplicates its research/pitch-queue tasks) and is missing a project-overrides.yaml entry entirely — flagged as conductor/t-039 for a human/Worker decision on whether to formally retire it rather than guessing.
- 2026-07-14 `newsfeed/t-001` — Burst-mode rotation picked the least-recently-touched active project by checking every task's `updated` timestamp across all roadmaps rather than defaulting to whatever had the most recent PR activity — newsfeed had zero timestamps on any task despite being priority: high. A real codebase audit (dedicated Explore subagent, not guesses) found two integration points already reserved (dashboardHelper.ts's wonder.newsfeed tab, content/newsfeed.md) that a blind implementation could have collided with or duplicated.
- 2026-07-14 `kind-robots/t-019` — Two-sided cross-repo task (conductor PR #506 draining requests.yaml, kind_robots PR #245 the front-end request bridge) — the task note said 'set done when both PRs merge' and both merged independently (by Silas directly) within an hour of each other, ahead of the next Reviewer sweep even noticing. Closing agent should re-check both halves' merge state before flipping status rather than assuming the note's gate is still open; used set_task_field.py for the surgical status flip per t-008's standing lesson.
- 2026-07-14 `conductor/t-036` — This file's own block-sequence indentation had silently mixed two depths (2-space nested vs 0-indent flush) since an earlier merge, breaking yaml.safe_load for the whole ledger and swallowing every append_learning() call system-wide. Root cause was never diagnosed at the time it broke because process_task_events.py's YAML-parse failure wasn't surfaced loudly enough to trace back to this file. Fix was a pure whitespace reflow (dedent every record under the mixed-depth block by 2 spaces to match the majority 0-indent style) verified line-for-line against the diff so no record content changed, then confirmed both yaml.safe_load and scripts/build_learning_summary.py run clean. Next time a script that reads this file throws on task-close, check LEARNING.yaml's own parseability first before assuming the bug is in the caller.
- 2026-07-14 `challenge-center/t-008` — resolve_deps.py (like process_task_events.py, flagged separately as t-020) rewrites the entire roadmap file with yaml.safe_dump whenever it applies an unblock, turning a two-task status flip into a 940-line diff (escaped Unicode, flow-style indentation, changed quoting). Ran it once, saw the blast radius, reverted, and reapplied the same t-009/t-015 unblock with the surgical set_task_field.py instead — landed as a 26-line diff. Future cycles should default to set_task_field.py for post-done dependency unblocks and treat resolve_deps.py's write path as unsafe for a clean PR until t-020 fixes it too.
- 2026-07-14 `animation-manager/t-003` — Cross-repo software task (conductor roadmap + kind_robots implementation PR #237) closed cleanly with the conductor PR correctly citing the exact kind_robots commit/PR — verified independently and it matched byte-for-byte with the claim.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-14T14:33:36Z_
