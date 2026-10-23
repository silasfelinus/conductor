# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-10-23T09:44:45Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1303**
- Outcomes: blocked: 19, cancelled: 2, done: 1282
- Success rate: **98%**
- Average passes on successful tasks: **0.3**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 25 | 96% |
| animation-studio | 2 | 50% |
| appmaker | 11 | 100% |
| approval-portal | 2 | 0% |
| art-archive | 34 | 100% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| butterfly-gallery | 33 | 94% |
| challenge-center | 16 | 100% |
| coat-dance | 10 | 20% |
| coloring-book | 47 | 100% |
| conductor | 142 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 53 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 30 | 100% |
| ecosystem-map | 5 | 100% |
| emperor-of-dust | 7 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 22 | 95% |
| interface-vision | 141 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 11 | 100% |
| kind-oracle | 1 | 100% |
| kind-pinball | 1 | 100% |
| kind-robots | 79 | 99% |
| kindrobots-unraid | 9 | 100% |
| kr-arcade | 21 | 100% |
| kr-solitaire | 1 | 100% |
| lora-ingestion | 11 | 100% |
| mandarin-tutor | 16 | 94% |
| media-watchlist | 12 | 100% |
| memory-dungeon | 1 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 85 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| music-video | 2 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-bullet-hell-space-princess | 12 | 100% |
| rainbow-butterflies | 21 | 100% |
| ruler-hooked | 29 | 100% |
| save-the-plumber | 1 | 100% |
| scene-animator | 3 | 100% |
| serendipity | 3 | 100% |
| shifting-desks | 5 | 100% |
| sketchy | 3 | 100% |
| storybook | 46 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 8 | 100% |
| tzaddik-gallery | 26 | 100% |
| weird-humboldt | 13 | 100% |
| zuzu-pinball | 4 | 100% |
| zuzu-shifting-lands | 4 | 100% |
| zuzu-showdown | 9 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 18 | 50% |
| software | 1285 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 52 |
| actionable | 22 |
| transient | 18 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 20% success over 10 closed tasks; aim the next kaizen task here
- kind `content` — 50% success over 18 closed tasks; aim the next kaizen task here
- failure category `quality` — 52 occurrences; look for the shared cause across its records
- failure category `actionable` — 22 occurrences; look for the shared cause across its records
- failure category `transient` — 18 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-10-23 `cthulhuquarium/t-087` — Intro story data and art already existed; presenting it with proper cinematic hierarchy avoided inventing a second incompatible onboarding flow. Icon audit and formatting failed on first pass, then were corrected and verified green.
- 2026-10-22 `zuzu-shifting-lands/t-042` — Version dice-rule changes rather than rewriting replayed saves, and compare matched adversarial seed cohorts before calling a balance adjustment successful.
- 2026-10-23 `weird-humboldt/t-059` — For collectible endings, test whether the route story honestly reflects attempted but failed commitments, not only the ending identifier or score.
- 2026-10-22 `zuzu-shifting-lands/t-041` — Show per-land outcome and encounter coverage by adversarial policy; a supposedly safe test policy can conceal an overly narrow decision heuristic.
- 2026-10-23 `weird-humboldt/t-057` — When a game advertises an origin power, test the state-consuming action, its UI availability, and save/reload, not merely the label.
- 2026-10-22 `shifting-desks/t-034` — For cross-repository story edits, change canonical and runtime prose together, validate structural invariants, merge source first, stamp the exact source merge commit in runtime, and wait for all CI shards.
- 2026-10-22 `emperor-of-dust/t-055` — A success meter cannot substitute for a conscious narrative decision when an ending defines political rule. Simulation factions must include meaningful non-host factions; otherwise a supposedly neutral test persona unintentionally chooses sides.
- 2026-10-22 `emperor-of-dust/t-054` — Seed-selected throne petition IDs cached in dayAudiences must be recalculated when a rewind changes the branch; otherwise the newly selected audience IDs are filtered out and Day 1 can deadlock. Keep seeded rewind, save-codec and all-policy 50-day simulations on the daily Emperor contract.
- 2026-10-22 `memory-dungeon/t-017` — Name a fixed overworld and verify route adjacency before procedural dungeon expansion; preserve separation between map discoveries and nested memory encounters.
- 2026-10-22 `weird-humboldt/t-031` — A four-location story pass demonstrated that a large seeded regional deck can still miss meaningful named-place beats. Check actual guaranteed draw reachability and save/scene consequences per card rather than inferring a complete playable atlas from raw script totals; keep ArtJob status separate from published asset-file presence and review.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-10-23T09:44:45Z_
