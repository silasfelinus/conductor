# Roadmap Audit

Generated: `2026-07-16T17:36:13.009470+00:00`

This is a conservative structural audit. It reports suspicious state; it does not automatically change task status or remove human gates.

## Portfolio snapshot

- **40** roadmaps, **32** active projects, **553** tasks
- **101 ready**, **54 waiting**, **24 needs-human**, **0 claimed/review**, **363 done**
- Findings: **0 errors**, **5 warnings**, **47 informational**

## Project inventory

| # | Project | State | Kind | Ready | Waiting | Human | In progress | Done / Total |
|---:|---|---|---|---:|---:|---:|---:|---:|
| 1 | `challenge-center` | active | software | 0 | 0 | 0 | 0 | 20 / 20 |
| 2 | `ai-art-academy` | active | software | 7 | 1 | 2 | 0 | 15 / 25 |
| 3 | `coloring-book` | active | software | 3 | 5 | 0 | 0 | 12 / 20 |
| 4 | `humboldt-scoop` | active | software | 0 | 0 | 0 | 0 | 8 / 8 |
| 5 | `humboldt-scoop-cms` | active | software | 0 | 4 | 1 | 0 | 6 / 11 |
| 6 | `digital-storefront` | active | software | 4 | 1 | 2 | 0 | 11 / 18 |
| 7 | `packmaker` | active | software | 0 | 1 | 1 | 0 | 5 / 7 |
| 8 | `mermaids-of-venice` | retired | content | 0 | 0 | 8 | 0 | 4 / 12 |
| 9 | `kind-robots` | active | software | 7 | 0 | 2 | 0 | 26 / 35 |
| 10 | `kindrobots-unraid` | active | software | 0 | 7 | 1 | 0 | 4 / 12 |
| 11 | `global-ui` | active | software | 5 | 0 | 0 | 0 | 14 / 19 |
| 12 | `superkate-services-calculator` | active | software | 0 | 0 | 1 | 0 | 35 / 36 |
| 13 | `superkate-hairstyle-ai` | active | software | 3 | 0 | 2 | 0 | 15 / 20 |
| 14 | `newsfeed` | active | software | 3 | 7 | 1 | 0 | 2 / 13 |
| 15 | `model-builder` | active | software | 4 | 0 | 0 | 0 | 25 / 29 |
| 16 | `animation-manager` | active | software | 4 | 2 | 0 | 0 | 4 / 10 |
| 17 | `ecosystem-map` | active | software | 2 | 1 | 0 | 0 | 5 / 8 |
| 18 | `conductor` | active | software | 13 | 0 | 2 | 0 | 39 / 54 |
| 19 | `serendipity` | active | software | 3 | 0 | 0 | 0 | 9 / 12 |
| 20 | `storymaker` | active | software | 2 | 0 | 0 | 0 | 8 / 10 |
| 21 | `davinci` | active | software | 2 | 0 | 0 | 0 | 12 / 14 |
| 22 | `art-generator-connect` | active | software | 2 | 0 | 0 | 0 | 19 / 21 |
| 23 | `mural-design` | active | content | 1 | 3 | 1 | 0 | 2 / 7 |
| 24 | `coat-dance` | active | content | 2 | 0 | 0 | 0 | 0 / 10 |
| 25 | `alexa-integration` | active | software | 2 | 1 | 0 | 0 | 13 / 16 |
| 26 | `conductor-app` | active | software | 6 | 0 | 0 | 0 | 7 / 13 |
| 27 | `appmaker` | active | software | 4 | 2 | 0 | 0 | 6 / 12 |
| 28 | `media-watchlist` | active | software | 1 | 0 | 0 | 0 | 5 / 6 |
| 29 | `sketchy` | active | software | 3 | 0 | 0 | 0 | 4 / 7 |
| 30 | `brainstorm` | active | proposal | 1 | 0 | 0 | 0 | 0 / 1 |
| 31 | `wishmaster` | active | software | 2 | 0 | 0 | 0 | 1 / 3 |
| 32 | `engagement` | finished | software | 0 | 0 | 0 | 0 | 3 / 3 |
| 33 | `ruler-hooked` | active | software | 4 | 0 | 0 | 0 | 7 / 11 |
| 34 | `dream-cycle` | active | software | 2 | 2 | 0 | 0 | 10 / 14 |
| — | `animation-studio` | missing | software | 3 | 4 | 0 | 0 | 1 / 8 |
| — | `approval-portal` | retired | software | 0 | 0 | 0 | 0 | 3 / 5 |
| — | `career-transition` | retired | content | 3 | 4 | 0 | 0 | 1 / 8 |
| — | `humboldt-impropriety-calendar` | retired | brainstorm | 0 | 5 | 0 | 0 | 0 / 6 |
| — | `pinball-hero` | retired | content | 2 | 2 | 0 | 0 | 2 / 6 |
| — | `recipe-box` | retired | software | 1 | 2 | 0 | 0 | 0 / 3 |

## Findings by severity

### Error (0)

_None._

### Warning (5)

- **ROADMAP_MISSING_OVERRIDE** — `animation-studio`: Roadmap has no project-overrides.yaml entry.
- **ACTIVE_PROJECT_ALL_DONE** — `challenge-center`: All tasks are done but project override remains active.
- **ACTIVE_PROJECT_NO_OPEN_TASKS** — `challenge-center`: Active project has no open tasks; mark finished/paused or add an intentional recurring task.
- **ACTIVE_PROJECT_ALL_DONE** — `humboldt-scoop`: All tasks are done but project override remains active.
- **ACTIVE_PROJECT_NO_OPEN_TASKS** — `humboldt-scoop`: Active project has no open tasks; mark finished/paused or add an intentional recurring task.

### Info (47)

- **APPROVAL_WITHOUT_GATE** — `ai-art-academy` / `t-002`: approved_by_human is set on a task that is not human-gated.
- **APPROVAL_WITHOUT_GATE** — `ai-art-academy` / `t-011`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `alexa-integration`: Roadmap has no friendly goal/definition of done.
- **INACTIVE_PROJECT_HAS_READY_TASKS** — `animation-studio`: Inactive project retains 3 ready task(s); harmless but misleading in generated status.
- **MISSING_GOAL** — `appmaker`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `approval-portal`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `art-generator-connect`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `brainstorm`: Roadmap has no friendly goal/definition of done.
- **INACTIVE_PROJECT_HAS_READY_TASKS** — `career-transition`: Inactive project retains 3 ready task(s); harmless but misleading in generated status.
- **MISSING_GOAL** — `career-transition`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `challenge-center`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `coat-dance`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `coloring-book` / `t-002`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `conductor`: Roadmap has no friendly goal/definition of done.
- **NEEDS_HUMAN_NOTE_FORMAT** — `conductor` / `t-037`: needs-human note does not use the AGENTS.md FOR SILAS action format.
- **MISSING_GOAL** — `conductor-app`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `davinci`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `davinci` / `t-002`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `digital-storefront`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `dream-cycle` / `t-002`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `ecosystem-map`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `ecosystem-map` / `t-002`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `engagement`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `global-ui`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `humboldt-impropriety-calendar`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `humboldt-scoop`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `humboldt-scoop-cms`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `kind-robots`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `kindrobots-unraid`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `kindrobots-unraid` / `t-002`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `media-watchlist`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `mermaids-of-venice`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `newsfeed`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `packmaker`: Roadmap has no friendly goal/definition of done.
- **INACTIVE_PROJECT_HAS_READY_TASKS** — `pinball-hero`: Inactive project retains 2 ready task(s); harmless but misleading in generated status.
- **MISSING_GOAL** — `pinball-hero`: Roadmap has no friendly goal/definition of done.
- **INACTIVE_PROJECT_HAS_READY_TASKS** — `recipe-box`: Inactive project retains 1 ready task(s); harmless but misleading in generated status.
- **MISSING_GOAL** — `recipe-box`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `ruler-hooked`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `ruler-hooked` / `t-002`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `serendipity`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `sketchy`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `storymaker`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `superkate-hairstyle-ai`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `superkate-services-calculator`: Roadmap has no friendly goal/definition of done.
- **NEEDS_HUMAN_NOTE_FORMAT** — `superkate-services-calculator` / `t-030`: needs-human note does not use the AGENTS.md FOR SILAS action format.
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
