# Ecotone Mysteries — playtest record (t-063)

**Ask, 2026-10-23 PT (Silas):** "playtest mystery interactions, and the originality and 'funness' of the experiences,
pass or fail."

## Method
- **Engine playthroughs:** `utils/scripts/ecotoneMysteryTranscript.ts` plays each case through the real engine: every
  path to every Real Ending (rotating routes and lead companion), a true cold case, a walk-away at Gate I, and every
  Gate III failure paired with the missed-trap reveal.
- **Blind grading:** independent reviewers who saw only the transcripts and the source (never the author's view) graded
  each case PASS/FAIL on **Originality**, **Fun**, **Interactions** (continuity across pass/fail paths, companions,
  digressions) and **Guardrails**. A case passes only if Originality and Fun pass with no serious interaction bug.
  A separate reviewer audited the whole set for repetition. Every round used fresh reviewers.
- **Mechanical playtest:** scripted clicks through the real UI in Chromium (local dev build) and the contract test
  `npm run test:ecotone-mysteries`.

## Results by round

| Case | Round 1 | Round 2 | Round 3 | Final |
| --- | --- | --- | --- | --- |
| I Ridge Ram | FAIL | FAIL (interactions) | PASS | **PASS** |
| II Stubborn Herd | FAIL | PASS | PASS | **PASS** |
| III Second Voice | FAIL | FAIL (originality, interactions) | FAIL (originality) | **PASS** (verified) |
| IV Crab Pot Ghost | FAIL | PASS | PASS | **PASS** |
| V Midnight Mane | FAIL | FAIL (originality, interactions) | PASS | **PASS** |
| VI Virgin Sacrifice | FAIL | PASS | PASS | **PASS** |
| VII Graveyard Gavel | FAIL | PASS | PASS + required fixes | **PASS** (verified) |
| VIII Murder Mountain | FAIL | conditional | PASS + required fixes | **PASS** (verified; tact on the nickname passed every round) |
| IX Wandering Arrows | FAIL | PASS | PASS | **PASS** |
| X Sea-Goat | FAIL | PASS | PASS | **PASS** |
| XI Dated Jugs | FAIL | PASS | FAIL (one recall line) | **PASS** (verified; originality borderline) |
| XII Two-Tailed Mermaid | FAIL | PASS | PASS | **PASS** (sensitivity check passed) |

| Set axis | Round 1 | Round 2 | Round 3 | Final |
| --- | --- | --- | --- | --- |
| Originality across runs | FAIL | FAIL | FAIL (narrow) | **PASS** |
| Culprit and motive variety | FAIL | FAIL | PASS | **PASS** (skew noted) |
| Mechanics variety | FAIL | FAIL | FAIL (narrow) | **PASS** |
| Companion voices | FAIL | PASS (narrow) | PASS (narrow) | **PASS** |

"Final" is a fresh verifier's full re-grade of the cases that failed or carried required fixes in round 3 (III, VII,
VIII, XI), a sensitivity check on XII, and a set re-grade, after a precision polish pass on all twelve.

## What the playtest found, and what changed
- **Interactions (every case, round 1):** reveals assumed the Gate III trap had worked even when it failed; later
  scenes assumed facts only one approach uncovered; messages named weekdays that vary by route. → New `afterMiss`
  reveals, approach memory and `recall` lines, a validator that enforces them, and transcripts that show every miss.
- **The set was one story twelve times (round 1):** a kind retiree in a costume, a grief speech, a glimpse of the
  future, a co-op montage, a keepsake in the mail. → Distinct culprits (five now in the wrong, three under 30),
  motives (pride, romance, ambition, a con, escape, freedom, duty), uncanny devices (four past, four future, four
  other), and ending shapes (several true endings stay on the night itself).
- **Companions had drifted from their bios:** Cedar had no cosmic jokes, Juniper had stopped teasing. → Restored.
- **Sensitivity (XII):** a performer presumed drowned. Coral now says plainly she chose to live; her recovery took a
  year, a crisis line and a counselor; Nadia asks her to call next time and she promises. Nothing romanticizes the sea.
- **Guardrails:** no sign named in the text (the "Aquarian Ranch" was renamed); the Trinidad pier sale rumor removed;
  Virgin Sacrifice moved to an invented parcel with no real landowner implied; no Native material; Murder Mountain
  invents no real crime, victim or property.

## Mechanical playtest (browser and contract)
- Two scripted full runs on the final text: one true path through a missed Gate III (afterMiss) to the Real Ending
  "Coffee for Ten", one cold case. Digression bubble on every gate, Real Ending framing, end-screen case summary, Case
  Files ledger correct, zero page errors.
- `npm run test:ecotone-mysteries`: gate timing on all three routes, decline, true path vs cold case, every Real Ending
  reachable in seeded play, missed-trap reveals exercised, approach flags and recall keys, Playbook nodes and links,
  live edits reaching mystery cards, ledger merge/sanitize, old saves.

## Still open (not blocking)
- Culprit skew: the person under the mask is a woman in 11 of 12 cases. A run draws one case, so it reads fine per
  run, but a future pass could vary it.
- Dated Jugs' land-grab villain is the most classic Scooby shape in the set; it passes on its twist (her free
  warnings became his buy list).
- The pun title "The Mystery of the Murder of Crows" was suggested for Case VIII; the title stays "Murder Mountain" per
  the owner's brief unless Silas prefers the pun.
- Silas's own editorial read; balance of the true-path rate after real play.

Review files live in the session scratchpad (not committed); this record is the durable summary.
