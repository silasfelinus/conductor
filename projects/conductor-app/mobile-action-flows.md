# Conductor App — Mobile Todo, Approval, Pitch, and Art Request Flows

Task: `conductor-app/t-003`
Date: 2026-07-03
Status: design refinement over the current Flutter scaffold in `apps/conductor/`

## Scope

This document refines the small-screen flows for the Conductor Flutter app after the first dashboard shell landed. It covers:

- create and edit Todo flows
- project-scoped task flows
- needs-human approval handling
- pitch voting
- art request browsing and submission

This is a design pass only. It does not change backend behavior, write roadmap YAML directly, submit store builds, publish anything, touch secrets, or call live production endpoints.

## Existing scaffold observed

The current app already has the right bones for this pass:

- `apps/conductor/lib/app.dart` uses `go_router`, `flutter_riverpod`, bottom navigation, admin-only Approvals, and a five-minute foreground refresh for todos and Agent Ops.
- `apps/conductor/lib/features/todos/todos_screen.dart` supports Open/Done/Archived filters, swipe-to-done, swipe-to-archive, a modal composer, priority, category, and edit-on-tap.
- `apps/conductor/lib/features/agent_ops/approvals_screen.dart` shows gated roadmap tasks, pending pitches, pitch approve/pass buttons, and conductor inbox replies.
- `apps/conductor/lib/features/agent_ops/agent_ops_repository.dart` keeps Agent Ops behind the signed-in admin user's JWT; no admin token is stored in the app.
- `apps/conductor/lib/features/projects/project_detail_screen.dart` supports project metadata editing, waypoints, project-scoped todos, wishlist, and project chat entry.
- `projects/conductor-app/app-architecture-v2.md` establishes the important boundary: core user project data is multi-user, while GitHub-backed Agent Ops is admin-only and single-tenant.

## Mobile principles

1. **One-handed first.** The primary action for each screen should sit in a bottom FAB, bottom sheet, or bottom action bar.
2. **No silent destructive changes.** Archive, pass, and delete actions should either be reversible or require confirmation/snackbar undo.
3. **Roadmap YAML stays read-only in-app.** Approval decisions become conductor inbox messages or AGENT todos; the app must not directly set `approved_by_human` or task status.
4. **Admin-only Agent Ops.** Pitch voting, roadmap approval replies, conductor inbox, and art queue writes stay hidden unless the signed-in user is admin on the selected server.
5. **Local mode degrades gracefully.** Local mode should keep project/todo editing available but hide hosted Agent Ops, pitch voting, and art queue writes.
6. **Every network action needs visible state.** Buttons should show loading/disabled state, then success or failure feedback via snackbar and provider refresh.

## Todo flows

### Global Todo list

Home: bottom nav → `Todos`.

Current behavior is close to MVP-ready:

- Segmented status filter: Open / Done / Archived.
- FAB opens the composer bottom sheet.
- Swipe right toggles Open ↔ Done.
- Swipe left archives.
- Tap opens edit composer.

Refinements:

- Add priority sorting inside each status group: HIGH, NORMAL, LOW, then newest first when timestamps are available.
- Add category chips with friendlier labels: Agent, Honey-do, Kaizen, Wishlist.
- Add an empty-state action for Open: `Create your first honey-do`.
- Add snackbar feedback after create, edit, done, reopen, and archive.
- Consider an undo snackbar for archive once repository support is ergonomic.

### Todo composer

Current bottom sheet fields are enough for MVP:

- title
- description
- priority
- category

Refinements:

- Wrap the sheet in `SafeArea` and make it scrollable for small keyboards.
- Disable Save until title is non-empty.
- For general users, default category to `HONEYDO` and hide `AGENT` if the server does not expose agent workflows.
- For project-scoped creation, prefill `dreamId` and show a small project context label so the user knows where the task will land.
- Keep all create/edit calls routed through `todosControllerProvider`; do not call API routes from widgets directly.

### Project-scoped tasks

Home: Dashboard → Project detail → Tasks.

Current behavior uses a project detail FAB that creates a simple HONEYDO task scoped by `dreamId`.

Refinements:

- Replace the one-field prompt with the shared Todo composer in project mode.
- Defaults in project mode:
  - category: `HONEYDO`
  - priority: `NORMAL`
  - status: `OPEN`
  - dreamId: current project id
- Show non-wishlist project todos as compact checklist tiles.
- Add a long-press or overflow menu for edit/archive so project tasks have parity with the global Todo list.

## Approval flows

Home: bottom nav → `Approvals` (admin only).

### Gated task review

Current behavior shows needs-human/gateHuman tasks and lets the admin send a conductor inbox reply.

Refined flow:

1. User taps an approval card.
2. Detail sheet opens with:
   - project slug and task id
   - title
   - status, stakes, gate flag
   - full `FOR SILAS` note
   - what approving unlocks, when present in the note
3. Bottom actions:
   - `Approve via inbox`
   - `Request changes`
   - `Copy task id`
4. `Approve via inbox` pre-fills:

   ```text
   [project/task-id] Approved — set approved_by_human: true and status: done.
   ```

5. `Request changes` pre-fills:

   ```text
   [project/task-id] Changes requested: <user text>
   ```

6. On send, invalidate Agent Ops data and show a snackbar.

Boundary: the app sends an inbox message only. It must not write roadmap YAML directly.

### Approval card hierarchy

Use visual priority:

1. `stakes: outward-facing` or `irreversible`
2. unapproved `gate_human: true`
3. ordinary `needs-human`
4. soft tool-blocked tasks

Cards should make the blocker obvious before the user opens them.

## Pitch voting flow

Home: bottom nav → `Approvals` → `Pitches awaiting a vote`.

Current behavior has approve/pass icon buttons.

Refinements:

- Use explicit text buttons on small screens: `Approve` and `Pass`, not just icons.
- Tap the card to open a pitch detail sheet before voting.
- The detail sheet should show title, slug, status, and a short summary if the API exposes one.
- Require confirmation for `Pass` because it can be easy to fat-finger.
- After voting, invalidate Agent Ops data and show `Approved <slug>` or `Passed <slug>`.

Boundary: pitch votes are admin-only Agent Ops writes. They stay hidden from non-admin users and local mode.

## Art request flow

The v2 architecture splits project artwork into current/project display and future ArtCollection/request tooling. The remaining app task `t-012` owns the implementation. This task defines the mobile flow so `t-012` has a target.

### Project artwork browsing

Home: Dashboard → Project detail → Artwork.

Recommended MVP placement:

- Add an `Artwork` section below project hero/chat and above wishlist.
- Show current hero/card/icon if present.
- Show an inspiration gallery when ArtCollection data is available for the project slug.
- Empty state: `No inspiration images queued for this project yet.`

### Admin art request submission

Entry points:

- Project detail → Artwork → `Request image`
- Approvals/Agent Ops → `Art requests` when a queue endpoint exists

Bottom sheet fields:

- image type: icon / card / hero / inspiration
- prompt
- dimensions preset
- optional style notes
- project slug, prefilled and locked from project detail

Submit behavior:

- admin-only
- remote server only
- sends through the Agent Ops/art-request repository method once implemented
- success message: `Queued art request for <project>`
- no generation call from the app; it only queues a request for the conductor/art pipeline

Boundary: no live image generation, no binary commit, and no direct edit to `projects/art-prompts.yaml` from UI components.

## Navigation model

Recommended bottom navigation remains:

1. Projects
2. Todos
3. Apps (remote only)
4. Approvals (admin only)
5. Settings

Within Project detail, prefer sections over more bottom-nav items:

- Overview
- Waypoints
- Tasks
- Chat
- Artwork
- Wishlist

On narrow screens, section anchors can become chips under the AppBar.

## Repository/store boundaries

Flutter widgets should call repositories/controllers only:

- Todo screens → `todosControllerProvider`
- Project detail → `projectsRepositoryProvider` and `todosControllerProvider`
- Approvals/pitches/inbox → `agentOpsRepositoryProvider`
- Future art requests → a small `artRequestsRepositoryProvider` or Agent Ops extension

Do not call API routes directly from widgets. Keep token handling inside `ApiClient` and auth storage.

## Implementation follow-ups

These are scoped candidates, not part of this design-only task:

1. Update project detail task creation to reuse the full Todo composer in project mode.
2. Add approval detail sheets with approve/request-changes message templates.
3. Replace pitch icon-only actions with detail sheet plus explicit buttons.
4. Add an art request repository and admin-only request sheet under the project Artwork section.
5. Add loading/error/snackbar states around all Agent Ops writes.

## Acceptance checklist for t-003

- Todo create/edit flow is specified for global and project contexts.
- Approval flow keeps roadmap YAML read-only and routes decisions through conductor inbox.
- Pitch voting flow is admin-only and has mobile-safe confirmation behavior.
- Art request flow is defined as queue-only, not generation or publishing.
- Store/repository boundaries are explicit for the next implementation tasks.
