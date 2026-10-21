# emperor-of-dust — task history archive

Full `note:` prose for completed emperor-of-dust tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-002 — Build admin-only illustrative region map with tutorial and project placement

<!-- note:begin t-002 -->
Create /admin/emperor-of-dust, discoverable requiredRole ADMIN tab, visual map, selectable regions and explicit not-playable labeling. Keep public Play and generic Arcade listings gated.

Private admin preview and requiredRole ADMIN tutorial are implemented in Kind Robots PR #3577, merged at 3e5e8fa0ebd77d5e7682515611b0b7a4bd2989e0 after all 30 workflow runs passed. The page explicitly says it is a concept, not playable. Conductor companion #6027 was previously merged with the game bible and 100-day outline. Deployment, actual gameplay and public /play release were not performed.
<!-- note:end t-002 -->

## t-003 — Build deterministic timed dispatch schema, leader/Horde allocation and resolver

<!-- note:begin t-003 -->
Proposed Kind Robots pure TypeScript dispatch engine, serializable schemas, seeded 2d6 odds, Horde troop reservations, travel and full return ETAs, authored moral outcomes, recoverable injury days and deterministic tests. Implementation branch worker/emperor-of-dust-t003-dispatch-20261012-c8f2.

Implemented the pure, deterministic in-game clock and dispatch foundation in Kind Robots PR #3600, merged at 689bf59e7fc839d26983c8f6a17a16f742f80eeb. Verified all 28 GitHub Actions workflows completed successfully on head 264251c0dcf29956053730e90b477be8b6408d1a, including Emperor of Dust Dispatch Contract, Contract Tests and TypeScript Type Check. Supports Horde troop reservations, 1-5h outward travel plus return, up to 3 unique leaders, chance odds, independent moral effects and multi-day injury downtime. No public Play route or live deploy.
<!-- note:end t-003 -->

## t-004 — Implement recruitable followers, multi-day injuries, rare death and saved campaigns

<!-- note:begin t-004 -->
Implemented first ten candidate leaders (five starters), gated Prosperity-funded recruiting, next-day arrivals, persistent injury recovery, story-flag-gated rare fatality memorials, defensive save validation, local Pinia storage and targeted contract tests in branch worker/emperor-of-dust-t004-saves-b83 of kind_robots. Gameplay/UI integration and ninety further authored followers remain.

First ten follower profiles and five starter leaders, gated Prosperity recruitment, one-day arrival, multi-day wound unavailability, explicitly authored and forewarned fatality memorials, defensive versioned local campaign saves and Pinia orchestration. Kind Robots PR #3603 merged as 32e4172007f4daf1bdfeb219611f509b1f01351c after all 29 exact-head GitHub Actions workflows passed. No images rendered, public Play changes, migrations or live deployment. Next: t-015 private map clock.
<!-- note:end t-004 -->

## t-005 — Script Act I, Days 01–10, as fortress days (briefing, audiences, quests)

<!-- note:begin t-005 -->
Rescoped 2026-10-18 for SYSTEMS-V03.md. Days 1-4 exist in kind_robots utils/emperorOfDust/day*.ts in the v0.2 Horde/hour format: convert them to throne-room audiences plus 1-3 day quests rather than discarding the writing. Follow DAY-PLAN.md anchors and its [A]/[Q]/[K]/[M] marks.
Merged kind_robots#3849 as b615b93355a8e7bac590b4905f1901f1b109b3db after all 20 checks passed on head 55569309739ede99a84953fd2b637594a4757c41. Act I Days 1-10 scripted: Vane's toll (grudge variant), the empty stable (each starter reveals a secret), the Crow warning with Komodo's first own lie (komodoLie), the Coldbrook family and the Abbey's offer, the first lethal convoy, the Gate Watch oath and the Thistledown raid moving faction strength. Wages 4->6 after a 200-run simulation (avg brass 380 -> ~290 at Day 10 before spending; ~2 injuries, 0.05 deaths per Act I run). Chromium check at 390/768/1440.
<!-- note:end t-005 -->

## t-006 — Script Act II (Days 11–20) and Act III (Days 21–30) with the Rustline and Black Verge reveals

<!-- note:begin t-006 -->
Merged kind_robots#3851 as 9f3f2852bf18d8794d882af06cfa0eab19e67d08 after all checks passed on head a3b270e6f72c179bbf7f736b4cec61a954e77752. Acts II (Rain Debt) and III (Kind Roads), Days 11-30: rain covenant and its debt, Mirefen cellars, Saffron's water engine (mustInclude quest), Brass Hourglass (Day 14) and Eye of the Elder Crow (Day 17) story routes, Abbess at court, Coldbrook callback, Flint's trial, Mara's page, Black Verge envoy and Sable, Keel's truce. Recruitment routes for Ash, Pell, Isolde, Vesper, Hollin, Keel and Sable. Komodo's own lies on Days 7/17/25/29. Engine: dawn-fixed court, mustInclude, Codex absorbs flag-revealed allegiances. 200-run sim Days 1-20: ~25 brass/~10 followers for a hire-everything player, 0.05 deaths, ~4 injuries per run.
<!-- note:end t-006 -->

## t-008 — Script Act V hideout (Days 41–50) and the eight ending families

<!-- note:begin t-008 -->
Hideout variants per SYSTEMS-V03.md (Mole tunnels, Crow cave, Bell cellars, Jackalwire wagons, caravan, Freehold barn, Rustline station, fallback cave), each changing Act V quests, market and ending options.
Act V (Days 41-50) and the eight ending families shipped in kind_robots#3869: hideout flag on betrayal, eight Day 42 host audiences and quests, Keeper Vellum's briefings, Day 49 peace choice, Day 50 last dispatch (front door, well road, bell tower), endings.ts and the end screen naming every lost follower. Left for t-028: hideout income and departing followers; for t-024: a hideout market. Sims (200 varied runs) reached 7 of 8 endings and 3 of 8 hideouts; balance goes to t-009.
<!-- note:end t-008 -->

## t-009 — Verify eight-image follower set, NPC moods, full 50-day balance and responsive QA

<!-- note:begin t-009 -->
Verified 2026-10-20 in kind_robots#3874. A seeded 13-policy harness (fortress/balance.ts; BALANCE-REPORT.md; CI test verifyEmperorFortressBalance) found the Freehold barn won the hideout in nearly every run, about 20 Ledger loans per full- barracks run, and A Hundred Candles unreachable. Fixed with cheaper, faction-spread chores, pledge-weighted hideout selection, two Rustline choices, wages 6 to 4, and two more lethal Act V expeditions with a two-death threshold. Each patron now hides with its faction in 88-100% of runs, all eight endings occur, and careful play loses the crypt 0-5% of the time. Follower moods show in the barracks and the advisor at the briefing. Responsive QA at 390, 768 and 1440 from Day 1 to the ending with real saves found no errors, broken art or horizontal scroll.
<!-- note:end t-009 -->

## t-011 — Author 20 followers in the v0.3 schema (stats, secret traits, unique ability, allegiance, art briefs)

<!-- note:begin t-011 -->
Rescoped 2026-10-18 from 100 leaders to 20 followers (SYSTEMS-V03.md). Re-express F001-F010 from FOLLOWERS-PILOT-01.md and author F011-F020: five 0-10 stats, 1-2 secret skills and weaknesses with reveal triggers, one unique ability, per-faction modifiers, origin vs true allegiance, romanceable flag (about 6), recruitment route, and a design sheet brief for the eight images. Two editorial batches of ten.
FOLLOWERS-V03.md authors all twenty in the v0.3 schema with eight-image art briefs; F011-F020 runtime records, ten new ability mechanics and seven Act I recruitment routes in kind_robots#3850 (pending CI).
Merged kind_robots#3850 as 0b388265360be35b9b07a230a1ff2f2da694304a after all checks passed on head 36bbfd4d1c52e3ac18f0dbbfed949f5a62a1b092. Twenty followers live: F011-F020 with ten new distinct abilities (Cave-Luck with honest two-roll odds, Confessor, Last Wall, Salvage Rights, Heeded Omens, Immaculate Apology, Thick Hide, Encore, Old Maps, Second Helpings), six romanceable, seven Act I recruitment routes. Each ability verified by the contract test.
<!-- note:end t-011 -->

## t-012 — Deliver eight images per follower (five illustrated moods, three portrait states) and NPC moods

<!-- note:begin t-012 -->
Rescoped 2026-10-18: 160 follower assets (illustrated neutral, happy, excited, sad, angry; portrait neutral, injured, dead as a memorial treatment) plus five moods for each of ~12-16 major NPCs and Komodo's betrayal image, via durable ArtJobs and a manifest. Batch in fives from a locked design sheet. Do not claim queued art delivered. 2026-10-19: Silas reviewed the cast before art: no two named characters share a species, F003 is now Kiyo (koala, Zuzu's mother), F007 Ash is a fennec, and six design sheets changed (FOLLOWERS-V03.md "2026-10-19 swaps"; NPCS-V03.md). Maps are Silas's, drawn with ChatGPT from MAP-LAYOUT.md. Every faction now has a named NPC (17 in all, counting the new Hester, Jinx and Keeper Vellum), so the count is 160 follower images, 17 x 5 NPC moods and Komodo's betrayal: 246. Silas approved the art the same day. Ledgers: art/CAST-ROUND-1.yaml (keepers) and art/CAST-ROUND-2.yaml (img2img moods and states; `approved` lists what was exported). kind_robots#3866 exports 232 of 246; 14 rejected on review are rerolling as -v3 subjects. Close once those are approved and exported.
Delivered 246/246 on 2026-10-19: kind_robots#3866 (232) and #3868 (the last 14 v3 rerolls). castArt.ts lists all 246 and the contract asserts the count; NPC reactions in the throne room and Komodo's betrayal at the Day 41 dawn use the moods.
<!-- note:end t-012 -->

## t-013 — Write all 50 three-report briefings with Young Komodo clues and his own seeded lies

<!-- note:begin t-013 -->
Rescoped 2026-10-18 to 50 days; some false reports are Komodo's own lies, readable in hindsight after the Day 40 betrayal (DAY-PLAN.md [K] days). Every scripted day: two true and one false intelligence snippets; author-known metadata, rotating lie position and conditional variants. Allow early lies to be erroneous flavor without unfair punishment. Eye of the Elder Crow highlights the false report when equipped.
Merged kind_robots#3929 as 001b8b0ffd3ca3771f723d9f92e59bde4431b32a (21/21 checks). Conditional briefing variants (Briefing.variants, briefings.ts; 35 variants on 18 days keyed on earlier-day flags; truth never varies so the Eye still marks one lie), lie slots rotated (14/20/16), Day 38 made Komodo's own lie (8 total), hindsight lines and a post-betrayal 'His own reports, read again' list in the briefing. Contract: rotation, [K] days carry Komodo lies, variant determinism across audience/reload/rewind, Eye marks exactly one. Chromium 1440/390.
<!-- note:end t-013 -->

## t-014 — Implement persistent Items of Power with one or two run slots

<!-- note:begin t-014 -->
Story-gated, meta-persistent rewards with scripted acquisition windows, no unearned initial Eye. Test loadouts and save migration.

Private Items of Power system developed on Kind Robots branch worker/emperor-of-dust-t014-relics-20261013-9af2: story-gated persistent relic vault, one/two next-run loadout slots, Eye highlights false reports, and once-per-day Brass Hourglass reduces only outbound travel. Backward- compatible saved campaigns and Admin collection UI with placeholders. Unlocks are gated for later authored days, not automatically distributed in the Day 1 prototype. Pending exact-head GitHub CI review and merge.

October12 PT at10:42PM: completed the private Items of Power system in kind_robots#3617 merged6de8caf2c585a710f79fc3176203c511514e2e58 after all33 actual checks completed successfully on9481dfafd3bf35cc5a56174d50a1ea57e1003d5f. Full nine-file diff/current reviews/threads inspected; expected-head merge with required checks/approvals satisfied and no bypass. Validated persistent vault, one/two next-run slots, story/day-gated ownership, Eye false-report reveal, once-daily outbound-only Hourglass and backward-compatible save fields. Independent relic/dispatch/campaign/map tests pass; actual compiled component with real Pinia/store and fixture storage fits390/768/1440 without errors. Artwork is explicitly placeholders; no final art delivery asserted. Current Day1 pilot cannot earn later story flags: t-005/t-013 still own authored days and discovery integration. This finishes system plumbing, not the100-day game or a completed daily playable content addition. No deploy/public release.
<!-- note:end t-014 -->

## t-015 — Build pausable day clock and mostly radial tower travel routes

<!-- note:begin t-015 -->
Top-center Emperor's Tower, mostly straight routes, 1-5h one-way distances plus mission and return, visible ETA and troop reservation. Follower available only after return or authored local-stationing.

Private Day 1 playable map branch worker/emperor-of-dust-t015-admin-map-20261012-k2n: top-center Emperor's Tower and radial roads, outbound time and return times, three authored incidents, Young Komodo's three-report briefing, actual Horde and leader selection, truthful odds, ticking deadlines, in-flight expeditions, injury/roster state, persisted pilot run, plus contract tests. Not a completed 100-day campaign or public Play publication.

Implemented the private Admin-only playable Day 1 vertical slice in Kind Robots PR #3615, squash-merged as 883a72dbbf3f163730ab0d25bceb2e7d83404f25. Verified all 32 GitHub Actions workflows completed successfully for exact head 0d0e5c42b3a4b7c2297f85759003a40ee24bf97d, including TypeScript, layout, component reachability, Emperor dispatch and shared Contract Tests. Added top-center Emperor's Tower and six mostly radial one-to-five-hour roads, three authored Day 1 incidents and Young Komodo briefing, active leader and numeric Horde selection, moral approaches and displayed odds, pause-and-advance clock, authored missed-deadline consequences, expedition travel/return, recovery state, browser-local saved run and a private character gallery with explicitly unrendered portrait placeholders. Later days support only recovery testing, not claimed as scripted. No public /play publication, image generation, deployment, schema migration or production mutation.
<!-- note:end t-015 -->

## t-016 — Develop Mole Revolutionary faction, anti-witch choices and the Mole tunnel hideout

<!-- note:begin t-016 -->
Eighth faction, opposes empire and swamp witches, with meaningful reconciliation arc, named leaders, authored tension effects and Day 50 ending variants; maintain pre-Zuzu continuity.
Merged kind_robots#3937 as 8b383514b216ca319aec5d44d666a7ff7b87de00 (19/19 checks). moles.ts: leaders Umber, Keel, Lumen plus Coal Harrow (hardline sapper captain) and Tobin Umber (courier); a reconciliation track of 23 concession and 9 grievance flags with moleAccord(); generic Requirement.standing / EpilogueCondition.standing (at least N of these flags). Five new audiences (Day 21 weir vs the Mothers, Day 32 reform list that finally makes F010 Lumen recruitable, Day 33 sappers in the fen, Day 44 two kegs in the tunnels, Day 50 the burrows turn out) and Mole epilogue variants. Balance unchanged; patron:moles 10/10 tunnels and Tunnels and Councils. Coal and Tobin have no portrait art yet.
<!-- note:end t-016 -->

## t-017 — Build the barracks: follower grid, illustrated view, Talk scenes and capacity upgrades

<!-- note:begin t-017 -->
Rescoped 2026-10-18 from the art-first roster gallery. Portrait grid by state (ready, on quest, injured, dead memorial row), full illustrated view with stat wheel, equipment, known traits, unique ability and faction modifiers, limited daily Talk conversations, 6 beds upgradeable to 9 and 12. Only use delivered images, with fallbacks. Keep the /play gate closed.
Merged kind_robots#3920 as 9bbd2574bfae23eb8cc1b7ed50fb648bd0ad8d21 after all 21 checks passed on head 57214f9fd2a98097d7f9a60522baef19f41104aa. Barracks Talk scenes: one conversation a day with a ready or injured follower, played as a branching scene (TalkDef, talkFor/talkScene/chooseTalkOption; heard:<id> and talk:<id>:<opt> flags; an open talk closes heard at dawn; saves validate talksHeard/talkDay/talkOpen). Roster dot for followers with something to say, Sit-with button (heart for romance steps), story- gated answers hidden. 63 talks across all 20 followers in stark prose, fortress talks close at the Day 41 betrayal and seven Act V talks open in the hideout; ~40 callbacks to throne-room flags; talk-teodor-letters, talk-isolde-coven and talk-sable-flight now revealable. Chromium 1440/390 from an injected Day 2 save: Rook's talk, beat and close, no page errors or horizontal scroll. Remaining scope not built: barracks capacity is still the existing 6/9/12 bed purchase; no stat wheel. F010 Lumen still has no recruitment route, so her talks wait.
<!-- note:end t-017 -->

## t-018 — Verify relic vault through actual Pinia restart and storage-failure boundaries.

<!-- note:begin t-018 -->
Reviewer kaizen after kind_robots#3617, targeting LEARNING-REPORT's recurring quality/consumer-boundary pattern. Existing pure vault and campaign codecs pass; add a fixture through the actual store for loaded ownership, next-loadout changes, beginNewRun and reload. Test full storage, malformed vaults and throwing localStorage access without clobbering unreadable data. The isolated render used explicitly in-memory storage; it is not this persistence proof. Existing load() tests typeof localStorage before its try block, which can throw on denied-access documents; reproduce and repair that boundary without disabling warnings or granting permissions. Keep t-005/t-013's later authored discovery branches independent and preserve private ADMIN scope; no account creation or production mutation.
Shipped in kind_robots#3934 (5ce02a7f). verifyEmperorFortressStore.test.ts runs the real Pinia store in Node with a fake localStorage that can quota-fail or throw (wired into the Emperor contract workflow). It reproduced and fixed six persistence bugs: a good autosave cleared the vault-unreadable warning; an unreadable autosave was overwritten by the next order; an unreadable Codex was overwritten by the next reveal; a throwing getItem read as empty; unreadable slots showed as Empty and could be overwritten (Chronicle now shows Unreadable with Clear); a refused Codex write was lost (now retried). The typeof localStorage boundary was already safe via storage().
<!-- note:end t-018 -->

## t-019 — Rebuild the engine for v0.3: remove Horde and hours, day-based quests, brass, factions

<!-- note:begin t-019 -->
Kind Robots utils/emperorOfDust + stores/emperorOfDustStore.ts. Remove all Horde, troop and hour/travel state; add Day/Act, quests with 1-3 day duration, 1-4 slots, expiry with consequences, five-stat bands with hidden requirements, lethal markers, seeded deterministic resolution, brass (taxes, wages, debt), 5 local supports and 10 kingdom affinities with strength, follower state (ready, on quest, injured, dead) and a new save version that discards v0.2 pilot saves with a notice. Keep relic vault and injury/death rules. Contract tests per SYSTEMS-V03.md acceptance.
Engine, store, Days 1-4 conversion, F001-F010 in the v0.3 schema and rewindable saves in kind_robots#3846. Built alongside the v0.2 pilot; t-020 swaps the /play UI over and retires the v0.2 modules.
Merged kind_robots#3846 as c2e120f03b4249cc86173bc176ea669d66d92624 after all 19 checks passed on head 784210258d64a166dc5d4efb1ae3b04bba968e56 (TypeScript, Seeded dispatch and recovery contract, contract shards, layout-contract, Changed-file Prettier). Local full vue-tsc also clean. The /play page still runs the v0.2 pilot until t-020; F011-F020 remain t-011; Days 5-50 remain t-005..t-008.
<!-- note:end t-019 -->

## t-020 — Build the Fortress shell: five rooms, HUD strip, Finish and animated day/night/dawn report

<!-- note:begin t-020 -->
Replace the map-first admin preview with a Fortress view: throne room, quest room, barracks, market, map room; top HUD (day, act, five local meters, brass); Finish with warnings that never block; day/night animation and dawn report cards. Phone: one room per screen with bottom room bar.
Merged kind_robots#3847 as 3de0acf35e342c712fd5ff80ed435ba07b300101 after all 22 checks passed on head 1f4ede3d864ba227c5188f1861865f5cbc745b0f (one push fixed a workflow-paths glob). /play/emperor-of-dust now runs the v0.3 fortress: HUD, throne room with streamed dialogue, quest room with live odds, barracks, market, map room, Chronicle (3 slots, rewind, relics), Finish and animated dawn report; v0.2 Horde/hour code retired. Verified in Chromium at 390/768/1440 with the real page/store/engine (only achievements stubbed): Day 1-3 loop, rewind, slot save, autosave reload, corrupt autosave preserved, no page errors or horizontal scroll. Basic rooms only: t-017 (Talk scenes), t-021 (seeded petitions, NPC art), t-022, t-024 (rotating stock), t-025 (act-end UI) keep their deeper scope. No portrait art yet.
<!-- note:end t-020 -->

## t-021 — Throne room audiences with gated solutions and the art-led dialogue box with streamed text

<!-- note:begin t-021 -->
Audience records (authored, consequence-driven and seeded minor petitions); options gated by brass, local support, affinity tier, follower or flag, shown locked with requirement. Dialogue box with nameplate, 2-4 choices, log, typewriter stream with tap-to-complete and a persisted speed setting (normal, fast, instant).
Merged kind_robots#3914 as 815fa731b4eff46cd1ab37ce2b65e0eb22cc43ab after all 21 checks passed on head b79ea712689bb78c7de2eb81d2ce839b33ee4717. Silas 2026-10-20 PT asked for a verbose visual-novel style with frequent morally testing choices. Audiences are now branching scenes: options with next lead into beats (AudienceBeat), lines can be handed to other speakers ({who, npc, text}) with nameplate and portrait, story-gated answers (flags, absent followers) are hidden rather than shown locked, mid-scene state saves and closes at dawn. All 50 days rewritten (98 audiences, 88 scenes, 139 beats, 956 answers, ~56k words, ~100 callback answers and a dozen callback audiences reading earlier flags; Komodo tells on lie days; Day 40 quiet word three beats deep with five evidence routes). Original ids/effects/quests preserved; balance test and 40-seed report hold (8/8 endings; rustline patron 33/40; freeholds loans 4.1/run). Chromium at 1440 and 390 on a local dev server: no page errors or horizontal scroll. Writing contract: projects/emperor-of-dust/SCENE-WRITING-GUIDE.md.
<!-- note:end t-021 -->

## t-022 — Quest room board: assignment slots, requirement bands, preview odds and expiry

<!-- note:begin t-022 -->
Merged kind_robots#3940 as c94cf4e003152df8466d5b7a7e4b26f5af3dbb66 (22/22 checks). Notices show requirement bands, Lethal and a countdown; the quest card states reward, the expiry consequence, danger with wound range, per-stat party total vs need (hidden as ?), never fogged factions or hidden strength. previewQuest adds injuryRisk, injuryDays and deathChance from the night-roll tables (matched against 400 seeds). Party slots, per-follower contribution, a What-counts list, non-blocking warnings beside Send, Call back restores the notice; Lamplight support 20 reveals every ? (LAMPLIGHT_SIGHT). Chromium 1440/390.
<!-- note:end t-022 -->

## t-023 — Follower secret traits, unique abilities, faction modifiers, hidden allegiance and the persistent Codex

<!-- note:begin t-023 -->
Reveal on first relevance, persist revealed traits and allegiance in a meta-save Codex across runs (never items, brass or relationships), apply hidden modifiers silently until revealed.
Shipped in kind_robots#3940 (c94cf4e0). codex.ts (trait index, allegiancesKnown, howLearned, codexPages, revealLine); decode/merge keep only follower trait ids (never items, brass or relationships); quest rewards that set an allegiance flag reveal it at dawn; allegiances absorbed on load; reveal moments (EmperorFortressCodexNote) in barracks and throne room; Chronicle Codex section, one page per follower, N of 46 secrets with how each was learned; all six talk allegiance flags reach the Codex; writes go through the saves worker's persistCodex guard. Not built: keyword highlights in quest text and the remaining ? reveal sources (follower secret skills, market maps, Komodo's hint).
<!-- note:end t-023 -->

## t-024 — Market with rotating per-run equipment (two slots), healing and barracks upgrades

<!-- note:begin t-024 -->
Merged kind_robots#3936 as dce5fb303eb9669ed73d48b3aaed7e2b45f1285c (21/21 checks). items.ts: 30 items (7 original + 23), stat bonuses, party powers and faction/tag edges, some with faction reactions on purchase (Mire charms cost the Abbey, Rustline relics cost Lamplight, the stolen clapper costs Hollow Bell). market.ts: seeded stock turning over three times an act (days 1-3, 4-6, 7-10), gated by banners on the map, wipe-outs, affinity tiers and local support, rerolled on a rewind branch, once per window per item, Act V peddler favours the host; Sell at half price; Treatments (surgeon 8 + 2/day, Saltroad discount; seeded Mire poultice 50/30/20, Abbey -1) once per follower per day; carpenters (beds) in the market. Market tabs Buy/Sell/Equipment/Treatments/All; run.market optional and validated. Chromium 1440/390 on Day 12. Item icons queued as ArtJobs 42323-42352 (art/ITEMS-ROUND-1.yaml); export keepers to public/emperor-of- dust/items/<id>.webp and list them in ITEM_ART. Balance bots do not shop (a shopping policy would be a follow-up).
<!-- note:end t-024 -->

## t-025 — Map room: territories, taxes, affinity tiers, act-end map events and telegraphed faction wipe-outs

<!-- note:begin t-025 -->
Days 10/20/30/40 events; Rustline revealed end of Act I, Black Verge end of Act II; wipe-outs only at act ends and warned one act ahead.
Merged kind_robots#3938 as 5ecc5218afd0393eb5feaae0002f33f4d7cf1beb (21/21 checks). Act- end map: wipe-outs and raids only at act-end dawns and only after an honest warning one act ahead (banner on map, strength <= 2, weakenable), rivalries (RIVALRIES) move territory (run.controllers), wiped factions' quests close; tier taxes (Wary/Hostile 0, Allied +50% tithe) with regionTax matching the map room; act-end dawn opens on a map page of stark event cards; map room warnings panel, threatened pins, region cards, What changed history; briefing map-room line; ledger taxes/wages. Freeholds-patron loans fell 4.1 -> 1.9. Follow-ups for content: allegiance shifts and refugee audiences after a wipe-out.
<!-- note:end t-025 -->

## t-026 — Romance arcs for about six followers, never Young Komodo

<!-- note:begin t-026 -->
Shipped in kind_robots#3920 (9bbd2574). Six romance arcs, never Young Komodo: Rook (rook-2, rook-3), Saffron, Nera, Ash, Sable and Vesper (three steps each, romance: true), final steps Days 27-38. Accepting sets romance-<name>, the last step romance-<name>-sealed; every step can be declined kindly (<name>-friendship, clears the arc). Only one romance can be sealed (courting() notFlags on rivals' sealed flags); three final steps are written jealousy dilemmas, shown only while the rival is alive and at court. Romance costs: a pass that bends Watch law, a lethal walk into the Abbey, the Verge offering war help for Sable, Rook's scout facing the gallows (rook-heartbroken).
<!-- note:end t-026 -->

## t-028 — Young Komodo betrayal track and Act V hideout selection engine

<!-- note:begin t-028 -->
Betrayal always fires on Day 40; buyer, departing followers and hideout location depend on state; fallback revolutionary cave guarantees no softlock.
Unblocked 2026-10-20 by t-025 (kind_robots#3938). Audit in that PR's worker report: betrayal always fires (Day 41 dawn), selectHideout + nameless-cave fallback and Act V host gating exist and are tested. Missing: (1) the buyer is always the Abbey, never chosen from state; (2) no followers depart with Komodo (no loyalty/hidden-allegiance departure, romance or finished arc protection); (3) hideout income is not modelled (Act V still collects regional taxes instead of the host's share).
Merged kind_robots#3947 as 2ffecc397286c249586378c9ce6ebb84a6b45d1b (22/22 checks). betrayal.ts: the buyer is chosen from state (buyer:<id>): the Abbey by default; the Black Verge when it stands stronger than the Abbey and the crown slighted it 3+ times or is Hostile; House Vask when Old Houses support <= 3; Verge outranks Vask; the Abbess is always the patron. SceneVariant swaps only the lines naming the tower's holder (Days 41/42/43/45/49). Departures: hidden allegiance to the buyer, or 10+ days unvisited while their own people were crossed; never estranged followers, sealed romances, finished arcs or followers away on quests; max 3 leave, min 4 stay; departed followers are alive but gone (talks, quests, wages stop; kit returns), shown on a Day 41 betrayal page and a Gone with Komodo barracks row with one-line reasons, plus a departed epilogue variant for all 20 followers. Hideout income: no region pays from Day 41; the host shares strength x3/x2/x1 by tier (cave 3) and wages are halved (HIDEOUT_WAGE, a design call Silas may overrule). Saves validated; old post-Day-41 saves read the Abbey. Balance ok; Chromium 1440/390.
<!-- note:end t-028 -->

## t-029 — Art-direction pass: bring the fortress front end to the painted drafts

<!-- note:begin t-029 -->
Silas, 2026-10-19 PT, with the painted drafts attached: "I want us to work on the discrepancy between our current front end and the idealized drafts." Gap table: FRONTEND-GAP.md. Shipped: kind_robots#3873 (merged b17d945473e3e4ff5c54c97824f215540022c44b, 21/21 checks) gave the fortress a scoped ink-and-gilt `emperor` theme, the crest HUD with meter chips, gilt room tabs, room stages with medallion/plate/tagline, and art-led throne (petitioner in scene + petition card), quest board (pinned notices, party slots), barracks (roster, follower in scene, stat pips, trait chips), market (filter, price pills) and chronicle (dawn list, parchment rewind card); kind_robots#3876 (merged 47632f50d97e0db8f19d945f923ed3fb46e275b7, 20/20 checks) added map-room stance banners and the legend. Silas then asked for full width and a prioritized intro: kind_robots#3879 (merged 6c16b343a9a0d0e5c311a72f4eb03cc9487f111b, 20/20 checks) removed the max-width cap, added an animated splash over the painted map on every visit, and a six-scene Komodo-narrated introduction for players without a save (replayable from the Chronicle). Silas's next notes (2026-10-19 PT): Finish beside Send, hidden until every petition is heard, dimmed with idle healthy followers, a confirm when nobody was sent; one header row with a court-ledger toggle and tooltips; an image for every quest and illustrated dawn outcomes; then the Briefing as its own first room, with the two-truths rule left for players to discover (a Day 3 whisper hints at it). kind_robots#3885 merged 451916d0d27c5dd649863dd41ea4eb4a7496d48f (21/21 checks). Quest art: 231 ArtJobs (notice, success, failure per quest, art/QUESTS-ROUND-1.yaml), queued 2026-10-20T04:3xZ; the map-crop fallback shows until they are exported into QUEST_ART. Verified in Chromium at 1440 and 390 with a full Day 1 loop, no page errors or horizontal scroll. Remaining: the six room backdrops (ArtJobs 40949-40960, art/ROOMS-ROUND-1.yaml) were still PENDING at the render relay on 2026-10-20T01:30Z; queued is not delivered. Still PENDING at the 2026-10-20T03:57Z check-in, behind a slow relay backlog (job 40961 was RUNNING then while 40940, queued 23:51Z, still waited), so no more check-ins were armed. When they render: pick keepers, export to public/emperor-of-dust/rooms and list them in ROOM_ART, then close. Item and quest-notice art are follow-ups. Visual acceptance stays t-010.
2026-10-20 PT: all 12 room renders and 231 quest renders were DONE. kind_robots#3915 merged as 787757b3068e791e0313d5550d0affe71c5b6279 (18/18 checks): six painted room backdrops (keepers throne a, quests b, barracks a, market a, map b, chronicle a; briefing keeps its gradient) in ROOM_ART, and 228 of 231 quest images in QUEST_ART. Ledgers in conductor#6405 (3e7f6dee). Rejected and rerolling, not yet delivered: barracks backdrop v2 (ArtJobs 42158, 42159; seed a ships with two small background figures) and q-d42-cave-forage notice/success/failure (42160-42162; crow-roost tags overpowered the cave). Those fall back to the map crop until exported; pick up with enqueue_art_requests.py --status on ROOMS-ROUND-1/QUESTS-ROUND-1. Visual acceptance stays t-010.
<!-- note:end t-029 -->

## t-030 — Afterwards: a consequences epilogue after Day 50 that remembers what the emperor did

<!-- note:begin t-030 -->
GAME-BIBLE promises "an ending and a consequences epilogue"; the end screen only showed the ending family and the names of the dead. epilogue.ts holds subjects (followers, NPCs, places, Komodo) with flag/ending/alive/dead-gated variants, first match wins; EmperorFortressEpilogue.vue plays them as an art-led slideshow under the ending. Contract: every flag an epilogue reads is set somewhere (audiences, quests, talks, engine). Branch worker/emperor-of-dust-t030-epilogue in kind_robots; stark prose per SCENE-WRITING-GUIDE.md.
Merged kind_robots#3921 as 93190f58f6d1bf870ee5883b073c15129b180500 after all 22 checks passed on head c431c29ddce1fd00d12c33fdd5c1273483bf9150. epilogue.ts: 42 subjects, 307 stark-prose variants (all 20 followers, the NPCs, factions, places, the hideout and Komodo last), first matching variant told; peace-only kingdom variants keep the Long Night dark. EmperorFortressEpilogue.vue slideshow with Read all, text-only cards where a subject has no art. Contract: every flag read is settable (audiences, beats, quests, talks, engine). 13 policies x 8 seeds: 21-30 entries per run. Chromium 1440/390 with an injected finished crows-bargain campaign: no page errors or horizontal scroll. Also fixed the Day 1 informant's pronoun on Day 4 (she, as Days 16 and 42). Follow-up: t-032 save size.
<!-- note:end t-030 -->

## t-031 — Stark-prose pass over all fifty days (King / Joe Hill / Lone Wolf and Cub)

<!-- note:begin t-031 -->
Silas 2026-10-20 PT: "we want crisp stark prose. Stephen King or his son Joe Hill, lone wolf and cub". kind_robots#3919 merged as f73f0a1df0effe9d6a3d132b13fa8ccde4bf1385 (18/18 checks): 2,591 prose strings across the six act files rewritten, about 16% fewer words, every fact, clue, Komodo tell and callback kept. A structure guard proved ids, effects, requirements, beats, quests, flags and line/option counts identical to main; contract, balance and playbook tests pass. Talks (t-017/t-026) were written to the same register.
<!-- note:end t-031 -->

## t-032 — Keep a finished campaign's saves well under the browser storage quota

<!-- note:begin t-032 -->
Found 2026-10-20 while verifying t-030: a seeded full 50-day run's autosave book is about 1 MB (318 flags; every dawn snapshot repeats the full `reports` history, so size grows roughly quadratically with days). decodeBook allows 3 MB, but autosave plus three manual slots (each a whole book) can approach the ~5 MB localStorage quota. Options: store dawn snapshots without the accumulated reports (rebuild them from the current run on rewind), or delta-encode dawns. Must keep the SYSTEMS-V03 save rules: validated saves, never overwrite unreadable data, rewind to any dawn. Add a contract test bounding a full run's encoded size.
Merged kind_robots#3934 as 5ce02a7f64557d9e2d55c0393ce24a73e9430d83 (21/21 checks). v4 save format packs each dawn's accumulated lists as shared-prefix + tail; full 50-day books 680-952 KB -> 92-116 KB (~8x); v3 books/slots migrate on read; tampered packing rejected. Contract bounds a full book under 250 KB and proves packed rewinds equal full rewinds at dawns 1/2/17/33/50. Caveat: during a deploy an old-code tab would read a v4 autosave as unreadable.
<!-- note:end t-032 -->

## t-034 — Phone width: tapping a fortress room tab shifts the frame sideways

<!-- note:begin t-034 -->
Seen independently by the market (t-024) and betrayal (t-028) workers on 2026-10-20: at 390px, tapping a room tab whose tooltip appears shifts the fortress shell about 21-24px sideways inside its overflow-hidden container (every room, so the page shell, not a room). The document itself never scrolls horizontally. Reproduce in Chromium at 390x844, fix the tooltip/tab overflow in pages/play/emperor-of-dust.vue, verify at 390/768/1440.
Merged kind_robots#3953 (384e4e8): room tabs no longer slide the fortress shell sideways at phone width; verified by measuring the shell's left edge before/after tapping every tab at 390/768/1440.
<!-- note:end t-034 -->

## t-035 — Playtest rewrites, Act I (Days 1-10)

<!-- note:begin t-035 -->
Implement playtest/2026-10-21/act1.md rewrite proposals: Day 10 act-end choice with real cost and a Day 9 warning about the convoy squeeze, narration/quest agreement (Thistledown, the Day 9 Pack hire), the Day 7 storm and Komodo's first lie actionable, dominant answers (fair tax, polite flour, archive rules, blanket stalls, apology, loan) given real costs, the Day 5 toll stops repeating the dust-lung twist, continuity (informant pronoun, rain days, lantern counts), stark dawn outcomes, fewer kindness-for-brass options. Vary the probe template. Preserve ids/effects unless noted.
Merged kind_robots#3964 (squash 28928080183ca3e6f04a08ae9f13eb1da826d188, 19 checks green). Day 10 has a real cost (riding out aids Thistledown, schedules hidden Day 11 postern theft / Ledger carts / stableboy-witness lines; 'never cheaply' warned and spent if the lethal convoy fails). Narration agrees with the board (strike/tincture/mercy settle Thistledown; broken promise costs Freeholds; Pack hire relabelled as aid; Day 9 warnings). Tincture fee and loan costs collected; Day 7 storm lands on Day 10; Komodo's galleries lie testable (q-d07-galleries). Probe template varied, Komodo openers cut. Dominant answers cost someone (fair tax, polite flour, archive rules, blanket stalls, apology, loan). Day 5 new reveal (the Abbey buys the tincture). Continuity fixed; kindness-for-brass reduced; ten dawn lines made stark. Story calls in PR body. Skipped: fair-chits-face duplicate, free-apology echoes in other acts, Day 4 bell-result gating, engine-level lethality from feeding farmers. New unread flags listed in t-043 (7).
<!-- note:end t-035 -->

## t-036 — Playtest rewrites, Act II (Days 11-20)

<!-- note:begin t-036 -->
Implement playtest/2026-10-21/act2.md proposals: let the player read clause eleven (free probe; Tamsin's reading continues the scene), fix the impossible Day 20 clause-eleven gate, rain timeline and covenant-state briefing variants, Day 34/42/epilogue branches for court runners and the fixed term, a flag for buying one season, Hollow Bell's vote reading the crown's history, the Yard's double loss noticed, dead threats paid off (Vane's bolt, the Verge, the substitution, the flooded Ford villages), the Day 12 dominant option, text/effect mismatches. Fewer Komodo openers.
Merged kind_robots#3960 (squash cceccd940c20d7f2f39daa90327ba296f556c4a0, 19 checks green). Clause eleven readable (read-eleven probe, Tamsin's reading continues, amend- term honoured Day 20, d11-rain-bought); one rain clock + covenant-state briefings; settlements remembered (substitution due, Day 34/42/epilogue runner and fixed-term branches); Hollow Bell vote reads crown history; dead threats paid via dues (Vane's bolt, Verge change, Ford burrows, Bell gate, forged tokens); Day 12 dominance broken; Komodo openers cut. Silas-delegated call (2026-10-21): runner-paid covenants get Linnet at the gate on Day 34 (buy-out 60 brass / leave / Tamsin goes in her place) instead of a brass bill. Skipped: Day 14 map/Saltroad reads, d18-water-taxed epilogue line, bell- vote-tied read, ford-dam-built reservoir read, briefing pattern variety, Nera bought- rain talk. Balance: patron:rustline hideout share at threshold (0.7).
<!-- note:end t-036 -->

## t-037 — Playtest rewrites, Act III (Days 21-30): make kindness the trap again

<!-- note:begin t-037 -->
Implement playtest/2026-10-21/act3.md R1-R10: cut the Abbey's winks so one hard tell lands before Day 29, add true innocent readings (a real fever ward, children who come back), give the Abbey credible defenders (Dunmore, Kiyo, Hester) instead of Komodo, put costs on screen; remember the big Abbey choices (d30-children-to-abbey, d23-*, d26-dry-well-followed, ...); fix the Day 21 alliance options not setting pack-alliance, the Day 30 adult-shelter mismatch, the Day 29 Pip trap, the four-cots continuity slip, the repeated parent-at-the-Abbey and Vask-frames shapes.
Merged kind_robots#3959 (squash 87da01d8d1e045bb8e3214b3476f29b014047750, 19 checks green). Abbey can be doubted again: ~30 winks cut, a real fever ward (Dunmore's jars, Teodor's graves), children who come back (Linnet at seventeen, Coldbrook readers, 41 of 60 war children return Day 34), one hard tell before Day 29 (the Day 25 census, 212 names for forty beds), Dunmore/Kiyo/Hester argue both sides while Komodo mostly argues against. Big choices remembered: Day 25/30 variants, ACT_THREE_DUES (six), three new epilogue subjects. R10 pack-alliance set; R8 adult-shelter fixed; Pip trap opened; Wenna flipped, Dunmore beside Vask; three cots; Vane's rhino line gated on F013. Story calls recorded in PR body. Skipped: global re-offered-options pass (balance), Komodo debunking briefings, actFour reads (t-038).
<!-- note:end t-037 -->

## t-038 — Playtest rewrites, Act IV (Days 31-40): costly alliances, fair Komodo, the quiet word

<!-- note:begin t-038 -->
Implement playtest/2026-10-21/act4.md: alliances that cost a rival (the dominant d31/d33/d34/d35 options), the Black Verge as a party the player can bargain with, quieter unearned Komodo tells on Days 36-38, the Day 40 quiet word rewrite (R8: sit first, the physician question for every path, its answers read later, holding him contradicts dawn, the morning line), make the suspicious player's precautions matter (seal checks, recalled watch, secret tunnel, rosters), the Day 36 rehearsal payoff, quest results read (the collapsed Mole tunnel), a visible likely-hideout hint before Day 41.
Merged kind_robots#3961 (squash 4de431a3f1e05ce13f2a579dda94996182705a99, 21 checks green). Precautions matter: PRECAUTIONS list in betrayal.ts (8 guarding, 3 line-only) lowers who leaves with Komodo (3 down to 1) and lines the betrayal page; Komodo's note quotes the physician answer; Day 50 d50-if-you-find-him per philosophy. Audiences aid matching quests (Day 31 Ford, Day 33 Thistledown, Day 36 cellar). Days 36-38 tells quieted. Quiet word rewritten (sit/ask only, physician question on every path, chain answer). Alliances cost a rival (Days 31/33/34/35); new Day 37 d37-verge-terms (fields, 40 brass, or hostage Corwin Vask or Sable) blocks the Verge as buyer while it holds. Rehearsal payoff (Teodor can be lost to the Abbess). Hideout hint in the map room Days 35-40 matching selectHideout. Quest results read (collapsed tunnel/burned trestle clear pledges; tally book read aloud). ask-runners removed. Story calls recorded in PR body. Skipped: probe-template variety beyond the Verge scene; R7 Vellum line/Day 43 count (paid on the betrayal page); unread flags rehearsal-caught, ford-held, waystation- defended, crow-debt-defaulted and the Tobin clash (moved to t-043).
<!-- note:end t-038 -->

## t-039 — Playtest rewrites, Act V and endings: alliances reach the finale, a reachable Bell, warned Candles

<!-- note:begin t-039 -->
Implement playtest/2026-10-21/act5.md (17 proposals): Act V alliances change the Day 50 odds (alliance items/roads), The Bell Restored reachable and requiring the bell rung, A Hundred Candles warned and not silently overriding the vote, hideout terms with real bargains and later collection, fake choices made real (Kiyo, Saffron, front door, dig vs hold), continuity (coalition, Reedlight after the dike, Dunmark's rank, Vellum's place), the Day 44 kegs given a real counterweight, missing quote marks, and the epilogue's repetition ("Nobody", annual rituals) and Long Night variants that read choices.
Merged kind_robots#3963 (squash 5b77657373c262f75b706bb0b4a388eef187265a, 19 checks green). Writing on top of t-040's mechanics: fake choices made real (Kiyo dismissed, Saffron traded for forty Pack riders as Day 50 aid, front-door dispatch +2, dig costs Moles, hold gives Granny's lamp); Day 44 kegs counterweight (dike drowns Abbey deep well, +2 all roads, costs the lantern-houses and Fennet); continuity via composed() line swaps (Dunmark demoted, Watch, Verge, Pack, Vellum at the fire); Candles spoken and the Day 49 vote preserved under it; all eight hosts collect Day 46 in their own voice; brass buys more than words; ~15 new epilogue variants reading previously unread flags; endings.ts explaining lines cut; Long Night variants; kingdom rituals made single dated acts. Skipped: deserter gate path (R4), host-patience audience, alliance item rewards (R13), lethal bell climb (left to t-041), ~40 barracks rituals. Balance: patron:saltroad 10 Open Roads; Hundred Candles still one reckless seed (thin).
<!-- note:end t-039 -->

## t-040 — Playtest engine hooks: audience-to-quest aid, flag-keyed outcome text, debts and laws that come due, finale reads alliances, honest throne stakes

<!-- note:begin t-040 -->
From the 2026-10-21 playtest (playtest/2026-10-21/SUMMARY.md and the act reports). Build the engine/UI hooks the act rewrites need: an option effect that aids or resolves a posted quest (so marching the Watch to the Ford changes that quest); flag-keyed variants for quest outcome/expiry text and other fixed lines; debts and laws that come due (Ledger loan repayment, the Day 2 tax rate as a standing law that changes daily taxes, fees that rise); a follower-leave effect; per-hideout bargain effects; Day 50 odds that read Act V alliances; honest stakes on the throne screen (which factions an answer warms or cools, brass gained, probes marked as continuing the scene). Balance test must hold.
Merged kind_robots#3957 (squash 9d795c6af256301c9dfb8ec9ea6183b52ee6e15e, 21 checks green). Hooks: effects.questAid + QuestDef.aid; FlagGate-keyed outcomeVariants/komodoVariants/whisper.variants/fellVariants/whyVariants/FALL_OPENINGS; quest:<id>:<tier> flags; DueDef dues and laws (ledger-loan Day 20, Day 2 rate as standing law, rain-covenant/crow-debt); effects.dismiss; HostTerms bargains + host-due Day 46 + effects.relocate; FINALE_AID; Bell Restored needs bell-rung; candlesLine from Day 45; optionStakes on every throne answer. Persona-run fixes: rain-covenant bill only when crow-debt-called, crisisLine display names, Komodo precaution variants. Open call for Silas: runner-paid covenant runs still billed Day 34 (exempting them broke the Storm Crow balance threshold).
<!-- note:end t-040 -->

## t-041 — Risk, economy and variety: quests that can fail, brass that runs short, more quest templates, honest previews

<!-- note:begin t-041 -->
From the 2026-10-21 persona runs (playtest/2026-10-21/runs.md): across three full campaigns no follower died, none left with Komodo, nobody needed a loan; 13 of ~240 parties went out below 80%; lethal quests showed 0-4% death; the Day 50 finale rolled 92-99%; A Hundred Candles unreachable; brass settled ~25 dilemmas and every run was rich in Act V with nothing to buy; only 10 quest templates (The Late Caravan up to 10 times a run, twice on one dawn with identical text); previews overstated odds when unrevealed weaknesses applied (94% shown, 75% rolled). Retune requirement bands/odds so a careful player still faces 50-70% calls and real losses, tighten brass (wages, taxes, rewards, Act V sinks), expand and vary quest templates with stark outcome text and no same-dawn duplicates, make previews honest about unknowns (range, not a point), and make departures and deaths reachable without being punitive. Keep all eight endings reachable; update the balance test's thresholds deliberately (document why) rather than weakening them blindly.
Merged kind_robots#3962 (squash 8daa9d719518f5bf5e17164825bef7de1ae0ea5a, 21 checks green). Requirement needs scale by act (1/1.15/1.3/1.4/1.5), lethal x1.2 (finale-aid roads exempt), exact-need 75% (was 90%); deep wound kills at 40% on failure, 8% on partial. Honest previews: ranges for unread applicable traits, worst-case death odds, Cave-Luck included (rolled outside shown range 33% -> 0%). Departures with weight: Komodo persuades the follower the emperor sat with most (named from Day 37; stopped by Day 40 hold/follow, sealed romance, or follower away); kin departures when the crown turned their people. Chores pay 3-12, Act V chores cost brass; 30 chores in chores.ts with day windows and stark alternates, max two posts per run, no same-dawn duplicates; finishDay repost bug fixed. 120-campaign metrics: deaths/run 0.16->0.40, Komodo departures 0->0.97 (ceiling; warned), loan runs 38%->71%, finale mean 95.5->84.2 (45-98), Day 50 brass median 133->44. Balance thresholds changed deliberately and documented in the test (deaths cap 1.0; floors on losses, Candles 1+ but <=20%, borrowing >=75%). Follow-up: q-d50-ring-the-bell and q-d50-crypt-path have no partial reward/outcome line.
<!-- note:end t-041 -->

## t-042 — Talk pacing: no week-long droughts, no talks naming absent followers

<!-- note:begin t-042 -->
From the 2026-10-21 persona runs: 17-23 of 50 days had no barracks talk available and then several arrived at once; some talks mention followers who are not in the court ("the rhino", "Mags"). Smooth fromDay spacing per follower, add short talks where the calendar runs dry, gate lines that name another follower on that follower being present (requires.follower or variants), and add a contract check that a full seeded run has a talk available on most days.
Merged kind_robots#3956 as 0a2784c65282c172016775de50f67076c00d3ce3 (19/19 checks). 45 new one-dilemma talks fill the calendar (existing ids/flags/fromDays unchanged); talk availability for a sit-daily player rose from 35-65% of days (dry streaks up to 19) to ~95% (longest 1; starters-only 87%, longest 3). Lines naming absent followers gated or rewritten (sable-1, sable-2, cobb-2, hollin-2). Contract: no talk names another follower unless gated on them; seeded sit-daily runs keep >=90% availability (>=80% starters- only), never more than 3 dry days.
<!-- note:end t-042 -->

## t-043 — Playtest follow-ups: Day 50 partial outcomes and the readbacks the act rewrites skipped

<!-- note:begin t-043 -->
Leftovers named by the t-036, t-039 and t-041 workers. (1) q-d50-ring-the-bell and q-d50-crypt-path have no partial reward or outcome line: a partial roll seals nothing and the dawn line is empty; give each a stark partial outcome. (2) Act II readbacks needing a later scene: the Day 14 flags on the map/Saltroad, d18-water-taxed in the epilogue, bell-vote-tied, ford-dam-built (the reservoir). (3) Act V: the deserter's "who opened the gate" path (R4, nameless cave) and a host-patience audience for a host whose demand went unpaid. (4) Name collision: t-036 named the Day 34 runner (Yard stoat) Linnet and t-037 named the Day 25 otter sister (former Yard orphan) Linnet; rename the otter sister (Act III, t-037 dues, epilogue). (5) Tobin clash: t-039 named Tobin Umber (Granny's grandson) and moles.ts has another Tobin. (6) Still-unread flags after t-038: rehearsal-caught, ford-held, waystation-defended, crow-debt-defaulted. (7) Optional, from t-035: d10-oath-names-houses, d10-oath-of-care-broken, d10-promise-broken, d03-tincture-fee-lapsed have no later readback yet. Same rules as t-035..t-039: stark prose, preserve ids/effects, contract assertions, balance honest.
Merged kind_robots#3968 (squash 415864ced98e0323f33f9e445f11a329ec741b25, 19 checks green). (1) done earlier by kind_robots#3965 (1302cad9): Day 50 crypt/bell partials, every Day 50 road lethal. (2) Act II readbacks: maps-copied aid, d14-abbey-maps-first Day 25 hill beat + crypt aid, d14-ledger-owns-roads Day 30 buy-roads-back, bell-vote- tied set and read Day 29 (Mara broke the tie for the crown), ford-dam-built Iron Rain aid, d18-water-taxed epilogue. (3) Deserter's who-opened beat in the nameless cave (consistent with FALL_OPENINGS) and seven Day 46 host-patience audiences (pay / named- follower surety / time / leave). (4) Day 25 otter sister renamed Moll. (5) Tobin Umber renamed Odo Umber. (6) rehearsal-caught, ford-held, waystation-defended, crow-debt- defaulted read. (7) the four Act I flags read. Balance unchanged in thresholds; Candles 8->9 runs. Note: vue-tsc needs --max-old-space-size=6144 in this container (3072 OOMs).
<!-- note:end t-043 -->

## t-045 — Story and art pilot: revise early quest aftermaths and queue illustrated throne-room choices

<!-- note:begin t-045 -->
Silas-directed 2026-10-21: prioritize polished, consequential quest and conversation writing, then private art submissions for an image-heavy Emperor of Dust. Pilot on Days 1-3 with canon-locked anthropomorphic species, distinctive characters, and separate choice aftermath plates. Preserve flags, quest IDs and mechanics; follow SCENE-WRITING-GUIDE.md. Do not confuse queued ArtJobs with rendered/displayed art. Subsequent batches should extend to every act, barracks talk and quest result.

First scene-writing slice updates 42 quest result texts and eight audience replies on Days 1-3, preserving ids, rewards, flags and quest logic. The private illustrated scene-art ledger and workflow submission follow in a companion PR.

Delivered 42 rewritten quest outcomes plus eight throne-room responses across Days 1-3 in kind_robots PR #3987, merged at a55243e76b1d1f80722ccbb71db2ad97dfa48c98 after all 13 CI suites succeeded. Authored 22 new private anthropomorphic illustrated audience/conversation plates, canon and naming production guide, and a durable Auto Art Generate submission step in conductor PR #6454, merged at 2106dbd97f30be8e210a68891575181cef9e4d51 after all final CI passed. The resulting Auto Art Generate workflow 39572940760 ran the Emperor submission step with GitHub conclusion success. Individual ArtJob IDs, renders, deliveries, and runtime wiring are not yet confirmed; t-052 owns these later gates. New coverage tasks t-046..t-052 for all remaining acts and follower talks merged through conductor PR #6459.
<!-- note:end t-045 -->
