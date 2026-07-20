# Wishmaster Interface Design — wish → costed plan → assembled output

Task: wishmaster/t-002
Status: design doc, **not an implementation authorization** — same needs-human posture as `scope.md`.
Builds on: `scope.md` (Composition model audit + Decisions, Silas 2026-07-04) and
`projects/kind-robots/PROJECT-CREATION.md` Surface 3 (LLM-driven project creation).

---

## 0. Schema reality check (read this before designing against `scope.md`)

`scope.md`'s Decisions section says the MVP schema additions (items 1–5: `wishText`, `status`/
`stepLog`, `outputDreamId`, `userApproved`/`approvedAt`, `manaCharged`/`bountyId`) "shipped to
Composition in kind_robots PR #87; Silas migrates manually."

Verified against `kind_robots` `main` today (2026-07-20):

- **No `Composition` model exists in `prisma/schema.prisma`.** A repo-wide search for
  `Composition` in the schema returns zero matches.
- **PR #87's actual diff does not touch a `Composition` model at all**, despite its title
  ("One-swoop merge: Challenge Center + KARMA_LIVE + **Wishmaster** + Da Vinci schema") and body
  claiming item 3 was "Wishmaster fields on Composition." The merged diff (5 changed files) is:
  the Challenge Center migration + schema, the `KARMA_LIVE = true` flip, and two bounty-route
  comment updates. No `wishText`/`status`/`stepLog`/`outputDreamId`/`userApproved`/`approvedAt`/
  `manaCharged`/`bountyId` field, and no Da Vinci `LifeRun` family of models, appear anywhere in
  that diff either — both apparently described work that didn't make it into the merged commit.
- **`Dream.dreamType` has no `PROJECT` value.** Per the July 2026 Dream/Project/Facet split
  (noted in `CONTROL.md`), "project-shaped wish → PROJECT Dream" from `scope.md`'s Decisions is
  now stale: projects are the standalone `Project` model (`/api/projects`), not a `Dream` variant.
  `PROJECT-CREATION.md` Surface 3 (already written, 2026-07-12) reflects the corrected shape and
  is what this doc designs against for the project-output path.
- `DreamType` does carry a `WISH` value already, with no code anywhere referencing it — status
  unclear, possibly a placeholder from early planning. Worth a one-line question to Silas rather
  than assuming it's load-bearing.

**Net effect on this design:** the Composition model itself — not just the five extra fields —
still needs to be created. Nothing about the interface design below changes because of this
(the flow is the same either way), but **the schema task is not "add fields to an existing table,"
it's "create the table."** Flagged as an open item in §7; do not schedule "just add the columns"
as the next task.

---

## 1. Actors and entry surface

Wishmaster is a `Bot` record (existing model, no schema change needed): `BotType` free-text field
distinguishes it from other bots the same way narrator/companion bots already work.  Wishes reach
it through the same chat surface every other Bot uses (`Bot.Chats[]`), so no new input widget is
required — voice (Alexa/voice-lab), the in-app chat panel, and any future API caller all funnel
through one `POST` to the bot's chat endpoint. This reuses `Bot.narrativeVoice` /
`Bot.sampleResponse` for tone, matching the "one brain, two output sizes" framing from `scope.md`'s
Decisions.

---

## 2. Flow overview

```
wish text (chat/voice)
   │
   ▼
① Intent parse  →  size classification: SMALL vs PROJECT
   │
   ▼
② Plan assembly (ingredients + output shape)
   │
   ▼
③ Cost estimation (mana, via existing manaCost.ts estimators)
   │
   ▼
④ Consent screen — user reviews plan + cost, approves/edits/cancels
   │
   ▼
⑤ Pipeline execution (status state machine, resumable)
   │
   ▼
⑥ Output: Composition row (SMALL)  |  Project + roadmap scaffold (PROJECT)
```

Steps ①–④ are synchronous and cheap (no generation calls, no mana spent) so a user can iterate on
plan wording for free before committing. Step ⑤ is the only stage that spends mana or writes
durable non-draft records, and it never starts before step ④'s explicit approval — this is the
single hard rule the interface exists to enforce (`userApproved`/`approvedAt` gate from
`scope.md` Gap 5).

---

## 3. Step ① — Intent parsing and size classification

The bot's first LLM pass does two things in one call: extract structured intent, and classify
wish size.

**Extracted fields:** working title, one-line description, entity types implied (character,
scenario, reward, art image, "a whole app/project"), and a `wishText` echo of the raw input
(verbatim, unedited — this is the field from `scope.md` Gap 3, stored regardless of size).

**Size classification — SMALL vs PROJECT:**

| Signal | SMALL | PROJECT |
|---|---|---|
| Requested output | One narrative pass, one art pass, or both, from a single prompt | An ongoing thing with its own roadmap: "build me a...", "start a project for...", multiple linked entities that will grow over sessions |
| Existing scope.md language | "small wishes remain plain Compositions" | "project-shaped wish flows into the project-creation LLM surface" |
| Cardinality | 1 output row | N Characters/Scenarios/Rewards over time, tracked via milestones |

This is a judgment call the LLM makes, not a keyword match — the plan-assembly step (§4) is where
the user gets to correct a misclassification before anything is spent, so a wrong first guess is
cheap to fix.

---

## 4. Step ② — Plan assembly

### SMALL path

Assemble a **Composition**-shaped plan (once the model exists — see §0): pick ingredient FKs from
existing records the wish plausibly references (Character/Dream/Scenario/Reward — the same four
slots `scope.md` documents), or freeform blurb overrides where no matching record exists. Decide
`mode` (`narrative` | `art` | `both`) from what the wish actually asked for. This mirrors
Composition's existing intended flow (`scope.md` §"Intended flow (as built)") — Wishmaster is a
new *producer* of Composition rows, not a new execution model.

### PROJECT path

Derive `title`, `description`, and a hyphenated `slug` per `PROJECT-CREATION.md` Surface 3 §"Flow"
steps 2–3, including the uniqueness check (`GET /api/projects/<slug>` → expect 404, retry with a
numeric suffix on collision, per that doc's §"Slug enforcement"). Sketch the standard three-
milestone scaffold (m1 SHAPE / m2 BUILD / m3 POLISH & SHIP, per `PROJECT-CREATION.md` Decision 4)
so the consent screen can show the user what they're actually kicking off, not just a slug.

Both paths present the same shape to step ③: a list of "things this will create or touch" plus a
draft `mode`/output-type selection the user can edit before cost is estimated.

---

## 5. Step ③ — Cost estimation

Reuse the existing estimators rather than inventing a parallel costing path:
`server/utils/manaCost.ts` (`estimateArtCostUsd`, `estimateTextCostUsd`) already price generation
by engine; Wishmaster calls these per planned output (one call per art pass, one per narrative
pass) and sums them into a single mana total for the plan. This total is what gets shown in step
④ and, on approval, is the amount `manaGate`/`applyMana` (`server/utils/mana.ts`) actually charges
during execution — the estimate and the charge must go through the same code path so the number
the user approved is the number they pay, not a rough guess that drifts at execution time.

PROJECT-path wishes show cost per planned output *and* flag that a project has no fixed total —
building continues over future sessions, each with its own mana cost at the time.

---

## 6. Step ④ — Consent screen

Single screen, one decision: **Approve / Edit / Cancel.**

Shows: the working title + description, the ingredient list (existing records linked, freeform
overrides spelled out), the output type(s) (narrative text / art image / both, or "new project"),
the mana total from step ③, and — PROJECT path only — the milestone scaffold preview.

- **Edit** returns to step ② with the user's correction folded in (e.g. "no, make it a scenario
  not a reward") and re-runs step ③ — no charge yet.
- **Cancel** discards the draft. Nothing is written except the ephemeral parse (no DB row needed
  until Approve, keeping abandoned wishes free of orphan records).
- **Approve** sets `userApproved: true` + `approvedAt: <now>` (`scope.md` Gap 5's minimal
  addition) and is the only trigger that starts step ⑤.

This directly encodes `scope.md`'s "What NOT to Do": *"Do not auto-create Dreams, Characters, or
Scenarios from a wish without user confirmation."* Nothing durable and non-draft exists before
this click.

---

## 7. Step ⑤ — Pipeline execution

State machine per `scope.md` Gap 2 (`status`: `DRAFT | PENDING | RUNNING | DONE | FAILED` +
`stepLog Json?` for the audit trail), so a multi-output wish (e.g. "three characters and a hero
image") can resume after a partial failure instead of restarting from scratch.

- **SMALL path:** one Composition row moves `PENDING → RUNNING` per generation pass (narrative,
  then art, or both in parallel), each pass appending a `stepLog` entry; `DONE` once every
  requested output exists.
- **PROJECT path:** `POST /api/projects` fires (Surface 3 step 4), which — once the still-pending
  auto-Todo hook exists (`PROJECT-CREATION.md` §"Pitch needed", Surfaces 2 and 3 both depend on
  this and it is not yet implemented) — creates the scaffold Todo the Worker picks up next cycle
  to write `projects/<slug>/roadmap.yaml`. Until that hook lands, the PROJECT path has a manual
  gap: either Wishmaster or a human has to nudge the Worker, so `status` should sit at `PENDING`
  with a `stepLog` note rather than silently going `DONE` with no roadmap yet.

Failures leave `status: FAILED` with the failing step's error in `stepLog`; retry re-enters at the
failed step, not from the top (avoids double-charging mana for already-completed passes — ties
into `manaCharged` accumulating per step, not being set once at the end).

---

## 8. Step ⑥ — The two output sizes

| | SMALL | PROJECT |
|---|---|---|
| Output record | One Composition row (`narrativeText`/`artPrompt`/`ArtImage`) | One `Project` row + `projects/<slug>/roadmap.yaml` |
| Linkage back to the wish | `Composition.wishText` on the row itself | `Project.description` carries the wish; no `outputDreamId`-equivalent link back exists yet on `Project` — open question, see §9 |
| Where the user sees it | Wherever Compositions render today (reactions, sharing) | The project's own dashboard surface, once scaffolded |
| Follow-up | None — the wish is fulfilled | Ongoing: milestones advance over future sessions/wishes |

---

## 9. Open items for Silas (not blocking this doc, but blocking implementation)

1. **Composition model doesn't exist yet** (§0) — the actual next schema task is "create
   Composition" (base fields from `scope.md`'s "Intended flow" section, plus the five MVP
   additions), not "add five columns." Suggest re-scoping wishmaster's schema task accordingly
   before anyone claims it.
2. **Auto-Todo on Project creation is still unimplemented** (`PROJECT-CREATION.md` §"Pitch
   needed") — this is a hard blocker for the PROJECT path ever reaching a built roadmap
   unattended. Worth prioritizing given Wishmaster is the second consumer of this same gap
   (Surface 2's front-end "New Project" button is the first).
3. **`Project` has no field pointing back to the originating wish** (parallel to Composition's
   `outputDreamId`). Minimal addition would be a `sourceWishId`-style pointer, or reuse
   `Composition.outputDreamId`'s naming convention renamed for the Project-not-Dream reality —
   Silas's call, since it's schema.
4. **`DreamType.WISH`** — confirm whether this existing-but-unused enum value is meant for
   anything here, or is dead from earlier planning and safe to ignore.
5. **Slug-uniqueness helper** (`PROJECT-CREATION.md` §"Pitch needed", Surface 3) — still needs
   writing; this doc assumes it exists per spec but it does not yet.

None of the above block *finishing this design doc* — they're the concrete next tasks once Silas
reviews and approves this interface shape, per the same needs-human posture `scope.md` set.

---

*Authored by Claude agent (conductor burst-rotation session), 2026-07-20. Reviewed by:
needs-human.*
