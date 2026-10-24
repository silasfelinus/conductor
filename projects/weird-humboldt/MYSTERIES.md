# Ecotone Mysteries — twelve local cases (t-062)

**Owner direction, 2026-10-23 PT (Silas):** an expansion of *Mysteries*: "a singular opportunity that
occurs once a game to pursue a random local mystery." Twelve multi-episode cases, each modeled on a sign
of the zodiac but never naming it ("unless it's buried in something like 'The mystery of the virgin
sacrifice'"); fresh stories in the backwoods and underbelly of Humboldt County; "a college aged Scooby
Doo vibe"; unique Mystery cards whose art hints at the sign; a **Case Files** screen showing which
mysteries you have uncovered and which gates you passed; about three gates per game, told as
digressions (a text from someone who clues you in); two passes open the true path, and a final choice
tree reaches one or more Real Endings.

Shipped in kind_robots `utils/ecotone/mysteries/` (engine, catalog, twelve case files), the Case Files
tab and `components/ecotone-mystery-card.vue`, with `npm run test:ecotone-mysteries` in the Ecotone
Gameplay Contract workflow.

## How a case plays

| Beat | When | What happens |
| --- | --- | --- |
| **Gate I** | before the run's first fork | A digression (text, voicemail, flyer, note, radio) pulls you into the case. 2–3 dice-checked approaches, or walk away and close the case for the run. |
| **Gate II** | before the crossroads | Second digression and scene; 2–3 checked approaches. |
| **Gate III** | before the finale | The trap / the confrontation; 2–3 checked approaches. |
| **True path** | 2 of 3 gates passed | The **reveal** (the unmasking) offers 2–4 choices; most lead to a **branch** scene with 2–3 more; every leaf is a **Real Ending** (true / bittersweet / strange). A closed case logs evidence (`Case closed: <title>`), which counts toward the county's future. |
| **Cold case** | fewer than 2 passes | The trail goes cold: a short scene with two small choices. |

- One case per run. New runs prefer cases you have not opened, so twelve runs can fill the shelf; after
  that any case can return. Older saves (no `mystery` field) derive their case from the seed and pick
  up Gate I at the next trigger, so nothing breaks.
- Gates play as interlude beats on the previous route index, so authored route positions, save version 4
  and every existing seeded contract are unchanged (the original Ecotone suite still passes: 1,764
  adversarial journeys, 8,400 campaigns, 84/84 endings).
- Gate effects are small (nerve/goodwill/weird ±1); the pass/fail flag is what the Case Files track.
- **Case Files** (localStorage `kr.ecotone.cases.v1`, owned by the store) keep the *best* result per
  gate across runs, whether the true path ever opened, whether a trail went cold, and which Real
  Endings you found.

## The twelve cases (after the playtest rewrites, 2026-10-24 PT)

| # | Seed | Case | Where | Under the mask (in the wrong?) | Uncanny | Real Endings (true · bittersweet · strange) |
| --- | --- | --- | --- | --- | --- | --- |
| I | Aries — go first | The Mystery of the Ridge Ram | Kneeland ridge and Kneeland Road | Hollis Ostrander, a retired county flagger who never once got to go first, leading a secret senior gravity-cart league behind an escaped ram (no) | the fog road; flaggers from every era | First Down the Mountain · The Ram Stays Wild · Waved Through |
| II | Taurus — stubborn, loyal to land | The Mystery of the Stubborn Herd | Eel River bottoms, Loleta–Ferndale | Rosie, the granddaughter who called you in — the calf is an inside job to stall a sale onto future floodland (mixed) | the herd refuses the tide line; Alma's 1964 flood | The Herd Knows · Sold, With Conditions · The Golden Calf |
| III | Gemini — two of everything | The Mystery of the Second Voice | Trinidad harbor and Trinidad Head | Twins Lyle and Lowell, living one life in shifts — and the whole harbor always knew (mixed) | a pirate radio that broadcasts what people haven't said yet | Two of a Kind · One Life, Shared · Talk to Yourself |
| IV | Cancer — home, shell, memory | The Mystery of the Crab Pot Ghost | King Salmon, Fields Landing, Buhne Point | Arne Sorensen, a widower living secretly aboard the crab boat in his late wife Ione's yellow oilskins, feeding neighbors behind on rent (no) | a delivery list of houses torn down long ago (the past) | Home Port · The Last Haul · Moored in 1970 |
| V | Leo — pride, the spotlight | The Mystery of the Midnight Mane | the Eureka waterfront, an invented movie palace | Marguerite Tsai, the owner and Ronnie's old understudy, running a pride-and-price con on her own buyer (yes) | a 1981 reel (the past) | Long Live the Queen · One More Saturday · The Reel From 1981 |
| VI | Virgo — meticulous service | The Mystery of the Virgin Sacrifice | an invented inholding above Rio Dell | the Sisters of the Understory, robed volunteer surveyors counting the last "virgin timber"; the real wrongdoer is a land-trust contact rounding their numbers down (yes, Spencer) | a core whose rings go on past counting | Every Tree Counted · One Tree Saved · The Uncounted Ring |
| VII | Libra — balance, partnership | The Mystery of the Graveyard Gavel | Ferndale cemetery and Main Street | Lupe and Soren, the feuding families' college-age grandchildren, in love; Wendell plays the judge they recruited (mixed, under 30) | a court of the dead (the past) | Court Adjourned · A Fair Split · The Older Docket |
| VIII | Scorpio — secrets, death and rebirth | The Mystery of Murder Mountain | Alderpoint and the ridges above the Eel | Reyna Pell guarding the clearing where her father Gus (alive, with dementia) buried letters to her; the crows mourn early (no) | crows mourning a death that hasn't happened | The Crows Remember · Let It Stay Buried · The Keeper of the Blue Bin |
| IX | Sagittarius — freedom | The Mystery of the Wandering Arrows | the Lost Coast | Dr. Wren Okonkwo-Barlow (they/them), ex-philosophy professor turned trail angel on horseback (no) | arrows that turn toward whoever is lost right now | Coffee for Ten · The Rider Moves On · The Arrow That Points at Wren |
| X | Capricorn — ambition | The Mystery of the Sea-Goat of Samoa | the Samoa pulp-mill pier | Tess Keough, a restoration biologist faking a documented monster to win her grant (yes) — then the real sea-goat surfaces | the classic sting | The Night Watch · The Whistle Stops · The Graveyard Shift |
| XI | Aquarius — futurist | The Mystery of the Dated Jugs | Blue Lake, Korbel, Highway 299 | Chance Pruitt, a water-rights broker in a UFO rig using hydrologist Saff's warning jugs as his buy list (yes); Saff is the red herring | jugs dated for the day each well fails | Water for Everyone · The Jugs Stop Coming · Contact |
| XII | Pisces — dreams, two currents | The Mystery of the Two-Tailed Mermaid | Moonstone Beach, Little River mouth, Clam Beach | two mermaids: Coral Venn, a busker presumed drowned who chose to live and vanished from a debt, and a fake staged by her ex-manager Dex for his tours (Dex, yes) | parallel lives, both alive | Both Tails · Let Her Swim · The Other Current |

84 playable scenes, 36 Real Endings, about 55,000 words. Five culprits are in the wrong, three are under 30, and the
uncanny devices split four past / four future / four other. Under the mask (2026-10-24 PT, Silas: "vary the culprit
genders across the twelve cases"): five women (II, V, VI, VIII, X), five men (I, III, IV, XI, XII), one nonbinary
(IX) and one couple (VII); the wrongdoers are three men (Spencer, Pruitt, Dex) and two women (Marguerite, Tess).

### Mechanics added in t-063
- `reveal.afterMiss`: the reveal's opening when the Gate III trap failed (the most common bug in the first playtest).
- Approach memory (`mystery_gN_via_<approach>`) and `recall` lines keyed `gN:pass|fail|<approach>`, so failures and
  discoveries visibly carry forward.
- Cold cases must acknowledge a Gate III win; the validator enforces all of it.
- Playbook Manager: every scene and Real Ending is a node, one Collection per case, live edits reach play.
- Playtest record: [MYSTERIES-PLAYTEST.md](MYSTERIES-PLAYTEST.md).

### Murder Mountain handling

Case VIII answers "why do they call it that" through an old-timer's line ("Folks up here'll tell you
it's for the crows… Folks down the hill'll tell you it's for the other thing. Both are true, and only
one of them is funny"), and the unmasking carries one plain, non-joke acknowledgement that real families
still search these roads for people who went missing. It invents no real crime, victim, case or
identifiable property, and nothing in it describes cultivation.

## Content guardrails (all twelve)

- No sign names, "zodiac", "horoscope" or "astrology" in player-facing text (the validator enforces it
  with word boundaries); the signs live only in the case's `sign` field, its temperament, its motif and
  its constellation.
- No Wiyot/Tuluwat or other Native cultural, spiritual or historical material (EXCLUDED-CONTENT-2026-10-22.md).
- Real places as geography only; every person, business and wrongdoing is invented and each case's
  `provenance` says what is real. Documented history (the 1992 Cape Mendocino uplift, the Luna tree-sit,
  the Samoa pulp mill closure and cleanup, crow face-recognition research) is phrased cautiously.
- Every case has an earned non-joke moment, a Scooby-Doo unmasking, and an uncanny remainder tied to
  Ecotone's overlapping futures.

## Mystery cards

`ecotone-mystery-card.vue` draws each card in code: the element's palette (fire, earth, air, water), the
case numeral, element marks in the corners, a faint unlabeled constellation of the sign, a motif (ram
horns, a cow at the tide line, twin lighthouse beams, a crab pot, a sun-mane, three redwoods, scales,
crows on a branch, an arrow, a goat-fish under a smokestack, a water jug, two fish) and fog. Unopened
cases show a card back. Painted art overlays the drawn card once it renders:
12 Krea 2 requests `weird-humboldt-mystery-card-*` in `projects/art-prompts.yaml`, delivering to
kind_robots `public/images/ecotone/mysteries/<id>.webp` (512×768). Queued is not rendered; check the
final URL.

## Follow-ups

- Done in t-063: Playbook Manager listing and live edits; scene, gate-outcome and Real Ending art
  (`art/MYSTERIES-ROUND-1.yaml`, 336 subjects, Z-Image); the blind playtest ([MYSTERIES-PLAYTEST.md](MYSTERIES-PLAYTEST.md)).
- Done in t-064: culprit genders varied (I, IV, IX rewritten; their culprit art re-briefed).
- Open: Silas's editorial read; true-path rate after real play.
