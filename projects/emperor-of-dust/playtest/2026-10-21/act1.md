# Emperor of Dust: Act I playtest (Days 1–10)

Scope: every audience and beat in `utils/emperorOfDust/fortress/actOne.ts` and `actOneLate.ts`, their quests' outcome text, and the Day 1–10 briefings. That is 25 audiences (four of them conditional), 22 authored quests and 30 briefings. I read everything in scope against the rubric. I checked consequences by grepping every flag Act I sets across `fortress/*.ts` (and across `components/` and `stores/`). I also read the engine paths that decide what a player sees: `chooseAudienceOption`, the act-end map, and option notes in `EmperorFortressThrone.vue`.

Scores are 1–5: Mood · Clarity · Uniqueness · Choice · Consequence. Each audience is scored as one scene, including its beats.

---

## 1. Summary table

| Scene id | Day | Mood | Clar | Uniq | Choice | Conseq | Verdict |
|---|---:|:-:|:-:|:-:|:-:|:-:|---|
| d01-aqueduct | 1 | 4 | 4 | 4 | 4 | 5 | A strong opener. Mara offers you the blame, and the bill comes due on Day 2. If you don't probe, though, it's a free "repair" against a greedy "levy". |
| d01-toll | 1 | 5 | 4 | 4 | 4 | 5 | The best scene in Act I. The dust-lung turn reframes the raiders, and `pack-medicine` echoes all game. |
| d01-mirefen | 1 | 5 | 4 | 4 | 4 | 5 | Kiyo's "it smells of honey" is the hook of the whole act. Quiet-count is quietly dominant when you pick it. |
| d02-dust-tax | 2 | 4 | 3 | 3 | **2** | **1** | Fine characters, but a dead law. "Fair" wins on every axis, and the tax rate is never read again. |
| d02-millers-price (req. `mara-millers-levy`) | 2 | 4 | 4 | 3 | 4 | **2** | A great payoff for Day 1, but its own four outcomes vanish. |
| d02-rain-bargain | 2 | 5 | 4 | 3 | 4 | 4 | Wren. The best moral weight in the act, though the drought has no mechanical teeth. |
| d03-bell-vigil | 3 | 4 | 3 | 3 | 3 | **2** | Atmospheric, but nobody's body is on the line today and no answer is remembered. |
| d03-fen-lanterns | 3 | 5 | 3 | 3 | 4 | 3 | "He was walking in step." Superb. The head-count arithmetic is muddled. |
| d03-tincture-letter (req. `pack-medicine`) | 3 | 4 | 4 | 3 | 5 | **2** | The hardest honest choice in Act I. Almost nothing it sets is ever read. |
| d04-letter-from-bell | 4 | 4 | 3 | 4 | 4 | 4 | "It is not a coin. It is a boy." Komodo folding the page is a perfect [K] clue. |
| d04-silent-crows | 4 | 5 | 4 | 3 | 4 | 3 | Strong image work. It's a second bonded crow child in three days, with no link to Wren. |
| d04-painted-feast | 4 | 4 | 3 | 3 | 4 | 3 | The informant beat is excellent. The branching is busy, and there's a gender continuity bug. |
| d05-toll (no `feast-armed`) | 5 | 4 | 4 | **2** | 3 | 3 | The probe re-runs Day 1's dust-lung reveal almost word for word. Saffron's ferry rescues it. |
| d05-toll-grudge (req. `feast-armed`) | 5 | 5 | 3 | 4 | **2** | **1** | The loaf with the knife baked in is great. "Apologize" is free and dominant, and its text claims a payment that never happens. |
| d05-flour | 5 | 4 | 3 | **2** | **2** | **2** | The third Yard-bread-against-Old-Houses squeeze in four days. The polite ask beats every other option. |
| d06-market-charter | 6 | 3 | 3 | **2** | **2** | **2** | Tallow's third visit, the Ledger against the Yard again, rules posted on the gate again. Two answers have no downside. |
| d06-stablehand | 6 | 4 | 4 | 3 | 3 | **1** | A good small human scene. Nothing it sets is ever read. |
| d07-crow-warning | 7 | 5 | 3 | 3 | 3 | **2** | The best Komodo-lie staging in the game, but the storm it sells never arrives. |
| d07-old-houses | 7 | 3 | 3 | **2** | 3 | **2** | Its "let the oath name us" ask is never checked by the Day 10 oath. |
| d08-family | 8 | 5 | 4 | 4 | 4 | 4 | The counting cord. Protect it. "Yard" is a cheap unicorn. |
| d08-ledger-loan | 8 | 3 | 3 | **2** | **2** | **1** | Free money. "Fifty at season's end" is never collected. |
| d09-convoy | 9 | 4 | 3 | 3 | 3 | **1** | A real dilemma, the hungry hill farmers, attached to options that change nothing. "Hire the Pack instead" is a lie. |
| d09-kitchens (req. yard 12) | 9 | 4 | 4 | 3 | 3 | 3 | Juniper's gossip beat is the best "state of the court" read in Act I. |
| d10-oath | 10 | 5 | 3 | 4 | **2** | 3 | The best framing in the act, "Thistledown or the gate", wired to nothing. The oath the scene argues against pays best. |
| d10-thistledown | 10 | 5 | **2** | 4 | 3 | 3 | Three options narrate a rescue that the dawn report can contradict ("No one went. Thistledown burned."). |
| Act I quests (22) | 1–10 | 3 | 4 | 3 | – | 2 | Audience prose is stark; quest outcomes slide into cozy comedy. Most quest flags are never read. |

**Is the hook working (Days 1–3)?** Mostly yes. Day 1 is genuinely good: three petitioners with distinct faces (the polite mayor, the grinning raider, the witch with a lamp lit at noon), each with a probe that flips the read, and a Komodo aside that hands the newcomer the key to the scene. Day 2's rain bargain (Wren) is the emotional peak of the act. The hook weakens in three ways:

- By the end of Day 2 the player has learned the formula: **press "Ask…" first.** It is always listed first, it is free, it always reveals a sympathetic hidden stake, and it always unlocks better answers. That holds for 25 of 25 audiences.
- Day 2's tax scene is procedural.
- Both Day 3 mysteries (the bell, the fen lanterns) post "go and watch" quests whose results are never read.

**Is the challenge legible to a newcomer?** Partly. The throne UI (`EmperorFortressThrone.vue` `choices`) shows only "Costs N brass" and "Posts a quest". It shows nothing for brass gained, nothing for faction swings, and nothing to say that an "Ask" keeps the audience open. Day 1 also names nine factions (Hollow Bell, Jackalwire, Saltroad, Mire Mothers, Old Houses, Ledger, Yard, Freeholds, Gate Watch) before any of them is introduced. "In the gallery an Old House fan snaps shut" means nothing on Day 1.

**Is Day 10's act-end choice genuinely hard?** No. On paper it is the best-framed dilemma in Act I: the Watch's mothers are in Thistledown, the gate is held by kitchen boys, and a kind oath has already failed them once. Mechanically, none of it bites:

- Riding out has no downside. Nothing threatens the gate.
- Neither oath changes Thistledown's fate. Only staffing `q-d10-freehold-raid` does.
- The oath Dunmark says failed them ("I will never spend you cheaply") is the most rewarded choice of the act. It gives +5 Gate Watch, the F013 recruit, and unlocks later options in Acts II, IV and V. It is never punished.

The true hard choice of Days 9–10 is staffing. If you send your strongest followers on the lethal convoy (2 days, back on Day 11), they cannot defend Thistledown on Day 10. Nothing on Day 9 tells the player that.

---

## 2. Top problems (ranked)

1. **Day 10's act-end dilemma is cosmetic, and the kind oath is mechanically dominant across the whole game.**
   - In `d10-oath` › `ranks`, `ride-out` gives `gate-watch +3, freeholds +10` and costs `old-houses -2, ledger -1`. `hold-gate` gives `gate-watch +1, freeholds -5`.
   - Neither flag (`d10-oath-on-the-road`, `d10-oath-of-the-gate`) is read anywhere. Neither changes the `q-d10-freehold-raid` odds. Nothing happens to the undefended gate. The text's "half of them swear it with their teeth shut" never costs anything.
   - In `last-oath` Dunmark says: "the Watch doesn't want a kind oath. It had one." Yet `care` (+5 Gate Watch, `recruitable: F013`) is the strongest oath, and `oath-of-care` unlocks options at actTwo:2569, actFour:455 and actFive:2088.
   - The scene's thesis and its payoffs point in opposite directions.

2. **Narrated outcomes contradict the quest board.** Audience effects cannot remove a posted quest, so an option can "solve" a problem whose quest then expires with the opposite text.
   - `d10-thistledown` › `strike-camp`: "Thistledown keeps what it had left." `tincture`: "Half the raiders go with her." `rook-mercy`.
   - If `q-d10-freehold-raid` is left unstaffed, the dawn reads "No one went. Thistledown burned." and sets `thistledown-burned`. That flag is read in actTwo, actFour, talks and the epilogue.
   - `d09-convoy` › `hire-pack`: "Hire the Jackalwire to ride with the convoy **instead**." `pack-guarded-iron` is never read. If the player trusts "instead", `q-d09-iron-convoy` expires: "The convoy went without an escort. It did not arrive." That costs Saltroad −10 and strength −1.
   - `vane-debt` has the same problem ("painted wagons flank Oriel's convoy").

3. **Debts and laws that are never collected.**
   - `d08-ledger-loan` › `accept`: +40 brass, +2 Ledger. The terms ("Fifty at season's end… the Watch does not search Ledger carts") never land, because `ledger-credit` is read nowhere. The loan is free money and the dominant answer.
   - `d02-dust-tax`: Komodo says "The first law of your reign anyone can read." `tax-high`, `tax-low` and `tax-posted` are read nowhere, and `dailyTaxes` ignores them. The rate is a one-time brass bump.
   - `d03-tincture-letter` › `pay-fee`: "The price of a kindness has been set. It will rise." It never rises.

4. **The Day 7 storm never comes.**
   - The briefing says "A dust storm will cross the Eastern Ford in three days", with the harvest "a week until it is in".
   - The forecast is the price of the whole audience (errand, 25 brass, or the Freeholds' trust), but `crow-forecast-day10` is read nowhere and Day 10 has no storm.
   - `d07-freeholds-sheltered` (20 brass, the fortress opened to goats and grandparents) is also never read.
   - Komodo's first lie is told in the same scene, and the best [K] staging in the act (the claw tapping twice) gives the player no way to act on the suspicion. No quest lets you send someone down the "collapsed" galleries.

5. **Every audience runs the same template, so the act turns predictable by Day 3.** The shape is: petitioner ask → Komodo closing aside → **"Ask…" listed first, free** → hidden sympathetic stake → the same options again plus one to three better ones.
   - 25 of 25 audiences open with a probe. There are 33 `ask-*` options in all.
   - Komodo speaks 61 times across 25 audiences. He has the last line before the options in 24 openings and most beats.
   - At least eight probes reveal that the threat has a sympathetic reason: dust lung (Days 1 and 5), the burned caravan and brother (Day 3), Mara's poor wards (Day 1), the grinders (Day 2), the boy's sister at the postern (Day 6), the hungry hill farmers (Day 9), the fiddler's sincere camp (Day 4), and the pups' wire crown (Day 5).

6. **Dominant options** ("best on every axis, or nearly so"):
   - `d02-dust-tax` `fair`: +15 brass, Ledger +1, Yard +1, Lamplight +1, no negative.
   - `d05-flour` `old-houses`: free, Yard +3, Old Houses −3, F008 offered. Its gate (`old-houses ≥ 8`) is met by default because `LOCAL_START = 10`. It beats `seize` (same swing plus Ledger −1) and `buy` (20 brass).
   - `d06-market-charter` `archive-rules`: Lamplight +2, Ledger +1, Yard +1. It is gated at Lamplight 9, which is also met by default. `blankets` gives +5 brass, Ledger +2, Yard +1, Freeholds +5.
   - `d05-toll-grudge` `apologize`: free, Pack +10, clears `feast-armed`. It costs only Old Houses −2 and Gate Watch −1, against 50 brass for `pay`.
   - `d08-ledger-loan` `accept`.

7. **The Day 5 toll re-runs Day 1's twist.** `d05-toll` › `prices` ("Because the tincture doubled… Dust lung. The pups cough. The Saltroad sells the cure") is Day 1's `dust-lung` beat again ("Dust lung. Half our pups cough black… Saltroad sells the tincture at triple"). The Day 3 tincture letter sits between them. A player who probes Day 1 gets the same reveal three times in five days.

8. **Continuity bugs a reader will catch:**
   - Day 4 `informant`: the ration-card pup is "He's alive… twenty paces from him", then the option says "claim **the girl**", and the responses say "the girl at the wheel" and "make room for **her**".
   - Day 2 says "has not rained… in thirty-eight days". Day 7 says "forty days", and nothing varies it for a run that signed the rain contract ("The rain comes in four days", which is Day 6).
   - Lantern counts disagree:
     - Day 3 sergeant: "Forty-one on the road… I counted them in. I counted them out."
     - Day 7 crow: "Forty-one lanterns… Thirty-eight walkers. **Your escort counted well.**"
     - `q-d01-mirefen-inspect` success: "**More** travelers than lanterns. Some lanterns had no one under them." That is self-contradictory, and it contradicts Day 7.
     - Day 3 Komodo: "Forty walk out, and one of those is a reed-cutter… where the other two went." That is two missing, against three empty lanterns on Day 7.
   - `d05-toll-grudge` `apologize`: "Forty, then. An apology is worth ten." No brass changes hands.

9. **Kindness is bought with brass, and only brass.** About 15 options are "the crown pays so nobody suffers":
   - medicine 30, Wren's bond 30, void chits 25, refund grinders 25, Saffron's ferry 25, claim the informant 25
   - crown pays the flour 20, one price 20, shelter the Freeholds 20, seed and cart 20, feed the farmers 20, repay the granary 20
   - return the levy 15, the Coldbrooks in the Yard 15, the stablehand's sister 10

   With taxes above wages early, these become the default "good" button. The cost rarely lands on someone the player has met. The exceptions are the strongest scenes: Wren ("She may not want to come"), the Saffron ferry (the pups lose their lever), and the tincture one-price (the brother's memorial).

10. **The register breaks in quest outcomes.** The audiences are mostly King/Hill stark. The dawn report reads like a cozy sitcom:
    - "plays a terrible song for the emperor"
    - "Hollow Bell is grateful and damp."
    - "lost track around the four-hundredth goat"
    - "scattered like startled fish"
    - "Something in the reeds ambushed the ambushers."
    - "The watchers fell asleep in the pews."
    - "The Crows pretend to be impressed."
    - "ate only one goat that was not theirs"
    - "The kitchens sing all night."
    - "tightens its belts and its jaws"

    Most quest result flags are also unread: `bell-rings-alone-seen`, `bell-stair-searched`, `fen-ambush`, `fen-lanterns-hailed`, `mire-lantern-ledger`, `crow-roost-seen`, `crow-silence-explained`, `survey-seal-read`, `family-of-five-safe`, `family-of-five-scattered`, `jackalwire-escort-pact`, `stable-recovered`. The Day 3 hail quest never mentions Corran, though the player was asked to "ask for her husband by name".

---

## 3. Rewrite proposals (every scene with an axis ≤ 2)

The proposals keep audience and option ids and their existing effects. Where a fix needs an effect added to an existing option, or an engine hook, it is marked **[effect add]** or **[engine]** so a lead can sign off.

### 3.1 `d10-oath`: Oath of the Gate (Day 10; Choice 2)

**The dilemma should be:** an oath you will be held to on Day 40 (Komodo's betrayal), sworn while Thistledown burns. Each oath should buy a specific future and cost a specific present.

- **Make ride-out cost tonight.** In `ranks` › `ride-out`, the response already says "the old guard and the kitchen boys hold the gate." Make that bite:
  - **[effect add]** `brass -15, local: { yard: -2 }`, and a response line: "Near midnight someone tries the postern. The kitchen boys find a filed latch and a Ledger cart nobody searched." This also ties back to the Day 6 stable thief and the unsearched carts in `d08-ledger-loan`.
  - Better still, **[engine]** let `d10-oath-on-the-road` add +1 effective `might` band to `q-d10-freehold-raid`, so that riding out actually saves Thistledown while costing the fortress. Then hold-gate becomes a real "my walls, their village" choice.
- **Make the kind oath risky.** Keep `care`'s effects. Add a reader:
  - **[engine]** When a follower dies on a lethal quest while `oath-of-care` is held and `d10-oath-of-reasons` is not, set `oath-of-care-broken` and play a Dunmark beat at the next dawn: "You said cheaply. Tell the yard what that was."
  - The existing Act II, IV and V unlocks stay. They become the reward for keeping the oath, not for saying it.
- **Read Day 7.** Add a `variants` entry on `last-oath`, flags `['old-houses-council-seat']`, where Lady Vask's interjection becomes: "You gave us a chair, Majesty. Give our sons a name to swear to." Add a new option, `name-houses`:
  - label: “The Watch swears to the crown and the Houses that fed it.”
  - effects: `old-houses +4, gate-watch -2, yard -2`, flag `d10-oath-names-houses`
  - response: "The young ones say it. The old ones move their lips."

  That makes Day 7's ask pay off. It also gives Komodo's Day 40 buyer (`old-houses`) a seed.
- Sample lines:
  - Ranks, after the choice: "Sixty voices. Fifty-nine. One boy is looking east."
  - Hold-gate: "The smoke stands up all afternoon. Nobody on the wall says the village's name."

### 3.2 `d10-thistledown`: Smoke Over Thistledown (Day 10; Clarity 2)

**The problem** is that `strike-camp`, `tincture` and `rook-mercy` narrate a rescue, while the board quest still decides the dawn.

- **Content-only fix (no engine):** rewrite the three responses so they *shift odds in prose* without claiming the outcome, and say plainly that the posting still needs hands.
  - `strike-camp`: "The raiders turn for home before dusk. Half of them. The rider counts the rest from the hill and runs back to the board."
  - `tincture`: keep "Half the raiders go with her. Half do not." and add: "The posting stays up. Somebody still has to stand in the granary door."
- **Better [engine]:** a `quest modifiers` hook keyed on flags. With `d10-camp-struck` or `d10-tincture-called-in`, `q-d10-freehold-raid` drops its might requirement from `high` to `mid`. With `d10-rook-asked-mercy`, Rook must be in the party (`mustInclude`), and success sets a debt flag Rook's talks already read.
- **Reshape `promise`.** It is free, +5 Freeholds, and its flag `d10-thistledown-promised` is unread. Make it a vow: if `d10-thistledown-promised` is held and the quest expires or fails, the dawn adds "The rider waited by the board until dark. Nobody signed." and Freeholds −10 **[engine]**. Promising becomes a gamble, not a freebie.
- **Fix Day 9's legibility, so Day 10 is fair.** Add a Day 9 `whisper`. Source: "A Thistledown carter, watering his pony at the gate". Text: "Painted wagons on the Freehold road at dusk. Going east. Not toward the canyon." Also add one sentence to Komodo's Day 9 line: "Whoever you send tonight will not be home tomorrow." That makes the convoy-versus-Thistledown squeeze the act's legible hard choice.

### 3.3 `d09-convoy`: Iron on the Road (Day 9; Conseq 1)

**The dilemma should be:** guarding the iron means guarding it against starving farmers. Every way of disarming that fight should change the fight.

- **Clarity (content-only):** relabel `hire-pack` (both copies) to “Hire the Jackalwire to ride alongside. Ours still have to go.” Add to its response: "The posting stays on the board. The Pack is extra, not instead."
- **Consequence [engine]:** `pack-guarded-iron` gives +1 band to the quest's might requirement. `d09-farmers-fed` and `d09-wagon-left` drop the quest from `lethal` to non-lethal. One campfire goes out; one bow fewer in the dark. That is exactly what the responses imply.
- **Echo:** add a `thistledown-held` / `thistledown-burned` dawn variant line for the hill farmers when `d09-farmers-fed` is set. A hill farmer at Thistledown on Day 10: "Your grain came up the hill road under a flour-sack flag. We came down to the granary. We owed it."

### 3.4 `d08-ledger-loan`: An Offer of Credit (Day 8; Uniq 2, Choice 2, Conseq 1)

**The dilemma should be:** money now against a door in your gate that never closes.

- **Make the terms real.** Add a collection audience at season's end (Act II scope; suggest Day 18 or 20), `d1x-ledger-collects`, gated on `ledger-credit`. Tallow asks for fifty, or the stall fees, or "one cart a week through your gate, unsearched, forever". On `d08-fees-pledged`, the market's brass goes to her.
- **Make the unsearched cart pay off.** Gate a Day 10 postern beat (see 3.1) on `ledger-credit` and not `d08-fees-pledged`. Gate Watch sergeant: "First unsearched cart rolled through at dusk. It rode low. Ledger carts ride high."
- **Uniqueness.** Give this visit a different petitioner from Tallow's house: a nervous junior clerk delivering the book, with Tallow absent. Or keep Tallow but put the Watch sergeant's objection in the *opening* lines so the scene is Watch against Ledger, not Tallow again. Sample: "The sergeant stands by the green book like it's a man he's been told not to search."

### 3.5 `d02-dust-tax`: Dust Tax (Day 2; Choice 2, Conseq 1)

**The dilemma should be:** the rate decides who carries the Pack's bridge. The game already wants that (Day 5: "Somebody pays for that bridge. It was always going to be the bread.").

- **Make "fair" cost a person.** Keep `fair`'s effects. Add a new `rate`-beat option alongside it, `fair-chits-face`:
  - label: “A posted rate. And the chits paid at face, to the cooks, not the holder.”
  - requires: `{ cost: 20 }`
  - effects: `{ local: { yard: 3, ledger: -4 }, brass: 15, flags: ['tax-posted','d02-chits-to-cooks'] }`
  - response: "Tallow reads the order twice. ‘You've just taught every debtor in the wasteland to sell to me and pray.’"

  That gives the scene a costly kindness that lands on a named person, Tallow.
- **Read the rate later (content-only, via `variants`):**
  - `d05-flour` opening variant for `tax-high`. Dunmore: "You taxed the market hard. The Saltroad paid it at the gate and took it back from my flour."
  - Variant for `tax-low`. Dunmore: "Cheap market. Cheap bread. Ledger's strongbox still full of my cooks' paper."
  - `d06-market-charter` variant for `tax-posted`. Tallow: "You painted a rate on the gate. Now the blankets can read it too."
- **[engine], optional:** make `tax-high` / `tax-low` modify `dailyTaxes` by ±3. Then it is a law, not a one-time bump, and "the first law anyone can read" is true.

### 3.6 `d05-toll-grudge`: The Toll Comes Due, after an armed feast (Day 5; Choice 2, Conseq 1)

**The dilemma should be:** pride before the court against brass the Yard needs. Right now the apology is free.

- **Fix the text/mechanics mismatch.** Vane says "Forty, then", so make the apology cost forty.
  - **[effect add]** `requires: { cost: 40 }` on `apologize`.
  - Or, without changing effects, change the response to: "Vane breaks the loaf, hands you the half without the knife. ‘An apology. And fifty. The apology is so I stop telling the story.’"
- **New option alongside:** `apologize-free`.
  - label: “Apologize. Pay nothing. Let him tell the story his way.”
  - effects: `affinity: { jackalwire: 5 }, local: { 'old-houses': -3, 'gate-watch': -2 }`, flag `d05-vane-tells-it`
  - Read `d05-vane-tells-it` in Act II's Vane scene (actTwo:920): "I told it at every fire. The emperor said sorry to a hyena. The pups loved it."
- **Echo `d05-apologized-to-vane`** in Act III's Vane alliance (actThree:328) as a gated option: "Remind him the crown once apologized to him in front of the Old Houses."

### 3.7 `d05-flour`: Three Days of Flour (Day 5; Uniq 2, Choice 2, Conseq 2)

**The problem** is the third bread squeeze in four days, and the polite ask dominates.

- **Gate the polite ask for real.** Raise `old-houses` to `{ 'old-houses': 12 }` **[requirement change]**. That way it only opens for a crown that courted the Houses (seat, levy refund). It currently shows as always available.
- **Make it new: put a person in the granary.** Replace Dunmore's second `short` line with a named Old House steward and a fact:

  "And the Old Houses' granary is full. Forty sacks a cart. Lady Vask's steward sleeps on them. He has a cough. He won't sell. He says he's seen two bad winters and he's not seeing a third."

  Then `seize` takes grain from a frightened old man the player can picture, not from "the Old Houses".
- **Read the tax.** Add the `variants` from 3.5 so this scene feels like Day 2's consequence, not its rerun.
- **Uniqueness:** cut Dunmore's sack-folding beat here. He folds or unfolds his arms four times in Act I. Give him one new physical tell: he counts loaves on his fingers, and stops at three.

### 3.8 `d06-market-charter`: A Charter for the Market (Day 6; Uniq 2, Choice 2, Conseq 2)

**The dilemma should be:** the egg-sellers' freedom against the market's order. Both currently have free answers.

- **Kill the free lunch.** `archive-rules` is gated at Lamplight 9 (met at the start value of 10). Raise it to 13 **[requirement change]** so it is earned by Days 3–4 Archive choices (posting Pip's page, counts).
- **Give `blankets` a cost the player meets.** Add a line to the `stalls` beat. A Yard cousin with a stall: "I pay. My mother paid. She pays in eggs?" Make the `blankets` response end on him: "The Yard cousin packs up his own stall that evening and sets a blanket down beside theirs."
- **Echo `d06-blanket-stalls`:** read it in the Day 8 `d08-family` `yard` option response (Wenna sells eggs on a blanket by Day 12) or in Act II's market.
- **Uniqueness:** this is Tallow's third audience in six days. Let the egg-seller speak first. Opening line: "A Freehold woman with a basket of eggs stands where the factor should be. Tallow is behind her, waiting to be second for once."

### 3.9 `d06-stablehand`: The Night Stablehand (Day 6; Conseq 1)

The scene is good. It is remembered by no one.

- **Read the flags:**
  - `d06-stablehand-sister` / `d06-stablehand-pardoned`: on Day 10, the `ranks` young sentry is the boy's cousin, or the boy himself carries water to the Watch. "The stableboy runs the line with a bucket. Nobody told him to."
  - `d06-postern-informant`: the Day 10 midnight postern line (3.1) is reported *by him*. "He saw the cart. He saw who opened the postern. He's afraid to say the name in the hall." Seed the name for Act IV.
  - `d06-stablehand-stocks`: the postern stays shut, so a Day 10 riding-out costs less (no unsearched way in).
- **Choice:** `sister` closes the human problem and quietly drops the security one, since the postern has stood open a month. Add to the response: "Nobody latches the postern. It doesn't come up again until it does."

### 3.10 `d07-crow-warning`: A Crow's Warning (Day 7; Conseq 2)

**The dilemma should be:** pay a crow, carry a witch's parcel, or trust your advisor about the tunnels. The storm makes all three matter.

- **Land the storm.** Add a Day 10 briefing variant or a Day 10 dawn event **[engine]**: the storm crosses the Ford on Day 10.
  - With `crow-forecast-day10`: "The Freeholds cut by the hour the crows gave. The harvest is in." Freeholds +5.
  - Without it: "Half the Freehold harvest is in the dust." Freeholds −5, and the Day 10 Thistledown rider's opening varies: "Storm took the fields Tuesday. Raiders came for the granary Wednesday."

  This also makes Thistledown's granary the last food, which raises the act-end stakes.
- **Let the player act on Komodo's lie.** On `shelter`, add a new option `galleries-anyway`:
  - label: “Send someone down the old galleries anyway. Quietly.”
  - posts a new quest `q-d07-galleries` (1 day, guile mid, lore low hidden). Success sets `galleries-not-empty`: "Forty Mole families, and a path worn smooth."
  - Read it in Komodo's hindsight. Read it in the Day 40 betrayal as a gated "I knew you lied on Day 7" line.

  This is the biggest missed hook in Act I: the game hands an attentive player the contradiction (the whisper's "path… worn smooth" against Komodo's "Rubble and rats") and gives them nothing to do with it.
- **Echo the rain contract.** Add a `variants` entry on the opening for `crow-favor-owed`. Envoy: "The Conclave has not named its favor yet. Do not mistake this for it."
- **Fix the drought numbers:** "forty days" should be "forty-three". Add a variant for `crow-favor-owed`: "The fields are still dark from the Conclave's rain. The envoy looks at them like a man checking a receipt."

### 3.11 `d07-old-houses`: A Seat at Court (Day 7; Uniq 2, Conseq 2)

- **Echo:** 3.1 makes the Day 10 oath read `old-houses-council-seat`. Also read `d07-oath-kept-clean` on Day 10. Vask from the gallery: "You told me the Watch swears to the crown alone. Let us see you keep that one."
- **Uniqueness:** this is the third Yard/Old-Houses/Ledger table scene, and Dunmore's cameo makes it the fourth Dunmore. Replace Dunmore's interjection with a Gate Watch recruit who is an Old House son. Sample: "‘My father wants the oath to say his name, Majesty. I'd rather it said mine.’ He is maybe sixteen." This puts a body on the choice and sets up the Day 10 sentry.

### 3.12 `d02-millers-price`: The Millers' Price (Day 2, conditional; Conseq 2)

- **Read the flags on Day 3 or Day 5:**
  - `d02-flour-capped`: Day 5 Dunmore: "Hollow Bell's capped flour. They ground exactly what they ground last year. Not one sack more. That's why I'm here."
  - `d02-flour-dear`: "A third dearer since your mill order. That's the three days."
  - `d02-flour-subsidy`: Tallow on Day 6: "The crown buys its commons' bread. The Ledger underlined that."
  - `d02-grinders-refunded`: a grinder appears in the Day 3 bell scene's gallery.

  This turns Day 5's flour scene into Day 2's consequence (and fixes 3.7's repetition).

### 3.13 `d03-bell-vigil`: The Bell That Rang Alone (Day 3; Conseq 2)

**The dilemma should be:** a mayor's privacy against the town's fear, with a person's safety at stake.

- **Put a body in it.** Add one line to `chapel`: "Last time it rang through the night, a well-cleaner's boy went missing in the far wards. That was a dry month. Like this one." That sets up Pip's Tobin page the next day. The vigil becomes "find out what happened to boys like Tobin", not "watch a rope".
- **Read the results:**
  - `bell-rings-alone-seen`, `bell-stair-searched`, `d03-mara-keeps-vigil`, `d03-chapel-key`: gate Day 4 `page` options on them. "You were in her vestry. Was there a third volume on her table?" With the key: “Open the vestry before Mara wakes.”
  - The vigil quest's success outcome should name a detail Pip later confirms, for example a green thread caught on the rope.

### 3.14 `d03-tincture-letter`: A Cold Letter, Delivered Warm (Day 3, conditional; Conseq 2)

This is the best-written moral scene in scope, and it is wasted.

- **Read the flags in Day 5 `d05-toll` `prices`.** This also kills the repetition in Top problem 7:
  - `d03-tincture-one-price`: Vane: "One price at the bridge, Your Majesty. The pups drink. So I came for the toll anyway. Habit." The toll beat then becomes about something new (Saffron's ferry, Vane's age).
  - `d03-caravan-burners-named`: Vane: "Red Spoke. You named them at court. They were mine once. They are not now, because of you."
  - `d03-kiyo-brews`: Saffron, as `pay-fee` already teases: "Kiyo's kettle in the Yard. The factor sent two letters about it. Both cold."
- **Make "It will rise" true.** If `d03-tincture-fee-paid` is held, Day 5 `d05-toll` `remind` costs 10 more **[effect add]**, and the response: "The factor's fee doubled the morning after you paid it."

### 3.15 `d05-toll`: The Toll Comes Due (Day 5; Uniq 2)

- **Replace the `prices` beat when the player already heard the dust-lung reveal.** Add `variants` on `prices` for `chose:d01-toll:ask-toll`:

  “‘You know why. You asked the fiddler.’ Vane spreads his coat. ‘So ask me something new. Ask me who's buying the tincture now.’”

  Answer: the fine-coated captain from the Day 4 feast is cornering it. That turns the second visit into an escalation, not a reprint.
- Cut "Bring snacks" ×3 (also used as "Bring friends" ×2 on Day 1). Keep one.

---

## 4. Patterns (counted across actOne.ts + actOneLate.ts)

**Scene shape**
- Probe option listed first in **25 / 25** audiences, with 33 `ask-*` ids in all. It always reveals a hidden sympathetic stake, then offers the same options again plus more. The rubric's "probe → hidden truth → same options" shape is the *only* shape in Act I.
- Komodo speaks in the opening lines of **25 / 25** audiences, and his line is the last one before the options in 24 of them. The exception is `d07-old-houses`, where Vask answers him. He interjects **61** times in all.
- The "pay brass for the kind outcome" button appears about **15** times (listed in Top problem 9).
- "Post a watching or escort quest about a mystery" covers the bell, the fen lanterns twice, the crows' silence twice, and the survey flags. **None** of their result flags is read again.
- "Crown pays, Ledger writes it down": "underlines it twice" ×4, plus a dozen "writes it down" or "makes a note".

**Repeated people in Days 1–10**
- Dunmore Ash appears or speaks in 6 scenes. Marisol Tallow has 3 audiences. Mara has 2 audiences plus 3 cameos. Saffron's "rode with the Pack once" label appears twice on consecutive days.
- Bonded crow children: Wren (Day 2) and the fledgling (Day 4), with no link between them.

**Repeated images and phrases**
- "lantern", in prose: about 40. There are three lantern scenes and four lantern quests in three days.
- "posted / painted / nailed on the gate" or "beside the tax rate": 6.
- "…twice" (reads, counts, underlines): 21. "counts every sack twice" appears word for word twice.
- "Nobody …" sentence stings: 69 uses of nobody/Nobody. "Nobody went" ×4, "Nobody smiles" ×2, "Nobody profits" ×2.
- The "…worse" sting ("That is worse." ×3, "which is worse", "That is the worst part", "the worst thing she has done so far"): 6.
- "a long time / a long moment / a long look": 9.
- "like a man / like someone / like a …" similes: about 25, several explaining themselves ("like a man paying a debt he means to collect").
- Gallery reaction shots (fan snaps shut, six fans open, scribes trade a look): 17 mentions of "the gallery".
- "Bring friends" ×2 and "Bring snacks" ×3: one joke, five times.
- The dust-lung or tincture reveal: 3 tellings in 5 days.
- Arms folded or unfolded as Dunmore's tell: 5.

**The briefing lies teach nothing hard.** The false report is always the cheerful or supernatural one: a silver bell, the Moles paying, the toll "abolished out of loyalty", a peace feast, the ghost, cursed iron. On Days 1–6 and 10, Komodo names the lie in his own line. That works as [K] set-up (he earns trust before his Day 7 lie). Still, only Day 7 (his lie) and Day 8 ("raiders gone", read by Wenna's `seed`) carry any stakes.

---

## 5. What works (protect these)

1. **`d01-toll`, the dust-lung turn.** "The captain stops grinning. It is the worst thing she has done so far." A raider gets a reason with no speech, and `pack-medicine` threads through Acts I–III and the epilogue. This is the model for a Day 1 choice whose cost lands later on people the player met.
2. **`d02-rain-bargain` › `named`, Wren.** "Her name was Wren." / "Her mother still sets a place." Komodo's counterweight ("The year the rain failed, the Yard buried more than one") makes the harsh answer genuinely defensible. Thoughtful people split here. Keep the shape: one child against many, with no villain.
3. **`d08-family`, the counting cord.** "One, two, three. A knot moves along the cord for each." Wenna's "I can feed one, if I don't eat." Ordinary object, total dread, no adjectives. This is the house style working at full strength.
4. **`d07-crow-warning` › `shelter`, Komodo's claw tapping twice.** This, plus the gatehouse whisper ("the path to the old door is still worn smooth"), is the best fair-play clue in the game. A careful player can catch the advisor lying on Day 7. Give them something to do with it (3.10), and don't soften it.
5. **`d04-letter-from-bell` › `recall`.** "It is not a coin," Pip says, to the floor. "It is a boy." Komodo folds the page "along a line only he sees" and locks it in his own dispatch chest. That is a perfect betrayal seed hidden inside a kindness scene. Also protect the `d05-toll-grudge` loaf with the knife baked into the crust and the `d01-mirefen` gold flame that "smells of honey".
