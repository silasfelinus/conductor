# Roadmap Audit

Generated: `2026-07-18T10:22:34.008369+00:00`

This is a conservative structural audit. It reports suspicious state; it does not automatically change task status or remove human gates.

## Portfolio snapshot

- **40** roadmaps, **31** active projects, **601** tasks
- **70 ready**, **55 waiting**, **28 needs-human**, **2 claimed/review**, **435 done**
- Findings: **0 errors**, **6 warnings**, **45 informational**

## Project inventory

| # | Project | State | Kind | Ready | Waiting | Human | In progress | Done / Total |
|---:|---|---|---|---:|---:|---:|---:|---:|
| 1 | `challenge-center` | finished | software | 0 | 0 | 0 | 0 | 20 / 20 |
| 2 | `ai-art-academy` | active | software | 2 | 0 | 2 | 0 | 27 / 31 |
| 3 | `coloring-book` | active | software | 1 | 9 | 0 | 0 | 19 / 29 |
| 4 | `humboldt-scoop` | active | software | 0 | 0 | 0 | 0 | 8 / 8 |
| 5 | `humboldt-scoop-cms` | active | software | 0 | 4 | 1 | 0 | 6 / 11 |
| 6 | `digital-storefront` | active | software | 1 | 2 | 3 | 1 | 16 / 23 |
| 7 | `packmaker` | active | software | 0 | 0 | 0 | 0 | 10 / 10 |
| 8 | `mermaids-of-venice` | retired | content | 0 | 0 | 8 | 0 | 4 / 12 |
| 9 | `kind-robots` | active | software | 1 | 0 | 4 | 0 | 32 / 37 |
| 10 | `kindrobots-unraid` | active | software | 0 | 7 | 1 | 0 | 4 / 12 |
| 11 | `global-ui` | active | software | 1 | 0 | 1 | 1 | 21 / 24 |
| 12 | `superkate-services-calculator` | active | software | 0 | 0 | 1 | 0 | 35 / 36 |
| 13 | `superkate-hairstyle-ai` | active | software | 2 | 0 | 2 | 0 | 16 / 20 |
| 14 | `newsfeed` | active | software | 3 | 7 | 1 | 0 | 3 / 14 |
| 15 | `model-builder` | active | software | 4 | 0 | 0 | 0 | 26 / 30 |
| 16 | `animation-manager` | active | software | 3 | 2 | 0 | 0 | 5 / 10 |
| 17 | `animation-studio` | missing | software | 3 | 4 | 0 | 0 | 1 / 8 |
| 18 | `ecosystem-map` | active | software | 2 | 1 | 0 | 0 | 5 / 8 |
| 19 | `conductor` | active | software | 5 | 0 | 3 | 0 | 57 / 65 |
| 20 | `serendipity` | active | software | 3 | 0 | 0 | 0 | 9 / 12 |
| 21 | `storymaker` | active | software | 2 | 0 | 0 | 0 | 8 / 10 |
| 22 | `davinci` | active | software | 2 | 0 | 0 | 0 | 12 / 14 |
| 23 | `art-generator-connect` | active | software | 2 | 0 | 0 | 0 | 19 / 21 |
| 24 | `mural-design` | active | content | 1 | 3 | 1 | 0 | 2 / 7 |
| 25 | `coat-dance` | active | content | 2 | 0 | 0 | 0 | 0 / 10 |
| 26 | `career-transition` | retired | content | 3 | 4 | 0 | 0 | 1 / 8 |
| 27 | `alexa-integration` | active | software | 2 | 0 | 0 | 0 | 14 / 16 |
| 28 | `conductor-app` | active | software | 6 | 0 | 0 | 0 | 7 / 13 |
| 29 | `appmaker` | active | software | 4 | 2 | 0 | 0 | 6 / 12 |
| 30 | `media-watchlist` | active | software | 1 | 0 | 0 | 0 | 6 / 7 |
| 31 | `sketchy` | active | software | 3 | 0 | 0 | 0 | 4 / 7 |
| 32 | `pinball-hero` | retired | content | 2 | 2 | 0 | 0 | 2 / 6 |
| 33 | `recipe-box` | retired | software | 1 | 2 | 0 | 0 | 0 / 3 |
| 34 | `brainstorm` | active | proposal | 1 | 0 | 0 | 0 | 0 / 1 |
| 35 | `wishmaster` | active | software | 2 | 0 | 0 | 0 | 1 / 3 |
| 36 | `engagement` | finished | software | 0 | 0 | 0 | 0 | 3 / 3 |
| 37 | `ruler-hooked` | active | software | 2 | 1 | 0 | 0 | 9 / 12 |
| 38 | `dream-cycle` | active | software | 3 | 0 | 0 | 0 | 14 / 17 |
| — | `approval-portal` | retired | software | 0 | 0 | 0 | 0 | 3 / 5 |
| — | `humboldt-impropriety-calendar` | retired | brainstorm | 0 | 5 | 0 | 0 | 0 / 6 |

## Findings by severity

### Error (0)

_None._

### Warning (6)

- **ROADMAP_MISSING_OVERRIDE** — `animation-studio`: Roadmap has no project-overrides.yaml entry.
- **ACTIVE_PROJECT_ALL_DONE** — `humboldt-scoop`: All tasks are done but project override remains active.
- **ACTIVE_PROJECT_NO_OPEN_TASKS** — `humboldt-scoop`: Active project has no open tasks; mark finished/paused or add an intentional recurring task.
- **SOFT_NEEDS_HUMAN** — `kind-robots` / `t-037`: needs-human has no obvious hard-gate marker; consider returning it to ready, setting soft_gate: true, or documenting the actual gate.
- **ACTIVE_PROJECT_ALL_DONE** — `packmaker`: All tasks are done but project override remains active.
- **ACTIVE_PROJECT_NO_OPEN_TASKS** — `packmaker`: Active project has no open tasks; mark finished/paused or add an intentional recurring task.

### Info (45)

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
