# Conductor App — Architecture and API Contract

Generated: 2026-06-30
Task: conductor-app/t-001
Informed by: docs/kr-api-surface.md

---

## Purpose

Define the Conductor App architecture, screen list, data flow, and API contract so Silas can approve the app shape before implementation begins. All screens are read-only or write-through-existing-API; no new backend infrastructure is built until approved.

---

## Platform Target

**Flutter** (cross-platform, single codebase)

| Target | Priority |
|---|---|
| Android | Primary |
| iOS | Primary |
| Web (Flutter web) | Stretch; not MVP |
| Desktop (macOS/Windows) | Deferred |

---

## Screen List

### 1. Dashboard (Home)
- Active project cards (scroll list)
- "Needs your attention" count badge (pending approvals + needs-human tasks)
- Quick-add todo button
- Last updated timestamp per project

### 2. Project Detail
- Project title, description, milestones progress bar
- Task list: status indicators (done/ready/waiting/blocked/needs-human)
- Task tap → expanded note, depends_on, stakes, gate_human flag
- "Write message to conductor" shortcut (opens Compose screen)

### 3. Todos
- Open todo list (sorted priority + date)
- Swipe-to-complete (PATCH /api/todos/[id] with status=DONE)
- FAB → new todo
- Filter chips: OPEN / DONE / ARCHIVED

### 4. Create/Edit Todo
- Title (required)
- Description (optional)
- Priority picker: LOW / NORMAL / HIGH
- Category: AGENT / KAIZEN / HONEYDO
- Due date (optional)

### 5. Approvals Queue
- List of gate_human tasks not yet approved (from GET /api/conductor/projects, filtered)
- Each item: project slug, task id, title, note
- "Compose message to conductor inbox" action (routes to Compose screen)
- No in-app approve button (YAML-write goes through conductor inbox or PR)

### 6. Art Requests
- List queued art requests (from art-prompts.yaml via conductor endpoint — see Gap below)
- Form to queue a new request: POST /api/conductor/art-request

### 7. Pitch Voting
- List pitches with status: awaiting-silas / approved / passed
- Vote button → POST /api/conductor/pitch-vote { slug, vote: "approved" | "passed" }
- Submit new pitch → POST /api/conductor/pitch

### 8. Compose (Message to Conductor)
- Free-text message → POST /api/conductor/message
- Used for approval actions, requests, and notes to the Worker

### 9. Profile
- GET /api/users/me display: username, karma, mana
- Logout (clear stored JWT)

### 10. Login
- Email + password form → POST /api/auth/login → JWT stored in Flutter secure storage
- "Sign in with Google" → WebView OAuth flow (GET /api/auth/google)

---

## Data Flow

```
App startup
  └─ Restore JWT from secure storage
  └─ GET /api/users/me (verify JWT valid)
  └─ GET /api/conductor/projects (fetch all data)
  └─ GET /api/todos (fetch user todos)
  └─ Render dashboard from cached data

Background refresh (every 5 min, app in foreground)
  └─ Same requests; diff against cached state
  └─ Push local notification if new gate_human task found

User actions
  ├─ Create todo     → POST /api/todos          (JWT)
  ├─ Update todo     → PATCH /api/todos/[id]    (JWT)
  ├─ Delete todo     → DELETE /api/todos/[id]   (JWT)
  ├─ Vote on pitch   → POST /api/conductor/pitch-vote  (Admin token)
  ├─ Submit pitch    → POST /api/conductor/pitch       (Admin token)
  ├─ Inbox message   → POST /api/conductor/message     (no auth, server GitHub token)
  └─ Art request     → POST /api/conductor/art-request (Admin token)
```

---

## Auth Architecture

```
Flutter Secure Storage
  ├─ USER_JWT         → for todo and user profile endpoints
  └─ KR_API_TOKEN     → for admin endpoints (pitch voting, art requests)
```

**Token refresh:** kind_robots does not issue refresh tokens at MVP. On 401 response, redirect to Login screen and prompt re-auth. The admin token (`KR_API_TOKEN`) is a static long-lived API key — store as a build-time environment variable via `--dart-define` at app build time (not in source).

**Security note:** The admin API token in the app's binary is acceptable for a Silas-only personal app. Do not ship this pattern in a multi-user public app without proper API key scoping and rotation.

---

## Known API Gaps (from kr-api-surface.md)

| Gap | Impact | MVP approach |
|---|---|---|
| No `projectSlug` on Todo | Can't filter todos by project in-app | Client-side filter by title prefix convention (`[conductor]`, `[sketchy]`, etc.) |
| No pending art requests endpoint | Can't list queued requests from DB | Show "submit request" only; no queue list at MVP |
| No push notification infra | No native notifications | Poll on 5-minute timer while app is in foreground; local notification on new gate task |
| Task status is YAML/GitHub-only | Can't approve tasks in-app | "Write to conductor inbox" workaround; YAML approval via PR only |

---

## State Management

Use the Flutter BLoC pattern (or Riverpod — decision deferred, both are viable):
- `ProjectsBloc`: loads and caches /api/conductor/projects
- `TodosBloc`: loads, creates, updates, deletes todos
- `AuthBloc`: handles login/logout and token storage

---

## Notification Strategy (MVP)

No native push infrastructure at MVP. Strategy:
1. **Foreground polling**: Every 5 minutes, re-fetch /api/conductor/projects
2. **Change detection**: Compare new response against cached; if `needs-human` count increases, show a local notification via `flutter_local_notifications`
3. **Badge count**: Update home screen badge with count of pending approvals

Future pitch: `POST /api/users/[id]/push-token` to register FCM token; backend sends push on task state change. Defer until the app ships and usage is validated.

---

## Dependencies

| Package | Purpose |
|---|---|
| `http` | HTTP client |
| `flutter_secure_storage` | JWT + API key storage |
| `flutter_local_notifications` | Foreground change alerts |
| `cached_network_image` | Project card images |
| `intl` | Date formatting |
| `bloc` or `riverpod` | State management |

---

## Critical Constraint

**Task state is read-only in the app.** Roadmap YAML files are the authority. The app can read task state from GET /api/conductor/projects but cannot write it. To trigger a task update, the app must either:
- Create a Todo for the Worker (POST /api/todos)
- Send a message to the conductor inbox (POST /api/conductor/message)

This constraint is intentional. Do not implement any direct task status update flow in the app.

---

## What Gets Built Next (After Approval)

- conductor-app/t-002: Dashboard shell (Flutter scaffold + ProjectsBloc)
- conductor-app/t-003: Mobile todo and approval flows (design pass)
- conductor-app/t-004: Notification strategy (spec + polling implementation)
