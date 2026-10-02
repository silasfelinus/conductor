# Conductor Portfolio Oversight

Generated: `2026-10-02T22:20:08.486774+00:00`

Overall status: **action-needed**

This is a deterministic sensor. For semantic roadmap/progress intent review, follow `projects/conductor/OVERSIGHT-AGENT.md`.

## Legacy OpenAI scheduled-agent git diagnostic

- Latest visible OpenAI scheduled-Agent activity: `2026-10-02T19:47:22+00:00` (2.55h ago; overdue at 6.0h).
- Stale by legacy threshold: **false**
- Authoritative for ChatGPT scheduler health: **false**
- Note: Legacy git diagnostic only: OPENAI-SCHEDULED-HEARTBEAT.json and coordination markers do not determine ChatGPT scheduler health. Native ChatGPT task metadata is authoritative for scheduler liveness.

## Kind Robots ↔ Conductor project parity

- Forward drift (KR row claims missing roadmap): **3**
- Reverse orphans (active Conductor roadmap missing KR row): **0**
  - `kind-word-puzzles` claimed by KR Project #2127 'kind-word-puzzles', but the roadmap is missing.
  - `robot-dress-up` claimed by KR Project #2126 'robot-dress-up', but the roadmap is missing.
  - `hidden-robots` claimed by KR Project #2125 'hidden-robots', but the roadmap is missing.

## Roadmap/CONTROL structural audit

- Errors: **0**
- Warnings: **8**
- Warning details remain in `ROADMAP-AUDIT.md`; errors above take precedence for this sensor.

## Semantic intent review

- Latest: `INTENT-AUDIT-2026-09-29.md` (3 day(s) ago; due at 3.0 days).
- Due: **true**

## Agent routing

When action is needed, use `projects/conductor/OVERSIGHT-AGENT.md` before falling through to ordinary Worker/Reviewer selection.
