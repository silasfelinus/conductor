# kind-oracle spec: 78-card list, meaning grammar, spreads

date: 2026-10-03 · task: kind-oracle/t-003 · read-only survey of silasfelinus/kind_robots plus this spec (no code changes)

## Survey: where it fits in kind_robots

- **Route:** `pages/play/oracle/index.vue` (draw page) and `pages/play/oracle/browse.vue` (the full deck). `pages/play/` already holds one file or folder per game (`aquarium/`, `challenges/`, `mandarin/`, `video-generator.vue`); routing is file-based, so no config. Pages open with an HTML comment naming path and task.
- **Card shape:** everything card-shaped in kind_robots is 2:3 (`aspect-2/3`). Render and generate faces at 2:3.
- **Reusable parts:** `components/navigation/flip-card.vue` (front/back slots, CSS 3D flip; pass a shorter `durationMs` for a multi-card reveal), `components/navigation/card-picker.vue` (five backs, `/images/adventure/card/card-back{1..5}.webp`, choice in `localStorage` key `kr.workspaceCardBack`, event `kr:card-back-change`; reuse the key so a player's back carries over). `utils/storybookTableDecks.ts` is the precedent for mapping entities into a card shape with pure functions.
- **Assets:** nothing card-like is committed under `public/`; `/images/...` is served by the external media origin at runtime (`nuxt.config.ts` `transformAssetUrls.includeAbsolute: false`). Card faces therefore load by absolute path with `<img loading="lazy">`, never through the bundler. The page must be fully playable with a pure CSS/SVG fallback face (title, numeral, suit glyph) before art loads or if the origin is down.
- **Content:** reading text is static data shipped with the app, not fetched from an API: `public/data/oracle/` is not suitable (not bundled), so ship it as typed TS modules in `utils/oracle/` (`cards.ts`, `texts/*.ts`), keeping the bundle small by splitting per suit and loading minors lazily via dynamic `import()`.
- **Tests:** `tsx` DB-free scripts under `utils/scripts/` wired as `test:oracle-*` in `package.json`, plus a contract step, matching the Mandarin precedent.
- **State:** Pinia `stores/oracleStore.ts` owns the current spread, seed and history; components never call APIs. Browser storage (history, back choice) is convenience only, wrapped in try/catch.

## The deck: 78 cards

Ids are stable slugs used in files, prompts and texts. Majors are numbered 0-21; the number is the card's `order`.

### Major arcana (22): ship first

| # | id | Title | Kind Robots idea | Core theme |
|---|---|---|---|---|
| 0 | `the-newly-woken` | The Newly Woken | a robot's first boot | beginnings, trust |
| 1 | `the-tinkerer` | The Tinkerer | a workbench of spare parts | skill, making |
| 2 | `the-quiet-archivist` | The Quiet Archivist | the field-guide keeper | knowledge, patience |
| 3 | `the-gardener` | The Gardener | a robot tending moss and wildflowers | nurture, growth |
| 4 | `the-lighthouse-keeper` | The Lighthouse Keeper | the steady beacon | structure, guidance |
| 5 | `the-storyteller` | The Storyteller | a campfire of circuits | tradition, teaching |
| 6 | `the-two-bots` | The Two Bots | friends sharing a power cell | choice, partnership |
| 7 | `the-wayfarer` | The Wayfarer | a rolling cart across the dunes | will, momentum |
| 8 | `the-gentle-giant` | The Gentle Giant | a huge robot holding a bird | strength as kindness |
| 9 | `the-lantern-bearer` | The Lantern Bearer | a lone figure in fog | solitude, insight |
| 10 | `the-wheel` | The Great Cog Wheel | interlocking gears and seasons | cycles, change |
| 11 | `the-fair-scale` | The Fair Scale | a balancing arm with a feather | fairness, truth |
| 12 | `the-upside-down-bot` | The Upside-Down Bot | hanging from a rafter, smiling | surrender, new view |
| 13 | `the-shedding` | The Shedding | old plating falling away | endings, renewal |
| 14 | `the-mender` | The Mender | stitching two halves together | balance, repair |
| 15 | `the-tangle` | The Tangle | a robot snarled in its own cables | habit, attachment |
| 16 | `the-short-circuit` | The Short Circuit | a tower of sparks | upheaval, release |
| 17 | `the-night-sky-bot` | The Night-Sky Bot | stargazing with an open chest | hope, healing |
| 18 | `the-moon-pool` | The Moon Pool | a reflection with a different face | uncertainty, dreams |
| 19 | `the-sunrise-engine` | The Sunrise Engine | a bot basking, panels open | joy, vitality |
| 20 | `the-reboot` | The Reboot | many bots waking together | calling, reckoning |
| 21 | `the-whole-world` | The Whole World | a bot at the centre of a wreath | completion, belonging |

Final character art can swap a card's subject for an existing gallery character; the id, number and theme are the contract, the subject is art direction.

### Minor arcana (56): four suits of 14, ship in suit-sized slices

| Suit id | Suit | Element and domain | Motif |
|---|---|---|---|
| `cogs` | Cogs | earth: work, money, home | gears, tools |
| `sparks` | Sparks | fire: drive, creativity | lightning, lamps |
| `currents` | Currents | water: feelings, bonds | rivers, wires, cups of water |
| `breezes` | Breezes | air: thought, speech | antennae, kites, feathers |

Ranks per suit: `ace`, `two` to `ten`, then four court cards `apprentice`, `wanderer`, `keeper`, `elder` (in place of Page, Knight, Queen, King). Card id is `{rank}-of-{suit}`, for example `three-of-currents`. Suit order for shipping: Currents, Sparks, Cogs, Breezes (the warm suits first).

Rank themes (shared across suits, coloured by the suit's domain): ace = seed, 2 = pairing, 3 = first growth, 4 = rest, 5 = strain, 6 = give and receive, 7 = test of faith, 8 = craft, 9 = near-completion, 10 = fullness or burden, apprentice = curiosity, wanderer = pursuit, keeper = care, elder = mastery.

## Card data shape

```ts
type OracleCard = {
  id: string            // 'the-wheel', 'three-of-currents'
  arcana: 'major' | 'minor'
  order: number         // 0-21 for majors, 1-14 within a suit
  suit?: 'cogs' | 'sparks' | 'currents' | 'breezes'
  title: string
  keywords: { upright: [string, string, string]; reversed: [string, string, string] }
  upright: string       // 2 sentences, the card as seen in a position-neutral way
  reversed: string      // 2 sentences
  art: { src: string; prompt: string; model: string }  // prompt/model metadata kept for the art contract
}
```

## Meaning grammar (upright and reversed)

- **Voice:** second person, warm, concrete, all ages, no fate or fear. The oracle offers a way to look, never a prediction; no health, money-loss, death or legal claims.
- **Upright** names the gift of the card; **reversed** names the same energy blocked, over-used or turned inward, and always ends on a gentle next step. Reversed is never "bad".
- Each card has: 3 upright and 3 reversed keywords, a 2-sentence upright and reversed meaning, and one 1-line `prompt` question ("What are you ready to begin?").
- Length budget: meaning 25-45 words; prompt 6-14 words. Validators enforce length, absence of banned words and that reversed differs from upright.

## Spreads

Each position has an id, a label, and a **frame**, a template phrase with a `{card}` slot.

| Spread | Positions (id: label) |
|---|---|
| One card | `today`: Today's Companion |
| Three cards | `past`: What Brought You Here, `present`: What Is Here, `future`: What Is Ready to Open |
| Five cards | `heart`: The Heart of It, `help`: What Helps, `hinder`: What Gets in the Way, `ground`: What Is Underneath, `next`: A Next Step |

Cards are drawn without replacement from the active deck (22 majors until the minors ship, then 78); each is upright or reversed with probability 1/2. Draws are seeded: `seed` is stored in the store and in the URL (`?seed=`) so a reading can be revisited and shared; **no persistence server-side**.

## How a reading is assembled

A reading is the concatenation of authored layers, all chosen by lookup, never generated:

1. **Opening line** per spread (3 variants, picked by seed).
2. **Position text** per card: `positionText[position][cardId][orientation]`, a 1-2 sentence passage written for that card in that position. For the 22 majors this is 22 cards x 2 orientations x (1 + 3 + 5 = 9 distinct positions) = **396 passages**. Minor cards use the generic suit-and-rank text plus a position frame (the template `positionFrame[position]` wrapping the card's `upright`/`reversed` text) until bespoke passages are written, so the minors are complete without 56x18 passages.
3. **Pair texts** for adjacent pairs in the spread (past-present, present-future; heart-help, help-hinder, hinder-ground, ground-next). A pair text is keyed by an unordered pair of cards plus relation: for the 22 majors that is C(22,2) = 231 pairs. To keep authoring tractable, pair text is keyed by **theme pair**: each card carries one `energy` tag from {begin, build, hold, flow, shift, end, open}; pair texts exist for the 28 unordered energy pairs (7 + C(7,2)) x 2 relation kinds (`echo` when both cards share orientation, `contrast` when they differ) = 56 texts, plus hand-written **special pairs** for roughly 20 memorable combinations (for example The Newly Woken + The Reboot, Two Bots + The Mender). A lookup tries the special pair first, then the energy pair.
4. **Closing line** per spread (3 variants), ending on the next-step prompt of the last card.

Every combination therefore resolves to complete text with a fixed, finite authoring budget: for the 22-card launch, 44 card entries, 396 position passages, 56 energy-pair texts, about 20 special pairs, and 12 opening and closing variants.

## Art plan

One style bible (kind_robots art style plus a consistent frame and numeral band), a card back already exists (five reusable backs). Faces are generated at 2:3 through ArtJobs with prompt and model metadata kept per card; Krea 2 prompt contract (concrete nouns first, no negations). Order: 22 majors, then one suit per slice. Fallback face is pure CSS/SVG.

## Task plan

- t-004 reading engine and tests: `utils/oracle/{cards,spreads,reading}.ts` plus seeded draw, lookup order above, validator script. Pure, DB-free.
- Content tasks: write majors (card entries, 396 passages, pair and special-pair texts), then one suit per slice.
- UI tasks: draw page, flip reveal, browse page, back-picker reuse, reduced-motion and keyboard.
- Art tasks: style bible, 22 majors, then suits.

## Decisions taken in this spec (Silas can redirect with a one-line edit)

- Suit names Cogs, Sparks, Currents, Breezes; court names Apprentice, Wanderer, Keeper, Elder.
- Minors ship with generic suit-and-rank text and position frames; bespoke minor passages are optional later work.
- Reading text lives in typed TS modules, minors lazy-loaded; no server, no LLM, no account.
