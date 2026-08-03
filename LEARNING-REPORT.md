# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-03T09:20:03Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **482**
- Outcomes: blocked: 13, cancelled: 1, done: 468
- Success rate: **97%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 55 | 98% |
| alexa-integration | 2 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 6 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 25 | 100% |
| conductor | 59 | 100% |
| conductor-app | 2 | 100% |
| davinci | 2 | 100% |
| digital-storefront | 24 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| interface-vision | 40 | 100% |
| kind-robots | 39 | 97% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 48 | 100% |
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
| taskmaster | 2 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 467 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 9 |
| actionable | 9 |
| transient | 7 |
| scope | 1 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `quality` — 9 occurrences; look for the shared cause across its records
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `transient` — 7 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-03 `interface-vision/t-048` — A task released as actionable/stale (blocked on an unrelated component not yet migrated) can become trivially doable again once other, unrelated work lands -- re-verify the live premise from code before trusting a stale roadmap note, rather than assuming a prior session's blocker still holds.
- 2026-08-03 `interface-vision/t-057` — When a task's own verification instruction assumes infrastructure (a PR preview) that a repo-wide config (vercel.json) silently excludes for the exact branch prefix agent sessions use, the fallback isn't to skip verification -- it's to verify what CAN be checked (CI, structural reasoning about the change's own properties) and be explicit in the roadmap/PR about what's still open, rather than silently declaring full verification done.
- 2026-08-03 `interface-vision/t-031` — The object-card divergence was concentrated in Dream's shell and the repeated card body, not five wholly bespoke cards; inspect shared wrappers before planning a broad convergence rewrite.
- 2026-08-03 `interface-vision/t-065` — The implementation half of this task (scripts/next_free_task_id.py, PR #1588) merged, but the task couldn't close because it was left with a queued rearm task-event that the processor rejected every run (`rearm requires recurring: true` -- t-065 isn't a recurring task). A connector-only session can't tell mid-task whether a target task is recurring without reading the live roadmap first; docs/github-connector-worker.md listed `rearm` and `ready` as interchangeable options with no mention of the recurring gate, so the wrong operation was a natural mistake, not carelessness. A concurrent session fixed the stuck event with the correct `operation: ready` while this session was independently mid-flight on the actual remaining work (wiring scripts/next_free_task_id.py into AGENTS.md's task-id-assignment call sites); rebasing onto that fix rather than duplicating it is what let both land cleanly. Documented the rearm-vs-ready distinction in docs/github-connector-worker.md so the next connector session doesn't repeat it.

- 2026-08-03 `interface-vision/t-062` — A roadmap can carry two tasks sharing an id (find_task/find_task_block match the first occurrence, silently stranding the second) because audit_roadmaps.py's DUPLICATE_TASK_ID check existed but was purely advisory -- main() never returned non-zero, and its report only got committed to main under a stale one-off branch condition. Detection without enforcement doesn't stop the bug; wire the check into something CI actually gates (a pytest-covered script) or it will collide again, as it did here even on the very fix meant to prevent it.
- 2026-08-02 `interface-vision/t-030` — Before reimplementing a ready task, compare its note, current code, and recent merged PRs. A task can carry a complete merged result but remain incorrectly ready because an earlier closeout targeted a different task ID; repair roadmap state instead of duplicating the code.
- 2026-08-02 `dream-cycle/t-006` — A self-modifying "bootstrap a CI job that patches, tests, then commits" pattern has a sharp edge: if the commit step fails, everything the job did in its ephemeral checkout is silently discarded -- there is no partial-progress trail beyond whatever the job log happened to print. Here the patch applied cleanly and 802 tests passed, but `git diff --check` (run right after tests, right before the commit) caught a stray blank line at EOF the patch script itself introduced, and the job died there -- twice, identically, across two separate one-shot workflow files (agent-run-daily-dream-art-dedup.yml, agent-apply-daily-dream-art-dedup.yml), each triggered by a "push the workflow file to trigger it" bootstrap. Neither failure was ever investigated between attempts; a third workflow was authored instead of reading the first failure's job log, which would have shown the exact line and exit code. When a verified/tested CI step fails on the *next* step, read that step's log before re-authoring the automation -- the fix is often a one-line bug in the patcher itself, not a reason to change approach. Bounded, self-removing one-shot patch scripts are fine, but they should be run and debugged locally first, not iterated against CI round-trips at ~5 minutes per failed attempt.

- 2026-08-02 `interface-vision/t-053` — A content page mounting the wrong component doesn't error -- it silently renders whatever the mount resolves to (content/button.md mounted :lab-manager since its creation in PR #1280, a copy-paste mistake with no route in that component's own tab mapping; /button just fell back to WonderLab's review UI). git blame the file's origin before assuming a mount was ever correct and later drifted. Separately: fixing the mount is not automatically safe on its own -- mounting a component via MDC for the first time can expose a pre-existing kr-surface/kr-scroll violation that verifyMdcScrollOwnership.ts (not just verifyLayoutContract.ts) will catch, since an MDC-mounted page must not fight pages/[...slug].vue's content-host for scroll ownership. With no local dev server (DB unreachable) and no Vercel PR-preview for agent branches (vercel.json exclusion), match the proven-safe pattern already used by other MDC-mounted -page.vue components (plain divs, no scroll classes) rather than guessing whether kr-surface's h-full behaves inside an auto-height flex host -- and widen the root-surface allow-list deliberately (documented, not gamed) rather than force a scroll primitive onto a component the checker didn't originally evaluate as MDC-mounted.

- 2026-08-02 `interface-vision/t-024` — Similar-looking gallery grids may own fundamentally different picker, CRUD, taxonomy, or relationship behavior. Classify live responsibilities and callers before extracting a shared shell; reuse behavior-neutral primitives rather than forcing a passive browse abstraction onto stateful tools.
- 2026-08-02 `interface-vision/t-017` — A file classified as a "page" purely by living in components/pages/ (verifyLayoutContract.ts's isPageComponent()) can still be an embedded widget, not a real page -- conductor-project-chat.vue was a per-project chat panel mounted inside conductor-page.vue, not a standalone view. Before forcing kr-surface/kr-scroll onto a root-surface violation, check whether the file is actually reachable as its own route/tab or only ever rendered as a child; moving it out of components/pages/ is often the correct fix, not a class change. Also: a LEARNING.yaml record with an invalid kind value breaks test_backfill_learning.py for every subsequent PR on main regardless of that PR's own diff -- confirm the base branch is broken before assuming a red "Python test suite" check means your own change is at fault.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-03T09:20:03Z_
