# challenge-center — task history archive

Full `note:` prose for completed challenge-center tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Add Challenge and ChallengeSubmission Prisma models to kind_robots

<!-- note:begin t-001 -->
Complete: kind_robots PR #87 merged 2026-07-04 (Vercel deploy succeeded), which ran the additive migration (Challenge + ChallengeSubmission tables, CHALLENGE_SUBMISSION reaction category, nullable Reaction FK, DB-enforced unique (userId, challengeSubmissionId)). Unblocks t-002 (originally Bot registration, since redefined as the Contender migration — see its note) once the Worker's next cycle runs resolve_deps.py.
<!-- note:end t-001 -->

## t-002 — Schema: add Contender model and submission variant fields

<!-- note:begin t-002 -->
SUPERSEDES the original "register Bots" task (Silas, 2026-07-05): Bots are character-driven narrators and specialized GPTs — contenders get their own model. In silasfelinus/kind_robots, one additive migration:

  model Contender:
    id, createdAt, updatedAt
    slug            String  @unique @db.VarChar(255)
    name            String  @db.VarChar(255)
    kind            ContenderKind  (AGENT_STACK | LLM_MODEL | ART_GENERATOR)
    provider        String? @db.VarChar(128)   // anthropic | openai | local...
    model           String? @db.VarChar(255)   // claude-fable-5, gpt-5...
    generator       String? @db.VarChar(128)   // claude-api | openai-api |
                                               // art-sd | comfy-flux | ...
    defaultSettings Json?
    description     String? @db.Text
    avatarImageId   Int?    (FK → ArtImage, nullable)
    isActive        Boolean @default(true)

  ChallengeSubmission additions:
    contenderId      Int?  (FK → Contender; required in app logic, nullable
                            in DB only so the migration is additive)
    variantKey       String @default("default") @db.VarChar(128)
      — distinguishes multiple entries by one contender in one challenge
        ("terse", "detailed", "random-3", "temp-0.2")
    promptUsed       String? @db.Text   // exact final prompt sent
    settings         Json?              // overrides of defaultSettings
    randomSelections Json?              // randomStore key→value map used
    @@unique([challengeId, contenderId, variantKey])

  Deprecate botId: make it nullable, keep the column (never DROP data),
  stop writing it. Remove or keep the old (challengeId, botId) unique —
  if removed, verify the migration is only DROP INDEX, not DROP COLUMN.

No CHALLENGE_AGENT bots were ever registered and no API exists yet, so this pivot has zero data to migrate. NOT human-gated (Silas, 2026-07-05): this is additive-only, so per the AGENTS.md migration rule the Worker opens the PR and the Reviewer audits migration.sql line-by-line and merges it — Silas is not a gate. If the generated migration turns out to contain any destructive statement, it reverts to hard needs-human.
REVIEWER (pass 1/3, 2026-07-06): kind_robots PR #107 closed without merge. migration.sql itself is a clean additive migration (audited line-by-line), but the PR never applied the matching schema.prisma patch — it only left docs/challenge-center-t-002-schema-patch.md describing what schema.prisma needs. That drift is why the PR's Vercel deployment check failed. Next attempt must include the actual schema.prisma edit (Contender model, ContenderKind enum, ArtImage.Contenders relation, ChallengeSubmission field/relation additions — see the doc above for the exact patch) in the same PR, then `npx prisma validate && npx prisma generate` before opening for review again. Also: no `claim: challenge-center/t-002` commit was found on conductor main before this PR was opened — make sure the claim step actually runs.
REVIEWER (resolved, 2026-07-07): kind_robots PR #116 (Silas-directed session, `claude/challenge-center-contenders-t002` → main, merged 2026-07-07T07:54:58Z) rebuilt the stranded work cleanly on current main: applied the exact migration.sql from the original branch verbatim (re-audited line-by-line — still additive-only: CREATE TABLE Contender, ADD COLUMN/MODIFY...NULL on ChallengeSubmission, one DROP INDEX immediately replaced by the new unique index, plus FKs; no DROP TABLE/COLUMN/data rewrite) AND applied the schema.prisma patch from docs/challenge-center-t-002-schema-patch.md (ContenderKind enum, Contender model, ArtImage.Contenders relation, ChallengeSubmission field/relation/index additions). Confirmed directly against current kind_robots main: schema.prisma now matches migration.sql exactly (Contender model, enum, and all ChallengeSubmission fields present). Note: kind_robots PR #118 (`worker/challenge-center-t-002`, the original stale branch) was also merged ~10 minutes later by Silas directly; its diff was identical/already-superseded content so it landed as a no-op, but the stale branch should have been deleted per PR #116's own note instead of being merged separately afterward (see t-017, filed as this cycle's kaizen). Task is genuinely complete now — t-003, t-005, t-008, t-012, and t-014 all unblock via the Worker's next `resolve_deps.py` run.
<!-- note:end t-002 -->

## t-003 — Create /api/challenges CRUD and submission routes in kind_robots

<!-- note:begin t-003 -->
In silasfelinus/kind_robots, add API routes under server/api/challenges/. Builds against Contender from day one (t-002) — nothing references Bot.

  GET  /api/challenges         — list open challenges (filter: type, status)
  GET  /api/challenges/[slug]  — one challenge with submissions and scores
  POST /api/challenges         — create challenge (admin only)
  GET  /api/contenders         — list active contenders (filter: kind)

  POST /api/challenges/[slug]/submissions
    body: { contenderSlug, variantKey?, promptUsed?, settings?,
            randomSelections?, outputText?, artImageId?, characterId? }
    creates ChallengeSubmission, sets status: READY
    returns submission id
    rejects a duplicate (challenge, contender, variantKey) with a clear error

  GET  /api/challenges/[slug]/leaderboard
    returns contenders ranked by net score (loved+clapped - booed-hated);
    a contender with multiple variants aggregates across them, with a
    per-variant breakdown included

  GET  /api/challenges/leaderboard
    global leaderboard: aggregate scores across all challenges per Contender

Use existing auth/session patterns from kind_robots. Script submissions should be accepted with an API key (reuse Server.apiKey pattern or a new env var). Leaderboard responses group by contenderId, never by raw submission row, so variant rows aggregate cleanly.

DONE (Reviewer verification, 2026-07-11): the full API surface already exists on kind_robots main and was verified endpoint-by-endpoint against this spec — list with type/status filters, slug detail with per-submission scores, admin-only create (403 gate), active-contender list with kind filter, API-key-authenticated submissions (validateApiKey) that set READY and reject (challenge, contender, variantKey) duplicates with a clear 409, and both leaderboards ranked by net score with per-variant breakdowns grouped by contenderId (server/utils/challengeCenter.ts). No new work needed; closed by verification alone. t-004 and t-005 unblock via the Worker's next resolve_deps.py run.
<!-- note:end t-003 -->

## t-006 — Build /challenges/[slug] voting page in kind_robots

<!-- note:begin t-006 -->
DONE (bookkeeping reconciliation, 2026-07-14): kind_robots PR #210 ("challenge-center: build the logged-in voting arena") merged this task 2026-07-13T00:52:11Z — a /challenges/[slug] arena with VS split (2 submissions) / select-screen grid (3+), ART/TEXT/Character/Scenario rendering, logged-in LOVED/CLAPPED/BOOED/HATED reactions via POST /api/challenges/submissions/[id]/reaction enforcing the (userId, challengeSubmissionId) unique key, and a per-challenge mini leaderboard. Contract Tests and the whole-project vue-tsc check passed; Vercel build completed. The roadmap task itself was left at claimed for ~25h with the claim timestamp unchanged and zero worker/* branch/commit/PR anywhere in that window (confirmed via list_branches + list_commits across many Reviewer sweeps, see conductor TALKBACK.md recurrences 42-48 under t-026) — a stale-claim/bookkeeping-drift case per docs/worker-stale-claim-recovery.md, not a still-open task. Reconciled directly against the merged PR as authoritative evidence.
Original task spec: Challenge detail page. Show the challenge prompt and judgeNotes at top. Below: all submissions side by side (or stacked on mobile). Each submission card shows: contender name/avatar (from Contender), the output (art image or text block), and reaction buttons (LOVED/CLAPPED/BOOED/HATED) using the existing KR Reaction component — category: CHALLENGE_SUBMISSION. Voting requires a logged-in user; the DB enforces one reaction per user per submission (unique userId+challengeSubmissionId), so tallies are legitimate. Show net score and current rank on each card once scored. For ART challenges, render the ArtImage thumbnail. For TEXT challenges, render the outputText with a read-more expander. For CHARACTER challenges, render the Character card. DESIGN DIRECTION (Silas): this is the VS screen — submissions face off side by side like a title bout, agent avatars as fighter portraits. See notes_from_silas. Design the layout for N contenders, not exactly two: a duel renders as the classic VS split, 3+ renders as a select-screen grid. M5 matchups (model-vs-model, generator-vs-generator, prompt-variant grids) reuse this page unchanged.
<!-- note:end t-006 -->

## t-007 — Build leaderboard page in kind_robots

<!-- note:begin t-007 -->
Add /challenges/leaderboard page. Two views:
  - Global: top agents by total net score across all challenges (table/podium)
  - Per-type: filter to ART/TEXT/CHARACTER etc., show rankings for that type
Contender row shows: avatar, name, challenges attempted, challenges won, total score, win rate. Also show on each /challenges/[slug] page: a mini leaderboard for that challenge. Link back to /challenges browser. DESIGN DIRECTION (Silas): championship presentation — podium, belts, win records, fighter cards. See notes_from_silas.

Reviewer note 2026-07-14: Silas built this directly in kind_robots
(commit 98fb8e01, "challenge-center: build championship leaderboard",
merged to main). Verified pages/challenges/leaderboard.vue covers both
global and per-type (ART/TEXT/CHARACTER/SCENARIO/REASONING) views with
podium/championship styling, and server/api/challenges/[slug]/leaderboard.get.ts
+ pages/challenges/[slug].vue provide the per-challenge mini leaderboard.
Marking done to prevent the Worker from duplicating already-shipped work.


Kind Robots PR
<!-- note:end t-007 -->

## t-008 — Write scripts/challenge_submit.py in conductor

<!-- note:begin t-008 -->
In silasfelinus/conductor, write scripts/challenge_submit.py. Usage: python scripts/challenge_submit.py <challenge-slug> [--contender conductor-claude] Steps:
  1. Fetch challenge from KR API (GET /api/challenges/<slug>)
  2. Print promptText to stdout / pipe to agent
  3. Accept agent output via stdin or --output flag
  4. POST to /api/challenges/<slug>/submissions with contender slug + output
  5. Print submission id and current leaderboard standing
Reads KR_API_TOKEN and KR_BASE_URL from env. This becomes the bridge between conductor agent runs and the challenge system.

DONE (2026-07-14, single-session burst cycle): added scripts/challenge_submit.py per
spec above. GET /api/challenges/<slug>, print promptText only when --output is omitted
(prompt-only mode, so it pipes cleanly to an agent); accept the agent's answer via
--output <file>|-; POST /api/challenges/<slug>/submissions with contenderSlug (default
conductor-claude, matching kind_robots scripts/seed_contenders.ts)/variantKey/
outputText/promptUsed; print the created submission id and this contender's current
leaderboard rank via GET /api/challenges/<slug>/leaderboard. Verified request/response
shapes directly against kind_robots main (server/api/challenges/[slug].get.ts,
[slug]/submissions.post.ts, [slug]/leaderboard.get.ts, prisma/schema.prisma
Challenge/ChallengeSubmission models) rather than assuming from the task note alone.
14 unit tests added in tests/test_challenge_submit.py (mocked HTTP, no live token
needed): fetch/submit/leaderboard success and error paths (404, 409 duplicate, missing
KR_API_TOKEN), stdin/file/empty-output handling, --dry-run, and both CLI modes
end-to-end. Full suite (136 tests) and scripts/*.py syntax check both green. t-009
(portos submission script) unblocks via resolve_deps.py.
<!-- note:end t-008 -->

## t-009 — Write challenge submission script in silasfelinus/portos

<!-- note:begin t-009 -->
DONE (2026-07-14, burst-mode session): silasfelinus/portos PR #6 (branch
claude/blissful-goldberg-e7lam7 -> main) merged, adding
scripts/challenge_submit.py mirroring this repo's script (fetch prompt ->
run configured CLI provider -> POST submission as contender
"portos-agent" -> print leaderboard standing), plus
scripts/lib/run_cli_provider.mjs (a one-shot helper wrapping PortOS's
existing pickCliProvider/runCliProviderPrompt from
server/lib/cliProviderRun.js so the script doesn't hardcode a CLI's argv
convention) and a new settings.challengeSubmit provider/model config slot
validated the same way as the existing autofixer/calendarSync slots.
Verified locally: syntax checks, an end-to-end smoke test against a fake
CLI provider (spawn/stdin/stdout plumbing), and a stubbed-HTTP run of the
full fetch->agent->submit->leaderboard flow, plus the full PortOS server
vitest suite (712 passed, 1 pre-existing unrelated failure in
services/imageGen/codex.test.js, 140 skipped). PortOS's GitHub Actions CI
never ran on the PR (repo has zero workflow runs in its history — Actions
appear disabled/unenabled for this repo, likely a fork-default), so the
merge decision rested on the manual verification above rather than a
green CI check; flagged here in case that's worth enabling. Unblocks
t-010 (auto-runner) pending t-008 too. Original task intent below.

In silasfelinus/portos, add a challenge submission script mirroring the conductor one. Usage: (whatever invocation pattern portos uses) challenge_submit <challenge-slug> Steps:
  1. Fetch challenge from KR API (GET /api/challenges/<slug>)
  2. Pass promptText to the portos agent
  3. Collect agent output
  4. POST to /api/challenges/<slug>/submissions with contenderSlug "portos-agent" + output
  5. Return submission id
Reads KR_API_TOKEN and KR_BASE_URL from env (same vars as conductor). Worker should look at silasfelinus/portos to understand its agent invocation pattern before writing this — don't assume it matches conductor's.
<!-- note:end t-009 -->

## t-010 — Build auto-runner: dispatch active challenges to all registered agents

<!-- note:begin t-010 -->
In silasfelinus/conductor, write scripts/challenge_runner.py. Usage: python scripts/challenge_runner.py [--challenge <slug>] [--all] Steps:
  1. Fetch open challenges from KR API
  2. For each challenge, skip if conductor-claude already has a submission
  3. Build the challenge prompt (from promptText + any system context)
  4. Call the conductor agent (via Claude API or existing agent invocation pattern)
  5. Submit the output via challenge_submit.py
  6. Print summary: challenges attempted, submissions created
This lets conductor auto-participate in challenges without manual intervention. Designed to run on a schedule (e.g. nightly cron via AGENTS.md todo mechanism).

DONE (2026-07-14, hourly burst-mode cycle): added scripts/challenge_runner.py. Fetches OPEN
challenges via GET /api/challenges?status=OPEN (or a single slug via --challenge),
skips any challengeType this runner doesn't handle and any challenge the contender
already has a leaderboard entry for (GET .../leaderboard, reused from challenge_submit.py), generates
an answer via the Claude Messages API (model overridable via CHALLENGE_RUNNER_MODEL,
default claude-sonnet-5), and submits it via challenge_submit.py's submit_challenge/
fetch_leaderboard helpers (imported, not duplicated). Scope decision: only TEXT and
REASONING challengeTypes are handled -- their submissions are plain outputText, which
is all challenge_submit.py's --output flow supports. ART needs a generated ArtImage
(separate scripts/curate_art.py pipeline) and CHARACTER/SCENARIO need a KR
Character/Scenario record created first (per kind_robots prisma schema.prisma Challenge/
ChallengeSubmission models) -- both skipped with a printed reason rather than attempted;
follow-up wiring for those three types is a natural next task. --dry-run evaluates
and reports outcomes (submitted/skipped-type/skipped-duplicate/dry-run/error) without
calling the Claude API or submitting. 21 new tests in tests/test_challenge_runner.py
cover fetch/dedup/generation/submission/CLI paths; full suite (172 tests, up from 151)
passes via python3 -m pytest (the /root/.local/bin/pytest uv-tool venv still lacks
PyYAML per the known gap noted on t-039/t-041 sessions -- unrelated to this change).
scripts/audit_roadmaps.py: 0 errors, 1 pre-existing warning (unchanged).
<!-- note:end t-010 -->

## t-012 — Seed contender roster: agent stacks, models, and art generators

<!-- note:begin t-012 -->
Write scripts/seed_contenders.ts in kind_robots (idempotent, upsert by slug). Starting roster:
  AGENT_STACK: conductor-claude ("Conductor (Claude)", generator: claude-api),
               portos-agent ("Port0s")
  LLM_MODEL:   claude-fable (model: claude-fable-5),
               claude-opus (model: claude-opus-4-8),
               openai-gpt (provider: openai)
  ART_GENERATOR: art-sd (generator: art-sd),
                 art-comfy-flux, art-comfy-sdxl (generator: comfy-*),
                 art-openai (generator: openai-images)
Each gets a name and a description naming the exact backend it fronts. These are the fighter cards for matchups — avatar art can come later through the normal ART-PROMPTS pipeline (avatarImageId is nullable).


Claiming highest-priority ready task after merging the connector-safe task-event bridge.
<!-- note:end t-012 -->

## t-013 — Matchup runner: dispatch one challenge across a contender matrix

<!-- note:begin t-013 -->
In silasfelinus/conductor, write scripts/challenge_matchup.py — the generalization of t-010's runner. Input: a challenge slug plus a matchup spec (inline JSON or a YAML file):

  contenders:
    - { contender: claude-fable }
    - { contender: claude-opus }
    - { contender: openai-gpt, settings: { temperature: 1.0 } }
    - { contender: conductor-claude, variantKey: detailed,
        promptSuffix: "..." }

Backend/model resolution comes from the Contender record (its generator/ model/defaultSettings fields); the spec only overrides per-entry. For each entry: build the final prompt (base promptText + any variant edits), call the right backend (Claude API, OpenAI API, or a kind_robots art endpoint for ART challenges), and POST the submission with the t-002 variant fields filled in (variantKey, settings, promptUsed). ART challenge outputs go through the existing kind_robots art save path so the submission gets a real artImageId. Print a matchup summary table. Reads KR_API_TOKEN, KR_BASE_URL, ANTHROPIC_API_KEY, OPENAI_API_KEY from env; skip (with a clear note) any contender whose key/backend is unavailable.


Claimed for implementation of the general contender matchup runner on current main.

Complete in conductor PR #522 (squash 610f718): added scripts/challenge_matchup.py with JSON/YAML contender matrices, live contender resolution, Anthropic/OpenAI text dispatch, queued A1111/Comfy art generation, OpenAI Images generation, real ArtImage submission links, variant audit metadata, safe per-entry skips, and summary reporting. Worker PR CI and Security Audit passed before merge.
<!-- note:end t-013 -->

## t-014 — Prompt-variant generator using kind_robots random lists

<!-- note:begin t-014 -->
Support "same generator, different prompts" matchups where the difference is randomized variables. In silasfelinus/kind_robots, add a server util (and a small API route, e.g. POST /api/challenges/variants) that takes a base prompt containing placeholder keys and a variant count N, and returns N concrete prompts by substituting from the random pools in stores/helpers/ randomHelper.ts (adjective, animal, backstory, class, color, genre, honorific, inventory, item, material, name, noun, personality, quirk, skill, species, verb) and, when a placeholder names one, a user RANDOMLIST dream. Each returned variant includes the key\u2192value map so the caller can store it as randomSelections on the submission (t-002) \u2014 variants must be auditable and reproducible, not mystery rolls. The conductor matchup runner (t-013) consumes this to enter one contender N times with variantKey "random-1"..."random-N".
DONE (hourly burst-mode cycle, 2026-07-14 ~20:15 UTC): kind_robots PR #256 (`claude/upbeat-pascal-pu2vtz` \u2192 main, merged) adds server/utils/promptVariants.ts (`generatePromptVariants`, a pure {{key}} placeholder resolver taking an injected pool-provider function so it needs no DB in tests) and POST /api/challenges/variants, which wires it to the built-in randomHelper.ts pools plus a Prisma lookup of visible RANDOMLIST dreams (stored as dreamType: BRAINSTORM per dreamHelper.ts's LEGACY_DREAM_TYPE_MAP \u2014 RANDOMLIST has no such value in the Prisma enum) matched by normalized title, scoped to isPublic || own userId. Every variant returns variantKey ("random-1".."random-N"), promptUsed, and a randomSelections key\u2192value map for auditability. Added utils/scripts/verifyPromptVariants.ts (assert-based, matches the existing verifyFacetAliases.ts convention) wired as `npm run test:prompt-variants`. Verified: the new verify script passes; `npm test` (vue-tsc) shows no new errors \u2014 eslint and prettier clean on all changed files. PR's "TypeScript" CI check failed, but on investigation (see kind-robots/t-020, filed this cycle) it's a pre-existing break on main unrelated to this change \u2014 confirmed by running the identical typecheck against a clean origin/main worktree with no PR changes applied, same two errors, same two unrelated files. All other checks (Contract verifiers, facet-alias-smoke, GitGuardian, Vercel deploy) passed; merged since mergeable_state stayed "unstable" (not hard-blocked).
<!-- note:end t-014 -->

## t-015 — Faceted leaderboards: rank by model, generator, and prompt strategy

<!-- note:begin t-015 -->
DONE (2026-07-14, hourly conductor cycle, Reviewer solo full-cycle session): kind_robots PR #258 (`claude/admiring-mayer-th2kzy` -> main, merged) adds `buildFacetLeaderboard()` in server/utils/challengeCenter.ts, grouping scored submissions by Contender kind/provider/model/generator instead of by individual contender (contenders missing the requested facet are excluded, not bucketed under "unknown"). GET /api/challenges/leaderboard gained a `facet` query param wired to it, with challengesAttempted/challengesWon/winRate computed per facet value the same way as per-contender today. Also closed the "per-variant within a challenge" bullet: buildChallengeLeaderboard() variants[] now carry promptUsed/randomSelections/rank plus a bestVariantKey on the entry, and /challenges/[slug] surfaces a "Best variant" badge and a "Random rolls used" collapse. pages/challenges/leaderboard.vue got a comparison-axis selector (contender/model/generator/provider/kind). New utils/scripts/verifyChallengeCenter.ts (wired as npm run test:challenge-center) covers both functions. Verified: new verify script passes, npm run test (vue-tsc) shows no new errors under Node 22 locally. PR CI: Facet Alias Smoke Test and Contract Tests green; TypeScript Type Check failed on GitHub Actions (Node 24 runner) — reproduced the exact same two pre-existing errors (server/api/art/image/index.get.ts:153, server/api/model-builder/items/[id]/commit.post.ts:644/646, tracked in kind-robots/t-020) by installing Node 24 locally and running a fresh `npm ci` + typecheck against this branch, byte-identical file:line match, confirming no regression from this change. Vercel deploy check failed on an unrelated build-rate-limit (24h retry), also pre-existing/environmental. mergeable_state stayed "unstable" (not blocked), matching the PR #256 precedent for merging past this known-red pre-existing check; merged.
<!-- note:end t-015 -->

## t-016 — Write docs/comparison-axes.md summarizing the five M5 comparison axes

<!-- note:begin t-016 -->
DONE (2026-07-07, Silas-directed session): wrote projects/challenge-center/docs/comparison-axes.md as the canonical M5 reference — axis list and Contender-design paragraphs quoted verbatim from notes_from_silas, plus an axis->field->task mapping table (t-002 schema, t-012 roster, t-013 runner, t-014 variants, t-015 leaderboards) and the design guardrails. Original task intent below. Kaizen from the Reviewer's M5-expansion merge (conductor PR #188): the M5 tasks each restate pieces of the comparison-axes design inline (provider vs provider, model vs model, generator vs generator, prompt vs prompt via random substitution, settings vs settings) and the contender split (Contender = leaderboard identity, ChallengeSubmission = the "how": variantKey/promptUsed/ settings/randomSelections). Write projects/challenge-center/docs/comparison-axes.md as the one canonical reference doc — pull the axis list and Contender-design paragraphs from notes_from_silas verbatim, then a short table mapping each axis to the task(s) that implement it (t-002 schema, t-012 roster, t-013 runner, t-014 variants, t-015 leaderboards). Future task notes and PR reviews should check against this doc instead of re-deriving the design from scattered task notes.
<!-- note:end t-016 -->

## t-017 — Delete superseded worker/* branches right after a rescue PR merges the same task

<!-- note:begin t-017 -->
DONE (2026-07-07, Silas-directed session): added a 'Rescue / salvage PRs — delete the superseded branch in the same session' subsection to AGENTS.md (after the cross-repo guidance) instructing agents to delete a superseded worker/* or claude/* branch in the same session the rescue PR merges, and to treat a rescue PR body's 'can be deleted' line as an instruction to delete now. Original task intent below. Kaizen from the Reviewer's t-002 resolution (2026-07-07): kind_robots PR #116 (a Silas-directed session branch) rescued t-002's stranded migration+schema work onto current main and explicitly said in its own PR body "the old worker/challenge-center-t-002 branch can be deleted" once it landed. Instead, that exact stale branch was opened as PR #118 and merged separately about ten minutes later — harmless here only because its content was byte-identical to what #116 had already landed, so it merged as a no-op, but a stale worker branch that has DIVERGED from a rescue merge could just as easily reintroduce already-superseded or conflicting content. Add a habit/checklist step (in AGENTS.md's cross-repo or rescue-PR guidance): whenever a rescue/salvage PR supersedes a stranded worker/* or claude/* branch, delete that branch in the same session the rescue PR merges, rather than leaving it for a later PR to accidentally reopen and merge.
<!-- note:end t-017 -->

## t-018 — Add a CI check that runs seed scripts in validation-only mode

<!-- note:begin t-018 -->
Kaizen from t-004 (Worker's suggestion, kind_robots PR #199): add a CI job/step that runs scripts/seed_challenges.ts (and future seed scripts following the same dry-run-by-default pattern, e.g. utils/scripts/seedDaVinciEndings.ts) without --write and without a database, so malformed seed catalogs (bad enum values, missing required fields, duplicate slugs, wrong type coverage) fail CI before merge instead of only being caught by manual review.


Worker run claimed the highest-priority eligible ready task after current-main priority scan.

IMPLEMENTED (2026-07-14): kind_robots PR #263 (branch claude/upbeat-pascal-w87yxr) adds test:seed-challenges / test:seed-contenders npm scripts (plain tsx runs of scripts/seed_challenges.ts and scripts/seed_contenders.ts with no --write flag — both already validate slugs/enum coverage/required fields and skip all Prisma/DB work unless --write is passed) and wires both into .github/workflows/contract-tests.yml, which already gates every PR and needs no database. Verified locally with no DATABASE_URL set: both scripts validate and exit 0; confirmed the failure path by feeding validateChallengeSeeds a duplicate-slug catalog and seeing it throw non-zero. utils/scripts/seedDaVinciEndings.ts was left out of scope (see PR body) since it requires a file argument rather than an embedded catalog and already has its own nightly DB-backed regression job. PR opened against main; awaiting CI (Contract verifiers/TypeScript/facet-alias-smoke) before merge.

DONE (2026-07-14 22:19 UTC): Silas merged kind_robots PR #263 directly (merge commit on main, 2026-07-14T22:16:49Z), despite two pre-existing red checks unrelated to this diff (Contract verifiers failing on "Channel content contract"; TypeScript failing on the already-tracked kind-robots/t-020 errors) -- neither check ran against, or was caused by, this PR's two-file diff. Filed kind-robots/t-021 for the newly-observed Channel content contract failure (3 files reference unknown home/{account,friends,messages} tabs) as this cycle's kaizen, alongside the already-open kind-robots/t-020.
<!-- note:end t-018 -->

## t-019 — Polish and upgrade Challenge Center front-end surface

<!-- note:begin t-019 -->
DONE (kind_robots PR #265, merged): added 'challenges' to tutorialChannels (mirrors 'mural' pattern) + wired into tutorialRouteMap; added dashboard-tab/thumb/tutorial webp art derived from the already-approved conductor/projects/images/challenge-center-hero.webp (no live image-gen pipeline available this session). Step 4 ("evolve the placeholder scaffold") was already done by prior tasks t-004/t-008/t-014/t-015 -- verified by reading challenge-center-page.vue and pages/challenges/[slug].vue directly, the "placeholder scaffold" framing was stale. Step 3 (liveUrl): PROJECT_PLACEMENTS['challenge-center'] already correctly specifies route '/challenges' in code; live DB sync needs an admin to click the Conductor Placements button (out of session scope, not a code change). See TALKBACK for CI findings (kind-robots/t-021 pre-existing, confirmed unrelated) and kaizen.
<!-- note:end t-019 -->

## t-020 — Make task-event roadmap mutations surgical, formatting-preserving, and conflict-safe

<!-- note:begin t-020 -->
Context: scripts/process_task_events.py currently rewrites complete authoritative YAML files with PyYAML safe_dump. A one-task state change therefore produced hundreds of unrelated changed lines, escaped readable Unicode, changed block and quote styles, and created unnecessary merge-conflict risk. The bridge must remain connector-safe without treating an entire roadmap as disposable generated output.

Required implementation:
  1. Parse the complete roadmap for structural validation, but mutate only the requested task fields and the dependency statuses that resolve as a direct consequence of that event.
  2. Preserve every byte outside the intended YAML nodes. Do not reserialize notes_from_silas, unrelated tasks, comments, blank lines, key ordering, quote style, Unicode, or multiline block style.
  3. Preserve the existing key order and local formatting of the target task wherever possible. A status-only event must create a status-sized diff, not a file-sized diff.
  4. Append to LEARNING.yaml without reformatting existing records. Duplicate task/outcome learning entries must remain idempotent.
  5. Make the workflow conflict-safe: fetch current main immediately before committing, never force-push, retry one clean non-fast-forward race by replaying the still-pending event on current main, and otherwise fail with the event left intact.
  6. Make processing atomic. Invalid events, resolver failures, validation failures, or unresolved push conflicts must not leave a partial roadmap or ledger commit.
  7. Keep successfully processed events removable and failed events inspectable. Re-running after success must be a no-op.

Regression coverage:
  - Use a checked-in fixture copied from the real Challenge Center roadmap, including long notes, Unicode arrows and em dashes, quoted values, block scalars, and dependency lists.
  - A claim event may change only status, owner, updated, and the consumed event file. Assert all unrelated source lines are byte-identical.
  - A done event may change only the target task, directly unblocked dependents, one append-only learning record, and the consumed event file.
  - An invalid transition must produce zero authoritative-file diff and leave the event in place.
  - A second run after success must produce zero diff and no duplicate learning record.
  - Add a test that fails if an event causes broad roadmap churn, escaped Unicode, or conversion of literal blocks into folded/quoted strings.

Implementation guidance: a targeted source-span patcher is preferred. A round-trip YAML library is acceptable only if the byte-preservation tests above pass. Do not call yaml.safe_dump on authoritative roadmap or learning files.

Definition of done: the full task-event test suite passes in CI; processing representative claim and done fixtures produces a minimal expected diff; both output files parse with yaml.safe_load; documentation explains the atomic retry behavior; and no unrelated roadmap text changes.

ADDENDUM (Claude, 2026-07-14, found while closing t-008): scripts/resolve_deps.py (main(), around the yaml.safe_dump call) has the identical defect — running it after t-008 closed turned a two-task status flip (t-009, t-015: waiting -> ready) into a 940-line diff of the same kind (escaped Unicode, flow-style reindentation, changed quoting) across the whole challenge-center roadmap. Worked around this cycle by reverting and reapplying the same edits with set_task_field.py (26-line diff) instead of running resolve_deps.py for real. In scope for this task: extend whatever surgical patcher t-020 builds to resolve_deps.py's dependency-unblock writes too, not just process_task_events.py's event-driven ones — both call the same unsafe dump-the-whole-file pattern and should share one safe write path.


IMPLEMENTED (2026-07-14): scripts/roadmap_text_patch.py adds a shared surgical, multi-field, multiline-aware patcher (set/unset ops built on set_task_field.py's find_task_block/field_value_end primitives, plus a literal-block '|-' renderer for multi-paragraph note text so paragraph breaks and literal Unicode survive instead of being flattened or \u-escaped).

process_task_events.py now computes a list of field ops per event and applies them via apply_task_field_ops instead of yaml.safe_dump-ing the whole roadmap. It also validates any learning payload BEFORE touching the roadmap file, so an invalid learning block can no longer strand an already-applied transition with its event undeleted (atomicity fix). LEARNING.yaml appends are now pure trailing-text writes -- existing records are never re-touched.

resolve_deps.py (the addendum found while closing t-008) uses the same patcher for its waiting-to-ready status writes, so a multi-task unblock only changes those status lines.

Added scripts/validate_roadmaps.py (extracted from an inline workflow heredoc -- heredocs can't be indented under a plain '<<' terminator inside a YAML block scalar, which was the original approach and would have broken silently) and hardened .github/workflows/process-task-events.yml: it now fetches origin/main immediately before pushing, never force-pushes, and retries exactly once by git reset --hard origin/main plus a full replay of the processing step on a non-fast-forward race, otherwise failing with the event left intact on origin.

Regression coverage: tests/test_roadmap_text_patch.py (10 tests against a checked-in frozen fixture copied from the real challenge-center roadmap.yaml -- byte-identical unrelated tasks, literal Unicode em-dash/arrow preservation, literal-block notes, unset-as-noop, idempotent re-apply), plus new tests in test_process_task_events.py (byte-preservation, atomicity on a bad learning payload, repeat-claim zero-diff idempotency, multiline note block rendering) and test_resolve_deps.py (surgical multi-task unblock, Unicode preservation). Wired the new and existing task-event test files into ci.yml's authz-regression job so they actually run in CI. Documented the atomic-retry and surgical-write behavior in task-events/README.md.

Full suite: 225/225 passing locally. Not done: a live end-to-end exercise of the GitHub Actions conflict-retry path itself (bash syntax-checked and logic-reviewed, but not runnable outside real CI).

conductor PR #534 merged (squash 81eae2f). scripts/roadmap_text_patch.py now performs all
roadmap/LEARNING.yaml mutations surgically in process_task_events.py and resolve_deps.py;
process-task-events.yml fetches main immediately before pushing and retries once on a
non-fast-forward race instead of force-pushing. 225 tests passing, all 19 PR checks green.
<!-- note:end t-020 -->

## t-021 — Investigate provisioning Node 24.x in the sandbox session environment for local CI reproduction

<!-- note:begin t-021 -->
DONE (2026-07-15, burst-mode session): resolved via conductor PR #535 (scripts/provision_node24.sh + docs/2026-07-15-node24-sandbox-provisioning.md). Chose the fetch-official-tarball path over nvm/fnm (not preinstalled, no durable install across ephemeral sessions), nodesource apt (blocked by proxy egress allowlist, 403), and CI artifact download (redirects to un-proxied Azure Blob URLs) -- nodejs.org's own dist host IS reachable through the sandbox proxy. Script downloads a pinned Node 24.x linux-x64 tarball to $HOME/.nodejs24, no root/version-manager needed, idempotent, ~30MB. Verified: node --version -> v24.18.0 (matches kind_robots' engines: node 24.x pin exactly), re-run correctly skips re-download. Future sessions should 'source scripts/provision_node24.sh' before any local kind_robots CI reproduction.
<!-- note:end t-021 -->
