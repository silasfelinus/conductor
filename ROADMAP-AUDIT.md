# Roadmap Audit

Generated: `2026-08-05T02:29:13.148711+00:00`

This is a conservative structural audit. It reports suspicious state; it does not automatically change task status or remove human gates.

## Portfolio snapshot

- **45** roadmaps, **27** active projects, **874** tasks
- **48 ready**, **47 waiting**, **10 needs-human**, **2 claimed/review**, **757 done**
- Findings: **3 errors**, **7 warnings**, **65 informational**

## Project inventory

| # | Project | State | Kind | Ready | Waiting | Human | In progress | Done / Total |
|---:|---|---|---|---:|---:|---:|---:|---:|
| 1 | `interface-vision` | active | software | 0 | 0 | 0 | 0 | 101 / 101 |
| 2 | `challenge-center` | finished | software | 0 | 0 | 0 | 0 | 20 / 20 |
| 3 | `ai-art-academy` | active | software | 2 | 1 | 0 | 1 | 50 / 54 |
| 4 | `coloring-book` | active | software | 0 | 9 | 1 | 1 | 26 / 37 |
| 5 | `humboldt-scoop` | finished | software | 0 | 0 | 0 | 0 | 8 / 8 |
| 6 | `humboldt-scoop-cms` | active | software | 1 | 0 | 0 | 0 | 11 / 12 |
| 7 | `digital-storefront` | active | software | 1 | 0 | 0 | 0 | 32 / 33 |
| 8 | `packmaker` | finished | software | 0 | 0 | 0 | 0 | 10 / 10 |
| 9 | `mermaids-of-venice` | active | content | 9 | 0 | 0 | 0 | 4 / 13 |
| 10 | `kind-robots` | active | software | 3 | 0 | 0 | 0 | 50 / 53 |
| 11 | `kindrobots-unraid` | active | software | 1 | 7 | 0 | 0 | 4 / 12 |
| 12 | `global-ui` | finished | software | 0 | 0 | 0 | 0 | 25 / 25 |
| 13 | `mona-salai` | paused | software | 2 | 10 | 0 | 0 | 1 / 13 |
| 14 | `superkate-services-calculator` | finished | software | 0 | 0 | 0 | 0 | 37 / 37 |
| 15 | `superkate-hairstyle-ai` | paused | software | 1 | 0 | 1 | 0 | 19 / 21 |
| 16 | `newsfeed` | active | software | 0 | 0 | 0 | 0 | 22 / 22 |
| 17 | `model-builder` | active | software | 2 | 0 | 0 | 0 | 37 / 39 |
| 18 | `animation-manager` | active | software | 2 | 0 | 0 | 0 | 15 / 17 |
| 19 | `animation-studio` | retired | software | 3 | 4 | 0 | 0 | 1 / 8 |
| 20 | `ecosystem-map` | finished | software | 0 | 0 | 0 | 0 | 8 / 8 |
| 21 | `conductor` | active | software | 2 | 0 | 0 | 0 | 96 / 98 |
| 22 | `serendipity` | retired | software | 1 | 0 | 0 | 0 | 11 / 12 |
| 23 | `taskmaster` | active | software | 1 | 0 | 0 | 0 | 2 / 3 |
| 24 | `storybook` | active | software | 1 | 0 | 0 | 0 | 9 / 10 |
| 25 | `davinci` | active | software | 0 | 0 | 0 | 0 | 16 / 16 |
| 26 | `art-generator-connect` | finished | software | 0 | 0 | 0 | 0 | 22 / 22 |
| 27 | `mural-design` | active | content | 0 | 3 | 1 | 0 | 3 / 7 |
| 28 | `coat-dance` | active | content | 2 | 0 | 0 | 0 | 1 / 10 |
| 29 | `career-transition` | retired | content | 0 | 4 | 3 | 0 | 1 / 8 |
| 30 | `alexa-integration` | active | software | 2 | 0 | 1 | 0 | 16 / 19 |
| 31 | `conductor-app` | active | software | 2 | 0 | 0 | 0 | 12 / 14 |
| 32 | `appmaker` | active | software | 2 | 0 | 0 | 0 | 10 / 12 |
| 33 | `media-watchlist` | active | software | 1 | 0 | 0 | 0 | 15 / 16 |
| 34 | `sketchy` | finished | software | 0 | 0 | 0 | 0 | 8 / 8 |
| 35 | `pinball-hero` | retired | content | 0 | 2 | 2 | 0 | 2 / 6 |
| 36 | `recipe-box` | retired | software | 0 | 2 | 1 | 0 | 0 / 3 |
| 37 | `brainstorm` | active | proposal | 1 | 0 | 0 | 0 | 0 / 1 |
| 38 | `wishmaster` | active | software | 1 | 0 | 0 | 0 | 2 / 3 |
| 39 | `engagement` | finished | software | 0 | 0 | 0 | 0 | 3 / 3 |
| 40 | `ruler-hooked` | active | software | 1 | 0 | 0 | 0 | 11 / 12 |
| 41 | `music-mentor` | active | software | 1 | 0 | 0 | 0 | 8 / 9 |
| 42 | `dream-cycle` | active | software | 2 | 0 | 0 | 0 | 20 / 22 |
| — | `approval-portal` | retired | software | 0 | 0 | 0 | 0 | 3 / 5 |
| — | `humboldt-impropriety-calendar` | retired | brainstorm | 0 | 5 | 0 | 0 | 0 / 6 |
| — | `lora-ingestion` | active | infrastructure | 1 | 0 | 0 | 0 | 5 / 6 |

## Findings by severity

### Error (3)

- **CONTROL_PRIORITY_DRIFT** — `_global`: CONTROL.md priority band ['challenge-center', 'ai-art-academy', 'coloring-book', 'humboldt-scoop', 'humboldt-scoop-cms', 'digital-storefront', 'packmaker', 'mermaids-of-venice', 'kind-robots', 'kindrobots-unraid', 'global-ui'] does not match priority.yaml prefix ['interface-vision', 'challenge-center', 'ai-art-academy', 'coloring-book', 'humboldt-scoop', 'humboldt-scoop-cms', 'digital-storefront', 'packmaker', 'mermaids-of-venice', 'kind-robots', 'kindrobots-unraid'].
- **ACTIVE_MISSING_PRIORITY** — `lora-ingestion`: Active project is absent from projects/priority.yaml.
- **ACTIVE_ROADMAP_MISSING_PRIORITY** — `lora-ingestion`: Active roadmap is not selectable because it is absent from priority.yaml.

### Warning (7)

- **STALE_IN_PROGRESS** — `coloring-book` / `t-022`: Task has remained claimed for 3 days.
- **ACTIVE_PROJECT_ALL_DONE** — `davinci`: All tasks are done but project override remains active.
- **ACTIVE_PROJECT_NO_OPEN_TASKS** — `davinci`: Active project has no open tasks; mark finished/paused or add an intentional recurring task.
- **ACTIVE_PROJECT_ALL_DONE** — `interface-vision`: All tasks are done but project override remains active.
- **ACTIVE_PROJECT_NO_OPEN_TASKS** — `interface-vision`: Active project has no open tasks; mark finished/paused or add an intentional recurring task.
- **ACTIVE_PROJECT_ALL_DONE** — `newsfeed`: All tasks are done but project override remains active.
- **ACTIVE_PROJECT_NO_OPEN_TASKS** — `newsfeed`: Active project has no open tasks; mark finished/paused or add an intentional recurring task.

### Info (65)

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
- **MISSING_GOAL** — `interface-vision`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `interface-vision` / `t-016`: approved_by_human is set on a task that is not human-gated.
- **APPROVAL_WITHOUT_GATE** — `interface-vision` / `t-040`: approved_by_human is set on a task that is not human-gated.
- **APPROVAL_WITHOUT_GATE** — `interface-vision` / `t-056`: approved_by_human is set on a task that is not human-gated.
- **APPROVAL_WITHOUT_GATE** — `interface-vision` / `t-071`: approved_by_human is set on a task that is not human-gated.
- **APPROVAL_WITHOUT_GATE** — `interface-vision` / `t-074`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `kind-robots`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `kind-robots` / `t-029`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `kindrobots-unraid`: Roadmap has no friendly goal/definition of done.
- **APPROVAL_WITHOUT_GATE** — `kindrobots-unraid` / `t-002`: approved_by_human is set on a task that is not human-gated.
- **MISSING_GOAL** — `lora-ingestion`: Roadmap has no friendly goal/definition of done.
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
- **MISSING_GOAL** — `storybook`: Roadmap has no friendly goal/definition of done.
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
