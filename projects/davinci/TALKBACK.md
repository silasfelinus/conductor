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
