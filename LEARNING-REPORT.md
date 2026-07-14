# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-14T12:58:59Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **29**
- Outcomes: done: 29
- Success rate: **100%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| alexa-integration | 1 | 100% |
| animation-manager | 3 | 100% |
| animation-studio | 1 | 100% |
| challenge-center | 5 | 100% |
| conductor | 4 | 100% |
| kind-robots | 2 | 100% |
| model-builder | 12 | 100% |
| newsfeed | 1 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 3 | 100% |
| software | 26 | 100% |

## Failure categories

| Category | Count |
|---|---|
| quality | 2 |
| actionable | 1 |

## Kaizen targets

_No systematic weaknesses above thresholds. Kaizen freely._

## Recent lessons

- 2026-07-14 `animation-studio/t-003` — Stale bookkeeping: kind_robots PR #238 (Gravity Garden animation) merged 2026-07-14T07:40Z but the animation-studio roadmap task was left at status: review with no updated timestamp, only surfaced by scripts/audit_roadmaps.py's IN_PROGRESS_WITHOUT_TIMESTAMP warning. Verified merge state directly via pull_request_read before flipping to done rather than trusting the roadmap's stale status. animation-studio also appears to be the pre-animation-manager pilot project (animation-manager PR #494 duplicates its research/pitch-queue tasks) and is missing a project-overrides.yaml entry entirely — flagged as conductor/t-039 for a human/Worker decision on whether to formally retire it rather than guessing.
- 2026-07-14 `newsfeed/t-001` — Burst-mode rotation picked the least-recently-touched active project by checking every task's `updated` timestamp across all roadmaps rather than defaulting to whatever had the most recent PR activity — newsfeed had zero timestamps on any task despite being priority: high. A real codebase audit (dedicated Explore subagent, not guesses) found two integration points already reserved (dashboardHelper.ts's wonder.newsfeed tab, content/newsfeed.md) that a blind implementation could have collided with or duplicated.
- 2026-07-14 `kind-robots/t-019` — Two-sided cross-repo task (conductor PR #506 draining requests.yaml, kind_robots PR #245 the front-end request bridge) — the task note said 'set done when both PRs merge' and both merged independently (by Silas directly) within an hour of each other, ahead of the next Reviewer sweep even noticing. Closing agent should re-check both halves' merge state before flipping status rather than assuming the note's gate is still open; used set_task_field.py for the surgical status flip per t-008's standing lesson.
- 2026-07-14 `conductor/t-036` — This file's own block-sequence indentation had silently mixed two depths (2-space nested vs 0-indent flush) since an earlier merge, breaking yaml.safe_load for the whole ledger and swallowing every append_learning() call system-wide. Root cause was never diagnosed at the time it broke because process_task_events.py's YAML-parse failure wasn't surfaced loudly enough to trace back to this file. Fix was a pure whitespace reflow (dedent every record under the mixed-depth block by 2 spaces to match the majority 0-indent style) verified line-for-line against the diff so no record content changed, then confirmed both yaml.safe_load and scripts/build_learning_summary.py run clean. Next time a script that reads this file throws on task-close, check LEARNING.yaml's own parseability first before assuming the bug is in the caller.
- 2026-07-14 `challenge-center/t-008` — resolve_deps.py (like process_task_events.py, flagged separately as t-020) rewrites the entire roadmap file with yaml.safe_dump whenever it applies an unblock, turning a two-task status flip into a 940-line diff (escaped Unicode, flow-style indentation, changed quoting). Ran it once, saw the blast radius, reverted, and reapplied the same t-009/t-015 unblock with the surgical set_task_field.py instead — landed as a 26-line diff. Future cycles should default to set_task_field.py for post-done dependency unblocks and treat resolve_deps.py's write path as unsafe for a clean PR until t-020 fixes it too.
- 2026-07-14 `animation-manager/t-003` — Cross-repo software task (conductor roadmap + kind_robots implementation PR #237) closed cleanly with the conductor PR correctly citing the exact kind_robots commit/PR — verified independently and it matched byte-for-byte with the claim.
- 2026-07-14 `animation-manager/t-002` — Front-loading twelve diverse pitches before the first build gave the recurring daily-pitch task (t-006) real runway immediately instead of starting from an empty queue.
- 2026-07-14 `animation-manager/t-001` — First milestone of a new autonomous project (research + quality contract docs) landed clean in one pass with concrete, falsifiable acceptance criteria rather than vague prose — good template for future autonomous-project kickoffs.
- 2026-07-14 `alexa-integration/t-006` — The Worker's earlier connector-block on silasfelinus/serendipity-voice was transient to that session, not a lasting boundary — a later Claude session with direct repo write access closed t-006 with no branch-creation issue at all. When a preserved cross-repo handoff doc is picked up later, treat it as a design reference rather than a literal patch to apply: the target repo's adapter architecture (art-submit.ts's gated-submission pattern) had evolved past the doc's shape since it was written, and re-deriving the implementation against current code avoided reintroducing a stale design.
- 2026-07-14 `conductor/kind_robots-ci-green` — 'Harden MariaDB connection pooling' (kind_robots 0ee601f8) dropped the pool's connectionLimit default from the mariadb driver's own 10 to 2 with no env var anywhere to override it, silently pool-starving production and cascading into ~14 failing Cypress spec files. When a config 'hardening' commit introduces a new numeric default, diff it against the library's own built-in default rather than picking an arbitrary small number — and grep the whole repo/deploy config for whether anything actually sets the new env var before assuming it's tunable in practice.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-14T12:58:59Z_
