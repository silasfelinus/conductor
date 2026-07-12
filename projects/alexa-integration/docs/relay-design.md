# Alexa Relay Design Note

## Scope

This is a document-only design for a small relay layer between an Alexa skill and the existing Conductor / Kind Robots surfaces. It does not create a live Alexa skill, expose a public endpoint, add secrets, change billing, touch DNS, trigger a deploy, or write to production data.

The relay's job is intentionally narrow: translate approved voice intents into safe reads or draft-only actions, apply guardrails, and return short voice-friendly responses.

The updated product target is the Serendipity voice surface: local Echo devices should be able to route `Serendipity: <request>` into Kind Robots chat, Character roleplay, Dream story sessions, approved local music playback, and safe project-work drafts. See `projects/alexa-integration/docs/serendipity-voice-surface.md` for the command contract.

## Goals

- Let Silas ask for project status, pending approvals, recent activity, and safe task summaries by voice.
- Let Silas ask custom LLM questions through Kind Robots chat streams.
- Let Silas route a voice request through a selected Character role/persona.
- Let Silas start or continue a Serendipity Dream story using LOCATION, GENRE, vibe, and goal.
- Let Silas play approved local music files through a local-only adapter.
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
  "intent": "SerendipityRequestIntent",
  "slots": {
    "requestText": "what is next for alexa integration"
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

- `serendipityRouter`: parses `Serendipity: <request>` text into chat, character, dream, music, project, or unknown domains.
- `chatAdapter`: creates or continues a Kind Robots chat request.
- `characterAdapter`: resolves a Character and adds role/persona context to the request.
- `dreamAdapter`: reads Dream ingredients and PROJECT Dream `goal`; project progress (milestones, next task) comes from the Conductor roadmap.
- `conductorAdapter`: reads project status, roadmaps, pending approval summaries, and activity summaries.
- `kindRobotsAdapter`: reads Dream/project display data and, later, creates Todos if machine auth is approved.
- `musicAdapter`: resolves approved local music file, folder, or playlist targets from configured library roots only.
- `artAdapter`: queues or drafts art requests only when explicitly approved by the command policy.

Adapters should return normalized relay objects instead of leaking raw API responses into voice formatting.

### 4. Policy layer

Every intent must pass through a policy table before it can call an adapter.

Suggested policy fields:

```ts
type RelayPolicy = {
  intent: string
  mode: 'read' | 'draft' | 'local' | 'blocked'
  requiresConfirmation: boolean
  allowedWithApiKey: boolean
  allowedWithUserJwt: boolean
  humanGateRequired: boolean
}
```

This makes it obvious which commands are safe reads, which commands are local-only, and which commands are not allowed until Silas approves the auth model.

## Intent mapping

| Voice action | Intent | Relay mode | Upstream surface | Safety rule |
| --- | --- | --- | --- | --- |
| `Serendipity: what is next for Serendipity?` | `ProjectStatusIntent` | read | Project goal + Conductor roadmap (next ready task, milestones) | Read only |
| `Serendipity: ask AMI why the relay is cranky` | `ChatIntent` | read/draft | Kind Robots chat stream | No production mutation |
| `Serendipity: have Captain Whisker explain this as a quest` | `CharacterIntent` | read/draft | Character + chat stream | No production mutation |
| `Serendipity: start a cozy mystery in the redwood library` | `DreamStoryIntent` | read/draft | Serendipity Dream story loop | Persist only after approved write path |
| `Serendipity: play rainy day coding` | `LocalMusicIntent` | local | Local music adapter | Configured library roots only |
| `Serendipity: draft a task for Alexa integration to add tests` | `CreateAgentTodoIntent` | draft | Kind Robots Todo API | Requires confirmation and approved auth |
| `Serendipity: what needs my approval?` | `PendingApprovalsIntent` | read | Conductor roadmaps / pending gates | Read only |
| `Serendipity: what changed today?` | `ActivitySummaryIntent` | read | Conductor changelog / status artifact | Read only |
| `Serendipity: queue art for this project` | `QueueArtRequestIntent` | draft | Conductor art request dry-run | Draft only; no live generation without approval |
| `Serendipity: approve this task` | `ApproveTaskIntent` | blocked | Roadmap human gate | Always blocked by voice; Alexa can say where to approve manually |
| `Serendipity: merge this PR` | `MergePrIntent` | blocked | GitHub | Always blocked by voice |
| `Serendipity: publish this` | `PublishIntent` | blocked | External surfaces | Always blocked by voice |

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
SERENDIPITY_MUSIC_ROOTS=
SERENDIPITY_MUSIC_ENABLED=false
```

`KR_USER_JWT` should not be required for the first read-only relay prototype. Todo creation should remain disabled until Silas explicitly chooses a long-lived user auth strategy or a dedicated machine-auth route exists.

## Response format

Voice responses should be short, concrete, and confirm whether an action happened.

Examples:

- Project status: "Alexa integration is working toward local Serendipity voice control. Next task: build the request router."
- Pending approvals: "You have four approval gates. Top priority: digital storefront platform choice."
- Chat answer: "AMI says the relay is cranky because it needs a policy table before adapters. Classic goblin behavior."
- Dream story: "The redwood library opens under your feet. A moth librarian asks which task you came to rescue."
- Music clarification: "I found three rainy day playlists. Do you want coding, piano, or thunderstorm?"
- Create todo blocked: "I can draft that later, but todo creation needs approved user authentication first."
- Blocked action: "I can't approve or merge by voice. Open the conductor page and approve it there."

The relay can include longer debug detail in logs, but Alexa should speak the short form.

## Guardrails

- Read-only commands are allowed first.
- Local music commands are local-only, feature-flagged, and restricted to configured library roots.
- Draft commands must say "draft" or "queue" and may not publish, deploy, spend, send, approve, or merge.
- Voice cannot set `approved_by_human: true`.
- Voice cannot edit roadmap YAML directly.
- Voice cannot trigger live art generation until Silas approves that flow separately.
- Voice cannot touch DNS, billing, secrets, deploys, production data, or public publishing.
- Every relay request gets an audit log line with timestamp, intent, project slug if present, mode, result, and request id.
- Failed upstream calls return a safe explanation, not stack traces.

## Minimal first prototype

Build the first relay prototype with only the Serendipity router and safe local responses:

1. `ProjectStatusIntent`
2. `PendingApprovalsIntent`
3. `ChatIntent`
4. `CharacterIntent`
5. `DreamStoryIntent`
6. `CreateAgentTodoIntent` as confirmation-only/draft-only
7. `LocalMusicIntent` behind `SERENDIPITY_MUSIC_ENABLED=false` by default

Stub all write/draft intents as policy-blocked until the relevant auth and confirmation path is approved. This proves the voice loop without mutation risk.

## Suggested file layout for a later implementation

```text
projects/alexa-integration/relay/
  package.json
  tsconfig.json
  src/server.ts
  src/policy.ts
  src/intents.ts
  src/serendipity-router.ts
  src/adapters/chat.ts
  src/adapters/character.ts
  src/adapters/conductor.ts
  src/adapters/dream.ts
  src/adapters/kind-robots.ts
  src/adapters/music.ts
  src/voice-response.ts
```

## Verification plan for the later implementation

- Unit-test every intent against the policy table.
- Unit-test `Serendipity: <request>` domain routing.
- Snapshot-test Alexa response text for the safe read/draft intents.
- Test that blocked intents never call adapters.
- Test that missing credentials produce safe "not configured" messages.
- Test that no route can approve, merge, publish, deploy, spend, or touch secrets.
- Test that local music cannot escape configured library roots.
- Run locally only until Silas approves a rollout checklist.

## Open questions for Silas

- Should the relay live inside conductor, inside kind_robots, or as a tiny separate self-hosted service on Unraid?
- Should Todo creation use a long-lived user JWT, a new machine-auth route, or stay manual-only?
- Should Alexa ever be allowed to queue dry-run art requests, or should it only report art queue status?
- Should local music play through Echo, an existing local player, or the Unraid host?
- Which Character is the default when the user says `Serendipity:` without naming one?
- What phrase should Alexa use when redirecting approval actions to the web UI?

## Next task unlocked

After this design is accepted, the next safe step is the Serendipity voice request router: parse `Serendipity: <request>`, classify the domain, apply policy, and return a short local response without live publishing or production mutation.
