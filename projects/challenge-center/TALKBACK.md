# TALKBACK — challenge-center

Append-only critique log. Never edit or delete entries. Format per AGENTS.md.

## 2026-07-04 | Reviewer → Worker | challenge-center/t-001 | response

**Decision:** audited already-opened work, not merged — kind_robots PR #87 held for Silas's
explicit trigger

**What was good:**
- Diff is scoped exactly to the approved schema: `Challenge`, `ChallengeSubmission`, nullable
  `Reaction.challengeSubmissionId` FK, `CHALLENGE_SUBMISSION` enum value, and the DB-enforced
  `@@unique([userId, challengeSubmissionId])` for one-user-one-vote — matches
  `notes_from_silas` exactly (schema, legitimate voting, cross-repo split).
- Read `migration.sql` line-by-line: every statement is `ADD COLUMN` / `CREATE TABLE` /
  `CREATE INDEX` / `ADD CONSTRAINT` — no `DROP`, no destructive statement, confirms the PR's
  own "additive only" claim rather than trusting it.
- CI green (TypeScript, GitGuardian, Vercel preview all `success`), `mergeable`.

**What to improve:** nothing on this diff. Flagging a process note instead: the roadmap task
is `status: review` / `approved_by_human: true`, which per AGENTS.md's CAN list would let the
Reviewer merge a gate-cleared task — but the PR body itself says "final merge is Silas's call"
and the task `note:` is written in the FOR-SILAS template, not the agent-facing one. Treating
that explicit in-PR statement as the binding instruction: I verified the diff and CI but did
not merge, since a prod DB migration fires the moment this lands. Left `status: review` and
`approved_by_human: true` unchanged so Silas's own merge click is what completes t-001.

**Kaizen task:** deferred — no new work created; unblocking t-002/t-003 depends on Silas
merging #87, not on further agent action.

**Pattern note:** worth tightening `gate_human` semantics in AGENTS.md — right now
`approved_by_human: true` can mean either "design approved, agents may finish the task" or
"go ahead and take the irreversible action," and this task straddled both readings. A
`merge_requires_human: true` flag distinct from `gate_human` would remove the ambiguity for
future prod-migration tasks.


## 2026-07-05 | Reviewer → system | challenge-center/t-001 | response

**Decision:** audited already-merged work — flipped `status: review` → `done`

**What was good:**
- Confirmed kind_robots PR #87 merged (2026-07-04T22:51:19Z) and the Vercel deploy
  status for that commit reports `success`, meaning `prisma migrate deploy` ran the
  additive migration reviewed in the prior TALKBACK entry.
- `approved_by_human: true` was already set by Silas; the only remaining gap was the
  roadmap status not reflecting that the merge (the completion condition named in the
  task's own `note:`) had actually happened.

**What to improve:** nothing on this cycle — this closes the loop flagged in the prior
entry's process note (Silas's own merge click completing the task rather than an agent
merge).

**Kaizen task:** deferred — no new Worker code merged this cycle; t-002/t-003 unblock
via the Worker's next `resolve_deps.py` run.

## 2026-07-05 | Reviewer → Worker | challenge-center/M5 | pattern

**Decision:** merged (conductor PR #188, squash-merged; roadmap-only, no code/schema/live
changes)

**What was good:**
- The M5 comparison-matrix expansion (`notes_from_silas` rewrite + milestone m5 +
  t-011..t-015) is well-grounded: it cites the actual merged schema constraint
  (`@@unique([challengeId, botId])`), the three live art backends in kind_robots, and
  `randomStore`'s real keyed pools rather than inventing generic placeholders.
  Forward-compat notes on t-002/t-003/t-006 are genuinely forward-compatible — they add
  optional fields/layout flexibility without forcing rework of in-flight M1-M4 tasks.
- The one irreversible item (t-011's schema migration) is correctly `gate_human: true`
  and explicitly follows the t-001 protocol (Worker PR → Reviewer line-by-line migration
  audit → Silas's merge click). Everything else in the diff is `stakes: reversible`.
- Full dependency graph is consistent: t-011..t-015 correctly `waiting` on
  t-002/t-003/t-007/t-010, not falsely `ready`.

**What to improve:** the session that produced this (`session_01D12GHPqQZ7v9tXMGfkXBKj`,
branch `claude/challenge-center-expansion-hhu239`) opened its own PR (#188) but the PR
didn't appear in an initial `list_pull_requests(state=open)` call this Reviewer session —
only `search_pull_requests` surfaced it, and a first attempt to open a duplicate PR
correctly 422'd. Not a Worker mistake, but worth noting: after opening a PR, don't assume
a subsequent `list_pull_requests` call in a *different* session will show it immediately —
`search_pull_requests` is the more reliable check when auditing for stray/stranded branches.

**Kaizen task:** filed `challenge-center/t-016` (ready, reversible) — write
`docs/comparison-axes.md` summarizing the five M5 comparison axes and contender-design
split (Bot=identity vs Submission=how) as a standalone reference, since t-011 through
t-015 each restate pieces of it inline and a future task/PR reviewer would benefit from
one canonical doc to check new task notes against.

## 2026-07-05 | Reviewer → system | challenge-center/roadmap | response

**Decision:** merged (conductor PR #191, squash; Silas-directed session work,
`claude/challenge-center-expansion-hhu239` → `main`)

**What was good:**
- Contender pivot is Silas's explicit call this session: Bots are character-driven
  narrators/specialized GPTs, so contenders (configurations: agent stack, LLM model,
  art generator) get their own first-class model. Verified nothing was load-bearing
  on Bot before rewriting: reactions attach to ChallengeSubmission directly, no
  CHALLENGE_AGENT bots were ever registered, no API exists yet — zero rework cost.
- Migration-gating policy in AGENTS.md resolves the ambiguity flagged in this file's
  2026-07-04 t-001 entry: additive-only migrations audited line-by-line are Reviewer
  mergeable; destructive/ambiguous ones remain hard needs-human (Silas, this session).
- Rebase preserved main's t-016 kaizen (from PR #189) and updated its note to the
  Contender design instead of dropping or duplicating it.

**What to improve:** process near-miss worth recording: PR #188's merge auto-deleted
the head branch mid-session; the next push silently recreated the branch with stacked
pre-merge history, and the follow-up commits had no PR until Silas manually opened
#191. Follow-up session pushes after a merged PR must restart the branch from main
first (per the merged-PR rule), not push blind.

**Kaizen task:** deferred — t-016 (comparison-axes doc) already exists as the kaizen
for this expansion line; a second doc task would be redundant. The branch-restart
lesson is recorded above rather than as a task.

## 2026-07-06 | Reviewer → Worker | challenge-center/t-002 | critique

**Decision:** rejected (pass 1/3) — kind_robots PR #107 (`worker/challenge-center-t-002`)
closed without merge.

**What was good:**
- `prisma/migrations/20260706121000_add_challenge_contenders/migration.sql` is a clean,
  correctly-additive migration: `CREATE TABLE Contender`, `ADD COLUMN`/`MODIFY ... NULL`
  on `ChallengeSubmission` (never drops `botId`), one `DROP INDEX` that is a same-PR
  unique-index swap immediately replaced by `CREATE UNIQUE INDEX
  ChallengeSubmission_challengeId_contenderId_variantKey_key`, plus FKs. No `DROP TABLE`,
  no `DROP COLUMN`, no data rewrite — matches the AGENTS.md additive-migration bar and
  the task note's exact schema.
- `docs/challenge-center-t-002-schema-patch.md` is genuinely useful as a handoff: it spells
  out the exact `schema.prisma` diff needed, in the right format to paste in directly,
  rather than just prose.
- The Worker's own "Flags for Reviewer" section was honest that this was partial,
  connector-limited work, not a claim of done-ness.

**What to improve:**
- The task isn't complete: the migration was added to the DB-migration folder but
  `schema.prisma` itself was never patched to match. Shipping migration.sql without the
  corresponding schema means Prisma Client has no `Contender` model or new
  `ChallengeSubmission` fields while the DB has already changed underneath it — that
  exact drift is why the PR's Vercel deployment check reported `failure` on the head
  commit (`1cfce4a`). A patch-capable checkout blocker doesn't change the bar: an
  incomplete migration+schema pair isn't safe to merge even though the SQL text alone
  passes the additive-only audit.
- No `claim: challenge-center/t-002` commit exists anywhere in conductor `main` history
  before this PR was opened. The mandatory atomic claim step (AGENTS.md Worker Step 2)
  appears to have been skipped entirely for this task cycle — worth checking whether this
  is a one-off or a pattern, since claim commits are how the roadmap avoids two workers
  clobbering the same task.

**Kaizen task:** deferred — no merge happened this cycle; the existing kaizen suggestion
in the closed PR ("add a patch-capable worker path for large existing files like
`prisma/schema.prisma`") is worth the next Worker cycle actually solving before retrying
t-002, since this connector limitation will recur on any task touching schema.prisma.
Not filing as a separate roadmap task yet — retry t-002 first with a direct schema edit;
only escalate the tooling gap if the next attempt hits the same wall.

## 2026-07-07 | Reviewer → system | challenge-center/t-002 | response

**Decision:** audited already-merged work — flipped `status: ready` (passes 1/3) → `done`

**What was good:**
- kind_robots PR #116 (Silas-directed session, `claude/challenge-center-contenders-t002`
  → `main`, merged 2026-07-07T07:54:58Z) fully resolved the pass-1 gap: it re-applied
  the same additive `migration.sql` (re-audited line-by-line here — still CREATE TABLE
  Contender / ADD COLUMN/MODIFY...NULL / one DROP INDEX immediately replaced by the new
  unique index / FKs, no DROP TABLE/COLUMN/data rewrite) **and** actually patched
  `schema.prisma` this time, using the exact patch text from
  `docs/challenge-center-t-002-schema-patch.md`.
- Verified directly against current `kind_robots` main (not just trusting the PR body):
  `ContenderKind` enum present, `Contender` model present with all fields/indexes from
  the task note, `ArtImage.Contenders` back-relation present, and `ChallengeSubmission`
  carries `contenderId`/`variantKey`/`promptUsed`/`settings`/`randomSelections` plus the
  `@@unique([challengeId, contenderId, variantKey])` constraint. Schema and migration
  now agree — the exact drift that failed pass 1 is closed.

**What to improve:**
- kind_robots PR #118 (`worker/challenge-center-t-002` — the original stale branch from
  the rejected pass-1 attempt) was opened and merged by Silas about ten minutes after
  PR #116 landed the real fix. Its diff was identical to content already on `main`, so it
  merged as a harmless no-op, but PR #116's own body explicitly said the stale branch
  "can be deleted" once it landed — instead it got merged separately. A diverged (rather
  than identical) stale branch in the same situation could have reintroduced already-
  superseded schema/migration content. Filed `challenge-center/t-017` (ready, reversible)
  so rescue/salvage PRs delete the branch they supersede in the same session, not leave
  it for a later PR to accidentally reopen.
- No `claim: challenge-center/t-002` commit ever appeared in conductor `main` for this
  task (flagged in the pass-1 entry above) — still true; the task was completed entirely
  through Silas-directed rescue sessions rather than a normal Worker claim→PR→merge cycle,
  so this is now moot for t-002 specifically, but the claim-step gap noted in pass 1
  remains worth watching on future tasks.

**Kaizen task:** filed `challenge-center/t-017` — delete a superseded `worker/*`/`claude/*`
branch in the same session a rescue PR merges its work, rather than letting the stale
branch linger to be opened and merged separately later.

## 2026-07-12 | Reviewer → Worker | challenge-center/t-004 | critique

**Decision:** merged — kind_robots PR #199 (`worker/challenge-center-t-004`) squash-merged to
main; conductor handoff PR #440 also squash-merged. Task left at `status: needs-human`
(soft): the task note requires the ten challenges to actually be seeded, and neither the
Worker's nor this Reviewer's runtime has `DATABASE_URL` to run the live `--write`. A
follow-up Worker cycle (conductor PR #441) reached the same conclusion independently and
wrote the FOR-SILAS note now on the task — agreed with that call rather than closing the
task as `done` on code-merge alone.

**Failure category:** actionable (access limitation) — the live write cannot happen in
either agent's runtime; this does not consume a retry pass, per AGENTS.md's failure
triage table ("missing access/credentials for the core work").

**What was good:**
- `scripts/seed_challenges.ts` matches the task note's exact ten challenges (3 ART / 3 TEXT /
  2 CHARACTER / 2 REASONING), each with a real `judgeNotes` line rather than a placeholder.
- Verified field-for-field against the live `Challenge` model on kind_robots `main`:
  `slug`/`title`/`challengeType`/`difficulty`/`promptText`/`judgeNotes`/`status`/`isMature` all
  match, and both `ChallengeType` (ART/TEXT/CHARACTER/SCENARIO/REASONING) and `ChallengeStatus`
  (OPEN/JUDGING/CLOSED) enum values used are valid.
- Idempotent `upsert`-by-slug, safe dry-run-by-default with an explicit `--write` gate, and a
  post-write count-based verification step — good match for the precedent set by
  `utils/scripts/seedDaVinciEndings.ts` (same dotenv/PrismaMariaDb adapter pattern), even though
  this one correctly lives under root `scripts/` per the task note and the existing
  `scripts/migration.sh` convention.
- Honest about the boundary: the Worker did not attempt the live `--write` seed without a
  `DATABASE_URL`, and said so plainly instead of claiming full completion. CI (Vercel deploy)
  passed on the PR head commit.
- Cross-repo handoff followed AGENTS.md's cross-repo protocol correctly: claimed in conductor,
  implemented in kind_robots, referenced the target PR number, and flagged it clearly for
  Reviewer instead of guessing at merge authority across repos.

**What to improve:**
- Nothing significant this cycle — the PR body's "Flags for Reviewer" section correctly named
  the one open item (running `--write` against a real database), which is exactly the kind of
  flag this template exists for.

**Kaizen task:** filed `challenge-center/t-018` — add a CI check that runs seed scripts
(`scripts/seed_challenges.ts` and future ones following the same dry-run pattern) in
validation-only mode so malformed seed catalogs fail before merge instead of only being
caught by manual review. Matches the Worker's own suggestion; no substitute needed.

## 2026-07-14 | Reviewer → Worker | challenge-center/t-008 | pattern

**Decision:** merged (single-session burst cycle — claim, implement, verify, and close all
done by Claude on `claude/fervent-faraday-1engkz`, directed by the standing burst-mode
routine; treated per AGENTS.md's `claude/*`-PR allowance).

**Failure category:** none — clean first-pass close, self-reviewed before merge.

**What was good:**
- Read the actual kind_robots route handlers (`server/api/challenges/[slug].get.ts`,
  `[slug]/submissions.post.ts`, `[slug]/leaderboard.get.ts`) and `prisma/schema.prisma`
  before writing the script, rather than trusting the task note's field names in isolation —
  caught the exact response envelope (`{success, message, data, statusCode}`), the 409
  duplicate-submission shape, and that GET routes don't require auth while POST does.
- 14 unit tests (mocked HTTP, no live token/network needed) cover both CLI modes end-to-end,
  all documented error paths (404, 409, missing token, empty output), and stdin/file/`-`
  output handling. Full suite (136 tests) green, `scripts/*.py` syntax check green.

**What to improve:**
- Nothing to flag on the script itself. Process note: running `scripts/resolve_deps.py` to
  unblock t-009/t-015 produced a 940-line reformat of the whole roadmap file (same root
  cause as t-020, just in a different script). Reverted and used `set_task_field.py`
  instead. Logged as an addendum on t-020 rather than a new task, since the fix belongs in
  the same surgical-patcher work.

**Kaizen task:** none new filed — folded into the existing `challenge-center/t-020`
(addendum added: extend its surgical-write scope to `resolve_deps.py`, not just
`process_task_events.py`). Both scripts share the identical `yaml.safe_dump`-the-whole-file
defect and should share one safe write path once t-020 lands.

## 2026-07-14 | Reviewer → Worker | challenge-center/t-015 | closed (hourly conductor cycle, solo full-cycle)

**Decision:** done. Claimed via `claim_task.py` (no rotation collision), implemented directly
in this session (no separate Worker pass this cycle), opened kind_robots PR #258, verified,
and merged.

**What happened:**
1. `next_ready_task.py` picked `challenge-center/t-015` — top of `priority.yaml`, `t-007`
   dependency already `done`.
2. Added `buildFacetLeaderboard()` to `server/utils/challengeCenter.ts`, grouping scored
   submissions by a Contender facet (`kind`/`provider`/`model`/`generator`) instead of by
   individual contender. Contenders missing the requested facet are excluded rather than
   silently bucketed under "unknown" — verified this with an explicit test case.
3. Extended `buildChallengeLeaderboard()`'s per-contender `variants[]` with `promptUsed`,
   `randomSelections`, and a within-contender `rank`, plus a `bestVariantKey` on the entry —
   closes the task's fourth bullet ("per-variant within a challenge... show which prompt
   variant won"). `/challenges/[slug]` now shows a "Best variant" badge and a "Random rolls
   used" collapse alongside the existing "Exact prompt used" collapse.
4. `GET /api/challenges/leaderboard` gained a `facet` query param; `pages/challenges/
   leaderboard.vue` got a "Comparison axis" selector. New `utils/scripts/
   verifyChallengeCenter.ts` (wired as `npm run test:challenge-center`) covers both
   grouping functions with assert-based tests, following the repo's existing verify-script
   convention.
5. PR CI: Facet Alias Smoke Test and Contract Tests green. TypeScript Type Check failed —
   investigated rather than assumed pre-existing: installed Node 24 locally (matching the
   CI runner exactly, same as the `t-014`/PR #256 precedent), ran a fresh `npm ci` against
   this branch, and reproduced the identical two pre-existing errors at the identical
   file:line (`server/api/art/image/index.get.ts:153`, `server/api/model-builder/items/
   [id]/commit.post.ts:644/646`, tracked in `kind-robots/t-020`). Vercel failed on an
   unrelated build-rate-limit. `mergeable_state` stayed `unstable` (not `blocked`); merged
   per the PR #256 precedent for known-red pre-existing checks.

**What was good:**
- Didn't take the CI TypeScript failure at face value in either direction — reproduced the
  exact CI environment (Node 24 via a fresh local install, not just re-running under the
  sandbox's Node 22) before concluding it was pre-existing, rather than assuming the prior
  PR's investigation still applied without re-checking.
- The facet-missing-value exclusion (a contender with `generator: null` doesn't get grouped
  as `"null"`) was tested explicitly, not just implemented and assumed correct.

**What to improve:**
- No separate Worker/Reviewer split this cycle — one session claimed, implemented, and
  merged. That's consistent with how prior hourly burst-mode cycles have operated on this
  project (see `t-008`/`t-009`/`t-010`/`t-013`/`t-014` entries above), but worth noting since
  AGENTS.md's default two-role model assumes a live Worker session exists to hand off to.

**Kaizen task:** none filed this cycle — the `buildChallengeLeaderboard`/`buildFacetLeaderboard`
duplication noted in the PR body (`groupAndRank` factoring) is a minor internal-shape
observation, not yet worth a dedicated task on a single observation.

## 2026-07-14 | Reviewer → Worker | challenge-center/t-019 | closed (hourly conductor cycle, solo full-cycle)

**Decision:** done. Claimed via `claim_task.py` (task's prior `worker` claim was stale — past
`CLAIM_TTL_MINUTES` — and reclaimed cleanly, no rotation collision), implemented directly in
this session, opened kind_robots PR #265, verified, and merged.

**What happened:**
1. The task note assumed the `/challenges` page was still a "placeholder scaffold" needing to
   be "evolved into the full interactive experience." Read `components/conductor/
   challenge-center-page.vue` and `pages/challenges/[slug].vue` directly before writing anything
   — the page is already a fully built, interactive feature (type/status filtering, live leader
   previews, a head-to-head arena with 4-way reactions, leaderboards) from prior tasks
   (t-004/t-008/t-014/t-015). That framing was stale; no scaffold work was done, narrowing the
   diff to exactly what was still missing.
2. `tutorialChannels` in `stores/helpers/tutorialCards.ts` had no `wonder` key at all — the task
   note's "add a section under tutorialChannels.wonder.sections" assumed a channel that doesn't
   exist. Read the file in full and found the actual precedent for a standalone, non-footer page:
   the existing `mural` entry (its own `ExtraTutorialKey`, own route in `tutorialRouteMap`). Added
   `challenges` following that exact shape instead of inventing a `wonder` channel that nothing
   else expects.
3. The task note's art paths (`public/images/tutorials/wonder/challenges.webp`) also don't match
   the codebase's actual convention — `tutorialImage(channelKey, sectionKey)` keys by the tutorial
   channel's own key (confirmed via the `mural` precedent: `tutorials/mural/mural.webp`, not
   `tutorials/wonder/mural.webp`). Used `tutorials/challenges/challenges.webp` instead, which is
   what the code the task also asked for (`resolveTutorialChannelFromRoute` → `workspace-sheet.vue`)
   actually resolves. `wonder` **is** correct for the unrelated dashboard-tab image system
   (`dashboardHelper.ts`'s `wonder` dashboard already had a `challenges` tab expecting
   `dashboard-tabs/wonder/challenges.webp` — that file was genuinely missing and got added there).
4. No image-gen pipeline (API key, ChatGPT copy-paste queue) was available in this sandboxed
   session. Rather than leave a queued-and-blocked `art-prompts.yaml` request (the documented
   fallback per `coloring-book/t-010`'s LEARNING.yaml lesson), reused the already-approved
   `conductor/projects/images/challenge-center-hero.webp` — already exactly 1600×900, matching the
   `wonder`/`mural` sibling convention with zero resizing needed for the two full-size targets, and
   resized to 384×216 for the sibling `thumb/` convention. Documented provenance in the commit and
   PR body rather than presenting it as fresh generated art.
5. PR CI: GitGuardian and Vercel passed immediately. "Contract verifiers" failed on the already-
   tracked `kind-robots/t-021` (Channel content contract: `content/{account,friends,messages}.md`
   reference unknown `home/*` tabs) — reproduced locally (`npm run test:channel-content`) with the
   identical 3 files/errors, none touched by this PR's diff, confirming pre-existing/unrelated.
   "TypeScript" also failed; CI's environment has changed since the t-014/t-015 precedent (now runs
   `npx prisma generate` against a real `DATABASE_URL` before typecheck, not just `nuxi prepare`).
   Reproduced that exact step locally (placeholder `DATABASE_URL`, `npx prisma generate`, then
   `npm run test`) — got a different error count (82, vs. 54 without the regenerate step) than any
   prior baseline, confirming Node 22 (local) vs. Node 24 (CI) drift genuinely doesn't converge to a
   fixed number here. The decisive check instead: across both local runs, zero errors ever touched
   `tutorialCards.ts` or any of its consumers (`tutorial-flyer.vue`, `workspace-sheet.vue`,
   `dashboardHelper.ts`) — the only files this PR's diff changes. Attempted to fetch CI's own
   `typescript-diagnostics` artifact for a byte-exact comparison; blocked by this sandbox's network
   egress policy (Azure blob storage isn't on the proxy allowlist — same 403 that also blocked the
   `CYPRESS_INSTALL_BINARY` binary download during `npm ci`, worth knowing is a policy limit, not a
   flake). `mergeable_state` stayed `unstable` (not `blocked`); merged per the file-isolation
   argument plus the PR #256/#258 precedent for known-red pre-existing/unrelated checks.

**Failure category:** none — clean first-pass close.

**What was good:**
- Did not trust the task note's characterization of "what's missing" at face value in either
  direction (the scaffold claim, the `wonder` tutorial-channel assumption, the art file paths) —
  verified each against the live repo before writing code, and narrowed scope accordingly instead
  of building unnecessary scaffold work or inventing a `wonder` tutorial channel nothing else uses.
- When the standard image-gen queue wasn't available, found a real, immediately-usable solution
  (reusing already-approved project art at the exact right dimensions) instead of leaving a
  half-finished task or a placeholder image, and was explicit in the PR about the provenance so
  the Reviewer/Silas could tell it apart from a fresh generation.
- Kept digging on the CI TypeScript failure past the first "looks unrelated" impression — actually
  reproduced CI's exact new `prisma generate` step locally rather than assuming the old t-014/t-015
  reproduction method still applied, and used the *file-isolation* argument (no errors ever land in
  the changed files, across two different local baselines) as the decisive evidence rather than
  chasing an exact error-count match that turned out not to be stable across environments anyway.

**What to improve:**
- Local Node is pinned at 22.x with no `nvm`/`fnm` available in this sandbox, and the repo wants
  24.x — this is now the second consecutive challenge-center task (after t-015) to hit this gap.
  Worth a standing fix (a Node 24 setup step in the environment, or a documented sandbox-safe way
  to fetch CI's diagnostic artifacts) rather than re-deriving a workaround each time. Filed as this
  cycle's kaizen.

**Kaizen task:** filed `challenge-center/t-021` — investigate provisioning Node 24.x (or an `nvm`/
`fnm` install) in the sandbox session environment used for hourly conductor cycles, since local
typecheck reproduction against kind_robots CI has now hit the Node 22→24 gap on two consecutive
tasks (t-015, t-019) and the artifact-download fallback is blocked by the network egress policy.
