# Conductor Portfolio Oversight

Generated: `2026-09-18T11:26:16.505147+00:00`

Overall status: **action-needed**

This is a deterministic sensor. For semantic roadmap/progress intent review, follow `projects/conductor/OVERSIGHT-AGENT.md`.

## OpenAI scheduled-agent heartbeat

- Latest visible OpenAI scheduled-Agent activity: `2026-09-18T10:20:41+00:00` (1.09h ago; overdue at 6.0h).
- Overdue: **false**
- Note: OpenAI coordination activity is a heartbeat only; a clean no-op OpenAI cycle may leave no commit.

## Kind Robots ↔ Conductor project parity

- Forward drift (KR row claims missing roadmap): **0**
- Reverse orphans (active Conductor roadmap missing KR row): **0**

## Roadmap/CONTROL structural audit

- Errors: **1**
- Warnings: **8**
  - **CONTROL_PRIORITY_DRIFT** — `_global`: CONTROL.md priority band ['cthulhuquarium', 'kind-economy', 'interface-vision', 'coloring-book', 'humboldt-scoop-cms', 'digital-storefront', 'kind-robots', 'rainbow-butterflies'] does not match priority.yaml prefix ['cthulhuquarium', 'kind-economy', 'butterfly-gallery', 'art-archive', 'interface-vision', 'coloring-book', 'humboldt-scoop-cms', 'digital-storefront'].
- Warning details remain in `ROADMAP-AUDIT.md`; errors above take precedence for this sensor.

## Semantic intent review

- Latest: `INTENT-AUDIT-2026-09-17.md` (1 day(s) ago; due at 3.0 days).
- Due: **false**

## Agent routing

When action is needed, use `projects/conductor/OVERSIGHT-AGENT.md` before falling through to ordinary Worker/Reviewer selection.
