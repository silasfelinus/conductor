# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-02T22:37:16Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **477**
- Outcomes: blocked: 13, cancelled: 1, done: 463
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
| interface-vision | 35 | 100% |
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
| coordination | 1 | 100% |
| software | 461 | 99% |

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

- 2026-08-02 `interface-vision/t-030` — Before reimplementing a ready task, compare its note, current code, and recent merged PRs. A task can carry a complete merged result but remain incorrectly ready because an earlier closeout targeted a different task ID; repair roadmap state instead of duplicating the code.
- 2026-08-02 `dream-cycle/t-006` — A self-modifying "bootstrap a CI job that patches, tests, then commits" pattern has a sharp edge: if the commit step fails, everything the job did in its ephemeral checkout is silently discarded -- there is no partial-progress trail beyond whatever the job log happened to print. Here the patch applied cleanly and 802 tests passed, but `git diff --check` (run right after tests, right before the commit) caught a stray blank line at EOF the patch script itself introduced, and the job died there -- twice, identically, across two separate one-shot workflow files (agent-run-daily-dream-art-dedup.yml, agent-apply-daily-dream-art-dedup.yml), each triggered by a "push the workflow file to trigger it" bootstrap. Neither failure was ever investigated between attempts; a third workflow was authored instead of reading the first failure's job log, which would have shown the exact line and exit code. When a verified/tested CI step fails on the *next* step, read that step's log before re-authoring the automation -- the fix is often a one-line bug in the patcher itself, not a reason to change approach. Bounded, self-removing one-shot patch scripts are fine, but they should be run and debugged locally first, not iterated against CI round-trips at ~5 minutes per failed attempt.

- 2026-08-02 `interface-vision/t-053` — A content page mounting the wrong component doesn't error -- it silently renders whatever the mount resolves to (content/button.md mounted :lab-manager since its creation in PR #1280, a copy-paste mistake with no route in that component's own tab mapping; /button just fell back to WonderLab's review UI). git blame the file's origin before assuming a mount was ever correct and later drifted. Separately: fixing the mount is not automatically safe on its own -- mounting a component via MDC for the first time can expose a pre-existing kr-surface/kr-scroll violation that verifyMdcScrollOwnership.ts (not just verifyLayoutContract.ts) will catch, since an MDC-mounted page must not fight pages/[...slug].vue's content-host for scroll ownership. With no local dev server (DB unreachable) and no Vercel PR-preview for agent branches (vercel.json exclusion), match the proven-safe pattern already used by other MDC-mounted -page.vue components (plain divs, no scroll classes) rather than guessing whether kr-surface's h-full behaves inside an auto-height flex host -- and widen the root-surface allow-list deliberately (documented, not gamed) rather than force a scroll primitive onto a component the checker didn't originally evaluate as MDC-mounted.

- 2026-08-02 `interface-vision/t-024` — Similar-looking gallery grids may own fundamentally different picker, CRUD, taxonomy, or relationship behavior. Classify live responsibilities and callers before extracting a shared shell; reuse behavior-neutral primitives rather than forcing a passive browse abstraction onto stateful tools.
- 2026-08-02 `interface-vision/t-017` — A file classified as a "page" purely by living in components/pages/ (verifyLayoutContract.ts's isPageComponent()) can still be an embedded widget, not a real page -- conductor-project-chat.vue was a per-project chat panel mounted inside conductor-page.vue, not a standalone view. Before forcing kr-surface/kr-scroll onto a root-surface violation, check whether the file is actually reachable as its own route/tab or only ever rendered as a child; moving it out of components/pages/ is often the correct fix, not a class change. Also: a LEARNING.yaml record with an invalid kind value breaks test_backfill_learning.py for every subsequent PR on main regardless of that PR's own diff -- confirm the base branch is broken before assuming a red "Python test suite" check means your own change is at fault.
- 2026-08-02 `interface-vision/t-017` — verifyLayoutContract.ts's root-tag regex only matches lowercase-first tag names, so a page component whose own template root is a PascalCase component reference (e.g. <ProjectFrontPage>) can never satisfy root-surface, even with the correct class present. When a shared shell is invoked from many call sites, check whether the checker can even parse the call site's own root tag before assuming a class-attribute fix will register — filed t-055 to fix the regex itself.
- 2026-08-02 `interface-vision/t-033` — When two CI scripts parse the same authored tree, keep one implementation and preserve old script names only as compatibility aliases so workflow callers do not drift.
- 2026-08-02 `interface-vision/t-047` — The one-scroll bucket contains at least two distinct shapes: mutually exclusive tab-switcher branches that can be mechanically consolidated under one shared scroll owner, and genuine dual-pane layouts that require a deliberate design decision about which pane owns scrolling. Grouping violations by shape keeps mechanical cleanup separate from judgment-heavy redesign.
- 2026-08-02 `interface-vision/t-025` — New whole-repository conformance rules should first measure the live debt through CI, then record that exact result as a shrink-only baseline so future violations fail without pretending historical debt is new.
- 2026-08-02 `interface-vision/t-022` — Composition-aware contracts need the same ratchet strategy as file-local contracts: measure existing debt explicitly, block additions immediately, and let future sweeps shrink the baseline instead of making the first honest measurement unmergeable.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-02T22:37:16Z_
