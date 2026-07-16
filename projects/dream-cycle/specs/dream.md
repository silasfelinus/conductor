# Playbook: `type: dream`

**Creation type:** dream · **Task:** dream-cycle/t-004 · **Date:** 2026-07-16

The first per-type playbook. A `dream` build turns one backlog outline into a
complete, self-consistent slice of kind_robots content — a location with a vibe,
the cast who inhabit it, the rewards it grants, the scenarios that play out there,
and (optionally) a bot narrator who hosts it. Runs under `CREATION-SPEC.md`'s loop
(one stage per idle cycle, one creation building at a time). No new backend models —
everything maps to existing kind_robots models; all are **api-ready** per
`docs/api-surface.md`.

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

A backlog outline (`backlog/_template.md`) provides: `## The idea`, one
`## Location dream`, one `## Vibe / genre dream`, `## Characters (2-4)`,
`## Rewards (3-6)`, `## Scenarios (1-2)`, `## Narrator` (or `narrator: no`). Daily
proposals carry **2** locations instead of 1 — the playbook handles N locations the
same way (create each, relate each to the vibe).

---

## The 8 stages (one per idle cycle)

### Stage 1 — Flesh out
- **Input:** the raw outline.
- **Do:** promote the outline into a full, buildable spec **in its own backlog file** —
  fill any thin section (concrete character looks/drives, reward rarities, scenario
  casts, art directions) so later stages have exact inputs. No API calls.
- **Verify:** the file has ≥1 location, a vibe, 2–4 characters, 3–6 rewards with a
  rarity spread, 1–2 scenarios, and a narrator block or an explicit `narrator: no`.
  Append Build log; flip card to `building`.

### Stage 2 — Dreams (location + vibe + relations)
- **Create call:** `POST /api/dreams` (`requireApiUser`) for the **GENRE** vibe Dream
  (reuse an existing GENRE Dream when one fits — GET/search first), then one
  **LOCATION** Dream per location. A PITCH "world card" Dream carries the idea.
- **Edges:** `POST /api/dream-relations` (`requireApiUser`), body
  `{fromDreamId, toDreamId, relationType, note?}` with `relationType ∈ dreamRelationTypes`
  (e.g. `CONTAINS` world→location, `RELATED` location→genre). *(This closes the old
  t-017 gap — the endpoint now exists.)*
- **Verify:** each Dream returns `data.id`; relation rows created; GENRE reused, not
  duplicated. Build log.

### Stage 3 — Characters
- **Create call:** `POST /api/characters` (`requireApiUser`) for each of the 2–4
  characters (backstory, drive, quirks, look, stats), plus a CHARACTER card Dream each,
  linked via the Dream's `dreamIds` relation.
- **Verify:** every character row has an id and is linked to its CHARACTER Dream; count
  matches the outline. Build log.

### Stage 4 — Rewards
- **Create call:** `POST /api/rewards` (`validateApiKey`) for each of the 3–6 rewards,
  each with a `rewardType` and a rarity. Ensure a **rarity spread** (not all COMMON);
  a dream should offer at least one SKILL-type and one ITEM-type reward where the
  outline supports it.
- **Verify:** reward rows created with the intended rarities/types. Build log.

### Stage 5 — Scenarios
- **Create call:** `POST /api/scenarios` (`validateApiKey`) for the 1–2 scenarios,
  each wiring the location(s), vibe, and named cast together.
- **Verify:** scenario rows reference the correct location/character ids. Build log.

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
- **Verify:** one pending request per card element appended; no backend edits. Build log.

### Stage 8 — Ship
- **Do:** run the checklist below; flip the card `status: built` and set `built_pr`;
  append the `SHIPPED.md` ledger entry; replenish the backlog to ≥5 buildable outlines
  if it dropped below (per `CREATION-SPEC.md`).
- **Ship checklist:**
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
