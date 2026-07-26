# AI Art Academy roadmap accuracy audit — 2026-07-26

## Scope

This pass checks the live roadmap against the work described in its own task notes. It does not change production systems, dispatch generation, or reinterpret human gates.

## Current milestone truth

| Milestone | Roadmap status | Evidence from task state | Assessment |
|---|---|---|---|
| m1 — Design brief, policy, and model strategy | done | t-001 and t-002 are done; scope approval is recorded | Accurate |
| m2 — Style registry and LoRA/knowledge evaluation | in-progress | t-003 is done; t-004 remains open and depends on t-037 | Accurate |
| m3 — Curriculum content | in-progress | Core outline work is done, but open curriculum work and approval-dependent items remain | Accurate |
| m4 — Academy front end | done | The milestone's implementation tasks are recorded as complete; later t-010 polish is recurring maintenance rather than unfinished milestone scope | Accurate |
| m5 — Project art and inspiration assets | in-progress | Asset-generation and promotion work remains open or operationally constrained | Accurate |
| m6 — Continuous improvement loop | in-progress | t-010 is recurring and intentionally never closes | Accurate |

## Material roadmap findings

### 1. t-004 is technically ready but operationally not session-ready

`t-004` is marked `ready`, and its dependency on `t-037` is satisfied, but the latest task note records a growing single-worker render backlog: 141 pending jobs, one running slot, and daily inflow exceeding completions at the last check. The task's actual deliverable requires multiple prompt-versus-LoRA comparisons and traceable result images, so claiming it without first checking queue health is likely to create another non-productive cycle.

This is not an undeclared code dependency anymore. It is a readiness precondition that should remain explicit in the task note:

- Check queue depth and oldest pending age before claiming.
- Proceed only when a small A/B batch can plausibly finish in one Worker cycle.
- Do not repeat the already-closed seed-overflow investigation unless fresh post-fix jobs show the same error.

The task can remain `ready` because the queue may recover between cycles, but selection logic should treat the queue-health check as the first acceptance gate rather than assuming `ready` means immediately executable.

### 2. t-010 rotation notes are carrying too much historical state

The recurring task note is now a long chronological execution log. That preserves provenance, but the actionable rotation state is buried among older runs. A future roadmap-maintenance task should move historical `RAN ...` entries into a dedicated run ledger while keeping only these fields in the task note:

- last completed lane
- next preferred lane
- current blockers relevant to lane selection
- latest merged PR and verification result

This pass does not perform that migration because changing the canonical history format deserves its own scoped task and regression check; silently pruning the note would be data loss wearing a tidy haircut.

### 3. Recurring polish work should not reopen m4

Front-end accessibility and race-condition fixes completed through t-010 are maintenance improvements after the Academy front-end milestone shipped. Keeping m4 at `done` is correct. The roadmap should continue treating t-010 lane 1 as continuous improvement under m6 rather than toggling m4 back to `in-progress` after every polish PR.

### 4. The next useful t-010 lane should not be another roadmap-only pass

This audit found no incorrect milestone status and no dependency that can be safely auto-resolved from repository state alone. The next preferred lane should therefore be one of:

1. front-end polish, after checking recent Academy PRs to avoid repeating an already-fixed accessibility pattern;
2. curriculum depth, using a movement or tradition not already represented in the candidate directory;
3. inspiration assets, only after checking queue health and avoiding generation work that cannot complete during the cycle.

A second consecutive roadmap audit would mostly create paperwork about the paperwork.

## Decisions recorded

- Keep milestone statuses unchanged.
- Keep t-004 at `ready`, but preserve queue-health verification as its first execution gate.
- Keep m4 at `done`; recurring front-end polish belongs to m6.
- Record this cycle as t-010 lane 2 (roadmap accuracy).
- Prefer lane 1 or lane 4 next, with lane 3 conditional on render-queue health.

## Kaizen suggestion

Add a small `continuous_improvement:` mapping to recurring tasks with `last_lane`, `next_lane`, `last_run`, and `last_pr`. Generate the human-readable history elsewhere. This would make selection deterministic without forcing agents to parse an archaeological dig site every hour.
