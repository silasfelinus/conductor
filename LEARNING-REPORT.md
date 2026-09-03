# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-03T20:35:51Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **870**
- Outcomes: blocked: 16, cancelled: 1, done: 853
- Success rate: **98%**
- Average passes on successful tasks: **0.1**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 72 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 14 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 9 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 93 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 41 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 22 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 97 | 100% |
| kapowarr | 49 | 100% |
| kind-economy | 6 | 100% |
| kind-robots | 54 | 98% |
| kindrobots-unraid | 5 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 11 | 100% |
| media-watchlist | 11 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 83 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 20 | 100% |
| ruler-hooked | 11 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 16 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 854 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 16 |
| transient | 13 |
| actionable | 12 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 16 occurrences; look for the shared cause across its records
- failure category `transient` — 13 occurrences; look for the shared cause across its records
- failure category `actionable` — 12 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-03 `rainbow-butterflies/t-027` — State-reconciliation drift: PR kind_robots#2344 merged 2026-09-03T00:05Z but the roadmap task was left at status=review rather than done. Same pattern as media-watchlist/t-006 this cycle -- reconciled via GitHub MCP after the raw API probe 403'd.
- 2026-09-03 `media-watchlist/t-006` — State-reconciliation drift: PR kind_robots#2275 merged 2026-08-31 but the roadmap task sat at status=claimed for ~3 days with no queued task-event to auto-correct it. check_pr_merged_drift.py's raw urllib GitHub API probe 403'd in this sandbox (documented, connector-only limitation) and reported it unverifiable rather than confirming the merge -- reconciled via GitHub MCP pull_request_read directly. A session running the drift check should not stop at 'could not verify' when a working MCP transport is available in the same session; cross-check before treating the finding as inconclusive.
- 2026-09-02 `model-builder/t-029` — This task's own icon-coverage guard (cycle 82/84) only ever scanned the three shared data-structure arrays in modelBuilderRecipes.ts, leaving every per-component kind-icon: literal (view-mode toggles, inline button icons) completely unchecked -- a real, live, user-facing blank-icon bug (model-builder-source-picker.vue's List button, kind-icon:document, assets/icons/document.svg never existed) sat unnoticed through 84 prior cycles of otherwise-thorough code reading because none of them grepped literal icon-name strings against the actual assets/icons/ directory. When a project defines a 'coverage guard' for a hand-typed-name class of bug, scope it to every place that name shape can appear (grep the whole component family, not just the canonical data source), not just the one file where the bug was first found -- a guard that only covers its own origin story leaves the same failure mode live everywhere else. Also: a guard's own explanatory code comment can trip its own widened regex if it quotes the broken value literally (kind-icon:document appearing in prose) -- run a newly widened guard against your own diff before pushing, not just against the target file, to catch this class of self-inflicted false positive before CI does.
- 2026-09-02 `model-builder/t-029` — A non-nested-brace entry-split regex is fragile against free-text comments that themselves contain a literal open/close brace pair (a code path like server/api/(dreams,scenarios)/... quoted in a comment, using curly braces in the real source) -- it can silently swallow the real entry that follows, while the guard still prints a plausible-looking pass/total. verifyModelBuilderIconCoverageGuard.ts (cycle 82) shipped with exactly this gap for a full cycle before cycle 84 caught it while building an unrelated sibling guard. verifyModelBuilderSourceFieldGuard.ts already used a safer key-boundary split (index-based chunking between consecutive `key: '...'` matches, never touching brace characters at all) -- worth defaulting new SOURCE_TYPES/BUILD_STAGES/RECIPES-array guards to that pattern from the start rather than brace matching, and worth a future cycle double-checking any other guard in this family that still uses brace matching.
- 2026-09-02 `dream-cycle/t-025` — Added a per-bundle consecutive-failure counter (persisted state file already covered by the existing workflow's git-add step, so no CI/workflow change needed) to stop repair_dream_prose_catalog.py from retrying a chronically-failing bundle forever. Kept the existing per-bundle atomicity (failed bundles stay untouched, retried next run) as the default, only adding a circuit breaker on top after N consecutive failures -- and explicitly exempted an editor's own extra_fields retry from the breaker, since a human-directed re-ask is a different thing from an unattended scheduled retry. Worth remembering for any other 'runs on a schedule forever' loop in this pipeline: distinguish transient-retry-in-place from persistent-content-issue before assuming every failure is worth retrying indefinitely.
- 2026-09-02 `dream-cycle/t-024` — Wired repair_dream_prose_catalog.py --verify-live --strict into daily-digest.yml's existing recurring cycle (same continue-on-error + folded-into-final-gate pattern as the build/Facet/ArtJob/commit steps) rather than depending on an agent remembering to run it during a t-006 maintenance pass. A scheduled workflow step that already runs daily is a more reliable detection point for silent drift than an agent-recalled manual check -- prefer wiring a new verification into an existing recurring CI/workflow run over adding it to an agent's task checklist when both are available.
- 2026-09-02 `kapowarr/t-070` — Found an open, fully green, well-tested Kapowarr PR (branch claude/missing-comics-j8osws, not claimed through conductor's task loop) during a routine open-PR check. Reviewed the diff directly before merging (release_feed.py's stateless feed-poll design, the settings/interval wiring, and the Newznab/Torznab query-omission change) rather than merging on green CI alone, then retroactively filed the roadmap task so the shipped feature is visible to future audits. Not every merge-worthy PR in a watched repo arrives through claim_task.py -- worth checking open PRs directly across all in-scope repos, not just ones with a matching worker/* branch.
- 2026-09-02 `rainbow-butterflies/t-051` — next_ready_task.py surfaced this as a reclaimable stale claim (claimed_at 09:04:00Z, past the 90-minute TTL). Before implementing, checked kind_robots for existing work under the original claiming session's name and found kind_robots#2329 already merged 46 minutes after the claim -- the full two-tool MCP bridge (rainbow_agent_identity, rainbow_check_in) the task specified. The implementation was real and complete; only the roadmap claimed -> done transition was missing. Checking for already-merged work under a stale claim's session id before starting a fresh implementation avoided duplicating an already-shipped feature.
- 2026-09-02 `interface-vision/t-104` — State reconciliation found the task's own note already said 're-arming to ready for the next slice' after slice 36 (kind_robots#2331) merged, but the status field was left at review -- fixed by re-arming to ready directly rather than re-deriving from scratch. Then worked slice 37: the kr-panel-section codemod's dry-run flagged 4 files, but only one (academy-style-detail.vue's Gallery wall section, exact p-4 sm:p-5 override match to slice 36's precedent) was byte-equivalent. The other three all lacked their own padding class (padding lived entirely in child elements), so migrating them would add kr-panel-section's baked-in p-5 on top of existing child padding with nothing to oppose it -- a real geometry change the codemod's BASE_TOKENS-subset check can't detect on its own. Worth teaching the codemod itself to skip a candidate whose own class list carries no padding token at all, rather than relying on a human/reviewer catching it by reading the file.
- 2026-09-02 `conductor/t-141` — Reviewed and merged conductor#3477 (soft PR-time warning comparing changed roadmap task ids against the PR base, flagging simultaneous title+milestone rewrites -- the t-091 id-reuse shape). CI was fully green before merge; no changes requested.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-03T20:35:51Z_
