# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-16T04:28:18Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **626**
- Outcomes: blocked: 14, cancelled: 1, done: 611
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
| kapowarr | 15 | 100% |
| kind-robots | 50 | 98% |
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
| software | 610 | 99% |

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

- 2026-08-16 `kind-robots/t-065` — A task note's own paraphrase of 'same pattern as an earlier task' can be less precise than that earlier task's actual diff -- t-065's note said 'add a short dated correction note to t-046,' but t-055 (the cited precedent) had actually added a dated entry to a separate site-audit-inventory-notes.md doc specifically to avoid rewriting an already-closed task's long note. Reading the real precedent's implementation, not just its task-note summary, produced the better (and actually-intended) outcome.
- 2026-08-16 `kapowarr/t-020` — Milestone-level status: fields don't auto-derive from their tasks' individual statuses in this roadmap format -- they're independently hand-set and can silently drift stale even when every task under them is accurate. This is the third independent surfacing of the same pattern (after kind-robots/t-058 and kindrobots-unraid's noted-but-unfiled instance in the same audit), reinforcing the audit's own kaizen suggestion that validate_roadmaps.py should warn when a milestone's tasks are more advanced than its own status field.
- 2026-08-16 `kapowarr/t-019` — When a task note says 'port X, scoped down per the note,' read the note's stated scope literally rather than porting everything -- dropping conductor's own STRANDED-tier age-based judgment logic (as the task explicitly asked) kept silasfelinus/Kapowarr#11's branch_janitor.py to two simple tiers (MERGED auto-delete, FORCE explicit override) instead of over-porting complexity the target repo didn't need. A live end-to-end smoke test against a real local bare git remote (not just mocked unit tests) is what actually proved the merged/unmerged/force-delete behavior worked, matching this repo's own convention for anything that shells out to git.
- 2026-08-16 `kapowarr/t-018` — mypy passing is necessary but not sufficient -- a leftover reference to a variable no longer bound in its enclosing scope (a stale `finally: executor.shutdown(...)` left behind after refactoring the executor into a shared helper) is a pure runtime NameError that static typing doesn't catch. Only caught because live testing against a real unreachable host is a hard requirement for this class of change, not skipped as 'just a dedupe.'
- 2026-08-16 `kapowarr/t-017` — A ThreadPoolExecutor-bounded call that touches Settings()/get_db() needs its own Flask app context pushed inside the worker function (Server().app.app_context()) -- Settings.get_settings()'s @lru_cache(1) usually masks a missing context in production (whichever thread calls it first warms the cache for everyone), but a cold-cache path (fresh process, or the first call ever) hits a hard RuntimeError. Hit and fixed for send_notification() in t-012, then independently for ExternalClients.add()/update_client() here -- ExternalClients.test() itself likely has the same latent gap (kapowarr/t-018 kaizen).
- 2026-08-15 `kapowarr/t-016` — Bounding a call's *duration* (NOTIFICATION_REQUEST_TIMEOUT) and bounding its *fan-out* (how many can run at once) are separate problems needing separate fixes -- t-013/t-012 solved the former, t-016 solved the latter with a shared ThreadPoolExecutor replacing per-call Thread() spawns. Verified live with both an isolated concurrency test (peak=8 of 30 submissions) and a full DB-to-HTTP end-to-end delivery test.
- 2026-08-15 `kapowarr/t-015` — A retry/backoff bug fixed once for one caller (health.py's HEALTH_CHECK_TIMEOUT) doesn't fix itself for other callers of the same unbounded ExternalClients.test() -- the interactive Test button had the identical 90+s hang until bounded separately in Kapowarr#6; add()/update_client() still have it (kapowarr/t-017 kaizen).
- 2026-08-15 `kapowarr/t-012` — Implemented + merged silasfelinus/Kapowarr#5. Live end-to-end testing (running the actual app, not just static checks) caught two real bugs before merge: a 90+ second unbounded retry/backoff on the new Test button (same bug class health.py already fixed once in t-013 -- fixed the same way, ThreadPoolExecutor + future.result(timeout=...)); and a "Working outside of application context" crash because the bounding executor's worker thread doesn't inherit the caller's Flask app context, needed explicitly via Server().app.app_context(). Any new background-thread network call in this codebase should assume neither Session's default retry/backoff nor Flask's app context are safe to take for granted off the request/download thread.

- 2026-08-15 `kapowarr/t-013` — Designed and implemented from scratch (unlike t-002/t-003/t-004, no prior handoff doc existed) -- found three existing, already-used primitives (ComicVine.test_key(), ExternalClients.test(), RootFolder.size is None) to build the new health check on top of instead of writing new low-level detection logic. Live testing (not just unit-level checks) caught a real bug the design alone wouldn't have surfaced: aggregating multiple network checks into one endpoint that fires on every page load inherited each check's full retry/ backoff duration (90+ seconds for one unreachable client), which is fine for a one-off Settings "Test" button but not for an every-page-load health panel. Fixed with a bounded per-check timeout, and a second live test caught that `with ThreadPoolExecutor(...) as executor` still blocks on `shutdown(wait=True)` even after individual futures time out -- switching to manual `shutdown(wait=False)` was needed too. Running the actual app end-to-end, not just static checks, is what found both issues.
- 2026-08-15 `kapowarr/t-004` — Same cycle as t-002/t-003 -- applied projects/kapowarr/docs/t-004-launch-flair.md verbatim. Live smoke test against an empty library confirmed GET /api/system/launchflair returns {"title": null} and exercises the frontend's DEFAULT_FLAIR_LINES fallback path, not just the happy path.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-16T04:28:18Z_
