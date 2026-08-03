# Pitch: Port conductor's `branch-janitor` to kind_robots

date: 2026-07-28
project-target: ai-networker-itself
status: rejected

## The idea

Conductor already solved "runs kept ending with open PRs / stranded branches"
with `scripts/branch_janitor.py` + `.github/workflows/branch-janitor.yml`
(hourly + `workflow_dispatch`, auto-deletes `claude/*`/`worker/*` branches that
are strict ancestors of `main`, reports-but-never-auto-deletes genuinely stale
unmerged branches, and takes a `force_delete_branches` list for verified-superseded
ones — see `projects/conductor/roadmap.yaml` t-060, done 2026-07-16). kind_robots
has no equivalent. Sessions working kind_robots PRs hit the exact same
ref-deletion-403 sandbox limitation conductor was built to route around, but with
nowhere to route it to — two separate TALKBACK entries this week (`ai-art-academy/t-010`,
2026-07-28) note a superseded kind_robots branch that "could not be deleted from
this session... and kind_robots has no `branch-janitor`-equivalent workflow to
force-delete it via `workflow_dispatch`, unlike conductor," each ending with "no
automated path to actually clear it for kind_robots." Port the same tooling over.

## Why it's worth doing

- **The fix already exists and is proven in production on a sibling repo** — this
  is a straight port of `scripts/branch_janitor.py` + the workflow YAML, not a new
  design. Low risk, mirrors CONTROL.md's standing preference for reusing systems
  over inventing them.
- **The gap is actively costing cleanup time right now, not hypothetically** — two
  independent TALKBACK entries in the same week flagged the identical missing
  capability from two different task sessions, each having to just leave a stray
  branch behind with a note instead of clearing it.
- **kind_robots has strictly more PR volume than conductor** (its own PR numbers
  are already in the 1000s per recent TALKBACK entries), so the same
  stranded-branch accumulation problem conductor hit is, if anything, more likely
  to recur there, not less.
- **Reversible and low-stakes**: the janitor only deletes branches that are strict
  ancestors of `main` (already-merged) by default, and only ever reports (never
  force-deletes) anything else unless a human explicitly lists it — same safety
  envelope already proven safe in conductor.

## Rough effort

small — porting an existing, tested script + workflow file to a second repo,
adjusting only repo-specific constants (branch prefixes already match the
`claude/*`/`worker/*` convention both repos share).

## Suggested first task

Copy `scripts/branch_janitor.py` and `.github/workflows/branch-janitor.yml` into
kind_robots, adjusting only the repo name/constants (no logic changes — this repo's
branch-naming convention already matches). Port the existing
`tests/test_branch_janitor.py` suite alongside it so the safety invariants (never
auto-delete a non-ancestor branch, `force_delete_branches` requires an explicit
list) are verified in the new repo the same way they are here. Note in the PR that
this doesn't touch conductor's own janitor at all — it's an independent copy scoped
to kind_robots' own branches.

## Existing-work check

Closest existing work inspected: `projects/conductor/roadmap.yaml` t-060 (the
original branch-janitor implementation and its rationale) and this week's
`TALKBACK.md` entries dated 2026-07-28 (`ai-art-academy/t-010` closeout, and the
`select_role.py` GitHub-API-403 entry) which independently surfaced the missing
kind_robots equivalent as a real, current gap rather than a speculative one. No
existing pitch or kind_robots roadmap task proposes this; `kind-robots/roadmap.yaml`
and `kindrobots-unraid/roadmap.yaml` were checked directly and contain no
branch-cleanup or janitor-related task. This is distinct from the separate,
already-flagged "close-out collision" observation in the same TALKBACK entry (two
sessions both closing out the same task) — that is a claim/workflow-sequencing
question Silas was explicitly left to weigh in on, not a tooling gap, and this
pitch does not attempt to resolve it.
