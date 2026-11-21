# Cthulhuquarium — release-candidate dossier (t-096)

2026-11-21. The first human playtest of the descent: five floors, bought keys,
visual-novel scenes with replies, the Memory Book and three endings. This page
gathers the evidence, the three independent reviews and what was done about
them. The playtest itself is [PLAYTEST-CHECKLIST.md](PLAYTEST-CHECKLIST.md).

## What ships

| Repo | PR | What |
|---|---|---|
| kind_robots | #5472, #5479 | The descent: floors, scenes, replies, Memory Book, Hatchery |
| kind_robots | #5497 | Canon-rarity economy and floor keys (t-105) |
| kind_robots | #5498 | Settings, title card, endings shelf, coverage report (t-100, t-092) |
| kind_robots | #5499 | t-084 step 1: breeding/egg/stat fields out of the Prisma client |
| kind_robots | #5500 | Cross-device QA fixes; editorial pass and 15 Wilbur floor portraits |
| kind_robots | RC fixes PR | Review fixes below; last 5 portraits; second editorial pass |
| canon | #82–#89 | Scenes, plates, editorial passes, Wilbur's 20 floor portraits, art ledger |
| conductor | #7702, #7717, #7735 | Ledgers, simulators, suites, audits, this dossier |

## Evidence

- **Economy:** [ECONOMY-SUITE.md](ECONOMY-SUITE.md).
  - Nine play strategies over the real roster.
  - 26 adversarial API checks, all passing, including concurrency: ten parallel ticks settle once, parallel buys can't overdraw or overfill, a double-tapped finale charges once, and a new tank is never given free keys.
  - The floor-key play-through passes 15 of 15.
- **Cross-device QA:** [qa/acceptance.mjs](qa/acceptance.mjs) and the screenshot sheet.
  - Six viewports, plus reduced motion with every portrait missing.
  - Covers the title card, every room, buying a key into its scene and choosing a reply, settings, the Memory Book and its endings, keyboard play and focus, and no outer scroll.
- **Writing:** [coverage/](coverage/) holds the machine-readable report (every scene, bark pool and background is reachable) and the editorial verdict.
- **Art:** canon `art/LEDGER.md` (`scripts/art_ledger.py`) tracks every required render from prompt to its place in the game.
- **Standard:** [STANDARD-AUDIT-2026-11-21.md](STANDARD-AUDIT-2026-11-21.md). Every item is Met except characters, which is your call.

## The three independent reviews

Each reviewer was given only the code, the canon and the evidence, not my
conclusions.

### Technical and economy: "close; fix two first"
| Finding | Done |
|---|---|
| Parallel ticks paid the same absence two or more times, so two open tabs doubled offline income | **Fixed.** Every money-moving write takes a tank row lock. A tick whose snapshot went stale settles nothing |
| The grandfather cutoff (22 Nov) would hand playtesters free keys | **Fixed.** A per-tank marker replaces it: the first time the key system sees a tank, it grants the floors that tank's count had already opened. New tanks get the marker at birth |
| Parallel species buys overdrew coins and overfilled the tank, and could log a milestone twice | **Fixed.** Coins and room are re-checked under the lock |
| Sets, decor, feed and finale had unguarded check-then-spend | **Fixed.** Same lock. A double-tapped finale now charges once |
| The shop rotation isn't enforced on purchase | Left as is (low; a known species can always be re-ordered) |
| The leaderboard returns `userId`; tank creation isn't race-safe | Follow-up |

### Experience and narrative: "conditionally ready"
| Finding | Done |
|---|---|
| Glass winks: "it tapped back", "trying to get out", "kept count", the outside face of the glass, visitors kept on an island, "never stops watching" | **Fixed** in canon #88 |
| Wilbur as the joke: "he always comes back up", and the startle bark shown with his wince portrait | **Fixed:** the line is rewritten and the startle pool uses `explaining` |
| Floor scenes treated keys as gifts | **Fixed:** floor III acknowledges the sale, floor IV gets a cut copy of her mother's key, and the floor V key is no longer "opens nothing" |
| "Portsmouth · After closing" eyebrow; the locked ending hint "the most expensive thing in the shop" | **Fixed** (kind_robots RC PR) |
| A 30-minute playtest only reaches floors I–II | **Playtest instruction** (below) |
| The weirdness curve jumps at floor II and then flattens; three fish names collide with place names | Follow-up, needs your design eye |
| The intro switches between sheet and full screen five times | Follow-up |

### Front end and accessibility: "not ready unsupervised; a moderated session is fine"
| Finding | Done |
|---|---|
| A "Store Error" toast for an achievement missing from the catalog | Local only. Production has all 19 Cthulhuquarium achievements seeded, which I checked |
| Saved settings applied only if the story API answered | **Fixed:** settings load first, on mount |
| Scenes didn't take focus, and Space on a background button could skip a scene | **Fixed:** the scene focuses Continue on open, restores focus on close, and only stage buttons can claim Space/Enter |
| The in-game Motion setting was ignored in scenes | **Fixed:** it is reactive, and stage animations stop |
| Endings titles overflowed at 390px | **Fixed:** the grid wraps |
| The reveal, welcome-back and finale dialogs don't take focus or close on Esc; reply cards announce as list items; no load-failure retry | Follow-ups |
| 320px HUD; short landscape phones | Follow-up (the suite now covers 390px and up only) |

## How to run the playtest

1. **Wait for the deploy.** Force-update once kind_robots main includes the RC fixes PR. Then check that `/api/version` shows it.
2. **A fresh account for the first 20 minutes**, on a phone. This covers the intro, the first purchases, buying the key and Below Stairs.
3. **Then a seeded tank, to see the deep story.** A 30-minute session never reaches floors III–V, so either:
   - play your own veteran tank: its floors are kept, and each visit plays one missed floor scene; or
   - watch the floor scenes in order from the Memory Book, under World & story.
4. **Use the checklist.** Write a verdict per item in [PLAYTEST-CHECKLIST.md](PLAYTEST-CHECKLIST.md). The pacing question (the long save before the floor V key) and "is Wilbur's escalation sympathetic" matter most.

## Not done here, on purpose

- **t-084 step 2**, the irreversible column drop. Merge it only once `/api/version` shows a build containing #5499.
- **Graduating the project to `playtest` status.** `playtest_readiness.py` decides that, after the merges and the roadmap close-out.
