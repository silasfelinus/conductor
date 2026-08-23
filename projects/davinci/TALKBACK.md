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
  from Storybook's side too — that gap is this merge's kaizen.

**Kaizen task:** storybook/t-009 — cross-link the Da Vinci boundary rules
from Storybook's roadmap so future session-schema work reads them first.

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

## 2026-07-20 | Worker (burst) | davinci/t-015 | done (conductor PR pending)

**Decision:** implemented (docs-only, conductor repo), self-merge candidate.

**Failure category:** none — clean first pass, no live environment or
egress dependency, so nothing blocked this cycle.

**What was good:**
- Rotation landed here after ai-art-academy (run twice today, recurring
  filler), kind-robots/t-033 (rechecked twice already, no new evidence),
  superkate-hairstyle-ai/t-019 (needs a live Comfy/Kontext box, not
  reachable this cycle), and model-builder/t-029 (remaining steps gated on
  art-generation egress + an admin-only Placements click) were all either
  already covered today or genuinely blocked — davinci/t-015 was the next
  priority.yaml entry with ready, tractable, non-live-dependent work.
- Grounded the spec in real code instead of inventing a contract from
  scratch: read `server/utils/davinci.ts` (DAVINCI_DIMENSIONS, resolve
  flow), `prisma/schema.prisma` (LifeRun/LifeChoice/LifeStat/LifeRunArt
  shapes), the existing `GET /api/narrators/[type]/[slug]` route (reused
  as-is for narrator lookup), and the OpenAI `json_schema` strict-mode +
  server-side re-validation pattern already live in
  `server/utils/wonderLabReviewDraftGenerator.ts` — the narration layer's
  validation contract mirrors that rather than a new bespoke shape.
- Kept the design honest about state ownership: the proposed
  `/narrate` endpoint only returns a candidate `DaVinciNarrationResult`;
  the client still calls the existing `/choices` and `/resolve` endpoints
  separately, so no new durable-state owner is introduced and the
  play-loop doc's "AI narrates, app owns state" boundary holds.
- Wrote projects/davinci/docs/narration-layer-spec.md rather than editing
  design-brief.md in place — the design brief is the project-level pitch
  doc (already referenced by storybook-boundary-comparison.md); this is a
  focused implementation-contract doc for one layer, consistent with how
  storybook-boundary-comparison.md itself is a separate focused doc.
- Left the actual `/narrate` route + client run-screen implementation
  unfiled as a new task rather than scoping it myself in the same pass —
  a docs-only spec cycle shouldn't also invent the next task's exact
  shape; better for Silas or the next cycle to size that build task
  fresh against the finished spec.
- `python scripts/audit_roadmaps.py` — 0 errors both before and after the
  roadmap edit.

**What to improve:** none this cycle.

**Kaizen task:** none filed this cycle — the natural next task (build the
`/narrate` endpoint + minimal run-screen UI per the spec's "First build
slice" section) is real but deliberately left unfiled per the note above.

## 2026-07-21 | Worker (burst) | davinci/t-014 | done

**Decision:** implemented, merged this session (reversible, scoped — session
claude-conductor-agentrun-20260721T2000Z-davinci-t014).

**Failure category:** none — clean first pass.

**What was good:**
- Picked up the gap the 2026-07-20 cycle (kind_robots PR #645) deliberately
  left open: that cycle judged a full playable run UI premature because the
  AI-narration layer (design-brief.md's Chat-as-narrator contract) wasn't
  specced yet, and shipped only a static achievements list instead. The
  narration spec landed later that same day (davinci/t-015, done) but still
  has no implementation, so this cycle built a genuinely playable first
  slice without waiting further: a curated 8-chapter content pool (one
  chapter per narrative-device pattern named in design-brief.md) drives the
  UI, while all durable state and outcome math stay server-side through the
  existing play-loop API exactly as designed — the curated content is
  swappable flavor text, not a second source of truth. This matches
  design-brief.md's own "First build slice" guidance ("add a minimal run
  shell only if needed for testing unlocks") more literally than either
  waiting indefinitely or building a second state layer would have.
- Read the actual implementation before writing UI code instead of
  guessing at shapes: `server/utils/davinci.ts` (resolve math, play-loop
  helpers), all 4 `server/api/davinci/**` route files (request/response
  wrapper conventions), and the `LifeRun`/`LifeChoice`/`LifeStat`/
  `LifeEnding` Prisma models directly — caught the `recordLifeChoice`
  "only advances currentChapter when the submitted chapter is greater"
  quirk early and designed around it (chapter pointer tracked as
  `Choices.length + 1` client-side rather than trusting `currentChapter`
  naively, which would have skipped chapter 1 on a fresh run).
  Cross-referenced `challenge-center-page.vue` (a finished, fully
  interactive `#interactive`-slot project) for the `performFetch` +
  loading/error-state conventions rather than inventing new ones.
- Hit a real process bug mid-cycle and caught it before it shipped:
  `claim_task.py` pushes its claim commit straight to `origin/main` via git
  plumbing without touching the caller's working tree, so the local
  conductor checkout stayed stale after claiming; `set_task_field.py`
  edits whatever's on disk. Running `set_task_field.py status review`
  against that stale tree would have silently reintroduced a week-old
  `claimed_by`/`claimed_at` and clobbered the actual claim. Caught by
  diffing the field values against what had just been claimed, fixed by
  fetching + fast-forwarding before reapplying. Also caught and fixed a
  second, subtler bug of my own making: appending a new `note:` paragraph
  by hand without a blank-line separator collapsed all three PROGRESS
  paragraphs into one run-on line under YAML's folded (`>`) scalar rules
  once re-parsed — verified by re-parsing the note (not just eyeballing
  the raw diff) and comparing the paragraph-boundary bytes against the
  original file's own convention before committing.
- Verified: `npm run test` (`vue-tsc --noEmit`) exit 0, `eslint` clean,
  `prettier --check` clean (after `--write`); `audit_roadmaps.py` — 0
  errors, same 12-warning/44-info baseline before and after. kind_robots
  PR #822: all 3 CI checks green (TypeScript, Contract verifiers,
  GitGuardian) — merged squash `24ccea95`. Conductor PR #993: all 23 CI
  checks green — merged squash `941865af`.

**What to improve:** none this cycle.

**Kaizen task:** conductor/t-077 (new) — `set_task_field.py`'s docstring
doesn't warn that (unlike `claim_task.py`) it operates on the caller's
local working tree rather than fetching `origin/main` fresh, which is
exactly the staleness trap this cycle hit right after using
`claim_task.py` in the same session. Add an explicit warning to the
docstring/usage text recommending `git fetch origin main && git merge
origin/main --ff-only` (or equivalent) immediately before any
`set_task_field.py` call that follows a `claim_task.py` call in the same
session.

## 2026-08-20 | Agent (scheduled conductor sweep) | davinci/t-021 | reviewer

**Decision:** picked davinci/t-021 (slice 10) as the top eligible priority.yaml
project with genuinely fresh ready work — mermaids-of-venice/t-013 (higher
priority) had already recorded its once-per-Pacific-day no-op earlier the
same Pacific day, and model-builder/t-029 and storybook/t-010 (also higher
priority) had each already run a cycle earlier the same UTC day per the two
prior TALKBACK entries immediately above this one — re-running any of the
three the same day would have been a duplicate, not fresh work.

**What happened:**
- Read slice 9's own REMAINING note (t-021's roadmap note) verbatim rather
  than re-deriving scope: it explicitly named the next concrete gap — the
  OUTER `phase` (`loading`/`start`/`playing`/`ending`) v-if/v-else-if chain
  in `davinci-page.vue` has no persistent wrapper, the identical focus-loss
  shape slice 9 fixed one level down for `chapterRegion`, and flagged that
  the narrower fix can't catch every case: `resolveLife`'s "See your ending"
  click lives inside `chapterRegion`, but its phase transition unmounts the
  entire `playing` block, `chapterRegion` included.
- Implemented the same wrap-and-watch pattern one level up: a persistent
  `phaseRegion` (`tabindex="-1"`) wrapping the whole outer chain, plus a
  `watch(phase, ...)` that restores focus when the transition originated
  from an in-region click. Added the 10th `verifyDaVinci*` guard
  (`verifyDaVinciPhaseFocusGuard.ts` + selftest), wired into `package.json`
  and `contract-tests.yml` alongside the nine existing guards.
- Verified per the PR body: new guard fails pre-fix / passes post-fix
  (git-stash round-trip against the real component), new guard selftest +
  guard pass, all 9 prior `verifyDaVinci*` guards + selftests still pass,
  `test:davinci-narration` (16/16) still passes, `test:layout-contract`
  holds with no new violations, eslint clean, prettier clean (after one
  `--write` reindent pass), `vue-tsc --noEmit` repo-wide exit 0, exactly the
  5 intended files touched. Confirmed the large line-count diff on
  `davinci-page.vue` (566 lines) was prettier's reindent of the whole
  newly-wrapped block, not unintended content drift, via
  `git diff --ignore-all-space`.
- kind_robots PR #1980: watched all 34 check runs directly (not just
  `mergeable_state`) rather than trusting a single poll — the aggregate
  "Contract verifiers" job (461 steps across the growing `contract-tests.yml`
  suite) genuinely took ~2m45s this cycle, confirmed still progressing via
  `get_workflow_job`'s per-step timestamps rather than assumed-stuck.
  Squash-merged once every check but the known-slow non-required "Build
  production image" deploy job was green, per the established
  merge-when-unstable precedent this project's slices have used since #1895.

**What was good:** read the prior slice's own REMAINING note as the actual
scope handoff rather than re-auditing the whole file from scratch, and
caught the case the narrower slice-9 fix couldn't cover (the nested-click
transition that unmounts the outer container too) by tracing `resolveLife`'s
actual call path instead of assuming the two focus regions were independent.

**What to improve:** none this cycle.

**Kaizen task:** deferred — the PR's own kaizen suggestion (remaining
kr-panel/kr-stat wrapper consistency for the dimension grid, or the
still-outstanding cross-width visual verification) is already recorded on
the task note as the next lead, not yet a confirmed separate roadmap task.

## 2026-08-21 | Agent (scheduled conductor sweep) | davinci/t-021 | worker

**Decision:** slice 11, no code change. Checked slice 10's own lead, found it didn't
pan out, released the claim.

**What happened:** slice 10's REMAINING note flagged "kr-panel/kr-stat wrapper
consistency for the dimension grid" as the next lead. Ran
`utils/scripts/codemods/kr_panel_codemod.py` (dry-run, whole repo) and confirmed zero
candidate substitutions anywhere in `davinci-page.vue` — the dimension-pill wrapper
divs use dynamic `:class` bindings (`dimensionPillClass()`/`dimensionValueClass()`)
for per-item tone, not a static `class="..."` sequence the mechanical codemod can
rewrite, and their border/bg values already follow the same status-tint formula
(`border-{status}/40 + bg-{status}/10`) documented for `.kr-note` elsewhere in the
design system. So the lead was speculative, not a real gap. Re-read the entire
interactive template (every `v-if`/`v-else-if` phase and chapter block, the
resolve/ending panel, the endings-on-record list, every button and
`NarrativeArtStatus` usage) against the same focus-loss/aria-grouping/status-tone
patterns the prior 10 slices fixed — found nothing further. `phaseRegion` and
`chapterRegion` already cover every phase/chapter transition; the dimension grid
already has `role="group"` + tone; narration error/resuming/narrating states already
have their own guards.

**What was good:** ran the actual codemod the prior slice's lead pointed at instead of
eyeballing whether it applied, and reported the negative result honestly instead of
forcing a marginal change to look productive.

**What to improve:** none this cycle.

**Kaizen task:** none — a future slice should look for a genuinely new interaction gap
(e.g. as Da Vinci narration content evolves) rather than re-checking this same
speculative lead; noted directly on the task's own note.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-23 | Agent (scheduled conductor sweep) → self | davinci/t-025 | resolution

**Decision:** implemented the shared composable t-025's own note proposed
(`stores/helpers/persistedNarrativeArtJobsHelper.ts`, `createPersistedNarrativeArtJobsController()`)
and migrated storybookStore.ts + davinci-page.vue. First CI push failed on
`verifyNarrativeArtPersistence.mjs`: it asserts `stores/taskmasterStore.ts` also
contains `createNarrativeArtJobsController()` — a third call site, byte-for-byte
identical to storybookStore.ts's `resumeNarrativeArtJobs()`, that the initial
investigation (grepping only the two files the task note named) missed entirely.
This is exactly the "third narrative surface" scenario the task's own note used to
justify the full extraction — it turned out to already exist. Migrated
taskmasterStore.ts too and updated `verifyNarrativeArtPersistence.mjs`'s checks to
match. Also caught and fixed a self-inflicted issue before the second push: an
earlier `prettier --write` on the whole `stores/taskmasterStore.ts` and
`utils/scripts/verifyNarrativeArtPersistence.mjs` files reformatted large unrelated
regions (both files were already prettier-noncompliant on `main` before this change,
confirmed via `git checkout`/`git stash`) — reverted to the pristine originals and
re-applied only the intended edits via scoped string replacement, keeping the diff to
exactly what the task touches. Updated `verifyDaVinciArtResumeGuard.ts`'s narrow
textual checks (and its self-test) to track davinci-page.vue's new
`readCache()`/`writeCache()`-based shape.

Verified: 27 `test:davinci-*` + 23 `test:storybook-*` contract scripts pass,
`verifyNarrativeArtPersistence.mjs` passes, eslint/prettier clean except two
pre-existing unrelated issues confirmed present on `main` before this diff,
`vue-tsc --noEmit` clean except one pre-existing unrelated error (filed as kaizen
davinci/t-026). Both PRs (kind_robots#2051, conductor#2735) went fully green and were
merged; task closed to `status: done`.

**What was good:** did not treat the CI failure as a blocker to route around —
diagnosed the actual guard assertion, found the real missing call site, and fixed the
task's true scope rather than narrowing the task to dodge the failing check. Caught
my own unrelated-reformatting mistake by diffing against the pristine pre-change file
before committing, rather than shipping a bloated diff.

**What to improve:** the initial investigation should have grepped the whole repo for
`createNarrativeArtJobsController`/`resumeNarrativeArtJobs` before scoping the
composable, instead of trusting the task note's "two call sites" framing at face
value — a repo-wide symbol search would have found taskmasterStore.ts before the
first push, not after a red CI check.

**Kaizen task:** filed davinci/t-026 — fix the pre-existing stale `prisma/generated`
client (`BUTTERFLY` missing from `Reaction_reactionCategory`'s `ExpectedTargetField`
map in `server/api/reactions/index.post.ts`), surfaced by `vue-tsc` but unrelated to
this task.

---
_Generated by [Claude Code](https://claude.ai/code)_
