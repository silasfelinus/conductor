# Wishmaster Scope Audit

> **needs-human** — Do NOT implement Wishmaster based on this document alone.
> This is a research artifact. All implementation decisions require Silas review.

## What `Composition` Was Designed For

`Composition` is a single-table recipe model that assembles content from existing kind_robots
entities into a paired output (narrative text + art prompt / image).

### Fields

| Group | Fields | Notes |
|---|---|---|
| Identity | `id`, `title`, `description`, `label` | Display metadata |
| Mode | `mode` (`'narrative'` \| `'art'` \| `'both'`) | Controls which outputs are produced |
| Flags | `isPublic`, `isMature`, `isActive`, `designer` | Standard visibility flags |
| Ingredient FKs | `characterId`, `dreamId`, `scenarioId`, `rewardId` | All optional; pull real records |
| Freeform overrides | `characterBlurb`, `dreamBlurb`, `scenarioBlurb`, `rewardBlurb` | Used when no FK set, or to override the FK record's description |
| Dual outputs | `narrativeText` (Text), `artPrompt` (Text), `imagePath` (VarChar) | Narrative text from the storytelling pass; art prompt / saved image from the generation pass |
| Relations | `userId`, `artImageId` (@unique) | One saved ArtImage per Composition |

### Intended flow (as built)

1. User (or agent) creates a Composition, picking ingredient FKs and/or writing freeform blurbs.
2. Server assembles a context block from whichever ingredients are present.
3. If `mode` includes `'narrative'`: LLM writes `narrativeText`.
4. If `mode` includes `'art'`: LLM writes `artPrompt`; generation endpoint produces and saves an `ArtImage`.
5. The Composition row stores both outputs; reactions and sharing flow from there.

### What it does well

- Ingredient selection is flexible: any mix of real FK records + freeform text overrides.
- Dual-output mode is already wired (single row holds both narrative and art).
- `@unique` on `artImageId` enforces one-image-per-composition cleanly.
- Reactions, user attribution, and visibility flags are inherited from the standard pattern.

---

## Gaps for a "Wish → Assembled Project" Flow

Wishmaster's goal is: *user speaks a desire → bot interprets it → a full Dream (with Characters,
Scenarios, Rewards, ArtImages, and an ArtCollection) is assembled and saved*. `Composition` covers
one slice of that (single narrative + art pass), but the wish-fulfillment flow needs several things
it does not currently have.

### Gap 1 — No link to the output Dream

`Composition` produces `narrativeText` + one `ArtImage`, but has no `dreamId` output FK — only an
*input* `dreamId` (source ingredient). After a wish is fulfilled, the resulting Dream (the assembled
project) has no record of which Composition produced it, and the Composition has no pointer to the
Dream it spawned.

**Minimal addition:** Add `outputDreamId Int? @unique` on `Composition` + `SourceComposition
Composition? @relation("CompositionOutputDream")` on `Dream`.

### Gap 2 — No multi-step / pipeline state

A wish that produces a Dream with three Characters, two Scenarios, and five ArtImages requires
multiple sequential generation passes. `Composition` has no concept of pipeline state (`pending` /
`in_progress` / `complete` / `failed`), no step ordering, and no way to resume after a partial run.

**Minimal addition:** A `status` enum (`DRAFT | PENDING | RUNNING | DONE | FAILED`) + `stepLog
Json?` for audit trail. Alternatively, treat each generation pass as a child `Composition` row
(one per output entity) linked by a shared `wishId` — simpler, composable with existing tooling.

### Gap 3 — No "wish" text input field

The user's original freeform wish ("I want a pirate adventure set in 1720 with a female captain")
has nowhere to live. `description` is 512 chars and doubles as display copy. `dreamBlurb` is the
input ingredient override, not the user's intent.

**Minimal addition:** `wishText Text?` — the raw unmodified user input, stored separately from
agent-interpreted blurbs.

### Gap 4 — Ingredient set is fixed at four types

`Composition` hard-codes four ingredient slots (character, dream, scenario, reward). Wishmaster
may need to assemble arbitrary combinations: e.g. a wish that adds a Bot, a Theme, or a
newly-created ArtCollection. Adding new ingredient types currently requires schema migrations +
new FK columns.

**Minimal addition:** A `WishIngredient` join table (`compositionId`, `entityType` enum, `entityId`
Int, `blurb Text?`) would make ingredients open-ended without repeated migrations. This is the
bigger architectural lift and the one that most needs human design review before implementing.

### Gap 5 — No user-facing confirmation / approval step

The current flow goes straight from input to generation. Wishmaster should show the user the
assembled ingredient list and proposed Dream shape before firing expensive generation calls.
There is no `approvedAt` timestamp or `userApproved Boolean` field to gate execution on.

**Minimal addition:** `userApproved Boolean @default(false)` + `approvedAt DateTime?` on
`Composition` (or on a parent wish record).

### Gap 6 — Economy is not wired

Generation costs mana. Bounty economics (house pays both poster and fulfiller) apply when a wish
is fulfilled by another user. Neither mana deduction nor bounty attribution is handled at the
Composition layer — they happen ad-hoc in the art/text generation endpoints.

**Minimal addition:** A `manaCharged Int?` + `bountyId Int?` column so the Composition row is the
reconciliation anchor. Actual mana / karma writes remain `needs-human` gated.

---

## Minimal Additions Summary

In priority order for MVP Wishmaster (smallest surface, biggest unlock):

1. **`wishText Text?`** on `Composition` — captures raw user intent.
2. **`status` enum** (`DRAFT|PENDING|RUNNING|DONE|FAILED`) + `stepLog Json?` — pipeline state.
3. **`outputDreamId Int? @unique`** on `Composition` — links fulfillment to the spawned Dream.
4. **`userApproved Boolean @default(false)` + `approvedAt DateTime?`** — confirmation gate.
5. **`manaCharged Int?` + `bountyId Int?`** — economy reconciliation anchor.
6. **`WishIngredient` join table** — open-ended ingredient set (biggest schema change; needs separate design review).

Items 1–5 are additive single-column additions that can land in one migration with no breaking
changes. Item 6 is an architectural decision; skip it for MVP and use the existing four FK slots
with freeform overrides.

---

## What NOT to Do

- Do not rename or remove any existing `Composition` fields — other code reads them.
- Do not implement live mana/bounty writes without the `needs-human` review.
- Do not auto-create Dreams, Characters, or Scenarios from a wish without user confirmation
  (Gap 5 above).
- Do not hardcode Wishmaster logic inside the Composition CRUD routes — add a separate
  `server/api/wishmaster/` namespace.

---

*Authored by Claude agent on 2026-06-29. Reviewed by: needs-human.*
