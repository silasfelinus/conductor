# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-11-20T16:02:16Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1372**
- Outcomes: blocked: 19, cancelled: 2, done: 1351
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
| comet-city-academy | 1 | 100% |
| conductor | 147 | 100% |
| conductor-app | 4 | 100% |
| crystal-street | 1 | 100% |
| cthulhuquarium | 54 | 98% |
| davinci | 8 | 100% |
| dead-air | 2 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 31 | 100% |
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
| rainbow-bullet-hell-space-princess | 12 | 100% |
| rainbow-butterflies | 21 | 100% |
| ruler-hooked | 30 | 100% |
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
| software | 1352 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 53 |
| actionable | 23 |
| transient | 18 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 20% success over 10 closed tasks; aim the next kaizen task here
- kind `content` — 55% success over 20 closed tasks; aim the next kaizen task here
- failure category `quality` — 53 occurrences; look for the shared cause across its records
- failure category `actionable` — 23 occurrences; look for the shared cause across its records
- failure category `transient` — 18 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-11-20 `comet-city-academy/t-036` — A workflow run line written as a plain YAML scalar that contains a colon-space (e.g. a chore-prefixed commit message) breaks parsing of the whole workflow. Use a block scalar, and run test_workflow_schema_sanity.py before pushing workflow edits.
- 2026-11-20 `conductor/t-220` — When a filter reuses a tri-state helper, check what each state also covers. Here 'pending' also meant "zero check runs", so the filter needed a staleness escape hatch.
- 2026-11-20 `tarot-studio/t-001` — A design brief that names the data-ownership boundary (art/print state vs canonical reading identity) up front gives later implementation PRs a concrete review criterion.
- 2026-11-19 `weird-humboldt/t-077` — Review contact sheets per style before export and withdraw off-prompt renders to a known-good fallback lane; land the conductor close-out only after the implementation PR merges.
- 2026-11-18 `conductor/t-211` — When tightening a readiness rule, update the fixtures of every exception path (the owner waiver) to model the real roadmap, and rebase roadmap edits on main so task-event transitions are not reverted.
- 2026-11-17 `slime-city/t-044` — Small single-subject redo rounds with named foreground species and pushed-back secondary figures converge fast; judge redos against the task's stated reject criteria, not incidental details.
- 2026-11-17 `shifting-desks/t-051` — Preserve art evidence before enforcing a strict queue gate so failures are actionable rather than obscured.
- 2026-11-17 `shifting-desks/t-057` — Dry-run output should use actual request dimensions where the payload has them, and source/subject dimensions where a targeted edit omits them.
- 2026-11-17 `slime-city/t-053` — Moving lettering-prone scenes into bare stone settings (tunnels, cisterns, vaults) cleared persistent sign glyphs in one redo; when a second redo round lands, make the intake contract chain rounds so each redo must replace the latest rejected render, not the round-1 id.
- 2026-11-17 `slime-city/t-052` — A clean 102-render round still needs a recorded verdict file plus contract test so the curation is traceable; a 20-up contact sheet catches theme and age, but zoom sign-prone plates (booths, panels, consoles) 5-up before claiming no lettering.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-11-20T16:02:16Z_
