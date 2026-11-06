# Every Villain Tactics · TALKBACK

## 2026-10-31 PT · Worker · t-019 · PR #4566

**What landed:** Merged [Kind Robots PR #4566](https://github.com/silasfelinus/kind_robots/pull/4566) as `2c7258c` after 22/22 completed checks passed. Mission finishes now award deterministic points for objectives, rivals, rescues, evidence, extraction health and speed, with earned medals and a replay-safe scrapbook history. A visible debrief and a dedicated regression suite accompany the award logic.

**What I challenged:** The original scrapbook offered no numerical debrief, so battle completion never became a comparable outcome. Scoring is tied to the verified save state; re-saving an unchanged outcome does not mint points again. The first CI attempt caught an unused test import through the lint ratchet, which was fixed before the green merge.

**Remaining:** Do not call the task complete. Capture *damage taken during the battle*, distinct from health at extraction, before awarding a genuinely flawless medal. Add independently witnessed secret routes, heroes won with, villains defeated, and full run achievement provenance. Keep the roadmap t-019 `ready`.

**Kaizen:** Score the combat event ledger, not just the end-state snapshot, to prevent accidental false medals after healing.


## 2026-10-31 PT · Worker · t-019 damage provenance, PR #4568

**Shipped:** PR #4568 merged as `9d2ab94` after 18/18 completed checks passed. The tactical engine now counts historical squad HP loss from shots, overwatch, powered effects, telegraphed AoE, fire, electrified water and collapsing terrain. The earned *Untouched* medal requires a victorious, fully healthy squad with recorded zero damage. Legacy saves keep their validity but do not claim historical zero-damage achievements.

**Review finding:** An additional score line initially exceeded the earned-score validator's maximum. Dedicated scoring regression exposed it; the bound was increased without weakening points total and source validation. An unused import/format finding from earlier work was already closed before this pass.

**Remaining:** Task t-019 is `ready` for authored secrets and distinct hero/villain ledger achievements. A client checksum validates consistency, not cryptographic authenticity.

**Kaizen:** Couple future achievements to a compact event history so one turn's healer cannot counterfeit battle-level feats.

## 2026-11-06 | Worker → Reviewer | every-villain-tactics/t-007 | critique
type: critique

**Subject:** A finished battle must give the player a genuine onward action, and campaign progress must reflect playable content.

**Detail:**
- Kind Robots [PR #4855](https://github.com/silasfelinus/kind_robots/pull/4855) merged as `ea4c4c8` after all eight workflows completed successfully, including four contract shards. First Bell's old finish showed a long score sheet, dead combat controls, a duplicate victory log and six decorative chapter numbers, with only a replay action.
- The repair provides a full-area illustrated result, reachable One-Shot encounter selection, replay and menu; it removes fake campaign progress, makes directional cover/walls legible and reuses verified shipped portrait/scenery art.
- The six authored story chapters and bespoke top-down tactical environments remain undone. Generic venue illustrations must not be counted as final battle-map art.

**Suggested action:** Keep t-007 `ready` for genuine mission progression, reserve dedicated art queue work for designed top-down boards, and make next-playable-action plus correct terrain labelling a required human-playtest gate.
