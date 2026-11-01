# Space Couch creativity bases: every new system should be worth laughing at

**Authority:** Silas, 2026-11-01 PT. The following is reusable creative direction for the whole Space Couch experience, not a production status report or human design approval. The 101-species issue is [kind_robots #4592](https://github.com/silasfelinus/kind_robots/issues/4592).

## Three choices, three distinctly different stories

A weird alien encounter should be a **three-choice scene**, not an inventory-management exercise or seven-button dialogue wheel. Example: **make a ridiculous mistake (chaos), try to play it cool (alien flees), become its improbable best friend.** At least two options can count as *documenting* the species. No option should permanently ruin a rare collectible or punish a player with missed content forever.

Create genuine consequences, not three synonyms for "Observe": a heartfelt outcome, an absurd disaster, and a near miss are better than six shades of reasonable. Let the joke escalate without flattening the residents or mistaking coercion for friendship. The bestiary is absurd ecology, not a collection of servants. Friendship requires an offer and a response, not a high stat roll.

## 101 living creatures, not 101 palette swaps

The authored species and art keys are in `utils/gameOfCaptains/alienSpecies.ts`; the new private art job ledger is `art/ALIEN-SCRAPBOOK-101-ROUND-1.yaml`.

| Creative starting point | Count |
| --- | ---: |
| Zodiac creatures that mix celestial signs and Earth animals | 12 |
| Two-animal hybrids with readable silhouettes | 24 |
| Cosmic-phenomenon animal mashups | 20 |
| Emotional, social, gently absurd animals | 20 |
| Predator, prey, colony, symbiosis and multi-generational ecology | 15 |
| Impossible and legendary lifeforms, including elders and hatchlings | 10 |
| **Total** | **101** |

Deliberately vary body size, life stage, palette, social structure, movement, predation, sentience and habitat. Avoid making every species a paper-pushing bureaucrat with a clever species name, or copying terrestrial species without metamorphosis. Give each one a silhouette, an independently funny ecological behavior, a field-note reveal, and an image-keyed large splash. No collage and no lettering in art. The long red upholstered space couch and its invisible safety bubble remain recurring canonical props in contextual images, not mandatory clutter inside every creature portrait.

## Emotional rock-paper-scissors, not outcome shopping

**Three player-visible *actions*, three hidden results, three legible emotional situations.**
The same action must be able to create a friendship, a ridiculous incident, or a retreat depending on the creature's cues. Do not title a button "Run Away," "Guarantee Friendship," "Record Alien," or "Chaos." The player chooses how the couch behaves; the alien chooses its response.

| Creature's present state | Peaceful greeting | Quiet observation | Ridiculous improvisation |
| --- | --- | --- | --- |
| Wary or overwhelmed | Retreats from too much proximity | Chooses to approach and bond | Chaos, documented |
| Playful or attention-seeking | Bonds through play | Unintended public spectacle, documented | Overwhelmed and retreats |
| Protective or defensive | Intrusion triggers chaos, documented | Feels watched, retreats | A compassionate distraction creates trust |

This is a balanced three-by-three design: every emotional state gives one bond, one chaotic record, and one escape; every player tactic can yield all three across situations. **The emotional clue is readable but not an outcome label.** Make it a fair interpretation, not hidden dice behind a decorative question.

### Buried information is part of the play

Never print the emotional state as a label or announce the optimal answer. The player should find *evidence*, not instructions: a dropped object, a repeated invitation, something guarded from danger, a change of rhythm or light, an ecological detail the field guide mentioned several scenes earlier. Each of six creature families needs distinct environmental versions of all three emotional situations. Favor two modest clues over a sentence such as "a quiet pause seems to calm it," which solves the scene for the player.

The player's history is meaningful: after contact, record the observed environmental tell, the action chosen, and the actual result in a **captain's marginalia** scrapbook entry. A later sighting can quote a previous observation from the same creature family, but it must *not* automatically match the current emotional state. The point is analogy and attentive reading, not the UI selecting the correct option.

A careful reader should do better than random selection without needing an encyclopedic memory. The clues should be consistent and fair, not arbitrary mood dice disguised as a narrative. Failed guesses remain funny, recoverable, and worthy of a ship-log anecdote. Test that all eighteen category-by-emotion cue sets are genuinely different and that prior observations persist through save/restore.

Consequences must extend beyond a sentence: a friendship lives in the scrapbook and can prompt a later callback; chaos becomes an embellished captain's-log incident and can change later first-contact rumors; retreat still informs a next encounter and must not make that species impossible to obtain. Do not tie a free optional collector encounter to unrecoverable ship damage, death, or mandatory mission failure. Every creature's field note, habitat and social situation should influence setup and aftermath; avoid the same generalized gag 101 times.

## Discovery without frustration

- Encounter opportunities ride alongside **existing** chapters, expedition side routes, planetary/casino/Serendipity beats and late-game anomalies. One discovery opportunity per chapter is the pilot cap, not a mandatory menu before progression.
- Rarities change *which* creatures appear, not whether the player is allowed to have fun. Rare creatures should have hints, a soft guaranteed revisit path and no permanently missable encounter.
- Collection persists across voyages; a new run must not reset the scrapbook. The initial implementation follows the game's existing device-local persistence pattern, and account-bound multi-device syncing remains separate work before release.
- A milestone at **5, 12, 25, 50, 75 and 100** recorded species causes a fresh absurd incident that changes how the galaxy reacts to a conspicuously zoological red couch. It must be *played* as a new encounter and not only as a static achievement toast.
- The last undiscovered alien must remain guaranteed findable; no impossible limited-time RNG unlocks.

## Final authoring and balance review

Audit the three choices for comedic contrast, not moral purity. Test avoiding every alien, chasing rare creatures, meeting each milestone, resetting voyages, saving/loading, limited storage, mobile/desktop gallery reachability, slow/failing ArtJobs and giant images. Verify real rendered splash IDs and in-browser URL access. Keep t-012 final human acceptance and public release separate.

**Status contract:** 101 authored descriptions and 101 queued prompts are not proof of 101 pictures; no image counts toward completion until its ArtJob is DONE, the final ArtImage exists, it is shown on the signed-in scrapbook and its crop has been checked.
