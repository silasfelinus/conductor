# Da Vinci AI-Narration Layer — Design Brief

**Task:** davinci/t-015 — kaizen from t-014 (kind_robots PR #645). The
play-loop API (`docs/notes/davinci-play-loop-api.md`) and the ending/
achievement seed (`davinci-ending-{outcomeKey}` triggerCodes) are both built
and live, but nothing generates the chapter prose, choice text, or effect
deltas a player would actually see. This is the design for that layer.

## Scope

This layer is a caller of the play-loop endpoints, not a fifth endpoint and
not a new durable-state owner. It:

- reads the current run (`GET /api/davinci/runs/:id`) to get chapter,
  protagonist, genre, seed, and accumulated `LifeStat` values,
- asks a narrator (Bot or Character) for the next chapter's prose + choice
  options + proposed effect deltas + an optional art prompt,
- validates that response against a strict schema and app-owned bounds,
- lets the player pick (or the client interprets freeform text into one of
  the offered choices — see "Freeform input" below),
- calls `POST /api/davinci/runs/:id/choices` with the *validated* effects —
  the narration layer never writes `LifeChoice`/`LifeStat` rows directly.

It does not own chapter advancement, stat storage, resolution, or award
logic — those stay exactly where they are in `server/utils/davinci.ts`.

## Narrator selection

Reuse `GET /api/narrators/[type]/[slug]` as-is (already normalizes both Bot
and Character into one narrator shape with `prompt`, `personality`,
`narrativeVoice`, `botIntro`). A `LifeRun` already carries optional
`botId`/`characterId` links (`prisma/schema.prisma:1567-1568`):

- If `LifeRun.botId` is set, resolve `bot/{slug}`.
- Else if `LifeRun.characterId` is set, resolve `character/{slug}`.
- Else fall back to the existing `defaultNarratorBotId` (433) the narrator
  route already uses for character-less lookups.

No new narrator-selection endpoint or table — this is a two-branch lookup at
the top of the narration call, not a new subsystem.

## Chapters, choices, and resolution timing

- **Choices per chapter:** 2–4, narrator's discretion within that band
  (enforced by schema `minItems`/`maxItems`, not a fixed constant) — mirrors
  the pass/fail-by-threshold design where different runs can take different
  numbers of chapters to swing all ten dimensions.
- **Chapter count:** no fixed total. The client offers a player-visible "end
  the run" action any time after chapter 6 (raised from the original design
  default of 3 — see t-024 below, simulation-backed: at chapter 3 an average
  of 4.2/10 dimensions had never been touched by any choice at all); the
  narrator is *not* told when to end things — see "First build slice" in
  `design-brief.md`, which already scopes the run shell as minimal.
- **Resolution timing:** unchanged from the existing API — the client calls
  `POST /api/davinci/runs/:id/resolve` explicitly (player-triggered "end my
  life" action), not something the narration layer decides or calls
  automatically. Keeps the same "app owns the moment of truth" boundary the
  play-loop doc already states for `/resolve`.

## Request/response contract

```ts
// server/utils/davinciNarration.ts (new — narration-only, imports
// DAVINCI_DIMENSIONS from davinci.ts but adds no state of its own)

interface DaVinciNarrationRequest {
  runId: number
  chapter: number
  protagonistName: string | null
  genre: string | null
  seed: string
  narrator: {
    name: string
    personality: string | null
    narrativeVoice: string | null
    prompt: string | null // system-prompt fragment from the Bot/Character row
  }
  statsSoFar: Record<string, number> // current LifeStat rows, DAVINCI_DIMENSIONS-keyed subset
  recentChoices: Array<{ chapter: number; choiceText: string; resultText: string | null }> // last 3, for continuity
}

interface DaVinciChoiceOption {
  id: string // stable within this chapter's response, e.g. "a" | "b" | "c"
  choiceText: string
  effects: Partial<Record<DaVinciDimension, number>> // proposed deltas, -2..+2
}

interface DaVinciNarrationResult {
  narrativeText: string
  choices: DaVinciChoiceOption[]
  artPrompt: string | null
  milestoneCandidate: string | null // narrator's guess at a resonant ending theme — display-only, never awarded from this field
}
```

`milestoneCandidate` is carried through for UI flavor (e.g. a small
"heading toward..." hint) but the resolver in `davinci.ts` never reads it —
outcome math stays 100% derived from stored `LifeStat` rows, per the design
brief's existing rule that AI "can help lead users toward achievements... but
should not silently award achievements or invent durable state."

## Effect derivation from `DAVINCI_DIMENSIONS`

The narrator proposes deltas; the app clamps and validates before they ever
reach `POST /api/davinci/runs/:id/choices`:

1. Reject any key not in `DAVINCI_DIMENSIONS` (ten fixed dimensions —
   `server/utils/davinci.ts:12-23`). A narration response that invents an
   eleventh stat name is a schema violation, not a new stat.
2. Clamp each proposed delta to `[-2, 2]`. `LifeStat` values are unbounded
   in storage today (upsert-increment, no ceiling in `davinci.ts`), but the
   narration layer is the one place that should enforce a reasonable
   per-choice swing — the ending only needs `>= DAVINCI_PASS_VALUE (1)` to
   pass a dimension, so large single-choice swings would make individual
   narrator responses overpowered relative to a full run.
3. A choice option may omit dimensions entirely (an option can be flavor
   with zero mechanical effect) — validate `effects` as optional per-key,
   not required-all-ten.
4. The chosen option's `effects` object is passed through unchanged as the
   `effects` body param on `POST /api/davinci/runs/:id/choices` — no
   separate derivation step at that call site; validation already happened
   when the narration response was received.

## Freeform input

The play-loop doc doesn't currently take freeform text at the choices
endpoint, and this layer doesn't add a second choices-recording path. Two
options for how the client offers "type your own":

- **Recommended for the first build slice:** don't build it yet. Structured
  choice buttons only. `DaVinciNarrationResult.choices` already gives 2-4
  concrete options every chapter, which is enough for a playable MVP and
  keeps the validation surface small (a small enum, not an
  interpret-arbitrary-text pass).
- **Deferred:** if freeform is added later, it becomes a *second* narrator
  call — one that takes the player's typed text plus the same chapter
  context and returns the same `DaVinciNarrationResult` shape (interpreting
  the freeform text into a synthesized `choiceText` + `effects`), so the
  validation and effect-clamping path is identical either way. This keeps
  freeform from becoming a parallel state-mutation route.

## Validation and safety (app-owned enforcement)

Follow the existing `requestOpenAiReview` / `validateGeneratedPayload`
pattern in `server/utils/wonderLabReviewDraftGenerator.ts` rather than
inventing a new one:

- Call the model with `response_format: { type: 'json_schema', json_schema:
  { strict: true, schema: <DaVinciNarrationResult JSON Schema> } }`.
- Parse and re-validate server-side anyway (`validateGeneratedPayload`-style
  function) — `strict: true` constrains the model's output shape but the
  app still checks value ranges (dimension-key allowlist, delta clamp,
  choice count 2-4, non-empty `narrativeText`) before anything reaches the
  play-loop endpoints.
- Same timeout/abort pattern (`AbortController` + a serverless-safe
  timeout) — narration calls are synchronous from the player's point of
  view (they're waiting for the next chapter), so this needs a tighter
  budget than the async WonderLab review generator, not a looser one.
- On validation failure: retry once with the same request (models
  occasionally emit a truncated/invalid document even under strict mode),
  then surface a "the narrator is having trouble" error to the client
  rather than falling back to a synthetic chapter — a broken chapter is
  worse than a visible retry prompt.

## Art prompt integration

`artPrompt` flows into the existing `LifeRunArt` model
(`prisma/schema.prisma:1703-1718`), which already has the scene-type enum
this needs (`MOMENT` fits a chapter scene; `THRESHOLD`/`ENDING_ICON`/
`ENDING_HERO` are separately triggered by dimension-threshold crossings and
the resolve flow, not by every chapter). The narration layer only proposes
the prompt string; actual image generation stays wherever the rest of Kind
Robots' art-generation queue already lives — this spec does not add a new
generation path.

## Relationship to Storybook's narrator pattern

Per `storybook-boundary-comparison.md`, narration prompt assembly is the
first concrete piece both projects could share (item 1 under "What they
genuinely could share — later"), but Storybook has no schema yet, so there
is nothing to extract from today. This spec is written so extraction stays
possible without a rewrite:

- The `(narrator config + seed objects + state snapshot + recent history) →
  structured response` shape here is generic — it doesn't reference
  `LifeRun` fields directly in the request contract, only plain values
  (`protagonistName`, `genre`, `seed`, `statsSoFar`, `recentChoices`).
- The one Da Vinci–specific piece is the `DaVinciDimension`-keyed `effects`
  map. If/when a shared utility is extracted, that becomes a generic
  `Record<string, number>` at the utility boundary, with each caller
  (Da Vinci, later Storybook) supplying its own allowed-keys validator.
- Per the boundary doc's standing rule, this stays inside
  `server/utils/davinciNarration.ts` until Storybook's own m1 schema lands
  and there's real duplicated code to extract from, not before.

## First build slice (what unblocks a playable run UI)

1. `server/utils/davinciNarration.ts`: request builder + OpenAI call +
   `validateGeneratedPayload`-equivalent, following the pattern above.
2. `POST /api/davinci/runs/:id/narrate` (new, thin route wrapping the util):
   loads the run + narrator + recent choices, calls the util, returns
   `DaVinciNarrationResult`. Does not itself write anything — the client
   still calls `/choices` and `/resolve` as separate steps, same as today.
3. Minimal client run screen: chapter text, 2-4 choice buttons, an "end my
   life" button gated on chapter >= 3, wired to the existing three
   play-loop endpoints plus the new `/narrate` route.
4. JSON Schema for `DaVinciNarrationResult`, generated from the TS interface
   above (or hand-written once and kept in sync — this repo doesn't have a
   ts-to-json-schema pipeline yet, so hand-written + a schema/type parity
   test is the pragmatic choice for the first slice).

Explicitly deferred past the first slice: freeform choice input, the
"heading toward..." `milestoneCandidate` UI treatment, and the shared
Storybook narration utility.

## Open question for Silas

The per-choice effect clamp (`[-2, 2]`) and the "offer end-run after chapter
3" rule above are both design defaults, not values pulled from an existing
spec — flag if either should be tuned once real playtesting data exists
(this doc's defaults are meant to be revisited after the first build slice
plays a few live runs, not treated as final).

---

## Implementation status (added 2026-07-31, davinci/t-016)

**Built.** kind_robots commit `fa7db9c` implements the "First build slice"
section above: `server/utils/davinciNarration.ts`, `POST /api/davinci/runs/:id/narrate`,
and the run-screen wiring in `components/conductor/davinci-page.vue`. Contract
coverage lives in `utils/scripts/verifyDaVinciNarration.ts`
(`npm run test:davinci-narration`, 35 checks, wired into `contract-tests.yml`).

Two deliberate deviations from this document, both forced by OpenAI strict mode
rather than by preference:

1. **`effects` is not an optional-key map.** Strict mode forbids optional
   properties, so all ten dimensions are declared `required` and typed
   `["integer", "null"]`. Null means "this choice does not move that dimension"
   and is dropped during validation, which preserves this spec's rule that a
   choice may be pure flavor with zero mechanical effect.
2. **Bounds are enforced server-side only.** `minimum`/`maximum`/`minItems`/
   `maxItems` are omitted from the schema — strict-mode support for them is
   uneven — and the `[-2, 2]` clamp and 2–4 choice band are enforced in
   `validateNarrationPayload` instead. This spec already required that
   re-validation, so nothing is weakened; the schema just stops carrying
   bounds it cannot be relied on to apply.

One deviation of convenience: narrator selection reads the Bot/Character rows
through prisma directly rather than calling `GET /api/narrators/[type]/[slug]`
over HTTP from inside a server util. Same two-branch `botId → characterId →
default bot 433` order, same columns, same normalized shape — just no self-HTTP
hop.

**The open question above is resolved (davinci/t-024, 2026-08-15).** Simulated
20k+ runs against the actual production constants and effect distribution
(`NARRATION_EFFECT_MIN`/`MAX` in `davinciNarration.ts`,
`MIN_CHAPTERS_BEFORE_ENDING` in `davinci-page.vue`). Findings: the `[-2, 2]`
swing is not the driver of early lock-in — `DAVINCI_PASS_VALUE` is 1, so any
single nonzero positive touch already passes a dimension regardless of
whether the max swing is 1 or 2 — left unchanged. The real lever is chapter
count: at the original chapter-3 gate, an average of 4.2/10 dimensions had
never been touched by any choice (guaranteed-fail, not a player decision);
raised the gate to chapter 6 (~1.8/10 untouched on average) so a real spread
of dimensions gets a chance to move before a player can lock in an ending.
Both remain single constants, so further tuning is still a one-line change.

Still deferred, unchanged: freeform choice input, the `milestoneCandidate`
UI treatment beyond a one-line hint, `LifeRunArt` generation from the proposed
`artPrompt` (the narrator returns the string; nothing consumes it yet), and the
shared Storybook narration utility.
