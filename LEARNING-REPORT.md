# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-11-26T07:56:51Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1414**
- Outcomes: blocked: 19, cancelled: 2, done: 1393
- Success rate: **99%**
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
| chessweeper | 1 | 100% |
| coat-dance | 10 | 20% |
| coloring-book | 47 | 100% |
| comet-city-academy | 11 | 100% |
| conductor | 147 | 100% |
| conductor-app | 4 | 100% |
| crystal-street | 1 | 100% |
| cthulhuquarium | 54 | 98% |
| davinci | 8 | 100% |
| dead-air | 2 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 31 | 100% |
| ecosystem-map | 5 | 100% |
| emperor-of-dust | 13 | 100% |
| every-villain-tactics | 3 | 100% |
| game-of-captains | 9 | 100% |
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
| kr-arcade | 25 | 100% |
| kr-solitaire | 1 | 100% |
| lora-ingestion | 11 | 100% |
| mandarin-tutor | 16 | 94% |
| media-watchlist | 12 | 100% |
| memory-dungeon | 7 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 85 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| music-video | 2 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| playbook-kit | 2 | 100% |
| rainbow-bullet-hell-space-princess | 26 | 100% |
| rainbow-butterflies | 21 | 100% |
| ruler-hooked | 39 | 100% |
| save-the-plumber | 1 | 100% |
| scene-animator | 3 | 100% |
| serendipity | 3 | 100% |
| shifting-desks | 10 | 100% |
| sketchy | 3 | 100% |
| slime-city | 17 | 100% |
| storybook | 46 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| tarot-studio | 1 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 8 | 100% |
| tzaddik-gallery | 26 | 100% |
| weird-humboldt | 23 | 100% |
| zuzu-pinball | 4 | 100% |
| zuzu-shifting-lands | 6 | 100% |
| zuzu-showdown | 9 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 20 | 55% |
| software | 1394 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 55 |
| actionable | 23 |
| transient | 18 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 20% success over 10 closed tasks; aim the next kaizen task here
- kind `content` — 55% success over 20 closed tasks; aim the next kaizen task here
- failure category `quality` — 55 occurrences; look for the shared cause across its records
- failure category `actionable` — 23 occurrences; look for the shared cause across its records
- failure category `transient` — 18 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-11-25 `rainbow-bullet-hell-space-princess/t-011` — A broad recurring polish task whose note repeats a "still open" list can churn long after sibling tasks shipped that scope; before another micro-increment, check the list against the committed assets and pin the acceptance criterion in a test so the task can close.
- 2026-11-25 `rainbow-bullet-hell-space-princess/t-065` — To add run-to-run variety to an authored shooter without breaking seeded tests, mirror whole waves from one rng draw, and skip that draw entirely for the demo and scripted scenarios so their rng streams stay byte-identical.
- 2026-11-24 `rainbow-bullet-hell-space-princess/t-067` — When a small-resolution canvas HUD is unreadable on an upright phone, mirror its status as large DOM text in the empty space the touch layout already plans, rather than enlarging canvas type.
- 2026-11-24 `ruler-hooked/t-060` — Reconcile completed PRs against their actual scope and latest-head checks before spending another production cycle on already merged work.
- 2026-11-24 `kr-arcade/t-178` — Keep authored campaign boards deterministic and reserve end-to-end solvability/device evidence for dedicated campaign QA.
- 2026-11-24 `kr-arcade/t-180` — Keep narrative choices and ending records independently testable through the same career save.
- 2026-11-24 `kr-arcade/t-176` — Reconcile merged engine foundations promptly so dependent campaign tasks are not stranded.
- 2026-11-23 `ruler-hooked/t-031` — Long thin species (pipefish, eels) drift into multi-specimen tiled renders under the generic one-fish frame; inspect every new plate at game scale before closing a roster task.
- 2026-11-23 `ruler-hooked/t-076` — A parity test that skips in CI is not a contract; commit a snapshot fixture and keep the live checkout only as the fixture's own drift detector.
- 2026-11-23 `ruler-hooked/t-075` — Escaped literals in Python string splits ('\\n]') silently match nothing and the test still passes; assert the split delimiter was actually found.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-11-26T07:56:51Z_
