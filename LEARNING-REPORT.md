# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-16T20:02:54Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **206**
- Outcomes: blocked: 12, done: 194
- Success rate: **94%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 18 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 4 | 100% |
| animation-studio | 1 | 100% |
| appmaker | 2 | 100% |
| approval-portal | 2 | 0% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 12 | 100% |
| conductor | 23 | 100% |
| digital-storefront | 6 | 100% |
| dream-cycle | 11 | 100% |
| ecosystem-map | 4 | 100% |
| global-ui | 3 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 22 | 95% |
| kindrobots-unraid | 4 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 27 | 100% |
| mural-design | 1 | 100% |
| newsfeed | 2 | 100% |
| packmaker | 5 | 100% |
| serendipity | 1 | 100% |
| superkate-hairstyle-ai | 15 | 100% |
| superkate-services-calculator | 11 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 191 | 98% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 5 |
| quality | 3 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `actionable` — 5 occurrences; look for the shared cause across its records
- failure category `quality` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-16 `conductor/t-051` — CLI-gating tests (main()'s argument-combination branches) are a distinct coverage layer from the unit tests of the function they wrap (t-050) — both are needed, and it's easy to declare a file "tested" after only the unit layer lands.

- 2026-07-16 `conductor/t-046` — A proven manual recipe (CYPRESS_INSTALL_BINARY=0 + dummy DATABASE_URL) is only as useful as its discoverability — turning it into a script closes half the gap, but it still needs a pointer from AGENTS.md (t-057) or future sessions will re-derive the same recipe from scratch.

- 2026-07-16 `conductor/t-031` — Before adding a CI step, check whether the existing job already covers it (the full pytest tests/ run since t-047 already discovered the new test file) — avoids a redundant, easy-to-miss-in-review duplicate wire-up.

- 2026-07-16 `conductor/t-045` — Documenting a fix in AGENTS.md doesn't finish the story if the same session that merges it also hits the Reviewer-side half of the same race (see t-056) — a written rule for one role doesn't cover the other role's version of the problem.

- 2026-07-16 `ai-art-academy/t-025` — A kaizen task filed with owner: reviewer from a prior merge can be picked up and implemented directly in a later autonomous cycle acting as Worker when no separate Worker session is active that hour — the owner field on a ready task is a hint, not a hard assignment. When adapting source prose (here: teaching-notes.md's table) into code strings rather than copying verbatim, file a small follow-on diff-check task rather than trusting the cleanup by eye; it is cheap insurance against silent meaning drift.

- 2026-07-16 `dream-cycle/t-004` — Write the type-agnostic loop contract (CREATION-SPEC.md) once and have each specs/<type>.md playbook plug into it, rather than restating queue/one-building/ledger rules per playbook; cite create-calls from the API audit so stages stay in sync with the real endpoints.
- 2026-07-16 `conductor/t-025` — Before building a new helper, grep for an existing one — the t-025 scaffolder already lived in scripts/intake.py, so the work was a small extension (DESIGN-BRIEF.md + CONTROL.md block) plus the tests it never had, not a greenfield script.
- 2026-07-16 `newsfeed/t-004` — When a design brief documents an "Audit findings" section with exact file paths and line numbers for the conventions a new module must follow (here: stores/helpers/<domain>.ts for types, a private safeGetLocalStorage/ safeSetLocalStorage pair per store instead of a shared util or DB table), trust it literally rather than re-deriving the pattern from scratch — it was written by a prior session that already did the archaeology. Attempting live verification of candidate external URLs before committing them (even when it fails, as it did here with a 403 from the sandbox's egress allowlist on every probe) is worth the two minutes: it turns "these RSS URLs are probably fine" into an explicit, auditable `verified: false` plus a follow-on task, instead of a silent assumption baked into the registry.

- 2026-07-16 `superkate-hairstyle-ai/t-017` — A task can be fully implemented and merged (kind_robots PR #317) while still sitting at roadmap status: claimed — the Reviewer sweep found it only by checking the open-PR list directly, not roadmap state. This is the second instance of a Silas-directed claude/* session finishing work without flipping the task through status: review first (see project TALKBACK 2026-07-10 entry); filed superkate-hairstyle-ai/t-020 to close the gap going forward.

- 2026-07-16 `global-ui/t-018` — Cross-repo kaizen tasks that extend an already-shipped computed pattern (here, t-015's doneTasksByMilestone done/active split) are cheapest to verify against the widest-blast-radius check available even when the change is tiny: running the full-project vue-tsc --noEmit (not just the touched file) caught that this environment's freshly-installed prettier version reformats unrelated pre-existing union-type lines on save, which would have silently expanded the diff's blast radius if not checked for and manually reverted before committing.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-16T20:02:54Z_
