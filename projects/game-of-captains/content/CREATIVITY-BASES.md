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

## Discovery without frustration

- Encounter opportunities ride alongside **existing** chapters, expedition side routes, planetary/casino/Serendipity beats and late-game anomalies. One discovery opportunity per chapter is the pilot cap, not a mandatory menu before progression.
- Rarities change *which* creatures appear, not whether the player is allowed to have fun. Rare creatures should have hints, a soft guaranteed revisit path and no permanently missable encounter.
- Collection persists across voyages; a new run must not reset the scrapbook. The initial implementation follows the game's existing device-local persistence pattern, and account-bound multi-device syncing remains separate work before release.
- A milestone at **5, 12, 25, 50, 75 and 100** recorded species causes a fresh absurd incident that changes how the galaxy reacts to a conspicuously zoological red couch. It must be *played* as a new encounter and not only as a static achievement toast.
- The last undiscovered alien must remain guaranteed findable; no impossible limited-time RNG unlocks.

## Final authoring and balance review

Audit the three choices for comedic contrast, not moral purity. Test avoiding every alien, chasing rare creatures, meeting each milestone, resetting voyages, saving/loading, limited storage, mobile/desktop gallery reachability, slow/failing ArtJobs and giant images. Verify real rendered splash IDs and in-browser URL access. Keep t-012 final human acceptance and public release separate.

**Status contract:** 101 authored descriptions and 101 queued prompts are not proof of 101 pictures; no image counts toward completion until its ArtJob is DONE, the final ArtImage exists, it is shown on the signed-in scrapbook and its crop has been checked.
