# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-17T02:28:40Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **638**
- Outcomes: blocked: 14, cancelled: 1, done: 623
- Success rate: **98%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 64 | 98% |
| alexa-integration | 5 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 7 | 100% |
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
| text-generation | 1 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 622 | 99% |

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

- 2026-08-17 `text-generation/t-001` — The roadmap note assumed the private-server path was mostly unbuilt; a full read of server/api/chats/{openai,anthropic,ollama}/stream.post.ts, serverResolver.ts, and the Server Prisma model showed the opposite -- a working native Ollama route, full server CRUD/health infrastructure, and consistent mana gating already exist. The real gaps were narrower and more specific: serverResolver.ts's capabilityWhere('text') silently excludes OLLAMA from type-based resolution, three near-identical chat routes each duplicate a private cost estimator that has drifted from an already-correct shared estimateTextCostUsd (which also correctly multiplies by n, unlike the OpenAI route's local copy), and there is zero AbortController/cancellation wiring anywhere in the stack (server or chatStore.ts). Treating 'map the existing code' as a literal instruction rather than a formality caught a concrete, fixable billing-undercount bug (uncounted n) and a routing gap (Ollama) that a memory-based/greenfield-assuming brief would have missed or re-invented differently.
- 2026-08-16 `alexa-integration/t-021` — t-020's own kaizen note named a plausible-sounding follow-up scope (audit the 'unknown theme'/'no match' error branches) that turned out, on a fresh read, to already be functionally correct -- both branches already had the early return / proper if-else split needed to avoid a false-success ack. The real gap was regression coverage, not a bug: nothing protected those two branches from a future edit quietly dropping the early return, the lastError/pushLocalMessage report, or the postAck() success-only gating, which is exactly the false-success shape t-015/t-020 fixed for the action-mismatch case. Extended the existing checkSerendipityVoiceActionGuard.ts file with a second exported check (index-based anchor comparisons rather than full brace-parsing) instead of adding a fourth guard file, per the task note's own preference -- kept the fix inside the file whose npm script/CI step already covered it, so no workflow-file change was needed.
- 2026-08-16 `alexa-integration/t-020` — The target/action-mismatch bug class from t-015 (a shared VoiceBusCommand.action union reaching a dispatch branch where most of its values are meaningless) generalized cleanly to the other two targets once actually re-read fresh: applyThemeCommand() and applyArtCommand() never checked command.action at all, an omission invisible unless you specifically compare each dispatch function against its siblings for the same missing guard shape. Extending the existing guard into a TARGET_FUNCTIONS structure (mirroring modelBuilderStore.ts's own multi-function guard convention) kept the fix in one file instead of three near-duplicates.
- 2026-08-16 `appmaker/t-012` — A condition like `tasks.length === 0` reads as a reasonable 'freshly scaffolded' check in isolation, but was backwards in practice because the scaffolder (scripts/new_app.py) always seeds 3 tasks up front -- checking the UI condition against the actual data-seeding code, not just its surface plausibility, is what surfaced that every real app's card silently showed a blank description while the fallback literal only fired on a genuine lookup failure. Separately: a single CI job failing with a live-API 502 unrelated to the diff (GET /api/characters, in a population-quality contract check) is a textbook transient failure -- rerunning just that job and confirming a clean pass on retry is the correct triage, not blaming the diff or force-merging past it unexamined.
- 2026-08-16 `alexa-integration/t-015` — applyCommand()'s action parameter is a union shared across every command target (on/off/toggle/clear/set/draft), but set/draft only carry meaning for the theme/art targets. Unsupported *targets* were already reported as ignored; unsupported *actions* on a supported target had no equivalent check, so an animation command with action: set/draft fell through untouched and still posted a false 'Applied: <effect> on.' success message. When a field's type is a union shared across multiple branches, each branch needs its own explicit valid-subset check -- a guard scoped to one branch (here, target) doesn't protect the others by default. Kaizen t-020 audits the theme/art branches for the same class of gap.
- 2026-08-16 `model-builder/t-045` — t-029 cycle 7's item.error persistence sweep (#1908) covered generateItemAsset/ generateItemAssetAsync/pollAsyncArtJob/commitItem but deliberately left out draftText() to keep that fix surgical -- exactly the kind of scoped-on-purpose gap a filed kaizen task exists to close, rather than something the original cycle missed. draftText() turned out to be the highest-frequency failure path of all (autoBuildItem's very first step), so the gap was live from the moment #1908 merged. When a fix is deliberately scoped narrower than the full bug class it demonstrates, filing the remaining scope as its own task (rather than letting 'surgical for now' quietly become 'permanent') is what actually closes the loop -- this cycle also resolved the fix's own deferred sub-decision (whether manual edits should clear a stale error too) rather than re-deferring it a second time.
- 2026-08-16 `model-builder/t-029` — This is at least the fourth model-builder/t-029 cycle to find a 'local-only store mutation never actually reaches the server' bug in modelBuilderStore.ts -- stageStatuses/ sourceSnapshot JSON-string parsing on resume, prose-field truncation on commit, and now item.error never persisted on any failure branch (silently dropping the entire per-item failure-visibility feature on reload/reopen). Tracing a field's read side back to its write side across the whole store, not just the function that was the original suspect, is what surfaces these. A single meta-guard enumerating every server-readable field and asserting at least one pushItem/PATCH call site writes it -- rather than one guard per fixed field -- would likely catch this class proactively; filed as model-builder/t-045's sibling suggestion for a future cycle.
- 2026-08-16 `storybook/t-010` — A completeness guard (t-017's verifyStorybookObjectEntryLinks.mjs) that only asserts wiring is *present* -- button exists, query key is sent, seedFromQuery consumes it -- can pass cleanly while the values flowing through that wiring silently disagree. characterOptions built a synthetic id-based slug while the deep-link sender used the entity's real slug; three sibling ingredient types (Scenario/Facet/Reward) all keyed off the real slug correctly, so cross-checking a new field against its siblings' convention (not just its own local logic) is what surfaced the one outlier. A presence guard and an agreement guard test different failure modes -- both are worth having when a value crosses a wire boundary.
- 2026-08-16 `kapowarr/t-021` — The old library-import path masked ComicVine throttling as a no-match, making a reliability failure look like harmless empty search results. Large unattended jobs also need a stable work snapshot: self-review caught and removed an initial design that would have rescanned the entire library for every processed folder. Finally, the fork's Python Tests workflow was development-only, so PR/main test triggers were enabled and verified across Python 3.8 through 3.12 before merge.
- 2026-08-16 `model-builder/t-029` — A sixth same-day cycle again avoided the five already-mined leads and instead read the genuinely unexplored item-panel/recipe-selector/source-picker/run-history/manager front-end files, tracing a UI code comment ('snapshot survives resume') that turned out to be aspirational rather than true back to its root cause: normalizeStages()/adaptRun() gated JSON-string server data on typeof raw === 'object', which is never true once a value has round-tripped through a String @db.LongText column. A code comment asserting behavior ('X survives Y') is a claim, not a guarantee -- when a comment describes a property the surrounding code doesn't visibly enforce, tracing the actual data path back to its type at the boundary (string vs. parsed object) is a cheap way to catch the gap between what a comment promises and what the code actually does.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-17T02:28:40Z_
