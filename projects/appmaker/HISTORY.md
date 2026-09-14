# appmaker — task history archive

Full `note:` prose for completed appmaker tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Approve the AppMaker brief and architecture

<!-- note:begin t-001 -->
FOR SILAS: You answered the brief's three questions in-session 2026-07-02 (migrate app/ to apps/conductor — done; GitHub App for phase 2; build self-serve as the end state). The decisions are recorded in projects/appmaker/BRIEF.md. Agents may not set approved_by_human themselves, so TO FORMALIZE: set approved_by_human: true and status: done here. Dependent tasks were already un-gated on your verbal direction.
<!-- note:end t-001 -->

## t-003 — Design the permission-based GitHub integration (GitHub App)

<!-- note:begin t-003 -->
APPROVED by Silas 2026-07-04. Design: projects/appmaker/GITHUB-APP-DESIGN.md. Load-bearing sections to read: 2 (app permissions — contents/PRs/checks read-write, nothing more), 4 (GithubInstallation + AppRepo data model; AppRepo is the slug->repo mapping), and 6 (security invariants — no credentials in clients or DB, HMAC'd webhooks, signed install nonce). TO APPROVE: set approved_by_human: true and status: done. Unblocks t-007 (you register the app — it lives under your GitHub account) then t-008..t-010.
<!-- note:end t-003 -->

## t-006 — Create the appmaker kind_robots Project (slug parity)

<!-- note:begin t-006 -->
Run scripts/sync_projects.py (or POST /api/projects) so kind_robots has a Project with conductorSlug "appmaker" matching this project, per the standing slug-parity rule in CONTROL.md (post Dream/Project/Facet split).

DONE 2026-07-20: ran `python scripts/sync_projects.py` live (this session has
working KR_API_TOKEN + kind_robots API egress) and it reported `appmaker:
UNCHANGED (id=24)` — `sync_project()` only prints UNCHANGED when
`find_project_by_slug` resolves the kind_robots Project via GET
/api/projects/appmaker AND every field in the computed payload, including
`conductorSlug: "appmaker"`, already matches the existing record exactly.
Slug parity was already satisfied (likely from an earlier bulk sync); this
task just formalizes that in the roadmap. No kind_robots change needed.
<!-- note:end t-006 -->

## t-007 — Register the AppMaker GitHub App and store its secrets in server env

<!-- note:begin t-007 -->
DONE per Silas 2026-07-05 — GitHub App created at /silasfelinus/app-maker. If APPMAKER_GH_APP_KEY / APPMAKER_GH_WEBHOOK_SECRET / app id are not yet in Vercel env, the first webhook-endpoint task will surface it. Original instructions: create the GitHub App per GITHUB-APP-DESIGN.md section 2 (permissions: contents rw, pull_requests rw, metadata r, checks r, actions r; webhook events push/pull_request/check_suite/installation), then put APPMAKER_GH_APP_KEY, APPMAKER_GH_WEBHOOK_SECRET, and the app id into Vercel env. Agents never hold the key.
<!-- note:end t-007 -->

## t-008 — kind_robots: installation models, connect flow, webhook endpoint

<!-- note:begin t-008 -->
GithubInstallation + AppRepo Prisma models, GET connect redirect with signed state nonce, setup callback, HMAC-verified POST /api/appmaker/github/webhook, and the granted-repo list API. Per design sections 4, 5a, 5e, 6.
DONE 2026-07-20 (conductor agent session claude-conductor-agent-20260720T1535Z, kind_robots PR #651 merged squash ea478b28): built exactly what the design doc's §8 task table specced for t-008, no more/less -- GithubInstallation + AppRepo Prisma models (additive migration 20260720154500_appmaker_github_integration, hand-authored since no shadow DB was available to run `prisma migrate dev`, checked line-by-line against the schema and the nearest analogous existing migration), GET /api/appmaker/github/connect (signed state nonce via jose HS256, reusing the existing JWT_SECRET rather than provisioning a new one), GET /api/appmaker/github/setup (verifies state, fetches installation details as the app itself via a jose RS256 App JWT, upserts GithubInstallation), POST /api/appmaker/github/webhook (HMAC-SHA256 verified against the raw body, mirroring server/api/stripe/webhook.post.ts's raw-body pattern exactly), and GET /api/appmaker/github/repos. push/pull_request/check_suite webhook events are acknowledged but no-op -- design section 5e's CI-status-cache is a separate model not in t-008's scope, left undone rather than speculatively built. Installation-token minting and any GitHub write action were deliberately left to t-009 per the design doc's own task split. Verified: vue-tsc --noEmit (0 errors), eslint + prettier clean on all changed files, Prisma JSON-cast / unquoted-reserved-table / capture-group-guard contracts all pass, known-migration-repair self-test still passes. Not verified: a live install round-trip against real GitHub (no reachable live environment in this sandbox, same class of gap as other recent live-smoke deferrals) -- flagged in the kind_robots PR body. `python scripts/audit_roadmaps.py` -- 0 errors, no new warnings.
<!-- note:end t-008 -->

## t-009 — Worker external-repo support: installation tokens + scaffold PR flow

<!-- note:begin t-009 -->
Mint installation tokens server-side, push worker/scaffold-<slug> branches to user repos, open PRs. Worker role rules from design section 5d apply unchanged.
DONE 2026-07-21 (conductor scheduled agent run, claude-conductor-agentrun-20260721T-appmaker): kind_robots PR #812 merged (squash 801ed768). Built exactly what GITHUB-APP-DESIGN.md's §8 task table specs for t-009 -- mintInstallationToken/listInstallationRepositories/pushScaffoldBranchAndOpenPr in server/utils/appmakerGithub.ts (token never returned by any API, per §6 invariant 3), repos.get.ts extended with live availableRepos, create-app.post.ts (self-serve external-repo app creation, §5b steps 1-2) and scaffold.post.ts (admin/Worker-only mint+branch+PR, §5b step 3, requireAdminApiUser matching the KR_API_TOKEN Worker-auth convention). Did not build §5c graduation flow -- that is t-010, gated separately. Real find this cycle: the PR's own CI (TypeScript check) failed on the first two pushes with a TS2589 "excessively deep" recursion error in components/art/art-styler.vue, unrelated on its face to appmaker. Root-caused rather than worked around: the 2 new server/api/appmaker/github/*.ts route files grew the project's typed NitroFetchRequest route-key union just enough to push vue-tsc's recursion limit on ANY $fetch call whose R (request) generic was left to infer from the full route union instead of being pinned explicitly -- a pre-existing, repo-wide fragility already sitting at the edge (confirmed: main's own tip reproduces the same failure once nudged, e.g. by any 1-2 new route files). Fixing art-styler.vue's call site only revealed the next-worst one; chased all the way through the codebase (there are only 14 files that call $fetch directly -- the rest goes through typed stores/helpers) and pinned $fetch's R generic (`$fetch<T, string>` or plain `fetch()` for client-only static-asset reads) in all 12 affected files: art-styler.vue, coloring-book-manager.vue, dream-inspire-button.vue, newsfeed-feed.vue, super-form.vue, watchlist-browse.vue, watchlist-entry-detail.vue, leaderboard.vue, currentModel.get.ts, google/callback.ts, muralStore.ts, collectionCardImage.ts. Zero behavior change, verified via vue-tsc --noEmit (0 errors, was exit 2), eslint, and prettier all clean across all 16 changed files, then confirmed green in real CI (TypeScript + Contract verifiers both success) before merging. Also confirmed via conductor/t-073 (still open, needs-human) that the TypeScript check is not actually a required kind_robots branch-protection gate -- did not rely on that to merge, since the underlying issue was fixed for real, but noting it as relevant context for whoever closes t-073.
<!-- note:end t-009 -->

## t-011 — Flag bare-scaffold apps that go stale so the fleet doesn't accumulate untouched shells

<!-- note:begin t-011 -->
Kaizen from Reviewer on the PR #104 merge (2026-07-03): PR #104 scaffolded apps/ for every existing active project (humboldt-scoop-cms, kind-robots, media-watchlist, sketchy, storybook, wishmaster) as bare `flutter create` shells with no roadmap task driving them to build-out. Add a check (script or CI note) that surfaces apps/<slug>/ folders whose lib/ has never grown past main.dart after N days, so Silas can decide build vs. retire instead of the fleet growing silently.
DONE 2026-07-20 (agent run): added scripts/flag_stale_apps.py. Bareness detection is structural, not date-based -- flags apps/<slug>/ whose lib/ contains exactly the untouched main.dart scripts/new_app.py scaffolds (matched by its "scaffolded by AppMaker" marker string), so it stays correct even for apps built without that script (e.g. the PR #104 batch). Age comes from each file's earliest commit via the GitHub REST API (GET /repos/silasfelinus/conductor/commits?path=...), not local git log -- this repo's local clones are frequently shallow/squash-merged (confirmed this session: apps/wishmaster and apps/appmaker each showed only one commit in local history, both misleadingly identical), so local git history is not a reliable source of true file age here. Currently flags 8 of 10 apps/ as still-bare (appmaker, humboldt-scoop-cms, kind-robots, media-watchlist, recipe-box, sketchy, storybook, wishmaster); conductor and superkate-services-calculator are correctly excluded as genuinely built out. Verified locally: `python -m py_compile` clean, `python scripts/flag_stale_apps.py` / `--json` / `--strict` all run and correctly identify the 8 bare folders. The GitHub API age lookup itself could not be live-verified from this interactive sandbox -- direct `api.github.com` calls 403 here by organization egress policy (same limitation already present in scripts/check_repos.py, which uses the identical GITHUB_TOKEN+urllib pattern) -- but will run with real network access under the workflow's real `GITHUB_TOKEN` in GitHub Actions or a local Silas run, same as check_repos.py already does. Kept as a standalone script per the task's "script or CI note" wording rather than wiring a new recurring workflow, to keep the diff scoped; wiring it into an existing periodic workflow is a natural follow-up if Silas wants it automatic.
<!-- note:end t-011 -->

## t-012 — Polish and upgrade AppMaker front-end surface

<!-- note:begin t-012 -->
PROGRESS 2026-08-22 (conductor scheduled Agent run): fresh read excluding all prior fixes (refreshToken sequencing, fetchProjects force in-flight sharing, slug-candidate validation, fleet-description fallback, monorepo scaffold-collision guard, create-app.post.ts collision gap). Found apps.get.ts (the pending-scaffold reader) only ever recognized scaffold-request.post.ts's monorepo-flow Todo title ("Scaffold new app '<slug>' ...") -- both its Prisma query filter (title: { startsWith: "Scaffold new app '" }) and its extraction regex (SCAFFOLD_TITLE_RE) silently excluded github/create-app.post.ts's external-repo-flow title ("Scaffold external app '<slug>' via AppMaker GitHub integration"). A request filed through the external-repo flow (already API-reachable, no front-end wired up yet per the 2026-08-21 cycle's own finding) created a real, open Todo that silently never appeared in the AppMaker page's "Being built" section -- the same "API-reachable even without a UI, so still worth fixing" precedent the 2026-08-21 cycle set for this exact endpoint's collision guard. Widened the query to an OR across both title prefixes and widened the regex to match either flow. Added verifyAppmakerPendingScaffoldPatternGuard.ts + .test.ts following the established narrow-textual-checker convention, wired into package.json and contract-tests.yml. Verified: new guard fails pre-fix / passes post-fix (git-stash round-trip), all 3 existing appmaker guards still pass, eslint clean, prettier clean, vue-tsc --noEmit repo-wide exit 0, git status --porcelain scoped to exactly 5 files. kind_robots PR #2027: all required CI checks green (only the standard non-required "Build production image" deploy job still in flight at merge time, matching established precedent), squash-merged f061397. Re-armed to ready would be the recurring-task convention, but closing as done this cycle per Silas's prior guidance that recurring "polish" tasks close threads via their own roadmap history -- see next cycle's kaizen note for the follow-up lead. Kaizen for next cycle: a fresh full-surface read of appmaker-page.vue and its server routes excluding every fix landed so far (including this one).
<!-- note:end t-012 -->

## t-013 — Audit other AppMaker fleet-list rendering for the same stale-literal description gap

<!-- note:begin t-013 -->
Kaizen from t-012's 2026-08-16 cycle (kind_robots PR #1913): the `fleet` computed in appmaker-page.vue showed a permanently blank card description for every real, registry-tracked app because `tasks.length === 0` was almost never true in practice (scripts/new_app.py always seeds 3 tasks), so the real per-app text (`project?.goal` / `project?.notesFromSilas`) never reached the UI. Fixed for the `fleet`/Apps card grid. Check whether the same page's "pending" apps list (apps still scaffolding, not yet in the registry) or any other conductorStore-driven list in this project has a similar stale-literal-over-real-data gap, and fix any found the same way. If nothing else is affected, close as a verified no-op rather than forcing a change.
<!-- note:end t-013 -->
