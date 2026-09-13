# Conductor Portfolio Oversight

Generated: `2026-09-13T12:00:53.139292+00:00`

Overall status: **action-needed**

This is a deterministic sensor. For semantic roadmap/progress intent review, follow `projects/conductor/OVERSIGHT-AGENT.md`.

## OpenAI scheduled-agent heartbeat

- Latest visible OpenAI scheduled-Agent activity: `2026-09-13T11:32:32+00:00` (0.47h ago; overdue at 6.0h).
- Overdue: **false**
- Note: OpenAI coordination activity is a heartbeat only; a clean no-op OpenAI cycle may leave no commit.

## Kind Robots ↔ Conductor project parity

- Forward drift (KR row claims missing roadmap): **0**
- Reverse orphans (active Conductor roadmap missing KR row): **0**

## Roadmap/CONTROL structural audit

- Errors: **2**
- Warnings: **7**
  - **READY_WITH_UNMET_DEPS** — `storybook` / `t-035`: Ready task has unmet dependencies: t-034.
  - **READY_WITH_UNMET_DEPS** — `storybook` / `t-036`: Ready task has unmet dependencies: t-035.
- Warning details remain in `ROADMAP-AUDIT.md`; errors above take precedence for this sensor.

## Semantic intent review

- Latest: `INTENT-AUDIT-2026-09-10.md` (3 day(s) ago; due at 3.0 days).
- Due: **true**

## Agent routing

When action is needed, use `projects/conductor/OVERSIGHT-AGENT.md` before falling through to ordinary Worker/Reviewer selection.
