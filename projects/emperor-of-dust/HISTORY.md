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

## t-010 — Obtain explicit human visual acceptance and public Play release approval

<!-- note:begin t-010 -->
Internal admin preview is permitted; no public /play route or published campaign without later explicit approval.

APPROVED by Silas in session 2026-11-11 PT: "Emperor of dust should have already been moved to play long ago." Public Play release is approved. Verified the same day that /play/emperor-of-dust already serves (HTTP 200), /admin/emperor-of-dust 301-redirects there, and the game is listed in the Arcade placements and home visitor directory, so no further release step is needed. Remaining art delivery and polish continue under t-052 and the new t-063 (wire rendered art), t-064 (ending plates + gallery), t-065 (achievements) and t-066 (new-run carry-overs).
<!-- note:end t-010 -->

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

## t-033 — Export the market item icons and the pending room/quest rerolls when they render

<!-- note:begin t-033 -->
ArtJobs 42323-42352 (art/ITEMS-ROUND-1.yaml, 30 market item icons) and 42158-42162 (ROOMS-ROUND-1 barracks v2, QUESTS-ROUND-1 q-d42-cave-forage) were queued 2026-10-20 behind a multi-hour backlog. Run enqueue_art_requests.py --status on each ledger (safe on relay 502s since conductor#6416), contact-sheet and review, reroll rejects as -v2 subjects, export keepers to kind_robots public/emperor-of-dust/items/<id>.webp (list in ITEM_ART), rooms/ (ROOM_ART) and quests/ (QUEST_ART), and record approved/keepers in the ledgers.
2026-10-21 partial: barracks backdrop keeper barracks-b-v2 exported in kind_robots#3955 (f8a577a), ledgers updated in conductor#6431 (5f33b39). Cave-forage v2 rerolls (42160-42162) rejected (no cave in any); v3 rerolls queued as ArtJobs 42353-42355. All 30 item icons (42323-42352) still PENDING behind a slow shared queue (~85 jobs ahead at 01:20Z). Re-armed to ready: when the queue reaches them, run enqueue_art_requests.py --status on ITEMS-ROUND-1 and QUESTS-ROUND-1, review on contact sheets, export items to public/emperor-of-dust/items/<id>.webp (320px, q80) listed in ITEM_ART and the cave set to quests/ in QUEST_ART, then render the market at 1440/390. Helper: polish/tools/items.py in the 2026-10-20 session scratchpad (paths need updating). 2026-10-21 04:20Z: ITEMS-ROUND-1 status DONE=3, RUNNING=1, PENDING=26; re-check with enqueue_art_requests.py --status and export once all 30 are DONE.
2026-11-19 PT partial: ITEMS-ROUND-1 was all DONE but never exported (ITEM_ART was empty). Curated on contact sheets: kept 6 (road-lantern, carbide-lamp, abbey-candle, night-draught, brass-bell-charm, surveyors-glass) and shipped them with an ITEM_ART contract test in kind_robots#5383. Rejected 24 because the lane suffix 'warm candlelight' drew a candle dish instead of the item; verdicts are in the ledger. Rerolls are in ITEMS-ROUND-2.yaml (ArtJobs 71164-71187; suffix now rim light, candles in the negative). Next: run enqueue_art_requests.py --status on ITEMS-ROUND-2, contact-sheet it, and export keepers with export_round_art.py --require-keep --max-edge 320, adding them to ITEM_ART. The q-d42 cave-forage v3 set (42353-42355) is still to be checked. Released to ready.
2026-11-20 PT partial: ITEMS-ROUND-2 all 24 DONE. Contact sheet plus full-size check kept 4 (caravan-salve, silent-bell-rosary, verge-signet, watch-buckler), shipped in kind_robots#5389 (ITEM_ART 6 -> 10). Rejected 20 (mostly generic discs or the wrong object; field-kit and ledger-abacus were dropped at full size for pseudo-lettering). Verdicts are in the ledger. Rerolls are in ITEMS-ROUND-3.yaml (ArtJobs 71188-71207): the prefix drops 'item icon', prompts lead with the object noun, and the negative adds coin/medallion/disc/label. Next: enqueue_art_requests.py --status ITEMS-ROUND-3, curate at full size, export keepers. The q-d42 cave-forage v3 set (42353-42355) is still unchecked.
kind_robots#5389 merged at 4504d1f (13/13 checks green). Released to ready: curate ITEMS-ROUND-3 (71188-71207) once it renders.
2026-11-20 PT partial: ITEMS-ROUND-3 all 20 DONE. Contact sheet plus full-size check kept 12 (bell-clapper, freehold-spade, lamplight-folio, ledger-abacus, lost-human- gauntlet, magpie-scales, rain-feather, reed-poppet, signal-coil, snare-kit, storm-glass- vial, witchwater-phial), shipped in kind_robots#5394 (ITEM_ART 10 -> 22). Rejected 8 (verdicts in ledger). Rerolls are in ITEMS-ROUND-4.yaml (auto_submit, seeds 74001-74008) with plainer object nouns and wrong-object negatives. Next: enqueue_art_requests.py --status ITEMS-ROUND-4, curate at full size, export keepers. The q-d42 cave-forage v3 set (42353-42355) is still unchecked. Released to ready.
2026-11-20 PT partial (r4): ITEMS-ROUND-4 all 8 DONE; full-size check kept 3 (field-kit, saltroad-waybill, crow-glass-eye), shipped in kind_robots#5400 (ITEM_ART 22 -> 25). Rejected 5 (crowbar drew a goose, lockpicks a spanner, spurs a wheel, cutters a blade, tooth a creature bust); rerolls in ITEMS-ROUND-5.yaml (auto_submit, seeds 75001-75005). q-d42 cave-forage v3 finally checked: notice+success approved and exported to QUEST_ART in the same PR; failure rejected (warm fire, full baskets) and falls back to the notice. Ledgers in conductor#7655. Next: enqueue_art_requests.py --status ITEMS-ROUND-5, curate at full size, export keepers. Released to ready.

2026-11-20 PT partial (r5): ITEMS-ROUND-5 all 5 DONE. Full-size check kept 0. The crowbar was the right object but only a hairline sliver at icon size; lockpick-roll drew a brass tube and one pick, courier-spurs a boot with no spur, rustline-cutters a clamp-blade, hyena-tooth a toothed bone. Verdicts are in the ledger. Rerolls are in ITEMS-ROUND-6.yaml (ArtJobs 71221-71225, seeds 76001-76005): close-up framing, familiar look-alikes (pencil roll, horseshoe band, pendant charm) and wrong-object negatives. ITEM_ART stays 25/30. Next: enqueue_art_requests.py --status ITEMS-ROUND-6, curate at full size, export keepers with export_round_art.py --require-keep --max-edge 320. Released to ready.

2026-11-20 PT partial (r6): ITEMS-ROUND-6 all 5 DONE; full-size check kept 0 (crowbar a
bent hairpin rod, lockpick-roll a closed tube, courier-spurs a spiked mace ball,
rustline-cutters a tong/clamp, hyena-tooth a dagger pendant). Verdicts in the ledger.
Two Arthemy rounds missed these five, so ITEMS-ROUND-7.yaml moves them to the Krea 2
prose lane (ArtJobs 74311-74315, seeds 77001-77005), merged in conductor#7667. Next:
enqueue_art_requests.py --status ITEMS-ROUND-7, curate at full size, export keepers with
export_round_art.py --require-keep --max-edge 320. ITEM_ART stays 25/30. Released to
ready.

2026-11-20 PT (r7): ITEMS-ROUND-7 (Krea 2 prose lane) all 5 DONE. The full-size check
kept all 5: crowbar, lockpick-roll, courier-spurs, rustline-cutters and hyena-tooth
(verdicts in the ledger). Exported at 320px to kind_robots#5451 (ITEM_ART 25 -> 30,
every market item now has an icon). The contract test now requires an icon for every
ITEMS entry. The room and quest rerolls were already resolved (barracks
kind_robots#3955, cave-forage conductor#7655). Done once #5451 merges green. Lesson: two
Arthemy rounds missed these literal objects, and the Krea prose lane got all five on its
first try.

kind_robots#5451 merged green (squash 9e57005, all 14 checks passed). The Emperor market
ships 30/30 item icons. Task complete.
<!-- note:end t-033 -->

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

## t-044 — Second playtest: score the rewritten game against the 2026-10-21 rubric

<!-- note:begin t-044 -->
The first playtest (playtest/2026-10-21/, PLAYTEST-RUBRIC.md) drove t-035..t-043 and t-041, all merged 2026-10-21 (kind_robots#3959-#3968). Re-run it on current main with the same rubric (mood, clarity of the challenge, uniqueness, choice quality, consequence; Silas: "not just rescue the unicorn versus throw the puppies in the lava"): one reviewer per act plus a persona-campaign run (deaths, departures, loans, odds spread, finale odds, brass, chore repetition; the t-041 measurement scripts are the model). Write results to playtest/<date>/ beside the first pass, compare scores act by act, and file only real regressions or still-weak scenes as new tasks. Read-only for the reviewers; run at most three at a time (six parallel Opus workers hit the session usage limit on 2026-10-21) and keep at most one Nuxt dev server up (the container OOMs; vue-tsc needs NODE_OPTIONS=--max-old-space-size=6144).

Second playable engine pass underway: Kiyo paid infirmary, intentional quest slack, seeded daily encounters, 5 secret followers, Kiyo friendship and romance. Implementation PR and CI follow. Playtest report to accompany merge.

2026-11-04 PT reconciliation: not done. Stale 2026-10-22 claim; no second scored
playtest folder exists (only playtest/2026-10-21/, whose SECOND-PASS-SYSTEMS-AUDIT.md
says per-act rubric scoring is still open), and EditorialAcceptance calls itself a
deterministic proxy. Back to ready to do the scored per-act second playtest as written
(read-only, no art needed).

Added a reproducible second-pass five-act scoring protocol and evidence schema on worker/emperor-of-dust-t-044-rubric-b6e2. This is a partial increment; actual scored playthroughs and transcripts remain pending.

2026-11-20 PT reviewer: merged the worker's SECOND-PASS-SCORING-PROTOCOL.md
(playtest/2026-11-19/) as a partial increment; rubric, evidence rules and reviewer-
record schema are sound. Not done: no reviewer records, traces or per-act scores exist
yet. Back to ready (no pass spent; incomplete, not a quality failure). Next cycle: run
the per-act scored reads per this protocol (max three reviewers at once) and fill
reviewer records under playtest/2026-11-19/.

Implemented full day-by-day modeled campaign trace capture across eight policies and two seeds; narrative scenes, choices, dispatches, quest results, 51 dawns, saved checkpoints and Day 31 rewind. Kind Robots PR #5390 open. Independent rubric scoring still open.

2026-11-19 PT: Merged Kind Robots #5390 at fe974cf80f94b52eee1aadafdcb0a8617214efa3 after all eight exact-head workflows completed successfully on e40e79f90b4c4e655934fb1b56a5111f4906088f. The Emperor workflow generated a 14.35 MB artifact with sixteen reproducible 50-day model-simulation traces, narrative transcripts, checkpoints and rewind evidence. This is simulation evidence, not independent scored editorial or human playtest acceptance. Release t-044 to ready for real act-by-act scoring, documented weaknesses, repairs and cross-width QA.

Inspected actual Kind Robots run 44675257192 / artifact 14601418218 (16 complete model-simulated campaigns). All 51 dawns, four distinct ending IDs, zero observed deaths or loan use; selected marshal-17 for act-by-act source-grounded scoring. Kind Robots branch worker/emperor-of-dust-t044-trace-fidelity-b4e9 records actual choice costs/requirements and ending coverage; PR and independent review record staged next. This is partial t-044, not full independent scored multi-persona acceptance.

2026-11-20 PT: Merged Kind Robots #5424 at a02749bc3cfa151e58919c4355b42e14fdf04eb7 after all 7 exact-head workflow families including four contract shards and verifier succeeded on 1b54e7e6020b858c922e3ca1e9f17a0504015837. Verified the produced CI artifact 14625771393 (run 44728766903) contains 16 full 51-dawn campaigns, every sampled audience and barracks choice records requirements/costs, and explicit 4/8 ending coverage. Merged Conductor #7665 at 9cc5796c4f7f030f08dfc35eedc0dd6ba7f587a7 after all four exact-head workflows passed on 3f142b95b42382925c56e3cfa775823fdbf0675d, adding a provisional scored reviewer-model-marshal-17.yaml and a committed-record validator regression. Score totals for this one simulated marshal/17 run: Act I 18/25, Act II 19/25, Act III 17/25, Act IV 17/25, Act V 19/25. Not final acceptance: bell-restored, crows-bargain, tunnels-and-councils and hundred-candles are still not visited by the 16-run matrix, no follower deaths or loans observed, other personas and UI/cross-width and real art deliveries not independently accepted. No ArtImage bytes exported or production deployed. Return task to ready with original unfinished scope preserved.

Partial second-pass evidence increment: added verifyEmperorEndingWitnesses.test.ts to find all eight ending families using only real seeded 50-day campaign play (same ten-seed policy grid as the existing balance contract), then replay each legally earned witness with 51 complete dawns, court decisions/eligibility/effects, quests, full saved states, six save roundtrips, and a Day 31 rewind. Emperor Dispatch CI now runs and uploads the eight trace/transcript pairs and manifest. Existing 16-persona 4/8 sample is preserved as a separate, honest sample; no flags or endings injected. Exact-head CI and PR merge remain pending. This does not constitute an independent rubric verdict, real rendered artwork delivery or cross-width browser acceptance.

2026-11-22 PT: scored second pass complete for its finite scope: protocol + reviewer
record (playtest/2026-11-19, acts 17-19/25), sixteen modeled campaigns and all eight
endings witnessed by real seeded play (verifyEmperorEndingWitnesses). Cross-width sample
captured 390/768/1440 on kind_robots#5529 head: no horizontal spill, game art loads.
Closed at the playtest handoff (docs/agents/GAME-PLAYTEST-CLOSEOUT-2026-11-18.md): all
50 days authored and route-tested in CI (adversarial seeds, eight real-play ending
witnesses, sixteen 50-day traces, market/refugee/water-debt route matrices). Further
line-level editorial judgement is subjective human-playtest feedback, outside the finite
roadmap; new fixes use playtest_iteration: true.
<!-- note:end t-044 -->

## t-045 — Story and art pilot: revise early quest aftermaths and queue illustrated throne-room choices

<!-- note:begin t-045 -->
Silas-directed 2026-10-21: prioritize polished, consequential quest and conversation writing, then private art submissions for an image-heavy Emperor of Dust. Pilot on Days 1-3 with canon-locked anthropomorphic species, distinctive characters, and separate choice aftermath plates. Preserve flags, quest IDs and mechanics; follow SCENE-WRITING-GUIDE.md. Do not confuse queued ArtJobs with rendered/displayed art. Subsequent batches should extend to every act, barracks talk and quest result.

First scene-writing slice updates 42 quest result texts and eight audience replies on Days 1-3, preserving ids, rewards, flags and quest logic. The private illustrated scene-art ledger and workflow submission follow in a companion PR.

Delivered 42 rewritten quest outcomes plus eight throne-room responses across Days 1-3 in kind_robots PR #3987, merged at a55243e76b1d1f80722ccbb71db2ad97dfa48c98 after all 13 CI suites succeeded. Authored 22 new private anthropomorphic illustrated audience/conversation plates, canon and naming production guide, and a durable Auto Art Generate submission step in conductor PR #6454, merged at 2106dbd97f30be8e210a68891575181cef9e4d51 after all final CI passed. The resulting Auto Art Generate workflow 39572940760 ran the Emperor submission step with GitHub conclusion success. Individual ArtJob IDs, renders, deliveries, and runtime wiring are not yet confirmed; t-052 owns these later gates. New coverage tasks t-046..t-052 for all remaining acts and follower talks merged through conductor PR #6459.
<!-- note:end t-045 -->

## t-046 — Act I continuation: polish Days 4–10 quest and audience paths, then submit scene art

<!-- note:begin t-046 -->
Audit every authored Act I audience, probe, beat and quest result after Day 3. Rewrite thin consequences, repeated templates and dominant choices without breaking stable flags, ids, effect contracts or later callbacks. Use canon species and first appearance data. Once the prose is merged, author private per-scene entry/choice/outcome plates in the Arthemy lane, validate prompt contracts and enqueue via the durable ledger. Track art as requested, queued, rendered, exported and wired separately.

First Act I implementation slice: 31 distinct Days 5-10 quest outcomes rewritten with concrete stakes, retaining all effects and quest identifiers. New private Arthemy ledger with nine choice/outcome plates proposed for opt-in auto-submission. Full scene coverage, ArtJob receipt verification and visual exports remain follow-on work; do not call final art delivered.

First narrative/art production slice merged: kind_robots#4104 at 692b8d654d2660a1cb9209fb95216a5a05f0ba0f after 13/13 checks, and conductor#6578 at 63068404fab20c0bd14da3d5bca77d4ad90e9e6e with full Conductor CI green. 31 Days 5-10 quest result passages are rewritten; nine private Arthemy scene/outcome requests now have a durable auto_submit ledger. No new ArtJob IDs, editorially approved images, exported assets or game wiring verified yet. Remaining t-046 scope: audit Day 4-10 audience/probe/beat paths and finish distinct visual coverage, review and delivery. Leave ready for next pass.

Day 9 callback slice: new loan-cart and coerced-postern-informant audiences with conditional visibility, costly choices, probe beats and state assertions. Target PR in kind_robots; remaining Days 4-10 and art production stay open.

2026-10-25 PT: Merged Act I Day 9 callback slice in kind_robots#4198 (f17a22febe5f9d40f92335f40cc4390a3472e955). Conditional Ledger loan-cart and coerced stablehand-informant audiences each add an investigative beat, costly options, persistent flags and distinct consequences. 14/14 exact-head GitHub Actions workflows passed, including all four Contract Tests shards, TypeScript and Emperor Dispatch Contract. Static main-branch verification confirms both scenes. This is PARTIAL t-046 progress: continue Days 4-10 prose and quest review, then submit durable Arthemy art jobs, review renders, export and wire accepted plates. No ArtJob IDs or art delivery claimed.

Day 10 Coldbrook callback implementation and targeted regression tests are on worker/emperor-of-dust-t-046-20261026-c8f7b; PR and CI verification follow.

2026-10-26 PT: Day 8 Coldbrook homeward decision now unlocks a Day 10 Thistledown probe with a paid Yard rescue, uncertain runner warning, or the original village promise. Two Day 11 due reports and durable flags, role-first prose fixes, and focused state/save assertions merged in kind_robots#4236 at 69a8dd9d. All 14 exact-head Actions workflows passed, including fortress/balance/adversarial, TypeScript, formatting and all four contract shards. Master issue evidence: https://github.com/silasfelinus/kind_robots/issues/4142#issuecomment-6422407435 Remaining t-046: Days 4-10 audience/quest editorial coverage, genuine ArtJob submission/receipts, rendered review, export and gameplay wiring. No new ArtJob IDs, verified renders or deployment this increment.

Scoped Day 9 canyon-to-Day 10 Thistledown follow-through: two earned rescue tactics, explicit faction costs, quest aid, Day 11 reports and state/save regressions. Implementation branch worker/emperor-of-dust-t-046-20261026-b7e3; PR and exact-head CI to follow. Broader Act I/art scope remains open.

2026-10-26 PT: Merged Day 9 canyon-to-Day 10 Thistledown causal pair in kind_robots#4247 at 17b94910 (exact PR head 1f741a55, all 14 completed Actions workflows green: Emperor Dispatch 40408467537, Contract Tests 40408467489, TypeScript 40408467451, formatting 40408467431). Hill-farmer grain and iron-wagon bargains unlock mutually exclusive, costly evacuation/barricade tactics, +2 quest aid, and distinct Day 11 reports with durable flags. Regression tests verify conditional visibility, costs, quest odds, dawn reports and serialized state; not yet full fresh-game playthrough. Master issue: https://github.com/silasfelinus/kind_robots/issues/4142#issuecomment-6428399673. Remaining t-046: Days 4-10 audience/quest editorial audit and real ArtJob submission/receipts, rendered review, export and wiring. No ArtJobs, rendered art or deployment this increment; keep task ready and game active.

Polished Day 4 carryover: the Pack faction split changes Day 5 toll bargaining, and a sheltered or returned Storm Crow runner gives distinct costly Day 7 forecast paths. Added regression assertions for visibility, affordability, persisted flags and day-10 storm scheduling. This is a partial Act I and art task; further audiences and verified scene art remain.

Merged Kind Robots PR #4673 at 1e0f8914482fda8e400f9761f0dc3edf2759c9be after all 8 exact-head GitHub Actions workflows and all 13 check runs passed. Day 4 Pack splinter choices now alter Day 5 Vane toll talks and Day 10 Thistledown grain bargain/quest outcome; Day 4 sheltered or returned bonded crow messenger drives distinct costly Day 7 forecast options. Added real branch, gate, brass, quest aid, serializable state and scheduling assertions; fortress balance, adversarial, store, secret talk and role-first prose checks passed. PR #4673 has a scored editorial read-through with open deficits. Further Days 4-10 scene coverage and real ArtJob submission/render/export/wiring remain; keep t-046 ready, umbrella issue #4142 open and final human gate untouched.

2026-11-04 PT: Day 6 market-charter no-exemption path now leads to a Day 8 Freehold blanket-seller hearing. Restitution, seven-day tenancy and enforcement have distinct costs, responses and flags. Added scene-gate, beat, affordability, save validation and effect regressions on kind_robots branch worker/emperor-of-dust-t-046-market-blankets-b61f. CI and PR review pending. This is a partial Act I prose increment; art submission and comprehensive Day 4-10 editorial coverage remain open.

2026-11-04 PT: Act I Day 6 market charter now telegraphs its Freehold blanket-stall consequences. New Day 8 court hearing supports restoring, leasing or enforcing eviction with actual Watch fees, factions, dialogue, and durable flags. Those outcomes unlock three distinct paid Thistledown evacuation-aid routes on Day 10. Tests cover gates, exact costs, persistence, and quest aid. Merged kind_robots PR #4748 at 9bcd5a43eacbf074bf53e9099bbdb84977b306eb after all eight exact-head GitHub Actions workflows and 13 check runs completed successfully, including fortress balance, TypeScript and four contract shards. No new ArtJobs, rendered images or deployment were claimed. Remaining t-046 work: comprehensive Days 4-10 writing audit, art requests, render review, export and wiring. Keep t-046 ready and master kind_robots issue #4142 open for the next increment.

2026-11-04 PT: Added Day 5 bread-ration flag on both original ration routes; the Day 7 Old Houses audience now confronts the rationing court with an independent grain purchase, a grain-for-council-seat pact, or continued rationing. All three carry costs and durable flags that alter Day 10 Thistledown evacuation offers, including real dispatch aid. Added live-engine regressions for route gates, faction costs, affordability, save validity and quest aid on kind_robots branch worker/emperor-of-dust-t-046-bread-council-f7c3. CI and review pending. Remaining Act I/art scope stays open.

2026-11-04 PT: Merged Kind Robots PR #4752 at f669ad61d4b6c3aef0a6fd8f8a995d7ad5e92a84. Day 5 bread rationing now causes Day 7 Old Houses grain bargains and three mechanically distinct Day 10 Thistledown food-relief dispatch routes. Existing IDs preserved; live-engine coverage added for conditional dialogue, exact costs, factions, flags, quest aid, and save validity. All eight exact-head GitHub Actions workflows and 13 checks completed green, including fortress/balance, TypeScript, formatting and all four contract shards. Merged private nine-plate Arthemy art ledger in Conductor PR #7021 at 2baa02b570d753253171c8b6fdcf85a466bfc9ee, with green PR CI; Auto Art Generate workflow run 41927764001 began for this ledger. No new job IDs, rendered ArtImages, accepted exports, game wiring or production deployment verified at closeout. Keep t-046 ready for remaining Days 4-10 editorial audit, render receipt checks and art delivery; master kind_robots issue #4142 remains open.

2026-11-04 PT: Wrote a conditional Day 10 Gate Watch oath branch for players who gave both the Yard and Old Houses seats on Day 7. New shared council opening, investigative beat and three costly outcomes (12-brass relief patrol with real quest aid, public Watch accounting, or Old Houses veto) have distinct political/faction effects and durable flags. Added live engine route/affordability/save regressions on branch worker/emperor-of-dust-t-046-shared-oath-2d91. CI and code review pending; broader Act I editorial and art completion remain.

2026-11-04 PT: Merged Kind Robots PR #4756 at 75cc2382bbbf3a33b07bbcdc1ffd2f66f6b52f70. Day 7 open-council (Houses and Yard) earns a gated Day 10 Watch-oath scene and three distinct outcomes: 12-brass relief with actual +2 Wits dispatch aid, public accounting, or House veto. Engine regressions cover flag gates, both earned Day 7 paths, affordability, effects and JSON save validity. Eight exact-head Actions workflows and 13 checks green. Merged Conductor private five-plate Arthemy art ledger in PR #7024 at 8d3e0bac76fe9cf01d3c262229ced2cc377bc0b8 with 24 green checks. New plate ArtJob receipts, renders, acceptance, export and wiring remain to verify. Prior grain/council ArtJobs 63774-63782 were last verified PENDING. No production deploy or visual acceptance claimed. Keep task ready for broader Act I QA and delivery; master kind_robots issue #4142 stays open.

2026-11-04 PT: Days 4–10 writing/state slice ready as a patch, not yet a PR (base
4815d312). All 36 Days 4–10 flags that were set but never read now pay off, additively:
25 hidden dawn dues, 9 scene opening variants (Vane on Day 5, Tallow on Day 8, Oriel on
Day 9, Dunmark on Day 10, the mapmaker on Day 16), 3 Day 10 Komodo morning variants, 1
quest aid (stable mounts on the Day 8 escort) and a convoy outcome pair. Prose now
matches state: the Day 4 informant is a girl as everywhere else, the surety loan says
thirty (what it pays) and the Day 9 Ledger cart argues the search term, the convoy
success counts nine wagons, and three "later" promises (ration card, bog myrtle, blank
tally) arrive as dawns. Line-level voice pass on the Days 4–10 audiences. A new t-046
block in verifyEmperorFortress fails on any forgotten Days 4–10 flag (posted quests
included) or any Act I due nothing schedules. Fortress, Adversarial, Balance,
SecretTalks, EditorialAcceptance, GuidedCampaigns and RoleFirstProse are green; full
vue-tsc has 0 errors; editorial flagged rows went from 475 to 469. Remaining for t-046:
the art half (plates, ArtJob receipts, render review, wiring) and a Days 4–10 path
playtest; Day 16's turn-away line still says the card comes down "a week later" for
players who already saw it burned.  Merged as kind_robots #4829.

Partial Act I continuity repair prepared on Kind Robots worker/emperor-of-dust-t-046-20261119-f8c2: Day 16 mapmaker rejection no longer burns the ration card a second time after the Day 11 consequence of the Day 4 denial. Regression asserts both Day 4 branches and preserved outcomes. Exact-head CI and art delivery remain unverified.

2026-11-19 PT: Reviewer merged kind_robots#5342 at c7ceb5cce4aca68dcaa67fdb9b08adb58619b334 after all eight exact-head workflows succeeded on f41df235c8a5ae51ef91dac5e4e299cb98552794. Day 16 mapmaker rejection now respects Day 4 denial and Day 11 destruction of the ration-card map, with regression assertions for both routes. This is partial t-046 work; remaining Days 4-10 editorial coverage and genuine art exports/delivery remain open. Return to ready, not done.

2026-11-19 PT: Worker merged kind_robots#5392 at a94347fa15441f64868b8e29f8158bee7249fe0c after 13 exact-head checks succeeded on 1e3aa95869adb23a4525fc96b0ad3cedf7e4f46c. It rewrites 17 Days 4-10 quest aftermaths that the editorial screen flagged as under 100 characters: Day 4 survey/crow-elders/crow-roost/feast, Day 7 galleries expiry, and Day 9 convoy triumph, which now counts the nine wagons. It also deepens 10 early-board chore outcomes. The new prose stays inside each tier's real mechanics. A new t-046 regression in verifyEmperorFortress fails on any Days 4-10 quest result under 100 characters; I confirmed it fails against the old prose. Editorial flagged rows went from 458 to 442. Still open: 25 Days 4-10 scenes whose two terminal choices share mechanics, 24 unread-flag rows, 17 short after-responses, and the art half (plates, ArtJob receipts, render review, wiring). Partial work, so the task returns to ready rather than done (no pass spent).

Kind Robots #5401 adds 20 substantial Act I court-choice aftermaths, and 15 terminal-choice regressions pin the previous effects. This remains a partial writing increment; art delivery and other t-046 rows are not accepted.

2026-11-19 PT: Merged Kind Robots #5401 at 5fa0ae620be44debebe71f400949c3227880b04f after all eight exact-head workflows succeeded on 740a8c49623aa7ca1a6c1daf368b436ea502e79f, including all four Contract Tests shards and the final verifier, TypeScript, Prettier, and Emperor Dispatch. Expanded 20 thin Days 4-10 court-choice aftermaths with specific physical stakes; tests pin 15 terminal responses and preserve the ration and crown-oath effects. Partial t-046: further mechanically distinct choices and unread flag callbacks plus actual ArtImage review, export, wiring and viewport acceptance are outstanding. No new art bytes or live deployment claimed. Release to ready for remaining scope.

Reconciled previously conflicting Kind Robots #5399 using a normal two-parent merge commit 9ad2a2a9, preserving both latest main rewrites for Ledger factor Tallow and Juniper. The resulting PR diff is only the still-unshipped Day 8 Sister Marrow bedroom-count confrontation, with unchanged audience id, options, effects and save keys. Await exact-head CI before merge. This does not complete broad Act I editorial or scene-art delivery.

2026-11-20 PT partial Act I prose increment shipped by rescuing kind_robots#5399. The conflict was reconciled without force-push using two-parent commit 9ad2a2a9, preserving newer main Ledger-factor and Juniper replies; the final diff only improves Day 8 Sister Marrow's evasive Abbey bed-count answer. Merged at 574ed8a473aa8af921632e759c2e52cdfc437836 after all eight exact-head workflows and 14 checks passed on 9ad2a2a9d626eabd13766753c3c10711b035faef. IDs, flags, effects, saves and art paths unchanged. The full Days 4–10 editorial audit and actual rendered scene art delivery remain unfinished. Return to ready, not done; master issue #4142 stays open.

Partial Day 5-10 court consequence editorial pass prepared on worker/emperor-of-dust-t-046-editorial-7a9f: seven sharper probe, refusal and aftermath responses and matching static regression checks. All existing ids, cost requirements, effects, gates and save flags are unchanged. CI and merge required. Remaining Act I visual exports and wider review remain open.

Merged Kind Robots PR #5421 at 822c26422b308f48c8ab19f2b837f70b0ef53b6f after all eight exact-head CI workflows completed successfully on 56f8b780face7ff7eea1d0fd9f775b2f653e4806. Seven Day 5-10 audience probe/refusal/aftermath responses now carry concrete named human costs, with seven focused fortress regression checks covering opening and investigation beats. No choice IDs, flags, mechanics, costs, quest postings or save schemas changed. Full Act I audience/quest editorial coverage and real rendered ArtImage review, export and visual QA remain open. Master #4142 stays active and open.

Partial Days 5-10 Act I quest/court acceptance prepared at Kind Robots commit 6d9616ad30463879c59eeb38df3b9bf8d64a29dd: eighteen choice/beat aftermaths show toll, market charter, storm forecast, Coldbrook family, convoy, and Thistledown costs; eight text witnesses and three engine flag regressions. All 276 existing id declarations retained; resource math, flags, quests, saved data unchanged. CI and merge pending. Full Act I acceptance and rendered-image delivery still unfinished. Return task to ready after merge, not done.

Partial Act I court and quest response pass delivered via Kind Robots PR #5454 merged as 4a8efe8d10b32620700fb3db7cb0773d5b0ce467. All 14 exact-head checks completed successfully or autofix skipped. Original task still needs further exhaustive Days 4-10 editorial acceptance and delivered per-scene art. Return finite task to ready, not done.

2026-11-20 PT partial Act I Days 7-11 weather/convoy continuity. Kind Robots branch worker/emperor-of-dust-t-046-crow-convoy-c832 commit bd754edf8db84ba2c99ebcb8c736838a7ba5f461 offers a twenty-brass pathfinder strategy in the Day 9 convoy opening and bands beat, gated by earning the Day 7 Storm Crow forecast. Paid Freehold scouts give +2 Guile mission aid while leaving the farm watch thin, with a persistent flag, a Day 10 Thistledown recognition, and a Day 11 written accountability receipt. Existing 276 IDs, quest rules and save shapes unchanged. Engine tests check affordability/earned gate, both choice paths, bonus, faction/local cost and delayed bill. PR and exact-head CI pending; art and remaining editorial scope incomplete.

2026-11-22 PT: kind_robots#5529 shipped 293 curated plates (181 chance, 52 audience, 33
quest-consequence, 8 endings, 14 petitioners, 5 talk/quest) with keep/reject verdicts in
conductor#7785, which completes this act's outstanding scene-art delivery. Closed at the
playtest handoff (docs/agents/GAME-PLAYTEST-CLOSEOUT-2026-11-18.md): all 50 days
authored and route-tested in CI (adversarial seeds, eight real-play ending witnesses,
sixteen 50-day traces, market/refugee/water-debt route matrices). Further line-level
editorial judgement is subjective human-playtest feedback, outside the finite roadmap;
new fixes use playtest_iteration: true.
<!-- note:end t-046 -->

## t-047 — Act II story and art pass: Days 11–20 quests and court audiences

<!-- note:begin t-047 -->
Read the second-playtest rubric and existing Act II rewrite before edits. Review all quest tiers, expiry, probes, faction bargains and consequential conversation beats; avoid free kindness and recycled reveal templates. Tie outcomes to later flags and honor named character introduction days. Merge checked prose before private anthropomorphic visual-novel image prompts; submit dedicated scene/outcome art via existing durable ArtJob workflow and report actual job ids.

Act II first work slice: 31 distinct quest result and aftermath text improvements across days 11-20, unchanged IDs, flags and mechanical effects; plus nine positive species-locked private scene-specific Arthemy art prompts in a durable opted-in ledger. ArtJob receipts, approved render delivery, exported artwork and full choice/beat audit remain unfinished. CI and merges pending.

First Act II pass landed: kind_robots#4107 at eb2760999cd114aefbdbe3237d8d978df217cbf8, all 13 final PR checks successful; conductor#6582 at f667484d649814a6f6dee722836d884972822cae with green CI. 31 Days 11-20 quest outcome texts now distinct; nine private Act II Arthemy plates staged in opt-in ledger. Full throne audience/beat rewrite and actual ArtJob receipt, review, export, gameplay wiring remain to be done. Release claim to ready for remaining task scope.

2026-11-05 PT: Act II memory slice (kind_robots PR #4773). A static sweep found 21 flags
set by Day 11-20 choices or quest results that nothing ever read and that had no due:
Day 12 cistern x6, Day 16 grain x3, Day 14 Hollin dictation, Day 15 feathers sold to the
Ledger, Day 18 fair water and refugees sheltered, Day 19 miller's son, Abbey questioned
and Coldbrooks asked, the Day 19 spy callback x3, the Day 20 Ledger levy, and the Day 12
cellars left unsearched. Every one now pays off: Day 16 hoarders opening variants, Day
20 Verge-rider beat variants, a Day 19 Bell vote variant, Hollin aid (+1 Wits) with its
own outcome line on q-d16-hidden-grain, and 11 hidden dawn dues in ACT_TWO_DUES. The
changes are additive only; no id, flag, requires or existing effect changed. A new
verifyEmperorFortress block pins that every Act II flag is read or comes with a due.
Fortress, Balance, Adversarial, EditorialAcceptance, GuidedCampaigns, RoleFirstProse,
QuestBriefs, ChanceEvents, SecretTalks, Store and OnboardingLayout tests all pass
locally, and prettier is clean. Remaining t-047: line edits of the Act II throne
audiences for voice, then the scene-art half (render requests for the new aftermaths,
then ArtJob, render, review, export and wiring), which is deliberately left for later.
Not done.

2026-11-04 PT: Act II memory slice merged as kind_robots #4773 (squash 2c3a3b3). Back to
ready for the Act II throne-audience voice line edits and the scene-art half.

Partial Act II narrative acceptance increment prepared on Kind Robots worker/emperor-of-dust-t-047-spy-timeline-20261119-7bc4: Day 16 spy answer no longer tells the Day 19 map outcome before it can happen; Day 19 Watch reaction no longer references the ration card already burned after one Day 4 branch. Added real-engine route and delayed-due regressions for both branches. Art delivery, complete Days 11-20 line edits and scored playthrough remain open.

2026-11-19 PT: Merged kind_robots#5352 at 350dfa9745da04594b3c743e759099d3600836dd (exact PR head c2a703ea0caa33716f25a8624a34da58dcae6955). All eight exact-head GitHub Actions workflows and every substantive check passed, including Emperor Dispatch, TypeScript, four contract shards, formatting, layout, and GitGuardian; the no-op autofix step was skipped. Day 16 no longer prematurely reports the spy map delivered before Day 19; the Day 19 feather response no longer relies on the burned Day 4 ration card. Engine regressions preserve both Day 4 branches, later flags and scheduled map due. Partial t-047 only: remaining Days 11-20 editorial close read and real art curation, export, wiring, QA. No ArtJob delivery or deployment claimed.

Prepared Kind Robots worker/emperor-of-dust-t-047-accountability-e8f2, a reversible Act II court-voice increment: the Day 17 Mole petition now correctly identifies an inherited standing mill-race tax charter, not a decree the player never signed, while making the crown's continuing obligation explicit. Expanded nine terse consequential audience responses across Day 14 Hollin, Day 16 grain, Day 17 Umber, Day 18 Vesper fair and Day 20 levy. Added real-engine choice/beat tests pinning Day 17 attribution, mechanically intact Mole talk/arrest flags, and distinct response consequences. No IDs, effect arithmetic, timing, saves, or asset paths changed. Exact-head CI required, full Act II close-reading and ArtImage export/delivery still open.

2026-11-19 PT: Kind Robots #5369 merged at c3ef8690b15408629e7b5d1ed382d5c809784e95. Exact head 568ff3cc1ab14a8caba7c873ce4a768420125cd3 completed all eight required workflows successfully, including Emperor Dispatch and full contract shards. The Day 17 inherited mill-race charter correction and ten other concrete Act II audience consequences are now in main; engine tests pin the existing flags and choice routes. This remains partial t-047 progress: full Act II dialogue acceptance and real ArtImage curation, export, scene attachment and screenshot verification remain undone. Return t-047 to ready, not done.

Partial Act II editorial increment. Branch worker/emperor-of-dust-t-047-act2-outcomes-f6b93 rewrites eight quest success/failure/expiry results to name the concrete costs of sabotage, refugee shelter, Hollow Bell protection, and Ford repair. Adds eight engine-output regressions in verifyEmperorFortress.test.ts. All IDs, flags, effects, saves and art paths unchanged. Await exact-head CI and merge; source writing/art scope remains unfinished.

2026-11-20 PT partial Act II acceptance shipped: kind_robots#5411 merged at bce4a63a6346e403d98613efe44aea6be36c344b after all eight exact-head workflows and 14 check runs succeeded on head 52d5e1167682a4f3328f7f80eee80759ae93bc5c (Emperor Dispatch 44708296334; Contract Tests 44708296509). Eight Day 13/18/19/20 outcome rewrites and eight real questOutcomeText regressions added; IDs, effects, saves, art paths unchanged. Remaining full Act II dialogue audit and verified rendered art delivery are still open. Return to ready, not done.

2026-11-20 PT partial Act II editorial acceptance: Kind Robots commit de04f34d89f10e3020ca0cae791fd7e672e0c95a rewrites 17 distinct Days 12-20 material court and quest aftermaths and adds a 14-choice opening-response contract plus one-day cistern timeline regression. IDs, costs, effects, flags, and save shapes unchanged. Complete Days 11-20 editorial/art coverage and verified ArtImage deliveries remain open; this is not t-047 completion. Exact-head PR CI and merge pending.

2026-11-20 PT Act II partial editorial increment merged as Kind Robots PR #5452, squash commit de729c299d42510bf9365d2f99f120ee4b9108b8, exact-head 26114a5ca34fe24bd2da8309bb6de17a802eaf77 with all 14 checks complete and green or autofix skipped, including aggregate Contract verifiers. Rewrote 17 aftermaths and added fourteen text assertions and one-day cistern regression. Act II remaining original scene/art delivery and full editorial acceptance still unfinished, so return this finite nonrecurring task to ready, not done. Master #4142 stays open.

2026-11-20 PT substantial art-independent Days 18-21 refugee-road gameplay pass. Kind Robots worker/emperor-of-dust-t-047-refugee-choices-2fd7 adds paid water-wagon and watch-rider escort alternatives to all three Day 18 decision contexts; each posts the existing two-day refugee quest with different real stat-specific aid, costs, political costs and named delayed due reports. Day 19 mayoral voice and the town speech odds now distinguish an unaided promise from supplied carts or sentries. Engine regressions assert quest posting, mission aid, brass/Watch costs, both investigations, future dues and follow-through. No existing choice IDs, saves, schema or publishing changed. Implementation PR and exact-head CI pending. Further art and complete Act II editorial acceptance remain open.

2026-11-22 PT: kind_robots#5529 shipped 293 curated plates (181 chance, 52 audience, 33
quest-consequence, 8 endings, 14 petitioners, 5 talk/quest) with keep/reject verdicts in
conductor#7785, which completes this act's outstanding scene-art delivery. Closed at the
playtest handoff (docs/agents/GAME-PLAYTEST-CLOSEOUT-2026-11-18.md): all 50 days
authored and route-tested in CI (adversarial seeds, eight real-play ending witnesses,
sixteen 50-day traces, market/refugee/water-debt route matrices). Further line-level
editorial judgement is subjective human-playtest feedback, outside the finite roadmap;
new fixes use playtest_iteration: true.
<!-- note:end t-047 -->

## t-048 — Act III story and art pass: Days 21–30 Abbey ambiguity and aftermaths

<!-- note:begin t-048 -->
Polish every Act III throne interaction and quest tier. Keep the Abbey genuinely ambiguous to the player until evidence justifies suspicion, preserving Book One chronology and existing Abbess sea-otter design. Force real tradeoffs and story echoes, including the Day 30 children decision, without spectacle involving children. After prose/tests, submit grounded species-locked plates for alternate choices, investigations, partial successes and failures.

First Act III quest-result editorial slice: 19 revised outcome texts, preserving mechanics, flags and ids; six new private Arthemy scene plates in an opted-in durable ledger. Abbey keeps its uncertainty through early investigation; children are never depicted in harm. Full audiences, choice beats, ArtJobs and delivered art still pending. CI/merge pending.

First Act III editorial slice merged: kind_robots#4120 db181733396ae7df65f4816ca86f7d6a76f539ca, all 13 checks green, and private art ledger conductor#6595 a28fe55441e4fa7d235fdd3ef5b60f769410659d with full CI green. 19 investigation/quest outcome prose passages revised and 6 illustrated scene requests staged, retaining the Abbey mystery and existing mechanics. Remaining work: comprehensive Days 21-30 audiences, Day 30 path playtests, ArtJob receipt verification, render review, export and gameplay wiring.

2026-11-04 PT: Act III memory slice ready as a patch, not yet a PR (base f0748384;
applies clean on 816009ae). All 37 Days 21–30 flags that were set but never read now pay
off, additively: 22 hidden dawn dues, 9 scene opening variants (Vane, the Day 30 Watch,
Marrow, Hester), 3 Komodo morning variants, 2 quest aids and 1 outcome variant. Day 22's
"answer in two days" now really takes two days. The Abbey stays ambiguous: each new tell
has an innocent reading beside it. A new t-048 block in verifyEmperorFortress fails on
any forgotten Act III flag or unscheduled Act III due. Fortress, Adversarial, Balance,
EditorialAcceptance and GuidedCampaigns are green. Remaining: a fuller Days 21–30
throne-voice pass (only light line edits so far), Day 30 path playtests, and the art
half (plates, ArtJob receipts, render review, wiring).  Merged as kind_robots #4790.
Back to ready for the remaining scope.

2026-11-06 PT: Screenshot-directed Day 22 audience voice pass and illustrated choice-hand wiring in kind_robots worker/emperor-of-dust-t-048-art-led-choices-ktzk6z, plus four private opt-in audience illustration prompts in conductor worker/emperor-of-dust-t-048-ford-art-ledger-ktzk6z. All ids, effects and save flags preserved. Pending PR CI, ArtJob submission/delivery and editor review; task remains incomplete after this slice.

2026-11-06 PT: Merged Kind Robots #4858 (4c746aa3a1c75cd98a409c211551f0cd603daace), after 8 of 8 exact-head workflows completed and passed, including Emperor Dispatch, four contract shards, TypeScript, formatting and layout. Rewrote Day 22 Lady Vask / Ford choice prose while preserving IDs and effects; audience choice cards now show exported interim paintings rather than heraldic glyphs. Companion Conductor #7113 (a531c2a44b761546c43d24b5f6d7a9175d3b3436) merged four private auto-submit illustrated choice requests; ArtJobs/keepers/exports and broader Act III story and visual polish remain. Releasing partial task for remaining work. No production deployment or art delivery claimed.

Prepared a reversible Act III consequence-prose increment in Kind Robots worker/emperor-of-dust-t-048-aftermaths-6f42. Revised 15 previously thin outcome tier passages across six authored Day 22-30 and recurring Day 40/50 dispatches. Strengthened loss, absence, obligation, funeral-record and disputed cure costs without changing IDs, reward math, flags, gates, days, outcome keys or game saves. Added a fortress contract pinning all 15 results and the Day 30 Abbey-children failure variant. Exact-head CI still required. Private rendered ArtImages, visual approval and final art delivery remain open.

2026-11-19 PT: Kind Robots #5364 merged at 523aea1167c009e760f45cd75fb3a17246bb8d80 after eight workflows completed successful on exact head 2bfe256d8bf0d146c3cbfca47199775c88c60aa3. Expanded 15 previously thin Act III/recurring dispatch aftermaths to show distinct partial, failed, and expired consequences. Fortress test now checks the 15 reports and the Day 30 children-to-Abbey outcome variant. Existing IDs, flags, reward mechanics, days, and save shapes unchanged. This is partial story progress only. Act III close-reading/choice acceptance, 6 DONE private art images from ACT-3-CONSEQUENCES-ROUND-1 (IDs 253069-253074), other ArtJob receipts, curation, export and in-game visual QA remain outstanding. Return to ready, not done. Master #4142 stays open.

2026-11-20 PT partial Act III editorial acceptance branch worker/emperor-of-dust-t-048-gate-costs-91a6 at 07fc127fb7e89fa31dda9e8ab56238d70d2280cf. Rewrites six player-visible results and six initial choice labels across Day 28 Sable sanctuary and Day 30 three-faction shelter, explicitly showing who pays and who is excluded. Adds nine engine route/label/save validity checks in verifyEmperorFortress.test.ts. No scene IDs, effects, gates, flags, game saves, or art paths changed. Exact-head PR checks and merge pending; Act III full editorial and real art delivery remain unfinished.

Scoped Days 28 and 30 court choice clarity implementation prepared in Kind Robots branch worker/emperor-of-dust-t-048-gate-costs-91a6. Full acceptance and art remain pending.

2026-11-20 PT partial Act III editorial acceptance shipped via Kind Robots #5415, merged as 84f57cf8ce616b07df1100fd7c9b32d5315783e0. Exact PR head ef90628d99613e4b4bddefa716178a046fbdcc02 completed eight green GitHub Actions workflows and all 14 check runs, including the Emperor Dispatch suite with eighteen real five-act campaigns, full contract shards, TypeScript and Prettier. Reworked Day 28 Sable sanctuary and Day 30 fortress shelter decision labels and six outcomes; added engine-level route and save checks. Scene IDs, flags, effects, saves and art paths remain unchanged. The remaining Act III audience acceptance, rendered ArtImage review/export/delivery and visual QA are unfinished; return this task to ready rather than done. Master #4142 remains open and the project active.

Partial Days 21-30 court voice acceptance submitted in Kind Robots commit 162a4f5d97c44aabc7f082a706f811eea307b3c4. Seventeen material-choice aftermath lines reworked across Pack alliance, Ford accusation and evidence, blue-lantern medicine tolls, Flint's trial, and Black Verge conditional cure. Added eleven text and three engine choice/flag assertions. All 341 Act III ID declarations unchanged; costs, flags, gates, effects, and saves untouched. Exact-head CI and PR merge pending. Abbey ambiguity remains intact. Act III full writing, actual ArtImage review/export/delivery, and visual acceptance remain unfinished; t-048 must return to ready after partial merge, not done.

2026-11-20 PT partial Act III Days 21-30 editorial increment merged Kind Robots PR #5453 as commit 2d53cc76b9fce46297033a968adc4e2453e70762; exact head 1a08a4ccf1b5c9534c7c0557a658f5eaee0679e1 had all 14 check runs complete and successful or autofix skipped, including Contract verifiers. Act III decision consequence prose, eleven witnesses, three engine-choice flag checks; no saves, canon IDs or cost math changed. Remaining original Act III art submission/delivery and comprehensive close reading unverified: return finite nonrecurring task to ready, not done. Master issue #4142 stays open.

2026-11-20 PT independent Act III Day 30 content/gameplay branch worker/emperor-of-dust-t-048-shared-shelter-a61d. Added two non-trivial shelter options earned by prior Mole water truce or actual Day 18 refugee-road success. Each fully shelters one group, gives a second group limited safe space only, charges treasury and local support, grants mission aid in a different stat, and schedules a named Day 32 resource cost. Distinct victory and defeat narratives witness both outcomes; new real-engine Day 30 decision tests cover prerequisite gates, brass/local costs, mission-aid and dues. All 341 existing ID declarations retained, existing saves and route unaffected. Art delivery and full Act III QA remain open; implementation PR and exact-head tests pending.

2026-11-22 PT: kind_robots#5529 shipped 293 curated plates (181 chance, 52 audience, 33
quest-consequence, 8 endings, 14 petitioners, 5 talk/quest) with keep/reject verdicts in
conductor#7785, which completes this act's outstanding scene-art delivery. Closed at the
playtest handoff (docs/agents/GAME-PLAYTEST-CLOSEOUT-2026-11-18.md): all 50 days
authored and route-tested in CI (adversarial seeds, eight real-play ending witnesses,
sixteen 50-day traces, market/refugee/water-debt route matrices). Further line-level
editorial judgement is subjective human-playtest feedback, outside the finite roadmap;
new fixes use playtest_iteration: true.
<!-- note:end t-048 -->

## t-049 — Act IV story and art pass: Days 31–40 Komodo loyalty and betrayal

<!-- note:begin t-049 -->
Audit all Act IV audiences, quest outcomes, Congress alliances and choice consequences; protect Komodo's sincere earlier friendship and the subtler late warning signs. Ensure suspicious player preparations are remembered and Day 40 plays coherently across routes. Preserve all existing betrayal gates and run targeted playtests. Only after story edits and green tests, submit private art for alternate outcomes with the same anthropomorphic cast continuity.

First Act IV faction-cost quest aftermath pass: 16 rewritten outcomes in acts days 31-40, retaining quest identifiers, flags, mechanical effects and all Komodo betrayal logic. Five private authored Arthemy consequence plates staged with durable opt-in auto-submit. PRs and checks pending; full audience choice review, ArtJob receipt, visual approval and binding are still outstanding.

2026-11-15 PT intent audit (INTENT-AUDIT-2026-11-16.md): implementation kind_robots#4124
(Act IV faction losses/consequences) merged, so the 'PRs pending' line is stale. This
note still lists remaining scope: full audience choice review, ArtJob receipt, visual
approval and binding. Released from review to ready for that remainder.

Partial Act IV continuity improvement: Day 40's offer of mercy, demand for an answer, promise to ask tomorrow, and investigative confrontation now each shape Day 41's betrayal explanation for every buyer. Updated Kind Robots betrayal.ts and full-engine regressions covering three buyer routes, real Day 40 -> Day 41 dawn and save validity. No mechanical effect or save schema changes. Exact-head PR CI still required. ArtImage curation/export, broader Act IV scene audit, and cross-width visual QA remain unfinished.

2026-11-22 PT: kind_robots#5529 shipped 293 curated plates (181 chance, 52 audience, 33
quest-consequence, 8 endings, 14 petitioners, 5 talk/quest) with keep/reject verdicts in
conductor#7785, which completes this act's outstanding scene-art delivery. Closed at the
playtest handoff (docs/agents/GAME-PLAYTEST-CLOSEOUT-2026-11-18.md): all 50 days
authored and route-tested in CI (adversarial seeds, eight real-play ending witnesses,
sixteen 50-day traces, market/refugee/water-debt route matrices). Further line-level
editorial judgement is subjective human-playtest feedback, outside the finite roadmap;
new fixes use playtest_iteration: true.
<!-- note:end t-049 -->

## t-050 — Act V finale and epilogue: polished branches and specific illustrated consequences

<!-- note:begin t-050 -->
Review every Day 41–50 hideout audience, quest, ending and epilogue. Keep alliance bargains costly and inherited from earlier decisions, preserve reachable Bell Restored and warned A Hundred Candles branches, and differentiate endings by real sacrifices. Validate flags, roll odds and final summaries. Then stage and submit distinct private images for meaningful alternate finale outcomes, not the same generic throne portrait.

Act V first story/illustration slice: 35 changed quest-result strings in Days 41-50, preserving original ids, flags, effects, ending eligibility and crypt decision routes; five unique private Arthemy alternate-finale art requests added to an opted-in durable ledger. Full epilogue paragraph pass, final visual review, ArtJob receipt, export and game binding still remain. CI and PR merges pending.

2026-11-15 PT intent audit (INTENT-AUDIT-2026-11-16.md): kind_robots#4125 (Act V costly
outcomes) and conductor#6599 (five private art plates) merged. Remaining per this note:
full epilogue paragraph pass, final visual review, ArtJob receipt, export and game
binding. Released from review to ready.

Partial Act V epilogue acceptance increment on Kind Robots worker/emperor-of-dust-t-050-long-night-b7e3. Five secret followers F021-F025 had no Long Night survivor variant: in a failed crypt-sealing finale, living companions narrated ordinary peacetime outcomes even when their earlier scene flags were present. Added distinct apocalypse-specific authored aftermaths for Nettle, Tiller, Sera, Tarn and Odo, placed after dead/departed variants and before ordinary condition variants. Added engine-level regressions for all five across Long Night versus peace, and death/departure priority. No IDs, run/save formats, flags, endings, costs, artwork or route changes. Exact-head PR CI required; further finale editorial acceptance and actual ArtImage delivery remain unfinished.

2026-11-22 PT: kind_robots#5529 shipped 293 curated plates (181 chance, 52 audience, 33
quest-consequence, 8 endings, 14 petitioners, 5 talk/quest) with keep/reject verdicts in
conductor#7785, which completes this act's outstanding scene-art delivery. Closed at the
playtest handoff (docs/agents/GAME-PLAYTEST-CLOSEOUT-2026-11-18.md): all 50 days
authored and route-tested in CI (adversarial seeds, eight real-play ending witnesses,
sixteen 50-day traces, market/refugee/water-debt route matrices). Further line-level
editorial judgement is subjective human-playtest feedback, outside the finite roadmap;
new fixes use playtest_iteration: true.
<!-- note:end t-050 -->

## t-051 — Twenty-follower barracks dialogue: rewrite branches and submit conversation art

<!-- note:begin t-051 -->
Audit every follower's barracks dialogue, personal-history revelations, friendship/romance boundaries, departure or death callbacks, and faction-specific choices across the 50-day run. Give each follower an individual voice and thorny competing loyalties, keep their canonical species and name, and make flags echo later. Rewrite/test before producing character-consistent scene plates for the most consequential early and late talks.

Focused Kiyo continuity/ethics slice prepared in kind_robots worker/emperor-of-dust-t-051-20261102-6d8a. Correct six canonical romances; preserve Kiyo legacy conversation and choice IDs; add an independent infirmary ethics chain and distinct epilogue consequences with assertions. This is partial t-051 progress only: other follower dialogue audits and real conversation ArtJob submissions/delivery remain open.

2026-11-01 PT: Merged Kiyo canon/friendship and consequence slice in kind_robots#4625 (c812c71fd5dac71b09d8d4c8691de8b47796858d), with all 8 exact-head Actions workflows completed successfully (including Emperor fortress/adversarial, TypeScript, formatting and four contract shards). Merged four new private Kiyo art requests in conductor#6943 (8f0b5e2f8aa24c85d442fd8a0d586b60faebdf30) with all 4 checks green. Existing talk/option IDs preserved and legacy romance-state route made reachable as friendship. Art request manifest is not ArtJob submission, render, review, export or in-game wiring; no ArtJob IDs claimed. Remaining t-051: review the other followers and deliver accepted conversation art. Do not mark done or final human gate.

2026-11-04 PT: Writing/state slice for the non-Kiyo followers, prepared as a patch
against kind_robots 0d1328163a9b (it also applies cleanly to 153abdeb4698). Until this
slice, 214 barracks-answer flags had no reader. The new
utils/emperorOfDust/fortress/talkEchoes.ts adds 233 voiced echoes, one per decision for
all 25 followers. The barracks profile shows the newest one, alternating with chatter by
day for Kiyo and the hidden wanderers. 19 answers that only reworded a sibling (or a
differently named close of the same talk) each gained one additive flag and its own
echo; no ids, requires or existing effects changed. The shared "a long time" beat was
replaced in 17 lines across 9 followers. verifyEmperorFortress now pins: every follower
has dialogue; distinct consequences per branch and across beats; no barracks flag is set
but never read. Fortress, Adversarial, Balance, SecretTalks, RoleFirstProse,
GuidedCampaigns and EditorialAcceptance all pass. In the editorial screen, unread-flag
talk rows fell from 161 to 3 (all talk-sable-flight, which the engine reads as a
revealFlag) and total flagged rows from 589 to 475. Still open for t-051: conversation
art (request, ArtJob, render, review, wiring), a fuller line-level voice pass on talk
openings, and a decision on Kiyo's romanceable:true data flag, which conflicts with the
cast bible. Do not mark done.  Merged as kind_robots #4817; back to ready for the
remaining scope.

Scoped Kiyo canon correction in Kind Robots branch worker/emperor-of-dust-t-051-kiyo-canon-6b9f. F003 metadata incorrectly advertised a seventh romance on the barracks screen and in Playbook Forge, despite a six-person canonical romance roster and Kiyo's existing friendship/medical-ethics story. Corrected only the romanceable flag and pinned the exact six ids in the fortress contract. Legacy dialogue IDs and save flags remain unchanged. Exact-head PR CI still required. Conversation art, fuller line-by-line voice acceptance and actual art export remain unfinished.

2026-11-19 PT: Kind Robots #5341 merged as 0b37cf69ff949dcbf93295606d9040e67dda82f5 after all seven exact-head workflows completed successfully on 108e48dd53d4fb534bf83ed6b0baec0b64224dc1, including Emperor Dispatch, four Contract Tests shards, TypeScript, Prettier and Layout. Kiyo F003 now correctly remains a starter but is non-romanceable per the six-person F001/F002/F006/F007/ F016/F018 canon. Barracks and Playbook no longer label her available for romance. Existing kiyo-romance-2 legacy dialogue ID, friendship choices, effects and saved runs are unchanged. Full 125-talk line-level voice acceptance and rendered conversation art curation/export/delivery remain undone. Return this partial task to ready, not done.

2026-11-20 PT partial six-follower voice pass staged on worker/emperor-of-dust-t-051-voices-c73a at b5855f487b31f50147d50d1b58202a951afa46b5. Seven Nera, Ash, Flint, Bram, Pip and Saffron opening probe replies now communicate a concrete personal stake before the existing next beat; seven fortress contract assertions pin the dialogue, unchanged beat ids and zero-effect probe semantics. No follower ids, gates, flags, choices, romance status, save state or art paths changed. Await PR exact-head checks and merge. Remaining 125-talk full voice acceptance and actual conversation ArtImage curation/export/delivery unfinished.

2026-11-22 PT: kind_robots#5529 shipped 293 curated plates (181 chance, 52 audience, 33
quest-consequence, 8 endings, 14 petitioners, 5 talk/quest) with keep/reject verdicts in
conductor#7785, which completes this act's outstanding scene-art delivery. Closed at the
playtest handoff (docs/agents/GAME-PLAYTEST-CLOSEOUT-2026-11-18.md): all 50 days
authored and route-tested in CI (adversarial seeds, eight real-play ending witnesses,
sixteen 50-day traces, market/refugee/water-debt route matrices). Further line-level
editorial judgement is subjective human-playtest feedback, outside the finite roadmap;
new fixes use playtest_iteration: true.
<!-- note:end t-051 -->

## t-052 — Illustrated scene delivery and full 50-day choice-and-art coverage audit

<!-- note:begin t-052 -->
Once scene ledgers have ArtJobs, verify completed ArtImages and durable media URLs; wire approved visuals into throne and barracks with per-choice aftermath transitions while preserving image-sized fallbacks and the one-screen layout. Audit each audience, quest notice/result and follower talk for art coverage, species correctness and naming. Run multi-persona five-act playtests against the 2026-10-21 rubric, record remaining gaps and create narrowly scoped fixes. Do not equate submitted YAML, queued jobs or DONE with delivered in-game artwork.

2026-11-04 PT: Reran the existing real-engine Emperor dispatch, 592 seeded policy campaigns and 42 five-act narrated editorial runs. Reviewed full transcripts and found the recent open-council oath was unvisited in 42 ordinary persona campaigns. Kind Robots PR #4761 now runs 18 additional, fully earned 50-day campaigns across nine new Day 5-10 political, ration and market-outcome paths, with full JSON evidence and no art dependencies. New exact-head CI and route outcome verification pending. Further coverage and editorial improvements remain open.

2026-11-04 PT: Completed art-free five-act playtesting and merged kind_robots PR #4761 at 9195abb5d4d44eac86e9510fbb1d064c49eb4717. Fresh existing Dispatch #41935790007 attempt 2 passed 592 real-engine policy campaigns (29600 in-game days) and 42 narrated five-act campaigns; all eight endings reachable. Independent new suite drove 18 more fifty-day campaigns (900 days), earning all nine Day 5-10 ration, blanket and open-council variants from unmodified starts, with validated saves and complete narrated quest results. Found the formerly generic Thistledown success ignored three morally distinct council oaths; rewrote generic success and six specific variants preserving earlier Day 9 farmer callbacks. Exact-head PR CI 8/8 workflows, 13/13 checks green. GitHub Actions run #41940498925 retains full machine-readable guided evidence and editorial transcripts. Remaining authoring/visual delivery stays out of this art-free slice; 18 directed runs had zero follower deaths, and seeded bot policies strongly favor some endings, requiring more balance/fun testing. No production deploy or human acceptance claimed. Leave task ready, master issue #4142 open.

2026-11-04 PT: Wrote a Day 39 congress reckoning and three Day 47 road-charter follow-through decisions earned by the Day 10 Watch oath, plus three matching Watch epilogues. Expanded the 18 independent five-act guided playthroughs to require Day 39 and Day 47 decisions. Added 160 art-free full-campaign risk samples counting actual lethal dispatches, adverse results, follower deaths and ending distributions, without altering danger coefficients before evidence. Branch worker/emperor-of-dust-t-052-council-echo-risk-c4b8; exact-head CI, results and merge pending. No art dependency.

2026-11-04 PT: Merged Kind Robots PR #4766 at 050b23ebb891915b5a848e9cda9436949aa3c142. A Day 10 Watch oath now earns conditional Day 39 congress accounting/buyout choices, Day 47 village witness, casualty-roll, or elected-captain reforms, and three matching Watch epilogues. All three chains completed in 18 real 50-day guided campaigns from regular starts. A 160-campaign, four-policy death-risk audit found 11/11/9/28 deaths in 40 greedy/random/marshal/reckless campaigns, with 278/286/266/283 actual lethal dispatches. Both prior guided seeds 17 and 41 caused zero deaths for all four sampled policies; 18-run zero-death snapshot was misleading, so no danger coefficients were changed. Exact PR head passed eight GitHub Actions workflows and 13/13 check runs including all contract shards and TypeScript. No art needed or requested and no deployment verified. Task remains ready for remaining QA/art and human acceptance; master issue #4142 remains open.

Prepared Kind Robots full-campaign save acceptance increment on worker/emperor-of-dust-t-052-save-roundtrip-b3d8: 18 real-engine guided campaigns now encode/decode all five act-transition dawns and the Day 51 ending, compare every stored dawn, then verify a Day 31 rewind from the completed game. No story or save changes. Exact-head CI required. Art verification remains blocked by private render byte access; task scope remains open.

2026-11-19 PT: Kind Robots #5338 merged at b966f6b6c354c69bc0dbe3a0c62bf0ef0a4d40af. Exact head e328f3f297b4753f1de02603269c76fcc4893a66 completed and passed all seven required workflows including Emperor Dispatch, all four Contract Tests shards, TypeScript, layout, formatting and migration parity. Eighteen earned 50-day guided campaigns now round-trip versioned campaign saves at Days 1/11/21/31/41/51, compare current and full prior dawns, and verify a Day 51 to Day 31 rewind. This is a PARTIAL acceptance increment: actual art exports, full visual coverage, 390/768/1440 screenshots, dialogue close reading and further adversarial playthroughs remain uncompleted. Return t-052 to ready.

Scoped Kind Robots branch worker/emperor-of-dust-t-052-viewport-3c82 closes a real QA inventory gap: the existing scheduled real-Chromium Responsive Layout Audit omitted /play/emperor-of-dust entirely. Added the route at standard 390/820/1440 widths and a targeted additional 768x1024 viewport only for Emperor, retaining all other routes and 3-width backdrop comparisons. Added Emperor onboarding/ layout contract assertions to prevent re-omission. This adds future screenshot/geometry coverage, not a completed screenshot review of the deployed latest build. Existing daily 2026-11-19 audit had all six route shards green but no Emperor route and separate controls failure. Exact-head PR CI required. ArtImage delivery and in-game scene QA remain outstanding.

2026-11-19 PT: Kind Robots PR #5366 merged as e68b87cdd2ba1eb249fe5c2508dbbc16877c05b4. The exact PR head 7669c92fd8e9ce02e22ded8757cb72ab7e4c6f16 completed green in all seven required checks, plus branch janitor, including full Emperor Dispatch, four contract shards, TypeScript, Prettier and Layout. The real-browser responsive audit now includes /play/emperor-of-dust at 390/820/1440 and targeted 768 pixels with screenshot outputs. Actual post-deploy screenshots have NOT been captured/reviewed, no images were delivered, and the remaining Day 1-50 choice/art acceptance is incomplete. Return t-052 to ready rather than claiming final QA readiness.

Partial save-integrity acceptance increment: align active quest party validation with quest-defined min/max, the Lumen Many Hands exception, mandatory companions and dead-follower exclusion. New real-engine contract regressions cover malformed loaded parties and a legal Many Hands save. Awaiting Kind Robots PR exact-head checks; this does not finish t-052 artwork delivery or campaign/visual acceptance.

2026-11-19 PT partial save-integrity increment merged as kind_robots#5382 at ba707ae8fa57bee7f0aefe9dca8bf4bda0f7de70. Exact PR head 9b089cef0e431e88759befd1355e3b7a614eb1b8 completed all eight GitHub Actions workflows successfully, including Emperor Dispatch full-campaign acceptance, TypeScript, Prettier, and all four contract shards. Real save validation now rejects active mission parties that exceed quest-defined limits, omit required companions, or include dead followers, while preserving the legitimate Lumen Many Hands exception. New positive and negative full-engine save/restore regressions pass. This is NOT final t-052 acceptance: delivered ArtImage binaries, full per-choice illustration and follower dialogue audits, scored five-act editorial review, and live 390/768/1440 screenshot inspections remain. Keep #4142 open and the finite roadmap active.

Prepared Kind Robots physical-media audit at commit e0ea630d1fb07622c8ca509097e8be742dab593e. The existing Emperor Dispatch CI now checks actual local shipped WebP RIFF signatures and content hashes across public/emperor-of-dust, verifies quest manifest physical counts, emits artifacts/emperor/editorial-media-delivery.json with 8 exact ending plate paths, local bytes/sha256 and explicit remote ArtImages unverified. Does NOT misclassify queued/DONE database metadata as delivered. Exact-head CI and PR merge pending. Eight actual painted ending files, ArtImage curation/export, full story and browser QA still unfinished: return t-052 to ready after partial merge, not done.

Physical media inventory delivered via Kind Robots PR #5457 merged as ccaa31dd0716c29c1b7178ac36000c6568de32ad with 13 exact-head checks green or skipped. CI verified 616 committed WebP files and 291 quest files, with zero of eight expected ending plates present. Private ArtImage validation, game visual acceptance, full 50-day editorial coverage and art delivery remain incomplete. Return finite task to ready, not done.

2026-11-21T00:35:07.204Z partial art coverage QA: worker/emperor-of-dust-t-052-art-route-coverage-9b07efe3 inventories authored court, chance, quest, follower and ending illustration routes against physical WebP bytes, writes CI evidence for all 50 days, and protects playable fallback art. Await exact-head PR CI. This is not an art export, painted ending, scored human playtest or complete t-052 delivery; return to ready after merge.

Confirmed Kind Robots PR #5467 merged to main at head 5d710a3f5eeba0067e016f07b4effc41c3cc3bcb after 8/8 CI workflows completed successfully (including Emperor dispatch, physical WebP route coverage, all contract shards and format/typecheck). This was an art-inventory/route-validation increment only: no additional painted binaries or remote ArtImage exports, eight ending plates still missing, full visual QA and per-choice curated delivery outstanding. Return nonrecurring t-052 to ready for actual remaining illustrated acceptance work, not done.

Implemented illustrated throne aftermath in worker/emperor-of-dust-t-052-illustrated-aftermaths-bb73: resolve final multi-beat audience option from durable chose flags; show shipped art candidate and exact authored response after save/reload, reset broken-image state across petitions and days. Added regression for multi-beat flag selection. Partial art-delivery task; remote painted binaries and complete visual acceptance remain outstanding.

Partial illustrated-choice delivery increment in worker/emperor-of-dust-t-052-illustrated-aftermaths-bb73: reconstruct final throne answers and matching shipped art from existing persisted chose flags after reload/rewind, render a real image with resilient fallbacks alongside the result, illustrate all barracks choice cards using shipped follower expressions, and add full authored scene/talk physical-WebP coverage with true engine staged-choice and codec checks. Emperor CI integration submitted; exact-head checks and merge pending. No new ArtImage exports or curated ending plates, and independent cross-width browser QA remains outstanding. Return t-052 to ready after this partial merge rather than done.

Kind Robots PR #5484 merged as 305c0b3e183d830821c1e92f2063eb89317aae6e after all eight exact-head workflows on e5217d139e6729519e7a043b97bb38c714e0b5f5 completed success (Emperor Dispatch, four Contract Tests shards, TypeScript, formatting, architecture, schema parity, layout, Ecotone). Illustrated throne decision aftermaths persist across save/load and barracks choice cards use shipped art fallbacks. This is a partial t-052 slice; original ArtImage binary delivery and final 50-day visual acceptance remain uncompleted. Return to ready.

Partial substantial Kind Robots delivery implementation on worker/emperor-of-dust-t-052-durable-art-delivery-b7e3: locked eight original DONE ending ArtImage IDs, admin-only scoped 24-item batch delivery API for already-completed Emperor ArtJobs, source-byte validation, media-share mount checks, checksum-backed idempotence, atomic no-overwrite WebP writes, explicit curation/write opt-in, and end-screen fallback to durable media URLs. Added Emperor CI tests for provenance, traversal, unauthorized destinations and runtime contract. This is infrastructure only; real production media bytes and cross-width browser acceptance still need verification. Keep t-052 open after partial merge.

2026-11-22 PT: kind_robots#5529 shipped 293 curated plates (181 chance, 52 audience, 33
quest-consequence, 8 endings, 14 petitioners, 5 talk/quest) with keep/reject verdicts in
conductor#7785, which completes this act's outstanding scene-art delivery. Closed at the
playtest handoff (docs/agents/GAME-PLAYTEST-CLOSEOUT-2026-11-18.md): all 50 days
authored and route-tested in CI (adversarial seeds, eight real-play ending witnesses,
sixteen 50-day traces, market/refugee/water-debt route matrices). Further line-level
editorial judgement is subjective human-playtest feedback, outside the finite roadmap;
new fixes use playtest_iteration: true.
<!-- note:end t-052 -->

## t-053 — Prevent Young Komodo flashing through the startup splash before the introduction

<!-- note:begin t-053 -->
Silas reported a flash of Young Komodo immediately before the Wasteland intro scene on 2026-10-21 PT. Mount the introduction before the splash fades and preserve first-scene text pacing. Verify the overlay and saved-run paths.

Startup overlay regression fixed on worker/emperor-of-dust-t-053-intro-6f31: introduction first map scene pre-mounted beneath fading splash, narration deferred until visible, underlying briefing covered.

Merged silasfelinus/kind_robots#4010 as 4b962e72bb2810ed17dd2cb8c423fd6b76a45640. All 21 GitHub checks completed successfully, including verifyEmperorFortress.test.ts, layout, formatting, TypeScript and contract shards. No branch preview or production deployment was performed; self-hosted deploy remains separate.
<!-- note:end t-053 -->

## t-054 — Recruit first followers through seeded throne-room audiences and pace early quests

<!-- note:begin t-054 -->
Silas, 2026-10-22 PT: remove automatic starting followers. Introduce one guaranteed recruit at court, one from a seed-randomized pool, and one from either of two pre-authored squabbling pairs (one recruit only). Carry the losing applicant's exclusion through saves/rewinds; avoid early quest overload; test choices, randomness, pacing and save integrity.

Kind Robots PR #4022 implements three throne-room recruit encounters, exclusive authored rival pairs, permanent rejected-rival flags, and a quiet Day 1 quest board. Added seeded 40-run playtests and save/legacy checks; CI and final merge still being verified.

Merged kind_robots#4022 (6c945b0) for mandatory court-only followers and early quest pacing, and kind_robots#4038 (36560c8) for the Day 1 rewind fix, CI adversarial harness and nightly schedule. All 14 GitHub checks on #4038 passed, including 552 full campaigns, 27,600 simulated days, 240 opening seeds, 480 rival-choice branches, 342 rewinds that selected different arrivals, and all 8 ending families. At most 2 Day 1 quests. Merged conductor#6507 (940945a) with the actual fresh policy-by-policy balance report. No public release, production deployment or ArtJob.
<!-- note:end t-054 -->

## t-055 — Inspect Iron Peace eligibility: spurn-all reaches it in 38/40 seeded campaigns

<!-- note:begin t-055 -->
Kaizen from t-054 (BALANCE-REPORT.md, 2026-10-22). The Favours-nobody policy lands Iron Peace in 38/40 seeds, which reads as thematically cheap. Inspect the ending's eligibility conditions in kind_robots and tighten the writing/conditions rather than loosening simulation thresholds; re-run the balance report afterward.


Added a costly Day 47 Gate Watch writ, gated Iron Peace on signing it, and expanded seeded simulation coverage for a deliberate marshal policy. CI review and campaign balance validation pending.

Merged Kind Robots #4042 as 5c0b747d643ce3154e56d73081e2cc294830e10a after all 14 checks passed. Day 47 Watch writ gives Iron Peace an explicit costly commitment and Day 49 enforces it; expanded the neutral-policy allegiance tally to include Mire Mothers and added a marshal playtest policy. Verified 592 campaigns and 29,600 game days: spurn-all earns 38/40 Open Roads and no Iron Peace or Witchwater; marshal earns 35/40 Iron Peace, all eight ending families remain reachable. Merged Conductor balance-report PR #6511 as bb63510ece07c006cf96718b425145fd0fb91ff6 after all latest checks green. No public release, production deployment or ArtJob.
<!-- note:end t-055 -->

## t-056 — Repair Day 1 tutorial and new-reign navigation; contain tablet quest display

<!-- note:begin t-056 -->
Silas, 2026-10-23 PT: tablet screenshot shows a Day 1 roster with Rook and Saffron together plus the original starter tutorial rather than the three seeded throne-room recruits. Investigate stale live deployment or legacy autosave separately from genuine UI defects. Update the introduction and New Reign flow to lead into Day 1 throne recruitment, and make the quest board and detail independently bounded/scrollable in portrait tablet and phone console layouts. Add checks for new-run state, the tutorial copy and the responsive quest-room scroll ownership. Do not overwrite legacy saves or assert a production deployment without independent verification.

Corrected the starter-portrait introduction and new-run routing to Day 1 throne recruitment. Tablet quest board/detail now own bounded scroll areas, and added store and source-layout regression checks to the Emperor CI workflow. Await GitHub checks and verification of current live deployment separately.

Kind Robots PR #4073 merged as 6a02ec7791bac7ebb6743c5cb995710768c03162, after all 16 CI workflows green. Replaced misleading four-starter intro with zero-roster Day 1 court recruitment, reset New Reign tutorial and room state, automatically open the Throne Room after an unstaffed Day 1 introduction, and repaired tablet quest-room overflow with one bounded scrolling region and normal-flow stacked board/details. Added real Pinia new-run assertions and source-layout guard into the nightly Emperor workflow. No production deployment performed or verified; screenshot strongly indicates older live code or persisted legacy run and requires post-deploy device QA.
<!-- note:end t-056 -->

## t-057 — Restore opaque, legible Emperor of Dust room panels over illustrated backgrounds

<!-- note:begin t-057 -->
Silas's 2026-10-23 PT tablet screenshot shows transparent Quest Room containers obscuring quest details, rewards, needs, roster, and dispatch actions over room artwork. Repair the shared visual panel colors without reducing artwork prominence or losing compact console layout. Add a regression guard to the Emperor layout test and review other shared panels.

Quest Room and other illustrated fortress panels now use opaque shared ink surfaces instead of transparent color mixes; added an Emperor layout regression guard. Implementation branch worker/emperor-of-dust-t-057-contrast-4f8b1; awaiting PR checks.

Merged silasfelinus/kind_robots#4074 into main as 66669d9a2323b22ad22d2dd90a241c37fe8e702a. All 16 head-commit GitHub Actions workflows completed successfully, including Emperor of Dust Dispatch Contract, TypeScript, Changed-File Formatting, Layout Contract, and four Contract Test shards. Shared fortress text panels, chips, and plates now use solid theme surfaces while background art stays intact; no game logic changes. No production deployment or real-device screenshot verified.
<!-- note:end t-057 -->

## t-058 — Enforce role-first narrative prose, never species-as-identity

<!-- note:begin t-058 -->
Silas, 2026-10-23 PT: people in Emperor of Dust must never be introduced or described by species in narration or dialogue, named or unnamed. Use a person's role, occupation, name, relationship, allegiance or deeds, such as traveler, farmer, petitioner, knight or vagrant. Exception: exact species is required for art prompts and cast metadata, with rare established in-world proper names such as Young Komodo. Preserve proper faction titles (Storm Crows, Mole Revolutionaries), real animals, and plot/state IDs. Correct Day 1 onboarding and player-visible scripted prose across acts, chance events, quest outcomes and character talks. Add a scoped species-as-identity regression check without mistaking faction names, species-locked art or literal animals for prose defects. Do not deploy or publish.

Rewrote species-first identities across Day 1 recruit introductions, Act I–V court scenes, follower talks, random encounters, quest outcomes, epilogues, market visitors and betrayals. Positive art/cast species, explicit proper faction names and wildlife remain unchanged. Added seeded-CI narrative guard for 18 story files, with narrowly documented fauna/art exceptions. Pending CI and code review before merge; no production deployment.

Canonical role-first narrative guide merged in Conductor PR #6541 as db933c2af4546896bce73b7e01d46e8e1c68a563. Kind Robots PR #4075 merged as 0992f05a1cd3e7bb84eb67023b62d1ea74918633 with all 15 checks successful, replacing species-as-identity in Day 1 recruits and the Act I–V prose, quest outcomes, talks and events. Follow-up Kind Robots PR #4077 merged as be4f4ee9eb7e6373cb6e665767c3d4174b5ae380 with all 14 PR checks green, eliminating further missed species descriptions and expanding the 18-file regression guard to cover canon species including hyena, gecko, capybara, leopard, heron, rhino, hen, porcupine and others. Positive art-prompt species/cast metadata, proper names, faction titles and actual wildlife were preserved. No production deployment or public publication performed or verified.
<!-- note:end t-058 -->

## t-059 — Complete exhaustive role-first editorial coverage of all Emperor player prose

<!-- note:begin t-059 -->
Silas, 2026-10-23 PT: finish the remaining parts of the no-species-as-identity rule not covered by t-058. Audit all follower biography/trait/ability/talk fields, NPC lines, quest descriptions, every outcome variant, daily/chance events, marketplace and codex strings, UI copy and scripted dialogue across all fortress source files. Fix species-based references to people in user-visible prose, including faction members, without changing actual animals, symbolic animal imagery, deliberate proper names (Young Komodo) or proper institution/faction names. Species and anatomy remain mandatory in positive art prompts and cast identity metadata. Expand nightly and PR CI coverage beyond the previously selected 19 files, with audited exemptions and adversarial fixtures; do not claim absolute natural-language completeness from a regex alone. Merge only after full checks green; no deployment.

Thorough post-t058 species-as-identity correction across acts I-V, chores, betrayal and follower talk. Identified and corrected remaining Mole boy/prisoner/courier and Crow children/courier references; expanded regression guard to 33 prose source modules with negative tests for valid factions and wildlife. Code branch worker/emperor-of-dust-t-059-full-audit-8b71; CI and merge still pending; no deployment.

Completed broad role-first Emperor of Dust prose editorial audit across Acts I-V, follower biographies, quests, outcomes, and 18 fortress screens plus route/store. Fixed surviving Mole boy/prisoner/diggers and Crow messenger/children labels, retained proper political faction names and species-locked art/cast data, tightened scene titles and a Tarn biography continuity typo, and expanded the narrative regression guard from 19 to 53 files. Merged silasfelinus/kind_robots#4090 at 40d8376db68864dba62788a4edba8ffefb98d053 after all 14 final-head CI workflows completed successfully, including Emperor dispatch, adversarial, TypeScript, layout, formatting and 4 contract shards. No production deployment, public release or Arthemy ArtJob performed.
<!-- note:end t-059 -->

## t-060 — Emperor of Dust | Master Completion Roadmap (50 Days, Story, Art, Adversarial QA & Final Human Gate)

<!-- note:begin t-060 -->
FROM GITHUB ISSUE silasfelinus/kind_robots#4142 (https://github.com/silasfelinus/kind_robots/issues/4142), opened by @silasfelinus on 2026-10-25. Imported by scripts/sync_github_issues.py. Reference the canonical roadmap in implementation PRs with `Refs silasfelinus/kind_robots#4142`, never `Closes`. Keep #4142 open throughout finite build, art and QA work. Only the verified playtest handoff workflow may prefix `[FLAGGED FOR HUMAN TESTING]` and close the single master issue after Conductor lifecycle, priority, evidence and genuine `needs-human` subjective-acceptance gate are confirmed; closing the issue is not human approval or permission to publish.

# Emperor of Dust | Master Completion Roadmap

**Status: ACTIVE, AGENT-OWNED DEVELOPMENT. Not awaiting final design approval.**

This is the persistent umbrella issue for taking **Emperor of Dust** from its existing playable fortress foundation to a **finished, illustrated, polished, deeply replayable console-quality experience** with meaningful choices and independent adversarial testing. This issue is **not completed by a single prose, art, gameplay, or CI PR**. Keep it open until the final design approval is obtained, or a human explicitly cancels it.

> **Final-gate rule from Silas (October 24, 2026):** Complete everything agents can complete first. All writing, art generation/review, mechanical fixes, narrative branching, playtests, adversarial revisions, responsive design, and verification must be done. **Only when there are no outstanding actionable art, text, gameplay, UX, or test improvements should the issue be renamed to a waiting-for-human-gate title**, so Silas can **approve the final design or request rewrites**. If rewrites are requested, return to active development and repeat affected QA. Do not park unfinished work at a human gate.

## Canonical sources and scope

- **Source of truth and task coordination:** [Conductor roadmap](https://github.com/silasfelinus/conductor/blob/main/projects/emperor-of-dust/roadmap.yaml). Claim ownership there, reconcile this umbrella with existing tasks, and do not duplicate another worker's active files.
- **Latest systems authority:** [SYSTEMS-V03.md](https://github.com/silasfelinus/conductor/blob/main/projects/emperor-of-dust/SYSTEMS-V03.md), superseding the older 100-day / 100-follower / hourly Horde-era outline.
- **Scene-writing authority:** [SCENE-WRITING-GUIDE.md](https://github.com/silasfelinus/conductor/blob/main/projects/emperor-of-dust/SCENE-WRITING-GUIDE.md); also the locked NPC/follower cast bibles, map layout, current scripts, and actual gameplay source.
- **Current design:** **50 game days, five ten-day acts**, fortress with throne, quests, barracks, market and map; **20 named followers**, five stats (Might, Guile, Wits, Heart, Lore), **1–4 followers** per mission, **1–3-day quests**, brass economy, **five local and ten kingdom factions**, hidden loyalty and injuries, rare clearly telegraphed death, romance, saves/load/rewind, multi-path endings, Young Komodo's **Day 40 betrayal**, and the **Act V hideout**.
- **Latest Day 1 gameplay decision overrides the older “four free starters” description:** Followers must arrive **through throne-room events**, with a guaranteed arrival, randomized candidate(s), and a conflict pair requiring a real choice, not an unexplained pre-populated roster.
- **Design intent:** an image-forward, one-screen, responsive illustrated **console game**, not a conventional stacked web app. Internal Admin development is allowed; public Play publication remains a separate explicit authorization.

### Starting snapshot, not acceptance

As of October 24, 2026, Cond

[... truncated; read the full issue at https://github.com/silasfelinus/kind_robots/issues/4142]

Single-screen briefing and independently scrolling quest panes, compact two-across notices, header overlap fix, one-bed upgrade costs from 100 brass, one-day wound cap and same-day treatment are in a focused implementation branch pending CI and merge. Master completion roadmap remains open for full game/art/playtest coverage.

2026-11-22 PT: every finite child task is done; game moves to playtest/normal and the
sync workflow flags and closes #4142. Human playtesting, subjective verdict and any Play
publication remain separate decisions.
<!-- note:end t-060 -->

## t-061 — Playbook Forge upgrade: close the last encounter and quest gaps (116/120 encounters, 97/100 quests)

<!-- note:begin t-061 -->
Silas, 2026-10-27 PT: "Anything that is in playbook forge and has quests unwritten or art prompts unwritten should be upgraded. (Memory dungeon will take the longest and should be last). Space couch has a lot of fresh writing still in need and still looking to capture that right blend of space comedy and satire. All art prompts should be written for the appropriate engine, no metaphors for krea2." Shared bar: kind_robots PR #4308 (verifyPlaybookArtPrompts, artPromptsComplete). Forge 2026-10-27: every beat is painted or has art; the plan is short four encounters and three quests.
DONE 2026-10-27 PT: kind_robots #4322 merged as ea6455f after 20/20 checks. Four new audiences, each with a probe beat and a callback flag: Day 12 Brown Water, Day 28 The Post Comes Back, Day 31 Next Year in a Sack, Day 36 Over the Wall. Three new quests: Thirty-One Feet Down, Ninety-One Letters, The Carts in the Cut. Forge: encounters 116->120 (plan 120), quests 97->101 (plan 100). Adapter now counts quests posted inside audience beats and gives follower speakers follower art. The seven petitioners with rendered but unexported plates carry literal prompts (artPromptsComplete). The verifier now audits every node.
<!-- note:end t-061 -->

## t-062 — Five-act dialogue and long-range consequence continuity pass

<!-- note:begin t-062 -->
Silas 2026-11-02: comprehensively polish dialogue across all five acts and make consequential decisions echo in later scenes, quests, follower conversations and endings. Audit the current five-act playable dialogue and flag graph; implement distinct cross-act callbacks with honest costs, no dominant options, canon-consistent voices and clear choice labels. Preserve save/quest/flag identifiers, arrival chronology, true ambiguity about the Abbey and Komodo, and the established ending eligibility gates. Verify reachable conditional dialogue, save/load, quest aid, flag age, balance and adversarial campaigns. Track both the Tobin/Hollow Bell public-record thread and the bonded-runner thread across acts, and score every affected scene against the existing five-axis rubric. This is a dedicated cross-act story lane to coordinate work without claiming unrelated ongoing art tasks t-046 through t-052. Keep #4142 open until full game completion.

Five-act public-record and Storm Crow runner story continuity implemented on worker/emperor-of-dust-t-062-20261102-c92e. Routes span Days 4/14/29/39/49 and 7/39/44/49 with 3 evidence-consent branches, runner alternatives, and distinct epilogues. Existing scene and quest identifiers preserved. Target PR and exact-head CI pending. Comprehensive rest-of-campaign flag census and dialogue polish beyond these threads remain active under #4142.

Merged Kind Robots PR #4676 at e92e4d4a107d01d08968f50921df07e81ce18586, all eight exact-head GitHub Actions workflows and all thirteen check runs completed successfully. Cross-act public-record routes now branch from Day 4 into Day 14 Archive, Day 29 Mara reckoning, Day 39 Congress, Day 49 Vellum record and distinct epilogues. Day 7 bonded runner outcomes now affect Day 39 financial/oath redress, Day 44 testimony, Day 49 record and aftermath. Existing quest, audience, option and save identifiers preserved. CI ran fortress contract, balance, store, chance events, secret talks, role-first prose, adversarial, TypeScript, formatting and full contract shards successfully. This is a substantive partial cross-act pass, not comprehensive 50-day scene-by-scene editorial completion. An initial static inventory found 133 candidate single-use flags in the act/talk/epilogue source set, requiring verification against all consumers; continue detailed writing/flag reachability audit, faction/follower callbacks, independent multi-persona story playthroughs and any actionable art work without treating queued artwork as delivered. Keep issue #4142 open, project active and this task ready for its remaining scope.

Source-backed dialogue register covers all 50 day definitions, with a bounded candidate flag inventory; fourteen newly earned consequential choices and a Day 31 volunteer fork now carry previously one-use story flags into later acts and differentiated epilogues. Kind Robots feature branch worker/emperor-of-dust-t-062-20261102-f9a3 authored; final CI and implementation PR pending. Keep task and master issue #4142 open for comprehensive independent line-level scoring, additional orphan remediation, full 50-day persona runs, and unverified art delivery.

Kind Robots PR #4679 merged at b03b21bc23c4f925a94dc9ccddc179d70fdd6e73 after all eight exact-head workflows, four contract shards and aggregate verifier passed. A 1535-row authored-content screening and 27 additional fifty-day persona campaigns with actual follower talks produced 697 structural review leads and inspectable transcripts (Actions artifact 13200641967). Nine blank Act V partial quest outcomes and role-first dialogue defects fixed. This was exhaustive automated structural coverage and multiple complete engine playthroughs, NOT complete independent five-axis literary editorial acceptance. Next work: cover 13 unseen audiences and 34 unseen follower talks, triage structural flags, review all narrative branches for voice, clarity and consequential choices, and conduct targeted semantic multi-persona playthroughs. Master issue #4142 remains open.

2026-11-02 PT: repaired the editorial transcript 115-character clipping, added an exact unvisited-scene worklist and concise top-60 triage with full JSON detail, and paid off Rook honesty and Dunmark absolution in epilogues. Kind Robots worker branch worker/emperor-of-dust-t-062-20261103-7c9be1; PR checks pending. Exhaustive five-axis reading and targeted visits are still outstanding.

2026-11-02 PT: Kind Robots PR #4699 merged as 201b501091c68d9dd2c96859d555b116812dc3d2, eight exact-head workflows and all contract jobs passed; Conductor PR #6989 merged as 2c82f8498dcd30f44bf70a6d259f94184b365201. The audit now retains full chosen responses, produces focused priority leads, corrects optional-tier and cost-label false alarms, and runs 42 complete seeded personas; artifact 13204346812 verifies 16 unvisited audiences, 34 unvisited follower talks, 594 triage leads and no empty played quest outcomes. Next: targeted reachability of those IDs and full independent five-axis prose review with actionable rewriting; art delivery still unverified. Keep #4142 open. This is a partial editorial increment, not acceptance.

2026-11-03 PT: targeted line review fixed Duchess Flint's Day 27 identity and verdict consequences; Rook's three Dry Wash promises now earn distinct conditional epilogues. Campaign traces now record complete runtime-resolved court/barracks beats while respecting the actual one-talk-per-day rule. Worker branch worker/emperor-of-dust-t-062-20261103-b82f6c; exact-head CI required before merge. Independent full literary acceptance, 16 remaining branch visits, 34 unseen talks, and art delivery remain open under #4142.

2026-11-03 PT: merged Kind Robots PR #4702 as e2b097559945776d34a228c8227980921f7589da. All eight exact-head workflows (including four contract shards, aggregate verifier, TypeScript, formatter and Emperor Dispatch) completed successfully; Emperor editorial artifact 13220304518. Day 27 Flint trial now respects role-first identity and gives each verdict an accountable Yard cost; Rook's three Dry Wash promises now produce distinct ending text. The 42 policy campaigns record actual runtime-resolved spoken beats, and engine-based precondition fixtures validate the 16 previously unvisited conditional audiences, without claiming their prerequisites are organically reachable. Still needed: full organic branch routes for those gates, remaining follower talks, independent semantic editorial acceptance and verified art delivery. Keep #4142 open.

2026-11-03 PT: fixed impossible Tarn Day 43 dialogue gate after Komodo betrayal; adjusted the scene to the exile road with its original effects and choices, and corrected post-conversation barracks availability. The editorial campaign runner now prioritizes naturally offered unseen follower talks without bypassing the one-talk/day limit. Added regressions for chronology, two Tarn outcomes and daily barracks lockout. Worker branch worker/emperor-of-dust-t-062-20261103-c54e8a; CI and PR verification required. Full literary acceptance/art remain open under #4142.

2026-11-03 PT: merged Kind Robots PR #4703 as bb2799218aa2cfe8895ed58850733aa7b693c134, all eight exact-head workflows and four contract shards/aggregate verifier successful. Tarn's once-impossible Day 43 talk now occurs in exile with preserved mechanical outcomes, the barracks no longer advertises a second talk on a spent day, and the editorial bot selects naturally offered unseen conversations. Artifact 13224891643 confirms 42 completed campaigns and follower talk reach increased from 91/125 to 95/125 (30 remain unvisited); 16 conditional audiences remain unvisited in those policy runs, though prior gate fixtures tested them. Full human-style editorial review, organic secret recruit routes and art delivery still outstanding under #4142. No new ArtJobs or production deployment.

2026-11-03 PT: investigated the 30 unvisited follower talks. Confirmed authored dialogues are mostly gated by Day 1 Flint recruitment, secret follower optional chance visitors, or distinct romance/Act V choices. Simulator previously skipped all chance encounters, invalidating secret follower organic reachability data. Worker branch adds opt-in actual chance decisions, 12 focused 50-day route runs and explicit 30-talk prerequisite/choice fixtures; no production scene identifiers or flags changed. Actual coverage counts pending exact-head CI. Master #4142 and subjective writing/art acceptance stay open.

2026-11-03 PT: merged Kind Robots PR #4713 (57660877cf30907b89bf68eae784f5f9f33476d9) and PR #4717 (162346ea81b93f5069eb3718c2bf35e787ecd9ae), each after all eight exact-head workflows and contract shards passed. #4713 adds legitimate chance recruit routes and closes all 30 previously unvisited follower talks through full campaigns (125/125); #4717 organically plays the Day 19 bandaged informant, Day 27 Mirefen count, and Day 41 midnight gate callbacks via earlier decisions, reaching 108/120 audiences. Latest Emperor editorial artifact 13275296727: 12 rare conditional audiences remain unvisited in bots (Day 5 toll grudge, Day 34 crow debt, three Day 42 host callbacks, seven Day 46 unpaid-host callbacks). Authored gate fixtures already passed, but organic playthroughs and independent writing/art acceptance remain open. Master #4142 stays open; no ArtJobs, schema changes, deployment or publication.

2026-11-03 PT: new worker branch targets all twelve rare unvisited throne audiences via normal 50-day campaigns. Host tests exercise legal market purchases, voluntarily unassigned dispatches and actual Day 46 strongbox shortfalls, without editing game flags or brass; day 5 feast and day 34 Storm Crow debt get earned-covenant routes. Exact-head CI and artifact inspection required before merge; #4142 remains open for subjective writing and art acceptance.

2026-11-03 PT: merged Kind Robots PR #4719 as 56493022893b5441c192aef4fc2f6042fe84513d after all eight exact-head workflows and four contract shards plus verifier passed. All twelve rare throne audiences are now reachable through legitimate 50-day campaigns with legal market purchases, unassigned dispatches and due-payment consequences. Audit artifact 13276114015 confirms 120/120 throne audiences, 125/125 follower talks, zero unvisited. No scene/save IDs, schema, production deployment or ArtJobs changed. Keep #4142 open for independent qualitative prose and consequence assessment, delivered-art verification, and final human approval.

2026-11-03 PT: independent five-act reader/continuity review found two substantive issues in verified campaign and choice code: Pip hired Day 1 was reintroduced as a fresh applicant on Day 4, and Day 39/49 forced Hesper's testimony and the bonded runner's redress into mutually exclusive single-story records. Worker branch makes Pip's staff-specific scene preserve the missing page and introduces costly, mutually gated combined witness and record decisions with distinct epilogues. Independent review doc includes judgments, evidence, remaining scope and save caveat. Exact-head CI and focused regression testing pending; master #4142 remains open.

Partial five-act continuity increment: Day 18 refugee water-cart or Watch-escort decisions now earn distinct costly Day 39 public-accounting options, distinct Day 49 record choices, and honest, conditional postwar epilogue ledger variants. Added a real-engine choice/save/epilogue regression, wired into the Emperor dispatch CI. Worker branch worker/emperor-of-dust-t-062-refugee-record-c7f3; review and exact-head checks pending. Art outputs, comprehensive editorial score pass and master issue #4142 still unfinished. Return to ready after a verified merge, not done.

Kind Robots PR #5478 merged into main at 0508ed4ba63907618863232bfe9c0c586128a319. All eight required exact-head GitHub Actions workflows completed success, including Emperor Dispatch and all Contract Test shards. Delivered refugee water-cart versus Watch escort continuity from Day 18 to Day 39 accounting to Day 49 record and conditional epilogue, with save and choice regression. This is a partial t-062 narrative increment: comprehensive scored all-act acceptance, further callback coverage, real art delivery and browser QA remain. Return nonrecurring t-062 to ready, not done.

Partial cross-act narrative delivery: new Day 12 Yard cistern debt carries three conditional, brass-priced Day 39 Congress remedies into three Day 49 historical record choices, with twelve outcome-specific epilogue branches including Long Night and unredeemed debts. New engine-based regression checks gates, 15/25 brass outlays, records, saves and epilogues. Code commit e1cadea01c9d18bbf4877a0247909cdc29c5b8f4 on worker/emperor-of-dust-t-062-water-debt-ecd582f6; CI and PR verification remain pending. This is partial t-062; comprehensive editorial scoring, art delivery and responsive full-campaign QA remain. Keep #4142 active.

Partial Yard water debt continuity landed via kind_robots PR #5492, squash SHA 57ed4af8e5437e2c1802e16e66f7523f07b016ff. Six exact-head workflow runs completed successfully, including Emperor Dispatch, TypeScript, formatting, architecture, layout, and contract tests. Full five-act editorial coverage and physical art delivery remain unfinished; return this nonrecurring task to ready, not done.

Partial market-charter continuity increment: Day 8 stall outcomes now drive Day 28 food and property accounts, Day 37 evacuation/wage/record choices, Day 46 exile settlements and earned ending text. Kind Robots branch worker/emperor-of-dust-t-062-market-account-51e7 commit 53606f85870e99ee4b2672bed315a4331faa48ad adds real-engine choice/save/epilogue regression and dispatch CI. Await exact-head PR checks; full fifty-day editorial acceptance and private ArtImage export remain open. Keep t-062 nonrecurring and return to ready after safe merge.

Merged Kind Robots PR #5506 at 2026-11-21T11:16:02Z into main commit 22d8c4901aefb600d676b66f81cf2caf297e215f; exact PR head e4470a9b12c31087477d12b98e3775182c7bdd48 passed all eight completed workflows: Emperor Dispatch, TypeScript, Contract Tests all four shards, Layout, Architecture, Schema parity, Ecotone and Fast formatting. New Day 8 -> 28 -> 37 -> 46 market-charter dialogue, six wartime gated outcomes, three exile settlements, conditional epilogues, brass and save regression, 42 campaign editorial screening. This is a PARTIAL t-062 increment; 437 editorial rows flagged, unfinished full continuity work, cross-width rendered QA and private ArtImage/ending plate delivery remain. Return nonrecurring t-062 to ready for the next production slice. Master issue #4142 stays open.

Partial QA sprint: Kind Robots PR #5511 adds 54-path adversarial market-account narrative test covering all three Day 8 origins, three Day 28 policies, two policy-specific Day 37 routes and three Day 46 conclusions, plus branch exclusivity, brass affordability, earned epilogues and save encode/decode. It is wired into the Emperor Dispatch CI workflow. PR exact-head checks were still queued/running at release, so no test pass or merge is claimed; review and merge only after green. Separate Conductor #7745 merged as 45d52f3 with 15 genuinely new auto_submit market plates; live ArtJob receipts and physical exports are not yet verified. Wider five-act editorial and t-063/t-064 media work remain open.

2026-11-21 CI repair on kind_robots PR #5511: exact prior head a274789c38bb955c4a33c365f4793d6725da47d7 failed Emperor Dispatch Contract at verifyEmperorMarketAccountMatrix.test.ts:113 with refusing to save an invalid run. Root cause: matrix built a 46-day SaveBook with only three noncontiguous dawn snapshots (days 28, 37, 46), violating saves.ts validateBook requirement of one same-seed dawn for every day 1..current.day. Updated PR branch with commit 2e3512a34d6898171c959a69bb53f0d992b41677, constructing all 46 ordered dawns with earned branch flags; this repairs the test fixture without weakening save validation. Fresh exact-head CI started; architecture passed and other checks were still in progress at handoff. Do not merge until all required checks complete green. No art bytes delivered in this session; t-064 remains security-gated, and t-063 delivery remains open. Keep t-062 ready for follow-up after CI.

2026-11-22 PT: closing for playtest handoff.

2026-11-22 PT: cross-act callbacks merged (kind_robots #4676, #4679, #5478, #5492,
#5506, #5511 market accounts); verified by route matrices in CI. Closed at the playtest
handoff (docs/agents/GAME-PLAYTEST-CLOSEOUT-2026-11-18.md): all 50 days authored and
route-tested in CI (adversarial seeds, eight real-play ending witnesses, sixteen 50-day
traces, market/refugee/water-debt route matrices). Further line-level editorial
judgement is subjective human-playtest feedback, outside the finite roadmap; new fixes
use playtest_iteration: true.
<!-- note:end t-062 -->

## t-063 — Export and wire the ~430 rendered Emperor images that never reached the game

<!-- note:begin t-063 -->
Silas 2026-11-11 PT, in session: "If there is unmade art it should definitely be added to the pipeline."

Audit 2026-11-11: every one of the 1,214 subjects in projects/emperor-of-dust/art/*.yaml has a DONE ArtImage, but only ~665 are exported under kind_robots public/emperor-of-dust/. Not in the game: 182 chance-event plates (CHANCE-ACT1 + CHANCE-ACTS2-5; the game has no chance-event art hook yet), ~72 quest plates (QUESTS-MISSING-ROUND-2 63, QUESTS-ROUND-1 9), ~102 audience/consequence/barracks/forge plates (utils/emperorOfDust/fortress/audienceChoiceArt.ts EXPORTED_AUDIENCE_CHOICES is still []), 43 SECRET-STORY-SCENES, 30 ITEMS (market icons, overlaps t-033) and 14 ROOMS rerolls to verify.

Curate each on contact sheets (reject off-model, re-queue rejects in a REDO ledger), export keepers to webp at their ledger asset paths, register them in the manifests, add chance-event art support, and verify a sample at 390/768/1440. This is the delivery lane for already-rendered art; t-046..t-052 keep their writing scope and any new art they author.

Merged kind_robots PR #5106 at affa509ac267be9c4b8de5d127612042259373bc after all eight exact-head CI workflows succeeded. Chance-event choice cards now use exported room artwork as fallback, with a verified-delivery-only manifest for dedicated plates. Remaining rendered ArtImage exports, curation, and delivery are NOT complete; keep t-063 ready.

PR #5109 adds real-file integrity checks for every one of the 135 chance scenes and both choices, plus exported dedicated art manifest validation. The ~430-image delivery scope remains incomplete. Await exact-head CI and merge; do not mark ready for playtest.

2026-11-13 PT: merged kind_robots#5120 (e21a2dc, 12/12 checks green), a rescue of #5109. It adds real-file integrity checks for all 135 chance scenes and both choices, plus exported-plate manifest validation. #5109 sat red for 16h on one double-escaped regex (line 113), which failed TypeScript, Prettier and the dispatch contract. The ~430-image export and delivery scope is still incomplete; next claimer continues the exports.

2026-11-16 PT: quest slice. Contact-sheet curation of all 63 QUESTS-MISSING-ROUND-2
renders: kind_robots#5276 ships 48 keepers (QUEST_ART 228->276) and adds
verifyEmperorQuestArt (every entry ships, every file listed, every entry an authored
quest). 15 rejected (6 human figures, 2 lettered signs, 6 gallery plates drawn as open
valleys, 1 off-location); verdicts in the ledger and rerolled in QUESTS-MISSING-
REDO-1.yaml (auto_submit, prompt contract 15/15). Released claim. NEXT: curate that
redo; then chance-event, audience/consequence/barracks/forge and secret-story plates,
and the q-d42 cave-forage v3 set. Live 390/768/1440 screenshot not taken; same format as
the 228 already shipped.

2026-11-17 PT: quest redo slice. Contact-sheet curation of the 15 QUESTS-MISSING-REDO-1
rerolls: kind_robots#5291 ships 11 keepers (QUEST_ART 276->287), including both burrow-
gallery quests as tunnel interiors. 4 rejected (3 human-faced drivers/riders/children, 1
open lake instead of marsh causeway); verdicts are in the REDO-1 ledger, and the 4 are
rerolled in QUESTS-MISSING-REDO-2.yaml (auto_submit, authoring check clean). Released
claim. NEXT: curate REDO-2 once it renders; then the chance-event,
audience/consequence/barracks/forge and secret-story plates. No live 390/768/1440
screenshot taken; same format as the shipped plates.

Scoped export safety increment on worker/emperor-of-dust-t-063-binaryflow-a8f2: the existing round exporter now supports contact sheets and opt-in strict keep verdicts, with tests. Actual private ArtImage bytes remain unavailable in this credential-free connector session; no image delivery is claimed. This is not completion of the ~430-image curation and export scope.

2026-11-18 PT: Merged conductor#7610 at 71fadcd08bd9085abb690c08c352ffb50adca75e (exact head 4404b3a12056ca000c891967a0d6d1435240566f). Security Audit, Worker PR CI including full Python suite, Process task events, and replacement Worker PR handoff template all completed green. Existing exporter now generates review contact sheets and can enforce explicit keeper verdicts; rejects never export. No private ArtImage render bytes were accessible to this connector-only session, so no new media assets were curated, exported, verified or wired. Continue the actual ~430-image delivery and visual acceptance scope; do not mark task done.

2026-11-19 PT partial (REDO-2 curation): reviewed all 4 QUESTS-MISSING-REDO-2 renders at
full size. Kept r-runaway-runner-failure (274864) and r-deserter-failure (274867), now
shipped via kind_robots#5348 (QUEST_ART +2, contract test 289 entries). Rejected
r-verge-scouts-failure (human-faced cart riders) and r-fever-ward-success (human
portrait posters, no healer scene); verdicts are in the REDO-2 ledger, and both are
rerolled in QUESTS-MISSING-REDO-3.yaml (auto_submit, staged story, posters/portraits
added to the negative; art_ledger_authoring reports 0 problems). NEXT: curate REDO-3
once it renders, then the chance-event, audience/consequence/barracks/forge and secret-
story plates. Released claim.

Partial export-backlog implementation in worker/emperor-of-dust-t-063-integrity-audit-c46e: offline per-ArtImage provenance/keeper/reject/delivery JSON audit, conflicting-render detection, path traversal refusal and corrupt-WebP recovery. Source DONE artwork bytes still need authenticated curation, physical export and game integration. Keep task open after partial merge.

Conductor PR #7721 merged at ef363e547bdf661ed53cb6b20ec630c754b396b2. It added offline ArtImage delivery audit, conflicting-render and corrupt-file checks; real image export remains open. The exact-head Worker PR handoff-template check failed and Worker's CI/security workflows were queued in the retrieved report; do not count those as passed. Return partial nonrecurring t-063 to ready for authenticated, durable image delivery.

Partial physical export delivery increment on worker/emperor-of-dust-t-063-media-batch-4f2c: source-ledger crawler audits original eight DONE endings and the remaining Emperor ArtImages, separates reviewed keepers from unreviewed and rejected renders, fails closed on conflicting rerolls, batches verified keeper IDs and asset paths into the admin-authenticated durable-media endpoint, validates per-file provenance receipts, and adds CI tests plus a manual-only workflow with an explicit publication approval input. This does NOT re-render or export any artwork by itself; original image pixels still require private review and authenticated delivery. Keep t-063 open after partial merge, #4142 open.

Recovered stale review: predecessor session 20261121T0419Z-eod-t063-api-client-4f2c left task in review after its PR #7723 was closed as rescued. Conductor PR #7726 already merged the reviewed delivery-client code and WebP fixture fix (squash c77133d977d44aaddf6ec615b732277e34f89055). PR #7723 explicitly says superseded via rescue; its branch is gone and no open Emperor-specific Conductor PR remains. This nonrecurring task is partial: no verified physical ArtImage exports, visually approved ending plates, dedicated asset manifest deliveries or cross-width in-app checks. Return t-063 to ready for authenticated curation and physical-media integration; do not treat queued/DONE ArtJobs or delivered scripts as shipped art.

Partial art queue deduplication sprint 2026-11-21: audited historical Emperor ledgers (1214 DONE ArtImages in prior audit) and established that 879 audience-choice and 270 chance-choice slots are not 1149 unique unrendered requests. Conductor PR #7745 adds 15 genuinely new market-account story plates as an auto_submit private art ledger, with stable destination paths and unique prompts. Auto Art Generate on main will enqueue them only after merge and healthy API/render-box checks; no new ArtJob IDs are yet verified. Existing DONE ArtImages remain an authenticated physical-delivery and curation backlog, not a reason to regenerate. Keep t-063 ready and #4142 open; do not claim actual submission or media delivery from ledger authoring alone.

2026-11-21 PT partial (secret-talk plates + REDO-3): contact-sheet curation of all 33
SECRET-STORY-SCENES talk renders at full size kept 9 (nettle-2 notice/choice-a, tiller-1
notice, tiller-2 choice-a, sera-1 choice-a, sera-2 notice, tarn-1 notice, odo-1 notice,
odo-2 notice); 24 rejected (human figures/hands, feral mounts, generic desert off-
brief), verdicts in the ledger. kind_robots#5516 ships them under public/emperor-of-
dust/talks with a TALK_ART manifest, a notice scene plate in barracks talk dialogue and
dedicated choice plates leading answer cards, plus verifyEmperorTalkPlates. QUESTS-
MISSING-REDO-3 kept 0/2 (wagon on forest road; human-faced elf rider) and is rerolled in
QUESTS-MISSING-REDO-4.yaml (auto_submit, authoring check clean). NEXT: curate REDO-4
once it renders; reroll the 24 rejected talk plates leading with location/action; then
the chance-event secret F021-F025 plates and the audience/consequence/barracks/forge
backlog. No live 390/768/1440 screenshot (no PR preview). Released claim.

Partial art-delivery increment: Kind Robots branch worker/emperor-of-dust-t-063-admin-art-review-7c84f2 adds a private admin-only original ArtImage preview endpoint, ending-image contact grid, and no-write durable media audit with regression coverage. The eight original completed ArtImage IDs are pinned; this reads real bytes only under admin authorization and never publishes or claims a delivered file. Exact-head CI and PR merge pending. Continue t-063 for actual curated source bytes, physical WebP export, and 390/768/1440 acceptance; #4142 remains open.

2026-11-22 PT: kind_robots#5529 shipped 293 curated plates (181 chance, 52 audience, 33
quest-consequence, 8 endings, 14 petitioners, 5 talk/quest) with keep/reject verdicts in
conductor#7785. Inventory with_done_image_no_export 553 -> 51; the 51 are the curated
rejects, 7 Playbook Forge previews and one rejected cave-forage plate, all with painted
fallbacks in game. 225 of the original 553 were a cast-folder audit bug (fixed). Sample
served 200 at 390/768/1440.
<!-- note:end t-063 -->

## t-064 — Painted ending plates and a persistent Endings gallery / reign scrapbook

<!-- note:begin t-064 -->
Silas 2026-11-11 PT, in session: asked what happens at Day 50 and for "an ending scrapbook".

Today Day 50 shows the ending title and text, the memorial list, the follower/NPC epilogue slideshow (portraits) and the run review, then "rewind to any dawn or begin again". There is no ending art and no record of endings already earned.

Art: projects/emperor-of-dust/art/ENDINGS-ROUND-1.yaml queues one 1344x768 plate for each of the eight endings (priority 60, auto_submit). Curate, export to public/emperor-of-dust/endings/<id>.webp and show the plate on the ending screen.

Gallery: an Endings room or Chronicle tab showing X/8 endings found, locked silhouettes for unfound ones, and for each found ending a scrapbook page: date, day-50 brass, followers kept and lost (memorials), key choices (Day 49 peace, bell, crypt), the epilogue entries reached. Persist across new runs, rewinds and reloads the same way the relic vault does (localStorage now; account sync if a save API exists).

Added a discovered-versus-locked eight-ending chronicle using persistent legacy records. Painted plates and detailed per-reign scrapbook remain pending; this is a partial UI increment.

Merged kind_robots PR #5103 (3b0d455d): eight-ending discovered/locked chronicle with existing persistent legacy IDs, six exact-head CI workflows green. Remaining t-064 work is painted ending plate delivery and detailed per-reign scrapbook records. Return to ready, not done.

Implemented durable per-reign scrapbook snapshots, validation, replay deduplication, and discovered-ending detail UI with focused tests. Artwork delivery and full ending plate integration still outstanding.

2026-11-15 PT reviewer reconciliation: kind_robots#5103 merged 2026-11-13 as a partial
increment (chronicle). Per the note's own 'Return to ready, not done', review -> ready.
Remaining: painted ending plates and full plate integration; confirm whether the
scrapbook snapshot work landed (no open kind_robots PR found).

Emperor scrapbook/Chronicle implementation branch ships persistent resolved epilogue snapshots, backward-compatible old saves, a dedicated eight-fate locked/unlocked illustrated Chronicle with earned per-reign entries and loss/peace detail, and an end-screen plate slot with graceful fallback. Eight DONE original ending ArtImages still require curated binary export to public/emperor-of-dust/endings/ before t-064 can be marked done. App PR exact-head CI must pass; this increment is partial pending art.

2026-11-18 PT: Kind Robots PR #5334 merged at 46b4a9ff9ebb2d2608d224cbad0bc67fbf1f3b27 after all 13 executed exact-head checks succeeded on 1e0a8842240c8f31b46168800da47f338f5a97f9 (autofix skipped). Epilogue snapshots and Eight Fates UI landed. Eight painted ArtImage binary exports still missing; keep task ready until curated, delivered and verified. Master issue #4142 remains open.

Continued t-064 in its existing claim session. Conductor branch worker/emperor-of-dust-t-064-encrypted-review-a91c adds a single-purpose, short-lived GitHub Actions intake workflow that uses existing KR_API_TOKEN secret to fetch the eight ORIGINAL DONE ArtImage bytes into ephemeral runner scratch, verifies dimensions and SHA-256, builds a contact sheet, then encrypts all image pixels with an ephemeral public certificate before uploading only a two-day encrypted artifact. Private key stays outside GitHub. This is a delivery-enabling intake increment, NOT yet visual curation or exported game art. CI, main workflow and actual binary acceptance require verification before done or playtest handoff.

2026-11-19 PT Reviewer: conductor#7616 (encrypted private-art intake workflow) NOT
merged. It auto-runs on merge, uses KR_API_TOKEN, and uploads output encrypted to an
off-GitHub key with no named holder, so it is security-sensitive. FOR SILAS: recommended
path is to close #7616 and curate the eight ending plates via export_round_art.py --only
'^endings/' straight into a kind_robots worker branch (t-063 precedent,
kind_robots#5276). Or, if you want the encrypted pattern, name the key holder and make
it workflow_dispatch-only. Decision unblocks plate curation; Epilogue/Chronicle UI
already merged (kind_robots#5334).

2026-11-22 PT: all eight painted ending plates curated and shipped at public/emperor-of-
dust/endings/ via export_round_art (the reviewer's recommended non-workflow path);
EmperorFortressEndingPlate already loads them first. Eight Fates/scrapbook UI merged
earlier (#5103, #5334). The security-sensitive encrypted-intake PR conductor#7616 is
superseded and not needed; Silas may close it.
<!-- note:end t-064 -->

## t-065 — Emperor of Dust achievements for endings and long-run play

<!-- note:begin t-065 -->
Silas 2026-11-11 PT, in session: "Achievements?" Target 12+ live achievements per docs/agents/main-game-standard.md.

Only three live Achievement records exist (emperor-of-dust-orders-carried-out, -day-well-ruled, -merciful-court) and all fire on Day 1-level play. Add live Achievement rows through the existing achievements API (label, message, icon, karma, triggerCode) and award them from stores/emperorFortressStore.ts: reach Day 50; one per ending (8); all eight endings; finish with no follower lost; earn both relics; recruit all secret followers; ring the Silent Bell. Show them with components/achievements/game-achievement-strip.vue on the ending screen and gallery. Verify one award live after deploy.

Achievement upgrade merged in kind_robots#5056 (d35dd44), all checks green: 16 new + 3 kept = 19 (one per ending family x8, 50-day reign, triumph, crypt sealed, Abbess unmasked, first/both relics, no follower lost, full Codex). 'Every peace' skipped (needs the t-064 endings record). Catalog seed succeeded.
<!-- note:end t-065 -->

## t-066 — New-reign carry-overs: ending-earned unlocks that change the next run

<!-- note:begin t-066 -->
Silas 2026-11-11 PT, in session: "Are there unlocks that carry over into future rounds?"

Today only two Items of Power (Eye of the Elder Crow, Komodo's Brass Hourglass) and the follower Codex persist between runs. Design and implement a small legacy layer earned by endings: e.g. one heirloom per ending family, unlockable starting options (a chosen first follower, a faction favor, a harder "second reign" setting), each visible on the start screen with how it was earned. Keep runs from becoming trivial (balance report before/after), persist like the relic vault, and cover with store tests.

First scoped legacy slice: persistent earned ending ids and optional five-brass veteran writ on a new reign, with malformed-save protection and focused tests. UI selector and complete ending-family unlock design remain open; implementation PR pending CI.

2026-11-15 PT intent audit (INTENT-AUDIT-2026-11-16.md): kind_robots#5093 (earned
endings and legacy writ) plus #5103/#5104 (chronicle/scrapbook) merged, so 'PR pending
CI' is stale. Remaining per this note: the UI selector and the full ending-family unlock
design. Released from review to ready.

Feature commit ca369584: eight ending-specific starting favors and a no-favor choice; fixed new-run legacy application; Chronicle selector and title-screen preview; backwards-compatible stored preferences and regression assertions. Exact-head GitHub Actions required before merging.

Completed legacy replay unlocks. Kind Robots PR #5328 merged at 5c2e5c8f84bcb981f1b8c5596a37f6032abdef50 after 8/8 exact-head GitHub Actions workflows completed successfully on e9e401f. Fixed newRun bypassing applyLegacy, offered eight distinct earned starting faction favors versus the five-brass writ or no bonus, exposed selection in Chronicle and title preview, and tested save compatibility and all choices. Master roadmap issue remains open for independent original art, literary, and five-act acceptance tasks.
<!-- note:end t-066 -->

## t-067 — Main-game standard: audit and close the gaps for Emperor of Dust

<!-- note:begin t-067 -->
Silas 2026-11-11 PT, in session: "Our games should all have a base standard of quality ... We want our main games to have 12 plus achievements." Standard: docs/agents/main-game-standard.md; CONTROL.md global overview.

AUDIT DONE 2026-11-12: projects/emperor-of-dust/STANDARD-AUDIT-2026-11-12.md holds the Met/Partial/Missing table, a proposed achievement list with award points, character-fit notes and the three smallest next PRs. Start there.

Start with the audit table from docs/agents/main-game-standard.md (title screen; settings menu; save/load and persistent progress; 12+ achievements; scrapbook; multiple endings with painted plates; customizable characters; 3+ replay hooks), marking each Met / Partial / Missing with evidence (file, route, live record). Put the table in this note and the first PR. Then close each gap in small CI-tested PRs; queue any needed ending, scrapbook or portrait art in an auto_submit ledger.

Item 7 (customizable characters) applies "in most cases": if this genre makes it a poor fit, say so in the audit with the reason and leave it for Silas rather than skipping silently.

Achievements are tracked by their own task; this one covers everything else.

Title console first slice: explicit Continue/Day, guarded New Reign, and Settings access; further standard gaps remain for this task.

2026-11-20 PT: Previous t-067 review was last updated 2026-11-12 and its initial title console is merged. Releasing stale review for the still-unfinished main-game standard: reset-progress safety, title achievements/scrapbook discovery, and final art/QA. User explicitly directed continued progress toward completion; don't mark it done.

Partial main-game-standard closeout: Kind Robots worker/emperor-of-dust-t-067-reset-progress-3c7e adds an explicit ERASE-confirmed reset of all Emperor autosave/3 slots/codex/relic/legacy/scrapbook/intro progress, preserving reading settings and other games. Refused/unreadable storage is guarded with rollback attempts, resets in-memory Pinia state, and returns the title screen. Splash now has a direct Achievements link and names the Chronicle/Scrapbook. Store test covers successful reset, reload, corrupt slot, separate keys, and blocked/read failures. PR and exact-head CI still required. Account-backed saves, image plates, responsive visual approval and optional ruler creation remain open.

Stale review reconciliation (2026-11-21 PT): main-game standard partial PR kind_robots#5440 merged 2026-11-20T22:16:40Z. No open Emperor-specific PR remained for this task. Reset progress and title navigation were delivered, but account-backed save integration, cross-width rendered acceptance, optional ruler creation and painted ending plates still need work. Return nonrecurring t-067 to ready for an independent, scoped implementation session; do not mark done or alter #4142.

2026-11-22 PT: closing for playtest handoff.

2026-11-22 PT: standard met for handoff: title console with Continue/New
Reign/Settings/Chronicle/Achievements, settings incl. new music/sound volumes and mute
(kind_robots#5530), ERASE-confirmed reset, versioned autosave + 3 slots + per-dawn
rewind, 19 achievements, Eight Fates scrapbook with painted plates (#5529), relic/codex
carry-overs. Account-backed save not applicable (no Emperor save API; the standard says
where the game has one). Ruler creator: audit item B says the identity lives in follower
choices; left to Silas as a post-handoff design call, not a build prerequisite.
<!-- note:end t-067 -->

## t-068 — Add a validator that checks t-044 playtest reviewer-record YAMLs against the second-pass scoring protocol schema

<!-- note:begin t-068 -->
Reviewer kaizen from the 2026-11-20 PT merge of playtest/2026-11-19/SECOND-PASS-SCORING-PROTOCOL.md. Add a small conductor script plus test that loads every reviewer record under projects/emperor-of-dust/playtest/<date>/ and fails when a score lacks trace_path/transcript_path/kind_robots_sha/seed, when a score is outside 1-5 (N/A allowed), or when a per-act total is reported with any N/A dimension. Keeps model-simulated scores from being mistaken for complete evidence.

Implemented second-pass reviewer evidence validator and focused tests on worker/emperor-of-dust-t-068-evidence-8f3c. Await exact-head CI before completion.

Silas confirmed conductor PR #7649 merged. Reviewer evidence validator and five regression tests landed. No playtest score or artwork delivery is claimed.
<!-- note:end t-068 -->

## t-069 — Report a deduplicated Emperor ArtJob to ArtImage to media to manifest-slot inventory before new art is authored

<!-- note:begin t-069 -->
Reviewer kaizen from the 2026-11-21 PT merge of conductor#7745 (worker suggestion). Add a read-only conductor script and test that join every Emperor art ledger's ArtJob ids to DONE ArtImage ids, the exported file path, and the kind_robots manifest slot that uses it. Report unique subjects with no image, images with no export, and exports no slot references, so slot-count audits cannot inflate queue counts again.

Opened Conductor PR #7760, exact head a3d2663f5485e1b3917e7eb06ff6ab5978fb8b54, implementing read-only deduplicated ArtJob to ArtImage to physical WebP to static game reference inventory with five focused tests. Report explicitly distinguishes missing DONE images, completed but unexported assets, orphaned exports and conflicting reroll IDs. CI was queued, not passed; no real media bytes delivered and no live campaign acceptance claimed. Review and merge only after all exact-head checks complete green. Keep #4142 open.

Merged via conductor#7762, superseding
<!-- note:end t-069 -->

## t-070 — Separate runtime-built Emperor art paths from true orphans in the t-069 inventory's 370 exported-but-unreferenced images

<!-- note:begin t-070 -->
Reviewer kaizen from the 2026-11-21 PT review of t-069. Against kind_robots 9a898029 the inventory reports 538 DONE images with no valid WebP export (feeds t-063) and 370 exports with no static text reference. Static substring search cannot see paths assembled at runtime and also over-matches prefixes (rooms/a matches rooms/ab). Teach scripts/audit_emperor_art_inventory.py the path builders in utils/emperorOfDust (or read the generated manifest), match on whole path tokens, and report the remaining true orphans, with a test for each.

Reviewer 2026-11-21 PT: merged #7766 (squash a3b5d4f). Whole-token matching replaces
substring search; runtime-builder candidates (quest/chance/audience/talk) are reported
separately as reference_class=runtime_candidate, never as delivered. 11/11 inventory
tests pass locally; all CI checks green on head b634e14. Kaizen -> t-071.

Completed by merged Conductor PR #7766 at a3b5d4f88ead1f30ded6c903c2c1b8f8e60e4bce. Exact-head Process task events, Worker PR handoff template, Security Audit, and Worker PR CI all completed successfully. Implemented whole-token static reference matching and dynamic candidate classifications for quest, chance, audience and talk URLs, plus four regression tests. Runtime candidates remain unverified until actual WebP media delivery. No new ArtJobs or exported image bytes are claimed. Keep t-063 and #4142 open.
<!-- note:end t-070 -->

## t-071 — Have Kind Robots emit an Emperor art runtime manifest so the inventory verifies exact reachable paths instead of builder-pattern candidates

<!-- note:begin t-071 -->
Reviewer kaizen from the 2026-11-21 PT review of t-070 (#7766). The inventory now tags quest/chance/audience/talk exports as reference_class=runtime_candidate when the builder exists, but that is only potential reachability. Generate a JSON manifest of every art path the fortress builders can produce from the game data (one build-time script in kind_robots), read it in scripts/audit_emperor_art_inventory.py when present, and promote candidates that appear in it to a reachable class, with a test for each class. Do not mark any DONE-but-unexported image as delivered; keep t-063 and kind_robots#4142 open.

Partial reachability implementation: Kind Robots worker/emperor-of-dust-t-071-runtime-manifest-8d6e91 emits exact runtime/static art candidate paths from all authored fifty-day audience, chance, quest, talk and ending builders in its existing Emperor art coverage CI. Conductor worker/emperor-of-dust-t-071-reachability-audit-8d6e91 consumes the JSON manifest and distinguishes builder-reachable URLs from speculative regex candidates, preserving separate false/missing physical WebP status; four manifest tests added. Open PRs and exact-head CI pending, no ArtImages physically delivered, keep t-063 and #4142 open.

2026-11-21 PT reviewer: merged conductor #7771 (exact runtime-manifest consumption, 4
tests) and companion kind_robots #5524 (test-only manifest emission), both green at
exact head. Audit now classifies builder_reachable from the emitted manifest; no
ArtImages delivered by this task; t-063 stays open.
<!-- note:end t-071 -->

## t-072 — Add a deterministic fixture that checks the inventory audit's builder-reachable counts against the Kind Robots runtime path manifest

<!-- note:begin t-072 -->
Reviewer kaizen from conductor #7771 (2026-11-21 PT): pin a small manifest+ledger fixture so a drift between emitted runtime paths and audit builder_reachable totals fails CI instead of silently reclassifying assets as unreferenced.
2026-11-22 PT: fixture added in conductor#7785.
2026-11-22 PT: tests/fixtures/emperor_art_inventory + test_emperor_art_inventory_fixture.py pin summary counts (builder_reachable, unexported, unreferenced) against a small runtime manifest; also covers the cast/ media path.
<!-- note:end t-072 -->

## t-073 — Sound and music: synthesized score, wasteland ambience and effects with volume settings

<!-- note:begin t-073 -->
Silas 2026-11-21 PT, in session: sound and music were never mentioned but are needed for playtest. Merged kind_robots#5530 (e00f3d1): file-free WebAudio score (room styles x Act I-V, hideout and ending moods, crossfades), wind bed, 18 effects (brass, dispatch, results, injury, death, recruit, dawn bell, betrayal sting, achievement, save/rewind), master/music/effects volume + mute in Settings, backward-compatible prefs. verifyEmperorAudio in Emperor CI; browser smoke 2026-11-22: silent until first gesture, then one running AudioContext and 65 scheduled voices across rooms, no page errors; Sound panel checked at 390px. Mix levels not yet judged by ear (human playtest).
<!-- note:end t-073 -->

## t-075 — Light ruler creator: name, style of address (Emperor/Empress/Sovereign), starting temperament

<!-- note:begin t-075 -->
Design call 2026-11-22 PT under notes_from_silas delegation (closes the t-067 / STANDARD-AUDIT item B question): build a light creator, no portrait (art shows the ruler only as a gloved forearm). Optional name, style of address shown in high-visibility UI (authored prose keeps Your Majesty), and a small balanced Day 1 temperament nudge; defaults reproduce today's start; old saves load as defaults. Implementation on kind_robots worker/emperor-of-dust-t-075-ruler-creator.
2026-11-22 PT: kind_robots#5545 open, all exact-head checks green.
2026-11-22 PT: merged kind_robots#5545 (56f46be) after all exact-head checks passed. Creator on the first intro screen of an untouched reign: optional sanitized name, Emperor/Empress/Sovereign shown in header, splash, ending heading and scrapbook, and a Day 1 temperament nudge (Merciful, Iron, Cunning; None = today's start byte-for-byte). Old saves load as the nameless Emperor; rewind keeps identity without re-nudging. 14 policies x 2 seeds x 3 temperaments: at most 1/28 ending change. Checked at 390/768/1440.
<!-- note:end t-075 -->
