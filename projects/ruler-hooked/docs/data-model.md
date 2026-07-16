# The Ruler is Hooked — Play-Loop Data Model & Save System

date: 2026-07-16
task: ruler-hooked/t-004
status: spec complete (no code; design doc only)
related: docs/compositing.md (t-005 — region states this model stores),
docs/decks.md (t-006 — event/choice records this model logs),
docs/unreal-migration.md (t-009 — why this is data-first),
DESIGN-BRIEF.md (core loop, offline rule, time pillar, multiple saves)

## 0. Principles (the non-negotiables this model serves)

1. **Offline at runtime.** The shipped game runs with no network and no live LLM.
   All gameplay state lives **client-side**; the backend is *only* for optional
   account sync of finished saves, never for anything gameplay-critical. A player
   with zero connectivity plays the whole game.
2. **Content is data, not code.** Regions, decks, characters, rewards, and endings
   are declarative data files bundled with the game. Adding content is a data drop
   (a content task), never a code change. This is what lets the content survive the
   Unreal migration (t-009).
3. **No clock, ever** (Silas time pillar, 2026-07-05). State advances by **turns**
   (player actions), never wall-clock time. Time-of-day is a cosmetic cycle
   position computed from `turnCount`. Nothing expires, nothing is missable, no
   choice is time-gated. A save is identical after a month untouched.
4. **Multiple named saves** from the start, each fully independent.
5. **Deterministic replay.** A save plus its RNG `seed` reproduces the exact same
   sequence — required for save/load parity and for the pure-function compositor
   (t-005 §3).

## 1. Grounding in the kind_robots vocabulary

This is an offline game, so its authoritative state is a **local save document**,
not DB rows. But the vocabulary deliberately mirrors kind_robots so a save can
sync to the backend and reuse existing models. Mapping (verified against
`kind_robots/prisma/schema.prisma`, 2026-07-16):

| game concept          | kind_robots analog                          | notes |
|-----------------------|---------------------------------------------|-------|
| a playthrough/save    | **LifeRun** (`status`, `seed`, `currentChapter`, `statsSnapshot`, `dreamId`, `characterId`) | our `RunSave` is the offline superset |
| per-decision log      | **LifeChoice** (`prompt`, `choiceText`, `resultText`, `effects` JSON) | our `choiceLog` entries |
| normalized run stats  | **LifeStat** (`[lifeRunId,key]` unique, `value Int`) | our kingdom sliders + counters |
| run status enum       | **LifeRunStatus** `ACTIVE \| COMPLETE \| ABANDONED` | reused verbatim |
| a game character      | **Character** (`name, alignment, class, species, drive, quirks, personality`, six `Rarity` stats, `slug`) | reuse existing where they fit (t-006) |
| a reward (skill/item) | **Reward** (`rewardType`, `rarity`, `effect`, `name`, `slug`) | `RewardType` enum already has `SKILL, ITEM, POWER, PET, MAGIC, FAVOR` |
| the game world itself | **Dream** (`narratorId`, `Characters`, `Rewards`, `Scenarios`) | ruler-hooked as a Dream world; `conductorSlug` parity via t-003 |
| roadmap milestones    | **Conductor** (not the DB)                  | per the Project/Dream/Facet split |

Conventions we inherit so a sync layer is trivial: **camelCase** scalar keys,
enum values in **UPPER_SNAKE_CASE**, and **JSON stored as stringified text**
(kind_robots has no native `Json` column — `statsSnapshot`, `effects`, etc. are
`String @db.LongText`). Our save serializes to exactly that shape.

## 2. Storage & save slots

### 2.1 Where saves live (offline-first)

- **Primary store:** browser `IndexedDB` (web PoC) — structured, roomy, survives
  reloads, no server. One object store `saves` keyed by `saveId`, one `meta` store
  for the slot index and player settings. A packaged app (later) swaps IndexedDB
  for a local file/SQLite behind the same `SaveStore` interface — the format is
  identical, only the adapter changes.
- **Never** localStorage for save bodies (size + sync-write cost); localStorage
  only holds the tiny "last active slot" pointer for fast boot.
- **Optional cloud sync (soft, non-critical):** a logged-in kind_robots user may
  push a `RunSave` to the backend as a **LifeRun** row (with `statsSnapshot` = the
  serialized kingdom state) for cross-device continuity. Sync is a whole-document
  push/pull with last-writer-wins per slot; the game is **fully playable if it
  never syncs**. No partial/gameplay-critical server round-trips.

### 2.2 Slots

Multiple **named** saves. The slot index (`SaveIndex`) is a small list the
title/continue screen reads without loading full save bodies:

```jsonc
// SaveIndex (in the `meta` store)
{
  "schemaVersion": 3,
  "activeSaveId": "sv_ab12cd",
  "slots": [
    {
      "saveId": "sv_ab12cd",
      "name": "Queen Mo's lazy reign",     // player-named, renameable
      "rulerName": "Mo",
      "createdAt": "2026-07-16T10:00:00Z",  // display metadata only — NOT game time
      "updatedAt": "2026-07-16T10:42:00Z",
      "turnCount": 37,
      "status": "ACTIVE",                   // LifeRunStatus
      "thumbRegionSummary": { "treeline": "tended", "far_shore": "farmed" },
      "kingdomHealth": { "nature": 61, "prosperity": 40, "joy": 72 } // for slot art
    }
    // ... more slots, no fixed cap; UI paginates
  ]
}
```

- **Autosave** writes the active slot after every resolved choice/turn (a save is
  cheap and deterministic). A **manual "save as new slot"** clones the active save
  under a new `saveId` (branching a run is a feature, not a bug — it's offline and
  cheap).
- Timestamps in the index are **real-world display metadata** (so the player can
  find "the one from last night"). They are **never read by game logic** — this
  preserves the no-clock pillar. Game progression uses `turnCount` only.

## 3. The RunSave document (the core state)

One self-contained JSON document per slot. Everything needed to render the exact
play screen (t-005) and resume the loop lives here.

```jsonc
{
  "schemaVersion": 3,
  "saveId": "sv_ab12cd",
  "name": "Queen Mo's lazy reign",
  "dreamSlug": "ruler-hooked",        // the world this save belongs to
  "contentVersion": "2026.07",        // which bundled content set authored it (see §7)
  "seed": "mo-4820-lakeside",         // deterministic RNG seed (LifeRun.seed)
  "status": "ACTIVE",                 // LifeRunStatus: ACTIVE|COMPLETE|ABANDONED

  "ruler": {                          // the player-character
    "name": "Mo",
    "honorific": "Queen",             // King|Queen|other — cosmetic label
    "characterSlug": "ruler-mo",      // optional link to a Character record (t-006)
    "cosmetics": { "outfit": "fishing_casual", "crownTilt": true }
  },

  "turnCount": 37,                    // the ONLY progression counter (no clock)
  "cyclePosition": 2,                 // derived-but-cached time-of-day index (t-005 §4)

  "kingdomHealth": {                  // the sliders — 0..100 continuous axes (§4)
    "nature": 61,
    "prosperity": 40,
    "treasury": 55,
    "joy": 72,
    "order": 48
  },

  "counters": {                       // discrete tallies, LifeStat-style key/value
    "fishCaught": 14,
    "cardsResolved": 9,
    "warlockFavors": 1,
    "druidFavors": 2
  },

  "regionStates": {                   // committed visual state per region (t-005 §2)
    "treeline": "tended",
    "far_shore": "farmed",
    "village_edge": "township",
    "castle_grounds": "flourishing",
    "lake": "clear"
  },
  "regionOverrides": {                // event-pinned states, precede slider ramps (t-005 §3)
    "far_shore": "farmed"
  },

  "deckState": {                      // event/card engine state (detail in t-006)
    "seenCardIds": ["warlock-druid-north", "child-elopes-1"],
    "activeArcs": {                   // multi-card narrative arcs mid-progress
      "child-elopes": { "step": 2, "flags": { "blessedMatch": false } }
    },
    "cooldowns": { "tax-season": 3 },   // measured in TURNS, never time
    "drawBag": ["harvest-festival", "sunken-crown", "rival-angler"] // shuffled by seed
  },

  "inventory": {                      // Rewards earned — mirrors kind_robots Reward
    "skills": [                       // rewardType: SKILL
      { "slug": "patient-caster", "rarity": "UNCOMMON",
        "effect": "Fishing minigame difficulty eased by one step." }
    ],
    "items": [                        // rewardType: ITEM
      { "slug": "gilded-lure", "rarity": "RARE",
        "effect": "Unlocks the legendary-fish table at the far shore." }
    ]
  },

  "choiceLog": [                      // append-only, mirrors LifeChoice rows
    {
      "turn": 31,
      "cardId": "warlock-druid-north",
      "prompt": "The north woods: develop or preserve?",
      "choiceText": "Let the druids keep it.",
      "effects": { "nature": +12, "prosperity": -6,
                   "regionOverride": { "far_shore": "pristine" } },
      "resultText": "The druids plant a grove in your honor."
    }
  ],

  "flags": {                          // arbitrary world flags set by choices/arcs
    "metWarlock": true,
    "childEngaged": false
  },

  "endingKey": null,                  // set when status → COMPLETE (t-006 endings)
  "createdAt": "2026-07-16T10:00:00Z",
  "updatedAt": "2026-07-16T10:42:00Z" // display metadata only, not game logic
}
```

### 3.1 Why this shape

- **Self-contained & serializable:** the whole document round-trips to a single
  JSON string → drops straight into `LifeRun.statsSnapshot` (LongText) for sync.
- **Deterministic:** `seed` + `choiceLog` fully reconstruct the run; `drawBag` and
  RNG draws are seeded, so replays and reloads match (compositor is pure, t-005).
- **Append-only history:** `choiceLog` is never mutated, only appended — this is
  the audit trail *and* the basis for any future "rewind one choice" feature
  (mirrors the append-only `ModelBuildRevision` pattern in kind_robots).

## 4. Kingdom-health sliders (the axes)

The health of the kingdom is a small set of continuous **axes**, each `0..100`,
stored in `kingdomHealth`. They are the primary state that choices move and that
drives region art (t-005 §3). PoC axis set (tunable during playtest):

| axis         | 0 pole                     | 100 pole                    | drives (region ramp) |
|--------------|----------------------------|-----------------------------|----------------------|
| `nature`     | paved / industrial         | wild / thriving             | `treeline`, `far_shore` |
| `prosperity` | struggling                 | booming                     | `village_edge` |
| `treasury`   | broke                      | overflowing                 | `castle_grounds` (partial) |
| `joy`        | miserable subjects         | delighted subjects          | crowd/`fx` flavor, endings |
| `order`      | chaos                      | rigid                       | event availability, endings |

Design rules:
- **No axis is "good" or "bad."** High `order` reads as tyranny as easily as
  safety; the warlock/druid choice trades `nature` against `prosperity`. This is
  the Prime-Monster "honestly-evil, real-weight" register from the brief — sliders
  encode trade-offs, not a score.
- **Clamped, never terminal by clock.** An axis hitting 0 or 100 may unlock
  distinct events/endings (t-006) but never "fails" the run on a timer.
- **`counters`** are discrete tallies (fish caught, favors granted) — kept separate
  from the continuous axes so decks can trigger on either ("after 3 warlock
  favors…", "when nature < 20…").
- One save's sliders are **independent** of every other save's (offline, per-slot).

## 5. The turn / play loop (state transitions)

A **turn** is one iteration of the core loop. `turnCount` increments once per turn;
nothing else advances progression.

```
LOOP (one turn):
  1. FISH beat        — player fishes (minigame or one-tap). May grant counters,
                        occasionally a Reward. Advances cyclePosition cosmetically.
  2. MAYBE INTERRUPT  — deck engine (t-006) decides if a card fires this turn,
                        using seed + deckState (cooldowns/flags/slider triggers).
                        No card is guaranteed and none can EXPIRE — a skipped card
                        returns to the bag; nothing is missable (time pillar).
  3. CHOICE           — if a card fired, player picks an option.
  4. APPLY EFFECTS    — choice.effects mutate kingdomHealth / counters / flags /
                        regionOverrides; append a choiceLog entry; advance arcs.
  5. RESOLVE SCENE    — compositor recomputes regionStates from sliders+overrides
                        (t-005 §3) and crossfades changed bands.
  6. AUTOSAVE         — serialize RunSave to the active slot.
GOTO LOOP
```

- The loop has **no fail state and no timer.** The player can stop between any two
  steps; the autosave at step 6 (and a pre-choice checkpoint) means closing the tab
  mid-decision loses nothing.
- `status` flips to `COMPLETE` only when an **ending** condition is met (a chosen
  finale arc, not a clock); `endingKey` records which. A completed run is kept
  (readable, replayable), never deleted. `ABANDONED` is a player-initiated
  soft-delete that keeps the slot recoverable.

## 6. Content bundles (the read-only side)

The mutable save (§3) references **immutable content** shipped with the game.
Content is declarative data, loaded read-only at boot:

```
content/<contentVersion>/
  regions.yaml     # region/state/time manifest (t-005 §2)
  decks/*.yaml     # event & arc cards (t-006)
  characters/*.yaml# game Characters (mirror kind_robots Character fields; t-006)
  rewards/*.yaml   # Rewards (mirror kind_robots Reward: rewardType/rarity/effect)
  endings.yaml     # ending catalog (mirror LifeEnding: outcomeKey/victoryType)
  assets/          # the layer WebPs named per t-005 §4.3
```

- A save stores `contentVersion` + `seenCardIds`/slugs, **not** copies of the
  content. This keeps saves tiny and lets content be patched (§7).
- Characters and Rewards in content use the exact kind_robots field names
  (`alignment`, `drive`, `quirks`, `rewardType`, `rarity`, `effect`, `slug`) so the
  same authoring can populate the DB (t-006) and the offline bundle from one source.

## 7. Versioning & migration (saves must survive updates)

- **`schemaVersion`** (on `SaveIndex` and every `RunSave`) gates a forward-only
  migration ladder: `migrate(save)` applies ordered steps `v_n → v_n+1` on load.
  New optional fields default in; removed fields are dropped defensively. Never
  break an existing save on update — this is a keep-forever, put-it-down-for-months
  game.
- **`contentVersion`** decouples save data from content data. A content patch that
  *adds* cards/regions/rewards is safe for old saves (new content simply becomes
  drawable). A patch that *renames or removes* a referenced slug must ship an alias
  map (mirroring kind_robots' `FacetAlias` canonical-lookup pattern) so old
  `seenCardIds`/`regionStates`/inventory slugs still resolve. Region/reward/card
  removal is a content decision that always provides a fallback, never an orphan.
- **Determinism across versions:** a save's `seed` + `choiceLog` reconstruct its
  history even if the live content changed, because the log records the concrete
  `effects` applied at the time, not just a card id.

## 8. What the build (t-007) implements against this

- A `SaveStore` interface with an IndexedDB adapter (web) and the same interface
  ready for a file/SQLite adapter (packaged app) — format identical.
- `RunSave` (de)serialize + the `schemaVersion` migration ladder.
- A pure `applyEffects(save, choice) -> save` reducer (no I/O, deterministic) that
  the loop (§5 step 4) and any replay share.
- The slot UI reading `SaveIndex` for continue/new/rename/branch/delete.
- Optional: a thin `syncLifeRun()` that serializes a `RunSave` into a kind_robots
  **LifeRun** row for account continuity — strictly non-gameplay-critical.

## 9. Open questions for the build

- Final **axis list** and 0/100 semantics after playtest (§4 is the starting set).
- Whether `counters` and `kingdomHealth` unify into one LifeStat-style key/value
  map at the storage layer (cleaner sync) vs. stay split for readability
  (recommended: split in the doc, flatten only at the sync boundary).
- Autosave cadence vs. an explicit pre-choice checkpoint (recommend both).
- None of these block t-005/t-006 — they are storage-layer tuning, not format
  changes.
