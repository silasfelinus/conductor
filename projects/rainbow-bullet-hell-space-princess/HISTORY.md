# rainbow-bullet-hell-space-princess — task history archive

Full `note:` prose for completed rainbow-bullet-hell-space-princess tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-002 — Create cinematic production board, ship roster and boss storyboard

<!-- note:begin t-002 -->
Turn the brief into reproducible frame and enemy animation specifications: four heroine ships, base silhouettes and upgrades, enemy silhouettes and weak points, eight major stage-boss set pieces, final boss, intro/cutscene/outro panels, palette tokens, shots and parallax layers. Create source-led internal art requests with provenance. Make accessible design comps and ship only verified delivered art.

Created WORLD-BIBLE.md for four authored pilots, 24 distinct enemy behavior profiles, eight authored stage scores and finale, nine boss movesets, twelve pickup/powerup designs, storyboard boards and asset-ticket inventory. This completes the design-catalog slice; actual ArtJobs, rendered animation atlases and visual verification remain on this task and should return to ready after the documentation PR lands.

WORLD-BIBLE.md and DESIGN-BRIEF link merged as Conductor PR #6014. Authored cast, enemy behaviors, boss phases, 8 chapters plus finale, upgrades, storyboard C01-C17 and art tickets are ready for production. Remaining scope: submit tracked internal ArtJobs, verify delivered assets, build usable atlases and visual storyboard comps. No asset was rendered.

Authored CAST-BIBLE.md for all four adult princesses with the identities, bodies, gender expressions, cultural references and complex personalities Silas requested. Reconciled cast with existing ships/supers in WORLD-BIBLE, ART-DIRECTION, DESIGN-BRIEF, CONTROL and artwork prompt card. This is a design and prompt consistency update, not finished rendered portraits. Original t-002 art submission and verified asset/atlas work remain open.

Done 2026-10-17 PT, approved by Silas in session ('I allow and pass anything'). The
production board shipped: WORLD-BIBLE, CAST-BIBLE, ACT-STRUCTURE and COMMS bibles, and
the art they called for was rendered, reviewed and wired through t-022 rounds 1-31 (four
ships, cast portraits and cut-ins, every enemy family, nine bosses with three phases
each, guardians, pickups, eight stage strips and title cards), all now flying in the
eight-Act campaign on kind_robots main. Cinematic ending boards move with t-012.
<!-- note:end t-002 -->

## t-003 — Register private /admin Arcade prototype and isolated engine shell

<!-- note:begin t-003 -->
Inspect current Arcade renderer, games registry, input, audio and score APIs first. Add discoverable requiredRole ADMIN tab and private route; canvas/WebGL layer, pause, remappable input and gamepad support; no public /play exposure or published cabinet yet. Keep deterministic simulation separate from renderer and menu.

Private art-first flight-deck page, admin tutorial metadata, hidden Arcade registry preview, 1-4 seat deterministic Canvas 2D flight simulator, gameplay contract and placement have been committed for PR review. Eight stages and online multiplayer remain later roadmap tasks.

Merged kind_robots PR #3563 at deaab2f016fb2fcc13e199bef633cb26513eb343; 34 checks succeeded on f48df1f2552403b161eb31956215ba39f2bf81d3. Complete eight-file diff and reviews inspected. Actual Vue page and engine rendered in isolated Chromium at 390/768/1440px with no overflow and non-admin cabinet hidden. Shared cabinet/auth integration and full campaign acceptance remain later work. Tutorial body repaired through real tab resolver. Merge only, no deployment or public launch.
<!-- note:end t-003 -->

## t-004 — Implement ship movement, hitboxes, bullets, shields and weapons

<!-- note:begin t-004 -->
60 Hz fixed-step update, deterministic seeded scripted spawns, separate collision and graze hitboxes, invulnerability windows, primary/focus fire, charge/special weapons, 3-step upgrade paths, collectible power and shield modules, limited screen-clearing supers earned by play. No fake bullets, noninteractive art or score inflation.

Built real 60 Hz fixed-tick preview combat with normalized diagonal movement, focused flight, 4 distinct shot families, enemy projectiles, central hitbox, graze, invulnerability, collectible 3-step upgrades, shield modules and earned screen-clearing supers. Added seeded deterministic replay tests and private tutorial update. Await CI and integration review; stages/bosses are separate.

Reviewer accepted the scoped private combat foundation on October 12, 2026 at 3:51 AM PT. kind_robots#3590 merged at 439782cf4c5514b5a01a8813710fbd1adb071aef after all 32 checks completed green on d126aee609e57baf95bc4e75fcd0cdf6b5c0e71d. Complete four-file diff, comments/reviews and formatting repair inspected; no blocking review or protection bypass. Independent full branch arcade command passed 23 cabinet suites plus core/preview/seeded combat tests. Actual native 1/4-pilot renders at phone/tablet/desktop show independent numbered ships, live hostile bullets and readable charge/focus HUD without overflow. Private ADMIN preview remains excluded from public scores; stages, final cast art, network co-op and public launch remain separate tasks. No deployment or publication.
<!-- note:end t-004 -->

## t-005 — Deliver local 1–4 player simultaneous co-op with fair rules

<!-- note:begin t-005 -->
Join/leave without resetting campaign, 1–4 input slots, keyboard/gamepad assignments, readable colored/shape-coded ship markers and projectiles, independent lives, shield/revive rules, adaptive enemy pressure without hidden damage spikes, shared continues and per-player HUD. Test same-frame collisions, simultaneous supers and full four-player bullet load.

Partial local co-op integration drafted: Rainbow-only pause-time player switching in shared Arcade cabinet, optional live seat API, persistent benched ship positions/lives/upgrades, independent controls, bounded four-seat targeting/pressure, and earned Solenne Halo revive. Pure helper and real engine regression fixtures committed. Other 1-4 player acceptance and full in-run join/leave quality checks still remain. Reconcile with t-007 Pinkwake branch before final merge and return t-005 to ready after the scoped slice lands.

Quality pass 1 handoff merged in conductor#6052 at fb3d24a999224a7e7e777059b68449557a3403f1 after all 25 checks completed without failure on a4e7c9ff905cad1dc6ea7057a80fad7753216e3f. Release ownership and retain existing kind_robots#3599 for original-worker repair of inactive pilot pickup collection. Normal-input reproduction and scoped retry_context/TALKBACK are preserved; full branch arcade suite passes 29 cabinet suites but misses the consumer boundary. Reconcile/retest with repaired merged Pinkwake#3598 as required by the existing handoff. No gameplay merge, task completion, deployment or public publication claimed; full t-005 acceptance remains open. Avoid duplicate implementation and repeat rejection of unchanged heads.

Added real fixed-tick local co-op replay proving a benched pilot cannot collect a power pickup as it passes over the stored ship position, cannot receive unearned upgrades when rejoining, and preserves original position and lives. The engine active-seat pickup filter is already present on main; this codifies the quality pass1 reviewer reproduction. CI and broader shared-cabinet/device acceptance remain outstanding; after a green merge return t-005 to ready for its unfinished full co-op scope.

On October 12 PT, accepted partial quality repair in kind_robots#3614, merged at 0ead042a443bf072db86c520534459d6d0f8aa13 after all 28 current-head checks passed. Independently passed actual fixed-tick bench/pickup/rejoin test, removed only the active-seat collector guard in a local verification fixture and observed the intended failure, restored original bytes and passed again. Full shared-cabinet/device and 1-4 pilot acceptance remain unfinished. Retain pass1 history and dependent waiting gates; this is ready, not done and not recurring rearm. Do not close scope merely because #3599 or #3614 merged. Existing t-015/t-018 cover the remaining consumer fixture; no duplicate kaizen or done learning. No deployment/publication.

Acceptance complete in kind_robots#3768 (squash
d3c44f49b6172d492969320998fd863a2440435c), merged after all 20 checks passed on
51ec003a. verifyRainbowCoopLoad (test:arcade-engine) covers four same-frame supers with
Solenne's Halo, stacked same-frame hazards (mutation-checked: a ram that damages every
overlapping pilot fails it) and the four-seat Pearl storm load at about 0.08 ms average,
under 1 ms worst. verifyRainbowCoopCabinet (Rainbow cabinet browser workflow) drives
keyboard join, bench and rejoin through the cabinet's player switch without resetting
the Act, and four simultaneous touch pilots on a tablet. Shared continues landed with
t-016 in kind_robots#3760. Online co-op stays with t-006; physical gamepad play is
Silas's normal on-main check, not a gate.
<!-- note:end t-005 -->

## t-007 — Author and integrate stages 1–2 with complete tutorial and bosses

<!-- note:begin t-007 -->
Make two polished 10–15 minute authored scroll stages with wave scores, destructible cover, two distinct multi-phase bosses, collectable upgrades, checkpoint/continue and intentional difficulty curve. End each stage, not an endless swarm. Test 1-player and 4-player clears.

Submitted Act I Pinkwake vertical slice in Kind Robots with authored E01-E04 wave sequence, SOS-station rescue and shield award, B01 Pearl Seahorse three-phase boss, three low-threat Lilt-7 dialogue scenes, four parallax planes, deterministic fixture tests and private-admin tutorial. This is a shortened prototype, not t-007's two full 10-15-minute Acts; after a green merge return task to ready for the remaining full-length Act I and Act II work.

Reviewer quality pass1 recorded in merged conductor#6050 (4a76cf11c22a8210fe0c35d1c2e79b1bd0c30dc9), after all25 checks completed without failure on61eededd6f35f902e6f5bdd28b66a4ede23bcc5d. Retain existing kind_robots#3598 for its original worker to repair phase-boundary telegraph fairness; precise reproduction and retry_context preserved. The current implementation remains open despite greenCI; no gameplay merge or completion claimed. Release ownership for focused repair, avoid duplicate implementation, and preserve unfinished full ActsI–II scope and dependent co-op reconciliation. No deployment or publication.

On October12,2026 at12:53PM PT, reviewer accepted the scoped Pearl Seahorse fairness repair in kind_robots#3604 at9ba4375710d47fb94150ae7efe093b8ecf910230 after all28 checks completed successfully on540f36456a63d7b96daa8439ea70e000653b2ab4. Original#3598 had already merged at94ad676e04f258e6ad78652082f1efd1dc337ba4. Complete repair/formatting diff and reviews inspected, required checks satisfied and expected-head merge without bypass. Independent full arcade suite passed30 cabinet suites;1100 HP-threshold/crossing-frame scenarios covered5552 volleys, all with36 warning frames. Actual native1/4-seat initial warning/nonwarning renderer fits390/768/1440; these isolated demo proofs are not full device/auth/campaign acceptance. Initial Contract failure was only formatting in two named files; fixed through complete reads/current blob SHAs without baseline changes. Both final blobs verified on main. t-007 stays ready/unowned, passes1, for the full original unfinished scope; no done learning. Kaizen t-019 commits real player-damage/render cue replay. No deployment/publication.

Authored and integrated a deterministic second-act Moonjelly playable slice: continuous boss aftermath transition preserving lives, upgrades, score and local co-op; E05-E08-inspired new attack patterns; optional Nemi rescue with flag/charge consequence; three Lilt-7 conversation windows; B02 Aurelia Array with telegraphed 3-phase fan attacks and readable gaps; four-plane Moonjelly field parallax; seeded 1/4-pilot replay/boss warning tests; updated admin flight training. This remains a shortened vertical slice, not the full 10-15 minute two-Act delivery, full save/continue or browser acceptance. CI and actual render validation still required. Return t-007 to ready after merging verified reversible improvements.

October 12 PT at 10:32 PM: merged the scoped Moonjelly Act II continuation in kind_robots#3605 at cfdc04e8d57e3c76543ab68eb8fc49c4fd8879e8 after all 32 actual checks completed successfully on 9ff79308d618d61a6bac6bae080d6d889fd96579. Complete six-file diff and current reviews/threads inspected; required checks and approval rules satisfied, expected-head merge without bypass. Full combined Arcade command and nondemo 1/4-seat Nemi rescue/two-boss replay passed; resources persist through transition. Native Canvas warning renders at 390/768/1440 fit. This is a shortened private vertical slice: full 10-15-minute authored Acts, checkpoint/continue and shared-cabinet/device acceptance remain unfinished. Release ownership, preserve pass1 and dependent waiting gates; ready, not done or recurring rearm. No completion learning, deployment or public publication.

Progress 2026-10-16 (session 2026-10-16T131500Z-rainbow-act1-formations-q7v3), all
merged green on kind_robots main: #3750 Act I authored formation director (49 waves,
school bonus); #3752 Act II on the shared formation director (33 waves); #3757 painted
Act intro splash; #3760 checkpoint/continue (CONTINUE? countdown, rewinds the Act clock
to the last section checkpoint, score returns to the checkpoint, demo replays unchanged;
ordinary-input replay test); #3763 three escalation sections per Act (Act I 83 waves/273
craft, Act II 64 waves/202 craft, ten checkpoints each). Measured: the immortal demo
beats B01 at frame 15,834 (about 4.4 min) and clears Act II by frame 30,944 with one
pilot. Remaining: full 10-15-minute measured first clear per Act, and actual 1/4-player
shared-cabinet/device acceptance. Ready, not done.

Progress 2026-10-16 PT (kind_robots#3770 at 2b3ca7a6, #3771 at ec047fe9, both merged
green): boss hulls scale with the crew (2.5 base shares for the first pilot, 4 for each
after) with phases at two thirds and one third; a continue mid-fight keeps the damage
dealt; Act I gains Coral chicane, Urchin nursery and Tidal crescendo and Act II gains
Bell canyon, Relay storm and Bell veil (eleven sections and thirteen checkpoints each).
verifyRainbowFirstClear measures ordinary pilots: solo Act I 8.53 / Act II 8.87 min with
continues, four pilots 6.25 / 6.71 min; clean demo 6.7 / 6.5 min. The bible's 10-15
minute per-Act target (excluding retries) still needs about three more sections per Act;
ACT_FLOOR_MINUTES is a ratchet at 6. Device play remains Silas's on-main check.

Done 2026-10-16 PT. Acts I and II meet the world bible's pacing as written: a clean solo
run (deathless demo, retries excluded) takes 10.20 and 10.04 minutes per Act, asserted
10-15 in verifyRainbowFirstClear. Ordinary pilots with continues: solo 12.18 / 14.85,
four pilots 10.00 / 10.83. Delivered across kind_robots#3770 (boss hulls scale with the
crew, continues keep boss damage), #3771 and #3773 (authored sections), #3774 (Urchin
and Lantern mid-Act guardians), #3776 (three more sections per Act; squash 082ff35e).
Each Act: eighteen sections including a guardian, twenty checkpoints, two three-phase
bosses with 36-frame telegraphs, wave school bonuses, breakable coral cover, pickups,
tutorial in the admin tab. 1- and 4-player clears are tested in engine and in the shared
cabinet (Chromium fixtures for keyboard, gamepad and four touch pilots); physical-device
play is Silas's normal on-main check.
<!-- note:end t-007 -->

## t-008 — Author branching stages 3–5 and three distinct bosses

<!-- note:begin t-008 -->
Multiple encounter branches with persistent route choice, different silhouettes and objectives, jellyfish electrical fields, mantis-shrimp kinetic salvos, and dolphin escort-versus-pursuit patterns. Validate reachable paths and weapon viability. Progress 2026-10-17 PT: Act III (S03 Chromatic Trench) is playable end to end on kind_robots main. Its four craft and B03 Clawburst merged in #3777, and the Clawstrike guardian and the first pacing pass in #3779. #3780 brought a clean solo run to 10.12 min and added the salvage-vault versus safe-passage route choice. That choice persists through checkpoints, sets securedSalvage and changes later dialogue. Round-25 art (E13-E18, the Clawstrike guardian and B04/B05 phases) is in #3781. Next are Act IV (S04 Rosefin Express: E13-E15, the courier escort and B04 Delphion) and then Act V.
Done 2026-10-17 PT. Acts III-V and their bosses are on kind_robots main. Act III (#3777, #3779, #3780) has the salvage-vault versus safe-passage route, which sets securedSalvage. Act IV (#3783) is the Rosefin Express: E13-E15, the courier escort (rescuedCourier) and B04 Delphion, with the salvage dock as the intermission into it. Act V (#3784) is the Blossom Wreckyard: E16-E18, a scrap field, the 40-second depot-or- armory fork (freedDepot) and B05 Sawtooth Regent, ending on the memorial. The verifiers fly every route; clean solo runs are 10.12, 10.19 and 11.09 min. Every boss telegraphs all three phases.
<!-- note:end t-008 -->

## t-009 — Author stages 6–8, route convergence and final boss

<!-- note:begin t-009 -->
Finish substantial late campaign, capital reef-ship encounters, shark interceptor packs, final fortress with a readable multi-form showdown and ending branches. Eight stage bosses plus final boss; interstitial cutscenes and complete credits. Progress 2026-10-17 PT: Act VI (S06 Crown Reef: broodships, turrets, bulwarks, reef gates, Lilt's revelation, the relay-or-cache fork and B06 Lantern Ray) merged in kind_robots#3787, 10.43 min solo. Act VII (S07 Glass Current: mirror eels with phantom pellets, crystal squids, harbingers, prism pylons, the Mirror guardian, the machine echo, the optional Lost Navigator rescue and B07 Glass Eel) is in #3789, 10.76 min solo, with round-27 art (E22, E24, the Bulwark guardian, B08/B09 phases), merged. Act VIII (S08 Eclipse Palace: legacy craft in elite formations, the captive armada freed by breaking collars, the Herald guardian, a mid-Act council where earlier rescues add support, and B08 Prism Leviathan) is in #3790, 10.55 min solo. Next is the S09 final confrontation (B09 Eclipse Crown), endings and credits.
Done 2026-10-17 PT. Acts VI-VIII and the finale are on kind_robots main: Act VI Crown Reef (#3787, relay-or-cache fork, B06 Lantern Ray), Act VII Glass Current (#3789, phantom pellets, optional Lost Navigator rescue, B07 Glass Eel), Act VIII Eclipse Palace (#3790, legacy craft in elite formations, the captive armada freed by collars, a council where earlier rescues lend support, B08 Prism Leviathan), and the S09 finale (#3791: B09 Eclipse Crown's spokes and drifting heart, the restore/evacuate/sever choice flown by the crew, the prism-corridor escape, an ending composed from the choice, the six rescue flags and the crew, credits naming the rescued, THE END). The demo plays the whole campaign from Act I to THE END for 1-3 pilots; clean solo Acts run 10.4-10.8 min. Cinematic ending boards, voice and the 15-mask comms tracks remain t-012.
<!-- note:end t-009 -->

## t-010 — Add balanced 4-ship loadouts, upgrade matrix and replay incentives

<!-- note:begin t-010 -->
Four distinctive princess-ship silhouettes and mechanically meaningful beam, spread, drone and precision weapon families; bomb/super economy, shields, recoverable dropped upgrades, checkpoints, scores, medals, no-hit goals, difficulty settings and save/continue. Every default ship can beat every boss, including in a fresh run. Progress 2026-10-17 PT (Silas asked for difficulty levels): Cadet, Pilot and Ace merged in kind_robots#3796. A generic cabinet difficulty switch (meta.difficulty names, remembered per game, ArcadeGameOptions.difficulty); Rainbow scales lives (5/3/3), enemy pellet speed (0.8/1/1.15), craft (0.8/1/1.25) and boss hulls (0.7/1/1.3), and the recorded score (0.5/1/1.5) so one leaderboard stays fair. Remaining: ship loadouts and weapon families, the upgrade matrix, medals and no-hit goals, and save/continue across sessions.
Done 2026-10-17 PT. Difficulty (Cadet/Pilot/Ace) #3796; focused weapon families per ship (Rose Needle, piercing Prism Thread, converging Halo Link, wall-glancing Comet Arc), gold/silver/bronze Act medals, a 7-rung mastery ladder (First Light, Gold Wing, The End, Guardian Breaker, No One Left Behind, Every Ending, secret Ace) and Act-start saves with a Flight Log continue/new menu in #3798; U12 Recovery Cache (the lost power level waits 4 s for its pilot) in #3803; the pilot and difficulty select Silas asked for in his first playtest follows in the playtest PR series. Every default ship flies the whole campaign in the demo verifiers. Upgrade catalog still open for later slices: U03 Tide Tracker, U05 Echo Charge, U07 Repair Pearl, U09 Rescue Beacon, U10 Mirror Lens, U11 Score Coral.
<!-- note:end t-010 -->

## t-011 — Build lavish stage parallax, readable effects and character animation

<!-- note:begin t-011 -->
At least four separately moving planes per stage, rich painted underwater-cosmos scenery, sprite rigs or atlases, telegraphed boss tells, particles, lens/bloom budget and cinematic explosions. Set projectile outlines and luminance contrast independent of backgrounds; performance budgets, colorblind-safe and reduced-motion modes.
Progress 2026-10-17 PT: explosions as sparks within a 160-spark budget (bosses and guardians burst bigger with a shockwave), calm motion (the arcade's still-camera choice, which follows reduced motion: no full-screen flashes or shockwaves, fewer sparks, scenery at 30% drift) with a cabinet Motion switch that applies mid-game, and a dark halo under every solid hostile pellet merged in kind_robots#3802. After Silas's first Act I playtest: hit flash on damaged craft, craft shockwaves, pickup collect bursts and bobbing pickups, ship banking (#3805). Open: painted scenery planes per stage, sprite rigs, lens/bloom.
2026-11-01 PT claim-staleness assessment (Silas: stale claims are more likely finished- but-unrecorded than abandoned): partial work merged (#3802, #3805); open items per the 10-17 progress note: painted scenery planes per stage, sprite rigs, lens/bloom. Claim released.

Added a separate slow-moving atmospheric ocean scenery plane in a scoped Kind Robots branch. Further painted art, atlases and effects remain open.

PR silasfelinus/kind_robots#5351 merged as 27dae5faad78467b2af7bb39ad8264e241150603 after nine GitHub Actions workflows completed successfully, including TypeScript, Rainbow Cabinet Browser Contract, viewport matrix, Contract Tests and formatting. Added slow-moving bioluminescent ocean atmosphere. Task remains incomplete: painted stage planes, sprite atlases, lens/bloom and visual acceptance are outstanding.

Scoped ambient-motion fix: the sky's star twinkles and doodle pulses/rotation now honor calm-motion drift; full painted art and atlas scope remains outstanding.

Recovered stale review after PR #5355 was merged as ce8717b1; painted scenery, sprite atlases, visual effects and verification remain. No matching open Rainbow PR or task branch found. Return to ready, preserving shipped work.

Added two distant painted parallax depths to every main Act using its integrated reviewed scenery strips, with subdued alpha, independent scroll speeds, calm-motion scaling and regression assertions. Implementation commit 0a4553aa7b8040b8b523521fc03971750edf7364; broader original painted scenery and sprite-artist scope remains.

Additional scoped visual-effects increment in silasfelinus/kind_robots#5428: two-frame-budgeted localized boss glow, capped alpha and radius, under hostile bullet halos, suppressed entirely in calm mode; regression coverage for budgets and draw order. PR and latest-head CI pending; full t-011 art and atlas scope remains unfinished. Do not mark done until delivered assets and visual QA.

2026-11-24 PT intent audit: the increment's PR silasfelinus/kind_robots#5428 merged; the claim from 2026-11-20 was never released and the note says the wider scope is still partial. Returned to ready with the claim cleared so the next worker can pick it up. No scope change.

2026-11-24 PT lens/bloom increment: each budgeted boss flare (max 2) now draws one thin anamorphic lens streak, fainter than its glow. High-contrast shots (t-044) skip the bloom and streak entirely, so no screen-blend wash lifts scenery behind pellet halos. Calm motion still draws nothing. PR silasfelinus/kind_robots#5745 merged as 5e62f57e after 22 checks passed. Still open: painted stage planes, sprite rigs/atlases and visual acceptance. Stays ready and unclaimed.

2026-11-24 PT character-animation increment: a craft a shot just hurt now flinches,
squashing up to 14% and springing back over its six white-flash frames. Calm motion
keeps the flash only. New pure helper rainbowHitFlinch, with assertions in
verifyRainbowEffects. PR silasfelinus/kind_robots#5746. Still open: painted stage
planes, sprite rigs and atlases, and visual acceptance.

PR silasfelinus/kind_robots#5746 merged as 0d7a9d09 after 23 checks passed. The hurt-
craft flinch is live on main. Still open: painted stage planes, sprite rigs and atlases,
and visual acceptance. Stays ready and unclaimed.

2026-11-24 PT surge-lean increment: the pilot craft now stretches when surging forward
and squats when backing off, on top of the bank, via the pure helper rainbowShipPose
(draw-only, hitbox unmoved). Calm motion now damps the bank too. PR
silasfelinus/kind_robots#5747, CI pending. Still open: painted stage planes, sprite rigs
and atlases, and visual acceptance.

PR silasfelinus/kind_robots#5747 merged as b21837fb after 22 checks passed. The surge
lean and calm-damped bank are live on main. Still open: painted stage planes, sprite
rigs and atlases, and visual acceptance. Stays ready and unclaimed.

2026-11-24 PT boss-windup increment: B01 Pearl Seahorse now draws back and swells across
its 36-frame warning, deepest just before the volley, so the body telegraphs the beat
with the glow ring. Pure draw-only helper rainbowBossWindup (hitbox unmoved; calm keeps
a fifth), shared BOSS_TELEGRAPH_FRAMES. PR silasfelinus/kind_robots#5748 merged as
3e8c39c6 after 21 checks passed. Still open: painted stage planes, sprite rigs and
atlases, and visual acceptance. Stays ready and unclaimed.

2026-11-24 PT eel/ray windup increment: B07 Glass Eel (true body only) and B06 Lantern
Ray now wind up across their own warning lengths with the shared rainbowBossWindup;
nurseries, beacon, outline and rings stay on the hitbox. New exports
glassEelWarningFrames/lanternRayWarningFrames, assertions in verifyRainbowEffects. PR
silasfelinus/kind_robots#5752, CI pending. Branch-medic in the same run opened
kind_robots#5749-5751 to land the three round-1 critic reports. Still open: painted
stage planes, sprite rigs and atlases, and visual acceptance.

PR silasfelinus/kind_robots#5752 merged as 2492afc8. The B07/B06 windup is live on main.
Still open: painted stage planes, sprite rigs and atlases, and visual acceptance. Stays
ready and unclaimed.

2026-11-24 PT B04/B08 windup increment: B04 Delphion twins and B08 Prism Leviathan's
painted body now wind up across their own warning lengths with the shared
rainbowBossWindup (new delphionWarningFrames/prismLeviathanWarningFrames exports).
Coupling, link core, spire locks, gem and cue rings stay on the hitboxes; calm keeps a
fifth. PR silasfelinus/kind_robots#5753 merged as 20cbf17f after 21 checks passed. Still
open: painted stage planes, sprite rigs and atlases, and visual acceptance. Stays ready
and unclaimed.

2026-11-24 PT B05/B03 windup increment: B05 Sawtooth Regent and B03 Clawburst body
sprites now wind up across their own warning lengths with the shared rainbowBossWindup
(new sawtoothWarningFrames/clawburstWarningFrames exports). The Regent holds still mid-
charge; ring, jaw and cannon stay on the hitboxes; calm keeps a fifth. PR
silasfelinus/kind_robots#5754 merged as 706d0d36 after CI passed. Still open: painted
stage planes, sprite rigs and atlases, and visual acceptance. Stays ready and unclaimed.

2026-11-24 PT B02/guardian windup increment: B02 Aurelia Array (the last boss without a
body tell) and every act guardian now wind up across their 36-frame cues with the shared
rainbowBossWindup (new MOONJELLY_WARNING_FRAMES export; a leaving guardian rests).
Rings, lanes, HP bars and hitboxes stay put; calm keeps a fifth. PR
silasfelinus/kind_robots#5755, CI pending. Still open: painted stage planes, sprite rigs
and atlases, and visual acceptance.

PR silasfelinus/kind_robots#5755 merged as a743a411 after all checks passed. B02 and
guardian windups are live on main; every boss and guardian now telegraphs with its body.
Still open: painted stage planes, sprite rigs and atlases, and visual acceptance. Stays
ready and unclaimed.

2026-11-24 PT boss-recoil increment: every boss body (B01-B08, moon colony) and guardian
now rocks back about 2.5px and squashes slightly when a shot lands, then settles over 8
frames. The recoil is added on top of the windup via the pure helpers
rainbowBossRecoil/stackRainbowBossPose. It only changes drawing: hitboxes stay put, and
calm motion keeps the body still. Hit times are kept in a WeakMap, so no boss type
changed. PR silasfelinus/kind_robots#5763 merged as c3c41e43 after 23 checks passed.
Still open: painted stage planes, sprite rigs and atlases, and visual acceptance. Stays
ready and unclaimed.

2026-11-25 PT craft-windup increment: charging small craft (squid, harbinger, turret,
hammerhead, brood) now tense their bodies across their own charge warnings with
rainbowCraftWindup (the boss windup at half strength; CRAFT_WINDUP_FRAMES). Draw-only;
calm keeps a fifth; truce craft never tense. PR silasfelinus/kind_robots#5793 merged as
ae5461fd after all 21 checks passed. Still open: painted stage planes, sprite rigs and
atlases, and visual acceptance. Stays ready and unclaimed.

2026-11-24 PT pilot hit-jolt increment: a landed hit now knocks the pilot's craft back,
twists and squashes it over 10 frames (rainbowShipJolt, SHIP_JOLT_FRAMES), recorded in a
WeakMap at hitShip so the Ship type is unchanged. Draw-only; calm keeps it still. PR
silasfelinus/kind_robots#5802 (head a3a13163), CI pending. Note: #5797 (idle loops for
courier, cutter, clawstrike, dolphin) also merged since the last note. Still open:
painted stage planes, sprite rigs and atlases, and visual acceptance.

PR silasfelinus/kind_robots#5802 merged as 8a2f599c after all 23 checks passed. Pilot
hit-jolt is live on main. Still open: painted stage planes, sprite rigs and atlases, and
visual acceptance. Stays ready and unclaimed.

2026-11-24 PT idle-hover increment: a parked pilot craft now hovers (~1px bob, slight
sway, offset per seat) and fades into the flight pose as she banks or surges
(rainbowShipHover); the hull alone moves, so the hitbox core marker stays put. Maribel's
barrel roll now honours calm motion (rainbowBarrelRoll: shallow squash, no full flip).
PR silasfelinus/kind_robots#5807, CI pending. Still open: painted stage planes, sprite
rigs and atlases, and visual acceptance.

PR silasfelinus/kind_robots#5807 merged as 4769f260 after all 23 checks passed. Idle
hover and calm barrel roll are live on main. Still open: painted stage planes, sprite
rigs and atlases, and visual acceptance. Stays ready and unclaimed.

2026-11-25 PT pickup-bob increment: loose pickups' bob, ring pulse and glow moved into
the pure helper rainbowPickupBob; calm motion now keeps a fifth (it previously ignored
calm), and the no-sprite fallback badge and letter ride the same bob instead of sitting
still under the ring. PR silasfelinus/kind_robots#5809 merged as 73244d1c after all 23
checks passed. Still open: painted stage planes, sprite rigs and atlases, and visual
acceptance. Stays ready and unclaimed.

2026-11-25 PT current-crackle increment: the live eel barrier's alpha flicker and link
jitter and the Prism Beam's width throb (the fastest flickers on screen, and the last
ones ignoring calm) moved into the pure helper rainbowCurrentCrackle; calm keeps a fifth
of each. Draw-only. PR silasfelinus/kind_robots#5826 merged as 37e5a38d after all 22 run
checks passed. Still open: painted stage planes, sprite rigs and atlases, and visual
acceptance. Stays ready and unclaimed.

2026-11-25 PT signal-pulse increment: the last fast signal-light flickers that ignored
calm motion (the captive's collar, a glowing prism pylon's core, a relay pylon's lamp, a
staggered dolphin's daze ring) moved into the pure helper rainbowSignalPulse; calm keeps
a fifth of each swing. Draw-only. PR silasfelinus/kind_robots#5827 merged as 471f20dc
after all 23 checks passed. Still open: painted stage planes, sprite rigs and atlases,
and visual acceptance. Stays ready and unclaimed.

2026-11-25 PT route-marker increment: the dashed route-fork lines (trench, wreckyard,
crown reef) and the lighthouse next-lamp lane marker, the last 8-frame flickers that
ignored calm motion, now use rainbowSignalPulse, so calm keeps a fifth of the swing.
Draw-only. PR silasfelinus/kind_robots#5828 merged as afad99e8 after all 22 run checks
passed (recorded from superseded conductor#8020).

2026-11-25 PT acceptance reconciliation: the 'still open' list was stale. Painted stage
planes shipped under t-022 (sky, far, mid and fore for S01-S09 in both looks), and enemy
idle atlases plus pilot poses shipped under t-030. A contact sheet compositing all nine
stages' four planes at engine geometry shows every plane present. PR
silasfelinus/kind_robots#5830 pins the criterion in verifyRainbowGameArt: every stage
has four committed planes, each drifting faster than the one behind it. With that
merged, every t-011 criterion is met in code. Silas's subjective visual sign-off belongs
to t-042 (final creative approval), not this task. Close to done once #5830 merges.

PR silasfelinus/kind_robots#5830 merged as dfe3e290 after all 13 checks passed
(including TypeScript and Every Rainbow verifier). Every t-011 criterion is met and
pinned in tests. Silas's subjective visual sign-off continues under t-042.
<!-- note:end t-011 -->

## t-015 — Prove private flight-deck help and controls through the actual shared cabinet

<!-- note:begin t-015 -->
Reviewer kaizen after PR #3563: add a browser fixture using the actual shared ArcadeCabinet and Admin tab help renderer at phone/tablet/desktop widths; verify visible tutorial text, keyboard/gamepad pause/remapping and independent seated inputs. Keep private routes and scores excluded from public discovery. Local isolated engine pixels are not this integration proof.

Scoped Space Princess touch-D-pad responsiveness fix and pure eight-way input tests committed in Kind Robots branch. This does not yet satisfy t-015's full browser fixture requirement; leave task ready after merging the partial UX improvement.

Reviewer accepted the partial touch-control improvement on October 12, 2026 at 3:51 AM PT. kind_robots#3588 merged at 405f8f4cdca65c38d7f912dc62b52b0d92272cbb after all 30 checks completed green at fdfd06f8a3bf5116a99c198d48c5ac1e5d071d63. Full three-file diff and formatting-only ratchet repair inspected. Independent full branch arcade command passed 23 cabinet suites and preview checks. Actual extracted cabinet handlers/CSS in native browser fixtures at phone/tablet/desktop verified continuous diagonal drag, secondary-finger rejection, cancel/lostcapture release and the unchanged generic dead zone. This isolated handler proof does not complete the actual shared-cabinet/help integration fixture required by t-015. Return it to ready, clear ownership and retain implementation provenance; finish the original remaining scope in a new focused continuation, without duplicate fixture work. No deployment, publication or new human gate.

Done 2026-10-16: kind_robots#3766 merged green (all 21 checks, including the new Rainbow
Cabinet Browser Contract workflow). verifyRainbowCabinet.browser.test.mjs compiles the
actual arcade-cabinet.vue and tutorial-flyer.vue (scoped styles included) and mounts
them in Chromium with only the stores stubbed, the real admin tab content resolved
through resolveChannels, and the real Rainbow engine. At 390/768/1440px the flyer shows
the help headings and the cabinet fits with no sideways scroll; Enter starts, P/Escape
and gamepad Start pause and resume without refilling anything; two pilots split the
keyboard (S moves only P1, up-arrow only P2); with three pilots and one pad the pad
drives only P3. Fixed a real gap it found: gamepad players could not pause mid-run, so
games that never read Start in play can now opt in with ArcadeGameMeta.startPauses
(Rainbow does; other cabinets unchanged). Updated the stale how-to card (B REPAIR
SHIELD), blurb and admin help (checkpoints and continues). Synthetic input, not
physical-device evidence; touch replay stays with t-018. Private admin route unchanged.
<!-- note:end t-015 -->

## t-016 — Add a per-pilot ArtJob manifest and cast-identity QA contract before any atlas is marked ready

<!-- note:begin t-016 -->
Reviewer kaizen after Conductor PR #6021: check portrait identity/colour consistency, body-silhouette diversity, facial consistency across cinematics and rights/provenance against CAST-BIBLE.md. Docs only; do not overwrite approved art.

Done 2026-10-16: added art/CAST-MANIFEST.yaml (every shipped pilot asset with ArtImage,
ledger key, ArtJob, engine/checkpoint, seed and source image, generated from the ART-
ROUND ledgers and the kind_robots commits that shipped them, plus coverage of the CAST-
BIBLE base deliverables) and CAST-QA.md (a 10-line contract an asset must pass before it
is marked ready, inspection findings, monochrome silhouette test at 96/256px, and a
reconciliation table). Findings: identity holds across lock/comms/cut-in for all four
(Kontext from the menu ID lock); flags for the Azure r8 turnaround olive coat, Vivi's
missing lilac streaks (r8), gibberish shirt lettering (246033/247466), under-read builds
in Vivi comms/cut-in and the Solenne cut-in; all four existing group plates rejected as
non-canon. Missing for all pilots: helmet on/off, 6-frame action keys, colour callouts.
Docs only; no approved art overwritten; model licences for public release flagged for a
human.
<!-- note:end t-016 -->

## t-017 — Prove Space Princess earned-super and shield boundary behavior for every pilot.

<!-- note:begin t-017 -->
Reviewer kaizen after kind_robots#3590. Current seeded replay proves determinism, hostile bullets and modules, but only tracks a boolean for graze and does not assert a charged super's actual outcome. Add bounded deterministic actual-input proofs for below-full versus full charge, held B versus a fresh B edge, charge consumption/refill, bullet cancellation, pilot-specific effects, shield pickup caps, invulnerability and damage/life boundaries. Include eliminated-seat cases. Keep snapshot data immutable, use earned charge and existing consumer contracts, preserve private score exclusion, and fix only a reproduced scoped defect.

Scoped real-input four-pilot charge and super fixtures, non-stacking damage and invulnerability replay, plus a production core-vs-graze classification repair: protected direct projectile overlaps cannot award near-miss charge. Keep the private preview, no scores or release changes. Await complete Arcade and repository ratchet checks before safe merge.

Completed the earned-super and shield-boundary task with a real 4-pilot fixed-input combat replay, protected core-hit versus graze classification, charge threshold and fresh-B edge checks, actual projectile cancellation, earned refill checks, live shield-pickup cap and post-hit invulnerability, plus eliminated/benched-caster guards. kind_robots#3612 was safely merged at 02d3e4ff1cb0f7b3e145343b342b76e5e0b0510a after 30 of 30 check runs completed successfully on e94b3c23089fb97209c782f246def610d76699f4; no blocking reviews/threads or public release. The admin-only preview remains private and merge does not prove deployment.
<!-- note:end t-017 -->

## t-018 — Commit real-cabinet touch event replay for pointer capture, cancellation and resize boundaries.

<!-- note:begin t-018 -->
Reviewer kaizen after the partial touch improvement in kind_robots#3588. The independent isolated actual-handler/CSS probe passes; turn its pointerdown, move, up, cancel and lostcapture scenarios into durable browser regression evidence through the actual cabinet and seatInput consumer, including two fingers, independent seats, resize and compact versus generic dead-zone bounds. Reuse t-015's full cabinet/help integration fixture rather than a competing harness. Avoid a simultaneous overlapping t-015 claim; finish its original remaining help/input scope first when shared consumer work overlaps. Measure input-to-frame sampling, preserve other games' geometry and controls, and keep synthetic pointer evidence distinct from physical touch testing.
Done 2026-10-16: kind_robots#3767 merged green (all 18 checks, including the Rainbow Cabinet Browser Contract workflow that now runs both browser tests). Reuses t-015's fixture, extracted to utils/scripts/arcadeCabinetFixture.mjs. verifyRainbowTouch.browser.test.mjs dispatches touch pointer events on the actual cabinet's on-screen d-pads in a coarse-pointer Chromium page and reads back the cabinet's held state and the real Rainbow engine: pointerdown/move/up, pointercancel and lostpointercapture all release; a second finger cannot steal or release the owning finger's pad; a resize mid-hold (844x390 to 1024x768) is re-measured on the next move with nothing stuck; two fingers on two pads fly two pilots independently on a tablet; Space Princess's compact dead zone answers a near-centre touch that Hedgehog Crossing's generic dead zone ignores (other games' geometry unchanged). Touch-to-engine response measured in the page: 1 engine frame. Mutations (second finger may steal; generic dead zone for Space Princess) both fail. Synthetic pointers, not physical-touch evidence; real iPad/phone checks remain a device task.
<!-- note:end t-018 -->

## t-019 — Prove boss phase warnings through real player damage and rendered cue boundaries.

<!-- note:begin t-019 -->
Reviewer kaizen after kind_robots#3604, targeting LEARNING-REPORT's repeated quality/consumer-boundary pattern. The helper's exact269→270 regression and independent1100-scenario schedule sweep pass, but commit a deterministic replay that earns phase crossings through actual player shots and observes the real renderer's cue before each volley. Include HP100/50 boundaries during and outside charging, one/four seats, damage-after-step ordering, interrupted cues and safe boss defeat/pod cleanup without resetting ship resources. Verify at least36 fixed warning ticks and readable cue at phone/tablet/desktop; preserve original pacing. Distinguish isolated engine/render evidence from full shared-cabinet/device proof. Reuse existing Pinkwake fixtures and avoid overlapping t-007 implementation.
Done 2026-10-16: kind_robots#3764 merged green (all 19 checks). verifyRainbowBossCue plays 1/2/3/4-seat seeded crews with ordinary inputs (no demo immortality, no snapshot/HP edits; continues via #3760 where they fall) through Act I to B01 and earns both HP crossings with real shots. Every boss frame is drawn by the real render() into a recording canvas: the drawn cue matches the 36-frame warning window on every frame and precedes each volley by >=36 drawn frames; each of the 100/50 HP boundaries is crossed both mid-warning (interrupted cue restarts from scratch, next volley 72 frames out) and outside one; phase follows HP one step later (damage-after-step); defeat clears shots, craft and pod and keeps lives/shield/power/charge into Act II. Mutations (post-crossing warning 20 frames; drawn window 20 frames) both fail the test. Ring readability: warning rings now pulse 50-100% at 4px (were down to 10%); renders checked at 390/768/1440. Isolated engine/render evidence; shared-cabinet/device proof remains separate.
<!-- note:end t-019 -->

## t-020 — Pick the house Illustrious checkpoint with a front-end bake-off, then flood the art queue with it

<!-- note:begin t-020 -->
Silas, 2026-10-12 PT: "the art is falling behind. Start with the front end, then help us by submitting the art generation prompts. Don't worry about flooding the art generator ... we should decide on the checkpoint before anything substantial. Illustrious checkpoints have been great." Round 1 (art/ART-ROUND-1-CHECKPOINTS.yaml) renders nine front-end subjects (title key art, four pilot-select portraits, Lilt-7 comms bust, Petal Wing, Moonjelly Lantern, Pinkwake plate) on five installed Illustrious checkpoints with identical prompt, seed, sampler, steps and CFG. Silas picks the house lane from the sheet; later rounds render the WORLD-BIBLE asset tickets with it. Generated art is pre-approved internal work (AGENTS.md); public publication stays gated by t-014.
ROUND 1 DONE 2026-10-12 8:03 PM PT: 45/45 ArtJobs 37887-37931 rendered (ArtImage ids in the ledger). Agent read of the sheet: Arthemy Western v3 (C) is the only lane that kept all four pilots' canon colours, gave Solenne real muscle and very dark skin, drew Vivi curvy without sexualising her, and still produced a clean ship and Pinkwake plate. Nova Comic (D) drew the best machines (closest jellyfish starship) but turned Azure's coat pink and lightened Vivi. Illustrij (A) is semi-real, thin Solenne, baked shirt text on Vivi. NTR MIX (B) is flatter and put Solenne in full armour. Mol_Keun (E) dyed Maribel pink and Azure white. Recommendation to Silas: C as house lane. Builder fixes from this round: enemy/boss prompts drop the "mecha" tag and ban legs (C/E grew the Moonjelly dog legs), Lilt-7 forced androgynous (all five drew a cute girl), weighted canon colours for Maribel/Azure, Vivi bans shirt text.
STYLE CHANGE 2026-10-12 PT (Silas, after round 1): "we need a different style. It should be more like she ra princesses of power. Keep what was done for a specific theme...character ids in the menu. But for general flavor, we need more western cartoon, not faux realism." Round-1 Arthemy portraits became the menu character IDs (kind_robots#3619, merged a7edd55: Choose-your-princess roster on the private flight deck). Round 1B (art/ART-ROUND-1B-WESTERN-TOON.yaml, ArtJobs 37935-37979, 45/45 rendered) tested five western-toon lanes. Agent pick: Arthemy + toon tags (A) -- clean She-Ra-like flat look, best identity fidelity, and the same checkpoint as the menu IDs so cutscenes match the roster; B (Nova Comic) is the bolder runner-up; D (FurryToonMix) exaggerated bodies and is rejected. build_art_rounds.py now carries the 1B style plus fixes (Vivi hair lock, starship not battle cruiser, 4girls cap, larger key-art ships). Awaiting Silas's style pick before the 241-subject flood is submitted.
FLOOD SUBMITTED 2026-10-12 8:55 PM PT: Silas picked the recommended lane A ("Great, do it"). House lane = Arthemy Western Art v3.0 + round-1B western-toon tags, euler_ancestral 28 steps CFG 5. 241 private ArtJobs 37980-38220, 0 failed: R2 front end + cast 88 (37980-38067), R3 enemies 48 (38068-38115), R4 bosses 27 (38116-38142), R5 stage planes 38 (38143-38180), R6 cinema 20 (38181-38200), R7 pickups + FX 20 (38201-38220). Next: record ArtImage ids with --status, review contact sheets, reroll failures, then crop and key chosen frames into the game (t-011) and swap the admin hero SVG for the chosen title key art.
FLOOD RENDERED 2026-10-12 10:24 PM PT: 241/241 DONE (ArtImages 246122-246362, ids in each ledger). Agent review: KEEP enemies E01-E24 (all 48 clean, consistent toon sea-craft on dark grounds), Solenne's full set, supporting cast (Purl, Opal, Nemi, Navigator, Choir, Crown Voice), c04 pilot power-ups (Azure/Solenne/Vivi), Petal Wing + Prism Lance ships, title backdrops, boss heroes B02/B04-1/B05/B06/B07/B08, pickups u02/u06/u07/u08/u10, friendly/enemy/explosion FX sheets. REJECT: Maribel jacket recoloured yellow and Azure coat tan/black (suffix palette leak); Halo Fin and Comet Crown off-shape/off-colour; most stage planes (central starburst, floating pyramids); abstract cinema frames; c03 drew a Triforce (third-party IP, discard); FX supers/shield and u03/u04/u05 drew a Glimmer-like woman or stray characters/animals; group key art lost every identity (needs reference compositing, not txt2img). ROUND 8 (art/ART-ROUND-8-REROLLS.yaml) rerolls 95 of them in palette-free house-clean/house-scene lanes with colour/shape locks: ArtJobs 38272-38366, 0 failed.
ROUND 8 REVIEWED 2026-10-13 2:20 AM PT: 93/95 rendered (fx-super-halo and fx-super-comet still queued; their job ids are in the ledger, so --status fills them in later). KEEP: Maribel full set now pink (select, turnaround, cockpit, expressions, c04 power-up); Vivi lilac set and off-duty hoodie; B01 Pearl Seahorse heroes; B02/B06 rescues; c07 crowned jelly; pickups u01/u03/u05/u09; fx shield + Tidal Prism. STILL OFF: Azure coat navy/green not powder cyan; Vivi purple streaks never render; Halo Fin right disc+rings shape but bronze; Comet Crown lilac but spiky crystal; u04/u11/u12 wrong shapes; B09 crown machine abstract. RECOMMENDATION: txt2img has plateaued on multi-element scenes. Stage parallax planes (still centred islands/silhouettes) and cinema frames (sparse or off-brief) need a different method, not more rerolls: layout-guided generation for full-bleed horizontal planes, and Kontext composition from the approved cast/boss/enemy ArtImages for cutscenes and group key art. Colour misses (Azure, Halo Fin, Vivi streaks) are best fixed by Kontext recolour of the otherwise-good frames. Next: a follow-up task for that pass.
CLOSED 2026-10-14 PT: t-020's scope is complete. The checkpoint is picked (Arthemy Western v3 + western-toon tags, lane A, Silas 'Great, do it'), the 241-image flood plus 95 round-8 rerolls are rendered (336/336 DONE; ledgers art/ART-ROUND-1..8) and reviewed, and the front end ships the round-1 pilot IDs (kind_robots#3619) and the pearl-palace hero (kind_robots#3625). Final round-8 FX: fx-super-halo 246568 is a usable gold emblem; fx-super-comet 246570 drew a woman again (rejected). The remaining work (Kontext recolour/composition for off-colour frames, cutscenes and group art; layout-guided stage planes) continues in t-022 at Silas's request, 2026-10-14 PT.
<!-- note:end t-020 -->

## t-021 — Verify Nemi rescue and missed-beacon outcomes through actual eligible pilot inputs.

<!-- note:begin t-021 -->
Reviewer kaizen after kind_robots#3605, targeting recurring quality failures at the real consumer boundary. Extend the current Moonjelly engine replay to earn rescue through ordinary input and separately miss the beacon; verify branch dialogue, charge reward, expiry and active living-seat eligibility, including benched/dead seats. Never mutate snapshots or rely only on immortal demo mode. Reuse existing fixtures; coordinate with t-007 to avoid overlapping implementation and preserve authored timing/private ADMIN placement. t-015/t-018 cover cabinet inputs and t-019 boss warnings, so this narrow rescue-consumer scope does not duplicate them.
Done 2026-10-16: kind_robots#3765 merged (all required checks green; the non-required production image build was cancelled, test-only change). verifyRainbowNemiRescue flies ordinary-input crews (no demo immortality, no snapshot edits; continues via #3760) into Act II and reads Nemi and the A02.TURN line from what the real render() draws. Rescue: a living pilot in her lane brings her aboard (she leaves the field that frame, +750 score, +20 charge to every active seat, TURN says 'Nemi is aboard.'). Missed beacon: the pilot keeps clear, she is drawn across the whole field until expiry, no reward, TURN says 'We lost the Nemi beacon.' Fallen seat: pilot 2 dies in her lane at (140,157); the wreck stays put and she drifts over it unrescued; a later continue rewinds to the 1500 checkpoint and the restored pilot rescues her on replay. Benched seat: pilot 2 parked in her lane and benched with setPlayers(1) before she arrives; she drifts past, and on rejoin its charge is unchanged. Mutations (dead or benched ships may rescue) both fail the test. Isolated engine/render evidence; cabinet/device proof stays with t-015/t-018.
<!-- note:end t-021 -->

## t-023 — Recut Acts II-VIII to the playtest pacing: shorter, denser, obstacles, repeat fire, callouts

<!-- note:begin t-023 -->
Silas's first Act I playtest, 2026-10-17 PT: "First level to mini boss was too easy and too long ... It grew monotonous. We need obstacles, in stage elements to be maneuvered around, and enemies that take multiple hits. There must be more variation in combat." Act I was recut in kind_robots#3806 (eight dense sections, guardian at 1:25, boss at 3:30, clean solo 4.7 min; repeat fire, divers, coral spires, tougher craft, Lilt callouts every section) and every guardian beaten early now hands its Act on (#3805). This supersedes the WORLD-BIBLE 10-15 minute per-Act target for the remaining Acts: give each of Acts II-VIII the same treatment one Act per PR, about 4-6 minutes clean solo each, with at least one terrain or obstacle feature of its own, craft that keep firing, a section callout from Lilt for every section (solo lines included), and its per-Act verifier's pacing window tightened to match.
Done 2026-10-18 in kind_robots#3841 (merge 6a07ceb). One PR for all seven Acts, not one per Act: they share the recutTimeline helper (rainbowPacing.ts) and the cross-Act verifiers run the whole campaign. Each Act keeps its teaching sections, guardian, forks/rescues/reveals and two or three escalations; clean solo 4.5-6.1 min (II 4.53, III 4.93, IV 5.00, V 6.06, VI 5.81, VII 5.62, VIII 5.40), windows tightened 3-15 to 3.5-7. Reinforcement schools lift craft/min (V-VIII ~15 to ~50). Plain II/III/VIII craft repeat fire (slower than Act I's). Lilt callouts every section with solo replies (rainbowActBeats.ts); per-Act terrain in Act colours. Act VIII now has 13 captives (was 25). New verifyRainbowActBeats. Next: Silas playtests the recut Acts on main.
<!-- note:end t-023 -->

## t-024 — Second playtest: faster ship, tougher guardians, mortars, livelier craft

<!-- note:begin t-024 -->
Silas, 2026-10-19 PT, after playing the recut: "first level has much more dynamic play. ship should move faster. The miniboss died too quick, really quick. we need more variety in bullets: perhaps something that launches something else that explodes? Unless already planned, everything just sits and floats. it's easy and a little unexciting." Done in kind_robots#3864 (merge a781972): ship 2.6 -> 3.4; guardian base hull 24 -> 50 (125 solo) with guardian sections stretched 17-22 s (recutTimeline `stretch`; Act I's director now runs through it); mortars in every Act lob a ringed shell that bursts into three bomblets and again into fans; plain craft rush in, brake and slide toward a pilot's lane from range. Demo guardians now last 29-36 s (13-17 before); the ordinary first-clear pilot needs 39 continues for Acts I-II (24 before). New verifyRainbowPlaytestTwo. Next: Silas plays it.
<!-- note:end t-024 -->

## t-025 — A space-opera score: orchestral renditions of every cue, then ACE-Step takes

<!-- note:begin t-025 -->
Silas, 2026-10-19 PT: "we REALLY need better music. think space opera, and more than a midi 8 note on repeat." kind_robots#3865: 21 cues (nine flights, nine bosses, guardians, ending, failure) rendered offline by scripts/rainbow-score (numpy orchestra, hand-written Act themes, seamless loops, -18 LUFS) under public/rainbow-princess-audio/, played by the cabinet mixer as a MusicLoop's recorded rendition with the sequenced chiptune as fallback. The same 21 cues are queued as ACE-Step ArtJobs #40796-#40816 (rainbowRecordedScore.ts briefs); when they render, review each take and swap it in (source 'ace', its ArtJob id). Done when the orchestral score is on main; the ACE swap is its own follow-up.
Done 2026-10-19: kind_robots#3865 merged (654ec2d); all 21 orchestral cues play in the cabinet with the chiptune as fallback. ACE-Step takes #40796-#40816 still PENDING (render box idle); swapping them in is a follow-up once rendered.
<!-- note:end t-025 -->

## t-026 — Gen-2 route design: branching Luminous Ocean map, branch conditions, alternate stages

<!-- note:begin t-026 -->
Write projects/rainbow-bullet-hell-space-princess/ROUTE-MAP.md: the eight Acts become nodes on a branching route map (Star Fox 64 in spirit, original in content) with at least four alternate stages (Kelp Nebula Bypass, Sunken Lighthouse Ring, Coral Comet Trail, Mirror Shoal; backdrops in art/GEN2-ROUND-1.yaml), each branch opened by something done in the stage before (rescuing a captive, saving an escort, destroying a hidden generator, a no-continue clear), plus a per-stage medal goal and the routes that lead to each ending. Keep the three dialogue scenes per Act (ACT-STRUCTURE.md) and say which branch changes which scene.
DONE 2026-10-22: ROUTE-MAP.md and rainbowRoute.json (validate_route.py PASS: 14 nodes, four alternate detour stages each gated by a mechanic already in code, finale on all 16 routes, 13 medals, Palace Hangar fittings bounded so fairness never moves, a three-slot save measured at 5.9 KB).
<!-- note:end t-026 -->

## t-027 — Gen-2 memory: save slots, route map screen, medals and the persistent Palace Hangar

<!-- note:begin t-027 -->
2026-11-20T11:21:42Z connector recovery: prior claim 2026-11-20T05:40:00Z expired after 341 minutes, no open Rainbow PR or branch; implementing Palace Hangar on a scoped worker branch.

Reuse the generalized overworld/save-slot module (save-the-plumber/t-011, kr-arcade/t-160). Three slots; route map with cleared nodes, medals and discovered branches; a hangar where medals buy permanent, bounded upgrades (never pay-to-win against the fairness rules); pilot comms that recognise progress (first visit vs return, a branch found, a friend rescued last run). Migrate the current save.

Stale claim recovery: no matching open Rainbow PR or implementation branch; save slots, route map and Palace Hangar must be verified from current main before further implementation.

Three independent versioned checkpoint slots are implemented on a scoped Kind Robots branch with a Seas slot picker and test; slot one preserves the legacy save key. This is a partial t-027 PR, not completion of the route map or Palace Hangar.

Added saved-fork route intelligence to the Seas cards and a regression test. This is a partial route-map improvement, not the playable route navigation or Palace Hangar completion.

Implemented a working per-save-slot Palace Hangar. Best earned Act medals fund bounded shield, charge and life bonuses, persisted in Arcade preferences and equipped by all four pilots in the live cabinet. Tests added. Code branch worker/rainbow-bullet-hell-space-princess-t-027-hangar-x7p5. This is partial t-027: route-map navigation and stage replay remain open.

Scoped Palace Hangar PR silasfelinus/kind_robots#5423 merged after twelve completed green workflows at d1c300d. Hangar slot upgrades, medal spending and four-seat bonuses are shipped to main, but playable Luminous Ocean route-node navigation and authored stage replay remain unfinished.

Scoped keyboard-accessible route node inspection with stage descriptions and earned route intel committed as 7d7663b. This is partial t-027; actual replay selection and full route navigation remain outstanding.

2026-11-20 reviewer reconciliation: status was review with no open PR (claim from 16:39Z
expired). Already on kind_robots main: three save slots (#5384), Seas map branch intel
(#5393), working Palace Hangar upgrades (#5423), keyboard-inspectable route nodes
(#5441). Still missing on main: pilot comms that recognise progress (first visit vs
return, branch found, friend rescued last run). Also check the medal economy end to end
before closing. Also still open, per the notes above: playable route-node navigation and
authored stage replay selection.

Implemented a separate unlocked-Act replay launch path from the Seas map. It validates completion for the active save slot, reconstructs stage-start state without mutating the saved campaign, supports 1–4 pilots, stops at the selected Act clear, and awards the improved replay medal only to the Hangar. Scoped regression test added. t-027 remains partial until route-map branch navigation and other acceptance are verified.

Scope-limited Act replay PR silasfelinus/kind_robots#5443 merged as 4712fe42e5465dbe28d8cc25d482a917b45e7c56 after all 12 latest-head workflow runs completed successfully, including TypeScript after declaring the replayClear return property. Unlock-validated Act replay, 1-4 local seats, save isolation and earned Hangar medals are on main. t-027 remains incomplete until route-node branch navigation and full progression acceptance are verified.

Added slot-specific Lilt-7 and named-pilot comms on the Seas map. First launch, return flight, discovered branching routes, rescues and Motherland allegiance now have distinct deterministic dialogue, backed by the active save-slot flags rather than account-wide mastery. Existing Rainbow replay and logbook regression tests cover the new selection rules. This is a partial t-027 slice; full map-node navigation and progression acceptance remain.

Scope-limited Kind Robots PR #5450 merged at 0f3a842665d2570ff547f1272d43a74dd2fbabf1 after nine completed passing checks. Per-slot pilot/Lilt comms now ship, but full route-node navigation and progression acceptance remain unfinished. Return to ready.

Added route discovery guardrails, separate nursery and armory guardian outcome intel, and regression cases on scoped app branch. Partial t-027; full route navigation and progression acceptance remain.

Stale review claim from 2026-11-21T00:34Z has no open matching Rainbow PR or branch; existing partial map/Hangar work is on main. Releasing ownership for a scoped four-detour route discovery persistence and Seas-map pass.

Created four durable per-save-slot alternate-route discovery bits on entry into X1-X4 flight, restoring exact checkpoint proof on resume and continue and rejecting forged route-history masks in save decoder. Added accessible inspectable Seas map detour nodes and route-logbook regression. App branch worker/rainbow-bullet-hell-space-princess-t-027-detour-map-w3q8; partial t-027 pending CI and fuller route replay acceptance.

2026-11-22 PT: The prior review handoff is over 90 minutes old and no open Rainbow PR remains after #5607 merged. Preserve merged map/Hangar work and reopen t-027 for playable alternate-route navigation, without touching other review lanes.

2026-11-22 PT: Scoped four-route Seas map navigation on worker/rainbow-bullet-hell-space-princess-t-027-detour-approach-v8c4. Charted detours launch isolated replay of their authored origin Acts without overwriting campaign slots; 1-4-seat and locked-route regression added. Partial t-027 until full campaign progression and route QA are verified.

2026-11-24 PT: route-map art (gen2/route-map, 251317) and Hangar art (gen2/hangar,
251298) ship on the play page (kind_robots#5685, merged 5923d73d); ROUTE-MAP section 5
scene variants and section 6 stingers ship (kind_robots#5687, merged 12868a79): nine
route beats replace one named line each, liltMemoryRecovered/crownEcho derive from saved
fields, THE ROUTE credits and stinger fanfare. Slot-memory 'X found' hints were not
built (past-run discovery, superseded by the canonical detour order). With the three
slots, Hangar, medals and four-route Seas navigation already merged, t-027's scope
ships.
<!-- note:end t-027 -->

## t-028 — Gen-2 alternate stages: four branch stages with their own guardians

<!-- note:begin t-028 -->
One stage per PR, authored to the existing Act pacing and fairness rules, each with a guardian.

Stale claim recovery: no matching open Rainbow PR or implementation branch; preserve authored alternate stage scope and resume from actual main-branch implementation.

First alternate Act Lantern Nursery authored encounter-score foundation (20 waves, five sections, distinct lantern guardian, deterministic spawn contracts). Not yet wired into playable campaign; route/checkpoint integration and three other alternate Acts remain.

2026-11-19 PT: Lantern Nursery low-fork integration and regression checks are on worker/rainbow-bullet-hell-space-princess-t-028-lantern-runtime-m8q5. This is partial t-028; a distinct alternate guardian and standalone Gen-2 route still remain.

2026-11-20 PT: Matriarch runtime, distinct multi-pattern guardian, checkpoint-safe defeat, and earned-route four-seat regression implemented in worker/rainbow-bullet-hell-space-princess-t-028-matriarch-j7k4; partial t-028, not a full alternate Act.

Added dedicated in-flight Lantern Matriarch encounter with alternating ring/fan telegraphs, guardian outcome independent of Act III, checkpoint/continue recovery, and four-seat engine and legacy-save regression tests. Partial t-028, standalone Gen-2 Act/map/art and three other alternatives remain.

PR silasfelinus/kind_robots#5448 merged as a5b11d71a199a8e7ee179af22433f908a318cb90 after 12 completed successful workflows. Armory Siren branch guardian, telegraphs, checkpoint persistence and four-seat tests shipped. Partial t-028: four independent alternate Acts, painted guardian art and complete branch QA remain; return to ready.

2026-11-21T00:35:26Z PT-context sprint: Act VI low shield-cache now has an independent Pearl Warden encounter, rotating safe-gapped hoop and aimed crescents, per-checkpoint defeated/escaped state with legacy-save safety, and 1/4-seat regression. Code commit 2e8ef21e on worker/rainbow-bullet-hell-space-princess-t-028-reef-cache-m7q4. This is a partial t-028 milestone, not completion of four standalone alternate Acts or production guardian art.

Green PR kind_robots#5476 merged as f87d49b on 2026-11-20 PT. Authored X3 Sunken Lighthouse schedule, lamps and guardian volley exist on main, but are not flown in the cabinet; the alternate-stage transition, checkpoints, guardian adapter, art delivery and remaining detours are open. No matching open t-028 PR or branch; return to ready for next implementation.

Scoped X3 Drowned Bellkeeper guardian kind, alternating authored projectile geometry, 36-frame charge, one/four-pilot combat and escape tests, calm-motion profile, and temporary art fallback committed as kind_robots 4b2e7b78. This is partial t-028: X3 detour launch, lamp interactions, persistence, navigation, finished guardian art and other alternate Acts remain.

2026-11-20 PT: Previous X4 PR #5487 merged; GitHub now reports no open Rainbow PRs or t-028 branches. The earlier review claim is stale, and four standalone alternate flight adapters remain unfinished. Reopen for concrete integration.

2026-11-20 PT: X4 Mirror Shoal cabin flight adapter, high-lane co-op vote, guardian fight, checkpoints/resume, reflected waterline and regression assertions committed to kind_robots 27725758; verify on PR before merge. This is partial t-028; other alternate routes and painted final art remain.

2026-11-21 PT reviewer reconciliation: X4 Mirror Shoal flight adapter merged as
kind_robots#5495 (b7a1821c); no open t-028 PR or branch remains and the stale review
claim (06:53Z) is released. Partial t-028: remaining alternate Acts and painted guardian
art are still open; return to ready for the next slice.

Scoped X3 Sunken Lighthouse flight adapter committed to Kind Robots worker branch with earned relay/high-lane entry, 30 authored waves, six timed lane lamps, live Drowned Bellkeeper combat, three dialogue scenes, all four seats, checkpoint-safe save validation and restore, and new flight regression tests. Partial t-028: X1/X2 and final guardian art remain outstanding.

2026-11-21 PT: X3 Sunken Lighthouse standalone flight PR silasfelinus/kind_robots#5535 merged as afdfef1023e9bc41eb00625c4b7e25d6e49a56e1 after all 11 latest-head GitHub workflow runs completed successfully, including TypeScript, full four-shard Contract Tests, Lighthouse score, browser cabinet, and viewport. Earned X3 entry, six lamps, 30 waves, Drowned Bellkeeper, three comms scenes, all local 1-4 seats, checkpoint persistence and regression are integrated on main. Partial t-028; two standalone alternate Acts X1/X2, finished guardian art, and full route replay/QA remain. Ready for next implementation slice.

Partial X1 Lantern Nursery standalone flight model on kind_robots commit 28d4c564: six contiguous sections, authored 20-wave score, earned rescued-Nemi/cleared-trench low-lane local co-op vote, exact checkpoint proof, and dedicated CI contract. The model is not yet wired to cabinet flight/render/save; X2 and art still remain.

2026-11-22 PT: stale review claim dated 03:52Z (over eight hours old) with no open Rainbow implementation PR or matching worker branch in kind_robots. Preserved existing X1 flight-model commit and all prior X2-X4 integration; reopening only for the unblocked X1 art/gameplay follow-up.

X1 missing Gen-2 gameplay art is now authored in private auto-submit Krea 2 ledger GEN2-KELP-NEBULA-X1.yaml: idle/sweep/hurt Kelp Warden, Coral Choir rescue pod, and lashing frond hazard. The five subjects are queued for pipeline submission only after a green merge; none has a new ArtJob or reviewed ArtImage yet. Existing four-stage backdrops remain reused. This is partial t-028, which still needs rendered art review, export, runtime integration and route playtests.

Partial scope: PR #7833 merged with five Krea 2 X1 production-art requests; reopen for remaining X1 gameplay, image review, actual ArtJob intake and four-route acceptance.

Scoped X1 Kelp Nebula canonical gameplay implementation is committed on worker/rainbow-bullet-hell-space-princess-t028-kelp-choir-20261122: Kelp Warden telegraphed four-tooth attack, five timed Choir rescue pods, checkpoint and save migration validation, one-to-four-seat regression updates and X1 HUD. Art is still pending and t-028 will remain partial after merge. Await CI and verification.

Previous X1 partial-work review claimed 2026-11-22T12:32Z has no open Rainbow implementation PR or matching branch at 22:09Z; X1 is on main. Releasing stale review ownership for X2 checkpoint-rescue integrity and live four-seat replay validation.

Implemented X2 temporal cadet-mask and guardian-outcome validation in kind_robots worker branch worker/rainbow-bullet-hell-space-princess-t-028-comet-saveguard-f6k2, plus exhaustive bitmask / section boundaries and corrupt-save replay assertions. Partial t-028; guardian art and independent campaign QA remain.

2026-11-22 PT: Prior X2 checkpoint-review claim from 22:11Z is past the documented 90-minute TTL; no active t-028 PR or branch remains. Its X2 save protection is merged on main (#5601). Reopen for independent alternate-stage QA and gameplay implementation.

2026-11-22 PT: Independent four-detour completion progress on worker/rainbow-bullet-hell-space-princess-t-028-detour-clears-h5n8. X1-X4 route clears now record only after genuine alternate Act exits; checkpoints and decoder persist and validate separate discovery/completion bits. Exhaustive corruption and one-to-four-seat X2 exit tests added. Partial t-028; production art and full alternate guardian replay/visual QA remain.

2026-11-23 PT: kind_robots#5685 merged as 5923d73d after all 23 checks completed green.
X1-X4 now fly their own reviewed painted skies and keyed far/mid/near bands
(GEN2-ROUND-2 Krea 2; X2/X4 mids refused because moving asteroids/fish read as enemies),
X2 scrap is the coral asteroid (278622), kelp fronds (278928) mark the Kelp Warden comb
lanes, and the Armory Siren flies its own painting (ARMORY-SIREN-2026-11-23, 279830).
With #5614 clears, the guardians from t-059 and the per-detour flight/replay verifiers
now gated in CI by rainbow-verifier-suite, all four branch stages and their guardians
ship. Verdicts recorded in the ledgers.
<!-- note:end t-028 -->

## t-029 — Gen-2 art round 1: route map, Palace Hangar and four alternate-stage backdrops

<!-- note:begin t-029 -->
art/GEN2-ROUND-1.yaml (6 subjects x Z-Image/Krea 2 = 12 cells) submitted 2026-10-22 via scripts/sweep_art_ledgers.py. Review keepers in the ledger, then hand to t-027/t-028.
2026-10-22: rendering (6 of 12 DONE at last check). Next: review keepers in the ledger and hand them to t-027/t-028.
DONE 2026-10-22: all 12 rendered and reviewed in the ledger; the six Krea 2 renders keep (route map, Palace Hangar, Kelp Nebula Bypass, Sunken Lighthouse Ring, Coral Comet Trail, Mirror Shoal). Hand to t-027/t-028.
<!-- note:end t-029 -->

## t-031 — Resume at the last checkpoint: the cabinet keeps every checkpoint, not just Act starts

<!-- note:begin t-031 -->
Silas, 2026-10-23 PT (verbatim): "we should remember runs between games, returning should put us at the last checkpoint. If that isn't already implemented." Today the save is written only at an Act's frame 0 (writeSave in rainbowPrincessPreview.ts) and readRainbowSave rejects any checkpoint with frame > 0, so leaving mid-Act loses everything since the Act began. Write the save at every section/boss checkpoint (Act I too), accept and validate those checkpoints on load, and resume through the same rewind the CONTINUE? path uses. The continue menu names the Act and section. Narrow slice of t-027's memory work; t-027 keeps save slots and the route map.
DONE 2026-10-23 PT: kind_robots#4092 merged (da34189). The cabinet save is written at every section and boss checkpoint (Act I included) and validated against the engine's own checkpoint list on load (isRainbowCheckpoint). Continuing resumes the Act clock on that checkpoint frame through the CONTINUE? rewind, and the flight log names the section. All 34 Rainbow verifiers and 18 CI checks are green.
<!-- note:end t-031 -->

## t-032 — Animated projectiles: every enemy, guardian and boss shot family gets its own moving shape

<!-- note:begin t-032 -->
Silas, 2026-10-23 PT (verbatim): "We should have animations fo4 all projectiles, not these identical circles." Most hostile fire falls through to one dark circle with a yellow rim. Tag each shot with a look from the craft or boss that fired it (and inherit it through bursts), then draw code-drawn animated shapes per look: spinning stars, pulsing jelly bells, ink drops, bubbles, fin blades, prism shards, eclipse sparks. Keep the dark readability halo, the hitbox and every fairness rule unchanged; calm motion slows the animation. Player shots animate too (shimmer, trails).
DONE 2026-10-23 PT: kind_robots#4093 merged (b96288d). Every hostile shot carries a look from the craft, guardian or boss that fired it, drawn by rainbowShotLooks.ts as one of 20 animated code-drawn shapes. Hitboxes and fairness are unchanged; the 8 px halo softened. Pilot shots leave wakes. verifyRainbowEffects checks every plain pellet has a look, 14+ looks across the campaign, and that each look animates.
<!-- note:end t-032 -->

## t-033 — Enemy dynamism: plain craft move and attack in distinct sea-life patterns

<!-- note:begin t-033 -->
Silas, 2026-10-23 PT (verbatim): "improve the dyamism: enemies should move and attack in different ways." The plain craft of Acts I-III (picket, spiral, anchor, urchin, lantern, relay, skimmer, coral, pistol, angler, skate) share one leftward drift plus a sine and an aimed pellet. Give each its own movement (hover-and-strafe, true corkscrew loops, wall bounces, jelly pulse-swims, ceiling/floor skims, manta swoops) and its own attack (bursts, rotating fans, radial spikes, dropped bombs, lobbed shots), deterministic and telegraphed, within the existing fairness and pacing tests.
DONE 2026-10-23 PT: kind_robots#4094 merged (a52ee28). Each Act I-III plain craft swims and fires its own WORLD-BIBLE way: picket sidestep lead, spiral loop-the-loop with turning spokes, anchor mines, urchin wall-roll with an 8-spine fan, lantern pulse-swim with a gapped ring, relay link, skimmer rails with bead columns, coral floor lobs, skate manta swoop. Courier pods past the left edge no longer take hits. Two scripted test bots tightened (assertions unchanged); verifyRainbowCraftVariety is new. Side fix: kind_robots#4095 repaired main's broken production image build (ecotone-board inline handler from #4087).
<!-- note:end t-033 -->

## t-035 — Doodle direction bake-off: C.A.T.S. emblem, cat-ship key art, co-pilots, DOG commanders, restyled Maribel

<!-- note:begin t-035 -->
DOODLE-DIRECTION.md step 1. Render the 1980s neon airbrush school-folder look on two or more engines before restyling anything: C.A.T.S. emblem, title key art of the four cat ships, the four cat co-pilots (Biscuit, Comet, Butter, Glitch), King Rufus and Corporal Chihuahua, and Maribel restyled by Kontext from identity lock 246030. Pick the engine that holds the look and record it. Never name the artist or brand in a prompt.
PARKED 2026-10-23 PT while rendering: art/DOODLE-BAKEOFF-1.yaml jobs 44654-44665 (zimage + krea2) and art/DOODLE-BAKEOFF-KONTEXT-1.yaml jobs 44666-44673 (the four princesses restyled from identity locks with co-pilots). Next: --status both ledgers, review keepers against DOODLE-DIRECTION.md and CAST-QA identity, pick the engine, record it here, send Silas the contact sheet.
2026-10-23 PT: Silas withdrew the DOGS. Skip dd-king-rufus, dd-corporal-chihuahua and dd-collared-seahorse (withdrawn in the ledger); review only the emblem, key art, co- pilots and princess restyles.
2026-11-02 PT. FOR SILAS: the doodle-direction bake-off is reviewed, and the contact sheet was sent to you in session (keepers only; private art is not committed). Engine pick: Krea 2 for txt2img. It holds the 1980s neon airbrush school-folder look; Z-Image reads as flat modern kawaii. Kontext stays the engine for the princess restyles. Keepers: C.A.T.S. emblem 252575, cat co-pilots 252577, and restyles of Maribel 252851, Azure 252853 and Vivi 252856 (alternate 252857). Key art 252576 is shown as engine evidence only: it draws five cat ships, not four. Both Solenne restyles fail CAST-QA (lightened skin, navy hair) and are not shown. DECIDE: does this look go ahead for the t-036 full restyle? Reply yes, or say what to change. If yes, t-036 applies these fixes: name Solenne's deep-brown skin and black hair; give Azure jet-black hair and a new background; describe the co-pilots by color, including Biscuit's notched ear and a huge Butter; build exactly four cat ships by editing the existing ship sprites. Unblocks t-036 and t-038. Recommendation: approve. The emblem and co-pilots are on-direction.
2026-11-02 PT: Silas decided in session: "I don't know what the doodle issue is, but if it involves making new art in a doodle style as an optional shift, do it." The doodle look goes ahead as an OPTIONAL alternate style, and the shipped art stays the default. Engine pick recorded above: Krea 2 for new art, Kontext for restyles. t-036 is unblocked.
<!-- note:end t-035 -->

## t-036 — Doodle restyle of the cast, ships, co-pilot cut-ins and the nine DOG commanders

<!-- note:begin t-036 -->
DOODLE-DIRECTION.md step 2. Kontext-restyle every approved princess asset from its identity lock (CAST-QA identity still binding); cat ships keeping each silhouette and P1-P4 glyph; super cut-ins with each pilot's co-pilot; the nine DOG commanders per the table. Uses the engine t-035 picks.
2026-10-23 PT: no DOG commanders (Silas withdrew the DOGS). Restyle the space-animal fleet as the villains instead, plus Princess Kitty Power cut-ins with each co-pilot (PLOT-MOTHERLAND.md).
2026-11-02 PT: Doodle set queued as an optional alternate look: art/DOODLE-SET-1.yaml (93 cells, auto_submit, all pass the live contract). It restyles every shipped asset into public/rainbow-princess-art/doodle/<same path>. The 12 princess assets come from their CAST-MANIFEST identity-lock originals, with the bake-off fixes in the prompts. Ships, 27 boss phases, 33 enemies and 3 pickups come from the shipped sprites on a #00ff00 matte (key it out to alpha on export). The 8 stage cards, the hero plate and the 4 crew comms portraits are included too. The key art is a fresh Krea 2 render with exactly four cat ships. Not included: the 8 wide stage foreground strips (8:1, beyond Kontext's frame size); redraw those separately if the doodle stages need them. Next: curate against DOODLE-DIRECTION.md and CAST-QA, export keepers with alpha, then t-037 wires a style toggle (default stays the current art).
2026-11-05 PT: reviewed all 93 set-1 cells (art/DOODLE-SET-1-REVIEW.yaml). kind_robots#4764 ships 98 Fever Dream pictures (57 doodle keepers, the rest as a neon sticker treatment of the classic sprite) and a Classic / Fever Dream switch (t-037's toggle; Classic stays default). Held: Solenne portrait and comms (CAST-QA skin and hair). art/DOODLE-SET-2.yaml queues 35 re-renders with source_margin; review them, flip the matching review entries to keep, re-run scripts/export_rainbow_doodle_art.py.
Merged kind_robots#4764 (1c6b163): the Classic / Fever Dream switch is on main. The DOODLE-SET-2 re-review continues as t-043.
Silas decided 2026-11-05 PT (verbatim): "Yes, fever dream should be default." kind_robots#4765 makes Fever Dream the default look; a visitor who picks Classic keeps it.
<!-- note:end t-036 -->

## t-037 — C.A.T.S. vs DOGS in game: names, DOG commanders on boss bars and cut-ins, bones and hearts, doodle UI

<!-- note:begin t-037 -->
DOODLE-DIRECTION.md step 3. Faction names in comms and HUD; each boss bar names its DOG commander; boss fire drawn as bones, tennis balls and storm clouds, player fire as hearts and stars (decoration only, hitboxes unchanged); bubble-letter titles and sticker pickups. Code-drawn first; swap in t-036 art as it lands.
DONE 2026-10-23 PT (code-drawn layer): kind_robots#4097 merged. The C.A.T.S. squadron and cat co-pilots appear on the Pilots tab. A DOG commander per boss is named on the boss bar, barks on arrival, and is sent home with BAD DOG! on defeat. Boss fire is bones, balls and clouds; pilot fire is hearts and stars. verifyRainbowDogs covers all nine across the demo campaign. Painted commander art and the doodle UI skin follow from t-036 once t-035 picks the engine.
<!-- note:end t-037 -->

## t-038 — Recut the thrash-metal opening from the doodle art

<!-- note:begin t-038 -->
Silas chose to hold the old-style opening clips (44645-44653) and recut from new-style stills. New WAN clip ledger from t-035/t-036 keepers, then scripts/export_rainbow_opening.py with the new SHOTS; the thrash track (44644) stays.

Stale claim recovery: no matching open Rainbow PR or implementation branch; opening recut remains an actual undelivered requirement, not proof of active work.

2026-11-20 PT: Prepared eight approved DOODLE-SET-1 C.A.T.S. first/last-frame WAN MP4 opening clip requests, retaining ACE-Step ArtJob 44644. Conductor branch 7cafec3d stages auto-submit after green PR merge; no new ArtJob IDs yet, no rendered clips reviewed, no assembled intro. Partial t-038.

2026-11-21 PT reviewer: Conductor PR #7730 merged (squash a48a792e) with all 24 latest-head checks green. It lands the eight-shot OPENING-CLIPS-2-DOODLE request ledger and the MP4/WebM-capable exporter (historical 9-shot ledger kept via --ledger). Still partial: returned to ready, claim released. Remaining: confirm the auto-submitted ArtJob IDs, inspect the rendered WAN MP4s for identity locks, then export the 15-second cut and wire it into the kind_robots cabinet.

2026-11-22 PT reviewer: PR #7823 (squash b773e817) merged by another session with the
report-newline fix but still publishing staged /tmp media via Path.replace (EXDEV cross-
device) and misnaming --out WebM/poster. Follow-up conductor PR on claude/focused-
johnson-yxvq84 adds publish_artifact() (copy to hidden sibling + same-dir os.replace)
and main()-level tests simulating a cross-device /tmp; retry_context items resolved.
Still partial: confirm auto-submitted WAN ArtJob IDs, inspect rendered clips, export the
15s cut and wire it into the kind_robots cabinet.

Partial opening-recut reliability slice: exporter now resolves original completed ACE-Step soundtrack by pinned ArtJob #44644 rather than only the most recent 200 queue jobs. Added five regression tests for DONE, pending, malformed, missing ArtImage and HTTP denial. Full opening visual review/render and kind_robots integration remain outstanding.

Partial scope: PR #7834 merged with pinned soundtrack ArtJob #44644 resolver and regression tests; reopen for completed WAN clip visual review, final render and Kind Robots cabinet integration.

2026-11-22 PT worker: all eight WAN clips were DONE (ArtImages 277936-278013). Preview
export failed verification (14.68s vs 15s: the ACE-Step track is shorter than the cut
after silence trim and -shortest truncated the picture); fixed with apad plus a real-
ffmpeg regression test. Contact-sheet review: identities hold on all cast shots and the
title slam lands, but intro-dolphin-armada animated the dolphin sprite on flat chroma
green; re-pinned to approved stage-2 card 262204 and cleared its job so auto-submit
renders a new clip (the shot uses the still until then). Next: once the new intro-
dolphin-armada clip is DONE, run export_rainbow_opening.py --kind-robots ../kind_robots,
inspect, and open the kind_robots PR wiring opening mp4/webm and poster into the
cabinet.

Partial opening integration resilience: video decode/playback failure now offers a focused retry instead of silently marking the opening watched. WAN dolphin clip and final export still outstanding; keep task incomplete.

2026-11-22 PT recovery: the 19:33Z review handoff is past its TTL with no open t-038 PR or branch. The blocking intro-dolphin-armada re-render is DONE (ArtImage 279030), so the remaining step is the export and cabinet wiring (RAINBOW_OPENING is still null). Returned to ready; no prior work discarded.

2026-11-22 PT: Ran export_rainbow_opening.py: 15.0 s, 8/8 shots animated from the DONE
doodle clips (dolphin 279030) to track 252834; no rejected or still-fallback shots.
Contact sheet and Chromium playback (15.03 s, 1280x720) checked. RAINBOW_OPENING wired
in kind_robots#5618, which also fixes verifyRainbowOpening's double-escaped gamepad
regex (failed on main).

2026-11-22 PT done: kind_robots#5618 merged as e816817b after all checks completed green
(TypeScript, all four contract shards, Rainbow cabinet Chromium jobs, cabinet-viewport).
The opening now plays in the cabinet.
<!-- note:end t-038 -->

## t-039 — Remove the DOGS; Princess Kitty Power cut-ins; boss fire back to each creature's own look

<!-- note:begin t-039 -->
Silas withdrew the DOGS (PLOT-MOTHERLAND.md). Remove rainbowDogs.ts commanders, barks, BAD DOG send-off and bone/ball/cloud boss fire (kind_robots#4097); keep C.A.T.S., co-pilots, heart and star pilot shots. Each super cut-in becomes a Princess Kitty Power with the pilot's co-pilot.
DONE 2026-10-23 PT: kind_robots#4099 merged. Removed the DOGS layer: commanders, barks, BAD DOG, and bone/ball/cloud boss fire; bosses fire their creatures' own looks again. Kept C.A.T.S., co-pilots, and heart and star shots. Every super cut-in is a Princess Kitty Power with the co-pilot's face. verifyRainbowCats replaces verifyRainbowDogs.
<!-- note:end t-039 -->

## t-040 — The Motherland turn, first slice: Act V memorial reveal and the flown allegiance choice

<!-- note:begin t-040 -->
PLOT-MOTHERLAND.md. At Act V's memorial the crew realizes the Motherland is the colonizer; high lane TURN ON THE EMPIRE (allegiance rebel), low lane STAY THE COURSE (loyal), majority of living pilots, tie stays the course. Flag in checkpoints and saves; one allegiance line in each later Act's OPEN. Later slices: rebel-road waves, two finale targets, allegiance endings.
DONE 2026-10-23 PT (first slice): kind_robots#4100 merged. The Act V memorial plays the three-line Motherland reveal, then the flown choice: high is TURN ON THE EMPIRE (rebel), low is STAY THE COURSE (loyal); majority of living pilots, a tie stays the course. Allegiance is kept in checkpoints and saves and restored on continue. The lead's A06-A08 OPEN lines answer it. The memorial now runs 510-1050 frames, and the demo flies both roads. verifyRainbowMotherland is new. Next slices in PLOT-MOTHERLAND.md: rebel-road waves, two finale targets, allegiance endings; t-041 reframes Acts I-V.
<!-- note:end t-040 -->

## t-041 — Reframe Acts I-V dialogue toward the Motherland reveal (develop as we go with Silas)

<!-- note:begin t-041 -->
Early lines speak the Motherland's "pacification" story; Acts III-V plant the evidence (Motherland hardware, colony ships behind the convoy, the creatures' carers at the depot). Keep three scenes per Act and Lilt's arc.
Merged kind_robots#4105 (f1a1659): Acts I-V speak the Motherland pacification story and seed the evidence chain (beacons, lullaby, command codes and collar, colony ships, caretakers); verifyRainbowEvidence pins it.
<!-- note:end t-041 -->

## t-043 — Fever Dream look: review the doodle re-renders (DOODLE-SET-2) and ship the keepers

<!-- note:begin t-043 -->
Follow-up to t-036 (kind_robots#4764). art/DOODLE-SET-2.yaml (35 cells, auto_submit) re-renders what art/DOODLE-SET-1-REVIEW.yaml held: Solenne's portrait and comms (skin and hair lock), three ships (colour and silhouette lock), 12 boss phases (B02/B04/B07/B09), 17 enemies and guardians, and 2 pickups, each sprite on a source_margin green border so it stays whole. When the cells are DONE: contact-sheet them (portraits beside their CAST-MANIFEST identity locks; sprites keyed on dark, with the frame-edge check), flip the passing entries in DOODLE-SET-1-REVIEW.yaml to keep (a boss only with all three phases), re-run scripts/export_rainbow_doodle_art.py --kind-robots ../kind_robots, run utils/scripts/verifyRainbowFeverDream.test.ts, and PR the files. Once all four ships pass, also flip ships/petal-wing to keep.

Added export fail-closed checks for incomplete curated boss phase groups and missing finished key art. Art inspection and integration remain outstanding; this is a partial safety increment.

Reviewer 2026-11-20: export guard merged via PR #7694 (dry run passes on current ledgers; fails closed with exit 1 when a kept boss lacks finished phases). Back to ready, claim released: the contact-sheet review, keeper flips and the kind_robots export PR are still to do. All 12 DOODLE-SET-2 boss phases (b02/b04/b07/b09) already have finished renders. Kaizen t-046.

2026-11-20 PT: Added private DOODLE-SET-2 comparison sheets, ArtJob/ArtImage provenance and four tests. Visual acceptance and actual export still open; scoped PR awaiting CI.

Reviewer 2026-11-20: review-sheet builder merged via PR #7699
(scripts/review_rainbow_doodle_art.py; verdicts stay PENDING_VISUAL_INSPECTION). Back to
ready, claim released: generate sheets, do the visual pass, flip keepers in DOODLE-
SET-1-REVIEW.yaml, export to kind_robots and PR.

2026-11-22 PT visual pass of all 35 DOODLE-SET-2 renders (sheets from scripts/review_rainbow_doodle_art.py). Kept six whole enemy re-renders (brood, mirror, salvager, squid, lantern, guardian-bulwark) in DOODLE-SET-1-REVIEW.yaml (conductor#7841) and exported them to kind_robots (kind_robots#5584, Fever Dream verify test green). Held 29: Solenne portrait/comms fail CAST-QA 2/5; all ships fail colour lock or crop, so petal-wing stays fever; no boss has three whole phases; ten enemies/guardians and both pickups still cropped at the right edge. The source_margin green border did not stop Kontext cropping, so a further re-render round needs a different approach (txt2img lane or wider pad).
<!-- note:end t-043 -->

## t-045 — Rainbow Bullet Hell Space Princess achievement upgrade: 12 or more live achievements

<!-- note:begin t-045 -->
Silas 2026-11-11 PT, in session: "Our games should all have a base standard of quality ... We want our main games to have 12 plus achievements." Standard: docs/agents/main-game-standard.md; CONTROL.md global overview.

Live today: 0 Achievement record(s) with this game's triggerCode prefix (checked against /api/achievements 2026-11-11). Target 12+ (usually 12-30; tie some to endings but don't go overboard). Mix story, skill, discovery and completion. Create the live records through the existing achievements API (label, message, icon, karma, triggerCode prefixed with the game slug), award them from the game store, show them with components/achievements/game-achievement-strip.vue, and verify one award live after deploy.

Achievement upgrade merged in kind_robots#5042 (d870dd3), all checks green: 17 live arcade-prefixed achievements (7 mastery goals, 3 endings, 7 deeds) via a drainFeats() queue and mastery backfill at cabinet start; fixed Every Ending never being earnable. Catalog run 43140875677 succeeded. Not added: an all-pilots achievement (needs a new mastery-ladder entry).
<!-- note:end t-045 -->

## t-046 — Add a pytest that pins the Fever Dream export's fail-closed boss-phase and key-art preflight

<!-- note:begin t-046 -->
Kaizen from the PR #7694 review. The guard was verified by hand only. Build a tmp kind_robots tree with three boss phase webps and key-art, feed ledgers with one phase unfinished, and assert main(--dry-run) exits 1 naming the missing phase; then with all phases DONE assert it gets past preflight (stub render_path so no PIL or network is needed).

Added three pytest cases for incomplete boss phases, missing key art, and successful fully rendered dry-run export; PR and CI review still required.

Reviewer 2026-11-20: merged PR #7698 (three pytest cases pin fail-closed boss-phase and
key-art preflight; CI green). Done.
<!-- note:end t-046 -->

## t-047 — Make review_rainbow_doodle_art.py print an edge-risk summary so the DOODLE-SET-2 visual pass starts from the risky sprites

<!-- note:begin t-047 -->
Kaizen from the PR #7699 review. The sheet builder records edge_check per asset in visual-review.yaml but only prints a count. Print each edge-risk asset (rel path, ArtImage id) after the run and add a test that a non-green border appears in that list. Never change keeper verdicts.

Added edge-risk sprite relative paths and ArtImage IDs to the private doodle review CLI, with an offline mixed-border regression. Implementation commit 7d936bc460c8dbcd1cbe8bf4127de541722476a0; review pending.

Edge-risk relative paths and ArtImage IDs shipped in merged Conductor PR #7709 (2026-11-20 18:06 PT), with offline mixed-border regression. Follow-up shared fixture landed in PR #7713; no keeper verdicts changed.
<!-- note:end t-047 -->

## t-048 — Share one tmp kind_robots + DOODLE ledger fixture between the Rainbow doodle export and review tests

<!-- note:begin t-048 -->
Kaizen from the PR #7698 review. tests/test_export_rainbow_doodle_art.py and tests/test_review_rainbow_doodle_art.py each hand-build classic webps and ledgers with slightly different shapes (art.krea vs art.kontext, jobs present or not). Move the builder into one helper so both suites exercise the same ledger shape the real DOODLE-SET-2.yaml uses.

Shared synthetic-but-valid 64x48 WebP and PNG DOODLE-SET-2-shaped fixtures between exporter and contact-sheet tests. Two original fixture builders eliminated. Regression checks assert per-lane jobs, ArtImage provenance and importer schema. Kind Robots game code untouched. Commit bcb4951b; CI required before merge.

Shared DOODLE-SET-2 export/review fixture merged in Conductor PR #7713 at 6867d7b3e08a1d4ae419cc42ffe1a20b79cfaf9a. Worker PR CI, Security Audit, handoff and task-events checks passed on resolved head 02629878253480c39f390c49d9fef58c03f49d93. No production art or game runtime changes.
<!-- note:end t-048 -->

## t-049 — Validate each rendered opening clip's container, size and identity lock before the opening export composes it

<!-- note:begin t-049 -->
Kaizen from the PR #7730 review (worker suggestion). scripts/export_rainbow_opening.py now decodes WAN MP4/WebM via ffmpeg but trusts whatever bytes come back. Add a fail-closed per-clip check that runs before composition: magic-byte container type, minimum frame count and dimensions, and that the ledger subject's source_image_id still matches its DOODLE-SET-1 identity-locked keeper. Report bad clips by shot key and fall back to the pinned still instead of emitting a broken cut.

Reviewer 2026-11-21 PT: rescued worker PR #7747 as #7749 (merged c8d204f) after fixing
the double-escaped WebM magic literal and fixtures that never reached ffprobe; 11 tests
pass and all 8 live recut-2 shots pass the keeper gate. #7747 closed as superseded.
<!-- note:end t-049 -->

## t-050 — List the opening shots that fell back to stills in the delivery report so their WAN jobs can be re-queued

<!-- note:begin t-050 -->
Reviewer kaizen from the 2026-11-21 PT merge of conductor#7752 (b7e0a00), which made the manifest count only validated animated shots. export_rainbow_opening.py now knows exactly which keys decoded (accepted_clips). Print and record the complement, the shot keys whose clip was DONE in the ledger but fell back to the still, in the manifest and delivery report, with a test, so a reviewer can re-queue exactly those WAN jobs.

2026-11-21 PT Reviewer: merged conductor#7764 (squash 852e731). render() records DONE
WAN clips that failed validation as rejected (pending shots excluded); export prints
them and writes opening-rejected-clips.json beside the media. 12 tests pass locally;
full CI green. Reviewer restored the PR body to the handoff template (the only red
check). Kaizen -> t-051.
<!-- note:end t-050 -->

## t-051 — Surface opening-rejected-clips.json in the opening manifest or delivery report so the WAN re-queue list is visible without re-running the export

<!-- note:begin t-051 -->
Reviewer kaizen from the 2026-11-21 PT merge of conductor#7764. t-050 writes the rejected shot keys to a sidecar opening-rejected-clips.json beside the media, but the manifest and delivery report the task named still do not show them. Read the sidecar (or pass the list directly) into the manifest/delivery report, with a test, and note the shot keys a reviewer should re-queue.

Opening exporter now writes opening-delivery-report.json with accepted, rejected, pending-still and exact WAN requeue shot keys; added two regression tests. Implementation PR pending checks.

Reviewer merged conductor#7774 (e94f0e5) on green exact-head CI after rewriting the prose PR body into the handoff template; code unchanged. Kaizen t-053.
<!-- note:end t-051 -->

## t-052 — Check each queued opening WAN job against the export clip budget (8s, 128 frames) at queue time so over-budget renders fail before spending GPU time

<!-- note:begin t-052 -->
Reviewer kaizen from the 2026-11-21 PT merge of conductor#7768, which caps opening clip decode at MAX_CLIP_SECONDS=8 / MAX_CLIP_FRAMES=128 in scripts/export_rainbow_opening.py. A WAN job queued with a longer length would now render fine and then be rejected at export. Share the constants with the opening queue/ledger code and fail loudly at queue time, with a test.

Added pre-enqueue WAN clip budget validator and tests for approved ledger, excessive duration, excessive frame rate and invalid inputs. PR pending CI; queue submission integration remains to verify.

Reviewer 2026-11-21 PT: merged conductor#7776 (61a4f2a) on green exact-head CI.
Preflight validate_opening_queue_budget() plus --check-queue-budget; no separate queue
script exists, so kaizen t-054 wires the flag into CI.
<!-- note:end t-052 -->

## t-053 — Fold opening-rejected-clips.json into opening-delivery-report.json so the opening export writes one review sidecar instead of two overlapping ones

<!-- note:begin t-053 -->
Reviewer kaizen from the 2026-11-21 PT merge of conductor#7774. scripts/export_rainbow_opening.py now writes both opening-rejected-clips.json (t-050) and opening-delivery-report.json (t-051), and the report's rejected_shots/accepted_shots duplicate the older sidecar. Drop the older file (or make it a pointer), update any reader, and keep the tests asserting exact keys. Open the PR with the AGENTS.md handoff headings; five Worker PRs on this project today went red only on that check.

Removed redundant opening-rejected-clips.json output, added single authoritative report writer, stale legacy sidecar cleanup and regression test. PR pending CI.

Reviewer 2026-11-21 PT: merged conductor#7777 (00b602b) on green exact-head CI.
write_delivery_report() is the only sidecar writer and removes stale opening-rejected-
clips.json; no readers of the legacy file exist.
<!-- note:end t-053 -->

## t-054 — Run export_rainbow_opening.py --check-queue-budget in CI whenever the opening clip ledger changes so an over-budget WAN subject fails at PR time

<!-- note:begin t-054 -->
Reviewer kaizen from the 2026-11-21 PT merge of conductor#7776 (t-052). The budget preflight exists, but nothing calls it before ArtJobs are submitted: there is no separate opening queue script, so an agent editing projects/rainbow-bullet-hell-space-princess/art/OPENING-CLIPS-2-DOODLE.yaml can still queue a 10s WAN subject. Add a path-filtered CI step (or extend an existing ledger guard) that runs the flag, with a test that an over-budget fixture fails. Open the PR with the AGENTS.md handoff headings.

Added path-filtered opening WAN queue budget CI and three subprocess regression fixtures covering approved, over-duration and excessive-fps ledgers. Implementation branch worker/rainbow-bullet-hell-space-princess-t-054-budget-ci-b7e2.

The opening WAN budget CI workflow and three regression fixtures are present on Conductor main; the implementation PR #7781 is merged. Original PR handoff workflow failed on stale event payload despite corrected PR body. No gameplay or ArtJob delivery claimed.
<!-- note:end t-054 -->

## t-055 — Record each WAN shot's requested seconds, fps and frame headroom against the 8s/128-frame budget in opening-delivery-report.json

<!-- note:begin t-055 -->
Reviewer kaizen from the 2026-11-21 PT merge of conductor#7777 (t-053). opening-delivery-report.json is now the single review sidecar; reuse the t-052 budget arithmetic (validate_opening_queue_budget) so the report lists per-shot requested duration, fps, frames and remaining headroom. A reviewer can then see which re-queue shots are near the limit without reading the ledger. Assert exact values in a test.

opening-delivery-report.json now carries wan_shot_budgets (per WAN shot requested seconds, fps, frames, seconds_headroom, frame_headroom vs the 8s/128-frame budget), computed by wan_shot_budgets() which validate_opening_queue_budget now reuses. Exact values asserted in tests/test_rainbow_opening_queue_budget.py, including a tiny-overage (8.0001s) rejection regression guard.
<!-- note:end t-055 -->

## t-056 — Add a per-stage art audit that lists each Gen-2 stage's authored guardian/pickup/hazard asset paths with their completed ArtImage ids, flagging any still missing

<!-- note:begin t-056 -->
Reviewer kaizen from the 2026-11-22 PT merge of conductor#7810 (t-028 X2 art intake, Worker suggestion). Scope: read projects/rainbow-bullet-hell-space-princess/art/GEN2-*.yaml plus the art ledger and print, per stage (X1..X4), each subject asset path and its ArtImage id or MISSING; exit non-zero only with --strict. Pure local read, no API calls.

Added read-only X1-X4 guardian/pickup/hazard ArtImage audit and five local passing tests on worker/rainbow-bullet-hell-space-princess-t056-stage-art-audit-20261122; app code and asset state unchanged. Await CI and merge.

Conductor #7831 merged as 78355632 with all four completed green workflows. Read-only X1-X4 ArtImage audit shipped with five locally passing regression tests; strict mode flags absent authored asset categories, invalid IDs and conflicts. No visual approval, direct art delivery or game integration is claimed.
<!-- note:end t-056 -->

## t-057 — Unit-test validate_shot_coverage in export_rainbow_opening.py and give coverage failures their own error prefix

<!-- note:begin t-057 -->
Reviewer kaizen from the 2026-11-22 PT merge of conductor#7815. The new preflight shipped without tests; add cases for a missing shot, a duplicate key, a non-int or zero source_image_id, and both the doodle and legacy rounds. Failures currently print under the "opening WAN queue budget:" prefix; give coverage errors a distinct message.

Added opening coverage regression tests and distinct preflight error classification on worker/rainbow-t057-coverage-20261122.

Conductor PR #7827 merged on 2026-11-22 PT (head 34613e7), shipping six coverage/error-label regression tests and distinct coverage preflight diagnostics.

Reviewer merged conductor#7827 (6c624755) after all latest-head checks were green. The Worker PR handoff check initially failed on missing headings; the reviewer restructured the PR body only. Coverage tests cover missing/duplicate shots, invalid ArtImage IDs, both rounds and malformed subjects; coverage errors now print "opening shot coverage:".
<!-- note:end t-057 -->

## t-058 — Make the opening-wan-budget CI job assert the distinct 'opening shot coverage:' prefix against the live ledger

<!-- note:begin t-058 -->
Reviewer kaizen from the 2026-11-22 PT merge of conductor#7827 (t-057). Coverage and WAN-budget failures now have separate prefixes, but only unit tests pin that. Extend the opening-wan-budget workflow step (or a test it runs) so a coverage failure on the real ledger shows up under its own prefix in CI logs. No production data changes.

Added live-ledger-mutated missing, duplicated, and invalid ArtImage tests in scripts/test_rainbow_opening_budget_ci.py, proving opening shot coverage errors have their own prefix in CI rather than being mislabeled WAN budget failures. Implementation commit dc226f7. Await CI and merge.

Conductor PR #7836 merged as dbc31dc, with Worker PR CI, Security Audit, opening WAN budget, event processing and handoff checks all completed green. Live-ledger missing/duplicate/invalid shot fixtures now require distinct coverage failure prefix.
<!-- note:end t-058 -->

## t-059 — Ship the reviewed Gen-2 alternate-Act renders (X1-X4 guardians, rescue pods, lighthouse lamp) into the cabinet

<!-- note:begin t-059 -->
Silas, 2026-11-22 PT in-session: bring Rainbow to playtest readiness. 19 Gen-2 renders sit DONE in GEN2-KELP-NEBULA-X1, GEN2-CORAL-COMET-X2, GEN2-ALT-GUARDIANS-1 and MIRROR-SHOAL-X4, but none ships under kind_robots public/rainbow-princess-art; the Pearl Warden draws the Bulwark, the Bellkeeper draws the Mirror Eel and the Herder/Shoal Koi fall back to a scaled scout. Visually review each render, key the green matte, export the keepers and wire guardians, pods and lamp with code-drawn fallbacks. Kelp Warden sweep/hurt poses and the X4 parallax planes are reviewed separately (identity drift / grey horizon band).
2026-11-22 PT: Reviewed all 19 Gen-2 renders; shipped 8 (five X1-X4 guardians as their own paintings, X1/X2 rescue pods, X3 lighthouse lamp) with Fever Dream twins via scripts/export_rainbow_gen2_art.py (new muted-matte key; Krea paints the green matte too dull for key_green). Held: Kelp Warden sweep/hurt (identity drift), Shoal Koi pose frames and both hazards (no runtime hook), X4 planes (far plane grey band). Implementation kind_robots#5616.
2026-11-22 PT done: kind_robots#5616 merged as bf6b6ad8 after all checks completed green (incl. TypeScript, Contract verifiers, Rainbow cabinet Chromium jobs); conductor#7874 merged as 7137b5da. Follow-ups stay on the gap matrix: hazards (item 2), X1-X4 planes (item 4).
<!-- note:end t-059 -->

## t-060 — Rebel road changes the fight: Acts VI-VIII waves react to the flown allegiance

<!-- note:begin t-060 -->
PLAYTEST-GAP-MATRIX-2026-11-22 item 9 (issue #4146 section 5). The flown rebel/loyal choice currently changes only dialogue and ending titles (rainbowAllegiance.ts:56-92). On the rebel road Ocean craft hold fire and Motherland drones join Acts VI-VIII waves per PLOT-MOTHERLAND.md; loyal keeps the current waves. Deterministic seeded tests for both roads and 1-4 seats; save/continue preserves the road.
2026-11-22 PT: rainbowRebelRoad.ts: every third Ocean school per Act (aimed-volley kinds only) holds a truce (no fire, no ram, untouchable, dimmed under a heart); a Motherland drone pair launches a beat after each in its lane. New motherdrone kind + Krea art 279290. Seeded flight both roads: rebel 274 volleys held, drones seen; loyal unchanged. New PR workflow rainbow-rebel-road.yml. kind_robots#5634.
2026-11-22 PT done: kind_robots#5634 merged as 2123a7cd after all 24 checks completed green (incl. TypeScript and the new Rebel Road workflow).
<!-- note:end t-060 -->

## t-061 — Allegiance-specific finale: Motherland flagship vs Ocean heart, with the loyal late stand-down

<!-- note:begin t-061 -->
PLAYTEST-GAP-MATRIX-2026-11-22 item 10 (issue #4146 section 5). Rebel road fights the Motherland flagship, loyal road the Ocean heart, with the late course-correction PLOT-MOTHERLAND.md:43-50 describes. Distinct fights, not retitled ones; prove all six ending roads are reachable by flown input. Builds on rainbowEclipseFinale.ts.
2026-11-22 PT: Rebel road fights the Motherland flagship (lane lances, drone launches, bridge weak point; clamps open below half; painting 279298); loyal road fights the Crown, which pleads 7 s when its heart breaks loose — flying high stands down to the rebel road. All six road endings + the stand-down flown from real Act IX saves in verifyRainbowFinaleRoads. kind_robots#5640.
2026-11-22 PT done: kind_robots#5640 merged as 1bb732fb after all 24 checks completed green (TypeScript, ESLint/Prettier, the Rebel Road + finale workflow, all contract shards).
<!-- note:end t-061 -->

## t-062 — Run verifyRainbowSaveBytes and verifyRainbowSeasLogbook in CI

<!-- note:begin t-062 -->
PLAYTEST-GAP-MATRIX-2026-11-22 item 19. Both kind_robots tests exist on main but no workflow or package script runs them, so save-capacity and flight-log regressions can land silently. Add them to the Rainbow save/route workflow (or test:arcade-engine) and confirm a green run.
2026-11-22 PT: Both tests added to rainbow-alternate-route-memory.yml (PR-gating), with path triggers for rainbowSaveSlots.ts and arcade/saves.ts. Both pass locally. kind_robots#5619.
2026-11-22 PT done: kind_robots#5619 merged as fd2ee42e after all checks completed green; the route-memory job ran both new steps successfully.
<!-- note:end t-062 -->

## t-063 — Rainbow at 360x640 in the viewport suite, with a minimum rendered size for hostile shots

<!-- note:begin t-063 -->
PLAYTEST-GAP-MATRIX-2026-11-22 item 20 (issue #4146 section 8). verifyArcadeViewport covers Rainbow at 390x844 and wider but not 360x640, and reports sprite CSS px without asserting a floor for hostile bullets. Add the size and an assertion that hostile projectiles render at or above the readability floor at DPR 1/2/3.
2026-11-23 PT: kind_robots#5666 adds Rainbow 360x640 at DPR 1/2/3 to verifyArcadeViewport and asserts every hostile pellet body renders >= 8 CSS px (9.4 px at 360x640; halo larger; backing px >= CSS px), using the engine's exported RAINBOW_SHOT_BODY_RADIUS/HALO_RADIUS. Same PR adds rainbow-verifier-suite.yml so every verifyRainbow*.test.ts runs on Rainbow PRs. Merge when all checks complete green.
2026-11-23 PT: kind_robots#5666 merged as 23cedefd after all 23 checks completed green (incl. the new Every Rainbow verifier suite and cabinet-viewport at 360x640).
<!-- note:end t-063 -->

## t-064 — Re-render the Motherland flagship phase-2 painting so the sprung clamps and battered hull read in game

<!-- note:begin t-064 -->
Kaizen from the conductor#7897 review (t-061). ArtImage 279299 was rejected (not battered, clamps not sprung, hull colours drift), so phase 2 of the flagship fight reuses the phase-1 painting 279298 with code-drawn cues. Queue a new Krea 2 take seeded from 279298's composition (same hull palette, clamps visibly open, scorch and sparks), review it at game scale against the clamp-core hit geometry, and swap bosses/flagship phase 2 in kind_robots only if it beats the code cues.
2026-11-23 PT: Kontext take D (279493, ledger MOTHERLAND-FLAGSHIP-PHASE2-2026-11-23) beats phase 1 + code cues: battered hull, same palette/framing, no decoy ring. kind_robots#5670 swaps bosses/flagship-phase2 in both looks at phase 2 with its own Crown point (0.049, 0.257), checked at game scale against the 44 px ring. Merge when all checks complete green.
2026-11-23 PT: kind_robots#5670 merged as 86f62a5f after all 23 checks completed green; the rebel-road flagship turns battered (279493) when its clamps spring, in both looks.
<!-- note:end t-064 -->

## t-065 — Gameplay critic round 1: one-button super, super economy, co-op boss HP, guardian variety, Crown safe pockets

<!-- note:begin t-065 -->
From the independent gameplay critic (REVIEW-ROUND-1-2026-11-23.md, D1-D3, D5-D9, P-15): super on a short B tap only (hold stays focus); cut the kill refund, a radius wipe, boss damage as a share of max HP; co-op boss HP about 2.5 + 2(n-1); per-kind guardian movement, HP tier by Act, aimed fans that close the aimed line, varied arrival; Crown spoke and ring jitter or an aimed spoke so no ray is safe; Act-specific launchers; boss returns to the start of its phase on continue (D8 default, owner may override); optional seeded variations. Extend verifyRainbowBossCamping to every boss and the persona matrix as regression evidence.
2026-11-24 PT: kind_robots#5713 (merged 5b589b7b) ships D1 (B hold focus, tap super within 12 frames), D2 (kill refund 4, was 12; supers take 3.5%/5% of a boss hull; whole- screen wipe kept because the cut-in covers the comms band), D3 (2 base shares per extra pilot, was 4: 3.4x solo hull at four pilots), D5 (per-kind guardian motion; alternate aimed-fan volleys close the open lane with one slow pellet; a per-Act hull tier was tried and dropped because late guardians escaped), D6 (alternate Crown volleys aim a spoke; phase-2 pair closes on alternate volleys; verifyRainbowBossCamping covers Crown phase 1). D8 was tried (boss back to its phase start on continue) and reverted: it made B01 unbeatable for the solo test bot within its budget, so it stays Silas's call. Remaining: D7 Act-specific launchers, D9 seeded variation (optional), P-15 Leviathan burst, and the camping audit's other flagged phases (Delphion 2, Lantern Ray, Glass Eel, Leviathan 3) to confirm in-engine.
2026-11-24 PT: D7 (eight Act-specific mortar shells) and P-15 (the Leviathan burst spawns as two rings) fixed in kind_robots#5737. Left: D9 (optional seed variation).
2026-11-25 PT: D9 fixed in kind_robots#5829 (merged 6285d33d): a run's seed mirrors whole authored waves across the lane band, wave by wave; same seed replays exactly; the attract demo and scripted scenarios keep authored lanes and draw nothing extra from the rng. verifyRainbowWaveVariation added. Round-1 gameplay critic closed except D8 (owner call, unchanged).
<!-- note:end t-065 -->

## t-066 — Story critic round 1: choice-specific endings, spoken Crown plea, real crew exchanges, per-pilot Act voices, Lilt agency

<!-- note:begin t-066 -->
From the independent story critic (REVIEW-ROUND-1-2026-11-23.md, S3-S11, S15-S17, S20, S21; the blockers S1/S2 and S12-S14, S18, S19, S22 shipped in kind_robots#5709): give each final choice its own escape beat, Lilt resolution and crew line; an A09.PLEA scene and stand-down variants (TURN, AFTER, credits, archive); rewrite the 15 combination lines as 2-3 line exchanges with planted setup and spread speakers; role-true lines by pilot identity, not seat; at least one pilot-keyed line per present pilot per Act carrying her arc, and a third-voice slot for middle seats; one consequential act for Lilt-7 per road; one rescue tally everywhere; continue/defeat lines; speaker-only comms headers; in-world archive copy and a stand-down entry; branch the cadet epilogue on cadetsHome.
2026-11-24 PT: kind_robots#5721 (merged 74c93633) ships S4: A09.PLEA plays across the Crown's 7 s plea (the Crown asks, Lilt names the turn, the lead answers), and a stood- down crew hears the turn in A09.TURN, Lilt's resolution and the credits (THE ROAD: TURNED AT THE CROWN). Remaining: S3, S5-S11, S15-S17, S20, S21.
2026-11-24 PT: S5, S6, S17, S20, S21 fixed and S9 partly fixed in kind_robots#5737 (crew exchanges, speaker-only comms header, in-world scrapbook plus a stood-down page). S3 and S10 (choice-shaped escape and resolution; Lilt acts) are in kind_robots#5738. Left: S8 (pilot-keyed Act beats), S9 in Act scenes, S11 (road- and crew-aware ending plates, with P-03).
2026-11-24 PT: story critic round 1 is closed out except owner calls. Fixed: S3, S10 (kind_robots#5738); S8, S9 (#5740); S7, S15 (#5742); S11 (#5741). Earlier: S5, S6, S17, S20, S21 (#5737); S1, S2, S4, S12-S14, S16, S18, S19, S22 (#5709-#5729).
2026-11-25 PT reconciliation: every t-066 row in REVIEW-ROUND-1-2026-11-23.md is fixed and merged (S3-S11, S15-S17, S20, S21 via kind_robots#5709-#5742); the task stayed ready after its 11-24 close-out note. Closed done; round-2 story review will raise anything new.
<!-- note:end t-066 -->

## t-067 — Presentation critic round 1: co-op HUD and touch pads off the playfield, phone and large-screen layout, pellet readability

<!-- note:begin t-067 -->
From the independent presentation critic and the gameplay critic (REVIEW-ROUND-1-2026-11-23.md, D4, P-05, P-06, P-08 to P-11, P-13, P-16 to P-18, P-20 to P-23): move the 2-4p status panel off the playfield (top bar or bottom edge) and never over the boss bar; keep touch pads out of the stage (gutters, or no four touch seats on one tablet); a portrait-tuned HUD or rotate prompt and corner chips off the canvas on phones; size the stage from content height on large screens; collapse the switches on short screens; ambient bubbles never bullet-sized in the play band; a hostile pellet hue no scene uses (or bold by default); painted Act V wreck frames; per-Act colour keys; fade the control legend after Act I; seat tags off the hull; Seas cards keep art on phones and the route map is a real map. Verify in the real cabinet at 360x640, 390x844, 768x1024, 1024x768, 844x390, 1440x900 and 1920x1080, 1-4 seats.
2026-11-24 PT: kind_robots#5716 (merged af529b34) puts every pilot's status inside the 29 px HUD bar (D4/P-08: no panel over the playfield or the boss bar), shows the button legend in Act I only (P-21), firms the default pellet halo with a faint ring (P-11) and moves seat numbers behind the hull (P-22). kind_robots#5719 (open) makes the Act V cranes solid (P-13) and Classic's motes faint (P-10). Remaining: touch pads over the stage (P-05/P-06), phone portrait and short-landscape layout (P-09/P-23/P-17), large- screen stage size (P-16), per-Act colour keys (P-20), Seas on phone (P-18).
2026-11-24 PT: kind_robots#5719 (merged a5ec888c) makes the Act V cranes solid silhouettes (P-13) and Classic's ambient motes faint far-plane dots (P-10); kind_robots#5720 (merged 7b917371) lifts the Arcade-wide 64rem cap on the Rainbow page only, so the stage is 1446x813 (about 57%) at 1920x1080 instead of 994x559 (27%), measured on the real page with no page scroll (P-16). Remaining: P-05/P-06 touch pads over the stage, P-09/P-23/P-17 phone and short-landscape layout, P-20 per-Act colour keys, P-18 Seas on phone.
2026-11-24 PT: presentation layout findings fixed: P-05, P-06, P-17, P-23 and the in- scope part of P-09 (kind_robots#5741; the portrait HUD stays open); P-18 Seas on phone (#5756); P-20 per-Act colour keys (#5740).
2026-11-24 PT: P-09 portrait HUD: on an upright phone a large-type status readout (Act, score, shoals and novas, each pilot's lives, shields, power, charge and ready moves) fills the empty gap between the chips and the controls, above the turn-sideways prompt. kind_robots#5768, CI pending. With this, every t-067 finding from presentation critic round 1 has a fix.
kind_robots#5768 merged as 2b8f24fe after 23 checks passed. Every t-067 finding from presentation critic round 1 is fixed and covered by the browser layout tests at the listed viewports and seat counts.
<!-- note:end t-067 -->

## t-012 — Produce opening, between-stage dialogue, endings, sound and score

<!-- note:begin t-012 -->
Authored original short opening, mid-run character moments, distinct victory/failure and route endings, skippable credits, voice-optional subtitle treatment, original cleared sound rights, layered music and shot/hit/cue mixing. No copyrighted music/sample reuse.
Progress 2026-10-17 PT: an original layered chiptune score (each Act's key, mode and lead; drums for a guardian, drums and an arpeggio for a boss; ending and failure loops), Lilt's failure ending when the CONTINUE? countdown runs out, and A to skip the credits merged in kind_robots#3803. After Silas's first playtest (a solo Act I felt silent): Lilt calls out every Act I section with a pilot reply (#3806), and a pilot select renames the crew in Lilt's lines to the pilots flown. Open: the 15 composition banter tracks with a 4-bit pilot mask, between-stage dialogue for Acts II-VIII at the same density, voice-optional subtitle treatment, cinematic ending boards.
2026-11-01 PT claim-staleness assessment (Silas: stale claims are more likely finished- but-unrecorded than abandoned): partial work merged (#3803, #3806); open items per the 10-17 progress note: 15 banter tracks, Acts II-VIII between-stage dialogue, subtitles, ending boards. Claim released.
2026-11-06 PT (writing half, round 6): the finale now pays off the Act V allegiance choice. Each road (turn on the empire or stay the course) times each final choice is a named ending: ASK FIRST, OPEN WATER, NO MORE LEASHES, PEACE BY ORDER, AN EMPTY OCEAN and ORDERS BROKEN, plus the three shipped endings for flights saved before the memorial. The road sets the world consequence, Lilt's resolution, the epilogue for each crew size and the send-off, and the rescue verdict has four tiers. The credits and THE END name the ending. Acts VII and VIII close on a bridge line for each road, and the finale's opening and turn answer the road. Act I's opening is three punchy lines. A skips the ending line by line, and ending lines hold for 180 frames. verifyRainbowStoryScript pins: - intro, turn and outro dialogue for every Act; - 4,101 lines that fit the comms box at arcade pace, with no absent speakers; - every ending reachable by flying it; - the skip, through the engine.  Remains: the 15 partyMask composition tracks, with pilot-specific solo lines (dialogue is still written in seat terms and renamed by the pilot select); ROUTE-MAP route stingers once the t-028 alt flags exist; subtitle and comms settings (full, essential or off; replay); cinematic ending boards; and the sound and score half. Merged as kind_robots#4866 (2026-11-06).

Authored all fifteen distinct pilot-set reveal responses and ending stingers, integrated them into Act VI and the finale by the actual four-bit pilot mask, and added script validation. Implementation commit 98343fc9a85723dbd73fdd35098e718632df0a10; t-012 still has further audio, comms settings and cinematic work.

Merged Kind Robots PR #5360 as 0635f88902e2cd7aef0b27c4eb89239d1d821e9c after all 10 latest workflow checks passed. The 15 pilot-set reveal and ending tracks are integrated, but comms settings, cinematic boards and audio remain. Release claim for continued implementation.

Implemented independent local 1-4 player C.A.T.S. crew selection and checkpoint-safe ordered pilot rosters, making the 15 previously merged authored dialogue masks reachable in real play. PR pending. Audio, subtitle controls, full cinematics and 15-mask runtime QA remain open; this review is a partial implementation, not task completion.

2026-11-24 PT: kind_robots#5687 (merged 12868a79) adds four orchestral detour themes
rendered offline by scripts/rainbow-score (levels matched to the Act cues), distinct SFX
for super/shield/hurt/boss phase/route fork/stinger, and the route stingers. With comms
full/story/off (#5670) and the 15 party masks, t-012's remaining scope is the animated
cinematics, tracked under t-030.

2026-11-23 PT: kind_robots#5709 (merged 66b6caa8) fixes the independent story critic's
blockers (REVIEW-ROUND-1-2026-11-23.md): S1 only the crew speaks on comms, detours
included (crewLine maps unflown authored seats onto the crew); S2 the rebel and loyal
road epilogues play (loyal crews no longer hear a rebel-toned party line); plus S7 four-
pilot finale roles, S12 safe-route continuity, S13 credits, S14 plurals, S18 solo
address, S19 rebel log, S22 loyal verdict. verifyRainbowCrewVoices pins them. Story
majors S3-S11 and the remaining minors are t-066.

2026-11-26 PT intent audit: closed. #5709 (critic fixes), #5687 (score, SFX, stingers)
and #5670 (comms modes, 15 party masks) merged. The 11-24 note moved the only remaining
scope, animated cinematics, to t-030; the story majors went to t-066 (done). Closed so
that scope is not tracked twice. The 11-20 claim had expired.
<!-- note:end t-012 -->

## t-022 — Kontext pass: recolour off-model frames, compose cutscenes and group art, and build layout-guided stage planes

<!-- note:begin t-022 -->
Silas, 2026-10-14 PT: "yes, open the Kontext pass as its own task", following t-020's finding that txt2img has plateaued on multi-element scenes and stubborn colours (see t-020 note and art/ART-ROUND-1..8). Write art/ART-ROUND-9-KONTEXT.yaml and drive it with scripts/enqueue_art_requests.py (engine: kontext lanes, source_image_id / reference_image_id / source_pad / mask_box are already supported). Keep the house look: Arthemy Western v3 + western-toon tags; every source must be an approved ArtImage from the t-020 ledgers. (1) RECOLOUR, masked where possible: Azure coat to powder cyan from 246431 (select) and 246147/246149 (comms/neutral); Vivi's purple and coral streaks onto 246439/246440; Halo Fin hull to butter yellow and gold from 246443/246445; Comet Crown to a clean three-prong lilac arrowhead from 246448. Pass bar: canon colours per CAST-BIBLE.md, face and body unchanged. (2) COMPOSE: group key art from the four approved pilots as references (Maribel 246424, Azure recolour from (1), Solenne 246155, Vivi 246439) with heights and builds preserved; title key art from backdrop 246126 plus the four ship sources (246198, 246201, recoloured Halo Fin and Comet Crown); cutscenes C01-C03, C05-C09 and C14-C17 restaged from approved cast, boss and enemy ArtImages instead of txt2img; the B09 Eclipse Crown boss; and the Comet Parade super (246570 drew a woman) built from the Comet Crown ship plus drone trails. (3) STAGE PLANES: for S01-S09 x far/mid/near/fore, script a flat-colour layout guide (horizontal bands, edge-to-edge silhouettes, empty top third, nothing centred) and Kontext-paint it, keeping the 246449 and 246453 far plates as style anchors; then test tiling and parallax in the real cabinet at 390/768/1440. (4) Pickups u04, u11, u12 redrawn to their WORLD-BIBLE shapes. Do not reroll anything t-020 already kept. Generated art is pre-approved internal work (AGENTS.md); public release stays gated by t-014.
2026-11-01 PT claim-staleness assessment (Silas: stale claims are more likely finished- but-unrecorded than abandoned): no round-9 Kontext completion found; related art PRs (#3772-#3794) landed but the ledger items are unverified. Claim released; verify against art/ART-ROUND-9-KONTEXT.yaml before redoing.

Partial stage-depth milestone: implementation adds two distinct mirrored painted parallax layers with safe reviewed-art fallbacks and viewport coverage contracts; companion art ledger requests 16 source-backed far/mid panoramas for Acts I-VIII at priority 1000. Generation, review and media integration remain pending.

2026-11-23 PT: layout-guided stage planes delivered: seven reviewed DOODLE-STAGE-DEPTH-
PLANES (s01 far/mid, s02/s06/s08 far, s07 far/mid) replace the coral-crop stand-ins in
kind_robots#5685; the other nine were refused (jets/rockets read as enemies; s04
watermark) and keep the reviewed crop. Remaining t-022 scope is the round-9 off-model
recolour and cutscene/group composition, folded into t-030's moving-cutscene work.

2026-11-24 PT: P-04 painted sky, far and mid planes for all eight main Acts in both
looks (kind_robots#5761, #5762, #5764, #5767), plus the finale's Crown-interior planes
(#5767). Detour skies drift (#5742). Still rendering: the s09 card (P-07) and the Fever
Dream detour twins (P-14), conductor ART-BACKLOG-2026-11-24.

2026-11-25 PT: kind_robots#5767 merged: the finale's own card, strip and planes (P-04,
P-07) and X1-X3 Fever Dream detour twins (P-14); X4 sky in #5774. Retakes on a green key
for X1 far, X2 far, X3 mid/near and X4 far/near are rendering.

2026-11-26 PT intent audit: partial, so back to ready. The planes, cards and detour
twins shipped (#5767, #5774). The X1-X4 green-key retakes are still rendering (ART-
BACKLOG-2026-11-24). The 11-22 claim had expired.

2026-11-27 PT close: full scope verified. The X1-X4 green-key retakes the 11-26 audit
listed as rendering all rendered, were reviewed keep (ART-BACKLOG-2026-11-24 doodle-
alt-x*-2, 'Closes P-14') and shipped in kind_robots#5810 (merged 2026-11-25); all 14
doodle/alt planes are on kind_robots main. Stage planes: #5685, #5767, #5774, #5810.
Round-9 recolour and group/cutscene composition were folded into t-030 on 2026-11-23 and
stay tracked there; pickups u04/u11/u12 were redrawn in ART-ROUND-10-VOLUME.
<!-- note:end t-022 -->

## t-044 — Main-game standard: audit and close the gaps for Rainbow Bullet Hell Space Princess

<!-- note:begin t-044 -->
Silas 2026-11-11 PT, in session: "Our games should all have a base standard of quality ... We want our main games to have 12 plus achievements." Standard: docs/agents/main-game-standard.md; CONTROL.md global overview.

AUDIT DONE 2026-11-12: projects/rainbow-bullet-hell-space-princess/STANDARD-AUDIT-2026-11-12.md holds the Met/Partial/Missing table, a proposed achievement list with award points, character-fit notes and the three smallest next PRs. Start there.

Start with the audit table from docs/agents/main-game-standard.md (title screen; settings menu; save/load and persistent progress; 12+ achievements; scrapbook; multiple endings with painted plates; customizable characters; 3+ replay hooks), marking each Met / Partial / Missing with evidence (file, route, live record). Put the table in this note and the first PR. Then close each gap in small CI-tested PRs; queue any needed ending, scrapbook or portrait art in an auto_submit ledger.

Item 7 (customizable characters) applies "in most cases": if this genre makes it a poor fit, say so in the audit with the reason and leave it for Silas rather than skipping silently.

Achievements are tracked by their own task; this one covers everything else.

Stale claim recovery: no matching open Rainbow PR or implementation branch; no code is identified as committed by this claim. Keep main-game logbook and other acceptance gaps open, and reclaim before implementing.

Scoped Seas flight-log implementation pushed as 856edb03ba7a5a49a5668018e631eec6e44bc654: progress silhouettes, earned medals, current Act and ending count; added pure logbook regression test. This is one part of the still-open main-game standard, not completion of t-044.

Added a scoped ending scrapbook to the Rainbow cabinet, tracking only the three actually earned finale choices and keeping unearned endings locked. Distinct Motherland-road variant recording, incomplete ending illustrations, and remaining main-game-standard acceptance remain open.

2026-11-21 PT recovery: prior scrapbook review claim is over 24 hours old, no open t-044 PR or active branch remains; existing logbook/ending scrapbook work is preserved. Reopen for real allegiance-specific ending scrapbook unlocks without falsely attributing historical generic choice feats.

Partial t-044: standalone app PR silasfelinus/kind_robots#5547 (commit 0090f25d) records six exact Motherland rebel/loyal ending roads in existing mastery persistence, adds distinct nine-slot scrapbook with safe legacy generic-choice records, and full choice/road regression. Last-head CI and merge required. Additional polished ending art, full main-game standard acceptance and live device verification remain open.

2026-11-22 PT recovery: the 02:41Z review handoff is past its TTL with no open t-044 PR or branch (#5547 merged). Returned to ready; nothing discarded. Ending plates: Fever Dream restore 279195 and evacuate 279196 passed review and ship in the next kind_robots PR; sever 279197 failed CAST-QA and re-renders as ArtJob 76729 (ENDINGS-FEVER-DREAM-2026-11-22). Remaining main-game-standard scope per PLAYTEST-GAP-MATRIX-2026-11-22: sever plate, settings (comms, contrast, remap, erase flight log), call sign/paint.

2026-11-22 PT: kind_robots#5621 ships Fever Dream restore (279195) and evacuate (279196)
plates. Sever held: 279197 and 279201 both fail CAST-QA on Maribel's proportions; next
attempt from her doodle portrait via Kontext. Remaining t-044 scope after merge: sever
plate, settings (comms/contrast/remap/erase flight log), call sign/paint.

2026-11-22 PT: kind_robots#5621 merged as 9b74baa8 after all checks completed green;
restore and evacuate endings now show Fever Dream plates. Released for the remaining
scope: sever plate (start from Maribel's doodle portrait via Kontext), settings
(comms/contrast/remap/erase flight log), call sign/paint.

2026-11-22 PT: Silas said 'do what you think best' on the sever plate. Take 4 (279239)
passes CAST-QA and ships in kind_robots#5628, completing all three ending plates.
Remaining t-044 scope: settings (comms/contrast/remap/erase flight log), call
sign/paint.

2026-11-22 PT: kind_robots#5628 merged as c5129034 after all checks completed green; all
three endings (restore, evacuate, sever) now show Fever Dream plates. Released for
remaining scope: settings (comms/contrast/remap/erase flight log), call sign/paint.

2026-11-23 PT: kind_robots#5670 ships the settings gaps: comms full/story/off, high-
contrast (bold) enemy shots, erase-a-slot flight log (two-tap), and per-game key remap
for A/B/X/Y, with pure + real-cabinet Chromium tests. Remaining t-044 scope: call sign
(comms + credits) and three medal-unlocked paint schemes per ship.

2026-11-23 PT: kind_robots#5679 merged as de0e1b51 after all 23 checks completed green:
call sign (Hangar, comms header, credits) and three paint schemes per ship (Factory;
Tide at three silver-or-better medals; Nova at three golds), drawing only; credits now
name the pilots actually flown. With #5670 (comms/contrast/erase slot/key remap), #5628
(all three ending plates), #5547 (nine-slot ending scrapbook) and the existing title,
saves, replay hooks and achievements task, every main-game-standard row from STANDARD-
AUDIT-2026-11-12 now has shipped work. Ready for review against docs/agents/main-game-
standard.md; the final verdict stays with Silas (t-014).

2026-11-28 PT review: done. Every main-game-standard row has merged work on kind_robots main (#5547 0090f25d,
#5628 c5129034, #5670, #5679 de0e1b51; achievements t-045). Device, audible and live-account observations
transfer to the playtest handoff per the 2026-11-27 owner direction in main-game-standard.md.
<!-- note:end t-044 -->

## t-013 — Deterministic combat fairness, multiplayer soak and campaign QA

<!-- note:begin t-013 -->
Full-route autoplay/property runs, zero unavoidable-hit scenarios at documented skill window, seeded repeatability, 60 Hz render target and acceptable mobile fallback, browser refresh/resume, local 1/2/3/4 player soak (no online co-op, t-006 cancelled), keyboard/gamepad and phone/tablet/ desktop UI snapshots. Record measured median completion duration and test all endings; never assert parity to commercial classics based solely on an encounter list.
2026-11-23 PT QA groundwork: four Rainbow verifiers had drifted red on main because most verifyRainbow*.test.ts never ran in CI. kind_robots#5661 brought them in line with the canonical X1-X4 detours; kind_robots#5666 added rainbow-verifier-suite.yml so every Rainbow verifier (60) runs on Rainbow PRs, wall-clock CoopLoad alone. The full suite is now a trustworthy base for the campaign QA pass.
2026-11-24 PT: kind_robots#5689 (merged cf90e9d7): verifyRainbowCampaignMatrix flies 16 fresh campaigns (crews 1-4, two seeds, dock self/early) to THE END; canonical Act order with each detour in its slot; together every detour, both sides of every fork, both roads, the stand-down and all three choices; deterministic replay; median clean campaign 51.6 min (45.3-58.3). verifyRainbowPerformance.browser: four pilots in Act I's boss fight with real art served, engine p50/p95 0.2/0.4 ms, frame pacing p50/p95 16.7/16.7 ms, heap 58 MB. All 64 Rainbow verifiers gate every Rainbow PR. Remaining for an independent reviewer: scripted fail/retry personas (the autopilot never loses a ship) and blind critic passes.
2026-11-23 PT Silas decision (this session, verbatim): "Fresh agent sessions count as independent, go ahead". Fresh cloud agent sessions with no prior context satisfy #4146's blind critic passes and independent review. Launched 2026-11-23 PT: gameplay/fairness (session_01L5NKxambWbSZ7WwNsdzrW2, kind_robots branch claude/rainbow-review-gameplay), story/routes/endings (session_01L5NKxcoC41Nm2tWCsB9Wdk, claude/rainbow-review-story), art/motion/access/devices (session_01L5NKxc2Uyg6NvXB3Cv7jdw, claude/rainbow-review- presentation). Read-only; each pushes a defect report. Repeat the passes after the last significant art/animation change (t-030) before #4146's final verification.
2026-11-23 PT: kind_robots#5709 (merged 66b6caa8) adds utils/scripts/rainbowPersonas.ts, scripted fail-and-retry players (idle, novice, typical, no-super, expert, camper) flying the real engine with damage on and continues on or off, deciding only from the snapshot. First matrix (seed 7): solo typical reaches THE END in 62.8 min with 3 continues (no continues: dies in Act VII); solo expert finishes in 48.4 min with no continues; idle and novice loop in Act I with continues. It found a Delphion phase-3 stalemate (a parked four-pilot crew never hit and never hitting for an hour), fixed with aimed twin fans and pinned by verifyRainbowBossCamping.
2026-11-28 PT: done. Round-2 independent review after the last art change (#4146 section 9): three fresh read- only sessions on main 459343a2 (gameplay: 5 majors; story: ready, 2 majors; presentation: ready, 4 majors; no blockers). All 11 majors fixed and merged: story #6029, presentation #6034, gameplay #6041 (Halo revive by pilot, co-op X/Y, solo balance within 1.34x, Crown novice wipes 7-17 to 1-5, Clawburst pocket closed). All 72 Rainbow verifiers and the five Rainbow Chromium contracts pass on the combined branch. Device, audible and live- build observations transfer to human playtest. Table: READINESS-DOSSIER-2026-11-28.md section 2.
<!-- note:end t-013 -->

## t-014 — Verified production playtest handoff (public release separate)

<!-- note:begin t-014 -->
Assemble the tested preview, art delivery record, local four-player combat, full-run timing, performance/device captures and scores. Verify all finite original build, art, audio and QA tasks; follow CONTROL.md for playtest/normal and flag and close master issue #4146. Human gameplay/visual feedback and any new public Play registration, promotion or deployment are post-roadmap decisions requiring separate authorization. No human verdict is a prerequisite. Prior gate wording is preserved in Git history; no approval is inferred.
2026-11-28 PT: done at Silas's in-session request to finish the roadmap for human playtests. All finite tasks done; lifecycle set to playtest/normal in project-overrides.yaml; master issue #4146 flagged [FLAGGED FOR HUMAN TESTING] and closed as completed. Public /play, Arcade promotion and deployment remain separate approvals; no approval inferred.
<!-- note:end t-014 -->

## t-030 — Gen-2 animation: animated pilot cut-ins, enemy sprite cycles and moving cutscenes

<!-- note:begin t-030 -->
GEN2-STANDARD.md sections 5-6. WAN first/last-frame clips from the delivered cutscene stills (ART-ROUND-19) and pilot cut-ins, then enemy idle/attack cycles packed into atlases. Bullets stay crisp code-drawn shapes; animation is for craft, pilots and scenes.

Partial t-030: painted super cut-ins now have bounded per-pilot temporal camera animation, cropped art, and reduced-motion fallback, with a regression test in the Rainbow browser contract. Implementation commit 591a60cd; verify latest PR CI. Enemy frame atlases, moving cutscenes and full art verification remain outstanding.

2026-11-23 PT (session_01L5NKxaUAWmNr7wxdToBdp3): living Act title cards shipped for
S01, S02, S05, S06 (kind_robots#5703, merged 03f96cd4) and S07 (kind_robots#5704); Fever
Dream look only, calm motion keeps the still, verifyRainbowAnimation covers files and
gate. Rejected S03 (smear) and S04 (animated fake logo; the shipped s04 still also
carries it and needs a clean re-render). First-pass enemy loops all crop-zoomed; framed
-v2 cells and the eight pilot hit/victory poses are still rendering
(T030-ANIMATION-2026-11-23.yaml). Remaining: enemy atlases, poses + hit-pose HUD card,
S08.

2026-11-24 PT: kind_robots#5717 (merged 73cc425e) ships the first enemy frame animation,
Fever Dream idle atlases for picket and urchin (8 raw WAN frames each, matte keyed,
centred, 4 fps; calm holds cell 0), and the S08 living title card (640 px loop), so Acts
I, II, V-VIII now have living interludes. Rejected in review: spiral (turns to camera),
anchor and relay (near-static), lantern (green tentacle streaks), skimmer (source still
cut); third takes queued as jobs 77023-77026. Still open: those retakes, coral, S03/S04
card retakes, the eight pilot poses and hit-pose HUD card, boss/ship motion, and moving
endings (presentation critic P-01 to P-03).

2026-11-24 PT: kind_robots#5727 (merged 4706755f) ships seven pilot poses (Maribel,
Azure, Vivi hit and victory; Solenne victory; CAST-QA face, hair, skin and build against
each identity lock), a hit card that flashes the hit pose over a ship that loses a life,
and idle atlases for anchor and lantern (third takes), so picket, urchin, anchor and
lantern now animate. Rejected: Solenne's hit pose (no reaction), spiral (turns to camera
in both takes), relay and coral (near-static), skimmer (source cut). Still open: those
retakes, S03/S04 cards, boss and ship motion, moving endings.

2026-11-24 PT: P-02 one-shot Act card clips with real motion for all eight Acts
(kind_robots#5743, #5744). The idle-atlas clock (P-01) and moving-ending support (P-03)
are in #5767. 83 renders are in progress (conductor ANIM-BACKLOG-2026-11-24): idle loops
for every enemy, guardian, ship, boss phase, pickup and hazard; motion clips for the six
ending plates. B02 phase 2-3 redraws (P-12) and the Solenne Fever portrait (P-19) are in
ART-BACKLOG.

2026-11-25 PT: kind_robots#5767 merged (idle-atlas clock P-01, moving endings P-03,
Solenne Fever portrait/comms P-19). First reviewed idle loop (angler) ships in #5774; 81
loops and the six ending clips are still rendering (ANIM-BACKLOG-2026-11-24).

2026-11-26 PT intent audit: partial, so back to ready. The idle-atlas clock, moving
endings and P-19 shipped (#5767). Idle loops are being reviewed in batches
(conductor#8117, batch 12); the rest are still rendering (ANIM-BACKLOG-2026-11-24). The
11-22 claim had expired.

2026-11-27 PT: reviewed six more loops. Kept skate-v2 and guardian-bulwark-v2 (kind_robots#5978).
Rejected squid-v2 and turret-v2 (static), lighthouse-lamp-v3 (red flash, jitter) and salvager-v3 (morph).
19 v2/v3 retakes are still rendering (ANIM-BACKLOG-2026-11-24).

2026-11-27 PT (later): reviewed guardian clawstrike-v2, lantern-v2 and salvager-v2. All on model but
near-static (keyed motion 1.7-4.3 against 27.6 for the kept bulwark-v2), so rejected; v3 retakes with
bigger-motion prompts queued in ANIM-BACKLOG-2026-11-24. 16 earlier retakes are still rendering.

2026-11-27 PT (third pass): reviewed guardian-urchin-v2, comet-crown-v2 and halo-fin-v2 (art 280886-280888).
All on model but near-static (keyed motion 2.7-5.8 against 50.1 for the kept bulwark-v3), so rejected; v3
retakes with bigger-motion prompts queued. 18 earlier retakes are still pending or rendering.

2026-11-27 PT (fourth pass): kept guardian-salvager-v3 (art 280892, hover and tentacle curl on model, motion 60.3),
shipped as an idle atlas in kind_robots#5993. Rejected petal-wing-v2 and guardian-lantern-v3 (near-static, 6.6 and
7.7) and guardian-clawstrike-v3 (claw smear, cannon colour flicker). Final retakes queued: petal-wing-v3,
clawstrike-v4, lantern-v4. 16 earlier retakes are still pending or rendering.

2026-11-27 PT (fifth pass): kept halo-fin-v3 (art 280895, the saucer bobs and rocks, motion 74.7), shipped as the
first ship idle atlas (ships/halo-fin) in kind_robots#5994. Rejected prism-lance-v2 (near-static, 3.8),
guardian-urchin-v3 (spikes dissolve into a scribble on a mid-loop leap) and comet-crown-v3 (wings morph into
another jet). Retakes queued: prism-lance-v3, urchin-v4, comet-crown-v4. 16 earlier retakes still pending.

2026-11-27 PT (sixth pass): reviewed b07-phase1-v2, petal-wing-v3 and guardian-clawstrike-v4 (art 280915-280917).
Rejected all three: b07-phase1 and clawstrike near-static (keyed motion 0.86 and 0.96), petal-wing tumbles off
model (28.4). Petal-wing and guardian-clawstrike stay stills per the three-take rule; b07-phase1-v3 retake
queued. 15 earlier retakes still pending or rendering.

2026-11-27 PT (seventh pass): reviewed the final takes guardian-lantern-v4, prism-lance-v3 and guardian-urchin-v4
(art 280918-280920). Rejected all three: lantern and urchin near-static (foreground change 0.73 and 1.89 against
32.9 for the kept halo-fin-v3), prism-lance barely hovers and its tail fins swap shape and smear between cells.
All three stay stills per the three-take rule; no retakes queued. 14 retakes (incl. comet-crown-v4,
b07-phase1-v3) still pending or rendering.

2026-11-27 PT (eighth pass): reviewed comet-crown-v4 and b07-phase1-v3 (art 280921-280922). Rejected both:
comet-crown's swept wings fold away and regrow (silhouette height 146-501 px), so it stays a still per the
three-take rule; the b07-phase1 serpent now moves (67.9) but slides as a whole, its neck curve fills in and the
belly fins smear. Final retake b07-phase1-v4 queued (coil pinned, head and jaw only). 12 retakes still pending.

2026-11-27 PT (ninth pass): reviewed b07-phase2/3-v2, b09-phase1/2/3-v2, motherdrone-v2 and pistol-v2 (art
280923-280929). Kept motherdrone-v2 (nose tilts, thruster flares, on model, motion 51.2), shipped as an idle
atlas in kind_robots#5996. Rejected the five boss loops (on model but near-static, 5.6-7.6, only glows and
sparks move) and pistol-v2 (holds size now but static, 3.7). Queued bigger-motion v3 retakes for the five boss
phases and a final pistol-v3. 6 earlier retakes still pending or rendering.

2026-11-27 PT (tenth pass): reviewed the final takes b04-phase3-v3, guardian-kelp-warden-v3 and b07-phase1-v4
(art 280930-280932). Rejected all three: kelp-warden and b07-phase1 near-static (motion.py 0.90 and 0.86 against
19.98 for the shipped salvager atlas); b04-phase3 pops from a crouched first cell and smears its tail fluke. All
three stay stills per the three-take rule. 9 retakes (b01-p3, b03-p1, b08-p1, b07-p2/3, b09-p1/2/3, pistol v3)
still pending or rendering.

2026-11-27 PT (eleventh pass): reviewed b07-phase2/3-v3 and b09-phase1/2/3-v3 (art 280933-280937). Kept
b07-phase2-v3 (coil swells, head nods, jaw parts, on model, motion 20.7), shipped as an idle atlas after a
despeckle and despill pass in kind_robots#6017. Rejected b07-phase3 (head smears on the jaw open), b09-phase1
(cell 0 pops 27 px), and b09-phase2/3 (tail changes shape, green matte streak at the tail). These were second
rendered takes, so final v4 retakes are queued. Still pending: b01-p3, b03-p1, b08-p1 and pistol v3, plus the
four new v4s.

2026-11-28 PT (twelfth pass): kept b01-phase3-v3 (art 280948, jaws snap and the head rears, on model, motion
8.3), shipped as an idle atlas in kind_robots#6025. Rejected the final takes pistol-v3 (near-static, 1.85) and
b07-phase3-v4 (green matte through the open jaw, teeth lost); both stay stills per the three-take rule.
Still rendering, all final takes: b03-p1-v3, b08-p1-v3, b09-p1/2/3-v4.

2026-11-28 PT: done. Every ANIM-BACKLOG-2026-11-24 subject has a review verdict (177: 53 keep, 120 reject).
Final loops shipped this session: b01-phase3 (#6025), b09-phase2/3 (#6031), b08-phase1 (#6037); 46 idle atlases,
living cards for all eight Acts, pilot poses and cut-ins and moving endings are on main. 29 subjects keep
reviewed stills (READINESS-DOSSIER-2026-11-28.md section 1); squid and turret had one valid take each and stay
stills per Silas's 2026-11-28 PT note that nothing more in the queue was worth waiting for.
<!-- note:end t-030 -->

## t-042 — Rainbow Bullet Hell Space Princess — Master Roadmap to Verified Playtest Readiness

<!-- note:begin t-042 -->
FROM GITHUB ISSUE silasfelinus/kind_robots#4146 (https://github.com/silasfelinus/kind_robots/issues/4146). Master coordination task, not a second campaign specification. Keep the issue open through verified finite playtest readiness; reference it with Refs, not Closes. CONTROL.md's 2026-11-15 handoff rule and 2026-11-19 local-only co-op decision supersede older issue language.

Remaining scope: reconcile t-044 main-game standard, t-012 narrative/comms/audio, t-013 full local 1–4-player fairness/device QA, t-022 painted planes/retakes, and t-030 animation. Review the live art ledgers before submitting anything; P-03 all six ending clips shipped per recorded #5904, P-01 batch 14 reports ~29 pending loops and bulwark-v3/eel-v3 retakes. Keep rejected third attempts as stills only where accepted by the existing quality contract; never imply animation or visual verification from a ledger alone. Verify the latest evidence, attach accepted media and close each finite task only when its own scope passes. t-014 is the agent-owned readiness handoff; human feedback and publication are subsequent decisions. Refer to ROADMAP-OVERVIEW.md and the master issue for acceptance; earlier exact task note is in ROADMAP-HISTORY-2026-11-26.md#t-042. Existing T042-HISTORY.md remains intact.

2026-11-27 P-01 idle batch 6: bulwark-v3 kept and shipped (kind_robots#5928); brood and eel stay stills after three takes; harbinger, coral-choir-pod and lighthouse-lamp v3 retakes queued in ANIM-BACKLOG. Master task stays ready for the next review batch.
2026-11-27 PT P-01 idle batch 12: kept mirror-v2 (3.71) and coral-choir-pod-v3 (8.46), shipped in kind_robots#5955; harbinger stays a still after a third static take; salvager-v2 static (0.73), v3 retake queued. ~25 loops plus lighthouse-lamp-v3 pending.

2026-11-28 PT: done. Reconciled in READINESS-DOSSIER-2026-11-28.md: t-044, t-012, t-013, t-022 and t-030 done
with receipts, no queued mandatory render, no open Rainbow PR.
<!-- note:end t-042 -->
