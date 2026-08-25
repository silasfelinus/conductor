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
