# Conductor Portfolio Oversight

Generated: `2026-08-29T12:44:42.744852+00:00`

Overall status: **action-needed**

This is a deterministic sensor. For semantic roadmap/progress intent review, follow `projects/conductor/OVERSIGHT-AGENT.md`.

## OpenAI scheduled-agent heartbeat

- No commit containing `openai-scheduled-` was found in available history. Claude scheduled activity does not count.
- Overdue: **true**
- Note: No OpenAI scheduled-Agent heartbeat commit was found in available git history. Claude activity does not satisfy this check.

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

- No completed `INTENT-AUDIT-YYYY-MM-DD.md` report exists yet.
- Due: **true**

## Agent routing

When action is needed, use `projects/conductor/OVERSIGHT-AGENT.md` before falling through to ordinary Worker/Reviewer selection.
