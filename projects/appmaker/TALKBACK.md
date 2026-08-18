# TALKBACK.md — appmaker

Cross-agent critique log for this project. Both Worker (OpenAI) and Reviewer (Claude)
append here. Never edit or delete prior entries.

For system-level observations that span projects, use the root `TALKBACK.md`.

**Format:**
```
## YYYY-MM-DD | <Worker|Reviewer> → <Reviewer|Worker> | <project>/<task-id> | <type>
type: critique | pattern | challenge | response | security-flag

**Subject:** one sentence
**Detail:**
- specific point with evidence
- reference to the diff, file, or decision that prompted this

**Suggested action:** what the other agent or Silas should do differently
```

## 2026-07-20 | Worker (scheduled) | appmaker/t-006 | done (no kind_robots change needed)

**Decision:** closed done (session claude-conductor-scheduled-20260720T0524Z).

**Failure category:** none — task was already satisfied, this session just confirmed and closed it.

**What was good:**
- Before assuming the task needed real work, ran `python scripts/sync_projects.py`
  live (this session had a working `KR_API_TOKEN` and reachable kind_robots API —
  not always true across sessions, per ai-art-academy's egress notes) and read its
  output rather than guessing: `appmaker: UNCHANGED (id=24)`.
- Verified what `UNCHANGED` actually proves before trusting it, rather than taking
  the string at face value: `sync_project()` only prints it when
  `find_project_by_slug` resolves the Project via `GET /api/projects/appmaker` AND
  every field in the freshly-computed payload — including `conductorSlug:
  "appmaker"` — already matches the existing record exactly. That is a genuine,
  code-level confirmation of slug parity, not an assumption.
- No kind_robots PR was needed since there was nothing to change; closed the
  conductor-only roadmap task with the verification evidence recorded in its note.

**What to improve:** none this cycle.

**Kaizen task:** none — this was a stale-task cleanup, not new scope.

## 2026-07-20 | Worker (burst) | appmaker/t-012 | partial progress (kind_robots PR #639 merged)

**Decision:** implemented step (2), self-verified, merged (session claude-conductor-burst-20260720T0920Z). Task kept `ready` — steps (1) and (3) still outstanding, not agent-actionable this cycle.

**Failure category:** none — clean first pass on the scoped piece.

**What was good:**
- Rotation: walked `priority.yaml` order past the top few candidates because they were genuinely
  blocked, not just picked the first `ready` hit. ai-art-academy/t-019 and t-035 both need the
  art-generation relay (confirmed still down — `public/images/academy/styles/` still doesn't exist
  in the local kind_robots checkout). serendipity/t-012 was claimed and merged by a different session
  minutes before this one started. superkate-hairstyle-ai/t-019 needs a live Comfy/Kontext box run.
  model-builder/t-022 and t-031 need live prod DB access / a healthy ArtJob relay. conductor-app's
  t-007/t-008/t-012 live in `apps/conductor/` (Flutter) with no Flutter/Dart SDK available in this
  sandbox to safely verify a blind edit, so skipped in favor of a task with real local tooling.
  appmaker/t-012 was the first genuinely unblocked, scoped, verifiable candidate.
- Before touching the placeholder-scaffold framing in the task's own note, checked
  `components/pages/appmaker-page.vue` directly (270 lines) instead of trusting the note's wording —
  it's already a full interactive experience (browse fleet, create-app form, project jump-in) shipped
  by appmaker/t-004, not a stub. Recorded that finding instead of re-building something that already
  exists.
- Verified before opening the PR: `npx eslint` on the changed file (clean) and full-project
  `npm run test` (`vue-tsc --noEmit`, exit 0) after provisioning kind_robots deps via
  `scripts/provision_kind_robots_deps.sh`. All 3 kind_robots PR checks green (TypeScript, Contract
  verifiers, GitGuardian) before merge.
- Hit the documented conductor-side first-push HTTP 413 on this session's own `claude/*` branch
  (brand-new ref) when pushing the `status: review` tracking commit — used the `create_branch`
  MCP-tool workaround per CLAUDE.md, which required one extra rebase since `main` had advanced by a
  `chore: refresh STATUS.md` commit between the branch-create call and the retry push.

**What to improve:** none this cycle.

**Kaizen task:** none this cycle — small scoped follow-up to an existing task pattern, not new scope.

## 2026-07-20 | Reviewer (scheduled conductor sweep) | appmaker/t-012 | pattern

**Decision:** none — collision discovered while merging conductor PR #900, not a new task action.

**Failure category:** transient (rotation collision, not a quality issue in either session's actual work).

**What was good/what happened:**
- A separate Reviewer-role session (conductor PR #900, opened 09:29:21, after the
  Worker-burst session above had already merged kind_robots PR #639 at 09:26:56) picked
  up the same already-open kind_robots PR #639, reviewed it, and wrote up its own
  progress note + TALKBACK entry believing *it* performed the merge — citing squash
  `419e6fa`, which does not match the PR's actual squash SHA (`da1a258b`, confirmed via
  the GitHub API). The kind_robots-side work itself was correct and only merged once;
  this was a documentation race, not a duplicate code change.
- Resolved the conductor-side merge conflict (PR #900 vs `main`) by keeping this file's
  and `roadmap.yaml`'s entries above (the accurate, verified record) and dropping the
  duplicate/inaccurate write-up rather than appending a second entry with a wrong SHA
  into the permanent log.

**What to improve:** Before a Reviewer session credits itself with merging a PR, verify
the actual merge response (or re-fetch the PR) rather than writing up the outcome from
memory/assumption — this is the same class of race as the `claim_task.py` rotation
collisions in AGENTS.md, just on the review/merge side instead of the claim side.

**Kaizen task:** none — existing `claim_task.py` machinery covers claims; a matching
"confirm you're not reviewing a PR someone else already merged seconds ago" check would
be the natural analog but is small enough to fold into normal Reviewer practice rather
than needing its own roadmap task.
## 2026-07-20 | Worker (agent run) | appmaker/t-011 | done (scripts/flag_stale_apps.py)

**Decision:** implemented, self-verified, set `status: review` (session claude-conductor-agentrun-20260720-appmaker-t011).

**Failure category:** none — clean first pass.

**What was good:**
- Checked how "bare" should actually be detected before writing anything: local `git log`
  per-path turned out to be unreliable in this sandbox's shallow/squash-merged clone
  (`apps/wishmaster` and `apps/appmaker` both showed exactly one, identical-timestamp
  commit locally, despite being scaffolded separately) — caught this by comparing two
  unrelated apps' histories rather than trusting the first result. Switched the age
  lookup to the GitHub REST API (`commits?path=...`), which reflects true history
  regardless of local clone depth.
- Detected bareness structurally (an exact-match "scaffolded by AppMaker" marker string
  in `lib/main.dart`, mirroring `scripts/new_app.py`'s own scaffold template) rather than
  by file count or a hardcoded per-project date list, so it stays correct for apps
  scaffolded outside `new_app.py` (the PR #104 batch) without needing per-project
  special-casing.
- Verified what could be verified locally (`py_compile`, structural bareness detection
  correctly finds 8/10 apps, correctly excludes the two genuinely built-out ones) and
  was explicit in the roadmap note about what couldn't be (the GitHub API call 403s from
  this interactive sandbox by org egress policy — same known limitation as the existing
  `scripts/check_repos.py`, not a bug in the new script) rather than either skipping
  verification silently or claiming full verification it didn't have.

**What to improve:** none this cycle.

**Kaizen task:** none — this task's own scope was the kaizen (from the PR #104 merge);
a natural next step if Silas wants it automatic is wiring `flag_stale_apps.py` into an
existing periodic workflow, left as a follow-up rather than expanding this task's diff.

## 2026-07-20 | Reviewer (agent run) | appmaker/t-008 | done (kind_robots PR #651 merged)

**Decision:** implemented and self-merged (session claude-conductor-agent-20260720T1535Z).

**Failure category:** none — clean first pass.

**What was good:**
- Read `GITHUB-APP-DESIGN.md` in full before writing anything, including §8's own task
  split (t-008 = models + connect flow + webhook; t-009 = installation tokens + write
  actions), and held to that boundary rather than building the whole design in one pass —
  installation-token minting and any GitHub write action were left out entirely, even
  though the shared `appmakerGithub.ts` utils file would have been a natural place to
  add them opportunistically.
- Delegated research into kind_robots' concrete conventions (Prisma multi-file schema
  style, the existing Stripe webhook's raw-body/HMAC pattern, `jose` already being the
  in-repo JWT library, `authGuard.ts`'s guard functions, the raw-`fetch` GitHub API
  pattern in `conductor-github.ts`) to an Explore agent against the live repo before
  writing code, then matched every one of those conventions exactly rather than
  inventing new patterns (e.g. reused `JWT_SECRET` for the state nonce instead of
  requesting a new secret Silas hadn't provisioned; hand-rolled HMAC with Node's
  `crypto` instead of adding a GitHub SDK dependency for one webhook route).
- No shadow database was available in this sandbox to run `prisma migrate dev`, so the
  additive migration SQL was hand-authored — checked column-by-column against the
  schema and byte-for-byte against the DDL conventions of the most recent comparable
  migration (`20260717103700_add_storefront_product_order_entitlement`) rather than
  guessing at Prisma's MySQL output format.
- Verified everything verifiable without a live GitHub round-trip: full-project
  `vue-tsc --noEmit` (0 errors), `eslint`/`prettier` clean on every changed file, and
  every contract check plausibly relevant to a new Prisma model + webhook route
  (Prisma JSON-cast, unquoted-reserved-table, capture-group-guard, and the
  known-migration-repair self-test) — explicitly checked whether the "Conductor API
  auth-guard contract" applied (it only scans `server/api/conductor/`, confirmed by
  reading the checker script, not assumed) rather than either skipping the check or
  wrongly adding an auth guard to `setup.get.ts`/`webhook.post.ts` that would have
  broken their actual auth model (state nonce / HMAC, not a session token).
- Explicitly flagged the one thing that couldn't be verified (a live install
  round-trip against real GitHub) in both the PR body and the roadmap note instead of
  claiming full verification.
- `t-009` was already filed in the roadmap (waiting on t-008) — ran `resolve_deps.py`
  rather than hand-flipping its status, which correctly unblocked it to `ready`.

**What to improve:** none this cycle.

**Kaizen task:** none filed — `appmaker/t-009` (installation-token minting + scaffold-PR
flow) already exists and is now unblocked; it's the correct next step, not a new kaizen.

## 2026-07-21 | Worker (conductor scheduled agent) | appmaker/t-009 | pattern

**Decision:** implemented, self-merged (session claude-conductor-agentrun-20260721T-appmaker).
kind_robots PR #812 merged (squash 801ed768).

**Failure category:** none — real work found, root-caused a genuine pre-existing CI issue
rather than burning a pass on it.

**What was good:**
- Built exactly the scope GITHUB-APP-DESIGN.md's §8 task table specs for t-009 — token
  minting (`mintInstallationToken`, cached, never returned by any API per §6 invariant 3),
  live granted-repo listing (`listInstallationRepositories`, needed since `AppRepo` alone
  only reflects repos already mapped to a slug, not what GitHub currently grants), and
  the branch/write/PR helper (`pushScaffoldBranchAndOpenPr`, hard-coded to `worker/*` +
  PR-only, never merge, per §5d). Did not build §5c (graduation) — that's t-010, correctly
  left alone.
- When the PR's own CI failed with a cryptic TS2589 "excessively deep" error in
  components/art/art-styler.vue — a file this task never touched — did not accept the
  easy read ("pre-existing, unrelated, ignore it"). First checked that read empirically
  (stashed the diff including untracked files, reran `npm run test` against a truly
  clean tree) and it reproduced there too, which looked like confirmation... but then
  cross-checked against real GitHub Actions history for the exact same commit (kind_robots
  PR #811, which became this PR's base) and found TypeScript had passed clean there. That
  contradiction was the signal that the local sandbox's clean-tree failure and the real
  CI failure had different causes, and it was worth digging further rather than trusting
  the first (wrong) local repro.
- Root-caused properly: the PR's 2 new server/api/appmaker/github/*.ts files grew the
  project's typed NitroFetchRequest route-key union just enough to push vue-tsc's
  recursion limit on ANY `$fetch` call with an uninferred/un-pinned R generic — a
  pre-existing, repo-wide fragility already sitting at the edge, not something isolated
  to art-styler.vue. Confirmed by fixing that one call site and watching the *next*
  file surface the identical error, repeatedly, until all 14 files that call `$fetch`
  directly (out of the whole app — most code goes through typed composables/stores) were
  checked and the 12 affected ones fixed by pinning `$fetch<T, string>(...)` (or plain
  `fetch()` for the handful of client-only static-asset reads). Verified the fix is real,
  not a band-aid: `npm run test` went from exit 2 to 0 errors, and CI (TypeScript +
  Contract verifiers) went green on the very next push.
- Checked whether this needed to block the merge at all: conductor/t-073 (still open,
  needs-human) already documents that kind_robots' branch protection does not require
  the "TypeScript" check to pass. Noted that fact in the roadmap note as relevant context
  but did not rely on it — fixed the real issue rather than merging around a non-required
  check, since a red TypeScript check is a real signal worth keeping green regardless of
  whether it's a hard merge gate.
- Filed kind-robots/t-042 (contract test for un-pinned `$fetch` generics) as the kaizen
  task so this ceiling gets a durable early-warning instead of relying on the next PR's
  author to independently rediscover and root-cause the same whack-a-mole chain.

**What to improve:**
- The 12-file `$fetch` fix touched components/pages/stores well outside appmaker's own
  surface. It was the right call (the alternative was merging on a broken TypeScript
  check or leaving t-009's own PR permanently red for a cause it triggered), but a future
  session hitting this same ceiling from a different PR should check kind-robots/t-042
  first rather than repeating the same discovery-by-compile-loop process from scratch.

**Kaizen task:** kind-robots/t-042 — contract test to catch un-pinned `$fetch` generics
before they can trip vue-tsc's TS2589 recursion ceiling again.

## 2026-08-16 | Agent (scheduled conductor sweep) | appmaker/t-012 | worker

**Decision:** done for this cycle -- found and fixed a genuine UX bug, merged in silasfelinus/kind_robots#1913 (squash c17902d). Rearmed to `ready` per recurring-task convention.

**What was good:**
- Delegated to a background agent with explicit context excluding the three already-fixed items (refreshToken sequencing, `fetchProjects(force)` in-flight sharing, slug-candidate validation) so it read the surface fresh.
- Found a real bug by checking an assumption against the actual data-seeding code (`scripts/new_app.py`) rather than taking the UI logic's condition at face value: `tasks.length === 0` looked like a reasonable "freshly scaffolded" check, but the scaffolder always seeds 3 tasks, so the condition was backwards in practice and silently hid real per-app description text (`project?.goal` / `notesFromSilas`) that the template already had a slot for.
- One CI job (`comment-contract`) failed on first push with a live-API 502 unrelated to this diff (`GET /api/characters` in `verifyPopulationDraftQuality.ts`); correctly diagnosed as transient rather than blaming the diff, reran just that job, confirmed it passes clean -- did not force a merge past it blind, and did not treat it as a reason to hold the otherwise-green PR.
- Extended the existing guard convention (`verifyAppmakerSlugCandidateGuard.ts`) rather than inventing a new pattern.

**What to improve:** none this cycle -- shipped end-to-end with full verification, diff matched intended scope, correctly triaged one transient CI flake without over- or under-reacting to it.

**Kaizen task:** `t-013` -- audit whether the same stale-literal-over-real-data pattern affects any other conductorStore-driven list on this page (e.g. the pending-apps list), not just the `fleet` computed this cycle covered.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-18 | Agent (scheduled conductor sweep) | appmaker/t-012 | worker

**Decision:** audited already-merged ground, found no new bug -- legitimate no-op this cycle. Re-armed `t-012` to `ready`. Filed `t-014` at soft `needs-human` for Silas.

**What happened:**
- Priority-order sweep found `mermaids-of-venice`, `model-builder`, `storybook`, `davinci`, and `alexa-integration` already cycled today by earlier sessions in this rotation, and `coat-dance/t-010` genuinely blocked on its source video (t-003). Walked to `appmaker/t-012`, 2 days stale and untouched today -- claimed it via `claim_task.py`.
- Delegated to a worktree-isolated background agent against a fresh `kind_robots` clone. It read `appmaker-page.vue`, `conductorStore.ts`, the appmaker server routes, and both existing guards (`verifyAppmakerSlugCandidateGuard.ts`, `verifyAppmakerFleetDescriptionGuard.ts`) in full, confirmed all four prior cycles' fixes still hold, and checked slug case-handling, `FREE_PROJECT_LIMIT` client/server consistency, pending-scaffold dedup, and loading/creating state gating. No new code bug found -- correctly did not fabricate a change or open a PR.
- It did surface a real discrepancy: `/appmaker` is `requiredRole: ADMIN` (enforced live by `middleware/navigation-access.global.ts`) so no non-admin can reach it, yet the page's own copy and `FREE_PROJECT_LIMIT` messaging still read as open self-serve, and `scaffold-request.post.ts`'s non-admin cap path is unreachable in production. It checked sibling plan-channel tabs (conductor-app, voice-lab, watchlist also ADMIN-gated; brainstorm, model-builder, coloring open) and correctly judged this as a probably-deliberate current-phase choice rather than a bug, and correctly declined to unilaterally decide an access-control/copy question that's outward-facing in effect.
- Filed `appmaker/t-014` (soft `needs-human`, `stakes: reversible`) with a FOR SILAS note laying out both options (keep admin-only + fix copy, or open the tab + sanity-check abuse surface first).

**What was good:** honest "nothing new found" outcome instead of manufacturing a change to justify the cycle; correctly distinguished a genuine code bug (in scope, would have fixed and shipped) from an access-control/product-copy mismatch (out of scope, escalated with both options laid out rather than picking one).

**What to improve:** none this cycle.

**Kaizen task:** `t-014` filed directly from this cycle's own finding (see above) rather than a generic suggestion -- the finding itself was the kaizen-worthy item.

---
_Generated by [Claude Code](https://claude.ai/code)_
