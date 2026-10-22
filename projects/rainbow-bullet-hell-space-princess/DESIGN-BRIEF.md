# Rainbow Bullet Hell Space Princess

**Project:** `rainbow-bullet-hell-space-princess`  
**Genre:** cinematic horizontal-scrolling shooting game, 1–4 simultaneous players  
**Target:** complete premium-feeling original web campaign inside Kind Robots Arcade  
**References:** *Gradius*, *Darius* and *R-Type* for scale, precision, boss spectacle and meaningful powerups. Copy no protected designs, music, names or specific layouts.

## Production reference

[WORLD-BIBLE.md](WORLD-BIBLE.md) defines the stage-by-stage production roster and [CAST-BIBLE.md](CAST-BIBLE.md) governs the four full character designs, inclusive casting, relationships and illustration prompts. WORLD-BIBLE.md: four pilots, 24 behavior-defined enemies, nine boss fights, twelve upgrades, opening/ending boards, and tracked art tickets. The registry is planned content until individually implemented and verified.

**Act pacing authority:** [ACT-STRUCTURE.md](ACT-STRUCTURE.md) defines the continuous eight-Act campaign, three major dialogue scenes per Act, boss-aftermath bridges, rare optional tableau intermissions, and persistent ship/party state.

**Story and dialogue authority:** [COMMS-AND-ENDINGS-BIBLE.md](COMMS-AND-ENDINGS-BIBLE.md) supplies Lilt-7, universal solo comms, all 15 unique pilot-party reveals, conditional cinematics and deterministic runtime-selection/QA contracts.

## The pitch

The Luminous Ocean has been swallowed by the Prism Eclipse, a machine reef turning deep-space wildlife into obedient starships. Four courageous star princess pilots embark on a pastel-rainbow rescue run through nebula shallows, fluorescent kelp rings and drifting coral fortresses. The world is cheerfully pink, but the challenge is substantial. **Every bullet must be legible and every death teach something.**

## Core play promise

- **One to four players simultaneously:** solo/local keyboard + gamepads and true online room co-op. 4-player support means four live hitboxes, shots, independent shields and lives at once, not turn-taking. Local co-op first; connected multiplayer is an explicit milestone, not silently dropped.
- **Designed authored campaign:** eight stages of roughly 10–15 minutes for a practiced first-clear path, with genuine branching encounters and later route reconvergence; eight memorable stage bosses, a final multi-form boss, and cutscene transitions. Stage count is a minimum; length and difficulty judged by measured completed runs, not title cards.
- **Shooting with intent:** tap/fire, precision-focus movement, rapid beam/charge distinctions, tactical limited supers, targeted power pickup routing, shield choice and recovery. Player ships have distinctive tactical niches without pay-to-win or randomized handicaps.
- **No unfair bullet blizzards:** high-contrast bullet rings, fixed-step deterministic patterns, telegraph-first bursts, human-sized escape gaps calibrated against ship speed and collision geometry, no required damage without warning. Advanced difficulty adds interesting patterns, not unreactable projectiles.
- **Powerup matrix:** beam lane, petal spread, arcing rainbow homing, orbit drones, resonant charge and point-defense shield. Upgrades may stack with limits; losing a life drops recoverable energy, never strips all agency.
- **Co-op without visual mush:** translucent player-shot treatment, 4 distinct ship silhouettes and non-color markers, layered projectile priorities, separate HUD elements, shared revive tokens, fair boss-health scaling, deliberate team supers.
- **Rich layered scroll:** multi-plane star/silt skies, slow nebula whales and floating ice, middle shipyards, near kelp/reef silhouettes, combat lane and readable weapon FX. Background layers can glow lavishly while bullets always win the contrast war.

## The stage campaign

| Stage | Authored location | Mechanic/route tension | Boss |
| --- | --- | --- | --- |
| 1. Pinkwake Estuary | sparkling shoal and coral port | gentle formation onboarding, drifting cover | **The Pearl Seahorse**, armored coilship |
| 2. Moonjelly Fields | floating translucent bell towers | electricity arcs and safe-gap ribbons | **The Aurelia Array**, jellyfish command swarm |
| 3. Chromatic Trench | deep midnight indigo current | choose safer winding passage or salvage gauntlet | **Clawburst**, mantis-shrimp railgun corvette |
| 4. Rosefin Express | neon migratory space current | velocity changes and escort route | **Delphion**, dolphin interceptor twinship |
| 5. Blossom Wreckyard | derelict flower-ring cruiser | optional rescue pockets, destructible geometry | **Sawtooth Regent**, shark destroyer |
| 6. Crown Reef | colossal living machine coral | multi-path gates and satellite suppression | **The Lantern Ray**, manta carrier |
| 7. Glass Current | mirrored cosmos and fractured lanes | reflective bullet and drone reading | **The Glass Eel**, phased stealth dreadnought |
| 8. Eclipse Palace | artificial heart of the ocean sky | all learned mechanics remixed, elite formations | **The Prism Leviathan**, colossal whale-machine |
| Finale | heart of the machine reef | three forms, route-state payoffs and ending choice | **Eclipse Crown**, final superweapon |

Boss count deliberately exceeds stage count: eight end-stage encounters plus a separate finale. Branching changes encounters, upgrades and narrative outcomes without turning eight worlds into disconnected five-minute mini-games.

## Combat grammar and fairness

Enemy families begin with seahorse pickets (wave curves), moonjelly drones (delayed pulse arcs), mantis-shrimp kinetic snipers (charge warning), shark cutters (flank pressure), dolphin interceptors (synchronized sweep), manta carriers (deployable escorts), angler bait ships (false pickup tells) and octopus tendril fortresses (screen-area control). All are *futuristic spacecraft inspired by animals*, not ordinary sea creatures pasted onto a space wallpaper.

Telegraphs should be visible for enough frames to permit reaction at the intended scroll speed. Test from worst-case player positions with real movement acceleration, shield and focus movement. Keep a tested maximum total projectile/collider budget for four players; separate decorative particles from lethal bullets. Bosses have targetable component states, changing arenas and dramatic deaths, but clear vulnerable/readable hit regions.

## Technology and integration

Use existing Kind Robots Arcade surfaces, audio, device inputs, scores, art delivery and game-shell affordances. The high-count shooting scene may need its own batched Canvas/WebGL renderer and spatial hash. Isolate it behind a game adapter; use deterministic seeded fixed-step simulation and recordable inputs so CI can replay runs and co-op divergence. Avoid gameplay LLM and paid network services. Online multiplayer must undergo actual packet-loss/latency testing and reconnect handling before it is called complete.

The first working route is **`/admin/rainbow-bullet-hell-space-princess`** with a discoverable Admin navigation tab and `requiredRole: ADMIN`. Public `/play` and Arcade listing are an explicit publication gate; no silent auto-exposure while still making the first level.

## Opening and ending

Opening: a quiet floating seaside palace beneath a pink ring nebula; its royal signal fractures as the Eclipse Crown swallows a ship convoy. The princesses choose to fly, not await rescue. Three short skippable chapter vignettes reveal the truth of the machine reef. The final route can restore the wildlife fleet, rescue trapped pilots or win at the cost of lost Prism shards, producing distinct endings, credits and new-run incentives. Never bury the final payoff behind an endless survival loop.

## Acceptance bar

A complete first clear; 1–4 simultaneous playable pilots locally and online; eight authored stages plus real finale; all distinct bosses; skill-balanced powerups and shields; generous audiovisual treatment with individually readable hit danger; deterministic loss/restore/save tests; documented 60 Hz/frame performance on representative desktops with degradation controls; input/accessibility checks at mobile/tablet/desktop. Silas makes the final call after playing the actual build.

## Generation 2 (Silas, 2026-10-22 PT): route map and memory

"Rainbow space princess should have the same consideration. Games should have memory, recognize progress."
For a shooter the matching reference is **Star Fox 64**: the eight Acts become nodes on a **branching route
map** whose alternate paths open from things done in a stage (a captive rescued, an escort saved, a hidden
generator destroyed), with per-stage **medals**, **three save slots**, a persistent **Palace Hangar** where
medals buy bounded permanent upgrades, and pilot comms that recognise progress across runs. Four alternate
branch stages join the eight. Presentation moves to the N64 bar: animated pilot cut-ins, enemy cycles and
moving cutscenes, while bullets stay crisp code-drawn shapes. Shared rules:
[projects/kr-arcade/GEN2-STANDARD.md](../kr-arcade/GEN2-STANDARD.md). Roadmap milestone **m6** (t-026 to t-030);
art round 1 is `art/GEN2-ROUND-1.yaml`.
