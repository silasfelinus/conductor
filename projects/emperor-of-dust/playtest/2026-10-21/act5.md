# Emperor of Dust playtest: Act V (Days 41–50), endings, epilogue

Scope: `utils/emperorOfDust/fortress/actFive.ts` (all 24 dated audiences, all 8 Day 42 host-terms
variants, Act V quests), `endings.ts`, `epilogue.ts` (341 variants; five synthetic runs sampled through
`epilogueFor` + `endingOf`, see the end of this file), plus the engine paths that decide the ending
(`endingOf`, quest return timing in `finishDay`, `hostShare`). Read-only, no repo files edited.

## Headline answers to the three questions

**Does the emperor-without-a-throne feel different from the fortress acts?** In mood, yes. In choice
structure, mostly no. The fire, the borrowed blankets, the host who counts you as a wagon, brass that
has to be found for every kindness (seven options cost 25–30 brass in a week with no taxes): all of it
lands. But the emperor still mostly sits in judgment. Act V has four "judge the one who opened the door"
scenes (sentry d41, deserter d42, Holloway d43, cook d47), plus the informant (d42). The host never uses
its power over you. No scene has a host evict you, sell you, outvote you or call in its terms, even
though `host-terms-accepted` and `host-terms-paid` exist for exactly that and nothing reads them. The
act describes a court that can be refused. It never refuses you.

**Are the hosts' demands real dilemmas?** The demands themselves are not. Accept costs nothing, gives
+5 affinity (which raises your daily host share) and posts a low-danger chore. "Pay in brass" costs 30
and gives no affinity, so accept beats it on every axis. The real dilemmas are behind the optional "ask"
probe. Six of the eight are good there (Mole vote, Bell water, Pack tolls, Saltroad crates, Freehold
ribbon, Crow messenger). The Rail station's is dominated, and the Cave's is thin. A player who accepts
on sight never sees the dilemma at all.

**Are the endings earned?** The peace on Day 49 is partly earned, because each option is gated on a
Friendly tier built over 48 days. Survival is not earned by anything Act V asks you to do. Day 50 is a
stat roll of whoever you send (`q-d50-last-dispatch`: might high, lore high, heart mid). Not one Act V
alliance changes it: the Verge, the returned Watch, the inside gate, the lantern, the burrows digging,
the Crow sightings or the courier's map. Only two earlier quest *successes* (well, clapper) open extra
roads. Then a hidden override (two deaths, at any point in the campaign, become A Hundred Candles)
can erase the Day 49 vote without warning. The Bell Restored peace is unreachable in a normal run
because of quest timing (Top problem 2).

## 1. Summary table

Scores are Mood · Clarity · Uniqueness · Choice · Consequence (1–5).

| Scene id | Day | M | C | U | Ch | Co | Verdict |
|---|---|---|---|---|---|---|---|
| d41-roll-call | 41 | 5 | 4 | 4 | 3 | **1** | Best opening image of the act (the ladle across the knees). Nothing it sets is ever read. |
| d41-archive-saved | 41 | 4 | 4 | 4 | 4 | 3 | Real weapon-or-shelf dilemma. "Read it" is free and goes nowhere. |
| d41-trusted-road | 41 | 4 | 4 | 4 | 4 | **2** | Three honest answers to "did trust fail?" Two of them are never remembered. |
| d41-midnight-gate | 41 | 5 | 4 | **2** | 4 | **1** | "The horses are tall" is a perfect line. First of four gate-opener trials. No echo. |
| d42-terms-mole-tunnels | 42 | 4 | 4 | 4 | 4 | 3 | The 31–30 vote is the best host truth. Charter versus facing the thirty splits players. |
| d42-terms-crow-cave | 42 | 4 | 3 | 3 | 3 | **2** | Neutrality-versus-spy. The warned threat never lands, and the "four lines" letter is a blind choice. |
| d42-terms-bell-cellars | 42 | 5 | 4 | 4 | 4 | **2** | Abbey water for the children is a superb temptation. Nothing comes of it. |
| d42-terms-wagon-circle | 42 | 4 | 4 | 4 | 4 | 3 | The toll promise is paid for by the Saltroad, a third party the player knows. Good. |
| d42-terms-moving-caravan | 42 | 5 | 3 | 4 | 3 | 3 | The crates are the act's best horror reveal. There is one real path, and the bargain text claims an effect that does not exist. |
| d42-terms-freehold-barn | 42 | 5 | 4 | 4 | 4 | 3 | Decoy barn versus ribbon is genuine. The informant the ribbon warns about never arrives. |
| d42-terms-rail-station | 42 | 4 | 4 | 3 | **2** | 3 | Accept dominates: it keeps the parts from the Abbey, pays brass and raises affinity. |
| d42-terms-nameless-cave | 42 | 4 | 4 | 3 | 3 | **2** | Right register for the loss state. The deserter "saw who opened the gate" and nobody asks him. |
| d42-cage-wagon | 42 | 4 | 4 | 4 | 4 | 4 | The truth costs your host; the lie costs her life. Buying her out blunts it, but brass is scarce. |
| d42-thistledown | 42 | 4 | 4 | 3 | **2** | **2** | Saying the names free buys exactly what 30 brass buys. Dominant option. |
| d42-mill-doors | 42 | 4 | 4 | 3 | 3 | 3 | Ordering the mills costs less and pleases the host more than repaying. Acceptable trade. |
| d42-bonded-runners | 42 | 5 | 4 | 4 | 4 | 3 | "I wanted the emperor to see one of us. Once." The larger mercy (every bond shortened) is forgotten. |
| d42-the-courier | 42 | 4 | 4 | 3 | 3 | **1** | Spends a boy for intelligence that buys nothing. Neither flag is read. |
| d42-waystation-graves | 42 | 4 | 4 | **2** | **2** | 3 | Thistledown's twin: facing the families free equals paying them 30. |
| d43-defector | 43 | 5 | 4 | 3 | 4 | **2** | The Holloway beat is the act's best competing-goods choice. The 22 guards and the "gate from inside" never matter. |
| d44-crow-name | 44 | 4 | 4 | 4 | 4 | 3 | Complicity reveal with a real confess-or-keep trade. |
| d44-coal-powder | 44 | 4 | **2** | 4 | **2** | 3 | Drowning fen homes buys +10 Moles and no stated payoff. Unquoted speech blurs who is talking. |
| d45-envoy | 45 | 5 | 3 | 5 | 4 | 3 | Strongest petitioner of the act. "Help" is never defined, and `verge-allied` is never read. |
| d46-reedlight | 46 | 5 | 4 | 4 | 3 | 3 | Unpriced debt is classic. The lantern does nothing for the well it was made for. |
| d47-kiyo | 47 | 5 | 4 | 3 | **2** | **2** | "Not brave. Careful." is beautiful. "Go home now" is a fake choice. |
| d47-saffron | 47 | 4 | 4 | **2** | **2** | 3 | Every answer keeps her. Same shape as Kiyo, on the same night. |
| d47-letter-in-the-flour | 47 | 5 | 5 | 3 | 5 | 3 | The best scene in Act V. |
| d48-mara | 48 | 5 | 4 | 4 | 4 | 3 | The shoes at the top of the stair. The quest it sets up is non-lethal, so the warning has no teeth. |
| q-d48-bell-clapper | 48 | 4 | **2** | 4 | 3 | 3 | Two-day quest posted Day 48, so it returns Day 50, after the Day 49 vote that needs it. |
| d49-whose-peace | 49 | 4 | 3 | 4 | 3 | 3 | The "who does it leave out" beat is excellent. The coalition at the fire is static, and the vote can be silently overridden. |
| d49-the-record | 49 | 5 | 4 | 4 | 3 | 4 | Character-revealing epitaph. Good reuse of "Cheaper than war." |
| d50-roads-in | 50 | 4 | 3 | 3 | **2** | **2** | The finale's choice. "Front door" does nothing, "every road" dominates, and ten days of alliances count for nothing. |
| d50-if-you-find-him | 50 | 4 | 4 | 4 | 4 | 4 | Real moral fork with the strongest epilogue payoff in scope. |
| d50-burrows | 50 | 4 | 4 | 4 | **2** | **2** | An earned turnout. Digging versus holding the stairs changes nothing in the fight. |
| q-d50 trio (dispatch / well / bell) | 50 | 4 | 3 | 3 | **2** | 3 | Any one seal wins, so more roads is strictly better unless deaths are made legible. |
| endings.ts | – | 3 | **2** | 3 | **2** | 3 | Short and mostly generic. Four of the eight explain themselves. Bell Restored contradicts the run. |
| epilogue.ts | – | 4 | 4 | **2** | – | 4 | Reads as consequence when a choice flag hits. It flattens to a summary under the Long Night and Hundred Candles, and runs one formula about 70 times. |

## 2. Top problems (ranked)

### 1. The finale ignores Act V. Survival is a stat roll of the party you send.

`endingOf` reads three things: `horror-sealed`, `run.memorials.length >= 2` and the `peace-*` flag.
`horror-sealed` comes only from the three Day 50 quests, and their odds come only from follower stats
and abilities. Every Act V alliance the text frames as war preparation is a dead flag for the fight:

- `verge-allied`: set by 9 options on d45 and read nowhere. The Envoy says "The Verge does not forget a
  debt", and on Day 50 the Verge does not appear.
- `watch-returned` (set 7 times) and `watch-inside-tower` are read nowhere. d43's "turn" option promises
  "Send them back to the tower. Have them open the gate from inside." Day 50 never opens that gate.
- `abbey-road-watched` (Crow watch success: "a line of lanterns went up the Abbey road. None came
  down"), `crow-sightings`, `d42-courier-sent` ("the Abbey kitchens drawn on his arm in soot") and
  `d44-powder-to-crypt` (the keg "for the brick tunnel to the crypt") are all read nowhere.
- `reedlight-lantern` is read only by one epilogue line. Reedlight's pitch is "The well your people go
  into speaks back. Carry a light that doesn't." It has no effect on `q-d46-well-that-spoke`.
- `d50-moles-dig`: "We dig under the Abbey wall … and come up wherever you need a door." It is read only
  by the epilogue. No door appears in the quest.

The result is that the ending's most important axis does not follow from Act V's choices. A player who
built a five-faction coalition and a player who alienated everyone roll the same dispatch.

### 2. The Bell Restored peace is unreachable in a normal run, and it contradicts itself when reached.

- `q-d48-bell-clapper` is posted Day 48 with `durationDays: 2`. `assignQuest` sets `returnsDay = day +
  duration`, and `finishDay` resolves quests with `returnsDay <= next.day`. A Day 48 party therefore
  comes home at **Day 50 dawn**. The Day 49 "bell" peace option requires `clapper-recovered`, so it is
  unavailable unless the party has the swift ability (Rook Bramble or Courier's Spurs) or uses the Brass
  Hourglass. The player is never told this.
- When it is reached, `peace-bell` produces the ending "Hollow Bell rings again, with a clapper fished
  out of the Mirefen". That ending does not require `bell-rung`. A run whose Day 50 bell climb failed
  ("The bell cracked down its whole length without a sound"), or that never climbed, still gets that
  ending text. I sampled it (run D below): the ending says the bell rings, and no epilogue line
  mentions the bell at all, because Mara's subject matched `mara-protected` first.

### 3. A Hundred Candles silently overrides the Day 49 vote, and two endings flatten the epilogue into a summary.

- `HEAVY_LOSSES = 2` counts `run.memorials` across the **whole campaign**. A death on Day 12 and one on
  Day 50 erase whatever the player chose on Day 49. Day 49 never says so. Komodo's (Vellum's) advisor
  line, "Whoever you stand beside tonight shapes the kingdom you come back to", is false in that case.
  No `peace-*` flag is read by the epilogue, so under A Hundred Candles the vote disappears completely.
  In sampled run B, the iron peace, `d49-record-order` and `d43-dunmark-demoted` all vanish behind
  ending-keyed variants.
- Under A Hundred Candles the same image appears **four times in one epilogue**: the ending ("reads the
  names aloud, all of them, slowly"), the Yard ("one loaf for each name"), the Gate Watch ("a candle up
  the wall for each name"), and the Archive ("reads the names of the dead, all of them").
- Under the Long Night, `afterTheWar` disables every variant not keyed to an ending. In sampled run C,
  14 of 15 entries are generic Long Night text. Only Komodo's line remembers a choice
  (`komodo-bargain-known`). The hideout, the deserter and every Act V verdict are gone. That reads as a
  summary, not a consequence.
- There is a real hidden tension that should be made visible: "every road" sends more lethal parties,
  which raises the chance of a second memorial, which overrides the peace. The text never says this, so
  the trade-off cannot be a choice.

### 4. About 47 of roughly 119 Act V flags are never read, and several of those options explicitly promise a consequence.

Never read anywhere in the codebase: `crown-in-exile`, `d41-kitchen-door-open`, `d41-stayers-listed`,
`d41-trust-kept`, `d41-two-hands`, `d41-crown-owns-the-gate`, `d41-sentry-stripped`,
`d41-sentry-testified`, `komodo-ledger-saved`, `stragglers-found`, `cave-fed`, `host-terms-accepted`,
`host-terms-paid`, `d42-letter-to-abbess`, `d42-abbey-water-taken`, `d42-ribbon-taken-down`,
`d42-deserter-sent-away`, `d42-thistledown-named`, `d42-thistledown-repaid`, `d42-millers-ordered`,
`d42-runner-thanked`, `d42-bonds-shortened`, `d42-courier-kept`, `d42-courier-sent`, `d42-drivers-paid`,
`d43-dunmark-absolved`, `d43-holloway-left`, `d43-holloway-tried`, `watch-returned`,
`watch-inside-tower`, `crow-sightings`, `abbey-road-watched`, `d44-powder-to-crypt`,
`d44-coal-sent-off`, `verge-allied`, `d45-sable-first`, `kiyo-sent-home`, `d47-letter-sworn`,
`saffron-stays`, `d47-bridge-remembered`, `d47-cook-exiled`, `d47-false-letter`, `d48-mara-secret-kept`,
`d49-crown-laid-down`, `d50-every-road`, `d50-moles-hold-stairs`, `d50-moles-voted`.

The worst of these are promises in the text itself:
- d41: Vellum says "The record can hold either word, Majesty. Stayed. Or turned. … It keeps the one you
  choose a long time." Neither word is kept.
- d42 freehold ribbon: "By dusk three farms put out an extra bowl. So does somebody who will tell the
  riders." The informant never comes.
- d42 bell water: "Sister Marrow is seen at the edge of town, smiling, counting cellar windows." Nothing
  follows.
- d42 crow cave: Vellum says "By now she knows ours." Nothing follows.
- d49 "Nobody's peace. Lay the crown down tonight." This is the most radical act in the game. It sets
  `peace-roads` plus a flag nobody reads, so it ends identically to Open Roads.

### 5. Day 42 host terms: the demand is a chore, the bargain is a trap, and the dilemma is optional.

The `hostTerms` factory gives every hideout the same top level: accept (+5 host affinity, posts the
host quest), bargain (`requires: { cost: 30 }`, effects only `host-terms-paid`), and ask. Host affinity
drives daily income in hiding (`hostShare`: strength × tier rate), so accept beats bargain on brass,
affinity and future income. Bargain loses on all three.

The reworded `bargainAgain` labels describe effects the bargain does not have:
- "Pay the Saltroad to drop the back six at the next waystation": no Saltroad or Abbey effect, no flag.
- "Pay the Pardoes for their hayricks. Put a price on the grudge": no Freeholds effect.
- "Pay the Conclave to keep its other guest quiet": the messenger is never referenced again.

This is a mismatch between text and mechanics: the text says something happened, and the run never
records it.

### 6. Options that pay brass for what words buy free.

- d42-thistledown: "Say their names back to her" gives `freeholds +5` for free. "Send what brass the
  court can spare" gives `freeholds +5` for 30 brass. Neither flag is read.
- d42-waystation-graves: "Go to the third wagon" gives `saltroad +5` for free. "Pay the families a
  driver's wage" gives `saltroad +5` for 30. `d42-drivers-paid` is never read.

Thoughtful players will not split here. Paying is strictly worse, and the scene teaches that brass is
never worth spending on the dead.

### 7. Fake choices in the last three days.

- d47-kiyo "Tell her to go home to him now": she answers "Not yet. Please. Not yet. After." The flag
  `kiyo-sent-home` is read nowhere, and she is still in the roster for the Abbey.
- d47-saffron: every branch keeps her. "Tell her to choose for herself" gets "Then I choose to stay."
  `saffron-stays` is never read. Only `saffron-free` and the commission differ, and only in the
  epilogue.
- d50-roads-in "The front door. Everyone together." has `effects: {}` and posts nothing. The dispatch
  is already on the board through `quests: ['q-d50-last-dispatch']`.
- d50-burrows: "Dig" versus "Hold the stairs" changes no odds, no ending and no death risk.

Two followers in a row on Day 47 thinking about leaving, and neither able to, is the same beat twice.

### 8. The Day 49 coalition is static, and characters keep their ranks after losing them.

- d49 lines unconditionally seat Oriel, Granny Umber, Corvane, Dunmark, Reedlight and Mara at the fire,
  with "Sister Reedlight has set her lantern on the ground between the Moles and the Crows". This holds
  even after the player blew the north dike (`mire-mothers -20`), refused her lantern, burned Oriel's
  wagons, or seized the Moles' powder. The Verge, even when allied, is absent.
- `d43-dunmark-demoted` ("He takes off his captain's knot and puts it in your hand") is followed on
  Days 49 and 50 by the speaker label "Captain Ferro Dunmark", the costs beat, and "where an advisor
  used to stand."
- Day 50's advisor line says "I will be in the Archive, writing it down." The Archive is either in the
  occupied tower or in a crate by the fire, and the d50-roads-in lines put Vellum at the fire.

### 9. d44-coal-powder offers an atrocity with no reason, written in unmarked speech.

"One opens the north dike and drowns every lantern-house from here to the reed beds. … Then they're
ours." The option costs `mire-mothers -20`, `strength -1` and gains `moles +10`. Nothing explains what
"ours" buys against the Abbess, so the harsh option has no real reason. That is the unicorn-and-puppies
failure. The kind alternative, "Both kegs go to the surveyors, for the crypt road", sets
`d44-powder-to-crypt`, which nothing reads, so the kind option also buys nothing.

Clarity also breaks on the page:
- Coal's lines 3–4, Granny's `who` line, all of Granny's beat lines, and Vellum's line are
  **unquoted**. Every other speech in the file uses curly quotes, so a reader cannot tell narration
  from dialogue.
- Coal offers one keg for each purpose ("I haven't got a third"), but the option reads "Both kegs go to
  the surveyors."

The same unquoted-speech problem recurs in d50-burrows (Granny's lines 2–3, the Lumen beat, and
`vellumSays('Majesty. I have the vote written down. Both numbers.')`).

### 10. Repeated shapes and explaining cuts, worst in the endings.

- Four gate-opener trials (d41 sentry, d42 deserter, d43 Holloway, d47 cook), each offering forgive,
  punish, or a third way. Inside d47, the "witness" third way is reused as "mercy".
- About 22 "ask" probes in 24 audiences, each opening a beat that repeats the parent's options plus
  one.
- 26 Vellum interjections, most of them a closing aphorism ("That is how the important records are
  usually kept.").
- endings.ts explains itself four times: "That turns out to be enough." / "it is held very tightly"
  (an adverb plus "very", against the style guide) / "and it cost too much" / "Somewhere, people still
  tell stories about the emperor who tried."
- Act V responses also tell the reader what to feel: "It is the warmest thing he has ever said to you",
  "The most generous thing you have seen him do. It costs more than brass", "Nobody argues. That is
  worse", "It is worse now. Everyone knows what everyone else is afraid of", "He is quietly proud of it",
  "Corvane says nothing, loudly."

## 3. Rewrite proposals

Each proposal keeps the existing audience and option ids and their current effects unless it says
otherwise. New options and new flags are additions.

### R1. d41-roll-call (Consequence 1)

**The dilemma it should become:** feed the sixty who stayed, which lets spies in, versus list them,
which plans a purge. Both should come due.

- `door-open` (`d41-kitchen-door-open`): read it in d47-letter-in-the-flour. Add a `lines` variant
  keyed to the flag that makes the cook a walk-in. Dunmore: "He came out of the tower kitchens on the
  forty-third night. Through the door you opened. I wrote the board myself." The player who opened the
  door now judges someone who came through it.
- `names` (`d41-stayers-listed`): add a Yard epilogue variant. "Vellum's list of sixty went back up to
  the tower with the crown. Dunmore Ash asked to read it first. He crossed out four names: the dead. He
  handed back the rest and never asked what the page was for."
- `speech` (`crown-in-exile`): give it a cost so it stops being near-dominant (`ledger -1`: the brass
  count waits). Read it on Day 50 in the d50-roads-in lines variant: "Dunmore stands at the edge of
  the fire. He stood up for the speech on the first night. He stands up now."

### R2. d41-trusted-road (Consequence 2)

Keep the three options. Make two of them echo.
- `d41-two-hands`: Gate Watch epilogue variant, placed before the default. "Every order from the tower
  carries two seals now. The second hand belongs to a clerk nobody can bribe, because nobody knows which
  clerk. Dunmark says it slows the Watch by a day. He has never asked to change it."
- `d41-trust-kept`: on Day 50, d50-roads-in costs-beat variant. Vellum: "You wrote that the crown keeps
  trusting people, Majesty. Tonight it trusts whoever holds the rope at the well."
- Alternatively add an epilogue variant: "The crown kept trusting people. It was wrong twice that the
  record knows of. It kept trusting them."

### R3. d41-midnight-gate (Uniqueness 2, Consequence 1)

**Make it distinct from the other trials:** the question is not punishment but whether she ever stands
a gate again. Add option `repost`, with the label "Put her back on the gate. Tonight. Same post." and
effects `{ local: { 'gate-watch': -2, yard: 1 }, flags: ['d41-sentry-reposted'] }`. Response: "The
sergeant opens his mouth. Shuts it. She takes the bar in both hands. All night she does not sit."

Echo it on Day 50 with a d50-roads-in variant line keyed to `d41-sentry-reposted`: "The sentry from
the midnight gate holds the well rope. She has not let go of anything since." Also add epilogue Gate
Watch variants for `d41-sentry-stripped` ("The folded tabard is in the Watch chest. Nobody has worn it.
Nobody has thrown it out.") and `d41-crown-owns-the-gate`. Then cut the forgive/strip/witness triad
from one of the other trials (see R8) so the act does not run the same trial four times.

### R4. Day 42 host terms, all eight (shared skeleton) and the four weak hideouts

**Shared fix.**
1. Add an optional `bargainEffects` to `HostTerms`, merged into the reworded bargain, so each
   `bargainAgain` does what its label says:
   - Caravan: `affinity: { abbey: -5 }`, flag `d42-abbey-wagons-dropped`.
   - Barn: `affinity: { freeholds: 5 }`.
   - Crow cave: flag `d42-messenger-silenced`.
   - Moles: `affinity: { moles: 5 }`.
2. Make the top-level bargain cheaper (15) or give it +2 host affinity, so it is a real alternative to
   lending followers.
3. Use the unread flags. Add one host-patience audience on Day 45 or 46 per hideout, with `requires: {
   flags: ['hideout:<id>'], notFlags: ['host-terms-accepted'] }`. The host comes to collect, and the
   court can be refused. Vane: "The canyon asked again last night, Majesty. I gave it a song. I'm out of
   songs." Options: pay now (cost), give a follower to the host for two days (post a host quest with
   `mustInclude`), or leave the host tonight. Leaving should actually move the court, which needs a
   small engine hook: switch `run.hideout` to `nameless-cave`. This is where "emperor without a
   throne" becomes a felt condition rather than a backdrop.

**d42-terms-crow-cave (Consequence 2, Clarity 3).**
- Name the letter in the label: "Send the messenger home with a letter: the crown knows what is under
  the floor." The player should know what they are telling the Abbess.
- Read `d42-letter-to-abbess` on Day 50 with a d50-roads-in costs variant. Dunmark: "She knows we know,
  Majesty. Your letter said so. She'll have the well watched." Make that option post a harder well
  quest, or add a line that makes the cost legible.
- Read the stay-silent path (acceptAgain) in a Day 47 briefing variant: "Lanterns on the cave road last
  night. Grey ones." That makes "By now she knows ours" true.

**d42-terms-bell-cellars (Consequence 2).** Pay off `d42-abbey-water-taken` with dread, not punishment.
Add a d48-mara lines variant: "The children who drank Marrow's water hum in their sleep now. Not loud.
The same four notes. Their mothers sit up with them." Add a Mara epilogue variant: "The children who
drank the Abbey's water grew up well and quiet. When the bell rings they stop whatever they are doing
and wait. Then they go on." This makes the "kind" option (water for the children) carry a delayed cost
the player was warned about through "counting cellar windows".

**d42-terms-rail-station (Choice 2).** The dominant option is `acceptAgain`: "Strip it with Jinx. Keep
every part out of grey hands." Reshape it so each road costs something:
- Rewrite the acceptAgain label to "Strip it with Jinx. What she does with her share is her business."
  Response: "Jinx tosses you a wrench. At dusk the grey cart comes for the magpie's share. You hear it
  go." Add flag `d42-engine-half-sold`, read later like `d42-engine-sold-grey`.
- Then only `wreck` (Jinx's enmity) and `bargain` (scarce brass) keep the engine dead. That is a real
  split between friendliness, money and safety.
- Give `sell-grey` a moral pull beyond brass. The buyer adds the tower kitchen roster: "Who is still
  alive in the kitchens. Names. Kindly meant." Set `d42-kitchen-roster` and read it in d47 (the cook's
  family is on it).

**d42-terms-nameless-cave (Consequence 2).**
- Add path `who-opened`, label "Ask him who he saw open the gate." It sets `d42-deserter-witness`. Have
  him name the real opener: the sentry (if `komodo-asked-to-stay`) or Komodo's seal and a sergeant (if
  `komodo-escorted`). Sample: "A woman of the Watch. Young. She lifted the bar all the way. She said
  please."
- Read `d42-deserter-sent-away` in the hideout epilogue: "The deserter went into the dark with his
  helmet on. The good blanket went with one of the Moles. Neither came back. The cave kept the horse on
  the ceiling."

### R5. d42-thistledown (Choice 2, Consequence 2)

**Competing goods:** cheap acknowledgment versus a real repair that the court cannot afford twice.
- Change `names` effects to `{ affinity: { freeholds: 2 }, flags: [...] }`. Hester: "Names are free,
  Majesty. That's why I wrote them down."
- Raise `repay` to `freeholds +10` and read `d42-thistledown-repaid` in the Freeholds epilogue: "The
  crown's last thirty brass went into a well-digger's wages. Thistledown's new well is the deepest in
  the Freeholds. Hester drinks from it first, every morning, and says nothing to anyone about why."
- Optionally add a follower option (requires F017 Cobb Harrow): "Send Cobb to Thistledown in the
  morning. The court loses its builder before the Abbey." That costs a body, not brass.

### R6. d42-the-courier (Consequence 1)

`moles.ts` names the courier as **Tobin Umber, Granny Umber's grandson**, and the scene never says it.
Say it, and the scene becomes the act's hardest small choice.
- Line 4 becomes: "Granny says it's your choice. She's my gran. She says it's still your choice."
- Have `send` pay off. Read `d42-courier-sent` in d50-roads-in by adding an option `kitchen-stair`:
  "Take the kitchen stair the boy drew in soot." Effects `{}`, postsQuests `['q-d50-crypt-path']`, so
  the court gets a second road without the Day 46 well quest. The cost is real and was paid on Day 42.
- Have `keep` echo too, with an epilogue Moles variant: "Tobin Umber never carried another letter. He
  digs for the water assembly. Granny Umber says he is the slowest digger in the burrows. She says it
  like a medal."

### R7. d42-waystation-graves (Uniqueness 2, Choice 2)

Stop it being Thistledown's twin. **Competing goods:** the families want a name answered for, and the
name is your Watch.

Rework the final line: "They don't want brass, Majesty. They want the sergeant who rode for Thistledown
that noon to come to the third wagon and say why. He's at your fire."

Options:
- `face`: "Go yourself. The order was the crown's, not his." Keeps saltroad +5 and adds gate-watch +1.
- New `send-sergeant`: "Send the sergeant to the third wagon." Effects `{ affinity: { saltroad: 10 },
  local: { 'gate-watch': -3 }, flags: ['d42-sergeant-sent'] }`. Response: "He goes. An hour. When the
  caravan moves he walks beside the third wagon, not the court's. Nobody tells him to come back."
- `pay` keeps its cost, but read `d42-drivers-paid` in the Saltroad epilogue.

### R8. d43-defector (Consequence 2)

The scene is strong. Make its outcome reach the finale.
- In d50-roads-in, add option `inside-gate`, requires `['watch-inside-tower']`. Label: "Holloway lifts
  the bar from inside. Send the front door in quiet." Posts a new quest `q-d50-inside-gate`
  (might mid, guile mid, heart mid, lethal, seals with `horror-sealed`). The audacious Day 43 choice now
  buys a gentler road.
- Read `watch-returned` in the d50 costs beat. Dunmark variant: "Twenty-two more at the front door,
  Majesty. Half of us singing by the second courtyard is eleven more who aren't." Also grant
  `items: ['watch-buckler']` (guardian 10) on the `welcome`, `oath` and `absolve` options, so the
  returned Watch is a real shield.
- Read `d43-holloway-tried`, `-left` and `-absolved` in Gate Watch epilogue variants. Sample for tried:
  "Holloway carried the camp's water until the war ended, as sentenced. Then she kept carrying it. The
  Watch has stopped telling her she can stop."

### R9. d44-coal-powder (Clarity 2, Choice 2)

**The dilemma it should become:** drown the fen to drown the Abbey's deep well, or keep the fen dry and
walk in through a brick tunnel that may hold.
- Quote every spoken line. Fix "Both kegs" to "The keg goes to the surveyors."
- Give the dike a reason. Coal: "The north dike sits over the Abbey's deep well, Majesty. Open it and
  the fen goes down the well. Whatever she's waking wakes wet." Granny: "And forty lantern-houses go
  with it."
- Make `d44-dike-blown` mechanical. On Day 50, `q-d50-last-dispatch` loses one requirement band (a new
  quest variant `q-d50-last-dispatch-drowned`, posted by a d50 option that requires the flag). Or grant
  an item with `lucky`.
- Make the crypt-road keg mechanical too. `d44-powder-to-crypt` unlocks a d50 option `brick-tunnel`
  that posts `q-d50-crypt-path`. Now both kegs buy a road, and the price of one road is the fen.
- Keep `her-way`. It already pays (`d44-fen-asked` counts toward the Moles' standing).

### R10. d47-kiyo (Choice 2, Consequence 2)

Make "go home" real and costly.
- Engine: add `dismiss?: string[]` to `Effects`. It sets `departed` without the betrayal path, which is
  a small change.
- `home` then dismisses F003, and her field surgery leaves before the Abbey. Response: "Kiyo looks at
  the fire a long time. ‘That's not fair. Using my word.' She packs the kettle last. By dawn the
  infirmary has a needle and nobody to hold it."
- Add a Kiyo epilogue variant keyed to `kiyo-sent-home` that leads the subject: "Kiyo went home on the
  forty-eighth day. Her boy met her at the straits with a beetle in a jar to show her. She let it go
  for him."
- Read `d47-letter-sworn` in the dead-Kiyo epilogue variant: "The emperor crossed the straits with the
  letter that spring."

### R11. d47-saffron (Uniqueness 2, Choice 2)

Make the Pack's offer concrete and time-boxed, so staying costs the canyon something.

Vane's fiddler brings terms: "Come home tonight and the Pack rides to the Abbey wall tomorrow. Stay,
and we stay in the canyon." Options:
- `stay`: she stays. The Pack does not ride.
- `go` (rewrite): she leaves tonight (`dismiss` F002). Effects `jackalwire +10`, and posts a new
  non-lethal support quest, `q-d50-pack-at-the-wall`, or grants `items: ['hyena-tooth']`.
- `commission` stays as written.

A thoughtful player splits: a machinist with jury-rig in the party, or a war band at the wall. This
also separates her from Kiyo, whose dilemma is family. Saffron's becomes allegiance.

### R12. d49-whose-peace (no axis ≤2; included because it is the ending gate)

- Make the coalition conditional: add `lines` variants. If `d44-dike-blown`: "Sister Reedlight did not
  come. Her lantern did, on a pole, carried by a heron you have never met." If
  `d42-abbey-crates-opened`: Oriel's manifest line changes to "Oriel has burned six wagons this month
  and drafted nothing." If `verge-allied`: "The Envoy stands at the edge of the light. Nobody offers
  them the fire."
- Warn about the override in the left-out beat, through Dunmark: "Whatever we sign tonight, Majesty, it
  is a peace for the living. If we bury two more, nobody will remember what was signed. They'll
  remember the names."
- Give `no-crown` its own result: a new ending id `the-charter`, or a dedicated epilogue subject
  variant keyed to `d49-crown-laid-down`: "The charter from the last fire hangs in the tower hall. The
  emperor's name is at the bottom, with everyone else's, in the same ink. Visitors look for it. It
  takes a while."

### R13. d50-roads-in and the Day 50 quest trio (Choice 2, Consequence 2)

**The dilemma it should become:** more roads mean more chances to seal the door, and more chances to
lose a second name and turn any peace into A Hundred Candles. Make that trade legible, and let earned
alliances open safer roads.

- Costs beat, Dunmark, new line: "Every road you open is a road somebody might not come back up.
  Two empty chairs and the peace you chose last night goes with them."
- `front` should mean something. Rename it to "The front door. Everyone together. Nobody goes alone."
  and grant `items: ['watch-buckler']`. Or mark it as the safe choice: "Only the front door. One party.
  One risk."
- Alliance-gated roads, each posting a new lethal sealing quest with different stat demands, so the
  alliance gives you a road your roster can pass:
  - `inside-gate` (requires `watch-inside-tower`), see R8.
  - `under-the-wall` (requires `d50-moles-dig`).
  - `kitchen-stair` (requires `d42-courier-sent`), see R6.
  - `brick-tunnel` (requires `d44-powder-to-crypt`), see R9.
- Alliance boons that do not seal grant existing items:
  - `verge-allied` grants `verge-signet` (heart +3).
  - `crow-sightings` or `abbey-road-watched` grants `signal-coil` (scout).
  - `reedlight-lantern` grants `night-draught` (warden). Its text is a match: "Nobody who drinks it
    dies tonight. Something is owed."
- Make `q-d50-ring-the-bell` lethal. Mara's grandmother's cousin "didn't come down"; Vellum says
  "Somebody has to stand at the top and keep ringing." `d48-no-bell-ringer` then promises that one of
  *your* people dies at the top, which is real.

### R14. d50-burrows (Choice 2, Consequence 2)

- `dig` should open a door (see R13, `under-the-wall`). Then dig versus stairs becomes "a road for the
  court" versus "the burrows live".
- `stairs` should protect something. Grant `items: ['carbide-lamp']` and an epilogue Moles variant keyed
  to `d50-moles-hold-stairs`: "Two hundred and forty-six Moles held the stairs and none of them went
  down. Granny Umber counted them back up at dawn. All there. She counted again."
- Lumen's beat ("Hear the forty") costs "an hour you do not have". Make the hour real: if the player
  votes, the burrows' door opens on the far side of the wall (a harder `under-the-wall` variant).
- Quote every spoken line (see Top problem 9).

### R15. q-d48-bell-clapper timing (Clarity 2)

Pick one fix:
- Set `durationDays: 1` and `danger` to `high` (it is already lethal), so the clapper can be home for
  the Day 49 vote.
- Or post it on Day 47.
- Or make the Day 49 `bell` peace require `bell-promised` and `affinity: { 'hollow-bell': 'friendly' }`
  instead of `clapper-recovered`, and gate the Bell Restored ending on `bell-rung` in `endingOf`.

The briefing on Day 48 should also say "two days there and back".

### R16. endings.ts (Clarity 2, Choice 2)

- Gate `bell-restored` on `bell-rung`. In `endingOf`, a `peace-bell` run without `bell-rung` falls back
  to `open-roads`. Or keep it and rewrite the text so the bell does not ring: "The clapper hangs over
  the chapel door. The town gathered around a bell that did not ring, and decided that was a promise."
- Cut the explaining cuts. Rewrites:
  - Open Roads: "The crown comes home smaller. Councils run the Freeholds. The Saltroad writes its own
    charters. The tower is a place people come to argue. The roads are open."
  - Iron Peace: "The Gate Watch stands on every road. Nobody raids anybody. Nobody sings much. The hands
    that hold the peace remember how close it came, and do not loosen."
  - Long Night: end on "Somewhere, the court is still alive."
  - A Hundred Candles: "The horror sleeps. The kingdom stands. On the first night of every year the
    court lights a candle for each name it lost and reads them all aloud, slowly." This cuts "it cost
    too much".
- Pull the Hundred Candles names image out of two epilogue subjects (Yard, Archive) so the ending owns
  it. Keep Dunmark holding the last candle to his fingers.

### R17. epilogue.ts (Uniqueness 2)

- **The Long Night should remember.** Have `afterTheWar` let through variants keyed to a small
  whitelist of choice flags. Or write Long Night variants for hideout, Mara, Vane and Granny keyed to
  Act V flags. Example (hideout plus `d42-faced-the-thirty`): "The thirty who would have sold the crown
  hold the burrow mouth now. They do not let the singing in. They do not let anyone out."
- **A Hundred Candles should remember the vote.** Add a subject `peace` keyed to `peace-*` plus
  `hundred-candles`. Example: "The charter from the last fire said open roads. Nobody reads it now. It
  is pinned under the candle list, where the wax runs onto it every year."
- **Break the formula.** About 70 of 341 variants are an annual or habitual ritual ("every spring",
  "once a year", "on the first night of every year"). 17 are an anonymous gift or "No letter". 94 end
  on a negative sentence ("Nobody …", "never", "has not"). Target under 30 rituals. Convert some to a
  single dated act ("In the third spring she sold the mill.") or an ongoing present-tense condition
  without an anniversary.
- Add variants for the dead Act V flags listed in Top problem 4, especially `d47-false-letter`. That
  is the best choice in the act, and the epilogue is silent on it. Example: "Three nights of lanterns
  searched an empty valley. The cook's mother and sisters ate every one of those days. The cook does
  not know what the sisters did on the fourth. He bakes as if he does."

## 4. Patterns (counted)

Counts are for `actFive.ts` unless marked otherwise.

| Pattern | Count | Notes |
|---|---|---|
| Probe → hidden truth → beat repeating the parent options plus one | ~22 `ask*` probes in 24 audiences, plus the shared host-terms ask | Almost every Act V audience. The rubric's "same three options again". |
| Gate-opener or failed-guard trial (forgive / punish / third way) | 4 (d41 sentry, d42 deserter, d43 Holloway, d47 cook), 5 with the d42 informant | The emperor-as-judge shape, back at the fire. |
| Vellum interjection (`vellumSays`) | 26 | Usually the closing line before the options, often an "Archive has …" aphorism (9). |
| Host truth = "the Abbey already touched your host" | 7 of 8 hideouts | One per run, so invisible in a single play. A replay will notice. |
| Brass option dominated by a free option with the same effect | 3 scenes (thistledown, waystation, host bargain ×8) | Teaches that paying is never worth it. |
| Follower thinks of leaving; every option keeps them | 2 (Kiyo, Saffron), both Day 47 | |
| "fire" | 64 | It is the act's stage; fine, but every scene opens or closes at it. |
| "lantern" | 39 (+28 in epilogue) | Green lantern, grey lanterns, Abbey road lanterns, Isolde's lanterns, Reedlight's. |
| "count/counts/counting" | 48 (+21 in epilogue) | Oriel, Hester, Vellum, Dunmark, Granny, the court, Wenna all count. Good for one character; diluted across eight. |
| "Nobody" | 79 (+58 in epilogue) | 9 Act V responses end on a Nobody-sentence; 94 epilogue variants end negative. |
| "a long time / long while" | 15 | |
| "For him, that is a speech" family | 4 ("For him, that is a speech", "From her, a speech", "For him, that is dancing", epilogue "In the Yard that is a speech") | Pick one owner. |
| "He never underlines" | 2 (d41, epilogue) | Deliberate callback. Keep exactly two. |
| Kneels or sits "unasked" | 3 (sentry, Dunmark, Mara) | |
| "bows lower than any courtier ever has" | 2 (Envoy) | |
| "It is warm. It smells of rain." | 3 (Reedlight's lantern, identical) | |
| "As long as the Bell stands" | 6 (+1 in the ending text) | An intentional Book One foreshadow. Ration it to 2–3 so it stays a blade. |
| "That is worse" | 2 | |
| Granny bangs her cane and "is delighted" | 2 | |
| Superlative "first time / never seen him" tells | 6+ | "warmest thing he has ever said", "You have never seen him bow", "never seen him do that either", "most generous thing", "has never dimmed before", "first time all evening". |
| Unquoted spoken lines | 12 lines across d44-coal-powder and d50-burrows | The only place in scope where speech loses its quotes. |
| Epilogue annual or habitual ritual | ~70 of 341 | |
| Epilogue anonymous gift / "No letter" | 17 | |
| Act V flags never read | ~47 of ~119 | Full list in Top problem 4. |

## 5. What works (protect these)

1. **d47-letter-in-the-flour.** The confession is on the back of the letter, in the same clear hand.
   Vellum adds, "He is only the one we caught." Mercy then brings "eleven people … family in the tower …
   They have written nothing. Yet." The false-letter option ("Nobody asks what the sisters do when they
   find it empty") is the act's best competing-goods choice. Every option is defensible, and every one
   costs someone you have met.
2. **The caravan crates** (d42-terms-moving-caravan, `open-crates`): "small iron bed-frames and stacks
   of small grey blankets, all folded the same. Oriel looks a long time. Then she burns the six
   wagons." This is horror from mundane objects, exactly to the style guide.
3. **d48-mara, last-ring beat:** "They found the rope. And her shoes at the top of the stair, neatly
   paired." This is the act's best single image. It sets up the bell road; make that road lethal so it
   pays off (R13).
4. **d45-envoy singing beat and Sable's sent-home beat:** "They're perfectly happy. They don't know
   us." Also "Sable sings with the others now. Very well. They always had a good voice." The Freehold
   farmer's "Let them sing" makes aid a choice that costs the player's own people's goodwill.
5. **d43 Holloway beat and d41 midnight gate:** "Take them all back, the Watch learns a sergeant can
   open the gate and be forgiven. Send them all away, it learns twenty-one honest fools went out with
   her." And "lift it all the way, please. The horses are tall." These are competing goods and
   character in a single line each. Keep both, and give them consequences (R3, R8).

Also strong, and worth protecting in the epilogue: Dunmark holding the last candle "until it burns down
to his fingers. Then a while longer"; Komodo spared ("a ledger … correct to the copper"); Kiyo's dead
variant ("At her wake somebody tore the bread small, the way her boy likes it. There were no bells.");
and the `d46-debt-personal` payoff ("The emperor came back with wet hems and slept with a lamp lit for
a month.").

## Appendix: sampled epilogue runs (synthetic flag sets through `epilogueFor` / `endingOf`)

- **A. Mole tunnels, kind run** (charter, fen asked, Verge knelt, false letter, Holloway tried,
  lantern, debt personal, peace-tunnels, sealed). The ending is Tunnels and Councils. 13 entries.
  Consequence lands for the charter, the debt, the Verge, Saffron's commission and Komodo's message.
  Silent on the false letter, Holloway's trial, the returned Watch, the fen walk and the Day 49 record.
  Dunmark, Kiyo and Lumen get their default lines.
- **B. Freehold barn, hard run, two deaths** (iron peace chosen). The ending is **A Hundred Candles**,
  and the iron peace is gone without a trace. Names or candles read aloud appear four times (ending,
  Yard, Watch, Archive). `d43-dunmark-demoted` and `d49-record-order` are shadowed.
- **C. Nameless cave, horror wakes.** The ending is the Long Night. 14 of 15 entries are generic Long
  Night text; only Komodo's line reads a choice. Strong mood, but it reads as a summary.
- **D. Bell cellars, clapper home, peace-bell, bell never rung.** The ending is **The Bell Restored**
  ("Hollow Bell rings again") with no `bell-rung`. No Silent Bell entry appears. Mara's line is the
  `mara-protected` variant. This is a contradiction.
- **E. Wagon circle, "Nobody's peace", crown laid down.** The ending is Open Roads, identical to the
  ordinary roads choice. `d49-crown-laid-down` is unread. Dunmark gets his default line despite having
  "held his gorget, lost."

Sampling script (scratch, not in any repo):
`/tmp/claude-0/-home-user/29d02f93-b2f9-58d4-9a2c-e04749162d07/scratchpad/act5pt/sample.ts`
