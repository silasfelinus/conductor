# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-15T22:49:10Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **619**
- Outcomes: blocked: 14, cancelled: 1, done: 604
- Success rate: **98%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 64 | 98% |
| alexa-integration | 2 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 6 | 100% |
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
| humboldt-scoop-cms | 4 | 100% |
| interface-vision | 83 | 100% |
| kapowarr | 9 | 100% |
| kind-robots | 49 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 63 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 10 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 603 | 99% |

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

- 2026-08-15 `kapowarr/t-012` — Implemented + merged silasfelinus/Kapowarr#5. Live end-to-end testing (running the actual app, not just static checks) caught two real bugs before merge: a 90+ second unbounded retry/backoff on the new Test button (same bug class health.py already fixed once in t-013 -- fixed the same way, ThreadPoolExecutor + future.result(timeout=...)); and a "Working outside of application context" crash because the bounding executor's worker thread doesn't inherit the caller's Flask app context, needed explicitly via Server().app.app_context(). Any new background-thread network call in this codebase should assume neither Session's default retry/backoff nor Flask's app context are safe to take for granted off the request/download thread.

- 2026-08-15 `kapowarr/t-013` — Designed and implemented from scratch (unlike t-002/t-003/t-004, no prior handoff doc existed) -- found three existing, already-used primitives (ComicVine.test_key(), ExternalClients.test(), RootFolder.size is None) to build the new health check on top of instead of writing new low-level detection logic. Live testing (not just unit-level checks) caught a real bug the design alone wouldn't have surfaced: aggregating multiple network checks into one endpoint that fires on every page load inherited each check's full retry/ backoff duration (90+ seconds for one unreachable client), which is fine for a one-off Settings "Test" button but not for an every-page-load health panel. Fixed with a bounded per-check timeout, and a second live test caught that `with ThreadPoolExecutor(...) as executor` still blocks on `shutdown(wait=True)` even after individual futures time out -- switching to manual `shutdown(wait=False)` was needed too. Running the actual app end-to-end, not just static checks, is what found both issues.
- 2026-08-15 `kapowarr/t-004` — Same cycle as t-002/t-003 -- applied projects/kapowarr/docs/t-004-launch-flair.md verbatim. Live smoke test against an empty library confirmed GET /api/system/launchflair returns {"title": null} and exercises the frontend's DEFAULT_FLAIR_LINES fallback path, not just the happy path.
- 2026-08-15 `kapowarr/t-003` — Same cycle as t-002/t-004 -- applied projects/kapowarr/docs/t-003-configurable-title.md verbatim. Live smoke test confirmed the important edge case the design doc called out: app_title correctly excluded from the host/port/url_base restart-trigger tuple (no server restart on save), and the System Status page's upstream attribution/donate links render unchanged regardless of the configured title.
- 2026-08-15 `kapowarr/t-002` — This session's GitHub scope newly included silasfelinus/Kapowarr (a prior session's t-014 escalation had asked Silas to widen it) -- the fully designed handoff patch from projects/kapowarr/docs/t-002-loading-lines.md was applied verbatim, verified in a fresh venv (mypy, isort, unittest, node --check, and a live app run), and shipped as silasfelinus/Kapowarr#1 instead of producing a fourth handoff doc. A well-specified handoff written for a future differently-scoped session paid off exactly as designed once that session arrived.
- 2026-08-15 `model-builder/t-029` — Seventh t-029 cycle followed the prior cycle's suggestion to widen scope to modelBuilderFields.ts/modelBuilderRecipes.ts/relations.ts, found those genuinely race-free (pure static data and a pure read-only check), then broadened the search one hop further to the PATCH write paths that consume those files' output (prepareItemUpdate, feeding items/[id].patch.ts and items/batch.patch.ts) and found a real bug there instead: a blind wholesale stageStatuses overwrite, the same stale- snapshot class already fixed once in commit.post.ts's COMMIT-only write but never generalized to the PATCH/batch-PATCH routes. Most exploitable in the batch route, where every entry does its own DB round trip before the shared transaction starts, widening the concurrent-write window well past the single-item route's. When a suggested lead turns out clean, checking one hop downstream of it (what actually consumes that file's output) found a real bug an earlier cycle's own fix pattern had already named but not generalized -- a second instance of an already-known bug shape is still worth finding.
- 2026-08-15 `model-builder/t-029` — Sixth t-029 cycle found a bug class distinct from the five prior cycles: a server-side check-then-act race (findUnique-then-create against FacetProfile's single-column facetId PK) rather than another client-side async-fetch-ordering or unawaited-promise-before-toast instance. Two ModelBuildRuns can target the same existing Facet concurrently since nothing serializes runs by sourceId; the item-level idempotencyKey claim only prevents the same item double-committing. Fixed with facetProfile.upsert(), which resolves create-vs-update atomically at the database instead of racing on a stale client-side read. When a prior cycle explicitly names unexplored files, reading those files on their own terms (rather than pattern-matching the previous bug shape onto them) found a genuinely new, more severe bug — a whole-transaction rollback aborting a sibling write, not just a stale UI read.
- 2026-08-15 `kapowarr/t-010` — Verifying a cross-repo projection is stronger when grounded in the receiving side's actual code (dispatched a background agent to read kind_robots' server/api/conductor/sync.post.ts and conductorProjectionDb.ts) rather than just poking the public API and declaring it fine -- confirmed there's no separate Milestone/Task SQL table (roadmap YAML is stored as a blob and re-parsed per-request), which ruled out an entire class of task-level sync-lag risk. Found and fixed a real staleness bug the task note called out by name: m1/m2 milestone status was stuck at not-started despite real done/needs-human/ready tasks under both -- 'verify the projection' should mean checking the data is both present AND accurate, not just present.
- 2026-08-15 `kapowarr/t-005` — A read-only clone plus targeted grep for -arr-convention keywords (notification, webhook, health check, import_list, calendar) across the whole fork found two genuine, scoped gaps (no notification system, no health-warnings panel) while also confirming several areas the roadmap notes didn't call out as already mature (queue reorder/blocklist, per-issue search, download-client test-connection, multi-root-folder support) -- recording the negative findings in the audit doc, not just the positive ones, keeps a future audit from re-flagging already-solved territory. Deliberately declined to turn every absent feature into a task (import lists, calendar) when the friction was speculative rather than concrete, per the task's own 'convert concrete friction, not broad rewrites' instruction.
- 2026-08-15 `kapowarr/t-006` — A read-only git clone of the target repo (public HTTPS, no auth, distinct from the session's GitHub MCP scope) let a design-only task ground its spec in the actual ABC/class chain instead of the task note's abstractions -- found that TorrentDownload.update_status() already polls purely through the ExternalDownloadClient interface with zero torrent-specific logic, so a Usenet client is a peer implementation, not a new mechanism, and located the one real shared touchpoint (download_queue.py's TorrentDownload-specific isinstance dispatch) that does need to change. Worth doing before writing any cross-repo design/handoff doc: reading the real code turns a plausible design into a verified one and surfaces the one non-obvious shared edge a task note alone won't mention.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-15T22:49:10Z_
