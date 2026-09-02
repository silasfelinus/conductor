# Conductor Portfolio Oversight

Generated: `2026-09-02T21:07:45.191843+00:00`

Overall status: **action-needed**

This is a deterministic sensor. For semantic roadmap/progress intent review, follow `projects/conductor/OVERSIGHT-AGENT.md`.

## OpenAI scheduled-agent heartbeat

- Latest visible OpenAI scheduled-Agent activity: `2026-09-02T14:17:57+00:00` (6.83h ago; overdue at 6.0h).
- Overdue: **true**
- Note: OpenAI commit activity is a heartbeat only; a clean no-op OpenAI cycle may leave no commit.

## Kind Robots ↔ Conductor project parity

- Forward drift (KR row claims missing roadmap): **0**
- Reverse orphans (active Conductor roadmap missing KR row): **0**

## Roadmap/CONTROL structural audit

- Errors: **3**
- Warnings: **2**
  - **GATED_DONE_WITHOUT_APPROVAL** — `ai-art-academy` / `t-077`: Human-gated task is done without approved_by_human: true.
  - **GATED_DONE_WITHOUT_APPROVAL** — `mandarin-tutor` / `t-010`: Human-gated task is done without approved_by_human: true.
  - **GATED_DONE_WITHOUT_APPROVAL** — `mandarin-tutor` / `t-020`: Human-gated task is done without approved_by_human: true.
- Warning details remain in `ROADMAP-AUDIT.md`; errors above take precedence for this sensor.

## Semantic intent review

- Latest: `INTENT-AUDIT-2026-09-01.md` (1 day(s) ago; due at 3.0 days).
- Due: **false**

## Agent routing

When action is needed, use `projects/conductor/OVERSIGHT-AGENT.md` before falling through to ordinary Worker/Reviewer selection.
