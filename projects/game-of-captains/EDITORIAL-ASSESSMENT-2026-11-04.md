# Space Couch — editorial assessment, 2026-11-04 PT

Directed by Silas in-session: assess overall text quality, mission uniqueness, fun, clarity,
diversity of playthroughs and stickiness, and finish what can be finished. Measured on
kind_robots `main` at ae01754 plus the pass in kind_robots#4755.

## Method

- The existing gates: `test:game-of-captains` (all pass) and the full trace matrix
  (`--full`, 2,116 voyages, passes in 244 s).
- A scratch analysis harness built on `spaceCouchTraceHarness.ts`. It plays 240 voyages: 180
  "mixed human" drivers that lean toward one order but not exclusively (authored choices
  about 85% of the time, side quests, errands, a random finale) and 60 random walks. For
  each voyage it records the ending family, the nemesis variant, the call sequence, scene
  word counts and every sentence the player reads.
- A full read of the mission briefs and graded returns for all 30 calls, plus sampled endings.

## Scorecard

| Dimension | Score | Evidence |
| --- | --- | --- |
| Prose quality (authored scenes) | **8/10** | The brief's dry register holds: procedural, understated, with real jokes about a ridiculous premise. The 30 calls are clearly distinct premises: a sentient library with a predatory card clause, a vote counted by heat, a warranty AI that classes space as outdoor use. Before this pass, about a third of what players read was boilerplate connective text. |
| Mission uniqueness | **8/10** | 30 calls, each with its own flawless/costly/disaster return, and now its own plain success (120 distinct returns). The ethics are specific to each world, and no choice is a universal right answer. |
| Clarity | **6 → 7.5/10** | Odds, costs and fatality disclosures are on screen. The final log was one paragraph of about 650 words, with the full log printed again underneath. It now renders in labelled sections, with the raw log folded away. |
| Diversity of playthroughs | **6/10** | Mixed play reaches 12 of 18 ending families and 24 nemesis variants. But the board's default call repeats on every seed: refugees, archive and the bar appear in 100% of default voyages, and only 22 distinct nine-chapter sequences turned up in 228 voyages. The six destination families (Sanctuary Without a Map, Names on the Hull, The Unlicensed Cure, The Right to Refuse, A Table for Every Guest, The Courtesy Accord) were reached **0 times in 240 voyages**. Consistent single-order styles still lock to one ending family (an earlier finding). |
| Fun / moment-to-moment | **7/10** | The redshirt board, the three-choice alien encounters and the 101-species scrapbook carry the loop. Detour approach feedback ("For a moment it almost works.") is still generic. |
| Stickiness / replay | **6 → 7/10** | Before: only about 53% of the sentences in voyages 2–5 of a five-voyage player were new, and every voyage opened on the same transit lines. The 101-species collector takes 13–21 voyages, which is a long tail: good for a collector, and the reward ramp (six milestone incidents) is real. |

## Fixed in this pass (kind_robots#4755)

- **Connective prose rotates.** Eight seeded pools (travel, arrival, launch, return, clean
  sweep, detour, route memory, plot table), each at least as long as a voyage, so no
  connective line repeats inside one voyage. Repeated sentences within a voyage went from
  **34.4% to 16.2%**.
- **30 plain-success returns**, one per call, replace the shared sentence that was the
  single most-read result line.
- Casino and bar reactions rotate. The "(s)" plurals, "0 red uniforms" and the per-chapter
  "No pocket room is deployed." are fixed.
- **The ending reads in sections:** verdict, nemesis, captain, crew odysseys, worlds
  answered, found off the map, and fallen redshirts by name and system. The raw log is
  collapsed. Older saves fall back to the paragraph.
- A new `verifySpaceCouchReadability` regression keeps all of this from regressing.

## Still open (agent-owned unless marked)

1. **Seeded default route and reachable destination endings** (new task t-035). Pre-chart a
   seeded call for chapters 2–9 and re-pin the six test files that assume the first card. I
   tried this in this session: it works, but it breaks pinned traces in
   verifyGameOfCaptains, AuthoredExpansion, AuthoredRemainder, ActThreeOpening, Scarcity and
   Traces. Then audit why the six destination families are unreachable in practice.
2. Detour gambit and resolve lines are generic per approach. They should be written per
   crew and per stop, like the planetary dilemmas.
3. 95 of 101 aliens still lack causal action-by-mood outcomes (t-031).
4. Art delivery (t-008, t-009, t-033) and authenticated phone/tablet/desktop QA. The ending
   section block was checked only as a CSS mock at 390 and 1280 px.
5. **Silas:** final subjective acceptance (t-012) after the above. It stays a hard gate.
