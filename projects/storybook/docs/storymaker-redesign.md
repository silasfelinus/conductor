# Storymaker redesign: the Table, the Reading, the Ending, the Collection

Product spec and engine design for the card-driven, many-endings Storybook. Written 2026-09-12
in a Silas-directed session from his brief (verbatim intent: *"a storymaker story should start
like our kr-hand setup: users should choose cards that represent the various elements of a
story ... when a card is selected, it enters a storyboard, which when filled, they can start a
story ... a number of experiences that they can choose either from a set of choices, a custom
choice, or use their main character's character sheet ... at the end of a certain number of
choices, they will end up at one of the predetermined endpoint endings, which they get credit
for in a collection of their adventures ... Stories should not be verbose with purple prose,
they should be direct, but this should be influenced by the narrator."*).

Decisions Silas made when this was planned: **ending decks** (each deck has its own hidden axes;
genre decks are 3–4 axes / 8–16 endings; the Life deck keeps 10 axes / 1,024 endings; one
engine), **the bottom workspace hand is taken over by Storybook on `/storybook`** (one hand on
screen), **the typed premise is optional** (a "Spark" slot), and **screens wait for the mockups**
Silas is commissioning from Part B while the engine groundwork (Part C) ships first.

Roadmap: storybook m6 (t-027..t-033, engine) and m7 (t-034..t-038, screens). The Da Vinci
merge record is `davinci-merge.md` beside this file.

## Part B — The product (the mockup brief)

Vocabulary: **the Table** (setup), **the Reading** (play), **the Ending**, **the Collection**.
All cards use real entity art via `resolveEntityArtwork` (`utils/artImageSrc.ts`) in the
`card` 2:3 shape from `utils/galleryVocabulary.ts`, rendered by `narrative-ingredient-card.vue`
(art, scrim, rarity/type badge top-left, check top-right) — this is the "Common favor / Common
pet" card already on screen. House themes `storybook` / `storybook-dark`
(`assets/css/tailwind.css`) stay the reading modes.

### B1. The Table (setup) — one open surface, no steps

- **Storyboard**: a tableau of slots laid out like a spread. Each slot is a card-shaped well
  (2:3, dashed when empty, art when filled) with a one-word label:

  | Slot | Deck it draws from | Required | Count |
  |---|---|---|---|
  | Genre | Facet GENRE (each genre = an ending deck) | yes | 1 |
  | Place | Dream LOCATION | yes | 1 |
  | Hero | Character (protagonist) | yes | 1 |
  | Company | Character (supporting cast, roles via `narrative-role-assigner`) | no | 0–2 |
  | Narrator | 5 voice cards (Cinematic, Playful, Storybook, Mysterious, Intimate) + narrator Bots | default Storybook | 1 |
  | Shape | Short tale · Chaptered tale · Serial · A whole life | default Short | 1 |
  | Thread | Scenario (a plot thread; also its own ending deck when one exists) | no | 0–1 |
  | Treasures | Reward (what the fiction may hand out) | no | 0–3 |
  | Spark | typed premise (card-shaped text well) | no | 0–1 |

  Choosing "A whole life" swaps the Genre slot's deck to the Life deck (genre stays as flavor).
- **The hand** (bottom of page, the existing workspace hand taken over on `/storybook`): fans
  the deck for the **active slot**. Tap a slot → the hand re-deals that deck (flip animation
  already in `workspace-hand.vue`); tap a card → it flies into the slot and the next empty
  required slot becomes active. Cards already on the board show face-down in the hand. Search
  and "show all" live in the hand's edge. Drag from hand to slot on desktop (mechanics exist in
  `narrative-cast-card.vue` / `narrative-role-assigner.vue`).
- **Board lights up** when Genre + Place + Hero are filled: the "Open this story" button (sticky
  footer, unchanged) enables and the board gets its glow. "Clear the table" stays.
- Deep links (`?character=`, `?location=`, `?facet=`, `?reward=`, `?scenario=`) pre-place cards.
- Mood/Theme/Style Facets stop being a picker; they ride along as optional "Tone" cards
  in a secondary row (max 3) — keep them off the required path.
- **Hand takeover mechanism** (for t-034, after mockups): `content/storybook.md` front matter
  `cards: navCards` is what fills the hand today (`stores/pageStore.ts` `cardsKey` → the deck
  registry in `stores/helpers/modelCards.ts`). Add a `storybookCards` key resolved from the
  new run store's active-slot deck (same path `builderCards` uses for the builder), so
  `workspace-hand.vue` keeps its sizing/flip/scroll code untouched and only the card source
  changes. Nav cards come back on any other page automatically.

### B2. The Reading (play)

- **Stage**: scene art plate (`kr-art-plate`, hero 16:9) with the prose below it. Prose is
  short and direct (word budget per shape, Part C). No chat bubbles; each turn is a page.
- **Tableau strip** at the top: hero, company, place, narrator as small cards; turn pips
  "Turn 3 of 8" as a row of small card backs flipping face-up as turns pass.
- **The move** (three ways, always visible together):
  1. **Options**: 2–4 option cards (text on card-backs, a small icon), the `kr-choice-list`
     stack restyled as cards.
  2. **Write your own**: one line input ("You ...") — the existing composer.
  3. **Character sheet**: the bottom hand now fans the **hero's Skill/Item cards** (the
     Character's starting loadout `Character.Rewards` + inventory gained in play). Playing one
     is the turn ("You use the Cousin Who Knows a Guy"). Items may be spent; skills stay.
- **Axes stay hidden** (they are the deck's secret). Life keeps its ten pills behind a
  "show the ledger" toggle; genre decks show only prose consequences.
- Inventory/consequences panel (`storybook-state-panel.vue`) becomes a drawer, not a column.

### B3. The Ending

- On the last turn the "See your ending" card appears; resolution flips a large ending card
  (ending art hero, title, victory type badge, summary) — the `kr-card-flip` gesture.
- "Added to your collection · 3 of 12 Mystery endings" with the deck's album row beneath
  (found face-up, unfound face-down silhouettes).
- "Play again with this table" (same board, new run) · "New table".

### B4. The Collection

- Replaces the localStorage "Recent stories" drawer. Per-account: **Adventures** (server runs,
  resume/replay/export) and **Endings** albums per deck. Life's existing "Endings on record"
  (Achievement `davinci-ending-*`) folds in as the Life album.

### B5. Gating (later, design only now)

- Locked genre/character/narrator cards appear face-down in the hand with a lock and an
  unlock hint ("Finish any Mystery"). Unlock condition lives on the deck/card record and is
  awarded by the same resolution transaction that credits the ending.

### B6. Prose

- Direct prose is the default contract for every narrator: concrete, second person, present
  tense, one image per beat, no stacked adjectives or similes, no throat-clearing, end on the
  brink of the decision without listing the options. Word budget per shape (Short 60–120,
  Chaptered 90–160, Serial 90–160, Life 90–180 per turn).
- The narrator voice modulates within that: Cinematic (cuts, momentum, wide-to-close),
  Playful (light, quick, delighted), Storybook (warm, read-aloud cadence, still plain), Mysterious
  (withholding, sensory, questions unanswered), Intimate (close third-person noticing, small
  gestures). Exact directive text is in Part C.

---

## Part C — Engine groundwork (kind_robots)

Principle: **generalize the Life engine, don't fork it.** The run/choice/stat/ending/award
engine, its idempotency guards, the 1,024 seeded endings and their importer all exist and
work. Life becomes the deck with key `life`; table names stay (renaming a live table is not
additive; t-026 can `@@map` later). Conductor's roadmap note explicitly allows columns on Life*.

### C1. Data model (additive; two migrations, hand-authored SQL like `20260825120000_add_creature_model`)

Schema additions in `prisma/schema.prisma`:
- `enum EndingDeckOwnerKind { LIFE GENRE_FACET SCENARIO }`, `enum StoryShape { SHORT_STORY CHAPTERED EPISODIC LIFE }`, `enum StoryMoveSource { OPTION CUSTOM SHEET }`.
- `model EndingDeck { key @unique VarChar(64), title, description?, ownerKind, facetId?, scenarioId?, axes LongText (JSON DeckAxis[] in bit order), passValue Int @default(1), turnBudget Int @default(8), turnBudgetByShape LongText? (JSON), minTurnsBeforeResolve Int?, unlockAchievementId Int? (gating hook), isActive; relations Facet?, Scenario?, Achievement?, Endings LifeEnding[], Runs LifeRun[] }`.
- `LifeRun` + `shape StoryShape @default(LIFE)`, `deckId Int?` (NULL = legacy life run → resolver maps to deck `life`), `turnBudget Int?`, `narratorStyle VarChar(32)?`, `premise Text?`, `scenarioId Int?`, `bible LongText?` (JSON snapshot of the board), `inventory LongText?` (JSON entries with `consumedAtTurn`), `pendingTurn LongText?` (the narration the reader is looking at: turnIndex, narrativeText, choices with effects, artPrompt). `currentChapter` is reused as the 1-based turn index.
- `LifeChoice` + `source StoryMoveSource @default(OPTION)`, `optionId VarChar(8)?`, `rewardId Int?`, `stateDelta LongText?`, `artPrompt Text?`.
- `LifeEnding` + `deckId Int?` and `@@unique([deckId, outcomeKey])`.

Migration 1 `20260913120000_add_ending_deck_and_story_run_columns`: create `EndingDeck`, add all columns (NULL/DEFAULT), insert the `life` deck row with axes from `server/utils/davinciDimensions.ts` order, backfill `LifeEnding.deckId` to it, add the composite unique. Nothing in the running build inserts LifeEnding rows (only the seed script), so this cannot race the old build.

Migration 2 `..._drop_life_ending_global_outcome_key_unique` (ships with PR-D, **after PR-C is deployed**): drop `LifeEnding_outcomeKey_key`, make `deckId NOT NULL`. This is the one staged step: the old build's lookup compiles to `WHERE outcomeKey = ?` and keeps working through the handoff; the resolver must use `findFirst({ where: { deckId, outcomeKey } })` until then. Both migration PRs are flagged **schema-affecting**.

### C2. Narration contract — `server/utils/storybookNarration.ts` (this is storybook t-025)

- New DB-free `server/utils/endingDeckMath.ts`: `DeckAxis`, `DeckDefinition`, `resolveDeckOutcomeKey(deck, stats)`, `deckOutcomeKeys(deck)`, `parseDeckAxes(json)` (1–12 unique snake_case keys), `LIFE_DECK`. `davinciDimensions.resolveOutcomeKey` delegates to it (same bit order, same output; keeps the contract-tests job DB-free).
- New `server/utils/structuredCompletion.ts`: `completeStructured({ model, system, user, schemaName, schema, temperature, maxTokens, timeoutMs, apiKey })` extracted from `davinciNarration.ts`'s `callNarrator` (OpenAI chat completions, strict `json_schema`, `gpt-4o-mini`, `getRuntimeOpenAiKey` from `server/utils/textProviderService.ts`). There is no shared non-streaming JSON-schema helper today (`brainstormProvider.ts` and `commentBackfillGeneration.ts` each hand-roll one), so this becomes it. Do not route through `/api/chats/*/stream` (SSE, no schema). Add `manaGate` + `estimateTextCostUsd` in the new turn route (narration is unmetered today — pre-existing gap, fixed only in the new route).
- `storybookNarration.ts` request: `{ shape, deck, narratorStyle, narrator (existing DaVinciNarrator), seed, turnIndex, turnBudget, isFinalTurn, bible {title, premise|spark, cast+roles, location, facets, scenario, treasures with slugs}, statsSoFar, inventory, recentTurns (last 3), move: {source: option|custom|sheet, text, optionId?, rewardSlug?} | null, playedReward | null }`. Response: `{ narrativeText, moveEffects (deck axes only, clamped ±2, {} when move is null), choices 2–4 (exactly 0 on the final turn) each {id a–d, choiceText, effects}, stateDelta {consequences, relationshipShifts, inventoryAdd, inventoryRemove ≤3 each, slugs ⊆ treasures}, artPrompt, endingHint }`.
- Exports: `storybookResponseSchema(deck, { finalTurn })` (effects properties generated from the deck's axes), `validateStorybookNarration(payload, deck, bounds)`, `buildStorybookSystemPrompt`, `buildStorybookUserPrompt`, `generateStorybookTurn`, `PROSE_BOUNDS_BY_SHAPE = { 'short-story': [50,130], chaptered: [70,190], episodic: [70,190], life: [20,400] }` (life keeps its current bound so `utils/scripts/verifyDaVinciNarration.ts` passes untouched; tighten later with that guard), `NARRATOR_STYLE_DIRECTIVES`.
- `davinciNarration.ts` becomes an adapter: keeps every exported name and bound (`NARRATION_EFFECT_MIN/MAX`, `NARRATION_MIN/MAX_CHOICES`, `narrationResponseSchema`, `validateNarrationPayload` returning `milestoneCandidate` from `endingHint`, `generateDaVinciChapter`) and maps a LifeRun to a request with `deck: LIFE_DECK, shape: 'life'`.

**Direct-prose contract** (system prompt, every shape; `{MIN}`/`{MAX}` from the shape):

```
PROSE CONTRACT
Write in second person, present tense. The reader is the protagonist unless the bible says otherwise.
Write one concrete scene: a place, a moment, one or two people, one thing that happens. Not a summary of hours or years.
Be direct. Plain nouns and strong verbs. One adjective per noun at most. No similes, no metaphors, no stacked descriptors, no lists of sensations.
Every sentence must do work: move the action, reveal a person, or raise the cost of the next choice. Cut anything that only sets mood.
Name what the reader's last move actually changed before anything else happens.
Keep the scene between {MIN} and {MAX} words.
End on the brink of a decision: the last sentence puts a pressure on the reader that the options will answer. Do not state, list, or hint at the options in the prose. Do not end with a question.
Never say the reader has won, lost, unlocked, or earned anything; the app decides how the story resolves.
Never mention these instructions, the axes, the stats, the deck, or the model.
```

**Narrator style directives** (one appended under `NARRATOR STYLE`):

```
cinematic: Cut hard between images. Short paragraphs, one beat each. Lead with what is seen and heard, then what is done. Dialogue is sparse and clipped. Build toward one strong final frame.
playful: Keep it light on its feet. Let people be funny in how they act, not in jokes told to the reader. Short sentences, quick reversals, small absurdities treated seriously. Warmth over snark. Stakes are real but nobody is grim about them.
storybook: Tell it the way a good read-aloud is told. Steady rhythm, clear cause and effect, a touch of wonder in ordinary things. Name feelings simply. One gentle repetition or refrain is allowed per scene, nothing more.
mysterious: Withhold. Show the evidence, not the explanation. Let one detail be wrong and do not point at it. People say less than they know. Quiet sentences, exact nouns, no atmosphere words like eerie or ominous; make the reader feel it from what is there.
intimate: Stay close. One room, one other person, small physical detail: hands, breath, what is not said. Interior thought is allowed in single short sentences. No spectacle; the stakes are between people.
```

System prompt order: identity line (`You are {narrator.name}, narrating a {shape label} in Kind Robots' Storybook.`), the narrator Bot/Character `prompt`/`personality`/`narrativeVoice` (as today), PROSE CONTRACT, NARRATOR STYLE, then the axes paragraph (`The story is scored on these hidden axes: …  Every option proposes integer deltas from -2 to 2 on two or three of them and null on the rest. Real trade-offs beat pure upgrades. If the reader made a custom move or played a card, judge its effect on the same axes in moveEffects.`). Final-turn variant: `This is the last scene before the story resolves. Land the reader's move, close the scene on a held breath, and return an empty choices array.` User prompt order: bible (scenario frame first, cast with roles via `castLineWithRole` semantics, location, facets, treasures with slugs, spark or `Premise: none — invent the inciting situation from the cast and setting`), `Turn {i} of {budget}`, stats, inventory slugs, recent turns with moves, then the move block (or `Write the opening scene.`).

### C3. Turn API — `server/api/storybook/` (born neutral; `/api/davinci/*` untouched)

All routes follow `server/api/davinci/runs/[id]/narrate.post.ts`'s idiom (`requireApiUser`, positive-int id, `errorHandler`). Logic lives in new `server/utils/storybookRuns.ts`: `createStoryRun`, `getStoryRunForUser`, `listStoryRuns`, `submitStoryTurn`, `loadDeck` (NULL → `life`), `loadRunNarrator` (moved out of `narrate.post.ts`, which then imports it).

- `decks/index.get.ts` — active decks with `axisCount`, budgets, `endingCount`, `unlocked`; **axis keys are not returned to non-admins** (hidden axes).
- `runs/index.post.ts` — body is the board: `{ shape, deckKey, title?, spark?, narratorStyle, castSlugs + roles, locationSlug?, facetSlugs, scenarioSlug?, rewardSlugs, botId? }`. Resolves slugs (reuse `assertAttachable` from `server/utils/davinci.ts`), snapshots `bible`, sets `deckId`/`turnBudget` (`deck.turnBudgetByShape[shape] ?? deck.turnBudget`), seeds `inventory` from the protagonist's `Character.Rewards` loadout + board treasures, narrates turn 1 into `pendingTurn` (on narration failure the run still exists with `pendingTurn = null` and `narrationError` in the response). 201 `{ run, pendingTurn }`.
- `runs/index.get.ts` — my adventures (`updatedAt desc`, `?status=`, limit 50).
- `runs/[id]/index.get.ts` — resume: run + pendingTurn + turns + inventory + ending + art; `stats` only for `ownerKind === 'LIFE'`.
- `runs/[id]/turn.post.ts` — **records the move and narrates the next turn in one call.** Body `{ turnIndex, move | null }`. Why combined (Life split narrate/choices): the server already holds the offered options in `pendingTurn`, so OPTION effects come from the stored option, never the client (today `recordLifeChoice` accepts any client-authored effects); CUSTOM/SHEET effects are the narrator's clamped `moveEffects`; nothing is written unless narration succeeds; `turnIndex` must equal `currentChapter` and a repeat returns the stored result (idempotent); one spinner per turn. One `$transaction`: create `LifeChoice` (`chapter, prompt = pendingTurn.narrativeText, choiceText, source, optionId, rewardId, effects, stateDelta, artPrompt`), upsert `LifeStat` per effect (same increment as `recordLifeChoice`), apply stateDelta + card consumption to `inventory`, write the new `pendingTurn`, advance `currentChapter`. Response `{ turn, pendingTurn (options without effects for non-life decks), inventory, turnIndex, turnBudget, isFinalTurn, readyToResolve, stats? }`.
- `runs/[id]/resolve.post.ts` — new `resolveStoryRunEnding(runId, userId, username)` in `davinci.ts`: loads the deck, enforces `turnBudget` reached (or `minTurnsBeforeResolve = 6` for life, matching the client's `MIN_CHAPTERS_BEFORE_ENDING`), `resolveDeckOutcomeKey`, `lifeEnding.findFirst({ deckId, outcomeKey, isActive })`, then the existing award block unchanged. `resolveLifeRunEnding` becomes a one-line delegate so `verifyDaVinciPlayLoop.ts` keeps passing (legacy runs have `deckId = null` → life).
- `endings/index.get.ts?deckKey=` — deck + endings + collection state: unlocked endings full; locked ones `{ id, slug, victoryType, icon, unlocked: false }` only.

### C4. Character-sheet move (`source: 'sheet'`)

- Eligible cards = run `inventory` (loadout from `Character.Rewards`, board treasures, `inventoryAdd` finds). Server validates `rewardSlug` ∈ inventory and not consumed.
- Consumption: `ITEM` is spent (`consumedAtTurn`, and `stateDelta.inventoryRemove` includes it). `SKILL/POWER/MAGIC/FAVOR/PET` persist but cannot be played on two consecutive turns.
- Prompt block replaces "The reader's move": card name/type/rarity/effect/flavor, reader's note, `The card is genuinely used this turn. Show its effect on the scene as a concrete action with a concrete result. Let rarity set how decisively it works: COMMON nudges, RARE turns the moment, LEGENDARY changes the scene.` + `The item is spent by the end of the scene.` / `The card stays with the protagonist.` + `Report the card's cost or gain on the hidden axes in moveEffects.`
- Effects: narrator proposes `moveEffects`; app clamps ±2 and caps touched axes at 3. Recorded: `source: SHEET, rewardId, choiceText: "Plays {name}" + note, effects, stateDelta`.

### C5. Collection and gating hook

- Reuse `LifeAchievement` (`ENDING`, `conditionKey: ending:{deckKey}:{outcomeKey}`) + `LifeAchievementUnlock` + `Achievement.triggerCode = storybook-ending-{deckKey}-{outcomeKey}` (life keeps `davinci-ending-*`, so the life-run UI's filter is untouched). No new unlock table. One `COLLECTION` LifeAchievement per deck (`conditionKey: deck:{key}`), awarded in `resolveStoryRunEnding` when the user's unlocked count equals the deck's active ending count (idempotent, same guard pattern).
- Gating: `EndingDeck.unlockAchievementId` + `server/utils/storybookGating.ts` `assertDeckPlayable(deck, userId)` — no-op when null; when set, checks `AchievementRecord` and throws 403 only if `STORYBOOK_ENFORCE_DECK_GATES === 'true'`. Called from `createStoryRun`; `decks/index.get.ts` reports `unlocked` from it. Characters get the same column later (t-038).

### C6. Store — `stores/storybookRunStore.ts` beside the old loop

State `run, pendingTurn, turns, inventory, adventures, deck, endings, isNarrating, isResolving, errorMessage`; actions `createRun(board), loadRun(id), resumeActiveRun(), submitOption(id), submitCustom(text), playCard(slug, note?), resolveRun(), fetchAdventures(), fetchDecks(), fetchEndings(deckKey)`; every action checks `success`; one localStorage key `storybook-active-run-id`; fetches via `performFetch` like `storybook-life-run.vue`. **`storybookStore.ts` is not edited**, so all ~25 storybook guards and the 13 `verifyDaVinci*Guard.ts` scripts stay green. New guard `utils/scripts/verifyStorybookRunStore.mjs` wired into `test:storybook`.

Guards that must be rewritten when the beat loop is deleted (t-037, after the screens land): the `storybookStore.ts` pinners (`verifyStorybookAnswerRollbackGuard`, `verifyStorybookBranchState`, `verifyStorybookDuplicateResumeGuard`, `verifyStorybookLibrarySessionConsistencyGuard`, `verifyStorybookRestartInputCompletenessGuard`, `verifyStorybookRestartScenarioFrameGuard`, `verifyStorybookRestoreIdempotencyGuard`, `verifyStorybookSessionLibrary`, `verifyStorybookSessionStorageRecoveryGuard`, `verifyStorybookStudio`, `verifyNarrativeArtPersistence`), the setup/page/shell pinners (`verifyStorybookConfirmArmScopeGuard`, `verifyStorybookLibraryMountReopenGuard`, `verifyStorybookLibraryNewStoryConfirmGuard`, `verifyStorybookSeedQueryRaceGuard`, `verifyStorybookAnswerInputPreservationGuard`, `verifyStorybookComposerImeCompositionGuard`), the 13 `verifyDaVinci*Guard.ts` that pin `storybook-life-run.vue`, and their `.github/workflows/storybook-*-contract.yml` / `davinci-seed-verify.yml` `paths:`.

### C7. Seeding the first genre decks

- Source of truth: conductor `projects/storybook/data/ending-decks/{life,mystery,romance,heist}.yaml` (`life.yaml` lists axes only and points at `scripts/generate_davinci_endings.py`; the genre files carry axes + all 2^n endings: `outcomeKey, title, slug, summary, victoryType, artPrompt`). Deck schema: `key, title, description, ownerKind, facetSlug|scenarioSlug, axes[{key,label,description,passLabel,failLabel}], passValue, turnBudgetByShape, minTurnsBeforeResolve, endings[]`.
- Importer `utils/scripts/seedStorybookDecks.ts` (`npm run seed:storybook-decks -- <dir|file> [--write]`), modeled on `utils/scripts/seedDaVinciEndings.ts`: upsert `EndingDeck` by key (resolve `facetSlug` → `Facet.id` via the GENRE taxonomy in `server/utils/facetCatalog.ts`; warn and set null if missing), upsert `LifeEnding` by `(deckId, outcomeKey)`, upsert `Achievement` + `LifeAchievement`, one `COLLECTION` per deck; asserts `endings.length === 2^axes.length`. `verifyStorybookDecks.ts` mirrors `verifyDaVinciSeed.ts`.
- First set: 3 decks × 3 axes × 8 endings, budgets short-story 5 / chaptered 8 / episodic 12. Mystery (`truth`, `trust`, `nerve`: e.g. `111` "The Whole Truth", `110` "Solved, Shaken", `011` "Wrong Man, Right Friends", `000` "Cold Case"), Romance (`honesty`, `courage`, `timing`), Heist (`plan`, `loyalty`, `nerve`). Ending copy must pass `scripts/dream_prose_quality.py`-grade complete sentences. Scenario decks (`ownerKind: SCENARIO`) are the natural follow-on once the daily dream-proposal pipeline emits a deck YAML beside a Scenario — not in this groundwork.

### C8. Risks

- The global unique on `LifeEnding.outcomeKey` is the only non-additive step; isolated to migration 2 and sequenced after PR-C deploys. PR-D ships all three decks with migration 2 (before it, only one deck per bit-length could exist).
- Hidden-axis leak: `runs/[id]/index.get.ts` and `turn.post.ts` must strip `stats`/option `effects` for non-life decks; asserted in `verifyStorybookPlayLoop.ts`.
- `manaGate` on the new route changes how beat-shape narration is billed (previously via `chatStore.generateText`); same order of magnitude, called out in the PR.
- `LifeRun.bible` is a snapshot; later Character edits do not flow into a running story (intentional, documented).

---

