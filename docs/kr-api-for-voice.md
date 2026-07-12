# Kind Robots REST API — Voice / Alexa Suitability Audit

Generated: 2026-06-30
Task: alexa-integration/t-004

---

## Purpose

This document maps the kind_robots REST API endpoints that are relevant to voice control via an Alexa skill relay server. For each endpoint, it notes: HTTP method and path, auth requirement, voice suitability (response fits ≤10 words), and any blockers.

---

## Auth Model

kind_robots has two auth modes relevant to a relay server:

| Mode | Header | Who can use it | What endpoints |
|---|---|---|---|
| `requireApiUser` | `Authorization: Bearer <jwt>` | Users with valid session JWT | todos, dreams, reactions, most user-data endpoints |
| `validateApiKey` | `Authorization: Bearer <token>` or `x-api-key` | Admins with API token (KR_API_TOKEN) | conductor/*, art-request, some admin routes |

**Critical gap for Alexa relay:** The todo endpoints use `requireApiUser`, which validates a JWT tied to a specific user session. A relay server making calls on Silas's behalf needs a long-lived JWT (or a new machine-to-machine token path) — a simple static API key won't work for the todo routes as they exist today. The conductor/* endpoints (projects, message, pitch-vote) use the admin API key path and work cleanly for a relay.

---

## Endpoint Inventory — Voice-Relevant

### Todos

| Method | Path | Auth | Voice summary | Fits ≤10 words | Notes |
|---|---|---|---|---|---|
| GET | `/api/todos` | requireApiUser (JWT) | "You have N open todos." | ✓ | Supports `?status=OPEN`. Returns sorted list; relay reads count + titles |
| GET | `/api/todos` | requireApiUser (JWT) | "Your top todo is: [title]" | ✓ | Same endpoint; relay picks first item from priority-sorted list |
| POST | `/api/todos` | requireApiUser (JWT) | "Todo added: [title]" | ✓ | Body: `{ title, description?, priority?, category? }`. Priority: LOW/NORMAL/HIGH. Category: AGENT/KAIZEN/HONEYDO |
| PATCH | `/api/todos/[id]` | requireApiUser (JWT) | "Done." | ✓ | Mark todo complete; body: `{ status: "DONE" }` |

### Projects and Status

| Method | Path | Auth | Voice summary | Fits ≤10 words | Notes |
|---|---|---|---|---|---|
| GET | `/api/conductor/projects` | None (reads GitHub) | "[project] is [N]% complete." | ✓ | Returns all projects with milestones, tasks, progress %. Good for status readouts. |
| GET | `/api/conductor/overrides` | None (reads GitHub) | N/A (data only) | — | Returns status/priority map per project. Useful to filter active projects. |
| GET | `/api/conductor/prs` | None (reads GitHub) | "There are N open PRs." | ✓ | Returns open PRs count |

### Messages and Inbox

| Method | Path | Auth | Voice summary | Fits ≤10 words | Notes |
|---|---|---|---|---|---|
| POST | `/api/conductor/message` | None (writes to GitHub via server GITHUB_TOKEN) | "Message sent." | ✓ | Body: `{ message, type? }`. Prepends to conductor/INBOX.md. Voice: "Tell Silas: [message]" → writes message |
| POST | `/api/conductor/inbox` | None (same) | "Note saved." | ✓ | Body: `{ message, project? }`. Writes a dated note to conductor/inbox/. More permanent than message |

### Pitch Voting

| Method | Path | Auth | Voice summary | Fits ≤10 words | Notes |
|---|---|---|---|---|---|
| POST | `/api/conductor/pitch-vote` | validateApiKey (admin) | "[title] approved." | ✓ | Body: `{ slug, vote: "approved" | "passed" }`. Updates pitch status in GitHub. |

### Art Requests

| Method | Path | Auth | Voice summary | Fits ≤10 words | Notes |
|---|---|---|---|---|---|
| POST | `/api/conductor/art-request` | validateApiKey (admin) | "Art request queued." | ✓ | Complex body; adds entry to art-prompts.yaml. Voice trigger: "Request new icon for [project]" but complex to parameterize from voice |

### Dreams (Projects)

| Method | Path | Auth | Voice summary | Fits ≤10 words | Notes |
|---|---|---|---|---|---|
| GET | `/api/projects?status=ACTIVE` | Optional (public projects visible without auth) | "[name] is [status]." | ✓ | First-class Project model (post Dream/Project/Facet split). GET /api/projects/[slug] also resolves conductorSlug |
| PATCH | `/api/projects/[id]` | requireApiUser (JWT) or admin token | "Project updated." | ✓ | Can update status from voice: "Pause [project]" |

---

## Gaps for Alexa Integration

| Gap | Impact | Suggestion |
|---|---|---|
| **No agent activity summary endpoint** | Voice can't say "agents are idle / 3 tasks in flight" | Build `GET /api/conductor/status` returning a short phrase: active PRs count + in-flight tasks count |
| **Todos require user JWT (not API key)** | Relay can't use a static token for todo operations | Option A: generate a long-lived refresh token for the relay user. Option B: add a `POST /api/todos/machine` route that accepts KR_API_TOKEN + userId and bypasses JWT requirement for trusted relay calls |
| **No voice-optimized project status phrase** | GET /api/conductor/projects returns full YAML-parsed JSON; relay must compute "40% complete" | Relay-side computation is fine here; no new endpoint needed |
| **No "list today's approvals needed" endpoint** | Alexa can't announce "You have 2 gated tasks to approve" | Build `GET /api/conductor/pending-approvals` derived from projects data, or let relay filter gate_human tasks from the projects endpoint |

---

## Summary

**Endpoints ready to use for voice (no backend changes needed):**
- GET /api/conductor/projects — project status readouts
- POST /api/conductor/message — "Tell Silas [message]"
- POST /api/conductor/pitch-vote — "Approve pitch [slug]"
- GET /api/projects — project status via the Project model

**Endpoints that need relay workaround or backend change:**
- GET|POST|PATCH /api/todos — need long-lived JWT or machine auth route

**Endpoints to build before voice launch:**
- GET /api/conductor/status — short agent activity phrase
- GET /api/conductor/pending-approvals — today's blocked gates count

This feeds directly into alexa-integration/t-002 (relay design) once t-001 (voice command list) is approved by Silas.
