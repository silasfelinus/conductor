# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-29T10:05:15Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **424**
- Outcomes: blocked: 13, cancelled: 1, done: 410
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
| coloring-book | 21 | 100% |
| conductor | 59 | 100% |
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

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 409 | 99% |

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

- 2026-07-29 `conductor/t-095` — consume_art_requests.py's enqueue()->wait_for_job() gap: a submitted ArtJob's id was only ever printed to stdout, never persisted, before the (up to 600s) wait for completion -- so a timeout, FAILED/CANCELLED job, or killed process left no durable trace of which ArtJob had actually been submitted for a given request, exactly the shape of the ai-art-academy/t-010 fauvism incident (an id known only from a session's own prose, unrecoverable once out of context). Fixed by recording the id onto the request's own entry immediately after submission succeeds, before the blocking wait -- the general lesson: any script that submits an async job and then blocks waiting on it should persist the job id at submission time, not at completion time, so a timeout or crash mid-wait still leaves a recoverable trail. Separately confirmed via a new regression test that the non-zero-exit half of this kaizen was already correct; not every suspected two-part gap turns out to have two real parts.
- 2026-07-29 `media-watchlist/t-006` — This recurring polish task's own note pointed at a stale kaizen (Month/Season filters) that t-012 and t-016 had already closed two cycles earlier -- re-implementing it blind would have been a pure no-op. Re-diffing BROWSE-UX.md against the live components before picking a slice caught the drift and surfaced a different, still-open gap (Entry Detail's "Related entries" section, §3) that the note never flagged. Kaizen: on a recurring task with a multi-cycle PROGRESS history, treat the latest PROGRESS note's "not done yet" list as a hypothesis to verify against current main, not a ready-made todo -- prior cycles closing kaizens out-of-band (via their own follow-on tasks) can leave the recurring task's own note pointing at already-finished work.

- 2026-07-29 `model-builder/t-029` — After ~20 cycles finding only client-side store races (singleton-ownership guards, watch-clobber bugs, cancelled-run checks), this cycle found a genuinely different bug class: the server-side commit route (server/api/model-builder/items/[id]/commit.post.ts) never checked item.stageStatuses before executing the durable write, so the entire PITCH->FIELDS_AND_PROMPTS->GENERATE_ASSETS->COMMIT human-approval gate was enforced only client-side and could be bypassed by a direct POST. Kaizen: when a recurring bug-hunt task has exhausted one layer of a feature (here, the Pinia store's in-memory races), the next productive lens is the layer below it (the server route trusting client-enforced invariants) rather than re-scanning the same layer for a smaller variant of the same bug shape.

- 2026-07-29 `appmaker/t-012` — This "polish and upgrade front-end" task type had been repeatedly re-picked across cycles with steps (1) art and (3) admin-Placements backfill blocked, and step (4) already marked "fully covered" by an earlier cycle -- risking each new pickup being a pure no-op. Dispatching a fresh Explore pass specifically hunting for bugs (not re-checking the same three blocked steps) found two real, previously-unfixed issues: a missing request-sequencing guard in appmaker-page.vue's refresh() (concurrent onMounted/button/post-create calls could let a stale response overwrite fresh state) and a conductorStore.fetchProjects(force=true) call that silently no-op'd whenever any other fetch was already in flight, defeating every one of its five call sites that pass force:true expecting a real refresh. Kaizen: for any "polish" task whose obvious steps are all blocked/done, a targeted bug-hunt Explore pass over the actual shipped code is a reliable way to find genuine, safe, reversible work instead of re-confirming the same blocker note again.

- 2026-07-29 `model-builder/t-029` — Manual read-through of an async completion handler found a real, previously-unfixed race: pollAsyncArtJob cleared item.artJobId (the item panel's only "still working" signal, via isQueued) before its own finalizeQueuedArtImage network round-trip. On a regenerate, this let canApproveAssets briefly evaluate true using the item's stale prior artImageId, so a premature "Keep this asset" click could lock the stage to 'approved' moments before the finishing render silently overwrote artImageId/imagePath underneath it -- a fourth instance of this file's recurring "review gate silently bypassed" bug class (after canApproveAssets' original isGenerating/isQueued gap, the batch-editor stage-approval gate, and the cancelled-run guard). Fixed with a narrow status==='approved' check before the image write, plus a new textual regression checker (verifyModelBuilderApprovedAssetGuard.ts) mirroring the existing cancelled-run-guard/completion-gate checkers. Kaizen: this bug class keeps recurring in modelBuilderStore.ts's async completion paths -- a future cycle should consider whether verifyModelBuilderCompletionGate.ts's static ungated-write scan can be generalized from item.stages.KEY writes to cover item.artImageId/item.imagePath too, so the next instance is caught automatically instead of needing another manual read-through to find.

- 2026-07-29 `model-builder/t-029` — select_role.py's own api.github.com 403 (same known sandbox limitation as the t-092 entry above) made it report role=worker with zero open PRs visible, while GitHub-MCP-direct listing found one real open PR (#1377) waiting for review -- confirms AGENTS.md's existing guidance to cross-check GitHub MCP tools whenever select_role.py's github_api_unreachable flag is set, rather than trusting its worker/idle fallback at face value. Separately: the PR had gone stale (mergeable_state: dirty) against two STATUS.md/ROADMAP-AUDIT.* auto-gen commits that landed on main after it opened -- resolved per the existing hard-rule-9 convention (merge main in, take main's copy for the auto-generated files, keep the PR branch's real diff) rather than waiting for a human to notice the conflict.

- 2026-07-28 `conductor/t-092` — Direct api.github.com calls 403 from this sandbox even with a valid GITHUB_TOKEN and Authorization header (confirmed independently while building this task, matching select_role.py's existing finding) -- any new tool that needs live GitHub state from this environment should either go through the GitHub MCP tools or be written transport-agnostic (pure decision logic separated from the network call) rather than assuming urllib/requests against api.github.com will work.

- 2026-07-28 `model-builder/t-036` — Running a newly-written static checker against the real file BEFORE writing any fix (rather than writing the checker to match a known-clean state) is worth doing by default -- it immediately found a genuine, previously-unfixed instance of the exact bug class it was built to catch (an unconditional COMMIT-stage write in commitItem(), same shape as the GENERATE_ASSETS bug t-029 fixed ad hoc), which a code-review-only pass over commitItem() had not caught in three prior cycles of this file. Also reconfirmed: mirror the reference checker exactly on the main()-guard idiom (`if (process.argv[1] && import.meta.url === ...) main()`) whenever the new checker will be imported from its own self-test file -- an unconditional module-level main() call (fine for a checker with no test importer, like verifyModelBuilderLinkCoverage.ts) fires as a side effect on import and pollutes/masks the self-test's own output.
- 2026-07-28 `media-watchlist/t-016` — Confirms the t-015 lesson: select_role.py reported candidate_reviewable_pr_count: 0 and github_api_unreachable: true, but mcp__github__list_pull_requests/pull_request_read found this claude/* PR (and its kind_robots counterpart) fully green and ready to merge. A prior session did the implementation and left status: review with a clear PROGRESS note; this session only needed to verify CI and merge both PRs in order (implementation repo first, then the conductor tracking PR), matching the "Notes for reviewer" instructions left in the PR body.
- 2026-07-28 `media-watchlist/t-015` — select_role.py's direct api.github.com calls keep 403ing in this sandbox (recurred 3+ times same day); always cross-check with mcp__github__list_pull_requests directly before trusting a "0 reviewable PRs" result. Also confirmed: GET /api/media-entries already supported an unfiltered take/sort call for free (every filter param is optional and simply omitted when unset) -- worth checking existing route flexibility before assuming a backend change is needed for a "fixed global view" spec.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-29T10:05:15Z_
