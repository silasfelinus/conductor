# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-14T21:17:21Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **43**
- Outcomes: done: 43
- Success rate: **100%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 1 | 100% |
| alexa-integration | 1 | 100% |
| animation-manager | 4 | 100% |
| animation-studio | 1 | 100% |
| challenge-center | 8 | 100% |
| coloring-book | 1 | 100% |
| conductor | 9 | 100% |
| ecosystem-map | 2 | 100% |
| kind-robots | 2 | 100% |
| model-builder | 13 | 100% |
| newsfeed | 1 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 3 | 100% |
| software | 40 | 100% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 2 |
| quality | 2 |

## Kaizen targets

_No systematic weaknesses above thresholds. Kaizen freely._

## Recent lessons

- 2026-07-14 `challenge-center/t-015` — A red CI TypeScript check on a PR that touches unrelated files should be reproduced in the exact CI environment (matching Node major version via a fresh local install + npm ci), not just re-run under whatever Node happens to be in the sandbox -- confirming byte-identical file:line errors against a known pre-existing tracked issue (kind-robots/t-020) is what actually justifies merging past a red check, not an assumption that it 'must be the same one as last time.'
- 2026-07-14 `coloring-book/t-019` — The task's own framing ('evolve the placeholder scaffold page') was stale -- a repo read of kind_robots showed the coloring engine (store/canvas/manager) is already a functionally complete region+raster-flood-fill implementation with undo and export, not a placeholder. Read the target repo before trusting a roadmap task's characterization of current state; the actual thin spots (generic Generate/Proposals/Prompts sub-tabs, single hardcoded page set) were narrower than the task description implied and got split into a new focused task (t-020) instead of driving an oversized diff. Also: art-asset generation for dashboard-tab/tutorial thumbnails is a queue-and-wait step (projects/art-prompts.yaml requests:), not something a single session executes end-to-end without KR_API_TOKEN -- queuing the request IS the correct terminal action for that sub-step, not a soft-gate blocker.
- 2026-07-14 `ai-art-academy/t-012` — A 'confirm the resolver has no type-specific branching' task closed clean on first pass by reading satisfied() directly (scripts/resolve_deps.py) -- it only checks status/gate_human/approved_by_human, never task kind, so a licensing DECISION and a brief-confirmation gate were already handled identically. Backed the finding with tests/test_resolve_deps.py (12 tests, zero prior coverage) instead of a note-only close, so the guarantee is now regression-tested rather than asserted. Also picked up mid-cycle after a real rotation collision on challenge-center/t-013 -- claim_task.py's live origin/main check caught it before any duplicate work was pushed.
- 2026-07-14 `conductor/t-042` — A batch event processor that aborts entirely on the first unresolvable item turns any single stale/invalid event into a silent, indefinite blocker for every other queued item; process independently and only fail the run for visibility after the resolvable items have already been committed.
- 2026-07-14 `challenge-center/t-013` — Matrix runners should resolve backend identity from the authoritative contender roster and isolate missing credentials to one entry so a heterogeneous matchup can still make progress.

- 2026-07-14 `challenge-center/t-007` — Derive challenge win metrics from grouped scored submissions so multiple variants do not inflate attempts and tied leaders remain explicit.
- 2026-07-14 `conductor/t-041` — Documented the HTTP 413 first-push-of-a-session workaround (create the remote branch via GitHub MCP create_branch before the first git push, when the branch has no prior PR) in CLAUDE.md's Session end section, so future sessions hitting a brand-new-ref push failure don't have to re-diagnose it from a raw GIT_TRACE_CURL trace.
- 2026-07-14 `conductor/t-023` — The bug this fixed (commit_done_status() pushing straight to origin/main with no fallback) is the same shape as the git-proxy 413 fix documented in t-041 and the claim-commit git-plumbing design built for t-040 -- recent cycles keep hitting variations of 'a permission-restricted session's git push can fail in a way plain code doesn't expect.' Fixed by capturing the session's own branch before checking out main, and on a rejected main push, cherry-picking the done-status commit onto that branch and pushing there instead so the status flip still reaches main via a normal PR rather than vanishing into a merged-but-not-marked-done gap. Verified with unit tests that simulate the push rejection (not just the happy path) since that's the one path that can't be exercised by running the script normally in a session that already has push access.
- 2026-07-14 `conductor/t-038` — audit_roadmaps.py's CONTROL_PRIORITY_DRIFT finding pointed at two files that could disagree for two different reasons (real reprioritization vs. stale prose) -- git history on both files (not just diffing their current content) was what distinguished them: priority.yaml had carried the same order since file creation, so CONTROL.md's band text was the one that drifted, not an intentional Silas decision. Worth checking history before assuming a two-source-of-truth mismatch needs Silas's judgment call -- sometimes one side is just unmaintained prose.
- 2026-07-14 `conductor/t-040` — Building the fix directly surfaced a second, unrelated latent bug in the tool it depends on: set_task_field.py's normalize_scalar left a literal ISO-timestamp value unquoted, so PyYAML silently reparsed it as a native datetime instead of a string (only the `now` keyword path was quoted). Caught by a test asserting the round-tripped type, not by reading the code -- worth remembering that a field 'looks like a string' in a diff is not the same as verifying its parsed type. Also: designed the claim commit to be built via git plumbing (scratch index + commit-tree) rather than a real checkout/commit specifically so it never disturbs whatever branch or uncommitted work the calling session already has -- validated with a real throwaway git repo (bare + clone), not just unit-level YAML assertions, since the git push/race path is exactly the part most likely to look correct and behave wrong under concurrency.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-14T21:17:21Z_
