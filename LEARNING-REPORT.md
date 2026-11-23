# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-11-23T03:10:46Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1398**
- Outcomes: blocked: 19, cancelled: 2, done: 1377
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
| kr-arcade | 22 | 100% |
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
| rainbow-bullet-hell-space-princess | 21 | 100% |
| rainbow-butterflies | 21 | 100% |
| ruler-hooked | 31 | 100% |
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
| software | 1378 | 99% |

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

- 2026-11-22 `ruler-hooked/t-059` — Check delivered art's real pixel format (alpha vs opaque) before building a compositor around a spec; an opaque z-stack silently shows only its top layer.
- 2026-11-22 `comet-city-academy/t-047` — Avoid leaving test doubles inside production polling and grace-period loops; share one immutable parsed corpus for repeated exhaustive QA.
- 2026-11-22 `rainbow-bullet-hell-space-princess/t-043` — A green source_margin border does not stop Kontext from cropping sprites at the right edge; 22 of 35 re-renders were still cut off.
- 2026-11-22 `rainbow-bullet-hell-space-princess/t-057` — Worker PR bodies must use the exact AGENTS.md handoff headings; free-form Summary/Validation sections fail the handoff gate even when the code is green.
- 2026-11-22 `chessweeper/t-006` — Strict indexed-access diagnostics must be checked before merging typed board-engine extractions.
- 2026-11-22 `comet-city-academy/t-043` — A scheduled audit that skips when its dependency is missing reports green while checking nothing; fail instead, and pin that with a fast unmarked test that runs in PR CI.
- 2026-11-22 `kr-arcade/t-173` — A shared test-facing type derived from actual game exports prevents newly introduced modes from breaking independent verifier declarations.
- 2026-11-21 `comet-city-academy/t-045` — Guard canon anatomy at enqueue time (before an ArtJob is spent), and grandfather only already-accepted lanes so historic receipts are never re-submitted.
- 2026-11-21 `rainbow-bullet-hell-space-princess/t-055` — When refactoring a guard into a reporting helper, compare raw values, not rounded display fields, or tiny overages slip through.
- 2026-11-22 `comet-city-academy/t-044` — Treat DONE ledger labels, authenticated image bytes, visual approvals and actual game attachments as distinct states. Private media can be safely proven with a read-only Actions workflow that logs image identifiers, dimensions and pixel checksums, but publishes no media or tokens.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-11-23T03:10:46Z_
