# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-17T16:43:36Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **654**
- Outcomes: blocked: 14, cancelled: 1, done: 639
- Success rate: **98%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 64 | 98% |
| alexa-integration | 5 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 7 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 12 | 92% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 76 | 100% |
| conductor-app | 4 | 100% |
| davinci | 4 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 10 | 100% |
| interface-vision | 83 | 100% |
| kapowarr | 20 | 100% |
| kind-robots | 50 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 68 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 12 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 638 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 13 |
| actionable | 9 |
| transient | 9 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 13 occurrences; look for the shared cause across its records
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `transient` — 9 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-17 `kapowarr/t-009` — Writing regression coverage for a module that had zero tests surfaced a real production bug that manual reading alone hadn't caught: __load_downloads()'s LinkBroken except-handler referenced a dict key ('source') that doesn't exist on the row it was handling (the actual column is 'source_type') -- on a real sqlite3.Row this raises IndexError, uncaught by the surrounding except clause, silently killing the startup queue-restore loop partway through. The bug was invisible to mypy (dict/Row __getitem__ isn't statically typed) and to every prior manual code read across t-006/t-007/t-008. Lesson for future 'add tests to an untested module' tasks: write the regression test to actually exercise the exception-handling branches (not just the happy path), and verify each new test fails without its corresponding fix before committing -- a passing-on-first-try test for a bug you just 'fixed' is not proof it would have caught the original bug.
- 2026-08-17 `kapowarr/t-008` — Reusing an existing extensibility seam (get_subclasses(SearchSource), already used for GetComics) rather than inventing a parallel 'indexer type registry' the way external_clients.py has for download clients kept the diff scoped: Newznab is one shared API spec nearly every indexer implements identically, so per-indexer-instance CRUD rows (mirroring the simpler notifications.py registry, not the type-hierarchy external_clients.py one) was the right complexity match, not a rewrite. Also: a Newznab item's own title field carries no file extension (extract_filename_data needs it stripped from a Content-Disposition-recovered filename, or issue-number parsing silently corrupts) -- worth flagging for any future indexer/download-client task that recovers a title from a header rather than an API field.
- 2026-08-17 `kapowarr/t-022` — Before renaming a cosmetic torrent- id/label vocabulary to something generic, a repo-wide grep for the literal substring across every file type (not just the three files the task note named) is what confirms scope is actually complete -- it also cleanly separated the truly torrent-specific backend/implementations/torrent_clients/Transmission.py from the generic frontend UI, so nothing outside the intended 3 files needed touching.
- 2026-08-17 `kapowarr/t-007` — A prior design doc's 'confirmed by reading the template' claims are worth re-verifying, not just citing: tracing the actual settings-UI JS and API routes (not just the doc's summary) confirmed the client-type registry really was UI-driven with zero extra work needed, while the doc's separate 'update_status() needs zero changes' claim for the polling loop turned out to be wrong once the actual seeding_handling branch was read -- both a positive and negative case for the same 'verify, don't just cite' discipline in one task.
- 2026-08-17 `humboldt-scoop-cms/t-018` — A task note flagging 'this is more than a missing UI -- a permission check is written and called by nothing' was the real scope, not a footnote: shipping the CRUD UI alone would have handed out a can_request_changes grant the code still couldn't honour. Tracing the unused permission check to its actual enforcement point (change_request handling, keyed by WP user id) surfaced a real second gap -- rendering the form for a target account with no linked WP user id would have aggregated change-request history across unrelated no-account customers -- that a UI-only reading of the task would have missed entirely.
- 2026-08-17 `humboldt-scoop-cms/t-017` — For a schema-changing PR, the Reviewer's line-by-line migration audit is a real second check, not a formality -- reading class-hss-db.php's dbDelta diff directly (not just trusting the PR body's 'additive-only' claim) is what actually confirms no DROP/rewrite snuck in.
- 2026-08-17 `humboldt-scoop-cms/t-016` — A task named as a three-way unification (admin/dispatch/scooper) turned out, on actual survey, to need only a narrower slice -- two of the three surfaces were already correctly capability-gated from prior tasks. Surveying real current state before designing avoided rebuilding what already worked and kept the landed diff small and reviewable.
- 2026-08-17 `humboldt-scoop-cms/t-020` — A background survey of actual current write paths (not the task note's assumed shape) found the real address-edit flow was customer-portal-only with a duplicated, incomplete (address/city only, missing state/postal_code) safety check -- surveying before designing caught a real bug the task wouldn't otherwise have surfaced.
- 2026-08-17 `humboldt-scoop-cms/t-015` — server.ts's top-level side effects (opens a DB pool, starts listening) make it unimportable from a test -- pulling authorization logic into pure, side-effect-free modules (scopeVisits.ts) before wiring it into the entrypoint is what made 'test privilege boundaries' actually achievable rather than aspirational.
- 2026-08-17 `humboldt-scoop-cms/t-014` — docs/CANONICAL-SOURCES.md had already resolved this task's central design question (independent admin/scooper capability flags, not a mutually-exclusive enum) before implementation started -- reading a cross-repo project's own design docs first can eliminate a design decision entirely rather than re-deriving it in-session.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-17T16:43:36Z_
