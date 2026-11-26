# Hourly worker entrypoint

Use AGENTS.md as the single operating contract. For an explicit assignment, proceed directly; otherwise use the live role selector or connector STATUS.md pickup hints and open PRs. Read only the selected role, CONTROL.md global overview and chosen project/task. Resolve dependencies and verify ownership before implementation. For the assigned project consult [master issue index](../docs/agents/master-issues.yaml) and [targeted context](../docs/agents/project-issue-context.md) only as needed.

Use existing deterministic maintenance signals; run a targeted sweep to investigate a failed or stale signal, not a full portfolio scan before every assignment. Human-answer-unread is actionable: inspect the actual answer from audit_human_gates.py even if status remains needs-human. Respect actual approvals and never infer a gate was cleared.

Deliver one scoped tested improvement, open PR, merge only verified green ungated work and reconcile canonical task state. Continue independent eligible work while CI runs. Report evidence and real blockers; do not invent tasks or stop at inventory.

Prior details: [reference](../docs/agents/hourly-worker-reference-2026-11-26.md) (on demand only; current contract wins).
