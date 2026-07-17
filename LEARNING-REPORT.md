# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-17T01:08:37Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **212**
- Outcomes: blocked: 12, done: 200
- Success rate: **94%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 19 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 4 | 100% |
| animation-studio | 1 | 100% |
| appmaker | 2 | 100% |
| approval-portal | 2 | 0% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 12 | 100% |
| conductor | 24 | 100% |
| digital-storefront | 6 | 100% |
| dream-cycle | 13 | 100% |
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
| ruler-hooked | 2 | 100% |
| serendipity | 1 | 100% |
| superkate-hairstyle-ai | 15 | 100% |
| superkate-services-calculator | 11 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 197 | 98% |

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

- 2026-07-16 `dream-cycle/t-016` — A multi-write build against an intermittent DB must be atomic: track created row ids and roll them back (DELETE, newest-first) on ANY failure, never mark a partial build complete. Bailing only on total failure silently ships incomplete, un-retried records during blips.
- 2026-07-16 `ai-art-academy/t-026` — Kaizen-verification tasks (diff-checking an adapted/paraphrased backfill against its cited source) are a cheap, high-value rotation pick when the project's primary task is egress-blocked — conductor#656 closed clean with zero drift found across 21 entries, no kind_robots PR needed. Missing from that PR: no LEARNING.yaml entry on close (added here by the merging Reviewer) — closing agents should append the ledger record in the same PR that sets status: done, not leave it for review to backfill.
- 2026-07-16 `ruler-hooked/t-011` — A vocab-drift guard for prose design docs should flag only code-token variants (far-shore/farshore for far_shore) not spaced prose ("far shore"), and must match camelCase tokens case-SENSITIVELY so the correct regionOverride does not match its own lowercased variant. Validate art-prompts inspirations against the exact field distribute_images.py reads (image_path), not a guessed schema.
- 2026-07-16 `ruler-hooked/t-003` — Check whether the target already exists before "creating" it — the kind_robots Project (id 95, conductorSlug=ruler-hooked) already existed, so t-003 reduced to setting goal. Record the friendly goal in the roadmap top-level `goal:` field (sync_projects.py source of truth) rather than only PATCHing live, so it survives a transient DB-write 503 and backfills on the next sync. Reads can succeed while writes 503 — "db is up" is not binary.
- 2026-07-16 `dream-cycle/t-015` — When the live build path is egress-blocked from an interactive session, harden the loop OFFLINE instead of faking a build: a CI preflight that validates each outline against the playbook (accepting every real shape, lenient counts) catches unbuildable outlines before t-006 ever runs. Verify environment egress before claiming DB/token blockers.
- 2026-07-16 `conductor/t-059` — When a cleanup action is impossible from the session (ref deletion 403s here), fix it durably in a GitHub Actions workflow whose GITHUB_TOKEN has the permission, and make the desired end-state (clean main, no leftover branch) the explicit default in AGENTS.md/prompts rather than an opt-in a human must request.
- 2026-07-16 `conductor/t-051` — CLI-gating tests (main()'s argument-combination branches) are a distinct coverage layer from the unit tests of the function they wrap (t-050) — both are needed, and it's easy to declare a file "tested" after only the unit layer lands.

- 2026-07-16 `conductor/t-046` — A proven manual recipe (CYPRESS_INSTALL_BINARY=0 + dummy DATABASE_URL) is only as useful as its discoverability — turning it into a script closes half the gap, but it still needs a pointer from AGENTS.md (t-057) or future sessions will re-derive the same recipe from scratch.

- 2026-07-16 `conductor/t-031` — Before adding a CI step, check whether the existing job already covers it (the full pytest tests/ run since t-047 already discovered the new test file) — avoids a redundant, easy-to-miss-in-review duplicate wire-up.

- 2026-07-16 `conductor/t-045` — Documenting a fix in AGENTS.md doesn't finish the story if the same session that merges it also hits the Reviewer-side half of the same race (see t-056) — a written rule for one role doesn't cover the other role's version of the problem.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-17T01:08:37Z_
