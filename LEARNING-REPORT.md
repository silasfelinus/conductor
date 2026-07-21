# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-21T01:17:38Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **316**
- Outcomes: blocked: 12, done: 304
- Success rate: **96%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 34 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 8 | 100% |
| animation-studio | 1 | 100% |
| appmaker | 4 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 13 | 100% |
| conductor | 43 | 100% |
| conductor-app | 1 | 100% |
| digital-storefront | 12 | 100% |
| dream-cycle | 14 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 29 | 97% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 2 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 29 | 100% |
| mural-design | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 1 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 11 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 301 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 6 |
| actionable | 6 |
| transient | 4 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `quality` — 6 occurrences; look for the shared cause across its records
- failure category `actionable` — 6 occurrences; look for the shared cause across its records
- failure category `transient` — 4 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-20 `media-watchlist/t-009` — A prior spec-only task (t-008) that reconciles a proposal against real imported data before any code is written turns the follow-on build task into a single clean pass with zero open design questions -- worth doing as a standing pattern for any Prisma-model-plus-API task where the real data shape might differ from an earlier proposal.
- 2026-07-20 `ai-art-academy/t-010` — Milestone status can drift not just from new tasks appearing done/not-done under it, but from an *existing* task being re-tagged into a milestone that was already marked done (t-035 landed under m6 alongside the t-029/t-030 kaizen follow-ons after m6 had last been verified done, and the milestone was never revisited) -- a roadmap-accuracy audit should re-check a milestone's task list for membership changes, not just each member task's status, whenever a milestone is already 'done'.
- 2026-07-20 `sketchy/t-003` — When a spec-writing task's target area already has partial coverage scattered across sibling docs (PRODUCT-SPEC.md's dimension table, SKILL-LADDER.md's routing examples, docs/ai-critique-apis.md's integration notes), the value-add is turning illustrative/example-based coverage into deterministic, implementable rules (numeric anchors, explicit tie-break order, the literal prompt text) rather than re-describing what already exists — read every referenced sibling doc in full before drafting.
- 2026-07-20 `conductor-app/t-007` — Before implementing a roadmap task's stated problem, verify the problem still exists on current main -- t-007's premise (pitch votes and project priorities stuck in per-browser localStorage) was already false: priorities had already migrated to a real Prisma column and votes already flow through a real per-pitch API endpoint, just not via the code paths the task's note assumed. An Explore agent pass against the live repo (grep for the exact localStorage keys named in the task) caught this before any code was written; filed the genuinely-open sub-question (real per-user multi-voter tallying vs. today's single-admin-status design) as a separate soft-needs-human task instead of building speculative scope.
- 2026-07-20 `art-generator-connect/t-022` — When a workflow step blows past a --limit/--timeout ceiling that looks correctly plumbed, check for unbounded work happening BEFORE the bounded loop, not just inside it -- consume_art_requests.py's self-drain pre-scan (already_satisfied()) ran over the full pending backlog (not --limit-bounded, by design) and called the network-backed check twice per entry via two separate list comprehensions, which is what actually blew the ceiling, not wait_for_job/--timeout as the original note hypothesized.
- 2026-07-20 `appmaker/t-011` — For 'file age' checks in this repo, local git log is not trustworthy -- local clones are frequently shallow/squash-merged, and two unrelated apps/<slug>/lib/main.dart files both showed exactly one, identical-timestamp commit locally despite being scaffolded on different dates. Querying the GitHub REST API's commits?path=... endpoint for a file's earliest commit gives the true creation date regardless of local clone depth; scripts/check_repos.py's existing GITHUB_TOKEN+urllib pattern is the right template to reuse, even though the API call itself can't be live-verified from this interactive sandbox (org egress policy 403s api.github.com here) -- that's a known, pre-existing limitation, not new.
- 2026-07-20 `appmaker/t-006` — Before implementing a 'create the kind_robots Project for slug parity' task, run scripts/sync_projects.py live first -- it's idempotent and prints UNCHANGED (with a real field-by-field comparison, not just a slug match) when parity is already satisfied, which was the case here (id=24 already had conductorSlug=appmaker). Confirmed this session also has genuine KR_API_TOKEN + kind_robots API egress, unlike ai-art-academy's documented relay/museum-egress blocks -- worth checking live rather than assuming blocked.
- 2026-07-20 `ecosystem-map/t-006` — Before writing new implementation tasks off a stale audit doc, re-verify the audit's claims live against the target repo -- FRONTEND-SURFACE-MAP.md's 2026-07-10 snapshot of 15 missing/incomplete surfaces was 10 days out of date; checking kind_robots main's dashboardHelper.ts and content/*.md directly showed all 15 already had scaffold routes, and each project's own roadmap.yaml already carried the matching 'Polish and upgrade <Project> front-end surface' follow-up task (5 done, 10 ready). Filing new tasks from the doc's text alone would have created 15 duplicate entries forking the same work into two roadmap locations. Also: closing a project's last open task can flip it into ACTIVE_PROJECT_ALL_DONE/ACTIVE_PROJECT_NO_OPEN_TASKS in audit_roadmaps.py -- left project-overrides.yaml's status untouched since flipping active->finished/paused looks like a Silas-approval decision per that file's existing precedent comments, matching how humboldt-scoop already sits in the identical state unremediated.
- 2026-07-20 `storymaker/t-009` — A task that says 'add a section to the session data model doc (or a pointer in notes_from_silas)' should not assume the primary doc exists -- t-001's 'session data model' was approved via its roadmap note only, never written as a standalone doc file, so checking for the doc's actual existence before picking an implementation shape (rather than defaulting to the first-listed option) avoided inventing an unread new file. notes_from_silas is a good landing spot for cross-project boundary rules precisely because AGENTS.md's picking-order rules make every future session read it first.
- 2026-07-20 `animation-manager/t-012` — Burst-mode rotation picking superkate-hairstyle-ai/t-019 and model-builder/t-022, t-029, t-031 next in priority.yaml order all turned out to need a live deployed backend (a Tailscale ts.net Comfy box or an admin-only action) this sandbox can't reach -- confirmed via each task's own note/TALKBACK history before skipping rather than claiming and stalling. animation-manager/t-012 (a kaizen from t-005's review) was the first genuinely pure-code ready task further down the list. The fix itself was a clean first pass: extracted the WORKING-attempt-to-supersede lookup as a pure, testable helper (findAttemptToSupersede in animationComponentHelper.ts) instead of inlining the filter in the store action, matching the existing listAnimationAttempts/getLatestAnimationAttempt pattern and letting the new behavior be covered in the same DB-free verify script (verifyAnimationComponentAttempts.ts) rather than needing a Pinia-mocking store test that doesn't exist yet for this store.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-21T01:17:38Z_
