# Prom of Doom: One Identity, Three Contexts, Evolution and Heel Turns

**Directive:** Silas, 2026-10-26 PT, superseded where inconsistent by the 2026-10-28 PT single-name revision. **Status:** canonical expansion of the [30-day DESIGN-BRIEF](DESIGN-BRIEF.md), not completion of its runtime/quest/art/QA gates. The paired Kind Robots runtime catalogue is `utils/cometAcademy/identityArcs.json`.

## Canonical revision: one permanent name, three story splashes (2026-10-28 PT)

**48 distinct people, not 144 characters.** Every origin × affinity combination maps to exactly one stable person, one codename, one recognizable anatomy/face/silhouette and one canonical look. For example, Granny Mayhem is **always Granny Mayhem** whether the story casts her as protagonist, sidekick/partner or villainous opponent. Do not create Hotplate/Backdraft/Flashpoint as three independently named identities for one person; Dez Okafor's sole superhero name is **Backdraft** across roles. Old variant names in git history are retired presentation labels, not save keys.

**Three different splash pages per person are still required:** (a) rookie/sidekick life, (b) self-directed heroic intervention, (c) antagonist/heel circumstances. Each is an original scene and composition with the **same character model**, not a new costume, codename or unrelated anatomy. 48 people × 3 contexts = 144 illustrated *scenes*, never 144 different character designs. The existing stable art keys `identities/<signature>/student|hero|villain` are preserved for compatibility, but their suffixes now mean narrative context; do not report three rendered character identities. Optional additional emotion/injury/quest art still counts separately, with rendered/exported/verified evidence.

Hero, rogue, ally, romance, sidekick and villain routes may change methods, stats, alliances, moral agency, consequences and dialogue, but never **who that person is called**. The player chooses a role and writes a history, not a new superhero. Keep the six origins × eight affinities, relationships, heel-turn/antagonist variety, forty-eight existing biographies, unique face/body variety, saved signatures and Yearbook records. The former mandatory **288 six-track** quantity is **revoked** as a content budget; author however many substantive unique scenes and alternative methods each person and relationship actually needs, proving accessibility via seeded tests. Cross-project guests retain their prior canonical identities until reconciled with their source games.

**Night patrol revision:** first two nights open with the protagonist talking alone on patrol; night three brings two simultaneous catastrophes and a friend who joins the roster by phone. The player chooses to split coverage or combine forces for one exceptional rescue with a second explicit refusal consequence. Afterward night patrol grows gradually alongside earned contacts. See Kind Robots #4402 / #4404.

## Origin × Affinity (canonical selection, Silas 2026-10-26 PT)

Silas replaced the old **Form × Affinity** picker (Impact/Arc/Veil/Step/Weave/Beacon × Fire/Ice/Storm/Stone/Light/Shadow/Bloom/Gravity) because it described attack shapes rather than people. Player creation is now:

- **Origin** (where the power came from, 6): Freak Accident, Mutant, Tech, Magic, Alien / Dimensional, Psychic.
- **Affinity** (what the power answers to, 8): Fire, Air, Earth, Water, Discipline, Genius, Birthright, Social.

6 × 8 = **48 people**, signature IDs `<origin>-<affinity>` (e.g. `accident-fire` = Dez Okafor, superhero **Backdraft** throughout). Each person has **student/sidekick, hero and villain story contexts**, and each persona carries its own `focus` (one of 17 play styles: brawler, blaster, speedster, acrobat, duelist, tank, controller, infiltrator, mastermind, gadgeteer, healer, face, summoner, shapeshifter, mentalist, trickster, commander) and its own six stats (Might, Speed, Smarts, Heart, Control, Grit; 1–5 each; students total 12–16, heroes and villains 18–23). The 48 do **not** share motifs by origin or affinity, and a villain is expected to abandon the hero's toolkit rather than reskin it: the runtime test requires hero ≠ villain stats for every person and a different focus for at least 36 of 48.

The student persona's strongest stat sets the run's field skill (Might→kinetic, Speed→spatial, Smarts→technopathy, Heart→empathy, Control→elemental, Grit→biotech), so origin and affinity choices change dispatch odds, and dispatch cards now say which stat a call needs.

**Save continuity:** the 48 pre-redesign `form-element` IDs map one-to-one onto new people (`impact→accident`, `arc→magic`, `veil→psychic`, `step→alien`, `weave→tech`, `beacon→mutant`; `fire→fire`, `ice→water`, `storm→air`, `stone→earth`, `light→genius`, `shadow→social`, `bloom→birthright`, `gravity→discipline`). An old `comet-city-academy-slice-v1` save restores as that new person with a recomputed field skill. The old names (Flaming Fists, Ari Nadir and so on) are retired. Older art requests in `art/COMPOSITE-POWERS-ROUND-1.yaml` and `content/COMPOSITE-POWERS-ROUND-1.json` describe the retired forms/elements and are superseded for any future ArtJobs.

Runtime source: Kind Robots `utils/cometAcademy/specialPowers.json` (origins, affinities, vows, powers, legacy map) and `utils/cometAcademy/identityArcs.json` (48 people with personas, stats, quests and bonds; the old `identityLives.json` is merged in).

## Premise: choose potential, live into identity

Each combination of **origin + affinity** selects a *person*, not merely an attack move. Every person has three different **narrative contexts and art splashes** (student/sidekick, hero and antagonist), while one immutable superhero name and recognizable physical design connect them. Their methods, relationships, social position, dialogue, quests and ending consequences can differ across contexts. A heroic identity may use acrobatics while its villain incarnation prefers a powered suit, laboratories or coercion. Shared origin is a narrative through-line, **not a demand for compatible ability kits**.

The playable prototype uses 6 origins × 8 affinities = **48 signature IDs** and separately records one of three vows. Its 48-person catalogue is in Kind Robots; those 48 identities are *original candidates*, not evidence of 48 finished six-path quest graphs. Pre-redesign saves migrate through the explicit legacy map above rather than being thrown away. The requested **Animal + Technical Training → Zuzu, Koala Samurai** remains a visiting guest outside the 48 (Zuzu's natural fit would be Alien / Dimensional × Discipline, but that slot belongs to Raxa Vel; do not overwrite either without cross-project reconciliation). A 48-or-so count is flexible; content quality and compatibility win.

### Required identity model (all 48+ characters)

- `signatureId`, `studentId`, stable identity/person ID, name/pronouns and adult consent/boundaries. NPC and protagonist use the **same underlying person**, regardless of viewpoint.
- `student`: same codename, novice kit, insecurity, early field mistakes and at least one mentoring/partner scene.
- `hero`: same codename and body, evolved specialty, ethical compromise, civilian cost, signature victory and hero epilogue.
- `villain`: same codename and recognizable body, different choices/tactics, intelligible motivation, accomplice network, counterplay and villain epilogue.
- `relationship`: platonic partner path, optional consensual romance path, rivalry, break-up, loyalty and defection conditions. **Romance is not mandatory for evolution.** Relationship quests can precipitate a hero or villain choice; agency must remain with the person whose identity is evolving.
- `quests`: **six authored tracks minimum** per character: protagonist in student/hero/villain mode, antagonist in student/hero/villain mode. Each track needs a setup, escalating choice, differentiated success/mixed/failure/refusal consequences, culmination, and at least one relationship/sidekick callback. Protagonist routes are playable with meaningful agency; antagonist routes aren't merely the protagonist text with pronouns inverted.
- `art`: consistent student, hero, villain character turnarounds and full-body splashes; role-specific emotional portraits including injury; evolution cinematics, relationship beats and consequence/finale plates. Track request, queued, rendered, delivered and verified separately; placeholders do not fulfill this obligation.

48 × 3 contexts = **144 story splash pages** using only **48 underlying character designs**. The former 288-track floor is retired; branching scene quality, replay reachability and personal consequences govern production, not a claim that these are implemented.

## State machine and pacing

1. **Initial enrollment:** the title shows only New Game / Yearbook / Settings / Tutorial, then separate illustrated origin and affinity stages, a collectible six-stat identity trading card, three story promises, confirmation and tutorial. A first-time player starts as student/sidekick. Previously *earned* hero and villain identities are selectable for real New Game Plus runs, but remain locked otherwise; permanent Yearbook discoveries survive new runs. Origin/affinity selects future potential. The third selection (current vow) should express an intention, never lock future faction or identity. Show the three possible identities as **potential futures**, with silhouettes or spoiler-safe names depending on scrapbook discovery.
2. **Bond acts (days 1–14):** meet classmates naturally, patrol together, grow trust and discover nontrivial friction. Partnership requires agreements about duty and methods. Romantic scenes require independent consent, boundaries, and mutual choice. Student identity has its own useful powers and content, so delaying transformation remains valid.
3. **First break (days 15–21):** earned crisis, active quest flags and relationship history open transformation choices. A person can embrace heroism, pursue villainy, or remain an independent sidekick/rogue; no irreversible promotion from one dialogue option or numeric affinity threshold.
4. **Reckoning (days 22–28):** heroic or villainous transformations have dedicated training/costumes, revised mission odds and follower availability, competing factions, changed partner/romance dialogue and counterquests. Defection or heel turn updates the roster, mission board, city map, and friendship consequences. Former partners are allowed to mourn or disagree rather than instantly forgiving.
5. **Prom (days 29–30):** identities, relationships, and betrayal alter the opponent's actual plan, ally resources, possible turnarounds and endings. Keep existing 12 core ending floors, but add character-specific role/vow/partner epilogues, not 144 interchangeable name substitutions. A villain identity may be redeemed at cost or remain a compelling antagonist.

**No arbitrary alignment toggle.** Transformation prerequisites must be legible: completed personal quests, actionable evidence, values under pressure, agreement with a mentor/partner (when applicable), public actions, and civilian consequences. A role change alters gameplay, resources, risks, enemy counters and authored dialogue, not simply a label.

## Signature villain henchmen (2026-10-29 PT)

Each of the **48 permanent villains** has one original *named one-hit henchman breed*, with its own named spokesperson, appearance, telegraphed battlefield move, counterplay and personal loyalty fault line. Read the 48-row [Villain Henchman Bestiary](VILLAIN-HENCHMEN.md) and its linked Kind Robots `utils/cometAcademy/villainHenchmen.json`, indexed by the exact, stable `signature`. This is **one henchman family per existing villain**, **not** a fourth playable form or 48 new origin/affinity heroes. The same association is used by Every Villain Tactics.

Common henchmen are one-hit *routs, stuns or disarms*, not automatic death scenes. Their species and named representative should carry agency and can switch allegiances; the primary mastermind's at least two independently motivated, persistent accomplices are a different narrative layer and still mandatory. New ArtJobs, actual `SPECIES` Facet records, playable patrol deployments and tactical special moves have **not** been delivered merely by the authored catalogue.

## Guaranteed heel turn without fake choice

**Every full 30-day run has at least one real heel turn.** Seed-select from a pool of **at least four authored candidates** with different motives, dates, evidence trails and faction triggers. The betrayal must be foreshadowed and change at least one mission, rescue, social relationship and climax option. Avoid cheap reveal-only twists.

Player actions may expose, soften, prevent *one candidate's* betrayal, negotiate terms or facilitate redemption. If one is prevented, another genuine independently prepared turn remains eligible; do not silently force a specific friend to betray contrary to every scene. Make the betrayal auditable in a seeded transcript and log **who**, **when**, **why**, **what shifted**, **who knew**, and **whether the player could act**. The player's own heel turn is optional and cannot count as the sole guarantee.

The primary threat must have **evil accomplices**, plural: at least two independently motivated, active henchpeople per selected mastermind arc. They can pursue conflicting agendas, seek romance or partnership only with real consent, double-cross their boss, be negotiated with or refuse coercion. Their victory conditions and methods need not match their patron's abilities. A defeated mastermind does not make their accomplices vanish from the story.

## Six-track authoring template

For every entry in the [48-person runtime identity register](https://github.com/silasfelinus/kind_robots/blob/main/utils/cometAcademy/identityArcs.json), write **separate** narrative beats for:

| Role | Protagonist arc | Antagonist arc |
| --- | --- | --- |
| Student / sidekick | Learn the flaw, choose a mentor or partner, make first independent decision | Rival helps or undermines a case, hints at hidden motive, can be recruited or challenged |
| Hero | Claim heroic name and specialty, pay a public price, face a personal counter | Hero's sincere protective goal obstructs the player, with diplomacy and counterplay |
| Villain | Discover new method and accomplices, seize or redirect an unjust system, decide what price to impose | Opposing villain pursues a specific destructive plan, threatens something personal, permits several earned defeats |

Add relationship-specific variants to each track, including non-romantic equivalents. A character can be the player's romantic partner *and* oppose them ethically. Sidekick loyalty cannot be bought with affection. Where triads exist, each adult must affirm independently and can withdraw without mechanical punishment.

### Example: Animal × Technical Training

- **Student:** Zuzu, a promising koala student whose precision and mechanical curiosity outpace judgment. The name **Zuzu** belongs to this individual, not to the power mechanic.
- **Hero:** **Zuzu, Koala Samurai**. Distinct sword form, disciplined acrobatics and ritual promises; must decide whether saving an opponent violates a mentor's doctrine.
- **Villain possibility:** a mechanically augmented duelist with a new name and evolving exosuit. The later choice can privilege mechanical intelligence over physical swordsmanship, with separate vulnerabilities and allies. Do not overwrite existing Zuzu canon without explicit cross-project reconciliation.
- **From protagonist:** train with a rival, reconcile an old oath, choose a method of saving a classmate.
- **From antagonist:** confront the hero's restraint or the villain's exosuit surveillance; distinguish sympathetic motives from acceptable conduct.
- **Partner/romance:** the key test is whether a partner may openly disagree with the oath; romance is optional, trust is not a stat gate.

### Example: the Frogman divergence

- **Student:** an ambitious amphibian-themed junior rescuer, best at fast rooftop movement.
- **Hero:** **The Incredible Frogman**, spring-loaded acrobatic rescues, improvisation and commitment to vulnerable bystanders.
- **Villain:** **Evil Dr. Frog**, who abandons acrobatics for an engineered supersuit, ruthless intelligence and a laboratory-centered plot. This is *not* merely a green palette swap or a stronger version of a jump.
- **Protagonist/antagonist variants:** the player may use Frogman's rescue routes or unmask Dr. Frog's false clinical trials. As an NPC adversary, the two identities create fundamentally different obstacles. A colleague can defect from Dr. Frog's lab after seeing the cost.

## Verified crossover continuity (2026-10-26 PT)

**The 48 origin/affinity people are the main roster**, and existing `comet-city-academy-slice-v1` saves migrate onto them. The two requested guests are **additional people**, not aliases replacing an existing power combination. Their prospective special patterns, Animal + Technical Training and Stellar Navigation, must be introduced as additive selectable power families only after save-safe runtime taxonomy work; the current first-week game initially hosts them as visiting NPCs.

- **Zuzu** comes from the anthropomorphic weird-west Zuzu world. Dimensional displacement through an unstable Comet City gate makes him a genuine visitor, not a Comet City native retroactively given his name. He arrives with his assassin training and his original oath; in Comet City his chosen hero codename is **Zuzu, Koala Assassin**, while **Koala Samurai** remains an earlier/home-world heroic interpretation rather than a different civilian. **Shogun Null** is a *possible* villainous heel personality using stolen dimensional targeting and a mechanized exosuit. Never presume the player can force his turn by buying a warrant.
- **Tess Helio** is the established navigator from **This Means Warp** (Kind Robots `utils/gameOfCaptains/crewAssignments.ts`, crew ID `tess`). She has a grandmother's secret map of drifting safe harbors; her origin, name, pronouns and crew duty must match the source. Comet City aliases: visiting student **Starling**, heroic **Starwake**, potential heel **The Void Cartographer**. Her choice between protecting refugees and controlling routes may evolve, but the academy cannot quietly rewrite her ship or her independence.

Neither visitor can be made a villain by a single player's selfish response: their actual heel transformations require their own authored ethical crisis, choices and consequences. These guest arrivals also cannot stand in for the required independent, foreshadowed full-run NPC betrayal.

Their first-week arrival cases and choice callbacks live in Kind Robots `utils/cometAcademy/rules.ts` and the named source `utils/cometAcademy/guestIdentities.ts`. They have civilian backstories, distinct student/hero/villain aliases, protagonist and NPC hooks, independent platonic/sidekick/partner/optional adult-romance paths, and projected ally/heel consequences. **These are initial scenes and previews**, not six completed playable tracks or production art. They do not satisfy the 30-day evolution graph or guaranteed seeded heel-turn requirement. The main 48 also have original civilian real names, pronouns and backstories in `identityArcs.json`, shared by every viewpoint and moral role. The role-specific story lenses are **authored seeds**, not the full 288 questlines.

**Next integration gates:** preserve cross-project names, author Zuzu and Tess as full six-track guest quest graphs alongside the 48, add non-romantic hero/villain transformation decisions and NPC agency, provide real Krea 2 → Arthemy ArtJob provenance for three costumes and multiple emotion/injury states, then prove with real 30-day seeded playtraces that each can be a partner, ally or adversary independently of romance.

## Implementation and adversarial acceptance

**Historical initial scaffold (superseded 2026-10-28):** runtime originally had 48 distinct student/hero/villain aliases, divergent methods, one personal conflict, a protagonist hook, antagonist hook and partner decision per signature, plus a typed lookup, selection preview, first-week simulated ending foreshadow, and catalogue tests. This is **not** the completed 288 quest-track engine, heel-turn director or delivered art.

Continue with sequenced slices:

1. ~~Extend the taxonomy with safe migration~~ Done 2026-10-26 as Origin × Affinity with per-persona focus and stats (old `comet-city-academy-slice-v1` saves migrate). Still open: persist stable person ID and role history, and reconcile Zuzu/Tess as selectable guests.
2. Author the first **six full six-track** playable character arcs, two heel-turn candidates and two accomplice plots; wire meaningful companion/romance/partner quest state and evolution gates into the actual day/night engine.
3. Add four or more betrayal candidates, guarantee a seeded heel turn, validate prevention/redemption and antagonist recasting.
4. Expand to 48 six-track graphs with authored outcomes, art prompt IDs, requested/rendered/delivered/verified assets and scrapbook unlocks.
5. Seeded adversarial whole-run tests must prove both hero/villain methods work, villain kit is not just hero + damage, romance never gates rescue, heel turn always happens without contradicting player agency, accomplices stay active, every arc is reachable from a clean start, saves migrate, and real images show at all relevant states.

**Human gate:** only after the full 30-day narrative, this roster, authored art, every ending graph and adversarial checks are complete. Do not call the player identity preview final-game delivery.
