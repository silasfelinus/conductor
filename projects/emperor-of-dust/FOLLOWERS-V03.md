# Emperor of Dust: the twenty followers (v0.3)

*emperor-of-dust/t-011, 2026-10-19 PT. This is the cast for SYSTEMS-V03.md. The runtime records live in
Kind Robots `utils/emperorOfDust/fortress/followers.ts`, and that file is authoritative for numbers.
F001–F010 come from [FOLLOWERS-PILOT-01.md](FOLLOWERS-PILOT-01.md), re-expressed in the v0.3
schema. F011–F020 are new. No images exist yet: the art lines below are briefs for t-012, and a
brief is not a delivered image.*

## Rules this cast follows

- **Stats:** five stats from 0 to 10 (Might, Guile, Wits, Heart, Lore), totalling 19–26, so no one
  is good at everything.
- **Secrets:** each follower has a secret skill and a secret weakness, revealed the first time one
  matters on a quest. Some also have a **hidden allegiance** that differs from their origin, revealed
  only in conversation. The Codex remembers revealed secrets across runs.
- **Abilities:** each follower has **one unique ability**, and no two followers share a mechanic.
  A flat bonus to a stat is not an ability, since it plays exactly like a higher stat (Silas,
  2026-10-19). The three +2-stat "Rally" abilities and the two +5-affinity "Envoy" abilities were
  replaced that day with Stalling Letters, Hot Meals First, Under the Wall, Reads the Wind and Many
  Hands (below).
- **Romance:** six of the twenty are romanceable (Rook, Saffron, Nera, Ash, Vesper, Sable), across
  genders and presentations, whatever the emperor's presentation. **Young Komodo is never
  romanceable.**
- **Species:** a species never decides morality or skill (WORLD-GUIDE.md). **No two named
  characters share a species**, followers and NPCs together (Silas, 2026-10-19; Kind Robots tests
  this against `npcs.ts`). Unnamed extras may repeat species, so the Abbey's nuns stay otters as in
  Book One.
- **Zuzu's mother is at court.** This is a prequel running up to the devastation that makes the
  wasteland worse. **F003 Kiyo**, a koala, is Zuzu's mother, and Zuzu is a toddler at the fortress
  (Silas, 2026-10-19). Zuzu is not a recruit. Kiyo never names her homeland, so the WORLD-GUIDE's
  "a homeland nobody here has heard of" still holds. **F007 Ash is a fennec**, the species of Book
  One's orphaned siblings (who are not born yet in this era).
- **Recruitment:** four start at court (F001–F004). Everyone else needs a route in the story, and
  some can be missed entirely.

## Roster

| ID | Name | Species · pronouns | Origin → true allegiance | M/G/W/H/L | Unique ability | Romance | Recruited |
|---|---|---|---|---|---|---|---|
| F001 | Rook Bramble | hare · they | Freeholds | 5/7/6/4/2 | **Trailwise**: quests take a day less | yes | Starter |
| F002 | Saffron Kett | jackal · she | Jackalwire → secretly still Pack | 5/4/9/2/3 | **Jury-rig**: shores up the weakest requirement | yes | Starter |
| F003 | Kiyo | koala · she | Saltroad (came by sea) | 3/3/7/7/4 | **Bitter Tea**: party injuries 2 days shorter | no | Starter |
| F004 | Duchess Flint | tortoise · she | Freeholds | 4/1/5/9/3 | **Shell and Shawl**: party injury chance −15 | no | Starter |
| F005 | Pip Thread | moth · they | Hollow Bell → works against the mayor's office | 1/4/8/3/7 | **Footnotes**: reveals hidden requirements | no | Day 4 audience |
| F006 | Nera Gale | storm petrel · she | Storm Crows | 2/5/6/5/8 | **Reads the Wind**: at home, marks each day's false briefing | yes | Day 7, if the court carries the Crow parcel |
| F007 | Ash Quill | fennec · they | Saltroad | 4/8/5/5/2 | **Stalling Letters**: at home, one expiring quest gets a day more each night | yes | Act II, the missing-courier line |
| F008 | Bram Coil | buffalo · he | Freeholds | 9/2/6/3/2 | **Hot Meals First**: at home, the wounded heal a day faster each night | no | Day 5, if flour is bought or begged |
| F009 | Keel Understone | armadillo · they | Moles | 4/5/8/4/4 | **Under the Wall**: Keel's Wits also count toward Might | no | Act III, a genuine Mole truce |
| F010 | Lumen Shale | prairie dog · she | Moles | 2/3/6/9/4 | **Many Hands**: never takes a party place | no | Act IV, Mole reforms |
| F011 | Tamsin Gutterwing | gecko · she | Storm Crows → hates the Conclave | 3/8/5/3/6 | **Cave-Luck**: the party rolls twice, keeps the better | no | Day 7, the Crows' bonded runner |
| F012 | Brother Teodor Lull | capybara · he | Abbey → still writes to the Abbess | 2/4/5/8/6 | **Confessor**: on success, reveals one secret of each companion | no | Day 8, if the Coldbrook family is not handed over |
| F013 | Mags Ironhide | rhino · she | Gate Watch | 10/1/4/5/1 | **Last Wall**: no one on her quest can die | no | Day 10, after the Watch's oath |
| F014 | Pell Quickmarrow | rat · he | Rustline | 3/7/8/3/4 | **Salvage Rights**: +15 brass on success | no | Act II, after the Rustline appears |
| F015 | Isolde Brack | newt · she | Mire Mothers → believes the coven can be saved | 1/5/5/4/9 | **Heeded Omens**: a failure becomes a partial result | no | Act II, the Mirefen lanterns |
| F016 | Sable Thorne | black leopard · they | Black Verge Court → hunted by it | 8/4/5/6/3 | **Immaculate Apology**: failure costs half the goodwill | yes | Act III, a defector at the gate |
| F017 | Cobb Harrow | badger · he | Freeholds (Thistledown) | 7/3/4/6/1 | **Thick Hide**: his own injuries heal in half the time | no | Day 10, whatever becomes of Thistledown |
| F018 | Vesper Fanfare | ferret · she | Saltroad | 4/7/4/8/3 | **Encore**: triumphs come far more often | yes | Act II, a Saltroad fair |
| F019 | Hollin Moss | owl · he | Lamplight Archive | 1/3/9/4/8 | **Old Maps**: after any quest, every hidden requirement on the board is revealed | no | Act II, Lamplight support 12+ |
| F020 | Juniper Slate | opossum · they | The Yard | 4/6/5/7/2 | **Second Helpings**: the Yard warms by 2 on success | no | Day 9, Yard support 12+ |

## F011–F020 in full

### F011 Tamsin Gutterwing
**Gecko weather-runner, she/her. Origin: Storm Crow Conclave. True allegiance: against it.**

Tamsin was sold to the Conclave as a child to carry forecasts between the caves. She knows every
draught in the Heights and every price the Crows charge. She left owing nothing, and she means to
keep it that way.

| Kind | Name | What it does |
|---|---|---|
| Skill | Storm Legs | Weather: +3 |
| Weakness | Never Learned to Bargain | Negotiation: −2 |
| Hidden allegiance (`talk-tamsin-bonds`) | The Bonded Runner | Storm Crows: −3. She will not help the Conclave, and Crow audiences gain a hostile option while she is at court. |
| Ability | **Cave-Luck** | The party's quest is rolled twice, and the better roll is kept. |

**Arc:** she can help expose the bonded-runner trade or settle a quiet debt with one elder. Crow
affinity and her loyalty pull in opposite directions.

**Art:**
- *Design sheet:* slim olive-gold gecko; climbing wraps on hands and feet; storm-grey runner's sash
  with tally knots; one torn earring.
- *Illustrated moods:*
  - neutral: wary, pressed to a wall
  - happy: grin on a high ledge
  - excited: mid-leap
  - sad: picking at the old tally knots
  - angry: tail lashing, sash torn off
- *Portraits:*
  - neutral: sharp sideways look
  - injured: bandaged hand, tail splinted
  - dead: memorial frame, her sash laid across it

### F012 Brother Teodor Lull
**Capybara, former Abbey novice, he/him. Origin: the Abbey. True allegiance: still writes to the
Abbess.**

Teodor ran soup kitchens for the Abbey and left when Sister Marrow's arithmetic about beds stopped
adding up. He is kind, funny and generous, and every week he writes the Abbess a letter he tells
himself is harmless.

| Kind | Name | What it does |
|---|---|---|
| Skill | Gentle Voice | Negotiation: +2 |
| Weakness | Swamp Terrors | Mire Mothers: −2 |
| Hidden allegiance (`talk-teodor-letters`) | Letters to the Abbess | The Abbey: +3. The Abbey's quests go suspiciously smoothly with him along. |
| Ability | **Confessor** | On success, each companion's first hidden secret is revealed to the court. |

**Arc:** the Abbey's best informant is also a deeply good man. He can be turned, confronted or
lost to Komodo's buyer at Day 40.

**Art:**
- *Design sheet:* a round, unhurried capybara; grey novice robe with the hood cut off; ladle on a
  cord; ink on his fingers.
- *Illustrated moods:*
  - neutral: hands folded
  - happy: serving soup
  - excited: telling a joke too early
  - sad: an unsent letter
  - angry: the ladle thrown down
- *Portraits:*
  - neutral: kind eyes
  - injured: arm in a sling, still smiling
  - dead: memorial frame, a candle and an unopened letter

### F013 Mags Ironhide
**Rhino, Gate Watch veteran, she/her. Origin: the Gate Watch.**

Mags has stood at more gates than she can count. She reads poorly, sings badly and has never once
stepped aside.

| Kind | Name | What it does |
|---|---|---|
| Skill | The Wall | Defense: +3 |
| Weakness | Letters Swim | Records: −2 |
| Ability | **Last Wall** | On a quest she joins, a lethal blow becomes a wound instead. Nobody dies. |

**Arc:** the first follower who can make a lethal posting safe. Her worth depends on whether the
crown kept its Day 10 oath.

**Art:**
- *Design sheet:* broad grey rhino; dented brass gorget; a spear wrapped in prayer ribbons; a horn
  capped in iron.
- *Illustrated moods:*
  - neutral: at attention
  - happy: laughing with the Watch
  - excited: a charge
  - sad: polishing a dead friend's helmet
  - angry: the gate slammed shut
- *Portraits:*
  - neutral: a steady stare
  - injured: horn cap cracked, head bandaged
  - dead: memorial frame, her spear laid across

### F014 Pell Quickmarrow
**Rat salvager, he/him. Origin: the Rustline.**

Pell knows the sunken rail yards like a tongue knows teeth. He sells relics he does not understand
and, quietly, keeps the ones that hum.

| Kind | Name | What it does |
|---|---|---|
| Skill | Rail-Rat | Tunnels: +2 |
| Weakness | The Saltroad Debt | Saltroad: −2 |
| Ability | **Salvage Rights** | +15 brass on any success. |

**Arc:** the Archive wants his finds studied, and the Ledger wants them sold. He will choose
whoever pays and respects him first.

**Art:**
- *Design sheet:* wiry brown rat; patchwork coat with forty pockets; a lens on a chain; a rail spike
  for a walking stick.
- *Illustrated moods:*
  - neutral: weighing a relic
  - happy: a jackpot
  - excited: digging
  - sad: a relic that crumbled
  - angry: cheated at the counter
- *Portraits:*
  - neutral: an appraising squint
  - injured: a crushed paw, splinted
  - dead: memorial frame, the humming glass

### F015 Isolde Brack
**Newt witch, she/her. Origin: the Mire Mothers. True allegiance: believes the coven can be
saved.**

Isolde is a true fen-witch who left the Mothers' inner circle without leaving the coven. She
believes most witches are good and that the leadership can be outlasted.

| Kind | Name | What it does |
|---|---|---|
| Skill | Fen-Sight | Any quest that needs Lore: +2 |
| Weakness | Mole-Hated | Moles: −3 |
| Hidden allegiance (`talk-isolde-coven`) | Still a Daughter of the Fen | Mire Mothers: +3 |
| Ability | **Heeded Omens** | A failure on her quest becomes a partial result. |

**Arc:** Lumen, Keel and Wisp all distrust her. She may be right about the coven, or the most
sympathetic face of its darkest work.

**Art:**
- *Design sheet:* dappled orange newt; a reed crown; damp green shawl; lantern of green glass.
- *Illustrated moods:*
  - neutral: listening to water
  - happy: lanterns lit
  - excited: an omen read
  - sad: a reed crown floating away
  - angry: the lantern flares
- *Portraits:*
  - neutral: a calm gaze
  - injured: burned shawl, a bandaged arm
  - dead: memorial frame, a drowned lantern

### F016 Sable Thorne
**Black leopard courtier and defector, they/them. Origin: the Black Verge Court. Hunted by it.**

Sable left the Black Verge Court before its condition could be pressed on them, and has been
running ever since with impeccable manners.

| Kind | Name | What it does |
|---|---|---|
| Skill | Court Manners | Negotiation: +3 |
| Weakness | The Long Fever | Urgent quests: −3 |
| Hidden allegiance (`talk-sable-flight`) | Hunted | Black Verge Court: −3 |
| Ability | **Immaculate Apology** | Goodwill lost on a failed or partial quest is halved. |

**Arc:** the Court will ask for Sable back, politely and then not politely. Romanceable.

**Art:**
- *Design sheet:* a tall, lean black leopard with faint rosettes in strong light; a moth-eaten court
  coat of dark plum; white gloves; a single dark earring.
- *Illustrated moods:*
  - neutral: a bow
  - happy: a dry smile over tea
  - excited: dancing
  - sad: a mirror turned away
  - angry: gloves off
- *Portraits:*
  - neutral: composed
  - injured: fevered, collar loosened
  - dead: memorial frame, a white glove

### F017 Cobb Harrow
**Badger farmer, he/him. Origin: the Border Freeholds (Thistledown).**

Cobb has rebuilt the same barn three times. Whatever happened at Thistledown on Day 10, he walks
to the fortress afterward: to thank the crown, or to ask why nobody came.

| Kind | Name | What it does |
|---|---|---|
| Skill | Barn-Raiser | Repair: +2 |
| Weakness | The Burning | Jackalwire: −3 |
| Ability | **Thick Hide** | His own injuries heal in half the time. |

**Arc:** whether he can serve beside Saffron Kett, or ever sit at a Jackalwire table.

**Art:**
- *Design sheet:* stocky badger; patched overalls; a pitchfork with a bent tine; a straw hat with a
  burn hole.
- *Illustrated moods:*
  - neutral: leaning on the fork
  - happy: harvest in
  - excited: barn raising
  - sad: ashes
  - angry: the fork leveled
- *Portraits:*
  - neutral: a stubborn jaw
  - injured: a bandaged snout, still upright
  - dead: memorial frame, the burned hat

### F018 Vesper Fanfare
**Ferret fire-juggler, she/her. Origin: the Saltroad.**

Vesper works the caravan fairs juggling fire and passing the hat. She talks her way into anywhere
and out of most things, and she is happiest with a crowd.

| Kind | Name | What it does |
|---|---|---|
| Skill | Showstopper | Any quest that needs Heart: +2 |
| Weakness | Can't Sit Still | Records: −2 |
| Ability | **Encore** | Triumphs come far more often on her quests. |

**Arc:** a performer's honesty, fair-day politics on the Saltroad, and a romance that plays out in
public. Romanceable.

**Art:**
- *Design sheet:* sleek cream-and-sable ferret; a red sash; scorched gloves; three fire clubs.
- *Illustrated moods:*
  - neutral: twirling a club
  - happy: a bow to the crowd
  - excited: mid-juggle, flames high
  - sad: an empty hat
  - angry: clubs snuffed
- *Portraits:*
  - neutral: a mischievous smile
  - injured: a burned paw, a wrapped glove
  - dead: memorial frame, three cold clubs

### F019 Hollin Moss
**Owl archivist, he/him. Origin: the Lamplight Archive.**

Hollin is the Archive's oldest mapmaker. He flies slowly, reads everything and remembers roads that
no longer exist.

| Kind | Name | What it does |
|---|---|---|
| Skill | Knows the Old Maps | Tunnels: +2 |
| Weakness | Slow Wings | Urgent quests: −3 |
| Ability | **Old Maps** | After any quest he joins, every hidden requirement on the board is revealed. |

**Arc:** he finds the ledger page that does not add up (Day 32) and may be the first to suspect
Komodo.

**Art:**
- *Design sheet:* grey-brown barn owl; tiny spectacles; a scroll case; ink-stained flight feathers.
- *Illustrated moods:*
  - neutral: reading
  - happy: a rediscovered road
  - excited: maps spread out
  - sad: a burned archive
  - angry: feathers up over a forged record
- *Portraits:*
  - neutral: a thoughtful look
  - injured: wing bound
  - dead: memorial frame, a closed folio

### F020 Juniper Slate
**Opossum cook, they/them. Origin: the Yard.**

Juniper runs the fortress kitchens and knows everyone's business through their stomach. They
patch people up with broth and gossip.

| Kind | Name | What it does |
|---|---|---|
| Skill | Broth and Bandages | Medicine: +2 |
| Weakness | Won't Bully | Coercion: −3 |
| Ability | **Second Helpings** | The Yard's support rises by 2 on any success. |

**Arc:** the Yard's voice in the barracks. If the Yard ever turns on the throne, Juniper decides
which side the kitchens are on.

**Art:**
- *Design sheet:* grey-white opossum; a flour-dusted apron; a ladle and a wooden spoon tucked in the
  belt; a headscarf.
- *Illustrated moods:*
  - neutral: stirring a pot
  - happy: feeding a crowd
  - excited: a new recipe
  - sad: empty pots
  - angry: the spoon slammed down
- *Portraits:*
  - neutral: a warm grin
  - injured: a burned arm wrapped
  - dead: memorial frame, the ladle

## 2026-10-19 swaps in F001–F010

Silas's review on 2026-10-19 changed six of the first ten. The pilot's design sheets for these six
are superseded by the ones below; the others still carry from the pilot.

### F003 Kiyo, Zuzu's mother
**Koala medic, she/her. Origin: arrived by sea through the Saltroad. Starter.**

Hard straits drove Kiyo's family out of a homeland nobody at court has heard of, and a salt boat
carried what was left of them to the wasteland. She mends the court's wounded with a kettle, a
needle and a bitter tea from home, and keeps one eye on the door in case her little son Zuzu has
wandered off again. She is not romanceable.

| Kind | Name | What it does |
|---|---|---|
| Skill | Kettle and Needle | Medicine: +3 |
| Weakness | Strange Country | Tracking: −2 (two years here, still lost past the second well) |
| Ability | **Bitter Tea** | Injured members of her party come home with 2 fewer injury days. |

**Toddler Zuzu (barracks lines, one a day).** He is giggly, distractible and without any ambition,
which is bittersweet for anyone who knows the grave ronin he becomes. The lines include: he chases a
beetle and forgets it, delighted twice; he slept through the storm on the crossing; he will not sit
for a lesson and "wants nothing at all"; he calls every bird "Komodo" and Young Komodo is gracious
about it; a word for holding a sword, a word for bowing to it, a word for rationed water; he gave
his only toy to a crying stranger; "he likes his bread torn small, and he is afraid of bells";
"Everyone becomes serious out here. Not him. Not yet. Please, not yet."

**Art:**
- *Design sheet:* a small, sturdy grey koala with a round face and tufted ears; a faded indigo
  travelling coat with a foreign cut and a patched hem; a copper kettle and a needle case on her
  belt; a child's wooden toy tucked in a pocket. Same build and palette family as Zuzu (CAST-PICKS
  Z2), so the resemblance reads.
- *Illustrated moods:*
  - neutral: kneeling to bandage a wrist
  - happy: laughing as a toddler-sized blur passes
  - excited: Zuzu's first word in the new tongue
  - sad: looking out to sea from a high wall
  - angry: between a raider and the infirmary door
- *Portraits:* neutral: a tired, kind look; injured: a bandaged arm in a sling; dead: memorial
  frame, the kettle and the little toy.

### F002 Saffron Kett: jackal (was hyena)
- *Design sheet:* a lean golden jackal with big ears and a welding scar across the muzzle; machinist
  goggles; an oil-dark apron with a toolkit whose lid hides the Pack's welded insignia.

### F006 Nera Gale: storm petrel (was crow)
In wasteland slang a "stormy petrel" brings trouble with her, which suits a dissident.
- **Ability: Reads the Wind.** While Nera is at the fortress, the morning briefing that is false is
  marked. Komodo's own lies have "no weather in them at all": she can tell they are wrong, but not
  why.
- *Design sheet:* a small, sooty-dark seabird with a white rump flash and a hooked black bill; a
  scholar's coat of storm-grey with copper weather pins; a storm-glass on a chain.

### F007 Ash Quill: fennec (was fox)
Their sibling vanished on the Mission Road; a generation later, Book One's fennec orphans are taken
to the same Abbey.
- **Ability: Stalling Letters.** While Ash is at the fortress, one quest that would expire tonight
  gets one more day on the board (once per quest; authored quests before chores).
- *Design sheet:* a tiny sand-coloured fennec with enormous ears; a courier's satchel stuffed with
  letters; ink-stained paws; a cheerful red sash.

### F008 Bram Coil (species unchanged)
- **Ability: Hot Meals First.** While Bram is at the fortress, every injured follower heals a day
  faster each night. Sending him out has a cost.

### F009 Keel Understone: armadillo (was mole)
The Mole Revolutionaries are moles and the other burrowers who joined them.
- **Ability: Under the Wall.** Keel digs under what others push through: Keel's Wits also count
  toward the quest's Might requirements.
- *Design sheet:* a banded armadillo with a surveyor's chain, a brass lantern held high and a
  head-lamp; plates scuffed from tunnel walls.

### F010 Lumen Shale: prairie dog (was mole)
- **Ability: Many Hands.** Lumen never takes a party place: she can join a quest whose party is
  already full (party size up to five).
- *Design sheet:* an upright, alert prairie dog in a patched community-hall sash covered with
  hand-stitched names; a speaking trumpet made from a funnel.

## F001–F010 art (carried from the pilot)

Each keeps the pilot's visual brief as its design sheet, except the swaps above. The eight images are:
- **Illustrated moods (5):**
  - neutral: the pilot's healthy portrait pose
  - happy and excited: from their arc's best moment
  - sad: their arc's loss
  - angry: their flaw at its worst
- **Portraits (3):**
  - neutral and injured: the pilot's healthy and injured portraits, cropped to a bust
  - dead: a memorial frame with their keepsake: Rook's compass, Saffron's goggles, Kiyo's kettle,
    Flint's signet, Pip's spectacles, Nera's storm-glass, Ash's sash, Bram's abacus, Keel's lantern
    and Lumen's sash.

Asset ids follow SYSTEMS-V03.md: `followers/FNNN/illustrated/<mood>` and
`followers/FNNN/portrait/<state>`.

## Recruitment routes now in the game

- **Act I (Kind Robots, alongside this cast):**
  - F005 Pip (Day 4)
  - F006 Nera (Day 7, carrying the Crow parcel)
  - F008 Bram (Day 5, flour secured)
  - F011 Tamsin (Day 7)
  - F012 Teodor (Day 8, Coldbrooks not handed over)
  - F013 Mags (Day 10 oath)
  - F017 Cobb (Day 10, Thistledown)
  - F020 Juniper (Day 9, Yard support 12+)
- **Later acts (scripted with t-006 to t-008):** Ash, Keel, Lumen, Pell, Isolde, Sable, Vesper and
  Hollin.
