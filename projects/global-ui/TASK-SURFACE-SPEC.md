# TASK-SURFACE-SPEC.md — global-ui

Product and interface specification for the user-facing task taxonomy and presentation rules in the Kind Robots workspace.

Version: 1.0
Date: 2026-06-30
Status: Approved (gate removed 2026-06-30; Silas pre-approves this direction)
Vocabulary: all terms defined precisely in GLOSSARY.md

---

## 1. Surface map

| Surface | Scope | Where shown in UI | Source of truth |
|---|---|---|---|
| Project task | Per-project, milestone-scoped | Project detail → roadmap section | conductor roadmap.yaml |
| Todo | Global | Not a primary user-facing surface — Worker-only flow | kind_robots DB (Todo) |
| Honeydo | Global | "For You" inbox / honeydo queue (top-level nav) | kind_robots DB (Todo, category: HONEYDO) |
| Kaizen | Per-project | Project detail → kaizen section (below roadmap) | kind_robots DB (scoped to dreamId) until promoted; then roadmap.yaml |
| Desired feature | Per-project | Project detail → wishlist section (orderable list) | kind_robots DB (scoped to dreamId, with order index) |
| Approval gate | Per-project | Roadmap task card badge ("awaiting approval") | conductor roadmap.yaml (gate_human, approvedByHuman) |
| Completed task | Per-project | Roadmap section, collapsed under disclosure | conductor roadmap.yaml (status: done) |

---

## 2. Project task cards (roadmap view)

Each task card in the roadmap section displays:

- **Status badge** — color-coded: `ready` (blue), `claimed/in-progress` (yellow), `done` (green), `needs-human` (accent), `blocked` (red), `waiting` (gray)
- **Title** — full task title, one line
- **Stakes badge** — shown only for non-reversible stakes: `irreversible` (error/red), `outward-facing` (warning/yellow), `needs-human` (accent)
- **Depends-on** — comma-separated task ids when present (`depends: t-001, t-002`)
- **Gate state** — `awaiting approval` (accent) or `✓ approved` (success) when `gate_human: true`
- **Note preview** — truncated to 3 lines; expandable on click
- **Relative timestamp** — `just now`, `Nd ago`, `Nmo ago` from the `updated` field; shown at the far right in muted text

User actions on task cards:
- Expand note (tap/click card body)
- No direct edit from UI in v1 — task management stays in conductor files and PRs

Grouping: tasks grouped by milestone. Within each milestone: `ready` and `in-progress` first, then `waiting`, then `done` (collapsed).

---

## 3. Honeydo inbox ("For You" queue)

The honeydo inbox is a global, non-project-specific surface. It is the user's action queue — things the AI has determined Silas needs to do to unblock projects.

Each honeydo card shows:
- **Title** — the human-readable request
- **Priority badge** — HIGH (red), NORMAL (default), LOW (muted)
- **Related project** — if `dreamId` is set on the Todo record (optional; may be null for cross-project honeydos)
- **Created timestamp** (relative)

User actions:
- Mark complete (archives the Todo)
- Defer / snooze (to be designed in t-003)
- View related project (navigates to project detail)

Empty state: "Nothing needs your attention right now."

---

## 4. Kaizen section (project detail)

The kaizen section appears below the roadmap in each project detail view. It shows:

- The most recent unresolved kaizen suggestion for the project (if any)
- A brief contextual prompt: "Here's something to move this project forward:"
- Action buttons: "Promote to task" | "Dismiss"
- Optional secondary prompt: "How can I make this look better?" — a free-text input that feeds into kaizen or desired-feature creation for this specific project

**Promote to task flow** (triggers t-002):
1. User clicks "Promote to task"
2. UI presents a pre-filled task draft (title from kaizen text, stakes: reversible)
3. User edits/confirms
4. Task creation routes through Pinia store → Todo API → Worker picks it up next cycle → Worker creates a proper roadmap task during execution

**Only one active kaizen per project** is displayed at a time. If the Worker has suggested multiple, show the most recent; older ones stay in the DB but are not surfaced until the current one is resolved.

---

## 5. Desired-feature wishlist (project detail)

An orderable list of product ideas for the project that haven't been scoped into tasks yet. Shown in the project detail view.

Display:
- Drag-to-reorder list (or up/down buttons as fallback)
- Items show title + status icon: `active` (default), `promoted` (grayed, strikethrough), `retired` (hidden unless "show retired" toggle)
- "Add feature idea" input at the bottom of the list (free-text)

User actions:
- Add new item (free text, optional description)
- Reorder (drag or buttons) — persisted with debounce
- Edit wording (inline edit)
- Promote to task → enters the same task-creation flow as kaizens
- Retire (soft-delete; hides from default view)
- Unretire (restore)

AI actions:
- Suggest new desired-feature items (appear at top with "suggested" badge; user accepts or dismisses)
- Annotate an existing item with a rationale or implementation note

**Graduation does not touch the conductor roadmap directly.** The item is marked `promoted: true` in the DB; the task appears in the roadmap after Worker execution.

---

## 6. Source-of-truth rules

| Entity | Authoritative source | Kind Robots DB role | UI write? |
|---|---|---|---|
| Project task | conductor roadmap.yaml | Mirror / display (projects.get.ts reads YAML) | No — read-only from UI |
| Todo | kind_robots DB | Authoritative | Yes (Silas creates via Todo flow) |
| Honeydo | kind_robots DB | Authoritative | Yes (AI creates; Silas marks complete) |
| Kaizen (suggestion) | kind_robots DB until promoted | Temporary | Yes (Silas promotes or dismisses) |
| Kaizen (promoted task) | conductor roadmap.yaml | Mirror after Worker run | No |
| Desired feature | kind_robots DB (dreamId-scoped) | Authoritative | Yes |
| Approval gate | conductor roadmap.yaml | Display only | No — Silas edits YAML directly in v1 |

**Key constraint:** The UI never writes to conductor roadmap.yaml. The conductor filesystem is the authority for project tasks. All UI actions that should result in a new task route through the Todo/Pinia flow — the Worker then creates or updates the roadmap task during its next cycle.

---

## 7. Completed and terminal state display

| Status | Display treatment |
|---|---|
| `done` | Green badge; shown in collapsed "Completed (N)" disclosure per milestone |
| `needs-human` | Accent badge "Awaiting Silas"; task note is prominently expandable |
| `blocked` | Red badge "Blocked (pass N)"; muted, shown but not interactive |
| `waiting` | Gray badge "Waiting"; dependency chain shown in muted text |
| `challenged` | Orange badge "Challenged"; shown in roadmap with link to TALKBACK note |

Completed tasks default to collapsed. The disclosure header shows the count: "Completed (3)." The user can expand to see the history.

---

## 8. Deferred to downstream tasks

The following are explicitly out of scope for this spec and will be designed in t-002 through t-009:
- Specific component names, Pinia store method signatures, or API route shapes
- Mobile/responsive layout details
- Real-time / socket architecture for live updates
- The recurring site-audit agent cadence and trigger mechanism
- The admin-only Todo creation UI (Silas already creates these directly)
- Detailed empty-state copy beyond what is noted above
