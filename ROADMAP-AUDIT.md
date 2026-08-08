# Roadmap Audit

Generated: `2026-08-08T22:34:46.683634+00:00`

This is a conservative structural audit. It reports suspicious state; it does not automatically change task status or remove human gates.

## Portfolio snapshot

- **45** roadmaps, **24** active + **2** continuous projects, **931** tasks
- **41 ready**, **59 waiting**, **24 needs-human**, **3 claimed/review**, **794 done**
- Findings: **0 errors**, **0 warnings**, **60 informational**

## Project inventory

| # | Project | State | Kind | Ready | Waiting | Human | In progress | Done / Total |
|---:|---|---|---|---:|---:|---:|---:|---:|
| 1 | `interface-vision` | active | software | 0 | 2 | 0 | 1 | 112 / 115 |
| 2 | `ai-art-academy` | active | software | 1 | 3 | 2 | 0 | 60 / 66 |
| 3 | `coloring-book` | active | software | 1 | 9 | 1 | 0 | 26 / 37 |
| 4 | `humboldt-scoop-cms` | active | software | 0 | 0 | 1 | 0 | 11 / 12 |
| 5 | `digital-storefront` | active | software | 0 | 3 | 1 | 2 | 35 / 41 |
| 6 | `mermaids-of-venice` | active | content | 1 | 0 | 8 | 0 | 4 / 13 |
| 7 | `kind-robots` | active | software | 1 | 0 | 0 | 0 | 54 / 55 |
| 8 | `kindrobots-unraid` | active | software | 1 | 7 | 0 | 0 | 4 / 12 |
| 9 | `model-builder` | active | software | 2 | 0 | 0 | 0 | 37 / 39 |
| 10 | `lora-ingestion` | active | infrastructure | 1 | 0 | 0 | 0 | 5 / 6 |
| 11 | `conductor` | active | software | 0 | 0 | 1 | 0 | 105 / 106 |
| 12 | `taskmaster` | active | software | 1 | 0 | 0 | 0 | 2 / 3 |
| 13 | `storybook` | active | software | 5 | 1 | 1 | 0 | 9 / 16 |
| 14 | `davinci` | active | software | 2 | 4 | 0 | 0 | 16 / 22 |
| 15 | `mural-design` | active | content | 0 | 3 | 1 | 0 | 3 / 7 |
| 16 | `coat-dance` | active | content | 2 | 0 | 0 | 0 | 1 / 10 |
| 17 | `alexa-integration` | active | software | 2 | 0 | 1 | 0 | 16 / 19 |
| 18 | `conductor-app` | active | software | 2 | 0 | 0 | 0 | 12 / 14 |
| 19 | `appmaker` | active | software | 2 | 0 | 0 | 0 | 10 / 12 |
| 20 | `media-watchlist` | active | software | 1 | 0 | 0 | 0 | 15 / 16 |
| 21 | `brainstorm` | active | proposal | 1 | 0 | 0 | 0 | 0 / 1 |
| 22 | `wishmaster` | active | software | 1 | 0 | 0 | 0 | 2 / 3 |
| 23 | `ruler-hooked` | active | software | 2 | 0 | 0 | 0 | 11 / 13 |
| 24 | `music-mentor` | active | software | 1 | 0 | 0 | 0 | 8 / 9 |
| 25 | `animation-manager` | continuous | software | 2 | 0 | 0 | 0 | 15 / 17 |
| 26 | `dream-cycle` | continuous | software | 2 | 0 | 0 | 0 | 20 / 22 |
| — | `animation-studio` | retired | software | 3 | 4 | 0 | 0 | 1 / 8 |
| — | `approval-portal` | retired | software | 0 | 0 | 0 | 0 | 3 / 5 |
| — | `art-generator-connect` | finished | software | 0 | 0 | 0 | 0 | 22 / 22 |
| — | `career-transition` | retired | content | 0 | 4 | 3 | 0 | 1 / 8 |
| — | `challenge-center` | finished | software | 0 | 0 | 0 | 0 | 20 / 20 |
| — | `ecosystem-map` | finished | software | 0 | 0 | 0 | 0 | 8 / 8 |
| — | `engagement` | finished | software | 0 | 0 | 0 | 0 | 3 / 3 |
| — | `global-ui` | finished | software | 0 | 0 | 0 | 0 | 25 / 25 |
| — | `humboldt-impropriety-calendar` | retired | brainstorm | 0 | 5 | 0 | 0 | 0 / 6 |
| — | `humboldt-scoop` | finished | software | 0 | 0 | 0 | 0 | 8 / 8 |
| — | `mona-salai` | paused | software | 2 | 10 | 0 | 0 | 1 / 13 |
| — | `newsfeed` | finished | software | 0 | 0 | 0 | 0 | 22 / 22 |
| — | `packmaker` | finished | software | 0 | 0 | 0 | 0 | 10 / 10 |
| — | `pinball-hero` | retired | content | 0 | 2 | 2 | 0 | 2 / 6 |
| — | `recipe-box` | retired | software | 0 | 2 | 1 | 0 | 0 / 3 |
| — | `serendipity` | retired | software | 1 | 0 | 0 | 0 | 11 / 12 |
| — | `sketchy` | finished | software | 0 | 0 | 0 | 0 | 8 / 8 |
| — | `superkate-hairstyle-ai` | paused | software | 1 | 0 | 1 | 0 | 19 / 21 |
| — | `superkate-services-calculator` | finished | software | 0 | 0 | 0 | 0 | 37 / 37 |

## Findings by severity

### Error (0)

_None._

### Warning (0)

_None._

### Info (60)

- **APPROVAL_WITHOUT_GATE** — `ai-art-academy` / `t-002`: approved_by_human is set on a task that is not human-gated.
- **APPROVAL_WITHOUT_GATE** — `ai-art-academy` / `t-011`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `alexa-integration`: Roadmap has no friendly goal/definition of done.
- **INACTIVE_PROJECT_HAS_READY_TASKS** — `animation-studio`: Inactive project retains 3 ready task(s); harmless but misleading in generated status.
- **MISSING_GOAL** — `appmaker`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `approval-portal`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `art-generator-connect`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `brainstorm`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `career-transition`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `challenge-center`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `coat-dance`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `coloring-book` / `t-002`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `conductor`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `conductor` / `t-026`: approved_by_human is set on a task that is not human-gated.
- **APPROVAL_WITHOUT_GATE** — `conductor` / `t-033`: approved_by_human is set on a task that is not human-gated.
- **APPROVAL_WITHOUT_GATE** — `conductor` / `t-048`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `conductor-app`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `conductor-app` / `t-014`: approved_by_human is set on a task that is not human-gated.
- **APPROVAL_WITHOUT_GATE** — `davinci` / `t-002`: approved_by_human is set on a task that is not human-gated.
- **APPROVAL_WITHOUT_GATE** — `digital-storefront` / `t-020`: approved_by_human is set on a task that is not human-gated.
- **APPROVAL_WITHOUT_GATE** — `digital-storefront` / `t-021`: approved_by_human is set on a task that is not human-gated.
- **APPROVAL_WITHOUT_GATE** — `dream-cycle` / `t-002`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `ecosystem-map`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `ecosystem-map` / `t-002`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `engagement`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `global-ui`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `global-ui` / `t-016`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `humboldt-impropriety-calendar`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `humboldt-scoop`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `humboldt-scoop-cms`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `interface-vision` / `t-016`: approved_by_human is set on a task that is not human-gated.
- **APPROVAL_WITHOUT_GATE** — `interface-vision` / `t-040`: approved_by_human is set on a task that is not human-gated.
- **APPROVAL_WITHOUT_GATE** — `interface-vision` / `t-056`: approved_by_human is set on a task that is not human-gated.
- **APPROVAL_WITHOUT_GATE** — `interface-vision` / `t-071`: approved_by_human is set on a task that is not human-gated.
- **APPROVAL_WITHOUT_GATE** — `interface-vision` / `t-074`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `kind-robots`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `kind-robots` / `t-029`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `kindrobots-unraid`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `kindrobots-unraid` / `t-002`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `media-watchlist`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `mermaids-of-venice`: Roadmap has no friendly goal/definition of done.
- **INACTIVE_PROJECT_HAS_READY_TASKS** — `mona-salai`: Inactive project retains 2 ready task(s); harmless but misleading in generated status.
- **NEEDS_HUMAN_NOTE_FORMAT** — `mural-design` / `t-002`: needs-human note does not use the AGENTS.md FOR SILAS action format.
- **APPROVAL_WITHOUT_GATE** — `mural-design` / `t-006`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `music-mentor`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `newsfeed`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `newsfeed` / `t-002`: approved_by_human is set on a task that is not human-gated.
- **APPROVAL_WITHOUT_GATE** — `newsfeed` / `t-021`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `packmaker`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `pinball-hero`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `recipe-box`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `ruler-hooked` / `t-002`: approved_by_human is set on a task that is not human-gated.
- **INACTIVE_PROJECT_HAS_READY_TASKS** — `serendipity`: Inactive project retains 1 ready task(s); harmless but misleading in generated status.
- **MISSING_GOAL** — `serendipity`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `sketchy`: Roadmap has no friendly goal/definition of done.
- **INACTIVE_PROJECT_HAS_READY_TASKS** — `superkate-hairstyle-ai`: Inactive project retains 1 ready task(s); harmless but misleading in generated status.
- **MISSING_GOAL** — `superkate-hairstyle-ai`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `superkate-hairstyle-ai` / `t-011`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `superkate-services-calculator`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `wishmaster`: Roadmap has no friendly goal/definition of done.

## Interpretation rules

- **Errors** are deterministic framework or state defects and should normally be repaired promptly.
- **Warnings** need judgment; they are candidates for roadmap cleanup, gate removal, or project-state changes.
- **Informational** findings improve consistency but should not interrupt productive Worker execution.
- A reported `POSSIBLY_UNNECESSARY_GATE` is not permission to bypass a real approval boundary. Confirm the task has no publishing, money, legal, production, secret, DNS, destructive, or security-sensitive consequence before removing the gate.

## Regeneration

```bash
python scripts/audit_roadmaps.py
```

Use `--json <path>` and `--markdown <path>` to override output locations.
