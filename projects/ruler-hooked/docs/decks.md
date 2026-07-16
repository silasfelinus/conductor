# The Ruler is Hooked — Event / Character Card Deck Format

date: 2026-07-16
task: ruler-hooked/t-006
status: spec complete (no code; design doc only)
related: docs/data-model.md (t-004 — deckState, choiceLog, sliders this reads/writes),
docs/compositing.md (t-005 — region effects choices apply),
docs/art-direction.md (t-008 — card & character art),
DESIGN-BRIEF.md (Prime Monster tone, replay variety, elope arc)

## 0. What this spec is

The kingdom interrupts the fishing with **cards**. A card is a slide: a bit of
narration, a character, and a set of **choices**, each of which moves kingdom
sliders, swaps region art, and advances the story. This doc defines the **data
format** for those cards and for the **decks/arcs** that group them, so that:

- **Adding an arc is a content task, not a code task** (a YAML drop, no engine
  change) — a hard requirement from the brief.
- **Different runs surface different characters and events** — replay variety is
  built into how cards are selected, not hand-scripted per run.
- Characters reuse the **kind_robots `Character` model** and rewards reuse the
  **`Reward` model** (verified against `kind_robots/prisma/schema.prisma`,
  2026-07-16), so one authoring source populates both the offline bundle and the DB.

Everything here is declarative data loaded read-only at boot (t-004 §6); the engine
that reads it is generic.

## 1. Vocabulary anchors (kind_robots parity)

| deck concept        | kind_robots model / enum                                    |
|---------------------|-------------------------------------------------------------|
| a character on a card | **Character** — `name, honorific, alignment, class, species, drive, quirks, personality, role, title, slug`, six `Rarity` stats (`charm, empathy, grace, luck, might, wits`) |
| a reward from a choice | **Reward** — `rewardType` (`SKILL\|ITEM\|POWER\|PET\|MAGIC\|FAVOR`), `rarity` (`Rarity`), `effect` (narrative hook), `name`, `slug` |
| the world the decks belong to | **Dream** (`ruler-hooked`) — `narratorId` (the narrator bot), `Characters`, `Rewards`, `Scenarios` |
| a decision record   | **LifeChoice** — `prompt, choiceText, resultText, effects` (JSON) — one per resolved choice (t-004 `choiceLog`) |
| an ending           | **LifeEnding** — `outcomeKey`, `victoryType` (`VICTORY\|FAILURE\|MIXED\|SECRET`) |

Cards **reference** characters and rewards by `slug`; they never inline a copy. A
card that features the warlock points at `character: warlock-vex`; the engine
resolves the slug against the bundled `characters/` set (or a synced DB Character).
This is what "reuse existing Characters where they fit" means in practice — a card
can name any existing `Character.slug`.

## 2. The card (atomic unit)

```yaml
# content/<version>/decks/kingdom-core.yaml  →  one entry in `cards:`
- id: warlock-druid-north           # unique, stable, referenced by seenCardIds
  deck: kingdom-core                # which deck it belongs to (see §4)
  kind: interrupt                   # interrupt | arc-step | ambient | finale
  weight: 3                         # relative draw weight within its pool (§5)
  once: false                       # if true, never redraws once seen this run

  # ---- who & what the player sees ----
  narratorId: dream                 # narrator bot voice (Dream.narratorId), optional
  characters: [warlock-vex, druid-sela]   # Character slugs featured on the slide
  title: "The North Woods Question"
  body: >
    Vex the warlock-developer unrolls blueprints across your tackle box.
    Across the clearing, Sela the druid just… waits, watering can in hand.
  art: card-warlock-druid-north     # art asset key (t-008); optional, falls back

  # ---- when it may fire ----
  trigger:                          # ALL conditions must hold (§3)
    minTurn: 3
    requires: { sliders: { nature: { gte: 30 } } }
    forbids: { flags: [northWoodsSettled] }
    cooldown: 6                     # turns before this card can redraw (never time)

  # ---- the choices ----
  choices:
    - id: develop
      text: "Let Vex build. Progress!"
      effects:                      # applied on pick (§6)
        sliders: { nature: -20, prosperity: +15, treasury: +8 }
        regionOverride: { far_shore: industrial, treeline: logged }
        flags: { set: [northWoodsSettled, metWarlock] }
        counters: { warlockFavors: +1 }
        grant: [ { reward: buildpermit-scroll } ]   # Reward slug (rewardType ITEM)
        arc: { start: warlock-patronage }           # may kick off an arc (§4)
      result: "Vex cackles and breaks ground before you finish your sentence."

    - id: preserve
      text: "The druids keep it. Let it grow."
      effects:
        sliders: { nature: +12, prosperity: -6, joy: +5 }
        regionOverride: { far_shore: pristine, treeline: wild }
        flags: { set: [northWoodsSettled, metDruids] }
        counters: { druidFavors: +1 }
        grant: [ { reward: druid-charm } ]          # rewardType SKILL
      result: "Sela plants a grove in your honor. The frogs approve."

    - id: defer
      text: "…I'm fishing. Ask me later."
      effects: { sliders: { order: -3 } }
      requeue: true                 # returns to the bag — NOTHING is missable (time pillar)
      result: "They both sigh and wander off. For now."
```

### 2.1 Card kinds

- **`interrupt`** — the default kingdom-task card: a standalone decision (warlock/
  druid). Drawn from the ambient pool by weight.
- **`arc-step`** — a card that is part of a multi-card arc (§4); not drawn freely,
  it fires when its arc reaches its step.
- **`ambient`** — low-stakes flavor cards (a fisherman's tale, a duck census) that
  add texture and small slider nudges; higher draw weight, `once: false`.
- **`finale`** — a card whose choice can set `status: COMPLETE` and an `endingKey`
  (§7). Only eligible once its trigger conditions (usually slider extremes or an
  arc completion) are met.

### 2.2 The "defer" guarantee (time pillar)

Every interrupt card **must** offer a `requeue: true` path (an "ask me later" /
"I'm fishing" option) so the player is never forced to decide and no card can trap
the loop. A requeued card returns to the draw bag; it is never lost, never expires.
This is the deck-format encoding of Silas's no-missable-content pillar.

## 3. Triggers (when a card is eligible)

A card's `trigger` block is a pure predicate over the current `RunSave` (t-004).
The engine evaluates it with **no side effects and no wall-clock input**:

```yaml
trigger:
  minTurn: 3                        # turnCount >= 3   (turns, not time)
  maxTurn: null                     # optional upper bound (still turns)
  requires:                         # ALL must hold
    sliders: { nature: { gte: 30, lt: 80 } }
    counters: { warlockFavors: { gte: 1 } }
    flags: [metWarlock]             # these flags must be set
    rewards: [gilded-lure]          # player must own these Reward slugs
  forbids:                          # NONE may hold
    flags: [northWoodsSettled]
    cardsSeen: [rival-angler-3]
  cooldown: 6                       # min turns since this card last fired
  weightBonus:                      # optional situational weighting (§5)
    when: { sliders: { joy: { lt: 25 } } }
    add: 4
```

Supported comparators: `gte, gt, lte, lt, eq, neq` on numeric sliders/counters;
set-membership for `flags`, `rewards`, `cardsSeen`. `requires`/`forbids` are the
whole conditional vocabulary — deliberately small so triggers stay data-authorable
and inspectable, and so **no trigger can reference time**. If a future condition is
needed, it is added to this closed list in the engine (a rare code task), never
expressed as an escape hatch in content.

## 4. Decks and arcs (grouping & sequencing)

### 4.1 Decks

A **deck** is a named file of cards drawn from together. The PoC ships a few:

```yaml
# content/<version>/decks/kingdom-core.yaml
deck:
  id: kingdom-core
  title: "Kingdom Interruptions"
  description: "The everyday decisions of a monarch who would rather fish."
cards: [ ... ]                      # the card entries (§2)
```

Decks let content be organized and toggled by theme (kingdom politics, family
drama, lake mysteries) without the engine knowing their contents. Adding a deck =
dropping a file and listing it in `content/<version>/manifest.yaml`.

### 4.2 Arcs (multi-card stories)

An **arc** is an ordered/branching sequence of `arc-step` cards sharing state. The
brief's example — *the ruler's child wants to elope* — is an arc:

```yaml
# content/<version>/decks/family-elope.arc.yaml
arc:
  id: child-elopes
  title: "The Heir's Secret Sweetheart"
  characters: [heir-robin, sweetheart-ash]   # Character slugs
  start:                                       # eligibility to BEGIN the arc
    trigger: { minTurn: 8, requires: { flags: [hasHeir] }, chance: 0.5 }
  steps:
    - id: elope-1
      # ... a card (§2) with kind: arc-step ...
      choices:
        - id: bless
          effects: { arc: { advance: elope-blessing }, flags: { set: [blessedMatch] } }
        - id: forbid
          effects: { arc: { advance: elope-defiance }, sliders: { joy: -8 } }
    - id: elope-blessing   # branch A
      # ...
    - id: elope-defiance   # branch B
      # ...
  # arc state lives in save.deckState.activeArcs["child-elopes"]:
  #   { step: "elope-1", flags: { blessedMatch: false } }
```

- **Arc state** (`step`, arc-local `flags`) lives in `save.deckState.activeArcs`
  (t-004 §3). The engine advances an arc only via a choice's
  `effects.arc: { advance: <stepId> }`; `arc: { start: <arcId> }` and
  `arc: { complete: <arcId> }` begin and end one.
- Arcs **branch** by pointing different choices at different next steps — no code,
  just data. A branch can also **grant a Reward** or **pin a region** like any card.
- **No arc step is time-gated.** An arc paused at step 2 waits forever; the player
  may fish for a month between steps.

## 5. Selection & per-run variety (the replay engine)

Each turn, the deck engine decides whether a card fires and which one, producing
different runs from the same content. The algorithm is fully **seeded** (t-004
`seed`) so a save reloads to the identical sequence:

```
onTurn(save):
  1. Advance any ACTIVE arc that has a ready next step → fire that arc-step card.
     (Arcs take priority so ongoing stories resolve.)
  2. Else, with probability P(interruptChance, tunable), build the ELIGIBLE POOL:
       every card whose trigger predicate (§3) holds against `save`,
       minus cards on cooldown, minus `once` cards already in seenCardIds.
  3. Weighted pick from the pool using effectiveWeight =
       card.weight + Σ(matching trigger.weightBonus.add).
     RNG draws come from the seeded stream, so the pick is deterministic per save.
  4. If the pool is empty, no card fires this turn (pure fishing) — always valid.
```

Variety comes from three seeded sources, none of which gate content:
- **Different eligible pools** per run (different slider trajectories → different
  triggers satisfied).
- **`chance` on arc `start`** and **weighted draws** → different arcs surface on
  different playthroughs (the heir's elopement happens in one run, not another).
- **Character reuse:** cards reference Character slugs; swapping which Characters a
  deck features (or which existing kind_robots Characters are cast) reshapes a run
  without new cards.

Because everything is seeded and deterministic, "replay variety" and "reload
parity" are the same mechanism viewed two ways.

## 6. Effects grammar (what a choice does)

A choice's `effects` is a closed, declarative grammar — the only way content mutates
the save. The engine applies it atomically and logs it (t-004 `choiceLog`):

| key              | meaning                                                        |
|------------------|----------------------------------------------------------------|
| `sliders`        | `{ axis: ±n }` — additive deltas to `kingdomHealth`, clamped 0..100 |
| `counters`       | `{ key: ±n }` — additive deltas to discrete tallies             |
| `regionOverride` | `{ region: state }` — pin a region's visual state (t-005 §3)    |
| `flags`          | `{ set: [...], clear: [...] }` — world flags                    |
| `grant`          | `[ { reward: <slug> } ]` — add a Reward to inventory (§1)       |
| `revoke`         | `[ <reward-slug> ]` — remove a Reward                           |
| `arc`            | `{ start \| advance \| complete: <id> }` — arc control (§4)      |
| `ending`         | `<endingKey>` — set on `finale` choices only (§7)               |
| `requeue`        | `true` — return this card to the bag (defer, §2.2)              |

Rules:
- **Additive, never absolute** for sliders/counters, so effects compose and stay
  legible; the engine clamps.
- **Effects are the audit record.** The applied `effects` object is copied into the
  `choiceLog` entry, so a run reconstructs even if the card's authored effects later
  change (t-004 §7 determinism).
- **No `effects` key can reference or set time.** There is deliberately no `time`
  or `expire` verb in the grammar.

## 7. Endings (closing a run without a clock)

- A `finale` card's choice may carry `effects.ending: <endingKey>`, setting
  `save.status = COMPLETE` and `save.endingKey`. Endings are cataloged in
  `content/<version>/endings.yaml`, mirroring **LifeEnding**:

```yaml
endings:
  - outcomeKey: druid-utopia
    victoryType: VICTORY            # LifeVictoryType: VICTORY|FAILURE|MIXED|SECRET
    title: "The Angler's Grove"
    trigger: { requires: { sliders: { nature: { gte: 85 }, joy: { gte: 70 } } } }
    body: "Your kingdom is a garden. You have caught every fish. Twice."
  - outcomeKey: warlock-metropolis
    victoryType: MIXED
    title: "Boomtown by the Lake"
    trigger: { requires: { sliders: { prosperity: { gte: 85 } } } }
```

- Endings are **reachable, never forced.** They surface as an eligible `finale`
  card when their trigger holds; the player may keep fishing and decline. Nothing
  ends a run on a timer. A `SECRET` ending is just one whose trigger is obscure.
- A completed run is kept and replayable; ending achievements can map to
  kind_robots **LifeAchievement** if synced.

## 8. Authoring workflow (why this stays a content task)

To add content, an author (human or an agent on a content task):

1. Writes/edits a YAML file under `content/<version>/decks/` (a card, a deck, or an
   `.arc.yaml`) using the schemas above.
2. Adds any new **Character** as a `characters/<slug>.yaml` using the kind_robots
   `Character` field names — or references an existing Character slug.
3. Adds any new **Reward** as `rewards/<slug>.yaml` using `rewardType`/`rarity`/
   `effect`.
4. Registers new files in `content/<version>/manifest.yaml`.

No engine code changes. The generic selection (§5), trigger (§3), and effects (§6)
machinery already handle it. This is the concrete meaning of the brief's rule:
**"Adding an arc must be a content task, not a code task."**

## 9. Open questions for the build (t-007)

- `interruptChance` tuning and whether it scales with turns-since-last-card (a
  gentle pacing curve, still turn-based).
- Whether ambient cards draw from a separate, higher-frequency pool than interrupts
  (recommended: yes, so flavor doesn't crowd out decisions).
- Exact set of PoC arcs beyond warlock/druid + elope (endings.yaml needs ≥2 for the
  m2 criterion "one complete narrative arc").
- Whether narrator voice varies per deck (multiple narrator bots) or one Dream
  narrator for the PoC (recommend one for the PoC).

None block t-007's build against this format; they are content-tuning decisions.
