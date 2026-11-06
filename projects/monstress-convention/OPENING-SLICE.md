# Opening Vertical Slice: The Case of the Locked Dressing Room

**Scope:** One playable 25–45 minute complete mystery tutorial in the Grand Gloaming. This document names author-visible beats, not public hints.

## Graph
`parking -> lobby -> registration -> convention hall -> hot tub courtyard`, with `lobby -> stair -> upstairs corridor -> Celestine suite`. Reception unlocks the lift; staff access lets the player bypass a locked corridor after meeting Pip. Keep the number of transitions low and icon travel immediate.

## Sequence and proof
1. Start with Iris and Nico in parking lot. Initial Look/Talk/Use prompts teach contextual verbs, a sign advertises convention timing, and both have unique observations.
2. Get a press credential. Nico can recover a forged-but-harmless fan-pass from autographs plus a clerical mistake. Iris can document a legitimate photograph commission and get official access through Marta. Both lead to the same panel but generate different witness trust flags.
3. Witness Celestine disagreeing with Odette about a contract before the panel. Celestine's line about 'afterlife residuals' works as a joke and as later evidence.
4. At the brand panel, a rolling blackout lets Odette depart along the staff hall, but the fan is seen outside the suite and looks immediately guilty. Celestine is discovered dead in her locked room. The player is not asked to solve the whole conspiracy in a tutorial.
5. Ghost appears first in a fogged bathroom mirror. She remembers bitter developer-smell, a short mechanical bell, and that she never saw who touched her. Her memory is **not** a magical lie detector.
6. Both characters may interrogate the ghost. Nico learns tabloid gossip; Iris documents that the 'bell' is the laundry lift call and finds an impossible schedule discrepancy.
7. Reconstruct the mini-timeline: photograph a service bell scratch + consult night porter call log + compare fanboy room photographs. Fan has stalked someone and should be accountable for it, but his photos prove he was elsewhere at murder time.
8. Close prototype with choice: publish an unverified allegation, keep working, or issue a cautious bulletin. All conclude a self-contained episode and unlock an ending/scene in the Playbook Kit. Subsequent full game follows the stronger evidence.

## Fail-forward cases
- Miss badge path: lobby/manager offers alternate task.
- Burn a clue during an item-combination experiment: evidence copy in notebook survives.
- Exhaust all Nico questions: switch to Iris; both have independent ways to unlock the service route.
- Accuse the fan prematurely: he flees to the parking lot and the photo timestamp can still be recovered via his camera found with consent/manager inventory. His behavior is not forgiven.
- Turn off optional adult flirtation: no puzzle progression changes.

## Data contracts to implement
`Room`, `Hotspot`, `Verb`, `Item`, `Topic`, `InterviewBranch`, `Clue`, `Puzzle`, `CaseFlag`, `CharacterPresence`, `Ending`. Each clue records two source paths. Topic key includes `actorId`, `targetId`, `topicId` and `caseStage`. Saves preserve room, selected protagonist, inventory owners, unlocked topics, exhausted branches, case flags, scene unlocks and art IDs.