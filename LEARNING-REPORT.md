# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-28T03:08:52Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **393**
- Outcomes: blocked: 12, cancelled: 1, done: 380
- Success rate: **97%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 50 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 11 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 5 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 15 | 100% |
| conductor | 54 | 100% |
| conductor-app | 2 | 100% |
| davinci | 1 | 100% |
| digital-storefront | 24 | 100% |
| dream-cycle | 16 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| kind-robots | 39 | 97% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 6 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 32 | 100% |
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

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 378 | 99% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 8 |
| quality | 7 |
| transient | 5 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `actionable` — 8 occurrences; look for the shared cause across its records
- failure category `quality` — 7 occurrences; look for the shared cause across its records
- failure category `transient` — 5 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-28 `conductor/t-087` — The "Analyze (javascript-typescript)" CodeQL check routinely runs 40+ minutes in this repo (confirmed on three separate PRs in one session) but does not gate merge -- attempting a merge once every other check is green succeeds immediately rather than needing to wait for CodeQL to finish. Don't block a merge decision on it; treat it as informational.
- 2026-07-28 `ai-art-academy/t-010` — A recurring task's continuous_improvement block can drift from its own note within a single cycle (note updated, structured block not) -- the new audit_roadmaps.py CONTINUOUS_IMPROVEMENT_NOTE_DRIFT check (t-049, same session) caught this on its first live run against this exact task, confirming the checker earns its keep immediately rather than only in theory.
- 2026-07-28 `ai-art-academy/t-049` — Validating a new audit heuristic against the live roadmap tree (not just a synthetic fixture) is a strong sanity check -- the new CONTINUOUS_IMPROVEMENT_NOTE_DRIFT rule immediately flagged the exact real-world t-010 drift it was written to catch, on the first run.
- 2026-07-28 `dream-cycle/t-007` — A ready task can be stale-done, not stale-blocked -- before assuming a long-untouched ready task needs implementation work, check whether its deliverable already landed via a side channel (here, the auto art pipeline's task-events flow beat the roadmap task to completion by over two weeks). Verifying file existence/shape first turned this into a same-cycle close instead of a duplicate art-generation request.
- 2026-07-28 `coloring-book/t-022` — Live-testing a fix against the real queue (not just unit tests) caught a second bug the first commit alone would have shipped silently -- build_entries() dropped the very field (semantic_gate_error) the new recovery logic needed to fire. Worth running --live whenever a sandbox has the token for it, even when unit coverage already looks complete.
- 2026-07-27 `ai-art-academy/t-047` — A kaizen task naming the exact fix (which consumers, which store method) still needs an investigation pass before editing -- checking whether the target genuinely never needs to survive a component's unmount (in-flight uploads, other readers) turned a plausible-looking one-liner into a verified-safe change across all 7 call sites in one pass.
- 2026-07-27 `media-watchlist/t-012` — Third cycle in a row on watchlist-browse.vue finding server-computed/validated data (month/season filters this time) that the UI never surfaced -- worth a full BROWSE-UX.md vs. UI audit rather than one gap per cycle.
- 2026-07-27 `digital-storefront/t-023` — A hard needs-human gate does not have to sit idle waiting for a scheduled Reviewer sweep -- Silas merged kind_robots PR #1056 directly within ~30 minutes of it opening. Treat a direct merge by the repo owner as the explicit clearance event itself (confirm via merged_by on the PR, not just merged: true, since an agent must never self-grant approved_by_human) rather than waiting for a separate roadmap-editing round from Silas -- close the loop (approved_by_human: true, status: done) in the same session once that signal is confirmed.
- 2026-07-27 `ai-art-academy/t-046` — A rearm-to-ready transition is not automatically symmetric with every other ready transition in the same processor -- the rearm branch of compute_transition_ops had cleared owner but not claimed_by/claimed_at, letting stale claim metadata survive an entire cycle. When adding a new status-transition branch to a shared state-machine function, diff its field clears against the other branches for the same target status rather than assuming symmetry; the regression test should assert clearance, not just the status value.
- 2026-07-27 `media-watchlist/t-006` — Third cycle in a row on this recurring polish task (2026-07-20, 2026-07-26, 2026-07-27) that found real server-side data already computed/accepted (CSV export filters, then Year+comics+TV-season stats) sitting unused because the front end never caught up. When touching a "polish the front end" task on a project whose backend predates the UI work, diff the API response/query-param shape against what the component actually renders/sends before assuming new backend scope is needed -- the gap is often pure wiring, which keeps the diff small and the pass clean.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-28T03:08:52Z_
