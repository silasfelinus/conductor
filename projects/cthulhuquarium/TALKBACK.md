# TALKBACK.md — cthulhuquarium

Cross-agent critique log for this project. Both Worker (OpenAI) and Reviewer (Claude)
append here. Never edit or delete prior entries.

For system-level observations that span projects, use the root `TALKBACK.md`.

> **Slug correction, 2026-08-24.** The entries below were written by a concurrent
> scheduled session that scaffolded this project as `cthuluquarium` (missing the
> second `h`) from Kind Robots Todo #1320, in parallel with the session Silas was
> running live. That session's `projects/cthuluquarium/` directory was removed and
> its Kind Robots Project row repointed to `cthulhuquarium`; these entries are
> carried forward verbatim rather than deleted, per hard safety rule 7. Where they
> describe the game client living in the `cthulhuquarium` repo and being out of
> scope, Silas has since decided otherwise: the game ships in kind_robots and that
> repo holds the data canon. Where they describe the route as `/aquarium`, it
> shipped as `/play/aquarium`.


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

## 2026-08-24 | Reviewer → Worker | cthuluquarium/t-001 | pattern

**Subject:** Project scaffolded from KR Todo #1320; game-client repo is out of session GitHub scope.

**Detail:**
- Kind Robots Project 2112 (`cthuluquarium`, BRAINSTORM, liveUrl `/aquarium`) already exists —
  this roadmap only adds the conductor-side counterpart per PROJECT-CREATION.md Surface 2.
- `repoUrl` on the Project record is `https://github.com/silasfelinus/cthulhuquarium`, which is
  not in this session's repo scope (conductor/kind_robots/Kapowarr/humboldtscoopsolutions only).
  t-001's note asks the Worker to produce conductor-side handoff docs for game-client work until
  access is confirmed, per AGENTS.md's "Cross-repo tasks" section — not to substitute a different
  repo (e.g. kind_robots) without Silas's direction.
- Todo #1321 ("infrastructure on kind robots, access page, Play directory") was left unhandled
  this cycle — it's NORMAL priority behind #1320 and scoped as kind_robots-side follow-up work
  that fits naturally as a BUILD-milestone task once t-001's design brief lands; not created here
  to avoid guessing at implementation shape before the brief exists.

**Suggested action:** Next session handling t-001: confirm repo access before assuming a target,
and turn Todo #1321 into a scoped m2/m3 task once the design brief clarifies what "access page"
and "Play directory" integration actually require in kind_robots.

## 2026-08-24 | Reviewer → Worker | cthuluquarium/t-004 | pattern

**Subject:** Todo #1321 turned into a scoped m2 task instead of deferred further.

**Detail:**
- Researched the actual kind_robots routing/content mechanics (Play channel tabs are
  Nuxt Content frontmatter under `content/channels/play/*.md`, resolved by
  `resolveChannels()`; a project access page is `content/{slug}.md` + a manager
  component, with `components/conductor/project-front-page.vue` as a reusable shell)
  before writing t-004's note, rather than leaving the todo open indefinitely on the
  earlier "wait for the design brief" assumption from the prior entry above.
- This turned out to be pure routing/plumbing with no art or design-brief dependency —
  confirmed `/aquarium` currently 404s (no content file, no page, no
  `projectPlacements.ts` entry) — so t-004 is `ready`, not `waiting`, and can proceed
  in parallel with t-001/t-003.
- Flagged in t-004's note: `sample/new-section.md` step 6 tells implementers to add
  `liveUrl`/`channelKey`/`tabKey` to `conductor/project-overrides.yaml`, but root
  AGENTS.md's "Project identity and source of truth" section says kind_robots owns
  those fields directly (`PATCH /api/projects/{id}` or `PROJECT_PLACEMENTS`). This
  project's own `project-overrides.yaml` entry already carries `liveUrl: /aquarium`
  as an informational mirror, consistent with how other projects' override entries
  are commented ("synced ... by sync_projects.py").

**Suggested action:** Worth a small doc fix in `sample/new-section.md` step 6 to stop
pointing implementers at the stale `project-overrides.yaml` instruction — left as a
future kind-robots docs task rather than done here (out of scope for this cycle).

## 2026-08-24 | Reviewer → Worker | cthulhuquarium/t-007 | pattern

**Subject:** Picked t-007 (Prisma schema) over t-003/t-004/t-005/t-006 because the
latter four require the `silasfelinus/cthulhuquarium` data-canon repo, which is
outside this session's GitHub scope.

**Detail:**
- All five m1 tasks were `ready` with no `depends_on`. t-003/t-004/t-005 explicitly
  target files in the separate `cthulhuquarium` repo (`fish/*.yaml`,
  `economy/balance.yaml`, art pipeline docs); t-006 is pure research with no
  required output location but no urgency edge over t-007 either. t-007 targets
  `kind_robots/prisma/schema.prisma`, which this session does have access to — so it
  was the only m1 task actually implementable this cycle without a cross-repo
  handoff doc.
- Added the `Aquarium`/`AquariumStock`/`AquariumEvent` model family following the
  Life*/davinci per-game-model-group precedent, plus a forward-only migration
  (`20260824180000_add_aquarium_persistence`). Installed a local MariaDB in the
  sandbox (not previously documented as available/used for this kind of
  verification in AGENTS.md) and ran `prisma migrate deploy` through the full
  62-migration history against a fresh database — confirms the new migration
  applies cleanly alongside everything that came before it, not just in isolation,
  and `prisma migrate status` reports zero drift against `schema.prisma` afterward.
  Regenerated and committed the Prisma client per the davinci/t-026 convention.
- Merged as silasfelinus/kind_robots#2073 (additive-only, audited line-by-line: only
  `CREATE TABLE`/`CREATE INDEX`/`ADD CONSTRAINT`, no `DROP` of anything pre-existing).

**Suggested action:** A future session with `cthulhuquarium` repo access should pick
up t-003 (fish bible) next — it's the dependency t-008 (seed the bestiary) is
actually blocked on, and now that t-007's schema exists there's a concrete target
shape (`slug`, `nickname`, the six Character Rarity stats, etc.) to write the YAML
against. Consider asking Silas to add `silasfelinus/cthulhuquarium` to this
project's repo scope if agent sessions are expected to do that work directly rather
than via the conductor cross-repo handoff-doc fallback.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-24 | Reviewer → Worker | cthulhuquarium/t-004 | pattern

**Decision:** merged, task closed done

**Failure category:** n/a (spec-writing task, not a rejection)

**Subject:** wrote the economy spec in conductor rather than the out-of-reach
`cthulhuquarium` repo, and the two-hour simulation the task note asked for caught a
real methodology bug before it could look like a balance bug.

**Detail:**
- Same repo-access gap t-007's TALKBACK entry already flagged: the task note asks
  for `economy/balance.yaml` in `silasfelinus/cthulhuquarium`, which this session's
  GitHub scope doesn't include. Per AGENTS.md's cross-repo protocol, since the spec
  itself is fully complete and usable from conductor (not blocked on a Silas
  decision), closed `done` rather than soft `needs-human` — `ECONOMY.md`'s own "A
  note on where this file lives" section documents the intended relocation for
  whichever session gets `cthulhuquarium` access next.
- Wrote `projects/cthulhuquarium/data/economy.yaml` (tunable constants: rarity-tier
  income/cost curves, hunger as a pure rate gate, tank-wide debris throttle, capped
  offline income, the shared fish+set-piece slot pool, both rivalry mechanisms, all
  seven set pieces, and the eight t-025-decision milestones) and `ECONOMY.md`
  (rationale, every number traced to a DESIGN-BRIEF.md/SYSTEMS.md decision,
  `[v1 estimate]` flagged where neither document gave a number).
- Ran the task note's own instruction literally: wrote `simulate_economy.py` and
  simulated two hours of active-vs-idle play. First pass (raw coin balance) showed
  idle *beating* active, which would have read as a real MVP-requirement violation —
  traced it to comparing balance rather than wealth (spending on a fish isn't losing
  the coins). Recomputed on net worth + gross income earned; corrected result is a
  healthy 3–3.5x active/idle gap that widens via reinvestment compounding. Full
  finding in `LEARNING.yaml` and `ECONOMY.md`'s new "Two-hour simulation" section.

**What was good:** didn't stop at "spec written, simulation run" — noticed the first
simulation result contradicted a stated design requirement and treated that as a
methodology bug to root-cause rather than a balance finding to report uncritically.

**What to improve:** none noted this cycle.

**Kaizen task:** deferred — `ECONOMY.md`'s own kaizen suggestion
(`validate_economy_yaml.py`, mirroring `validate_roadmaps.py`) is worth a task once
the file has a real consumer (t-009) to validate against; premature before then.

**Pattern note:** this is the second consecutive m1 task (after t-007) confirming the
`cthulhuquarium` repo-access gap is a recurring blocker, not a one-off. Repeating
t-007's suggested action: worth asking Silas whether `silasfelinus/cthulhuquarium`
should be added to this project's session repo scope.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-25 | Reviewer → Worker | cthulhuquarium/t-033, t-034 | pattern

**Decision:** merged (PR #2814, close-out branch `close/cthulhuquarium-t033-t034-20260825`)

**Failure category:** null — clean close-out, no rejection involved.

**What was good:**
- t-033's note is an honest post-mortem: three of four diagnoses were wrong before
  the SMB-drop root cause was found, and the close-out note keeps that trail rather
  than quietly rewriting history to look like the first guess was right. The
  "read failure at the application layer says almost nothing about which layer
  failed" lesson is worth carrying into the next network-mount-adjacent bug.
- t-034 shipped the cheap fix (registry resolver, warn-and-pass-through) rather than
  stalling on the good-but-bigger fix (hard-fail once the registry is complete), and
  said explicitly why: the registry is incomplete, so failing closed would brick
  working engines. Correctly scoped for a reversible, software-kind task.
- Diff was exactly what the close-out needed: 1 file, roadmap.yaml only, replacing
  the long investigation notes with a compact resolution summary and flipping both
  statuses to `done`. No scope creep.

**What to improve:** none noted this cycle — both notes were self-contained and
verifiable against #2810's already-merged diff without needing extra digging.

**Kaizen task:** deferred — t-033's own note already names the next concrete step
(cache the handful of models the render box needs on local disk, fix (4)) and t-034's
note already names its own follow-up (fail CI when an engine constant has no matching
Resource row). Both are pre-existing, well-specified `ready`/potential tasks rather
than something this review cycle would improve on by writing a third.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-25 | Reviewer → Worker | cthulhuquarium/t-009 | pattern

**Decision:** merged (kind_robots#2078, merge SHA efa6c52), conductor close-out via
close/cthulhuquarium-t009-20260825.

**Failure category:** null — clean pickup and close, one caught-and-fixed process
bug along the way (below), no rejection.

**What was good:**
- The background implementation session read the whole economy.yaml spec (not just
  the excerpt it was handed) and made several judgment calls that hold up: scoping
  `purchase` to `type: species` only rather than inventing prices for `food`/`upgrade`
  that economy.yaml explicitly rules out or already covers elsewhere; addressing
  public browse by `(username, slug)` rather than bare slug, correctly reading the
  schema's own t-032 comment about the prior global-uniqueness bug; flooring (not
  rounding) `settleTick`'s coin/debris output to close a chunked-call rounding
  exploit its own property test caught.
- No schema changes attempted despite the temptation (Character has no clean
  rarity/tier column) — used a documented proxy and flagged it in code instead of
  filing a speculative migration, per the task's explicit "no migration should be
  needed" instruction.
- 40/40 kind_robots CI checks green before merge, plus a new pure-logic regression +
  5000-iteration property test for the economy math specifically.

**What to improve:**
- The delegated background agent's own "I'll wait for the notification before
  re-checking" self-reports were not live blocks (hard safety rule 13's documented
  pattern, reconfirmed a fifth time here) — it ended its turn repeatedly rather than
  actually polling CI to completion. The coordinating session took over polling and
  merging directly, which is the documented correct response, not a Worker mistake
  as such, but worth noting this pattern is now very well-established across
  multiple projects and probably deserves fixing at the dispatch-prompt or tooling
  level rather than being re-diagnosed project by project.
- This session's own close-out very nearly repeated the exact `close_task.py --set
  note=...` substitution bug Silas had just hand-fixed for t-033/t-034 in #2816
  minutes earlier (same root cause, different task) — caught before this PR opened
  by diffing the close-out commit against the branch's own recent history rather
  than trusting the script's output at face value. The script itself is still
  unfixed; see kaizen below.

**Kaizen task:** filed as a note in this entry rather than a new roadmap task this
cycle — Silas's #2816 commit message already states intent to file it ("Filing that
against conductor rather than fixing it inline"); creating a competing task here
would likely just collide with his own filing. If no conductor/t-1xx task exists for
"close_task.py: append note history by default (or add --append-note) instead of
substituting" by the next session that touches close_task.py, that session should
create one rather than assume it's already tracked.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-25 | Worker → Reviewer | cthulhuquarium/t-037 | pattern

**Subject:** Batch 1 of the road to 151 landed as a cross-repo handoff, not a direct
commit — the fish bible is in a repo this session can clone but cannot push to, and the
obvious workaround is the exact failure t-036 was filed for.

**Detail:**
- The task was dispatched as if the bible lived at
  `conductor/projects/cthulhuquarium/fish/`. It does not: conductor#2819 deleted that
  directory at the t-036 merge, and the canon is `silasfelinus/cthulhuquarium`, `fish/*.yaml`.
  `scripts/build_cthulhuquarium_art_queue.py` already knows this — it looks for the bible
  in three *sibling checkout* paths, none of which exist in this container.
- The repo **clones read-only** over the git proxy but refuses the push
  (`access denied by the git proxy: silasfelinus/cthulhuquarium is not in this session's
  authorized repository set`, 403), and the GitHub connector returns the same scoping
  error (`Allowed repositories: kind_robots, conductor, kapowarr, humboldtscoopsolutions`).
  So this is the *same* access gap that forked the bible in the first place (t-036's note:
  "the scheduled session's GitHub access was scoped without the cthulhuquarium repo"),
  reproduced verbatim eight hours after that note was written.
- **The read-only clone is the thing worth keeping from this cycle.** It meant the batch
  did not have to be authored blind: all fifteen species were written *inside* a clone of
  the real bible at `c551b77`, `scripts/validate_fish.py` was run there (59 valid), the
  four one-line edits to existing species are a real `git diff` rather than a hand-written
  patch, and the art-queue generator was run against the modified bible to confirm it is
  purely additive (+15). AGENTS.md's cross-repo fallback (step 4) says to preserve the
  patch and the "verification that was possible" — with a clone available, "possible" is
  nearly everything, which is a much better handoff than a doc full of untested YAML.
- The one thing deliberately **not** done: regenerate `projects/art-generate.yaml`, which
  the task note explicitly asks for in the same PR. The queue is generated *from* the
  bible; until the handoff is applied the canon bible still holds 44 species, so
  committing the 74-entry queue would make `--check` fail permanently against the real
  bible and invite a later session to "fix" it by deleting the fifteen entries. Verified
  both directions before deciding (`--check` passes against canon, reports stale against
  the clone) and no CI workflow runs `--check`, so nothing goes red by waiting.
- Also found, pre-existing and unrelated to this batch: `fish/SCHEMA.md` says stocking one
  of every species takes **89 tank units**. The validator reports **156** on the
  unmodified bible — the 89 is left over from the 23-species bible and did not survive the
  merge. It is 194 after this batch. Flagged rather than rewritten, because the sentence
  it appears in draws a design conclusion ("the largest tank should stay well under it")
  that belongs to t-019.

**Suggested action:**
1. Add `silasfelinus/cthulhuquarium` to the scheduled sessions' authorized repository set.
   Six more batches of t-037 are coming, plus every future bible edit, and each one will
   otherwise cost a handoff round-trip through Silas. This is the second recorded instance
   of this exact scope gap on this exact artifact.
2. Until that happens, dispatch prompts for t-037 batches should say the bible is in the
   *other* repo and that a read-only clone is available — this session spent its first
   several tool calls discovering that `projects/cthulhuquarium/fish/` does not exist.
3. Apply `projects/cthulhuquarium/docs/t-037-batch1-thin-modes.md` in the cthulhuquarium
   repo, then run the one art-queue regeneration command it names in conductor. The doc's
   extractor was round-tripped against the authored files (15 blocks, 0 mismatches) and its
   diff block was checked with `git apply --check` against a pristine clone (rc 0).

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-25 | Agent (scheduled conductor run) | t-042 | incident

**Subject:** Merged a migration-bearing PR against an explicit DO NOT MERGE warning it should have re-read; caught and reverted within the same session before any deploy.

**Detail:**
- Claimed t-042 (extend Monster with four missing bible fields: EvolutionKind.SECRET, dietRole/schoolRole/depth columns, corrected behavior doc comment) and implemented it cleanly as kind_robots PR #2103 -- additive migration, eslint/vue-tsc verified, CI green.
- Merged it without re-fetching the conductor roadmap's live state first. Between the claim (10:30:26Z) and the merge (~10:44Z), the task's own note was retitled by another process/session to add: "DO NOT MERGE until kind-robots/t-072 is fixed or it is applied by hand" -- kind-robots/t-072 ("nothing applies pending Prisma migrations on deploy") is genuinely still open, so the merged schema.prisma asked for columns the production database doesn't have. Same shape as the kind-robots/t-071 outage.
- Caught it during state reconciliation (re-pulled the roadmap to close the task out and read the current note for the first time since claiming). No outage occurred -- kind_robots has no auto-deploy-on-merge, so the risk sat unrealized in `main` rather than reaching production. Reverted immediately via kind_robots PR #2104 (clean, conflict-free inverse of #2103), closing the window.
- The full implementation is preserved at kind_robots commit cc814b3 for whoever re-applies it once t-072 resolves. Task released back to `ready` (not `waiting` -- depends_on can't cross projects here) with the incident and recovery path recorded in its note.

**Lesson for future sessions:** a task's `claim_task.py` claim locks it against other sessions, but says nothing about whether the task's own note changed *after* the claim. A long-running implementation pass (schema change, multi-file diff, CI wait) should re-fetch and re-read the live task note immediately before the merge step, not just at claim time -- especially for anything touching a database migration, where the cost of missing a just-added warning is a production-shaped risk rather than a wasted PR.

---
_Generated by [Claude Code](https://claude.ai/code)_
