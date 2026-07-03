# Storymaker Profile Artifact Mapping

Storymaker sessions should feel playful in the moment, but the best outputs should also become reusable profile objects. This document defines which rewards, locations, items, characters, and story fragments can persist beyond one session, how they unlock, and how future sessions can remix them without turning every improvised detail into permanent clutter.

## Goals

- Preserve memorable session outputs as reusable player-facing artifacts.
- Keep the existing Kind Robots object families meaningful: Characters, Dreams, Rewards, Scenarios, Bots, and Chats.
- Separate ephemeral session state from profile-level canon.
- Make rarity and unlock rules clear enough for later UI/API implementation.
- Support genre remixes without duplicating the same object endlessly.

## Artifact lifecycle

Every generated or player-authored object moves through four possible states:

1. **Ephemeral** — exists only inside the current StorySession turn log.
2. **Candidate** — highlighted by the narrator or player as worth keeping.
3. **Unlocked** — copied or linked into the player's profile inventory/library.
4. **Reusable** — available as a seed, companion, location, item, reward, or cameo in future sessions.

Default rule: new session details stay ephemeral unless the turn lifecycle explicitly marks them as a candidate. This avoids profile spam and keeps the library curated.

## What becomes reusable

### Rewards

Rewards are the strongest fit for direct profile persistence. A Storymaker reward can become a profile object when it represents a meaningful achievement, item, title, badge, or cosmetic unlock.

Recommended persisted fields:

- `name` — player-facing artifact name.
- `rewardType` — badge, title, item, companion, cosmetic, lore, or meta unlock.
- `rarity` — common, uncommon, rare, epic, legendary, mythic.
- `sourceSessionId` — link back to the originating session.
- `sourceTurnId` — optional turn where the artifact was earned.
- `genreTags` — tags used for future remixing.
- `description` — short flavorful description.
- `mechanicalEffect` — optional, only if later systems need stat or choice modifiers.

Unlock rules:

- A normal branch choice can unlock common or uncommon rewards.
- A custom input that meaningfully changes the scene can unlock uncommon or rare rewards.
- A costly choice, clever callback, or completed mini-arc can unlock rare or epic rewards.
- Legendary or mythic rewards should require explicit narrator selection, milestone completion, or human-authored scenario rules.

Do not let random generation mint high-rarity permanent profile objects without a clear story reason. Loot confetti is cute until the database becomes a raccoon nest.

### Locations

Locations should usually persist as Dreams with a location-like type or tag, not as Rewards. A session location becomes reusable when it is named, revisited, materially changed, or chosen as a future setting seed.

Candidate triggers:

- The player names a place.
- The story returns to the place across multiple turns.
- The place gains a distinct rule, mood, NPC, artifact, or unresolved hook.
- The player explicitly saves it.

Recommended persisted fields:

- `slug` — stable generated slug, namespaced if needed.
- `title` — display name.
- `dreamType` — LOCATION if available, otherwise Dream with `genreTags` and `source: storymaker` metadata.
- `vibe` — short mood phrase.
- `description` — 2-4 sentence place summary.
- `sourceSessionId` and `sourceTurnId`.
- `reuseMode` — setting, cameo, memory, obstacle, sanctuary.

Future-session reuse:

- **Setting**: the location anchors a new session.
- **Cameo**: it appears as a brief callback.
- **Memory**: it influences narrator flavor but does not appear physically.
- **Obstacle**: an unresolved danger returns.
- **Sanctuary**: a safe hub or reward space.

### Items

Items can persist as Rewards when they are collectible or achievement-like. They should only become standalone profile artifacts if later schema adds an Item model. Until then, model them as Reward objects with `rewardType: item`.

Item persistence tiers:

- **Session item** — temporary inventory used only during the current session.
- **Keepsake** — flavor-only reward, reusable as a callback.
- **Tool** — can influence later branch options.
- **Relic** — rare item with scenario-level importance.

Recommended rules:

- Consumables stay session-scoped by default.
- Keepsakes persist after emotionally meaningful scenes.
- Tools persist when earned through a deliberate choice or challenge.
- Relics persist only through scenario milestones or narrator-approved events.

### Characters

Characters should persist only when they are distinct enough to survive outside the scene. Most NPCs stay ephemeral. Recurring companions, rivals, mentors, and player-created figures can become Character records or character-like profile artifacts.

Candidate triggers:

- The character receives a name and role.
- The player forms a bond, rivalry, pact, or debt with them.
- The character appears in more than one turn.
- The character changes the branch state.
- The player chooses to save them.

Recommended persisted fields:

- `name`.
- `role` — companion, rival, mentor, merchant, guide, antagonist, cameo.
- `rarity` — based on narrative importance, not power level.
- `originSessionId` and `originTurnId`.
- `genreTags`.
- `relationshipState` — ally, wary, indebted, bonded, unresolved, hostile.
- `summary` — what future sessions need to know.

Future-session reuse:

- Companions may appear in the session setup picker.
- Rivals and antagonists can return as complications.
- Mentors can offer hints or framing.
- Cameo characters should be lightweight and optional.

### Story fragments and titles

Some outputs are not objects but still deserve profile-level persistence: titles, prophecies, vows, scars, catchphrases, faction reputations, or unresolved mysteries. These should be stored as lightweight Reward or lore entries until there is a dedicated memory model.

Examples:

- `Title: Friend of the Rainlit Library`
- `Reputation: The Clockwork Foxes trust you`
- `Mystery: Who moved the moon behind the glass mountain?`
- `Vow: Return the silver seed before winter`

These entries are excellent seeds for future Serendipity or Storymaker sessions.

## Rarity model

Rarity should communicate narrative weight, not just numerical value.

| Rarity | Meaning | Typical source |
| --- | --- | --- |
| common | Fun callback or small keepsake | ordinary branch choice |
| uncommon | Named detail with future flavor | player-authored custom input |
| rare | Meaningful relationship, tool, or location | clever choice or mini-arc completion |
| epic | Major session outcome | scenario milestone or costly decision |
| legendary | Campaign-defining artifact or figure | finale, special challenge, or human-authored scenario |
| mythic | Account-level signature artifact | rare curated event; never routine auto-mint |

Rarity upgrades should be possible when an existing artifact reappears and gains importance. Example: a common `Bent Brass Key` can become rare if it later unlocks the sleeping observatory.

## Unlock rules

A session can unlock profile artifacts through these mechanisms:

1. **Narrator award** — the engine grants a reward after a milestone or dramatic beat.
2. **Player save** — the player marks a character, location, or item as worth keeping.
3. **Scenario rule** — a designed Scenario declares specific unlocks.
4. **Completion reward** — finishing a session grants a title, badge, or summary artifact.
5. **Human-curated import** — Silas or an admin promotes an especially good generated object.

MVP recommendation: support narrator award and player save first. Scenario rules and human-curated imports can come later.

## Genre remixes

Reusable artifacts should not be locked to one genre unless the artifact explicitly requires it. Store genre tags and remix instructions separately.

Remix modes:

- **Literal** — the artifact returns unchanged.
- **Reskinned** — same identity, genre-appropriate presentation.
- **Echo** — a symbolic version appears.
- **Legacy** — consequences of the artifact appear, not the artifact itself.
- **Forbidden** — artifact should not be reused outside its source genre.

Examples:

- A cozy fantasy `Lantern of Small Mercies` can become a cyberpunk `Mercy Beacon` in reskinned mode.
- A noir detective rival can appear in a space opera as an echo: a transmission with the same catchphrase.
- A mythic one-of-one finale reward may be forbidden outside the source scenario.

## Future-session reuse contract

When starting a new Storymaker session, the engine can offer profile artifacts as optional ingredients:

- saved locations as settings;
- saved characters as companions, rivals, or cameos;
- saved item rewards as starting inventory or callbacks;
- titles and lore as narrator flavor;
- unresolved mysteries as scenario hooks.

The session seed should record which artifacts were imported so the engine can avoid contradiction and write back changes responsibly.

Suggested seed shape:

```json
{
  "mode": "guided-adventure",
  "genreTags": ["cozy-fantasy", "mystery"],
  "importedArtifacts": [
    {
      "id": "reward_123",
      "kind": "item",
      "reuseMode": "tool",
      "remixMode": "literal"
    },
    {
      "id": "dream_456",
      "kind": "location",
      "reuseMode": "setting",
      "remixMode": "reskinned"
    }
  ]
}
```

## Boundaries and safety

- Do not mutate existing profile artifacts automatically without recording a session event.
- Do not delete profile artifacts from a session; retire/archive should be a separate user action.
- Do not overwrite player-authored names without confirmation.
- Do not persist private or sensitive user text into reusable public-facing objects by default.
- Do not mint outward-facing marketplace or social content from Storymaker artifacts without a separate human gate.

## MVP implementation path

1. Add session-scoped candidate marking in the Storymaker state model.
2. Let the player save a candidate as a Reward-backed profile artifact.
3. Support `rewardType: item`, `rewardType: title`, and `rewardType: lore` first.
4. Add saved Characters and LOCATION Dreams after the save flow is stable.
5. Add future-session seed import UI once there are enough saved artifacts to reuse.

## Open questions for implementation

- Should saved locations always become Dreams, or should Storymaker keep an app-owned saved-location table first?
- Should character persistence require a full Character record immediately, or start with lightweight reward/lore entries?
- How much control should the player have over rarity, versus the narrator assigning it?
- Should imported artifacts be consumed, changed, or duplicated when remixed into a new genre?

The safe default is conservative persistence: save fewer things, make them feel special, and let the player promote what matters.