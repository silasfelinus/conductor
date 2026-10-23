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

## The twelve cases

| # | Seed | Case | Where | Who is behind it | Real Endings (true · bittersweet · strange) |
| --- | --- | --- | --- | --- | --- |
| I | Aries — charge first, compete | The Mystery of the Ridge Ram | Kneeland ridge and Kneeland Road | Bev Ostrander, 71, retired flagger in a horned welding helmet, founder of a secret senior gravity-cart league led downhill by an escaped ram | First Down the Mountain · The Ram Stays Wild · Headfirst Into Tomorrow |
| II | Taurus — stubborn, loyal to land, pleasure | The Mystery of the Stubborn Herd | Eel River bottoms, Loleta–Ferndale dairy country | Alma Furtado, 80, in a glow-painted calf costume; her cows refuse the pastures that sea-level rise will take | The Herd Knows · Sold, With Conditions · The Golden Calf |
| III | Gemini — duality, chatter | The Mystery of the Second Voice | Trinidad harbor and Trinidad Head | Twins Lyle and Lowell Pettibone, living one life in shifts for twenty years; a pirate radio is their handoff | Two of a Kind · One Life, Shared · Talk to Yourself |
| IV | Cancer — home, shell, mothering | The Mystery of the Crab Pot Ghost | King Salmon, Fields Landing, Buhne Point | Ione Sorensen, 78, living secretly aboard her late husband's crab boat and feeding neighbors behind on rent | Home Port · The Last Haul · Moored in Tomorrow |
| V | Leo — pride, the spotlight, a generous heart | The Mystery of the Midnight Mane | Old Town Eureka, the (invented) Bellwether Palace | Ronnie "Lady Mane" Delacroix, 71, the shadow cast's lead from 1981 to 2009, retired "for younger legs" | Long Live the Queen · One More Saturday · The Reel From Next Year |
| VI | Virgo — meticulous service | The Mystery of the Virgin Sacrifice | Ridges above Scotia and Rio Dell | The Sisters of the Understory, robed volunteer surveyors measuring the last uncut ("virgin timber") grove before an invented land company can log it | Every Tree Counted · One Tree Saved · The Ring for Next Year |
| VII | Libra — balance, fairness | The Mystery of the Midnight Magistrate | Ferndale cemetery and Main Street | Wendell Ames, retired mediator, holding ghost court over a sixty-year fence-and-pie feud | Court Adjourned · A Fair Split · The Scales Tip Forward |
| VIII | Scorpio — secrets, death and rebirth | The Mystery of Murder Mountain | Alderpoint and the ridges above the Eel | The Crow Man is Reyna Pell, guarding the clearing where her father Gus (alive, with dementia, in Fortuna) buried letters to her; the crows mourn a death that hasn't happened yet | The Crows Remember · Let It Stay Buried · A Murder, Adjourned |
| IX | Sagittarius — freedom, philosophy, travel | The Mystery of the Wandering Arrows | Lost Coast: Shelter Cove, Black Sands, Petrolia, King Range | Dr. Wren Okonkwo-Barlow, ex-philosophy professor turned backcountry trail angel on her horse Socrates | Follow the Arrow · The Rider Moves On · The Trail That Isn't There Yet |
| X | Capricorn — duty, the climb | The Mystery of the Sea-Goat of Samoa | Samoa Peninsula, the old pulp mill and pier | Marisol Keough, marine biologist and the last foreman's daughter, in a goat-fish costume guarding eelgrass plots from scrap thieves | The Climb · The Whistle Stops · Half of Something New |
| XI | Aquarius — eccentric, communal, futurist | The Mystery of the Midnight Water Bearer | Blue Lake, Korbel, Highway 299 | Saff Gutierrez, 58, commune kid turned off-grid hydrologist leaving dated jugs where wells will fail | Water for Everyone · The Jugs Stop Coming · Contact |
| XII | Pisces — dreams, escape, two fish | The Mystery of the Two-Tailed Mermaid | Moonstone Beach, Little River mouth, Clam Beach | Coral Venn, a glasswalker and fire juggler presumed drowned, living at the river mouth and singing to the seals | Both Tails · Let Her Swim · The Other Current |

Totals: 84 playable scenes, 36 Real Endings, ~42,000 words.

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

## Follow-ups (not in this change)

- Playbook Manager: list mystery scenes alongside beats and encounters so they can be edited live.
- Scene and outcome art for the 84 mystery scenes (only the twelve card faces are queued).
- Editorial read of all twelve cases by Silas; balance check of the true-path rate after real play.
