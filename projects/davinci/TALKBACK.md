# TALKBACK — davinci

Append-only critique log. Never edit or delete entries. Format per AGENTS.md.

## 2026-07-04 | Reviewer → Worker | davinci/schema | critique

**Decision:** applied schema patch to kind_robots (PR #87), folding it in after
discovering it had landed under a duplicate project

**What was good:**
- Correctly recognized Milestone already carries icon/artImageId/artPrompt and
  avoided a risky rewrite; piggybacked the existing art system throughout.
- Declined a blind 1,600-line whole-file overwrite via the connector — right call;
  preserved the patch as a handoff instead.
- Clean modeling: Cascade on run-owned children, SetNull on optional links,
  seeded runs, per-run stat uniqueness.

**What to improve:**
- `@@unique([userId, achievementId, lifeRunId])` permits repeat unlocks when
  `lifeRunId` is NULL (MySQL NULLs are distinct in unique indexes). Global
  achievements need an upsert-guard in the API layer — noted on PR #87 and on
  t-004 in this project's roadmap.

**Kaizen task:** folded into t-003/t-005 (ending-dimension and milestone-mapping
work already queued in this roadmap).

## 2026-07-04 | Reviewer → Reviewer | davinci/da-vinci | pattern

**Subject:** A same-day Reviewer session re-scaffolded this exact project under a
second slug (`projects/da-vinci/`, hyphenated) instead of finding the existing
`projects/davinci/` (no hyphen), producing two roadmaps, two TALKBACKs, and a
duplicate `ready` task for the same design-brief work `davinci/t-001` had already
completed.

**Detail:**
- `projects/davinci/` was scaffolded first (conductor PR #179, `worker/davinci-project-foundation`):
  registered in `CONTROL.md`, `projects/priority.yaml`, and `project-overrides.yaml`;
  t-001 (design brief) already `done`; t-003 through t-007 laid out a full
  SHAPE→BUILD→INTEGRATE→POLISH plan.
- `projects/da-vinci/` appeared later the same day (conductor PR #181) with the
  commit message "no conductor project existed" for the life-sim schema — false;
  it existed, just under the un-hyphenated slug. It duplicated the schema-critique
  TALKBACK entry and re-opened a `ready` "write the design brief and start building"
  task that this project's t-001 had already finished, plus a second redundant
  `needs-human` scope-confirmation task duplicating this project's t-002.
- Net effect if left alone: the next Worker cycle could have picked up
  `da-vinci/t-001` and written a second, inconsistent design brief for the same
  game, and `STATUS.md` already shows both slugs as separate projects.
- Resolved this cycle: folded `da-vinci`'s unique content (the schema-critique
  TALKBACK entry, above) into this project, recorded the schema's completion on
  t-004, and deleted the duplicate `projects/da-vinci/` folder. Registrations in
  `CONTROL.md` / `priority.yaml` / `project-overrides.yaml` only ever pointed at
  `davinci`, so no cleanup was needed there.

**Suggested action:** Before scaffolding a new project, grep
`projects/priority.yaml`, `project-overrides.yaml`, and `CONTROL.md` for
near-spellings of the proposed slug (hyphenated/un-hyphenated, spacing) in
addition to checking `projects/<slug>/` directly — a directory-existence check
alone missed this because the slug itself differed.

## 2026-07-05 | Reviewer → Worker | davinci/t-008 | pattern

**Decision:** merged both PRs as-is — kind_robots #89 (seed importer script) and
conductor #197 (roadmap bookkeeping: t-008 done, t-009 waiting → ready).

**What was good:**
- Correctly matched to existing upsert keys (`triggerCode`, `outcomeKey`,
  `conditionKey`) instead of inventing new ones, keeping the importer safely
  re-runnable.
- Honored the ArtImage exclusion boundary exactly — verified zero ArtImage rows
  created, path-string-only icon/hero fields.
- Caught and documented a real schema mismatch (no `artPrompt` column on
  LifeAchievement) instead of silently dropping the field or crashing.
- Verified end-to-end against a throwaway MariaDB with concrete counts
  (1024/1024/1024) and confirmed idempotency with a second `--write` run,
  rather than just claiming "should work."
- Repaired pre-existing `package-lock.json` drift as a narrow, additive side
  fix (documented, not silently bundled) rather than leaving `npm ci` broken
  for the next session.

**What to improve:**
- No "Kaizen suggestion" section was included in the kind_robots PR body
  despite the handoff template requiring one — this cycle's kaizen task
  (t-010) was substituted by the Reviewer instead. Include it even when the
  task feels complete; the compounding-improvement loop depends on it.
- The `lifeAchievement` upsert-by-`findFirst`-then-update/create isn't atomic,
  which is fine for a single-writer offline seed script but should be called
  out explicitly as a boundary (single-invocation only) in the script's own
  comments, not just implied by context.

**Kaizen task:** t-010 — add an automated regression check for the importer's
row counts and link integrity, so future edits don't need another manual
MariaDB run to catch a regression.

## 2026-07-05 | Reviewer → system | davinci/t-009 | response

**Decision:** merged (kind_robots PR #92; roadmap PR #205)

**Context:** Silas-directed session work executed and merged under the
standing overnight authority he granted in-session ("do whatever you feel
best until I wake up"). Same-agent build-and-merge, so this entry documents
the verification basis rather than an independent review.

**What was good:**
- Addressed the prior cycle's critique: the PR body includes an explicit
  Kaizen suggestion this time (became t-011).
- The t-004 NULL-lifeRunId constraint gap got its promised API-layer guard,
  and the exact failure scenario (second run, same user, same ending) was
  exercised directly: exactly one unlock row survives.
- Verified beyond typecheck: 24 helper assertions against the seeded
  throwaway MariaDB plus a live dev-server HTTP matrix (200/401/400/403/404).

**What to improve:**
- Same-agent merge means no adversarial reading of the diff happened; the
  next independent Reviewer pass should audit server/utils/davinci.ts,
  especially the recompute-on-call behavior for already-COMPLETE runs noted
  in the PR flags.

**Kaizen task:** t-011 — LifeRun status-transition guard + end-to-end play-loop
API test (from the Worker-side kaizen suggestion in PR #92).

## 2026-07-05 | Reviewer → system | davinci/t-010 | response

**Decision:** merged (kind_robots PR #93)

**Context:** Silas-directed overnight session work, same standing authority as
t-009. Same-agent build-and-merge again — verification basis documented here,
independent audit still welcome.

**What was good:**
- Closed the t-008 TALKBACK critique directly: the importer now documents its
  single-invocation boundary in its own header, and the manual verification is
  a repeatable 15-check suite (npm run seed:davinci:verify) with a tested
  failure path (truncated seed file exits 1).
- Refactor kept one source of truth: the verifier imports the importer's own
  parse/validate/import functions rather than duplicating them.

**What to improve:**
- The suite still needs a database to run against, so it is manual-triggered
  until CI gets a MariaDB service. That wiring became t-012 rather than being
  smuggled into this diff.

**Kaizen task:** t-012 — nightly CI job with a MariaDB service container that
runs the generator + seed:davinci:verify end-to-end across both repos.

## 2026-07-05 | Reviewer → system | davinci/t-007 | response

**Decision:** merged (conductor PR #207)

**Context:** Silas-directed overnight session work; analysis doc, zero code
risk. Same-agent build-and-merge, documented per the running pattern.

**What was good:**
- The task's own timing condition was honored: the comparison waited until
  the endpoint engine was concretely merged and verified, so the boundary
  argument rests on real code (custody checks, unlock guards, regression
  suite) rather than intentions.
- Ends with an explicit re-open condition (both MVPs merged) instead of a
  vague "revisit later."

**What to improve:**
- The doc's proposed standing boundary rules only bind if they're visible
  from Storymaker's side too — that gap is this merge's kaizen.

**Kaizen task:** storymaker/t-009 — cross-link the Da Vinci boundary rules
from Storymaker's roadmap so future session-schema work reads them first.

## 2026-07-05 | Reviewer → system | davinci/t-012 | response

**Decision:** merged (kind_robots PR #94), then verified live

**Context:** Silas-directed overnight session work, same standing authority.
Unlike the earlier same-agent merges, this one got a true post-merge
verification: the workflow was dispatched on main and run #1 completed
green in ~2 minutes (MariaDB service up, conductor checkout, 1024-line
generation, prisma db push, all 15 verify checks passed on GitHub's infra).

**What was good:**
- The t-012 open question (which repo hosts) was answered with a reasoned
  decision in the PR rather than an escalation stall.
- Merge-then-dispatch closed the "can't test Actions locally" gap the same
  hour it was created.

**What to improve:**
- The workflow only covers the seed path; the resolution/award path still has
  no CI coverage. Folded into t-011 (headless tsx driver) rather than a new
  task, to avoid near-duplicate roadmap entries.

**Kaizen task:** deferred — folded into t-011's note (headless resolution
driver for the CI job); creating a separate task would duplicate it.

## 2026-07-06 | Reviewer → system | davinci/t-013 | response

**Decision:** merged (kind_robots PR #103)

**Context:** Silas-directed session ("aperitif" before tonight's project),
same standing authority. Same-agent build-and-merge; verification basis below.

**What was good:**
- Closed the m2 engine gap the roadmap had promised ("run, choice, and ending")
  — only the ending half existed before this.
- The play loop was proven to COMPOSE with the t-009 resolver, not just work in
  isolation: the outcomeKey derived from stats accumulated through create ->
  choices equals what resolveLifeRunEnding computes (1011000101 in the driver).
- Verified beyond typecheck: 28 helper assertions + a live dev-server HTTP
  matrix, mirroring the t-009 discipline.
- Reused the environment from the prior session (seeded MariaDB survived), so
  the verification ran against the real 1024-ending dataset.

**What to improve:**
- Still same-agent merge — an independent pass over server/utils/davinci.ts
  (the transaction boundaries in recordLifeChoice, chapter-advance semantics)
  would be healthy.
- The choice side now guards status (409 on non-ACTIVE); the resolve side's
  recompute-on-COMPLETE is still open. Correctly left to t-011 rather than
  scope-creeping this task.

**Kaizen task:** deferred — folded into t-011 (headless create->choices->resolve
CI driver). t-011 is now `ready` (both deps done).

## 2026-07-20 | Reviewer → system | davinci/t-014 | response

**Decision:** merged (kind_robots PR #645), task returned to `ready` (not `done`)

**Context:** Conductor agent run, picked davinci/t-014 from priority.yaml
rotation after ai-art-academy's ready tasks were either blocked on the (still
down) art-generation relay or already run twice earlier today, and
kind-robots/t-033 had already been rechecked twice with no new evidence.

**What was good:**
- Confirmed step (2) of t-014 (tutorialChannels entry) was already done before
  touching anything, avoiding a duplicate edit.
- Found a real, reusable seam instead of inventing scope: `Achievement.triggerCode`
  follows a `davinci-ending-{outcomeKey}` convention (per
  `utils/scripts/seedDaVinciEndings.ts`), so the front page's `#interactive`
  slot could show genuine live achievement data via the existing public
  `GET /api/achievements` endpoint — no new API needed.
- Explicitly declined to build the "full interactive experience" (step 4)
  once it became clear the play-loop API has no AI-narration layer generating
  actual chapter content yet (`docs/notes/davinci-play-loop-api.md` says so
  directly) — a playable UI right now would have nothing real to display.
  Filed that gap as the new kaizen task (t-015) instead of shipping a
  half-working stub.
- Verified live via API, not assumption: `GET /api/projects` on the deployed
  site confirmed davinci's `liveUrl`/`channelKey`/`tabKey` are still null
  (step 3), rather than repeating a stale claim from the task note.

**What to improve:**
- None this cycle — first pass, clean CI (TypeScript, Contract verifiers,
  GitGuardian all green).

**Kaizen task:** t-015 — spec the AI-narration layer that generates Da Vinci
chapter prompts/choices, the actual blocker between the existing play-loop
API and a real playable run UI.
