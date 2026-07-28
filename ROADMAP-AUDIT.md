# Roadmap Audit

Generated: `2026-07-28T06:15:13.382699+00:00`

This is a conservative structural audit. It reports suspicious state; it does not automatically change task status or remove human gates.

## Portfolio snapshot

- **42** roadmaps, **23** active projects, **724** tasks
- **34 ready**, **47 waiting**, **24 needs-human**, **1 claimed/review**, **607 done**
- Findings: **0 errors**, **2 warnings**, **56 informational**

## Project inventory

| # | Project | State | Kind | Ready | Waiting | Human | In progress | Done / Total |
|---:|---|---|---|---:|---:|---:|---:|---:|
| 1 | `challenge-center` | finished | software | 0 | 0 | 0 | 0 | 20 / 20 |
| 2 | `ai-art-academy` | active | software | 1 | 1 | 2 | 0 | 45 / 49 |
| 3 | `coloring-book` | active | software | 1 | 9 | 0 | 1 | 21 / 32 |
| 4 | `humboldt-scoop` | finished | software | 0 | 0 | 0 | 0 | 8 / 8 |
| 5 | `humboldt-scoop-cms` | active | software | 0 | 0 | 1 | 0 | 11 / 12 |
| 6 | `digital-storefront` | active | software | 0 | 0 | 1 | 0 | 31 / 32 |
| 7 | `packmaker` | finished | software | 0 | 0 | 0 | 0 | 10 / 10 |
| 8 | `mermaids-of-venice` | paused | content | 0 | 0 | 8 | 0 | 4 / 12 |
| 9 | `kind-robots` | active | software | 0 | 0 | 1 | 0 | 49 / 50 |
| 10 | `kindrobots-unraid` | active | software | 0 | 7 | 1 | 0 | 4 / 12 |
| 11 | `global-ui` | finished | software | 0 | 0 | 0 | 0 | 25 / 25 |
| 12 | `mona-salai` | paused | software | 2 | 10 | 0 | 0 | 1 / 13 |
| 13 | `superkate-services-calculator` | finished | software | 0 | 0 | 0 | 0 | 37 / 37 |
| 14 | `superkate-hairstyle-ai` | paused | software | 1 | 0 | 1 | 0 | 19 / 21 |
| 15 | `newsfeed` | active | software | 0 | 0 | 0 | 0 | 22 / 22 |
| 16 | `model-builder` | active | software | 3 | 0 | 0 | 0 | 29 / 32 |
| 17 | `animation-manager` | active | software | 3 | 0 | 0 | 0 | 12 / 15 |
| 18 | `animation-studio` | retired | software | 3 | 4 | 0 | 0 | 1 / 8 |
| 19 | `ecosystem-map` | finished | software | 0 | 0 | 0 | 0 | 8 / 8 |
| 20 | `conductor` | active | software | 1 | 0 | 2 | 0 | 86 / 89 |
| 21 | `serendipity` | active | software | 1 | 0 | 0 | 0 | 11 / 12 |
| 22 | `storymaker` | active | software | 1 | 0 | 0 | 0 | 9 / 10 |
| 23 | `davinci` | finished | software | 0 | 0 | 0 | 0 | 15 / 15 |
| 24 | `art-generator-connect` | finished | software | 0 | 0 | 0 | 0 | 22 / 22 |
| 25 | `mural-design` | active | content | 1 | 3 | 0 | 0 | 3 / 7 |
| 26 | `coat-dance` | active | content | 2 | 0 | 0 | 0 | 1 / 10 |
| 27 | `career-transition` | retired | content | 0 | 4 | 3 | 0 | 1 / 8 |
| 28 | `alexa-integration` | active | software | 1 | 0 | 1 | 0 | 16 / 18 |
| 29 | `conductor-app` | active | software | 2 | 0 | 0 | 0 | 12 / 14 |
| 30 | `appmaker` | active | software | 2 | 0 | 0 | 0 | 10 / 12 |
| 31 | `media-watchlist` | active | software | 2 | 0 | 0 | 0 | 11 / 13 |
| 32 | `sketchy` | finished | software | 0 | 0 | 0 | 0 | 8 / 8 |
| 33 | `pinball-hero` | retired | content | 0 | 2 | 2 | 0 | 2 / 6 |
| 34 | `recipe-box` | retired | software | 0 | 2 | 1 | 0 | 0 / 3 |
| 35 | `brainstorm` | active | proposal | 1 | 0 | 0 | 0 | 0 / 1 |
| 36 | `wishmaster` | active | software | 1 | 0 | 0 | 0 | 2 / 3 |
| 37 | `engagement` | finished | software | 0 | 0 | 0 | 0 | 3 / 3 |
| 38 | `ruler-hooked` | active | software | 1 | 0 | 0 | 0 | 11 / 12 |
| 39 | `music-mentor` | active | software | 1 | 0 | 0 | 0 | 8 / 9 |
| 40 | `dream-cycle` | active | software | 3 | 0 | 0 | 0 | 16 / 20 |
| — | `approval-portal` | retired | software | 0 | 0 | 0 | 0 | 3 / 5 |
| — | `humboldt-impropriety-calendar` | retired | brainstorm | 0 | 5 | 0 | 0 | 0 / 6 |

## Findings by severity

### Error (0)

_None._

### Warning (2)

- **ACTIVE_PROJECT_ALL_DONE** — `newsfeed`: All tasks are done but project override remains active.
- **ACTIVE_PROJECT_NO_OPEN_TASKS** — `newsfeed`: Active project has no open tasks; mark finished/paused or add an intentional recurring task.

### Info (56)

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
- **MISSING_GOAL** — `davinci`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `davinci` / `t-002`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `digital-storefront`: Roadmap has no friendly goal/definition of done.
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
- **MISSING_GOAL** — `kind-robots`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `kind-robots` / `t-029`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `kindrobots-unraid`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `kindrobots-unraid` / `t-002`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `media-watchlist`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `mermaids-of-venice`: Roadmap has no friendly goal/definition of done.
- **INACTIVE_PROJECT_HAS_READY_TASKS** — `mona-salai`: Inactive project retains 2 ready task(s); harmless but misleading in generated status.
- **APPROVAL_WITHOUT_GATE** — `mural-design` / `t-006`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `music-mentor`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `newsfeed`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `newsfeed` / `t-002`: approved_by_human is set on a task that is not human-gated.
- **APPROVAL_WITHOUT_GATE** — `newsfeed` / `t-021`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `packmaker`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `pinball-hero`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `recipe-box`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `ruler-hooked` / `t-002`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `serendipity`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `sketchy`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `storymaker`: Roadmap has no friendly goal/definition of done.
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
