# The Ruler Is Hooked — full-game gap audit

Date: 2026-08-26

## Why this audit exists

The project is currently marked `finished` because all 15 tasks in the original roadmap are done and the roadmap goal is explicitly a **playable web proof of concept**. That is accurate for the PoC milestone, but misleading for the bucket-list game described in `DESIGN-BRIEF.md`.

The current implementation proves the architecture. It does **not** represent a mostly-developed full game.

This distinction matters because `project-overrides.yaml` currently excludes `ruler-hooked` from normal scheduling. A future lifecycle/roadmap reconciliation should reopen the project for full-game work instead of treating the completed PoC task count as product completion.

## Verified implementation as of this audit

Kind Robots contains a real playable prototype with:

- deterministic, framework-free turn/deck/effect logic;
- local/offline save slots and seeded runs;
- kingdom-health sliders and region-state effects;
- a compositing/fallback model for landscape regions;
- 25 authored cards, 3 narrative arcs, and 4 endings from the t-014 content pass;
- 11 bundled `CharacterRef` records used by those cards/arcs;
- an installable/offline PWA wrapper;
- a simple playable Vue surface with casting, event cards, health, endings, and save slots.

On 2026-08-26 Kind Robots PR #2130 also made the game directly discoverable from the Play navigation while preserving the existing `/plan/projects/ruler-hooked` route.

## Verified gaps

### Fishing is still a placeholder mechanic

The current turn loop treats fishing as a cosmetic heartbeat. Each cast advances the turn and has a 50% chance to increment the integer `fishCaught` counter. There is no fish species domain model, catch table, rarity/size/quality roll, lure or gear system, named catch result, fishing progression, or fish-driven economy.

This means the title activity of the game is currently less developed than the kingdom-choice prototype surrounding it.

### No Fishopedia exists

A repository search found no Fishopedia/Fishopedia implementation and no fish-species collection model. There is therefore no discovery catalog, caught/unseen state, specimen record, lore entry, habitat, rarity, size record, or collection-completion loop.

### Characters are content references, not a finished character system

The bundled content has 11 `CharacterRef` objects. That is useful data-driven scaffolding, but repository evidence does not show those slugs being seeded/linked as first-class Kind Robots `Character` entities, nor a portrait/expression asset set for the game cast.

The design brief explicitly calls for game characters to use or reuse the Kind Robots Character model where appropriate. That parity remains work.

### Encounter selection exists; encounter generation/authoring scale does not

The engine can deterministically select cards and advance arcs from authored data. That is a good runtime system.

The actual content is still a small static bundle. There is no demonstrated build-time encounter-generation/curation pipeline capable of producing, validating, balancing, and accepting a large offline deck. The final game must remain offline, so AI-assisted generation belongs in development tooling, not runtime.

### Gameplay art has not landed

The current stage component explicitly renders colored gradient bands so region changes are visible **before real art lands**, then attempts to overlay files from `/images/ruler-hooked/...` if they exist.

As of this audit, the tracked `public/images/ruler-hooked/` gameplay-art directory does not exist in Kind Robots. Project promo/tutorial art exists elsewhere, but it is not the composited gameplay asset matrix described by the design brief.

The current region manifest alone describes 37 authored state/time combinations:

- sky: 1 state × 3 times = 3
- far shore: 3 × 2 = 6
- treeline: 4 × 3 = 12
- village edge: 3 × 2 = 6
- castle grounds: 3 × 2 = 6
- lake: 1 × 2 = 2
- near bank: 1 base = 1
- ruler: 1 base = 1

That is **37 landscape-layer assets before card art, character portraits/expressions, fish art, rewards, endings, UI illustration, or additional content states**. If all 17 current region states eventually received exact variants for the five visual cycle positions already represented by the engine (`day`, `golden`, `dusk`, `night`, `dawn`), the environment alone would be 85 layer variants. A polished full game can therefore reasonably reach hundreds of art assets.

### Front-end quality is PoC-level

The current UI is functional, but it is intentionally simple: composited/placeholder stage, one cast button, health meters, event card, ending panel, and save slots. It has not reached the lively image-first presentation bar described in the Prime Monster reference section of the design brief.

## Recommended next roadmap

The existing m1–m3 history should stay intact as the completed **PoC phase**. Do not erase that work. Add new milestones for the actual game.

### m4 — Full-game vertical slice

1. **Reconcile lifecycle and goal** — reopen the project and make the goal distinguish PoC completion from full-game completion.
2. **Fishing domain model** — species, habitats/tables, rarity, size/quality, catch outcomes, lure/gear hooks, and deterministic seeded resolution.
3. **Fishopedia** — discovery/caught state, specimen records, lore/habitat/rarity data, personal bests, and an image-first collection UI.
4. **Character parity** — seed/reuse first-class Character entities, map content slugs, and define portrait/expression asset requirements.
5. **Encounter authoring pipeline** — development-time generation/import/validation tools that produce offline card/arc data, with duplicate, tone, trigger, balance, and broken-reference checks.
6. **Progression/economy** — fishing rewards, useful gear/unlocks, kingdom consequences, and reasons for catches to matter beyond an integer counter.
7. **Vertical-slice content target** — enough fish, characters, encounters, art, and endings to judge whether the core loop is genuinely fun before scaling production.

A reasonable first slice is deliberately smaller than the final catalog: roughly 12–20 fish species, several meaningful gear/lure choices, 5–6 substantial character arcs, and enough free-draw encounters that a replay does not immediately repeat itself.

### m5 — Art and content production

1. **Canonical gameplay asset manifest** — every environment layer/state/time, card, character, fish, reward, ending, and UI asset gets a stable key/path and generation status.
2. **Environment art pipeline** — establish one approved visual style with a small acceptance batch, then render the region matrix through durable ArtJobs.
3. **Character/fish/card production** — portraits/expressions, species illustrations, card scenes, rewards and ending art.
4. **Content expansion** — scale decks/arcs/endings only after the vertical slice demonstrates the systems and tone.
5. **Presentation polish** — move from prototype controls/gradient bands toward the image-first slideshow experience in the design brief; cover responsive, accessibility, refresh/direct-load and offline behavior.
6. **Playtest and balance** — repeated seeded runs, content-frequency telemetry during development, dead-trigger checks, economy tuning, and replay-variety targets.

## Completion language going forward

Use these phrases distinctly:

- **PoC complete**: true today.
- **Core engine mostly developed**: broadly fair.
- **Full game mostly developed**: not supported by the current repository/content/art evidence.
- **Project finished**: should be reserved for the full product goal once the lifecycle/roadmap is reconciled.

The next development work should prioritize the fishing/Fishopedia vertical slice and its asset/content manifest before launching a huge art batch. That gives the art pipeline a real schema to target instead of generating hundreds of disconnected pictures first.
