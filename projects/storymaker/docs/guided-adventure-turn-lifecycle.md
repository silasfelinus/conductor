# Guided Adventure Turn Lifecycle

## Purpose

Guided Adventure mode is a structured Storymaker session where the narrator bot advances a shared story one turn at a time. Each turn starts from persisted session state, builds a bounded prompt, produces a short narrative beat, offers branch options, accepts either a selected branch or custom player input, applies any allowed reward/stat effects, persists the resulting state mutation, and hands off to the next turn.

This document is a server-side lifecycle spec only. It does not create schema, call live APIs, publish content, deploy anything, or mutate production data.

## Existing model anchors

The lifecycle assumes the app can read or adapt the existing Kind Robots objects described in `docs/storymaker-session-model.md` and `docs/kr-model-audit.md`:

- `Bot` supplies narrator identity, tone, and system voice.
- `Character` supplies protagonist or party stats, rarity traits, inventory-like rewards, and profile context.
- `Scenario` supplies setting, genre, cast, locations, and opening constraints.
- `Chat` or an app-owned `StorySession` record groups turns into a resumable session.
- `Reward` supplies reusable items, abilities, or unlocks that may influence turn options.

## Turn state input

Each server turn should receive a session id and an actor id. The server loads the current persisted session state and validates that the actor is allowed to act on the current turn.

Minimum state required:

- session id, mode `GUIDED_ADVENTURE`, status, and owner/participants
- narrator bot id and narrator configuration snapshot
- scenario id and scenario configuration snapshot
- current scene summary
- branch history and current branch id
- visible inventory/reward ids
- character ids and active character snapshot(s)
- safety profile and content boundaries
- turn index, current actor id, and pending choice state

The server should treat stored state as the source of truth. Client-provided story text, inventory, branch ids, or stat mutations are suggestions only and must be validated before use. Tiny trust goblin, very suspicious. 🕵️

## Lifecycle overview

1. Load and validate session state.
2. Build the narrator prompt from bounded state.
3. Generate a story beat and branch options.
4. Validate and normalize the model output.
5. Present options plus optional custom-input affordance.
6. Accept player action for the pending turn.
7. Validate custom input or selected option.
8. Apply optional stat/reward spends.
9. Mutate session state.
10. Persist turn log and new state atomically.
11. Hand off to the next turn.

## 1. Load and validate session state

The server rejects a turn request unless all of these are true:

- the session exists
- mode is `GUIDED_ADVENTURE`
- status allows play, such as `ACTIVE` or `PAUSED_RESUMABLE`
- the requesting user is the session owner or an allowed participant
- it is that user's turn, or the session allows solo owner control
- required narrator, scenario, and character references are readable

If a linked object is missing or no longer readable, the server should pause the session with a recoverable state instead of improvising a replacement.

## 2. Build the narrator prompt

The prompt should be assembled from server-held state, not raw client text. Keep it compact, structured, and repeatable.

Recommended prompt sections:

- narrator role: bot name, narrative voice, tone, hard boundaries
- scenario capsule: setting, genre, major locations, current stakes
- protagonist capsule: character name, visible traits, current inventory/rewards
- state capsule: current scene summary, last 3-5 turn summaries, unresolved flags
- player intent: chosen branch or validated custom input, if continuing from a pending action
- output contract: JSON object with `sceneText`, `options`, `statePatch`, and `safetyNotes`

The narrator should produce short, vivid, second-person prose. One turn should feel like a colorful scene card, not a novella wearing roller skates.

## 3. Generate story beat and branch options

The model output should include:

```json
{
  "sceneText": "A short second-person story beat.",
  "options": [
    { "id": "a", "label": "Follow the lanterns", "intent": "investigate", "risk": "low" },
    { "id": "b", "label": "Ask the fox-shaped door a question", "intent": "social", "risk": "medium" },
    { "id": "c", "label": "Spend a reward to reveal a hidden path", "intent": "reward", "risk": "low", "requiresRewardId": "reward-id" }
  ],
  "statePatch": {
    "sceneSummary": "One-sentence updated summary.",
    "flags": [],
    "suggestedRewards": [],
    "suggestedInventoryChanges": []
  },
  "safetyNotes": []
}
```

The server should require 2-4 branch options. Each option needs a stable id, short label, intent, and optional cost or requirement metadata. The model may suggest state changes, but the server decides what is legal to persist.

## 4. Validate and normalize model output

Before persisting or displaying a generated beat, validate:

- `sceneText` exists and fits length limits
- branch option count is within bounds
- branch option ids are unique and simple
- reward requirements reference rewards actually owned or available
- state patch keys are allowed
- suggested inventory/reward changes are valid for this session
- generated text does not claim live side effects happened outside the story

If validation fails, retry once with a repair prompt. If repair fails, store a safe error turn and preserve the previous session state.

## 5. Present choices to the client

The response to the client should include:

- turn id
- scene text
- normalized option list
- whether custom input is allowed
- any visible reward/stat spend affordances
- short state summary for resume UX

Custom input should be framed as an alternate action, not as unlimited prompt injection. The client can let the user type something delightful, but the server still gets the bouncer clipboard.

## 6. Accept selected branch or custom input

A player action request should include:

- session id
- pending turn id
- selected option id, or custom input text
- optional reward/stat spend ids

The server validates that the pending turn is still current and has not already been resolved. Duplicate submissions should be idempotent when possible: return the already-resolved next state instead of creating a second branch.

## 7. Validate custom input

Custom input is allowed only if the session configuration permits it. Validation rules:

- trim and length-limit the text
- reject instructions that attempt to override system, safety, or persistence rules
- reject requests to perform real-world actions, spending, publishing, account changes, or external contact
- classify the input intent, such as `explore`, `social`, `combat-lite`, `craft`, `rest`, or `inspect`
- convert valid custom text into a server-owned action summary

The action summary, not raw untrusted text, should be passed to the narrator prompt. Keep the user's flavor, remove the cursed puppet strings.

## 8. Apply stat or reward spends

Reward/stat spends should be optional and deterministic. The server checks:

- the user owns or can access the reward
- the reward is usable in this session mode
- the reward is not already consumed, unless it is reusable
- any stat cost is affordable
- the spend does not bypass a human approval gate or real-world action boundary

Spend effects should be small and story-facing for MVP:

- unlock a special branch option
- add advantage to a risky narrative move
- reveal extra scenario detail
- convert a failure into a complication
- add a temporary story flag

Do not mutate permanent profile inventory until a later approved task defines that flow.

## 9. Mutate state

After resolving the player action and narrator output, the server builds an explicit state patch.

Allowed MVP mutations:

- increment turn index
- append branch history entry
- update current scene summary
- update active location id or label
- append unresolved story flags
- mark temporary rewards as used within this session
- store a compact summary of the generated beat
- set next actor id

Disallowed MVP mutations:

- permanent account/profile changes
- public posts or published story pages
- external API side effects
- billing, deployment, DNS, auth, or permission changes
- real Todo or roadmap write-back

Those disallowed mutations can become later gated tasks. No sneaky side quests.

## 10. Persist atomically

The server should persist the turn log and session state in one transaction or transaction-like operation.

Suggested records:

- `StoryTurn`: immutable log of actor, action, generated scene, options shown, selected option/custom summary, and resulting state patch
- `StorySession.currentState`: compact resumable state snapshot
- `StorySession.updatedAt`: used for resume ordering

If using existing `Chat` records before a dedicated `StoryTurn` model exists, store the generated beat as a chat message and keep a structured state snapshot in app-owned session storage. Avoid overloading public chat content with hidden control metadata.

## 11. Hand off to next turn

For solo Guided Adventure, next actor is usually the same user. For future multi-user Guided Adventure, next actor can rotate through participants.

The handoff response should include:

- next turn index
- next actor id
- short summary of what changed
- whether a new prompt should generate immediately or wait for player input
- resume token or route target

The UI should be able to resume a session from this response without replaying the entire story.

## Safety limits

Guided Adventure turns should enforce:

- max prompt context size
- max scene text length
- max options per turn
- max custom input length
- max turns per session before summary compression
- retry limit for invalid model output
- no direct write-back to Todos, roadmaps, publishing systems, billing, DNS, secrets, or deployments

The story can ask the player to decide something, but it cannot silently take the decision for them.

## Error handling

Use recoverable failure states:

- `PAUSED_NEEDS_REPAIR` when linked story data is missing
- `TURN_GENERATION_FAILED` when model output cannot be repaired
- `ACTION_REJECTED` when custom input or reward spend is invalid
- `SESSION_LOCKED` when another request is already resolving the turn

The client should show a friendly retry/resume message and preserve all prior session state.

## Verification checklist for implementation

When this lifecycle is implemented later, verify:

- a session can generate a first beat from narrator + scenario + character state
- branch options are stable and selectable
- custom input is accepted only through server normalization
- invalid reward spends are rejected
- duplicate action submissions do not fork the same turn twice
- generated state patches only touch allowed fields
- session resumes from compact state without losing branch history
- no task queue, roadmap, publishing, billing, secret, DNS, or deploy side effects occur

## Follow-up tasks suggested

- Define the `StoryTurn` persistence shape and whether it lives in app-owned schema or current chat metadata.
- Write the Exquisite Corpse visibility and mutation rules separately from this Guided Adventure lifecycle.
- Sketch the first UX flow for choosing a narrator, scenario, branch option, and custom action.
