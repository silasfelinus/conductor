# Playbook: `type: dream`

**Creation type:** dream · **Task:** dream-cycle/t-004 · **Date:** 2026-07-16  
**Creative seed contract added:** 2026-07-24, from Silas's direct direction

The first per-type playbook. A `dream` build turns one backlog outline into a
complete, self-consistent slice of kind_robots content — a world grown from a
required genre/occupation/species seed fusion, the locations that result from
it, the cast who inhabit it, the rewards it grants, the scenarios that play out
there, and (optionally) a bot narrator who hosts it. Runs under
`CREATION-SPEC.md`'s loop (one stage per idle cycle, one creation building at a
time). No new backend models — everything maps to existing kind_robots models;
all are **api-ready** per `docs/api-surface.md`.

## Creative seed contract — mandatory before the place exists

Read `../CREATIVE-SEED-CONTRACT.md`. Every newly planned Dream must begin by
choosing:

- **1-2 actual story genres**
- **1 specific occupation, trade, duty, or vocation**
- **1 animal or species**

Only after those choices are recorded may the author invent the world,
locations, cast, narrator, rewards, scenarios, and art direction. Each seed must
materially alter at least two parts of the finished Dream. If deleting a seed
would leave the same concept, the outline has not passed the fusion test.

Do not default to another enchanted lighthouse, mystical bell tower, magical
archive, cozy market, lantern-lit workshop, or vaguely whimsical tower with
renamed nouns. Architecture is a consequence of the seed fusion, never the
starting prompt.

## Slugs & creationSource

All slugs follow `specs/SLUG-POLICY.md` (kebab-case, prefer two words, no leading
`the-` except a genuine two-word name; the world slug is the through-line every
element and its art reuse). The PITCH world card OWNS the proposal's slug so a
same-titled LOCATION can't collide with it. Dreams built by the autonomous daily
fast-lane carry `creationSource: "AI"` (not the DB-default `HUMAN`); use `HYBRID`
only when Silas seeded the idea.

## Auth & metadata (every write stage)

- **Auth:** `Authorization: Bearer $KR_API_TOKEN` (the beta-admin token; resolves to
  an admin user, so it clears both `requireApiUser` and the stricter admin/server gate
  on expression endpoints). See `docs/api-surface.md`.
- **Traceability (required):** every row carries `designer: "dream-cycle"` and source
  metadata — the originating backlog slug, and `proposalDate` when the outline is a
  daily proposal. Card Dreams also get a PitchSheet whose
  `extraData: {dreamCycle: <slug>, proposalDate, elementType, element}` groups the
  whole dream on the site's /daily-dream page and makes it removable as a unit.
- **Reference implementation:** `scripts/build_dream_records.py` is the working
  headless build of the core stages (2–5 + sheets + art). This playbook is the fuller
  idle-loop path — it adds the narrator stage (6) and DreamRelation edges that the
  headless fast-lane skips. Reuse its endpoint usage; don't re-derive it.

## Outline shape it consumes

A backlog outline (`backlog/_template.md`) provides: `## Creative seeds` with
Genres / Occupation / Animal or species / Fusion, `## The idea`, one
`## Location dream`, one `## Vibe / genre dream`, `## Characters (2-4)`,
`## Rewards (3-6)`, `## Scenarios (1-2)`, `## Narrator` (or `narrator: no`).
Daily proposals carry **2** locations instead of 1 — the playbook handles N
locations the same way (create each, relate each to the vibe).

---

## The 8 stages (one per idle cycle)

### Stage 1 — Seed, fuse, and flesh out
- **Input:** the raw outline.
- **Do first:** verify the outline records 1-2 genres, one occupation, one animal
  or species, and a concrete fusion explanation. For a legacy outline that
  predates this contract, choose and record the seeds before doing anything
  else; do not merely label the concept after it has already been invented.
- **Do next:** promote the outline into a full, buildable spec **in its own backlog
  file** — fill any thin section (concrete character looks/drives, reward
  rarities, scenario casts, art directions) so later stages have exact inputs.
  The occupation and species must have visible consequences in the locations,
  cast, conflicts, rewards, and art. No API calls.
- **Verify:** the file has the complete Creative seeds section and passes the
  fusion test; ≥1 location; a genre-bearing vibe; 2–4 characters; 3–6 rewards
  with a rarity spread; 1–2 scenarios; and a narrator block or an explicit
  `narrator: no`. Append Build log; flip card to `building`.

### Stage 2 — Dreams (location + vibe + relations)
- **Create call:** `POST /api/dreams` (`requireApiUser`) for the **GENRE** vibe Dream
  (reuse an existing GENRE Dream when one fits — GET/search first), then one
  **LOCATION** Dream per location. A PITCH "world card" Dream carries the idea.
- **Edges:** `POST /api/dream-relations` (`requireApiUser`), body
  `{fromDreamId, toDreamId, relationType, note?}` with `relationType ∈ dreamRelationTypes`
  (e.g. `CONTAINS` world→location, `RELATED` location→genre). *(This closes the old
  t-017 gap — the endpoint now exists.)*
- **Verify:** each Dream returns `data.id`; relation rows created; GENRE reused, not
  duplicated. Confirm that the selected genre or blend is visible in the actual
  descriptions rather than existing only in the seed record. Build log.

### Stage 3 — Characters
- **Create call:** `POST /api/characters` (`requireApiUser`) for each of the 2–4
  characters (backstory, drive, quirks, look, stats), plus a CHARACTER card Dream each,
  linked via the Dream's `dreamIds` relation.
- **Verify:** every character row has an id and is linked to its CHARACTER Dream; count
  matches the outline. At least two character concepts must visibly reflect the
  occupation, species, or biological/social consequences of the seed fusion. Build log.

### Stage 4 — Rewards
- **Create call:** `POST /api/rewards` (`validateApiKey`) for each of the 3–6 rewards,
  each with a `rewardType` and a rarity. Ensure a **rarity spread** (not all COMMON);
  a dream should offer at least one SKILL-type and one ITEM-type reward where the
  outline supports it.
- **Verify:** reward rows created with the intended rarities/types. Rewards must feel
  native to the chosen work and species rather than generic magic loot. Build log.

### Stage 5 — Scenarios
- **Create call:** `POST /api/scenarios` (`validateApiKey`) for the 1–2 scenarios,
  each wiring the location(s), vibe, and named cast together.
- **Verify:** scenario rows reference the correct location/character ids and use the
  selected genre as a story engine. Build log.

### Stage 6 — Narrator *(skip entirely if `narrator: no`)*
The narrator stage. If the outline sets `narrator: no`, **skip this stage cleanly**
(the pipeline advances to Art) — `static-garden`, `cartographers-greenhouse`, and
`sediment-spa` exist specifically to exercise this skip. Otherwise:
- **Bot:** `POST /api/bots` — the narrator Bot (name, voice, personality) + a NARRATOR
  card Dream.
- **Topics:** `POST /api/bots/topics` (batch upsert on `slug`) — **reuse fitting
  NarratorTopics**; create a new topic only when none fit. Required per row:
  `slug`, `title`, `prompt`. Check existing topics via
  `GET /api/narrators/{type}/{slug}` before creating.
- **Threads:** `POST /api/bots/threads` (batch upsert on `(botId, topicId)`) wiring the
  Bot to its topics. Required per row: a resolvable bot (`botId`|`botName`) + topic
  (`topicId`|`topicSlug`) + `openingText`.
- **Expressions:** `POST /api/bots/expressions` (batch upsert on `(owner, expressionKey)`,
  admin/server auth). Build the set: **NEUTRAL + ≥5 emotions + ≥2 actions**. Required
  per row: exactly one of `botId`/`characterId`, `expressionKey`, `expression` (enum),
  `kind` (`EMOTION`|`ACTION`). `imagePath`/`videoPath` fill in at Art time; rows can be
  created art-less and re-upserted.
- **Transitions (optional, deferred):** `POST /api/bots/transitions` needs a rendered
  `videoPath`, so it is a post-Art enrichment, not a core stage — skip unless a
  transition clip already exists.
- **Verify:** Bot exists; ≥1 thread on a fitting topic; expression set meets the
  NEUTRAL + ≥5 + ≥2 minimum; `GET /api/narrators/...` returns the narrator. Build log.

### Stage 7 — Art
- **Do:** queue one `requests:` entry **per card Dream** into
  `projects/art-prompts.yaml` (the existing self-draining pipeline —
  `scripts/build_dream_records.py:art_request_entry` is the exact format):
  `id: dream-cycle-<slug>-<element>`, `source: dream-cycle`, `status: pending`,
  `target_repo: silasfelinus/kind_robots`,
  `image_path: public/images/dreams/<slug>/<element>-card.webp`, `variant: card`,
  `size`, `label`, `prompt` (from each element's art direction). The nightly
  `auto-art-generate` workflow renders them and `distribute_images.py` lands them; a
  later `--attach`/PATCH pass sets each PitchSheet's `imagePath` once the public URL is
  live. `art-generate.yaml` is the dry-run manifest of concrete requests.
- **Metadata:** keep prompt/model/seed/source path per the generated-art rule so every
  image is traceable and removable.
- **Verify:** one pending request per card element appended; no backend edits. Every
  prompt shows consequences of the occupation/species fusion and avoids generic
  enchanted-architecture shorthand. Build log.

### Stage 8 — Ship
- **Do:** run the checklist below; flip the card `status: built` and set `built_pr`;
  append the `SHIPPED.md` ledger entry; replenish the backlog to ≥5 buildable outlines
  if it dropped below (per `CREATION-SPEC.md`).
- **Ship checklist:**
  - [ ] Creative seeds record has 1-2 genres + occupation + animal/species + fusion explanation
  - [ ] Each seed materially changes at least two finished elements; no removable garnish
  - [ ] LOCATION(s) + GENRE vibe Dream exist and are related (world CONTAINS location, location RELATED genre)
  - [ ] 2–4 Characters, each linked to a CHARACTER Dream
  - [ ] 3–6 Rewards with a rarity spread (SKILL + ITEM where applicable)
  - [ ] 1–2 Scenarios wiring location + vibe + cast
  - [ ] Narrator built (Bot + ≥1 thread + NEUTRAL/≥5/≥2 expressions) **or** cleanly skipped for `narrator: no`
  - [ ] A PitchSheet per card Dream, tagged `extraData.dreamCycle`
  - [ ] Art requests queued for every card element
  - [ ] Every row carries `designer: "dream-cycle"` + source metadata (traceable/removable)

---

## Reversibility

Because every row is tagged `designer: "dream-cycle"` with its source slug, a whole
dream can be found and removed as a unit if Silas vetoes it — the loop never leaves
orphaned, untraceable content. Missing/broken endpoints are filed as kind_robots
roadmap tasks or pitches (backend stays read-only/external), never patched directly.
