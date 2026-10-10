# Book One: The Bell That Never Rang — narrative outline

Silas, 2026-10-10: *"keep expanding the gamebook ... We want a full and immersive experience, with branching
choices, interesting moral dilemmas, etc. This is something that should be outlined first to allow a rich
narrative experience. then we'll build out the sections. The world of Zuzu is vast, it's rife with moral
dilemmas, cosmic horrors, magic, people in desperation, and rare glimpses of honor and beauty. this is a dark
horror world, but he has the choice to rise above it."*

This is the build plan for Book One. Authority order: [worlds/zuzu](../../worlds/zuzu/README.md) (canon,
WORLD-GUIDE and its gazetteer), Book One (the comic's chronology), then this outline. The gamebook is an
**alternate trail**: it may diverge from the comic's events, never from its world. Names marked
*(provisional)* are agent-proposed and become shared canon only through Book One or the registry.

Implementation: kind_robots `utils/zuzuGamebook/` (engine `adventure.ts`, types `types.ts`, content `book.ts`
plus one file per act under `acts/`). Section ids already shipped never change (saves reference them).

---

## 1. What the book is about

**The question every section asks:** in a world where kindness is bait, hunger is law and something vast is
pressing through the thin places, *what does a man of honor owe to strangers?* Zuzu can survive this book by
becoming what the world is. The book is about whether he chooses to rise above it, and what that costs.

- **Dark, not nihilistic.** Horror is the weather; honor and beauty are rare, earned and real. Every act holds
  at least one moment of beauty that is not a trick: an apple tree, a song for the dead, a bloom after rain,
  a child's first laugh, a bell that finally rings.
- **Choices with weight, not good/evil buttons.** Each dilemma sets two goods or two harms against each other
  (the children's water vs a dying stranger's; honesty vs a girl's safety; a quick victory vs innocents in the
  fire). There is rarely a free option, and the cost lands later, visibly.
- **Desperation explains, never excuses.** Raiders, sellers of false hope, a town that sold its children for
  water: the book shows *why*, and still lets Zuzu judge.
- **Cosmic horror is felt, not explained.** The thing behind the wall is never fully seen. It speaks in
  dreams, offers what Zuzu most wants (the way home), and its gifts are real. Taking them is the temptation.
- **Magic is costly and ambiguous.** Storm Crow witchcraft (WORLD-GUIDE: "costly, ambiguous") helps at a price
  that is always paid in something that matters.
- **Species is not destiny** (WORLD-GUIDE). The kind barkeep is a hard-eyed rabbit; the predator in the habit
  is a round-faced otter; the raider chief is a starving mother.
- **Children:** endangered, hungry, frightened and brave, never sensationalised; harm is the stakes, implied
  and aftermath-only.

## 2. The moral system

Zuzu's code (WORLD-GUIDE: duty and feeling, respect for the dead, debts repaid, the blade drawn only to be
used, silence, an outsider's eye) is a *source of choices*. Two tallies record what he does with it. Neither
is shown as a score to the player; both are felt in the prose, the journal and the endings.

| Tally | Grows when Zuzu... | Opens | Closes |
|---|---|---|---|
| **Honor** | keeps his word, honours the dead, repays debts, spares the defenceless, tells hard truths, gives what he cannot spare | allies who trust him (the coyote, the novice, the barkeep, the raider mother), the best ending (*The Bell Rings*), the sister's full trust | nothing: honor is never punished by the rules, only by the world (it costs supplies, time and blood) |
| **Taint** | listens to the whispering stone, takes the thing's gifts, makes a dark bargain, kills the helpless, uses the thin-place road | power: healing, Resolve, sight, shortcuts; the dark endings (*The Hollow Saint*, *The Bargain*) | the sister's trust at high taint; *The Bell Rings* (needs low taint) |

Mechanics (engine): a flag named `honor:<deed>` adds one Honor and `taint:<deed>` one Taint. A deed counts
once. Choices may need `needsHonor: n` or `needsTaint: n` (shown disabled with a hint, never hidden). Lasting
character change is an attribute shift of at most one step, between -2 and +4 (`effects.attr`): Mercy grows
through repeated kindness, Steel through hard fights, Shadow through deceit, Sense through attention.

**Debts** are named flags (`debt:coyote`, `debt:raider-mother`, `debt:looter`): a creature Zuzu spared or
helped who can repay him later, for better or worse.

## 3. Cast and arcs

| Character | Species | Role and arc | First / last appearance |
|---|---|---|---|
| **Zuzu** | koala | Ronin from a land nobody here knows. Arc: from refusing the children to leading a pack, or to the road alone, or to something worse. | I / IX |
| **The coyote** | coyote | Destitute one-eyed vagrant; loses his right (gun) hand to the croc. A bounty hangs on him in Dustwater. Debt or grudge. Can return as an ally (*One Fire*). | I / VII–IX |
| **The sister** | fennec, ~10 | Gaunt, fierce, taller than Zuzu, bandaged wrists. Trust is earned in small steps; she can steal, flee, or stay. Her dagger moment (SF3) is canon's mirror. | II / IX |
| **The toddler** | fennec | Babbles only. Falls ill on the road; eats as if food might be taken back; laughs once if the book allows it. | II / IX |
| **The Abbess** | otter | Elderly head of the mission; patient, warm, perfect manners; feeds children to the thing and means to bring it fully through. Never wins by force alone; she wins by making leaving feel kind. | V / VIII |
| **Sister Wren** *(provisional, gamebook-only)* | otter, novice | Young novice who suspects the truth and is afraid. Can be protected, betrayed or recruited. | V / IX |
| **Mags** *(provisional)* | rabbit | Dustwater barkeep, scattergun, lost her son to the mission road. Truth for kindness; grief that can become a mob. | VI / IX |
| **The raider mother** *(provisional: "Hollis")* | jackal | Leader of a starving raider band at the dry well; her kits are hidden in the rocks. Fight, bargain, or share. | IV / VII |
| **The looter** | raccoon, young | Stripping the dead in Hollow Bell. Spared, he becomes a raider scout who can warn or betray. | II / IV |
| **Brother Peddler** *(provisional)* | hare | Sells "blessed water" to desperate families. Con man or the last kindness left? Both. | IV |
| **The Storm Crow witch** *(provisional: "Old Ash")* | crow | A witch far from her cave, perched on a dead tree at a crossroads. Offers sight for a price. | IV (VII) |
| **Gideon Vane** *(provisional)* | pronghorn | Dustwater's water baron, who trades orphans to the mission for water rights. Desperation turned to business. | VI |
| **The bounty hunter** | badger | Hunting the coyote. Honest about it. | VI |
| **The thing** | — | Coiled, vast, patient, behind the wall in the crypt; speaks in dreams; never fully seen; offers the way home. | IV (whisper) / VIII–IX |

## 4. Threads that run through the book

- **The bell.** Hollow Bell's tower; the mission's bell with no clapper (the Abbess cut it out so no alarm can
  ring); the toll heard with no ringer. Payoff: Zuzu can forge or find a clapper (the croc's tooth? a relic
  iron? the coyote's gun barrel) and **ring the bell** in the best ending: the bell that never rang, rings.
- **The thin places.** The world wears thin near the mission. Roads shift at night (VII); the stone face in
  the waste whispers (IV); the crypt wall is "deep the way water is deep" (V). Never explains the lost humans.
- **The lost humans.** Relics only: a straight stone road under sand, script nobody reads, bones of a shape
  nobody names, a cracked stone face. Kept unexplained (WORLD-GUIDE). The thing may *claim* to know what
  happened; it lies, or it doesn't. The book never says.
- **Hunger and water.** Water is the currency of every dilemma: who drinks, who is sold for it, what it buys.
- **Three on the road.** The book's motion: alone, followed, a pack (Book One SF2).

## 5. Structure: nine acts

Budgets total about 400 numbered sections (Fighting Fantasy scale) including endings. "Shipped" counts the
68 live sections as of 2026-10-10. Each act lists its **entry** and **exits** so acts can be authored
independently; ids in `code` already exist.

| Act | Title | Book One | Budget | Shipped |
|---|---|---|---|---|
| I | Waters | ch. 1 | 35 | 11 |
| II | Ashes | ch. 2–3 | 40 | 8 |
| III | The Followers | ch. 4–5 | 40 | 6 |
| IV | The Waste | (gamebook) | 45 | 8 |
| V | The Mission | ch. 6 | 55 | 18 |
| VI | Dustwater | ch. 7 | 40 | 4 |
| VII | The Night Road | (ch. 8 run) | 25 | 3 |
| VIII | The Dark | ch. 8 | 55 | 10 |
| IX | The Bell | ch. 8–9 | 35 + 13 endings | 8 endings |

### Act I · Waters (entry `the-crossing`; exits `hollow-bell`, `dust-road`, `ending-water`)
Zuzu alone; the standoff; the croc; the bandage; trust. **Adds:**
- *Before the standoff:* approaching by the black stones (Sense) reveals old bones in the shallows; a cracked
  bowl with a child's name scratched in it (first quiet hint of the mission road).
- *The standoff branches* (Mercy / Steel / Shadow): drop the hand, hold, or circle downwind. Shadow route
  sees the croc first.
- *The fight's terrain:* lure the croc onto the stones, use the coyote's shot (if warned), or the reeds.
- **Dilemma — the gun in the water.** After the fight the coyote's revolver lies in the shallows. Return it to
  a man who can no longer shoot right-handed (`honor:returned-the-gun`, `debt:coyote` deepens), keep it to
  trade (Dustwater pays well; he will remember), or throw it into the deep (he never forgives, or thanks you
  later).
- **Dilemma — the nest.** Croc eggs on the far bank: food for days (heal, provisions) or leave them.
- **Beauty:** the parting at dusk, two shadows, and a night where the stars are spilled.
- *Taint seed:* none yet. The water is only water.

### Act II · Ashes (entry `hollow-bell`; exits `they-follow`, `ending-alone`)
Hollow Bell after the massacre. **Adds:**
- **Investigation:** who did this? Clues point two ways and the book never settles it: raider boot prints,
  shell casings, AND black candle wax on a threshold and every child's bed empty. (`clue:wax`, `clue:raiders`)
- **Dilemma — the dying shopkeeper** (an old badger): one canteen. Give it to a man who will die anyway (he
  tells you, with his last breath, that "the bell rang inside the smoke" and that the children were taken
  *before* the fire; `honor:last-water`) or keep it for the children you have not yet found.
- **Dilemma — the looter** (a young raccoon stripping boots from the dead): break his hand (taint), shame him
  and send him off with nothing, or let him take what he needs and leave the dead their boots
  (`debt:looter`). He returns in Act IV.
- *The bell tower:* climb it; from the top see the mission's tower far south, and a line of small tracks.
- *Honour the dead* (shipped) gains a song: Zuzu sings what his people sing for the dead (`honor:sang`). Beauty.
- The siblings (shipped) gain more ways to earn the first inch of trust.

### Act III · The Followers (entry `they-follow`; exit `canyon-road`, `ending-alone`)
The road with two small shadows behind. **Adds:**
- *Days on the road*, compressed: the distance between fires shrinks with each kindness.
- **Dilemma — the theft.** The sister steals your last food in the night. Confront her (she runs; trust lost),
  let it go and say nothing (`honor:let-her-keep-it`), or let her see you saw and still say nothing
  (Mercy +1, trust gained).
- **Dilemma — the fever.** The toddler burns with fever. Spend Last Kindness, your water, or your bandage;
  or keep walking and hope. The cost is real either way.
- **The cowled watcher** (shipped) gains a follow-up: tracks of soft sandals, a dropped black candle.
- The apple tree (shipped) gains its canon key image: the sister's paw reaching for the apples, and she feeds
  her brother first. **Beauty.**

### Act IV · The Waste (entry `canyon-road`; exit `mission-gate`)
New gamebook act between the apple tree and the mission: the land itself. **Adds:**
- *The rope bridge and the dry river* (shipped), *the relic* (shipped) gains **the whispering stone face**: a
  cracked stone face too large for any animal. Listen (it tells you the mission's bell has no clapper and
  that it is hungry, `taint:listened`) or cover the children's ears and walk on.
- **The dry well and the raiders.** A starving jackal band holds the only water and demands a toll: the girl.
  Options: fight five (very hard), pay everything you carry, trick them (Shadow), or find the hidden kits in
  the rocks and *share* your water with the raider mother (`honor:shared-water`, `debt:raider-mother`). The
  looter from Act II, if spared, is their scout and may warn you or vouch for you.
- **Brother Peddler** sells "blessed water" to a ruined family at a waystation. Expose him (the family loses
  hope and the water), stay silent, or pay him to give it away free (lose supplies, `honor:paid-for-hope`).
- **The Storm Crow witch at the crossroads.** On a dead tree, a crow witch far from her cave. She offers a
  black feather that shows true faces (it reveals the Abbess in Act V) for a price: a memory of home (lose the
  thread to your homeland; a later dream offer has nothing to bargain with), a drop of blood (`taint:blood`),
  or a debt. Refusing is allowed and costs nothing but the sight.
- **The storm and the shrine.** A dust storm drives the three into a ruin of the lost humans. A night of
  shelter, the children asleep against him: **beauty**, and in the morning a desert bloom after rain.
- *The vulture's wagon* (shipped) with the child's shoe leads to the mission road.

### Act V · The Mission (entry `mission-gate`; exits `mission`, `night-flight`, `take-them`, `cellar`)
The welcome, then the dread (Silas, 2026-10-09). Shipped: lantern, supper, courtyard, tracks, chapel, bell,
dormitory, locked door, crypt glimpse, morning. **Adds:**
- **A second day:** Zuzu asked to stay and mend the wall, chores alongside the nuns; the children bathed and
  dressed in clean clothes (the sister refuses to give up her rags).
- **Sister Wren**, the novice: slips Zuzu a note, *go*. Dilemma: tell the Abbess (buys her trust, damns
  Wren), protect Wren's secret, or ask Wren to help (she can open the crypt, hold a door, or betray you if
  frightened).
- **The other children:** a silent rabbit kit who has been here "a long time", the doll's owner, gone.
- **Dilemma — the Abbess's commission.** She offers Zuzu water and coin to escort a "pilgrim child" to a sister
  house in Dustwater. Accept (you deliver a child into the barter: `taint:delivered`), refuse, or accept and
  look in the wagon on the road (it opens Act VI's truth about the water baron).
- **The dream.** That night the thing speaks: it can show Zuzu the road home. Listen (`taint:dreamed`; the
  homeland thread, if the witch did not take it, becomes a hook) or wake.
- *The feather* (Act IV) shows the Abbess's true face at supper: the warmth is a mask over something
  patient and hungry.

### Act VI · Dustwater (entry `posters`; exit `run-back`, `ending-warning`)
The notice town (Book One ch. 7; WORLD-GUIDE: Dustwater Crossing's outskirts). **Adds:**
- **Mags** the barkeep (shipped as "the barkeep"): truth for kindness; her son's notice on the wall.
- **Gideon Vane, water baron:** the town's wells are his; orphans go to the mission and water comes back. Expose
  him to the town (riot), make him confess and pay the town's water forward (`honor:bound-the-baron`), or kill
  him in his office (`taint:killed-unarmed` if he begs).
- **The mob.** Mags gathers torches to burn the mission tonight, with the children still inside. Lead them
  (faster; fire does not choose), talk them down (`honor:held-the-mob`, Mercy check), or slip away alone.
- **The bounty hunter** (a badger) is hunting the coyote: protect the coyote (if met), sell him for water
  (`taint:sold-him`), or tell the truth and let the badger decide.
- The notice wall (shipped) and SF1, the realisation.

### Act VII · The Night Road (entry `run-back`; exit `mission-night`)
The run back on foot. **Adds:**
- **The road shifts.** In the dark the land is not where it was. The thin-place shortcut through the black
  rocks gets you there in time and leaves a mark (`taint:thin-road`); the long way costs `late`.
- The coyote's return (shipped) can now also come via the raider mother's band if `debt:raider-mother`.
- The witch, if paid, appears on a fence post and points.

### Act VIII · The Dark (entry `mission-night`; exits `rescue`, `last-breath`, endings)
The mission at night (Book One ch. 8). **Adds:**
- Approaches: alone, with Wren, with the coyote, with the mob at the gate (fire), by the crypt passage.
- **Free the other children first** (time) or go straight to the altar (they may not be there when you
  return).
- The nuns (shipped battle) gain non-combat routes: Wren opens a door, the feather shows which nun is afraid.
- **The Abbess at knifepoint:** "Leave now, and the girl lives." Sometimes true. Trust her, refuse, or strike.
- **The thing speaks aloud:** "Give me the small one and I will give you home." Refuse (`honor:refused-the-dark`),
  or accept (*The Bargain*).
- The sister's dagger (shipped) remains the canon mirror: she can save Zuzu if he cut her free.

### Act IX · The Bell (entry `rescue`; endings)
After. **Adds:**
- **The surviving nuns** beg for mercy: spare them, hand them to Dustwater's mob, or leave them to the
  desert. Wren's fate.
- **The mission's children**: take them to Dustwater (Mags), leave them with Wren, or walk on with only the two.
- **The sister** stands among the dead with the knife (SF3 mirror). What Zuzu does next decides whether she
  follows behind him or walks beside him.
- **The bell**: forge a clapper and ring it.

## 6. Endings (13)

| # | Ending | Tone | Route / requirement |
|---|---|---|---|
| 1 | Silence Beneath the Surface | dark | lose to the croc |
| 2 | One Shadow on the Road | bittersweet | abandon the children |
| 3 | The Unheard Warning | bittersweet | warn the towns and leave |
| 4 | The Bell Without a Ringer | dark | fall at the altar |
| 5 | Hunted | bittersweet | escape with the children; the Abbess lives |
| 6 | Three Small Shadows | hope | the canon ending |
| 7 | One Fire | hope | the coyote repays his debt |
| 8 | What the Desert Keeps | hope | seal the breach at a price |
| 9 | **The Bell Rings** | best | free every child, seal or sever the breach, ring the bell; Honor ≥ 6, Taint ≤ 1 |
| 10 | Ashes on the Wind | dark | the mob burns the mission with the children inside |
| 11 | The Hollow Saint | dark | Taint ≥ 3: Zuzu takes the thing into himself to close it; the children live and fear him |
| 12 | The Bargain | dark | trade the toddler for the road home |
| 13 | The Coyote's Road | bittersweet | the sister and toddler go with the coyote; Zuzu stays to bury the dead |

Endings record the journal (debts kept, the bell, the feather) so a single ending can read differently on
different runs. Variants of wording are not counted as separate endings.

## 7. Flag registry (shared contract)

Shipped flags keep their names. New flags use prefixes:

- `honor:*`, `taint:*` (counted, see §2); `debt:*`; `clue:*` (journal facts); `met:*` (who Zuzu has met).
- Shipped: `coyote-kindness`, `coyote-warned`, `coyote-trust`, `coyote-debt`, `honoured-dead`, `poster-clue`,
  `siblings-fed`, `siblings-follow`, `sister-trust`, `went-back`, `night-kindness`, `watcher-seen`,
  `apples-left`, `relic-seen`, `shoe-seen`, `staying`, `abbess-doubt`, `no-tracks-out`, `silent-bell`,
  `doll-found`, `abbess-wary`, `crypt-seen`, `abbess-suspicion`, `late`, `ally-coyote`, `sister-free`,
  `siblings-saved`, `portal-closed`.
- Planned: `debt:looter`, `debt:raider-mother`, `clue:wax`, `clue:raiders`, `feather`, `homeland-lost`,
  `met:wren`, `wren-ally`, `wren-betrayed`, `met:mags`, `baron-bound`, `mob-coming`, `mob-held`, `bounty-sold`,
  `thin-road`, `children-freed`, `clapper`.

## 8. Art plan

Reuse vetted plates first (37 shipped; the `worlds/zuzu` ledger inventory holds 800+ renders). New plates per act,
queued as ArtJob rounds in `art/ROUND-n.yaml` (house lane Arthemy Western Art v3.0; Kontext restaging of the locked
cast for character moments; prompt contract pre-checked; words that drew wrong things are avoided: poster, kasa in
still lifes, flint, bandage, smoking).

| Act | New plates (priority) |
|---|---|
| I | the gun in the shallows; croc eggs on the bank; bones and a cracked bowl in the shallows |
| II | the dying badger shopkeeper; the raccoon looter among boots; candle wax on a threshold; view from the bell tower |
| III | the sister asleep with stolen bread; the toddler feverish by the fire; the sister feeding her brother apples |
| IV | the whispering stone face; the dry well and jackal raiders; the raider mother's hidden kits; the hare peddler; the crow witch on a dead tree; the shrine in the storm; the desert bloom |
| V | Sister Wren; the silent rabbit kit; the pilgrim wagon; the dream (coiled dark and a road of light) |
| VI | Mags behind the bar; the water baron's office; the torch mob; the badger bounty hunter |
| VII | the shifting road among black rocks |
| VIII | the mob's fire at the gate; children in the cellar cells; the Abbess at knifepoint |
| IX | the nuns on their knees; the children leaving; **the bell rung at dawn** |

## 9. Build order

1. Engine: Honor/Taint tallies, `needsHonor`/`needsTaint`, `effects.attr` (done with this outline).
2. Acts I–IV to budget (the road to the mission), with art round 4.
3. Acts V–VI, then VII–IX, each with its art round.
4. Balance pass: stateful exploration must reach all 13 endings; each act's dilemmas must each be taken in play.
