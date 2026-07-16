# Pitch: Concurrent Worker claims via per-project leases (bounded parallelism)

date: 2026-07-16
project-target: ai-networker-itself
status: awaiting-silas

## The idea

Let more than one Worker session hold a claim at once, safely, by turning the
current single-claim rule into a **bounded, leased** one. Today AGENTS.md hard
rule 4 ("one task in flight at a time... never hold two active claims at once")
plus the one-atomic-claim-commit protocol effectively serialize all Worker
throughput onto a single lane, even though `scripts/claim_task.py` /
`roadmap_claims.py` already implement most of what concurrency needs: a
`claimed_by`/`claimed_at` lease, a `CLAIM_TTL_MINUTES` (90) staleness expiry, and
a re-check-against-`origin/main`-then-retry loop that fails a losing session into
`ALREADY_CLAIMED`. PortOS CoS (docs/2026-07-11-portos-cos-learnings.md) runs 3
concurrent agents with a git worktree per agent plus claim leases; this pitch
evaluates adopting the same shape here.

The change is **not** "remove the safety rule" — it's "replace *global serial*
with *per-project mutual exclusion + a global concurrency cap*":

- **Per-project lease (unchanged granularity):** at most one active claim per
  `project/task` — already true. Add: at most one active claim *per project* at a
  time is the conservative v1 (keeps TALKBACK/roadmap edits within a project
  single-writer), or drop straight to per-task if we accept per-project TALKBACK
  contention (see risks).
- **Global cap N:** a session may only claim if fewer than N claims are currently
  active across the board (N=3, matching PortOS). Enforced the same way claims are
  today — read live `origin/main`, count non-stale `claimed` tasks, refuse over cap.
- **Worktree isolation:** each concurrent Worker operates in its own git worktree
  so their branches, indexes, and rebases never collide on a shared checkout.

## Why it's worth doing

Tonight's autonomous batch is concrete evidence of the serialization tax. Working
five conductor tasks in one session, every task paid the same overhead **in
sequence**: `claim_task.py` (a push to main) → new branch off the fresh tip →
implement → rebase onto whatever auto-`chore:` commits landed meanwhile →
`create_branch` (413 workaround) → delta push → PR. Between my tasks, other
sessions' claims and the STATUS.md refresh bot advanced `main` repeatedly, so I
rebased before nearly every push. That friction is inherent to a single lane
being shared by bursty, hourly, and ad-hoc sessions — and it *grows* with more
agents contending for the one lane, not shrinks.

The building blocks are already here, which is what makes this cheap to pilot:

- **Leases exist.** `roadmap_claims.py` already stamps `claimed_by`/`claimed_at`
  and treats a claim older than `CLAIM_TTL_MINUTES` as reclaimable — the exact
  staleness mechanism concurrency needs so a crashed agent can't wedge a lane.
- **Collision handling exists.** `claim_task.py` already re-reads `origin/main`
  immediately before writing the claim and retries under a push race, failing the
  loser into `ALREADY_CLAIMED` (the fix from the 2026-07-14 double-build incident).
  A global-cap check is one more predicate in that same critical section.
- **The default outcome is already "updated main."** Nothing about parallel lanes
  changes what a task *produces*; it changes how many can be in flight.

Upside: on a board with many independent `ready` tasks (tonight there were ~20
egress-free ones alone), N=3 is close to a 3× wall-clock speedup for burst cycles,
with no change to review quality — each lane still opens its own scoped PR.

## Rough effort

medium

The claim/lease primitives exist; the work is (1) a global-cap check in the claim
critical section, (2) worktree-per-session orchestration in the session harness
(the biggest piece, and partly a runner concern, not a repo concern), (3)
AGENTS.md rule changes, and (4) hardening the shared-writer surfaces (TALKBACK,
LEARNING.yaml, roadmap) against concurrent appends.

## Suggested first task

Write a **design doc** (`projects/conductor/docs/concurrent-claims.md`), not code,
that pins the contention model before any harness change:

1. **Lease semantics:** confirm `CLAIM_TTL_MINUTES` is the right staleness bound
   for parallel lanes and define what a session must do if its own lease expires
   mid-task (currently nothing enforces re-validation before the PR).
2. **The cap check:** specify the exact predicate added to `claim_task.py`'s
   critical section — "count active non-stale claims on `origin/main`; refuse if
   ≥ N" — and whether the cap is global or per-project.
3. **Shared-writer safety:** TALKBACK.md, LEARNING.yaml, and roadmap.yaml are
   append/edit targets. Today serialization hides the contention; enumerate which
   are append-only (safe under concurrent add with rebase) vs. edit-in-place
   (need a merge strategy), and confirm hard rule 9's "auto-gen conflicts resolve
   to main" already covers STATUS.md/workspace.html/ROADMAP-AUDIT.* churn (t-045
   just codified the rebase-before-PR step that makes this tractable).
4. **Rollout:** propose N=2 behind a flag on one high-volume project first, measure
   collision/`ALREADY_CLAIMED` rates, then widen.

Keep it pitch-then-design; the structural risk (two Workers merging conflicting
roadmap/TALKBACK edits) must be settled on paper before the harness runs lanes in
parallel.
