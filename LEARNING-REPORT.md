# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-21T09:13:49Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1097**
- Outcomes: blocked: 18, cancelled: 2, done: 1077
- Success rate: **98%**
- Average passes on successful tasks: **0.2**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 14 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 11 | 100% |
| approval-portal | 2 | 0% |
| art-archive | 32 | 100% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| butterfly-gallery | 29 | 93% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 39 | 100% |
| conductor | 127 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 25 | 100% |
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
| ruler-hooked | 19 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 33 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1080 | 99% |

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

- 2026-09-21 `ruler-hooked/t-027` — Merged silasfelinus/kind_robots#2949 (catch-reveal art + image-first Fishopedia): the task's own art dependency (t-019) was still 1/15 species short (choirfish's corrected re-render pending), but 14/15 bestiary images already existed and the UI change didn't need to wait for the last one -- the broken-image-safe <img> pattern already established in ruler-hooked-cosmetics-picker.vue (hide on @error instead of a broken-image icon) made shipping against a mostly-complete asset set safe. General lesson: a task blocked on "the art isn't all done yet" is often still workable once the display layer degrades gracefully per-asset --  check whether the existing broken-image/fallback convention in the codebase covers the gap before treating partial asset completion as a hard blocker. Also worth noting: running `prettier --write` on a whole pre-existing file that predates the repo's prettier adoption reformats far more than the actual change (this repo tracks such files in a documented ratchet, `verifyPrettierRatchet.ts`) -- reverting and hand-editing to match the file's existing style kept the diff scoped to the 9 lines actually added.
- 2026-09-21 `dream-cycle/t-028` — Merged silasfelinus/conductor#4913: build_dream_records.py's queue_art() now runs every assembled art_prompt through the same conditional-instruction check build_ruler_hooked_art_queue.py already used, extracted into shared scripts/art_prompt_conditional_check.py so the regex lives in exactly one Python place instead of a third copy. A violation is recorded as an ordinary failed API-call entry rather than a bare exception, so it rides the existing partial-failure rollback path for free -- the whole bundle rolls back and stays unbuilt for the next sweep, and nothing reaches art-prompts.yaml where it would otherwise re-fail a scheduled digest run silently. General lesson: when a validation gap is found downstream (here, kind_robots' server-side 422), check whether the same build script already has a partial-failure/rollback mechanism before reaching for a bare raise -- routing the new check through the existing failure shape (a synthetic entry in the results list) is less code and gets atomic rollback for free.
- 2026-09-21 `storybook/t-056` — Merged silasfelinus/kind_robots#2948, a clean concurrency-guard fix for submitStoryTurn: a conditional updateMany keyed on the narrated chapter replaces an unconditional write after an LLM round-trip, so a losing race replays the winner's committed turn (buildReplayedTurnResult) instead of double-writing LifeChoice/ LifeStat rows. Full CI green including the new regression test in verifyStorybookPlayLoop.ts (two concurrent submitStoryTurn calls, asserts exactly one LifeChoice row and one stat increment survive) run via the path-triggered davinci-seed-verify.yml workflow -- confirmed that workflow actually executed for this head SHA (not just inferred from a generic "verify" check name) before relying on it as the test evidence for a concurrency fix.
- 2026-09-21 `ruler-hooked/t-035` — Reviewed and merged silasfelinus/conductor#4899 (a concurrent session's clean, well-scoped, self-verified additive change). Its only red check, "Validate Worker PR handoff", was a missing "### Kaizen suggestion" heading in the PR body -- not a code defect. Fixed by editing the PR description directly (the workflow re-runs on `edited`, not just `synchronize`) rather than asking the Worker session to push a fix for a description-only gap. A stale failed check run from before the edit persisted in the check-runs list alongside the new passing one for the same head SHA; a status script must key off the latest run per check name; startTime, not just conclusion, when a check can legitimately re-run on the same commit.
- 2026-09-21 `conductor/t-177` — Start-Job is not a free way to bound a call: PowerShell 5.1 backs a background job with a real second powershell.exe process, confirmed by direct process trace popping its own visible console on the desktop every tick regardless of the parent task's own window state or how it was launched. When "run this with a timeout" is the actual requirement on Windows, System.Diagnostics.Process with CreateNoWindow=$true/ UseShellExecute=$false plus a manual WaitForExit(timeout)+Kill() gets the same bounded guarantee without a second process or its console. This sandbox has no PowerShell by default, but the official Linux pwsh tarball is fetchable through the agent proxy and is enough to AST-parse every .ps1 in the repo and exercise new process-launching logic against real child processes (stdin/stdout, timeout+kill, non-deadlocking large output) -- a meaningfully stronger verification bar than syntax-parsing alone for a change to a production watchdog this sandbox cannot otherwise observe running.
- 2026-09-21 `storybook/t-010` — Cycle 81 of the recurring storybook/t-010 bug-hunt: a system prompt and its schema/ validator can silently disagree about the SAME condition when they read it from two different places. buildStorybookSystemPrompt() read request.isFinalTurn directly to tell the model "return an empty choices array," while the schema/validator decided the choice-count rule from a separate options.finalTurn the caller had to remember to pass -- and the one production call site never did. The lesson generalizes: when a prompt and its own response contract both depend on the same boolean, derive the contract's flag FROM the prompt's input at the call site that builds both, rather than accepting it as a second, independently-suppliable parameter that can drift from the first. Also: forgot the DATABASE_URL-at-import-time gotcha from cycle 80's own lesson while writing this cycle's own guard script (a static import of storybookRuns.ts, which initializes Prisma) -- had to relearn it via a live CI failure on the first push, despite it being spelled out in the immediately preceding LEARNING.yaml entry. Reading the prior cycle's own lesson before writing a new guard script would have caught this before pushing, not after.
- 2026-09-21 `storybook/t-010` — Cycle 80 of the recurring storybook/t-010 bug-hunt: applyQuestProposal()'s idempotency check ("clicking twice must not create two to-dos") only keyed on the SAME proposal id being re-applied, but a needs-info checkpoint stays activeCheckpoint() across turns and can accumulate more than one unapplied proposal before any is accepted -- and the UI renders every unapplied proposal with its own independent Accept button. The write-back guarantee needs to be keyed on the CHECKPOINT, not the proposal, whenever a ledger/queue lets more than one pending item point at the same underlying real-world write. Also: a module that mixes pure logic with a Prisma-backed write path (storybookQuest.ts) forces every consumer, including a pure-logic test, to pay the module-level DATABASE_URL check at import time -- the fix was the existing verifyChildMaturityRestriction.ts pattern (dummy DATABASE_URL set before a dynamic import), not a source refactor, but it cost a full CI round-trip to discover contract-tests.yml's "Contract verifiers" job is genuinely DB-free and doesn't set one.
- 2026-09-20 `conductor/t-186` — A "grep every *.ps1 for a banned direct-call shape" regression guard needs a self-test proving it actually fires on a synthetic reintroduction, not just that today's files happen to be clean -- otherwise a regex that silently stops matching (a refactor, an escaping mistake) looks identical to "the gap stays closed" until the next manual audit finds it the hard way again. Comment-only references to the banned pattern (several files here legitimately explain in prose why they no longer call it that way) also need an explicit skip, or the guard flags its own documentation.
- 2026-09-20 `conductor/t-185` — Moving a pinned function out of one file into a shared, dot-sourced library is safe to do blind-to-runtime (no PowerShell available in this sandbox) as long as every consumer of the moved code is re-verified structurally: not just "does the new file parse" but "does each caller still have every free variable/function the moved code references in scope at the point it dot-sources the library" (here: Write-Log, $comfyDir, $comfyPython). Equally important: a file moved into a new subdirectory can silently drop out of a checker that globs non-recursively even when the CI *workflow's* own path-trigger filter still fires on it -- the workflow ran, reported green, and would have kept doing so while quietly no longer checking the one file that just moved. Grep for every place a repo re-derives "which files does this check cover" (a Get-ChildItem, a glob(), an rglob()) whenever adding a subdirectory to a previously-flat file layout, not just the CI trigger definition.
- 2026-09-20 `conductor/t-184` — When a task's own scope note offers a binary choice ("route it through X, or document why it's a deliberate exception") and a real gap is found that isn't actually deliberate, a third outcome -- document the gap honestly as a known, tracked issue and file a properly- scoped follow-up task -- is often the right call, especially when the "correct" fix (here: extracting a function pinned by source-contract tests out of a production Windows watchdog script) can't be behaviorally verified in a sandbox with no PowerShell, only syntax-checked by CI after the fact.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-21T09:13:49Z_
