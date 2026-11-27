# Completion lifecycle

Owner direction, 2026-11-26 PT. This applies to all current and future roadmaps.

## One canonical state

- A task is done only after its original acceptance is verified. Partial scope returns to ready; pending work stays open; recurring work re-arms. No human approval is inferred. A completed task is not a source of routine follow-up.
- Keep the canonical YAML task ID, milestone, title, terminal status, dependencies, approval/receipt fields and compact note. These are the completion index, not an instruction to read its old work. Do not remove IDs or reuse them. The original detailed note is recoverable in the project's HISTORY.md; original directives and complete prior YAML are also recoverable in Git history. Preserve existing archival material and links verbatim.
- A milestone becomes done when it has at least one finite task and every finite task is genuinely done, including required human approvals. Recurring upkeep is separate. Never mark an empty, blocked, pending or merely cancelled scope complete by inference. Complete milestones and tasks appear collapsed in the project board; open only on explicit historical lookup.
- The serialized task-event writer reconciles completed milestones and archives lengthy done notes using the existing archive helper. Apply the same process to the current workable roadmaps; paused, retired and finished projects are not reopened. Keep live state/claims/IDs unchanged apart from verified milestone closure and lossless archival. No second authority.
- Agent context uses only nonterminal task locators, current direction and relevant live specs. Do not load completed task history or closed milestone detail unless needed for an explicit lookup, dependency evidence or a concrete defect.

## Feedback is not an endless task generator

TALKBACK is an append-only historical ledger plus current unresolved critique. Do not use completed-task entries as current instructions; consult only relevant unresolved feedback for the selected open task, preferably its retry_context. Routine successful review is recorded by the PR, compact completion receipt and required learning outcome. New TALKBACK is for actionable unresolved feedback, challenges, escalation or material patterns, not obligatory praise/critique on every merge. Once resolved, prior feedback is history; durable general lessons live in LEARNING.yaml. Do not delete old ledger entries or alter their wording. The existing history remains directly searchable. An evidenced regression or explicit new direction is separate scoped work, not automatic reopening or kaizen.

## Acceptance and safety

The canonical roadmap remains compatible with dependency and projection readers. A historical note is replaced only after exact round-trip verification and preservation of prior history. Existing real gates, approvals, task state and dependencies remain intact. A failure to archive safely must leave the original untouched and be reported. CI and live projection are verified separately; no publication or deployment authority is added.
