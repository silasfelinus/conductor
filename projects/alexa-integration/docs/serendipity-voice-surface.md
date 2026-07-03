# Serendipity Alexa Voice Surface

## Target outcome

Local Amazon Echo devices should be able to summon a custom Kind Robots request through the Serendipity skill surface:

```text
Serendipity: <request>
```

In Alexa's actual phrasing this may become `Alexa, ask Serendipity to <request>` or an opened session where the user says `<request>` after launch. In our project vocabulary, `Serendipity: ____` is the stable command prefix: the words after the colon are routed by the relay.

The goal is not a generic Alexa novelty skill. It is a local voice doorway into Kind Robots and Conductor: chat, characters, dreams, art generation, music, and project work, with the same human gates the rest of the system already respects.

## What exists now

The project already has design work for safe voice commands, the relay layer, and rollout guardrails. The next phase should stop treating Alexa as only a Conductor status reader and make it the Serendipity voice surface.

Relevant current facts:

- The runtime repo now exists at `silasfelinus/serendipity-voice`.
- The relay is a small service between Alexa and existing Conductor / Kind Robots surfaces.
- The relay already separates Alexa handling, policy checks, upstream adapters, and short voice responses.
- Dream records now have `goal` and `waypoints` fields for project direction.
- `waypoints` are pipe-delimited strings where `✓ ` means done, `~ ` means in progress, and plain entries are pending.
- Dream patch routes can update `goal` and `waypoints` through the app-owned Dream API.

## Voice domains

| Domain | Example request | Expected behavior | First safe mode |
| --- | --- | --- | --- |
| LLM chat | `Serendipity: ask AMI why my relay is cranky` | Route the request into a normal Kind Robots chat stream and return a short spoken answer plus optional longer UI transcript. | read/draft |
| Character role | `Serendipity: have Professor Sparklebiscuit explain this as a dungeon quest` | Select a Character persona and run the request through that role. | read/draft |
| Dream story | `Serendipity: start a cozy mystery in the redwood library` | Start or continue a Serendipity Dream session using LOCATION, GENRE, vibe, goal, and waypoints as context. | read/draft |
| Art generation | `Serendipity: generate art of a robot fox painting a portal` | Route a spoken art request into the approved Kind Robots art generation path and return a short acknowledgement plus optional gallery/transcript link. | draft/queued |
| Local music | `Serendipity: play the rainy day coding playlist` | Ask the local relay to find and play an approved local music file, folder, or playlist. | local-only prototype |
| Project work | `Serendipity: move Alexa integration forward` | Read Dream.goal/waypoints and Conductor roadmap state, then draft a Todo or next-step note instead of editing roadmap YAML directly. | draft |

## Command interpretation

The relay should parse the command after `Serendipity:` into this shape:

```ts
type SerendipityVoiceRequest = {
  rawText: string
  domain: 'chat' | 'character' | 'dream' | 'music' | 'project' | 'art' | 'unknown'
  projectSlug?: string
  dreamSlug?: string
  characterSlug?: string
  musicTarget?: string
  artPrompt?: string
  userIntent: string
  requiresConfirmation: boolean
}
```

Parsing should favor safety over cleverness. If the domain is ambiguous, Alexa should ask one short clarification instead of guessing.

## Dream.goal and Dream.waypoints contract

For PROJECT dreams, Alexa should treat the Dream fields as the user-facing project card truth:

- `goal` = the project's definition of done, spoken when the user asks what the project is trying to become.
- `waypoints` = lightweight step list, spoken when the user asks what is next.
- `✓ ` prefix = completed step.
- `~ ` prefix = in-progress step.
- no prefix = pending step.

Conductor roadmap YAML remains the authoritative agent task queue. Dream.goal and Dream.waypoints are the friendly display layer. The relay may read both, but it should not silently mutate roadmap YAML.

## Local Echo / local relay architecture

The first useful build should run locally before any public exposure:

```text
Echo device
  → Alexa skill invocation: Serendipity
  → skill handler from serendipity-voice
  → policy router
  → Kind Robots / Conductor / local music adapters
  → short spoken response
```

Adapters should stay separate:

- `chatAdapter`: creates or continues a Kind Robots chat request.
- `characterAdapter`: resolves a Character and adds role/persona context.
- `dreamAdapter`: reads Dreams, LOCATION/GENRE ingredients, goal, and waypoints.
- `artAdapter`: queues or drafts art generation requests through the approved Kind Robots art path.
- `projectAdapter`: reads Conductor roadmap and drafts AGENT/HONEYDO Todos.
- `musicAdapter`: indexes and plays approved local music targets from a configured library root.

## Runtime and repository shape

We do not need to run our own Alexa replacement. Alexa devices still invoke an Alexa skill through Amazon's skill path. The code we own is the skill handler plus a relay/adapters runtime.

Current split:

- `silasfelinus/serendipity-voice` owns deployable/runtime code: skill handler glue, request router, relay/adapters, local harnesses, and tests.
- `silasfelinus/conductor/projects/alexa-integration` owns planning, task state, docs, rollout gates, and coordination.
- Kind Robots integration should stay behind existing Kind Robots APIs/stores unless a separate approved task changes that boundary.

The repo name intentionally uses `serendipity-voice`, not plain `serendipity`, to avoid collision with the separate Serendipity story/task project.

## Art guardrails

Art generation by voice should queue or draft requests first:

- Capture the spoken prompt as `artPrompt`.
- Confirm style, size, and target gallery when missing.
- Prefer drafts/queued jobs over immediate generation until the adapter policy is approved.
- Never publish generated images publicly from voice alone.
- Never mutate existing gallery records without an explicit approved adapter path.

## Music guardrails

Music playback should be local-first and boring on purpose:

- Only read from configured library roots.
- Never expose arbitrary filesystem browsing by voice.
- Return a clarification when multiple albums/playlists match.
- Log requested target and resolved file/folder/playlist, not the full library dump.
- Do not delete, rename, tag, or move music files.

## Project-work guardrails

Project work by voice should create draftable next steps, not secretly rewrite the machine:

Allowed first:

- Read project goal.
- Read next waypoint.
- Read in-progress waypoint.
- Summarize pending human gates.
- Draft an AGENT Todo from the spoken request.
- Draft or append a friendly project note through approved app APIs.

Blocked by voice:

- Setting `approved_by_human: true`.
- Merging PRs.
- Publishing, deploying, exposing endpoints, touching DNS, spending money, or changing secrets.
- Direct roadmap YAML mutation unless a separate human-approved task explicitly allows it.

## First implementation slice

Build the first Serendipity voice prototype with these commands only:

1. `Serendipity: what is the goal of <project>`
2. `Serendipity: what is next for <project>`
3. `Serendipity: ask <character> <question>`
4. `Serendipity: start a <genre> story in <location>`
5. `Serendipity: draft a task for <project> to <request>`
6. `Serendipity: generate art of <prompt>`
7. `Serendipity: play <music target>` behind a local-only feature flag

The prototype is successful when each request produces a short spoken answer, a logged structured intent, and no blocked action can call its adapter.

## Open questions

- Which exact Alexa invocation phrasing should we train around: `ask Serendipity to`, `open Serendipity`, or both?
- Should music playback target the Echo speaker, an existing local player, or a server-side player on Unraid?
- Which Character should be the default when the user says `Serendipity:` without naming one?
- Should Dream story sessions persist to the database immediately, or start local/draft-only until the play loop feels right?
- Should the first art adapter create draft Art records, queue jobs, or only return prompt previews until the gallery workflow is approved?
