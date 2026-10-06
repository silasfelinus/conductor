# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-10-06T23:14:50Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1231**
- Outcomes: blocked: 19, cancelled: 2, done: 1210
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
| coat-dance | 9 | 11% |
| coloring-book | 47 | 100% |
| conductor | 142 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 52 | 98% |
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
| kind-oracle | 1 | 100% |
| kind-robots | 79 | 99% |
| kindrobots-unraid | 9 | 100% |
| kr-arcade | 9 | 100% |
| kr-solitaire | 1 | 100% |
| lora-ingestion | 11 | 100% |
| mandarin-tutor | 16 | 94% |
| media-watchlist | 12 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 85 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| music-video | 2 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 21 | 100% |
| ruler-hooked | 29 | 100% |
| scene-animator | 3 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 46 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 8 | 100% |
| tzaddik-gallery | 26 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 18 | 50% |
| software | 1213 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 47 |
| actionable | 20 |
| transient | 18 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 50% success over 18 closed tasks; aim the next kaizen task here
- failure category `quality` — 47 occurrences; look for the shared cause across its records
- failure category `actionable` — 20 occurrences; look for the shared cause across its records
- failure category `transient` — 18 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-10-06 `kr-arcade/t-009` — Arcade game factory cycle: write the game against the engine kit, then probe balance with a scratch tsx script that drives the game's own demoInput() pilot for a few thousand ticks; a pilot that never climbs or dies in the first wave flags a physics or curve bug before any browser test.
- 2026-10-06 `music-video/t-028` — The Worker PR handoff check requires the AGENTS.md headings (Task, What changed, How I verified, Stakes, Kaizen suggestion, Notes for reviewer) in the PR body from the first push; a free-form body fails CI. Read server route sources in the sibling kind_robots checkout for API contracts when no live token is available.
- 2026-10-06 `kr-arcade/t-008` — Claim a conductor task on main before cutting the close-out branch; a claim pushed after the branch was cut conflicts with its own close-out and blocks pull_request CI until merged in. With no database, the arcade per-browser fallback board makes the full play/initials/save loop testable.
- 2026-10-06 `kr-arcade/t-002` — In Krea 2 prompts, "android" paints the Android mascot and any marquee or panel left undescribed gets fake lettering; describe characters by look, not brand-adjacent nouns, and fill every panel with imagery.
- 2026-10-06 `kr-arcade/t-007` — Balance probes with a perfect-aim demo pilot overrate how easy a shooter is for humans, but they still expose a dead first few waves; tune the early curve until the pilot actually takes damage by wave 3.
- 2026-10-06 `kr-arcade/t-006` — Author arcade mazes as string rows and test them (symmetry, every pellet reachable, no dead ends) before writing ghost AI; a BFS demo pilot that avoids danger tiles doubles as a balance probe.
- 2026-10-06 `kr-arcade/t-010` — Krea 2 cabinet/marquee art came back lettering-free when prompts filled every surface with concrete painted imagery (rainbows, faces, starfields) instead of naming or banning text.
- 2026-10-06 `kr-arcade/t-005` — With no local MariaDB (and prisma migrate diff blocked by the secret-guard hook), kind_robots CI "Replay migrations on MariaDB" is what proves a hand-written additive migration applies.
- 2026-10-06 `kr-arcade/t-004` — Keep arcade game metadata free of canvas code and lazy-load the game modules, so the scores API can import the same registry to validate submissions and headless tests can run every game.
- 2026-10-06 `kr-arcade/t-003` — The kind_robots shell header matches tabs by exact route, so a real sub-page of a tab (e.g. /play/arcade/<game>) falls back to the Dashboard header; serve tab sub-views via a query parameter on the tab route, and keep presentation fields in kind_robots, not project-overrides.yaml.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-10-06T23:14:50Z_
