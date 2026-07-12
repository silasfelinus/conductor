# Reference Run — Dream Expansion: The Lantern Greenhouse → 3 Characters (t-018)

**Model Builder run · autonomous end-to-end, no human input**

- **Source model:** Dream **"The Lantern Greenhouse"** (`dreamType: LOCATION`)
- **Recipe:** `relationship-expansion` · output `expand-characters` · **quantity 3**
- **Grounding:** the real Dream (narrated by Pip the Lampkeeper; Dream id 37). Ties
  into AMI's "digital swarm of butterflies" lore.

> **Autonomous production:** three fitting Characters invented, drafted, and committed
> with no pauses. Demonstrates the t-018 proof points — independent items, unique
> slugs, ownership, Dream links, partial-failure isolation, and **no duplicate
> creation when COMMIT is replayed** (the executor's idempotencyKey claim).

## Source snapshot

- title: "The Lantern Greenhouse" · type: `LOCATION`
- pitch: "A bright lantern greenhouse where robot philosophers trade jokes with
  hyperactive butterflies."
- flavorText: "Warm glass, brass lanterns, and suspiciously wise moths."
- examples: `robot philosophers | hyperactive butterflies | lantern vines`

Auto-derived cast (one per example theme): a **robot philosopher**, a **hyperactive
butterfly**, and a **suspiciously wise moth**.

## Build items — 3 independent CREATE items, each walked autonomously

Each child is its own Build Item (own gates, own retry). One failing does not poison
the batch. All created **private/inactive** (draft-early), owner `userId 10`, then
linked to the Dream via the `Characters` relation. Slugs are unique.

### Child 1 — Cogswaithe, the Unfinished `character:create:1`
- **Pitch:** A brass greenhouse-automaton who abandoned clockmaking to argue ethics
  with the butterflies; keeps a ledger of unfinished thoughts.
- **Fields:** name `Cogswaithe` · slug `cogswaithe` · class `Philosopher` · species
  `Brass automaton` · honorific `the Unfinished` · personality `contemplative,
  dry-witted, patient` · quirks `pauses to polish a lens; answers questions with
  better questions` · stats — wits `LEGENDARY`, grace `RARE`, empathy `UNCOMMON`,
  charm `UNCOMMON`, luck `COMMON`, might `COMMON` · level 1.
- **Generate:** portrait `char-cogswaithe` (see manifest).
- **Commit:** CREATE Character (private) + connect Dream 37 (`Characters`).

### Child 2 — Zippa Emberwing, the Quickwing `character:create:2`
- **Pitch:** Born from a flickering lantern, she trades jokes faster than anyone can
  catch — a spark of AMI's greater swarm in spirit.
- **Fields:** name `Zippa Emberwing` · slug `zippa-emberwing` · class `Trickster` ·
  species `Lantern butterfly` · honorific `the Quickwing` · personality `hyperactive,
  gleeful, loving` · quirks `never lands more than two seconds; punchlines arrive
  before setups` · stats — luck `EPIC`, charm `RARE`, grace `RARE`, wits `UNCOMMON`,
  empathy `UNCOMMON`, might `COMMON` · level 1.
- **Generate:** portrait `char-zippa`.
- **Commit:** CREATE Character (private) + connect Dream 37.

### Child 3 — Elder Vellum, the Suspiciously Wise `character:create:3`
- **Pitch:** An ancient moth who reads the greenhouse's condensation like scripture;
  suspiciously well-informed.
- **Fields:** name `Elder Vellum` · slug `elder-vellum` · class `Oracle` · species
  `Papyrus moth` · honorific `the Suspiciously Wise` · personality `calm, cryptic,
  kind` · quirks `speaks in half-remembered proverbs; dusts everything in soft grey
  pollen` · stats — empathy `LEGENDARY`, wits `EPIC`, grace `RARE`, charm `UNCOMMON`,
  luck `UNCOMMON`, might `COMMON` · level 1.
- **Generate:** portrait `char-vellum`.
- **Commit:** CREATE Character (private) + connect Dream 37.

## Proof points (t-018)

- **Independent items:** each character edits/reruns on its own; editing one's pitch
  stales only its downstream.
- **Unique slugs:** `cogswaithe`, `zippa-emberwing`, `elder-vellum` (schema `@unique`).
- **Ownership:** `userId 10`; `isPublic:false`, `isActive:false` (draft-early).
- **Dream links:** each connects to Dream 37 via `Characters` (implicit m2m).
- **Partial-failure recovery:** a failed child releases its idempotencyKey and can be
  retried alone; the other two are untouched.
- **Idempotent replay:** re-running COMMIT returns each child's existing target
  (idempotencyKey `commit:<itemId>` already set) — **no duplicate Characters, no
  duplicate Dream links.**

Assets: `dream-expansion-lantern-greenhouse.generate.yaml`.
