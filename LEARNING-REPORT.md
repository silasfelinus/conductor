# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-29T04:06:24Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **418**
- Outcomes: blocked: 13, cancelled: 1, done: 404
- Success rate: **97%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 55 | 98% |
| alexa-integration | 2 | 100% |
| animation-manager | 12 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 5 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 21 | 100% |
| conductor | 56 | 100% |
| conductor-app | 2 | 100% |
| davinci | 1 | 100% |
| digital-storefront | 24 | 100% |
| dream-cycle | 16 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| kind-robots | 39 | 97% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 9 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 40 | 100% |
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

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 403 | 99% |

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

- 2026-07-29 `model-builder/t-029` — Manual read-through of an async completion handler found a real, previously-unfixed race: pollAsyncArtJob cleared item.artJobId (the item panel's only "still working" signal, via isQueued) before its own finalizeQueuedArtImage network round-trip. On a regenerate, this let canApproveAssets briefly evaluate true using the item's stale prior artImageId, so a premature "Keep this asset" click could lock the stage to 'approved' moments before the finishing render silently overwrote artImageId/imagePath underneath it -- a fourth instance of this file's recurring "review gate silently bypassed" bug class (after canApproveAssets' original isGenerating/isQueued gap, the batch-editor stage-approval gate, and the cancelled-run guard). Fixed with a narrow status==='approved' check before the image write, plus a new textual regression checker (verifyModelBuilderApprovedAssetGuard.ts) mirroring the existing cancelled-run-guard/completion-gate checkers. Kaizen: this bug class keeps recurring in modelBuilderStore.ts's async completion paths -- a future cycle should consider whether verifyModelBuilderCompletionGate.ts's static ungated-write scan can be generalized from item.stages.KEY writes to cover item.artImageId/item.imagePath too, so the next instance is caught automatically instead of needing another manual read-through to find.

- 2026-07-29 `model-builder/t-029` — select_role.py's own api.github.com 403 (same known sandbox limitation as the t-092 entry above) made it report role=worker with zero open PRs visible, while GitHub-MCP-direct listing found one real open PR (#1377) waiting for review -- confirms AGENTS.md's existing guidance to cross-check GitHub MCP tools whenever select_role.py's github_api_unreachable flag is set, rather than trusting its worker/idle fallback at face value. Separately: the PR had gone stale (mergeable_state: dirty) against two STATUS.md/ROADMAP-AUDIT.* auto-gen commits that landed on main after it opened -- resolved per the existing hard-rule-9 convention (merge main in, take main's copy for the auto-generated files, keep the PR branch's real diff) rather than waiting for a human to notice the conflict.

- 2026-07-28 `conductor/t-092` — Direct api.github.com calls 403 from this sandbox even with a valid GITHUB_TOKEN and Authorization header (confirmed independently while building this task, matching select_role.py's existing finding) -- any new tool that needs live GitHub state from this environment should either go through the GitHub MCP tools or be written transport-agnostic (pure decision logic separated from the network call) rather than assuming urllib/requests against api.github.com will work.

- 2026-07-28 `model-builder/t-036` — Running a newly-written static checker against the real file BEFORE writing any fix (rather than writing the checker to match a known-clean state) is worth doing by default -- it immediately found a genuine, previously-unfixed instance of the exact bug class it was built to catch (an unconditional COMMIT-stage write in commitItem(), same shape as the GENERATE_ASSETS bug t-029 fixed ad hoc), which a code-review-only pass over commitItem() had not caught in three prior cycles of this file. Also reconfirmed: mirror the reference checker exactly on the main()-guard idiom (`if (process.argv[1] && import.meta.url === ...) main()`) whenever the new checker will be imported from its own self-test file -- an unconditional module-level main() call (fine for a checker with no test importer, like verifyModelBuilderLinkCoverage.ts) fires as a side effect on import and pollutes/masks the self-test's own output.
- 2026-07-28 `media-watchlist/t-016` — Confirms the t-015 lesson: select_role.py reported candidate_reviewable_pr_count: 0 and github_api_unreachable: true, but mcp__github__list_pull_requests/pull_request_read found this claude/* PR (and its kind_robots counterpart) fully green and ready to merge. A prior session did the implementation and left status: review with a clear PROGRESS note; this session only needed to verify CI and merge both PRs in order (implementation repo first, then the conductor tracking PR), matching the "Notes for reviewer" instructions left in the PR body.
- 2026-07-28 `media-watchlist/t-015` — select_role.py's direct api.github.com calls keep 403ing in this sandbox (recurred 3+ times same day); always cross-check with mcp__github__list_pull_requests directly before trusting a "0 reviewable PRs" result. Also confirmed: GET /api/media-entries already supported an unfiltered take/sort call for free (every filter param is optional and simply omitted when unset) -- worth checking existing route flexibility before assuming a backend change is needed for a "fixed global view" spec.
- 2026-07-28 `model-builder/t-029` — Before dispatching a fresh explore-and-fix pass, actually run any regression guard a prior cycle's kaizen suggestion produced (e.g. verifyModelBuilderLinkCoverage.ts) rather than trusting the roadmap note's "unconfirmed" framing -- it may already be closed by an intervening task chain. Also: singleton-ownership-race fixes (guarding concurrent in-flight state) and stage-approval-gate fixes (guarding against overwriting already-reviewed/settled state) are distinct bug classes in this store -- batchDraftField/ batchSetField needed the latter, not another instance of the former.
- 2026-07-28 `coloring-book/t-036` — Distinguishing a credential-wall semantic_gate_error (ANTHROPIC_API_KEY is required) from a recoverable job-timeout or transient-enqueue one by message content -- rather than lumping all semantic_gate_error entries into one retry_safe check -- lets automation short-circuit "don't bother retrying, it's the same infra gate" instead of a human/agent re-deriving it from raw queue state each cycle.

- 2026-07-28 `model-builder/t-035` — Extending an existing schema-relation-vs-config-eligibility guard for a second failure direction (join-table-only relation claimed as CREATE-linkable) is clean on the first functional pass, but a naive "any model referencing both types" join-table heuristic false-positives on broad hub models (ArtImage) -- require the actual structural signature real join tables use in this schema (@@id([...]) composite key) before accepting a match. Separately: a green vue-tsc run does not guarantee a green CI, since this repo also runs a heuristic (non-type-checking) capture-group-guard linter that only recognizes specific guard shapes textually -- read that linter's own source for its recognized shapes rather than guessing when it flags new code TypeScript itself accepted.
- 2026-07-28 `coloring-book/t-035` — Clean first-pass fix, same shape as t-032's recovery-path fix but for the fresh-submission branch of the same loop: record_semantic_gate_error() now stamps the newly enqueued ArtJob's id onto the stored error whenever the message does not already carry a "job N" reference, so a missing-credential verification failure after a successful render stays recoverable instead of forcing a duplicate resubmission. Mirrors t-032's own regression test shape closely enough that reusing that test as a template for the new fresh-submission case caught the right edge cases (double-stamp avoidance, enqueue()-failure leaving the field unstamped) on the first attempt.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-29T04:06:24Z_
