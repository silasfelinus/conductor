# Every Villain Tactics

**Campaign One:** Capes & Tassels: **Prom of Doom: Crossfire**. Conductor slug `every-villain-tactics`; master [kind_robots issue #4407](https://github.com/silasfelinus/kind_robots/issues/4407). Created 2026-10-28 PT.

## Premise

In Comet City, every rescue is somebody else's invasion. Direct a squad of beautifully animated illustrated comic cards across a cinematic tactical board, watch alliances and mission goals change mid-fight, and discover why each opponent believes they're saving the world. One permanent character name, four materially distinct hero / villain / henchman / sidekick perspectives and a unique fixed-ensemble route for each. The separate original 30-day Prom of Doom game remains intact.

## Tier / scope

Use the Playbook Kit **Vignette** contract first: a 20–40 minute First Bell fight with deterministic LOS, cover, hit odds, branching intro/mid-fight/finale and four genuinely authored perspectives for one protagonist. Expand to Standard/Saga only with playtest evidence and written allowance for six missions, 48 identities, 192 role arcs and 48 hand-written personal routes. These totals are deliverables, **not existing art/script completion**. Hero name and physical identity are stable across moral roles; reuse Prom of Doom's existing three story splash variants as sourced.

## Signature supporting casts (2026-10-29 PT)

Every one of Prom of Doom's 48 villain identities has a **different named one-hit henchman family**, loaded by the villain's stable origin×affinity signature, with a named representative, recognizable look, telegraphed gimmick, counter and narrative motive. Source: [Prom of Doom Villain Henchmen](../comet-city-academy/VILLAIN-HENCHMEN.md) and Kind Robots `utils/cometAcademy/villainHenchmen.json`. **Warren Wreckers** led by Foreman Thumpkin belong to **Cornerstone** and anchor the Picnic Panic burrowing-bunny one-shot. Other alien, psychic, magical and gadget-derived troops provide varied combat roles, not renamed mercenary placeholders. This authoring material requires tactical engine integration, ArtJobs and playable scenes before it counts as finished.

## Combat and presentation

A selected unit previews walking range/path, legal destinations and from-destination LOS, target range, cover and exact hit chance **before moving**. Show formula components (aim, range, height, flank, cover, status) and seeded roll; resolution and AI use same math. Square-grid tactical map with elevations, destructible terrain, overwatch, multi-turn objectives, dramatic enemy decisions and genuinely costly outcomes. Cards have idle depth/parallax, flip, movement, strike, damage, status and death animation, with reduced-motion equivalents. Full-screen console presentation, not a conventional dashboard; gamepad, keyboard and touch. PlaybookKitShell owns Settings, Cast, Scrapbook, Trailer, Endings and save affordances.

## Six authored missions

| # | Mission | Mechanics / cinematic beats |
| --- | --- | --- |
| 1 | **First Bell** | Assembly disruption; first cover/LOS fight; role-specific rescue testimony |
| 2 | **Science Wing Lockdown** | Lab doors and destructibles; sabotage reveal and henchman arrival |
| 3 | **Crosswalk Crisis** | Evacuation-versus-pursuit split; special-guest reinforcement |
| 4 | **Rooftop Broadcast** | Height/overwatch; mid-fight ally betrayal or reconciliation |
| 5 | **Under-Comet Breach** | Hazards and countdown; antagonist's understandable cause |
| 6 | **Prom Night: Everybody's Villain** | Three-phase siege with changing factions, callbacks and earned finales |

Every mission has a distinct playable opening cinematic, multiple conditioned mid-fight conversations, and several closing outcomes. An opponent's role in a path changes their motives, objectives and unique lines, not merely their card color.

## Expanded game structure (Silas, 2026-10-29 PT)

**The tactical game opens on a cinematic SPLASH / title screen**, not a directly loaded training battle. The first actions are New, Continue, Settings and Scrapbook. New/Continue support both story and self-contained one-shot battles; save slots must identify mode and campaign progress, and one-shot battles cannot corrupt ongoing story saves. Story mode can cast *any* of the 48 permanent heroes opposite *any* chosen hero as villain using authored default plot beats. **Each hero also has an individually written foil pairing**, with a custom opposing hero, cast, secrets, dialogue and route outcome; the default matchup and bespoke foil stories are different productions, not a template-swap. Keep the four role perspectives and 48 bespoke routes. The Scrapbook records heroes whose campaigns the player completed, defeated villains, unique scripted hero/foil routes, stage secrets, tactical achievements and earned endings. The scrapbook must derive from verified saved results, not an optimistic animation.

**Playable battle types:** six authored campaign missions plus replayable one-shot set pieces. Priority one-shot: *Picnic Panic*, a daytime picnic at the City Plaza besieged by burrowing bunny men. Core campaign scenes need a college quad with an imposing **central fountain** that blocks LOS and reshapes the approach, and a **tight science lab** with narrow aisles, delicate cover and hazardous props. Preserve existing six-part chapter structure; supporting arena variants may be encountered as one-shots, studio templates, or set-piece phases.

**Combat differentiation:** every hero has at least one bespoke tactical active power, separate from generic fire/overwatch. Distinguish short-, medium- and long-range attacks, movement/dash/reposition skills, durability/tanking and defenses, support, cooldowns/AP, and readable telegraphs. Exact from-destination hit previews remain valid for special abilities. Ordinary henchmen are a mechanically distinct one-hit tier (unless an explicitly telegraphed elite), including **burrowing monsters** who can surface on new board positions, **teleporting imps** who change flanks, and **malfunctioning children's toys** that swarm and obstruct. These are supporting cast/species rather than a change to the permanent 48 heroes. Monster/henchman species integrate with Facet `SPECIES` taxonomy.

**Round review / score:** every completed combat round presents a quick stage result/points screen with a transparent breakdown for no knockouts, no damage taken, clearing all enemies, discovering secrets, saves/rescues, optional objectives and relevant tactical bonuses. Differentiate turn-end from final mission-end results; do not interrupt combat after every turn unless deliberately designed as a quick intermission. Record earned results to the save and Scrapbook, and ensure failed missions have coherent scored outcomes. Scores are deterministic from recorded gameplay events and testable without a renderer.

**Implementation boundary:** the current First Bell prototype is a Playbook Kit Vignette; the new college-quad/science-lab/picnic map presets are not claims of their complete story scripts, original art, unique enemy AI, environmental effects or release eligibility. Full bespoke routes, imported painted assets, menu, and progress persistence get their own milestones and gates. Keep the internal admin route until authorized for public Play.

## Level + cutscene studio

A painterly admin editor for tiles, elevation, directional cover, blockers, hazards, spawns, waves, AI goals, civilians, win/loss, variables and reinforcements. Linked node-graph editor creates opening, conditional triggered and closing conversations with actor/role/expression, framing, branches and state effects. Triggers on turn, tile entered, LOS, health, objective, rescue, casualty, secret or combined predicates. Validate impossible wins, cycles, missing actors/assets and unreachable dialogue. One-click playtest. Versioned save/load of battle/RNG/trigger state; private owned drafts, forkable shared levels and immutable public revisions with access and moderation.

## Art / canonical dependencies

Read `projects/comet-city-academy/IDENTITY-SYSTEM.md`, `DESIGN-BRIEF.md`, `roadmap.yaml` and [the original Prom master issue #4181](https://github.com/silasfelinus/kind_robots/issues/4181). The 48 existing heroes have one permanent superhero name each. Link original identities, power sets and visual assets, tracking actual provenance. Commission gaps in tactical standees, expressions, attacks, damage, knockdown and six location illustrations through real ArtJobs; never count queued art as delivered.

## Completion

One complete end-to-end battle before expanding. Track actual authored scene and asset coverage for all 192 arcs and 48 bespoke six-mission scripts. Seeded adversarial tests, editor safety, permissions, saved RNG, endings, phones/tablets/desktops/XL and keyboard/gamepad/motion. First route is `/admin/every-villain-tactics`; human subjective acceptance and public release/community sharing are separate gates.
