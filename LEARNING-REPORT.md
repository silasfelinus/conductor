# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-26T04:22:42Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1150**
- Outcomes: blocked: 19, cancelled: 2, done: 1129
- Success rate: **98%**
- Average passes on successful tasks: **0.3**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 20 | 95% |
| animation-studio | 2 | 50% |
| appmaker | 11 | 100% |
| approval-portal | 2 | 0% |
| art-archive | 34 | 100% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| butterfly-gallery | 32 | 94% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 39 | 100% |
| conductor | 136 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 28 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 140 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 11 | 100% |
| kind-robots | 73 | 99% |
| kindrobots-unraid | 9 | 100% |
| lora-ingestion | 11 | 100% |
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
| ruler-hooked | 23 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 44 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1133 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 42 |
| transient | 17 |
| actionable | 17 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 42 occurrences; look for the shared cause across its records
- failure category `transient` — 17 occurrences; look for the shared cause across its records
- failure category `actionable` — 17 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-26 `storybook/t-069` — A new mechanical checker (verifyVerifierFilenameReferences.mjs, t-068) that ships with only a --self-test on synthetic strings can still be badly broken on real repo state -- running it for real, as part of wiring it into CI, found it flagging 16 lines across the actual utils/scripts/ directory (2 genuine stale doc references plus 14 false positives from self-test/.test.ts fixtures and a multi-line historical-context miss). Before wiring any new "scan every file for X" guard into CI, run it once against the real tree, not just its own unit self-test, since the self-test only proves the matching function works on hand-picked strings.
- 2026-09-26 `conductor/t-196` — set_task_field.py's ALLOWED_FIELDS is a single shared allow-list -- close_task.py's --set imports and gates through the exact same constant rather than keeping a second copy, so a field gap the task description worded as "extend both scripts" only needed one edit. Confirmed by reading close_task.py's own import line before touching anything, rather than assuming the docstring's "both scripts" implied two allow-lists to keep in sync.
- 2026-09-26 `conductor/t-195` — A recurring task's "status stuck at claimed" drift was not a write-atomicity bug in claim_task.py/close_task.py (both always write status+claimed_by+claimed_at together) -- it was a merge-conflict resolution that took origin/main's whole conflicted hunk instead of resolving per-task, discarding this task's own just-written status fix while correctly keeping an unrelated task's genuinely newer claim from the same hunk. The reliable mechanical check is the invariant itself (a claimed status with claimed_by/claimed_at both null can never come from a live claim), not parsing recurring-task note prose for "re-arming to ready".
- 2026-09-26 `kind-robots/t-123` — A repo-wide doc fix from a kaizen suggestion is worth doing in the same session even when it ranks below the top priority.yaml project -- the priority order picks which project to work when several have real ready work, it is not a rule against picking up a quick, reversible, already-scoped kaizen task once the higher-ranked project's only ready task is a recurring monitor that was already re-checked minutes earlier with no change.
- 2026-09-26 `kind-robots/t-122` — A stranded worker branch (implementation done, PR never opened because a prior session's create_pull_request call hit a connector write-safety block) is safe to open as-is without reimplementing -- but re-verify it against a full CI run before merging, not just the one purpose-built verifier the original author ran locally. CI caught a real gap the original commit missed -- verifyMaturityPrivacyContract.ts still pinned the pre-change "activeTab.value !== 'gallery'" substring the diff had removed, even though the author had already updated the sibling verifyGalleryProgressiveRendering.ts for the same rename. One file's test being updated is not evidence every file pinning the same string was.
- 2026-09-25 `animation-manager/t-007` — A background subagent asked to poll its own PR's CI and hand back when green can loop its SubagentHandback if it runs its own internal Monitor task -- tell it up front to cancel that Monitor before the final handback, not just to stop when done, or the coordinator ends up re-processing the same report repeatedly.
- 2026-09-25 `storybook/t-068` — A closed-review task with no implementation_pr recorded is invisible to merged-PR drift checks that hit a lookup failure elsewhere (here, an unrelated 403 on a same-task-id lookup in a different repo) -- always record implementation_pr at close-out time so a later drift check has something to verify against directly instead of falling back to a repo-guessing search.
- 2026-09-25 `kind-robots/t-121` — Binary image fetches that bypass performFetch must carry the same Bearer token as normal API calls, and UI changes should be checked against the Prettier ratchet before the first CI pass.
- 2026-09-24 `ruler-hooked/t-030` — For image-led game-state views, reuse the canonical composited scene and live ContentBundle/save data rather than creating a second visual/state representation; container-responsive auto-fit grids also satisfy the layout contract better than viewport breakpoints inside reusable components.
- 2026-09-24 `kind-robots/t-119` — Gallery controls can exist yet be unreachable when a parent suppresses the child header; surface cross-view state at the owning page level. Also treat supportedServer as a loader lane, not a training-family guarantee, and preserve HUMAN LoRA classifications when repairing inferred categories.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-26T04:22:42Z_
