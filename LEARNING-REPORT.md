# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-10-20T00:52:51Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1279**
- Outcomes: blocked: 19, cancelled: 2, done: 1258
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
| emperor-of-dust | 4 | 100% |
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
| shifting-desks | 2 | 100% |
| sketchy | 3 | 100% |
| storybook | 46 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 8 | 100% |
| tzaddik-gallery | 26 | 100% |
| zuzu-pinball | 4 | 100% |
| zuzu-shifting-lands | 2 | 100% |
| zuzu-showdown | 9 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 18 | 50% |
| software | 1261 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 52 |
| actionable | 22 |
| transient | 18 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 50% success over 18 closed tasks; aim the next kaizen task here
- failure category `quality` — 52 occurrences; look for the shared cause across its records
- failure category `actionable` — 22 occurrences; look for the shared cause across its records
- failure category `transient` — 18 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-10-17 `rainbow-bullet-hell-space-princess/t-009` — A finale is not one more Act. Its choice and escape happen after the boss falls, at times the Act clock cannot checkpoint, so give them their own counters and make a continue restart the escape rather than rewind the clock. Keep the crew safe while it chooses, and stop the invulnerability blink there so every pilot can see where it is flying. Have the attract demo make each choice by crew size, so one verifier plays the whole campaign to THE END for every ending. Keep YAML front matter free of bare colons in prose.
- 2026-10-17 `rainbow-bullet-hell-space-princess/t-008` — An Act is a director module plus a boss module plus one engine block, and every new Act repeats the same seams (currentAct, checkpoints, resume, snapshot, render chains), so script those edits with anchored replacements and let a full demo run per crew size prove them. Make the attract demo pick routes on purpose (odd crews one way, even the other) so the verifier flies every branch deterministically, and re-check a stacked PR after its base squash-merges - merging main with --ours is only safe when the base commit is the only change to the conflicted files.
- 2026-10-16 `rainbow-bullet-hell-space-princess/t-007` — Read a pacing target as written before measuring it - the bible said 10-15 minutes per Act excluding retries, and an early measure of both Acts together with continues looked done when it was not. Measure the clean run with a deathless pilot, keep ordinary-pilot times as a ratchet, and grow length through new encounters (guardians) as well as more waves. Every inserted section moves timeline-pinned tests; anchor them to section names, not ticks.
- 2026-10-16 `rainbow-bullet-hell-space-princess/t-005` — Co-op acceptance needs a negative proof per rule - stack pilots on one spot and assert damage never exceeds the hazards that arrived, then mutate the rule (a ram hits every overlapping pilot) to show the test bites. For simultaneous supers, assert the order-dependent tick (59 or 60) rather than a single value, and measure load on the densest authored stretch with every frame drawn, not on an empty field.
- 2026-10-16 `rainbow-bullet-hell-space-princess/t-018` — Extract a browser fixture into a shared helper before a second test needs it, and measure input latency inside the page (dispatch, then sample the engine on animation frames) - polling from the test runner added two frames of round-trip noise that would have made a 1-frame response look like a flaky 3.
- 2026-10-16 `rainbow-bullet-hell-space-princess/t-015` — To prove a Nuxt component in a real browser without the app, compile the SFCs with esbuild and stub only the stores - but set each component's __scopeId (compileScript does not) and add the site's border-box reset, or the fixture fails on layout the real site never has. Driving the real cabinet surfaced a product gap (no gamepad pause mid-run) that engine-only tests could not.
- 2026-10-16 `rainbow-bullet-hell-space-princess/t-021` — Stage eligibility edge cases through play instead of state edits - a seat that rams craft until its last hit lands in the target lane leaves a wreck exactly where the check needs it, and the cabinet's own setPlayers benches a seat mid-run; then observe the outcome through what render() draws, mutate the eligibility rule to prove the test bites, and keep avoid-paths from crossing the lane they avoid.
- 2026-10-16 `rainbow-bullet-hell-space-princess/t-019` — Prove a telegraph through the consumer, not the helper - drive ordinary-input crews to the boss (continues make that reachable without demo immortality), record what render() actually strokes each frame, and assert the drawn cue against every volley; mutate the window and the post-crossing delay to show the test bites, and render at phone width because a pulsing alpha can dip below readable.
- 2026-10-13 `kr-arcade/t-065` — Separate purchase ceilings from earned gameplay and bounded save domains; exercise actual score awards, checkpoint serialization and public Continue at boundary counts, including loss and re-earn, and verify exact-head completed CI before closure.
- 2026-10-14 `rainbow-bullet-hell-space-princess/t-020` — Bake off checkpoints on the hardest real subjects before a flood, and keep palette words out of a lane-wide suffix because they recolour every outfit; txt2img plateaus on multi-element scenes, so stage planes and cutscenes need reference-driven Kontext or layout-guided passes rather than more rerolls.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-10-20T00:52:51Z_
