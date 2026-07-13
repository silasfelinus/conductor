# Roadmap Audit

Generated: `2026-07-13T09:34:12.209450+00:00`

This is a conservative structural audit. It reports suspicious state; it does not automatically change task status or remove human gates.

## Portfolio snapshot

- **37** roadmaps, **31** active projects, **446** tasks
- **99 ready**, **57 waiting**, **15 needs-human**, **2 claimed/review**, **262 done**
- Findings: **0 errors**, **15 warnings**, **44 informational**

## Project inventory

| # | Project | State | Kind | Ready | Waiting | Human | In progress | Done / Total |
|---:|---|---|---|---:|---:|---:|---:|---:|
| 1 | `superkate-services-calculator` | active | software | 0 | 0 | 1 | 0 | 35 / 36 |
| 2 | `challenge-center` | active | software | 5 | 5 | 0 | 1 | 7 / 18 |
| 3 | `ai-art-academy` | active | software | 5 | 0 | 0 | 0 | 7 / 12 |
| 4 | `coloring-book` | active | software | 4 | 5 | 0 | 0 | 10 / 19 |
| 5 | `humboldt-scoop` | active | software | 1 | 0 | 0 | 0 | 7 / 8 |
| 6 | `humboldt-scoop-cms` | active | software | 2 | 4 | 0 | 0 | 5 / 11 |
| 7 | `digital-storefront` | active | software | 3 | 7 | 0 | 0 | 5 / 15 |
| 8 | `packmaker` | active | software | 2 | 3 | 0 | 0 | 1 / 6 |
| 9 | `mermaids-of-venice` | active | content | 2 | 0 | 8 | 0 | 2 / 12 |
| 10 | `kind-robots` | active | software | 3 | 0 | 1 | 0 | 9 / 13 |
| 11 | `global-ui` | active | software | 2 | 0 | 0 | 0 | 11 / 13 |
| 12 | `newsfeed` | active | software | 2 | 9 | 1 | 0 | 0 / 12 |
| 13 | `model-builder` | active | software | 5 | 0 | 0 | 0 | 24 / 29 |
| 14 | `approval-portal` | retired | software | 0 | 0 | 0 | 0 | 3 / 5 |
| 15 | `superkate-hairstyle-ai` | active | software | 1 | 0 | 2 | 0 | 14 / 17 |
| 16 | `ecosystem-map` | active | software | 4 | 1 | 0 | 0 | 3 / 8 |
| 17 | `conductor` | active | software | 8 | 0 | 1 | 0 | 26 / 35 |
| 18 | `serendipity` | active | software | 3 | 0 | 0 | 0 | 9 / 12 |
| 19 | `storymaker` | active | software | 2 | 0 | 0 | 0 | 8 / 10 |
| 20 | `davinci` | active | software | 2 | 0 | 0 | 0 | 12 / 14 |
| 21 | `art-generator-connect` | active | software | 1 | 0 | 0 | 1 | 19 / 21 |
| 22 | `mural-design` | active | content | 1 | 3 | 1 | 0 | 2 / 7 |
| 23 | `coat-dance` | active | content | 2 | 0 | 0 | 0 | 0 / 10 |
| 24 | `alexa-integration` | active | software | 4 | 1 | 0 | 0 | 10 / 15 |
| 25 | `conductor-app` | active | software | 6 | 0 | 0 | 0 | 7 / 13 |
| 26 | `appmaker` | active | software | 4 | 2 | 0 | 0 | 6 / 12 |
| 27 | `media-watchlist` | active | software | 1 | 0 | 0 | 0 | 5 / 6 |
| 28 | `sketchy` | active | software | 3 | 0 | 0 | 0 | 4 / 7 |
| 29 | `brainstorm` | active | proposal | 1 | 0 | 0 | 0 | 0 / 1 |
| 30 | `wishmaster` | active | software | 2 | 0 | 0 | 0 | 1 / 3 |
| 31 | `engagement` | active | software | 0 | 0 | 0 | 0 | 3 / 3 |
| 32 | `ruler-hooked` | missing | software | 7 | 1 | 0 | 0 | 2 / 10 |
| 33 | `dream-cycle` | active | software | 5 | 3 | 0 | 0 | 2 / 10 |
| — | `career-transition` | retired | content | 3 | 4 | 0 | 0 | 1 / 8 |
| — | `humboldt-impropriety-calendar` | retired | brainstorm | 0 | 5 | 0 | 0 | 0 / 6 |
| — | `pinball-hero` | retired | content | 2 | 2 | 0 | 0 | 2 / 6 |
| — | `recipe-box` | retired | software | 1 | 2 | 0 | 0 | 0 / 3 |

## Findings by severity

### Error (0)

_None._

### Warning (15)

- **POSSIBLY_UNNECESSARY_GATE** — `art-generator-connect` / `t-001`: Reversible software task is human-gated without an obvious hard-gate reason in its note.
- **POSSIBLY_UNNECESSARY_GATE** — `art-generator-connect` / `t-009`: Reversible software task is human-gated without an obvious hard-gate reason in its note.
- **STALE_IN_PROGRESS** — `art-generator-connect` / `t-019`: Task has remained claimed for 6 days.
- **SOFT_NEEDS_HUMAN** — `conductor` / `t-026`: needs-human has no obvious hard-gate marker; consider returning it to ready or documenting the actual gate.
- **POSSIBLY_UNNECESSARY_GATE** — `digital-storefront` / `t-001`: Reversible software task is human-gated without an obvious hard-gate reason in its note.
- **POSSIBLY_UNNECESSARY_GATE** — `digital-storefront` / `t-002`: Reversible software task is human-gated without an obvious hard-gate reason in its note.
- **POSSIBLY_UNNECESSARY_GATE** — `digital-storefront` / `t-010`: Reversible software task is human-gated without an obvious hard-gate reason in its note.
- **ACTIVE_PROJECT_ALL_DONE** — `engagement`: All tasks are done but project override remains active.
- **ACTIVE_PROJECT_NO_OPEN_TASKS** — `engagement`: Active project has no open tasks; mark finished/paused or add an intentional recurring task.
- **POSSIBLY_UNNECESSARY_GATE** — `global-ui` / `t-009`: Reversible software task is human-gated without an obvious hard-gate reason in its note.
- **POSSIBLY_UNNECESSARY_GATE** — `kind-robots` / `t-002`: Reversible software task is human-gated without an obvious hard-gate reason in its note.
- **SOFT_NEEDS_HUMAN** — `kind-robots` / `t-011`: needs-human has no obvious hard-gate marker; consider returning it to ready or documenting the actual gate.
- **SOFT_NEEDS_HUMAN** — `newsfeed` / `t-002`: needs-human has no obvious hard-gate marker; consider returning it to ready or documenting the actual gate.
- **ROADMAP_MISSING_OVERRIDE** — `ruler-hooked`: Roadmap has no project-overrides.yaml entry.
- **SOFT_NEEDS_HUMAN** — `superkate-services-calculator` / `t-030`: needs-human has no obvious hard-gate marker; consider returning it to ready or documenting the actual gate.

### Info (44)

- **APPROVAL_WITHOUT_GATE** — `ai-art-academy` / `t-002`: approved_by_human is set on a task that is not human-gated.
- **APPROVAL_WITHOUT_GATE** — `ai-art-academy` / `t-011`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `alexa-integration`: Roadmap has no friendly goal/definition of done.
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
- **MISSING_GOAL** — `media-watchlist`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `mermaids-of-venice`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `newsfeed`: Roadmap has no friendly goal/definition of done.
- **MISSING_GOAL** — `packmaker`: Roadmap has no friendly goal/definition of done.
- **INACTIVE_PROJECT_HAS_READY_TASKS** — `pinball-hero`: Inactive project retains 2 ready task(s); harmless but misleading in generated status.
- **MISSING_GOAL** — `pinball-hero`: Roadmap has no friendly goal/definition of done.
- **INACTIVE_PROJECT_HAS_READY_TASKS** — `recipe-box`: Inactive project retains 1 ready task(s); harmless but misleading in generated status.
- **MISSING_GOAL** — `recipe-box`: Roadmap has no friendly goal/definition of done.
- **INACTIVE_PROJECT_HAS_READY_TASKS** — `ruler-hooked`: Inactive project retains 7 ready task(s); harmless but misleading in generated status.
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
