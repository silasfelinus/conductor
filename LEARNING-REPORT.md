# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-16T12:29:21Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **633**
- Outcomes: blocked: 14, cancelled: 1, done: 618
- Success rate: **98%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 64 | 98% |
| alexa-integration | 2 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 6 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 12 | 92% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 76 | 100% |
| conductor-app | 4 | 100% |
| davinci | 4 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| interface-vision | 83 | 100% |
| kapowarr | 16 | 100% |
| kind-robots | 50 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 68 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 11 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 617 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 13 |
| actionable | 9 |
| transient | 9 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 13 occurrences; look for the shared cause across its records
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `transient` — 9 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-16 `model-builder/t-045` — t-029 cycle 7's item.error persistence sweep (#1908) covered generateItemAsset/ generateItemAssetAsync/pollAsyncArtJob/commitItem but deliberately left out draftText() to keep that fix surgical -- exactly the kind of scoped-on-purpose gap a filed kaizen task exists to close, rather than something the original cycle missed. draftText() turned out to be the highest-frequency failure path of all (autoBuildItem's very first step), so the gap was live from the moment #1908 merged. When a fix is deliberately scoped narrower than the full bug class it demonstrates, filing the remaining scope as its own task (rather than letting 'surgical for now' quietly become 'permanent') is what actually closes the loop -- this cycle also resolved the fix's own deferred sub-decision (whether manual edits should clear a stale error too) rather than re-deferring it a second time.
- 2026-08-16 `model-builder/t-029` — This is at least the fourth model-builder/t-029 cycle to find a 'local-only store mutation never actually reaches the server' bug in modelBuilderStore.ts -- stageStatuses/ sourceSnapshot JSON-string parsing on resume, prose-field truncation on commit, and now item.error never persisted on any failure branch (silently dropping the entire per-item failure-visibility feature on reload/reopen). Tracing a field's read side back to its write side across the whole store, not just the function that was the original suspect, is what surfaces these. A single meta-guard enumerating every server-readable field and asserting at least one pushItem/PATCH call site writes it -- rather than one guard per fixed field -- would likely catch this class proactively; filed as model-builder/t-045's sibling suggestion for a future cycle.
- 2026-08-16 `storybook/t-010` — A completeness guard (t-017's verifyStorybookObjectEntryLinks.mjs) that only asserts wiring is *present* -- button exists, query key is sent, seedFromQuery consumes it -- can pass cleanly while the values flowing through that wiring silently disagree. characterOptions built a synthetic id-based slug while the deep-link sender used the entity's real slug; three sibling ingredient types (Scenario/Facet/Reward) all keyed off the real slug correctly, so cross-checking a new field against its siblings' convention (not just its own local logic) is what surfaced the one outlier. A presence guard and an agreement guard test different failure modes -- both are worth having when a value crosses a wire boundary.
- 2026-08-16 `kapowarr/t-021` — The old library-import path masked ComicVine throttling as a no-match, making a reliability failure look like harmless empty search results. Large unattended jobs also need a stable work snapshot: self-review caught and removed an initial design that would have rescanned the entire library for every processed folder. Finally, the fork's Python Tests workflow was development-only, so PR/main test triggers were enabled and verified across Python 3.8 through 3.12 before merge.
- 2026-08-16 `model-builder/t-029` — A sixth same-day cycle again avoided the five already-mined leads and instead read the genuinely unexplored item-panel/recipe-selector/source-picker/run-history/manager front-end files, tracing a UI code comment ('snapshot survives resume') that turned out to be aspirational rather than true back to its root cause: normalizeStages()/adaptRun() gated JSON-string server data on typeof raw === 'object', which is never true once a value has round-tripped through a String @db.LongText column. A code comment asserting behavior ('X survives Y') is a claim, not a guarantee -- when a comment describes a property the surrounding code doesn't visibly enforce, tracing the actual data path back to its type at the boundary (string vs. parsed object) is a cheap way to catch the gap between what a comment promises and what the code actually does.
- 2026-08-16 `model-builder/t-029` — A fifth same-day cycle deliberately avoided re-walking the four already-audited leads (backend commit/promotion races, autoBuildRun status accuracy, per-item outcome UI) and instead read a genuinely untouched file (stores/helpers/modelBuilderFields.ts), which surfaced a real silent data-loss bug: a duplicated blob parser in commit.post.ts dropped every line without a colon, truncating multi-line prose fields to their first line only at COMMIT time -- invisible in the preview panel, which parses the same blob correctly for display. Two independent copies of the same parsing logic drifting apart (one used for preview, one for the actual DB write) is exactly the shape of bug a single-copy refactor (delegate to one shared splitter) prevents structurally rather than relying on both copies staying in sync by discipline. Worth generalizing: when a codebase has a 'preview' and a 'commit' path over the same data, check whether they share one implementation or two -- a second copy is a standing invitation for silent drift.
- 2026-08-16 `model-builder/t-029` — A recurring task's title is the scope contract, not just a label -- after three same-day cycles of 'bug-hunt cycle' backend security audits on a task literally named 'Polish and upgrade Model Builder front-end surface,' the fourth cycle returned to genuine front-end work (a batch/auto-build per-item failure indicator) and found the store itself was under-instrumented for it (item.error only set on 2 of several 'failed' return paths), which the backend-only lens of the prior three cycles had no reason to surface. When a recurring task's cycles drift away from its own title toward whatever the last cycle's kaizen suggested, checking the title itself is a cheap way to catch scope drift before it compounds.
- 2026-08-16 `kind-robots/t-065` — A task note's own paraphrase of 'same pattern as an earlier task' can be less precise than that earlier task's actual diff -- t-065's note said 'add a short dated correction note to t-046,' but t-055 (the cited precedent) had actually added a dated entry to a separate site-audit-inventory-notes.md doc specifically to avoid rewriting an already-closed task's long note. Reading the real precedent's implementation, not just its task-note summary, produced the better (and actually-intended) outcome.
- 2026-08-16 `kapowarr/t-020` — Milestone-level status: fields don't auto-derive from their tasks' individual statuses in this roadmap format -- they're independently hand-set and can silently drift stale even when every task under them is accurate. This is the third independent surfacing of the same pattern (after kind-robots/t-058 and kindrobots-unraid's noted-but-unfiled instance in the same audit), reinforcing the audit's own kaizen suggestion that validate_roadmaps.py should warn when a milestone's tasks are more advanced than its own status field.
- 2026-08-16 `kapowarr/t-019` — When a task note says 'port X, scoped down per the note,' read the note's stated scope literally rather than porting everything -- dropping conductor's own STRANDED-tier age-based judgment logic (as the task explicitly asked) kept silasfelinus/Kapowarr#11's branch_janitor.py to two simple tiers (MERGED auto-delete, FORCE explicit override) instead of over-porting complexity the target repo didn't need. A live end-to-end smoke test against a real local bare git remote (not just mocked unit tests) is what actually proved the merged/unmerged/force-delete behavior worked, matching this repo's own convention for anything that shells out to git.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-16T12:29:21Z_
