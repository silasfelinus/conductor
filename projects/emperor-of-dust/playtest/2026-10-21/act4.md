# Act IV playtest: Days 31–40, "The Long Table"

Scope: every audience, beat, quest, briefing and variant in `utils/emperorOfDust/fortress/actFour.ts`, the Mole content on these days (`moles.ts` hooks, d32 reform list, d33 sappers, d35 tunnel, d38 courier), and the betrayal handoff in `betrayal.ts` (buyer `fell`/`why` text, departure lines and reasons). Flags were checked against every `.ts` file in `fortress/`. A flag counts as read only if some other scene, talk, briefing variant, engine rule or epilogue reads it. The automatic `chose:` flags are read nowhere in this scope.

**Headline numbers**
- Act IV sets **105 story flags. 55 of them are never read anywhere.** Most of those 55 are the precautions a suspicious player takes against Komodo (Days 35–40).
- **52 distinct options win a kingdom faction's favour. 21 cost a rival faction, 19 cost only an internal local faction (Yard, Watch, Old Houses, Ledger, Lamplight), and 12 cost no enemy at all**, at most some brass.
- **13 of 15 audiences open with a free probe.** In most of them the probe beat re-offers the top-level options plus one better one.
- **Young Komodo speaks in 15 of 16 audiences** (22 interjections), plus every morning line.
- **No Act IV audience uses a scene `variant`.** All 5 variants are briefings. No petitioner's opening lines ever change because of what the crown did earlier.

---

## 1. Summary table

Scores are 1–5. Choice is the central axis.

| Scene id | Day | Mood | Clarity | Uniq | Choice | Conseq | Verdict |
|---|---|---|---|---|---|---|---|
| d31-muster | 31 | 4 | **2** | 3 | **2** | **2** | Strong walls-vs-farms setup ("somebody burns a farm to empty them"). Then the Rustline option wins on every axis, and the quest board ignores the whole audience. |
| d32-ledger-page | 32 | 4 | 4 | 4 | 3 | 4 | A good clue scene. The trap option is honest, and burning the page has a reason and a later bill (d37). |
| d32-reform-list | 32 | 3 | 4 | 3 | 4 | 4 | The best-built Mole choice in the act: each reform costs a different house, and `seat-coal` is a real third road. |
| d33-both-roads | 33 | 4 | **2** | 3 | 3 | 3 | "Noon is when Thistledown eats" is superb. But a promise made here binds nothing on the board, and the "Gate Watch to Thistledown" option can still end in `thistledown-abandoned`. |
| d33-sappers | 33 | 5 | 4 | 4 | 3 | 3 | Reed knots, a lantern with no oil, and Umber's one-word "Most." are the act's best mood. The probe path ends in a +5/+5 win-win. |
| d34-crow-debt | 34 | 4 | 3 | 3 | 3 | 3 | "Pay brass or say no" again, saved by the water-rights option and Tamsin's beat. `wages` nearly dominates. |
| d34-outer-court | 34 | 4 | 4 | **2** | **2** | **1** | Feed / arm / send home: one faction, small numbers, and all three flags unread. A good gatepost image and nothing else. |
| d35-two-bridges | 35 | 4 | 3 | 4 | 3 | 3 | A real fork that feeds the hideout. `saffron` beats `trestle` outright, `secret-tunnel` beats `tunnel` and does nothing, and quest results are ignored. |
| d36-invitation | 36 | 5 | 3 | 4 | **2** | **1** | The best dread in the act ("sing toward the floor so the floor will learn the tune"), with no payoff. Sitting at the front, the decoy, and sending Teodor or Komodo all evaporate. |
| d37-market-closed | 37 | 4 | 4 | 3 | 4 | 3 | Competing goods: brass vs the Saltroad vs the Ledger vs the Yard vs the truth. `read-debts` is a great paid clue. |
| d37-dark-yard | 37 | 4 | 4 | 3 | 3 | **2** | A good bill for burning the page. `oil` buys its way out of the question, and only `silence` is ever remembered. |
| d38-pardon | 38 | 5 | 4 | 4 | 3 | 4 | Rust on the boy's cheek, two taps on the chain. The strongest scene in the act after Day 40, and also the loudest tell. |
| d39-congress | 39 | 4 | 3 | 4 | 4 | 3 | Every seat costs someone, and "a chair for whoever does not come" lands. But the coalition this congress supposedly forges is invisible. |
| d40-sealed-order | 40 | 4 | 3 | 3 | 3 | **1** | Recall, stand and check-the-seals are all forgotten. Day 43 opens "Half my night watch rode out on an order under your seal" even after you tore that order up. |
| d40-archive | 40 | 4 | 4 | 3 | 3 | **2** | "Keys clenched so they will not ring." The sealed name is never opened, and `morning` has no reason to exist. |
| d40-quiet-word | 40 | 5 | 3 | 5 | 3 | **2** | The best-written scene in Act IV, but not yet the best scene in the game: it can be skipped in one click, the perceptive path skips the physician question, and the answer to that question is never remembered. |
| Betrayal handoff (`betrayal.ts`) | 41 dawn | 4 | 3 | 3 | n/a | **2** | "Lanterns and soup" is perfect. Every precaution from Days 35–40 is ignored, and if Komodo is in a cell he still "opened the gate at midnight". |

Quests (scored briefly, since their choices live on the board):

| Quest | Day | Mood | Clarity | Uniq | Conseq | Note |
|---|---|---|---|---|---|---|
| q-d31-iron-rain | 31 | 4 | **2** | 3 | 3 | `ford-held` is unread. Its `expired` text ("Nobody rode to the Ford") contradicts `watch-marched`, `pack-hired-ford` and `rustline-barricades`. |
| q-d33-thistledown / q-d33-waystation | 33 | 4 | 3 | 3 | 3 | The abandoned flags are read. The defended flags are mostly unread. The waystation success line "On the Saltroad, same thing." is unclear. |
| q-d35-trestle / q-d35-tunnel | 35 | 5 | 3 | 4 | **1** | "A long orange comb. Then like nothing." is great. Held, burned and collapsed are all unread, so the `route-tunnel` pledge still counts after the Moles bring the roof down. |
| q-d36-bell-rehearsal | 36 | 5 | 3 | 5 | 3 | "Small shoes in a row, toes to the wall" and the "Paid." column are the best quest prose in the act. The tally book (`abbey-crypt-ledger`) and `rehearsal-caught` are unread. |

---

## 2. Top problems (ranked)

### 1. Seeing Komodo coming buys the player nothing. 23 precaution and confrontation flags are dead, and the Day 41 dawn contradicts several of them.

These are the options a perceptive player takes against Komodo. None is read by any later scene, the dawn, or `betrayal.ts`:
- `d35-tunnel-secret` ("Let the court believe you chose the trestle. Your advisor too.")
- `d38-hall-cleared`
- `d40-watch-recalled`, `d40-seal-order-stood`, `d40-seals-checked`
- `d40-vellum-sealed-name`
- `d40-komodo-confronted`, `d40-komodo-pressed`, `d40-komodo-asked-tomorrow`
- `d40-komodo-held`, `d40-komodo-followed`, `gate-doubled`
- `d36-komodo-at-rehearsal`
- The four answers to the physician question: `d40-komodo-told-ask`, `-told-do-it`, `-told-no-cure` and `-asked-who`.

`d38-rosters-changed` is read once, by a briefing variant that says the change did not help. The pattern holds back to Day 31, where `watch-marched` is also unread.

Contradictions this produces:
- **`cell`** ("Have the Watch hold him in the cells until morning") ends: *"At the bottom he asks the guard, kindly, which cell the Mole boy had."* That is the best line in the act. The next page reads `BUYERS.abbey.fell`: *"Young Komodo opened the gate at midnight with your seal."* No variant explains the cell.
- **`recall`**: Dunmark tears the order up. Day 43 (`d43-defector`) still opens: *"Half my Watch rode out on an order under your seal, Majesty."*
- **`secret-tunnel`**: you lie to the hall and Granny Umber gives you tunnel chalk ("Now forget where it goes."). Nothing reads it. It has the same effects as `tunnel` plus a flag, so it is strictly dominant and does nothing.

The betrayal is fixed by design, and that is fine. But if foresight never changes *how* the tower falls, *what* is lost or *who* goes, the tells are fair to read and pointless to act on. That is the "mechanical vs moral mismatch" failure in its most expensive form. See rewrite proposals R8 and R9.

### 2. Audiences and the quest board double-book the same crisis, and the board does not listen.

Quests are posted by `day.quests`. Nothing in the engine lets an audience option resolve, cancel or improve a quest. The only chance modifier is `scouted:` (`engine.ts`, around line 789).

- **d31**: "March the Watch to the Ford" answers *"By noon the walls are quiet."* "Pay the Rustline…": *"Nobody from the tower has to go."* The quest `q-d31-iron-rain` still sits on the board. If no party goes, its `expired` text says *"Nobody rode to the Ford. The Freeholds held it alone for one night. Then they did not."* It also costs −10 Freeholds affinity and sets `ford-lost`. The player has just been told that two hundred boxcars or the whole Gate Watch went there.
- **d33**: `watch` ("Send the Gate Watch to Thistledown and the court to the Saltroad") is pure text. Thistledown can still expire into `thistledown-abandoned`, which `d39`, Act V (`freehold-barn`) and the epilogue all hold against you. `promised-thistledown` and `promised-waystation` count only as hideout pledges. Breaking the promise is never noticed.
- **d36**: `decoy` ("Sit at the front, so every sister watches you, not the cellar stair") and `teodor-goes` ("Keep the sisters' eyes on the front row") promise to help `q-d36-bell-rehearsal`. They don't.

Clarity drops to 2 because the player cannot tell which surface decides the outcome.

### 3. The tells are fair, but by Days 36–38 they are too loud for a casual player to be surprised.

Fair: all 8 of the game's `komodoLie` briefings come from "Young Komodo's (own) runner". That is a learnable rule, and Nera's forecast marks them "unreadable". The claw-tap is planted 4 times in Acts I–III. Hollin's "left-handed, taps twice" pays it off. Good.

Too loud in Act IV:
- "tap" 17 times, "ledger under his arm" 7 times.
- d36: Marrow says *"She is so very fond of you,"* and on the decline path she *"bows to Komodo. Deeper than she bowed to you."*
- d37: Tallow says *"Some sit closer to the throne than I do,"* right after Komodo lies to her face about the Abbey.
- d38 framing (no option needed): *"Young Komodo has come down from the gallery, which he never does for thieves… ledger under his arm. When he speaks, the boy looks at the floor."* Then the whisper: *"The one with the ledger. Under his arm, always."*

A casual reader who reads the text has the answer by Day 38. The only surprises left are the buyer and the motive, and the buyer is invisible (see #7).

Fix: cut the three narrated tells that need no player action (Marrow's deeper bow, the boy looking at the floor in the opening, "which he never does for thieves"). Keep the option-gated ones. Move the surprise to motive: the physician hypothetical should be the reveal, not the confirmation.

### 4. The Day 40 quiet word's central choice is forgotten, and the players who earned it don't hear it.

- **Skippable**: the top-level menu offers `leave`, `stay` and `escort` before the player sits down. One click skips the act's best writing.
- **The physician question is reachable only through `step` or `accounts → trust/roads`.** All five confrontation options (`oil`, `hand`, `boy`, `escaped`, `reports`) route `→ cornered → door`. The player who gathered the most evidence never hears *"Suppose a physician came to court…"*
- **The answer is never read.** `ask-me` ("A crown that is not asked is only a hat"), `do-it`, `no-cure` and `who` are four genuinely split philosophies, and the best choice in the act. Nothing in Act V, the betrayal page or the epilogue reads any of them. `d50-if-you-find-him` reads only `komodo-bargain-known`. The epilogue reads only `d40-komodo-offered-mercy` and `d40-komodo-called-friend`.
- **The morning line spends the request**: *"Tonight I would like to ride to the Saltroad and settle some accounts."* The evening scene then opens with the same request.
- **Misquote**: Day 8 (`actOneLate.ts:1448`) reads *"Not today. But I would ask."* The `beds` callback quotes it as *"Not today, perhaps, I said."*

### 5. A third of the alliance moves cost no enemy, and the war's actual enemy is never at the table.

12 of 52 favour-winning options cost no rival: d31 `pack`, `rustline`, `volunteers`; d33 `disown`; d34 `brass`, `wages`; d35 `saffron`; d36 `accept`, `send-komodo`, `decoy`, `teodor-goes`; d37 `oil`. Dominant options:
- **d31 `rustline`**: 20 brass, +10 Rustline, +1 Freehold strength, the Watch stays home, nobody angry. It beats `pack` (30 brass, +5) on every axis. The Pack response even says *"The Freeholds will be grateful and appalled in equal parts"*, but there is no Freehold cost.
- **d31 `volunteers`** (oath holders): +5 Freeholds, **+2** Gate Watch, free. The kind option has no cost.
- **d33 `disown`**: +5 Moles and +5 Mire Mothers. The probe ends in a win-win.
- **d34 `wages`**: 20 brass and +1 Yard, against `brass` at 60. (It quietly omits `crow-debt-paid`, a hideout pledge. That is a hidden cost the player is never told about.)
- **d35 `saffron`**: +10 Jackalwire and no Mole penalty, against `trestle` at +5 / −5.

**The Black Verge, whose plum riders are the act's war, appears in effects only twice**: the Iron Rain triumph (strength −1) and d39 `front` (−10). No scene offers a separate peace, a bribe or a hostage trade. "Open faction war" turns out to be a weather system, not a party you can deal with. Wartime choices cost money and locals far more often than they cost an ally.

### 6. Day 36 builds the best dread in the act and pays none of it.

Komodo: *"It is also the seat furthest from the door."* Teodor: *"The rehearsal is not for the bell. Don't sit at the front."* Marrow: *"There is always a seat at the front."*

None of this is read anywhere:
- `rehearsal-attended` (accept, or decoy). The Abbess holds the emperor's hand for three hours.
- `d36-teodor-at-rehearsal`. Teodor is the only follower in the game with an Abbey allegiance ("Letters to the Abbess", +3), and Marrow takes his arm *"the way you hold someone who might run."*
- `d36-komodo-at-rehearsal`. You send the traitor to the buyer for an evening. He comes back smelling of candle wax.

Each of these is a loaded gun, and none is fired.

### 7. The coalition and the buyer are decided invisibly, and Komodo's warning comes too late to act on.

- The hideout comes from `selectHideout`: Friendly-or-better affinity plus 20 per pledge flag. The buyer comes from `selectBuyer`: Old Houses local ≤ 3 hands the tower to House Vask, and 3 Verge slights plus a stronger Verge hands it to the Black Verge.
- Day 39 and 40 options move both, silently. `front` is a Verge slight. `recall` costs Old Houses −2. `crown-at-foot` costs −2. `houses` (d37) gives +3.
- Nothing in the map room shows a candidate host before Day 41 (checked `EmperorFortressMapRoom.vue`: it shows `run.hideout` only after the fall).
- Komodo's door advice, *"Whoever your friends are on the map this evening, those are your walls tomorrow. Choose the ones with roofs,"* comes after the last choice that could act on it.
- House Vask's `why` (*"Komodo had paid Lady Vask's house for two years"*) is never planted in any Act IV scene.

### 8. Quest results are thrown away.

`ford-held`, `trestle-held`, `trestle-burned`, `tunnel-held`, `tunnel-collapsed`, `waystation-defended`, `abbey-crypt-ledger`, `abbey-crypt-heard` and `rehearsal-caught` are all unread. The worst case is Day 35, which sells itself as *"One will still be there when you need a way out. One won't."* If the tunnel quest fails (*"The Moles brought the tunnel down rather than lose it"*), `route-tunnel` still counts as a Mole pledge and the court can still hide in the Mole tunnels. The triumph tally book (*"A second column: 'Paid.'"*) is the most damning evidence in the act, and no scene can produce it.

### 9. The probe → hidden truth → same menu plus a bonus shape repeats 13 times.

Every audience except d34-outer-court and d37-dark-yard opens with an "Ask…" option worth nothing that leads to a beat repeating 2–4 of the top options plus one new one. Usually the new one is the best (d32 `count-barrels`, d33 `salt-house`, d34 `ford-rights`, d35 `secret-tunnel`, d37 `read-debts`, d38 `rosters`, d39 `crown-at-foot`, d40 `own-eyes`). By Day 33 the lesson is "always probe first", so the top-level menu is noise. Clarity is fine, since probes are honestly labelled "Ask…". Uniqueness is not.

### 10. Continuity and style nits a writer can fix in an hour

- **Dots**: d37 `read-debts` says *"A small dot before every number."* Hollin's talk (`talks.ts:5030`) says *"two small dots, then the figure"*, and the d32 Hollin response says *"Taps the pen before every number"* with no "twice". Make it two dots everywhere.
- **Name clash**: two Tobins. `moles.ts` has Tobin Umber (courier, Granny's grandson, the d38 boy). Acts I and III have Tobin Lowe (Pip's missing child). Rename the courier, or name the d38 boy on screen.
- **d33 waystation success**: *"On the Saltroad, same thing."* is unclear. Cut it.
- **d34 `refuse`**: gives `strength: { 'storm-crows': 1 }` with no explanation. If the Crows arm up out of spite, say so in the response.
- **d34**: Komodo threatens the Crows' second ledger (*"Nobody gets out"*), but `crow-debt-defaulted` is unread.
- **d32 reform list and d33 sappers**: speaker lines are unquoted strings next to quoted ones in other scenes, so narration and speech blur (*"Lumen Shale. I organize for the assembly."*).
- **Kitchen images in departure lines**: Kiyo's kettle, Bram's bread, Teodor's soup and ladle, Juniper's broth. That is 4 of 20 lines (see Patterns).

---

## 3. Rewrite proposals

All audience and option ids and existing effects are kept unless a line is marked **(effect change)**. Two small engine hooks would let most of these land without content gymnastics:

- **E1. Quest result overrides by flag.** `QuestDef.expiredVariants?: { flags: string[]; tier: 'partial' | 'failure'; text: string }[]`. When an audience has already sent help, an expired quest resolves at that tier with that text instead of `expired`.
- **E2. Fall variants.** `BuyerDef.fellVariants?: { flags: string[]; text: string }[]`, using first match like `resolveBriefing`, plus an optional `precautions` list that `applyBetrayal` reads (R9).

---

### R1. d31-muster: Iron Rain (Clarity 2, Choice 2, Conseq 2)

**Problem.** The audience and the quest fight over the same Ford. Rustline dominates. The kind `volunteers` option costs nothing. Dunmark's line *"empty the walls every time a farm burns, and some day somebody burns a farm to empty them"* is the act's best tell, and it is never paid off.

**Dilemma it should become.** Walls versus farms, with Komodo as the voice for emptying the walls. Every way of helping the Ford should cost someone you have met.

**Changes.**
- **`pack`** (effect change): add `affinity: { freeholds: -3 }`. Response: *"The Pack rides out whooping. The rider watches them go, her good hand on her knife. 'They'll want paying in our fields after,' she says. 'They always do.'"*
- **`rustline`** (effect change): add `affinity: { freeholds: -3 }` and `local: { yard: -1 }`. The magpies strip the Ford farms' fences and the Yard's rails for the barricade. Response: *"By noon the Ford is walled with boxcars and every fence for a mile. The magpies charge by the boxcar. The Freeholds will spend the winter rebuilding fences around fields they kept."*
- **`volunteers`** (effect change): make it cost the walls. Change `gate-watch +2` to `gate-watch -1` and keep the flag. Response addition: *"Thirty-one step forward. That night the youngest recruit stands the east wall alone. He is fifteen."*
- **E1** for `q-d31-iron-rain`:
  - With `watch-marched` or `d31-watch-volunteers`, expired becomes partial: *"Dunmark held the near bank with the Watch and no plan. They came home in carts."*
  - With `rustline-barricades` or `pack-hired-ford`, expired becomes partial: *"The boxcars held a day. Then the riders brought rope."*
- **Payoff**: read `watch-marched` or `d31-porters-on-walls` in d40-sealed-order (R6) and the dawn (R9). Dunmark: *"First the Ford took my walls. Now the Abbey wants my nights. Somebody's counting how often I'm gone, Majesty."*

---

### R2. d33-both-roads (Clarity 2)

**Problem.** A promise made here binds nothing. The `watch` option sends the Watch to Thistledown in text but not on the board. `salt-house` costs the Freeholds nothing although Hester walks out.

**Changes.**
- **`watch`**: use E1 so `q-d33-thistledown` can't expire into `thistledown-abandoned` while this flag holds. Add `flags: ['d33-watch-to-thistledown']`. The expired text becomes partial: *"The Watch reached Thistledown at noon and lost a barn holding the rest. Hester counted heads twice."* (This reuses the quest's existing `partial` line.)
- **`salt-house`** (effect change): add `affinity: { freeholds: -5 }`. Hester's exit already earns it.
- **Broken promise**: add a scene variant to d39-congress for `promised-thistledown` + `thistledown-abandoned`. Hester, before anyone sits: *"You said it out loud, Majesty. I've a whole village heard you."* Also add a `promised-waystation` + `waystation-abandoned` variant for Oriel: *"The crown chose us, it said. Then it chose nothing."* Make the existing `thistledown` and `waystation` apology options cost one more Old Houses point under this variant.

---

### R3. d34-outer-court (Uniq 2, Choice 2, Conseq 1)

**Problem.** Feed / arm / send home is "a faction wants X: pay brass or say no." Only the Freeholds care, and all three flags go nowhere. Yet the scene runs on the same day as d34-crow-debt, which can sign the Ford's water away. That is the competing good it should use.

**Dilemma it should become.** The militia will retake the Ford, but only if the Ford is still theirs to retake. Keep `feed`, `arm` and `home`, and add:
- **New option `stay-on-gate`**: *"Quarter them in the Yard. They stand the gate beside the Watch."* Effects: `affinity: { freeholds: 5 }`, `local: { yard: -3, 'gate-watch': 1 }`, `flags: ['d34-militia-on-gate']`. Response: *"The sergeant salutes with the hand that still works. That night there are rams on the gate. Foreman Ash counts thirty-one more bowls and says nothing about it, loudly."*
- **New option `water-first`**, requires `d34-ford-water-signed`: *"Tell them the truth: the Ford's water belongs to the Crows now."* Effects: `affinity: { freeholds: -5 }`, `flags: ['d34-militia-told-water']`. Response: *"The sergeant looks at the windows. A crow sits on every sill. 'Then what are we taking back,' he says. It is not a question. They go home."*

**Payoffs.**
- `d34-militia-on-gate` feeds E2: *"The Freehold sergeant had the gate at midnight. He would not lift the bar for a seal. They lifted it over him."* It also gets one Act V line (the sergeant in the hideout, one eye, still counting).
- `d34-militia-rearmed` adds one line in d39 (Hester: *"Your spears came back to us on the Ford. Some of them still had the Watch's marks."*).
- `d34-militia-sent-home` adds Hester's chalk: the child-height scratch on the gatepost is still there in the epilogue's Freehold line.

---

### R4. d36-invitation (Choice 2, Conseq 1)

**Problem.** The act's best dread is unpaid. Accepting the front seat is free +10 Abbey affinity. `decoy`, `send-komodo` and `teodor-goes` each promise something the engine never delivers.

**Dilemma it should become.** Who sits at the front? Everyone who can draw the sisters' eyes pays in the Abbess's attention. Make each option cost what it implies:
- **`accept` / `decoy`** (`rehearsal-attended`): with E1, the quest's `failure` becomes `partial` ("The sisters were watching the front row.") when `d36-emperor-decoy` holds. Cost: read `rehearsal-attended` in Act V Day 50 or the epilogue. *"She held your hand three hours on the thirty-sixth night. She remembered the warmth. She asked for it by name."* Keep the effects. The bill comes later, and Teodor's warning is the honest notice of it.
- **`teodor-goes`**: Teodor is the one Abbey-allegiance follower. Have `departureCheck` treat `d36-teodor-at-rehearsal` as overriding `storyHeard` (romance still keeps him). Warn the player in the label or response: *"Teodor nods. 'She will ask me to stay, Majesty. Six years she asked. I don't know what I'll say this time.' At the door Sister Marrow takes his arm, gently, the way you hold someone who might run."* The cost is a follower you like. The gain: with E1, the quest's `failure` becomes `partial` (*"Teodor sang flat for three hours. Every sister turned to glare."*).
- **`send-komodo`**: read it in `betrayal.ts` as the `why` for the Abbey buyer (via E2): *"You sent him to her yourself, on the thirty-sixth night. They had three hours. It was enough to agree a price."* That makes this the cruellest delayed consequence in the game, and it is fair: Marrow's *"Oh, would you? She is so very fond of you"* is the warning.

Also cut Marrow's deeper bow to Komodo on `decline` (problem #3). The `send-komodo` path carries that tell now.

---

### R5. d37-dark-yard (Conseq 2)

**Problem.** `oil` lets brass dodge a question about honesty. Only `silence` echoes (epilogue).

**Changes.**
- **`oil`** (effect change): keep +3 Yard and change the response so the dodge shows. *"The barrels come up the road by evening. The Yard lights every lamp it owns. Ash lights the last one himself, then stands under it. 'Thank you for the oil,' he says. 'You didn't answer me.'"*
- **New option `truth-and-oil`** (cost 25): `local: { yard: 4, 'old-houses': -2 }`, `flags: ['d37-burn-admitted', 'd37-yard-oil-bought']`. This is the expensive honest road.
- **Payoff**: E2 reads `d37-burn-admitted`. On the fall page add *"The Yard's ovens were lit when the sisters came in. Ash met them at the kitchen door with a peel. He had been told the truth once. He did not believe the soup."* Also read `d37-yard-oil-bought` in one Act V Yard line: *"Ash brought one lamp out of the tower. Full."*

---

### R6. d40-sealed-order (Conseq 1)

**Problem.** Recall, stand and check-the-seals are all forgotten, and Day 43 contradicts `recall`. The Old Houses cost (−2 on `recall`) can silently flip the buyer to House Vask.

**Changes.**
- **Day 43 `d43-defector`**: add a scene `variant` for `d40-watch-recalled`. Line 3 becomes: *"You called them back, Majesty. I tore it up myself. At the second bell a second order came down under the same seal. Twenty-two went. I went after them."* Make the "twenty-two" 11 under `d40-seals-checked` (he had to forge, not reuse).
- **`stand`**: E2 fall text. *"Half the Watch was on the mission road by your order. The other half opened the gate."*
- **`own-eyes`**: E2 fall text. *"He did not need an order. He had the seal itself, and a stack of grain chits to hide it under."* Komodo's midnight stack ("a dog's name for the Yard's register") is the setup.
- **Warn the Old Houses cost.** Lady Vask's existing remark stays. Add to the `recall` response: *"'The Old Houses hold their land by that seal, Majesty,' says Lady Vask. 'One does like to know it means something.'"* That is the player's notice that Vask is near the edge.
- **Use `watch-marched`** (R1) in the opening line when set: *"First the Ford. Now the mission road."*

---

### R7. d40-archive (Conseq 2)

**Problem.** The sealed name is never read, and `morning` has no reason except being wrong.

**Changes.**
- **Give `morning` a reason**: add a Vellum line to the `name` beat. *"If I move the books tonight, Majesty, the hand will know I found it. If I wait, the copies are still on the shelf when he comes."* Then `morning` is the gamble that keeps Komodo unwarned. Read it: if `chose:d40-archive:morning` holds and `archive-evacuated` does not, Act V Day 41 Vellum says *"He came to the Archive at eleven. He asked for the forty orders by number. I gave him the wrong forty."* (one line, plus `lamplight +1`). That turns a wrong answer into a bet.
- **Pay off `sealed-name`** with a Day 41 dawn line via E2's precaution list: *"At dawn you find Vellum's slip in your sleeve. The wax is whole. You never got to read it alone. One word. You knew it."* Mechanically, `d40-vellum-sealed-name` makes the Act V hindsight ledger (`komodoLiesInHindsight`) open with Vellum's attestation, and unlocks one extra option in the d41 ledger scene.

---

### R8. d40-quiet-word (Conseq 2)

**Problem.** The best-written scene in the act has five defects: (1) it can be skipped in one click; (2) the perceptive path skips the physician; (3) the physician answer is never read; (4) `cell` is contradicted by the dawn; (5) the morning line spends the request.

**Changes (ids kept).**
1. **Remove `leave`, `stay` and `escort` from the top-level `options`.** Keep `sit` and `accounts`, and keep all three in the `door` beat, where they already exist with better responses. The scene becomes a room the player has to walk into.
2. **Route `cornered` through `question`.** Change `tomorrow`, `now` and `mercy` from `next: 'door'` to `next: 'question'`. Prepend one line to `question` under a variant on `d40-komodo-confronted`: *"'Since you are counting,' he says, 'count this.'"*
3. **Remember the answer.** Read the four `d40-komodo-told-*` / `asked-who` flags in two places:
   - **The betrayal page** (E2): a note left with the seal on the gatehouse table.
     - ask-me: *"You said to ask. I am asking now, and you are not here to answer. Forgive the hat."*
     - do-it: *"You said that is what love is for. I am holding you to it."*
     - no-cure: *"You said there is no such cure. You were right. I am selling it anyway."*
     - who: *"You asked who. Ask the Abbess what she charges."*
   - **`d50-if-you-find-him`**: one new option per answer, alongside the existing four. Example for `d40-komodo-told-ask`: label *"Tell the party to ask him first. You promised him that much."* Response: *"Dunmark writes ASK on the back of his hand. He does not like it. He keeps it."*
4. **`cell`**: add an E2 variant for `d40-komodo-held`: *"At midnight Young Komodo was in the cell the Mole boy had. At one he was at the gate with your seal. The lock had not been forced."* It pays off d38's *"The lock has not been forced"* and his question to the guard.
5. **`follow`**: read `d40-komodo-followed` on Day 41. Rook can say which road the buyer's people use, unlocking an Act V scout option or a raid warning one day early. *"He walked his horse back in the old ruts so the tracks would lie. I know which ruts now."*
6. **Morning line**: cut the second sentence of `day 40 komodo` and keep *"Whatever happens, Your Majesty, remember I always told you the price of things. Nearly always."*
7. **Fix the `beds` quote** to *"Not today. But I would ask, I said."*
8. **Door advice**: as written it can't be acted on. Either move *"Whoever your friends are on the map this evening, those are your walls tomorrow"* into Day 39's `seating` beat, where the congress can still act on it, or reword it in Day 40 as epitaph, not advice: *"Whoever your friends were on the map this morning, those are your walls tomorrow. I hope you chose the ones with roofs."*

**Does it become the best scene in the game?** With changes 1–3, I think so. It already has the best single exchange (the physician and "only a hat") and the best pair of last images (*"In forty days he always has."* and *"which cell the Mole boy had."*). What it lacks is a choice the game remembers.

---

### R9. Betrayal handoff, `betrayal.ts` (Conseq 2)

**Problem.** `fell` is fixed text that ignores every Day 31–40 precaution. The `why` lines read as rule summaries. House Vask's motive is never planted. 4 of 20 departure lines are kitchen images.

**Changes.**
- **E2 `fellVariants`.** A short precaution layer, first match wins, appended after the fixed first sentence:

  | Flag | Line |
  |---|---|
  | `d40-komodo-held` | (R8) the cell line |
  | `komodo-escorted` | *"Dunmark rode beside him to the Abbey gate. There Komodo showed the sisters your seal, and the sisters showed Dunmark a cot."* |
  | `d34-militia-on-gate` | (R3) the sergeant line |
  | `d40-watch-recalled` | *"The walls were full. He did not come over the walls."* |
  | `d35-tunnel-secret` + `route-tunnel` | *"He sent riders down the trestle road after you. You were not on it."* |

- **Make foresight pay something countable without stopping the fall.** One option: each of `d35-tunnel-secret`, `d38-rosters-changed`, `d40-watch-recalled`, `d40-seals-checked`, `d40-komodo-held` and `archive-evacuated` lowers `MAX_DEPARTURES` by 1 (floor 1), or keeps 10 brass of a treasury Komodo otherwise takes. Name the saving on the page: *"You were ready for some of it. Two fewer went with him."* Komodo is still unstoppable; the player is no longer powerless.
- **`why` lines, made stark:**
  - abbey: *"He sold to the Abbess. He always had. Nobody else was bidding."*
  - black-verge: keep, but cut "again and again": *"The crown crossed the Black Verge three times. Its riders outnumber the sisters. The Abbess let them have the walls."*
  - old-houses: plant it first. In d37 `houses`, add to the response: *"Lady Vask signs without reading it… Komodo countersigns. His sevens are very proud."* That ties it to Vellum's *"proud of their sevens"*.
- **Departure lines**: four of twenty are food on a fire or a kettle (Kiyo F003, Bram F008, Teodor F012, Juniper F020). Keep Teodor's (*"took his ladle and his grey wax. The soup is still on the fire"*), which earns its Abbey link. Change Juniper to a non-kitchen image, for example *"Juniper's bunk is stripped to the boards. She left the blanket folded for whoever comes next."* Change Bram to keep the count but lose the bread, for example *"Bram counted the court's spears before he went. He took one. Exactly one."*

---

## 4. Patterns (counts across `actFour.ts` unless noted)

**Shapes**
- **Probe → beat → the same menu plus one better option**: 13 of 15 audiences. The new option is the best one in about 8 of them.
- **Komodo interjects**: 15 of 16 audiences, 22 lines, almost always ending on an aphorism. In 5 of 10 morning lines (Days 31, 33, 34, 35, 36) he debunks the day's false briefing. On the other 4 days his own runner is the liar. That is a fair, learnable inversion.
- **"Pay brass or say no" core**: d34-crow-debt (`brass` 60), d34-outer-court (`feed` 20), d37-market (`pay` 50), d37-dark-yard (`oil` 25), d31 (`pack` 30 / `rustline` 20). 5 of 16 audiences; 3 are rescued by a third road.
- **Favour without an enemy**: 12 of 52 favour options (problem #5).
- **Scene variants**: 0 audience variants in Act IV (5 briefing variants only).
- **Unread flags**: 55 of 105. They cluster on Days 36 and 40.

**Images and phrases**
- "ledger": 95 uses (faction, local and Komodo's book). "ledger under his arm": 7. "tap/taps/tapping": 17. A tell this loud stops being a tell.
- "lamp": 41, "candle": 9, "lantern": 5. The oil thread is the act's spine and deserves the weight. But lantern and lamp images also decorate Reedlight, Vellum, Granny's "bring a lamp", the dark Yard and the quiet word.
- "Nobody …" sentences: 28 sentence-initial (41 counting lowercase). About 10 are the final cut line of a response or outcome ("Nobody came." twice, "Nobody is meant to be, yet.", "Nobody saw her touch it.", "Nobody ever does.").
- "like weather" / "the way weather waits": 4 (Reedlight ×2, Corvane, and the quiet word's bell).
- "a long time" 6, "does not look" 7, "Komodo writes something down / writes nothing down" 6, "The room gets too warm" 3, "counts every coin twice" 3, "bows lower than he has ever bowed" 3. The verbatim repeats sit in duplicated top-level and beat responses, so a single playthrough sees fewer.
- "From a sloth, that is a speech": the "From X, that is a speech" joke appears 4 times across the game (actThree, actFour, actFive and Pip's talk), plus an epilogue echo. Retire it after this one.
- "asked after the emperor's health": 2 (the quest failure and `count-barrels`). This one is a good sinister motif, so keep it.

---

## 5. What works (protect these)

1. **The quiet word's physician hypothetical** (d40, `question` beat): *"Not broken. Not stolen. Set down, gently, by someone who loved it."* and *"A crown that is not asked is only a hat."* The game's best idea, and the right place for the surprise to live.
2. **Two endings for Komodo that land like blades**: `cell`, *"At the bottom he asks the guard, kindly, which cell the Mole boy had."*, and `friend`, *"At the door he does not look back. In forty days he always has."*
3. **The rehearsal**: Marrow's *"They sing toward the floor… so the floor will learn the tune"*, and the quest triumph's *"small shoes in a row, toes to the wall… A second column: 'Paid.'"* King and Hill dread made out of ordinary things.
4. **d38's boy**: *"There is rust on his cheek."* The two taps on the chain, *"Then he sees your face, and stops."*, and the `name-in-court` brass-buttons red herring that sends Tallow to horn buttons in the epilogue. A real misdirect.
5. **d31's line**: *"Empty the walls every time a farm burns, and some day somebody burns a farm to empty them."* It is the act's thesis and Komodo's method. Wire it to the fall (R1 and R6) and it becomes the line players quote.
