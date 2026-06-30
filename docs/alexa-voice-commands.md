# Alexa Voice Commands — Conductor Integration

Generated: 2026-06-30
Task: alexa-integration/t-001

---

## Purpose

Define the first command list and sample phrases for the Conductor/Alexa integration. These are design-only; no live service work until Silas approves. All commands map to existing kind_robots API endpoints or relay-side formatting of existing data.

---

## Auth Model Summary

- **Conductor/project reads**: Admin API key (`KR_API_TOKEN`) — safe for relay
- **Todo reads/creates**: User JWT required — relay must hold a long-lived or machine-auth JWT (this is the main auth gap; see pitches needed below)
- **Public project status**: No auth required (GET /api/conductor/projects, GET /api/dreams)

---

## Command Categories

### 1. Project Status

**Intent:** Get a quick status readout on one or all projects.

| Phrase | Relay action | Response format |
|---|---|---|
| "Alexa, ask Conductor for a project summary" | GET /api/conductor/projects → summarize active projects | "You have N active projects. Top priority: [name]. [name] has [X] ready tasks." |
| "Alexa, ask Conductor what's blocking [project name]" | GET /api/conductor/projects → find project, filter needs-human/blocked tasks | "The [project] project has [N] blocked tasks: [titles]." |
| "Alexa, ask Conductor what needs my attention today" | GET /api/conductor/projects → aggregate gate_human + needs-human tasks | "You have [N] decisions waiting. First: approve [task title] in [project]." |
| "Alexa, ask Conductor for the [project name] status" | GET /api/conductor/projects → find by slug or name match | "[project] is active with [N] tasks: [X] done, [Y] ready, [Z] blocked." |

**Missing endpoint pitch needed:** `GET /api/conductor/status` — returns a single phrase like "3 decisions waiting, 2 tasks in progress, last update 2h ago." This avoids summarizing the entire projects payload in the relay.

---

### 2. Task Status and Approvals

**Intent:** Hear what gates are waiting and approve or escalate them by voice.

| Phrase | Relay action | Response format |
|---|---|---|
| "Alexa, ask Conductor how many approvals are pending" | GET /api/conductor/projects → count gate_human:true, approved_by_human:false | "You have [N] pending approvals." |
| "Alexa, ask Conductor what approvals are waiting" | GET /api/conductor/projects → list needs-human tasks | "First approval needed: [task title] in [project]. Want to hear the note?" |
| "Alexa, ask Conductor to read me the [task ID] note" | GET /api/conductor/projects → find task by id, read note field | "[note text]" |

**Missing endpoint pitch needed:** `GET /api/conductor/pending-approvals` — returns a count and list of gate_human tasks not yet approved. Avoids sending the full projects payload to Alexa.

**Out of scope for voice (needs-human gate remains hard):** Approving a task (setting `approved_by_human: true`) requires writing back to the conductor roadmap YAML in GitHub. This write cannot happen via voice command without an explicit authorization step. Voice can READ what needs approval but cannot WRITE the approval. Silas must approve via the web UI or PR review.

---

### 3. Create Todos

**Intent:** Add a task or reminder to the todo list by voice.

| Phrase | Relay action | Response format |
|---|---|---|
| "Alexa, ask Conductor to add a todo: [description]" | POST /api/todos with title=[description], category=HONEYDO | "Added: [description]. Want to set a priority?" |
| "Alexa, ask Conductor to add a high priority todo: [description]" | POST /api/todos with priority=HIGH | "Added high-priority todo: [description]." |
| "Alexa, ask Conductor to remind me to [description]" | POST /api/todos with category=HONEYDO | "Reminder added: [description]." |
| "Alexa, ask Conductor what my open todos are" | GET /api/todos?status=OPEN → list top 3 | "You have [N] open todos. Top: [title 1], [title 2], [title 3]." |

**Auth note:** POST /api/todos and GET /api/todos require a user JWT (`requireApiUser`). The relay must store a long-lived user JWT or a machine auth token for Silas's account. This needs a pitch — the relay cannot use a static API key for todo operations.

---

### 4. Art Requests

**Intent:** Queue missing image requests for the art pipeline.

| Phrase | Relay action | Response format |
|---|---|---|
| "Alexa, ask Conductor to request art for [project name]" | POST /api/conductor/art-request with projectSlug inferred | "Art request queued for [project]. The Worker will generate images next cycle." |
| "Alexa, ask Conductor how many art requests are pending" | Relay reads from GET /api/conductor/projects or static count | "There are [N] art requests in the queue." |

**Auth note:** POST /api/conductor/art-request uses `validateApiKey` (admin API key) — compatible with static relay token.

**Gap:** There is no endpoint to list pending art requests from the DB. Those live in conductor/projects/art-prompts.yaml as YAML. Voice count requires the relay to either parse YAML from GitHub API or a new endpoint to be pitched.

---

### 5. Agent Activity Summary

**Intent:** Hear what the AI workers have been doing.

| Phrase | Relay action | Response format |
|---|---|---|
| "Alexa, ask Conductor what the workers did today" | GET /api/conductor/projects → filter tasks updated today | "Today the worker completed [N] tasks: [titles]." |
| "Alexa, ask Conductor for an agent summary" | Same + aggregate in-progress tasks | "[N] tasks completed today, [M] in progress, [K] waiting for you." |

**Missing endpoint pitch needed:** `GET /api/conductor/status` (same as above) with an optional `?summary=brief` parameter returns a voice-ready summary phrase without the full JSON payload.

---

## Phrases Not Supported (Out of Scope)

| Phrase | Reason |
|---|---|
| "Approve task [X]" | Requires GitHub write — needs-human gate cannot be cleared by voice |
| "Deploy [project]" | Deployment is a hard gate — not automatable by voice |
| "Cancel todo [title]" | DELETE requires title-to-id resolution; risky voice command; skip at MVP |
| "Read me the latest PR" | PR content is large and not voice-friendly |
| "Send a message to the team" | No messaging channel hooked to Alexa; out of scope |

---

## Pitches Needed Before Implementation

1. **`GET /api/conductor/status`** — short activity phrase (≤ 2 sentences) for voice summaries. Effort: small.
2. **`GET /api/conductor/pending-approvals`** — count of gate_human tasks not yet approved. Effort: small.
3. **Machine auth / long-lived JWT** for relay ↔ kind_robots todo operations (POST/GET /api/todos). Currently requires user JWT; relay cannot safely cache a short-lived token. Effort: medium (backend change to kind_robots).

---

## Summary

| Category | Commands | Auth requirement |
|---|---|---|
| Project status | 4 phrases | Admin API key (KR_API_TOKEN) |
| Approvals (read-only) | 3 phrases | Admin API key |
| Create todos | 4 phrases | User JWT (auth gap — needs pitch) |
| Art requests | 2 phrases | Admin API key |
| Agent summary | 2 phrases | Admin API key |

All 15 phrases produce ≤10-word voice responses at the relay layer with relay-side formatting. Three endpoints need to be pitched to kind_robots before the relay can implement them cleanly. Todo operations need an auth solution before they can go live.

This document feeds into alexa-integration/t-002 (relay design) so the relay spec knows exactly which endpoints to map and which gaps need pitching first.
