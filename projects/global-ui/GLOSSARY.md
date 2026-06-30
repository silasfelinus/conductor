# GLOSSARY.md — global-ui task surface vocabulary

Canonical definitions for the task-surface terms used across conductor, kind_robots, and the front-end workspace. The spec in TASK-SURFACE-SPEC.md uses these without re-definition — edit here if a term changes.

---

## task

A concrete unit of work scoped to a single conductor project, with a defined deliverable, milestone, and status lifecycle.

**Created by:** Human (initial roadmap setup) or AI agent (kaizen promotion, scope-new tasks discovered during work)
**Lives in:** `conductor/projects/<slug>/roadmap.yaml` — conductor filesystem is authoritative; kind_robots only mirrors/displays
**Acted on by:** Worker (claim and execute); Reviewer (mark done, reject, escalate)
**Status lifecycle:** `waiting → ready → claimed → review → done` with side exits `needs-human`, `blocked`, `challenged`
**Differs from todo:** A task is milestone-scoped with a full lifecycle; a todo is a one-off instruction with no milestone or project roadmap trace.
**Differs from honeydo:** A task is assigned *to* an AI agent; a honeydo is assigned *to* the human.

---

## todo

A lightweight, one-off work item created by Silas in the kind_robots workspace to direct AI agents to specific work outside the normal roadmap cycle.

**Created by:** Human (Silas only)
**Lives in:** kind_robots DB (Todo model). Fetched each Worker cycle via `scripts/fetch_todos.py`.
**Priority order:** HIGH → NORMAL → LOW; newest-first within same priority. Takes precedence over all roadmap tasks.
**Acted on by:** Worker (executes the work, calls `complete_todo.py <id>` when done); Reviewer does not claim or complete todos.
**Differs from task:** A todo is not tied to a project milestone; it archives on completion and leaves no roadmap trace. Scope is exactly the todo title/description — no follow-on tasks unless the todo explicitly asks.
**Differs from honeydo:** A todo delegates work *to* an AI agent; a honeydo delegates work *to* the human.

---

## honeydo

A task the AI/LLM assigns *to the human (Silas)* to help projects along — the inverse of a todo. Not project-specific for viewing; appears in a global user-facing queue or inbox.

**Created by:** AI/LLM agent
**Lives in:** kind_robots DB (Todo model, `category: HONEYDO`)
**Acted on by:** Human (Silas); AI agents create honeydos but do not mark them complete — Silas does.
**Display:** Global user-facing inbox, not scoped to a specific project view.
**Differs from todo:** A honeydo is directed *at* the human; a todo is directed *at* the AI.
**Differs from approval:** An approval is a structural gate on a specific conductor task; a honeydo is a general-purpose human request with no dependency chain in the roadmap.

---

## kaizen

A Worker-suggested improvement surfaced at the end of each PR handoff. After every successful merge, the Reviewer promotes one kaizen suggestion into a new `ready` task in the project roadmap (always `stakes: reversible`).

**Created by:** Worker (suggests in the PR handoff "Kaizen suggestion" section); Reviewer (promotes to a real task on merge, or substitutes a stronger one)
**Lives in:** PR handoff text until the Reviewer promotes it; then in conductor roadmap.yaml as a new `ready` task
**Rate:** One kaizen per merge. Not optional — if the Worker's suggestion is weak, the Reviewer substitutes their own.
**Acted on by:** Reviewer (promotes or defers with reason); Worker (executes on next cycle)
**Differs from task:** A kaizen suggestion is ephemeral until the Reviewer promotes it; once promoted it IS a task with the full lifecycle.
**Differs from desired-feature:** A kaizen targets a specific process/code improvement in an in-flight project; a desired-feature is a product wish that may not have a project home or a clear implementation path yet.

---

## desired-feature

An item on a project's feature wishlist — a product idea that hasn't been scoped into a concrete task yet. Orderable by importance; may be promoted, retired, or converted to a scoped task without touching the conductor roadmap directly.

**Created by:** Human or AI
**Lives in:** kind_robots DB (scoped to a Dream/project via dreamId, has an order index) — NOT in conductor roadmap until promoted
**Acted on by:** Human (add, reorder, retire, promote to task); AI (suggest, annotate, flag for promotion)
**Graduation path:** "Promote to task" action → task-creation flow → lands as a Todo → Worker picks it up → proper roadmap task created during execution. The desired-feature item is marked `promoted: true` in-place (still visible, grayed out).
**Differs from task:** A desired-feature has no milestone, owner, status lifecycle, or stakes; it is a wishlist item, not committed work.
**Differs from kaizen:** A kaizen is an agent-facing process improvement tied to an in-flight project; a desired-feature is a user-facing product wish that may span multiple projects or exist before any project scope is defined.

---

## approval

A structural gate on a conductor task: `gate_human: true` on the task record, resolved only when Silas sets `approved_by_human: true`. Blocks all downstream `waiting` tasks until cleared.

**This is a property of a task, not a standalone entity.**
**Created by:** N/A — the gate is defined in the roadmap by the human or agent who wrote the task
**Lives in:** conductor roadmap.yaml (`gate_human: true` + `approved_by_human: true/false`)
**Acted on by:** Silas ONLY — sets `approved_by_human: true` and `status: done`. Neither Worker nor Reviewer can set this field.
**Resolution:** After Silas approves, Worker runs `scripts/resolve_deps.py` which flips dependent `waiting` tasks to `ready`.
**Differs from todo:** A todo is a new work instruction; an approval is the resolution of already-completed gated work.
**Display cue:** Task card shows "awaiting approval" badge (accent color) when `gate_human: true && !approvedByHuman`, "approved" (success color) when cleared.

---

## completion

The terminal state of a task (`status: done`). A task is complete when its deliverable is merged (software), accepted by Silas (content/proposal), or manually approved after a human gate.

**Set by:** Reviewer on software merge; Silas after approving a human-gated task; convention for pre-completed tasks in the roadmap
**Lives in:** conductor roadmap.yaml (`status: done`, bumped `updated` timestamp)
**Exception — recurring tasks:** Tasks with `recurring: true` never reach `done`; they reset to `ready` after each cycle to re-arm for the next run. The pitches/output they produce ARE the deliverable; the task itself keeps cycling.
**Differs from paused/archived:** Completion is final for a task. A paused or archived state applies to a *project* (in project-overrides.yaml), not to individual tasks.
**Display:** Completed tasks are shown collapsed under a "Completed (N)" disclosure in the project roadmap view — visible but out of the way.
