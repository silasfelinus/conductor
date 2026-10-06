# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-10-06T03:53:51Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1220**
- Outcomes: blocked: 19, cancelled: 2, done: 1199
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
| kind-robots | 78 | 99% |
| kindrobots-unraid | 9 | 100% |
| kr-solitaire | 1 | 100% |
| lora-ingestion | 11 | 100% |
| mandarin-tutor | 16 | 94% |
| media-watchlist | 12 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 85 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| music-video | 1 | 100% |
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
| content | 17 | 47% |
| software | 1203 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 47 |
| actionable | 20 |
| transient | 18 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 47 occurrences; look for the shared cause across its records
- failure category `actionable` — 20 occurrences; look for the shared cause across its records
- failure category `transient` — 18 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-10-05 `kind-robots/t-130` — Multi-LoRA generation support has to extend through ArtJob retry and Resource-refresh helpers as well as initial workflow construction; stale scalar assumptions in shared retry plumbing can reject otherwise-valid stacked jobs before they ever re-enter the queue.
- 2026-10-05 `kind-robots/t-128` — Responsive navigation compaction must preserve explanatory copy; verification should pin content visibility as well as geometry.
- 2026-10-04 `animation-manager/t-026` — A provider header appearing in delivered MIME is not proof the provider honored it: verify the delivered content boundary, and keep critical action URLs recoverable outside provider-controlled tracking rewrites.
- 2026-10-03 `kind-robots/t-126` — Nested navigation needs one explicit hierarchy field shared by schema, resolver, menu rendering, route validation, destination flattening, and fallback cards; treating a submenu as a fake route leaks it back into navigation and cards.
- 2026-10-03 `kind-robots/t-125` — Navigation retirement needs one contract pass across channel metadata, page channelKey values, project placements, and route-specific verifiers; moving Markdown files alone leaves stale assertions and placement pointers.
- 2026-10-03 `kind-oracle/t-004` — New kind_robots TS files must pass noUncheckedIndexedAccess (Nuxt tsconfig) and the Prettier ratchet before the first push; check with the lockfile-pinned prettier (3.9.6), not a floating npx version.
- 2026-10-03 `butterfly-gallery/t-016` — Ambient runway motion reads more like background traffic when clips are separated by randomized quiet gaps and immediate repeats are excluded; keep cadence bounds in the stage contract when future tuning changes them.
- 2026-10-02 `conductor/t-204` — Removing a Conductor scaffold is not deletion intent for the Kind Robots Project row: the one-way projection cannot infer whether an absent roadmap is accidental deletion or a legitimate pre-scaffold project. Keep deletions explicit with exact identity tombstones, and make parity sensors distinguish archived rows from live scaffold claims.
- 2026-10-02 `kr-solitaire/t-004` — kind_robots typechecks with noUncheckedIndexedAccess, which a plain tsx run and a default tsc do not catch: the first PR passed its own tests and still failed the TypeScript check on every arr[i] access. Check new utils/ files with that flag (strict + noUncheckedIndexedAccess) before pushing.
- 2026-10-01 `music-video/t-003` — A task note saying egress is blocked was stale: docs.comfy.org, huggingface.co and raw.githubusercontent.com were all reachable, so test reachability before downgrading research to guesswork. The official workflow-template JSONs and ComfyUI's nodes_*.py source gave exact node ids, defaults and a deprecation (SaveAudioMP3 -> SaveAudioAdvanced) that docs prose and the task note both missed; read the source of truth, and mark what still needs a live run as UNVERIFIED rather than inventing numbers.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-10-06T03:53:51Z_
