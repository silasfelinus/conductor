# Daily Dream and daily pitch creative direction (Silas, 2026-10-12 PT)

Status: **approved direction; nine-asset Dream implementation pending**. This is a migration specification, not proof that the current six-record pipeline already meets it. The existing single-writer Daily Digest must remain healthy until an atomic, tested replacement is merged.

## Daily Dream after migration

Each Pacific day has two deliberately separate editorial lanes:

1. **One original daily dream vibe**, freshly invented and internally coherent, with its own distinctive setting, Facet combination, art direction and title. It remains independent. Do not make every other daily asset belong to its world or inherit its style.
2. **Zuzu-world production material**, drawn from the shared `worlds/zuzu` canon and allocated explicitly to either `zuzu-gamebook` or `emperor-of-dust`. This is authored game material, not six reskins of the independent vibe.

Daily minimum, including the standalone vibe: **1 unique vibe + 2 locations + 2 characters + 2 rewards (retain one ITEM and one SKILL until revised) + 2 moral-choice scenarios = 9 objects and 9 independently tracked durable ArtJobs**. The six Zuzu characters/locations/scenarios must not be turned into a second random daily world. Each dependent object needs an explicit `project_target` for its owning game. Rewards also need project targets. Avoid mixing incompatible period, characters, technologies, or lore from the two target games. Proposals must work in story/play terms, not merely be descriptive cards.

**Scenarios are choices:** each has an immediate incident, at least two consequential options, a meaningful tradeoff, and short- and longer-term fallout. No binary saint/villain framing. For gamebook, specify the branching scene, flag/skill effects and replay outcome; for Emperor, specify dispatch candidates, Horde/faction/resource effects, injury risk and subsequent-day consequences, consistent with its existing rules.

Art should **mostly use the Illustrious and Arthemy checkpoint families** for Zuzu materials, with the canonical Arthemy series house lane for established Zuzu characters and gamebook scenes. Resolve checkpoint/LoRA identities from the current resource catalog and Zuzu art ledgers; do not guess IDs or silently switch to Flux/Krea. Preserve existing canon designs and reuse delivered art before creating duplicates. Select the checkpoint per asset in the durable ArtJob request, record actual checkpoint/LoRA provenance, and verify delivered ArtImages rather than equating enqueue with completion. The one independent vibe retains its own coherent original visual identity.

**Emperor of Dust has a separate, consistent visual pitch:** see `projects/emperor-of-dust/DAILY-DREAM-VIBE.md`. Its material belongs to a pre-Zuzu reign and is neither a new project nor a synonym for the day's free-form vibe. Follower mortality is rare, injury more frequent with X-day recovery; the Horde is numerical and followers are its named leadership, not the whole Horde.

## Safe migration

- Maintain the existing one-writer transactional boundary and idempotent date/asset IDs. Never hand-create the three extra objects by direct REST or a second cron.
- Version the proposal/builder contract from six to nine and update author prompts, deterministic Facet plans, validation, ledger IDs, transactional rollback, target routing, nine ArtJob outputs, art staging, facet targets, digest rendering, retry semantics, remaster audits and tests together. Historical six-asset proposals/builds remain readable and immutable; distinguish old/new via recorded schema version and Pacific date. No silent backfill.
- The Zuzu six or eight dependent records must NOT be attached as children of the unrelated unique vibe's Dream. Store project-target attribution in the proposal and built metadata, and link to real canonical entities through an explicit supported relation/API contract. If the API lacks this, stage a task-scoped handoff rather than invent a database foreign key.
- Tests must verify 1/2/2/2/2 counts, two genuinely independent editorial lanes, both project targets, choices/consequences, facet completeness, nine unique art requests and stable retries/rollback, digest display, old-bundle compatibility, and the absence of a second writer.
- Any buffered **unbuilt** six-asset proposals should be reauthored/retired into idea inventory under the new contract, not sent to the old builder after cutover. Already-built work stays untouched.

## Daily pitch direction (effective for newly authored dockets starting 2026-10-13 PT)

Five daily pitches, all **expansions of existing active projects**: new stages/fighters for Zuzu Showdown, acts/ships/characters for Rainbow Princess Bullet Hell, book sections or card sets for Zuzu Gamebook, Shifting Lands encounter/deck packs, new follower sets and dilemmas for Emperor of Dust, or levels/power-ups for Arcade games. Each carries a real `target` project slug, an `expansion_kind`, a content hook, art plan and actionable first slice.

An approval is **not intake** and **not authorization to publish**. It is a durable request for the next agent to prepare a **polished scope and actionable roadmap additions in that existing project's roadmap.yaml**, with milestones, dependency ordering, tests/acceptance, art, and `source_pitch: pitches/<date>-<slug>.md` for deduplication. Notes from Silas must be folded in. Never create a new conductor or Kind Robots Project for a post-cutover daily pitch. Preserve pre-cutover pitch decisions and intake history.
