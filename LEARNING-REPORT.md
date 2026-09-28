# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-28T03:00:02Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1179**
- Outcomes: blocked: 19, cancelled: 2, done: 1158
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
| tzaddik-gallery | 12 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1162 | 99% |

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

- 2026-09-28 `tzaddik-gallery/t-015` — 'Give Silas a review surface' does not have to mean a live kind_robots UI/DB build -- a conductor-side script plus a small human-editable YAML ledger (scripts/tzaddik_review.py + discovery-decisions.yaml) satisfied the actual contract (approve/reject/defer/show-full-profile, wired into the session digest) in one landable pass, matching how Daily Dream's own conductor-side state is already surfaced. Also caught mid-close: t-014's own kaizen (t-027) had assumed t-015 would need a kind_robots database, which turned out to be moot once excluded_names() was re-read closely -- it already dedupes every docketed name permanently regardless of decision. Re-verify a dependent kaizen task's premise against what actually got built, not what was assumed, before letting it sit as 'ready' work for someone else to discover is unnecessary.
- 2026-09-28 `tzaddik-gallery/t-014` — DESIGN-BRIEF.md's daily discovery roster is a two-sided system (pipeline + review surface); scoping t-014 to only the conductor-side dedup/validate/render mechanism, and proving it by actually authoring a real docket rather than leaving the script unexercised, kept this a landable single-pass build instead of an oversized 'build the whole Daily-Dream-equivalent system' attempt.
- 2026-09-27 `tzaddik-gallery/t-008` — Clean first-pass build of admin approve/archive + explicit content overrides on top of schema t-003 already shipped -- confirming exact field/enum coverage before writing code (rather than assuming a migration was needed) kept this a pure application-layer PR. Following an existing precedent's shape (socialPostDraft.ts's approve/reject util split) for a new but structurally similar feature (Tzaddik's approve/archive) produced a smaller, more reviewable diff than inventing a new pattern.
- 2026-09-27 `tzaddik-gallery/t-007` — select_role.py's 'likely a zero-diff close' heuristic fired from a dependency note mentioning this task, but the note's own wording ('No karma/reaction wiring added -- out of scope') looked like real work remained. Reading the actual current code (not just the roadmap note chain) showed a later PR on the same dependency (t-005) had already closed the gap without updating t-006's note to say so. Always verify an audit-candidate flag against live code before either reimplementing blind or trusting the note at face value -- both are wrong in different directions.
- 2026-09-27 `tzaddik-gallery/t-017` — Clean first-pass build of the lg/xl composed gallery + person-review shell, scoped to exactly 2 files with 30/30 CI green (including layout-contract). A review-claim marker (REVIEWING: ...) was posted on the PR by the same session id that implemented the task, then never followed up past its own TTL -- a self-review-and-merge intent that didn't complete in-session. A later Reviewer sweep should treat a same-session-id marker past its TTL as free to act on, same as any other expired claim, rather than assuming it still means active work.
- 2026-09-27 `tzaddik-gallery/t-020` — Before building a 'multi-select tags + filtering' feature, checked the schema and API first and found the DB model (TzaddikCandidateTag/TzaddikEditorialTag) and both GET routes already returned Tags -- the actual remaining scope was UI-only (card badges, detail-sheet badges, a page-level filter), not the full-stack feature the task title implied. Also: a task description phrase like 'filtering by one or more tags' can be genuinely ambiguous (AND vs. OR semantics) -- pick a reasonable default, state the choice and the alternative explicitly in the PR's Flags-for-Reviewer section, and don't silently guess. When a task also names a surface ('review surfaces') that doesn't exist yet in the codebase, scope it out explicitly and file the gap as a kaizen/follow-on task rather than inventing a surface just to satisfy literal wording.
- 2026-09-27 `coloring-book/t-057` — The task's own predicted grep counts (1/25/21) matched the raw 'no text' substring hit count exactly, but 3 of those hits (2 in hollywood-recast, 1 in kind-robots) were inside historical NOT-ACCEPTED/recovery notes quoting the old wording in past tense, not live prompt.text fields -- rewriting them would have misrepresented what was actually tried and served no purpose since notes are never resubmitted as prompts. Checking each occurrence's YAML context (notes: list vs. prompt.text) before editing caught this; a blind find-and-replace across the matched line numbers would not have. Also surfaced a broader family of 'text'-adjacent clauses ("no readable text", "no logo or text", etc.) explicitly left out of scope since the task's own count only covered the literal two-word phrase -- filed as t-061 rather than scope-creeping into the same diff.
- 2026-09-27 `coloring-book/t-054` — A frozen fixture pinned to a live production file path is only as stable as that path's own guarantee of immutability -- color-art-jobs.yaml's production scripts move a superseded render to a rejected/ or revisions/ subdirectory rather than deleting it, so the original archived bytes usually still exist in the repo even after the canonical path is overwritten by a real accepted illustration. Finding and swapping in that archived original (same character, same historical measurements) fixes drift with zero loss of test coverage, instead of hunting for an unrelated known-bad substitute or dropping coverage entirely. Caught a SECOND live occurrence of the identical class (hwr-021) mid-fix, flagged by an independent concurrent session's roadmap note on the same task -- worth re-reading a task's own note for fresh evidence appended after a claim, not just what it said at claim time, since two unrelated production cycles hit the same drift class the same day.
- 2026-09-27 `coloring-book/t-052` — The whole-file-rewrite cost t-049 deliberately deferred (write_yaml(QUEUE_FILE, queue) dumping the entire ~3,000-line/~130KB in-memory tree on every single-entry mutation) narrows cleanly by mirroring a pattern the same file already had precedent for: replace_ledger_pair_value already text-splices one field of one ledger entry in place rather than rewriting the ledger. Generalizing that to a whole entry one nesting level deeper (books -> entries) needed only locating each level's block boundaries by its own list-item marker (0-indent '- order:' for books, 2-indent '  - ' for entries) and re-serializing just the touched entry with a fixed re-indent, rather than any structural rewrite of the read/load path. Verified beyond the unit-test round trip by running the new write function against a real scratch copy of the actual ~130KB production queue file and diffing every other book/entry and all top-level scalar keys before/after -- a synthetic fixture alone would not have caught an edge case specific to the real file's shape (e.g. a book or entry ordering quirk), and none existed here (108-entries, 3-books, all entry blocks IDed correctly).
- 2026-09-27 `conductor/t-198` — A test that calls a production CLI's main() end-to-end without mocking its network-dependent branch is only as isolated as the branch's own gating condition happens to be closed in the current process -- test_annotate_daily_dream_art_queue.py's isolation flake existed because _live_job_fetcher()'s bare `import consume_art_requests` failed silently (ImportError -> None) unless some *other* test file had already put scripts/ on sys.path, an accidental protection that full-suite collection order defeats deterministically while single-file runs never exercise. When a CLI-level test's correctness implicitly depends on an ambient secret/import/environment condition rather than an explicit mock, make that condition explicit (monkeypatch.delenv, an injected fetch_job, etc.) rather than fixing the accident that happened to mask it -- the accident (sys.path scope) is not the actual isolation boundary the test needs.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-28T03:00:02Z_
