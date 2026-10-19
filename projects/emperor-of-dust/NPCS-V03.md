# Emperor of Dust: major NPCs (v0.3)

*emperor-of-dust/t-027, 2026-10-19 PT. These are the speaking characters of the throne room and the
story, as distinct from the twenty followers ([FOLLOWERS-V03.md](FOLLOWERS-V03.md)). Under
SYSTEMS-V03.md, each **major NPC gets five illustrated moods** (neutral, happy, excited, sad, angry)
and **no portraits**. Young Komodo also gets a sixth image: **betrayal**. Minor petitioners (a
reed-cutter, a fledgling, a wagon-painter) get a faction crest and text only. No images exist yet:
these are briefs for t-012, and a brief is not a delivered image.*

Asset ids: `npcs/<slug>/illustrated/<mood>`. The `npc` field on an audience in Kind Robots
(`utils/emperorOfDust/fortress/act*.ts`) uses the slugs below.

## Canon guardrails

- **The Abbess** is Book One canon: an elderly otter with a short, blunt muzzle and a round, flat
  face, who is warm, patient and monstrous. Use her CAST-PICKS references (the abbess row, ArtJobs
  242177–242191) as her design sheet. Never design her afresh.
- Harm to children is stakes, never spectacle (WORLD-GUIDE.md). The Abbey's rooms are shown as
  neat, empty cots, never anything worse.
- Hollow Bell is still standing in this era. Nothing here names who destroys it in Book One.
- No two named characters share a species, NPCs and followers together (Silas, 2026-10-19).
  Kind Robots keeps the list in `utils/emperorOfDust/fortress/npcs.ts` and tests it. Book One's
  otter nuns stay otters as unnamed extras; Sister Marrow is a goat among them.
- Species never decides morality. Young Komodo looks friendly, and his look must not telegraph the
  betrayal.

## The cast

| Slug | Name | Who | First appears | Role in the story |
|---|---|---|---|---|
| `young-komodo` | **Young Komodo** | Komodo dragon, the emperor's advisor, he/him | Day 1 | Morning briefings and hints. His own lies are seeded from Day 7. **Betrays the throne on Day 40.** Never romanceable. |
| `mara-reedbell` | **Mara Reedbell** | Grey-muzzled mule, Mayor of Hollow Bell, she/her | Day 1 | Genial and protective of her town. Her ledgers hide terrible compromises (Day 29). |
| `the-abbess` | **The Abbess** | Elderly otter, head of the Abbey of the Silent Bell, she/her | Day 25 (in person) | Canon antagonist. Warm, generous and feeding something under the crypt. Becomes the patron of Komodo's betrayal. |
| `sister-marrow` | **Sister Marrow** | White goat, a nun of the Abbey, she/her | Day 8 | The Abbess's smiling hands in the world. Counts beds. |
| `sister-reedlight` | **Sister Reedlight** | Heron-witch of the Mire Mothers, she/her | Day 1 | The coven's gentle public face. Her lantern never flickers. |
| `gristle-vane` | **Captain Gristle Vane** | Hyena raider captain of the Jackalwire Pack, he/him | Day 1 (unnamed), Day 5 | Flamboyant extortionist with an excellent coat. Can become a rival, an ally or a corpse. |
| `oriel-saltmarsh` | **Oriel Saltmarsh** | Pelican caravan master of the Saltroad, she/her | Day 9 | Blunt, fair and ruthless about cargo. The Saltroad's voice at the Day 39 Congress. |
| `ferro-dunmark` | **Captain Ferro Dunmark** | Grey wolf, captain of the Gate Watch, he/him | Day 10 | Asks what the crown swears back. Holds the throne to its oath. |
| `ottoline-vask` | **Lady Ottoline Vask** | Black swan of the Old Houses, she/her | Day 7 | Precise, proud and patient about power. Her house may back Komodo. |
| `marisol-tallow` | **Factor Marisol Tallow** | Raccoon factor of the Ledger, she/her | Day 2 | Drafts charters before anyone asks. The Ledger's loans come with her handwriting. |
| `dunmore-ash` | **Foreman Dunmore Ash** | Boar foreman of the Yard, he/him | Day 2 | Says little, means all of it. Speaks for a hungry Yard. |
| `elder-corvane` | **Elder Corvane** | Ancient storm crow of the Conclave, he/him | Day 4 (silent), Act II | Sells rain, keeps bonded runners, and sees further than most. |
| `granny-umber` | **Granny Umber** | Elderly mole, a founder of the Mole Revolutionaries, she/her | Act II | Wants the throne gone, not burned. Can be reasoned with by deeds. |
| `the-verge-envoy` | **The Envoy of the Black Verge** | Gorilla courtier in white gloves, they/them | Act II end | Polite, patient and hungry. Wants Sable back. |

## Young Komodo

**Look:** a lanky young Komodo dragon in a patched, brass-buttoned coat (the description already
used in the Emperor of Dust achievement art). Clever, quick eyes, a ledger under one arm, and a habit
of tapping a claw when he is calculating.

**Voice:** dry, specific and comically precise about the price of a promise. He is the player's
friend for forty days, and that friendship should feel real.

**Motive (approved 2026-10-18):** he has bargained with the Abbess's order, believing that only a
surrendered throne lets the wasteland survive what is waking under the Abbey. He thinks he is the
pragmatic one.

**Seeded clues:**
- **Day 7:** his runner's false report about the empty Mole tunnels is his own lie (shipped, marked
  `komodoLie`).
- **Day 8:** he notices the Abbey's forty empty beds and tells the player to ask "not today, perhaps".
- **Day 17:** the Mole manifesto, which he reads first.
- **Day 25:** he greets the Abbess too warmly.
- **Day 32:** Hollin or the Archive finds a ledger page that does not add up.
- **Day 38:** a prisoner's name.
- **Day 39:** he seats the Congress.
- **Throughout:** with the Eye of the Elder Crow equipped, his lies are visible from Day 7 on a
  replay.

**Images:**
- **neutral:** the ledger open, a claw raised mid-point
- **happy:** a rare open grin over good news
- **excited:** pacing, the coat swinging
- **sad:** looking at the emperor when the emperor isn't looking
- **angry:** a cold, still stare, the ledger snapped shut
- **betrayal:** standing in the throne room doorway in the Abbey's grey, holding the emperor's
  seal, both sad and certain. Not a sneer.

## The others: art briefs

**Mara Reedbell:** a grey-muzzled mule in a mended mayoral sash, ink-stained hooves, a ledger chained
to her belt and a hand-bell on a cord.
- neutral: a smile above a closed ledger
- happy: laughing at a town fair
- excited: news of water
- sad: a closed door at night
- angry: the ledger slammed

**The Abbess:** canon design per the CAST-PICKS references.
- neutral: hands folded, warm smile
- happy: welcoming a traveller, children's shoes neatly paired behind her
- excited: listening at the crypt stair
- sad: a performed sorrow
- angry: the smile gone flat, which is the most frightening image in the game

**Sister Marrow:** a young white goat in grey Abbey robes, with a counting cord at her belt and
calm, rectangular-pupilled eyes.
- neutral: patient smile
- happy: gathering children's hands
- excited: counting beds
- sad: a mask of sympathy
- angry: smile unchanged, eyes not

**Sister Reedlight:** a slender grey heron-witch in a reed cloak, carrying a lantern of green glass
whose flame is perfectly still.
- neutral: a bow
- happy: lanterns on water
- excited: the lantern flares
- sad: the lantern dims
- angry: the reeds bend toward her

**Captain Gristle Vane:** a spotted hyena in a magnificent patched greatcoat of feathers, painted
leathers and a jangling ear-chain.
- neutral: a low bow
- happy: a cackle on a wagon roof
- excited: brandishing a toll ledger
- sad: a burned wagon
- angry: all teeth

**Oriel Saltmarsh:** a big white pelican with a weathered caravan coat, a ledger in her pouch and
goggles on her brow.
- neutral: counting wagons
- happy: a full convoy
- excited: a map unrolled
- sad: an empty road
- angry: wings spread

**Captain Ferro Dunmark:** a broad grey wolf in a dented gorget and Watch tabard, with a scarred
muzzle and one torn ear.
- neutral: at attention
- happy: a rare salute to the emperor
- excited: rallying the Watch
- sad: a list of names
- angry: the gate barred

**Lady Ottoline Vask:** an elegant black swan in a high-collared house coat, with heirloom rings
on her wingtips and a red bill.
- neutral: an inclined head
- happy: a thin smile
- excited: a council seat won
- sad: an empty portrait gallery
- angry: rings tapping the table

**Factor Marisol Tallow:** a sharp-eyed raccoon in a brass-buttoned waistcoat, with ink-stained
fingers and a pen behind her ear.
- neutral: the charter ready
- happy: brass counted
- excited: a deal struck
- sad: a defaulted loan
- angry: the pen snapped

**Foreman Dunmore Ash:** a heavy boar in a flour-dusted apron, sleeves rolled up and a ladle at his
belt.
- neutral: arms folded
- happy: ovens lit
- excited: a full larder
- sad: empty sacks
- angry: the ladle down hard

**Elder Corvane:** an ancient storm crow, feathers gone grey-blue, in a mantle of tiny copper chimes,
with clouded eyes that see fine.
- neutral: perched, silent
- happy: rain sold
- excited: the chimes ringing
- sad: a dry sky
- angry: the chimes silent

**Granny Umber:** an elderly mole in thick spectacles and a quilted vest of meeting notices, with a
cane of old pipe.
- neutral: a skeptical squint
- happy: a cell meeting
- excited: tunnels lit
- sad: a flooded burrow
- angry: the cane raised

**The Envoy of the Black Verge:** a tall gorilla courtier in a dark plum coat and white gloves, with
a faint pallor (a condition, not a species trait).
- neutral: a bow
- happy: a gift accepted
- excited: Sable sighted
- sad: refused
- angry: one glove removed

## Scripted appearances so far (Act I, live in Kind Robots)

| Day | NPC (slug) |
|---|---|
| 1 | `mara-reedbell`, `sister-reedlight`; Vane unnamed |
| 2 | Tallow and Dunmore, not yet slugged in the data |
| 3 | `mara-reedbell` |
| 5 | `gristle-vane` |
| 7 | Lady Vask, not yet slugged in the data |
| 8 | `sister-marrow` |
| 9 | `oriel-saltmarsh` |
| 10 | `ferro-dunmark` |

Later acts bring in the Abbess (Day 25), Corvane, Granny Umber and the Envoy. Komodo appears in
every briefing.
