# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-10-24T21:22:49Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1310**
- Outcomes: blocked: 19, cancelled: 2, done: 1289
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
| crystal-street | 1 | 100% |
| cthulhuquarium | 54 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 30 | 100% |
| ecosystem-map | 5 | 100% |
| emperor-of-dust | 10 | 100% |
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
| ruler-hooked | 30 | 100% |
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
| weird-humboldt | 14 | 100% |
| zuzu-pinball | 4 | 100% |
| zuzu-shifting-lands | 4 | 100% |
| zuzu-showdown | 9 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 18 | 50% |
| software | 1292 | 99% |

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

- 2026-10-24 `weird-humboldt/t-065` — For character artwork, pair stable identity IDs with canonical destination paths, source-controlled idempotent prompts and UI fallback; distinguish GitHub queue requests from ArtJob IDs and delivered images.
- 2026-10-24 `crystal-street/t-001` — Node-side contract tests never touch the Pinia proxy, so structuredClone passed every test and only failed in the browser. Click through a game store in a real page before merge, and clone store state with JSON. Also run the real artPromptContract over authored prompts, which caught 46 format/frame violations and a "no text" house style that a negation-only check missed.
- 2026-10-23 `emperor-of-dust/t-058` — A style rule that excludes only the obvious species misses the rest of the cast. Ground the prose linter in the complete canon species vocabulary, exempt deliberate proper faction labels and literal wildlife, and keep character identity in the dialogue tied to their social roles instead.
- 2026-10-23 `ruler-hooked/t-044` — User clarified that removing ruler customization was the wrong fix. Retaining cosmetic identity exclusively as an opening ceremony preserves roleplaying while preventing a generic monarch from contaminating first-person environment art. The old implementation stayed visible because the prior branch had not merged.
- 2026-10-23 `emperor-of-dust/t-057` — A translucent shared panel token exposes dense room artwork through gameplay text; use solid theme surfaces and guard CSS backgrounds in layout tests.
- 2026-10-23 `emperor-of-dust/t-056` — Simulation tests can prove seeded runtime data while the actual introduction still uses obsolete roster copy. Couple new-run store invariants with UI onboarding text/navigation tests, and keep tablet interaction within one scroll owner rather than nested overflowing panels. Merging is not deployment.
- 2026-10-23 `cthulhuquarium/t-088` — Uniform spawn height and a single globally shared food target made a batch feeding action look and behave like one falling item. Pure deterministic scatter/nearest-target functions made the correction testable without changing the server economy.
- 2026-10-23 `cthulhuquarium/t-087` — Intro story data and art already existed; presenting it with proper cinematic hierarchy avoided inventing a second incompatible onboarding flow. Icon audit and formatting failed on first pass, then were corrected and verified green.
- 2026-10-22 `zuzu-shifting-lands/t-042` — Version dice-rule changes rather than rewriting replayed saves, and compare matched adversarial seed cohorts before calling a balance adjustment successful.
- 2026-10-23 `weird-humboldt/t-059` — For collectible endings, test whether the route story honestly reflects attempted but failed commitments, not only the ending identifier or score.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-10-24T21:22:49Z_
