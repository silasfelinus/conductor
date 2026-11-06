# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-11-06T02:43:37Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1340**
- Outcomes: blocked: 19, cancelled: 2, done: 1319
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
| game-of-captains | 8 | 100% |
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
| memory-dungeon | 3 | 100% |
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
| slime-city | 5 | 100% |
| storybook | 46 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 8 | 100% |
| tzaddik-gallery | 26 | 100% |
| weird-humboldt | 21 | 100% |
| zuzu-pinball | 4 | 100% |
| zuzu-shifting-lands | 6 | 100% |
| zuzu-showdown | 9 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 18 | 50% |
| software | 1322 | 99% |

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

- 2026-11-05 `zuzu-shifting-lands/t-049` — A rule change that would have needed a deck schema bump (rejecting every saved run) shipped instead as a run-state marker that defaults absent for old saves, so history replays under the old rule and play continues under the new one.
- 2026-11-05 `zuzu-shifting-lands/t-036` — A 120-card line edit stayed safe across five batches because every batch proved rules byte-identical by stripping prose and comparing JSON projections plus fingerprints; the final audit's voice caps per land keep stock phrases from creeping back.
- 2026-11-04 `game-of-captains/t-036` — Measure the drain before tuning an economy; the suspected cause (alien contacts) never touched the hold, and the real leak was fixed upkeep exceeding income for a captain who spent nothing.
- 2026-11-04 `memory-dungeon/t-050` — Fifteen Memory Dungeon tasks sat in review under expired claims after their slices merged; slice PRs should return the umbrella task to ready in the same session, since review reads as nearly finished when most of the scope remains.
- 2026-11-04 `game-of-captains/t-020` — A merged implementation PR left the task sitting in review for days under a stale claim; reconcile review tasks against merged PRs in the same session the PR lands.
- 2026-11-04 `weird-humboldt/t-018` — Adversarial path batteries must drive only the choices the board actually offers (contextualOpeningChoices), and report per companion x lens rather than pooled; the pooled full-catalog test hid a declined-guide lockout for weeks.
- 2026-11-03 `slime-city/t-023` — A new game mode whose CPU never passes runs to the round clock; ship pass logic with the rules so game length is measured, not discovered after merge.
- 2026-11-02 `slime-city/t-020` — Card quantity and pack ratios can be verified in CI before any images render, but constructed-deck balance and subjective fun need full playtests.
- 2026-11-02 `slime-city/t-019` — Migrating game cadence requires auditing all narrative integration tests with hard-coded opening mana and hand sizes, plus seed-dependent win-path assertions that should instead use controlled finishing fixtures.
- 2026-11-02 `slime-city/t-018` — Faction expansions need dynamic collection-size assertions and exact-sha main reconciliation; don't let card-count tests hard-code the previous wave's population.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-11-06T02:43:37Z_
