# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-01T17:43:39Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **448**
- Outcomes: blocked: 13, cancelled: 1, done: 434
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
| interface-vision | 7 | 100% |
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
| software | 433 | 99% |

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

- 2026-08-01 `interface-vision/t-004` — CI caught a real conflict a general layout-contract sweep can't see: verifySerendipityRouteCutover.mjs hard-locks one page's exact <h1> markup as a route-cutover migration contract, unrelated to the one-header rule this task was adopting elsewhere. First push broke it, fixed in a follow-up commit. Filed t-023 (composition-lock audit) so t-017's later sweep can grep for hard-coded-markup contract tests across the remaining allow-list files up front instead of discovering them one CI failure at a time. General principle: a shrink-only CI ratchet only protects against violating ITS OWN rule -- it says nothing about whether some other, unrelated contract test depends on the exact markup being changed. Scope discipline (only fix what's asked, skip files another task/system explicitly owns) also paid off here -- deliberately left 8 of 29 files unfixed (admin routes, two "known offender" files t-017 already owns, one orphaned file, and this locked-contract file) rather than attempting a blind full sweep.

- 2026-08-01 `interface-vision/t-003b` — Flipping app.vue's shared shell from overflow-y-auto to overflow-hidden required auditing which of ~60 candidate page-level components actually needed their own scroll container vs. inherited one from an ancestor (pages/[...slug].vue's content-host for MDC routes, the shared ProjectFrontPage wrapper for conductor pages). A same-PR review catch (kr-hourly session) found the first push added scroll classes to six components that are mounted *inside* content-host, creating nested double-scroll regions -- the exact composition bug the task existed to fix. The file-by-file layout-contract verifier couldn't catch this because it has no parent/child composition awareness; grepping content/*.md for each candidate file's actual mount point before adding a scroll class (not just checking whether the file itself lacks one) would have caught it on the first pass. Fixed same-session via a follow-up commit once flagged. When a shared ancestor already owns scroll, verify a component is actually reachable outside that ancestor before adding its own overflow region -- otherwise ask "does this file's *rendering context* already scroll" before "does this file declare its own overflow."

- 2026-08-01 `interface-vision/t-010` — Clean first-pass except for one CI miss caught by the pipeline itself: a new content/*.md page needs a matching content/channels/<channel>/ <tab>.md registration or verifyChannelContent.ts fails with "references unknown tab" -- worth checking for that registration file up front whenever adding a new channelKey/tabKey pair, not just when CI catches it. Also: when a task note bundles a well-scoped bug fix with a vaguer "and show X on cards" ask that has no existing data model to support it, splitting the vague half into its own ready task (rather than guessing at scope) kept this PR small and reviewable.

- 2026-08-01 `interface-vision/t-003` — Task note prescribed a single risky change (flip app.vue's scroll ownership) with no mention of the 18-of-30 components/pages/*.vue files that would silently lose all scroll capability if flipped without per-page backfill first. Landed the safe structural half, split the audit-and-flip half into t-003b rather than attempting it blind in a sandbox with no local dev/DB to verify against -- treat "recommended fix" in a task note as a starting hypothesis to verify against the actual codebase, not a checklist to execute literally, especially for anything touching a shared ancestor every page depends on.

- 2026-08-01 `interface-vision/t-007` — Migration was audited line-by-line only after merge, not before -- caught the scope mismatch by luck (checking the migration for the audit rule) rather than by process (diffing file list against PR body before merging). Next time: pull_request_read get_files before merge_pull_request, every time, not just when the PR body itself flags a migration.

- 2026-08-01 `interface-vision/t-005` — verifyLayoutContract CI ratchet shipped inside the same PR as t-001, ahead of its declared depends_on (t-004) -- the dependency was aesthetic-neutral tooling work, not a hard blocker, so building it early was fine, but it means depends_on isn't a reliable signal for "has this actually not started yet" when a Worker judges a prerequisite doesn't really gate the dependent task's content.

- 2026-08-01 `interface-vision/t-001` — Storymaker aesthetic mockups (kind_robots PR #1252) landed correctly, but the roadmap task sat at status:ready with an open PR for hours -- a session picking up interface-vision should check open kind_robots PRs against roadmap task titles before claiming, since select_role.py's local script currently can't reach the GitHub API in this sandbox (403s), so a manual GitHub MCP check is the only way to catch this.

- 2026-08-01 `model-builder/t-039` — A recurring task (t-029) with a long streak of same-day merges hits diminishing returns fast on its own open-ended "read everything, find one new bug" pattern -- checking sibling ready tasks in the same project for an already-scoped, concrete kaizen (here, a deferred regression-guard task from two prior cycles) is a better use of a cycle than an Nth micro-race-condition hunt once N is already large for the day.

- 2026-08-01 `coloring-book/t-022` — When a recurring art-production task is blocked on a missing local credential (no ANTHROPIC_API_KEY here), the semantic gate's own rejection reasons are structured enough to drive real prompt revision work without live generation access -- mining "what specifically was missing" text into the next prompt attempt is a better use of a credential-blocked cycle than a no-op re-arm to ready. Separately: a full yaml.safe_dump round-trip on a hand-formatted queue file rewraps every folded scalar in the whole file, not just the touched entries -- a targeted line-level edit is the safe way to make a small status change without a large unrelated reformatting diff.

- 2026-08-01 `model-builder/t-038` — A per-item "is this busy" check that already exists as a component-local computed (isManualActionInFlight in model-builder-item-panel.vue) is worth promoting into the shared store the moment a second UI surface needs the same signal, rather than re-deriving it locally in each new component. Doing so here (isItemManualActionInFlight(itemId)) let two independent trigger buttons (batch editor, progress matrix) show an identical pre-click advisory with zero logic duplication and zero risk of the two copies drifting out of sync with the runtime guard inside autoBuildItem() itself.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-01T17:43:39Z_
