# Shifting Lands — Illustrated Board, Decks & Card Interaction Architecture

**Implementation-grade addendum to [DESIGN-BRIEF.md](DESIGN-BRIEF.md).** Requested by Silas, 2026-10-09: an art-heavy premium game board with **real front/back cards, physical-feeling draw decks, dealing, flip/reveal animations, discards, and visible travel history**, all using existing Kind Robots systems first. This is now **MVP**, not postlaunch polish. No playable UI is claimed by writing this document.

## Verified components in Kind Robots main (2026-10-09)

| Existing owner | Source path | Confirmed behavior | Shifting Lands integration |
| --- | --- | --- | --- |
| Persistent front/back gallery flip | `components/gallery/kr-card-flip.vue` | Overlay, backdrop, center/scale, escape/focus, cancel vs save reverse, reduced-motion. Caller provides faces; no store/fetch. | Use for opening a location's inspected card, inventory/companion back, lore or choices overlay. Wrap gameplay content; never have this component decide encounter effects. |
| Reusable inspected card back | `components/gallery/kr-card-back.vue` | Shared identity/art and extra details, action tier; supports archived image variations and independent editor slots. | Render read-only detailed reward/character/asset info. Present choices in a game-specific slot instead of smuggling mechanics into generic editor. |
| Deal spin | `components/navigation/flip-card.vue` | Front and back slots, 360° `rotateY`, `triggerKey`, start/halfway/done emits, duration/radius/scale, reduced-motion. **Returns to its FRONT**, not a persistent face-down state. | Use for the animated *deal* or transition onto the board, not for a card that must remain face up/back down. Persist card `faceState` in game state and use a small adapter to choose the visible side at the halfway event. |
| Card back art | `components/navigation/card-picker.vue` | Five existing backs at `/images/adventure/card/card-back{1..5}.webp`, and user preference `kr.workspaceCardBack`. | Reuse actual card back assets and preference when appropriate; optional Zuzu deck skins are variants, not mandatory new primitive. |
| Art-first 2:3 entity cards | `components/narrative/narrative-ingredient-card.vue`, `utils/narrativeIngredients.ts` | Existing image-first cards, badge/copy, selected/locked semantics, art placeholder and loading/failure behavior. | Feed it validated Character/Facet/Scenario/Reward/Location cards through adapter functions; preserve species/occupation as different taxonomy identity. |
| Storybook card-board spread | `components/storybook/storybook-table.vue`, `utils/storybookTableDecks.ts` | Named board slots with capacities, real entity decks (Hero, Company, Place, Thread, Treasure), selectable/dealt hand; art-backed source records. | Borrow slot layout/board selection and pure card-mapping concepts. Do **not** reuse Storybook's whole mutable board/run owner in combat or map navigation. |
| Storybook ending decks | `server/api/storybook/decks/index.get.ts`, `utils/storybookRuns.ts` | Server-run ending deck listing, unlock state and rule ownership. | Reuse lesson of server-authoritative decks but **not** treat ending decks as encounter deck infrastructure; these are not generic shuffled draw piles. |
| Global workspace hand | `components/navigation/workspace-hand.vue` | Responsive navigation hand with card art/backs and flip feedback, set preferences. | Its measured card sizing and gestures are useful patterns; **do not mount it as a combat/encounter hand**, as it owns global site navigation. |
| Flip-grid visual effect | `stores/flipStore.ts` | 3×6 staggered **image-slice board flip** transitioning between pictures. | Optional land-change/fog effect only; **not** a deck/hand engine. |
| Comic slot board | `components/comics/comic-slot-board.vue` | Art-first grid, selectable tiles, drag handling, source/render previews. | Reference for source-art-backed placement and responsive tiles; no dependence on Comic Studio save semantics. |
| Zuzu World Studio | `pages/admin/worlds/zuzu.vue`, `server/api/worlds/zuzu/assign.post.ts` | Read-guarded live ArtImage gallery and reversible `ProjectArtImage` links. | Query its Zuzu project associations and media provenance; source ArtImage IDs must be retained across cards, never copy binaries. |

**Important audit finding:** The verified pieces deliver visuals, flips, face art and Storybook selection/decks, but **they do not together constitute a general-purpose persistent shuffled draw/discard library**. Build the minimal **pure reducer/deck-state adapter** required for Shifting Lands, after searching remaining existing stores for suitable shuffle/draw helpers. Do not call the Storybook *ending deck* or global *navigation hand* a gameplay deck. Reuse presentation and event components while defining new game-only state transformations.

## Composition hierarchy

```text
/play/zuzu-shifting-lands (private, until public approval)
  └─ ShiftingLandsBoard (layout shell; no authoritative game outcomes)
      ├─ JourneyMap (5 land panels; card tiles, completed trail)
      │   ├─ LandBanner (large art / current chapter / progressive weather)
      │   ├─ LocationNodeCard ×3 (draw state / fog / face / mark / links)
      │   └─ BossGateCard (locked → staged → resolved)
      ├─ DeckDock (face-down piles, remaining count, shuffle/draw buttons)
      │   ├─ LocationDeck  EncounterDeck  RoleDeck  SpeciesDeck
      │   ├─ DispositionDeck [hidden during play]  EventDeck
      │   ├─ RewardDeck  CompanionDeck  BossDeck
      │   └─ DiscardStacks (reveal/inspect only if permitted)
      ├─ ActiveEncounter (large hero art / narrative / action cards / dice)
      ├─ PartyHand (Zuzu stats, companions, skill, condition, inventory cards)
      ├─ TimelineJournal (visited, altered map, discoveries, prior choices)
      └─ ArtworkInspector (gallery kr-card-flip / kr-card-back)
  ├─ useShiftingLandsStore (Pinia, one authority for current UI session)
  ├─ utils/shiftingLands/{cards,deckState,encounters,journey,reducer,seed}.ts
  └─ server/api/shifting-lands/... (source-authorized catalog, saves, optional story text)
```

**Ownership:** Board emits intent (`DRAW_DECK`, `FLIP_CARD`, `TRAVEL`, `CHOOSE`, `ROLL`, `RESOLVE`, `DISCARD`, `EQUIP`) to store/reducer; reducer validates and persists a versioned event. Only successful state transition schedules corresponding animation. Animation `done` signals visual completion, **never gameplay completion**, and refresh/reduced-motion do not cause duplicate effects.

## Board zones and desktop composition

```text
┌─ ZUZU: SHIFTING LANDS ─────────────── LAND 1 / 5 ─ Journal ─ Menu ┐
│  Full-bleed illustrated region environment and progress route              │
│  ┌──5-land journey rail: Homestead • Crossing • Tablelands • Cave • Verge┐ │
│  │   [Completed tiles + stamped trail]   [CURRENT]   [Fog of war]        │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│  [LOCATION 1]        [LOCATION 2]         [LOCATION 3]    [BOSS / GATE]    │
│   illustrated         back → front       face-down         locked          │
│                                                                           │
│  ┌──── Deck dock ────┐ ┌──────── LARGE CURRENT ENCOUNTER ──────────────┐  │
│  │ [Encounter]  12   │ │ scenic art: 65–75% of this area                │  │
│  │ [Event]       7   │ │ short prose, draw/play/skill choice cards      │  │
│  │ [Reward]      9   │ │ shown chance and risk; dice only on commit     │  │
│  │ [Companion]   3   │ └───────────────────────────────────────────────┘  │
│  │ [Discard]     4   │                                                     │
│  └───────────────────┘ Zuzu portrait/HP/stats · Companion hand · Inventory  │
└───────────────────────────────────────────────────────────────────────────┘
```

**Art is at least two-thirds of the primary board/encounter canvas**, with large environments, clear illustrated tiles and handsome backed stacks, **not a dashboard of counters and data tables**. Counts and status live on small physical-looking badges. Decks visually overlap like stacked cards, with subtle stagger/shadow/edge treatments. Completed locations get inked travel marks; altered unvisited nodes change with a recorded visual transition.

**Tablet:** central board first, side docks collapse to tabs/drawers, visible quick-draw affordance. **Phone:** horizontal swipeable 5-land progress strip, current land 3 location cards in a generous row/stack, persistent current-encounter art, bottom drawer for decks/hand, one large focused interaction at a time. Scrolling must not fight touch dragging. Respect `prefers-reduced-motion`, minimum touch target 44px, keyboard select/flip/resolve, readable semantic labels and focus return.

## Card model: image and rule identity are different

```ts
type CardKind =
  | 'land' | 'location' | 'encounter' | 'species' | 'role'
  | 'disposition' | 'companion' | 'reward' | 'event'
  | 'condition' | 'boss' | 'action'

type CardFaceState = 'back' | 'front'
type CardZone = 'deck' | 'offer' | 'board' | 'hand' | 'discard'
type SourceRef = {
  entityType: 'ArtImage' | 'Character' | 'Facet' | 'Scenario' | 'Reward'
  id: number
  provenance?: string
}
type GameCard = {
  instanceId: string        // stable per seeded journey; not a DB row ID
  templateId: string        // versioned source/game content card definition
  kind: CardKind
  faceState: CardFaceState
  zone: CardZone
  owner?: 'player' | 'world'
  art?: { sourceArtImageId: number; thumbUrl: string; previewUrl: string }
  sourceRefs: SourceRef[]
  publicFace: { title: string; label?: string; shortCopy?: string }
  gameFlags: string[]       // state keys, not loose code eval
}
type DrawPile = {
  id: string
  orderedCardIds: string[] // shuffled once from seeded RNG, stored
  discardCardIds: string[] // explicit destination, no implicit reshuffle
  exhaustionRule: 'stop' | 'reshuffle-discard' | 'advance-land'
}
```

**Location/Encounter** card fronts use actual source media; backs can use existing five card backs or the project's own approved art. **Species** and **Role** remain distinct deck IDs and type/taxonomy checks. A named Character may replace anonymous species+role slots only if the authored encounter permits it; maintain consistency and locked cast. Disposition/hidden motive are *allowed in GitHub canonical source*, but do not render on the face presented to players before discovery.

**Do not store unverified external image URLs in game state.** Save source IDs + verified template revision; resolve current authorized URL on demand. Cards may visually share an image but never become duplicate ArtImage rows. Artwork missing/unapproved yields deliberate painted placeholder or pending panel, not broken icons or a fabricated canon portrait.

## Draw/deal/flip lifecycle contract

1. **Setup:** load verified `worlds/zuzu` resources, approved art and typed source templates; create deterministic run seed; compose land layouts and eligible deck pools. Record seed + content revision + initial shuffled order; no hidden paid calls.
2. **Draw:** click/tap a stack. Reducer consumes one *top* `instanceId` and moves it to `offer` or `board`, atomically saving draw event. Display a card flying from stack to target using existing flip-card movement/flip treatment. Never choose a new random card on each render.
3. **Deal:** `components/navigation/flip-card.vue` animates a card to a target slot. Its `halfway` emit can switch illustrated face in an adapter, but **the component always returns to its starting side by design**. For a persistent back→front reveal, keep the reducer's `faceState` and render the settled card in that state. Do not turn the 360° component into a false persistent-state controller.
4. **Reveal:** one committed state transition changes `faceState`, plays an accessible turn animation, exposes source art/name/choices and registers a discovery event. Non-revealed backs retain neutral card-back art; avoid clue leaks from alt text, badges, aria labels or background art.
5. **Play/resolve:** selection of an action triggers a validated skill check or narrative outcome. Dice are generated once and saved; a UI repeat, retry, network duplication or refresh cannot reroll. Cards move to board/hand/discard and apply consequences exactly once.
6. **Discard:** visible discard stack records card IDs, last-card face art and discard reason. For a non-recyclable plot card, exhaustion `stop` or story gate; for events, reshuffle only as defined in the deck config and journal it.
7. **Inspect:** gallery `kr-card-flip.vue` shows detailed back, with `kr-card-back.vue` for shared entity records. Inspecting must **not** secretly reveal hidden motive, draw an extra card or change authoritative state.
8. **Land change:** completed encounters remain pinned on map and journal; use existing `flipStore` image-grid reveal only as optional **visual overlay** to portray region shifting, not as a gameplay location-state store.

**Draw limits:** one in-flight action per deck/run revision; disable concurrent operations; server verifies `expectedRevision` and idempotency key for mutations. Display deck empty/exhausted explicitly. Before using any generic `useFlipStore` transitions in the main page, confirm that multiple screens cannot collide with the global image flip demo state.

## Deck type and placement matrix

| Deck | Draw target | Flip/show behavior | Data owner | Exhaustion |
| --- | --- | --- | --- | --- |
| Lands (5) | map progression | visible completed/active, future back/ghost | five-land manifest | end journey |
| Locations (3/land) | three board tile wells | back until traveled; retain fronts in journal | land and map reducer | unlock boss |
| Encounter | large reader / event offer | face-down draw → reveal + choices | world-tagged Scenarios + templates | stop or authored land fallback |
| Species | encounter's participant slot | hidden until participant visible | verified `Facet(SPECIES)` | replenished per ecology on new land |
| Occupation/Role | participant description | independently sampled, can be unrevealed | `Facet(OCCUPATION/ROLE/ARCHETYPE)` | as defined by authored pool |
| Disposition/Motive | internal participant state | generally never visibly drawn to user | seeded run state | finite hidden pool |
| Event/Condition | board and status rail | reveal on effect | vetted world events/rewards | configured reshuffle |
| Companion | ally offer/party hand | art-backed profile, inspect backside | named Character + matching Facets | persistent/unique |
| Reward | player's hand/inventory | reveal, equip/use, discard where valid | verified Reward + ArtImage | land-tier pool |
| Boss/Challenge | gate of current land | back until boss unlocked | authored challenge template | exactly one per land |

The **species deck is not a monster deck**, and the **role deck is not an alignment deck**. The first Homestead sample can deal `Rabbit + Farmer + Helpful` or `Otter + Farmer + Hostile` with no special species moral weighting.

## Implementation order and acceptance tests

**S1 — audit & adapter:** Locate existing image/deal/flip/list components and add unit-tested thin adaptors with typed props/emits. Preserve global navigation and Storybook owner scopes. Create catalog-backed `CardFace`, `DeckPile`, `CardInspect` wrappers only where no reusable game-level component exists.

**S2 — playable vertical slice:** First land Homestead only, three illustrated locations + Abbey/Abbess gate, one encounter and reward draw stack, back/deal/reveal/discard/resume, readable Zuzu stats. Strictly reuse known gallery/flip primitives; include source ArtImage ID references. Allow the game's designed plot spoilers in GitHub; conceal them from players until clues.

**S3 — full journey:** Five lands × three encounters, region transformations with history, companion/condition/role/faction decks, boss alternatives, seed persistence and reproducible rolls, save/resume on all viewports.

**S4 — cinematic polish:** Deck shuffle/fan motion, lifted card shadows, non-obstructive sound, haptic where supported, full accessibility, reduced motion, robust art fallback and animation regression tests. No substitute CSS-only static card gallery qualifies as playable.

**Mandatory acceptance:**
- A card draws visibly from a backed stack, moves to a slot, turns over and **remains in its new face state**, surviving save/refresh.
- Distinct draw, discard and board/hand zones with accurate counts, exhaustion and traceable source IDs.
- Draw and roll results stable by seed, independent of animation/reduced-motion/refresh; no double application from rapid clicks.
- 3 location cards × 5 lands, five boss gates, journey journal and visibly changed unvisited geography.
- Species vs occupation independent, with rabbit and otter each able to appear in at least two different compatible roles; no morality/species lock.
- Zuzu is the approved grey koala ronin, not a fox; source images are actual Kind Robots approved assets or explicit awaiting-art states.
- Keyboard/touch/desktop interactions; test at 375, 768, and 1440px and record screenshots from the authenticated app; avoid fake data disguised as production media.
- No client leak *before its dramatic reveal* even though developers can read full canonical story in GitHub.
- At least one render-path and one nonanimated reduced-motion path have interaction-level tests; existing tests for Gallery, Storybook and global workspace navigation continue to pass.

## Out of scope for this addendum

Do not begin a second gallery store, an independent ArtImage/Facet/Reward database, a generic framework rewrite, an external card/deck library, or publishing the unfinished game. Preserve the existing user-approved automated agent scope; this addendum makes the art-heavy board and tactile interactions a first-class **release gate** rather than optional decoration.
