# Zuzu: Shifting Lands — Authored Encounter Implementation Order

**Decision:** 2026-10-09, newest user direction. **Scope:** Shifting Lands game only. **Status:** source-authoring complete for the Homestead draft, runtime changes not yet implemented. **Priorities:** readable flip → custom Zuzu backs → seeded illustrated encounters → choices/results → art and acceptance.

## Binding creative change

A **location** is a stable piece of geography, and it has a **pool of individually authored encounter cards**. Selecting a card chooses the **whole card** (written scene, specific species/occupation/cast, fixed art brief, motive, choices, stakes), never a species rolled separately from a job or disposition. This changes the **Shifting Lands game**; it does not repeal the world registry's independent `FacetProfile` taxonomy used by other Kind Robots projects. Different species may hold the same profession **across differently illustrated authored cards**, but not through a mid-run combinatorial swap.

For example, the **Border Farm** can draw **A Family at the Fence**, showing **rabbit homesteaders** in the illustration. The title must not redundantly identify their species. It is *one of four* authored possibilities for that location, not a fixed encounter or a mutable role template. Actor design can be changed through an explicit authored content revision, never by runtime casting.

A five-land expedition still has **five chapters, three encountered locations per chapter, one major gate per chapter**. The expanded authored pools create variability *within* those 15 story beats, rather than increasing every run to 12 mandatory scenes in Land 1.

## Authoring source and provenance

- **Schema**: [ENCOUNTER-PACK.schema.json](ENCOUNTER-PACK.schema.json), Draft 2020-12, `schema_version: 1`. Formal records for location pools, art/cast, flavor text, ≥2 semantic choices, 2d6 skill checks and alternative written outcomes.
- **First-land pack**: [HOMESTEAD-12.json](HOMESTEAD-12.json). 3 existing manifest location IDs × 4 encounters, with **4 good / 4 bad / 4 mixed**, 24 authored decisions and 48 result passages.
- **Contract/CI**: `encounter-pack.contract.mjs`, `encounter-pack.contract.test.mjs`, Shifting Lands manifest workflow.
- **Existing geography**: `../WORLD-DECKS.json` **v2** remains the canonical five-land route and first-land place-ID source. This encounter pack is a supplementary authored v1 design artifact, **not a silent replacement** or a claim that the v2 Kind Robots importer has already migrated. Do not change its IDs or overwrite the provenance-pinned client snapshot without versioning and CI.
- **Runtime media**: All 12 encounter-specific art refs are **null / design-only**. `art.brief` and `cast` describe intended original scenes, **not a generated image or known live ArtImage ID**. Verify content rating, links, source records and cast identity before assigning images.
- **Lore**: Conductor `worlds/zuzu/WORLD-GUIDE.md`, Book One and locked art remain upstream. The Abbess's motives are openly documented for agents; no accidental player-facing revelation or invented resolution to the lost-human mystery. Harm to children is implied narrative stakes, never spectacle.

## Data flow: deterministic and spoiler-safe

```text
Conductor location v2 (3 fixed places in Homestead)
    ↓ server/editor-approved authored encounter pack v1
Location pool [4 complete encounter identities; eligibility/weights]
    ↓ seeded selection of encounterId, once; persist the exact draw
Encounter instance { encounterId, cardRevision, fixed cast ref, faceState }
    ↓ encounter prose displayed (readable, screen-reader accessible)
2+ action cards { label, intent, risk_hint, roll: 2d6 + skill + modifier vs target }
    ↓ rules-only deterministic roll, persisted **before** animation outcome is shown
Success / failure { result text, HP, provisions, flags, optional prospective map shift }
    ↓ journal { encounterId, choiceId, dice, totals, result text, effects }
Discard and map memory; revisit shows existing history, no reroll/farming
```

Sampling is **per-run seeded weighted selection** over eligible cards, without replacement where configured. Never call an LLM to decide species, encounter identity, dice, HP, disposition, or outcome. Future writer models may produce optional atmospheric prose only from already-approved fact packets, never replace authored choices or alter the reducer.

**Versioning:** The current Kind Robots `utils/shiftingLands/journey.ts` has a v1 state with one implicit encounter per location. A **v2 save migration** is required, including active encounter ID, authored card revision, seeded draw state, choice/outcome identity, persisted dice, and resolved unique reward/flags. Existing saved v1 runs should remain readable in the isolated legacy workshop; do not silently apply new effects to an old roll. Reject stale/invalid blobs and provide an explicit new-run path. No separate Character or ArtImage rows created just to represent draft cast metadata.

## Execution sequence: task-ready, parallel where safe

| Order / Conductor task | Owner / repo | Dependencies | Implementation and acceptance |
| --- | --- | --- | --- |
| **A · t-007** Authored encounter contract and Homestead pack | Conductor source | t-003 | Deliver the schema, 12 cards, CI checks, canonical IDs, and revised directive. Preserve references as design-only. **This milestone**, not a claim of runtime migration. |
| **B · t-019** Readable flipping and encounter reading surface | Kind Robots | t-015 | Fix the current unreadable 360° card spin: use the verified `kr-card-flip` family for a **persistent face state** (or a focused adapter using the existing KR mechanics); `NavigationFlipCard` may still animate deal but must not be the persistent reader. Once revealed, flavor text stays still, readable and focused. Reduced motion, Escape/focus return, keyboard/touch, no duplicate reducer event on animation callbacks. |
| **C · t-022** Branded Zuzu card-back assets | Kind Robots + world art ledger | t-005 | Produce source-tracked **encounter** and **boss/trial** backs first, plus variants for future reward/event decks only if useful. Weird-west/Edo motifs, strong 2:3 silhouette, approved use/rights and responsive thumbnail legibility. Use existing art queues only within their authorization. Do not call generic KR card backs custom art. Card front remains proper authored scene art. |
| **D · t-020** Seeded authored encounter pool reducer | Kind Robots | t-007, t-006 | Import validated source pack; choose exactly one authored scene per visited location; attach fixed visual cast identity, seeded weighted choice and state-pinned revision; preserve 15-location/5-gate traversal. Implement distinct roll/flags/result outcomes. Explicit save versioning; deterministic replay, no refresh reroll. |
| **E · t-021** Choice-led story card reader | Kind Robots | t-019, t-020 | Connect UI to `flavor_text` and 2+ clear action cards. Each action has intent and visible risk/stat/target, choice-specific 2d6 check, success/failure prose and deltas; last check, chosen action and result remain inspectable. Screen reader announces encounter and result without speaking hidden developer notes. |
| **F · t-023** First-land illustration assignment + ledger | Kind Robots + Conductor | t-022, t-020, t-013 | Create/reuse 12 source-authorized **bespoke encounter faces**, one per authored fixed scene; preserve source media IDs and provenance, do not duplicate image rows. Temporary atmosphere art may remain visibly labeled pending until approved assets exist. |
| **G · t-010** Four later lands content packs | Conductor | t-020 | Author 3 locations × ≥3 authored encounters each for Dustwater, Tablelands, Storm-Crow Depths and Black Verge, with true favorable/dangerous/mixed possibilities, character-specific illustrated casts and 2+ unique checked choices per encounter. Retain original five bosses and earned reveal pacing. |
| **H · t-024** Content, dice, flip and accessibility quality gate | Kind Robots + Conductor | t-021, t-023 | Simulate hundreds of seeded runs, invalid saves, reload mid-flip, rapid double taps, hidden text and result persistence; test 375/768/1440 viewport screenshots, reduced motion and keyboard. Never imply this satisfies the public-launch human approval. |

**Related existing tasks:** t-008 expands skills/rewards/companions and should consume the choice/outcome model; t-009 owns durable save/replay integrity; t-011 authors boss alternative routes; t-014 is optional **post-authored** flavor enhancement, not mechanical generation; t-016 enriches inventory, dice and journal; t-017 verifies balancing and state invariants; **t-018 remains the human-gated authenticated UI/publication decision**. Do not rewrite an already claimed task or silently merge code while its current owner is working.

## Developer tickets: explicit implementation boundaries

### t-019: readable card reveal

**Files to inspect:** `components/navigation/flip-card.vue` (full spin that returns to front); `components/gallery/kr-card-flip.vue` (persistent inspect); `components/shifting-lands-journey-board.vue`; `pages/admin/zuzu-shifting-lands.vue`.

**Done when** initial deal visibly reveals a face and *stays* face-up, paragraph can be read throughout choice phase, flipping has a clear front/back identity, no double-choice due to animation, and accessibility/reduced-motion snapshots pass. Use real existing art and custom backs from t-022 when available; a temporary backed state can be used during development but may not be mistaken for final art acceptance.

### t-020: model + state migration

**Files to inspect:** `utils/shiftingLands/journey.ts`, `worldSnapshot.json`, `stores/shiftingLandsJourneyStore.ts`, Conductor importer and source manifest. **No parallel improvised species/occupation draw**, no mutable global `Character` records, no hand-edited world source snapshots with lost blob SHA. Choice resolution must be a single idempotent reducer transition; store the encounterId, choiceId, 2d6 faces, modifier, target, result and flags. Validate two paths through each same-location seed and past logs after refresh.

### t-021: authored prose and decisions

**Files to inspect:** `components/shifting-lands-journey-board.vue`, new pack DTO serializer, relevant source-backed art inspector. Default reader shows `title`, `flavor_text`, two or more meaningful labeled options, stat/target/risk affordances and a readable result passage after the roll. Distinct failure outcomes must advance the story rather than do nothing. Keep developer lore notes, hidden motive and unavailable art provenance out of player face.

### t-022 / t-023: art delivery

**First assets:** Zuzu encounter back, Zuzu boss back, twelve illustrated encounter faces. **Visual design:** weathered paper, burnt-ink border, Edo talisman geometry and frontier motifs; elegant, legible at 100px width. Distinguish encounter and boss without dependence on color alone. Reuse existing approved assets and locked characters wherever accurate; generated art is draft until reviewed and linked. No user-facing claims that a missing file was delivered.

## Acceptance checklist

- [ ] Every played location draws from 2+ authored options (Homestead has 4); a seeded run contains **3 location encounters per land**, not all drafts.
- [ ] Encounter casting is fixed in its illustration and content; no separate species/job randomizer for new Shifting Lands plays.
- [ ] Cards expose species through picture, not explicit species prefixes in titles.
- [ ] Encounter face rests in readable state and uses original Zuzu backs; keyboard, touch and reduced motion work.
- [ ] Each encounter renders prose and at least two context-specific choices; each choice commits its own 2d6-based consequences.
- [ ] Persist encounter, choice, dice, outcome text, resources/flags and relevant causal shift; refresh/replay cannot reroll.
- [ ] Archive visits, preserve map history and keep adult-cast/scenario art provenance; protect player-facing spoilers.
- [ ] Private `/admin` preview and existing separate Homestead save still work; publication requires t-018 human clearance.

**Explicit exclusions:** No live production deploy, paid image generation, unreviewed AI lore canonization, public `/play` publication, or schema/database migration is authorized by this *planning* delivery alone.
