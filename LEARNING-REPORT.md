# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-05T14:44:35Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **876**
- Outcomes: blocked: 16, cancelled: 1, done: 859
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
| dream-cycle | 23 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 99 | 100% |
| kapowarr | 50 | 100% |
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
| storybook | 18 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 860 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 17 |
| transient | 13 |
| actionable | 12 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 17 occurrences; look for the shared cause across its records
- failure category `transient` — 13 occurrences; look for the shared cause across its records
- failure category `actionable` — 12 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-05 `interface-vision/t-104` — Slice 83 of the recurring kr-btn consistency sweep: cross-checking the full existing .kr-btn-* size/radius grid for the bare (no color, no ghost) family before grepping found the gap directly -- .kr-btn-xs (btn btn-xs rounded-xl) was missing even though its ghost-family counterpart .kr-btn-ghost-xs already existed and the xs-size rounded-lg/rounded-2xl bare variants already existed too. Comparing across the family's established naming grid (color x size x radius) surfaces gaps faster than a fresh unconstrained grep every slice.
- 2026-09-05 `kapowarr/t-071` — library_conflicts.py's word-overlap heuristic for 'unrelated series sharing a folder' had a blind spot exactly at its most valuable case: volumes with the identical title share every word, so the check that skipped groups with any word in common skipped identical-title pairs before it skipped anything else -- and an identical-title pair sharing a folder is precisely the case where the importer cannot tell them apart and silently misattributes files. The fix asks the same match_title() function the importer itself uses, rather than inventing a second 'same series' notion in the diagnostic script. General lesson: when a diagnostic script re-implements a decision the system under test already makes elsewhere (here, 'are these two titles the same'), call the real function instead of a parallel heuristic -- a parallel heuristic can silently diverge from what actually happens at runtime, in exactly the direction that hides the worst cases.
- 2026-09-05 `dream-cycle/t-006` — kind_robots#2414's --repair-tainted path cancelled legacy PENDING ArtJobs and committed Facet.artPrompt updates before the eager queue.map(buildFacetArtPayload(...)) that can throw via assertArtPromptContract on any queued entry -- a destructive/cancelling write committed ahead of the step that can still fail, with no rollback. Pass 1's retry_context named the exact fix (build/validate jobRows before the cancellation); pass 2 fixed an adjacent real concern (deleted the unattended auto-merge repair workflow) but left the flagged file byte-identical, confirmed via git log on the changed file rather than trusting the PR description -- checking whether a retry actually touched the flagged file is what caught the drift before a third wasted pass. Pass 3 finally reordered validate-then-mutate as asked. General principle for any script that repairs/replaces existing state: build and validate the full replacement set first; only then commit any cancellation or in-place mutation of what it replaces.
- 2026-09-05 `interface-vision/t-104` — Slice 80 of the recurring kr-btn consistency sweep: the local kind_robots worktree checkout was found 8 commits behind origin/main (still at slice 71) before the candidate grep ran -- always fetch/ fast-forward the working checkout first, or a grep for the next uncovered class-set risks re-surfacing patterns already migrated by slices merged since the checkout was last synced, or missing that several prior slices already landed. Separately, a create_or_update_file API call built by hand (rather than passing already-read content through) wrote a literal placeholder string as the entire file content instead of the real payload -- caught immediately by reading the file back before opening the follow-on PR, fixed with a plain follow-up commit (no force-push). Always read back a large scripted file write before trusting it. Also: this task's TALKBACK.md had drifted four slices behind its own roadmap note (last entry was slice 69, though kind_robots slices 76-79 had already merged and the note already recorded them) -- worth a dedicated catch-up pass in a future slice.
- 2026-09-05 `storybook/t-010` — narratorStore.ts's activeDream.value?.id watch reset narratorSessionIds on Dream switch, but sendNarratorMessage() had no way to notice a switch that happened mid-await -- its addChat()/streamResponse() continuation still pushed the abandoned chat id into the new Dream's (already-reset) session list. Any store that (a) derives visible state from an array of ids scoped to some 'current context' ref, and (b) resets that array on a watch when the context changes, needs its own in-flight async writers to capture an epoch/ticket before their first await and re-check it after every await -- the same openRunRequestId shape already used in modelBuilderStore.ts. A stale retry_context is also worth checking before assuming a rejected fix was never resubmitted: git blame on the file it targets can confirm the fix already landed under a later, unlogged cycle, in which case the field should be cleared rather than left looking like an open rejection.
- 2026-09-04 `storybook/t-010` — A v-for split across several sibling lists by a computed classifier (narrative-role-assigner.vue's four casting tiers) is a real keyboard-focus hazard: an item that changes classification moves to a different <ul> entirely, which Vue cannot patch in place -- it unmounts the old node and mounts a fresh one, silently dropping focus to <body>. Any interactive element inside a re-classified v-for item needs an explicit post-nextTick refocus keyed on a stable identity (member+action), not just correctness of the classification logic itself. Worth checking other multi-tier/ multi-bucket v-for surfaces (stage role assignment, batch/queue boards) for the same pattern.
- 2026-09-03 `rainbow-butterflies/t-027` — State-reconciliation drift: PR kind_robots#2344 merged 2026-09-03T00:05Z but the roadmap task was left at status=review rather than done. Same pattern as media-watchlist/t-006 this cycle -- reconciled via GitHub MCP after the raw API probe 403'd.
- 2026-09-03 `media-watchlist/t-006` — State-reconciliation drift: PR kind_robots#2275 merged 2026-08-31 but the roadmap task sat at status=claimed for ~3 days with no queued task-event to auto-correct it. check_pr_merged_drift.py's raw urllib GitHub API probe 403'd in this sandbox (documented, connector-only limitation) and reported it unverifiable rather than confirming the merge -- reconciled via GitHub MCP pull_request_read directly. A session running the drift check should not stop at 'could not verify' when a working MCP transport is available in the same session; cross-check before treating the finding as inconclusive.
- 2026-09-02 `model-builder/t-029` — This task's own icon-coverage guard (cycle 82/84) only ever scanned the three shared data-structure arrays in modelBuilderRecipes.ts, leaving every per-component kind-icon: literal (view-mode toggles, inline button icons) completely unchecked -- a real, live, user-facing blank-icon bug (model-builder-source-picker.vue's List button, kind-icon:document, assets/icons/document.svg never existed) sat unnoticed through 84 prior cycles of otherwise-thorough code reading because none of them grepped literal icon-name strings against the actual assets/icons/ directory. When a project defines a 'coverage guard' for a hand-typed-name class of bug, scope it to every place that name shape can appear (grep the whole component family, not just the canonical data source), not just the one file where the bug was first found -- a guard that only covers its own origin story leaves the same failure mode live everywhere else. Also: a guard's own explanatory code comment can trip its own widened regex if it quotes the broken value literally (kind-icon:document appearing in prose) -- run a newly widened guard against your own diff before pushing, not just against the target file, to catch this class of self-inflicted false positive before CI does.
- 2026-09-02 `model-builder/t-029` — A non-nested-brace entry-split regex is fragile against free-text comments that themselves contain a literal open/close brace pair (a code path like server/api/(dreams,scenarios)/... quoted in a comment, using curly braces in the real source) -- it can silently swallow the real entry that follows, while the guard still prints a plausible-looking pass/total. verifyModelBuilderIconCoverageGuard.ts (cycle 82) shipped with exactly this gap for a full cycle before cycle 84 caught it while building an unrelated sibling guard. verifyModelBuilderSourceFieldGuard.ts already used a safer key-boundary split (index-based chunking between consecutive `key: '...'` matches, never touching brace characters at all) -- worth defaulting new SOURCE_TYPES/BUILD_STAGES/RECIPES-array guards to that pattern from the start rather than brace matching, and worth a future cycle double-checking any other guard in this family that still uses brace matching.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-05T14:44:35Z_
