# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-19T23:31:30Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1079**
- Outcomes: blocked: 18, cancelled: 2, done: 1059
- Success rate: **98%**
- Average passes on successful tasks: **0.2**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 14 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 11 | 100% |
| approval-portal | 2 | 0% |
| art-archive | 32 | 100% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| butterfly-gallery | 29 | 93% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 39 | 100% |
| conductor | 121 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 24 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 137 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 10 | 100% |
| kind-robots | 67 | 99% |
| kindrobots-unraid | 9 | 100% |
| lora-ingestion | 3 | 100% |
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
| ruler-hooked | 14 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 30 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1062 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 38 |
| transient | 17 |
| actionable | 17 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 38 occurrences; look for the shared cause across its records
- failure category `transient` — 17 occurrences; look for the shared cause across its records
- failure category `actionable` — 17 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-19 `kind-robots/t-113` — First pass, tiny scoped diff (+32/-0, one file, kind_robots#2903). Cross-repo pickup from a conductor session worked cleanly end-to-end: claim on conductor, implement+verify in the kind_robots checkout, review transition, merge, close. Verified the new expectOrder() assertion actually catches a regression (manually reordered the source, confirmed the failure message, reverted) rather than trusting that adding an assertion alone proves it works.
- 2026-09-19 `conductor/t-178` — Closed as a duplicate of t-179: both tasks asked for the same pm2 restart_time trend-alerting fix, filed the same day from the same comfyui crash-loop incident chain. Two sessions independently filed kaizen/incident-response tasks for the same underlying gap without cross-checking existing ready tasks first -- worth a quick grep of the target project's roadmap for matching titles/notes before filing a new task from an incident, not just from PR history.
- 2026-09-19 `interface-vision/t-105` — Recurring polish cycle (Achievements surface): the PR backed its screenshot-directed layout claims with source-level contract assertions (flow order, container-query breakpoints, leaderboard cell placement) rather than relying on the visual description alone -- worth holding as the bar for future screenshot-directed t-105 slices, since a contract test catches a future regression a screenshot never will.
- 2026-09-19 `kind-robots/t-112` — First pass, tiny scoped diff (+4/-4, one file), matched exactly what the PR described when diffed against the stated base. Reordering a fallback chain to prefer an explicit DOM identity contract over legacy private-Vue introspection is the kind of change worth a source-contract test pinning the order, not just relying on behavioral test coverage -- filed as kind-robots/t-113.
- 2026-09-19 `lora-ingestion/t-009` — Pass 1 (conductor PR #4737) had 3 real Python test failures from an unfinished lora-import->model-import/checkpoints-path rename plus a handoff-template violation; pass 2 (kind_robots#2894) additionally collapsed the Civitai base-model dropdown from an exhaustive version list into 14 supported/other families per Silas's explicit feedback ('I don't need 10 different versions of SD') -- future UI filters over an upstream enum should model the family a user picks, not the transport values, from the start.
- 2026-09-19 `mandarin-tutor/t-025` — An optional feature Silas did not select should close as a no-op rather than remain waiting on a dependency that will eventually satisfy and trigger WAITING_WITH_SATISFIED_DEPS.
- 2026-09-19 `mandarin-tutor/t-026` — t-022's buildMandarinLesson() already computed a teachability: 'structural'|'vocabulary' field, which made the coverage-gap audit almost free -- the real design decision was keeping vocabulary-only lessons out of the issues/byCode tally entirely (a separate coverage section) so an honest, source-faithful lesson is never mistaken for a bug or fails --strict.
- 2026-09-19 `mandarin-tutor/t-024` — kind_robots#2891 merged (all 49 checks green) but the roadmap task sat at status: review on main -- state reconciliation caught it via a direct PR read (state showing merged/closed) rather than trusting the roadmap's own claimed_by/status snapshot. Session-start sweeps should verify a review-status task's actual PR state, not just its roadmap fields, when select_role.py's own GitHub reachability is degraded.
- 2026-09-19 `art-archive/t-037` — Three independent inline aggregations of the same matchArchiveResources() output (CLI, admin import endpoint, admin dry-run endpoint) had already drifted in shape (confidenceCounts only tracked by one of the three) before any bug appeared -- extracting the aggregation into one pure helper the moment a second caller duplicates it is cheaper than waiting for a third to also duplicate it and only then noticing the drift.
- 2026-09-19 `art-archive/t-038` — Once a field is durably tagged on a payload and surfaced by its read endpoint (t-034), wiring it into a display badge is a one-line template change -- the bulk of the work was already done by the field's original plumbing, not the UI surface.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-19T23:31:30Z_
