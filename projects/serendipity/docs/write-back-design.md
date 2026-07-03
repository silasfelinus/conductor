# Serendipity Write-Back Design (t-006)

status: awaiting-silas
demo: https://github.com/silasfelinus/kind_robots/pull/77 (Story ledger, dry-run)

## What this decides

When the protagonist answers a woven question, what happens to the real task
underneath it? This document proposes the wiring. Nothing described here is
live: the kind_robots build only *demonstrates* the flow (the Story ledger
shows each captured answer and the exact write it would trigger). Implementing
the writes below is unblocked only by Silas approving this task.

## Proposed wiring

### Honey-do answers → mark the todo done

- Surface: `PATCH /api/todos/:id` via the existing `todoStore.updateTodo`.
- Write: `status: DONE`, with the protagonist's answer appended to the todo's
  `description` as a note (`"Story answer (serendipity): …"`).
- Trigger: an explicit per-item **Apply** button on the Story ledger — never
  automatic on answering. The story captures; the human applies.
- Reversal: todos can be flipped back to OPEN in one tap from the Todos page,
  so this write is low-stakes and reversible.

### Needs-human conductor task answers → record the decision, never edit the roadmap

- The app must NOT write conductor roadmap YAML. The roadmap stays edited only
  by Silas and the conductor agents (single source of truth, per CONTROL.md).
- Write: create a new Todo, `category: AGENT`, titled
  `"Story decision on <project>/<task-id>: <one-line answer>"`, with the full
  answer in the description and the task id preserved. This lands the decision
  in the normal review surfaces (kind_robots Todos, conductor fetch_todos)
  where Silas or the Worker acts on it through the existing gated flow.
- The conductor task itself remains `needs-human` until Silas edits the
  roadmap — the story never approves anything on his behalf.

### Preference answers → stay app-owned

No write. They persist in the session and feed t-010's finale recap; a later
task may promote selected preferences to KAIZEN/DESIRED_FEATURE todos, but
that is out of t-006's scope.

## Guardrails carried over from the brief

- Per-item explicit human action (Apply) for every write; no batch auto-apply.
- `writeBackStatus` walks `pending-human-gate → queued → written`, and the
  ledger shows the live status of each item.
- The UI never marks anything approved/done at answer time; the reassurance
  card stays.
- All writes go through existing authenticated stores/endpoints — no new API
  surface, no elevated permissions.

## TO APPROVE (Silas)

Read this doc, click through the ledger demo on kind_robots PR #77's preview,
then set `approved_by_human: true` and `status: done` on serendipity/t-006.
That unblocks t-007 (polish + first full playthrough) and green-lights
implementing the Apply buttons exactly as specified above. If the wiring
should differ (e.g. decisions as INBOX entries instead of AGENT todos), leave
a note on the task and it returns to `ready` with the revised design.
