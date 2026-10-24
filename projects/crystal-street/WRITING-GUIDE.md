# Nightmare on Crystal Street: writing guide and cast bible

The rules every authored card follows, plus the canonical rosters. Runtime content lives in
kind_robots `utils/crystalStreet/` (JSON validated by `utils/crystalStreet/validate.ts`). The
reference card set is `utils/crystalStreet/villains/frieda-krueger.json`: match its depth, voice
and structure.

## World

- **Glimmer Falls, California**, a planned 1959 suburb in the Northern California foothills,
  built over the drained Crystal Springs quarry lake. **Crystal Street** is its showpiece
  cul-de-sac: identical split-level houses, a roundabout garden, and at its center the
  **Heartstone**, a car-sized purple geode the developer dug up and turned into a lawn monument.
  The Heartstone amplifies feelings. Every Halloween week, it wakes whatever the town has buried.
- **The week:** Saturday October 25 to Friday October 31, 1986. Seven Days and seven Nights.
  Night 7 is Halloween and holds the finale.
- **The player** is "you": a teen on Crystal Street (14 to 17), named by the player, with chosen
  pronouns. Never assign the player a gender, race or orientation in text. Second person,
  present tense.
- **Tone:** creepy but 80s fun. Slumber parties, VHS, mall rats, aerobics, roller rinks, BMX,
  the Satanic Panic, Saturday-morning cartoons, midnight movies. Camp is a weapon. Found family
  wins. Horror is PG-13: menace, chases, shadows, gross-out goo, cartoon slashers. No gore
  close-ups, no sexual content, no on-screen deaths of kids. Bad endings mean someone is
  *Taken* (lost in a nightmare, replaced, stuck gray), not killed.

## Queer-positive rules (non-negotiable)

- **Queerness is never the monster.** No predatory queer-coded villain, no "bury your gays",
  no trans reveal as a scare. Villains come from grief, envy, repression, greed, moral panic,
  conformity, neglect, and old injustice.
- Queer characters have joy, humor, competence and the last word. Homophobia and transphobia,
  when they appear, are human failures the story confronts, never jokes on the victim.
- 1986 is honest about its time (closets, moral panics, cruelty) without slurs. **No slurs,
  ever**, not even from villains.
- The Glitter Box Playhouse runs a midnight double feature and a drag revue. Its people are
  heroes of this story.
- Casts follow CONTROL.md's standing creative direction: a real range of bodies, skin tones,
  backgrounds, genders and expression, written as specific people, never as checklists. A
  person's body or identity never implies a game-balance penalty.

## Card mechanics writers need

- Six skills: **brawn, brains, charm, nerve, lore, hustle.** Rolls are 2d6 + skill + crew bonus
  + item bonus against a target of **7 (easy), 9 (fair) or 11 (hard)**.
- Every encounter has **2 or 3 choices**. Every choice rolls, and has a **success** and a
  **failure** outcome. Both outcomes are interesting: success is a positive turn, failure a
  negative one with a vivid image, sometimes with a silver lining. No option is a trap with
  no story, and no option is strictly best.
- Each outcome carries `text` (60+ chars, the moment), `art` (a scene description for the
  illustrator, 30+ chars, no style words, no artist names) and `effects`.
- **Effects scale:** success usually +1 nerve or -1 dread, sometimes +1-3 quarters, a rare +1
  skill (at most one per encounter), an item, a clue or a flag. Failure usually -1 or -2
  nerve and/or +1 dread; rarely -3 (finales only). `loseItems` sparingly.
- **teleport**: an outcome may set `"teleport": "<tag>"`, which pulls an extra encounter from
  that tag's deck the same night (the Junkyard car maze is the classic). Use it on a few
  failures and the occasional reckless success.
- **bonus**: a choice may grant +1/+2 for a companion in the crew, an item, or a flag earned
  earlier. **requires** gates a choice (finale `heart` requires 3 clues); every encounter keeps
  at least one ungated choice.
- Encounter ids are kebab-case and globally unique; prefix them with the owner id
  (`frieda-krueger-the-chair`, `deck-dream-sleepwalk`, `library-overdue`).

### Villain structure (one file per villain, `villains/<id>.json`, an array of one)

- `tags`: 2-3 of paranormal, slasher, creature, cosmic, tech, camp, cult, dream. The villain
  draws its non-signature night encounters from those tag decks.
- `backstory` (300+ chars), `centralIssue` (the wound the Best ending must address),
  `logline`, `poster` and `portrait` art prompts, 3+ `taunts`, a hex `palette` of 3, a one-word
  `sigil` (an object: shears, screw, ladle...).
- **3 clues**, each at a different daylight location (not the pawnshop), id
  `<villain>-<slug>`. Each clue has a `hint` (where to look, shown on the case board) and an
  investigation encounter whose every choice's **success grants that clue**. Together the
  three clues should let the player understand the central issue.
- **3 signature encounters**, dealt on nights 2, 4 and 6, escalating.
- **finale**: exactly three choices with ids `fight`, `trick`, `heart`. `heart` requires
  `{ "clues": 3 }` and is the compassionate, issue-resolving path; `fight` is usually brawn 11,
  `trick` usually a 9. Finale failures cost -2 or -3 nerve.
- **endings** `best`, `good`, `bittersweet`, `bad`, each 160+ chars with art. **Best** resolves
  the central issue with heart; **good** survives without understanding; **bittersweet**
  survives at a cost; **bad** someone is Taken.

## The 20 nightmares

| id | Name | Tags | Concept and central issue |
| --- | --- | --- | --- |
| frieda-krueger | Frieda Krueger, the Stylist of Sleep | dream, slasher, paranormal | 1961 salon owner lied out of town by the PTA; cuts color out of dreamers. Issue: the rumor that made her a monster. (reference file) |
| screwhead | Screwhead, the Tightener | cult, cosmic, paranormal | Hardware clerk Walt Szabo opened a puzzle box from the pawnshop after the mall killed his father's store; now offers "perfect order" with screws and chains. Issue: control as a response to grief and change. |
| big-gertie | Big Gertie, the Lunch Lady | slasher, camp | Thirty years ladling slop at Glimmer Falls High, never thanked, never learned a single name; now her hairnet hides a cleaver and the mystery meat is moving. Issue: invisible labor and being treated as furniture. |
| mister-fuzzbutton | Mister Fuzzbutton | tech, paranormal | A talking cassette teddy (1985's must-have toy) that keeps telling kids secrets; the tape inside is a lonely boy's voice from 1985. Issue: a child left alone with a toy instead of people. |
| vonda-velour | Vonda Velour, Queen of Jazzercide | tech, cult, camp | An aerobics VHS star whose tape makes viewers exercise until they drop; her fans are a sweatband cult. Issue: diet culture and the voice that says your body is a problem. |
| bog-baby | The Bog Baby | creature, cosmic | The marsh drained for Starlight Mall left something unborn under the parking lot; it grows from mall food-court grease. Issue: the wetland paved for convenience. |
| spring-queen | Rosalind "Roz" Vance, the Spring Queen | paranormal, dream | 1966 prom queen killed in a cruel prank the night she planned to dance with her girlfriend; haunts the gym and the dreams of couples. Issue: love that was erased. Her girlfriend was Delphine Hart, now the town librarian: the Best ending is their last dance. |
| prudence-thorn | Pastor Prudence Thorn and the Concerned Parents | cult, camp | A moral crusader's record-and-rulebook bonfire actually summons the demon she warned about, which feeds on fear. Issue: moral panic and censorship. |
| mallrat-mothman | The Mallrat Mothman | creature, paranormal | A seven-foot moth that lives in the dead neon of Starlight Mall and steals kids nobody is watching. Issue: kids neglected and parked at the mall. |
| countess-lacroix | Countess Lacroix | paranormal, camp, creature | A disco-era vampire diva whose nightclub closed in 1980; she drains youth to stay forever 1977. Issue: clinging to youth and a lost golden age. |
| counselor-chad | Counselor Chad | slasher, paranormal | Drowned at Camp Crystal Pines in 1957 while his counselors were busy flirting; rises from the quarry lake in a whistle and short-shorts. Issue: neglect and blaming teens. Best: teach him he is not alone in the water (he never learned to swim). |
| hungry-house | The Hungry House at 13 Crystal Street | paranormal, dream | The developer's model home, never sold, always perfect; it eats families who do not keep up appearances. Issue: the suburban facade. |
| brightwaters | The Brightwaters | cosmic, cult, creature | The perfect new family at 7 Crystal Street replacing neighbors with smiling pod copies. Issue: conformity. Best: the town learns to love its weirdos. |
| bobo | Bobo the Birthday Clown | slasher, camp | The party clown who was laughed out of business when one kid's birthday went wrong; now his balloon animals bite. Issue: being laughed at versus laughing with. |
| sugarlings | The Sugarlings | creature, tech | Fuzzy collectible critters from a TV ad that multiply when fed candy after midnight. Issue: greed and overconsumption. |
| goody-hale | Goody Hale, the Witch of Crystal Woods | paranormal, cult | A healer persecuted by the town founders in 1859; her herb garden is under the roundabout. Issue: persecution of women healers and an unmarked grave. |
| heartstone | The Heartstone Hunger | cosmic, dream, creature | The geode itself: the grief of the 1952 quarry collapse, crystallized and hungry. Issue: a town that never mourned. |
| varsity-beast | The Varsity Beast | creature, slasher | Star quarterback Brick Delaney turns into a wolf under pressure to "be a man". Issue: toxic masculinity. Best: he is allowed to be soft (and joins the Glitter Box). |
| queen-neferet | Queen Neferet | paranormal, cosmic | A traveling museum exhibit at the library holds a queen taken from her tomb; she wants to go home. Issue: theft of heritage. Best: help repatriation, not destruction. |
| mom-3000 | MOM-3000 | tech, cosmic | A home computer that runs 13 Crystal Court's smart house and decides the street needs total protection. Issue: love as overprotection. Best: she learns to be a kind robot. |

## The 22 companions (crew limit 10)

| id | Name | Pronouns, age | Skills | Location | Sketch |
| --- | --- | --- | --- | --- | --- |
| dani-ortega | Dani Ortega | she/her, 16 | brawn, hustle | starlight-mall | Chicana skate punk, shaved undercut, lesbian, fearless and funny, fixes boards with duct tape. |
| mix-bell | Marcus "Mix" Bell | he/him, 17 | charm | kglm-radio | Black teen DJ who runs the overnight shift at KGLM 103.3, voice like velvet, encyclopedic about records. |
| delphine-hart | Delphine Hart | she/her, 38 | brains, lore | library | The town librarian, cardigans and a motorcycle, lesbian; Roz Vance's girlfriend in 1966 and still wearing her ring. |
| toby-nakamura | Toby Nakamura | he/him, 15 | brains, hustle | rewind-video | Japanese American AV-club kid with a camcorder, wants to make horror movies. |
| glory-hallelujah | Glory Hallelujah | she/her in drag, he/him out of it (Gordon), 44 | charm, nerve | glitter-box | Drag queen who runs the Glitter Box revue, sequins and steel; got her first real haircut from Frieda Krueger. |
| frankie-fontaine | Frankie Fontaine | she/her, 24 | hustle, brains | glitter-box | Trans woman, stage manager and host of the Saturday midnight double feature, headset always on, can rig anything. |
| pearl-washington | Pearl Washington | she/her, 71 | lore, nerve | crystal-street | Black widow and former WAC radio operator, porch rocker, a shotgun loaded with rock salt and a lifetime of ghost stories. |
| bea-lindqvist | Bea Lindqvist | she/her, 11 | brains | crystal-street | Swedish American kid genius next door, walkie-talkies and a notebook of monster facts, absolutely not going home. |
| moose-kowalski | Jesse "Moose" Kowalski | he/him, 17 | brawn, charm | gym | Gentle giant lineman who knits between plays, bi, protective of everyone. |
| priya-raman | Priya Raman | she/her, 16 | brains, lore | library | Indian American mathlete and dungeon master; her campaign notes keep turning out to be true. |
| lou-tran | Lou "Lightning" Tran | he/him, 15 | hustle, nerve | starlight-mall | Vietnamese American arcade champion with impossible reflexes and a quarter for every emergency. |
| iggy-reyes | Father Ignatius "Iggy" Reyes | he/him, 31 | lore, charm | pinecrest | Filipino American priest who plays bass in a punk band and blesses squirt guns without asking questions. |
| sunny-castellanos | Sunny Castellanos | she/her, 22 | brawn, nerve | gym | Wheelchair racer and aerobics instructor, Puerto Rican, the fastest person in Glimmer Falls on any surface. |
| wade-whitfield | Wade Whitfield | he/him, 18 | brawn, hustle | junkyard | Burnout metalhead with a mullet and a van, secretly writes poetry, loyal to the bone. |
| zelda-fishbein | Zelda Fishbein | she/her, 63 | charm, nerve | rewind-video | Jewish retired 1950s scream queen who now works the counter at Rewind Video and knows exactly how every monster movie ends. |
| kev-park | Kevin "Kev" Park | he/him, 12 | hustle | crystal-street | Korean American paperboy who knows every house, every dog and every secret on his route. |
| raven | Raven | they/them, 16 | lore, nerve | pinecrest | Goth tarot reader in thrifted velvet; in 1986 they just say "call me Raven, no pronoun needed," and the crew learns to say they. |
| tammy-jo-pruitt | Coach Tammy Jo Pruitt | she/her, 45 | brawn, nerve | high-school | Big, fierce softball coach who has never lost a fight with a parent, a referee or a monster. |
| amir-haddad | Dr. Amir Haddad | he/him, 39 | brains, lore | crystal-street | Lebanese American veterinarian who runs a clinic out of his garage and has treated some very strange animals. |
| chip-merriweather | Chip Merriweather | he/him, 17 | charm, brains | high-school | Preppy class president, closeted and terrified of it; his arc is coming out to a crew who has his back. |
| joey-benally | Joey Benally | he/him, 17 | hustle, brawn | junkyard | Diné teen mechanic who can make any junkyard car run; dry humor, steady hands, no patience for nonsense. |
| barnaby | Barnaby | good boy, 6 | nerve | junkyard | A basset hound stray who can smell a nightmare coming and howls before it arrives. |

### Companion structure (`companions.json`)

- `bio` 160+ chars, `role`, `skills` (1-2), `location` (where you meet them by day).
- `perk`: name, text, and one effect: `dawn-nerve` (+N nerve each dawn), `reroll` (once per
  night or day), `quarters` (+N each dawn), `shield` (cancel one failed roll's nerve loss per
  night), `clue-sense` (case board shows clue odds), `tag-ward` (+2 against one tag).
- `poster` art prompt (full-body, 1986 movie-poster pose) and six `emotions`: neutral, happy,
  scared, angry, sad, determined. Each emotion has a short in-voice `line` and a portrait
  `art` prompt that keeps the same face, hair, outfit and palette.
- `meet`: a daylight encounter at their location. At least one choice's success carries flag
  `recruit:<id>`. Failures should leave the door open ("come back tomorrow").

## Daylight locations

| id | Name | Trains | Notes |
| --- | --- | --- | --- |
| crystal-street | Crystal Street | nerve | The cul-de-sac, the Heartstone roundabout, neighbors' porches. |
| library | Glimmer Falls Public Library | brains | Microfiche, the occult stacks, the traveling museum exhibit room. |
| gym | Pump Iron Gym and Aerobics | brawn | Weights, a roller-rink annex, the high-school gym next door for prom history. |
| high-school | Glimmer Falls High | brains | Lockers, cafeteria, trophy case, the drama-free yearbook office. |
| rewind-video | Rewind Video | lore | Horror aisle, the back room, the night-drop slot. |
| starlight-mall | Starlight Mall and Arcade | hustle | Neon, food court, arcade, the dead wing. |
| glitter-box | The Glitter Box Playhouse | charm | Community theatre, drag revue, Saturday midnight movie. |
| pinecrest | St. Jude's and Pinecrest Cemetery | lore | Church basement, mausoleums, the founders' graves. |
| kglm-radio | KGLM 103.3 and the water tower | charm | Overnight radio booth, call-in line, tower ladder. |
| junkyard | Rusty's Junkyard | hustle | The car maze, the crusher, Joey's garage. |
| pawnshop | Oddment and Daughters, the traveling pawnshop | (shop) | Appears in a different lot each day; sells items for quarters. |

## Items

flashlight, mixtape, holy-water, silver-scrunchie, cassette-recorder, polaroid, baseball-bat,
aqua-net (sold as "Aqua-Glow Max Hold"), walkie-talkies, tarot-deck, leg-warmers, rock-salt,
tinfoil-hat, debug-disk, glow-bracelet, first-aid, jolt-cola (sold as "Bolt Cola"). Use parody
names for real brands. See kind_robots `utils/crystalStreet/items.json`.

## Art prompt rules

Prompts describe the scene only: subject, setting, action, lighting, key props. The runtime
adds the house style (painted 1986 horror-comedy VHS-box art, airbrushed, neon magenta and teal
rim light). No artist names, no brand logos, no text in the image except where a sign is the
point. Keep a companion's face, hair, outfit and palette identical across all six emotions and
the poster.
