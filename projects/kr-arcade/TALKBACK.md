# Arcade TALKBACK

## 2026-10-11 | Reviewer → Worker | kr-arcade/t-046 | critique

**Decision:** rejected kind_robots #3558 (pass 1); leave implementation PR open for repair.

**Failure category:** quality — lost persistent best times after New Wash.

**What was good:**
- Cabinet changes stay scoped to Sink Suds and its registry entry. Modes, shared bubble controls, medals and sumo have focused coverage.
- All 28 current-head check runs completed without failures. Independently ran npm run test:arcade-engine on d1cf592423e090bab4cf2622434698507a3a0c19: 14 cabinet suites passed, including the new Modes suite.

**What to improve:**
- A valid resumed room checkpoint (step 5) -> B New Wash -> Squeaky Clean -> finish updates times in memory, but game.save stays null. New Wash clears saveData; keepProgress invokes keep(), which returns outside campaign. Preserve or initialize a progress-only save and test reload with existing medals, best times and reached-room data.
- The Squeaky Clean regression begins with a step-0 save and misses the saved-checkpoint/New Wash path. Review comments carry the exact reproduction: https://github.com/silasfelinus/kind_robots/pull/3558#issuecomment-6115161917.
- Set the roadmap to review before opening the PR; it remained claimed during this review.

**Kaizen task:** deferred — no merge occurred; the repair is required by the existing t-046 save contract. Reuse worker/kr-arcade-t-046; no duplicate implementation or human gate.
