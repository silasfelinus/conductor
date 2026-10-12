# Save the Plumber

**Project:** `save-the-plumber`  
**Genre:** complete original 2D side-scrolling platform adventure  
**Target:** eight memorable worlds, 32 authored levels, original villains, bosses and secrets  
**Reference bar:** *Super Mario Bros.* (1 and 2) for tactile precision, breadth of platforming toy interactions and complete campaign progression, never for copied art, names, level maps, soundtrack or exact enemy designs.

## The premise

Every kingdom gets a princess rescue. This time a resourceful young woman crosses a delightfully strange, misbehaving world to rescue her plumber boyfriend, a competent maker captured while investigating why water is running upward. She becomes the heroine by being the one who acts. Warm and lightly comic, with actual stakes and a satisfying reunion.

At New Game, a reproducible random seed chooses **one young adult heroine** from a curated appearance/name palette. She stays visually and narratively stable for the whole save. Outfit, hair, skin tone and name are cosmetic; every randomized heroine has identical collision volume, default abilities and progression odds. Player may reroll before beginning. This is not eight different random main characters per world.

## Control and play

- Responsive run, crouch, momentum, short/long jumps, coyote time, buffered jump, ladders, lifts and basic grab/throw interactions.
- Enemies are interactive toys, not merely hazards: step on, toss, stun, carry, redirect, trick and make them collide with the level. Different families react differently.
- Three broad power disciplines: **Springstep** for platform mastery, **Bottled Storm** for a charged projectile and interaction, **Pocket Lift** for carry and double-purpose environmental puzzles. Multiple upgrades, tradeoffs, upgrades never required to escape a checkpoint.
- Player has recoverable health, lives and continues, world checkpoints and a mode with forgiving restarts; default difficulty requires mastery but avoids blind traps, pixel-perfect unattested leaps and arbitrary deaths.
- Alternate exits, hidden room chains and optional collectibles reward curiosity. Route shortcuts are deliberate, not accidental boss skips. Persist saves with versioned IDs and deterministic random heroine seed.
- Real authoring first: the next stage has designed terrain, art, set-pieces, enemy combinations, secrets and a closure point; no thin infinitely stitched obstacle template presented as a world.

## Dramatic progression

The waterworks corporation **Stardrain** siphons ordinary rivers up into a giant machine citadel. Its mechanical curator **Lady Spigot** mistakenly believes redirecting every river will make the planet perfectly tidy; the plumber discovered a safety valve network and was captured before he could free it. The heroine follows his tool-mark trail, solves the world's physics toys, allies with misplaced factory creatures and reaches the central pump. Keep the antagonist original, fun to fight, and the plumber an actual person rather than silent prize art.

## Level design requirement

**Eight worlds × four substantial authored stages = 32 levels.** A world introduces a mechanic in stage 1, combines it in stage 2, turns it inside out in stage 3, and delivers a boss/escape set-piece in stage 4. At least eight unique world bosses with multi-phase readable tells. Every level has its own progression route and hidden discovery. World 8 revisits early mechanics in an earned climax.

Target skilled full-campaign length and challenge comparable to a classic complete console platformer, not eight loading screens around 20-second micro-levels. Record first-clear/playtest times by level and balance actual results.

## Visual and audio bar

A modern storybook side-scroller with lavish painted backgrounds, personality-rich enemies, animated water and machine props, clear platform silhouettes, at least three parallax depths, varied palette across worlds, interactive splash and hand-illustrated cutscenes. Original leitmotifs for heroine, plumber and Lady Spigot. The look can honor late-80s platform energy without cloning NES sprites. Art must function at browser scale and touch controls must not obscure pits or enemy tells.

## Runtime and surface

Use the existing Arcade app shell, shared sound/gamepad input, score and project linking where reasonable, but build a stable domain-level platformer simulation, own save version, maps, difficulty profile, achievements and stage runtime. Initial preview under **`/admin/save-the-plumber`** plus a discoverable Admin tab with `requiredRole: ADMIN`. Do not publicly expose a half-game as a shipped Arcade cabinet. The separate public `/play` route and Arcade card are a gate requiring Silas's approval.

## Definition of finished

Player can complete all 32 levels, defeat every boss, unlock secrets, save and resume, reach the full written illustrated ending and credits on phone/tablet/desktop/controller as supported. Automated replay proves collision determinism, attainable exits and no stage softlocks; manual first-playthrough validates checkpoints and challenge; shipped art URLs verified. A completed milestone checklist is not the final acceptance test: Silas plays the campaign and judges its depth and quality.
