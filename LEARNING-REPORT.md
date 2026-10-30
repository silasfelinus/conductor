# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-10-30T22:13:01Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1329**
- Outcomes: blocked: 19, cancelled: 2, done: 1308
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
| conductor | 143 | 100% |
| conductor-app | 4 | 100% |
| crystal-street | 1 | 100% |
| cthulhuquarium | 54 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 30 | 100% |
| ecosystem-map | 5 | 100% |
| emperor-of-dust | 10 | 100% |
| every-villain-tactics | 3 | 100% |
| game-of-captains | 6 | 100% |
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
| playbook-kit | 2 | 100% |
| rainbow-bullet-hell-space-princess | 12 | 100% |
| rainbow-butterflies | 21 | 100% |
| ruler-hooked | 30 | 100% |
| save-the-plumber | 1 | 100% |
| scene-animator | 3 | 100% |
| serendipity | 3 | 100% |
| shifting-desks | 5 | 100% |
| sketchy | 3 | 100% |
| slime-city | 1 | 100% |
| storybook | 46 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 8 | 100% |
| tzaddik-gallery | 26 | 100% |
| weird-humboldt | 20 | 100% |
| zuzu-pinball | 4 | 100% |
| zuzu-shifting-lands | 4 | 100% |
| zuzu-showdown | 9 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 18 | 50% |
| software | 1311 | 99% |

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

- 2026-10-30 `slime-city/t-001` — When the combat format is undecided, implement testable variants against shared team and card data; isolate artwork and rendered acceptance from gameplay-code completion.
- 2026-10-29 `every-villain-tactics/t-003` — Vue animations require nullable impact guards and v-if/key/class attribute ordering; narrative text verifiers must tolerate Prettier line breaks.
- 2026-10-29 `every-villain-tactics/t-002` — Test terrain height separately from pathfinding's valid alternate routes; do not discard suppression before the affected squad has acted.
- 2026-10-29 `every-villain-tactics/t-001` — Do not equate a valid Vue template with a production build; complete all CI and reconcile concurrently merged fixes from current main without force pushing.
- 2026-10-27 `game-of-captains/t-025` — A standalone sparse checkout and dedicated submit owner avoids both large repository history checkout latency and collisions with the general art sweep. Reconcile full live queue by exact prompt, recover accepted IDs, and checkpoint 200 returned IDs before asserting success; art quality and provenance must be assessed separately.
- 2026-10-27 `game-of-captains/t-022` — Preserve original three mission IDs as stable save fallbacks while adding branchable chapters. Test two full new-game paths with identical seed but different party and policies. Check odds using staffed teams because min/max clamps can hide bonuses on empty-team previews. Finish contract lint-ratchet and source formatting on the exact merge SHA.
- 2026-10-27 `game-of-captains/t-021` — Keep companion routes individually authored; one crew pair is not a captain romance. Count only solo routes toward Forge crew-romance coverage. Preserve old save identifiers and use full seeded endings and rejection tests.
- 2026-10-27 `game-of-captains/t-017` — A relationship arc is only real when recruited adults can freely opt in and out, have individually written boundaries, conditional outcomes, and persisted history independent of crew assignment and mission scores. Keep optional route logic separate from an actively claimed voyage engine and merge its latest main changes without overwriting them.
- 2026-10-27 `game-of-captains/t-003` — Ensure task-event updated timestamps postdate roadmap.updated. Crew detours must be persistent, finite, supply-safe, and tested with full seeded voyages rather than documented as prose-only.
- 2026-10-27 `game-of-captains/t-002` — Ground a cast bible in the live code IDs and preserve narrator roles. Keep full-screen illustrated selection and physical couch constraints distinct from old bridge fiction. A complete prose bible is not delivered game content. A separate CI priority-repair PR #6706 kept the story diff scoped and restored all passing source checks before merge.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-10-30T22:13:01Z_
