# Conductor Portfolio Oversight

Generated: `2026-09-04T20:50:09.955732+00:00`

Overall status: **action-needed**

This is a deterministic sensor. For semantic roadmap/progress intent review, follow `projects/conductor/OVERSIGHT-AGENT.md`.

## OpenAI scheduled-agent heartbeat

- Latest visible OpenAI scheduled-Agent activity: `2026-09-04T20:11:54+00:00` (0.64h ago; overdue at 6.0h).
- Overdue: **false**
- Note: OpenAI commit activity is a heartbeat only; a clean no-op OpenAI cycle may leave no commit.

## Kind Robots ↔ Conductor project parity

- Forward drift (KR row claims missing roadmap): **0**
- Reverse orphans (active Conductor roadmap missing KR row): **0**

## Roadmap/CONTROL structural audit

- Errors: **1**
- Warnings: **2**
  - **GATED_DONE_WITHOUT_APPROVAL** — `kindrobots-unraid` / `t-014`: Human-gated task is done without approved_by_human: true.
- Warning details remain in `ROADMAP-AUDIT.md`; errors above take precedence for this sensor.

## Semantic intent review

- Latest: `INTENT-AUDIT-2026-09-01.md` (3 day(s) ago; due at 3.0 days).
- Due: **true**

## Agent routing

When action is needed, use `projects/conductor/OVERSIGHT-AGENT.md` before falling through to ordinary Worker/Reviewer selection.
