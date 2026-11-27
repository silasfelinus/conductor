# Project roadmap polishing

This is an on-demand editor guide, not required reading for every worker. The shared architecture is [Lightweight Conductor](../docs/agents/LIGHTWEIGHT-CONDUCTOR.md); [AGENTS.md](../AGENTS.md) governs safety and delivery.

## Keep a small, finite map

- The project roadmap is canonical for goal, milestones, task IDs, state, dependencies, claims and gates. Keep the goal one sentence; milestones represent outcomes, not work logs. Prefer a handful of meaningful deliverables.
- Give each task a concrete output and acceptance evidence. Use existing fields and references; do not introduce a new schema or rewrite task IDs. Place detailed specifications in the project's existing design/reference files (or a linked task-specific document if necessary), not another mandatory manual.
- Keep a current note with the latest verified receipt, missing scope and relevant links. Archive long historical notes using the existing verified archival scripts; preserve original content and links. Do not rewrite or drop append-only history.
- Role suggestions use existing lane/title/kind conventions; use a supported `lane: art|qa|build|human` only when helpful. A role hint is advisory, not an approval or eligibility change.
- Separate finite acceptance from ongoing maintenance and optional ideas. A completed game moves to playtest/normal after verified readiness, not after a subjective verdict; feedback/publishing are separate. Do not add tasks just because one closes.

## One project per cleanup

1. Read that project's current direction, master issue sections, live roadmap, recent relevant PRs and evidence. Use [scoped locators](../docs/agents/agent-context.md). Respect existing claims; don't rewrite actively owned tasks.
2. Reconcile merged verified complete scopes, partial reviews, blocked dependencies and genuine human gates using normal state transitions. Never infer completion from a merged PR alone. Don't reopen completed work without an evidenced defect or new owner direction.
3. Compare remaining tasks to the intended playable product. Retain unmet requirements; fold duplicate scope into one finite task only with explicit references and dependency-safe migration. Preserve old IDs and receipts; do not cancel tasks without owner authorization. Avoid giant umbrella tasks or endless polish.
4. Link detailed specs and evidence; keep the live task index concise. Prefer the existing [archive helpers](../docs/agents/reference-manual-2026-11-26.md) and targeted edits over mass reformatting.
5. Open a scoped PR. Run roadmap YAML/structural and relevant project checks, inspect exact diff, merge only current-head green ungated changes. Verify canonical state and refreshed locators. Report old/new task counts, actual closure evidence, remaining scopes and genuine gates.

## Stop condition

A cleaned roadmap is a truthful small map of what remains, not a smaller count achieved by hiding work. It retains every original requirement, stable identity, ownership, gates, dependency and historical receipt. Individual project redesign starts separately, after shared infrastructure changes; no portfolio-wide rewrite.

For new projects start with [_template/roadmap.yaml](_template/roadmap.yaml). For current status use [STATUS.md](../STATUS.md); for priority and lifecycle use [priority.yaml](priority.yaml) and [project-overrides.yaml](../project-overrides.yaml).
