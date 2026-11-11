# slime-city/t-009 — full note history archive

This file is the archaeology index for slime-city/t-009 ("Write and implement six genuinely different crew campaigns"). Its `note:` field in `roadmap.yaml` grew past `check_roadmap_note_size.py`'s 50,000-byte single-note threshold through ordinary recurring-cycle accumulation. The complete verbatim history through the archival point is preserved below; `roadmap.yaml` keeps only a short current-status pointer going forward. Do not restore this text into the live roadmap — read it here when you need to know what a specific past cycle found or did.

Archived under the AGENTS.md archival carve-out (byte-for-byte verified round-trip, pointer left behind, no history lost).

<!-- note:begin t-009 -->
Gene Riot Catgirls escaping their creators, Punk Bloodfairies organizing wild city uprising, cyber-ogres revolting against foundry owners, Riot Saints' explosive comedy, Undertow's information war, and Meat Exchange's rotten oligarchy. Different rivals, branching dialogue, authored rewards, earned endings and provenance-linked character/location art. A faction color is NOT a story and a paragraph is NOT an implemented playable campaign. Build one full vertical slice and test it before adding other chapters.

First campaign-depth increment: each of six crews has two distinct earned tactical echoes from prior chapter decisions. Previous victories visibly affect next-chapter Blackout opening conditions in both Story and city routes; losses do not unlock echoes or erase earned history. Added a six-crew deterministic test matrix. Source PR pending CI; further campaign depth, sourced illustration placement and human playtesting remain open.

PARTIAL MERGED 2026-11-02 PT: Kind Robots PR #4656 merged to main at 791ad976bc74d0f43766ed1ab83637e5447bad1e after all six latest-head GitHub Actions workflows passed: four contract shards, TypeScript, formatting, layout, architecture, schema parity and security checks. Twelve choice-specific campaign echoes now carry one prior victory into the next Blackout mission, with legible terms in Story and district launch, deterministic six-faction tests and independent account-saved progression. This is one substantial campaign-depth slice, not task completion. Continue richer character scenes, branching consequences and authored rewards; art placement and visual acceptance remain on their separate tracks. No self-hosted deployment or public publication was performed.

Developed faction campaign earned-support dossier on Kind Robots worker branch: player chooses one of previously won chapter favors, with twelve crew-lead voice lines, rival portraits and battle previews. Selection is local; eligibility is derived from already account-saved victories. Both city-launched and direct story matches apply exactly one selected favor. Added six-crew adversarial deterministic rules tests. Implementation PR requires completed current-head CI; full writing, art and human game-fun acceptance remain distinct.

PARTIAL MERGED 2026-11-02 PT: Kind Robots #4662 merged at 893e2343e9b242d24aa9503b00b3041a05cded43 after six completed and passing current-head GitHub Actions workflows. Added earned-support dossier for six faction campaigns: selectable favors from prior chapter victories, original twelve leader dialogue lines, reused crew portraits and visible battle effects in both Story and district missions. Existing account-saved decisions authorize eligibility; only one favor applies per fight, no stacking or resource grants. Six-crew deterministic regression coverage accompanies the implementation. Reconciled concurrent art-first campaign chapter imagery and animated KrChoiceHand from main without overwriting it. Full faction writing, deeper dialogue, balance and human playtests remain open; queued art does not block gameplay progress. No deployment triggered.

Authored and staged 30 individual rival-versus-player confrontation exchanges across all six Slime City crew campaigns, plus twelve decision-sensitive rival callbacks and six character-specific rematch beats. Connected account-saved chapter and choice history to the illustrated campaign UI with separate rival/player portraits, compact transcript panels and no additional persistence or currency changes. All six crews and five chapters now have deterministic replay, branch, defeat, faction-isolation and finale assertions. Source PR requires complete latest-head TypeScript, contract, layout and formatting CI. Further campaign writing, sourced illustration and subjective playtesting remain open in t-009.

PARTIAL MERGED 2026-11-02 PT: Kind Robots PR #4669 merged as 2c427c1b4153cc2c044abb0e6e01f3b91a430219. Authored 30 chapter-specific rival/leader conversations, 12 choice-memory callbacks and six defeat/rematch lines, illustrated in the existing Story interface. Further post-battle reactions, rewards, art verification and subjective playtesting remain on this task. No publish/deploy action claimed.

Next campaign-depth increment in Kind Robots worker branch: 60 authored rival response lines for victory/defeat across thirty battles, plus twelve player reflections specific to the chosen conviction/cunning tactic. Last attempted approach is now saved even on a defeat, as an optional validated account-story field compatible with preexisting saves. The illustrated post-battle result appears before the next chapter or epilogue; no reward, matchmaking or currency effects. Added six-crew, five-chapter, both-approach result and legacy-save integrity coverage. Latest-head PR tests required before merge; full campaign and human fun acceptance remain open.

PARTIAL MERGED 2026-11-02 PT: Kind Robots PR #4672 landed on main at 26ae5525bdb1b55c6aa085eeafee805f71132a65, with all six latest-head GitHub Actions workflows and all contract shards passing. Added 60 authored rival aftermath lines for distinct win/loss outcomes across six five-chapter campaigns, plus twelve approach-sensitive protagonist reflections and an illustrated verdict panel before the next chapter/ending. Campaign saves now remember attempted conviction or cunning even after defeat; optional validated field preserves compatibility with prior saves, and older losses never invent choices. Added deterministic six-faction and validator edge-case tests. Task remains partially complete: deeper branching rewards, art placement, adversarial fun and human acceptance remain. No production deployment or public release was triggered.

PARTIAL MERGED 2026-11-02 PT: Kind Robots PR #4672 merged as 26ae5525bdb1b55c6aa085eeafee805f71132a65. Shipped sixty chapter-specific rival victory/defeat reactions, twelve conviction/cunning leader reflections and an illustrated aftermath panel; saved the last attempted tactic even on losses while preserving old account saves. Human QA, art and further campaign distinctiveness still remain open. No live deploy triggered.

Replaced campaign dossier's two reusable faction effects with sixty individually authored chapter-by-approach support abilities. Each of six factions has ten different named choices, five per conviction/cunning approach; each chosen battle applies at most one already-account-earned favor. Effects stay within bounded mana, HP, armor, rivals, rounds and trap modifiers, with no wallet, card ownership or schema changes. Expanded existing deterministic overworld contract test to cover sixty names, legal effects, chapter unlock sequence and meaningful per-faction variation. Await complete current-head GitHub Actions before merge; additional campaign and subjective playtesting still open.

PARTIAL MERGED 2026-11-02 PT: Kind Robots PR #4674 merged at 9bbfb3378b27f290ad10d3d665dd5c231d87b1f1. Fixed the earned-support dossier's duplicated perks by authoring sixty distinct, chapter-and-approach-specific tactical favors across six crews. Each faction now has ten truly different bounded battle modifier combinations. Only one already-earned support applies per battle; no new currencies, card purchases, save fields or schema changes. Exhaustive six-crew progression, uniqueness, balance-bound and choice-gating tests added. All six source GitHub Actions workflows completed successfully on the latest PR head, including four contract shards. Deeper campaign gameplay, illustration and human fun testing still remain; no publishing or production deploy triggered.

Built a source-backed adverse campaign-favor playtest audit on a Kind Robots worker branch. Runs real CPU-versus-CPU Blackout engine bouts with paired identical-seed baseline controls: six crews, four usable previous chapters, two saved approaches, two next-story choices and two deterministic seeds. 192 favor-versus-baseline comparisons, 96 distinct baseline bouts, 48 repeated replays. Logs win/draw scores, command divergence, initial contact, rounds, faction differences and each of 48 earned usable favors. Identified a structural risk: all six fifth-chapter favor rewards are unlocked only when the campaign has no following battle, leaving them unusable. CI and measured results pending. This is a playtest increment, not subjective human fun acceptance or completion of t-009.

PARTIAL MERGED 2026-11-02 PT: Kind Robots PR #4678 merged bf86af3cd27020c9a7d8a0db2ed126e669e11705 after eight successful latest-head workflows and all contract shards. Real Blackout CPU headless tests compare 192 paired support trials against 96 controls with 48 deterministic replays. Original sample improved score 103 to 112 across 192; 35 changed outcomes, 135 different command histories, no stalls. Five round-only supports received small immediate bonuses and regression coverage. Remaining scope includes earned finale rewards with no post-campaign use and human fun acceptance.

PARTIAL MERGED 2026-11-05 PT: Kind Robots PR #4792 merged
df18a455ca7b2ba7e220ee6945b455ef58688e99 (11/11 latest-head checks incl. TypeScript and
four contract shards). Fixes the structural risk above: a finished campaign's five
favors, finale fifth by default, now carry into district rival and after-hours contract
bouts as the CREW LEGACY (campaignLegacyFor/campaignLegacyTerms; null mid-campaign so
campaign balance is unchanged). Favor picker extracted to components/slime-city-
favors.vue and shown on the finale screen; rival and contract panels name the legacy.
Tests cover all six crews plus a store rival bout vs a plain baseline; full test:slime-
city-lab passed. No save, wallet or schema change. Remaining: human fun acceptance;
finale-panel screenshot not yet taken; consider adding legacy bouts to the campaign
playtest audit.

2026-11-06 PT: Built (patch slime-city-t-009-r6, base e18fcb20) an authored BLACKOUT
battlefield and objective for all 30 campaign chapters, so the six crew campaigns no
longer fight the same pit with different numbers. There are four objectives: SMASH on a
rebuilt field, HEIST (the rival vault cannot be damaged and only a flag run wins), HOLD
OUT (survive to the bell with your base standing and your flag home) and BEAST (a named
giant such as the Paper Catgirl or the Patent Press, where the killing blow wins). Each
crew mixes at least three of them, and each chapter has a briefing tied to its scene;
the rules text is generated from the applied data. The engine hooks only activate on
campaign battlefields: holdout/heist, placeFighter veterans, set-piece traps outside the
trap cap, and a fix so nothing deploys onto the monster's square. The chapter panel
shows THE BATTLEFIELD and the arena names the objective. The new
verifySlimeCityCampaignBattlefields test proves: every chapter × approach is winnable by
seeded play and an idle player never wins (16 seeds); all six campaigns reach their
endings with real bouts; saves stay valid. All Slime City suites pass. Remaining: (1) a
pre-existing BLACKOUT softlock where a flag carrier and its own escort block each other
forever; a fix needs a balance re-baseline, and the battlefields are designed so it
cannot hand an idle player a win; (2) human fun acceptance, especially for the low-end
cunning finales (Moonlight Deed, The Boardroom); (3) Clash is now canonical, so a
decision is needed on whether campaigns move to Clash; (4) add the battlefields to the
favor playtest audit. Merged as kind_robots#4865 (2026-11-06).

2026-11-08 PT: First non-art split of Story and Alliance modes in Kind Robots worker/slime-city-t-009-story-cards-tower-20261109-c8v6: deterministic two-card reward drafts after each of six faction stories' Clash victories with rarity and campaign-only saved card loadouts; 12-floor persistent Alliance Tower with two scenic route choices, changing boss life, relic/guard/scar progression, two-card end-run legacy and anti-farm rules; previously unplayed Alliance equipment gets real board-value scoring. Source QA and full CI pending; five authored Story combat chapters per faction remain, long-form expansion still required. No account wallet/pack grants, release, or gameplay fun acceptance.

PR #4914 merged the five-chapter Story card-draft and twelve-floor Alliance Tower vertical slice on 2026-11-08 PT. It explicitly leaves long-form six-faction narrative, distinct tower encounters, richer branches and adversarial fun QA unfinished. Reopen t-009 for the next scoped content and gameplay increment; do not mark human acceptance or publishing complete.

Submitted focused twelve-floor Alliance Tower narrative pass: 24 unique authored route scenes, hazard effects unchanged, deterministic floor coverage contract. Source PR and latest-head CI are the next checks. This is a slice: six long-form faction stories, more Tower events and adversarial fun playtesting remain open.

Kind Robots #4919 merged as 00fec8ca051c7234df5c90a2c66495c9ca98ec63 after all six latest-head CI workflows completed green. Alliance Tower now has 12 distinct setting beats and 24 original route scenes with a strict compatibility test for previously saved legacy battle copy; original hazards, 300-card inventory and currency were unchanged. This is a partial narrative increment: six faction campaigns still need long-form writing and Alliance run variety and human fun QA.

First faction narrative vertical-slice review: 15 authored Gene Riot beats across five canonical story rivals with 30 immutable left/right decisions, callbacks, SOLO CLASH preparation effects, new scene/City entry hand, persistence and two complete divergent campaign tests. The updated single GitHub roadmap issue kind_robots#4535 tracks the other five campaigns and Alliance Tower. Code PR and final CI required; no human acceptance, wallet changes, art delivery or release.

PARTIAL MERGED 2026-11-09 PT: Kind Robots PR #4922 squash e37262b420eb25f134c94bebc1eb2fcab7746a51. All eight final-head CI workflows green, including four contract shards, TypeScript, formatter, architecture, layout, schema, facet and container build. Gene Riot now has fifteen original interactive scenes spanning its five existing story chapters, thirty choices with callbacks, saved scene progress, real SOLO CLASH boss-life choice effects, aftermath and epilogue changes, faction-specific illustration-first choice hand, and save/playthrough contract tests. Canonical GitHub master issue #4535 now lists S-01..S-07 and A-01..A-04 acceptance for other five faction journeys and Alliance Tower. Leave t-009 READY for remaining campaign expansion, visual art, seeded actual CPU fun playthroughs, human acceptance. No real-money or account-card wallet changes, deployment or publishing.

Bloodfairy Moshpit Republic implementation in review: fifteen original authored scenes and thirty choices across five canonical rivals, cumulative Call & Response Voices/Volume, real Story-only deck additions (Riot Choir and Bassquake), battle boss-life pressure and conditional coalition endings, actual Level 3 Wall of Sound/Backup Singers card reveal in chapter three, shared stage UI and city shortcut gating, save validation and two complete seeded-choice route tests. Source PR final CI required. t-009 remains a six-faction campaign umbrella; no account pack currency, art delivery or publication.

PARTIAL MERGED 2026-11-09 PT: Kind Robots PR #4923 squash d2f39aa675d97e41149c6b89ce36a8028e4b3bd6 after all eight latest-head workflows completed green (four contract shards, TypeScript, changed-file Prettier, layout, schema, architecture, facet, container). Bloodfairy Moshpit Republic adds fifteen original scenes, thirty coalition decisions, cumulative Voices/Volume affecting real Solo Clash boss life, coalition-selected Story-only Riot Choir and Bassquake cards, true authored Level 3 Wall of Sound/Backup Singers illustrated previews with normal earned evolution rules intact, distinct chapter callbacks, route epilogues, save/anti-forgery, city route gating and two complete divergent state-machine playthroughs. Gene Riot compatibility preserved; no wallet/inventory minting, new card IDs, migrations, art delivery, human fun approval or deployment claimed. t-009 remains READY for Ironjaw, Riot Saints, Undertow, Exchange and further art/adversarial QA.

2026-11-09 PT: THIRD CREW CAMPAIGN in review, kind_robots#4932: Ironjaw THE LAST SHIFT,
the lizard strike. 15 authored scenes over the 5 canonical chapters, 30 decisions,
SOLIDARITY/HEAT meter (COLD->BASKING->MOLTEN). Leans into the world per Silas
2026-11-09: wages in Meat coupons only good at the company store; shed skins filed as
worker IDs; a blast-heated floor that makes cold-blooded workers fast and cooks them;
cybernetics grown from harvested tails; Queen Pin's band holds the rafters. Choices
change callbacks, real Solo Clash boss terms (solidarity -> player life, heat -> rival
armor) and Story-only deck adds (Union Bridgebearer / Walking Foundry); no Meat/card
grants. Full test:slime-city-lab (44 PASS) and npm run test (vue-tsc) green locally.
Remaining t-009 scope: Riot Saints, Undertow and Meat Exchange campaigns, plus
adversarial fun playtesting. Leave t-009 ready after #4932 merges (umbrella), not done.

PARTIAL MERGED 2026-11-09 PT: kind_robots#4932 squash-merged after all 13 checks passed
(TypeScript, 4 contract shards + verifiers, layout-contract, facet-alias-smoke,
production image build, Prettier, verify x2, GitGuardian). Ironjaw THE LAST SHIFT is
live on main (after the next Unraid Force Update): 15 lizard-strike scenes, 30
decisions, SOLIDARITY/HEAT meter. Three of six crew campaigns are now authored (Gene
Riot, Bloodfairy Moshpit Republic, Ironjaw). t-009 stays READY for Riot Saints, Undertow
and Meat Exchange campaigns plus adversarial fun playtesting; follow the
campaignIronjaw.ts pattern (also update the overworld store test if a crew used there
gains a journey).

2026-11-10 PT: FOURTH CREW CAMPAIGN in review, kind_robots#4964: Anarkiss THE BEAUTIFUL
CATASTROPHE, the illegal midnight festival. 15 scenes over the 5 canonical chapters, 30
decisions, SAFETY/SPECTACLE meter (REHEARSAL->OPENING NIGHT->GRAND FINALE). Choices
change callbacks, real Solo Clash boss terms (safety -> player life + a round, spectacle
-> mana, eventually 1 life) and Story-only deck adds (Volunteer Safety Vest / Doctor
Blast Radius); no Meat/card grants. Cross-crew journal tests now use Undertow.
test:slime-city-lab (45 PASS) and npm run test (vue-tsc) green locally. Remaining after
merge: Undertow and Meat Exchange campaigns plus adversarial fun playtesting; return
t-009 to ready (umbrella), not done.

PARTIAL MERGED 2026-11-10 PT: kind_robots#4964 squash-merged at 7b877d2 after all 13
checks passed. Anarkiss THE BEAUTIFUL CATASTROPHE is live on main (after the next Unraid
Force Update). Four of six crew campaigns authored (Gene Riot, Bloodfairy, Ironjaw,
Anarkiss). t-009 stays READY for Undertow and Meat Exchange campaigns plus adversarial
fun playtesting; follow campaignRiot.ts, and move the other journey tests' cross-crew
checks from undertow to exchange when Undertow gains a journey.

Unified Solo/City narrative entry and linked Alliance/Solo deck selection; fixed server rejection of Alliance story bouts; immediate chapter choice progression; account-saved deck, team and aftermath restoration. Implementation PR and CI under review. This is a substantial slice of ongoing six-crew story depth, not completion.

Human-directed follow-up after Kind Robots #4967 merged: extend the unified Journey with genuine Alliance-specific branching scenes, saved consequences, and tests. The earlier reviewed vertical slice was merged; this broader story task remains open.

Alliance-specific narrative implementation ready for review: 30 directed crew pairings, 5 chapter contexts each, player-picked protection or gamble outcomes with server-verified Clash boss effects, a bounded same-ally callback, account-save validation, and handoff from the city's shared Journey. Regression tests include all 150 paired chapter combinations and store battle gating. This is a substantive slice of the continuing six-crew story-depth task, not final acceptance. Implementation PR follows current-head CI.

PARTIAL MERGED 2026-11-10 PT: Kind Robots PR #4969 merged to main at bd4d2c7b2570ee1d1404876fdfd1d72dbf56a4b1 after eight completed and passing latest-head GitHub workflows (four contract shards, TypeScript, formatting, layout, architecture, schema parity, Facet smoke, container build). Thirty directed Alliance relationship threads now add a saved player choice after each faction's authored chapter scenes. Five chapter contexts per partnership; protect/gamble alters verified Clash opening boss life, consecutive use of an ally creates one bounded callback, and city missions cannot bypass the interlude. The UI previews the actual battle terms, including format, and aftereffects persist in account story saves. New 150-case script and store launch tests included. No DB migration, new ArtJobs, manual deploy or public launch. Remaining scope under t-009: deepen chapter-specific ally writing, partner-specific endings and full-run human playtesting.

Directed Alliance act-and-finale follow-up is implemented for all 30 pairings: four authored chapter escalations each (120 unique dilemmas and 240 unique choice outcomes), 60 partner-specific finale alternatives, history-dependent ending callbacks, and a test suite covering 90 five-chapter narrative paths, 30 partner switches, and 30 loss/retry scenarios. PR/CI pending; full tactical balance and human fun acceptance remain open.

PARTIAL MERGED 2026-11-10 PT: Kind Robots PR #4970 merged on main at 9db89a095949af5fd8425cfd89329e19760b866f after all eight latest-head GitHub Actions workflows passed. Authored four additional escalation scenes per directed two-crew pairing (120 unique late crises, 240 unique later choice outcomes), with 30 ally-specific ending titles and 60 final-choice outcomes; the original solo/crew ending is retained. Callback text now cites the actual last decision, partner-switch history persists, and finale tone considers partner tenure and protect/risk choices. New scripted editorial tests passed 90 full five-chapter same-partner narrative runs, 30 switch runs, and 30 loss/retry paths; source-audit found 300 distinct total outcome paragraphs. Added an inspectable editorial/fun-risk report. This is narrative-only simulation, not human-controlled Clash combat or subjective fun approval. No schema migration, ArtJobs, or production deployment was triggered. Remaining t-009 scope includes actual human playtesting, combat balance and further crew-specific editorial acceptance; leave ready.

Alliance tactical choice pass ready for PR review: six ally signatures and five evolving chapter pulses replace the same repeated protect/gamble boss-life trade. Use explicit boss-life terms (rather than mislabeling them as legacy mana/armor), show the actual numerical risk on narrative choice cards, and retain server-issued/verifiable Clash boss values. New tests cover 300 pairing/chapter/choice combinations and 36 seeded real Alliance CPU matches. The work remains a reversible t-009 slice; broader human fun and balance acceptance is open.

PARTIAL MERGED 2026-11-10 PT: Kind Robots PR #4972 merged to main at 2ec8ffd8d5e5d5ab7ba36fc1cdaae5d1499e4098 with all eight latest-head workflows passed. Six ally-specific tactical profiles evolve over five chapter pulses, producing distinct bounded protect/gamble boss-life stakes with one-chapter loyalty; direct boss-life fields replace fake mana/armor modifiers. Alliance plan text no longer spoils victory before battle, and defeated or drawn bouts show ally-specific setbacks rather than success prose. Verified 300 pairing/chapter/choice combinations and 36 actual CPU-versus-CPU Alliance Clash completions, plus existing 150-scene save/retry contracts. Small fixed-opponent smoke: player 9 wins, enemy 27; particularly catgirls and Bloodfairies 0/6 against selected opponents. DO NOT generalize this to all matchups or apply global buffs without paired control seeds, both seat orders and comparable opponents. Remaining t-009 work: balanced seeded opponent/seat matrix, stronger card/evolution-specific narrative effects with server replay verification, and human quality/fun acceptance. No schema, ArtJobs, billing, public release or self-hosted deployment performed.

Paired Alliance Journey balance investigation open for PR review. The alarming 9/36 statistic came from a fixed-opponent targeted smoke that mainly ran Riot versus Ironjaw, not a balanced faction survey. Existing CI evidence includes 1140 constructed Alliance games (48.7% first-seat wins excluding draws) and 1080 evolution-deck matchups (50.5% first-seat wins). Added 600 seed/deck/seat-matched triplets (1800 actual CPU Clashes) to isolate baseline/protect/gamble story bonus effects across all six generals, allies and opponent generals; retained explicit CPU-only caveats and avoided arbitrary tuning before results. Authored an inspectable report and labeled the old smoke as nonrepresentative. Pending PR CI, not complete acceptance.

PARTIAL MERGED 2026-11-10 PT: Kind Robots PR #4975 merged on main at 57fde19bf7bee9fe0123614a3bcbaf17879305f6 with all eight latest-head GitHub workflows completed successfully. Investigation overturned the scary 9/36 smoke-test interpretation: tests were mainly Riot vs Ironjaw, and per-"catgirls"/"bloodfairies" output keys represented allies, NOT generals. Earlier CI's 1140 constructed Alliance games produced 48.7% first-seat wins, while 1080 other deck games produced 50.5%, indicating no sweeping seat bias. Added 600 Latin-square-matched setups / 1800 real CPU Clashes with identical decks/seeds in baseline/protect/gamble and both seat orders, 4 deterministic replays. FINAL corrected results (rates exclude draws): baseline story-owner 52.3%, protect 55.3%, gamble 58.5%; story-owner first seat 53.3% baseline vs second seat 51.3%. Protect changed 82/600 compared outcomes vs baseline, gamble 95/600, and protect vs gamble differed 119/600. Baseline ally breakdown varied (Bloodfairies 41%, Undertow 70%) despite rival/chapter rotation, but starter decks and simplified Alliance CPU evaluation limit causal claims. Do not apply blanket faction buffs or nerfs from these CPU-only samples. Suggested next t-009 slice: test constructed partner decks and evolved-card/CPU heuristic scoring on paired seeds, then human fun/balance approval. No game rules, cards, economy, database, ArtJobs, public release or self-hosted deployment modified.

Prepared focused Alliance support-role and CPU evolution-scoring follow-on: retain old policy comparator, enable bounded board-aware evolution payoff for Alliance CPU choices, and define legal fighter-forward / ally-forward 20-card mixes while preserving existing default starter. Added 600 identical-seed/deck/opponent/seat matched setups (2400 actual CPU Clashes) comparing legacy and new CPU with optional recipes; assert free-card legality, stage-two/three use, winners, draws, and replay. CI and PR review pending; human fun validation still separate.

PARTIAL MERGED 2026-11-10 PT: Kind Robots PR #4980 merged to main at a90c62317fb39bb9c7b10facf2fd6b595e6d8108 after all eight latest-head GitHub workflows completed successfully. Root cause: Alliance CPU used generic +1.2/+2.5 enter-stage boosts while ignoring the already-implemented board-aware evolution payoff. New default uses bounded [-2,+3] read-only evolution value plus <=0.7 future L2 value; original exact baseline remains selectable for paired tests. Added legal optional fighter-forward (12 creatures) and ally-forward 20-card starter recipes drawn entirely from free base cards without modifying existing decks. Controlled 600 seed/opponent/seat-matched setups / 2400 actual CPU Clashes and six deterministic replays: classic+old CPU 53.8%, classic+board-aware CPU 54.0% (L3 plays 239->259; 37/600 results changed), fighter-forward+board-aware 65.3% versus classic opponent (219/600 results changed), ally-forward 44.0% (263/600 changed). Fighter-forward is advantageous against classic decks, not a forecast when both sides choose it; don't automatically migrate player decks or globally buff factions. Detailed evidence is in docs/slime-city-ally-evolution-cpu-balance.md. Next t-009 focus: symmetric fighter-forward-vs-fighter-forward seat-balanced matchup and actual human satisfaction with evolved card choices, plus optional starter preset UI if desired. No DB migration, new ArtJobs, billing, direct production deployment, or irreversible changes.

Mercenary-first balance experiment ready for PR: add neutral control and synergy packages using four identically available free mercenary cards for any general/ally pair. Preserve existing fighter-forward composition, exactly seven ally cards, 12 fighters and 20 total cards; saved decks, card stats and defaults untouched. 300 matched general/ally/rival/seat scenarios, five comparison variants including symmetric mercenary mirrors (1500 real CPU Clashes). Documents equal availability versus unequal benefit and prioritizes shared tools over faction-specific buffs. CI pending.

PARTIAL MERGED 2026-11-10 PT: Kind Robots PR #4984 merged on main at a02412ee524ff6294ccc5c66af361226184412c5 after all eight latest-head GitHub Actions workflows completed successfully. Adopt Silas's direction that shared mercenaries are the preferred first balance lever for weak strategies, rather than faction-specific buffs. Added two optional legal crew-neutral bridge recipes from the 20 free starter mercenaries: control (Traffic Witch, Escape Artist Crab, Homebrew Antidote, Misaddressed Parcel), synergy (Sewer Sommelier, Escape Artist Crab, Counterfeit License, Cursed Sign). Each package adds four identically accessible cards to fighter-forward alliance decks, preserving seven ally slots, 12 fighters and 20-card legality; excludes existing neutral guest cards to avoid duplications. No human saved decks, card stats, default recipes, collection schema or live matches changed. CI ran 300 matched general/ally/rival/seat scenarios, five variant arms (1500 actual CPU Clashes): fighter-forward symmetric baseline 52.0%; control vs fighter-forward 60.0%; synergy vs fighter-forward 49.0%; control mirrors 43.7%; synergy mirrors 49.7%. Bloodfairies as ally baseline 28% -> control 46%, Catgirls as ally 40% -> 54%; equal card access did not translate into identical benefit. Control is a promising neutral counter-strategy, NOT a universal forced default; preserve faction identity and test symmetric adoptions before targeted mercenary evolution or stat tuning. Details/results in PR #4984 and docs/slime-city-mercenary-strategy-balance.md. Broader t-009 still needs subjective fun review and further cross-faction playtesting. No live deploy or ArtJobs executed.

PARTIAL MERGED 2026-11-11 PT: two crew campaigns landed that this note was missing. (1)
kind_robots#4964 (2026-11-10): Anarkiss THE BEAUTIFUL CATASTROPHE, 15 festival scenes,
30 decisions, SAFETY/SPECTACLE meter, Volunteer Safety Vest / Doctor Blast Radius Story-
deck cards. (2) kind_robots#4991 squash 4744a9400a033e6b1519dc7780b4f2afdf8678d9 after
all 13 checks passed (TypeScript, 4 contract shards + verifiers, Prettier, layout,
facet, image build, GitGuardian): Undertow THE CITY THAT LISTENS, 15 spy scenes across
the five canonical chapters, 30 decisions, TRUTH/LEVERAGE meter
(WHISPER->STATIC->BROADCAST). Truth lowers rival boss life and at 6 drops one rival;
leverage adds mana and at 9 arms a rival trap. Story-only Floodlight Sweep / Wiretap
Restraining Order. New verifySlimeCityUndertowJourney; other journey tests' cross-crew
checks now use exchange. Five of six crews are authored. Remaining: Meat Exchange
campaign (lovecraftian butcher-priesthood, follow campaignUndertow.ts; move cross-crew
checks to a non-journal field once all six exist) and adversarial fun playtesting. No
Meat/wallet/card grants, art or deploy claimed.

PARTIAL 2026-11-11 PT: sixth and final crew campaign, Meat Exchange THE BOOK OF FLESH,
in kind_robots#4997: 15 occult scenes (Gilt inherits the butcher-priesthood bound to the
Thing That Hungers), 30 decisions, MERCY/APPETITE meter (CANDLE->TITHE->RECKONING);
mercy lowers rival boss life and at 6 drops a rival, appetite adds mana and at 9 feeds
rival mana; story-only Contract Amendment / Emergency Margin Call. New
verifySlimeCityExchangeJourney; other journey tests' cross-crew checks now use an
unreached-chapter entry. All six crews authored. Remaining: adversarial fun playtesting
across the six campaigns (subjective).

MERGED 2026-11-11 PT: kind_robots#4997 squash 21d67af1 after all 13 checks green
(TypeScript, 4 contract shards + verifiers, Prettier, layout, facet, image build,
GitGuardian). All six crew campaigns are now authored and wired. Remaining t-009 scope:
adversarial/subjective fun playtesting across the six campaigns. No Meat/wallet/card
grants, art or deploy.
<!-- note:end t-009 -->
