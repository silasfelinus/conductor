# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-28T08:45:36Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **398**
- Outcomes: blocked: 12, cancelled: 1, done: 385
- Success rate: **97%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 51 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 12 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 5 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 16 | 100% |
| conductor | 55 | 100% |
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
| model-builder | 33 | 100% |
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
| software | 383 | 99% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 8 |
| quality | 7 |
| transient | 6 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `actionable` — 8 occurrences; look for the shared cause across its records
- failure category `quality` — 7 occurrences; look for the shared cause across its records
- failure category `transient` — 6 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-28 `animation-manager/t-015` — Small, well-scoped asset-plus-one-line-swap PRs (new icon + catalog reference + regenerated seed file) verify fast and merge clean when the implementer confirms the regenerated file came straight from the existing generator script rather than a hand edit -- worth keeping as the template for future one-off icon/asset requests.
- 2026-07-28 `model-builder/t-032` — A structural dev-time check (walk CREATE_TARGETS x the Prisma relation graph, assert linkSourceToTarget has a matching case) immediately caught a real gap (Reward -> Character) the same day it was written -- two prior gaps of this exact shape (Dream->Bot, Character->Scenario) had only ever surfaced via manual read-through across separate cycles. Where a hand-maintained mapping mirrors a second source of truth (here: Prisma relations), prefer a structural consistency check over relying on the next manual audit to catch drift.
- 2026-07-28 `ai-art-academy/t-010` — Running claim_task.py only after implementing (instead of before, per AGENTS.md step 6) turns the claim check into a post-hoc formality instead of a reservation — this session duplicated another session's identical lane-4 sync work and had to close its own kind_robots PR as superseded. Claim first, implement second, every time, even when the task looks unclaimed at a glance.
- 2026-07-28 `conductor/t-088` — A well-templated connector-only Worker PR (What changed/How I verified/Flags/Kaizen all filled in specifically) needs no manual roadmap close-out — the task-events auto-processor flipped this task to done within the same minute the merge landed.
- 2026-07-28 `coloring-book/t-031` — A local polling timeout is not proof that an asynchronous ArtJob failed. Generic consumers must rebuild an identical request identity on retry or persist and recover the original job id; otherwise a fresh randomized seed silently converts a retry into duplicate production work. Compatibility tests must also preserve the public module's monkeypatch surface when a long implementation is wrapped rather than edited in place.
- 2026-07-28 `conductor/t-087` — The "Analyze (javascript-typescript)" CodeQL check routinely runs 40+ minutes in this repo (confirmed on three separate PRs in one session) but does not gate merge -- attempting a merge once every other check is green succeeds immediately rather than needing to wait for CodeQL to finish. Don't block a merge decision on it; treat it as informational.
- 2026-07-28 `ai-art-academy/t-010` — A recurring task's continuous_improvement block can drift from its own note within a single cycle (note updated, structured block not) -- the new audit_roadmaps.py CONTINUOUS_IMPROVEMENT_NOTE_DRIFT check (t-049, same session) caught this on its first live run against this exact task, confirming the checker earns its keep immediately rather than only in theory.
- 2026-07-28 `ai-art-academy/t-049` — Validating a new audit heuristic against the live roadmap tree (not just a synthetic fixture) is a strong sanity check -- the new CONTINUOUS_IMPROVEMENT_NOTE_DRIFT rule immediately flagged the exact real-world t-010 drift it was written to catch, on the first run.
- 2026-07-28 `dream-cycle/t-007` — A ready task can be stale-done, not stale-blocked -- before assuming a long-untouched ready task needs implementation work, check whether its deliverable already landed via a side channel (here, the auto art pipeline's task-events flow beat the roadmap task to completion by over two weeks). Verifying file existence/shape first turned this into a same-cycle close instead of a duplicate art-generation request.
- 2026-07-28 `coloring-book/t-022` — Live-testing a fix against the real queue (not just unit tests) caught a second bug the first commit alone would have shipped silently -- build_entries() dropped the very field (semantic_gate_error) the new recovery logic needed to fire. Worth running --live whenever a sandbox has the token for it, even when unit coverage already looks complete.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-28T08:45:36Z_
