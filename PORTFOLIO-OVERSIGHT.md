# Conductor Portfolio Oversight

Generated: `2026-08-29T20:59:02.441104+00:00`

Overall status: **action-needed**

This is a deterministic sensor. For semantic roadmap/progress intent review, follow `projects/conductor/OVERSIGHT-AGENT.md`.

## OpenAI scheduled-agent heartbeat

- Latest visible OpenAI scheduled-Agent activity: `2026-08-29T20:36:35+00:00` (0.37h ago; overdue at 6.0h).
- Overdue: **false**
- Note: OpenAI commit activity is a heartbeat only; a clean no-op OpenAI cycle may leave no commit.

## Kind Robots ↔ Conductor project parity

- Forward drift (KR row claims missing roadmap): **0**
- Reverse orphans (active Conductor roadmap missing KR row): **0**

## Roadmap/CONTROL structural audit

- Errors: **3**
- Warnings: **9**
  - **CONTROL_PRIORITY_DRIFT** — `_global`: CONTROL.md priority band ['interface-vision', 'ai-art-academy', 'coloring-book', 'humboldt-scoop-cms', 'digital-storefront', 'mermaids-of-venice', 'kind-robots', 'kindrobots-unraid'] does not match priority.yaml prefix ['mandarin-tutor', 'cthulhuquarium', 'kapowarr', 'kind-economy', 'interface-vision', 'ai-art-academy', 'coloring-book', 'humboldt-scoop-cms'].
  - **READY_WITH_UNMET_DEPS** — `interface-vision` / `t-105`: Ready task has unmet dependencies: t-104.
  - **GATED_DONE_WITHOUT_APPROVAL** — `kind-robots` / `t-071`: Human-gated task is done without approved_by_human: true.
- Warning details remain in `ROADMAP-AUDIT.md`; errors above take precedence for this sensor.

## Semantic intent review

- Latest: `INTENT-AUDIT-2026-08-29.md` (0 day(s) ago; due at 3.0 days).
- Due: **false**

## Agent routing

When action is needed, use `projects/conductor/OVERSIGHT-AGENT.md` before falling through to ordinary Worker/Reviewer selection.
