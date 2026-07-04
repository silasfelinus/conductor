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
