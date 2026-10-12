# Daily Dream and daily pitch creative direction (Silas, 2026-10-12 PT)

Status: **approved corrected direction; 14-asset Dream implementation pending**. This is a migration specification, not proof that the current six-record pipeline already meets it. The existing single-writer Daily Digest must remain healthy until an atomic, tested replacement is merged.

## Daily Dream after migration (corrected by Silas, 2026-10-12 PT)

**Do not replace the original Daily Dream's six connected creations.** Silas explicitly
wants to keep the variety of a fresh day-by-day mini-world, with a cohesive
visual language across its people, places, rewards, and scene.

Daily delivery is **14 created assets in two independent editorial/art lanes**:

1. **The traditional complete Daily Dream, six linked outputs:**
   - One brand-new original **PITCH Dream/vibe**, with its own distinct theme and art style.
   - One **LOCATION Dream** linked by `CONTAINS` to that world.
   - One real **Character** linked to that world.
   - One ITEM and one SKILL **Reward**, linked to that world.
   - One **Scenario**, linked to the world and its location, referencing the world's
     location and character in its setup.
   - **All six share the vibe's coherent visual style.** The random daily vibe is
     genuinely independent, and its linked content is allowed to be just as strange
     and unexpected as the existing Daily Dream. Preserve the existing card gallery,
     Facet logic, relationship semantics, and distinctive art prompts.
2. **Eight *additional* Zuzu-world outputs, not linked to that day's vibe:**
   - Two locations, two characters, two rewards (ITEM and SKILL), and two
     moral-choice scenarios.
   - Each category provides one asset for `zuzu-gamebook` and one for
     `emperor-of-dust`, with explicit project target and provenance.
   - Use the **Arthemy and/or Illustrious** checkpoint families, chosen per Zuzu
     asset from the resource catalog; do not force either checkpoint onto the
     independent Daily Dream. Canon designs and existing visual references win.
   - The Zuzu assets may have supported canonical Zuzu connections of their own,
     but **none may inherit `dreamIds`, `CONTAINS`, Facets, scene setting, lore or
     random visual style from the original daily PITCH Dream**.

The standalone daily Dream is **not a placeholder**, teaser or ninth asset.
It is a complete mini-world; the Zuzu batch is *additional production material*.

**Zuzu scenarios are genuine choices.** Each has an immediate incident, at
least two consequential options, a meaningful tradeoff, and short- and
longer-term fallout. Avoid binary saint/villain decisions. For the gamebook,
specify branching scene, flags/skills and replay outcomes. For Emperor,
specify dispatch candidates, Horde/faction/resource impacts, injury risks and
subsequent-day consequences. The Horde is a number; the named followers lead it,
and injuries are more common than deaths.

**Emperor of Dust has its own consistent creative pitch**, `projects/emperor-of-dust/DAILY-DREAM-VIBE.md`.
It is *neither* a synonym for the daily random vibe nor a generic clone of
Zuzu Gamebook. Different periods and factions must not be conflated.

## Implementation and cutover contract

- **One canonical writer, one complete transaction**. Extend the existing
  six-record transactional builder to commit six linked original Dream outputs
  **plus** eight separately routed Zuzu assets in one coherent idempotent bundle.
  Keep rollback/failure/retry semantics and never create a parallel cron or
  direct-REST backfill. V2 historical six-record outputs remain immutable/readable.
- Version 3 proposal storage retains the existing top-level `vibe`, `locations`,
  `characters`, `rewards` and `scenarios` shapes with **original 1/1/2/1 counts**,
  plus a new, separate `zuzu_assets` object with **2/2/2/2 counts**. This prevents
  old consumers from mistaking the eight Zuzu entities for attached Dream children.
- Facet slots are the old six names plus eight distinct `zuzu_*` names. Explicit
  per-record IDs, project targets, checkpoint/LoRA catalog resolution, **14**
  noncolliding durable ArtJobs, target attachments, result provenance and
  art-rich digest presentation all need to agree before the new writer is enabled.
- Authoring, preflight, creative checks, relatedness/novelty checks, transactional
  builds, 14-row ArtJob audit, facet assignment, digest/report, remaster, retry
  and rollback must all migrate together. The existing six-output writer must
  **fail closed on v3 drafts** until end-to-end CI passes.
- Tests should establish: old linked-world relations are preserved; original
  art stays stylistically coherent; Zuzu assets never link to the daily vibe;
  6 + 8 = 14 distinct assets and ArtJobs, one asset per Zuzu project in each
  type; scenario consequences; both checkpoint families resolvable from the
  actual catalog; historical six-output compatibility; no partial commits.
- Buffered unbuilt pre-cutover proposals need an explicit safe decision, not
  a silent rewrite or automatic discard. Already-built data stays unchanged.
- Earlier guidance to produce **one unlinked vibe plus eight Zuzu assets (nine
  total)** is **superseded**. Never reintroduce it, including in examples, tasks,
  pitches, or agent prompts. This clarification was made *before* any nine-record
  rollout had been merged.

## Daily pitch direction (effective for newly authored dockets starting 2026-10-13 PT)

Five daily pitches, all **expansions of existing active projects**: new stages/fighters for Zuzu Showdown, acts/ships/characters for Rainbow Princess Bullet Hell, book sections or card sets for Zuzu Gamebook, Shifting Lands encounter/deck packs, new follower sets and dilemmas for Emperor of Dust, or levels/power-ups for Arcade games. Each carries a real `target` project slug, an `expansion_kind`, a content hook, art plan and actionable first slice.

An approval is **not intake** and **not authorization to publish**. It is a durable request for the next agent to prepare a **polished scope and actionable roadmap additions in that existing project's roadmap.yaml**, with milestones, dependency ordering, tests/acceptance, art, and `source_pitch: pitches/<date>-<slug>.md` for deduplication. Notes from Silas must be folded in. Never create a new conductor or Kind Robots Project for a post-cutover daily pitch. Preserve pre-cutover pitch decisions and intake history.
