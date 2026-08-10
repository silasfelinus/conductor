# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-10T23:53:47Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **579**
- Outcomes: blocked: 13, cancelled: 1, done: 565
- Success rate: **98%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 64 | 98% |
| alexa-integration | 2 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 6 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 9 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 25 | 100% |
| conductor | 72 | 100% |
| conductor-app | 2 | 100% |
| davinci | 3 | 100% |
| digital-storefront | 28 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| interface-vision | 82 | 100% |
| kind-robots | 49 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 51 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 5 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 2 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 564 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 12 |
| actionable | 9 |
| transient | 9 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `quality` — 12 occurrences; look for the shared cause across its records
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `transient` — 9 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-10 `davinci/t-023` — A long-running interactive flow (life run, quest, playthrough) needs a UI-level exit affordance from day one, not just a resolve-screen reset -- this one shipped with only a manually-cleared localStorage key as the real "abandon" path for weeks before the gap was caught. Reusing the existing reset function (playAgain) behind a window.confirm kept the fix to ~20 lines with no new state.
- 2026-08-10 `model-builder/t-040` — Pair server-side stale-write protection with matching client affordance guards when a conflicting action is known: the server preserves correctness, while the UI prevents users from entering the race in the first place.
- 2026-08-10 `model-builder/t-029` — items/[id]/commit.post.ts fetched the build item once at the top of the request and built the final stageStatuses write from that request-start snapshot, even though the write in between (promoteAsset/updateText/createRecord+linkSourceToTarget, the last inside a multi-step prisma.$transaction) can be slow -- and nothing blocks the client from reopening another already-approved stage (a fast PATCH /items/:id) while the commit POST is in flight, so the stale-snapshot final write could silently clobber that concurrent edit back to 'approved'. A distinct bug class from the ~30 prior client-side store races this recurring task has found: a server-side stale-snapshot full-object overwrite across a slow awaited write. Worth checking any route that reads a record early and writes a computed blob back late for the same shape -- re-read immediately before the final write rather than trusting the request-start snapshot.

- 2026-08-10 `storybook/t-011` — A strict WonderLab preview-audit CI check treats every new component with required props as a regression until it gets a fixture or skip reason -- even one extracted purely to avoid tripling markup in the same PR that adds it. Budget for that check whenever a component split introduces a new required-prop component; caught mid-PR via the subscribed PR-activity webhook rather than a manual poll, which is the faster signal path for a session's own open PR.
- 2026-08-10 `storybook/t-011` — Layout-first Storybook work stays safer when role meaning changes only presentation and leaves the controlled role-map interaction contract intact.
- 2026-08-10 `storybook/t-018` — When Storybook already consumes a deep-link seed key, add entry CTAs at the existing selected-object working surface and extend the narrow navigation contract instead of inventing a parallel detail route.
- 2026-08-10 `storybook/t-017` — A source-level contract can verify a cross-component behavioral handoff (click handler navigates with the right query key; the receiving page still reads that key) without asserting any markup, by checking substrings on each side of the seam independently rather than the whole line/attribute they sit inside.
- 2026-08-10 `conductor/t-113` — HTTPError subclasses URLError, so handle 404 before the generic network-failure branch when a task needs to distinguish a missing or inaccessible GitHub reference from an unverifiable transient failure.
- 2026-08-10 `conductor/t-112` — A task-events done event naming a merged PR is a claim, not a fact -- verify merge state via the GitHub API (or a shorthand repo#N note scan as a fallback) before writing status: done, and park to needs-human on mismatch instead of applying blind.
- 2026-08-10 `brainstorm/t-010` — A creative workspace deserves its own persistence semantics when existing models encode different domains; keep local draft continuity automatic, make durable account saves explicit/private, and validate a full candidate/revision/branch snapshot round-trip before trusting the schema.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-10T23:53:47Z_
