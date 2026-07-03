# Alexa Relay Design Note

## Scope

This is a document-only design for a small relay layer between an Alexa skill and the existing Conductor / Kind Robots surfaces. It does not create a live Alexa skill, expose a public endpoint, add secrets, change billing, touch DNS, trigger a deploy, or write to production data.

The relay's job is intentionally narrow: translate approved voice intents into safe reads or draft-only actions, apply guardrails, and return short voice-friendly responses.

## Goals

- Let Silas ask for project status, pending approvals, recent activity, and safe task summaries by voice.
- Let Silas create draft agent todos through a controlled relay path once authentication is approved.
- Keep voice output short enough for Alexa while preserving richer detail in logs or linked UI surfaces.
- Separate Alexa-specific interaction handling from Conductor roadmap files and Kind Robots backend details.
- Make dangerous or outward-facing actions impossible unless they become explicit human review tasks.

## Non-goals

- No live Alexa publishing.
- No new production endpoint in this task.
- No credential storage design beyond naming required environment variables.
- No direct roadmap mutation by voice.
- No deploy, DNS, billing, production data, or secret changes.
- No bypass of existing human gates.

## Proposed components

### 1. Alexa skill front door

The Alexa skill should collect a normalized intent and slots, then call the relay over HTTPS. The skill should not know Conductor roadmap structure or Kind Robots API details.

Example payload:

```json
{
  "intent": "ProjectStatusIntent",
  "slots": {
    "projectSlug": "serendipity"
  },
  "requestId": "amzn1.echo-api.request.example",
  "userId": "amzn1.ask.account.example"
}
```

### 2. Relay API

The relay can be a small self-hosted service, for example a Hono / TypeScript server or a tiny Python FastAPI service. It should expose one internal route first:

```text
POST /alexa/intent
```

The relay validates the request, maps the intent to an approved action, calls the required upstream read or draft endpoint, formats a short response, and writes an audit log entry.

### 3. Upstream adapters

Adapters keep upstream calls isolated:

- `conductorAdapter`: reads project status, roadmaps, pending approval summaries, and activity summaries.
- `kindRobotsAdapter`: reads Dream/project display data and, later, creates Todos if machine auth is approved.
- `artAdapter`: queues or drafts art requests only when explicitly approved by the command policy.

Adapters should return normalized relay objects instead of leaking raw API responses into voice formatting.

### 4. Policy layer

Every intent must pass through a policy table before it can call an adapter.

Suggested policy fields:

```ts
type RelayPolicy = {
  intent: string
  mode: 'read' | 'draft' | 'blocked'
  requiresConfirmation: boolean
  allowedWithApiKey: boolean
  allowedWithUserJwt: boolean
  humanGateRequired: boolean
}
```

This makes it obvious which commands are safe reads and which commands are not allowed until Silas approves the auth model.

## Intent mapping

| Voice action | Intent | Relay mode | Upstream surface | Safety rule |
| --- | --- | --- | --- | --- |
| "What is next for Serendipity?" | `ProjectStatusIntent` | read | Conductor project status / roadmap | Read only |
| "What needs my approval?" | `PendingApprovalsIntent` | read | Conductor roadmaps / pending gates | Read only |
| "What changed today?" | `ActivitySummaryIntent` | read | Conductor changelog / status artifact | Read only |
| "Add a task for the Worker" | `CreateAgentTodoIntent` | draft | Kind Robots Todo API | Block until JWT or machine auth is approved |
| "Queue art for this project" | `QueueArtRequestIntent` | draft | Conductor art request dry-run | Draft only; no live generation without approval |
| "Approve this task" | `ApproveTaskIntent` | blocked | Roadmap human gate | Always blocked by voice; Alexa can say where to approve manually |
| "Merge this PR" | `MergePrIntent` | blocked | GitHub | Always blocked by voice |
| "Publish this" | `PublishIntent` | blocked | External surfaces | Always blocked by voice |

## Authentication model

The relay should require two layers:

1. Alexa request verification or an equivalent skill-side shared-secret check.
2. Relay-to-upstream credentials stored outside source control.

Recommended environment variables:

```text
ALEXA_RELAY_SHARED_SECRET=
KR_BASE_URL=
KR_API_TOKEN=
KR_USER_JWT=
CONDUCTOR_REPO=silasfelinus/conductor
GITHUB_TOKEN=
```

`KR_USER_JWT` should not be required for the first read-only relay prototype. Todo creation should remain disabled until Silas explicitly chooses a long-lived user auth strategy or a dedicated machine-auth route exists.

## Response format

Voice responses should be short, concrete, and confirm whether an action happened.

Examples:

- Project status: "Serendipity is blocked on one approval: write-back design. Next agent task unlocks after approval."
- Pending approvals: "You have four approval gates. Top priority: digital storefront platform choice."
- Create todo blocked: "I can draft that later, but todo creation needs approved user authentication first."
- Blocked action: "I can't approve or merge by voice. Open the conductor page and approve it there."

The relay can include longer debug detail in logs, but Alexa should speak the short form.

## Guardrails

- Read-only commands are allowed first.
- Draft commands must say "draft" or "queue" and may not publish, deploy, spend, send, approve, or merge.
- Voice cannot set `approved_by_human: true`.
- Voice cannot edit roadmap YAML directly.
- Voice cannot trigger live art generation until Silas approves that flow separately.
- Voice cannot touch DNS, billing, secrets, deploys, production data, or public publishing.
- Every relay request gets an audit log line with timestamp, intent, project slug if present, mode, result, and request id.
- Failed upstream calls return a safe explanation, not stack traces.

## Minimal first prototype

Build the first relay prototype with only read intents:

1. `ProjectStatusIntent`
2. `PendingApprovalsIntent`
3. `ActivitySummaryIntent`

Stub all write/draft intents as policy-blocked with clear responses. This proves the voice loop without any production mutation risk.

## Suggested file layout for a later implementation

```text
projects/alexa-integration/relay/
  package.json
  tsconfig.json
  src/server.ts
  src/policy.ts
  src/intents.ts
  src/adapters/conductor.ts
  src/adapters/kind-robots.ts
  src/voice-response.ts
```

## Verification plan for the later implementation

- Unit-test every intent against the policy table.
- Snapshot-test Alexa response text for the three read-only intents.
- Test that blocked intents never call adapters.
- Test that missing credentials produce safe "not configured" messages.
- Test that no route can approve, merge, publish, deploy, or spend.
- Run locally only until Silas approves a rollout checklist.

## Open questions for Silas

- Should the relay live inside conductor, inside kind_robots, or as a tiny separate self-hosted service on Unraid?
- Should Todo creation use a long-lived user JWT, a new machine-auth route, or stay manual-only?
- Should Alexa ever be allowed to queue dry-run art requests, or should it only report art queue status?
- What phrase should Alexa use when redirecting approval actions to the web UI?

## Next task unlocked

After this design is accepted, the next safe step is the rollout and safety checklist: testing, disabling, logging, and review procedures before any real voice command integration is used.