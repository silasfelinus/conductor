# Roadmap state reconciliation

Conductor is the authoritative coordination record for project lifecycle, roadmap task state, dependencies, human gates, and agent claims. Kind Robots may present and cache that state, but it must not invent a second independent truth for the same fields.

A task is not finished when code merely reaches another repository. It is finished when the implementation, verification, and Conductor bookkeeping agree.

## Lifecycle-aware visibility

Always read `project-overrides.yaml` before scanning roadmaps.

- `active` projects participate in normal task selection, human-gate reports, notifications, and drift audits.
- `paused`, `retired`, and `finished` projects are preserved history. Exclude them by default.
- Include inactive projects only for an explicit archival audit or when Silas asks to review them.

A paused task is not deleted or silently closed. It simply stops competing for attention until the project is resumed.

## Reconcile in the same session

After any of these events, re-fetch the live roadmap and reconcile the matching task before the session ends:

1. The implementation PR merges.
2. A production incident meets its documented recovery criteria.
3. Silas explicitly approves, rejects, or otherwise decides a human gate.
4. A task note or linked artifact proves the requested work already exists.
5. A dependency resolver or recurring-task transition changes what is actionable.

Reconciliation includes all relevant fields, not only `status`:

- task status;
- `approved_by_human` when the current session contains Silas's decision;
- owner and claim fields when the transition should clear them;
- milestone status when every task in that milestone is complete;
- dependency resolution;
- a concise completion or decision note.

Use `task-events` or the documented close-out helper rather than hand-editing history casually. Verify that the processor applied the event. Creation of an event is not completion.

## Closing human gates safely

Do not auto-close a genuine preference, policy, private-infrastructure, payment, publication, privacy, or irreversible decision.

A human gate may be closed during a Silas-directed reconciliation session when objective evidence shows the gate's requested outcome already happened. Examples include:

- Silas directly merged the gated implementation PR;
- the task's own recovery criteria are met and verified;
- the task note says there is nothing left to approve and the named tests now pass;
- Silas explicitly confirms the requested local action or decision in the current conversation.

An unknown root cause does not require a recovered incident to remain open forever. Close the recovery task when its recovery bar is met, then file a separate root-cause or prevention task when that work remains useful.

## Required audits

Run these during startup and before final reporting when roadmap state may have changed:

```bash
python scripts/check_pr_merged_drift.py
python scripts/audit_human_gates.py
```

Both commands exclude inactive projects by default. Use `--include-inactive` only for an intentional archive sweep.

`check_pr_merged_drift.py` finds in-progress tasks whose referenced PR already merged.

`audit_human_gates.py` finds active `needs-human` tasks and highlights structural contradictions or language suggesting a resolved gate was never closed. Its suggestions are review prompts, not authorization to bypass a genuine gate.

## Final report invariant

Before saying the work is complete:

1. Re-fetch the relevant roadmap from `main`.
2. Confirm the task and milestone state match reality.
3. Confirm any task event was consumed.
4. Confirm the implementation PR is merged or explicitly parked at a genuine gate.
5. Report remaining human gates from active projects only, unless inactive projects were explicitly requested.
