# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-01T23:27:12Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **453**
- Outcomes: blocked: 13, cancelled: 1, done: 439
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
| interface-vision | 12 | 100% |
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
| software | 438 | 99% |

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

- 2026-08-01 `interface-vision/t-011` — A roadmap task note's factual claims about the codebase ("X is the most complete widget", "Y is imported by nothing") are a snapshot from planning time, not a live fact -- t-007 and t-009 both merged the same day this task's note was written, and by the time t-011 was picked up the note's premise (revive art-reactions.vue as canonical) was already stale: reaction-card.vue had already superseded it as the generic, actively-wired review panel. Read the current state of every file a note names before trusting its characterization, and when the literal instruction conflicts with what the code now shows, do the thing that closes the real gap (here: allowReviews was read by no gallery, not "no canonical panel exists") and document the deviation explicitly rather than either blindly following a stale instruction or silently reinterpreting it.

- 2026-08-01 `interface-vision/t-009` — Clean first pass (kind_robots PR #1269, all 14 CI checks green), but the task as originally scoped ("collapse three art-request pipelines into one") bundled a small, well-verified mechanical slice (repoint Project's art-replace onto the already-existing generic entity-art endpoint, delete two confirmed-dead routes, widen one component's type union) together with four genuinely separate decisions (a UX choice on Project's carousel UI, a product choice on Facet's dual art backends, a multi-entity schema migration, and a from-scratch admin UI) that each need their own PR and, in two cases, Silas's input before implementation. Investigating the actual code before implementing (rather than trusting the task note's characterization) also surfaced that one of the note's own technical claims was wrong: FacetArtImage was described as "declared-but-unused" but is live code serving a different purpose (ArtImage-to-Facet tagging, not a Facet art-history join) -- corrected in the split-out follow-up task (t-028) rather than propagated blind. Standing takeaway: a roadmap task note's own technical claims are a starting hypothesis, not verified fact, even when written carefully -- worth a quick repo-side confirmation pass before scoping work against a claim like "X is unused" or "Y already exists," especially when the note is old enough that the codebase could have moved under it.

- 2026-08-01 `interface-vision/t-006` — Clean first pass (kind_robots PR #1267), but the close-out step surfaced a real tooling gap this session had to work around by hand: claim_task.py pushed its claim commit straight to origin/main, and this session's local checkout was never re-fetched before set_task_field.py edited the roadmap to status: review -- set_task_field.py operates on whatever is in the local tree with no fetch of its own (its own docstring names this exact gotcha, conductor/t-077/davinci/t-014), so the resulting commit briefly clobbered the claim commit's owner/claimed_by/claimed_at fields on this session's branch. Caught before it reached main only because rebasing onto origin/main before opening this task's own conductor PR produced a merge conflict on the exact block claim_task.py had written -- resolved by keeping origin/main's claim metadata and folding in the intended status transition. Standing takeaway: after any claim_task.py call (or any other script documented to push straight to origin/main), fetch and fast-forward the local checkout before running set_task_field.py against the same file in the same session, not just before the final close-out push.

- 2026-08-01 `interface-vision/t-008` — A roadmap task assumed 7 differently-purposed Vue components (5 CRUD picker widgets with dashboard/row/dropdown variants, 1 taxonomy-search view, 1 content-collection list) were all "near-duplicates" of one passive browse gallery, based on line-count and surface description alone. Reading each target file's actual prop signature before writing any migration code caught the mismatch before implementation, not after -- a 5-minute grep for variant/mode props (`grep -n "variant\|GalleryVariant\|isDropdownMode"`) across the named files would let a task author flag this in the roadmap task itself instead of a Worker discovering it mid-implementation. Scope was shrunk to the one genuine match plus one confirmed-dead deletion; the remaining 6 objects moved to a new task (t-023) for honest per-object re-assessment rather than forced onto the same shell.

- 2026-08-01 `interface-vision/t-004` — CI caught a real conflict a general layout-contract sweep can't see: verifySerendipityRouteCutover.mjs hard-locks one page's exact <h1> markup as a route-cutover migration contract, unrelated to the one-header rule this task was adopting elsewhere. First push broke it, fixed in a follow-up commit. Filed t-023 (composition-lock audit) so t-017's later sweep can grep for hard-coded-markup contract tests across the remaining allow-list files up front instead of discovering them one CI failure at a time. General principle: a shrink-only CI ratchet only protects against violating ITS OWN rule -- it says nothing about whether some other, unrelated contract test depends on the exact markup being changed. Scope discipline (only fix what's asked, skip files another task/system explicitly owns) also paid off here -- deliberately left 8 of 29 files unfixed (admin routes, two "known offender" files t-017 already owns, one orphaned file, and this locked-contract file) rather than attempting a blind full sweep.

- 2026-08-01 `interface-vision/t-003b` — Flipping app.vue's shared shell from overflow-y-auto to overflow-hidden required auditing which of ~60 candidate page-level components actually needed their own scroll container vs. inherited one from an ancestor (pages/[...slug].vue's content-host for MDC routes, the shared ProjectFrontPage wrapper for conductor pages). A same-PR review catch (kr-hourly session) found the first push added scroll classes to six components that are mounted *inside* content-host, creating nested double-scroll regions -- the exact composition bug the task existed to fix. The file-by-file layout-contract verifier couldn't catch this because it has no parent/child composition awareness; grepping content/*.md for each candidate file's actual mount point before adding a scroll class (not just checking whether the file itself lacks one) would have caught it on the first pass. Fixed same-session via a follow-up commit once flagged. When a shared ancestor already owns scroll, verify a component is actually reachable outside that ancestor before adding its own overflow region -- otherwise ask "does this file's *rendering context* already scroll" before "does this file declare its own overflow."

- 2026-08-01 `interface-vision/t-010` — Clean first-pass except for one CI miss caught by the pipeline itself: a new content/*.md page needs a matching content/channels/<channel>/ <tab>.md registration or verifyChannelContent.ts fails with "references unknown tab" -- worth checking for that registration file up front whenever adding a new channelKey/tabKey pair, not just when CI catches it. Also: when a task note bundles a well-scoped bug fix with a vaguer "and show X on cards" ask that has no existing data model to support it, splitting the vague half into its own ready task (rather than guessing at scope) kept this PR small and reviewable.

- 2026-08-01 `interface-vision/t-003` — Task note prescribed a single risky change (flip app.vue's scroll ownership) with no mention of the 18-of-30 components/pages/*.vue files that would silently lose all scroll capability if flipped without per-page backfill first. Landed the safe structural half, split the audit-and-flip half into t-003b rather than attempting it blind in a sandbox with no local dev/DB to verify against -- treat "recommended fix" in a task note as a starting hypothesis to verify against the actual codebase, not a checklist to execute literally, especially for anything touching a shared ancestor every page depends on.

- 2026-08-01 `interface-vision/t-007` — Migration was audited line-by-line only after merge, not before -- caught the scope mismatch by luck (checking the migration for the audit rule) rather than by process (diffing file list against PR body before merging). Next time: pull_request_read get_files before merge_pull_request, every time, not just when the PR body itself flags a migration.

- 2026-08-01 `interface-vision/t-005` — verifyLayoutContract CI ratchet shipped inside the same PR as t-001, ahead of its declared depends_on (t-004) -- the dependency was aesthetic-neutral tooling work, not a hard blocker, so building it early was fine, but it means depends_on isn't a reliable signal for "has this actually not started yet" when a Worker judges a prerequisite doesn't really gate the dependent task's content.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-01T23:27:12Z_
