# Editorial verdict — writing and coverage (t-092)

2026-11-21. Inputs: `report-2026-11-21.json` (kind_robots
`utils/scripts/reportCthulhuquariumCoverage.ts`), and an independent read of
canon `story/scenes.yaml`, `story/barks.yaml`, `characters/*.yaml` and the
player-facing text of all 151 fish by a reviewer given only the canon and the
rules, not this session's conclusions.

## Coverage

All of it is reachable from live code:

| Content | Count | Detail |
|---|---|---|
| Scenes | 23 | 12 player replies |
| Bark pools | 15 | 109 lines |
| Backgrounds | 16 | |
| Species | 151 | 32 / 41 / 36 / 25 / 17 by floor |

The script walker covers 31 complete scene paths. The previously unused
`upgrades` bark pool now speaks on the upgrades shelf. The `sets` and `decor`
pools are bound to their screens.

## Rule verdicts, and what changed

Fixed in canon #85.

| Rule | Verdict before | Fix |
|---|---|---|
| Outside never shown, named or explained | Issues | The town and the street were named in five fish texts, and one line drew attention to the Outside. All rewritten so the building is the whole world. |
| No hint at the finale | Issues | Eight winks removed. They were about being kept or watched, a person kept in a tank, the motto "everything out is in", and a nod to the book the names come from. |
| Wilbur never mentions injuries or is the joke | Pass | No line mentions an injury. Two neutral lines used the `wince` portrait, so the plaster became the visual beat; those now use `explaining`. The kind_robots injury lint passes on 200 spoken lines. |
| Authored text only | Pass | No placeholders, TODOs or template tokens. |
| No breeding, eggs or hatching as mechanics | Issues | A bark, a fish voice and the Hatchery line are reworded. The canon `evolution_kind: breeding` is data only and is never shown to the player. |
| Clear descent | Mostly pass | Wilbur's trust arc lands floor by floor, and the fish get weirder by tier. The floor-opening scenes no longer state the species count aloud, because keys can now be bought later. Floor V's "there is no key" now agrees with buying it. |

The edit also fixed:
- two contradictions: who has been to the far end, and Charlotte having "grown up down there";
- a repeated rare-event line in the finale;
- a phrase in Charlotte's voice that Wilbur spoke;
- small grammar fixes.

## Left for the playtest

- When the book completes, `bestiary_complete` (Wilbur) and
  `milestone_bestiary_151` (Charlotte) play back to back. They read as one
  closing exchange now that the second no longer repeats the first. Watch
  whether testers find the double close too long.
- Two side backgrounds blur the floors' identities: the Wreck on Below Stairs
  and the Opera House at the Bottom. That's a design choice, so it's noted here
  rather than changed.
