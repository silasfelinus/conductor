# Slime City CLASH: plan for crafted evolutions and evolution art (230 cards + art for all 300)

**Written:** 2026-11-08 PT, after Silas's review of the first data-driven attempt:
*"We should have fresh art on the evolutions, not just frame effects. Each card should be custom created.
... doing it programmatically has a big risk of just giving stat boosts to later game cards, instead of
making substantive design changes. Do some research on good ccg design before moving forward and creating
a plan."*

**Status:** plan for Silas's approval. Governs `t-041` (230 remaining cards) and a new art track. Builds on
`CLASH-EVOLUTION-DESIGN.md` (the first 70) and `CARD-REDESIGN-300.md` (the per-card ledger and its
definition of done).

---

## 1. What the research says

**Solforge (the leveling model we copy).**
- Power is spread across a card's three levels, not stacked onto the last one. Justin Gary: *"the better a
  card is at level 1, the worse it will be at later levels."* A reviewer put it as cards that have *"a killer
  level 1 but don't progress well"* versus cards that *"start out mediocre but arrive somewhere insane."*
  ([Justin's Design Diary](https://justingarydesign.substack.com/p/justins-design-diary),
  [PHD Games review](https://www.phdgames.com/2022/03/28/playing-perusing-solforge-fusion/))
- Leveling exists *"to tell more interesting stories and give players more interesting play decisions than
  with a single static card."* The core tension is *play it now* versus *invest in its future*.
- The cautionary half: many real Solforge cards only scale a number (Grimgaunt Predator's bonus is +2, then
  +4, then +6; Ashurian Mystic +1/+2/+4) ([SolForge wiki](https://solforge.fandom.com/wiki/Card_List_Nekrium)).
  Those are the forgettable cards. Our bar is higher than Solforge's average card.
- Levels must stay recognizably the same card, and progression should be guessable once a player has seen
  the card's arc.

**Magic (Mark Rosewater).**
- *Top-down design*: start from the flavor (who this character is and what their story does), then find
  mechanics that make you feel it ([Top-Down and Goal](https://magic.wizards.com/en/news/making-magic/top-down-and-goal-2003-06-09)).
- *Lenticular design*: every card has an obvious surface use for a new player and a hidden strategic layer
  for a veteran. Complexity hides best in *timing* (when to play, when to hold), which is exactly what
  leveling creates ([Lenticular Design](https://magic.wizards.com/en/news/making-magic/lenticular-design-2014-03-31)).

**Hearthstone.**
- *Sideways design*: *"Instead of making cards better, cards are made situationally better"* (Ben Brode).
  A level-up that is strictly bigger is the least interesting option.
- Spellstones and Corrupt are earned upgrades. Spellstones are *"mini quests that level up in your hand
  ... and wouldn't force you to build around them"* (Peter Whalen,
  [GamesRadar](https://www.gamesradar.com/blizzard-talks-spellstones-epic-loot-and-christmas-gifts-in-hearthstones-kobolds-catacombs)).
  Upgrades feel great when you did something to earn them.
- Big moments: legendaries go *"a little bit more epic"*. Whalen: *"we want some of those moments that are
  super exciting"* but *"you're not going to win every time."* Design rule: *little victories*, moments
  where a player feels they turned the game ([Hearthstone 10 rules](https://80.lv/articles/hearthstone-10-rules-of-great-design)).

**Shadowverse.**
- Evolving is a scarce, timed decision (limited evolve points, once per turn), and the evolve effect is the
  moment ([Shadowverse](https://en.wikipedia.org/wiki/Shadowverse)). The worry players raise when evolving
  becomes abundant: the decision disappears. Leveling only matters if *when* you level is a choice.

## 2. What went wrong in the first data-driven pass (parked, not merged)

The Kind Robots branch `claude/pensive-albattani-ibljzj` (commits `b5a4093`, `5e7659b`) gave 230 cards
level 2/3 stages from a small effect language. It runs, and it is tested, but it fails the bar:

- **Mostly "more":** most level 2s add a rider (heal 1, deal 1, +1 power), and most level 3s are the same
  rider plus an area effect. Later is strictly better. That is the stat-boost trap in effect clothing.
- **The stat ramp is universal:** every card's attack and life roughly double from L1 to L3 regardless of its
  design. No early bloomers and no tradeoffs, which is the opposite of the Solforge principle.
- **Factions blurred:** with one shared vocabulary, Catgirls, Ironjaw and Exchange all ended up healing,
  shielding and draining in similar ways.
- **No story arcs, no new art, no named counterplay, no CPU understanding** of the new abilities.

Keep: the engine hooks (enter, hit, knockout, death, round end, turn start, spring) and the cinematic
"evolution moment" are reusable infrastructure. Drop: the authored content and the one-size stat ramp.
The branch stays unmerged until this plan is approved; then only the infrastructure is salvaged.

## 3. Design rules for every card

1. **Story first (top-down).** Each card gets a three-beat arc in one line each (who they are, what happens
   to them, what they become). Mechanics come second and must make the arc felt.
2. **Pick a trajectory, then a stat curve that matches it.** No universal ramp. Each card declares one:
   - **Early bloomer:** best at L1; L2/L3 trade raw power for utility or a new role.
   - **Late bloomer:** weak or awkward at L1; L3 transforms into something worth planning around.
   - **Role shift:** each level does a *different job* (brawler → bodyguard → field medic).
   - **Price to pay:** the level-up costs something (life, a sacrifice, a weaker body) for a bigger payoff.
   - **Earned:** L3 wants a condition met during the match (a Spellstone-style mini quest).
   - **Steady:** simple scaling, allowed only for a minority of cards, mostly cheap commons.
3. **L2 adds a decision, not a number.** A new timing, targeting or positioning choice (sideways).
4. **L3 is a moment, not a bigger L2.** A named transformation, a rules change, fresh art, the cinematic, and
   a visible counterplay. "Something cool happens no matter what" means *something different happens*.
5. **One clean sentence per level** (fits the 160-character card face). Depth lives in timing and
   combinations, never in hidden rules (lenticular).
6. **Named counterplay per card**, written down: how the opponent beats the L3 when they see it coming.
7. **Faction identity is protected.** Each faction owns its tools and borrows sparingly:

   | Faction | Owns | Never or rarely |
   |---|---|---|
   | Gene Riot Catgirls | rescue (revive, heal), ambush timing, lives that cheat death | wide area damage |
   | Punk Bloodfairies | crowd (tokens, swarm), life-steal, encores (replays) | armor, slow defense |
   | Ironjaw Chrome Ogres | solidarity (shields, armor), heavy bodies, boss breakthrough | randomness, drains |
   | Riot Saints | seeded gambles, martyrdom (death blasts), friendly fire | healing, armor |
   | Undertow Intelligence | stuns, information (draw, scout), patience payoffs, precision | big bodies, swarm |
   | Meat Exchange | boss drains, bounties, debt that compounds, buyouts | healing allies, stuns |
   | Mercenaries | one singular weird joke each, gentler numbers | copying a faction's signature |

8. **Mix targets per faction (30 cards):** at least 8 role shifts, 5 late bloomers, 5 early bloomers, 4 price
   cards, 3 earned, at most 5 steady. Reviewed per wave so no faction drifts into "everything gets bigger".
9. **Engine honesty:** card text is the rule. Bespoke code is fine when a card needs it; nothing is forced
   into a shared template.

## 4. Fresh evolution art (all 300 cards)

Today one painting serves all three levels and only the frame changes. Plan:

- **New card art for L2 and L3 of every card: 600 paintings** (the first 70 included). Each evolved painting is
  the *same character, transformed* by its story beat: the clinic cat now wears a stolen surgeon's coat,
  the Bassquake Colossus has grown a wall of speakers, and so on.
- **Method (revised 2026-11-08 PT):** Krea 2 text-to-image rounds (`EVOLUTIONS-<crew>-KREA.yaml`), one
  render per stage. The first method, Flux Kontext edits of each card's L1 ArtImage, is retired for the main
  gen. Silas, 2026-11-08: *"Flux dev is a slow generator, and we're getting a lot of the same looking images
  three times over. We shouldn't use it for the main gen, but we also need a much larger and fun escalation
  between evolution 1 and evolution 3."* Kontext preserves the source composition, so a prop swap was all
  it could deliver, at 20 Flux-dev steps × 2 seeds per stage. Identity now carries over through a per-card
  look anchor (species, adult build, signature colours, outfit, key prop) that opens both of the card's
  prompts. Each prompt is still written by hand from the card's arc (`art_ledger_authoring.py` enforces it).
- **Standing direction (Silas, 2026-11-08):** *"In general, these gens evolutions are supposed to look bigger
  and more impressive. They might tell a story."* Every evolution round follows two rules, whatever engine it uses:
  - **Bigger in the picture at every step (L1 < L2 < L3).** The hero gets physically larger in the frame and
    more powerful-looking: a growing aura, bigger gear, a costume that keeps upgrading. L2 is a low-angle hero
    shot with the character filling most of the frame and looming over rivals. L2 never uses a wide shot, an aerial view, a view from behind or an
    over-the-shoulder shot, because each of those shrinks the hero. At L3 the character is the biggest, most impressive thing in the scene.
    An epic wide view is allowed only when the character is colossal in it.
  - **One story across three paintings.** Each card carries one story thread from its L1 painting (a prop, a
    sidekick, a rival, a place) that has grown at L2 because of what the hero did, and pays off at L3.
    Both prompts name it.
- **The escalation ladder** (every step obvious at thumbnail size):
  - **L1:** the existing painting.
  - **L2, powered up:** one new signature upgrade worn or wielded, the signature thing at least twice as
    big, a bigger venue than L1, mid-story-beat with rivals or a crowd reacting, a low-angle hero shot.
  - **L3 / L3b, legendary:** an over-the-top, funny payoff pushing at least two of: scale (towering over
    rooftops), multiplication (a parade, an army), material change (molten gold, living neon, glowing
    slime), mythic form (crown, halo, wings, throne), a city-sized signature thing, the whole district
    reacting. Heroic low angle or epic wide, and a finale palette unlike L1. The gimmick varies across a
    crew. L3b goes just as big in the option-B direction.
- **Board tokens:** creatures get a new L3 token set (fierce/guard/hurt) once their L3 card art is accepted,
  roughly 110 creatures × 3 moods. These go in a later round, re-posed from the accepted L3 art.
- **Curation:** one seed per stage. Krea 2 is cheap enough to redo a miss rather than pre-buying a second
  seed. Reject anything that loses the character's identity, reads as a different creature, or doesn't
  read as a clear step up from the level below. Keep the ogres un-Shrek: chrome jaws, non-green skin.
- **Wiring:** `SLIME_CITY_ART.cards` gains per-level keys; the card face, hand, board and collection show the
  art for the card's current level.

## 5. Process per card

1. **Design sheet row** in `CARD-REDESIGN-300.md` (or per-faction sheets): arc (3 beats), trajectory, L1/L2/L3
   one-line rules, stat curve, counterplay, and the two art prompts.
2. **Silas review per batch** (a gate on subjective design acceptance, before code).
3. **Implementation:** per-card code where needed, a level-specific stat curve per trajectory, a battle
   fixture showing the payoff and the counterplay, and a CPU heuristic so the computer plays the card on
   purpose.
4. **Art round** queued from the approved arc; wired after curation.
5. **Balance sweep** per wave, and a reachability check (how often L3 actually happens).

## 6. Phasing

| Phase | Scope | Gate |
|---|---|---|
| **0. Pilot** | 10 Catgirls cards, end to end: design sheet, code, fixtures, L2+L3 Kontext art, board tokens | Silas plays it and approves the feel |
| 1 | Remaining 20 Catgirls cards + their art | design batch review |
| 2–6 | Bloodfairies, Ironjaw, Riot, Undertow, Exchange (30 each), one faction per wave | batch review per faction |
| 7 | 50 mercenaries | batch review |
| Art backfill | L2/L3 art for the first 70 hand-built cards | curation |
| Re-tune | crew balance across the finished roster | sweep report |

## 7. Questions for Silas

1. **Trade-offs:** is it OK that some cards get *weaker* at L3 in raw stats (early bloomers), as in Solforge?
2. **Choice:** should some level-ups offer a choice between two L3s, or keep every path fixed?
3. **Earned L3s:** should a few L3s require a match condition (Spellstone-style), or always unlock by
   replaying the card?
4. **Art scope:** new paintings at both L2 and L3, or L3 only for the first pass (300 instead of 600)?
5. **Pilot pick:** start with the Catgirls as proposed, or another faction?

---

## 8. Silas's answers (2026-11-08 PT) and the Catgirls pilot

*"Sure some cards can be weaker in level 3, but that should be rare for a mechanic. I like the idea of
situational level 3s. Not sure how a level 3 might require something, it sounds like a niche mechanic. Not a
bad idea for an occasional one shot gimmick though. New art for both, high priority. Catgirls pilot is fine."*

- Weaker level threes: allowed, rare (one in the pilot).
- Situational level threes: preferred (board-dependent payoffs, sideways design).
- Earned level threes: only an occasional one-shot gimmick, not a system.
- New art for both L2 and L3: high priority. Pilot round: `art/EVOLUTIONS-CATGIRLS-PILOT.yaml` (90 Kontext
  renders, two seeds per stage: L2 and L3 for all 21 pilot cards, plus each choose-one option B as `@3b`).

Follow-up, same day: *"I approved both situational and choose from two. I'm not sure what a 'ten card catgirl
pilot' is: our solo games are 20 cards and our alliance are 30. You need a sample of at least 20 from one
faction or 15 from 2 to make one side of a match."*

- **Choose one of two** at level three is approved. Three pilot cards offer it (table below). Whoever plays
  the card at L3 picks; the pick is a transcript field (`choice: 1`), so server-verified reward replays
  stay exact, and the fighter keeps its chosen stage for ongoing effects. The CPU picks by board state.
- **The pilot is a full Solo Clash side.** The Catgirls Solo/CPU deck is now 20 Catgirls, every one with
  its own L2/L3 story: the 10 hand-built twists from the first 70 (Neon Lynx, Mau-77, Clinic Calico,
  Madame Chimera, Catnip Overdrive, Scent Mine, Reknit Serum, Patent Shredders, Ninth Life Collar, Laser
  Pointer) plus 10 crafted cards. 11 fighters, 9 specials.
- **Balance.** CPU sweeps put the first 20-card list at 33.5% vs 44.5% for Catgirls on main. Two causes,
  both fixed: each fighter swapped for a special costs about 4 points (the dead 2-play Second Pounce Rig
  became a deck-builder pick, and Backstreet Organ Donor was crafted to take the slot), and the Tiger's
  weaker level one cost about 6.5 points alone (cut; its level three still hunts). Three paired seed sets
  after the fix: pilot 45.8 / 46.0 / 39.7% vs main 43.3 / 43.5 / 41.8%, parity inside the ±4 noise.

### Choose-one level threes

| Card | Option A (CPU takes it when…) | Option B |
|---|---|---|
| Splice Runner | *Midnight Ambulance*: never strikes; last fallen fighter returns as a 2/3 echo (someone has fallen) | *Black Market Run*: draw 2, and keep a fighting body |
| Gene-Spliced Tiger | *Apex Escapee*: fights the strongest foe on arrival (a foe is on the field) | *Back to the Wild*: +3 life, +2 power with no ally beside it |
| Mutual Aid Serum | *People's Pharmacy*: every unhurt ally +1 power for good (fewer than 2 allies hurt) | *Emergency Ward*: heal every ally 2 |

### Pilot design sheet (11 crafted cards)

| Card | Arc (3 beats) | Trajectory | L2 | L3 | Counterplay |
|---|---|---|---|---|---|
| Splice Runner | courier → contraband dealer → midnight ambulance | role shift | *Contraband Courier*: heal your most hurt ally 3 | *Midnight Ambulance*: never strikes; your last fallen fighter returns as a 2/3 echo | it never fights; the echo is fragile; no fallen ally = no rescue |
| Rooftop Phantom | lab-roof sneak → chimney leaps → skyline specter | late bloomer (tempo) | *Chimney Leap*: arriving in an empty alley, 2 to the rival boss | *Skyline Specter*: the leap, and a knockout sends it back to the top of your deck | blockers it cannot kill; keep the alley filled |
| Alley Veterinarian | back-alley vet → night shift for strays → passes her needle on | situational | *Stray Stitches*: round end, heal adjacent allies 1 | *Passes the Needle*: hurt allies gain REGEN; last breath heals neighbors 3 | burst the hurt allies; regen is slow |
| Parapet Ghost-Kitten | cutest nightmare → gargoyle still → nightmare shadow (still a kitten) | early bloomer, the pilot's one weaker L3 | *Gargoyle Stillness*: +2 shield each turn | *Nightmare of the Parapets*: smaller body (5/10), stuns the 3 facing foes on arrival | the stun lasts one strike; the kitten dies to anything |
| Gene-Spliced Tiger | escapee → loose in the lab → apex predator | late bloomer (plain heavy until L3; the weaker L1 was cut for balance) | *Loose in the Lab*: +1 power for good per knockout | *Apex Escapee*: on arrival it fights the strongest foe | a stronger foe wins the hunt; stunned prey cannot hit back, so stun yours first |
| Gutterglass Scout | glass-tower scout → shatters a window → the Glasswalk | role shift | *Barefoot on Shards*: hits splash 1 to adjacent foes | *The Glasswalk*: +3 shield; with 2+ allies watching, all allies +1 power now | the shield ends on her turn; no crowd, no roar |
| Mutual Aid Serum | free treatment → clinic night → people's pharmacy | situational | *Free Clinic Night*: unstun the target, +1 shield | *People's Pharmacy*: every unhurt ally +1 power for good | keep the crew chipped |
| Nine Lives, No Refunds | nine lives → the eighth is spent → the crew borrows the last | earned one-shot | *Eighth Life*: the target survives its next lethal hit at 1 | *No Refunds*: every ally survives its next lethal hit at 1 | chip twice; stun and wait |
| Catwalk Garrote | catwalk wire → the heavy drop → hangman's line | situational, then a second spring | *Heavy Drop*: +2 to a 2-play victim | *Hangman's Line*: re-arms once in the same alley | scan it; send cheap runners first |
| Second Pounce Rig | stolen rig → tuned for the pack → the second pounce | earned one-shot payoff | *Spring-Loaded*: +1 power beside an ally | *Second Pounce*: a knockout also sends its power into the rival boss | armored blockers; stun the wearer |
| Backstreet Organ Donor | a medic whose donor list is herself → every hit buys a stitch → the last donation | price (the payoff needs her to fall) | *Blood Drive*: a hit heals your most hurt ally 1 | *Last Donation*: when she falls, your most hurt ally gets +4 life and +1 power for good | stun her instead of killing her; finish the hurt ally first |

Second Pounce Rig stays crafted but leaves the starter deck (a 2-play +2 gear the CPU never chose); it is a
deck-builder pick.
