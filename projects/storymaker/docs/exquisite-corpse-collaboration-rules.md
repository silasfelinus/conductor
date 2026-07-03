# Exquisite Corpse Collaboration Rules

## Purpose

Exquisite Corpse mode is Storymaker's async-first collaboration format. Players take turns adding to a shared story while seeing only a bounded slice of prior context. The mode should preserve the surreal surprise of the classic game while still keeping enough structure for Kind Robots sessions, Characters, Scenarios, Rewards, Chats, and future app-owned story state to stay coherent.

This document is a rules and data-contract spec only. It does not create schema, call live APIs, publish content, deploy anything, or mutate production data.

## Design goals

- Keep play lightweight enough for asynchronous participation.
- Preserve partial-visibility surprise without making the resulting story unusable.
- Make every mutation server-validated and attributable to a player turn.
- Allow story, character, and world additions without letting one player rewrite the whole session.
- Produce a clean turn log that can later feed rewards, reusable artifacts, and UX summaries.

## Existing model anchors

Exquisite Corpse can start with the same anchors used by Guided Adventure:

- `Bot` supplies optional host, moderator, or narrator voice.
- `Character` supplies player personas, party members, or reusable figures introduced during play.
- `Scenario` supplies the premise, genre, opening constraints, location palette, and safety frame.
- `Chat` or an app-owned `StorySession` groups turns into a resumable collaborative session.
- `Reward` may eventually unlock prompts, constraints, or remix rights, but should not mutate permanent profile inventory in the MVP.

The server-held session state remains the source of truth. Client-provided text is a contribution request, not an authority to alter hidden state directly. Classic goblin rule: delight is welcome, custody of the database is not. 🧌

## Session configuration

Each Exquisite Corpse session should snapshot these settings at creation:

- session id, mode `EXQUISITE_CORPSE`, status, owner, and participant list
- host/narrator Bot id, if a bot is facilitating intros or summaries
- Scenario id and scenario capsule
- turn order strategy
- visibility mode
- contribution limits
- mutation permissions
- safety profile and content boundaries
- merge policy for story, character, and world elements
- completion condition

Recommended MVP defaults:

- turn order: fixed rotation by participant join order
- visibility: last visible fragment plus public session premise
- contribution length: 1-3 paragraphs or a short structured scene beat
- custom inputs: allowed only as the player's own contribution text
- bot assistance: optional rewrite/safety summary, never silent authorship
- completion: fixed turn count or owner-ended session

## Turn order

The server should own turn order. A client may display whose turn is next, but it should not decide it.

Supported turn order strategies:

1. `ROUND_ROBIN` — participants act in stable order.
2. `OPEN_CLAIM` — any eligible participant may claim the next turn until the claim expires.
3. `HOST_DIRECTED` — the owner or host bot selects the next actor from eligible participants.
4. `SOLO_TEST` — the owner can take every turn for testing and demos.

MVP should start with `ROUND_ROBIN` and `SOLO_TEST` only. `OPEN_CLAIM` and `HOST_DIRECTED` are useful later but introduce timeout, moderation, and fairness questions.

## Turn lifecycle

1. Load session state and validate actor eligibility.
2. Build the actor's visible context packet.
3. Accept a contribution draft.
4. Validate and normalize the draft.
5. Derive an allowed state patch.
6. Persist immutable turn log plus updated session state atomically.
7. Advance turn pointer or complete the session.
8. Generate optional public summary or next-player teaser.

## Actor validation

A turn request is valid only when:

- the session exists
- mode is `EXQUISITE_CORPSE`
- status allows play, such as `ACTIVE`
- the actor is a participant, owner, or permitted solo tester
- the actor matches the current turn pointer or has a valid turn claim
- the pending turn has not already been resolved
- the actor can read the visible context packet

Duplicate submissions for the same pending turn should be idempotent when possible. If the contribution was already accepted, return the accepted turn rather than forking the story.

## Visibility modes

Visibility is the heart of this mode. The server must construct the visible packet from stored state; the client should not receive hidden turns and merely promise not to display them.

Recommended visibility modes:

### `LAST_FRAGMENT_ONLY`

The player sees:

- session title and premise
- safety/tone boundaries
- the final paragraph or final 2-4 sentences of the previous accepted turn
- their own prior turns, if any
- any public artifacts the session has marked visible

They do not see the full story so far. This is the classic mode and the best MVP default.

### `SUMMARY_PLUS_FRAGMENT`

The player sees:

- a short bot-generated or server-curated summary of established facts
- the latest fragment
- public artifacts

This is less chaotic and better for longer sessions. It should be used when the story needs continuity across many turns.

### `FULL_CONTEXT_AFTER_LOCK`

While contributing, the player only sees the bounded context. After their turn is submitted, they may see more or all prior accepted turns depending on session settings.

This gives players a fun reveal moment without letting them optimize their contribution too much beforehand.

## What each player can see

Minimum player-visible packet:

```json
{
  "sessionId": "story-session-id",
  "mode": "EXQUISITE_CORPSE",
  "turnId": "pending-turn-id",
  "title": "The Moonlit Door Beneath the Laundromat",
  "premise": "A strange, hopeful urban fantasy story about hidden kindness.",
  "tone": ["whimsical", "eerie", "kind"],
  "visibleFragment": "The brass dryer door opened onto a hallway of blue moss.",
  "allowedContribution": {
    "minWords": 30,
    "maxWords": 250,
    "format": "scene-beat"
  },
  "publicArtifacts": [],
  "safetyBoundaries": ["no real-world actions", "no private data", "no hate or sexual content"]
}
```

The player should not receive hidden branch history, hidden turns, private participant notes, unmerged world facts, moderation notes, or pending rewards.

## Contribution rules

A player contribution may:

- continue from the visible fragment
- introduce one or more story events
- introduce a character, object, location detail, or mystery
- shift tone within the allowed scenario palette
- end with a hook for the next player

A player contribution may not:

- rewrite or delete accepted prior turns
- declare another real user's intent or identity outside the fiction
- reveal hidden turns that the actor could not see
- perform real-world actions, publishing, spending, DNS, secrets, auth, or deployment changes
- write to Todos, roadmaps, profile inventory, or public pages
- inject instructions to change the system prompt, persistence rules, or safety boundaries

The contribution text is user-authored content. If a bot helps polish it, preserve the original and store the transformed version separately or with explicit metadata.

## Mutation permissions

Each turn can propose three types of changes: story text, world facts, and reusable objects. They are not equally trusted.

### Always allowed after validation

- append accepted contribution text to the session turn log
- increment turn index
- advance current actor pointer
- update the latest visible fragment
- append a compact turn summary
- add temporary story flags

### Allowed with server normalization

- introduce a temporary character label
- introduce a temporary location label
- add a temporary item or clue
- add an unresolved mystery
- mark a tone or theme tag as active

### Disallowed in MVP

- permanent profile rewards or inventory changes
- public publishing
- task queue or roadmap write-back
- edits to existing Characters, Dreams, Scenarios, Bots, or Rewards
- real external calls
- billing, DNS, secrets, deployments, auth, or permission changes

Future tasks can define how temporary objects graduate into reusable profile artifacts. Until then, Exquisite Corpse outputs stay inside the session.

## Story merging rules

The canonical story is an append-only ordered list of accepted turns. The server may also maintain summaries and extracted facts, but those are derived views.

Merge policy:

- append the new contribution as the next immutable `StoryTurn`
- generate or accept a compact summary for the turn
- extract candidate facts into a `pendingFacts` list
- merge only non-conflicting facts into public session state
- keep conflicting facts as story tension unless they break safety or coherence

Contradiction is not automatically an error. In Exquisite Corpse, contradiction can be texture. The system should only reject contradictions that break the session contract, such as killing another player's character when the mode forbids it or revealing hidden text the player could not know.

## Character element merging

Temporary characters introduced during play should start as session-scoped artifacts, not permanent `Character` records.

Character merge fields:

- display name or label
- introducedByTurnId
- short description
- current visibility: hidden, public, revealed-after-lock
- relationship to existing player characters, if any
- continuity notes

Rules:

- a player may introduce a new temporary character if session settings allow it
- a player may add surface details to an existing temporary character
- a player may not overwrite another participant's player character identity
- promotion to a real reusable `Character` requires a later gated flow

## World and item element merging

Locations, items, clues, and world facts follow the same temporary-first principle.

World element fields:

- type: `LOCATION`, `ITEM`, `CLUE`, `FACTION`, `RULE`, or `MYSTERY`
- label
- description
- introducedByTurnId
- visibility
- status: `ACTIVE`, `RESOLVED`, `CONTRADICTED`, or `RETIRED`

Rules:

- new elements are session-scoped by default
- elements can be referenced by later turns if visible
- hidden elements should not be included in a player's visible packet until revealed
- permanent Dream/Scenario/Reward creation is out of scope for MVP

## Bot assistance

A host Bot may help in bounded ways:

- generate the opening premise from a Scenario
- summarize accepted turns
- extract candidate facts
- flag safety or continuity issues
- produce a final stitched reading after the session ends

The Bot should not secretly replace a player's contribution unless the UI explicitly labels it as an assisted rewrite. Even then, store attribution clearly. The vibe should be collaborative, not "the robot ate my homework and wore my hat."

## Safety and moderation

Before accepting a contribution, validate:

- actor permission and turn ownership
- length and format limits
- content boundaries from the session safety profile
- no private data requests or disclosures
- no attempts to mutate real tasks, accounts, deployments, billing, secrets, or permissions
- no instructions that override system or persistence rules
- no direct harassment of real participants

If validation fails, return a friendly rejection with the reason category and let the player revise. Do not advance the turn pointer.

Suggested rejection categories:

- `TOO_LONG`
- `OUT_OF_BOUNDS`
- `UNSAFE_CONTENT`
- `INVALID_MUTATION`
- `TURN_NOT_OWNED`
- `SESSION_LOCKED`

## Persistence shape

Suggested app-owned records or equivalent structured metadata:

```json
{
  "StorySession": {
    "id": "session-id",
    "mode": "EXQUISITE_CORPSE",
    "status": "ACTIVE",
    "visibilityMode": "LAST_FRAGMENT_ONLY",
    "turnOrder": ["user-1", "user-2"],
    "currentActorId": "user-2",
    "turnIndex": 4,
    "currentState": {
      "latestVisibleFragment": "...",
      "publicSummary": "...",
      "temporaryCharacters": [],
      "temporaryWorldElements": [],
      "flags": []
    }
  },
  "StoryTurn": {
    "id": "turn-id",
    "sessionId": "session-id",
    "actorId": "user-id",
    "turnIndex": 4,
    "visiblePacketHash": "hash-of-context-shown",
    "rawContribution": "player text",
    "acceptedText": "stored text",
    "summary": "one-sentence summary",
    "statePatch": {},
    "createdAt": "iso-date"
  }
}
```

`visiblePacketHash` is useful later for debugging fairness: it proves which bounded context the player received without storing duplicate hidden blobs everywhere.

## Completion and reveal

A session can complete when:

- fixed turn count is reached
- every participant has taken a configured number of turns
- owner ends the session
- moderation pauses or locks the session

On completion, the system may produce:

- full story reveal
- stitched reading with light formatting
- participant attribution by turn
- list of temporary artifacts introduced
- candidate rewards or reusable objects for a later gated review

No completed story should be published publicly without an explicit future approval flow.

## Error handling

Use recoverable states:

- `PAUSED_NEEDS_REPAIR` when state or linked anchors are missing
- `TURN_REJECTED` when validation fails
- `SESSION_LOCKED` when another request is resolving the turn
- `VISIBILITY_PACKET_FAILED` when the server cannot safely build bounded context
- `COMPLETED_PENDING_REVEAL` when play is done but the stitched view is still generating

The client should preserve the user's draft when possible so a validation failure does not feel like feeding a paragraph to a paper shredder.

## Verification checklist for implementation

When implemented later, verify:

- a player only receives the configured visible packet, not the full hidden story
- turn order is server-owned and cannot be advanced by the client
- duplicate submissions do not create duplicate turns
- contributions append to an immutable log
- hidden facts are not leaked through summaries or public artifacts
- temporary characters and world elements stay session-scoped
- invalid mutations are rejected without advancing the turn
- completed sessions can reveal a stitched story without publishing it
- no Todos, roadmaps, profile inventory, billing, DNS, secrets, deploys, or public pages are mutated

## Follow-up tasks suggested

- Define the exact `StoryTurn` persistence model and storage location.
- Add UX rules for the full-story reveal and participant attribution.
- Specify how session-scoped characters, locations, and items can later graduate into reusable profile artifacts.
