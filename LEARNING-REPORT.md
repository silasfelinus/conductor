# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-02T20:53:49Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **865**
- Outcomes: blocked: 16, cancelled: 1, done: 848
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
| dream-cycle | 21 | 100% |
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
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 81 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 19 | 100% |
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
| software | 849 | 99% |

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

- 2026-09-02 `dream-cycle/t-024` — Wired repair_dream_prose_catalog.py --verify-live --strict into daily-digest.yml's existing recurring cycle (same continue-on-error + folded-into-final-gate pattern as the build/Facet/ArtJob/commit steps) rather than depending on an agent remembering to run it during a t-006 maintenance pass. A scheduled workflow step that already runs daily is a more reliable detection point for silent drift than an agent-recalled manual check -- prefer wiring a new verification into an existing recurring CI/workflow run over adding it to an agent's task checklist when both are available.
- 2026-09-02 `kapowarr/t-070` — Found an open, fully green, well-tested Kapowarr PR (branch claude/missing-comics-j8osws, not claimed through conductor's task loop) during a routine open-PR check. Reviewed the diff directly before merging (release_feed.py's stateless feed-poll design, the settings/interval wiring, and the Newznab/Torznab query-omission change) rather than merging on green CI alone, then retroactively filed the roadmap task so the shipped feature is visible to future audits. Not every merge-worthy PR in a watched repo arrives through claim_task.py -- worth checking open PRs directly across all in-scope repos, not just ones with a matching worker/* branch.
- 2026-09-02 `rainbow-butterflies/t-051` — next_ready_task.py surfaced this as a reclaimable stale claim (claimed_at 09:04:00Z, past the 90-minute TTL). Before implementing, checked kind_robots for existing work under the original claiming session's name and found kind_robots#2329 already merged 46 minutes after the claim -- the full two-tool MCP bridge (rainbow_agent_identity, rainbow_check_in) the task specified. The implementation was real and complete; only the roadmap claimed -> done transition was missing. Checking for already-merged work under a stale claim's session id before starting a fresh implementation avoided duplicating an already-shipped feature.
- 2026-09-02 `interface-vision/t-104` — State reconciliation found the task's own note already said 're-arming to ready for the next slice' after slice 36 (kind_robots#2331) merged, but the status field was left at review -- fixed by re-arming to ready directly rather than re-deriving from scratch. Then worked slice 37: the kr-panel-section codemod's dry-run flagged 4 files, but only one (academy-style-detail.vue's Gallery wall section, exact p-4 sm:p-5 override match to slice 36's precedent) was byte-equivalent. The other three all lacked their own padding class (padding lived entirely in child elements), so migrating them would add kr-panel-section's baked-in p-5 on top of existing child padding with nothing to oppose it -- a real geometry change the codemod's BASE_TOKENS-subset check can't detect on its own. Worth teaching the codemod itself to skip a candidate whose own class list carries no padding token at all, rather than relying on a human/reviewer catching it by reading the file.
- 2026-09-02 `conductor/t-141` — Reviewed and merged conductor#3477 (soft PR-time warning comparing changed roadmap task ids against the PR base, flagging simultaneous title+milestone rewrites -- the t-091 id-reuse shape). CI was fully green before merge; no changes requested.
- 2026-09-02 `conductor/t-139` — check_pr_merged_drift.py's implementation_pr-field pass (0) treated a confirmed-merged field as the final word and never looked further, so a task reclaimed and reprogressed via a SECOND PR after the field was recorded left it silently stale with nothing left to catch it (real incident: interface-vision/t-104 closed with implementation_pr=kind_robots#2301 while a later cycle had already merged kind_robots#2303 first). Fixed with a new pass 0b (find_field_stale_findings): scan a field-confirmed task's own title+note for any OTHER PR reference that is both merged and title-confirmed as implementing this exact <project>/<task-id> -- same title-match bar the authoritative search pass already uses, so a note that merely quotes the PR whose kaizen suggestion filed the task doesn't false-positive. Deliberately scoped to field_findings only (never field_unresolved/malformed-field tasks) and best-effort (a failed lookup on the extra reference is silently skipped, not added to unresolved) so it adds zero API calls to every existing 'must not call the API further' test invariant. 17 new tests added; full repo suite still green (1585 passed, 1 skipped). Companion write-time fix already landed separately (close_task.py now warns on a stale --implementation-pr omission) -- t-139 was the read-side detection half.
- 2026-09-02 `conductor/t-145` — A soft/advisory CI check belongs on its own continue-on-error step inside an existing job (GitHub Actions ::warning:: annotations), not a new blocking job -- git diff --numstat plus git show <ref>:<path> is enough to diff base vs head line counts for any watched file without a second full-file-read diffing path. This session's sandbox pytest tool was again missing PyYAML (the same documented gap as t-140's session) and needed uv tool install pytest --with pyyaml --force before the 13 new tests could run.
- 2026-09-02 `conductor/t-140` — close_task.py now warns (not fails) when a review/ready close omits --implementation-pr while the roadmap already holds a different owner/repo#N value -- the write-time half of the drift class t-139 targets from the read side. Companion note: this session's own sandbox pytest tool was missing PyYAML (AGENTS.md's documented gap) and needed `uv tool install pytest --with pyyaml --force` before the new regression tests could run.
- 2026-09-02 `conductor/t-143` — GitHub's Contents API silently returns encoding:none/content:'' for files over 1MB, so any read-modify-write into a growing conductor file (art-prompts.yaml, TALKBACK.md, LEARNING.yaml) must fall back to the Git Blobs API and throw rather than treat a bodiless-but-nonempty read as an empty file -- kind_robots#2320 fixed both the queue write path and conductorGet() with this pattern plus an append-only invariant check.
- 2026-09-02 `ai-art-academy/t-078` — A workflow's KR_BASE_URL must be verified against the current self-hosted host (kindrobots.org), not copied from an older *.vercel.app pattern -- a wrong default would have made the new sentinel look deployed while silently never reaching its signature check. Caught in review before merge, fixed in one retry.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-02T20:53:49Z_
