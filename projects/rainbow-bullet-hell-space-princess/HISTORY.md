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
