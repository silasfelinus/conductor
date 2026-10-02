# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-10-02T10:28:38Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1212**
- Outcomes: blocked: 19, cancelled: 2, done: 1191
- Success rate: **98%**
- Average passes on successful tasks: **0.3**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 24 | 96% |
| animation-studio | 2 | 50% |
| appmaker | 11 | 100% |
| approval-portal | 2 | 0% |
| art-archive | 34 | 100% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| butterfly-gallery | 32 | 94% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 47 | 100% |
| conductor | 141 | 100% |
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
| kind-robots | 74 | 99% |
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
| software | 1195 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 46 |
| actionable | 20 |
| transient | 18 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 46 occurrences; look for the shared cause across its records
- failure category `actionable` — 20 occurrences; look for the shared cause across its records
- failure category `transient` — 18 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-10-02 `kr-solitaire/t-004` — kind_robots typechecks with noUncheckedIndexedAccess, which a plain tsx run and a default tsc do not catch: the first PR passed its own tests and still failed the TypeScript check on every arr[i] access. Check new utils/ files with that flag (strict + noUncheckedIndexedAccess) before pushing.
- 2026-10-01 `music-video/t-003` — A task note saying egress is blocked was stale: docs.comfy.org, huggingface.co and raw.githubusercontent.com were all reachable, so test reachability before downgrading research to guesswork. The official workflow-template JSONs and ComfyUI's nodes_*.py source gave exact node ids, defaults and a deprecation (SaveAudioMP3 -> SaveAudioAdvanced) that docs prose and the task note both missed; read the source of truth, and mark what still needs a live run as UNVERIFIED rather than inventing numbers.
- 2026-10-01 `coloring-book/t-061` — A prompt-contract fix scoped to one literal phrase leaves the whole rule family live: read the enforcing regex (negation + noun set) before grepping, so the audit counts what the gate counts.
- 2026-09-30 `cthulhuquarium/t-022` — A dry run that only reads proves nothing about the write path: the sync's dry run passed but the first write=true run 400'd because the PATCH route validated the games string as an ArtImage id. Exercise one real write before relying on an admin write path.
- 2026-09-30 `kind-robots/t-104` — A gate parked on 'needs Alexandria' cleared in one sitting once the note carried the exact two commands to paste.
- 2026-09-30 `scene-animator/t-005` — Only present a surface for acceptance after it works in production. The 2026-09-11 attempt failed on a missing mount, and the re-presentation after the fix cleared.
- 2026-09-30 `text-generation/t-009` — Closing-step acceptance gates are cheap for Silas to clear once they are presented alongside other gates rather than one at a time.
- 2026-09-30 `mandarin-tutor/t-027` — Batched visual acceptance clears fastest when the note names the exact surfaces to open.
- 2026-09-30 `storybook/t-016` — A visual gate that was sent back once cleared on the second pass once the redesign followed Silas's own written rejection point by point.
- 2026-09-30 `conductor/t-183` — A gate whose only remaining step was a hands-on diagnosis of a problem that had stopped recurring sat open for two weeks. Close on non-recurrence with a reopen trigger, rather than parking indefinitely.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-10-02T10:28:38Z_
