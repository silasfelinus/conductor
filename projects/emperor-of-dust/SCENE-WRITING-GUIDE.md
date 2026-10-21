# Emperor of Dust: writing throne-room scenes (visual-novel pass)

Silas's brief (2026-10-20 PT): *"Make sure all paths are interesting and unique, engaging conflicts and
challenging teetering of influences. An engaging visual novel style (but more verbose), where the reader
is often asked to make interesting choices that question morality."*

The engine now supports **multi-beat audience scenes**. Your job is to turn your act's throne-room
audiences from two-line petitions into scenes worth reading, and to make the choices hurt.

## Image-led narrative standard (Silas, 2026-10-21 PT)

The work is not complete when prose exists. **Polish the writing first**, then create private,
scene-specific render requests in `art/AUDIENCES-ROUND-*.yaml` or the matching quest/talk ledger.
Illustrate the choice's concrete physical consequence rather than a second interchangeable
portrait. Cover quest notice, triumph/success, partial/failure, and neglected/expired results,
plus important audience probes, endings, and follower conversations. The same image cannot
stand in for outcomes that tell opposing stories. Log requested, ArtJob queued, image rendered,
editorially accepted, exported, and used in the game as separate states.

**Species and naming are separate layers of canon.** Every visible resident is an identifiable,
upright anthropomorphic animal, clothed and acting in this wasteland society. State the exact
canon species and physical description in positive image prompts, especially for named cast;
do not assume the image model infers an animal body from a character's name. Named individuals
usually carry personal names (Mara Reedbell, Marisol Tallow, Rook Bramble, Sister Reedlight),
not animal labels. Explicit existing exceptions include Young Komodo and the Storm Crows'
faction name. An unnamed passerby may be described by species and role, but a named individual
must not be rebranded "the Fox" or "Rabbit Captain" in prose or art metadata.

Read `NPCS-V03.md`, `FOLLOWERS-V03.md` and the Book One cast picks before rendering.
Preserve species, relationships and **first-appearance chronology** across quests, talks and
artwork. Do not show a major NPC in an early quest epilogue before that character is introduced.
Young Komodo's friendly early design should never pre-signal betrayal. The Abbess uses her
locked sea-otter reference. Species never determines guilt, kindness or allegiance.

For Arthemy, describe objects, gestures, animal faces, light and atmosphere affirmatively.
Avoid forbidden positive prompt terms from the Zuzu video guardrails and model-literal
traps (for instance "duster", "muzzle", "squat"). Keep text, letters and logos in the
negative field. Render requests stay private until art review and the separate public release
gate. A submitted prompt is not a rendered image, and a rendered image is not yet a game asset.

## Prose style (Silas, 2026-10-20 PT, overrides anything softer below)
*"We want crisp stark prose. Stephen King or his son Joe Hill, Lone Wolf and Cub."*

- **Stark.** Short declarative sentences. Concrete nouns, hard verbs. Cut adverbs, cut "very", cut "seems
  to", cut "something like". One precise detail beats three pretty ones. White space is a weapon: a
  one-line paragraph after a long one lands like a blade.
- **King / Hill:** plain, colloquial, specific. Ordinary objects carry the dread (a ladle, a chalk mark,
  a child's shoe on the wrong side of a door). People talk like people: interrupted, practical, funny
  when they're scared. Let a voice run on when it's nervous, then stop dead. Horror comes from the
  mundane going slightly wrong, never from adjectives like "eerie" or "sinister".
- **Lone Wolf and Cub:** laconic, honor-bound, fatalistic. Silence does the talking. A choice is a
  road, and every road has a price paid in someone's body or someone's name. No speeches about
  morality; the consequence is shown and left there. Weather, dust and road as stage. Violence is
  sudden, brief and offscreen; its aftermath is shown plainly.
- **No purple.** No "lovely", "gentle", "a little too", "something sweeter underneath", stacked
  similes, or ending lines that explain their own meaning. Never wink. Trust the reader.
- **Length still matters.** The brief is still a verbose visual novel: give scenes room, but earn every
  line. More beats and more hard choices, not more decoration.
- Responses: one to three short sentences. The last sentence is the cut.

Example (before → after):
- Before: "Sister Reedlight looks down at her lantern as if noticing it for the first time, and laughs, and the laugh is lovely."
- After: "Sister Reedlight looks at the lantern. Then she laughs. It is a good laugh. You don’t trust it."

## Story calls are yours (Silas, 2026-10-21 PT)

"I'm not versed enough in the story beats to answer the impact of that choice. Make decisions
with emotional weight." Do not leave a story or design question open for Silas. Decide it: prefer
the version whose cost lands on a named person the player has met over one that lands on a number.
Write the call and its reasoning in your PR body. Secrets, publishing and irreversible operations
are still gates.

## Read first (skim, then keep open)
- `/home/user/conductor/projects/emperor-of-dust/GAME-BIBLE.md` (premise, tone, faction bible; v0.3 wins where they disagree)
- `/home/user/conductor/projects/emperor-of-dust/SYSTEMS-V03.md` (factions, Komodo and the betrayal, hideout)
- `/home/user/conductor/projects/emperor-of-dust/DAY-PLAN.md` (your act's anchors)
- `/home/user/conductor/projects/emperor-of-dust/NPCS-V03.md` and `FOLLOWERS-V03.md` (voices, secrets, canon guardrails)
- `/home/user/kind_robots/utils/emperorOfDust/fortress/types.ts` (`AudienceDef`, `AudienceBeat`, `AudienceOption`, `SceneLine`, `Requirement`, `Effects`)
- **The exemplar: Day 1 in `/home/user/kind_robots/utils/emperorOfDust/fortress/actOne.ts`** (audiences `d01-aqueduct`, `d01-toll`, `d01-mirefen`). Match its register, length and structure.

## The data shape
```ts
{
  id, title, speaker, npc?, faction?,
  lines: SceneLine[],           // string = the speaker or narration; { who, npc?, text } = someone else speaks
  options: AudienceOption[],    // option.next = id of a beat in this audience; no next = the scene closes
  beats?: AudienceBeat[],       // { id, speaker?, npc?, lines, options }
  requires?: Requirement,       // the audience only appears when this holds (flags / notFlags / affinity ...)
}
```
Every answer applies its `effects` (and `requires.cost`) immediately and leaves a flag `chose:<audienceId>:<optionId>`.
A scene closes when an option without `next` is chosen. If the day ends mid-scene the scene simply closes.

## Hard rules (the contract test enforces most of them)
1. **Edit only your assigned file.** No git commands. No changes to engine, types, tests or other acts.
2. **Never remove or rename** an existing audience id, option id, quest, flag, `postsQuests`, `requires` or
   `effects` of an existing option. Existing options stay in the opening `options` array with the same id,
   requires, effects and postsQuests. You MAY rewrite an existing option's `label` and `response` text for voice.
   Other code, tests and later acts depend on those ids and flags (grep `chose:<audienceId>` and flag names across
   `utils/emperorOfDust` and `utils/scripts/verifyEmperorFortress*.ts` before touching anything clever).
3. **Do not add `next` to an existing option.** Depth comes from NEW options that lead into beats.
4. Inside a beat you may re-offer existing decisive options **with the same id, requires, effects and
   postsQuests** (label/response may be reworded for the new context), alongside new paths. See Day 1.
5. Beat ids unique within the audience; option ids unique within one beat/opening; every beat reachable; no loops;
   at most 3 beats deep. Every option has a non-empty `response`.
6. **Who can speak.** Young Komodo (`npc: 'young-komodo'`) can interject freely through Day 40 (he betrays the
   throne at the Day 41 dawn; after that he is gone, and Act V's advisor is defined per day in the file).
   NPCs (slugs in `utils/emperorOfDust/fortress/npcs.ts`) can speak where they plausibly are.
   **Followers can die or be absent.** A follower may only speak in a beat reached through an option with
   `requires: { follower: 'F0xx' }` (the engine checks they are alive and at court), and the option's label should
   make clear it is their voice (e.g. "Let Saffron answer her."). Use follower ids as `npc` (e.g. `npc: 'F002'`) to
   show their art. Follower ids/names/species: `followers.ts`, `followersLate.ts`.
7. **Balance**: new options use modest numbers: brass -40..+30 (use `requires.cost` for paid solutions), affinity
   ±5..±15, local support ±1..±3. No new `recruit`, `recruitable` or `items` effects. Do not add new quests.
   New audiences are fine (callbacks, see below) but keep any day at **≤ 4 audiences**.
8. Text: curly apostrophes and quotes (’ “ ”), as the file already uses. PG-13. Darkness by implication, not gore.
   No em-dash spam. Canon guardrails: pre-Zuzu (Zuzu never appears), Hollow Bell is standing and its later fate is
   never explained, Kiyo is Zuzu's future mother (never say so), the Abbess's order works quietly.
9. Run `cd /home/user/kind_robots && npx prettier --write <your file> && npx tsx utils/scripts/verifyEmperorFortress.test.ts`
   until it prints `Emperor of Dust fortress contract: ok`. Then once, at the end:
   `npx tsx utils/scripts/verifyEmperorFortressBalance.test.ts` (slow; it plays hundreds of seeded campaigns).
   If a failure is clearly in ANOTHER act file (someone else is editing it right now), wait a minute and retry.
   If the balance test fails because of your numbers, soften them.

## What makes a scene good
- **Open in the room.** One or two lines of narration that put a body in the hall: what the petitioner carries,
  how they walk, what the court does while they talk. Then the petitioner in their own voice. 4–7 opening lines.
- **Every scene is a real dilemma.** No option is clean. The compassionate path costs something concrete (brass,
  a faction's support, a risk to someone named). The pragmatic path hurts someone specific, and the scene makes
  sure the emperor sees who. The harsh path has a defensible reason, voiced well by someone the player respects.
- **Teeter influences.** Most good choices push two factions in opposite directions. Track the local five
  (ledger, old-houses, yard, lamplight, gate-watch) as much as the kingdom ten: the court is watching the throne.
- **A probe option.** Most scenes should offer at least one way to *ask* before deciding ("Ask what the toll money
  is for", "Ask Pip what the ledger really says") that opens a beat with the hidden truth or a complication, a
  dissenting interjection, and a new path that did not exist before the question. Asking should feel rewarded,
  but the truth it reveals should make the decision harder, not easier.
- **Different speakers disagree.** Komodo is incisive and a little too comfortable with expedience; he is also,
  secretly, building toward betrayal (read his clue track in NPCS-V03.md and leave subtle tells on [K] days). NPCs
  have agendas. Let interjections argue with each other.
- **Responses land.** A closing response is 1–3 sentences that show a consequence in the room or on the road: a
  gesture, a cold letter, lights going out in the fen. Avoid summarizing effects in prose ("Hollow Bell likes you").
- **Echo earlier choices.** Use flags. A new option or audience gated on `requires: { flags: [...] }` (or
  `notFlags`) that calls back to a choice from earlier days (including Day 1's new flags: `mara-millers-levy`,
  `pack-medicine`, `pack-camp-mapped`, `mire-quiet-count`, `mire-road-closed`, and any `chose:<aud>:<opt>` flag) is
  the most valuable thing you can write: the world remembering. Aim for 2–4 callbacks in your act. New flags you
  invent must be kebab-case, prefixed with the day (`d07-...`), and listed in your report.
- **Coverage target:** every audience in your days gets a richer opening; at least two thirds of them get one or
  more beats with new morally distinct paths; add 2–4 new callback audiences or callback options across the act.
  Preserve all quests and their posting.

## Report back
A short list per day: scenes deepened, new beats, new options (with their effects in one line each), new flags,
callbacks (which earlier flag they read), and the final test output lines.
