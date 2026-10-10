# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-10-10T20:22:52Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1242**
- Outcomes: blocked: 19, cancelled: 2, done: 1221
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
| kind-pinball | 1 | 100% |
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
| zuzu-shifting-lands | 2 | 100% |
| zuzu-showdown | 8 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 18 | 50% |
| software | 1224 | 99% |

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

- 2026-10-10 `zuzu-shifting-lands/t-006` — Pin runtime geography to Conductor's authored manifest; enforce deterministic reducers and finite campaign outcomes with both replay and multi-seed difficulty checks. Format new code before repository-wide ratchet checks; never treat queued CI as green.
- 2026-10-09 `zuzu-shifting-lands/t-003` — Manifest-driven games should validate design-to-runtime references and use explicit spoiler-safe player DTO allowlists. GitHub Actions workflows must declare the least GITHUB_TOKEN permissions.
- 2026-10-07 `zuzu-showdown/t-009` — For game backdrops made from diffusion art, two things go wrong quietly. First, any animal word in a scenery prompt, even "a bleached cow skull", brings the whole animal back: all three pond renders had a longhorn even though the negative prompt banned animals. Name no animal or animal part, and ban them in the negative. Second, a single median-cut palette for a whole stage spends its colours on the sky's broad gradient and drops small bright features (the pond's water, then the sun). Quantize each parallax layer with its own octree palette, and look at a preview at both camera limits before shipping.
- 2026-10-07 `zuzu-showdown/t-010` — Hold a fighting game's frame data to its art mechanically, not by eye: have the rig render each attack's striking layer alone, write that reach into the frame map, and test every hitbox against it on the frames the game actually shows while the box is live. That check found what contact sheets hid: anti-airs and Pocket Sand striking a frame before their strike pose, low kicks drawn 11-12 px off the floor, and kicks shorter than their boxes. Also: cut-out source limbs are not vertical at rest, so pose angles are relative to the drawn angle (rotating 65 degrees from a leg already 30 degrees forward lifts the foot instead of extending it), and a smear is where the blade was, so keep it out of the reach measurement.
- 2026-10-06 `zuzu-showdown/t-007` — Flux Kontext keeps a character on-model but cannot animate: from a single reference with one fixed seed it ignored 'facing right', gave six near-identical walk frames, never produced the slash pose, and swapped props (sheathed sword to bare blade, a second sword) between frames. Use Kontext for HD art and parts sheets and drive motion with a rig, or wait for a pose ControlNet; keep HD masters and derive pixel art, because pixel is a render style, not the source.
- 2026-10-07 `kind-pinball/t-017` — The current 288x416 Canvas 2D contract is the dominant quality ceiling. Preserve the Arcade shell and completed t-003 shot-map prototype, but make premium pinball a lazy-loaded WebGL/Rapier specialization rather than forcing the retro renderer to imitate a physical machine.
- 2026-10-07 `zuzu-showdown/t-014` — A status effect that starts on hit must be timed against the hitstun it rides on: Pocket Sand's 20-frame can't-block window, counted from the hit, expired exactly as the 18-frame stagger ended and did nothing. Count such windows from the end of hitstun, and write a test that tries the follow-up the effect is meant to open.
- 2026-10-07 `zuzu-showdown/t-006` — kind_robots forbids URL-only pages (verifyNoHiddenRoutes): a not-yet-public page is an Admin tab, not 'unlisted'; and run prettier last, after every edit, because the prettier ratchet fails on any newly unformatted file.
- 2026-10-07 `zuzu-showdown/t-005` — kind_robots' contract job runs an ESLint ratchet that fails on any new finding, including in test files; run `npm run test:lint-ratchet` locally (after provision_kind_robots_deps.sh) before pushing, not just tsx and tsc.
- 2026-10-07 `zuzu-showdown/t-004` — Re-seeding a fuzz test (the input change shifted the random stream) found a sim bug the old seeds missed (wall back-throw overlap); run fuzz invariants over a dozen seeds, not three.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-10-10T20:22:52Z_
