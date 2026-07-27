# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-27T02:17:01Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **374**
- Outcomes: blocked: 12, cancelled: 1, done: 361
- Success rate: **97%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 41 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 11 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 5 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 14 | 100% |
| conductor | 53 | 100% |
| conductor-app | 2 | 100% |
| davinci | 1 | 100% |
| digital-storefront | 23 | 100% |
| dream-cycle | 14 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 3 | 100% |
| kind-robots | 39 | 97% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 4 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 32 | 100% |
| mural-design | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 359 | 99% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 7 |
| quality | 6 |
| transient | 5 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `actionable` — 7 occurrences; look for the shared cause across its records
- failure category `quality` — 6 occurrences; look for the shared cause across its records
- failure category `transient` — 5 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-27 `conductor/t-086` — A stale task-event that carries a learning/note payload used to vanish silently when process_task_events.py's stale_reason() dropped it -- the only trace was a terse STALE skip line easy to miss in a run's stdout. Added a visible WARNING to stderr specifically when the dropped event has non-empty learning/note, and closed the other half of the gap in AGENTS.md: before hand-writing a task's status: done transition, check task-events/ for an already-queued completion event for the same project/task first, rather than racing it blind.

- 2026-07-26 `conductor/t-085` — Append-only coordination ledgers still need compare-and-swap behavior: compute each append from a freshly fetched main tip and retry the entire transform after non-fast-forward rejection so concurrent entries are preserved rather than overwritten.
- 2026-07-26 `conductor/t-033` — Concurrent Worker lanes need more than per-task leases: sessions must revalidate ownership before review, the cap must be checked against fresh origin/main state, and append-only shared ledgers need retry-safe compare-and-swap writes before parallel rollout.
- 2026-07-26 `conductor/t-083` — select_role.py's GitHub API calls can 403 in this sandbox (no GITHUB_TOKEN in the script's env, a config gap not a real egress block) — observed live while reviewing this very task: the script degraded to role: worker while a fully-green, reviewable claude/* PR (this task's own #1168) sat open, caught only via a manual GitHub MCP list_pull_requests double-check. Filed t-084 so the JSON output itself flags the degraded-signal case instead of only printing a stderr warning a caller may not read.
- 2026-07-26 `animation-manager/t-013` — When the same sandbox-access blocker (no local DB, no interactive browser egress) recurs across several builds, formalize a standing acceptance-bar exception in the project's own spec (one section, referenced by tag) instead of leaving each future PR to re-derive and re-explain the identical two facts.
- 2026-07-26 `ai-art-academy/t-041` — When a small useful change is trapped in a conflicted bookkeeping-heavy PR, salvage only the substantive file onto current main and perform roadmap closeout through a session-owned task event rather than resolving conflicts by carrying stale generated or ledger edits.
- 2026-07-26 `conductor/t-081` — Three separate tasks (ai-art-academy/t-004, coloring-book/t-022, newsfeed/t-022) had independently hand-written the same "recheck the shared render backlog" prose paragraph -- the identical duplication EGRESS-BLOCKERS.md already solved for sandbox egress. When a burst-mode rotation finds every priority-order ready task blocked on the same shared cause, that's a signal to build the missing shared ledger/tool instead of re-probing and re-writing the Nth near-duplicate paragraph.
- 2026-07-26 `ai-art-academy/t-040` — Group embedded regex alternations and run the real tests; new workflows should declare least-privilege token permissions from their first revision.
- 2026-07-26 `humboldt-scoop-cms/t-012` — Infra scaffolding that can't be executed in-sandbox (Docker, external data fetch) is still verifiable to a meaningful degree without live execution -- config loads under its runtime, scripts pass a syntax check, and the checked-in contract matches what the calling app code already expects. Land it as scaffolding with an explicit "verify on the real box" flag rather than blocking on infrastructure access no sandbox session will ever have.
- 2026-07-26 `digital-storefront/t-035` — When two call sites independently re-implement the same eligibility-check-then-insert sequence, extracting a shared helper immediately after the second bug fix (rather than leaving both copies as "matching patterns") is cheap while the logic is fresh and prevents the next fix from landing in only one copy again.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-27T02:17:01Z_
