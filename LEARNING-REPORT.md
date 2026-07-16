# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-16T09:49:56Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **84**
- Outcomes: blocked: 1, done: 83
- Success rate: **99%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 7 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 4 | 100% |
| animation-studio | 1 | 100% |
| challenge-center | 12 | 100% |
| coloring-book | 1 | 100% |
| conductor | 14 | 100% |
| digital-storefront | 3 | 100% |
| ecosystem-map | 2 | 100% |
| global-ui | 1 | 100% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 15 | 93% |
| kindrobots-unraid | 1 | 100% |
| mermaids-of-venice | 1 | 100% |
| model-builder | 13 | 100% |
| newsfeed | 1 | 100% |
| packmaker | 4 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 3 | 100% |
| software | 81 | 99% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 4 |
| quality | 3 |

## Kaizen targets

- failure category `actionable` — 4 occurrences; look for the shared cause across its records
- failure category `quality` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-16 `kind-robots/t-024` — For a detection/guard script, verify the negative case explicitly (a temporary fixture that should fail the check) in addition to the clean-pass case -- a check that has never been proven to actually catch a violation is unverified regardless of how clean the real tree scans.
- 2026-07-16 `kind-robots/t-023` — Extracting shared inline-workflow bash into a repo-root scripts/*.sh file (rather than re-implementing the same logic inside the test) keeps a regression test provably in sync with the production step it's guarding -- worth doing whenever a test's whole point is 'catch future edits to this exact check'.
- 2026-07-16 `conductor/t-050` — Clean first-pass test-coverage closure: the kaizen note named the exact two plan_owner() branches to cover (missing/deactivate, orphan-loop skip) precisely enough to write direct unit tests against plan_owner() itself rather than going through main()'s CLI/argparse plumbing -- faster to write and to read than an equivalent integration test. Filed t-051 to cover the one thing plan_owner()-level tests structurally can't reach: main()'s --apply/--deactivate gating of whether missing rows actually get POSTed.

- 2026-07-16 `conductor/t-029` — A kaizen note that names its exact test cases up front ("covering: X, Y, Z, W") makes a script-testing task fully self-scoping -- no need to chase down the original throwaway harness (PR #360's body only described it in prose, no code was ever committed) when the note already specifies the behaviors precisely enough to write fresh monkeypatch-based tests against the current source. Two easy self-made test bugs worth flagging for future test-writing tasks: (1) synthetic fixture data using `id: i` starting at 0 silently trips falsy-id guards in the code under test (`if slug and row.get("id")`) -- start fabricated ids at 1; (2) `capsys` stdout from `json.dumps(..., indent=2)` is multi-line, so `.splitlines()[-1]` grabs a bare closing brace instead of the object -- parse the whole captured block.

- 2026-07-16 `kind-robots/t-028` — A guard script written to catch a bug class (t-026's dead-path-reference regression) is worth typechecking against the exact CI job it will run in before merging, not just eslint/prettier -- the first vue-tsc pass caught 12 noUncheckedIndexedAccess errors in the new script from plain array-index and regex-capture-group access, the identical bug class t-027 exists to sweep for elsewhere in the codebase. Writing a new script is also an opportunity to self-check it doesn't introduce the very pattern a sibling kaizen task is auditing for. Simulating the actual regression (temporarily removing a referenced file/fixture, confirming the check fails, restoring, confirming it passes again) before opening the PR is a cheap, high-confidence verification step for any "detect a missing reference" tool and should be the default verification pattern for this task shape.

- 2026-07-16 `kind-robots/t-008` — Design-only tasks (deliverable is a spec doc, not code/migration) are ideal fallback picks when the priority-ordered projects ahead are env-blocked (ai-art-academy museum-egress + KR_API_TOKEN, coloring-book and digital-storefront riding the same two blockers, ai-art-academy's recurring t-010 already run this window). t-008 had zero cross-repo dependency and zero external egress need, so it was fully landable in one pass. Grounding the design in the actual target schema (grep for existing models/fields before writing a line of the spec) surfaced a reusable structural precedent (UserRelation) that made the new Grant model's shape obvious rather than invented from scratch -- worth doing for any future spec-writing task that touches an existing app's data model.

- 2026-07-16 `conductor/t-043` — Kaizen from ai-art-academy/t-012 (2026-07-14): three scripts (resolve_deps.py, next_ready_task.py, audit_roadmaps.py) each independently reimplemented the same dependency-satisfaction check. Extracted scripts/roadmap_deps.py mirroring the existing roadmap_claims.py centralization pattern. One subtlety worth flagging for future dedup passes: audit_roadmaps.py is loaded standalone via importlib.util.spec_from_file_location in its policy test, with no package context, so a bare sibling import needs the same sys.path.insert(0, <script dir>) trick resolve_deps.py/next_ready_task.py already use -- a plain `from roadmap_deps import ...` without it would only work by accident of import order across the test session. Also another good burst-mode fallback pattern: ai-art-academy's ready tasks were all env-blocked again (museum-egress 403, missing KR_API_TOKEN, recurring t-010 already run this window) and coloring-book/ digital-storefront's ready tasks hit the same two blockers, so picked a fully self-contained in-repo task instead of re-treading known-blocked ground.

- 2026-07-16 `kind-robots/t-026` — CI-fixture kaizen task (facet-alias-smoke.yml's dead migration reference, filed from t-025). Recovering the pre-squash migration content via `git show <pre-squash-sha>:<path>` was essential -- the squashed migration.sql alone was missing the canonical-alias seed INSERT that the smoke test's assertions depend on, so a fixture built only from the squashed CREATE TABLE would have passed schema-shape review but still failed CI. Good burst-mode pick when the top-priority project (ai-art-academy) has all its ready tasks genuinely env-blocked (museum-egress 403 / missing KR_API_TOKEN) and its recurring continuous-improvement task already ran this window -- fell through to the next active project in priority.yaml with concrete, unblocked work.

- 2026-07-16 `packmaker/t-006` — Task bundled a mechanical always-doable step (tutorial channel wiring) with two env-blocked steps (art gen needs KR_API_TOKEN; admin Placements verification needs admin UI) and one step that duplicated a separately gated task (t-004, waiting on t-003's human approval). Split at pickup time rather than attempting the whole note: shipped kind_robots PR #306 for the landable slice, explicitly dropped the duplicate step, and documented the blocked steps in the closing note instead of leaving the task perpetually ready. Future roadmap authoring should split tasks like this into separate sub-tasks up front.

- 2026-07-16 `ai-art-academy/t-018` — Clean first-pass cross-repo seed sync (kind_robots PR #305), mirroring t-015's Neoclassicism precedent exactly: copy artist bios/remix_hint verbatim from the conductor curriculum doc rather than re-deriving them, and insert in curriculum order. Good burst-mode pick when the project's other ready tasks (t-004/t-008/t-009/t-013) are blocked on missing KR_API_TOKEN or museum-egress 403s -- this task needed neither.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-16T09:49:56Z_
