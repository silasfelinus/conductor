# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-28T06:49:14Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1183**
- Outcomes: blocked: 19, cancelled: 2, done: 1162
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
| coloring-book | 46 | 100% |
| conductor | 138 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 30 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 22 | 95% |
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
| ruler-hooked | 28 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 44 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |
| tzaddik-gallery | 16 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1166 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 46 |
| transient | 18 |
| actionable | 17 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 46 occurrences; look for the shared cause across its records
- failure category `transient` — 18 occurrences; look for the shared cause across its records
- failure category `actionable` — 17 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-28 `tzaddik-gallery/t-026` — check_pr_merged_drift.py caught a real gap: t-026's implementing PR (kind_robots#3072) merged over an hour before any session reconciled the roadmap task off status=review. Worth running the merged-PR drift check as a matter of course after any worker cycle that touches a cross-repo project, not only at session start/end, since a PR can merge mid-session on its own CI schedule without the conductor session that opened it noticing.
- 2026-09-28 `tzaddik-gallery/t-012` — select_role.py's kind_robots candidate_reviewable_pr_count reported 0 while a real, fully green, mergeable claude/* PR (kind_robots#3071) had been sitting open for ~4 hours. A direct list_pull_requests call against kind_robots found it immediately. Worth checking select_role.py's kind_robots PR-scan filter (branch prefix? PR age? author?) against this specific miss before trusting its reviewable-PR count as complete -- a manual cross-repo PR listing is cheap insurance in the meantime.
- 2026-09-28 `tzaddik-gallery/t-010` — A stale claim (t-010 sat claimed by an openai session for 5+ hours with no branch ever pushed) is safe to reclaim and complete directly once the TTL has expired -- next_ready_task.py already surfaces this correctly. Placing the new research-pool content inside discovery/ (matching the dated dockets' heading/section/tzaddik-meta format) rather than at the project root meant excluded_names() picked it up for dedup automatically, with zero code changes -- worth defaulting to 'shape new content to fit an existing scan' before reaching for a scanner-code change.
- 2026-09-28 `tzaddik-gallery/t-027` — A kaizen task's premise can be invalidated by how its own dependency actually gets built, not just by scope drift over time -- t-027 assumed t-015 would need a kind_robots-database pull for dedup state, but t-015 (#5323) made that moot in the same PR that unblocked t-027. Closing it required only re-reading excluded_names() and its own test coverage, no implementation. Worth claiming and closing a downstream kaizen immediately when its resolution is already evident, rather than leaving a 'ready' task in the queue that looks like real work but isn't.
- 2026-09-28 `tzaddik-gallery/t-015` — 'Give Silas a review surface' does not have to mean a live kind_robots UI/DB build -- a conductor-side script plus a small human-editable YAML ledger (scripts/tzaddik_review.py + discovery-decisions.yaml) satisfied the actual contract (approve/reject/defer/show-full-profile, wired into the session digest) in one landable pass, matching how Daily Dream's own conductor-side state is already surfaced. Also caught mid-close: t-014's own kaizen (t-027) had assumed t-015 would need a kind_robots database, which turned out to be moot once excluded_names() was re-read closely -- it already dedupes every docketed name permanently regardless of decision. Re-verify a dependent kaizen task's premise against what actually got built, not what was assumed, before letting it sit as 'ready' work for someone else to discover is unnecessary.
- 2026-09-28 `tzaddik-gallery/t-014` — DESIGN-BRIEF.md's daily discovery roster is a two-sided system (pipeline + review surface); scoping t-014 to only the conductor-side dedup/validate/render mechanism, and proving it by actually authoring a real docket rather than leaving the script unexercised, kept this a landable single-pass build instead of an oversized 'build the whole Daily-Dream-equivalent system' attempt.
- 2026-09-27 `tzaddik-gallery/t-008` — Clean first-pass build of admin approve/archive + explicit content overrides on top of schema t-003 already shipped -- confirming exact field/enum coverage before writing code (rather than assuming a migration was needed) kept this a pure application-layer PR. Following an existing precedent's shape (socialPostDraft.ts's approve/reject util split) for a new but structurally similar feature (Tzaddik's approve/archive) produced a smaller, more reviewable diff than inventing a new pattern.
- 2026-09-27 `tzaddik-gallery/t-007` — select_role.py's 'likely a zero-diff close' heuristic fired from a dependency note mentioning this task, but the note's own wording ('No karma/reaction wiring added -- out of scope') looked like real work remained. Reading the actual current code (not just the roadmap note chain) showed a later PR on the same dependency (t-005) had already closed the gap without updating t-006's note to say so. Always verify an audit-candidate flag against live code before either reimplementing blind or trusting the note at face value -- both are wrong in different directions.
- 2026-09-27 `tzaddik-gallery/t-017` — Clean first-pass build of the lg/xl composed gallery + person-review shell, scoped to exactly 2 files with 30/30 CI green (including layout-contract). A review-claim marker (REVIEWING: ...) was posted on the PR by the same session id that implemented the task, then never followed up past its own TTL -- a self-review-and-merge intent that didn't complete in-session. A later Reviewer sweep should treat a same-session-id marker past its TTL as free to act on, same as any other expired claim, rather than assuming it still means active work.
- 2026-09-27 `tzaddik-gallery/t-020` — Before building a 'multi-select tags + filtering' feature, checked the schema and API first and found the DB model (TzaddikCandidateTag/TzaddikEditorialTag) and both GET routes already returned Tags -- the actual remaining scope was UI-only (card badges, detail-sheet badges, a page-level filter), not the full-stack feature the task title implied. Also: a task description phrase like 'filtering by one or more tags' can be genuinely ambiguous (AND vs. OR semantics) -- pick a reasonable default, state the choice and the alternative explicitly in the PR's Flags-for-Reviewer section, and don't silently guess. When a task also names a surface ('review surfaces') that doesn't exist yet in the codebase, scope it out explicitly and file the gap as a kaizen/follow-on task rather than inventing a surface just to satisfy literal wording.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-28T06:49:14Z_
