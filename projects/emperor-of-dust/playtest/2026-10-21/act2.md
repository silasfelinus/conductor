# Playtest: Act II, Days 11–20 ("Rain Debt")

Scope: every audience and beat in `utils/emperorOfDust/fortress/actTwo.ts` (14 audiences, 20 beats), the 11 Act II quests and their outcome text, the Day 11–20 briefings (plus their variants and Komodo's commentary), and the Day 17 Mole content that `moles.ts` counts. To score consequence I grepped every flag Act II sets across `fortress/*.ts`, plus the `chose:<audience>:<option>` flags. No file reads a `chose:` flag for Days 11–20, so the named flags are the only memory this act has.

## 1. Summary table

Scores run 1–5 on each axis. "—" means the axis doesn't apply: quests have no in-scene choice.

| Scene | Day | Mood | Clarity | Uniq | Choice | Conseq | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| d11-rainmaker | 11 | 4 | **2** | 4 | 4 | 4 | The act's best dilemma. It tells you to read clause eleven and gives you no way to read it. |
| d12-mire-protection | 12 | 5 | 3 | 4 | **2** | 3 | Superb dread. "Investigate" is "defend" plus a free extra quest, so it dominates. |
| d13-saffron-deal | 13 | 4 | 4 | 4 | 5 | 3 | The best faction teeter in the act (Pack, Bell, Saffron). Its Bell flags die before the Bell votes. |
| d14-archive-funds | 14 | 4 | 3 | 3 | 3 | **1** | Lovely map-corner image. No later scene reads any of its three flags. |
| d14-hollin | 14 | 4 | 4 | **2** | **1** | 3 | A recruit card: take the owl, or get +1 lamplight. |
| d15-glass-feathers | 15 | 3 | 3 | 3 | **2** | 3 | Strong mystery hook. Choices are soft and "study" is free. Jinx's hunger costs nothing. |
| d16-hoarders | 16 | 4 | 4 | **2** | 3 | **1** | Yard against Old Houses again. Three of the four main answers leave no flag. |
| d16-bandaged-paw | 16 | 5 | 4 | 4 | 5 | 4 | Protect it. Every answer costs a person you have met. |
| d17-manifesto | 17 | 5 | 4 | 4 | 3 | 4 | The nail holes and the missing page are first-rate. "Meet" costs almost nothing. |
| d18-strangers | 18 | 4 | 4 | 3 | 4 | **2** | Hester and the melted tokens are excellent. Four of its six flags are never read. |
| d18-fair | 18 | 3 | 4 | 3 | 3 | **2** | Pleasant, a little cute. The kind answer loses the recruit and nothing remembers it. |
| d19-bell-vote | 19 | 4 | 3 | 4 | 3 | **2** | The vote ignores everything the crown did to the Bell on Days 13 and 18. Garrison dominates. |
| d20-levy | 20 | 5 | 4 | 3 | 4 | 3 | The white glove and "I know cheap. I've buried it." are strong. One effect contradicts its text. |
| d20-covenant-due | 20 | 4 | **2** | 4 | 4 | 3 | Real competing goods: Yard orphans, Freehold milk, Vask's nephew. The timeline and echoes contradict each other. |
| q-d12-mirefen-defense | 12 | 3 | 4 | 3 | — | 3 | Functional. The triumph line is garbled. |
| q-d12-mirefen-cellars | 12 | 5 | 4 | 5 | — | 4 | "Some jars are small." Protect it. |
| q-d13-water-engine | 13 | 4 | 4 | 3 | — | 3 | "She wept, then denied it." Good. |
| q-d13-engine-sabotage | 13 | 4 | 4 | 4 | — | 3 | Pays off in Saffron's "A Filed Pin" talk. The caught-branch threat is never paid. |
| q-d14-sick-courier | 14 | 3 | 4 | 3 | — | 4 | "Too quickly." Good Komodo seed. |
| q-d15-study-glass | 15 | 4 | 4 | 4 | — | 3 | Rings on the Bell's note. Good. |
| q-d16-hidden-grain | 16 | **2** | 3 | 3 | — | **1** | "A startled goat." Disconnected from the Day 16 audience. Its flag is dead. |
| q-d17-who-lies | 17 | 4 | 4 | 4 | — | 4 | The trail ends at the fortress gate. Good. |
| q-d18-refugee-road | 18 | 3 | 4 | 2 | — | **1** | `refugees-sheltered` is never read. |
| q-d19-bell-speech | 19 | 4 | 3 | 3 | — | **2** | "Somebody was holding the rope." Partial sets no flag. `bell-voted-no` is never read. |
| q-d20-ford-dam | 20 | **2** | **2** | 3 | — | **1** | "Covenant or not" undercuts Day 11. Two villages flood and no one ever mentions it. |

### Focus verdict 1: is the rain covenant a trap the player walks into with open eyes?

**Half yes.** The writing wants it badly and mostly earns it:
- Corvane lists the services "like salt and flour", with "Once, long ago, a name".
- The reeve says: "Whatever's in clause eleven, it isn't hunger."
- Komodo says: "I would still sign. A debt can be argued with. A dead field can't."
- The margin note (`amend`) is a beautiful second trap. Its response warns you outright: "flexible about the coin. Never about the sum." Day 20 then shows you the sum: Hester's goats.

Four things break the "open eyes" half:

1. **The player cannot read the clause.** Corvane says "Clause eleven. Read it if you like." No option lets you. The only reader is Tamsin (`tamsin`, `requires: { follower: 'F011' }`), and her option has no `next`, so it **ends the audience with nothing decided**. You get no covenant and no `no-rain` flag, so your choice simply vanishes. Reading the fine print forfeits the decision the fine print is about.
2. **One Day 20 option can never appear.** `clause-eleven` needs `bonded-runner-clause`, which only `tamsin` sets. The audience needs `rain-covenant`, which only `covenant` and `amend` set. Those options are mutually exclusive, so "Ask about clause eleven, the one Tamsin read" never shows up.
3. **The hidden term isn't fair-hidden.** "A season" turns out to mean nine years, and the only text that hints the Conclave does the counting is Tamsin's terminal reading. A player who signs without Tamsin learns the real price on Day 20 by ambush, not by having read it carelessly.
4. **The narration explains the trap instead of setting it.** "You sign with your eyes open. Corvane enjoys that." / "That is the Conclave's whole art." / Day 20: "You read it with your eyes open, Your Majesty. So did he. He read further." The house style says no lines that explain their own meaning, and here the trap is named three times.

The fix (rewrite proposal A) is small. Add a free `read-eleven` probe that shows the "counted by the Conclave" wording, and make `tamsin` continue into the scene instead of ending it.

### Focus verdict 2: do faction pressures teeter?

**Inside a single scene, often yes. Across scenes, rarely.**
- **Working teeters:** Day 13 (Pack thirst against the Bell's stream against Saffron's trust), Day 17 (`close-race` helps the Moles and stops the Old Houses' mills, and the Yard's flour comes from those mills), Day 18 (Freehold wells against strangers, with Hester's own cousins on the road), Day 20 covenant land beat (Yard children against Freehold milk).
- **Memory gaps:**
  - The Hollow Bell vote (Day 19) is decided only by Day 19 answers. Naming the Bell's saboteur on Day 13 sends a Watch rider to the Bell, then is forgotten. Warning Mara, the drained stream and the refugees walked to her square on Day 18 are forgotten too.
  - Pledging a Watch garrison to the Bell on Day 19 never thins the Watch that Dunmark calls "thin" on Day 20.
  - The Yard can lose its brass (`levy-yard`) and its children (`send-runners`) in the same morning. No line notices.
- **Teeters that collapse into one number:** the Yard/Old Houses local-support seesaw recurs in 6 scenes, always as ±2–5 support. It is the act's default tension, and it is starting to read as a meter rather than as people.

## 2. Top problems (ranked)

**1. The covenant's fine print can't be read, and reading it ends the scene (d11).**
- Evidence: Corvane says "Clause eleven. Read it if you like. Nobody likes it."
- No probe exists. `tamsin` (top level and in `price`) has no `next`. Its effects are `storm-crows -5, lamplight +2, flags bonded-runner-clause, talk-tamsin-bonds`, and the scene closes with no `rain-covenant` and no `no-rain`.
- Day 20 `clause-eleven` is therefore unreachable.
- `recall-clause-nine` leads into `price`, but `price` never mentions clause nine. The payoff is missing.

**2. The rain timeline contradicts itself, and in no-rain runs refusing costs nothing in the fiction.**
- `d20-covenant-due` opens with "The rain came three days ago. It still falls" (Day 17).
- The same morning's Day 20 briefing says "The rains will break over the Eastern Ford within two days."
- `q-d20-ford-dam` says "Rains are coming, covenant or not."
- Days 18–19 are drought scenes ("Our wells are low", "where does a fair find water... in a drought", Day 19 "Pledge the crown's share of the covenant rain").
- A `no-rain` run still gets "rains will break... within two days" and a dam to build against the rain it refused. The epilogue then says "the Freeholds stayed dry."
- No briefing or quest text varies on `rain-covenant` or `no-rain`.

**3. How you settle the covenant is remembered wrongly, or not at all.**
- `court-runners` sets `covenant-paid-in-runners`. So Day 42's bonded runner says "You sent three of us **from the Yard**", and the epilogue says "Children of the Yard climbed the Heights". The player sent clerks' children and Lady Vask's nephew.
- `fixed-term` (three months, "by your calendar") still meets the Day 42 runner: "The bond runs seven more years."
- Day 34 says "Two came home. One stayed." Day 42 says "Two of us fell." Both are gated on the same flag.
- `pay-brass` threatens "We will remember the substitution", in three copies. `covenant-bought-out` is read nowhere.
- `d20-pastures-ceded` is read nowhere. Three hundred goats lose their pasture and nobody mentions it again.
- `one-season` (40 brass on Day 11) sets **no flag**, so the rain you bought has no memory at all.
- Hidden mechanical penalty: `rain-covenant` is a Storm Crow **pledge** (engine.ts `PLEDGES`, weight 20 in the hideout score). Every Day 20 answer clears it. Only runner payments put a pledge back. So `cede-pastures`, labelled "it keeps its promises", silently costs the crown 20 points of Crow host score.

**4. Hollow Bell votes as if Days 13 and 18 never happened (d19).**
- The vote is set only by `garrison`, `water` and `repeal-levy` (`bell-voted-yes`) or by the speech quest's odds, and quest odds ignore affinity.
- These flags shape Hollow Bell and are never read: `d13-bell-saboteur-named` ("A Watch rider leaves for the Bell within the hour. Mara Reedbell will hear the hooves before the reason"), `d13-bell-warned`, `d13-water-shared`, `refugees-sheltered`.
- `garrison` costs only `gate-watch -2` (support starts at 10, so it is usually open), wins the vote outright and sets **two** Bell pledges.
- On Day 20, Dunmark's "The Watch is thin" never mentions the garrison you just sent.

**5. 26 of the 62 flags Act II sets are never read anywhere.**
- `d12-raiders-heard`, `engine-sabotage-caught`, `d13-water-shared`, `d13-bell-warned`, `d13-bell-saboteur-named`, `maps-copied`, `d14-abbey-maps-first`, `d14-ledger-owns-roads`, `d15-vault-watched`, `grain-found`, `d16-border-silver-seized`, `refugees-sheltered`, `d18-water-trade-banned`, `d18-water-taxed`, `d18-crown-tokens`, `d18-fair-water-shared`, `bell-voted-no`, `d19-abbey-questioned`, `d19-coldbrooks-asked`, `ford-dam-built`, `ford-flooded`, `d20-levy-ledger`, `d20-volunteer-bounty`, `covenant-bought-out`, `d20-court-runners`, `d20-pastures-ceded`.
- The worst cases are threats the text makes and never keeps:
  - Gristle Vane "will show [the filed bolt] to people".
  - The Verge "do not, I am told, accept apologies".
  - "Corvane: We will remember the substitution."
  - "The Ford flooded two villages." The Moles live in the Ford tunnels (Day 17), and nothing connects the two.

**6. In the Mirefen scene, investigating strictly beats defending (d12).**
- `defend` and `investigate` both have `effects: {}`. `investigate` posts both quests.
- `q-d12-mirefen-cellars` has `expired: {}`, so posting it and ignoring it costs nothing.
- The scene's real question is protecting children who are in the houses now against learning whether the houses took children. That question is never priced. The one answer that takes the raiders' side, `hear-raiders`, sets `d12-raiders-heard`, which is never read.

**7. The Yard/Old Houses seesaw is the default shape (6 scenes), and the Day 16 audience leaves no trace.**
- The six: d16 hoarders, d17 `close-race`, d18 Vask's well line, d19 `repeal-levy`, d20 levy, d20 `court-runners`.
- In `d16-hoarders`, `requisition`, `buy`, `leave` and `council-vote` set **no flags**.
- `seize-silver` is near-dominant. It gives +20 brass and `yard +2`, and it hurts the Old Houses *less* than `requisition` (−3 vs −4). Its threat from the border buyer is never paid, even though Day 20 reveals the Verge "pay in silver."

**8. Soft-choice scenes: d15 feathers and d14 Hollin.**
- Jinx: "The Yard has forty mouths and no harvest. Studying feeds nobody." Yet `study` is free, and quest success gives `rustline +10`, a recruit and `lamplight +3`. The hunger costs the Rustline nothing.
- `watch-car` ends "They watch an empty car." That setup is never paid off.
- `d14-hollin` offers `welcome` (recruit F019, `lamplight +1`) or `archive` (`lamplight +2`). No one loses anything.

**9. Effects contradict their own text.**
- `levy-ledger`: "interest on every Yard loan in the market has risen by exactly the levy", yet effects give `yard +1`.
- `ledger-copies`: "Let the Ledger pay its half." Tallow offered "half the cost". The option costs the crown nothing.
- `wells-shared` (pay the Freeholds to open wells, `freeholds -5`) is a **Freehold pledge** in engine `PLEDGES`.
- `name-culprit` (Day 13) posts no quest, so the Pack's engine stays broken. The text never says so, and the Pack still gets `+5`.
- `d11 amend` says "the Old Houses, who own most of the high pastures." Day 20 says the Freeholds graze them ("every Freehold child's milk"). The victim the scene foreshadows is not the one who pays.

**10. One template for every audience.**
- 13 of 14 audiences follow the same shape: opener, Komodo aside, an "Ask…" probe, then a beat that repeats the same three answers with new labels plus one or two new ones.
- Komodo speaks in **14/14 openers and 17/20 beats**. He often states the dilemma for you, for example "Repeal the levy and you buy eleven hands with the poor wards' water. Keep it and lose the Bell for keeping your word."
- Briefings are exactly two true and one false on **10/10 days**, and Komodo debunks the false one on **9/10**. The Day 17 lie is a strong payoff, but it makes the briefings a solved puzzle.

## 3. Rewrite proposals

Each proposal keeps existing audience and option ids and effects unless it says otherwise. New options are additions.

### A. d11-rainmaker (Clarity 2): let the player read the clause, and make reading it cost something other than the choice

**Problem.** The scene says "read it if you like" and gives no way to. The only reader (Tamsin) ends the audience without a decision. That orphans Day 20 `clause-eleven`. The scene also spells out its own trap.

**Changes:**
1. **New probe in `price`:** `read-eleven`.
   - Label: "Read clause eleven yourself before anyone signs."
   - `effects: {}`, `next: 'eleven'`.
2. **New beat `eleven`.** Lines:
   - "The hand is old and close. The ink has gone brown. Clause eleven: *The service owed may be paid in runners, the season to be counted by the Conclave.*"
   - "You read *counted* twice. Corvane waits. He has waited for that word before."
   - `{ who: 'A Freehold reeve', text: 'How long's a season, to a crow?' }`
   - `{ who: 'Young Komodo', npc: 'young-komodo', text: 'Nobody in this hall knows, Your Majesty. Only one person does, and he is smiling.' }`
3. **Options in `eleven`:** the existing `covenant`, `one-season`, `refuse` and `amend` (same ids and effects), plus a new option:
   - `amend-term`: "Sign, and write in the margin: a season is ninety days, by the tower's calendar."
   - Effects: `storm-crows +5, freeholds +10, yard +2`, flags `['rain-covenant','d11-term-fixed']`.
   - Response: "Corvane reads the margin a long time. He initials it. 'Ninety days,' he says. 'By your calendar.' He does not ask whose hand keeps it."
   - Day 20 then honours `d11-term-fixed` by opening the `fixed-term` result directly. Its own term is already written, so it makes a tidy echo.
4. **Make `tamsin` continue the scene instead of ending it.** In both places, keep the effects and add a `next`: top level gets `next: 'price'`, the `price` copy gets `next: 'eleven'`. Tamsin's reading becomes the witness, not a forfeit, and `bonded-runner-clause` can now coexist with `rain-covenant`, which makes Day 20 `clause-eleven` reachable. Stark addition to her response: "She stops. 'I was counted,' she says. 'Eleven years.' She does not finish the page."
5. **`recall-clause-nine` payoff.** Add a `variants` entry to `price` keyed on `crow-contract-read`, with this line first: "'Clause nine is gone, as your readers wished,' says Corvane. 'The Conclave names the favour before the rain now.' He taps the cloth. 'In eleven.'"
6. **`one-season` memory.** Add flag `d11-rain-bought`. Day 19 `water` could accept either flag, and the epilogue and Nera's talk get a third branch.
7. **Cut the explaining lines:**
   - Covenant response: change "You sign with your eyes open. Corvane enjoys that." to "You sign. Corvane watches the pen to the last letter."
   - Komodo in `price`: drop "That is the Conclave's whole art."
8. **Fix the pasture owner in `amend`'s response:** "...the Old Houses, who lease the high pastures to Freehold herds, begin to whisper." The effects stay the same, and the foreshadowing now points at Hester.

### B. d20-covenant-due (Clarity 2): fix the clock and make the echoes match what was paid

1. **Timeline.**
   - Opener: change "The rain came three days ago. It still falls..." to "The rain broke before dawn. It falls soft and steady from the Ford to the Bell."
   - Add a Day 20 `rains-coming` briefing variant keyed on `rain-covenant`, source Storm Crow Heights: "The Conclave's rain broke over the Heights before dawn. It is walking toward the Ford."
   - Add a variant keyed on `no-rain`: "Clouds over the Heights. They stop at the tower's border, like a line drawn with a rule." This matches the epilogue's later image.
2. **`q-d20-ford-dam` summary.** Change "Rains are coming, covenant or not" to "The Ford's old dam is cracked. The first real rain will take it, whenever it comes."
3. **Yard pile-up.** Add a `variants` entry to `season` keyed on `levy-yard`, in place of Dunmore's line: `{ who: 'Foreman Dunmore Ash', text: 'You took the Yard's brass at breakfast, Majesty. Now three of its children. Is there a third thing? I'd like to know before supper.' }`
4. **Downstream branches** (in actFour.ts, actFive.ts and epilogue.ts, listed here because they echo this scene):
   - Day 42 bonded runner: if `d20-court-runners`, she says "You sent three of us from your own households. I was the clerk's girl." If `d20-runners-term-fixed`, replace "seven more years" with "They let the other two go on the day, to the hour. They kept me. I asked them to."
   - Day 34: gate "Two came home" on `d20-runners-term-fixed`. Otherwise use "None have come home. It has been a month. A season is a long word."
   - Epilogue `runners`: add a `d20-court-runners` branch, for example "Lady Vask's nephew came down from the Heights a grown bird who would not sit at her table."
5. **Make the substitution threat real.** Read `covenant-bought-out` in one later Crow beat, for example in Act III or IV: "The Conclave's forecast arrives a day late, every time. Exact."
6. **Pastures.** Read `d20-pastures-ceded` in the next Freehold audience. Hester: "Goats on the low road now, Majesty. Eating the verge to the root." Also count `d20-pastures-ceded` (and `covenant-bought-out`, if desired) as Storm Crow `PLEDGES`, so keeping the deal doesn't silently cost the Crow host score.

### C. d12-mire-protection (Choice 2): price the trust

**Problem.** `investigate` is `defend` plus a free quest. The real hinge (the eleven names) has no cost.

1. **New option `swear-unsearched`** in `grievance` and at the top level:
   - Label: "Hold the edge, and swear before the court that no one of the crown's will set foot in the lantern-houses."
   - Effects: `mire-mothers +10`, flags `['d12-houses-sworn']`. Posts `q-d12-mirefen-defense`.
   - Response: "Sister Reedlight's lantern stands dead still. 'Sworn,' she says. 'The fen heard it.' The young newt at the back closes her eyes."
   - A later Mothers scene, or the cellars talk options, reads the oath. If the crown searches anyway, through another route or Lumen's talk, the Mothers say so aloud.
2. **New option `names-first`** in `grievance`:
   - Label: "Ask the Mothers to say the eleven names, here, before a single blade goes to the fen."
   - Effects: `mire-mothers -5`, `lamplight +2`, flags `['d12-names-spoken']`. Posts `q-d12-mirefen-defense`.
   - Response: "She says them. All eleven. In the order the raiders shout them. She has been listening too."
3. **Give the cellars quest a cost when ignored:** `expired: { affinity: { 'mire-mothers': -5 }, flags: ['d12-cellars-unlooked'] }`. The Mothers saw the crown post a search and not dare it. This stops "investigate" from being free.
4. **Wire `d12-raiders-heard`.** Add a Day 18 `road` variant line for Hester: "Low Carrow folk too. They say the crown listened to them once. They're walking here to see if it does twice."

### D. d14-archive-funds (Consequence 1): make the maps matter later

- **Wire `d14-abbey-maps-first`.** Add a probe in the next Abbey audience: "Ask why a sister wanted the plans of what stood on the Abbey's hill." Gate the Abbess's answer on the flag: "Because it is still standing, Majesty. Underneath."
- **Wire `maps-copied`.** A bonus or extra option for one Act III/IV tunnel or Ford quest: "The Archive's copy shows a second shaft at the river end."
- **Wire `d14-ledger-owns-roads`.** Add a later Saltroad petition: "The Ledger charges us a toll to read our own roads, Majesty. You sold them."
- **Fix the label:** change `ledger-copies` to "Let the Ledger pay for the copying and keep the trade-road copies." The effects stay the same.

### E. d14-hollin (Uniqueness 2, Choice 1): the last copy, or the last wish

**Problem.** Taking the owl costs nothing, and the alternative is +1 lamplight.

- **New opener line** (Keeper Vellum, from the gallery): "Half the roads he drew are only in his head, Majesty. If he dies on a road, the road dies with him."
- **Keep `welcome` and `archive`** with their effects. Add a line to `welcome`'s response: "Vellum bows, very slowly. 'Send him back to me when he is dying,' he says. 'I will need a week.'"
- **New option `dictate`:**
   - Label: "Take him at court. Send a scribe to sit with him every night until the roads are on paper."
   - Cost 10. Effects: `recruitable F019`, `lamplight +1`, flags `['d14-hollin-dictates']`.
   - Response: "Hollin looks at the scribe, then at you. 'Every night,' he says. 'Owls are awake at night. Scribes are not.' The scribe goes grey by the second week."
- **Optional cost on `welcome`.** If Hollin dies on a quest without `d14-hollin-dictates`, emit the event "The roads in Hollin's head are gone. The Archive marks three shelves *unknown*."

### F. d15-glass-feathers (Choice 2): make the hunger real and the buyer close

**Problem.** "Studying feeds nobody", yet studying feeds the Rustline the most. The mystery buyer is never connected to anything.

1. **New option `sell-to-tallow`** in `vault`:
   - Label: "Let the Ledger buy the crate tonight. The Rustline eats."
   - Effects: `rustline +10, ledger +3, lamplight -2`, flags `['d15-feathers-to-ledger']`.
   - Response: "Factor Tallow pays triple without counting. 'A buyer in the east will be so pleased,' she says, and stops, and smiles, as if she had not said it."
   - Now selling feeds forty mouths and arms the other buyer, while studying keeps the secret and starves the Yard.
2. **Give the hunger a visible cost.** Add a response line to `study` in `vault`: "That week two Rustline kits are caught eating the Archive's paste." Better still, a small `rustline -5` on `study`, offset by the quest's `+10`, so the cost lands first and the reward only if the study succeeds.
3. **Wire `d15-vault-watched`.** In Act III or IV, the lookouts report who came to the car, whoever the plot names (grey sisters or white gloves): "Two whistles in the night, Majesty. Then one."

### G. d16-hoarders (Uniqueness 2, Consequence 1): turn the seesaw toward the border

**Problem.** It is the sixth Yard/Old Houses seesaw, three of its four main answers leave no flag, and the "people who do not accept apologies" go nowhere.

1. **Add flags to the existing answers:** `requisition` → `d16-granary-requisitioned`; `buy` → `d16-surplus-bought`; `leave` → `d16-grain-sold-east`.
2. **New option `follow-grain`** in `spoken-for`:
   - Label: "Let the grain go east. Put a rider on the carts and see who eats it."
   - Effects: `yard -3, old-houses +2, lamplight +2`, flags `['d16-grain-followed','d16-grain-sold-east']`.
   - Response: "Dunmore picks up the empty sack. Folds it. Puts it inside his coat. 'I'll keep this for when your rider comes back,' he says."
3. **Day 20 `plum` beat variants:**
   - If `d16-grain-followed`, Dunmark adds: "Rider came back. Their horses were eating Freehold oats out of Old House sacks."
   - If `d16-border-silver-seized`, the gloved rider asks the sergeant "after some silver that went astray," and `answer-verge` costs more Verge affinity.
4. **Balance `seize-silver`.** Add `black-verge -10` so the silver has an owner, or take `yard +2` down to `+1`.
5. **`q-d16-hidden-grain`:** see quest note J.

### H. d18-strangers (Consequence 2): every ruling should reach the road

- **`d18-crown-tokens`.** The crown "answers for any forgeries", so make it answer. In Act III, Hester: "Sixty crown tokens on the road this week, Majesty. You sealed eleven." Offer a choice there: pay for the forgeries, or call in the tokens and betray Thistledown.
- **`d18-water-taxed`.** An epilogue or Act III line: "The clerk at the back gate kept a table there until the war. The road called it the crown's well."
- **`d18-water-trade-banned`.** Show the cost. A Day 21+ briefing (true): "A stranger died at a Freehold back gate with brass in his fist. Nothing to spend it on."
- **Pledge mismatch.** `wells-shared` is currently a Freehold `PLEDGE` while costing Freehold affinity. Move it to the Hollow Bell pledges, or replace it with `wells-closed`. That one sides with the Freeholds, and Keel's talk already reads it.

### I. d18-fair (Consequence 2): remember the night the fair gave its water away

- **Wire `d18-fair-water-shared`.** Let Vesper be recruited later (for example Day 22, through a variant) with: "You made us pour cider water on the road. I juggled for people who couldn't pay. Turns out I liked it. Got a bed?"
- **Trim the cute register.** Change "three goats objecting" and "So do you, by the look of you" to: "You hear the fair first. A fiddle. A drum. A goat screaming like a person." Vesper: "The Yard needs a night off, Majesty. You look like you need a year."

### J. d19-bell-vote (Consequence 2): the Bell remembers

1. **Opener variants.** Mara's second line changes by flag:
   - `d13-bell-saboteur-named`: "Your Watch took the Hessle boy out of his mother's mill on Day Thirteen, Majesty. Seventeen. She votes tomorrow. So do her cousins."
   - `d13-bell-warned`: "You sent word before the Pack's engine drank our stream. The Bell remembers who knocks first."
   - `refugees-sheltered`: "Forty of your strangers sleep in my square. Half can't vote. The other half watched who walked them here."
2. **New option `free-miller-son`** (requires `d13-bell-saboteur-named`):
   - Label: "Release the miller's son into Mara's custody before the vote."
   - Effects: `hollow-bell +10, jackalwire -10, gate-watch -1`, flags `['d19-miller-son-released','bell-voted-yes']`.
   - Response: "Mara signs for him like a parcel. Down the canyon, Gristle Vane hears the bell ring and knows exactly what it cost him."
   - This is a real Pack-against-Bell teeter, aimed at the man who named him.
3. **Garrison cost.** Keep the effects, and have Day 20 read `bell-under-protection`. Dunmark's list in the `d20-levy` opener: "Twelve of these gaps are at Hollow Bell, Majesty. You put them there yesterday."
4. **Wire `bell-voted-no`.** In Act III, the Bell's gate is shut to the crown's riders on a quest, or the Abbey's soup carts are in the square.
5. **Clarity.** The `speech` label should signal that it is a gamble: "Send someone to make the case in the square. The vote turns on how they do."

### K. Quests with an axis ≤ 2

- **`q-d16-hidden-grain`** (Mood 2, Consequence 1):
   - Replace "The third held hay and a startled goat." with "The third held hay. And a Gate Watch lantern, still warm."
   - The lantern implies the Watch was in on it. Read `grain-found` in Day 20 `d20-levy`: "Dunmark's list is shorter by two names this morning. He doesn't say why."
- **`q-d18-refugee-road`** (Consequence 1): read `refugees-sheltered` in Day 19 (see J). The success line could add "Mara wrote every name. Then she looked at the crown's riders and wrote theirs." Note this is the fourth "wrote every name".
- **`q-d19-bell-speech`** (Consequence 2):
   - The `partial` result sets no flag. Add `bell-vote-tied`, and let one later Bell scene read it: "Mara never says which way she broke the tie. The garrison she asks for says it for her."
   - Read `bell-voted-no` (see J).
- **`q-d20-ford-dam`** (Mood 2, Clarity 2, Consequence 1):
   - Summary: see B.2.
   - Failure line: "The dam failed. The Ford took two villages and came through the burrow ceilings again."
   - Add `ford-flooded` to the Mole grievance list, or read it in the next Mole scene: "You said talks. The water didn't wait for them." This connects to Day 17's "Mind they're quicker than the water."
   - Read `ford-dam-built` in an Act IV map-room beat, where the reservoir actually exists.
   - Fix the triumph line in `q-d12-mirefen-defense` too: "had the throne room for a witch" → "did the throne have room for a witch who disagreed with her elders?"

## 4. Patterns (counted across actTwo.ts)

| Pattern | Count | Notes |
|---|---:|---|
| Audience template: opener → Komodo aside → "Ask…" probe → beat that repeats the base three answers + 1–2 new | 13 / 14 audiences | Only `d14-hollin` breaks it. Expect a probe, a truth, the same three answers plus a better one. |
| Young Komodo speaks in the opener | 14 / 14 | He speaks in 17 of 20 beats too. He often states the dilemma's thesis ("Somebody pays for this levy… who gets to call it fair"; the millers' line; "They are arguing about each other"). |
| Briefings: exactly 2 true + 1 false | 10 / 10 days | Komodo identifies the false one on 9 of 10. It builds trust for the Day 17 lie, but no day risks two lies or a misleading true one. |
| Probe "tell": an accessory or habit stops when the probe lands | 10 | Rings stop clicking, ear-chain stops, chimes go quiet, hands tighten, Jinx and Pell glance, Hester's feathers, Vesper juggles, Mara glances, Dunmark folds, Corvane tilts. Good once; formulaic by the fifth. |
| "Small gesture = huge feeling, for this species" | 6 | "For him, that is dancing" ×2 (both `fund` responses), "In an owl, that is a great deal of feeling", "In a crow his age, a shrug", "the most excited he has been all day", "in a better week, would have been a laugh". |
| Someone writes in a book as a reaction | 10 | Mara "writes one word/line" ×4, Vask "writes something down" ×2, Tallow ×2, "Komodo writes nothing down", Corvane writes the term. |
| Lists of names written or spoken | 8 | Eleven children's names ×2, forty families' names ×3, Mara writes every name ×2, Thistledown tokens "by name". |
| The number **eleven** with three meanings | 14 occurrences | Clause eleven (covenant), eleven children's names (Mirefen), eleven hands (millers / Bell vote). Three unrelated elevens in ten days read like a clue that leads nowhere. Change the millers to "nine hands". |
| "a long moment" / "looks at you a long moment" | 7 | |
| "the colour of a bruise" | 4 | Three identical `break` responses, plus the Verge plum coats on the same day. |
| Verbatim duplicate responses | 3 sets | "We will remember the substitution" ×3, "Komodo looks relieved…" ×3, "We'll make do. Until we can't." ×3. |
| Yard vs Old Houses local-support seesaw | 6 scenes | d16, d17, d18, d19, d20 levy, d20 court-runners. |
| Brass-gated "pay to make it kinder" option | 15 distinct options (25 counting beat duplicates) in 11 of 14 audiences | Usually the kindest answer. Brass is tight (loans common in the balance sim), so it is a real cost, but the shape is constant. |
| "Nobody …" sentences | 27 | 8 of them in quest outcomes ("Nobody went down", "Nobody came in time", "Nobody believes it"…). |
| Flags set but never read | 26 of 62 | Listed in Top problem 5. |
| Narration explaining its own meaning | 6+ | "You sign with your eyes open"; "That is the Conclave's whole art"; "That is the worst of it"; "She is not sure that is a relief"; "Everyone is a bit unhappy" ×2 (also flat); "eyes open… He read further." |

## 5. What works (protect these)

1. **`d16-bandaged-paw`.** "She looks at her bandaged paw. Then she holds out the other. It is bandaged now too." Every answer costs a fifteen-year-old you have met. The `spy` response ("The next one is late. The Watch pins both above the fire and waits for the third.") is the act's best line. All four answers echo in the epilogue.
2. **`d17-manifesto` `seal` beat.** "Two nail holes at the top, two more a hand lower, where a second sheet could have hung behind it." It pays off Komodo's briefing lie in the same scene without saying so. `write-names` ends with Komodo offering, kindly, to file the page himself. Pure dread, no adjectives.
3. **The Mirefen thread** (`grievance` and `count` beats, plus `q-d12-mirefen-cellars`): torches shouting eleven children's names into the reeds; the vole in a reed cloak much too big for him; "Jars… Some jars are small. The party took the ledger and left the jars."
4. **`d18-strangers` `tokens` beat.** "Brass tokens melt, did you know that? I didn't. Little puddles in the ash." Hester's tears on `freehold-rights` give the harsh answer a real reason. Thoughtful players will split here.
5. **The covenant's Day 20 `land` and `season` beats.** "We are not cruel, young ruler. We are exact." Hester: "You wrote that margin. You never asked us what it cost." Here the trap lands on someone you have met. Fix the clock and the clause (proposals A and B), and this becomes the spine of the act.

Honourable mentions:
- Day 13 Saffron: "I built it to sip, not gulp."
- Day 20 white glove: "He's been sick since." Also "I know cheap. I've buried it."
- The Day 14 courier: "Komodo let the court keep it. Too quickly."
