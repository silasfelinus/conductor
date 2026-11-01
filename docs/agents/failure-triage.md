# Failure triage, retry context and the learning ledger

> Moved verbatim from `AGENTS.md` on 2026-11-01 PT (token-essentialization pass 2). `AGENTS.md`
> keeps the condensed rule and links here; this file holds the full detail and the incident
> history behind it. If the two ever disagree, the rule in `AGENTS.md` wins — fix this file.
> Read when a pass fails, a task is rejected, or a task closes with a lesson.

## Failure triage — classify before you retry or escalate

(Adopted 2026-07-11 from the PortOS CoS error-triage design — see
`docs/2026-07-11-portos-cos-learnings.md`.) A failed pass is not one thing. Before
deciding what happens next, whoever observed the failure (Worker mid-task, or Reviewer
on rejection) assigns one of four categories. The category decides whether the pass
budget is spent and where the task goes:

| Category | What it looks like | Route | Consumes a pass? |
|---|---|---|---|
| **transient** | Environment hiccup unrelated to the work: connector/tooling failure, rate or session limits, CI flake, generated-file merge noise, network errors | Retry within the cycle if cheap; otherwise leave `ready` with a note and move to other work | No |
| **actionable** | The task cannot succeed as specified no matter how many retries: missing access/credentials for the core work, stale or wrong task spec, an undeclared dependency, verification permanently impossible | Do NOT retry. Fix the roadmap (add `depends_on`, create the prerequisite task) or go straight to soft `needs-human` with a FOR SILAS note | No — retrying is waste |
| **quality** | The work was attempted and is wrong: bugs, scope violations, verification gaps, doesn't do what the task says | Reviewer rejects with `retry_context` (below), task back to `ready`, Worker retries | Yes — this is what the budget is for |
| **scope** | The task is too big to land in one pass: oversized diff, half-finished work, "and also" sprawl | Split it: create smaller `ready` tasks covering the remainder; the original either shrinks to its landable core or goes `waiting` on the new parts | Yes (the failed attempt), but stop retrying the monolith |

Rules:
- Only **quality** and **scope** failures increment `passes`. A transient or actionable
  failure never burns the budget — the budget exists to bound *rework*, not to punish
  environment problems.
- **Sandbox egress blocks** (a `transient` network failure that recurs across sessions,
  e.g. a museum/CDN/API host the agent proxy's allowlist rejects) belong in the shared
  `EGRESS-BLOCKERS.md` ledger, not a new hand-written "RECHECKED &lt;date&gt;..." paragraph
  on the task. Run `python scripts/recheck_egress_blocks.py <host> --task <project>/<task-id>`
  to probe and stamp a dated entry; link the task note to the ledger instead of repeating
  the recheck prose each cycle (conductor/t-052).
- On **actionable**: escalate or fix the roadmap the FIRST time. Burning three passes on
  a task that can never succeed as specified is the failure mode this section exists to
  prevent.
- On **scope**: prefer decomposition over a third heroic attempt. Scope discipline
  (hard rule 6) already says unrelated problems become new tasks — this extends it to
  oversized related work.
- The Reviewer records the category as `**Failure category:**` in its rejection feedback
  and in the learning ledger (below). A Worker that self-triages mid-task records it in
  the task `note:`.
- When genuinely unsure between transient and quality, treat it as quality (spend the
  pass). When unsure between quality and actionable, spend one pass before escalating.

### Retry context — failed passes must teach the next one

When the Reviewer rejects a task (`status: ready`, `passes` incremented), it also writes
a `retry_context:` field on the task in `roadmap.yaml`:

```yaml
retry_context: >
  pass 1 failed (quality): <what specifically went wrong, with file/PR reference>.
  Do differently: <the concrete change of approach for the next attempt>.
```

- The Worker MUST read `retry_context` before re-claiming any task with `passes > 0`,
  and the retry PR's "Flags for Reviewer" section must say how the attempt addressed it.
- The Reviewer overwrites `retry_context` on each subsequent rejection (git history
  preserves priors) and removes the field when the task reaches `done`.
- A task at `passes > 0` with no `retry_context` is a template-discipline gap — the
  Worker should note it in TALKBACK and reconstruct the context from the PR comments
  before retrying blind.
- `retry_context` can go stale when a human merges the referenced PR directly,
  bypassing the reject-retry loop (Silas can and does override a Reviewer rejection).
  Before acting on a `retry_context` for a cross-repo task, check whether the PR it
  references already merged — or whether the task's `passes`/`status` otherwise looks
  inconsistent with an open PR — and re-verify against current target-repo `main`
  first, rather than assuming the recorded rejection still holds. See
  ruler-hooked/t-012 (conductor/t-074) for the case that prompted this: a
  `retry_context` sat stale for 5 days describing a rejection Silas had already
  overridden by merging directly.

## Learning ledger — outcomes feed back into behavior

Kaizen improves the system one suggestion per merge; the ledger makes *systematic*
weaknesses visible across tasks, projects, and cycles (adopted from the PortOS CoS
task-learning design). `LEARNING.yaml` at the repo root is an append-only ledger of
task outcomes.

**When a task closes** (`done`, `blocked`, or cancelled by Silas), the agent that closes
it appends one record:

```yaml
- date: YYYY-MM-DD
  project: <slug>
  task: <task-id>
  kind: software | content | proposal
  stakes: reversible | outward-facing | irreversible
  passes: <final pass count>
  outcome: done | blocked | cancelled
  failure_category: transient | actionable | quality | scope | null
  lesson: "one sentence — what the next similar task should know"
```

- Append-only, same rule as TALKBACK: never edit or delete a prior record.
- `failure_category` is `null` for clean first-pass successes; for anything that burned
  a pass or blocked, use the triage category of the *dominant* failure.
- Recurring tasks don't get a record per cycle — only if one cycle blocks or teaches
  something worth a `lesson`.
- `python scripts/build_learning_summary.py` regenerates `LEARNING-REPORT.md`
  (auto-generated, read-only — same rules as STATUS.md / KAIZEN.md).
- **Kaizen targeting:** before creating the kaizen task on a merge, the Reviewer checks
  `LEARNING-REPORT.md`. If a systematic weakness (success rate < 60% for a project or
  kind with 3+ records, or a failure category recurring 3+ times) applies to the project
  at hand, the kaizen task targets that weakness instead of a generic improvement.
