# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-11-17T01:47:08Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1362**
- Outcomes: blocked: 19, cancelled: 2, done: 1341
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
| conductor | 145 | 100% |
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
| shifting-desks | 8 | 100% |
| sketchy | 3 | 100% |
| slime-city | 14 | 100% |
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
| software | 1343 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 53 |
| actionable | 22 |
| transient | 18 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 20% success over 10 closed tasks; aim the next kaizen task here
- kind `content` — 53% success over 19 closed tasks; aim the next kaizen task here
- failure category `quality` — 53 occurrences; look for the shared cause across its records
- failure category `actionable` — 22 occurrences; look for the shared cause across its records
- failure category `transient` — 18 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-11-16 `slime-city/t-070` — A string-level diff of L2 vs L3 evolution effects narrows a 60-card continuity review to the flagged cards fast, but most hits are arc-stated role shifts; read each arc before changing rules, and check the 160-char card face when L3 keeps an extra effect.
- 2026-11-16 `dream-cycle/t-040` — Before preserving a reversible direction gate, reconcile it against Silas's standing conversation directives; a missing repository citation does not erase an explicit catalog-only clarification.
- 2026-11-15 `shifting-desks/t-056` — Running close_task review in the same minute as the claim commit can base on a pre-claim main and conflict; fetch after the claim lands before preparing the close-out.
- 2026-11-15 `shifting-desks/t-055` — Even after the t-054 lesson the next one-line PR used ad-hoc headings; validate the body locally with check_pr_handoff_template.py before opening, not after CI goes red.
- 2026-11-15 `shifting-desks/t-054` — Connector-only Workers keep opening PRs without the handoff headings; paste the check_pr_handoff_template.py headings even for one-file test PRs.
- 2026-11-15 `slime-city/t-068` — Check desktop container-query sizing against the actual side-rail width and add a live-browser bounding-box assertion after deployment; a source-level contract alone does not establish pixel geometry.
- 2026-11-15 `slime-city/t-017` — A "needs an authenticated environment" step can usually be done by any session with the sanctioned cypress-* login in docs/agents/frontend-verification.md; check that doc before deferring verification.
- 2026-11-14 `conductor/t-212` — When a review fixes one stale generated instruction, grep every roadmap for the same text and fix the generator too; the t-048 note had six siblings produced by the same importer template.
- 2026-11-14 `dead-air/t-009` — Restoring a suspended creation target requires executable writer steps, preserved durable ArtJob evidence, and explicit distinctions between authored inputs, submitted jobs and delivered film/image assets.
- 2026-11-14 `dead-air/t-008` — A green morning email can precede a late film and five cards from one PR can overstate new production; order recovery before delivery and report unique PR and generated-ArtJob evidence explicitly.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-11-17T01:47:08Z_
