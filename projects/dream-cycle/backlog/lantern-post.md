---
slug: lantern-post
title: The Lantern Post
type: dream
status: parked
priority: normal
narrator: yes
created: 2026-07-10
built_pr: null
---

## The idea
A night-sky post office staffed by giant gentle moths who deliver the letters people
never sent: apologies, confessions, thank-yous written in dreams. Every lantern on
the sorting floor is an undelivered feeling looking for its address. Melancholy but
hopeful — the mail always moves.

## Location dream
**The Lantern Post** — LOCATION. A timber-and-brass sorting hall balanced on a
lighthouse above the cloud line, pigeonholes stretching into the dark like a star
map. Flavor: "No postage required. It was already paid in the wanting." Art
direction: warm lantern gold against deep indigo, moth-wing dust motes, soft focus.

## Vibe / genre dream
**Gentle Melancholy** — GENRE (create; reuse if an existing bittersweet/cozy-night
GENRE fits). Quiet, sincere, tearjerker-adjacent but always landing on hope. Edges:
`lantern-post RELATED gentle-melancholy`.

## Characters (2-4)
- **Postmistress Vesper** — a luna moth in a mail-carrier's cap; remembers every
  letter she's ever carried and exactly one she couldn't deliver. Drive: to finally
  deliver that one letter, though she no longer remembers the address. Look: pale
  lime-green moth wings dusted with faint eyespots, a brass-buttoned postal coat
  fitted over her thorax, wire spectacles, antennae permanently ink-stained from
  decades of sorting. Quirk: hums the same three notes of an unfinished tune while
  working, never noticing she's doing it.
- **Smudge** — an apprentice moth, clumsy, keeps eating the corners of envelopes;
  has perfect recall of feelings but not names. Drive: desperate to earn a real
  postal cap of their own instead of the hand-me-down one that slides over their
  eyes. Look: small mottled-brown moth, tattered wing edges from over-eager
  flying, perpetually smudged with lantern soot and paper pulp (the namesake).
  Quirk: narrates deliveries out loud in third person to stay focused.
- **The Dead-Letter Clerk** — a shadowy, kindly figure who files the letters whose
  recipients are gone; insists his department is the most hopeful one. Drive: to
  prove that an ending isn't the same as being forgotten. Look: a tall silhouette
  built from folded, overlapping paper — indigo shadow where a face would be, hands
  made of stacked envelope corners, a single warm lantern-glow where a heart would
  sit. Quirk: always finishes a filing task exactly as the lantern he's holding
  gutters low, never sooner or later.

## Rewards (3-6)
- **Moth-Dust Stamp** (ITEM, COMMON) — a lantern-gold postage stamp; affixed to any
  message, it makes the sender 10% braver in delivering it.
- **Return to Sender** (SKILL, UNCOMMON) — a passive boon: the next kindness the
  bearer does for a stranger quietly comes back around to them, once per day.
- **The Unsent Letter** (ITEM, RARE) — a folded, blank envelope that only reveals
  its contents once the bearer knows what it needed to say.
- **Vesper's Last Route** (SKILL, LEGENDARY) — a one-time favor: Vesper personally
  flies one delivery anywhere, to anyone, at any point in memory.

## Scenarios (1-2)
- **The Misdirected Confession** — a lantern is addressed to two people at once and
  Smudge ate the disambiguating corner; the player rides the night route to sort it out.
- **Dead Letter Day** — once a year the Dead-Letter office reads one letter aloud to
  the stars; the Clerk asks the player to choose which.

## Narrator (if narrator: yes)
**Postmistress Vesper** as narrator bot: soft-spoken, precise, speaks in postal
metaphor, gently funny about grief. Expressions: NEUTRAL, LOVING, SORROWFUL, JOYFUL,
THINKING, PROUD; actions: WHISPERING, CRYING (rare, earned). Topics/threads: "Night
Routes" (guided deliveries), "The Dead-Letter Office" (stories of closure), "Write
It Anyway" (helping users draft the letter they never sent).

## Notes from Silas
- (leave notes here — agents fold them in before building and never edit this section)

## Build log
- 2026-07-21 | Stage 1 (Flesh out) | conductor scheduled burst
  (claude-conductor-burst-20260721T232500Z-dc-t006) | Promoted from `outline` to
  `building` (oldest buildable dream-type outline, `created: 2026-07-10`, tied with
  static-garden/tidepool-arcade — picked alphabetically first; monster-recast is
  `approved`/higher-priority but its delegated home task, coloring-book/t-022, is at
  `needs-human`, blocked on the art-generation relay, so it can't advance this cycle).
  Filled the two thin sections Stage 1 calls out: each character now has an explicit
  physical `Look` plus a one-line `Drive` (previously implied only through backstory/
  quirk), and each reward now carries an explicit `rewardType` (2 ITEM, 2 SKILL —
  satisfies Stage 4's rarity+type spread requirement) alongside its existing rarity.
  Verified against Stage 1's checklist: 1 location (The Lantern Post), 1 vibe (Gentle
  Melancholy), 3 characters (2-4 ✓), 4 rewards with a COMMON→LEGENDARY rarity spread
  and a SKILL/ITEM type spread (3-6 ✓), 2 scenarios (1-2 ✓), narrator block present
  (Vesper, 6 expressions, 2 actions, 3 topics). No API calls this stage per the
  playbook. Next: Stage 2 (Dreams — location + vibe + relations via
  POST /api/dreams, POST /api/dream-relations) on a future idle cycle.
- 2026-07-22 | Stage 2 (Dreams — location + vibe + relations) | conductor scheduled
  burst (claude-conductor-burst-20260722T0425Z-dc-t006) | Searched existing GENRE
  Dreams via `GET /api/dreams?dreamType=GENRE` for an existing bittersweet/hopeful-grief
  vibe before creating a new one, per the playbook's reuse-first instruction: found
  `elegiac-wonder` (id 2330, "Elegiac Wonder", flavorText "grief, catalogued and kept
  warm") — thematically the closest existing GENRE to "Gentle Melancholy" (quiet,
  sincere, tearjerker-adjacent, always landing on hope), so reused it rather than
  creating a duplicate vibe node. Created the PITCH world card (`POST /api/dreams`,
  id 3194, slug `lantern-post` — the proposal's own slug, per SLUG-POLICY.md rule 4)
  and the LOCATION dream (id 3195). Per SLUG-POLICY.md rule 4 (PITCH and LOCATION must
  not collide), gave the location a distinct slug `sorting-hall` (evocative of "sorting
  floor"/"sorting hall" from the outline) rather than reusing `lantern-post` for both —
  confirmed both slugs were free via `GET /api/dreams?search=...` first. Created edges
  via `POST /api/dream-relations`: world (3194) CONTAINS location (3195, relation id
  77); location (3195) RELATED genre (2330, relation id 78). Also created a PitchSheet
  for both card Dreams via `POST /api/sheets/by-dream/{id}` (ids 476, 477), each with
  `extraData: {dreamCycle: "lantern-post", elementType, element}` per the traceability
  contract — bundled with dream creation now (matching `build_dream_records.py`'s
  `card_dream()` pattern) rather than deferred to Stage 8, so the pitch cards render
  correctly as soon as this stage lands. Verified: `GET /api/dreams/3194` returns the
  created world Dream; `GET /api/dream-relations?fromDreamId=3194` confirms the CONTAINS
  edge. Every row carries `designer: "dream-cycle"`, `creationSource: "AI"`. Next: Stage
  3 (Characters — POST /api/characters for Vesper, Smudge, the Dead-Letter Clerk, each
  linked to the world Dream via dreamIds) on a future idle cycle.
- 2026-08-02 | Legacy staged path retired | Parked this card so no future agent resumes
  Stage 3 or creates a second bundle. Existing production evidence is retained exactly
  as created: reused GENRE Dream 2330, PITCH Dream 3194, LOCATION Dream 3195,
  DreamRelations 77/78, and PitchSheets 476/477. Characters, Rewards, Scenarios,
  narrator, and art were never created from this card. The concept remains idea inventory;
  any future adaptation must be authored as a new dated six-asset proposal and must not
  silently complete or duplicate these historical rows.
