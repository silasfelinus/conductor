# Kind Robots API Surface — Conductor App Map

Generated: 2026-06-30
Updated: 2026-07-12 — Dreams no longer carry project state; the Dream model
split into Dream / Project / Facet. Project identity now lives at
`/api/projects` (section 4).
Task: conductor-app/t-005

---

## Purpose

Map the kind_robots REST API surface that the Conductor App (Flutter) would need for its core features: projects, todos, dreams, art requests, pitch voting, user auth, and notifications. Note what exists, what the auth requirement is, and what needs to be built.

---

## Auth Summary

The app needs to support at least:
- JWT login flow (email/password or Google OAuth)
- Store JWT in secure storage; refresh on expiry
- Admin operations (pitch voting, art requests, conductor writes) via KR_API_TOKEN or admin JWT

---

## Feature Areas

### 1. Authentication

| Method | Path | Auth | Status | Notes |
|---|---|---|---|---|
| POST | `/api/auth/login` | None | ✓ Exists | Body: `{ username, password }` → returns JWT |
| GET | `/api/auth/google` | None | ✓ Exists | Google OAuth flow (web-based; needs WebView in Flutter for OAuth) |
| GET | `/api/users/me` | JWT | ✓ Exists | Returns current user profile |
| POST | `/api/users/register` | None | ✓ Exists | Create new user account |

---

### 2. Projects (Conductor)

These endpoints read the conductor GitHub repo — no DB writes.

| Method | Path | Auth | Status | Notes |
|---|---|---|---|---|
| GET | `/api/conductor/projects` | None | ✓ Exists | Returns all projects with milestones, tasks, progress %, image paths |
| GET | `/api/conductor/overrides` | None | ✓ Exists | Returns project status/priority overrides (active/paused/etc.) |
| GET | `/api/conductor/prs` | None | ✓ Exists | Returns open PR list from GitHub |
| POST | `/api/conductor/pitch` | Admin token | ✓ Exists | Submit a new pitch to conductor |
| POST | `/api/conductor/pitch-vote` | Admin token | ✓ Exists | Vote approved/passed on a pitch |
| POST | `/api/conductor/message` | None (server GitHub token) | ✓ Exists | Write a message to conductor INBOX.md |
| POST | `/api/conductor/art-request` | Admin token | ✓ Exists | Queue a missing-image request in art-prompts.yaml |

**Gap:** There is no endpoint to update a task's status or modify a roadmap. Task state lives in GitHub YAML files, not the DB. The app can READ task state but cannot WRITE it directly. This is intentional (conductor.yaml is the authority). To trigger a task update, the app must either: (a) create a Todo for the Worker, or (b) send a message to the conductor inbox. Document this constraint in the architecture spec.

---

### 3. Todos

| Method | Path | Auth | Status | Notes |
|---|---|---|---|---|
| GET | `/api/todos` | JWT (user-scoped) | ✓ Exists | Query: `?status=OPEN|DONE|ARCHIVED` or `?includeArchived=1`. Returns sorted by priority+date |
| POST | `/api/todos` | JWT | ✓ Exists | Body: `{ title, description?, priority?: LOW|NORMAL|HIGH, category?: AGENT|KAIZEN|HONEYDO, dueDate?, icon?, imagePath? }` |
| PATCH | `/api/todos/[id]` | JWT | ✓ Exists | Partial update (title, status, priority, description, etc.) |
| DELETE | `/api/todos/[id]` | JWT | ✓ Exists | Delete a todo |

**Gap:** Todos are user-scoped, not project-scoped. There's no `projectSlug` field on Todo. An app wanting "todos for project X" must fetch all todos and filter client-side by title convention, or add `projectSlug` to the Todo model (would require a backend pitch).

---

### 4. Projects (Project Identity Layer)

The Dream model split into Dream / Project / Facet (July 2026). Project
identity, status, priority, goal, and waypoints live on the first-class
Project model; `conductorSlug` is the join key with conductor.

| Method | Path | Auth | Status | Notes |
|---|---|---|---|---|
| GET | `/api/projects` | Optional (public projects visible) | ✓ Exists | Query: `?status=ACTIVE`, `?priority=HIGH`, `?channelKey=`, `?search=`, `?mine=`, `?take=`, `?skip=` |
| GET | `/api/projects/[id]` | Optional | ✓ Exists | By numeric id, `slug`, or `conductorSlug` |
| POST | `/api/projects` | JWT | ✓ Exists | Create a Project (title, slug, conductorSlug, status, priority, goal, waypoints, lastSyncedAt, …) |
| PATCH | `/api/projects/[id]` | JWT | ✓ Exists | Partial update — same fields as create, incl. priority and lastSyncedAt |
| DELETE | `/api/projects/[id]` | JWT | ✓ Exists | Soft-archive (isActive false, status ARCHIVED) |

Dreams remain the creative-concept layer (`/api/dreams`, dreamType =
ART/BRAINSTORM/…/PITCH/WISH) and no longer accept `dreamType=PROJECT`,
`projectStatus`, or a priority endpoint. Facets (`/api/facets`) hold reusable
creative flavor (GENRE, COLOR, THEME, ANIMAL, …) with alias resolution.

---

### 5. Art Requests

| Method | Path | Auth | Status | Notes |
|---|---|---|---|---|
| POST | `/api/conductor/art-request` | Admin token | ✓ Exists | Queues a missing image into conductor art-prompts.yaml. Body: `{ src/imagePath/sourceUrl, pageUrl?, alt?, label?, variant?, prompt? }` |
| GET | `/api/art/image/[id]` | Optional | ✓ Exists | Get a single ArtImage record |
| GET | `/api/art/image` | Optional | ✓ Exists | List ArtImages (filterable) |
| POST | `/api/comfy/flux/generate` | Admin token | ✓ Exists | Trigger ComfyUI Flux generation |
| POST | `/api/art/generate` | Auth required | ✓ Exists | Generic art generation trigger |

**Gap:** There's no "list pending art requests" endpoint — those live in conductor/projects/art-prompts.yaml as YAML, not in the DB. The app would need to read from `GET /api/conductor/projects` (which doesn't include art-prompts.yaml) or make a separate conductor GitHub read.

---

### 6. Pitch Voting (Workspace)

| Method | Path | Auth | Status | Notes |
|---|---|---|---|---|
| GET | `/api/conductor/projects` | None | ✓ Exists | Pitches are embedded in the ConductorData response (pitches array, each with status: awaiting-silas|approved|passed) |
| POST | `/api/conductor/pitch-vote` | Admin token | ✓ Exists | Body: `{ slug, vote: "approved" | "passed" }`. Updates pitch status file in GitHub. |
| POST | `/api/conductor/pitch` | Admin token | ✓ Exists | Submit a new pitch file to GitHub |

---

### 7. User Profile

| Method | Path | Auth | Status | Notes |
|---|---|---|---|---|
| GET | `/api/users/me` | JWT | ✓ Exists | Current user (id, username, email, Role, karma, mana, referralCode, etc.) |
| GET | `/api/users/[id]` | JWT or admin | ✓ Exists | User by ID |
| GET | `/api/users/public/[id]` | None | ✓ Exists | Public-safe user profile |
| PATCH | `/api/users/[id]` | JWT (own user) | ✓ Exists | Update user profile |

---

### 8. Notifications

**Gap: No push notification system exists.** kind_robots has no endpoint for registering a push token (APNs, FCM) or sending push notifications. Options for the app:

- **Option A — Polling:** App polls `GET /api/todos` and `GET /api/conductor/projects` on an interval. Simple but drains battery.
- **Option B — Web push via service worker:** Works for web target; not native push for Flutter mobile.
- **Option C — Build push notification infrastructure:** Register FCM/APNs token via `POST /api/users/[id]/push-token`, send notifications from kind_robots server when todo status changes or task gates open. Needs to be a pitch (backend change).

Recommendation: Polling for MVP; pitch push notification infrastructure as a future milestone once the app ships.

---

## Summary Table

| Feature | Endpoint(s) | Exists? | Auth needed |
|---|---|---|---|
| Login / register | /api/auth/* | ✓ | None |
| Current user | /api/users/me | ✓ | JWT |
| All projects + tasks | /api/conductor/projects | ✓ | None |
| Project overrides | /api/conductor/overrides | ✓ | None |
| Project records | /api/projects | ✓ | None (public) |
| Todos CRUD | /api/todos, /api/todos/[id] | ✓ | JWT |
| Todo project link | n/a | ✗ — no `projectSlug` on Todo | — |
| Submit message to conductor | /api/conductor/message | ✓ | None |
| Vote on pitch | /api/conductor/pitch-vote | ✓ | Admin token |
| Art request queue | /api/conductor/art-request | ✓ | Admin token |
| List pending art requests | n/a | ✗ — YAML only, not DB | — |
| Push notifications | n/a | ✗ — not built | — |
| Task status write | n/a | ✗ — YAML/GitHub only | — |

This document feeds into conductor-app/t-001 (architecture spec) so the spec can be precise about what exists and what the app must build.
