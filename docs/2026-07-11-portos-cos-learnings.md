# PortOS CoS → Conductor learnings (2026-07-11)

Design record for the changes landed on `claude/conductor-portos-comparison-wdpdoq`.
Source: a side-by-side analysis of Conductor (this repo) and the PortOS Chief-of-Staff
agent system (`atomantic/PortOS`, `server/services/cos*.js`), requested by Silas.

## The comparison in one paragraph

Conductor and the PortOS CoS are the same problem solved from opposite ends. Conductor
puts the intelligence in **documents and a social protocol**: Git+YAML substrate, two
agents (Worker/Reviewer) governed by prose law in AGENTS.md, judgment confined to
supervised sessions, escalation to the human on disagreement. CoS puts the intelligence
in **runtime machinery**: a deterministic PM2-managed scheduler (`dequeueNextTask`),
ephemeral LLM workers in isolated git worktrees, pattern-based error triage, and a
learning store that reroutes model choice by measured success rate. Conductor optimizes
for auditability and human trust; CoS optimizes for throughput and unattended
resilience. Neither is strictly better — but each has mechanisms the other lacks.

## What Conductor adopted (this change)

1. **Failure triage** (AGENTS.md § "Failure triage") — from CoS's `agentErrorAnalysis.js`
   `ERROR_PATTERNS` table, which classifies every agent failure as *actionable* (config/
   spec problem a retry can't fix → block immediately + investigation task) vs
   *transient* (→ retry with counter). Conductor previously treated every failed pass
   identically: 3 passes then `blocked`, burning budget on unretryable failures and
   escalating retryable ones. Now four categories — transient / actionable / quality /
   scope — decide whether a pass is consumed and where the task routes.

2. **Retry context** (AGENTS.md § "Retry context") — from CoS's compaction-on-retry
   (`buildCompactionSection`): a failed run's *reason for failure* is injected into the
   retry attempt's prompt. Conductor's analog: the Reviewer writes a `retry_context:`
   field on the task at rejection; the Worker must read it before re-claiming and say in
   the PR how the retry addressed it. Pass 2 no longer starts blind.

3. **Learning ledger** (AGENTS.md § "Learning ledger", `LEARNING.yaml`,
   `scripts/build_learning_summary.py` → `LEARNING-REPORT.md`) — from CoS's
   `taskLearning/` store (success rates by task type → model routing, adaptive
   cooldowns, skip-and-rehabilitate). Conductor's git-native analog: one append-only
   outcome record per closed task; a generated summary of success rates by project/kind
   and failure-category recurrence. Wired into kaizen: the Reviewer targets systematic
   weaknesses from the report instead of only per-merge one-off suggestions.

## What was considered and deferred (future updates)

Tracked as `ready` tasks in `projects/conductor/roadmap.yaml`:

- **Worktree-parallel Workers.** Conductor's one-atomic-claim-commit rule serializes the
  Worker. CoS runs 3 concurrent agents safely via a git worktree per agent
  (`worktreeManager.js`) plus claim leases for multi-machine federation
  (`cosTaskClaim.js`). Adopting this is a structural change to the claim protocol —
  needs a pitch, not a patch.
- **CI wiring for the learning report.** Regenerate `LEARNING-REPORT.md` on push like
  STATUS.md/KAIZEN.md, and run the new tests in Worker PR CI.
- **Ledger backfill.** Seed `LEARNING.yaml` from recent git history + TALKBACK so the
  report has signal before new closures accumulate.
- **kind_robots dashboard convergence.** kind_robots is already Conductor's web control
  plane (`server/api/conductor/*`), and a `portos-page.vue` placeholder exists. The
  interesting long-term shape: one dashboard, two backends — Conductor as the governance
  layer, CoS as an execution runtime.

## What CoS could adopt from Conductor (for the brother, informational)

- The **challenge protocol** (`status: challenged` + two-way TALKBACK): CoS sub-agents
  cannot dispute a reviewer verdict; a wrong rejection just gets "fixed."
- **`kind` as a safety type** (software/content/proposal changing what "done" means):
  CoS's confidence-tier auto-approval has no notion of inherently-outward-facing work.
- **Human-readable escalation prose** (the "FOR SILAS / TO APPROVE / what unblocks"
  note template) for CoS's investigation tasks.
- **Self-modifying operating manual with provenance** — Conductor folds incident
  learnings back into AGENTS.md with citations; CoS's rules live in code comments.
