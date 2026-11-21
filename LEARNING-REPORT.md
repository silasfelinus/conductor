# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-11-21T04:01:02Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1380**
- Outcomes: blocked: 19, cancelled: 2, done: 1359
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
| comet-city-academy | 7 | 100% |
| conductor | 147 | 100% |
| conductor-app | 4 | 100% |
| crystal-street | 1 | 100% |
| cthulhuquarium | 54 | 98% |
| davinci | 8 | 100% |
| dead-air | 2 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 31 | 100% |
| ecosystem-map | 5 | 100% |
| emperor-of-dust | 11 | 100% |
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
| rainbow-bullet-hell-space-princess | 13 | 100% |
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
| software | 1360 | 99% |

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

- 2026-11-20 `rainbow-bullet-hell-space-princess/t-046` — Pin a hand-verified fail-closed guard with tests that stub the slow/network step and assert both the exit code and that no partial output was written.
- 2026-11-20 `emperor-of-dust/t-033` — When a tag-prompt lane misses the same literal objects twice, switch to a prose lane (Krea 2) that follows object descriptions rather than rerolling the same lane again.
- 2026-11-20 `comet-city-academy/t-042` — Move an exhaustive real-data test to a scheduled lane behind a pytest marker, and pin the split with a tiny test so it can't quietly return to every PR or vanish.
- 2026-11-20 `comet-city-academy/t-041` — A test that sweeps real repo data with the slow code path inherits that path's runtime on every CI run. Measure it before merging and budget it like a feature.
- 2026-11-20 `comet-city-academy/t-040` — Route every parse through one small helper so a loader swap is one line and tests can monkeypatch a single seam instead of yaml.safe_load globally.
- 2026-11-20 `comet-city-academy/t-039` — A text prefilter in front of a slow parser should err loose (case, quoting, YAML 1.1 booleans). A false match costs one parse; a false miss silently drops a ledger. Prove equivalence once against a full parse.
- 2026-11-20 `comet-city-academy/t-038` — A perf task with a numeric target needs before/after timings in the handoff. Removing the second parse saved nothing measurable (85s vs 88s); the cost was parsing 27 MB of art YAML during discovery, which a cheap text gate cut to ~21s (t-039).
- 2026-11-20 `comet-city-academy/t-037` — Before registering a script in session_sweep.py, time it in a libyaml-less sandbox. The 90s per-check timeout is shared headroom, and a double YAML parse of ~240 ledgers already uses ~78s of it.
- 2026-11-20 `comet-city-academy/t-036` — A workflow run line written as a plain YAML scalar that contains a colon-space (e.g. a chore-prefixed commit message) breaks parsing of the whole workflow. Use a block scalar, and run test_workflow_schema_sanity.py before pushing workflow edits.
- 2026-11-20 `conductor/t-220` — When a filter reuses a tri-state helper, check what each state also covers. Here 'pending' also meant "zero check runs", so the filter needed a staleness escape hatch.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-11-21T04:01:02Z_
