# Storymaker Session Data Model

Generated: 2026-06-30
Task: storymaker/t-001
Informed by: docs/kr-model-audit.md

---

## Purpose

Specify the Storymaker session data model: participants, narrator Bot, Scenario variables, current narrative state, inventory changes, branch history, turn ownership, and persistence between turns. This document is for Silas to review before backend implementation begins.

---

## What Exists in kind_robots (Ready to Use)

From `kr-model-audit.md`:

- **Bot**: narrator system (narrativeVoice, forgeIntro, botIntro, NarratorThread[])
- **Character**: 6 Rarity stats, level/experience, Rewards[], Chats[]
- **Scenario**: intros, cast JSON, locations, genres, difficulty, ScenarioOutputType
- **Chat**: originId threading (session grouping), botId + characterId + userId
- **Reward**: rarity, effect, collection, Character ownership via junction

None of these models need changes for MVP. The session layer sits on top of them.

---

## New Models Required (Must Pitch to kind_robots Backend)

### 1. StorySession

Represents a single play session from start to finish.

```
StorySession {
  id              Int       PK autoincrement
  createdAt       DateTime
  updatedAt       DateTime
  startedAt       DateTime  // when the first turn was taken
  endedAt         DateTime? // null = still active
  
  // Identity
  mode            Enum      GUIDED_ADVENTURE | EXQUISITE_CORPSE
  status          Enum      ACTIVE | PAUSED | COMPLETE | ABANDONED
  title           String?   // human-readable session name (optional)

  // Narrator + setting
  botId           Int       FK → Bot (the narrator)
  scenarioId      Int       FK → Scenario (the starting world)

  // Participants (JSON array of userIds or characterIds)
  participantUserIds    Json   // [userId, ...]
  participantCharIds    Json   // [characterId, ...] — parallel array to userIds
  
  // Turn tracking
  currentTurnUserId   Int?  // whose turn it is right now
  turnCount           Int   @default(0)

  // Session state (freeform JSON for scenario variables)
  stateSnapshot   Json?   // { locationId, flags: {...}, inventoryChanges: [...] }

  // Chat thread anchor
  originId        Int?    // shared originId for all Chat messages in this session

  // Relations
  Bot             Bot
  Scenario        Scenario
  TurnChoices     TurnChoice[]  // branch log
}
```

**Notes:**
- `stateSnapshot` is freeform JSON so scenarios can store arbitrary state without schema migrations (location flags, quest vars, counter values, etc.)
- `originId` links back to the Chat model's existing thread system — no new message storage needed
- `participantUserIds` / `participantCharIds` are JSON arrays rather than junction tables at MVP to avoid adding two more tables; can normalize later if needed

---

### 2. TurnChoice

Logs branch options and the player's selection at each turn.

```
TurnChoice {
  id              Int       PK autoincrement
  createdAt       DateTime

  // Linkage
  sessionId       Int       FK → StorySession
  chatId          Int       FK → Chat (the message that presented the options)
  userId          Int?      FK → User (who made the choice)
  characterId     Int?      FK → Character (which character made the choice)

  // Options
  optionsOffered  Json      // [{ id: "A", text: "...", statCost?: { might: 1 } }, ...]
  optionChosen    String?   // id of the chosen option, or null if custom input used
  customInput     String?   // free-text input if player chose "other"

  // Outcome
  outcomeText     String?   @db.Text  // what happened after this choice
  rewardsGranted  Json?     // [{ rewardId: X, quantity: 1 }, ...]
  statChanges     Json?     // { might: +1, luck: -1, ... } applied this turn

  // Relations
  StorySession    StorySession
  Chat            Chat
}
```

**Notes:**
- `optionsOffered` stores the full menu the narrator presented, not just what was chosen — this lets sessions be replayed or audited
- `customInput` handles the "none of the above, I do this instead" case that Guided Adventure must support
- `rewardsGranted` and `statChanges` record what was earned/consumed this turn as a log; actual Character stat and Reward records are still updated on their own models

---

## Session Lifecycle

```
created → ACTIVE → PAUSED ←→ ACTIVE → COMPLETE
                               ↓
                           ABANDONED
```

**State transitions:**
- `ACTIVE`: turns can be taken
- `PAUSED`: async play; no turn timer; resumes when the current player returns
- `COMPLETE`: all scenario objectives met or the narrator ended the session; stateSnapshot frozen
- `ABANDONED`: player left without completing; orphaned after 30 days

---

## Turn Lifecycle (Guided Adventure)

1. Narrator Bot generates narrative text + 2–4 branch options (+ optional "custom" slot)
2. Options are stored in TurnChoice.optionsOffered before the player responds
3. Player selects an option (or provides custom input)
4. Relay persists TurnChoice with optionChosen/customInput
5. Stat check (if any): compare Character stat Rarity against difficulty, apply luck modifier
6. Narrator Bot generates the consequence + next scene
7. outcomeText, rewardsGranted, statChanges written to TurnChoice
8. StorySession.stateSnapshot updated (location, flags, counters)
9. StorySession.turnCount++, currentTurnUserId advances (for multi-player)

---

## Turn Lifecycle (Exquisite Corpse)

1. Current author's turn begins; they see only their "window" of the story (configurable: last N sentences)
2. They write a continuation; it is saved as a Chat message (botId=null, userId=author)
3. TurnChoice records this as a "contribution" with optionsOffered=[] and customInput=their text
4. StorySession.currentTurnUserId advances to the next participant
5. StorySession.stateSnapshot tracks word/sentence counts and contribution order
6. Session COMPLETE when all N rounds are filled; full story is assembled from Chat.originId thread

---

## Inventory and Rewards

- **New rewards earned during a session**: Create CharacterToReward relation entries on the Character
- **Consumed items**: Remove CharacterToReward relation entries (or add a `consumed: boolean` to the junction if needed)
- **Session-scoped inventory**: tracked in TurnChoice.rewardsGranted per turn and in StorySession.stateSnapshot.inventoryChanges for a session total; this reconciles to the Character.Rewards relation at session end

**MVP approach:** Update Character.Rewards immediately when a reward is granted. No deferred batch; the session is authoritative in real time.

---

## Persistence Between Sessions

- The StorySession row keeps stateSnapshot; a character can rejoin a PAUSED session and pick up at the same location with the same flags
- Character stat and Reward changes from a completed session are permanent — they are written to the Character model during the session, not deferred
- TurnChoice log is the full audit trail — the entire session can be reconstructed from it

---

## Fields NOT Needed at MVP

| Gap | Reason to defer |
|---|---|
| `Character.activeSessionId` | Session layer tracks this; query `StorySession WHERE currentTurnUserId = X AND status = ACTIVE` |
| `Reward.quantity` | One relation record per reward copy at MVP; normalize later if inventory grows |
| `Bot.isStoryteller` flag | Filter by `botType` convention ("narrator") for now |
| Session-scoped Character stat snapshot | Character stats are mutated live; no snapshot needed at MVP |

---

## Summary

**Must pitch to kind_robots backend:**
1. `StorySession` model (status, mode, originId, stateSnapshot, participantIds, turn tracking)
2. `TurnChoice` model (optionsOffered, optionChosen, customInput, rewardsGranted, statChanges)

**Uses existing models as-is:**
- Bot, Character, Scenario, Chat, Reward — no schema changes

**Document feeds into:**
- storymaker/t-002 (Guided Adventure turn lifecycle spec)
- storymaker/t-003 (Exquisite Corpse collaboration rules)
- storymaker/t-004 (rewards and reusable artifacts spec)
