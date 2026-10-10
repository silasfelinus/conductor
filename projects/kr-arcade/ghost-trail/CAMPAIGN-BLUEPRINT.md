# Zuzu: Ghost Trail — Campaign Rebuild Blueprint

**Owner:** `kr-arcade` / cabinet `zuzu-ghost-trail` in `kind_robots`  
**Direction:** Silas's 2026-10-10 acceptance of the moonlit ghost town, haunted ravine, and Bell Heretic mockups.  
**Status:** Implementation target, **not** a claim that the current game has these features.

## The promise

A complete original haunted weird-west action platformer worthy of a dedicated arcade cabinet: **60–90 minutes for a first successful normal-mode clear**, six authored stages with distinct mechanics, secrets, six headline boss encounters, a satisfying finale and post-clear challenge mode. A strong player can improve their run time; difficulty must come from mastery and discovery, not timer padding, endless enemies or artificial grinding.

Keep the current splash art, player/cabinet controls, free-play, shared leaderboard, accessibility preferences and 60 Hz deterministic simulation. Reuse the existing stage/enemy/boss module as a **prototype**; its four endlessly looping short trails are not the finished campaign.

## Visual target

The three accepted 2026-10-10 mockups establish the art language:
1. **Moonlit Ghost Town:** layered frontier streets, rickety saloon balconies and warm lanterns against purple mesas and a vast moon. Zuzu is readable in motion facing a spectral bone-coyote.
2. **Haunted Ravine:** broken bridge, tombstones and high vertical chapel terraces; Zuzu leaps between platforms while avoiding a ghost monk and bone beasts.
3. **Mission Bell Tower:** ruined stone bell architecture, burning braziers, crimson occult effects and the enormous Bell Heretic with a legible boss-health bar.

These are visual **concepts**, not usable tilemaps or verified collision geometry. Implement gameplay-authored silhouettes/tiles first; use generated backplates/character reference artwork as sources for layered art and animated sprite atlases. Do not flatten a screenshot into the interactive layer.

**Composition:** 4:3 playfield; important action fills the lower/middle 70%; Zuzu's gameplay silhouette should read at 40–48 logical pixels tall on a 240-high screen (the current vector hero is ~30). Larger enemies and 2–3× original prop detail; camera anticipates facing and vertical jumps. Preserve enough sightline for a reaction window. HUD height <=30 logical pixels. Foreground occluders must never hide a lethal tell or a landing spot.

**Palette:** midnight indigo, dusty plum, warm bone, amber lanterns, rust poncho, spectral cyan, and rare danger-crimson. Pixel and HD are *two exports of one art direction*; do not equate HD with interpolation of a tiny sprite. Keep scanlines optional, never baked into game assets. Any title, weapon, score or level text is drawn by the UI, not image generation.

**Canon:** koala Zuzu, stern expression, broad straw kasa, rust poncho with orange zigzag trim, katana hilt over right shoulder. The first hit tears off poncho/hat and changes sprite set; second hit is fatal. Consult `projects/comic-creator/issues/zuzu-koala-assassin-01/VIDEO-GUARDRAILS.md` and `CAST-PICKS.md` before every character prompt. The Zuzu world is an anthropomorphic strange west with Edo-era stranger Zuzu, not a generic samurai-versus-monsters reskin.

## Six-stage campaign (70–84 minute playtest budget)

| Stage | Major mechanics and authorship | Boss, secret, target |
| --- | --- | --- |
| 1. **Ghost Town / Silver Gulch** | Two acts: boardwalk/tutorial street then abandoned courthouse; diagonals, ladders, split rooftop vs street path | **Grave Marshal**, behind cover and two telegraphed lanes; secret saloon crawlspace; 9–11 min |
| 2. **Bone Yard / Haunted Ravine** | Two acts: crypts, shattering floors, long jumps, hanging bells and a broken bridge | **Bone Bull**, charge/stagger in redesigned arena; forgotten grave with first bell sigil; 10–12 min |
| 3. **Drowned Watering Hole** | Flood rises and drains on telegraphed cycles; moveable raft, submerged optional passage, escape route | **Drowned Ferryman**, two water-level phases; River Croc is a cameo/conditional ally, not a disposable monster; 10–12 min |
| 4. **Storm Crow Pass** | Canyon updrafts, tree canopy, moving rope lifts and sheltered caves; readable lightning timing | **Storm-Crow Matriarch**, summons vs safe perches; cave cache and shortcut; 10–13 min |
| 5. **Mission Bell Tower** | Switches, bell lifts, rotating hazards, stairways, falling masonry; boss foreshadowing throughout | **Bell Heretic**, giant chain/bell weapon and crimson waves; hidden bell order puzzle; 11–14 min |
| 6. **Abbey Beneath the Bell** | Hidden ritual tunnels, escalating rooms that remix learned moves; story discovery and optional rescue | **The Abbess**, two real telegraphed phases and an escape sequence; true ending through collected relics; 15–22 min |

**Structure:** two to three authored acts per stage, one mid-stage checkpoint each, bosses separated by recovery/decision beats, at least one branching path plus one unique secret each. Bosses demand movement and observation; not damage sponges. Stage 6 is a *conclusion* with credits/result summary, not an automatic lap back to stage 1. Post-clear New Game+ and score attack are opt-in.

**Timing definition:** first successful *normal campaign completion*, including cutscenes and exploration but excluding menu idling, should test at >=60 minutes for representative unfamiliar players, median 70–90. Also track fast skilled runs and all deaths/retries. Do not hard gate with a minimum timer. Failing to hit the runtime target triggers more authored encounter content, not slowed movement or HP inflation.

## Player mechanics and anti-farm policy

- Movement: responsive acceleration on the ground, committed jump trajectory with visual landing affordances, optional crouch/slide unlocked through play, bounded knockback. Each level introduces one new environmental interaction and revisits earlier ones in combinations.
- Attack: primary kunai stays usable throughout but has visible cadence and a small in-flight cap. Subweapons (three-way shuriken, returning kasa, lantern fire, iai cut) have distinct tradeoffs and resource/cooldown presentation. No held-key automatic super-speed fire.
- Enemy spawns: **finite encounter credits earned only by advancing into new world segments.** Standing in one place cannot generate unlimited foes, coins, points or lives. Death and checkpoint retries do not reset already-earned segment budget. Fixed authored enemy squads and secret ambushes replace the prototype timer spawner over time.
- Economy: enemy points + set-piece clear bonuses + remaining-time bonus + collectible treasure. Repeat kills after a checkpoint never count twice in a run; hidden room rewards have stable identities. Extra lives capped per stage or moved to relic milestones.
- Hit rule: poncho/hat loss, meaningful invulnerability/knockback, checkpoint restore. No frame-perfect mandatory blind jumps.
- Camera: forward lookahead, vertical rooms with safe preview of next ledge, no enemy creation outside telegraphable sightlines.
- State: track seeded run, discovered paths, resolved ambushes, opened crates, bosses, relics, checkpoint, time, deaths, ending. Story checkpoints/resume should avoid rewarding replay exploits. Leaderboard only accepts complete rules-compliant run submissions.
- Boss readability: at least three attack tells per boss, 0.5–1.0 seconds response time based on hazard, generous pre-attack windups, boss HP and phase changes communicated with sprite/audio/HUD.

## Art pipeline (Conductor -> durable ArtJobs -> assets -> game)

1. Queue per-stage **background reference plates** and **single-character model sheets** via `projects/art-prompts.yaml`. Stage backplates have *no interactive geometry*, text, HUD or foreground collision elements. Distinct layers required for final composition: sky, distant architecture, midground silhouettes, nearest dressing.
2. Check job IDs, results and actual final URLs. A queued request is not a rendered asset. Record jobs and image sources in the local art manifest.
3. Use the existing Zuzu Showdown sprite/rig pipeline as a starting point, with gameplay-specific actions: idle 6, walk 8, jump 3, fall 2, attack 5, throw 4, crouch 2, hit 4, poncho-loss 6, death 8. Separate poncho/intact vs exposed/tunic sets, mirrored only when canon-appropriate (katana handedness).
4. Create enemy atlas sets (idle, patrol, telegraph, attack, damage, death) and tileable foreground pieces on transparent backgrounds. Do not trust AI-generated multi-cell sheets without inspecting and normalizing frame geometry.
5. Output art for Pixel and HD using one versioned manifest with source prompt, model, ArtJob ID, original path, crop, transparent matte, pivot, visual bounds, frame durations, stage layering and license. Draw on 2D canvas using cached `Image` objects. Include vector fallback until assets have shipped.
6. The accepted mockups may guide palette/shape/lighting but are not exact gameplay maps. All collision platforms, enemy spawn positions, boss tells and secrets come from level data and tests.

## Definition of done / CI acceptance

- Deterministic no-input/held-attack 40-second tests cannot exceed 1,000 points or award extra lives in the starting area. Checkpoint suicide cannot reset the encounter ledger.
- Each stage has distinguishable art, geometry, enemy roster, mid-stage checkpoint, secret and unique boss; no full-route reuse of the same platform layout with a different background color.
- Test every main and secret route with seeded headless bot walks; no unreachable pickup, infinite stuck softlock, camera-less pit, stale projectile, invulnerable boss or permanent gate.
- Boss phase tests verify telegraph, active and recovery states; source-aligned hurtboxes and visual feedback.
- Art QA inspects sprite poses and atlas pivots on desktop/tablet/phone at DPR 1/2/3; check keyboard, gamepad and touch. Pixel and HD both render legibly.
- Manual playtest logs (actual elapsed time, deaths, checkpoints, secrets, boss clears, attack counts) support the >=60-minute campaign target. Existing high score submission remains compatible, with no farming loophole.
- Credits/ending and optional New Game+ are reachable only after six boss clears. Save/resume is deliberate rather than resetting secrets/rewards on reload.

## Delivery slices for agents

1. **Rules hygiene**: progress-gated enemy budget + deterministic regression (first PR).
2. **Asset direction**: art reference queue, delivered/reviewed plates, rigged koala poses and first playable sprite.
3. **Visual vertical slice**: Ghost Town layered terrain, parallax, enemy animations, boss tells and upgraded HUD, captured and vetted at screen sizes.
4. **Campaign engine**: authored encounter graph, secrets, progression, save/checkpoints and a real win state.
5. **World delivery**: stages 2–6 in sequential slices with unique gameplay and assets.
6. **Polish/QA**: boss tuning, soundscape/music, accessibility and elapsed-time testing.

**No substitutions:** do not represent queued images as shipped; do not present screenshots as actual engine renders; do not call a 4-stage infinite loop a 6-stage complete game; and do not declare 60-minute completion without a timed playtest.
