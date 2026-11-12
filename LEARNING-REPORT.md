# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-11-12T10:47:56Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1350**
- Outcomes: blocked: 19, cancelled: 2, done: 1329
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
| conductor | 144 | 100% |
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
| memory-dungeon | 6 | 100% |
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
| slime-city | 10 | 100% |
| storybook | 46 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 8 | 100% |
| tzaddik-gallery | 26 | 100% |
| weird-humboldt | 22 | 100% |
| zuzu-pinball | 4 | 100% |
| zuzu-shifting-lands | 6 | 100% |
| zuzu-showdown | 9 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 19 | 53% |
| software | 1331 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 52 |
| actionable | 22 |
| transient | 18 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 20% success over 10 closed tasks; aim the next kaizen task here
- kind `content` — 53% success over 19 closed tasks; aim the next kaizen task here
- failure category `quality` — 52 occurrences; look for the shared cause across its records
- failure category `actionable` — 22 occurrences; look for the shared cause across its records
- failure category `transient` — 18 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-11-11 `memory-dungeon/t-067` — A sweep-only guard catches a bad close-out after it merges; anchoring the "remaining:" match at line start (optionally date-prefixed) is what keeps quoted historical prose from tripping it.
- 2026-11-11 `conductor/t-209` — Match task-declaration lines in PR bodies, not any mention; the anchored match found four real stale review tasks on its first live run, all from handoff-template "### Task" lines.
- 2026-11-11 `slime-city/t-028` — A task can ship and still sit at review when its PR names the task only in the body; the drift check matches titles, so put "<project>/<task-id>" in the implementation PR title.
- 2026-11-11 `memory-dungeon/t-066` — Copying audit-ledger "remaining acceptance" into each task note (with a ledger-row link) puts the gap where claimers actually look; this time the Worker opened the PR with the handoff template, ending the three-miss streak.
- 2026-11-11 `slime-city/t-057` — When every archetype of one crew runs hot and no single card stands out, tune the crew-wide lever (here the faction power) and pick the step size that leaves the starter guard the most headroom, not the one that centres the constructed number.
- 2026-11-11 `slime-city/t-056` — Before adding a balance lever for an outlier from a one-bout-per-pairing audit, replay on several disjoint seed families; Riot's 0.41 was mostly noise, and the stable outlier turned out to be Exchange (~0.60).
- 2026-11-11 `slime-city/t-021` — When an audit finds never-played cards, A/B the CPU before patching it; forcing the heavy specials lost games, so the bug was card strength (handed to t-051), not AI valuation, and the CPU change was reverted unshipped.
- 2026-11-11 `slime-city/t-048` — Re-measure a balance task's targets before tuning; the six weak snares had already left the starters (t-051), so the fix became a general payoff (defuse VOLATILE) plus CPU valuation, confirmed by an A/B on a held-out seed set.
- 2026-11-10 `memory-dungeon/t-065` — A merged PR proves a slice exists, not task acceptance; the reset audit closed 0 of 24 tasks and wrote remaining acceptance per task instead of title-matching PRs to done.
- 2026-11-07 `weird-humboldt/t-024` — Before building a claimed task, check the target repo main; the lens journeys already existed, so a re-run of the verifiers plus a reconciliation note closed it with no duplicate code.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-11-12T10:47:56Z_
