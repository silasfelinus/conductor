# Emperor of Dust: balance report

*Originally generated for `emperor-of-dust/t-009` on 2026-10-20, updated 2026-10-22 from kind_robots
`utils/scripts/emperorFortressBalanceReport.ts` (the same simulation
`verifyEmperorFortressBalance.test.ts` holds in CI). Re-run it after content or
engine changes and paste the table between the markers.*

## How it plays

Each policy plays whole 50-day campaigns through the real engine. It takes on
every follower who offers, buying beds when it can afford them, and answers
every audience by its own rule. It staffs quests with the best-odds party when
the odds are 45% or better, except the reckless and idle policies.

- **Greedy** takes the first answer; **random** varies it; **spurn-all** avoids
  positive faction affinity, including the Mire Mothers.
- **Marshal** prioritizes the Day 47 Watch writ, the Day 49 Iron Peace and Gate
  Watch support, to verify the coercive path remains accessible.
- **Reckless** sends the smallest party anywhere, whatever the odds.
- **Idle** answers petitions against everyone and never sends a party.
- **Patron of X** always picks the choice that raises X most. Between equal
  choices it helps no other host, and it staffs X's quests first.

Patrons do not shop in the market, so their brass is a ceiling, not a floor.

## Findings and fixes (t-009)

| Finding | Fix |
|---|---|
| The Freehold barn won the hideout in nearly every run, whoever the crown courted. Chores and Act I dawn quests pushed the Freeholds to 100 affinity. | Chores pay 3 affinity, not 5–8. Five new chores cover the Storm Crows, Mire Mothers, Pack, Moles and Rustline, and a faction's chores wait for its banner. The hideout weighs **pledges** (story flags where the crown took a side) at 20 each on top of affinity. |
| The Rustline had almost nothing to win. | Two Act IV choices: the Day 31 Ford barricade and the Day 37 salvage market. Blue Lantern pays the Rustline on a plain success, and buying Jinx's crate counts as a pledge. |
| About 20 Ledger loans per run with a full barracks: taxes top out at 41 brass a day, and 12 followers at 6 cost 72. | Wage is 4 per follower. |
| A Hundred Candles (3 deaths) was unreachable with five lethal quests. | It now takes two deaths. The Well That Spoke and the Bell's Lost Clapper are lethal. |

## Notes for later
- **Iron Peace** now requires a deliberate, costly Day 47 Watch charter;
  support alone is not sufficient. The `marshal` simulation proves the
  ending remains available. Six peaces serve seven possible hideout hosts,
  and the Mire Mothers can influence the ending without hosting the court.
- **Faction wipe-outs** happen only to neglect (the idle policy, about one per
  run). The act-end war rules in SYSTEMS-V03.md, where a war's loser cedes a
  region, are not built yet.
- **t-028** still owes hideout income (the host's share) and followers leaving
  with Komodo. Act V brass will tighten when that lands, so re-run this report.

<!-- balance-report:start -->
40 fresh-onboarding campaigns per policy (seeds 1–40), each lasting 50 game days, verified with the real Kind Robots engine on 2026-10-22 in `verifyEmperorFortressAdversarial.test.ts`. Includes the new marshal policy and all eight ending families.

| Policy | Hideouts | Endings | Deaths / run | Runs losing 2+ | Loans / run | Factions wiped / run | Lowest final brass |
|---|---|---|---:|---:|---:|---:|---:|
| Takes the first answer (`greedy`) | freehold-barn 40 | Open Roads 38, A Hundred Candles 1, The Long Night 1 | 0.30 | 1 | 0.60 | 0.00 | 5 |
| Answers at random (`random`) | freehold-barn 23, bell-cellars 13, moving-caravan 3, mole-tunnels 1 | Open Roads 27, The Bell Restored 4, The Crow’s Bargain 2, The Long Night 2, Tunnels and Councils 2, The Witchwater Throne 2, Iron Peace 1 | 0.33 | 0 | 0.90 | 0.00 | 0 |
| Favours nobody (`spurn-all`) | freehold-barn 38, moving-caravan 2 | Open Roads 38, The Long Night 2 | 0.20 | 0 | 0.50 | 0.00 | 12 |
| Builds a Gate Watch mandate (`marshal`) | freehold-barn 39, bell-cellars 1 | Iron Peace 35, The Long Night 5 | 0.23 | 1 | 1.52 | 0.00 | 5 |
| Sends anyone, anywhere (`reckless`) | freehold-barn 39, bell-cellars 1 | Open Roads 29, The Long Night 9, A Hundred Candles 2 | 0.50 | 3 | 3.00 | 0.00 | 5 |
| Never sends a party (`idle`) | nameless-cave 40 | The Long Night 40 | 0.00 | 0 | 8.45 | 1.00 | 1 |
| Patron of moles (`patron:moles`) | mole-tunnels 40 | Tunnels and Councils 39, A Hundred Candles 1 | 0.35 | 1 | 0.38 | 0.00 | 27 |
| Patron of storm-crows (`patron:storm-crows`) | crow-cave 36, freehold-barn 4 | The Crow’s Bargain 38, A Hundred Candles 1, The Long Night 1 | 0.38 | 1 | 0.17 | 0.00 | 9 |
| Patron of hollow-bell (`patron:hollow-bell`) | bell-cellars 40 | The Bell Restored 22, Open Roads 17, The Long Night 1 | 0.35 | 0 | 0.30 | 0.00 | 3 |
| Patron of jackalwire (`patron:jackalwire`) | wagon-circle 39, freehold-barn 1 | Open Roads 39, A Hundred Candles 1 | 0.28 | 1 | 0.38 | 0.00 | 0 |
| Patron of saltroad (`patron:saltroad`) | moving-caravan 40 | Open Roads 40 | 0.30 | 0 | 0.70 | 0.00 | 12 |
| Patron of freeholds (`patron:freeholds`) | freehold-barn 40 | Open Roads 39, The Long Night 1 | 0.40 | 0 | 0.45 | 0.00 | 38 |
| Patron of rustline (`patron:rustline`) | rail-station 36, freehold-barn 4 | Open Roads 39, The Long Night 1 | 0.38 | 0 | 0.75 | 0.00 | 1 |
| Patron of mire-mothers (`patron:mire-mothers`) | freehold-barn 40 | The Witchwater Throne 35, Open Roads 4, The Long Night 1 | 0.38 | 0 | 0.33 | 0.00 | 10 |

### Iron Peace correction (t-055; 2026-10-22)

- Previously a passive Gate Watch support threshold gave the politically nonaligned `spurn-all` ruler **38/40 Iron Peace** endings. Iron Peace now requires a signed Day 47 Watch writ *and* adequate Watch support on Day 49. Signing the writ funds road checkpoints and detention powers at the expense of Yard provisions and Freehold, Mole and Saltroad support. Declining leaves civilian charters intact.
- Re-ran **592 full campaigns, 29,600 game days**, including 1,632 individually checked dawn states; **all eight** ending families remain reachable. The `spurn-all` ruler now earns **38/40 Open Roads, 0/40 Iron Peace, and 0/40 Witchwater**. The purpose-built `marshal` policy earns **35/40 Iron Peace**, keeping it playable.
- A second simulation defect was exposed and fixed: `spurn-all` counted gains for seven potential hideout hosts but excluded the non-host Mire Mothers, accidentally favoring their Witchwater ending in 21/40 initial follow-up simulations. It now scores all political factions, independently of hideout eligibility. No game-world faction affinity numbers were changed to hide the problem.
- The 240 seeded openings and 480 rival-choice branches remain valid, with at most 2 quests on Day 1. The original onboarding/rewind regression suite continues to run in scheduled CI.
- Across the 560 base policy campaigns: 174 follower deaths, 8 campaigns with two or more lost followers, 737 loans, and 40 faction wipe-outs (all within the deliberate idle strategy).

Verification: GitHub Actions `Emperor of Dust Dispatch Contract` for Kind Robots commit `5342961774ed8389827e7f4f6d2316a28ca065ce`, run `39862753999`.
<!-- balance-report:end -->
