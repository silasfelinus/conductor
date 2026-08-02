# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-02T20:40:31Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **474**
- Outcomes: blocked: 13, cancelled: 1, done: 460
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
| dream-cycle | 18 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| interface-vision | 33 | 100% |
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
| software | 459 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 9 |
| actionable | 9 |
| transient | 6 |
| scope | 1 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `quality` — 9 occurrences; look for the shared cause across its records
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `transient` — 6 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-02 `interface-vision/t-024` — Similar-looking gallery grids may own fundamentally different picker, CRUD, taxonomy, or relationship behavior. Classify live responsibilities and callers before extracting a shared shell; reuse behavior-neutral primitives rather than forcing a passive browse abstraction onto stateful tools.
- 2026-08-02 `interface-vision/t-017` — A file classified as a "page" purely by living in components/pages/ (verifyLayoutContract.ts's isPageComponent()) can still be an embedded widget, not a real page -- conductor-project-chat.vue was a per-project chat panel mounted inside conductor-page.vue, not a standalone view. Before forcing kr-surface/kr-scroll onto a root-surface violation, check whether the file is actually reachable as its own route/tab or only ever rendered as a child; moving it out of components/pages/ is often the correct fix, not a class change. Also: a LEARNING.yaml record with an invalid kind value breaks test_backfill_learning.py for every subsequent PR on main regardless of that PR's own diff -- confirm the base branch is broken before assuming a red "Python test suite" check means your own change is at fault.
- 2026-08-02 `interface-vision/t-017` — verifyLayoutContract.ts's root-tag regex only matches lowercase-first tag names, so a page component whose own template root is a PascalCase component reference (e.g. <ProjectFrontPage>) can never satisfy root-surface, even with the correct class present. When a shared shell is invoked from many call sites, check whether the checker can even parse the call site's own root tag before assuming a class-attribute fix will register — filed t-055 to fix the regex itself.
- 2026-08-02 `interface-vision/t-033` — When two CI scripts parse the same authored tree, keep one implementation and preserve old script names only as compatibility aliases so workflow callers do not drift.
- 2026-08-02 `interface-vision/t-047` — The one-scroll bucket contains at least two distinct shapes: mutually exclusive tab-switcher branches that can be mechanically consolidated under one shared scroll owner, and genuine dual-pane layouts that require a deliberate design decision about which pane owns scrolling. Grouping violations by shape keeps mechanical cleanup separate from judgment-heavy redesign.
- 2026-08-02 `interface-vision/t-025` — New whole-repository conformance rules should first measure the live debt through CI, then record that exact result as a shrink-only baseline so future violations fail without pretending historical debt is new.
- 2026-08-02 `interface-vision/t-022` — Composition-aware contracts need the same ratchet strategy as file-local contracts: measure existing debt explicitly, block additions immediately, and let future sweeps shrink the baseline instead of making the first honest measurement unmergeable.
- 2026-08-02 `interface-vision/t-021` — Re-verifying flagged-orphan components before deletion (not trusting a prior audit's flag blind) caught two false positives with live contract usage.
- 2026-08-02 `interface-vision/t-039` — Contract verifiers should emit concise pass/fail output; diagnostic source bundles need a real consumer or an explicit verbose mode.
- 2026-08-02 `interface-vision/t-020` — Achievement rewards must be granted atomically through server-side karma and mana ledgers; direct client balance patches are neither authoritative nor permitted.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-02T20:40:31Z_
