# Playtest: Act III "Kind Roads", Days 21–30

Scope: all 16 audiences and their beats in `utils/emperorOfDust/fortress/actThree.ts`, the act's 8 quests, the Day 21–30 briefings and variants, and the Act III Mole items in `moles.ts`. I also grepped every flag the act sets against the whole repo (all `fortress/*.ts`, components, pages) to see which ones anything reads later. I changed no repo file.

---

## The headline question: does the player ever doubt the Abbey's kindness?

**No.** The act's brief is that the Abbey's charity hides something and that kindness itself is the trap. As written, the Abbey reads as evil by Day 23 at the latest. From Day 25 on, every Abbey choice is "trust the obvious villain or don't". That is the unicorn-vs-puppies shape Silas asked us to kill.

### How fast doubt runs out (Abbey signals by day)

| Day | Sinister signals the player gets | Real counterweight (the Abbey's good is real, or there is an innocent reading) |
|---|---|---|
| ≤20 (carried in) | Clapperless bell. "Forty empty beds." "A door, not a room." "They knew our names. I never told anybody" (D8). "They know exactly how many orphans we have. I never told them" (D19). | "Whatever else is true, the soup is real" (Komodo, D8). |
| 22 | Drowned visitors carry Abbey tokens. Ash: "That road doesn't cross the Ford. Not anywhere." Quest: "None of them had been sent home." | Vask: "They mean the dead were poor." This comes from the act's least credible speaker. |
| 23 | Poppy syrup "enough to quiet a lot of coughs". Abbey windows lit till dawn after the seizure. "Sister Marrow knows my children's names. I never told her" (**third use** of this beat). Tam's room "where nobody's ever hungry. Or cold. Or sad. **Or anything.**" "Very well chosen." Teodor: "The children who went down were always the ones she called well chosen." Guard asks for the night wall. A honey-cake on the keep step that nobody left. | Dunmore: "The sisters' bread fed the Yard all winter." **This is the act's only credible pro-Abbey line before Day 25.** |
| 24 | Form letter with the son's name added in other ink. The hand belongs to the "register of unclaimed children". "Small footprints… None coming back." Clothes folded "for a child who won't come back". Three drawings of the same grey door. Empty cots: "They are at lessons. They were not." | Kiyo: "Maybe it means something else here." Komodo: "Efficient, not wicked." |
| 25 | The Abbess praises Komodo as "such a friend to the mission". "Send someone young. The stairs are steep. We would hate to lose anyone." A "purse that never empties" (×3). The face goes "flat" under the smile. "Wenna is with her children now." 212 names against 40 beds. Teodor's letters were spying. | She walks on foot and brings bread. Dunmore: "I can't feed what's coming." |
| 26 | Slavers take people north and come back with flour sacks **stamped with the clapperless bell**. A brick tunnel runs toward the mission road. | none |
| 27 | Marrow tried to buy the fen's child count. "What moves under the mission road… is getting louder." | none |
| 29 | Mara: the Abbey traded water for the names of children nobody would miss. | none |
| 30 | "We have counted the beds." Wagons go north "without lanterns". | Komodo: "I cannot find the flaw." In context this is a tell. |

That is roughly 30 hard signals against 4 counterweights, and two of the four come from Komodo. By Day 25 the player has also caught Komodo lying in-scene about the census. Every voice that defends the Abbey in Act III is therefore one the player has learned to distrust: Komodo (11 Abbey defenses in ten days), Lady Vask, and the Abbess herself. The only credible defender is Dunmore Ash, and he speaks twice.

### What the act should do instead (applies to every Abbey rewrite below)

1. **Ration the tells.** Allow at most one hard tell before Day 29, and let Mara's confession on Day 29 be the act's first confirmation. DAY-PLAN asks Act III for "the *first* hard evidence about missing children", not thirty pieces of it. Day 32 (*A Name in the Ledger*) and Day 36 (*Silent Bell Rehearsal*) can carry the rest.
2. **Give every clue a true innocent reading.** The Abbey really does run a fever ward, and the poppy syrup is for it. Some children really are apprenticed out, so show one who came back, healthy and loyal to the sisters. The real horror is that the Abbey does both. Kindness is the trap only if the kindness is real.
3. **Take the winks out of the Abbess's mouth.** She should be the most reasonable person in the room. Cut "send someone young… lose anyone", "purse that never empties", the flat face and "such a friend to the mission". The style guide says "Never wink."
4. **Move the Abbey's defense to credible people.** Give it to Dunmore, Kiyo (a healer who has seen the Abbey's infirmary work), Hester (Freehold orphans the Abbey took after the raids are alive and fed), and Saffron. Let Komodo sometimes argue *against* the Abbey so his defense stops working as a tell.
5. **Make anti-Abbey choices cost something on screen, and make the cost land on someone the player has met:** a named Yard child coughing again, Hollow Bell's far wards thirsty, orphans with no bed on Day 31. Then read those flags later.

The strongest moments in the act already work this way. They put the cost on the player's own kindness rather than on a villain's: Vane's pups as "guests", the tincture "loan", reading the mother the kind version of the letter, refusing the Abbey's water and having the Abbey bring water carts for free, sheltering every child and no adult. Build the Abbey line on that model.

---

## 1. Summary table

Scale is 1–5. A `↳` row scores a single beat that differs sharply from its scene.

| Scene id | Day | Mood | Clarity | Uniq | Choice | Conseq | Verdict |
|---|---|---|---|---|---|---|---|
| d21-captains-promise | 21 | 4 | 4 | 4 | 4 | 3 | Kindness-as-hostage done right. Three "alliance" options forget to set the alliance flag. |
| d21-fen-weir | 21 | 5 | 4 | 3 | 4 | 4 | The keg and the door with a shoe put a body in the room. First of three water disputes this act. |
| d22-blame | 22 | 5 | 4 | 3 | 3 | 4 | Good two-clue scene. The top level is "arrest the innocent or don't". |
| d23-smugglers | 23 | 4 | 4 | 3 | 3 | **2** | Medicine vs revenue is a real split. The poppy-syrup line winks. The licence is remembered nowhere. |
| d23-yard-sisters | 23 | 5 | 4 | **2** | **2** | **1** | Should be the act's kindness trap. Tam and Teodor confirm the horror instead, and nothing reads any of its flags. |
| ↳ d23-yard-sisters / teodor | 23 | 4 | 4 | 2 | **1** | **1** | After "the children who went down", "keep the bread coming" is puppies in lava. |
| d24-mothers-petition | 24 | 5 | 4 | 3 | 4 | **2** | Best small dilemma in the act (truth vs a kind lie). The mother then vanishes. |
| d24-coldbrook | 24 | 5 | 4 | **2** | **2** | 3 | A second parent-at-the-gate on the same day. "Trust" is pure cruelty. |
| d25-the-abbess | 25 | 3 | 3 | 4 | 3 | **2** | The writ is the best Abbey dilemma, hidden behind one of four mutually exclusive probes. The Abbess winks. |
| ↳ d25-the-abbess / offer | 25 | 4 | 4 | 5 | 4 | 3 | Dunmore against Dunmark. This is the shape to copy. |
| d26-friendly-raid | 26 | 5 | 4 | 4 | 4 | **1** | Follow vs save is excellent. The follow is never paid off, and the bell-stamped sack ends all doubt. |
| d26-mole-truce | 26 | 5 | 4 | 3 | 3 | 4 | Keel is a great voice. "Half" is a dead option. |
| d27-trial | 27 | 4 | 4 | **2** | 3 | 3 | Vask frames someone again, five days after the Ford. |
| d27-fen-count | 27 | 5 | 3 | 4 | 4 | 3 | Name-for-a-book is uncanny and genuinely splits players. "Accept the fen's help" pays nothing. |
| d28-verge-envoy | 28 | 4 | 4 | 3 | 3 | 3 | Cold grain is a great image. A second "sinister kindness" faction dilutes the Abbey. |
| d28-defector | 28 | 4 | 4 | 3 | 4 | 4 | "Returning Sable may be kinder" is a real doubt. Solid. |
| d29-mayors-secret | 29 | 5 | 4 | 4 | 5 | 3 | The act's best scene. It arrives as the seventh confirmation instead of the reveal. |
| d30-terms | 30 | 4 | 3 | 4 | 4 | **2** | The four-way triage is superb. The Abbey wagons are puppies in lava and nothing remembers them. |
| ↳ d30-terms / marrow | 30 | 4 | **2** | 4 | **2** | **1** | Accepting closes the scene without the adult shelter Marrow just offered. |

### Quests

| Quest | Mood | Clarity | Uniq | Conseq | Note |
|---|---|---|---|---|---|
| q-d22-ford-bodies | 4 | 4 | 4 | **2** | `ford-bodies-identified` is unread. Only the failure flag `moles-blamed` echoes. |
| q-d23-blue-lantern | 3 | 4 | 3 | 3 | The triumph text is generic ("glad to share rather than hang"). The route is a Rustline pledge. |
| q-d24-mission-road | 5 | 4 | 4 | 4 | Strong and read on D25 and in Act IV. But "Many. None coming back." is a hard tell on Day 24. |
| q-d24-coldbrook-visit | 5 | 4 | 3 | 3 | **Continuity error:** "Four cots". Wenna gave the Abbey three children ("nine, and six, and four"), and the epilogue says "her other three". `coldbrook-visit` is unread. |
| q-d26-dry-well | 3 | 4 | 3 | **1** | `dry-well-cleared` is unread. "This time nobody brought knives" refers to nothing. |
| q-d27-flint-evidence | 4 | 4 | 3 | **1** | `flint-cleared` and `flint-doubted` are unread. Clearing Flint is never mentioned by Flint, her talks or the epilogue. |
| q-d28-rot-cure | 5 | 4 | 4 | **1** | `verge-cure-tested` and `verge-cure-tainted` are unread. "Something to the testers' dreams" is a hook nobody pulls. |
| q-d30-hold-the-line | **2** | 4 | **2** | 3 | "The line held." Generic. Always the Freeholds, whoever the player sheltered that night. |

---

## 2. Top problems (ranked)

1. **The Abbey is not doubtable, so the act's theme fails.** See the curve above. Specific killers: Tam's "Or anything" and "very well chosen" plus Teodor's "the children who went down" (D23). Then the Abbess's "Send someone young. The stairs are steep. We would hate to lose anyone." and "a purse that never empties" (D25, ×3). Then the slavers' flour sack "stamped… a bell with no clapper" (D26). Once these land, every Abbey-friendly option (`keep-bread`, `trust`, `read-kindly`, `honor`, `pay-wenna`, `abbey-takes-children`) is the puppies-in-lava option.

2. **The act's biggest Abbey choices are remembered by nothing.** No file outside `actThree.ts` reads any of these flags:
   - `abbess-honored`, which the naive player most likely takes
   - `abbess-questioned` and `abbess-warned`
   - `d23-sisters-barred`, `d23-sisters-welcome`, `d23-tam-visited`, `d23-coldbrooks-in-keep`
   - `d24-letter-read-kindly`, `d24-form-letter-told`, `d24-coldbrooks-demanded`, `d24-wenna-paid`
   - `d25-census-clerk`, `d25-visiting-clause`, `d25-orphans-kept`, `d25-komodo-census-noted`
   - `d23-mission-syrup-seized`, `d23-manifests-copied`, `rail-route-licensed`
   - `d26-dry-well-followed`, `dry-well-cleared`
   - `d29-bell-refuses-water`, `d29-mara-confession`, `d29-page-sealed`, `d29-runner-question`
   - **`d30-children-to-abbey`**: the player sends every child of three peoples to the Abbey ten days before the horror wakes under it, and the game never mentions it again.

   Two of these promise a payoff in their own text and never deliver. Tam "wasn't allowed downstairs yet. 'Next time.'" The Watch rides out under "do not interfere, whatever they see."

3. **The pro-Abbey voice is the known liar.** Komodo defends the Abbey 11 times in ten days: "Let the dead keep them", "I would not read a ghost story into a grocery list", "Children embroider", "Read her the kind parts", "Efficient, not wicked", "I would not frighten her over laundry", "We need friends who feed people", "Do not shame him", "Leave the bricks to the rats", "Burn the page", "I cannot find the flaw". On D25 the Abbess exposes his census lie in-scene. That telegraphs both the Abbey and the Day 40 betrayal, and it stops any player from treating his arguments as arguments.

4. **The "alliance" options don't create an alliance (mechanical bug).** In `d21-captains-promise`, these options say the Pack allies or "agrees to everything" but omit the `pack-alliance` / `pack-truce` flag and the strength bump:
   - `pups-as-guests` ("Take the pups as guests of the crown, **and the alliance**")
   - `tincture-debt` ("He agrees to everything")
   - `camp-threat` ("He will stand with the tower")
   - Saffron's `pups-back` ("Swear the alliance")

   `engine.ts` PLEDGES (jackalwire), which decides the Act V hideout, and `epilogue.ts:342` both read only `pack-alliance` / `pack-truce`. The player picks the most interesting alliance and the game records no alliance.

5. **Day 30, `abbey-takes-children` contradicts the offer.** Marrow says "Shelter whichever grown folk you like", but accepting ends the audience with no `sheltered-*` flag and no strength. The Abbey option is therefore also the mechanically worst one, so the text and the mechanics both push away from it. That leaves nothing to tempt the player.

6. **Every audience re-offers its top-level answers inside its beats.** This happens in all 16/16 audiences: 65 of 189 options (34%) are re-offers with identical effects. `honor` appears 5 times in `d25-the-abbess`. Probing is always free, so the dominant strategy is "always probe, then pick". The rubric's "probe → hidden truth → same three options" shape is the act's default.

7. **Probes are silently mutually exclusive.** This matters most where it hides the best content:
   - In `d25-the-abbess`, `ask-census`, `ask-wants` and `teodor` each lead to their own beat, and none returns. The orphan writ, the act's best Abbey dilemma, is reachable only through `ask-wants`.
   - `d22-blame` knife vs tokens: taking the knife beat locks out Ash's token reading, which seeds Act IV (`d22-token-stamp-copied`).
   - `d29-mayors-secret` price vs envelope.

   The UI (`EmperorFortressThrone.vue`) notes cost and posted quests but says nothing about a probe closing the others.

8. **A follower-option convention trap on Day 29.** Every "Let <follower> …" option in the act is a free probe (`ask-saffron`, `ask-ash`, `ask-teodor`, `ask-pip` on D24, `ask-kiyo`, `teodor`). The one exception is `d29` `pip`, "Let Pip read the page aloud.", which is **terminal**: abbey −10, hollow-bell −5, it sets `bell-abbey-ledger` and closes the audience. A player who learned the convention loses Mara's price beat, the act's best beat.

9. **Same shapes back to back.**
   - Day 24 runs two parent-at-the-Abbey-gate audiences in a row (the mother, then Wenna). Both have the same option skeleton: send someone, write to the Abbess, trust the Abbey.
   - Lady Vask frames someone on D22 (Moles) and again on D27 (Flint).
   - "The Abbess/Abbey writes back warmly, by return" appears 4 times (D22 `write-abbey`, D24 `ask-abbey` ×2, D24 `demand-return`).
   - "She does not come to court again" / "stopped coming to court" appears 3 times.

10. **Briefings are solved for the player.** On 7 of the 8 days that are not Komodo lies, Komodo's comment openly debunks the false item:
    - "Ghosts do not lower the price of medicine"
    - "Vane will die old in bed"
    - "Flint would be boiled before she confessed"
    - "Some carry a condition… Not all"
    - "No one has signed anything"

    On his two lie days (D25 census, D29 forgery) he *endorses* a report. The only days he backs a briefing are the days he is lying, which is a structural tell. The false items are also cartoonish ("a ghost with no feet", "Everyone… is a vampire", "a hopeful herald"). There are only 7 variants across 10 days, and none reacts to an Act III Abbey choice.

---

## 3. Rewrite proposals (every scene with an axis ≤ 2)

Each proposal keeps existing audience and option ids and existing effects unless it says otherwise. New options and flags are additions.

### R1. `d23-yard-sisters` (Uniq 2, Choice 2, Conseq 1): make the bread real and the room ambiguous

**Dilemma it should be:** the sisters' bread keeps the Yard alive, and Sister Marrow has personally saved one of Wenna's children. Tam wants to go. Barring the sisters costs named people food, and letting them stay costs uncertainty. Thoughtful players should split.

- **Opening.** Replace "Sister Marrow knows my children's names. I never told her." (the third use of that beat) with a debt:
  > "When the baby took the fever, Sister Marrow sat up with her. All night. I slept. First time since the farm."
  > "Now Tam wants to see their lessons. The Yard thinks I'm ungrateful for asking you. Maybe I am."
- **Tam beat.** Cut "Or anything" and "very well chosen". Make the room plausibly a sickroom:
  > "There's a room at the bottom where the sick ones sleep. Nobody coughs down there. They said I could carry soup down. They said I have steady hands."
  > Wenna: "Steady hands. He spills everything, Majesty."

  This is still unsettling, and it has an innocent reading.
- **Teodor beat.** Keep the key on the counting cord, but give the innocent reading a real voice:
  > "Six years, never below the third floor. Marrow kept that key. I asked once. She said 'fever ward', and that I had a family to think of. I did. There was fever that year. I buried two of ours myself."
- **Costs on screen.** `bar-sisters` already has yard −2. Add a named cost by reading `d23-sisters-barred` in a D24 or D25 briefing variant: *"The Yard's cough is back. Two children in Kiyo's infirmary. The cooks say the bread stopped."*
- **New option alongside:** `bread-at-gate`, "Take the bread. Keep the sisters outside the Yard gate."
  - Effects: `affinity: { abbey: -3 }`, `local: { yard: -1 }`, `flags: ['d23-bread-at-gate']`
  - Response: "The baskets come to the gate. The sisters wait outside, smiling, until the last one is empty. Tam watches them through the bars every night."
- **Pay off later:**
  - `d23-tam-visited` → Day 30 `marrow` beat line variant: Marrow calls Tam by name and asks whether he wants to ride on the first wagon.
  - `d23-sisters-welcome` and `d23-sisters-barred` → epilogue lines.
  - The Yard-branch epilogue already has "Tam… will not eat honey-cake". Gate it on `d23-tam-visited` so it means something.

### R2. `d24-coldbrook` (Uniq 2, Choice 2): flip Wenna from accuser to defender

**Dilemma it should be:** the mother's petition on the same day already covers "a parent wants in". Make Wenna want the crown to **stay out**. She believes, or has been told, that the children are punished when parents make trouble. Respecting her plea and protecting her children now pull against each other.

- **Opening:**
  > "That woman from the Freeholds. Shouting at the gate. Make her stop, Majesty."
  > "Sister Marrow says the little ones cry for a week when a mother shouts. I've been quiet four times. I'll be quiet forty."
  > "They gave me this last time. For being good."
- `trust` ("The Abbey has its rules. Be patient.") now honours a mother's explicit wish. It is no longer pure cruelty. Keep its effects.
- `go-with-her` now overrides her. Add to the response: "Wenna begs you not to. You send them anyway. She walks behind the party, ten steps back, the whole way."
- Keep the bundle beat and Kiyo's line. They are the scene's best material.
- **New option alongside in `bundle`:** `quiet-watch`, "Do as she asks. Post one Watch rider on the mission road, out of sight of the gate."
  - Effects: `local: { 'gate-watch': -1 }`, `flags: ['d24-quiet-watch']`
  - Read it in Act IV (D36) as a variant: the rider saw which nights the side gate opened.

### R3. `d24-mothers-petition` (Conseq 2): name her and follow her

- Give her a name and a body in the opening, for example "Bett Ormond, a Freehold mother". Hester's D30 line "A mother on my roads…" should then be gated on whether the player met her and what they told her.
- `d24-form-letter-told` → D26 briefing variant (Freehold reeves): *"Bett Ormond sleeps at the mission-road well now. The sisters bring her soup. She takes it."*
- `d24-letter-read-kindly` → epilogue line, the kindness that became the trap:
  > "Bett Ormond still gets a letter on the first of every month, in a fine hand. Dov is well, and very busy. She keeps them in a tin. She can't read them. She doesn't need to."
- `asked-abbey-politely` → D25: the Abbess opens by thanking the crown for "your courteous letter about the Ormond boy". It is warm, and it tells the player the Abbey reads the crown's mail closely.

### R4. `d25-the-abbess` (Mood 3, Clarity 3, Conseq 2): make the Abbess the most reasonable person in the room

- **Cut the winks:**
  - "Send someone young. The stairs are steep. We would hate to lose anyone." → "Send whoever you like. Come yourself. Mind the third stair, it's loose. I keep meaning to have it seen to."
  - "from a purse that never empties" (×3) → "She pays from a plain purse, counts it twice, and asks for a receipt."
  - Opening "What a fine young advisor. Young Komodo has been such a friend to the mission." → cut. Keep only the census-beat admission that he copied pages. One quiet tell is enough.
- **`cots` option.** Replace the flat face with an answer that is partly true and costs her something:
  > The Abbess does not smile. "Two were in the fever ward. One ran. We found her at the Ford on the third day. I wrote to no one. I should have. I was ashamed."

  Keep its effects. The player now has to weigh a confession against a cover story.
- **`tax` is dominant** (+30 brass, and abbey −15 reads as a bonus). Give it a real cost: `local: { yard: -2 }` with the response "She pays. 'The bread was always our tithe, Your Majesty. Now it is brass.' The baskets stop coming up the hill."
- **Clarity of the exclusive probes.** Either let `census` and `teodor` end with a `next: 'offer'` option ("Ask what she walked here for"), or move the writ request into her opening lines so every player gets the act's best Abbey dilemma.
- **Pay off later:**
  - `abbess-honored` → D30 Marrow variant ("The Abbess remembers how you honoured her") and the betrayal buyer weighting.
  - `abbess-questioned` → D30 Marrow: "The Abbess asked me to say she has not forgotten your questions. She is glad of them."
  - `d25-census-clerk` → D32 *A Name in the Ledger* variant: "Your clerk counted 212 names and 40 beds. She says they showed her every floor but one: the fever ward, where she could not go without a mask they did not have."
  - `d25-komodo-census-noted` → `komodoLiesInHindsight` extra line after the betrayal.
  - `d25-visiting-clause` → Act IV: a visit at an odd hour finds the children asleep, fed and well, which deepens the doubt.

### R5. `d23-smugglers` (Conseq 2)

- **Cut the wink:** "Enough to quiet a lot of coughs" → "Twelve jars, every third night. The Ledger doesn't care who drinks it."
- Add an innocent reading from a credible voice. If Kiyo is in the roster, she says: "Twelve jars is what a fever ward of forty burns through in three nights. I would know."
- **Pay off later:**
  - `rail-route-licensed` → D31 or D33 briefing variant (Freehold reeves): *"Medicine costs a fifth more on the farms since the licence. Two farms stopped buying."*
  - `d23-mission-syrup-seized` → D25 Abbess line, ambiguous and costly: "Our fever ward cried for three nights, Your Majesty. Your Watch has the jars. I don't blame you. Someone told you something." Keep the existing "windows lit until dawn" response. It now reads either as children in pain or as a signal.
  - `d23-manifests-copied` → D32: the Archive's copies show the Mission's jars doubled the week the Coldbrooks arrived.

### R6. `d26-friendly-raid` (Conseq 1): pay off the cruel choice and take the stamp off the sack

- **Remove the clapperless bell from the sack** in the opening `where` beat. Make it "Good white flour. Nobody in the canyon's seen that in years. The Abbey mills white. So does Hollow Bell. So does the Ledger." That gives three suspects and keeps the doubt.
- `d26-dry-well-followed` → D28 briefing variant (the Watch): *"The Watch followed the dry-well jackals north for three days. Eleven Freehold people, roped. Handed to unmarked wagons at a crossroads below the mission road. The Watch did not interfere. Orders."* That puts the stamp back as earned evidence, a day later and at a price. Also read it in a D30 Dunmark line: "My riders watched eleven people go by on a rope, Majesty. On your word. Don't ask them to do it twice."
- `dry-well-cleared` → D31 briefing: farms stop emptying, and the Pack is cocky. Pay off "nobody brought knives" with an actual feast scene line, or cut that line.

### R7. `d27-trial` (Uniq 2): change the accuser

Vask framing someone again five days after the Ford flattens both scenes. Make the co-accuser someone the player likes, so the trial becomes kindness against fairness inside the crown.

- **Opening:** Dunmore Ash stands beside Lady Vask.
  > Dunmore: "Forty days of ration went down a Mole hole, Majesty. My cooks' children ate soup water that month. I'm not with the Houses. I'm with the soup."
- `censure` now has a real reason (fairness to the Yard), not only "keep the Old Houses quiet". Keep its effects and add `local: { yard: 1 }`.
- `pardon-public` now costs Dunmore. Add `local: { yard: -1 }` with Dunmore's line "Then the crown honours what it took from my kitchen."
- Keep the `levy` beat as Vask's. That is where the politics belongs.
- Pay off `flint-cleared` / `flint-doubted` in Flint's barracks talk and epilogue line.

### R8. `d30-terms` / `marrow` (Clarity 2, Choice 2, Conseq 1–2)

- **Fix the mechanics:** `abbey-takes-children` should end with `next: 'losses'` so the player still shelters adults, as Marrow offered. Keep its effects. The Abbey option then genuinely solves the triage: it is the same kindness as `children-first` with no cost to the Yard. That is the trap, and it only bites if the Abbey is still doubtable on Day 30 (see the plan above).
- **Credible voices on both sides:**
  - Hester stays against.
  - Add Dunmore for: "Three to a bed and no milk, Majesty. Or hot milk on a wagon. I know what I'd want for mine."
  - Change Komodo's "I cannot find the flaw" to something useful or silent. It is a tell.
- **Pay off later:**
  - `d30-children-to-abbey` → Act IV:
    - D33 briefing: "The Abbey sent back forty children to the Freehold farms, fed, in new shoes. The rest are 'still at lessons.'" This is partial return, so the doubt survives.
    - D40 betrayal line.
    - Epilogue branch: which children came home.
  - `d30-children-sheltered` → D31 Yard crowding briefing, plus an epilogue line about the night parents kissed their children at the gate.

### R9. Quests with Conseq 1 (`q-d26-dry-well`, `q-d27-flint-evidence`, `q-d28-rot-cure`) and `q-d30-hold-the-line` (Mood 2, Uniq 2)

- `verge-cure-tainted` → a D29 briefing: "Two of the testers sleepwalked to the north gate last night. Both stood facing the Verge until dawn." `verge-cure-tested` → an epilogue line about the cold bread.
- `q-d30-hold-the-line`:
  - Bind the defended faction to whoever the player sheltered (`sheltered-*`), or post a variant per faction.
  - Give the outcomes a body. Instead of "The line held.", for example: "The line held at the Freehold fence posts. Dunmark brought back every rider. One horse. They ate it."

### R10. `d21-captains-promise` bug fix (not axis-driven, but it corrupts Conseq)

Add `pack-alliance` (and `strength: { jackalwire: 1 }` where the text says alliance) to `pups-as-guests`, `tincture-debt`, `camp-threat` and Saffron's `pups-back`. Otherwise these alliances don't count toward the hideout PLEDGES or the epilogue Pack line.

---

## 4. Patterns (counts across `actThree.ts`)

**Option structure**
- 16/16 audiences re-offer top-level options inside beats: 65 of 189 options (34%) are identical re-offers. `honor` ×5 in one scene.
- "Probe → hidden truth → same options plus one or two new ones" is the shape of every audience. No probe costs anything. Several probes silently lock out others: D21, D22, D25, D29.

**Komodo**
- He speaks in every one of the 16 audiences: 30 interjections, plus 10 briefing comments.
- 11 of those are Abbey defenses. 7 of the 8 non-lie briefings get debunked by him. He endorses only his own two lies.

**Recurring beats**
- "Knows names I never told them": 3 times across acts (D8, D19, D23).
- "Abbey writes back warmly, same day / by return": ×4.
- "does not come to court again / stopped coming to court": ×3. "leaves without a word": ×9.
- Two "parent can't see child at the Abbey" audiences on Day 24.
- Vask frames someone: ×2 (D22, D27).
- Water as the currency of a dispute: ×3 (D21 weir, D26 water rights and cistern, D29 Abbey well). Tolls and licences: D21 bridge toll, D23 rail route.
- "Sinister kindness" factions: ×2. The Black Verge offers doctors for pups (D21), warmth-charms (D28) and "returning Sable would be a kindness" (D28). Its shape copies the Abbey's and blurs it.

**Phrases and images**
- `ledger` ×48, `lantern` ×29, `kind`/`kindness` ×28, `warm` ×19, `smile` ×15, `grey` ×12, `gloves` ×10.
- "Nobody …" sentences: 42 uses of "Nobody", including closers like "Nobody asks.", "Nobody writes that down.", "Nobody does the sum aloud.", "Nobody picks up the shoe." (×2).
- Repeated exact lines:
  - "bows lower than he bows to you" ×5
  - "How judicious" ×4
  - "Does not blink" / "without blinking" / "unblinking" ×4
  - "spits in his palm" ×3
  - "feel the same about crowns" ×3
  - "finger by finger" ×3
  - "purse that never empties" ×3
  - "It sounds like a threat." ×3
  - "I know how those work" ×3
  - "choose another mayor… They should." ×3
  - "'Good,' says Flint" ×3
  - "taps the cover of his ledger twice. Then it is still." ×2
- Honey-cake ×6 in two scenes.

**Style-guide breaches ("never wink", "no lines that explain their own meaning")**
- "It sounds like a threat." (×3)
- "All evening he is kind to you. You will remember that later."
- "Comfort or confession. Nobody asks."
- "It is what she does instead of crying."
- "Not a good thing to see on that face."
- The Abbess's "lose anyone" line.

---

## 5. What works (protect these)

1. **D21, Vane's price beat.** "That is a hostage, Your Majesty, offered as a kindness. Or a kindness offered as a hostage. I cannot tell which. Neither can he." Then the six pups walking into the Yard nose to tail, and `tincture-debt`'s "So it was a loan. I thought it was the other thing." This is the act's thesis, done with real doubt.
2. **D29, Mara's price beat.** "Tell me which of those children you'd have traded for the far wards, Majesty. I'll tell you mine." Then `refuse-water`: "By week's end Abbey sisters are at the Bell's gate with water carts. Free. Asking nothing." This is the only place where the Abbey's kindness is the trap, and it is excellent.
3. **D24, the form letter.** "She holds out a folded letter in both hands, the way people carry what they can't read." The name is added in other ink. `tell-her` vs `read-kindly` is a true split between truth and mercy. Keep it, and give it consequences (R3).
4. **D30, the losses beat.** Four envoys, four honest losses. Hester won't sleep beside the Moles. `children-first`: "They kiss them at the gate and walk away alone. … Nobody sleeps." This is real triage with costs on people the player has met.
5. **D26, Vane's "where" beat, and the D21 weir opening.** "A goat you sell back. A person you ransom. These do neither." `follow`: "And they call us the raiders." The keg: "'Empty,' he says, before the Watch can draw." The door carried in with wet bedding, a kettle and a child's shoe. This is stark register at its best.

Also worth keeping: the D22 root-knife ("a Mole's root-knife lives in soil like a spoon lives in soup"), Keel's "Surveyors know when a wall is wrong", and the D28 frosted grain that stays cold even from the oven.
